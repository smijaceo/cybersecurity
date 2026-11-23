# QuietWin

> Verified Windows logging coverage for MSSPs on Wazuh: per-tenant audit-policy and Sysmon rollout, drift alerts and a monthly client evidence report.

Opening `msp-windows-detection` (priority 1) · from User activity audit logging on servers (theme 4, stability 0.76), SIEM log collection and noise filtering (theme 16, stability 0.94), Ransomware detection and recovery for file servers (theme 33, stability 1.0)

## Buyer and user

- **Buyer:** Owner or security lead of a small MSSP / security-focused MSP — MSSP or security MSP with 2-15 analysts running self-hosted Wazuh or Wazuh Cloud for 10-150 SMB clients with Windows servers (DCs, file servers, RDS hosts); sells a monthly security service and must show clients what is monitored. Sentinel-based MSSPs are a second segment, added only on paid demand.
- **User:** The MSSP's detection engineer or senior analyst who rolls packs out per tenant and watches coverage drift; account managers who hand the monthly per-client evidence report to the client.

## Problem

Small MSSPs run Wazuh with default Windows collection: audit policy is often left at defaults, Sysmon is missing or unmanaged, and nobody notices when a GPO, agent update or full log overwrites coverage. Noisy channels flood the indexer while logon, RDP and admin-change evidence is missing when a client asks. Free configs exist, but rolling them out, verifying them per tenant and proving coverage to clients is unpaid manual work.

