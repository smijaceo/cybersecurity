from __future__ import annotations

import json

import pytest

from gapfinder import analysis


def write(path, rows):
    path.write_text("\n".join(json.dumps(r) for r in rows) + "\n")
    return path


def name(tid, coherent="y"):
    return {"theme_id": tid, "coherent": coherent, "name": "n", "need": "d",
            "search_query": "q", "reason": "r"}


def test_load_names_validates(tmp_path):
    ok = analysis.load_names(write(tmp_path / "n.jsonl", [name(0), name(1, "n")]), {0, 1})
    assert ok[1]["coherent"] == "n"
    with pytest.raises(ValueError, match="names cover"):
        analysis.load_names(write(tmp_path / "n.jsonl", [name(0)]), {0, 1})
    bad = name(0)
    del bad["search_query"]
    with pytest.raises(ValueError, match="missing search_query"):
        analysis.load_names(write(tmp_path / "n.jsonl", [bad]), {0})


THREAT_INPUT = [{"theme_id": 0, "candidates": [{"id": "T1"}, {"id": "T2"}]},
                {"theme_id": 3, "candidates": [{"id": "T9"}]}]


def test_load_threat_accepts_valid(tmp_path):
    rows = [{"theme_id": 0, "techniques": ["T2"], "threat_relevance": 3, "reason": "r"},
            {"theme_id": 3, "techniques": [], "threat_relevance": 0, "reason": "r"}]
    out = analysis.load_threat(write(tmp_path / "t.jsonl", rows), THREAT_INPUT)
    assert out[0]["threat_relevance"] == 3 and out[3]["techniques"] == []


@pytest.mark.parametrize("row, msg", [
    ({"theme_id": 0, "techniques": ["T9"], "threat_relevance": 2}, "candidates"),  # not its candidate
    ({"theme_id": 0, "techniques": [], "threat_relevance": 5}, "0-3"),
    ({"theme_id": 7, "techniques": [], "threat_relevance": 1}, "unknown theme"),
])
def test_load_threat_rejects(tmp_path, row, msg):
    other = {"theme_id": 3, "techniques": [], "threat_relevance": 0}
    with pytest.raises(ValueError, match=msg):
        analysis.load_threat(write(tmp_path / "t.jsonl", [row, other]), THREAT_INPUT)


def test_paid_pain_matches_price_and_vendor_language():
    sigs = [{"title": "SSO tax is absurd", "body": ""},
            {"title": "Need SCIM", "body": "only on the Enterprise plan, too expensive"},
            {"title": "Alternative to Okta?", "body": ""},
            {"title": "Support IAM auth", "body": "please add"}]
    assert [s["title"] for s in analysis.paid_pain(sigs)] == [
        "SSO tax is absurd", "Need SCIM", "Alternative to Okta?"]


def market(tid=0, **over):
    d = {"theme_id": tid,
         "vendors": [{"name": "V", "url": "https://v", "offering": "o", "pricing": "$5/user",
                      "segment": "SMB", "source": "https://v/pricing"}],
         "crowdedness": 2, "paid_market_gaps": [{"gap": "g", "evidence": "https://e"}],
         "willingness_to_pay": 2, "wtp_evidence": "w", "wtp_sources": ["https://s"],
         "bundling_risk": "low", "bundling_note": "n", "summary": "s"}
    d.update(over)
    return d


def test_load_market_accepts_valid(tmp_path):
    out = analysis.load_market(write(tmp_path / "m.jsonl", [market()]), [{"theme_id": 0}])
    assert out[0]["crowdedness"] == 2


@pytest.mark.parametrize("over, msg", [
    ({"crowdedness": 4}, "crowdedness must be 0-3"),
    ({"bundling_risk": "maybe"}, "bundling_risk"),
    ({"wtp_sources": []}, "source URLs"),
    ({"paid_market_gaps": [{"gap": "g", "evidence": "trust me"}]}, "evidence URL"),
    ({"vendors": [{"name": "V", "url": "u", "offering": "o", "pricing": "p", "segment": "s",
                   "source": "none"}]}, "no source URL"),
    ({"extra": 1}, "keys"),
])
def test_load_market_rejects(tmp_path, over, msg):
    with pytest.raises(ValueError, match=msg):
        analysis.load_market(write(tmp_path / "m.jsonl", [market(**over)]), [{"theme_id": 0}])
