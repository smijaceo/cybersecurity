# Decision log

Decisions that shape scope. New decisions are appended; superseded ones are marked, not deleted.

| ID | Date | Decision | Why | Revisit when |
|---|---|---|---|---|
| D1 | 2026-11-22 | **Free data sources only** (HN, GitHub, Stack Exchange, NVD, CISA KEV). No paid keyword-volume APIs. | Prove the signal is useful before spending. | Phase 5, or if free signals are too thin. |
| D2 | 2026-11-22 | **Claude Code runs the LLM work** (relevance filtering, idea generation, critics) as subagents in sessions. No API key yet; the Python package handles data collection and scoring. | No API key or spend needed to start. | When the pipeline needs to run unattended. |
| D3 | 2026-11-22 | **First scan covers 4 segments**: cloud security, appsec & software supply chain, identity & access, SMB security operations. | Sharper signal than the whole market. | After the Phase 2 gap report. |
| D4 | 2026-11-22 | **Target is a startup / commercial product.** Critics weigh willingness to pay, go-to-market and competition. | PM's goal. | — |
| D5 | 2026-11-22 | **Dedicated `cybersecurity` cloud environment** (personal) allowing hn.algolia.com, api.stackexchange.com, services.nvd.nist.gov, www.cisa.gov, raw.githubusercontent.com. | The Default environment blocked these, and it's shared by all repositories. | When a new data source is added. |
| D6 | 2026-11-22 | **Use official APIs only**; no scraping of sites whose terms forbid it (e.g. G2). | Legal and reliability. | — |
| D7 | 2026-11-22 | **Reuse existing open-source tools and data before writing our own.** Custom code is limited to glue, scoring and what no maintained project covers. Each phase lists the projects it builds on. | PM direction: don't reinvent the wheel. | — |
| D8 | 2026-11-22 | **Signal quality is checked by an automated relevance judge, not by manual PM review.** A Claude Code subagent labels the sample against a written rubric (`docs/rubrics/relevance.md`); `gapfinder evaluate` validates the labels and applies the pass threshold. Labels and reports are committed under `reports/` so anyone can audit them. | PM asked for the check to be automated instead of done by hand. A fixed rubric and a separate judge agent keep it independent of the collector code. | If spot-checks show the judge disagreeing with the PM. |
