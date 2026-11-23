"""Schemas for every agent's output (pydantic, decision D7).

Each agent step writes JSON Lines; `load_jsonl` validates every line against its model and
reports the line number on failure. Cross-file checks (coverage of all inputs, technique IDs
being among the candidates) stay with the caller.
"""

from __future__ import annotations

from pathlib import Path
from typing import Literal, TypeVar

from pydantic import BaseModel, ConfigDict, Field, ValidationError, model_validator

Url = Field(pattern=r"^https?://\S+$")
YN = Literal["y", "n"]
Rating = Literal[0, 1, 2, 3]


class Strict(BaseModel):
    model_config = ConfigDict(extra="forbid")


class RelevanceLabel(Strict):
    id: str
    on_segment: YN
    need: YN
    reason: str = ""

    @model_validator(mode="after")
    def need_requires_on_segment(self):
        if self.need == "y" and self.on_segment == "n":
            raise ValueError("need=y requires on_segment=y")
        return self


class ThemeName(Strict):
    theme_id: int
    coherent: YN
    name: str
    need: str
    search_query: str
    reason: str = ""


class ThreatMapping(Strict):
    theme_id: int
    techniques: list[str] = Field(max_length=3)
    threat_relevance: Rating
    reason: str = ""


class Vendor(Strict):
    name: str
    url: str
    offering: str
    pricing: str
    segment: str
    source: str = Url


class PaidMarketGap(Strict):
    gap: str
    evidence: str = Url


class MarketResearch(Strict):
    theme_id: int
    vendors: list[Vendor] = Field(max_length=8)
    crowdedness: Rating
    paid_market_gaps: list[PaidMarketGap] = Field(max_length=4)
    willingness_to_pay: Rating
    wtp_evidence: str
    wtp_sources: list[str] = Field(min_length=1, max_length=3)
    bundling_risk: Literal["low", "medium", "high"]
    bundling_note: str
    summary: str

    @model_validator(mode="after")
    def sources_are_urls(self):
        bad = [u for u in self.wtp_sources if not u.startswith(("http://", "https://"))]
        if bad:
            raise ValueError(f"wtp_sources must be URLs: {bad}")
        return self


class FactCheckProblem(Strict):
    theme_id: int
    claim: str
    issue: str


class FactCheck(Strict):
    round: int = Field(ge=1)
    checked: int = Field(ge=0)
    problems: list[FactCheckProblem]


# ---------------------------------------------------------------- Phase 3 concepts

class Sourced(Strict):
    claim: str
    url: str = Url


class Feature(Strict):
    feature: str
    why: str


class Competitor(Strict):
    name: str
    url: str = Url
    how_we_differ: str


class Comparable(Strict):
    vendor: str
    price: str
    source: str = Url


class Buyer(Strict):
    role: str
    company_profile: str


class Problem(Strict):
    summary: str
    evidence: list[Sourced] = Field(min_length=3, max_length=8)


class WhyNow(Strict):
    summary: str
    sources: list[str] = Field(min_length=1)


class Mvp(Strict):
    features: list[Feature] = Field(min_length=3, max_length=7)
    out_of_scope: list[str] = Field(min_length=1)


class Build(Strict):
    team: str
    months_to_mvp: int = Field(ge=1, le=36)
    hardest_parts: list[str] = Field(min_length=2, max_length=5)


class Pricing(Strict):
    model: str
    entry_price: str
    rationale: str
    comparables: list[Comparable] = Field(min_length=2, max_length=6)


class GoToMarket(Strict):
    first_customers: str
    channel: str
    wedge: str


class RiskiestAssumption(Strict):
    assumption: str
    test: str
    success_signal: str


class Concept(Strict):
    opening_id: str
    slug: str = Field(pattern=r"^[a-z0-9]+(-[a-z0-9]+)*$")
    name: str
    one_liner: str
    buyer: Buyer
    user: str
    problem: Problem
    why_now: WhyNow
    mvp: Mvp
    competitors: list[Competitor] = Field(min_length=3, max_length=8)
    differentiation: str
    build: Build
    pricing: Pricing
    go_to_market: GoToMarket
    risks: list[str] = Field(min_length=3, max_length=6)
    riskiest_assumption: RiskiestAssumption
    open_questions: list[str] = Field(min_length=1)

    @model_validator(mode="after")
    def why_now_sources_are_urls(self):
        bad = [u for u in self.why_now.sources if not u.startswith(("http://", "https://"))]
        if bad:
            raise ValueError(f"why_now.sources must be URLs: {bad}")
        return self


M = TypeVar("M", bound=BaseModel)


class SchemaError(ValueError):
    pass


def load_jsonl(path: str | Path, model: type[M]) -> list[M]:
    rows = []
    for n, line in enumerate(Path(path).read_text().splitlines(), 1):
        if not line.strip():
            continue
        try:
            rows.append(model.model_validate_json(line))
        except ValidationError as exc:
            first = exc.errors()[0]
            loc = ".".join(str(p) for p in first["loc"])
            raise SchemaError(f"{Path(path).name} line {n}: {loc}: {first['msg']}") from None
    return rows
