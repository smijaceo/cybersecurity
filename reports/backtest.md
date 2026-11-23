# Backtest — does the method work?

Pre-registered in [config/backtest.yaml](../config/backtest.yaml) before any run (decision D18).

## Gap finder (data before 2020-01-01, open discovery only)

- Recall@10: **0.222** — verified categories found in the top 10 themes: compliance-automation, software-supply-chain
- Found at any rank: compliance-automation, software-supply-chain
- Precision@10: **0.222** (share of top themes matching a category)
- Categories kept after date verification: api-security, browser-security, cloud-posture-agentless, compliance-automation, data-security-posture, identity-threat-detection, non-human-identity, software-supply-chain, zero-trust-mesh-vpn
- Dropped (already funded before the cutoff): secrets-in-code
- Coherent themes ranked: 9

## Critic panel calibration

- **AUC 0.781** for the panel mean (0.5 = chance, 1.0 = perfect separation of later successes from failures).

| Lens | AUC |
|---|---|
| market-skeptic | 0.75 |
| competitor-analyst | 0.75 |
| security-practitioner | 0.812 |
| technical-feasibility | 0.75 |
| gtm-pricing | 0.75 |
| legal-ethics | 0.25 |
| economic-buyer | 0.531 |
| defensibility | 0.75 |

| Concept | Outcome | Company (revealed after scoring) | Panel mean |
|---|---|---|---|
| cal-04 | success | Demisto | 6 |
| cal-02 | success | Bridgecrew | 5.88 |
| cal-08 | success | Vulcan Cyber | 5.88 |
| cal-03 | failure | Datree | 5.5 |
| cal-05 | failure | Hysolate | 5.5 |
| cal-01 | failure | Blue Hexagon | 5.38 |
| cal-06 | failure | ShieldX Networks | 5 |
| cal-07 | success | Vdoo | 5 |

Limitation: the model may recognise well-known companies despite anonymisation; report it.


## Interpretation (2026-11-23)

**Gap finder.** From 901 pre-2020 signals (208 need statements, 9 coherent themes) the
pipeline found 2 of 9 verified categories: compliance automation (rank 4, high-confidence
match — about two years before Vanta's and Drata's Series A) and, partially, software supply
chain (rank 5, medium). It missed every technology-shift category (agentless cloud posture,
zero-trust mesh VPN, API security, browser security, DSPM, non-human identity, ITDR): people
don't post pain about categories that don't exist yet. **The method finds pain- and
compliance-driven markets and is blind to technology-driven ones.** Small sample: 9 categories,
9 themes.

**Critic panel.** Direction is right (AUC 0.781: three of four successes scored above every
failure), but with 4 + 4 companies it is not statistically reliable (one-sided exact
Mann-Whitney p = 0.171). Scores are compressed: all eight companies scored 5.0–6.0, including
Demisto (acquired for about $560M), so **no eventual success would pass the GO threshold of 7**.
The current concepts (5.33–5.83) sit inside the range of eventual successes. Per lens,
legal-ethics was inverted (0.25) and economic-buyer at chance (0.53) — a flag, not yet grounds
to reweight on eight companies. A name check found no critique naming the company it judged
(Demisto appears only as a period competitor in another company's critique); implicit
recognition can't be ruled out.
