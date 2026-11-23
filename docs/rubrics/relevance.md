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

## Source-specific rules (decision D16)

- **Open discovery** (`segment = open-discovery`): `on_segment = y` for any cybersecurity need.
- **Public tenders** (`source = ted`; text may be in any EU language — read it as is): a contract
  notice is a buyer formally procuring something. `need = y` when it procures a security
  capability in the segment (product, managed service, audit/testing); `n` for hardware-only
  purchases, generic IT, or when security is incidental.
- **Job postings** (`source = jobs`): `need = y` only when the posting shows recurring security
  work a product could take on or a gap the team is hiring around (e.g. "manually triage
  alerts", "build our vulnerability management program", "own SOC 2 evidence collection").
  A generic role description or a tool list alone is `n`.
- **Regulations** (`source = regulation`): `need = y` when the obligation requires an
  organisation in the segment to do or evidence something a product or service could support.

## Output

One JSON object per signal: `{"id": ..., "on_segment": "y"|"n", "need": "y"|"n", "reason": "<= 15 words"}`.
Judge only what the text says; don't guess from engagement or source.
