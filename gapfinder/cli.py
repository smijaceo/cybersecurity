"""Command line: python -m gapfinder {collect,stats,export}."""

from __future__ import annotations

import argparse
from datetime import date
import json
import logging
import sys
from pathlib import Path

import yaml

from . import relevance, review
from .collectors import COLLECTORS
from .store import Store

ROOT = Path(__file__).resolve().parent.parent
DEFAULT_CONFIG = ROOT / "config" / "segments.yaml"
DEFAULT_DB = ROOT / "data" / "signals.db"
DEFAULT_SCORING = ROOT / "config" / "scoring.yaml"
DEFAULT_PHASE2 = ROOT / "reports" / "phase2"

# Query style per source, chosen from measured result quality (see docs/ROADMAP.md, P1):
# - github: pain phrase + term, both quoted. GitHub honours exact phrases, and
#   combining them finds feature requests about the term.
# - hn: the quoted term only. Algolia returns almost nothing for two quoted phrases.
# - stackexchange: the bare term, matched against question titles by the collector.
#   Full-text search there matches loose words ("secrets" -> Messenger "Secret
#   Conversations"); title match is precise but low volume. ~300 requests/day quota.
# Separating real need statements from general discussion is the Phase 2 relevance filter.
PHRASE_SOURCES = {"github"}
QUOTED_TERM_SOURCES = {"hn", "ted"}   # ted: FT~("term") within security procurement codes

log = logging.getLogger("gapfinder")


def load_config(path: Path) -> dict:
    with open(path) as f:
        return yaml.safe_load(f)


def build_queries(config: dict, segment: str, source: str) -> list[str]:
    seg = config["segments"][segment]
    if source in seg.get("queries", {}):  # explicit per-source queries (e.g. open discovery)
        return list(seg["queries"][source])
    if seg.get("queries") and not seg.get("terms"):
        return []  # query-only segment that doesn't cover this source
    terms = seg.get("terms", [])
    if source in QUOTED_TERM_SOURCES:
        return [f'"{t}"' for t in terms]
    if source not in PHRASE_SOURCES:
        return list(terms)
    # Quote both parts so search engines match them as exact phrases, not loose words.
    return [f'"{p}" "{t}"' for t in terms for p in config.get("pain_phrases", [])]


def cmd_collect(args) -> int:
    config = load_config(args.config)
    segments = args.segment or list(config["segments"])
    unknown = set(segments) - set(config["segments"])
    if unknown:
        log.error("unknown segment(s): %s", ", ".join(sorted(unknown)))
        return 2
    store = Store(args.db)
    if args.fresh:
        for segment in segments:
            print(f"removed {store.delete_segment(segment)} old signals from {segment}")
    total = 0
    for source in args.source:
        try:
            collector = COLLECTORS[source](before=args.before)
        except ValueError as exc:  # e.g. a live job board asked for history
            log.warning("skipping %s: %s", source, exc)
            continue
        for segment in segments:
            for query in build_queries(config, segment, source):
                try:
                    n = store.upsert(collector.collect(segment, query, args.limit))
                except Exception as exc:  # keep going; one bad query shouldn't stop a run
                    log.warning("%s %s %r failed: %s", source, segment, query, exc)
                    continue
                total += n
                log.info("%-13s %-20s %-45s %3d", source, segment, query[:45], n)
    store.close()
    print(f"collected {total} signals into {args.db}")
    return 0


def cmd_stats(args) -> int:
    store = Store(args.db)
    rows = store.stats()
    if not rows:
        print("no signals yet; run: python -m gapfinder collect")
        return 0
    print(f"{'segment':22} {'source':14} {'signals':>8} {'engagement':>11}")
    for r in rows:
        print(f"{r['segment']:22} {r['source']:14} {r['n']:>8} {r['engagement'] or 0:>11}")
    return 0


