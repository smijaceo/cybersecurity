"""Collector parsing tests with canned API responses (no network)."""

from __future__ import annotations

from gapfinder.collectors import (
    GitHubIssuesCollector,
    HackerNewsCollector,
    StackExchangeCollector,
)


class FakeResponse:
    def __init__(self, payload, status=200, headers=None):
        self._payload = payload
        self.status_code = status
        self.headers = headers or {}

    def json(self):
        return self._payload

    def raise_for_status(self):
        if self.status_code >= 400:
            raise RuntimeError(f"HTTP {self.status_code}")


class FakeSession:
    def __init__(self, *responses):
        self.responses = list(responses)
        self.headers = {}
        self.calls = []

    def get(self, url, params=None, timeout=None):
        self.calls.append((url, params))
        return self.responses.pop(0)


def no_sleep(_):
    pass


def test_hn_story_and_comment():
    payload = {"hits": [
        {"objectID": "1", "_tags": ["story"], "title": "Ask HN: <b>CSPM</b> for startups?",
         "story_text": "Is there a tool &amp; cheap?", "points": 40, "num_comments": 12,
         "created_at_i": 1700000000},
        {"objectID": "2", "_tags": ["comment"], "story_title": "Parent",
         "comment_text": "<p>We gave up on it</p>", "created_at_i": 1700000001},
    ]}
    c = HackerNewsCollector(session=FakeSession(FakeResponse(payload)), sleep=no_sleep)
    story, comment = list(c.collect("cloud-security", "CSPM", 10))
    assert story.id == "hn:1"
    assert story.title == "Ask HN: CSPM for startups?"
    assert story.body == "Is there a tool & cheap?"
    assert story.engagement == 52
    assert story.created_at.startswith("2023-11-14")
    assert comment.metadata["kind"] == "comment"
    assert comment.body == "We gave up on it"
    assert comment.engagement == 0


def test_stackexchange_engagement_and_unanswered_flag():
    payload = {"items": [{"question_id": 9, "title": "SBOM tool?", "body": "<p>Need one</p>",
                          "link": "https://security.stackexchange.com/q/9", "score": 3,
                          "answer_count": 0, "view_count": 1250, "is_answered": False,
                          "creation_date": 1700000000, "tags": ["sbom"]}],
               "quota_remaining": 299}
    session = FakeSession(FakeResponse(payload))
    c = StackExchangeCollector(session=session, sleep=no_sleep)
    (sig,) = list(c.collect("appsec-supply-chain", "SBOM", 10))
    assert session.calls[0][1]["title"] == "SBOM"
    assert sig.id == "stackexchange:security:9"
    assert sig.engagement == 3 + 0 + 12
    assert sig.metadata["is_answered"] is False


def test_github_retries_after_rate_limit():
    ok = {"items": [{"id": 77, "title": "Secrets scanning mode", "body": "please",
                     "html_url": "https://github.com/o/r/issues/1",
                     "repository_url": "https://api.github.com/repos/o/r",
                     "created_at": "2026-01-01T00:00:00Z", "comments": 4,
                     "reactions": {"total_count": 10}, "state": "open",
                     "labels": [{"name": "enhancement"}]}]}
    session = FakeSession(FakeResponse({}, 403, {"Retry-After": "1"}), FakeResponse(ok))
    c = GitHubIssuesCollector(session=session, sleep=no_sleep, token="")
    (sig,) = list(c.collect("appsec-supply-chain", "secrets scanning", 10))
    assert len(session.calls) == 2
    assert session.calls[0][1]["q"] == "secrets scanning in:title,body is:issue"
    assert sig.engagement == 14
    assert sig.metadata["repo"] == "o/r"
    assert sig.metadata["labels"] == ["enhancement"]
