from __future__ import annotations

from gapfinder.cli import build_queries
from gapfinder.models import Signal
from gapfinder.store import Store


def make(native_id: str, engagement: int, segment: str = "cloud-security") -> Signal:
    return Signal("hn", native_id, segment, "q", "t", "b", "u", "2026-01-01T00:00:00+00:00",
                  engagement, {"k": 1})


def test_upsert_is_idempotent_and_refreshes_engagement(tmp_path):
    store = Store(tmp_path / "s.db")
    store.upsert([make("1", 5), make("2", 1, "identity-access")])
    store.upsert([make("1", 9)])
    rows = list(store.iter_signals())
    assert [r["id"] for r in rows] == ["hn:1", "hn:2"]
    assert rows[0]["engagement"] == 9
    assert rows[0]["metadata"] == {"k": 1}
    assert [r["id"] for r in store.iter_signals(segment="identity-access")] == ["hn:2"]
    assert [r["id"] for r in store.iter_signals(min_engagement=6)] == ["hn:1"]


def test_build_queries_per_source():
    config = {"pain_phrases": ["is there a tool", "alternative to"],
              "segments": {"s": {"terms": ["SBOM", "SIEM"]}}}
    assert build_queries(config, "s", "stackexchange") == ["SBOM", "SIEM"]
    assert build_queries(config, "s", "hn") == ['"SBOM"', '"SIEM"']
    assert build_queries(config, "s", "github") == [
        '"is there a tool" "SBOM"', '"alternative to" "SBOM"',
        '"is there a tool" "SIEM"', '"alternative to" "SIEM"',
    ]


def test_negative_engagement_is_not_dropped(tmp_path):
    store = Store(tmp_path / "s.db")
    store.upsert([make("1", -2), make("2", 3)])
    assert {r["id"] for r in store.iter_signals()} == {"hn:1", "hn:2"}
    assert [r["id"] for r in store.iter_signals(min_engagement=0)] == ["hn:2"]
