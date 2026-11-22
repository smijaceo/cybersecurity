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
