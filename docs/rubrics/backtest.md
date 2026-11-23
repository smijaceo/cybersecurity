# Backtest rubrics (decision D18)

Pre-registration lives in `config/backtest.yaml`. Never change it during a run.

## Category verifier

For ONE category in `config/backtest.yaml` (gap_finder.categories), check the example
companies' founding dates and first major funding (Series A or later) in primary or reputable
sources (company announcements, press, Crunchbase/Wikipedia pages you open). `keep = true` only
if the category's commercial wave came at or after the cutoff year — i.e. most examples were
founded or raised their first major round in or after that year. Output one JSON object:
`{id, keep, evidence: [URLs], note}` (note ≤ 40 words, with the dates you found).

## Theme matcher (blind)

Input: the backtest's ranked themes (`ranked.json`: name and need only) and the category
DEFINITIONS (not the example companies). For each theme decide which category it describes, if
any. Match on the need, not on shared words: "rotate leaked AWS keys" matches secrets-in-code;
"general AWS questions" matches nothing. `confidence`: high (clearly the same need), medium
(substantially overlaps), low (loosely related). Output one JSON object per theme:
`{theme_id, category, confidence, note}` with `category = null` for no match. Don't use outside
knowledge of which companies later succeeded.

## Calibration builder

Select companies by `panel_calibration.selection`: founded in the window; successes (acquired
for ≥ $100M or raised Series C+) and failures (shut down or sold for parts by 2025), each with
a cited source. Prefer security startups that fit the concept schema (B2B security products).
Pick from varied subsegments; don't pick only household names.

For each, write a founding-stage concept (`schemas.Concept` format) using only what was public
at founding: launch posts, early website via the Wayback Machine, seed announcements. No later
facts (customers, funding, outcomes). Replace company, product and founder names with neutral
ones; remove dates later than founding. Ids are `cal-01` … `cal-08`, in an order that doesn't
reveal outcomes (e.g. alphabetical by real name).

Write each concept to `backtest/calibration/<id>.json` and a minimal input file
`backtest/calibration/<id>.input.json`:
`{"opening_id": id, "priority": 0, "thesis": "", "themes": [], "flagged_claims": []}`.
Write the labels ONLY to `backtest/calibration-labels.jsonl`: `{id, outcome, company, evidence}`.
