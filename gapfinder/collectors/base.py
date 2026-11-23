"""Shared HTTP behaviour for collectors: timeouts, retries, polite rate limiting."""

from __future__ import annotations

import logging
import time
from datetime import date, datetime, timezone
from typing import Iterable

import requests

from ..models import Signal

log = logging.getLogger(__name__)

USER_AGENT = "gapfinder/0.1 (market research; contact via repository)"


class Collector:
    name: str = "base"
    min_interval: float = 1.0  # seconds between requests to this source

    supports_before = True  # False for sources with no history (e.g. live job boards)

    def __init__(self, session: requests.Session | None = None, sleep=time.sleep,
                 before: date | None = None):
        """`before`: only collect items created before this date (used by the backtest, D18)."""
        if before and not self.supports_before:
            raise ValueError(f"{self.name} has no history; it can't collect before {before}")
        self.before = before
        self.session = session or requests.Session()
        self.session.headers.setdefault("User-Agent", USER_AGENT)
        self._sleep = sleep
        self._last = 0.0

    def get_json(self, url: str, params: dict, retries: int = 3) -> dict:
        for attempt in range(retries):
            wait = self.min_interval - (time.monotonic() - self._last)
            if wait > 0:
                self._sleep(wait)
            self._last = time.monotonic()
            resp = self.session.get(url, params=params, timeout=30)
            if resp.status_code in (429, 403) and attempt < retries - 1:
                delay = self.backoff(resp, attempt)
                log.warning("%s: HTTP %s, backing off %.0fs", self.name, resp.status_code, delay)
                self._sleep(delay)
                continue
            resp.raise_for_status()
            return resp.json()
        raise RuntimeError(f"{self.name}: retries exhausted for {url}")

    def backoff(self, resp: requests.Response, attempt: int) -> float:
        retry_after = resp.headers.get("Retry-After")
        if retry_after and retry_after.isdigit():
            return min(float(retry_after), 120)
        return min(10 * 2**attempt, 120)

    def before_ts(self) -> int | None:
        if not self.before:
            return None
        return int(datetime(self.before.year, self.before.month, self.before.day,
                            tzinfo=timezone.utc).timestamp())

    def collect(self, segment: str, query: str, limit: int) -> Iterable[Signal]:
        raise NotImplementedError
