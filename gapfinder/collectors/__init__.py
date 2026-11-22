from .github import GitHubIssuesCollector
from .hn import HackerNewsCollector
from .stackexchange import StackExchangeCollector

COLLECTORS = {
    "hn": HackerNewsCollector,
    "stackexchange": StackExchangeCollector,
    "github": GitHubIssuesCollector,
}

__all__ = ["COLLECTORS", "GitHubIssuesCollector", "HackerNewsCollector", "StackExchangeCollector"]
