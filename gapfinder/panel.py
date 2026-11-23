"""Phase 4: critic panel aggregation (decision D2 critics, go/no-go by code).

Critiques live at ideas/critiques/<opening_id>/r<round>-<lens>.json, one per lens per round,
each validated against schemas.Critique. The final round decides GO / CONDITIONAL / NO-GO using
thresholds in config/scoring.yaml (panel). Outputs: ideas/<slug>.critique.md per concept and
reports/phase4/panel.md (ranked shortlist).
"""

from __future__ import annotations

import json
from pathlib import Path
from statistics import mean

from . import schemas

CRITIQUES = "critiques"


def critique_path(ideas_dir: Path, opening: str, rnd: int, lens: str) -> Path:
    return ideas_dir / CRITIQUES / opening / f"r{rnd}-{lens}.json"


def load_critique(path: Path) -> schemas.Critique:
    c = schemas.Critique.model_validate_json(path.read_text())
    expected = f"r{c.round}-{c.lens}.json"
    if path.name != expected or path.parent.name != c.concept_id:
        raise ValueError(f"{path}: content says {c.concept_id}/{expected}")
    return c


def load_round(ideas_dir: Path, opening: str, rnd: int) -> dict[str, schemas.Critique]:
    out = {}
    for lens in schemas.LENSES:
        p = critique_path(ideas_dir, opening, rnd, lens)
        if p.exists():
            out[lens] = load_critique(p)
    return out


def decide(critiques: dict[str, schemas.Critique], cfg: dict) -> dict:
    scores = {l: c.score for l, c in critiques.items()}
    fatal = [(l, o.objection) for l, c in critiques.items() for o in c.objections
             if o.severity == "fatal"]
    m, lo = mean(scores.values()), min(scores.values())
    g, cond = cfg["go"], cfg["conditional"]
    required = cfg.get("lenses", list(schemas.LENSES))
    if not set(required) <= set(critiques):
        decision = "INCOMPLETE"
    elif m >= g["min_mean"] and lo >= g["min_lens"] and len(fatal) <= g["max_fatal"]:
        decision = "GO"
    elif m >= cond["min_mean"] and lo >= cond["min_lens"]:
        decision = "CONDITIONAL"
    else:
        decision = "NO-GO"
    return {"decision": decision, "mean": round(m, 2), "min": lo, "scores": scores,
            "fatal": fatal, "lenses": len(critiques)}


def _cell(t: str) -> str:
    return str(t).replace("|", "/").replace("\n", " ")


def _ev(e: str) -> str:
    return f" ([evidence]({e}))" if e.startswith("http") else (f" — _{e}_" if e else "")


def render_concept(concept: schemas.Concept, rounds: dict[int, dict], decisions: dict[int, dict]) -> str:
    final = max(rounds)
    d = decisions[final]
    L = [f"# Critic panel — {concept.name}", "", f"> {concept.one_liner}", "",
         f"**Decision (round {final}): {d['decision']}** · mean {d['mean']} · lowest lens "
         f"{d['min']} · fatal objections {len(d['fatal'])}", ""]
    if len(rounds) > 1:
        L += ["| Lens | " + " | ".join(f"Round {r}" for r in sorted(rounds)) + " |",
              "|---|" + "---|" * len(rounds)]
        for lens in schemas.LENSES:
            L.append(f"| {lens} | " + " | ".join(
                f"{rounds[r][lens].score} ({rounds[r][lens].verdict})" if lens in rounds[r] else "—"
                for r in sorted(rounds)) + " |")
        L.append("| **mean** | " + " | ".join(f"**{decisions[r]['mean']}**" for r in sorted(rounds)) + " |")
        L.append("")
    if concept.revision_log:
        L += ["## What the revision changed", "", *[f"- {x}" for x in concept.revision_log], ""]
    for r in sorted(rounds, reverse=True):
        L += [f"## Round {r}", ""]
        for lens in schemas.LENSES:
            c = rounds[r].get(lens)
            if not c:
                continue
            L += [f"### {lens} — {c.score}/10, {c.verdict}", "", c.summary, "",
                  f"Strongest point: {c.strongest_point}", ""]
            L += [f"- **{o.severity}**: {o.objection}{_ev(o.evidence)}" for o in c.objections]
            if c.resolved_prior:
                L += ["", "Round-1 objections:"]
                L += [f"- {'✅ resolved' if p.resolved else '❌ not resolved'}: {p.objection}"
                      + (f" — {p.note}" if p.note else "") for p in c.resolved_prior]
            L += ["", "Would change my mind: " + "; ".join(c.what_would_change_my_mind), ""]
    return "\n".join(L) + "\n"


