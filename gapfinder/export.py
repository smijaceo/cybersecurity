"""Export one concept as a launch brief for a downstream launch repository.

`gapfinder export <opening_id>` writes exports/<slug>/brief.json (validated against
schemas.LaunchBrief) and a short README. The brief is the contract between gapfinder (what to
build) and a launch repo (brand, copy, website, validation assets).
"""

from __future__ import annotations

import json
import subprocess
from datetime import datetime, timezone
from pathlib import Path

import yaml

from . import panel, schemas


def _commit(root: Path) -> str:
    try:
        return subprocess.run(["git", "rev-parse", "HEAD"], cwd=root, capture_output=True,
                              text=True, check=True).stdout.strip()
    except (OSError, subprocess.CalledProcessError):
        return "unknown"


def build_brief(root: Path, opening: str, panel_cfg: dict) -> schemas.LaunchBrief:
    ideas = root / "ideas"
    concept = schemas.Concept.model_validate_json((ideas / f"{opening}.json").read_text())
    concept_input = json.loads((ideas / f"{opening}.input.json").read_text())
    rounds = {r: c for r in (1, 2, 3) if (c := panel.load_round(ideas, opening, r))}
    if not rounds:
        raise ValueError(f"{opening}: no critiques yet — run the critic panel first")
    final = rounds[max(rounds)]
    if panel_cfg.get("mode") == "history":
        verdict = panel.decide_history(final, panel_cfg, panel.history_reference(panel_cfg["history"]["results"]))
    else:
        verdict = panel.decide(final, panel_cfg)
    objections = [{"lens": l, "severity": o.severity, "objection": o.objection, "evidence": o.evidence}
                  for l, c in final.items() for o in c.objections if o.severity in ("fatal", "major")]
    return schemas.LaunchBrief(
        exported_at=datetime.now(timezone.utc).isoformat(timespec="seconds"),
        gapfinder_commit=_commit(root),
        opening_id=opening,
        concept=concept,
        panel={**{k: verdict.get(k) for k in ("decision", "mean", "min", "scores", "founder_fit",
                                               "above_successes", "n_successes",
                                               "above_failures", "n_failures")},
               "final_round": max(rounds), "fatal_count": len(verdict["fatal"])},
        open_objections=objections,
        change_my_mind=[{"lens": l, "evidence_needed": x} for l, c in final.items()
                        for x in c.what_would_change_my_mind],
        evidence_signals=[{"title": s["title"], "url": s["url"], "theme": t["name"]}
                          for t in concept_input["themes"] for s in t["need_statements"]],
        flagged_claims=concept_input.get("flagged_claims", []),
        founder=yaml.safe_load((root / "config" / "founder.yaml").read_text()),
    )


def write(root: Path, brief: schemas.LaunchBrief, out_root: Path) -> Path:
    out = out_root / brief.concept.slug
    out.mkdir(parents=True, exist_ok=True)
    (out / "brief.json").write_text(brief.model_dump_json(indent=1))
    p, c = brief.panel, brief.concept
    (out / "README.md").write_text(
        f"# Launch brief: {c.name}\n\n> {c.one_liner}\n\n"
        f"- Status: **{brief.status}** — panel verdict {p['decision']} (mean {p['mean']}, "
        f"founder fit {p.get('founder_fit')}); not yet tested with real buyers.\n"
        f"- Riskiest assumption: {c.riskiest_assumption.assumption}\n"
        f"- First test: {c.riskiest_assumption.test}\n"
        f"- Success signal: {c.riskiest_assumption.success_signal}\n"
        f"- Open fatal/major objections: {len(brief.open_objections)}; claims never to reuse: "
        f"{len(brief.flagged_claims)}\n\n"
        f"`brief.json` validates against `gapfinder.schemas.LaunchBrief` (gapfinder commit "
        f"`{brief.gapfinder_commit[:12]}`).\n")
    return out
