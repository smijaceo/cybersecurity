"""Quality review of collected signals (Phase 1 exit check, Phase 2 relevance filter).

Workflow (decision D8):
1. `gapfinder sample` picks the top signals per segment into a JSON file.
2. The relevance judge (Claude Code subagent, rubric in docs/rubrics/relevance.md)
   writes one label per signal to a JSONL file.
3. `gapfinder evaluate` validates the labels, scores each segment against the
   threshold and writes a markdown report.
"""

from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path

from . import schemas
from .store import Store

BODY_EXCERPT = 700


def build_sample(store: Store, config: dict, per_segment: int = 20,
                 per_source_cap: int = 10) -> list[dict]:
    """Top signals by engagement per segment, capping each source so none dominates."""
    sample = []
    for segment, seg_cfg in config["segments"].items():
        per_source: dict[str, int] = {}
        picked = 0
        for sig in store.iter_signals(segment):
            if per_source.get(sig["source"], 0) >= per_source_cap:
                continue
            per_source[sig["source"]] = per_source.get(sig["source"], 0) + 1
            sample.append({
                "id": sig["id"],
                "segment": segment,
                "segment_description": seg_cfg["description"],
                "source": sig["source"],
                "engagement": sig["engagement"],
                "title": sig["title"],
                "body": sig["body"][:BODY_EXCERPT],
                "url": sig["url"],
            })
            picked += 1
            if picked == per_segment:
                break
    return sample


LabelError = schemas.SchemaError


def load_labels(path: str | Path, sample: list[dict]) -> dict[str, dict]:
    """Read judge labels; check each against the schema and that they cover the sample exactly."""
    labels: dict[str, dict] = {}
    for lab in schemas.load_jsonl(path, schemas.RelevanceLabel):
        if lab.id in labels:
            raise LabelError(f"duplicate id {lab.id}")
        labels[lab.id] = lab.model_dump()
    expected = {s["id"] for s in sample}
    missing, extra = expected - labels.keys(), labels.keys() - expected
    if missing or extra:
        raise LabelError(f"labels don't match sample: {len(missing)} missing, {len(extra)} extra")
    return labels


@dataclass
class SegmentResult:
    segment: str
    total: int
    on_segment: int
    need: int
    threshold: float

    @property
    def on_segment_rate(self) -> float:
        return self.on_segment / self.total if self.total else 0.0

    @property
    def passed(self) -> bool:
        return self.total > 0 and self.on_segment_rate >= self.threshold


def evaluate(sample: list[dict], labels: dict[str, dict], threshold: float = 0.5) -> list[SegmentResult]:
    results: dict[str, SegmentResult] = {}
    for item in sample:
        r = results.setdefault(item["segment"], SegmentResult(item["segment"], 0, 0, 0, threshold))
        lab = labels[item["id"]]
        r.total += 1
        r.on_segment += lab["on_segment"] == "y"
        r.need += lab["need"] == "y"
    return list(results.values())


def render_report(sample: list[dict], labels: dict[str, dict], results: list[SegmentResult],
                  title: str, notes: str = "") -> str:
    out = [f"# {title}", ""]
    if notes:
        out += [notes, ""]
    out += [
        "Labels from the relevance judge (Claude Code subagent) using "
        "[docs/rubrics/relevance.md](../docs/rubrics/relevance.md). "
        "Pass = on-segment rate ≥ threshold. `need` is the baseline for the Phase 2 filter.",
        "",
        "| Segment | Sampled | On-segment | Need | Result |",
        "|---|---|---|---|---|",
    ]
    for r in results:
        out.append(f"| {r.segment} | {r.total} | {r.on_segment} ({r.on_segment_rate:.0%}) | "
                   f"{r.need} | {'pass' if r.passed else 'FAIL'} |")
    out.append("")
    for r in results:
        out += [f"## {r.segment}", "", "| # | Source | Eng. | Title | Seg. | Need | Judge's reason |",
                "|---|---|---|---|---|---|---|"]
        items = [s for s in sample if s["segment"] == r.segment]
        for i, s in enumerate(items, 1):
            lab = labels[s["id"]]
            t = (s["title"] or s["body"][:90]).replace("|", "/")[:90]
            reason = lab.get("reason", "").replace("|", "/")
            out.append(f"| {i} | {s['source']} | {s['engagement']} | [{t}]({s['url']}) | "
                       f"{lab['on_segment']} | {lab['need']} | {reason} |")
        out.append("")
    return "\n".join(out) + "\n"
