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


# ---------------------------------------------------------------- regulation scout (D16)

class RegulationSignal(Strict):
    regulation: str            # e.g. "EU Cyber Resilience Act (Regulation 2024/2847)"
    jurisdiction: str          # e.g. "EU", "US federal", "US — New York"
    obligation: str            # what must be done or evidenced, in plain words
    applies_to: str            # who is obliged (size, sector, role)
    effective: str = Field(pattern=r"^\d{4}-\d{2}-\d{2}$")  # date the obligation applies
    segment: str               # segment key from config/segments.yaml
    source: str = Url          # primary text (official journal, regulator page)
    article: str = ""          # article/section reference


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
    revision_log: list[str] = Field(default_factory=list)  # Phase 4: what changed and why

    @model_validator(mode="after")
    def why_now_sources_are_urls(self):
        bad = [u for u in self.why_now.sources if not u.startswith(("http://", "https://"))]
        if bad:
            raise ValueError(f"why_now.sources must be URLs: {bad}")
        return self


class VariantScore(Strict):
    variant: Literal["v1", "v2", "v3"]
    angle: str                       # what makes this variant different
    buyer_budget: int = Field(ge=1, le=5)
    defensibility: int = Field(ge=1, le=5)
    founder_fit: int = Field(ge=1, le=5)
    time_to_revenue: int = Field(ge=1, le=5)
    risk: int = Field(ge=1, le=5)    # 5 = lowest risk
    note: str

    @property
    def total(self) -> int:
        return (self.buyer_budget + self.defensibility + self.founder_fit
                + self.time_to_revenue + self.risk)


class VariantJudgment(Strict):
    opening_id: str
    scores: list[VariantScore] = Field(min_length=3, max_length=3)
    winner: Literal["v1", "v2", "v3"]
    grafted: list[str] = Field(default_factory=list)   # ideas taken from the other variants
    reasoning: str

    @model_validator(mode="after")
    def winner_is_scored_and_variants_distinct(self):
        names = [v.variant for v in self.scores]
        if sorted(names) != ["v1", "v2", "v3"]:
            raise ValueError("score each of v1, v2, v3 exactly once")
        return self


# ---------------------------------------------------------------- backtest (D18)

class CategoryCheck(Strict):
    id: str
    keep: bool                       # False if the category was already funded before the cutoff
    evidence: list[str] = Field(min_length=1)   # URLs with founding / funding dates
    note: str

    @model_validator(mode="after")
    def urls(self):
        if not all(u.startswith(("http://", "https://")) for u in self.evidence):
            raise ValueError("evidence must be URLs")
        return self


class ThemeMatch(Strict):
    theme_id: int
    category: str | None             # pre-registered category id, or None
    confidence: Literal["high", "medium", "low"]
    note: str = ""


class CalibrationLabel(Strict):
    id: str                          # anonymised concept id, e.g. cal-01
    outcome: Literal["success", "failure"]
    company: str
    evidence: list[str] = Field(min_length=1)


# ---------------------------------------------------------------- Phase 4 critics

LENSES = ("market-skeptic", "competitor-analyst", "security-practitioner",
          "technical-feasibility", "gtm-pricing", "legal-ethics",
          "economic-buyer", "defensibility", "founder-fit")   # last three: decision D19
Lens = Literal["market-skeptic", "competitor-analyst", "security-practitioner",
               "technical-feasibility", "gtm-pricing", "legal-ethics",
               "economic-buyer", "defensibility", "founder-fit"]


class Objection(Strict):
    objection: str
    severity: Literal["fatal", "major", "minor"]
    evidence: str = ""

    @model_validator(mode="after")
    def serious_needs_evidence(self):
        if self.severity in ("fatal", "major") and not self.evidence.strip():
            raise ValueError(f"{self.severity} objection needs evidence")
        return self


class PriorResolution(Strict):
    objection: str
    resolved: bool
    note: str = ""


class Critique(Strict):
    concept_id: str
    lens: Lens
    round: int = Field(ge=1, le=3)
    score: int = Field(ge=1, le=10)
    verdict: Literal["go", "conditional", "no-go"]
    summary: str
    objections: list[Objection] = Field(min_length=1, max_length=6)
    strongest_point: str
    what_would_change_my_mind: list[str] = Field(min_length=1)
    resolved_prior: list[PriorResolution] = Field(default_factory=list)
    sources: list[str] = Field(default_factory=list)

    @model_validator(mode="after")
    def consistent(self):
        if self.verdict == "go" and (self.score < 7 or any(o.severity == "fatal"
                                                           for o in self.objections)):
            raise ValueError("verdict go needs score >= 7 and no fatal objection")
        if self.round == 1 and self.resolved_prior:
            raise ValueError("round 1 has no prior objections to resolve")
        if self.round > 1 and not self.resolved_prior:
            raise ValueError("round 2+ must say whether each prior objection was resolved")
        bad = [u for u in self.sources if not u.startswith(("http://", "https://"))]
        if bad:
            raise ValueError(f"sources must be URLs: {bad}")
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
