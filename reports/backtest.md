# Backtest — does the method work?

Pre-registered in [config/backtest.yaml](../config/backtest.yaml) before any run (decision D18).

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