def run(ideas_dir: Path, cfg: dict, report_path: Path) -> list[dict]:
    """Validate all critiques, decide, render per-concept files and the ranked panel report."""
    results = []
    for inp in sorted(ideas_dir.glob("*.input.json")):
        oid = inp.name.removesuffix(".input.json")
        concept = schemas.Concept.model_validate_json((ideas_dir / f"{oid}.json").read_text())
        rounds = {}
        for rnd in (1, 2, 3):
            got = load_round(ideas_dir, oid, rnd)
            if got:
                rounds[rnd] = got
        if not rounds:
            continue
        decisions = {r: decide(c, cfg) for r, c in rounds.items()}
        (ideas_dir / f"{concept.slug}.critique.md").write_text(
            render_concept(concept, rounds, decisions))
        final = max(rounds)
        majors = [(l, o.objection) for l, c in rounds[final].items() for o in c.objections
                  if o.severity == "major"]
        results.append({"opening_id": oid, "name": concept.name, "slug": concept.slug,
                        "one_liner": concept.one_liner, "entry_price": concept.pricing.entry_price,
                        "final_round": final, **decisions[final],
                        "round1_mean": decisions[min(rounds)]["mean"], "majors": majors,
                        "riskiest_assumption": concept.riskiest_assumption.model_dump(),
                        "change_my_mind": [(l, c.what_would_change_my_mind[0])
                                           for l, c in rounds[final].items()]})
    order = {"GO": 0, "CONDITIONAL": 1, "NO-GO": 2, "INCOMPLETE": 3}
    results.sort(key=lambda r: (order[r["decision"]], -r["mean"], -r["min"]))
    report_path.parent.mkdir(parents=True, exist_ok=True)
    report_path.write_text(render_panel(results, cfg))
    (report_path.parent / "panel.json").write_text(json.dumps(results, indent=1))
    return results


def render_panel(results: list[dict], cfg: dict) -> str:
    g, c = cfg["go"], cfg["conditional"]
    L = ["# Critic panel — ranked shortlist", "",
         f"Six independent critics per concept ({', '.join(schemas.LENSES)}), rubric "
         "[docs/rubrics/critics.md](../../docs/rubrics/critics.md). Decision by code on the "
         f"final round: **GO** = mean ≥ {g['min_mean']}, every lens ≥ {g['min_lens']}, no fatal "
         f"objection; **CONDITIONAL** = mean ≥ {c['min_mean']}, every lens ≥ {c['min_lens']}; "
         "otherwise **NO-GO**.", "",
         "| # | Concept | Decision | Mean (round 1 → final) | Lowest lens | Fatal | Entry price |",
         "|---|---|---|---|---|---|---|"]
    for i, r in enumerate(results, 1):
        L.append(f"| {i} | [{r['name']}](../../ideas/{r['slug']}.md) | **{r['decision']}** | "
                 f"{r['round1_mean']} → {r['mean']} | {r['min']} | {len(r['fatal'])} | "
                 f"{_cell(r['entry_price'])} |")
    L.append("")
    for i, r in enumerate(results, 1):
        L += [f"## {i}. {r['name']} — {r['decision']}", "", f"> {r['one_liner']}", "",
              "Scores: " + ", ".join(f"{l} {s}" for l, s in r["scores"].items()) + ". "
              f"Full critique: [{r['slug']}.critique.md](../../ideas/{r['slug']}.critique.md).", ""]
        if r["fatal"]:
            L += ["**Fatal objections:**", *[f"- ({l}) {o}" for l, o in r["fatal"]], ""]
        if r["majors"]:
            L += ["**Major objections still open:**", *[f"- ({l}) {o}" for l, o in r["majors"]], ""]
        ra = r["riskiest_assumption"]
        L += ["**Next step — test the riskiest assumption:** " + ra["assumption"], "",
              f"- Test: {ra['test']}", f"- Success: {ra['success_signal']}", "",
              "**What would change the critics' minds:**",
              *[f"- ({l}) {x}" for l, x in r["change_my_mind"]], ""]
    return "\n".join(L) + "\n"
