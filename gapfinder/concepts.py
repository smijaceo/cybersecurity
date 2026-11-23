"""Phase 3: startup concepts from the PM's shortlist (decision D14).

1. `gapfinder concept-prepare` writes one input file per opening: need statements, the
   fact-checked market research for its themes, threat mapping, and claims the fact-checker
   flagged as unsupported.
2. The concept writer (Claude Code subagent, docs/rubrics/concept.md) writes ideas/<id>.json.
3. `gapfinder concept-render` validates each concept (schema + grounding) and writes
   ideas/<slug>.md.
"""

from __future__ import annotations

import json
from pathlib import Path

from pydantic import ValidationError

from . import schemas
from .store import Store


def build_inputs(shortlist: dict, phase2: Path, store: Store, out_dir: Path) -> list[Path]:
    by_id = {s["id"]: s for s in store.need_signals()}
    themes = {t["theme_id"]: t for t in json.loads((phase2 / "themes.json").read_text())["themes"]}
    names = {n.theme_id: n.model_dump()
             for n in schemas.load_jsonl(phase2 / "theme-names.jsonl", schemas.ThemeName)}
    market = {m.theme_id: m.model_dump()
              for m in schemas.load_jsonl(phase2 / "market-research.jsonl", schemas.MarketResearch)}
    threat = {t.theme_id: t.model_dump()
              for t in schemas.load_jsonl(phase2 / "threat-mapping.jsonl", schemas.ThreatMapping)}
    fc_path = phase2 / "fact-check.json"
    flagged = (schemas.FactCheck.model_validate_json(fc_path.read_text()).problems
               if fc_path.exists() else [])
    gaps = {g["theme_id"]: g for g in json.loads((phase2 / "gaps.json").read_text())}

    out_dir.mkdir(parents=True, exist_ok=True)
    paths = []
    for op in shortlist["openings"]:
        missing = [t for t in op["theme_ids"] if t not in market]
        if missing:
            raise ValueError(f"{op['id']}: no market research for themes {missing}")
        item = {
            "opening_id": op["id"],
            "priority": op["priority"],
            "thesis": op["thesis"],
            "themes": [{
                "theme_id": tid,
                "name": names[tid]["name"],
                "need": names[tid]["need"],
                "gap_score": gaps[tid]["gap_score"] if tid in gaps else None,
                "stability": themes[tid]["stability"],
                "need_statements": [
                    {"title": by_id[i]["title"], "body": by_id[i]["body"][:300],
                     "url": by_id[i]["url"], "engagement": by_id[i]["engagement"]}
                    for i in sorted(themes[tid]["signal_ids"],
                                    key=lambda i: -by_id[i]["engagement"])],
                "market_research": market[tid],
                "threat": threat.get(tid),
                "open_source_leaders": gaps[tid]["supply"]["top_repos"][:5] if tid in gaps else [],
            } for tid in op["theme_ids"]],
            "flagged_claims": [p.model_dump() for p in flagged if p.theme_id in op["theme_ids"]],
        }
        path = out_dir / f"{op['id']}.input.json"
        path.write_text(json.dumps(item, indent=1))
        paths.append(path)
    return paths


def allowed_urls(concept_input: dict) -> tuple[set[str], set[str]]:
    """(evidence URLs, market-research URLs) a concept may cite for grounded fields."""
    evidence, market = set(), set()
    for t in concept_input["themes"]:
        evidence |= {s["url"] for s in t["need_statements"]}
        m = t["market_research"]
        market |= {v["source"] for v in m["vendors"]} | {v["url"] for v in m["vendors"]}
        market |= set(m["wtp_sources"]) | {g["evidence"] for g in m["paid_market_gaps"]}
    return evidence | market, market


def _norm(url: str) -> str:
    return url.strip().rstrip("/").replace("http://", "https://")


def check_grounding(concept: schemas.Concept, concept_input: dict) -> list[str]:
    """Problems with evidence or price comparables that don't trace back to the input."""
    evidence_ok, market_ok = (set(map(_norm, s)) for s in allowed_urls(concept_input))
    problems = []
    if concept.opening_id != concept_input["opening_id"]:
        problems.append(f"opening_id {concept.opening_id!r} != {concept_input['opening_id']!r}")
    for e in concept.problem.evidence:
        if _norm(e.url) not in evidence_ok:
            problems.append(f"problem evidence not from input: {e.url}")
    for c in concept.pricing.comparables:
        if _norm(c.source) not in market_ok:
            problems.append(f"price comparable not from fact-checked research: {c.vendor} {c.source}")
    return problems


