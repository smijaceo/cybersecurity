"""GitHub issue search: feature requests and "is there a tool" issues.

Unauthenticated search is limited to ~10 requests/minute, so requests are
spaced 6s apart. Set GITHUB_TOKEN to raise the limit to 30/minute.
"""

from __future__ import annotations

import os
from typing import Iterable

from ..models import Signal
from ..text import clean
from .base import Collector

URL = "https://api.github.com/search/issues"


class GitHubIssuesCollector(Collector):
    name = "github"
    min_interval = 6.0

    def __init__(self, *args, token: str | None = None, **kwargs):
        super().__init__(*args, **kwargs)
        token = token or os.environ.get("GITHUB_TOKEN")
        self.session.headers["Accept"] = "application/vnd.github+json"
        if token:
            self.session.headers["Authorization"] = f"Bearer {token}"
            self.min_interval = 2.0

    def backoff(self, resp, attempt: int) -> float:
        reset = resp.headers.get("X-RateLimit-Reset")
        if reset and reset.isdigit():
            import time

            return max(1.0, min(float(reset) - time.time() + 1, 120))
        return super().backoff(resp, attempt)

    def collect(self, segment: str, query: str, limit: int = 50) -> Iterable[Signal]:
        data = self.get_json(
            URL,
            {
                "q": f"{query} in:title,body is:issue",
                "sort": "reactions",
                "order": "desc",
                "per_page": min(limit, 100),
            },
        )
        for issue in data.get("items", []):
            reactions = (issue.get("reactions") or {}).get("total_count", 0)
            comments = issue.get("comments", 0)
            repo = issue.get("repository_url", "").removeprefix("https://api.github.com/repos/")
            yield Signal(
                source=self.name,
                native_id=str(issue["id"]),
                segment=segment,
                query=query,
                title=clean(issue.get("title"), 300),
                body=clean(issue.get("body")),
                url=issue.get("html_url", ""),
                created_at=issue.get("created_at", ""),
                # Engagement: reactions (mostly +1s) + comments.
                engagement=int(reactions) + int(comments),
                metadata={
                    "repo": repo,
                    "state": issue.get("state"),
                    "reactions": reactions,
                    "comments": comments,
                    "labels": [l.get("name") for l in issue.get("labels", [])],
                },
            )