def cmd_export(args) -> int:
    store = Store(args.db)
    out = open(args.out, "w") if args.out else sys.stdout
    n = 0
    try:
        for sig in store.iter_signals(args.segment, args.min_engagement):
            out.write(json.dumps(sig) + "\n")
            n += 1
    except BrokenPipeError:  # e.g. piped into `head`
        sys.stderr.close()
        return 0
    if args.out:
        out.close()
        print(f"exported {n} signals to {args.out}", file=sys.stderr)
    return 0


def cmd_sample(args) -> int:
    config = load_config(args.config)
    store = Store(args.db)
    sample = review.build_sample(store, config, args.per_segment, args.per_source_cap)
    Path(args.out).parent.mkdir(parents=True, exist_ok=True)
    Path(args.out).write_text(json.dumps(sample, indent=1))
    print(f"wrote {len(sample)} signals to {args.out}")
    return 0


def cmd_evaluate(args) -> int:
    sample = json.loads(Path(args.sample).read_text())
    try:
        labels = review.load_labels(args.labels, sample)
    except review.LabelError as exc:
        log.error("invalid labels: %s", exc)
        return 2
    results = review.evaluate(sample, labels, args.threshold)
    for r in results:
        print(f"{r.segment:22} on-segment {r.on_segment:>3}/{r.total} ({r.on_segment_rate:.0%})"
              f"  need {r.need:>3}  {'pass' if r.passed else 'FAIL'}")
    if args.report:
        Path(args.report).write_text(review.render_report(sample, labels, results, args.title))
        print(f"report: {args.report}")
    return 0 if all(r.passed for r in results) else 1


def cmd_judge_prepare(args) -> int:
    config = load_config(args.config)
    store = Store(args.db)
    dropped, kept = relevance.apply_rules(store)
    print(f"rules dropped {dropped} signals; {kept} left for the judge")
    paths = relevance.export_batches(store, config, args.out_dir, args.batch_size)
    for p in paths:
        print(f"  {p}")
    return 0


def cmd_judge_import(args) -> int:
    store = Store(args.db)
    try:
        n = relevance.import_labels(store, args.batch, args.labels)
    except review.LabelError as exc:
        log.error("rejected %s: %s", args.labels, exc)
        return 2
    print(f"stored {n} judgments from {args.labels}")
    return 0


def cmd_judge_stats(args) -> int:
    store = Store(args.db)
    print(f"{'segment':22} {'total':>6} {'judged':>7} {'rules':>6} {'on-seg':>7} {'need':>5}")
    for r in store.judgment_stats():
        print(f"{r['segment']:22} {r['total']:>6} {r['judged']:>7} {r['dropped_by_rules'] or 0:>6}"
              f" {r['on_segment'] or 0:>7} {r['need'] or 0:>5}")
    return 0


def cmd_themes(args) -> int:
    from . import analysis

    store = Store(args.db)
    result = analysis.build_themes(store, args.out_dir)
    for t in result["themes"]:
        print(f"theme {t['theme_id']:>2}  {len(t['signal_ids']):>3} statements  "
              f"stability {t['stability']:.2f}  {', '.join(t['keywords'][:5])}")
    print(f"{len(result['themes'])} themes, {len(result['outliers'])} outliers -> "
          f"{args.out_dir}/themes.json; namer input: {args.out_dir}/theme-naming-input.json")
    return 0


def _load_theme_names(args):
    from . import analysis

    theme_data = json.loads((args.out_dir / "themes.json").read_text())
    names = analysis.load_names(args.out_dir / "theme-names.jsonl",
                                {t["theme_id"] for t in theme_data["themes"]})
    return theme_data, names


def cmd_threat_prepare(args) -> int:
    from . import analysis

    try:
        theme_data, names = _load_theme_names(args)
    except (ValueError, FileNotFoundError) as exc:
        log.error("theme names: %s", exc)
        return 2
    items = analysis.build_threat_input(theme_data["themes"], names, load_config(args.config),
                                        load_config(args.scoring), args.out_dir)
    print(f"{len(items)} coherent themes -> {args.out_dir}/threat-mapping-input.json")
    return 0


