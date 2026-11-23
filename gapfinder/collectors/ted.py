"""EU public procurement notices (TED API v3, no key) — buyers with budgets (decision D16).

Only contract notices (open calls) for security software/services CPV codes are collected, so
each signal is a public buyer formally asking to buy a capability. The query term narrows
notices by full text within those codes. Text stays in its original language.
"""

from __future__ import annotations

from typing import Iterable

from ..models import Signal
from ..text import clean
from .base import Collector

URL = "https://api.ted.europa.eu/v3/notices/search"

# Security software packages, data/file security, security software development, IT audit
# and testing services.
SECURITY_CPV = ["48730000", "48731000", "48732000", "72212730", "72800000", "72810000",
                "72820000"]
FIELDS = ["notice-title", "title-proc", "description-proc", "description-lot", "buyer-name",
          "buyer-country",
          "publication-date", "classification-cpv", "notice-type"]


def _pick(multilang, prefer=("eng",)) -> str:
    """TED text fields are {lang: text or [texts]}; prefer English, else the first language."""
    if not multilang:
        return ""
    if isinstance(multilang, str):
        return multilang
    for lang in prefer:
        if lang in multilang:
            v = multilang[lang]
            return " ".join(v) if isinstance(v, list) else v
    v = next(iter(multilang.values()))
    return " ".join(v) if isinstance(v, list) else v


class TedCollector(Collector):
    name = "ted"

    def build_query(self, query: str) -> str:
        q = f"classification-cpv IN ({' '.join(SECURITY_CPV)}) AND notice-type IN (cn-standard cn-social)"
        if query and query.strip('"') not in ("security", "cybersecurity"):
            q += f" AND FT~({query})"
        if self.before:
            q += f" AND PD<{self.before.strftime('%Y%m%d')}"
        return q + " SORT BY publication-date DESC"

    min_interval = 2.0     # TED returns 429 when hit faster
    page_size = 100

    def collect(self, segment: str, query: str, limit: int = 50) -> Iterable[Signal]:
        """Newest notices first; pages through results until `limit` notices."""
        page, seen = 1, 0
        while seen < limit:
            size = min(self.page_size, limit - seen)
            data = self.request_json("POST", URL, json_body={
                "query": self.build_query(query), "fields": FIELDS, "limit": size, "page": page,
                "scope": "ALL", "paginationMode": "PAGE_NUMBER"})
            notices = data.get("notices", [])
            yield from self._parse(segment, query, notices)
            seen += len(notices)
            if len(notices) < size:
                break
            page += 1

    def _parse(self, segment: str, query: str, notices: list[dict]) -> Iterable[Signal]:
        for n in notices:
            buyers = n.get("buyer-name") or {}
            buyer = _pick(buyers)
            yield Signal(
                source=self.name,
                native_id=n["publication-number"],
                segment=segment,
                query=query,
                title=clean(_pick(n.get("title-proc")) or _pick(n.get("notice-title")), 300),
                body=clean(" ".join(filter(None, [_pick(n.get("description-proc")),
                                                  _pick(n.get("description-lot"))]))),
                url=f"https://ted.europa.eu/en/notice/-/detail/{n['publication-number']}",
                created_at=(n.get("publication-date") or "")[:10],
                # Engagement: a tender is one buyer with a budget; weight comes from audience.
                engagement=1,
                metadata={"buyer": buyer, "country": n.get("buyer-country"),
                          "cpv": sorted(set(n.get("classification-cpv") or [])),
                          "notice_type": n.get("notice-type")},
            )
