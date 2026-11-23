"""Phase 2 pipeline: themes -> (theme namer agent) -> supply/threat/demand -> gap report.

Steps
1. `gapfinder themes`  : cluster need statements, write themes.json and the namer's input.
2. Theme namer (Claude Code subagent, docs/rubrics/theme-naming.md) writes theme-names.jsonl.
3. `gapfinder threat-prepare` / `market-prepare`: inputs for the two agent steps below.
4. Threat mapper (Claude Code subagent, docs/rubrics/threat-mapping.md) writes
   threat-mapping.jsonl.
5. Market researcher (subagent with web search, docs/rubrics/market-research.md) writes
   market-research.jsonl (decision D11).
6. `gapfinder gaps`    : GitHub supply + NVD lookups, scoring, gap report.
"""

from __future__ import annotations

import json
import re
from datetime import date
from pathlib import Path

from . import embed, gaps, refdata, schemas, themes
from .collectors.base import Collector
from .store import Store

NVD_URL = "https://services.nvd.nist.gov/rest/json/cves/2.0"


# ------------------------------------------------------------------ step 1

def build_themes(store: Store, out_dir: Path) -> dict:
    signals = store.need_signals()
    result = themes.find_themes_with_stability(signals)
    by_id = {s["id"]: s for s in signals}
    lean = {
        "generated": date.today().isoformat(),
        "need_signals": len(signals),
        "seeds": result["seeds"],
        "outliers": result["outliers"],
        "themes": [{k: t[k] for k in ("theme_id", "keywords", "signal_ids", "stability")}
                   for t in result["themes"]],
    }
    naming_input = [{
        "theme_id": t["theme_id"],
        "keywords": t["keywords"],
        "signals": [{"title": by_id[i]["title"], "body": by_id[i]["body"][:250],
                     "segment": by_id[i]["segment"]} for i in t["signal_ids"][:12]],
    } for t in result["themes"]]
    out_dir.mkdir(parents=True, exist_ok=True)
    (out_dir / "themes.json").write_text(json.dumps(lean, indent=1))
    (out_dir / "theme-naming-input.json").write_text(json.dumps(naming_input, indent=1))
    return lean


def load_names(path: Path, theme_ids: set[int]) -> dict[int, dict]:
    names = {n.theme_id: n.model_dump() for n in schemas.load_jsonl(path, schemas.ThemeName)}
    if set(names) != theme_ids:
        raise ValueError(f"names cover {sorted(names)}, themes are {sorted(theme_ids)}")
    return names


# ------------------------------------------------------------------ step 3

def build_threat_input(theme_list: list[dict], names: dict[int, dict], config: dict,
                       scoring: dict, out_dir: Path) -> list[dict]:
    """Shortlist ATT&CK candidates per coherent theme for the threat mapper agent."""
    attack = refdata.load_attack(config)
    att_emb = embed.encode([a["text"] for a in attack], embed.RETRIEVAL_MODEL)
    k = scoring["threat"]["attack_candidates"]
    items = []
    for t in theme_list:
        meta = names[t["theme_id"]]
        if meta["coherent"] != "y":
            continue
        q = embed.encode([f"{meta['name']}. {meta['need']}"], embed.RETRIEVAL_MODEL)[0]
        _, idx = gaps.top_k_similar(q, att_emb, k)
        items.append({
            "theme_id": t["theme_id"], "name": meta["name"], "need": meta["need"],
            "candidates": [{"id": attack[i]["id"], "name": attack[i]["name"],
                            "description": attack[i]["text"][:300]} for i in idx],
        })
    (out_dir / "threat-mapping-input.json").write_text(json.dumps(items, indent=1))
    return items


def load_threat(path: Path, threat_input: list[dict]) -> dict[int, dict]:
    expected = {i["theme_id"]: {c["id"] for c in i["candidates"]} for i in threat_input}
    out = {}
    for m in schemas.load_jsonl(path, schemas.ThreatMapping):
        if m.theme_id not in expected:
            raise ValueError(f"unknown theme {m.theme_id}")
        bad = set(m.techniques) - expected[m.theme_id]
        if bad:
            raise ValueError(f"theme {m.theme_id}: techniques must be among its candidates; got {sorted(bad)}")
        out[m.theme_id] = m.model_dump()
    if set(out) != set(expected):
        raise ValueError(f"threat mapping covers {sorted(out)}, expected {sorted(expected)}")
    return out


