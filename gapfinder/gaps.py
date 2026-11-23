"""Gap scoring: demand x supply weakness x threat relevance, per theme."""

from __future__ import annotations

import math
from datetime import datetime, timezone

import numpy as np
from scipy.stats import rankdata

from .models import audience


def percentile_rank(values: list[float]) -> list[float]:
    """Rank in [0, 1]; ties share the average rank (scipy). A single value ranks 0.5."""
    n = len(values)
    if n == 1:
        return [0.5]
    return [float(r) for r in (rankdata(values, method="average") - 1) / (n - 1)]


def top_k_similar(centroid: np.ndarray, matrix: np.ndarray, k: int) -> tuple[float, list[int]]:
    """Mean cosine similarity of the k nearest rows, and their indices (best first)."""
    if matrix.shape[0] == 0:
        return 0.0, []
    sims = matrix @ centroid
    idx = np.argsort(-sims)[:k]
    return float(sims[idx].mean()), [int(i) for i in idx]


def demand_features(signals: list[dict], recent_years: int, now: datetime | None = None,
                    audience_weights: dict | None = None) -> dict:
    now = now or datetime.now(timezone.utc)
    cutoff = now.replace(year=now.year - recent_years)
    recent = 0
    for s in signals:
        try:
            created = datetime.fromisoformat(s["created_at"])
            if created.tzinfo is None:  # date-only sources (tenders, regulations, some job boards)
                created = created.replace(tzinfo=timezone.utc)
            if created >= cutoff:
                recent += 1
        except ValueError:
            pass
    weights = audience_weights or {}
    mix: dict[str, int] = {}
    for s in signals:
        a = audience(s["source"])
        mix[a] = mix.get(a, 0) + 1
    return {
        "need_signals": len(signals),
        # Buyers' needs count more than developers' (decision D16).
        "weighted_need": round(sum(weights.get(a, 1.0) * n for a, n in mix.items()), 2),
        "audience_mix": dict(sorted(mix.items())),
        "engagement": sum(s["engagement"] for s in signals),
        "recent_share": recent / len(signals) if signals else 0.0,
        "segments": sorted({s["segment"] for s in signals}),
    }


BUNDLING_SAFETY = {"low": 2, "medium": 1, "high": 0}


def score(themes: list[dict], weights: dict) -> list[dict]:
    """Add demand/supply/threat component scores and the weighted gap score to each theme.

    Each theme needs: demand{need_signals, engagement, recent_share},
    supply{total_repos, top_stars, active_top_repos, crowdedness},
    monetization{willingness_to_pay, paid_pain_share, bundling_risk}, threat{relevance}.
    """
    def ranks(f):
        return percentile_rank([f(t) for t in themes])

    d = [0.5 * a + 0.3 * b + 0.2 * c for a, b, c in zip(
        ranks(lambda t: t["demand"].get("weighted_need", t["demand"]["need_signals"])),
        ranks(lambda t: math.log1p(t["demand"]["engagement"])),
        ranks(lambda t: t["demand"]["recent_share"]))]
    oss = [0.4 * a + 0.3 * b + 0.3 * c for a, b, c in zip(
        ranks(lambda t: math.log1p(t["supply"]["total_repos"])),
        ranks(lambda t: math.log1p(t["supply"]["top_stars"])),
        ranks(lambda t: t["supply"]["active_top_repos"]))]
    s = [0.6 * c + 0.4 * o for c, o in zip(ranks(lambda t: t["supply"]["crowdedness"]), oss)]
    m = [0.5 * a + 0.25 * b + 0.25 * c for a, b, c in zip(
        ranks(lambda t: t["monetization"]["willingness_to_pay"]),
        ranks(lambda t: t["monetization"]["paid_pain_share"]),
        ranks(lambda t: BUNDLING_SAFETY[t["monetization"]["bundling_risk"]]))]
    th = ranks(lambda t: t["threat"]["relevance"])
    w = weights
    for t, dv, sv, mv, tv in zip(themes, d, s, m, th):
        t["scores"] = {
            "demand": round(dv, 3),
            "supply_gap": round(1 - sv, 3),
            "monetization": round(mv, 3),
            "threat": round(tv, 3),
        }
        t["gap_score"] = round(w["demand"] * dv + w["supply_gap"] * (1 - sv)
                               + w["monetization"] * mv + w["threat"] * tv, 3)
    return sorted(themes, key=lambda t: -t["gap_score"])