def cmd_market_prepare(args) -> int:
    from . import analysis

    try:
        theme_data, names = _load_theme_names(args)
    except (ValueError, FileNotFoundError) as exc:
        log.error("theme names: %s", exc)
        return 2
    items = analysis.build_market_input(theme_data["themes"], names, Store(args.db), args.out_dir)
    for i in items:
        print(f"theme {i['theme_id']:>2}  {i['name']}  "
              f"({len(i['price_or_vendor_statements'])} price/vendor statements)")
    print(f"-> {args.out_dir}/market-research-input.json")
    return 0


def cmd_market_merge(args) -> int:
    from . import analysis

    market_input = json.loads((args.out_dir / "market-research-input.json").read_text())
    try:
        n = analysis.merge_market_parts(args.out_dir / "market-research-parts", market_input,
                                        args.out_dir / "market-research.jsonl")
    except ValueError as exc:
        log.error("market research: %s", exc)
        return 2
    print(f"merged {n} themes -> {args.out_dir}/market-research.jsonl")
    return 0


def cmd_gaps(args) -> int:
    from datetime import date

    from . import analysis, gaps

    config, scoring = load_config(args.config), load_config(args.scoring)
    store = Store(args.db)
    try:
        theme_data, names = _load_theme_names(args)
        threat_input = json.loads((args.out_dir / "threat-mapping-input.json").read_text())
        threat = analysis.load_threat(args.out_dir / "threat-mapping.jsonl", threat_input)
        market_input = json.loads((args.out_dir / "market-research-input.json").read_text())
        market = analysis.load_market(args.out_dir / "market-research.jsonl", market_input)
    except (ValueError, FileNotFoundError) as exc:
        log.error("agent output: %s", exc)
        return 2
    feats = analysis.theme_features(theme_data["themes"], names, threat, market, store, config,
                                    scoring)
    ranked = gaps.score(feats, scoring["weights"])
    excluded = [{**t, "reason": names[t["theme_id"]].get("reason", "")}
                for t in theme_data["themes"] if names[t["theme_id"]]["coherent"] != "y"]
    meta = {**theme_data, "generated": date.today().isoformat(),
            "signals_total": sum(r["n"] for r in store.stats()),
            "themes_total": len(theme_data["themes"]),
            "fact_check_path": str(args.out_dir / "fact-check.json")}
    (args.out_dir / "gaps.json").write_text(json.dumps(ranked, indent=1))
    report = args.out_dir.parent / f"gaps-{meta['generated']}.md"
    report.write_text(analysis.render_report(ranked, excluded, meta, scoring))
    for i, t in enumerate(ranked, 1):
        print(f"{i:>2}. {t['gap_score']:.3f}  {t['name']}  ({t['demand']['need_signals']} statements,"
              f" stability {t['stability']}, crowded {t['supply']['crowdedness']}/3,"
              f" WTP {t['monetization']['willingness_to_pay']}/3) {t['scores']}")
    print(f"report: {report}")
    return 0


def cmd_concept_prepare(args) -> int:
    from . import concepts

    shortlist = load_config(args.shortlist)
    try:
        paths = concepts.build_inputs(shortlist, DEFAULT_PHASE2, Store(args.db), args.ideas_dir)
    except (ValueError, FileNotFoundError) as exc:
        log.error("concept-prepare: %s", exc)
        return 2
    for p in paths:
        print(p)
    return 0


def cmd_concept_render(args) -> int:
    from . import concepts

    results = concepts.render_all(args.ideas_dir, args.only)
    ok = True
    for oid, problems in results:
        if problems:
            ok = False
            print(f"{oid}: {len(problems)} problem(s)")
            for p in problems:
                print(f"  - {p}")
        else:
            print(f"{oid}: ok")
    return 0 if ok and results else 1


def cmd_critique_check(args) -> int:
    from . import panel

    try:
        c = panel.load_critique(args.path)
    except (ValueError, FileNotFoundError) as exc:
        log.error("%s", exc)
        return 2
    print(f"ok: {c.concept_id} {c.lens} round {c.round} score {c.score} {c.verdict}")
    return 0