- Admins ask for a simple way to track terminal server logins, session durations, disconnections and failed logons and cannot find one (2009 question, still among the most-engaged). ([source](https://serverfault.com/questions/13451/terminal-server-logging))
- Windows file-server object auditing forwarded to Graylog floods the collector with noise from routine access, burying the events the admin wanted. ([source](https://serverfault.com/questions/1078821/windows-server-audit-logs))
- Teams are told to pre-filter logs before the SIEM to save money and ask what detection risk that creates. ([source](https://security.stackexchange.com/questions/41068/siem-log-pre-filtering-question))
- In a survey of senior IT leaders (not MSSP-specific), teams report dropping logs to control cost, creating blind spots. ([source](https://www.helpnetsecurity.com/2026/06/19/report-log-management-security-risk/))
- Admins running OSSEC (Wazuh's ancestor) across hundreds of servers want correlation and security value without a full SIEM. ([source](https://serverfault.com/questions/539342/ossec-as-a-siem))
- Admins are asked to produce domain-controller audit trails of who changed what and look for tooling to do it. ([source](https://serverfault.com/questions/328968/domain-controller-audit-log))
- An admin was asked by HR for a report of users exempt from a lockout GPO and had no automated way to produce it. ([source](https://serverfault.com/questions/981094/enterprise-wide-gpo-audit))
- MSP-focused vendor Huntress filters Windows events at the source to keep its SIEM affordable, showing the channel treats Windows volume as a real cost problem. ([source](https://www.huntress.com/blog/unlocking-siem-the-role-of-smart-filtering))

## Why now

Microsoft now ships Sysmon as a built-in optional feature of Windows 11 and Server 2025, serviced monthly and accepting custom configs, but it does not analyse its events, is off by default and cannot coexist with standalone Sysmon, which SMB servers on 2016-2022 still need. MSSPs therefore face a two-flavour Sysmon migration across client fleets over the next few years. Meanwhile independent pipeline vendors are being bought by SIEM/XDR vendors (SentinelOne-Observo), and Wazuh remains the free SIEM small MSSPs standardise on, with Windows collection that is configured per agent. [1](https://learn.microsoft.com/windows/security/operating-system-security/sysmon/overview) [2](https://techcommunity.microsoft.com/blog/windows-itpro-blog/native-sysmon-functionality-coming-to-windows/4468112) [3](https://www.securityweek.com/sentinelone-to-acquire-observo-ai-in-225-million-deal/) [4](https://documentation.wazuh.com/current/user-manual/capabilities/log-data-collection/configuration.html) [5](https://wazuh.com/cloud/)

## MVP

- **Wazuh-only role packs (DC, file server, RDS host, workstation): advanced audit policy GPO, Sysmon config built on sysmon-modular (MIT, credited) for standalone and built-in Sysmon, Wazuh agent eventchannel XPath queries and log-size settings** — Narrow scope one founder can test; reuses the best free baseline instead of competing with it; covers the Server 2016-2022 majority as well as built-in Sysmon.
- **Coverage verifier run per host via RMM (local only, no data leaves the client): checks auditpol subcategories, Sysmon flavour/version/config hash, log sizes and Wazuh agent config, and emits a coverage-state event into the MSSP's own Wazuh** — Turns static configs into a per-tenant stateful service: drift (overwritten GPO, stopped Sysmon, tiny logs) raises a Wazuh alert. This is the monthly value free configs do not give.
- **Wazuh decoders, rules and dashboards for per-tenant coverage and drift, plus a local report runner that queries the Wazuh indexer and renders a monthly client PDF: logons, RDP sessions, failed logons, privilege use, group and GPO changes, coverage status** — A client-facing deliverable the MSSP can resell per client; free Wazuh has no scheduled per-client evidence report.
- **Coverage proof: CI lab replaying ~20 Atomic Red Team techniques per role pack, publishing which Sigma/Wazuh rules still fire, plus an IR-question checklist (lateral-movement timeline, logon/logoff, admin changes) each pack must answer** — Evidence MSSP owners need before trusting a solo vendor; IR questions, not just detections, guard against forensic gaps.
- **Two profiles per role: 'Keep' (no source-side drops beyond documented noise) and 'Lean' (documented drops, each with rationale), with guidance to enable Wazuh compressed archives as a full-fidelity safety net** — Agent-side drops are unrecoverable, so drops are opt-in, documented and backed by a cheap archive rather than the default.
- **Per-pack compliance mapping (PCI DSS Req. 10, HIPAA 164.312(b)) and an employee-monitoring notice / DPIA template shipped with the logon report** — Gives the evidence report a compliance reason to exist and keeps MSPs on the right side of GDPR and works-council rules.
- **Fixed-fee onboarding: founder deploys and tunes packs for one MSSP's tenants; $500 single-tenant pilot credited toward the $2,500 multi-tenant engagement** — Revenue from month one and the field experience that builds credibility; one consistent price ladder.

Out of scope for v1: Hosting, processing or receiving any customer logs (verifier and report runner run inside the MSSP's environment); SIEMs other than Wazuh in v1 (Sentinel DCR/KQL port only after 3 paying Sentinel MSSPs ask); Ransomware canary folders and active response (EDR already detects shadow-copy deletion; we keep only the mapped Sigma detections); Volume simulator across SIEMs (v1 reports per-event-ID volume from Wazuh only); General log pipeline for non-Windows sources; Running detections or a SOC.

## Competition

| Competitor | How we differ |
|---|---|
| [sysmon-modular (free, MIT)](https://github.com/olafhartong/sysmon-modular) | Best maintained free Sysmon baseline, which we build on and credit. It ships configs, not per-tenant rollout, audit policy, Wazuh collection, drift alerts or client reports. |
| [Yamato Security EnableWindowsLogSettings / WELA (free)](https://github.com/Yamato-Security/EnableWindowsLogSettings) | Excellent audit-policy guidance and a per-host auditor; we add fleet-wide RMM rollout, continuous drift monitoring in Wazuh and client-facing evidence. |
| [Wazuh default Windows collection and ruleset (free)](https://documentation.wazuh.com/current/user-manual/capabilities/log-data-collection/configuration.html) | Provides the eventchannel mechanism and generic rules; leaves audit policy, Sysmon config, XPath tuning and per-client reporting to the MSSP. |
| [Microsoft Sentinel Windows Security Events (Common/Minimal sets)](https://learn.microsoft.com/en-us/azure/sentinel/windows-security-event-id-reference) | Free curated event sets inside Sentinel; this is why v1 does not target Sentinel. Wazuh MSSPs have no equivalent curated layer. |
| [Huntress Managed SIEM (Smart Filtering)](https://www.huntress.com/pricing/siem) | Strongest MSP-channel competitor: filtering and SOC inside its own platform. We serve MSSPs who keep their own Wazuh stack and SOC margin. |
| [Cribl Stream (free to 1TB/day, Windows packs)](https://cribl.io/pricing/) | Free pipeline with Windows event-size reduction packs, but a pipeline to run and route; it doesn't set audit policy or Sysmon, verify coverage or report to clients. |
| [ManageEngine ADAudit Plus](https://www.manageengine.com/products/active-directory-audit/) | Turnkey AD/logon reports licensed per client estate; we ride on the Wazuh stack the MSSP already runs, under one per-tenant subscription. |
| [LimaCharlie](https://limacharlie.io/pricing) | Per-endpoint security platform with MSSP tiers that replaces the stack; we suit MSSPs that have standardised on Wazuh and won't migrate. |

**Differentiation:** Not a better config: free baselines (sysmon-modular, Yamato) are the starting point we credit. We sell what they leave to the MSSP: per-tenant RMM rollout of audit policy, both Sysmon flavours and Wazuh collection; continuous drift alerts; replay-tested proof that detections and IR questions still work; and a monthly client evidence report the MSSP can resell. Wazuh-native, no hosted logs, priced per client tenant.

## Build

- Team: 1 technical founder (Windows detection engineering); no hires needed to first revenue
- Time to MVP: 3 months
- Hardest parts: Learning Wazuh decoders, rules, indexer queries and dashboards to a sellable standard (est. 3-5 weeks; free to run in a home lab); Supporting standalone and built-in Sysmon, including per-host migration, with XML-field parsing because built-in messages are localized; Running a replay lab (DC, file server, RDS host, workstation, Wazuh) cheaply enough to re-test monthly; Keeping RMM rollout safe: signed packs, staged rings, preview of auditpol changes and per-tenant rollback; Making the verifier and report runner reliable across client estates without holding credentials or data

## Pricing and business model

- **Model:** Open baseline on GitHub; paid per-client-tenant subscription for maintained packs, drift monitoring content, report runner and support; fixed-fee onboarding
- **Entry price:** $9 per client tenant/month, minimum $149/month (e.g. $450/month at 50 tenants); onboarding $2,500 fixed, with a $500 single-tenant pilot credited toward it
- **Rationale:** Value is per client (drift alerts and a monthly evidence report the MSSP can resell), so price grows with the MSSP's client count and gives a per-client SKU to mark up. It sits well under per-estate audit tools such as ADAudit Plus and Netwrix, and is a small add-on to Wazuh Cloud (from $571/month for 100 agents). The pitch is coverage and client evidence, not ingest savings, because Wazuh has no per-GB licence.

| Comparable | Price |
|---|---|
| ManageEngine ADAudit Plus | [Annual: from $245 (100 workstations); 2 Windows file servers $495; 2 DCs $595 Standard / $945 Professional](https://www.manageengine.com/products/active-directory-audit/pricing-details.html) |
| Netwrix Auditor | [Essentials self-service from $20 per enabled AD user](https://netwrix.com/en/buy-now) |
| Blumira | [~$12-$21/employee/month, flat, no data limits (third-party estimate)](https://www.capterra.com/p/208225/Blumira/pricing/) |
| Cribl Stream | [Free up to 1TB/day; self-managed Standard $4,800 for up to 100GB/day](https://cribl.io/pricing/) |

## Go to market

- **First customers:** Ten small MSSPs or security-led MSPs (2-15 analysts) already running Wazuh for Windows-heavy SMB clients, ideally with PCI, HIPAA or cyber-insurance-driven clients who ask for logon evidence; first from the founder's contacts, then from the Wazuh community and r/msp.
- **Channel:** Founder-led: public repo with replay-tested coverage results and write-ups on built-in Sysmon migration for Wazuh; helpful answers in Wazuh community channels (no vendor spam); later a Wazuh partner/marketplace listing and RMM script-library listings for distribution.
- **Wedge:** Free local 'Windows coverage check' run via RMM on one client: reports audit-policy gaps, Sysmon state, Sigma/IR coverage and noisiest event IDs in the MSSP's Wazuh, plus a sample client evidence report; then a $500 pilot to fix and monitor that tenant.

## Risks

- Bundling and free substitutes: Wazuh, Microsoft (built-in Sysmon default config, Sentinel event sets) or Huntress could ship good Windows defaults; free sysmon-modular and Yamato already cover the config layer. Paid value rests on rollout, drift monitoring and reports, which Wazuh itself could add.
- Weak moat: configs are copyable and customers can cancel and keep them. Defences are the drift/report layer, replay-test results, an opt-in cross-MSSP coverage benchmark, and founder trust; none is strong early.
- Demand evidence is indirect and old: need statements come from in-house admins, many from 2009-2021, not MSSP owners; the Wazuh MSSP niche is likely low thousands of firms, a lifestyle-scale business unless a Wazuh or RMM partner distributes it.
- Liability and forensic gaps: a dropped or missing event later needed in an incident lands on the MSSP and then on us; needs a lawyer-reviewed agreement with liability cap and no-completeness warranty, 'Keep' as default, archive guidance, and tech E&O cover.
- Privacy and data custody: logon reports are employee monitoring (GDPR, works councils); onboarding touches client logs, so a DPA, local-only tooling and NDAs are required. Upstream licences (Sigma DRL, CC BY, Sysinternals terms) require attribution and no Sysmon binary redistribution.
- Solo-founder capacity and credibility: onboarding engagements compete with pack maintenance, and without production MSSP history trust may take 3-6 months of public, replay-tested work to build.

## Riskiest assumption

- **Assumption:** Small MSSPs on Wazuh will pay per client tenant for verified, monitored Windows coverage and a client evidence report, rather than deploying free configs themselves.
- **Cheap test:** Over two weeks, hold 15 short calls with Wazuh-running MSSPs from the founder's contacts and Wazuh/r/msp communities, showing a mock client evidence report and drift alert (slides, no product), asking what they use today and offering the $500 single-tenant pilot with payment up front.
- **Success signal:** At least 6 of 15 say they tried free configs (sysmon-modular, Yamato, Wazuh defaults) and still lack per-tenant verification or client reports, at least 4 say they would resell the report per client, and at least 2 pay the $500 pilot.

## Open questions

- How many small MSSPs run Wazuh for Windows-heavy clients, and how many would resell a per-client evidence report?
- Do cyber-insurance questionnaires or SOC 2 / PCI audits of SMB clients ask for server logon evidence or audit-policy baselines?
- Will Wazuh (or an RMM vendor) partner, list or OEM the packs, or build the same feature?
- Do pilot customers renew at month 3 once packs are deployed, i.e. is drift monitoring felt as monthly value?
- When will SMB fleets move to Server 2025/Windows 11 built-in Sysmon, and how painful is the migration?
- Is there enough paid demand from Sentinel MSSPs (where ingest savings are real but often billed to the client) to justify a second SIEM?

