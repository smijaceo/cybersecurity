"""Text helpers."""

from __future__ import annotations

import html
import re

_TAG = re.compile(r"<[^>]+>")
_WS = re.compile(r"\s+")

MAX_BODY = 4000


def clean(text: str | None, limit: int = MAX_BODY) -> str:
    """Strip HTML tags and entities, collapse whitespace, truncate."""
    if not text:
        return ""
    text = _TAG.sub(" ", text)
    text = html.unescape(text)
    text = _WS.sub(" ", text).strip()
    return text[:limit]
