"""Reference data for gap analysis: existing tools (supply) and threat context.

All sources are public and reused as-is (decision D7):
- awesome-lists on GitHub -> catalogue of existing tools
- GitHub repository search -> how many maintained open-source projects exist for a theme
- CISA Known Exploited Vulnerabilities -> what attackers are exploiting now
- MITRE ATT&CK enterprise techniques -> attacker behaviour a theme helps with
Downloads are cached in data/cache/ so repeated runs don't refetch.
"""

from __future__ import annotations

import json
import re
from datetime import datetime, timezone
from pathlib import Path

import requests

from .collectors.base import USER_AGENT, Collector

CACHE = Path(__file__).resolve().parent.parent / "data" / "cache"

_ENTRY = re.compile(r"^\s*[-*]\s+\[(?P<name>[^\]]+)\]\((?P<url>https?://[^)\s]+)\)\s*[-:–—]?\s*(?P<desc>.*)$")
_HEADING = re.compile(r"^(?P<level>#{2,6})\s+(?P<title>.+?)\s*$")
_REPO = re.compile(r"^https?://github\.com/([^/#?\s]+)/([^/#?\s]+?)(?:\.git)?/?$")


def _cached_get(url: str, cache_name: str, refresh: bool = False) -> bytes:
    CACHE.mkdir(parents=True, exist_ok=True)
    path = CACHE / cache_name
    if path.exists() and not refresh:
        return path.read_bytes()
    resp = requests.get(url, timeout=120, headers={"User-Agent": USER_AGENT})
    resp.raise_for_status()
    path.write_bytes(resp.content)
    return resp.content


# ---------------------------------------------------------------- supply side

def parse_awesome(markdown: str, list_name: str) -> list[dict]:
    """Extract `- [Name](url) - description` entries with their section path.

    Table-of-contents links (in-page anchors) are skipped because they aren't https URLs.
    """
    entries, sections = [], {}
    for line in markdown.splitlines():
        h = _HEADING.match(line)
        if h:
            level = len(h["level"])
            sections = {k: v for k, v in sections.items() if k < level}
            sections[level] = h["title"].strip("# ")
            continue
        m = _ENTRY.match(line)
        if not m:
            continue
        url = m["url"].rstrip(".,")
        repo = _REPO.match(url)
        entries.append({
            "name": m["name"].strip(),
            "url": url,
            "description": re.sub(r"\s+", " ", m["desc"]).strip()[:300],
            "section": " > ".join(sections[k] for k in sorted(sections)),
            "list": list_name,
            "github_repo": f"{repo[1]}/{repo[2]}" if repo else None,
        })
    return entries


def load_tool_catalog(config: dict, refresh: bool = False) -> list[dict]:
    """All awesome-list entries, de-duplicated by URL (first list wins)."""
    seen, catalog = set(), []
    for spec in config.get("awesome_lists", []):
        url = f"https://raw.githubusercontent.com/{spec['repo']}/{spec['branch']}/{spec['file']}"
        md = _cached_get(url, f"awesome__{spec['repo'].replace('/', '__')}.md", refresh).decode()
        for e in parse_awesome(md, spec["repo"]):
            if e["url"] not in seen:
                seen.add(e["url"])
                catalog.append(e)
    return catalog


class GitHubRepoSearch(Collector):
    """Repository search: how much maintained open-source supply exists for a query."""

    name = "github-repos"
    min_interval = 2.5  # search API allows 30/min with a token

    def __init__(self, *args, token: str | None = None, **kwargs):
        super().__init__(*args, **kwargs)
        import os
        token = token or os.environ.get("GITHUB_TOKEN")
        self.session.headers["Accept"] = "application/vnd.github+json"
        if token:
            self.session.headers["Authorization"] = f"Bearer {token}"
        else:
            self.min_interval = 6.5

    def supply(self, query: str, top: int = 10, now: datetime | None = None) -> dict:
        data = self.get_json("https://api.github.com/search/repositories",
                             {"q": f"{query} archived:false", "sort": "stars",
                              "order": "desc", "per_page": top})
        return summarize_repos(data, now)


def summarize_repos(data: dict, now: datetime | None = None) -> dict:
    now = now or datetime.now(timezone.utc)
    repos = []
    for r in data.get("items", []):
        pushed = datetime.fromisoformat(r["pushed_at"].replace("Z", "+00:00"))
        repos.append({"name": r["full_name"], "url": r["html_url"], "stars": r["stargazers_count"],
                      "days_since_push": (now - pushed).days})
    active = [r for r in repos if r["days_since_push"] <= 365]
    return {
        "total_repos": data.get("total_count", 0),
        "top_repos": repos,
        "top_stars": max((r["stars"] for r in repos), default=0),
        "active_top_repos": len(active),
    }


# ---------------------------------------------------------------- threat side

def load_kev(config: dict, refresh: bool = False) -> list[dict]:
    data = json.loads(_cached_get(config["threat_data"]["kev"], "kev.json", refresh))
    return [{
        "id": v["cveID"],
        "text": f"{v.get('vendorProject', '')} {v.get('product', '')}: "
                f"{v.get('vulnerabilityName', '')}. {v.get('shortDescription', '')}",
        "date_added": v.get("dateAdded", ""),
        "ransomware": v.get("knownRansomwareCampaignUse") == "Known",
    } for v in data.get("vulnerabilities", [])]


def parse_attack(bundle: dict) -> list[dict]:
    """Active (non-revoked, non-deprecated) enterprise techniques from a STIX bundle."""
    out = []
    for o in bundle.get("objects", []):
        if o.get("type") != "attack-pattern" or o.get("revoked") or o.get("x_mitre_deprecated"):
            continue
        ext = next((r for r in o.get("external_references", [])
                    if r.get("source_name") == "mitre-attack"), None)
        if not ext:
            continue
        desc = re.sub(r"\(Citation:[^)]*\)", "", o.get("description", ""))
        out.append({"id": ext["external_id"], "name": o["name"],
                    "text": f"{o['name']}. {desc[:500]}", "url": ext.get("url", "")})
    return out


def load_attack(config: dict, refresh: bool = False) -> list[dict]:
    return parse_attack(json.loads(_cached_get(config["threat_data"]["attack"],
                                               "enterprise-attack.json", refresh)))
