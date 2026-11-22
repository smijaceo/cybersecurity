# Roadmap

**Goal:** find unmet needs in the cybersecurity tools market from public demand signals, turn the
strongest gaps into startup product concepts, and stress-test each concept against a panel of
critic agents until only defensible ideas remain.

**Product manager:** repository owner. **Implementer:** Claude Code sessions.

## Rules for changing this plan

1. This file is the source of truth. Work follows the phases in order; a phase starts only when the
   previous phase's exit criteria are met.
2. Changing scope, order or exit criteria needs the product manager's approval and an entry in
   [DECISIONS.md](DECISIONS.md). Implementation details inside a phase don't.
3. Every change to a status below is made in the same commit as the work it reports.
4. Code changes come with tests; `python -m pytest` passes before every commit.

Status values: `not started` · `in progress` · `done` · `blocked (reason)`

---

## Phase 0 — Foundation · `done`

| Deliverable | Status |
|---|---|
| Python package `gapfinder`, `pyproject.toml`, `.gitignore` | done |
| Cloud environment `cybersecurity` with the data-source hosts allowed | done |
| Plan, decision log, `CLAUDE.md` working rules | done |
| Environment setup script installs dependencies for new sessions | done |

**Exit criteria:** tests run in a fresh session with no manual setup. ✅

## Phase 1 — Demand collection · `in progress`

Collect posts, questions and issues where people express a need, for the four segments in
[`config/segments.yaml`](../config/segments.yaml) (decision D3).

| Deliverable | Status |
|---|---|
| Common `Signal` record + SQLite store (idempotent upsert) | done |
| Collector: Hacker News (Algolia API) | done |
| Collector: Stack Exchange (security.stackexchange.com) | done — weak source, see notes |
| Collector: GitHub issues | done |
| CLI: `collect`, `stats`, `export` | done |
| Full run across all 4 segments, results reviewed with PM | not started |
| Collector: Reddit (needs OAuth app + credential, decision pending) | not started |

**Exit criteria**
- All four segments collected from every enabled source.
- A sample of 20 top signals per segment is reviewed; at least half are on-topic.
- Collection is repeatable: re-running updates engagement, doesn't duplicate rows.

**Notes from the first live run (appsec-supply-chain)**
- GitHub matched the words of unquoted terms separately and returned popular off-topic issues.
  Fixed by quoting phrase and term and restricting to `in:title,body`.
- Hacker News returned ~nothing for two quoted phrases; it now searches the quoted term only
  (85/85 results on-topic).
- Stack Exchange full-text search matched loose words ("secrets" → Messenger "Secret
  Conversations"). It now matches titles only: precise but few results. Unauthenticated quota is
  ~300 requests/day. Treat it as a supporting source.

## Phase 2 — Gap analysis · `not started`

Turn raw signals into a ranked list of unmet needs, each with evidence.

Builds on existing projects (decision D7):

| Deliverable | Planned approach | Reused projects / data |
|---|---|---|
| Relevance filter: keep only real need statements ("I need / is there / we struggle / too expensive") | Rule-based pre-filter in code, then Claude Code subagent classification over exported JSONL (D2) | — |
| Need themes per segment | Topic modelling over the filtered signals | BERTopic, sentence-transformers (model download needs huggingface.co allowed: environment change, PM approval) |
| Supply map: existing tools per theme | Tools listed per theme, with stars and last-commit date as health signals | awesome-security, awesome-pentest, awesome-devsecops lists; GitHub repo search API |
| Threat relevance | Keyword overlap between themes and exploited vulnerabilities / techniques | CISA KEV feed, NVD API, MITRE ATT&CK STIX data (mitre/cti) |
| Gap score | demand (volume, growth) × pain × supply weakness × threat relevance; weights in config |
| Gap report | `reports/gaps-<date>.md`: top 10 gaps, score breakdown, evidence links |

**Exit criteria:** a gap report the PM agrees is credible; each top gap links ≥5 real signals.

## Phase 3 — Idea generation · `not started`

For each top gap, a structured startup concept (decision D4: commercial product) saved to
`ideas/<slug>.md`: target buyer and user, problem with evidence, MVP scope, differentiation vs the
supply map, build effort, pricing and business model, riskiest assumption.

**Exit criteria:** 3–5 concepts from the top gaps, each following the template.

## Phase 4 — Critic panel · `not started`

Claude Code subagents in `.claude/agents/` (decision D2), each with a fixed rubric, scoring 1–10
with objections and the evidence that would change their mind:

| Critic | Question it answers |
|---|---|
| Market skeptic | Is the demand real and large, or a few loud voices? |
| Competitor analyst | Who already does this, or could ship it next quarter? |
| Security practitioner | Would a real security team adopt it and trust it? |
| Technical feasibility | Can a small team build the MVP, and what's hard? |
| Go-to-market and pricing | Who pays, how much, and how do you reach them? |
| Legal and ethics | Dual-use risk, data handling, platform terms |

Process: critique → revise concept → re-score, at most 2 rounds. Panel output saved to
`ideas/<slug>.critique.md`.

**Exit criteria:** every concept has a scored critique; a ranked shortlist with a go/no-go
recommendation for the PM.

## Phase 5 — Validation loop · `not started`

Scheduled re-collection to track trends; compare critic predictions with real-world signals
(landing-page interest, community response). Paid search-volume data (DataForSEO/SerpAPI) is
reconsidered here (decision D1).

## Later / parked

- Automate idea generation and critics through the Claude API (requires an API key; D2 revisit).
- Reddit collector (OAuth app and credential).
