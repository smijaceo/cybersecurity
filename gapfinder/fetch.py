"""Read a web page as plain text for agents (decision D7: reuse trafilatura and Playwright).

Agents' built-in fetchers can fail on sites this machine reaches fine; agents fall back to
`python -m gapfinder fetch URL` (static pages) or `--render` (JavaScript-rendered pages such
as AWS Marketplace listings, where prices appear only after scripts run).
"""

from __future__ import annotations

from pathlib import Path

import requests
import trafilatura

BROWSER_UA = ("Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) "
              "Chrome/131.0 Safari/537.36")
MAX_CHARS = 20000


def extract(html: str) -> str:
    """Main text of a page (tables kept: pricing usually lives in them)."""
    text = trafilatura.extract(html, include_tables=True, include_links=False,
                               favor_recall=True) or ""
    return text.strip()


def fetch_static(url: str, timeout: int = 30) -> str:
    resp = requests.get(url, timeout=timeout, headers={"User-Agent": BROWSER_UA})
    resp.raise_for_status()
    return resp.text


# The cloud environment ships Chromium here; elsewhere Playwright's own download is used.
CHROMIUM = Path("/opt/pw-browsers/chromium")


def fetch_rendered(url: str, timeout_ms: int = 45000) -> str:
    from playwright.sync_api import sync_playwright

    with sync_playwright() as p:
        browser = p.chromium.launch(
            executable_path=str(CHROMIUM) if CHROMIUM.exists() else None)
        try:
            page = browser.new_page(user_agent=BROWSER_UA)
            page.goto(url, timeout=timeout_ms, wait_until="networkidle")
            return page.content()
        finally:
            browser.close()


def fetch_text(url: str, render: bool = False, max_chars: int = MAX_CHARS) -> str:
    html = fetch_rendered(url) if render else fetch_static(url)
    text = extract(html)
    if not render and len(text) < 300:
        # Probably a JavaScript app shell; render it.
        text = extract(fetch_rendered(url))
    return text[:max_chars] if max_chars else text
