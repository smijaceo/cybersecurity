# Relevance rubric

Used by the relevance judge (Claude Code subagent, decision D2) to label demand signals.
Phase 1 uses it to check collection quality; Phase 2 uses it as the relevance filter.

Each signal gets two labels.

## 1. `on_segment` — is this about the segment's problem space?

- **y**: the main subject is the segment as described in `config/segments.yaml`
  (e.g. for cloud-security: cloud posture, misconfiguration, cloud IAM, Kubernetes security).
- **n**: the segment term appears only in passing, or the main subject is something else
  (an OS compatibility issue that mentions AWS IAM once is `n`).

## 2. `need` — does it express an unmet or poorly met need?

- **y**: someone states a problem, pain, missing capability, cost or usability complaint,
  asks whether a tool exists, asks for an alternative, or requests a feature that would solve a
  security problem. Feature requests on a security tool count.
- **n**: news, announcements, product launches, tutorials, best-practice guides, general
  how-it-works questions with no sign of a gap, or bug reports unrelated to a missing capability.

`need` can only be `y` when `on_segment` is `y`.

## Output

One JSON object per signal: `{"id": ..., "on_segment": "y"|"n", "need": "y"|"n", "reason": "<= 15 words"}`.
Judge only what the text says; don't guess from engagement or source.
