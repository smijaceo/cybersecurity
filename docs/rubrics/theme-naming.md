# Theme naming rubric

Used by the theme namer (Claude Code subagent, decision D2) in Phase 2. Input: each theme's
BERTopic keywords and up to 12 member need statements. Judge only from that text.

For each theme, decide:

- **coherent** — `y` if most statements describe the same underlying need, so one product could
  address them. `n` if they're unrelated needs grouped by surface words (e.g. all mention
  "GitHub issue" or "feature request" but ask for different things).
- **name** — 3–7 words naming the need, not a product. ("SBOM generation for container images",
  not "SBOM tool".)
- **need** — one sentence, in the users' terms: who struggles with what. Use only what the
  statements show; don't invent market facts.
- **search_query** — 2–4 plain words to search GitHub repositories and NVD for existing tools in
  this space (e.g. `scim provisioning`). No quotes or operators.
- **reason** — ≤ 15 words: why coherent or not.

Output one JSON object per theme, in input order:

```json
{"theme_id": 0, "coherent": "y", "name": "...", "need": "...", "search_query": "...", "reason": "..."}
```

Give an incoherent theme a name and need anyway (describe the mix); it is excluded from ranking.
