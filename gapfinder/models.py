"""Common record shape every collector produces."""

from __future__ import annotations

import json
from dataclasses import asdict, dataclass, field
from datetime import datetime, timezone


@dataclass
class Signal:
    """One piece of demand evidence: a post, question or issue expressing a need."""

    source: str          # "hn" | "stackexchange" | "github"
    native_id: str       # id within the source
    segment: str         # segment key from config/segments.yaml
    query: str           # query that found it
    title: str
    body: str            # plain text, HTML stripped, truncated
    url: str
    created_at: str      # ISO 8601 UTC
    engagement: int      # source-specific popularity score, see each collector
    metadata: dict = field(default_factory=dict)

    @property
    def id(self) -> str:
        return f"{self.source}:{self.native_id}"

    def to_row(self) -> dict:
        row = asdict(self)
        row["id"] = self.id
        row["metadata"] = json.dumps(self.metadata, sort_keys=True)
        return row


def iso_from_unix(ts: int | float) -> str:
    return datetime.fromtimestamp(ts, tz=timezone.utc).isoformat()
