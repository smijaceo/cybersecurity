"""SQLite storage for collected signals."""

from __future__ import annotations

import json
import sqlite3
from datetime import datetime, timezone
from pathlib import Path
from typing import Iterable, Iterator

from .models import Signal

SCHEMA = """
CREATE TABLE IF NOT EXISTS signals (
    id           TEXT PRIMARY KEY,
    source       TEXT NOT NULL,
    native_id    TEXT NOT NULL,
    segment      TEXT NOT NULL,
    query        TEXT NOT NULL,
    title        TEXT NOT NULL,
    body         TEXT NOT NULL,
    url          TEXT NOT NULL,
    created_at   TEXT NOT NULL,
    engagement   INTEGER NOT NULL,
    metadata     TEXT NOT NULL,
    collected_at TEXT NOT NULL
);
CREATE INDEX IF NOT EXISTS idx_signals_segment ON signals(segment);
CREATE INDEX IF NOT EXISTS idx_signals_source ON signals(source);
"""


class Store:
    def __init__(self, path: str | Path):
        self.path = Path(path)
        self.path.parent.mkdir(parents=True, exist_ok=True)
        self.conn = sqlite3.connect(self.path)
        self.conn.row_factory = sqlite3.Row
        self.conn.executescript(SCHEMA)

    def upsert(self, signals: Iterable[Signal]) -> int:
        """Insert or refresh signals. Returns the number of rows written."""
        now = datetime.now(timezone.utc).isoformat()
        rows = [{**s.to_row(), "collected_at": now} for s in signals]
        if not rows:
            return 0
        self.conn.executemany(
            """
            INSERT INTO signals (id, source, native_id, segment, query, title, body, url,
                                 created_at, engagement, metadata, collected_at)
            VALUES (:id, :source, :native_id, :segment, :query, :title, :body, :url,
                    :created_at, :engagement, :metadata, :collected_at)
            ON CONFLICT(id) DO UPDATE SET
                engagement = excluded.engagement,
                metadata = excluded.metadata,
                collected_at = excluded.collected_at
            """,
            rows,
        )
        self.conn.commit()
        return len(rows)

    def stats(self) -> list[sqlite3.Row]:
        return self.conn.execute(
            """
            SELECT segment, source, COUNT(*) AS n, SUM(engagement) AS engagement
            FROM signals GROUP BY segment, source ORDER BY segment, source
            """
        ).fetchall()

    def iter_signals(self, segment: str | None = None, min_engagement: int = 0) -> Iterator[dict]:
        sql = "SELECT * FROM signals WHERE engagement >= ?"
        params: list = [min_engagement]
        if segment:
            sql += " AND segment = ?"
            params.append(segment)
        sql += " ORDER BY engagement DESC"
        for row in self.conn.execute(sql, params):
            d = dict(row)
            d["metadata"] = json.loads(d["metadata"])
            yield d

    def close(self) -> None:
        self.conn.close()
