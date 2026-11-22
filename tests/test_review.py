from __future__ import annotations

import json

import pytest

from gapfinder import review
from gapfinder.models import Signal
from gapfinder.store import Store

CONFIG = {"segments": {"a": {"description": "seg a"}, "b": {"description": "seg b"}}}


def sig(source, nid, segment, engagement):
    return Signal(source, nid, segment, "q", f"t{nid}", "body", f"u{nid}",
                  "2026-01-01T00:00:00+00:00", engagement)


@pytest.fixture
def store(tmp_path):
    s = Store(tmp_path / "s.db")
    s.upsert([sig("github", str(i), "a", 100 - i) for i in range(5)]
             + [sig("hn", "h1", "a", 1), sig("hn", "h2", "b", 5)])
    return s


def test_build_sample_caps_each_source(store):
    sample = review.build_sample(store, CONFIG, per_segment=4, per_source_cap=2)
    a = [s["id"] for s in sample if s["segment"] == "a"]
    assert a == ["github:0", "github:1", "hn:h1"]  # github capped at 2, segment has no more
    assert [s["id"] for s in sample if s["segment"] == "b"] == ["hn:h2"]
    assert sample[0]["segment_description"] == "seg a"


def write_labels(path, rows):
    path.write_text("\n".join(json.dumps(r) for r in rows) + "\n")


def test_evaluate_pass_and_fail(tmp_path):
    sample = [{"id": i, "segment": seg} for i, seg in [("1", "a"), ("2", "a"), ("3", "b"), ("4", "b")]]
    write_labels(tmp_path / "l.jsonl", [
        {"id": "1", "on_segment": "y", "need": "y"}, {"id": "2", "on_segment": "n", "need": "n"},
        {"id": "3", "on_segment": "n", "need": "n"}, {"id": "4", "on_segment": "n", "need": "n"},
    ])
    labels = review.load_labels(tmp_path / "l.jsonl", sample)
    a, b = review.evaluate(sample, labels, threshold=0.5)
    assert (a.on_segment, a.need, a.passed) == (1, 1, True)
    assert (b.on_segment, b.passed) == (0, False)


@pytest.mark.parametrize("rows, msg", [
    ([{"id": "1", "on_segment": "n", "need": "y"}], "need=y requires"),
    ([{"id": "1", "on_segment": "maybe", "need": "n"}], "on_segment"),
    ([], "1 missing"),
])
def test_load_labels_rejects_bad_input(tmp_path, rows, msg):
    write_labels(tmp_path / "l.jsonl", rows)
    with pytest.raises(review.LabelError, match=msg):
        review.load_labels(tmp_path / "l.jsonl", [{"id": "1", "segment": "a"}])


def test_delete_segment(store):
    assert store.delete_segment("a") == 6
    assert [s["id"] for s in store.iter_signals()] == ["hn:h2"]
