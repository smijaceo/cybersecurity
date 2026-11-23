from __future__ import annotations

import json

import pytest

from gapfinder import concepts, schemas

INPUT = {
    "opening_id": "op", "priority": 1, "thesis": "t",
    "themes": [{
        "theme_id": 3, "name": "SCIM", "need": "n", "gap_score": 0.5, "stability": 0.5,
        "need_statements": [{"title": f"s{i}", "body": "", "url": f"https://github.com/x/{i}",
                             "engagement": 1} for i in range(4)],
        "market_research": {
            "vendors": [{"name": "WorkOS", "url": "https://workos.com",
                         "source": "https://workos.com/pricing"}],
            "wtp_sources": ["https://stytch.com/pricing"],
            "paid_market_gaps": [{"gap": "g", "evidence": "https://example.com/gap"}],
        },
        "threat": None, "open_source_leaders": [],
    }],
    "flagged_claims": [],
}


def concept(**over):
    d = {
        "opening_id": "op", "slug": "scim-bridge", "name": "SCIM Bridge", "one_liner": "o",
        "buyer": {"role": "IT lead", "company_profile": "200-1000 staff"}, "user": "IT admin",
        "problem": {"summary": "p", "evidence": [
            {"claim": f"c{i}", "url": f"https://github.com/x/{i}"} for i in range(3)]},
        "why_now": {"summary": "w", "sources": ["https://news.example.com/a"]},
        "mvp": {"features": [{"feature": f"f{i}", "why": "y"} for i in range(3)],
                "out_of_scope": ["x"]},
        "competitors": [{"name": f"C{i}", "url": f"https://c{i}.com", "how_we_differ": "d"}
                        for i in range(3)],
        "differentiation": "d",
        "build": {"team": "2 eng", "months_to_mvp": 4, "hardest_parts": ["a", "b"]},
        "pricing": {"model": "per app", "entry_price": "$300/month", "rationale": "r",
                    "comparables": [{"vendor": "WorkOS", "price": "$125/connection",
                                     "source": "https://workos.com/pricing/"},
                                    {"vendor": "Stytch", "price": "$125",
                                     "source": "http://stytch.com/pricing"}]},
        "go_to_market": {"first_customers": "f", "channel": "c", "wedge": "w"},
        "risks": ["a", "b", "c"],
        "riskiest_assumption": {"assumption": "a", "test": "t", "success_signal": "s"},
        "open_questions": ["q"],
    }
    d.update(over)
    return schemas.Concept.model_validate(d)


def test_grounded_concept_passes_and_renders():
    c = concept()
    assert concepts.check_grounding(c, INPUT) == []  # trailing slash / http normalised
    md = concepts.render(c, INPUT)
    assert md.startswith("# SCIM Bridge")
    assert "[$125/connection](https://workos.com/pricing/)" in md
    assert "SCIM (theme 3, stability 0.5)" in md


def test_ungrounded_evidence_and_prices_are_flagged():
    c = concept(problem={"summary": "p", "evidence": [
        {"claim": "c", "url": "https://github.com/x/0"},
        {"claim": "c", "url": "https://github.com/x/1"},
        {"claim": "invented", "url": "https://made-up.example/report"}]},
        pricing={"model": "m", "entry_price": "e", "rationale": "r", "comparables": [
            {"vendor": "WorkOS", "price": "$125", "source": "https://workos.com/pricing"},
            {"vendor": "Mystery", "price": "$9", "source": "https://blog.example/prices"}]})
    problems = concepts.check_grounding(c, INPUT)
    assert any("made-up.example" in p for p in problems)
    assert any("Mystery" in p for p in problems)
    # evidence may cite need statements only via the evidence set; market URLs are fine too
    assert len(problems) == 2


def test_schema_rejects_thin_concepts():
    with pytest.raises(Exception):
        concept(competitors=[])
    with pytest.raises(Exception):
        concept(slug="Not A Slug")


def test_render_all_reports_missing_and_invalid(tmp_path):
    (tmp_path / "op.input.json").write_text(json.dumps(INPUT))
    assert concepts.render_all(tmp_path) == [("op", ["concept file missing"])]
    (tmp_path / "op.json").write_text(json.dumps({"opening_id": "op"}))
    (oid, problems), = concepts.render_all(tmp_path)
    assert oid == "op" and problems[0].startswith("schema:")
    (tmp_path / "op.json").write_text(concept().model_dump_json())
    assert concepts.render_all(tmp_path) == [("op", [])]
    assert (tmp_path / "scim-bridge.md").exists()


def _variants(tmp_path, buyers=("IT lead", "MSP owner", "CISO")):
    (tmp_path / "op.input.json").write_text(json.dumps(INPUT))
    vdir = tmp_path / "variants" / "op"
    vdir.mkdir(parents=True)
    for i, b in enumerate(buyers, 1):
        c = concept(buyer={"role": b, "company_profile": "x"})
        (vdir / f"v{i}.json").write_text(c.model_dump_json())
    return vdir


JUDGMENT = {"opening_id": "op", "winner": "v2", "grafted": ["v1 pricing"], "reasoning": "r",
            "scores": [{"variant": v, "angle": "a", "buyer_budget": 3, "defensibility": 2,
                        "founder_fit": 4, "time_to_revenue": 3, "risk": 3, "note": "n"}
                       for v in ("v1", "v2", "v3")]}


def test_check_variants_ok_and_failures(tmp_path):
    vdir = _variants(tmp_path)
    assert concepts.check_variants(tmp_path, "op") == ["judgment.json: missing"]
    (vdir / "judgment.json").write_text(json.dumps(JUDGMENT))
    assert concepts.check_variants(tmp_path, "op") == []
    bad = dict(JUDGMENT, scores=JUDGMENT["scores"][:2] + [dict(JUDGMENT["scores"][0])])
    (vdir / "judgment.json").write_text(json.dumps(bad))
    assert any("v1, v2, v3" in p for p in concepts.check_variants(tmp_path, "op"))


def test_variants_must_differ(tmp_path):
    vdir = _variants(tmp_path, buyers=("IT lead", "IT lead", "IT lead"))
    (vdir / "judgment.json").write_text(json.dumps(JUDGMENT))
    assert concepts.check_variants(tmp_path, "op") == [
        "variants must differ in buyer, business model or channel"]
