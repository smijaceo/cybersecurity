"""Phase 2 relevance filter.

Two layers:
1. Rules (`prefilter`) drop signals that can't be need statements: launch posts,
   dead/empty posts. Cheap, deterministic, and they save judge effort.
2. The relevance judge (Claude Code subagent, docs/rubrics/relevance.md) labels the
   rest. `export_batches` writes its input files; `import_labels` validates and stores
   its output in the `judgments` table.
"""

from __future__ import annotations

import json
import re
from pathlib import Path

from . import review
from .store import Store

RUBRIC_VERSION = "relevance-v1"
BODY_EXCERPT = 400

# Titles that announce something rather than ask for something.
_LAUNCH = re.compile(r"^\s*(show hn|launch hn|tell hn)\b", re.IGNORECASE)


def prefilter(signal: dict) -> str | None:
    """Return a reason to drop the signal, or None to keep it for the judge."""
    title = (signal.get("title") or "").strip()
    body = (signal.get("body") or "").strip()
    if _LAUNCH.match(title):
        return "rule: launch/announcement post"
    if title.lower() in ("[dead]", "[flagged]") or (not title and not body):
        return "rule: dead or empty post"
    return None


def apply_rules(store: Store) -> tuple[int, int]:
    """Record rule rejections as judgments. Returns (dropped, kept_for_judge)."""
    dropped = kept = 0
    for sig in store.iter_signals():
        if store.get_judgment(sig["id"]) is not None:
            continue
        reason = prefilter(sig)
        if reason:
            store.save_judgment(sig["id"], "n", "n", reason, "rules")
            dropped += 1
        else:
            kept += 1
    return dropped, kept


def export_batches(store: Store, config: dict, out_dir: str | Path, batch_size: int) -> list[Path]:
    """Write unjudged signals as judge input files (same shape as the Phase 1 sample)."""
    out_dir = Path(out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    pending = [
        {
            "id": s["id"],
            "segment": s["segment"],
            "segment_description": config["segments"][s["segment"]]["description"],
            "source": s["source"],
            "engagement": s["engagement"],
            "title": s["title"],
            "body": s["body"][:BODY_EXCERPT],
            "url": s["url"],
        }
        for s in store.iter_signals()
        if s["segment"] in config["segments"] and store.get_judgment(s["id"]) is None
    ]
    paths = []
    for i in range(0, len(pending), batch_size):
        p = out_dir / f"batch-{i // batch_size:02d}.json"
        p.write_text(json.dumps(pending[i:i + batch_size], indent=1))
        paths.append(p)
    return paths


def import_labels(store: Store, batch_file: str | Path, labels_file: str | Path) -> int:
    """Validate a judge's labels against its input batch, then store them."""
    batch = json.loads(Path(batch_file).read_text())
    labels = review.load_labels(labels_file, batch)  # raises LabelError on any mismatch
    for item in batch:
        lab = labels[item["id"]]
        store.save_judgment(item["id"], lab["on_segment"], lab["need"],
                            lab.get("reason", ""), RUBRIC_VERSION)
    return len(batch)
