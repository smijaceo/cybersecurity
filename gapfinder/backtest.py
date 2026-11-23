"""Backtest the method (decision D18). Configuration and pre-registration: config/backtest.yaml.

Gap finder: signals before the cutoff (open discovery only) -> judge -> themes -> namer ->
`rank` by demand -> category verifier -> blind matcher -> `score` (recall@k, precision@k).
Panel: anonymised founding-stage pitches of known successes/failures -> critics ->
`calibration` (ROC AUC of panel mean score).
"""

from __future__ import annotations

import json
from pathlib import Path
from statistics import mean

from . import gaps, panel, schemas
from .store import Store


def rank(store: Store, out_dir: Path, recent_years: int, audience_weights: dict) -> list[dict]:
    """Coherent themes ranked by demand only (market data can't be sent back in time)."""
    themes = json.loads((out_dir / "themes.json").read_text())["themes"]
    names = {n.theme_id: n for n in schemas.load_jsonl(out_dir / "theme-names.jsonl", schemas.ThemeName)}
    by_id = {s["id"]: s for s in store.need_signals()}
    rows = []
    for t in themes:
        n = names[t["theme_id"]]
        if n.coherent != "y":
            continue
        d = gaps.demand_features([by_id[i] for i in t["signal_ids"]], recent_years,
                                 audience_weights=audience_weights)
        rows.append({"theme_id": t["theme_id"], "name": n.name, "need": n.need,
                     "stability": t["stability"], "demand": d})
    r1 = gaps.percentile_rank([r["demand"]["weighted_need"] for r in rows])
    r2 = gaps.percentile_rank([r["demand"]["engagement"] for r in rows])
    for r, a, b in zip(rows, r1, r2):
        r["demand_score"] = round(0.6 * a + 0.4 * b, 3)
    rows.sort(key=lambda r: -r["demand_score"])
    (out_dir / "ranked.json").write_text(json.dumps(rows, indent=1))
    return rows


def score(ranked: list[dict], matches: list[schemas.ThemeMatch],
          checks: list[schemas.CategoryCheck], top_k: int) -> dict:
    kept = {c.id for c in checks if c.keep}
    top = {r["theme_id"] for r in ranked[:top_k]}
    good = [m for m in matches if m.category in kept and m.confidence in ("high", "medium")]
    found = {m.category for m in good if m.theme_id in top}
    found_anywhere = {m.category for m in good}
    top_matched = {m.theme_id for m in good if m.theme_id in top}
    return {
        "categories_verified": sorted(kept),
        "categories_dropped": sorted(c.id for c in checks if not c.keep),
        "found_top_k": sorted(found),
        "found_any_rank": sorted(found_anywhere),
        "recall_at_k": round(len(found) / len(kept), 3) if kept else None,
        "precision_at_k": round(len(top_matched) / min(top_k, len(ranked)), 3) if ranked else None,
        "top_k": top_k,
        "themes_ranked": len(ranked),
    }


def calibration(cal_dir: Path, labels: list[schemas.CalibrationLabel], lenses: list[str]) -> dict:
    from sklearn.metrics import roc_auc_score

    rows = []
    for lab in labels:
        crit = panel.load_round(cal_dir, lab.id, 1)
        missing = [l for l in lenses if l not in crit]
        if missing:
            raise ValueError(f"{lab.id}: missing critiques for {missing}")
        rows.append({"id": lab.id, "company": lab.company, "outcome": lab.outcome,
                     "mean": round(mean(crit[l].score for l in lenses), 2),
                     "scores": {l: crit[l].score for l in lenses}})
    y = [1 if r["outcome"] == "success" else 0 for r in rows]
    if len(set(y)) < 2:
        raise ValueError("need both successes and failures")
    auc = roc_auc_score(y, [r["mean"] for r in rows])
    per_lens = {l: round(roc_auc_score(y, [r["scores"][l] for r in rows]), 3) for l in lenses}
    return {"auc": round(auc, 3), "per_lens_auc": per_lens, "concepts": rows}


def render(gap: dict | None, cal: dict | None, cfg: dict) -> str:
    L = ["# Backtest — does the method work?", "",
         "Pre-registered in [config/backtest.yaml](../config/backtest.yaml) before any run "
         "(decision D18).", ""]
    if gap:
        L += ["## Gap finder (data before " + cfg["gap_finder"]["cutoff"] + ", open discovery only)", "",
              f"- Recall@{gap['top_k']}: **{gap['recall_at_k']}** — verified categories found in the "
              f"top {gap['top_k']} themes: {', '.join(gap['found_top_k']) or 'none'}",
              f"- Found at any rank: {', '.join(gap['found_any_rank']) or 'none'}",
              f"- Precision@{gap['top_k']}: **{gap['precision_at_k']}** (share of top themes matching a category)",
              f"- Categories kept after date verification: {', '.join(gap['categories_verified'])}",
              f"- Dropped (already funded before the cutoff): {', '.join(gap['categories_dropped']) or 'none'}",
              f"- Coherent themes ranked: {gap['themes_ranked']}", ""]
    if cal:
        L += ["## Critic panel calibration", "",
              f"- **AUC {cal['auc']}** for the panel mean (0.5 = chance, 1.0 = perfect separation of "
              "later successes from failures).", "",
              "| Lens | AUC |", "|---|---|",
              *[f"| {l} | {a} |" for l, a in cal["per_lens_auc"].items()], "",
              "| Concept | Outcome | Company (revealed after scoring) | Panel mean |", "|---|---|---|---|",
              *[f"| {r['id']} | {r['outcome']} | {r['company']} | {r['mean']} |"
                for r in sorted(cal["concepts"], key=lambda r: -r["mean"])], "",
              f"Limitation: {cfg['panel_calibration']['limitation']}", ""]
    return "\n".join(L) + "\n"