_PAID_PAIN = re.compile(
    r"\b(expensive|pricing|priced|price|cost(s|ly)?|licen[cs](e|es|ing)|paid|paywall|"
    r"subscription|per[- ]seat|enterprise (plan|tier|edition|license)|sso tax|vendor lock|"
    r"budget|alternative to)\b", re.IGNORECASE)


def paid_pain(signals: list[dict]) -> list[dict]:
    """Need statements that mention price, licensing or vendor alternatives."""
    return [s for s in signals if _PAID_PAIN.search(f"{s['title']} {s['body']}")]


def build_market_input(theme_list: list[dict], names: dict[int, dict], store: Store,
                       out_dir: Path, repo_search=None) -> list[dict]:
    """Per coherent theme: what the market researcher agent needs to start from."""
    by_id = {s["id"]: s for s in store.need_signals()}
    repo_search = repo_search or refdata.GitHubRepoSearch()
    items = []
    for t in theme_list:
        meta = names[t["theme_id"]]
        if meta["coherent"] != "y":
            continue
        sigs = sorted((by_id[i] for i in t["signal_ids"]), key=lambda s: -s["engagement"])
        repos = repo_search.supply(meta["search_query"])
        items.append({
            "theme_id": t["theme_id"], "name": meta["name"], "need": meta["need"],
            "open_source_leaders": [f"{r['name']} ({r['stars']} stars)"
                                    for r in repos["top_repos"][:5]],
            "statements": [{"title": s["title"], "body": s["body"][:200], "url": s["url"]}
                           for s in sigs[:10]],
            "price_or_vendor_statements": [{"title": s["title"], "body": s["body"][:300],
                                            "url": s["url"]} for s in paid_pain(sigs)][:8],
        })
    (out_dir / "market-research-input.json").write_text(json.dumps(items, indent=1))
    return items


def load_market(path: Path, market_input: list[dict]) -> dict[int, dict]:
    """Validate market research (schema per line) and that it covers exactly the input themes."""
    expected = {i["theme_id"] for i in market_input}
    out = {}
    for m in schemas.load_jsonl(path, schemas.MarketResearch):
        if m.theme_id not in expected:
            raise ValueError(f"unknown theme {m.theme_id}")
        if m.theme_id in out:
            raise ValueError(f"theme {m.theme_id} appears twice")
        out[m.theme_id] = m.model_dump()
    if set(out) != expected:
        raise ValueError(f"market research covers {sorted(out)}, expected {sorted(expected)}")
    return out


def merge_market_parts(parts_dir: Path, market_input: list[dict], out_path: Path) -> int:
    """Combine researchers' part files into one file in input order, validating everything."""
    rows: dict[int, dict] = {}
    for part in sorted(parts_dir.glob("*.jsonl")):
        for m in schemas.load_jsonl(part, schemas.MarketResearch):
            if m.theme_id in rows:
                raise ValueError(f"theme {m.theme_id} researched twice (again in {part.name})")
            rows[m.theme_id] = m.model_dump()
    order = [i["theme_id"] for i in market_input]
    missing = [t for t in order if t not in rows]
    if missing:
        raise ValueError(f"no market research for themes {missing}")
    out_path.write_text("".join(json.dumps(rows[t]) + "\n" for t in order))
    return len(order)


class NvdCounter(Collector):
    name = "nvd"
    min_interval = 6.5  # public NVD API: 5 requests / 30 s without a key

    def count(self, query: str) -> int:
        data = self.get_json(NVD_URL, {"keywordSearch": query, "resultsPerPage": 1})
        return int(data.get("totalResults", 0))


