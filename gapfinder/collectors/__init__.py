from functools import partial

from .github import GitHubIssuesCollector
from .hn import HackerNewsCollector
from .jobs import JobsCollector
from .stackexchange import StackExchangeCollector
from .ted import TedCollector

COLLECTORS = {
    "hn": HackerNewsCollector,
    "stackexchange": StackExchangeCollector,
    "serverfault": partial(StackExchangeCollector, site="serverfault"),
    "github": GitHubIssuesCollector,
    "ted": TedCollector,
    "jobs": JobsCollector,
}

__all__ = ["COLLECTORS", "GitHubIssuesCollector", "HackerNewsCollector", "StackExchangeCollector", "TedCollector", "JobsCollector"]