def cmd_panel(args) -> int:
    from . import panel

    cfg = load_config(args.scoring)["panel"]
    try:
        results = panel.run(args.ideas_dir, cfg, args.report)
    except (ValueError, FileNotFoundError) as exc:
        log.error("panel: %s", exc)
        return 2
    for i, r in enumerate(results, 1):
        print(f"{i}. {r['decision']:<11} mean {r['mean']:<5} (r1 {r['round1_mean']}) "
              f"min {r['min']}  {r['name']}")
    print(f"report: {args.report}")
    return 0 if results else 1


def cmd_import_regulations(args) -> int:
    import hashlib

    from . import schemas
    from .models import Signal

    config = load_config(args.config)
    try:
        rows = schemas.load_jsonl(args.path, schemas.RegulationSignal)
    except schemas.SchemaError as exc:
        log.error("%s", exc)
        return 2
    bad = sorted({r.segment for r in rows} - set(config["segments"]))
    if bad:
        log.error("unknown segment(s): %s", ", ".join(bad))
        return 2
    sigs = [Signal(
        source="regulation",
        native_id=hashlib.sha1(f"{r.regulation}|{r.article}|{r.obligation}".encode()).hexdigest()[:16],
        segment=r.segment, query="regulation-scout",
        title=f"{r.regulation}: {r.obligation}"[:300],
        body=f"{r.obligation} Applies to: {r.applies_to}. Jurisdiction: {r.jurisdiction}. "
             f"Effective {r.effective}. {r.article}".strip(),
        url=r.source, created_at=r.effective, engagement=1,
        metadata={"regulation": r.regulation, "jurisdiction": r.jurisdiction,
                  "applies_to": r.applies_to, "article": r.article}) for r in rows]
    n = Store(args.db).upsert(sigs)
    print(f"imported {n} regulatory obligations from {args.path}")
    return 0


