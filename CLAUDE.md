# gapfinder — working rules

This project finds unmet needs in the cybersecurity tools market, turns them into startup concepts
and stress-tests them with critic agents. The repository owner is the product manager.

## Follow the plan

- **Read [docs/ROADMAP.md](docs/ROADMAP.md) before starting work.** It is the source of truth.
  Work on the current phase only; don't start a phase whose predecessor's exit criteria aren't met.
- Scope, order or exit-criteria changes need the PM's approval and an entry in
  [docs/DECISIONS.md](docs/DECISIONS.md). Don't silently change the plan.
- Update the status tables in ROADMAP.md in the same commit as the work they describe.
- Record surprises from live runs (bad results, quota limits, API changes) in the phase's notes.

## Engineering

- Python ≥3.11, package `gapfinder/`. Run: `python -m gapfinder {collect,stats,export,sample,evaluate}`.
- Tests: `python -m pytest`. Must pass before every commit. New collectors and scoring logic get
  tests with canned API responses (no network in tests).
- Collectors use official APIs only, respect rate limits, and send no personal data.
- Never commit secrets or `data/*.db`. API keys go into the cloud environment as secrets.
- LLM work (filtering, idea generation, critics) runs as Claude Code subagents per decision D2;
  don't add an Anthropic API dependency without a decision entry.
- Relevance judging uses [docs/rubrics/relevance.md](docs/rubrics/relevance.md) via a fresh
  subagent that sees only the rubric and the data. Commit its labels and the `evaluate` report.
