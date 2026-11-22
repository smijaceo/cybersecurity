"""Command line: python -m gapfinder {collect,stats,export}."""

from __future__ import annotations

import argparse
import json
import logging
import sys
from pathlib import Path

import yaml

from . import review
from .collectors import COLLECTORS
from .store import Store

ROOT = Path(__file__).resolve().parent.parent
DEFAULT_CONFIG = ROOT / "config" / "segments.yaml"
DEFAULT_DB = ROOT / "data" / "signals.db"

# Query style per source, chosen from measured result quality (see docs/ROADMAP.md, P1):
# - github: pain phrase + term, both quoted. GitHub honours exact phrases, and
#   combining them finds feature requests about the term.
# - hn: the quoted term only. Algolia returns almost nothing for two quoted phrases.
# - stackexchange: the bare term, matched against question titles by the collector.
#   Full-text search there matches loose words ("secrets" -> Messenger "Secret
#   Conversations"); title match is precise but low volume. ~300 requests/day quota.
# Separating real need statements from general discussion is the Phase 2 relevance filter.
PHRASE_SOURCES = {"github"}
QUOTED_TERM_SOURCES = {"hn"}

log = logging.getLogger("gapfinder")


def load_config(path: Path) -> dict:
    with open(path) as f:
        return yaml.safe_load(f)


def build_queries(config: dict, segment: str, source: str) -> list[str]:
    terms = config["segments"][segment]["terms"]
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
        collector = COLLECTORS[source]()
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
    c.add_argument("--fresh", action="store_true",
                   help="delete the segments' existing signals first (after changing search terms)")
    c.set_defaults(func=cmd_collect)

    s = sub.add_parser("stats", help="signal counts per segment and source")
    s.set_defaults(func=cmd_stats)

    e = sub.add_parser("export", help="dump signals as JSON lines for analysis")
    e.add_argument("--segment")
    e.add_argument("--min-engagement", type=int, default=0)
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

    args = p.parse_args(argv)
    if getattr(args, "source", None) is None and args.cmd == "collect":
        args.source = sorted(COLLECTORS)
    logging.basicConfig(level=logging.INFO if args.verbose else logging.WARNING,
                        format="%(message)s")
    return args.func(args)