def theme_features(theme_list: list[dict], names: dict[int, dict], threat: dict[int, dict],
                   market: dict[int, dict], store: Store, config: dict, scoring: dict,
                   repo_search=None, nvd=None) -> list[dict]:
    """Demand, supply and threat features for each coherent theme."""
    by_id = {s["id"]: s for s in store.need_signals()}
    attack = {a["id"]: a for a in refdata.load_attack(config)}
    repo_search = repo_search or refdata.GitHubRepoSearch()
    nvd = nvd or NvdCounter()

    out = []
    for t in theme_list:
        meta = names[t["theme_id"]]
        if meta["coherent"] != "y":
            continue
        sigs = [by_id[i] for i in t["signal_ids"]]
        repos = repo_search.supply(meta["search_query"])
        try:
            nvd_count = nvd.count(meta["search_query"])
        except Exception:  # informational only; don't fail the report on NVD hiccups
            nvd_count = None
        th = threat[t["theme_id"]]
        out.append({
            "theme_id": t["theme_id"],
            "name": meta["name"],
            "need": meta["need"],
            "search_query": meta["search_query"],
            "keywords": t["keywords"],
            "stability": t["stability"],
            "demand": gaps.demand_features(sigs, scoring["demand"]["recent_years"]),
            "supply": {
                **{k: repos[k] for k in ("total_repos", "top_stars", "active_top_repos",
                                         "top_repos")},
                "crowdedness": market[t["theme_id"]]["crowdedness"],
                "vendors": market[t["theme_id"]]["vendors"],
            },
            "monetization": {
                "willingness_to_pay": market[t["theme_id"]]["willingness_to_pay"],
                "wtp_evidence": market[t["theme_id"]]["wtp_evidence"],
                "wtp_sources": market[t["theme_id"]]["wtp_sources"],
                "paid_pain_share": round(len(paid_pain(sigs)) / len(sigs), 3),
                "paid_pain_examples": [{"title": s["title"], "url": s["url"]}
                                       for s in paid_pain(sigs)[:3]],
                "bundling_risk": market[t["theme_id"]]["bundling_risk"],
                "bundling_note": market[t["theme_id"]]["bundling_note"],
                "paid_market_gaps": market[t["theme_id"]]["paid_market_gaps"],
                "summary": market[t["theme_id"]]["summary"],
            },
            "threat": {
                "relevance": th["threat_relevance"],
                "reason": th.get("reason", ""),
                "techniques": [{k: attack[i][k] for k in ("id", "name", "url")}
                               for i in th.get("techniques", [])],
                "nvd_cves": nvd_count,
            },
            "evidence": sorted(
                ({k: s[k] for k in ("title", "url", "source", "engagement", "segment",
                                    "created_at")} for s in sigs),
                key=lambda e: -e["engagement"]),
        })
    return out


