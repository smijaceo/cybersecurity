from __future__ import annotations

import json

import pytest

from gapfinder import panel, schemas
from tests.test_concepts import INPUT, concept

CFG = {"lenses": list(schemas.LENSES), "go": {"min_mean": 7.0, "min_lens": 5, "max_fatal": 0},
       "conditional": {"min_mean": 5.5, "min_lens": 3}}


def crit(lens, score, verdict="conditional", rnd=1, severity="major", cid="op", **over):
    d = {"concept_id": cid, "lens": lens, "round": rnd, "score": score, "verdict": verdict,
         "summary": "s", "objections": [{"objection": f"{lens} issue", "severity": severity,
                                         "evidence": "concept:pricing.entry_price"}],
         "strongest_point": "p", "what_would_change_my_mind": ["x"],
         "resolved_prior": [] if rnd == 1 else [{"objection": "o", "resolved": True}],
         "sources": []}
    d.update(over)
    return schemas.Critique.model_validate(d)


def panel_of(scores, **kw):
    return {l: crit(l, s, **kw) for l, s in zip(schemas.LENSES, scores)}


@pytest.mark.parametrize("scores, severity, expected", [
    ([8, 8, 7, 7, 8, 7, 7, 8, 7], "major", "GO"),
    ([8, 8, 7, 7, 8, 7, 7, 8, 7], "fatal", "CONDITIONAL"),   # fatal objection blocks GO
    ([9, 9, 9, 9, 9, 9, 9, 9, 4], "major", "CONDITIONAL"),   # one weak lens blocks GO
    ([6, 6, 5, 6, 6, 5, 6, 6, 6], "major", "CONDITIONAL"),
    ([7, 7, 7, 7, 7, 7, 7, 7, 2], "major", "NO-GO"),         # a lens at 2 rules out conditional
    ([5, 5, 5, 5, 5, 5, 5, 5, 5], "minor", "NO-GO"),
])
def test_decide(scores, severity, expected):
    assert panel.decide(panel_of(scores, severity=severity), CFG)["decision"] == expected


def test_decide_incomplete_panel():
    p = panel_of([8, 8, 8, 8, 8, 8])
    p.pop("legal-ethics")
    assert panel.decide(p, CFG)["decision"] == "INCOMPLETE"


@pytest.mark.parametrize("over, msg", [
    ({"verdict": "go"}, "verdict go"),  # score 6 from crit() is below 7
    ({"objections": [{"objection": "o", "severity": "major", "evidence": ""}]}, "needs evidence"),
    ({"resolved_prior": [{"objection": "o", "resolved": False}]}, "round 1"),
    ({"lens": "vibes"}, "lens"),
    ({"summary": None}, "summary"),
    ({"sources": ["my notes"]}, "URLs"),
])
def test_critique_schema_rejects(over, msg):
    with pytest.raises(Exception, match=msg):
        crit("gtm-pricing", 6, **over)


def test_round2_requires_resolution_list():
    with pytest.raises(Exception, match="round 2"):
        crit("gtm-pricing", 6, rnd=2, resolved_prior=[])


def test_load_critique_checks_path(tmp_path):
    p = panel.critique_path(tmp_path, "op", 1, "gtm-pricing")
    p.parent.mkdir(parents=True)
    p.write_text(crit("gtm-pricing", 6).model_dump_json())
    assert panel.load_critique(p).score == 6
    wrong = p.parent / "r1-legal-ethics.json"
    wrong.write_text(crit("gtm-pricing", 6).model_dump_json())
    with pytest.raises(ValueError, match="content says"):
        panel.load_critique(wrong)