def render(c: schemas.Concept, concept_input: dict) -> str:
    themes = ", ".join(f"{t['name']} (theme {t['theme_id']}, stability {t['stability']})"
                       for t in concept_input["themes"])
    L = [
        f"# {c.name}", "",
        f"> {c.one_liner}", "",
        f"Opening `{c.opening_id}` (priority {concept_input['priority']}) · from {themes}", "",
        "## Buyer and user", "",
        f"- **Buyer:** {c.buyer.role} — {c.buyer.company_profile}",
        f"- **User:** {c.user}", "",
        "## Problem", "", c.problem.summary, "",
        *[f"- {e.claim} ([source]({e.url}))" for e in c.problem.evidence], "",
        "## Why now", "", c.why_now.summary + " "
        + " ".join(f"[{i}]({u})" for i, u in enumerate(c.why_now.sources, 1)), "",
        "## MVP", "",
        *[f"- **{f.feature}** — {f.why}" for f in c.mvp.features], "",
        "Out of scope for v1: " + "; ".join(c.mvp.out_of_scope) + ".", "",
        "## Competition", "",
        "| Competitor | How we differ |", "|---|---|",
        *[f"| [{x.name}]({x.url}) | {x.how_we_differ.replace('|', '/')} |" for x in c.competitors],
        "", f"**Differentiation:** {c.differentiation}", "",
        "## Build", "",
        f"- Team: {c.build.team}", f"- Time to MVP: {c.build.months_to_mvp} months",
        "- Hardest parts: " + "; ".join(c.build.hardest_parts), "",
        "## Pricing and business model", "",
        f"- **Model:** {c.pricing.model}", f"- **Entry price:** {c.pricing.entry_price}",
        f"- **Rationale:** {c.pricing.rationale}", "",
        "| Comparable | Price |", "|---|---|",
        *[f"| {x.vendor} | [{x.price.replace('|', '/')}]({x.source}) |" for x in c.pricing.comparables],
        "", "## Go to market", "",
        f"- **First customers:** {c.go_to_market.first_customers}",
        f"- **Channel:** {c.go_to_market.channel}", f"- **Wedge:** {c.go_to_market.wedge}", "",
        "## Risks", "", *[f"- {r}" for r in c.risks], "",
        "## Riskiest assumption", "",
        f"- **Assumption:** {c.riskiest_assumption.assumption}",
        f"- **Cheap test:** {c.riskiest_assumption.test}",
        f"- **Success signal:** {c.riskiest_assumption.success_signal}", "",
        "## Open questions", "", *[f"- {q}" for q in c.open_questions], "",
    ]
    return "\n".join(L) + "\n"


def render_all(ideas_dir: Path, only: str | None = None) -> list[tuple[str, list[str]]]:
    """Validate and render every ideas/<id>.json (or just `only`); (id, problems) per concept."""
    results = []
    for inp in sorted(ideas_dir.glob("*.input.json")):
        oid = inp.name.removesuffix(".input.json")
        if only and oid != only:
            continue
        cpath = ideas_dir / f"{oid}.json"
        if not cpath.exists():
            results.append((oid, ["concept file missing"]))
            continue
        try:
            concept = schemas.Concept.model_validate_json(cpath.read_text())
        except ValidationError as exc:
            results.append((oid, [f"schema: {e['loc']}: {e['msg']}" for e in exc.errors()[:5]]))
            continue
        concept_input = json.loads(inp.read_text())
        problems = check_grounding(concept, concept_input)
        if not problems:
            (ideas_dir / f"{concept.slug}.md").write_text(render(concept, concept_input))
        results.append((oid, problems))
    return results


# ---------------------------------------------------------------- variants (decision D19)

VARIANTS = "variants"


def check_file(path: Path, ideas_dir: Path, opening: str) -> list[str]:
    """Schema + grounding check of any concept file (final concept or a variant)."""
    concept_input = json.loads((ideas_dir / f"{opening}.input.json").read_text())
    try:
        concept = schemas.Concept.model_validate_json(path.read_text())
    except ValidationError as exc:
        return [f"schema: {e['loc']}: {e['msg']}" for e in exc.errors()[:5]]
    return check_grounding(concept, concept_input)


def check_variants(ideas_dir: Path, opening: str) -> list[str]:
    """All three variants valid and genuinely different; judgment valid and consistent."""
    vdir = ideas_dir / VARIANTS / opening
    problems, concepts = [], {}
    for v in ("v1", "v2", "v3"):
        p = vdir / f"{v}.json"
        if not p.exists():
            problems.append(f"{v}: missing")
            continue
        errs = check_file(p, ideas_dir, opening)
        problems += [f"{v}: {e}" for e in errs]
        if not errs:
            concepts[v] = schemas.Concept.model_validate_json(p.read_text())
    if len(concepts) == 3:
        keys = {v: (c.buyer.role.lower(), c.pricing.model.lower(), c.go_to_market.channel.lower())
                for v, c in concepts.items()}
        if len(set(keys.values())) < 3:
            problems.append("variants must differ in buyer, business model or channel")
    jp = vdir / "judgment.json"
    if jp.exists():
        try:
            j = schemas.VariantJudgment.model_validate_json(jp.read_text())
            if j.opening_id != opening:
                problems.append(f"judgment opening_id {j.opening_id!r} != {opening!r}")
        except ValidationError as exc:
            problems += [f"judgment: {e['loc']}: {e['msg']}" for e in exc.errors()[:3]]
    else:
        problems.append("judgment.json: missing")
    return problems