def render_report(ranked: list[dict], excluded: list[dict], meta: dict, scoring: dict) -> str:
    top_n, min_ev = scoring["report"]["top_gaps"], scoring["report"]["min_evidence"]
    w = scoring["weights"]
    lines = [
        f"# Gap report — {meta['generated']}", "",
        f"{meta['need_signals']} need statements (from {meta['signals_total']} collected signals) "
        f"grouped into {meta['themes_total']} themes; {len(excluded)} judged incoherent and "
        f"excluded; {len(meta['outliers'])} statements fit no theme.", "",
        f"**Gap score** = {w['demand']} × demand + {w['supply_gap']} × supply gap + "
        f"{w['monetization']} × monetization + {w['threat']} × threat relevance. "
        "Supply gap weighs commercial crowdedness 60% and open-source supply 40%; monetization "
        "combines willingness to pay, the share of statements complaining about price or "
        "vendors, and bundling risk (decision D11). Each component is a percentile rank across themes "
        "(0–1), so scores are relative to this run, not absolute. "
        "Weights: [config/scoring.yaml](../../config/scoring.yaml).", "",
        "**Stability** = how consistently a theme's statements cluster together across "
        f"{len(meta['seeds']['stability'])} other random seeds (1.0 = always). Treat themes "
        "below 0.5 as provisional.", "",
        "**Paid-market data** (vendors, prices, gaps, willingness to pay) comes from a market "
        "researcher agent using web search, with a source link for every claim "
        "([rubric](../docs/rubrics/market-research.md)). Prices change; check sources before "
        "relying on them.", "",
    ]
    fc_path = Path(meta.get("fact_check_path", ""))
    if fc_path.is_file():
        fc = schemas.FactCheck.model_validate_json(fc_path.read_text())
        by_theme: dict[int, int] = {}
        for p in fc.problems:
            by_theme[p.theme_id] = by_theme.get(p.theme_id, 0) + 1
        lines += [
            f"**Fact-check** (round {fc.round}): an adversarial checker re-opened the sources for "
            f"{fc.checked} vendor and willingness-to-pay claims; {len(fc.problems)} are not fully "
            "supported by their cited source. Per-gap counts are shown below; details in "
            "[phase2/fact-check.json](phase2/fact-check.json).", "",
        ]
        meta["_fact_check_by_theme"] = by_theme
    lines += [
        "## Ranking", "",
        "| # | Gap | Score | Demand | Supply gap | Monetization | Threat | Crowdedness | "
        "Willingness to pay | Statements | Stability |",
        "|---|---|---|---|---|---|---|---|---|---|---|",
    ]
    for i, t in enumerate(ranked, 1):
        flag = "" if t["stability"] >= 0.5 else " ⚠"
        lines.append(f"| {i} | [{t['name']}](#{i}-{_anchor(t['name'])}) | **{t['gap_score']}** | "
                     f"{t['scores']['demand']} | {t['scores']['supply_gap']} | "
                     f"{t['scores']['monetization']} | {t['scores']['threat']} | "
                     f"{t['supply']['crowdedness']}/3 | "
                     f"{t['monetization']['willingness_to_pay']}/3 | "
                     f"{t['demand']['need_signals']} | {t['stability']}{flag} |")
    lines.append("")
    for i, t in enumerate(ranked[:top_n], 1):
        d, s, th, m = t["demand"], t["supply"], t["threat"], t["monetization"]
        lines += [
            f"## {i}. {t['name']}", "",
            f"> {t['need']}", "",
            f"Gap score **{t['gap_score']}** · stability {t['stability']} · segments: "
            f"{', '.join(d['segments'])} · keywords: {', '.join(t['keywords'][:6])}", "",
            f"- **Demand**: {d['need_signals']} need statements, total engagement "
            f"{d['engagement']}, {d['recent_share']:.0%} from the last "
            f"{scoring['demand']['recent_years']} years.",
            f"**Opportunity:** {m['summary']}", "",
            f"- **Open-source supply** (GitHub repositories for `{t['search_query']}`): {s['total_repos']} "
            f"repos, leader {s['top_stars']}★, {s['active_top_repos']} of the top 10 pushed in "
            "the last year. Leading projects: "
            + (", ".join(f"[{r['name']}]({r['url']}) {r['stars']}★" for r in s["top_repos"][:3])
               or "none") + ".",
            f"- **Threat relevance** {th['relevance']}/3: {th['reason']}"
            + (" ATT&CK: " + ", ".join(f"[{a['id']} {a['name']}]({a['url']})"
                                       for a in th["techniques"]) + "." if th["techniques"]
               else "")
            + (f" NVD CVEs matching the query: {th['nvd_cves']}." if th["nvd_cves"] is not None
               else ""),
            "",
            f"**Paid market** — crowdedness {s['crowdedness']}/3, willingness to pay "
            f"{m['willingness_to_pay']}/3, bundling risk {m['bundling_risk']}."
            + (f" ⚠ {meta['_fact_check_by_theme'][t['theme_id']]} claim(s) here not fully "
               "supported by their source (see fact-check)."
               if meta.get("_fact_check_by_theme", {}).get(t["theme_id"]) else ""), "",
        ]
        if s["vendors"]:
            lines += ["| Vendor | Offering | Pricing | Sells to |", "|---|---|---|---|"]
            for v in s["vendors"]:
                lines.append(f"| [{v['name']}]({v['url']}) | {_cell(v['offering'])} | "
                             f"[{_cell(v['pricing'])}]({v['source']}) | {_cell(v['segment'])} |")
            lines.append("")
        else:
            lines += ["No commercial vendors found.", ""]
        lines.append(f"- **Willingness to pay**: {m['wtp_evidence']} "
                     + " ".join(f"[source {k}]({u})" for k, u in enumerate(m["wtp_sources"], 1)))
        lines.append(f"- **Bundling risk ({m['bundling_risk']})**: {m['bundling_note']}")
        share = m["paid_pain_share"]
        lines.append(f"- **Users complaining about price or vendors**: {share:.0%} of statements"
                     + (": " + ", ".join(f"[{_cell(x['title'][:60])}]({x['url']})"
                                         for x in m["paid_pain_examples"]) if share else "") + ".")
        if m["paid_market_gaps"]:
            lines.append("- **Where paying customers are underserved**:")
            lines += [f"  - {g['gap']} ([evidence]({g['evidence']}))" for g in m["paid_market_gaps"]]
        lines += ["", f"**Evidence** ({len(t['evidence'])} need statements; top {max(min_ev, 8)}):", ""]
        for e in t["evidence"][:max(min_ev, 8)]:
            lines.append(f"- [{e['title'][:100]}]({e['url']}) — {e['source']}, "
                         f"{e['engagement']} engagement, {e['created_at'][:4]}")
        lines.append("")
    if excluded:
        lines += ["## Excluded as incoherent", "",
                  "| Theme | Keywords | Namer's reason |", "|---|---|---|"]
        for x in excluded:
            lines.append(f"| {x['theme_id']} | {', '.join(x['keywords'][:6])} | {x['reason']} |")
        lines.append("")
    return "\n".join(lines) + "\n"


def _cell(text: str) -> str:
    return str(text).replace("|", "/").replace("\n", " ")


def _anchor(name: str) -> str:
    import re
    return re.sub(r"[^a-z0-9 -]", "", name.lower()).replace(" ", "-")
