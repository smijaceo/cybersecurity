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

-- Relevance labels (Phase 2). judge = "rules" or the rubric version used by the judge.
CREATE TABLE IF NOT EXISTS judgments (
    signal_id  TEXT PRIMARY KEY REFERENCES signals(id) ON DELETE CASCADE,
    on_segment TEXT NOT NULL CHECK (on_segment IN ('y', 'n')),
    need       TEXT NOT NULL CHECK (need IN ('y', 'n')),
    reason     TEXT NOT NULL,
    judge      TEXT NOT NULL,
    judged_at  TEXT NOT NULL
);
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

    def save_judgment(self, signal_id: str, on_segment: str, need: str, reason: str,
                      judge: str) -> None:
        self.conn.execute(
            """
            INSERT INTO judgments (signal_id, on_segment, need, reason, judge, judged_at)
            VALUES (?, ?, ?, ?, ?, ?)
            ON CONFLICT(signal_id) DO UPDATE SET on_segment = excluded.on_segment,
                need = excluded.need, reason = excluded.reason, judge = excluded.judge,
                judged_at = excluded.judged_at
            """,
            (signal_id, on_segment, need, reason, judge, datetime.now(timezone.utc).isoformat()),
        )
        self.conn.commit()

    def get_judgment(self, signal_id: str) -> dict | None:
        row = self.conn.execute("SELECT * FROM judgments WHERE signal_id = ?",
                                (signal_id,)).fetchone()
        return dict(row) if row else None

    def need_signals(self) -> list[dict]:
        """Signals the judge marked as need statements, highest engagement first."""
        rows = self.conn.execute(
            """
            SELECT s.* FROM signals s JOIN judgments j ON j.signal_id = s.id
            WHERE j.need = 'y' ORDER BY s.engagement DESC
            """
        ).fetchall()
        out = []
        for r in rows:
            d = dict(r)
            d["metadata"] = json.loads(d["metadata"])
            out.append(d)
        return out

    def judgment_stats(self) -> list[sqlite3.Row]:
        return self.conn.execute(
            """
            SELECT s.segment, COUNT(s.id) AS total, COUNT(j.signal_id) AS judged,
                   SUM(j.judge = 'rules') AS dropped_by_rules,
                   SUM(j.on_segment = 'y') AS on_segment, SUM(j.need = 'y') AS need
            FROM signals s LEFT JOIN judgments j ON j.signal_id = s.id
            GROUP BY s.segment ORDER BY s.segment
            """
        ).fetchall()

    def delete_segment(self, segment: str) -> int:
        """Remove a segment's signals, e.g. before re-collecting with changed search terms."""
        self.conn.execute(
            "DELETE FROM judgments WHERE signal_id IN (SELECT id FROM signals WHERE segment = ?)",
            (segment,))
        cur = self.conn.execute("DELETE FROM signals WHERE segment = ?", (segment,))
        self.conn.commit()
        return cur.rowcount

    def stats(self) -> list[sqlite3.Row]:
        return self.conn.execute(
            """
            SELECT segment, source, COUNT(*) AS n, SUM(engagement) AS engagement
            FROM signals GROUP BY segment, source ORDER BY segment, source
            """
        ).fetchall()

    def iter_signals(self, segment: str | None = None,
                     min_engagement: int | None = None) -> Iterator[dict]:
        # Engagement can be negative (down-voted Stack Exchange questions), so only
        # filter on it when asked.
        sql = "SELECT * FROM signals WHERE 1 = 1"
        params: list = []
        if min_engagement is not None:
            sql += " AND engagement >= ?"
            params.append(min_engagement)
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
