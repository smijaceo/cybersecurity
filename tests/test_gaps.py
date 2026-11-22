from __future__ import annotations

from datetime import datetime, timezone

import numpy as np

from gapfinder import gaps

W = {"demand": 0.4, "supply_gap": 0.35, "threat": 0.25}


def test_percentile_rank_with_ties():
    assert gaps.percentile_rank([3, 1, 3, 2]) == [5 / 6, 0.0, 5 / 6, 1 / 3]
    assert gaps.percentile_rank([7]) == [0.5]


def test_top_k_similar():
    m = np.array([[1, 0], [0, 1], [0.6, 0.8]], dtype=np.float32)
    mean, idx = gaps.top_k_similar(np.array([1, 0], dtype=np.float32), m, 2)
    assert idx == [0, 2] and abs(mean - 0.8) < 1e-6
    assert gaps.top_k_similar(np.array([1, 0]), np.zeros((0, 2)), 3) == (0.0, [])


def test_demand_features_recent_share():
    now = datetime(2026, 11, 22, tzinfo=timezone.utc)
    sigs = [{"created_at": "2026-01-01T00:00:00+00:00", "engagement": 5, "segment": "a"},
            {"created_at": "2019-01-01T00:00:00+00:00", "engagement": 1, "segment": "b"}]
    f = gaps.demand_features(sigs, recent_years=2, now=now)
    assert f == {"need_signals": 2, "engagement": 6, "recent_share": 0.5, "segments": ["a", "b"]}


def theme(name, need, repos, relevance):
    return {"name": name,
            "demand": {"need_signals": need, "engagement": need * 10, "recent_share": 0.5},
            "supply": {"total_repos": repos, "top_stars": repos * 10, "active_top_repos": 5},
            "threat": {"relevance": relevance}}


def test_score_prefers_high_demand_low_supply():
    ranked = gaps.score([theme("crowded", 5, 1000, 2), theme("gap", 20, 30, 2)], W)
    assert [t["name"] for t in ranked] == ["gap", "crowded"]
    assert ranked[0]["scores"]["supply_gap"] > ranked[1]["scores"]["supply_gap"]
    assert 0 <= ranked[1]["gap_score"] <= ranked[0]["gap_score"] <= 1