def test_run_two_rounds_renders_reports(tmp_path):
    (tmp_path / "op.input.json").write_text(json.dumps(INPUT))
    (tmp_path / "op.json").write_text(concept(revision_log=["cut price to $99"]).model_dump_json())
    for rnd, scores in ((1, [5] * 9), (2, [8, 7, 7, 8, 7, 7, 8, 7, 7])):
        for lens, sc in zip(schemas.LENSES, scores):
            p = panel.critique_path(tmp_path, "op", rnd, lens)
            p.parent.mkdir(parents=True, exist_ok=True)
            p.write_text(crit(lens, sc, rnd=rnd, verdict="go" if sc >= 7 else "conditional")
                         .model_dump_json())
    (r,) = panel.run(tmp_path, CFG, tmp_path / "report" / "panel.md")
    assert (r["decision"], r["round1_mean"], r["final_round"]) == ("GO", 5, 2)
    md = (tmp_path / "scim-bridge.critique.md").read_text()
    assert "Decision (round 2): GO" in md and "cut price to $99" in md and "✅ resolved" in md
    assert "| 1 | [SCIM Bridge]" in (tmp_path / "report" / "panel.md").read_text()


def test_score_out_of_range():
    with pytest.raises(Exception, match="score"):
        crit("gtm-pricing", 11)


def test_decide_uses_configured_lenses():
    six = {"lenses": list(schemas.LENSES[:6]), **{k: v for k, v in CFG.items() if k != "lenses"}}
    p = panel_of([8, 8, 8, 8, 8, 8])          # only the original six lenses
    assert panel.decide(p, six)["decision"] == "GO"
    assert panel.decide(p, CFG)["decision"] == "INCOMPLETE"


def test_decide_history(tmp_path):
    ref = {"successes": [5.0, 5.88, 5.88, 6.0], "failures": [5.0, 5.38, 5.5, 5.5]}
    cfg = {"lenses": list(schemas.LENSES), "history": {"lenses": list(schemas.LENSES[:8])}}
    strong = panel.decide_history(panel_of([6] * 8 + [3]), cfg, ref)
    assert strong["decision"] == "STRONG" and strong["mean"] == 6 and strong["founder_fit"] == 3
    assert (strong["above_successes"], strong["above_failures"]) == (3, 4)
    assert panel.decide_history(panel_of([6, 6, 6, 6, 5, 5, 6, 6, 9]), cfg, ref)["decision"] == "PROMISING"  # 5.75
    assert panel.decide_history(panel_of([5] * 9), cfg, ref)["decision"] == "WEAK"
    p = panel_of([6] * 9)
    p.pop("founder-fit")
    assert panel.decide_history(p, cfg, ref)["decision"] == "INCOMPLETE"


def test_history_reference(tmp_path):
    f = tmp_path / "r.json"
    f.write_text(json.dumps({"calibration": {"concepts": [
        {"outcome": "success", "mean": 6}, {"outcome": "failure", "mean": 5}]}}))
    assert panel.history_reference(f) == {"successes": [6], "failures": [5]}


def test_export_brief(tmp_path):
    import yaml

    from gapfinder import export

    root = tmp_path
    ideas = root / "ideas"
    ideas.mkdir()
    (root / "config").mkdir()
    (root / "config" / "founder.yaml").write_text(yaml.safe_dump({"constraints": {"capital": "none"}}))
    (ideas / "op.input.json").write_text(json.dumps(INPUT))
    (ideas / "op.json").write_text(concept().model_dump_json())
    for lens in schemas.LENSES:
        p = panel.critique_path(ideas, "op", 1, lens)
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(crit(lens, 6).model_dump_json())
    ref = root / "r.json"
    ref.write_text(json.dumps({"calibration": {"concepts": [{"outcome": "success", "mean": 5.88},
                                                            {"outcome": "failure", "mean": 5.5}]}}))
    cfg = {"mode": "history", "lenses": list(schemas.LENSES),
           "history": {"lenses": list(schemas.LENSES[:8]), "results": str(ref)}}
    brief = export.build_brief(root, "op", cfg)
    assert brief.status == "unvalidated" and brief.panel["decision"] == "STRONG"
    assert len(brief.open_objections) == 9 and len(brief.evidence_signals) == 4
    out = export.write(root, brief, root / "exports")
    again = schemas.LaunchBrief.model_validate_json((out / "brief.json").read_text())
    assert again.concept.slug == "scim-bridge" and (out / "README.md").exists()
