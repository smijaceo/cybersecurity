from __future__ import annotations

from datetime import date

import pytest

from gapfinder.collectors import COLLECTORS, GitHubIssuesCollector, HackerNewsCollector, JobsCollector, TedCollector
from gapfinder.collectors.stackexchange import StackExchangeCollector
from gapfinder.models import audience
from tests.test_collectors import FakeResponse, FakeSession, no_sleep


class PostSession(FakeSession):
    def post(self, url, json=None, timeout=None):
        self.calls.append((url, json))
        return self.responses.pop(0)


def test_ted_query_and_parsing():
    payload = {"notices": [{
        "publication-number": "123-2026",
        "title-proc": {"ces": "Pořízení SIEM"}, "notice-title": {"eng": "Czechia-Prague: Software"},
        "description-proc": {"eng": "Procurement of a SIEM"}, "description-lot": {"ces": ["Lot 1"]},
        "buyer-name": {"ces": ["Město Praha"]}, "buyer-country": ["CZE"],
        "publication-date": "2026-11-23+01:00", "classification-cpv": ["48730000", "48730000"],
        "notice-type": "cn-standard"}]}
    session = PostSession(FakeResponse(payload))
    c = TedCollector(session=session, sleep=no_sleep, before=date(2020, 1, 1))
    (sig,) = list(c.collect("smb-security-ops", '"SIEM"', 10))
    q = session.calls[0][1]["query"]
    assert "classification-cpv IN (48730000" in q and 'FT~("SIEM")' in q
    assert "PD<20200101" in q and q.endswith("SORT BY publication-date DESC")
    assert sig.id == "ted:123-2026" and sig.title == "Pořízení SIEM"   # procedure title over generic
    assert sig.body == "Procurement of a SIEM Lot 1"
    assert sig.metadata["buyer"] == "Město Praha" and sig.metadata["cpv"] == ["48730000"]
    assert sig.created_at == "2026-11-23"


def test_ted_generic_term_adds_no_fulltext():
    assert "FT~" not in TedCollector(session=PostSession()).build_query('"security"')


def test_jobs_hn_threads_and_remotive():
    threads = {"hits": [{"objectID": "900", "title": "Ask HN: Who is hiring? (November 2026)"},
                        {"objectID": "901", "title": "Ask HN: Who wants to be hired?"}]}
    hn = {"hits": [{"objectID": "5", "comment_text": "Acme | Security Engineer | build SIEM detections",
                    "created_at_i": 1795000000, "story_id": 900}]}
    remotive = {"jobs": [{"id": 7, "title": "SOC Analyst", "company_name": "Beta",
                          "description": "<p>Triage alerts manually</p>", "url": "https://r/7",
                          "publication_date": "2026-11-01T10:00:00", "tags": ["siem"]}]}
    session = FakeSession(FakeResponse(threads), FakeResponse(hn), FakeResponse(remotive))
    sigs = list(JobsCollector(session=session, sleep=no_sleep).collect("s", '"SIEM"', 10))
    assert [s.native_id for s in sigs] == ["hn-5", "remotive-7"]
    assert session.calls[1][1]["tags"] == "comment,(story_900)"   # only "Who is hiring" threads
    assert sigs[0].title == "Acme" and sigs[1].body == "Triage alerts manually"


def test_jobs_backtest_skips_live_board():
    threads = {"hits": [{"objectID": "800", "title": "Ask HN: Who is hiring? (May 2019)"}]}
    session = FakeSession(FakeResponse(threads), FakeResponse({"hits": []}))
    c = JobsCollector(session=session, sleep=no_sleep, before=date(2020, 1, 1))
    assert list(c.collect("s", "SIEM", 10)) == []
    assert len(session.calls) == 2 and "created_at_i<" in session.calls[0][1]["numericFilters"]


def test_before_filters_on_existing_collectors():
    hn = FakeSession(FakeResponse({"hits": []}))
    list(HackerNewsCollector(session=hn, sleep=no_sleep, before=date(2020, 1, 1)).collect("s", "q", 5))
    assert hn.calls[0][1]["numericFilters"] == "created_at_i<1577836800"
    gh = FakeSession(FakeResponse({"items": []}))
    list(GitHubIssuesCollector(session=gh, sleep=no_sleep, token="", before=date(2020, 1, 1)).collect("s", "q", 5))
    assert gh.calls[0][1]["q"].endswith("created:<2020-01-01")
    se = FakeSession(FakeResponse({"items": []}))
    list(StackExchangeCollector(session=se, sleep=no_sleep, before=date(2020, 1, 1)).collect("s", "q", 5))
    assert se.calls[0][1]["todate"] == 1577836800


def test_serverfault_is_its_own_source_and_audiences():
    assert COLLECTORS["serverfault"]().name == "serverfault"
    assert [audience(s) for s in ("github", "serverfault", "ted", "jobs", "regulation")] == [
        "developer", "practitioner", "buyer", "buyer", "buyer"]


def test_import_regulations(tmp_path):
    import json

    from gapfinder.cli import main
    from gapfinder.store import Store

    rows = [{"regulation": "EU CRA", "jurisdiction": "EU", "obligation": "Report exploited vulns in 24h",
             "applies_to": "manufacturers", "effective": "2026-09-11", "segment": "appsec-supply-chain",
             "source": "https://eur-lex.europa.eu/eli/reg/2024/2847/oj", "article": "Art. 14"}]
    f = tmp_path / "r.jsonl"
    f.write_text("\n".join(json.dumps(r) for r in rows))
    db = tmp_path / "s.db"
    assert main(["--db", str(db), "import-regulations", str(f)]) == 0
    (sig,) = list(Store(db).iter_signals())
    assert sig["source"] == "regulation" and sig["created_at"] == "2026-09-11"
    rows[0]["segment"] = "nope"
    f.write_text(json.dumps(rows[0]))
    assert main(["--db", str(db), "import-regulations", str(f)]) == 2
    rows[0]["segment"], rows[0]["effective"] = "appsec-supply-chain", "Sept 2026"
    f.write_text(json.dumps(rows[0]))
    assert main(["--db", str(db), "import-regulations", str(f)]) == 2
