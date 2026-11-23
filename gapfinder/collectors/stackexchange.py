"""Stack Exchange API (security.stackexchange.com by default).

Matches the query against question titles (full-text search was too noisy).
Unauthenticated quota is ~300 requests/day per IP. An unanswered question
with many views is a strong "unmet need" signal, so both are kept in metadata.
"""

from __future__ import annotations

from typing import Iterable

from ..models import Signal, iso_from_unix
from ..text import clean
from .base import Collector

URL = "https://api.stackexchange.com/2.3/search/advanced"


class StackExchangeCollector(Collector):
    name = "stackexchange"
    min_interval = 1.0

    def __init__(self, *args, site: str = "security", **kwargs):
        super().__init__(*args, **kwargs)
        self.site = site
        if site != "security":
            self.name = site  # e.g. "serverfault": its own source name and audience

    def collect(self, segment: str, query: str, limit: int = 50) -> Iterable[Signal]:
        data = self.get_json(
            URL,
            {
                "title": query,  # title match: precise; full-text matches loose words
                "site": self.site,
                "pagesize": min(limit, 100),
                "order": "desc",
                "sort": "relevance",
                "filter": "withbody",
                **({"todate": self.before_ts()} if self.before else {}),
            },
        )
        if data.get("backoff"):
            # API asks clients to wait this many seconds before the next call.
            self._sleep(int(data["backoff"]))
        for q in data.get("items", []):
            views = q.get("view_count", 0)
            yield Signal(
                source=self.name,
                native_id=f"{self.site}:{q['question_id']}",
                segment=segment,
                query=query,
                title=clean(q.get("title"), 300),
                body=clean(q.get("body")),
                url=q.get("link", ""),
                created_at=iso_from_unix(q.get("creation_date", 0)),
                # Engagement: votes + answers + views scaled down (1 point per 100 views).
                engagement=int(q.get("score", 0)) + int(q.get("answer_count", 0)) + views // 100,
                metadata={
                    "site": self.site,
                    "score": q.get("score", 0),
                    "answer_count": q.get("answer_count", 0),
                    "view_count": views,
                    "is_answered": q.get("is_answered", False),
                    "tags": q.get("tags", []),
                    "quota_remaining": data.get("quota_remaining"),
                },
            )
