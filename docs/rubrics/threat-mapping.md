# Threat mapping rubric

Used by the threat mapper (Claude Code subagent, decision D2) in Phase 2. Input: each coherent
theme's name and need statement, plus up to 15 candidate MITRE ATT&CK techniques shortlisted by
embedding similarity. Candidates are only suggestions; most may be irrelevant.

For each theme:

- **techniques** — the candidate IDs (0–3) that a product meeting this need would directly help
  prevent, detect or limit. Choose only from the candidates. Pick none rather than a stretch.
- **threat_relevance** — integer 0–3:
  - 3: the need directly addresses a common, actively exploited attack path
    (e.g. compromised dependencies, stolen cloud credentials).
  - 2: it materially reduces exposure to a known technique, but indirectly
    (e.g. inventory or hygiene that enables faster response).
  - 1: weak or speculative security benefit; mostly operational or compliance.
  - 0: no meaningful link to attacker behaviour.
- **reason** — ≤ 20 words.

Output one JSON object per theme, in input order:

```json
{"theme_id": 0, "techniques": ["T1195.001"], "threat_relevance": 3, "reason": "..."}
```
