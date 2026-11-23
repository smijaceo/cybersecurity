# Launch brief: QuietWin

> Verified Windows logging coverage for MSSPs on Wazuh: per-tenant audit-policy and Sysmon rollout, drift alerts and a monthly client evidence report.

- Status: **unvalidated** — panel verdict WEAK (mean 5.5, founder fit 7); not yet tested with real buyers.
- Riskiest assumption: Small MSSPs on Wazuh will pay per client tenant for verified, monitored Windows coverage and a client evidence report, rather than deploying free configs themselves.
- First test: Over two weeks, hold 15 short calls with Wazuh-running MSSPs from the founder's contacts and Wazuh/r/msp communities, showing a mock client evidence report and drift alert (slides, no product), asking what they use today and offering the $500 single-tenant pilot with payment up front.
- Success signal: At least 6 of 15 say they tried free configs (sysmon-modular, Yamato, Wazuh defaults) and still lack per-tenant verification or client reports, at least 4 say they would resell the report per client, and at least 2 pay the $500 pilot.
- Open fatal/major objections: 24; claims never to reuse: 3

`brief.json` validates against `gapfinder.schemas.LaunchBrief` (gapfinder commit `3788cea387d2`).
