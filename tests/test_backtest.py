from __future__ import annotations

import pytest

from gapfinder import backtest, panel, schemas
from tests.test_panel import crit


def test_score_recall_and_precision():
    ranked = [{"theme_id": i} for i in (5, 3, 9, 1)]
    matches = [schemas.ThemeMatch(theme_id=5, category="a", confidence="high"),
               schemas.ThemeMatch(theme_id=9, category="b", confidence="medium"),
               schemas.ThemeMatch(theme_id=1, category="c", confidence="high"),   # outside top 3
               schemas.ThemeMatch(theme_id=3, category="d", confidence="low"),    # too weak
               schemas.ThemeMatch(theme_id=3, category="z", confidence="high")]   # dropped category
    checks = [schemas.CategoryCheck(id=c, keep=c != "z", evidence=["https://e"], note="")
              for c in ("a", "b", "c", "d", "z")]
    r = backtest.score(ranked, matches, checks, top_k=3)
    assert r["found_top_k"] == ["a", "b"] and r["found_any_rank"] == ["a", "b", "c"]
    assert r["recall_at_k"] == 0.5          # 2 of 4 kept categories
    assert r["precision_at_k"] == 0.667     # themes 5 and 9 of the top 3
    assert r["categories_dropped"] == ["z"]


def test_calibration_auc(tmp_path):
    lenses = ["gtm-pricing", "defensibility"]
    labels = []
    for i, (outcome, s) in enumerate([("success", 8), ("success", 7), ("failure", 4), ("failure", 7)]):
        cid = f"cal-0{i}"
        labels.append(schemas.CalibrationLabel(id=cid, outcome=outcome, company=f"Co{i}",
                                               evidence=["https://e"]))
        for lens in lenses:
            p = panel.critique_path(tmp_path, cid, 1, lens)
            p.parent.mkdir(parents=True, exist_ok=True)
            p.write_text(crit(lens, s, cid=cid, verdict="go" if s >= 7 else "conditional").model_dump_json())
    r = backtest.calibration(tmp_path, labels, lenses)
    assert r["auc"] == 0.875   # one tie between a success (7) and a failure (7)
    with pytest.raises(ValueError, match="missing critiques"):
        backtest.calibration(tmp_path, labels, lenses + ["legal-ethics"])
