from __future__ import annotations

from datetime import datetime, timezone

from gapfinder import refdata

MD = """# Awesome X
- [Network](#network)
## Network
### Scanning
- [nmap](https://github.com/nmap/nmap) - Network scanner.
* [Site](https://example.com/tool): A hosted tool
## Identity
- [Keycloak](https://github.com/keycloak/keycloak.git/) – IAM server
"""


def test_parse_awesome_sections_and_repos():
    e = refdata.parse_awesome(MD, "o/awesome-x")
    assert [x["name"] for x in e] == ["nmap", "Site", "Keycloak"]  # TOC anchor skipped
    assert e[0]["section"] == "Network > Scanning"
    assert e[0]["github_repo"] == "nmap/nmap"
    assert e[0]["description"] == "Network scanner."
    assert e[1]["github_repo"] is None and e[1]["description"] == "A hosted tool"
    assert e[2]["section"] == "Identity"  # deeper heading from previous section dropped
    assert e[2]["github_repo"] == "keycloak/keycloak"


def test_parse_attack_skips_revoked_and_deprecated():
    bundle = {"objects": [
        {"type": "attack-pattern", "name": "Phishing", "description": "Send mail (Citation: X)",
         "external_references": [{"source_name": "mitre-attack", "external_id": "T1566",
                                  "url": "u"}]},
        {"type": "attack-pattern", "name": "Old", "revoked": True, "external_references": []},
        {"type": "attack-pattern", "name": "Dep", "x_mitre_deprecated": True,
         "external_references": [{"source_name": "mitre-attack", "external_id": "T9"}]},
        {"type": "malware", "name": "Not a technique"},
    ]}
    (t,) = refdata.parse_attack(bundle)
    assert (t["id"], t["name"]) == ("T1566", "Phishing")
    assert "Citation" not in t["text"]


def test_summarize_repos():
    now = datetime(2026, 11, 22, tzinfo=timezone.utc)
    data = {"total_count": 42, "items": [
        {"full_name": "a/b", "html_url": "u1", "stargazers_count": 900, "pushed_at": "2026-10-01T00:00:00Z"},
        {"full_name": "c/d", "html_url": "u2", "stargazers_count": 50, "pushed_at": "2023-01-01T00:00:00Z"},
    ]}
    s = refdata.summarize_repos(data, now)
    assert (s["total_repos"], s["top_stars"], s["active_top_repos"]) == (42, 900, 1)
    assert s["top_repos"][1]["days_since_push"] > 365