def cmd_fetch(args) -> int:
    from .fetch import fetch_text

    try:
        print(fetch_text(args.url, render=args.render))
    except Exception as exc:
        log.error("fetch failed: %s", exc)
        return 1
    return 0


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(prog="gapfinder", description=__doc__)
    p.add_argument("--db", type=Path, default=DEFAULT_DB)
    p.add_argument("--config", type=Path, default=DEFAULT_CONFIG)
    p.add_argument("-v", "--verbose", action="store_true")
    sub = p.add_subparsers(dest="cmd", required=True)

    c = sub.add_parser("collect", help="fetch demand signals from sources")
    c.add_argument("--segment", action="append", help="segment key (repeatable; default all)")
    c.add_argument("--source", action="append", choices=sorted(COLLECTORS),
                   help="source (repeatable; default all)")
    c.add_argument("--limit", type=int, default=30, help="max results per query")
    c.add_argument("--before", type=date.fromisoformat,
                   help="only items created before YYYY-MM-DD (backtest, D18)")
    c.add_argument("--fresh", action="store_true",
                   help="delete the segments' existing signals first (after changing search terms)")
    c.set_defaults(func=cmd_collect)

    s = sub.add_parser("stats", help="signal counts per segment and source")
    s.set_defaults(func=cmd_stats)

    e = sub.add_parser("export", help="dump signals as JSON lines for analysis")
    e.add_argument("--segment")
    e.add_argument("--min-engagement", type=int, default=None)
    e.add_argument("--out", help="file path (default stdout)")
    e.set_defaults(func=cmd_export)

    sm = sub.add_parser("sample", help="pick top signals per segment for the relevance judge")
    sm.add_argument("--out", required=True)
    sm.add_argument("--per-segment", type=int, default=20)
    sm.add_argument("--per-source-cap", type=int, default=10)
    sm.set_defaults(func=cmd_sample)

    ev = sub.add_parser("evaluate", help="score judge labels; exit 1 if any segment fails")
    ev.add_argument("--sample", required=True)
    ev.add_argument("--labels", required=True)
    ev.add_argument("--threshold", type=float, default=0.5)
    ev.add_argument("--report", help="write a markdown report here")
    ev.add_argument("--title", default="Signal quality review")
    ev.set_defaults(func=cmd_evaluate)

    jp = sub.add_parser("judge-prepare",
                        help="apply rule filter, write unjudged signals as judge batches")
    jp.add_argument("--out-dir", required=True)
    jp.add_argument("--batch-size", type=int, default=150)
    jp.set_defaults(func=cmd_judge_prepare)

    ji = sub.add_parser("judge-import", help="validate and store a judge's labels for one batch")
    ji.add_argument("--batch", required=True)
    ji.add_argument("--labels", required=True)
    ji.set_defaults(func=cmd_judge_import)

    js = sub.add_parser("judge-stats", help="judgment counts per segment")
    js.set_defaults(func=cmd_judge_stats)

    th = sub.add_parser("themes", help="cluster need statements into themes (BERTopic)")
    th.add_argument("--out-dir", type=Path, default=DEFAULT_PHASE2)
    th.set_defaults(func=cmd_themes)

    tp = sub.add_parser("threat-prepare", help="shortlist ATT&CK candidates for the threat mapper")
    tp.add_argument("--out-dir", type=Path, default=DEFAULT_PHASE2)
    tp.add_argument("--scoring", type=Path, default=DEFAULT_SCORING)
    tp.set_defaults(func=cmd_threat_prepare)

    mp = sub.add_parser("market-prepare", help="input for the paid-market researcher agents")
    mp.add_argument("--out-dir", type=Path, default=DEFAULT_PHASE2)
    mp.set_defaults(func=cmd_market_prepare)

    mm = sub.add_parser("market-merge", help="validate and combine market research part files")
    mm.add_argument("--out-dir", type=Path, default=DEFAULT_PHASE2)
    mm.set_defaults(func=cmd_market_merge)

    gp = sub.add_parser("gaps", help="score named themes and write the gap report")
    gp.add_argument("--out-dir", type=Path, default=DEFAULT_PHASE2)
    gp.add_argument("--scoring", type=Path, default=DEFAULT_SCORING)
    gp.set_defaults(func=cmd_gaps)

    cp = sub.add_parser("concept-prepare", help="Phase 3: write concept-writer inputs per opening")
    cp.add_argument("--shortlist", type=Path, default=ROOT / "config" / "shortlist.yaml")
    cp.add_argument("--ideas-dir", type=Path, default=ROOT / "ideas")
    cp.set_defaults(func=cmd_concept_prepare)

    cr = sub.add_parser("concept-render", help="Phase 3: validate concepts and write ideas/<slug>.md")
    cr.add_argument("--ideas-dir", type=Path, default=ROOT / "ideas")
    cr.add_argument("--only", help="validate/render just this opening id")
    cr.set_defaults(func=cmd_concept_render)

    cc = sub.add_parser("critique-check", help="Phase 4: validate one critique file")
    cc.add_argument("path", type=Path)
    cc.set_defaults(func=cmd_critique_check)

    pn = sub.add_parser("panel", help="Phase 4: decide go/no-go, write critique and panel reports")
    pn.add_argument("--ideas-dir", type=Path, default=ROOT / "ideas")
    pn.add_argument("--scoring", type=Path, default=DEFAULT_SCORING)
    pn.add_argument("--report", type=Path, default=ROOT / "reports" / "phase4" / "panel.md")
    pn.set_defaults(func=cmd_panel)

    ir = sub.add_parser("import-regulations",
                        help="validate and import the regulation scout's obligations as signals")
    ir.add_argument("path", type=Path)
    ir.set_defaults(func=cmd_import_regulations)

    fp = sub.add_parser("fetch", help="print a web page's main text (for agents)")
    fp.add_argument("url")
    fp.add_argument("--render", action="store_true", help="render JavaScript with Chromium")
    fp.set_defaults(func=cmd_fetch)

    args = p.parse_args(argv)
    if getattr(args, "source", None) is None and args.cmd == "collect":
        args.source = sorted(COLLECTORS)
    logging.basicConfig(level=logging.INFO if args.verbose else logging.WARNING,
                        format="%(message)s")
    return args.func(args)
