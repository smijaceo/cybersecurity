from __future__ import annotations

import json

import pytest

from gapfinder import panel, schemas
from tests.test_concepts import INPUT, concept

CFG = {"go": {"min_mean": 7.0, "min_lens": 5, "max_fatal": 0},
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
    ([8, 8, 7, 7, 8, 7], "major", "GO"),
    ([8, 8, 7, 7, 8, 7], "fatal", "CONDITIONAL"),   # fatal objection blocks GO
    ([9, 9, 9, 9, 9, 4], "major", "CONDITIONAL"),   # one weak lens blocks GO
    ([6, 6, 5, 6, 6, 5], "major", "CONDITIONAL"),
    ([7, 7, 7, 7, 7, 2], "major", "NO-GO"),         # a lens at 2 rules out conditional
    ([5, 5, 5, 5, 5, 5], "minor", "NO-GO"),
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
    for rnd, scores in ((1, [5, 5, 5, 5, 5, 5]), (2, [8, 7, 7, 8, 7, 7])):
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
