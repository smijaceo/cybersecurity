from __future__ import annotations

import json

import pytest

from gapfinder import relevance, review
from gapfinder.models import Signal
from gapfinder.store import Store

CONFIG = {"segments": {"a": {"description": "seg a"}}}


@pytest.mark.parametrize("title, body, dropped", [
    ("Show HN: My SIEM", "", True),
    ("launch hn: Acme (YC W24)", "x", True),
    ("[dead]", "", True),
    ("", "", True),
    ("Ask HN: Is there a tool for SBOM diffing?", "", False),
    ("Feature request: SCIM", "please add", False),
    ("Showing HN users how", "", False),
])
def test_prefilter(title, body, dropped):
    assert (relevance.prefilter({"title": title, "body": body}) is not None) is dropped


@pytest.fixture
def store(tmp_path):
    s = Store(tmp_path / "s.db")
    s.upsert([
        Signal("hn", "1", "a", "q", "Show HN: thing", "", "u1", "2026-01-01T00:00:00+00:00", 9),
        Signal("hn", "2", "a", "q", "Need a tool for X", "body", "u2", "2026-01-01T00:00:00+00:00", 5),
        Signal("hn", "3", "a", "q", "Pain with Y", "body", "u3", "2026-01-01T00:00:00+00:00", 1),
    ])
    return s


def test_rules_then_batches_then_import(store, tmp_path):
    assert relevance.apply_rules(store) == (1, 2)
    assert relevance.apply_rules(store) == (0, 2)  # idempotent: judged rows are skipped
    (batch,) = relevance.export_batches(store, CONFIG, tmp_path / "b", batch_size=10)
    items = json.loads(batch.read_text())
    assert [i["id"] for i in items] == ["hn:2", "hn:3"]

    labels = tmp_path / "l.jsonl"
    labels.write_text(json.dumps({"id": "hn:2", "on_segment": "y", "need": "y", "reason": "r"}) + "\n"
                      + json.dumps({"id": "hn:3", "on_segment": "y", "need": "n", "reason": "r"}) + "\n")
    assert relevance.import_labels(store, batch, labels) == 2
    assert [s["id"] for s in store.need_signals()] == ["hn:2"]
    assert store.get_judgment("hn:1")["judge"] == "rules"
    assert relevance.export_batches(store, CONFIG, tmp_path / "b2", 10) == []
    (row,) = store.judgment_stats()
    assert (row["total"], row["judged"], row["dropped_by_rules"], row["need"]) == (3, 3, 1, 1)


def test_import_rejects_incomplete_labels(store, tmp_path):
    relevance.apply_rules(store)
    (batch,) = relevance.export_batches(store, CONFIG, tmp_path / "b", 10)
    labels = tmp_path / "l.jsonl"
    labels.write_text(json.dumps({"id": "hn:2", "on_segment": "y", "need": "y"}) + "\n")
    with pytest.raises(review.LabelError):
        relevance.import_labels(store, batch, labels)
    assert store.get_judgment("hn:2") is None  # nothing stored on failure


def test_delete_segment_removes_judgments(store):
    relevance.apply_rules(store)
    store.delete_segment("a")
    assert store.get_judgment("hn:1") is None


def test_export_batches_never_overwrites(store, tmp_path):
    relevance.apply_rules(store)
    out = tmp_path / "b"
    out.mkdir()
    (out / "batch-00.json").write_text("[]")
    (out / "batch-03.json").write_text("[]")
    (p,) = relevance.export_batches(store, CONFIG, out, batch_size=10)
    assert p.name == "batch-04.json"
    assert (out / "batch-00.json").read_text() == "[]"
