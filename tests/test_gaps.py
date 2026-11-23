from __future__ import annotations

from datetime import datetime, timezone

import numpy as np

from gapfinder import gaps

W = {"demand": 0.3, "supply_gap": 0.3, "monetization": 0.25, "threat": 0.15}


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
    for s, src in zip(sigs, ("github", "ted")):
        s["source"] = src
    f = gaps.demand_features(sigs, recent_years=2, now=now,
                             audience_weights={"developer": 1.0, "buyer": 2.5})
    assert f == {"need_signals": 2, "weighted_need": 3.5, "audience_mix": {"buyer": 1, "developer": 1},
                 "engagement": 6, "recent_share": 0.5, "segments": ["a", "b"]}


def theme(name, need=10, repos=100, crowded=2, wtp=2, pain=0.1, bundling="medium", relevance=2):
    return {"name": name,
            "demand": {"need_signals": need, "engagement": need * 10, "recent_share": 0.5},
            "supply": {"total_repos": repos, "top_stars": repos * 10, "active_top_repos": 5,
                       "crowdedness": crowded},
            "monetization": {"willingness_to_pay": wtp, "paid_pain_share": pain,
                             "bundling_risk": bundling},
            "threat": {"relevance": relevance}}


def test_score_prefers_high_demand_low_supply():
    ranked = gaps.score([theme("crowded", need=5, repos=1000, crowded=3),
                         theme("gap", need=20, repos=30, crowded=1)], W)
    assert [t["name"] for t in ranked] == ["gap", "crowded"]
    assert ranked[0]["scores"]["supply_gap"] > ranked[1]["scores"]["supply_gap"]
    assert 0 <= ranked[1]["gap_score"] <= ranked[0]["gap_score"] <= 1


def test_commercial_crowding_outweighs_open_source_scarcity():
    # few open-source repos but crowded commercially vs many repos but no vendors
    a = theme("vendors-everywhere", repos=10, crowded=3)
    b = theme("oss-only", repos=1000, crowded=0)
    ranked = gaps.score([a, b], W)
    assert ranked[0]["name"] == "oss-only"


def test_monetization_rewards_wtp_and_low_bundling():
    ranked = gaps.score([theme("free-stuff", wtp=0, pain=0.0, bundling="high"),
                         theme("paid", wtp=3, pain=0.4, bundling="low")], W)
    assert ranked[0]["name"] == "paid"
    assert ranked[0]["scores"]["monetization"] == 1.0


def test_buyer_demand_outranks_same_count_of_developer_demand():
    dev = theme("dev", need=10)
    buy = theme("buy", need=10)
    dev["demand"]["weighted_need"], buy["demand"]["weighted_need"] = 10, 25
    assert gaps.score([dev, buy], W)[0]["name"] == "buy"


def test_demand_features_accepts_dates_without_timezone():
    now = datetime(2026, 11, 22, tzinfo=timezone.utc)
    sigs = [{"created_at": "2026-09-11", "engagement": 1, "segment": "a", "source": "regulation"},
            {"created_at": "2026-11-01T10:00:00", "engagement": 1, "segment": "a", "source": "jobs"},
            {"created_at": "2019-01-01T00:00:00+00:00", "engagement": 1, "segment": "a", "source": "hn"}]
    assert gaps.demand_features(sigs, recent_years=2, now=now)["recent_share"] == 2 / 3
