# Variant judge rubric

Used by the variant judge (Claude Code subagent, decision D19) in Phase 3. Input: three competing
concept variants for one opening (`ideas/variants/<opening>/v1..v3.json`), the opening's input
(`ideas/<opening>.input.json`) and the founder profile (`config/founder.yaml`).

Score each variant 1–5 (5 = best) on:

- **buyer_budget** — is there a named buyer with an existing budget line or a forcing function
  (regulation, audit, insurance, incident)? Evidence from the input counts more than assertion.
- **defensibility** — once it works, how hard is it for incumbents or open source to copy?
- **founder_fit** — can this solo, bootstrapped technical founder build it and win the first
  paying customers without capital or a sales team?
- **time_to_revenue** — how soon could it earn money (paid pilots and services count)?
- **risk** — 5 = lowest combined technical, legal and bundling risk.

Then pick the `winner` (usually the highest total; explain if not), list ideas worth `grafted`
from the losers, and write `reasoning` (≤ 120 words).

Finally write the final concept to `ideas/<opening>.json`: the winning variant with the grafted
ideas merged in, and one `revision_log` entry per graft (`[variant vN] what was taken`). Keep the
concept rubric's grounding rules.
