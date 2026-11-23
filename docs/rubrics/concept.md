# Startup concept rubric

Used by the concept writer (Claude Code subagent, decision D2) in Phase 3. Input: one opening
from `config/shortlist.yaml` with its need statements, the fact-checked paid-market research for
its themes (vendors, prices, gaps, willingness to pay, bundling risk), threat mapping, and the
claims the fact-checker flagged as unsupported.

Write a concept a founder could act on and a skeptic could attack. It's a commercial product
(decision D4). Be concrete: name the buyer, the price, the first ten customers' profile.

## Grounding rules (checked by code)

- `problem.evidence` URLs must come from the input: need statements or market sources.
- `pricing.comparables` must come from the input market research (it has been fact-checked).
- Don't reuse any claim listed under `flagged_claims` unless you re-verified it from a primary
  source and cite that source.
- New facts (e.g. in `why_now` or `competitors`) need a source URL you opened. Use WebFetch, or
  `python -m gapfinder fetch [--render] URL` if WebFetch fails.

## Fields

- `opening_id`, `slug` (kebab-case), `name` (working product name), `one_liner` (≤ 25 words).
- `buyer` — who signs the cheque: `role`, `company_profile` (size, industry, situation).
- `user` — who uses it day to day.
- `problem` — `summary` (≤ 80 words) and `evidence`: 3–8 items `{claim, url}`.
- `why_now` — `summary` and `sources` (URLs): regulation, market shift, pricing change.
- `mvp` — `features`: 3–7 items `{feature, why}`; `out_of_scope`: what v1 deliberately skips.
- `competitors` — 3–8 items `{name, url, how_we_differ}`; include the closest paid vendors and
  the free/bundled alternative.
- `differentiation` — ≤ 80 words: why a buyer picks this over the competitors above.
- `build` — `team` (e.g. "2 engineers + 1 founder-seller"), `months_to_mvp` (integer),
  `hardest_parts` (2–5 items).
- `pricing` — `model`, `entry_price` (concrete, e.g. "$X/month for up to N products"),
  `rationale`, `comparables`: 2–6 items `{vendor, price, source}` from the input research.
- `go_to_market` — `first_customers` (profile of the first ten), `channel`, `wedge`.
- `risks` — 3–6 items: business, technical, bundling, regulatory.
- `riskiest_assumption` — `assumption`, `test` (a cheap experiment, ≤ 2 weeks, no product
  build), `success_signal` (a measurable threshold).
- `open_questions` — what this concept can't answer yet.

Output one JSON object to the given path; validate with the command in your task.
