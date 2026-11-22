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
| Environment setup script installs dependencies for new sessions | done (updated for Phase 2) |

**Exit criteria:** tests run in a fresh session with no manual setup. ✅

## Phase 1 — Demand collection · `done`

Collect posts, questions and issues where people express a need, for the four segments in
[`config/segments.yaml`](../config/segments.yaml) (decision D3).

| Deliverable | Status |
|---|---|
| Common `Signal` record + SQLite store (idempotent upsert) | done |
| Collector: Hacker News (Algolia API) | done |
| Collector: Stack Exchange (security.stackexchange.com) | done — weak source, see notes |
| Collector: GitHub issues | done |
| CLI: `collect`, `stats`, `export` | done |
| Full run across all 4 segments | done — 1,193 signals (2026-11-22) |
| Automated quality review (`sample` → relevance judge → `evaluate`, decision D8) | done — all segments pass, see [round 2](../reports/phase1/round2-review.md) |
| Collector: Reddit | moved to *Later / parked* (needs an OAuth app and credential) |

**Exit criteria** (review method changed by D8)
- All four segments collected from every enabled source. ✅
- The relevance judge labels the top 20 signals per segment against
  [docs/rubrics/relevance.md](rubrics/relevance.md); `gapfinder evaluate` passes when at least
  half of every segment's sample is on-segment. ✅ (round 2)
- Collection is repeatable: re-running updates engagement, doesn't duplicate rows. ✅ (tested)

**Notes from the first live run (appsec-supply-chain)**
- GitHub matched the words of unquoted terms separately and returned popular off-topic issues.
  Fixed by quoting phrase and term and restricting to `in:title,body`.
- Hacker News returned ~nothing for two quoted phrases; it now searches the quoted term only
  (85/85 results on-topic).
