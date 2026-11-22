"""Hacker News via the Algolia search API (no key needed)."""

from __future__ import annotations

from typing import Iterable

from ..models import Signal, iso_from_unix
from ..text import clean
from .base import Collector

URL = "https://hn.algolia.com/api/v1/search"


class HackerNewsCollector(Collector):
    name = "hn"
    min_interval = 0.5

    def collect(self, segment: str, query: str, limit: int = 50) -> Iterable[Signal]:
        data = self.get_json(
            URL,
            {"query": query, "tags": "(story,comment)", "hitsPerPage": min(limit, 100)},
        )
        for hit in data.get("hits", []):
            is_comment = "comment" in hit.get("_tags", [])
            title = hit.get("title") or hit.get("story_title") or ""
            body = hit.get("comment_text") if is_comment else (hit.get("story_text") or "")
            points = hit.get("points") or 0
            comments = hit.get("num_comments") or 0
            yield Signal(
                source=self.name,
                native_id=str(hit["objectID"]),
                segment=segment,
                query=query,
                title=clean(title, 300),
                body=clean(body),
                url=f"https://news.ycombinator.com/item?id={hit['objectID']}",
                created_at=iso_from_unix(hit.get("created_at_i", 0)),
                # Engagement: upvotes + discussion. Comments carry no points in the API.
                engagement=int(points) + int(comments),
                metadata={"kind": "comment" if is_comment else "story",
                          "points": points, "num_comments": comments},
            )
