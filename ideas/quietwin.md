# QuietWin

> Maintained, detection-mapped Windows logging packs for MSPs and MSSPs: cut SIEM volume, keep logon evidence and ransomware precursors, any SIEM.

Opening `msp-windows-detection` (priority 1) · from User activity audit logging on servers (theme 4, stability 0.76), SIEM log collection and noise filtering (theme 16, stability 0.94), Ransomware detection and recovery for file servers (theme 33, stability 1.0)

## Buyer and user

- **Buyer:** Security lead or owner of an MSSP / security-focused MSP — MSSP or security MSP with 2-15 analysts running Wazuh, Graylog, Elastic, Microsoft Sentinel or another volume-billed SIEM for 10-150 SMB clients; Windows event volume is the biggest line on their ingest bill and their analysts drown in noise.
- **User:** The MSSP's detection engineer or senior analyst who deploys configs and reviews coverage reports; MSP technicians who hand the monthly per-client access report to the client.

## Problem

Windows hosts produce most SIEM volume at small-business clients, and teams cut cost by dropping logs blindly, creating forensic blind spots. Pipeline tools that filter intelligently are priced for enterprises. MSSPs and MSPs need versioned Windows audit policy, Sysmon and forwarding configs that keep exactly what detections, logon evidence requests and ransomware investigations need, and drop the rest.

