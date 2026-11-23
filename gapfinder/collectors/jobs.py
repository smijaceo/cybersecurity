"""Job postings — work employers pay people to do (decision D16).

Sources: Remotive (remote jobs API, no key) and Hacker News "Who is hiring?" threads via the
Algolia API. Live job boards have no history, so Remotive can't be backtested; HN can.
"""

from __future__ import annotations

from typing import Iterable

from ..models import Signal, iso_from_unix
from ..text import clean
from .base import Collector

REMOTIVE = "https://remotive.com/api/remote-jobs"
ALGOLIA = "https://hn.algolia.com/api/v1/search"
ALGOLIA_BY_DATE = "https://hn.algolia.com/api/v1/search_by_date"


class JobsCollector(Collector):
    name = "jobs"
    min_interval = 1.0
    hiring_threads = 6  # most recent monthly "Who is hiring?" threads to search

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._threads: list[int] | None = None

    def threads(self) -> list[int]:
        if self._threads is None:
            params = {"tags": "story,author_whoishiring", "query": "who is hiring",
                      "hitsPerPage": self.hiring_threads}
            if self.before:
                params["numericFilters"] = f"created_at_i<{self.before_ts()}"
            data = self.get_json(ALGOLIA_BY_DATE, params)
            self._threads = [int(h["objectID"]) for h in data.get("hits", [])
                             if "hiring" in (h.get("title") or "").lower()]
        return self._threads

    def collect(self, segment: str, query: str, limit: int = 50) -> Iterable[Signal]:
        yield from self.collect_hn(segment, query, limit)
        if not self.before:  # Remotive only lists open jobs
            yield from self.collect_remotive(segment, query, limit)

    def collect_hn(self, segment, query, limit):
        tags = "comment,(" + ",".join(f"story_{t}" for t in self.threads()) + ")"
        if not self.threads():
            return
        data = self.get_json(ALGOLIA, {"query": query.strip('"'), "tags": tags,
                                       "hitsPerPage": min(limit, 100)})
        for h in data.get("hits", []):
            text = clean(h.get("comment_text"))
            yield Signal(
                source=self.name, native_id=f"hn-{h['objectID']}", segment=segment, query=query,
                title=clean(text.split("|")[0], 200) or "HN job posting", body=text,
                url=f"https://news.ycombinator.com/item?id={h['objectID']}",
                created_at=iso_from_unix(h.get("created_at_i", 0)), engagement=1,
                metadata={"board": "hn-whoishiring", "thread": h.get("story_id")})

    def collect_remotive(self, segment, query, limit):
        data = self.get_json(REMOTIVE, {"search": query.strip('"'), "limit": min(limit, 100)})
        for j in data.get("jobs", []):
            yield Signal(
                source=self.name, native_id=f"remotive-{j['id']}", segment=segment, query=query,
                title=clean(f"{j.get('title', '')} — {j.get('company_name', '')}", 300),
                body=clean(j.get("description")), url=j.get("url", ""),
                created_at=(j.get("publication_date") or "")[:19], engagement=1,
                metadata={"board": "remotive", "company": j.get("company_name"),
                          "category": j.get("category"), "tags": j.get("tags", [])})