- Stack Exchange full-text search matched loose words ("secrets" → Messenger "Secret
  Conversations"). It now matches titles only: precise but few results. Unauthenticated quota is
  ~300 requests/day. Treat it as a supporting source.

**Full run (2026-11-22): 1,193 signals**

| Segment | GitHub | HN | Stack Exchange |
|---|---|---|---|
| appsec-supply-chain | 311 | 85 | 1 |
| cloud-security | 216 | 100 | 6 |
| identity-access | 194 | 94 | 5 |
| smb-security-ops | 115 | 36 | 30 |

- Most of the top signals belong to their segment, but many are news, guides or launches rather than
  stated needs. Separating the two is the Phase 2 relevance filter.
- GitHub still lets through long issues that mention a term only in passing (top cloud-security item:
  Homebrew's "macOS Big Sur compatibility"), and sorting by reactions pushes them up. Phase 2 must
  down-weight body-only matches.
- One GitHub rate-limit response during the run; the retry recovered it.

**Quality review (2026-11-22)**

| Segment | Round 1 on-segment | Round 2 on-segment | Need statements (round 2) |
|---|---|---|---|
| cloud-security | 13/20 | 13/20 (unchanged) | 5 |
| appsec-supply-chain | 18/20 | 18/20 (unchanged) | 7 |
| identity-access | 7/20 — **fail** | 17/20 | 5 |
| smb-security-ops | 12/20 | 12/20 (unchanged) | 6 |

- Round 1 failed identity-access: "access review" matched video-game and code reviews, and
  "privileged access" matched breach news. Round 2 replaced the terms (see
  `config/segments.yaml`) and re-collected only that segment.
- Only 25–35% of top signals are need statements. Ranking by engagement favours launches
  ("Show HN", "Launch HN"), essays and news. Phase 2's relevance filter must drop these before
  clustering, and should look past the top-engagement items.

## Phase 2 — Gap analysis · `done — awaiting PM sign-off on the report`

Turn raw signals into a ranked list of unmet needs, each with evidence.
Output: **[reports/gaps-2026-11-22.md](../reports/gaps-2026-11-22.md)**.

| Deliverable | Status | How (reused projects per D7) |
|---|---|---|
| Relevance filter | done | Rules drop launch/dead posts (43), then the relevance judge labels the other 1,094 in batches (`judge-prepare` → judge → `judge-import`). 225 need statements. |
| Need themes | done | BERTopic with the model2vec `potion-base-8M` backend (D9), outlier reduction at similarity ≥ 0.6. 16 themes; theme namer marked 8 coherent. Per-theme stability across 3 extra seeds. |
| Supply map | done — changed by D10 | GitHub repository search per theme (repo count, leader's stars, active top repos). Awesome-lists dropped from scoring. |
| Threat relevance | done — changed by D10 | ATT&CK candidates shortlisted with `potion-retrieval-32M`; threat mapper rates 0–3 and picks techniques. NVD keyword count shown, not scored. |
| Gap score | done | [config/scoring.yaml](../config/scoring.yaml): 0.40 demand + 0.35 supply gap + 0.25 threat, percentile ranks. |
| Gap report | done | `gapfinder gaps` → `reports/gaps-<date>.md` + `reports/phase2/gaps.json`. |

**Exit criteria**
- Each top gap links ≥ 5 real signals. ✅ (smallest coherent theme: 6)
- The PM agrees the report is credible. ⏳ waiting on PM.

**Pipeline** (all agent inputs and outputs committed under `reports/phase2/`):
`judge-prepare` → relevance judge → `judge-import` → `themes` → theme namer → `threat-prepare`
→ threat mapper → `gaps`.

**Results (2026-11-22)**

| # | Gap | Score | Statements | Stability |
|---|---|---|---|---|
| 1 | AWS role credentials for workloads | 0.731 | 11 | 0.41 ⚠ |
| 2 | Remediating vulnerable third-party dependencies | 0.688 | 18 | 0.76 |
| 3 | SBOM generation across build ecosystems | 0.559 | 31 | 0.74 |
| 4 | SCIM user provisioning for applications | 0.535 | 23 | 0.52 |
| 5 | Managing SIEM log noise and ingestion | 0.528 | 7 | 0.51 |
| 6 | IAM-based authentication in AWS service clients | 0.469 | 15 | 0.47 ⚠ |
| 7 | Dependency context for vulnerability impact | 0.361 | 6 | 0.73 |
| 8 | CycloneDX SBOM output and attestation | 0.130 | 6 | 1.00 |

**Notes and known limitations**
- Judge calibration: on the 69 signals labelled in both Phase 1 and Phase 2, the judges agreed
  on 64 `need` labels (93%) and 65 `on_segment` labels (94%). The highest-engagement batch leaned
  slightly lenient (4 of 5 disagreements were n → y).
- Bug found and fixed: signals with negative engagement (down-voted Stack Exchange questions)
  were skipped by export, sampling and judging. One signal was affected; it couldn't have been
  in the Phase 1 samples.
- Theme stability is moderate (adjusted Rand index 0.44–0.66 between seeds), as expected for
  225 short texts. The report shows per-theme stability and flags themes below 0.5.
- Half the themes were incoherent. Notably secrets scanning: only ~4 of its statements were
  about secrets, so it isn't ranked. SMB security ops contributed only one coherent theme
  (21 need statements in total).
- The awesome-lists contain no SBOM tools, no Dependabot/Renovate and one SCIM entry, so they
  can't measure supply for these themes; embedding matches against them were noise (D10).
- Supply depends on the namer's search query: `sbom generation` misses Syft, which is tagged
  `sbom`. GitHub search also returns some off-topic repos (e.g. for "vulnerability impact").
- The ATT&CK shortlist sometimes misses the obvious technique (T1078 Valid Accounts for SCIM,
  T1552.001 Credentials In Files for AWS keys). The mapper's 0–3 rating doesn't depend on it.
- Most evidence comes from GitHub feature requests on specific projects, so several gaps are
  "projects keep being asked for X" rather than "no product does X". The Phase 4 competitor
  critic must test that.

## Phase 3 — Idea generation · `not started` (next, after PM sign-off)

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
- Reddit collector (needs a Reddit OAuth app and a credential stored on the environment).