- Teams are told to pre-filter health and status messages before the SIEM to save money and ask what detection risk that creates. ([source](https://security.stackexchange.com/questions/41068/siem-log-pre-filtering-question))
- Windows file-server object auditing forwarded to Graylog floods the collector with noise from routine access, burying the events the admin wanted. ([source](https://serverfault.com/questions/1078821/windows-server-audit-logs))
- Teams drop logs to cut cost and create forensic blind spots; the paid gap is detection-aware filtering with cheap archive. ([source](https://www.helpnetsecurity.com/2026/06/19/report-log-management-security-risk/))
- Pipeline tools are priced for enterprises (per-vCPU tiers, credits); small teams must author filters themselves. ([source](https://www.datadoghq.com/pricing/list/))
- Independent pipeline vendors are being absorbed by SIEM/XDR vendors (SentinelOne bought Observo AI for ~$225M), shrinking vendor-neutral options. ([source](https://www.securityweek.com/sentinelone-to-acquire-observo-ai-in-225-million-deal/))
- Admins running OSSEC/syslog-ng across hundreds of servers look for ways to add correlation without a full SIEM. ([source](https://serverfault.com/questions/539342/ossec-as-a-siem))
- Admins ask for a simple way to track terminal server logins, session durations, disconnections and failed logons and cannot find one. ([source](https://serverfault.com/questions/13451/terminal-server-logging))
- A Server 2008 R2 file server was encrypted after ransomware spread from one PC; the malware deleted the shadow copies the admin hoped to restore from. ([source](https://serverfault.com/questions/874140/restore-shadow-copy-deleted-by-ransomware))

## Why now

Microsoft is shipping Sysmon as a built-in optional feature of Windows 11 and Windows Server 2025, serviced by Windows Update, but it 'doesn't analyze the events it generates' and is off by default. Every MSP now gets free, supported telemetry and still needs configs, collection and detections on top. Built-in Sysmon accepts custom configuration files and is updated monthly, so a maintained, tested config is now the product. Meanwhile independent log-pipeline vendors are being bought by SIEM/XDR vendors (SentinelOne-Observo), and log cost pressure keeps rising. [1](https://learn.microsoft.com/windows/security/operating-system-security/sysmon/overview) [2](https://techcommunity.microsoft.com/blog/windows-itpro-blog/native-sysmon-functionality-coming-to-windows/4468112) [3](https://www.securityweek.com/sentinelone-to-acquire-observo-ai-in-225-million-deal/) [4](https://www.helpnetsecurity.com/2026/06/19/report-log-management-security-risk/)

## MVP

- **Open-source baseline: Windows advanced audit policy GPO, built-in Sysmon config and WEF subscriptions, each event mapped to the Sigma/ATT&CK detections that need it** — Free, credible top of funnel in the founder's own specialty; proves detection-awareness.
- **Paid tiers: role-specific config packs (DC, file server, RDS host, workstation) maintained monthly against new Windows/Sysmon releases** — Maintenance is what MSSPs will not do themselves and what Microsoft's monthly Sysmon updates create demand for.
- **Logon evidence pack: curated logon, RDP-session, failed-logon, privilege-use and group/GPO-change event set with per-client monthly access-review report queries for each supported SIEM** — Answers the most common need statements (terminal server logging, who logged in today) and gives MSPs a client-facing deliverable without hosting logs.
- **Ransomware-precursor pack: detections for shadow-copy deletion (vssadmin/wmic) and audited canary folders on file shares, mapped to T1490/T1486** — Shadow-copy deletion is the classic precursor; canary-folder auditing gives low-false-positive file-share warnings as config, not a privileged service.
- **Coverage-versus-volume report: script that measures a client's current Windows event volume, simulates the pack, and shows GB saved and detections still covered** — Gives the buyer a dollar number to justify the subscription.
- **Drop-in output mappings for Wazuh, Graylog, Elastic and Sentinel, plus RMM scripts (e.g. NinjaOne, ConnectWise) that apply and verify packs per client** — Vendor-neutral: works with whatever SIEM the MSSP already pays for, deployed the way MSPs already push changes, with no new agent.
- **Fixed-fee tuning engagement: founder tunes the packs to one MSSP's environment and detections in 5 days** — Revenue from month one without building a platform.

Out of scope for v1: Hosting or processing any customer logs; A general log pipeline for non-Windows sources; Running detections or a SOC; Rehydration/archive storage.

## Competition

| Competitor | How we differ |
|---|---|
| [Cribl Stream](https://cribl.io/pricing/) | General-purpose pipeline the team must configure; we ship the Windows-specific, detection-mapped content and need no pipeline at all. |
| [Datadog Observability Pipelines](https://www.datadoghq.com/product/observability-pipelines/) | Priced per GB and per vCPU for enterprises; we are a flat subscription for small MSSPs. |
| [Huntress Managed SIEM (Smart Filtering)](https://www.huntress.com/pricing/siem) | Filtering only inside Huntress's own SIEM; ours works with any SIEM the MSSP runs. |
| [ManageEngine ADAudit Plus](https://www.manageengine.com/products/active-directory-audit/) | Installed and licensed per client estate with per-source add-ons; our logon evidence pack rides on the SIEM the MSP already runs, under one MSP subscription. |
| [Graylog Open / Wazuh default rules (free)](https://graylog.org/pricing/) | Free platforms with generic defaults; we supply the tuned Windows collection layer they lack. |
| [Community Sysmon configs and built-in Sysmon (free)](https://learn.microsoft.com/windows/security/operating-system-security/sysmon/overview) | Free configs are general-purpose and not mapped to volume or maintained per Windows release; we sell maintenance, measurement and support. |
| [Tenzir](https://docs.tenzir.com/faqs) | Pipeline engine for teams that will build pipelines; we sell finished content for teams that won't. |

**Differentiation:** Content, not a platform: tested Windows audit policy, Sysmon and forwarding configs where every kept event is justified by a detection or an evidence request, measured against the buyer's own volume and maintained as Windows changes. Vendor-neutral where Huntress and SIEM-owned pipelines are not, priced for a 5-analyst MSSP where Cribl and Datadog are not, and holds no customer logs.

## Build

- Team: 1 technical founder (Windows detection engineering); no hires needed to first revenue
- Time to MVP: 2 months
- Hardest parts: Proving coverage claims: a test lab that replays attack techniques (e.g. Atomic Red Team) against each pack to show detections still fire; Keeping packs current with monthly built-in Sysmon and Windows updates; Defending a content business against copying once configs are shipped; Translating packs into each SIEM's collector syntax; Making canary folders and logon reports work across each SIEM without the product running on client servers

## Pricing and business model

- **Model:** Open-core: free baseline on GitHub; paid subscription per MSSP for maintained packs, volume reports and support; optional fixed-fee tuning
- **Entry price:** $249/month per MSSP/MSP for up to 50 client tenants (all packs, incl. logon evidence and ransomware-precursor packs); tuning engagement $2,500 fixed fee
- **Rationale:** Cribl's self-managed Standard licence is $4,800 for up to 100GB/day and Datadog charges per GB plus per vCPU; a small MSSP paying volume-based SIEM ingest saves more than $249/month if the packs cut Windows volume meaningfully, and the price stays under a credit-card approval threshold.

| Comparable | Price |
|---|---|
| Cribl Stream | [Free up to 1TB/day; self-managed Standard $4,800 for up to 100GB/day](https://cribl.io/pricing/) |
| Datadog Observability Pipelines | [$0.095-$0.12 per ingested GB/month; Plus $1,950-$2,808 per vCPU/month](https://www.datadoghq.com/pricing/list/) |
| Blumira | [~$12-$21/employee/month, flat, no data limits (third-party estimate)](https://www.capterra.com/p/208225/Blumira/pricing/) |
| ManageEngine ADAudit Plus | [Annual per server: 2 DCs $595 Standard / $945 Professional; 2 Windows file servers $495](https://www.manageengine.com/products/active-directory-audit/pricing-details.html) |

## Go to market

- **First customers:** Ten small MSSPs or security-led MSPs (2-15 analysts) running Wazuh, Graylog or Sentinel for SMB clients, who have complained publicly about Windows event volume or ingest cost; reached through the founder's few industry contacts, r/msp, r/blueteamsec and the Wazuh/Graylog communities.
- **Channel:** Open-source GitHub repo and write-ups on built-in Sysmon configuration as inbound; founder sells subscriptions and tuning directly; no paid ads.
- **Wedge:** Free 'Windows log diet' report: run one script on a client's collector and get GB/day saved and ATT&CK coverage kept, plus a sample client logon access report; then pay to get the maintained packs.

## Risks

- Bundling: Microsoft, Huntress, Blumira or Wazuh could ship good default Windows configs, eroding paid value.
- Content is easy to copy and community configs (e.g. popular open-source Sysmon configs) are free; revenue depends on maintenance and trust, not secrecy.
- Small MSSPs on flat-priced SIEMs (Blumira, Huntress) have no volume pain; the logon evidence and ransomware-precursor packs must carry the sale for them.
- Liability: a pack that drops an event later needed in an incident invites blame; contracts and coverage testing must address it.
- A services-heavy start may cap growth; tuning revenue must convert to subscriptions.

## Riskiest assumption

- **Assumption:** Small MSSPs feel enough Windows-event cost or noise pain to pay a recurring fee for configs they could, in principle, write themselves.
- **Cheap test:** Publish the free baseline config and a 'log diet' measuring script, post a write-up in r/msp, r/blueteamsec and the Wazuh/Graylog communities, and offer a $500 one-off tuning pilot to the first responders; founder does the work by hand.
- **Success signal:** At least 3 paid pilots and 10 MSSPs asking for subscription pricing within 2 weeks, and measured Windows volume reduction of at least 40% with no loss of mapped detections in the pilots.

## Open questions

- What share of small MSSPs pay volume-based ingest versus flat-priced SIEMs?
- How quickly will built-in Sysmon be enabled in SMB fleets, and on which Server versions?
- Would RMM or SIEM vendors license the packs (OEM) instead of MSSPs buying them?
- What contract language limits liability for dropped events?
- Do insurers' questionnaires actually ask for server logon evidence, or only MFA/EDR?

