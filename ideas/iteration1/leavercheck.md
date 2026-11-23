# LeaverCheck

> Read-only offboarding verification: within an hour of an Okta or Entra deactivation, checks every app, including non-SCIM ones, and chases leftover accounts.

Opening `buyer-side-provisioning` (priority 2) · from SCIM user provisioning for applications (theme 3, stability 0.52)

## Buyer and user

- **Buyer:** Head of IT / IT manager (often also owns security and SOC 2 evidence) — Companies with 150-1,500 employees, typically tech or professional services, on Okta or Microsoft Entra ID, with a SOC 2 or ISO 27001 audit cycle and 10 or more apps whose offboarding is manual, scripted in Okta Workflows, or handled by a bridge such as Scimify or Aquera. They want to know that leavers are actually gone everywhere, not just deactivated in the IdP, and have no budget for an IGA platform.
- **User:** The one to three IT admins who run leaver tickets, plus the app owners (finance, engineering, sales ops) who get asked to remove leftover accounts in apps IT can't reach.

## Problem

IdP provisioning only reaches SCIM apps, and many apps don't offer SCIM or paywall it (a vendor analysis of 721 apps, Stitchflow's own data). For those apps, offboarding is a ticket, a script or a third-party bridge, and none of them shows whether the account is really gone. Missed removals leave active accounts behind after the IdP shows the user as deactivated. Paid fixes come bundled in SaaS-management or governance platforms.

- Vendor analysis of 721 SaaS apps: 42-43% lock SCIM behind enterprise tiers and 57% offer no SCIM at all (Stitchflow's own data). ([source](https://www.stitchflow.com/blog/scim-tax-worst-offenders))
- Postman users report that provisioning and de-provisioning users is a manual process and ask for SCIM. ([source](https://github.com/postmanlabs/postman-app-support/issues/6235))
- An Okta administrator says SCIM provisioning support is the key thing they need from an IdP, beyond SSO. ([source](https://news.ycombinator.com/item?id=35644662))
- Tracecat admins have to invite each new user, wait for them to sign up, then add them to the workspace by hand. ([source](https://github.com/TracecatHQ/tracecat/issues/1031))
- Okta's entry Starter suite ($6/user/month) lacks Lifecycle Management; IdP-side SCIM provisioning needs an add-on or an upgrade to Core Essentials ($14/user/month). ([source](https://www.okta.com/pricing/))
- Even where SCIM exists, it can break on real directory data: Postman's SCIM won't provision Azure groups whose names contain periods. ([source](https://github.com/postmanlabs/postman-app-support/issues/12551))

## Why now

Write-side bridges for non-SCIM apps have become cheap and plentiful: Scimify is listed in the Okta Integration Network at from $0.90/user/month with unlimited integrations, Aquera is an Okta partner and a Microsoft-listed partner-driven integration path, and Stitchflow, Zluri and Cerby sell browser automation. So a mid-market company now offboards through a mix of IdP SCIM, bridges, Workflows and manual tickets, and none of those paths verifies itself independently. Okta event hooks push user-deactivation events to an external endpoint asynchronously, so a read-only checker can react within minutes without sitting in the provisioning path. Okta Lifecycle Management needs Core Essentials ($14/user/month) or an add-on on Starter, so many buyers mix paths rather than standardise on one. [1](https://www.okta.com/en-au/integrations/veraproof-scimify/) [2](https://veraproof.pages.dev/blog/20260524-scimify-claude-openai-enterprise-scim-savings/) [3](https://www.okta.com/partners/aquera/) [4](https://learn.microsoft.com/en-us/entra/identity/app-provisioning/partner-driven-integrations) [5](https://www.cerby.com/blog/provisioning-and-deprovisioning-apps-without-scim) [6](https://developer.okta.com/docs/concepts/event-hooks/) [7](https://www.okta.com/pricing/)

## MVP

- **Okta event hook and Entra audit-log listener for user deactivation, which starts a per-leaver check run** — Checks run within the hour, not at quarter-end, and the product never sits in the synchronous SCIM path, so it can't block or fake a deprovision
- **Read-only API connectors for about 12 high-demand apps that list users and their status, using the least-privileged read scope each app offers** — A read token can't create or delete accounts, which shrinks the blast radius, eases security reviews and sidesteps vendor terms on shared admin logins
- **CSV and scheduled-export ingestion for apps with no usable list API: the app owner uploads or emails the app's user export** — Covers the long tail without browser agents, MFA seeds or SSO-bypass accounts; the product holds no credential for those apps at all
- **Identity matching with review: email, immutable IdP ID and manual links, with ambiguous matches flagged and never auto-actioned** — Username changes and aliases cause false positives; a verifier that cries wolf gets ignored
- **Leftover-account workflow: a Slack or Jira task to the app owner with a deadline, re-checked until the account is gone, then closed** — Turns a finding into a closed loop without us ever holding write access
- **Per-leaver check log exportable for auditors: which apps were checked, when, by which method, and what was found** — Auditors ask for evidence that offboarding happened; this records that checks ran, without claiming completeness

Out of scope for v1: Writing to apps: provisioning, deprovisioning or a SCIM endpoint (Scimify, Aquera, Okta LCM and Workflows already do this; we verify whichever path the buyer uses); Browser agents, stored admin passwords and TOTP seeds; Onboarding and mover checks (v2 at the earliest); SaaS spend management, shadow-IT discovery and license optimisation; Access requests, approvals and access reviews (IGA); Google Workspace, JumpCloud and other IdPs (v2 at the earliest).

## Competition

| Competitor | How we differ |
|---|---|
| [Veraproof Scimify](https://veraproof.pages.dev/scimify/) | Scimify is a write-side bridge that translates Okta SCIM to app APIs, from $0.90/user/month with unlimited integrations. It does the deprovisioning; we check independently that it, or any other path, actually worked, and we cover apps it has no connector for via exports. We'd rather integrate with it than fight it. |
| [Aquera SCIM Gateway](https://www.okta.com/partners/aquera/) | Aquera provisions hundreds of apps via Okta and Entra, uses robotic automation where there's no API, and feeds discovered entitlements into Okta Access Audit Reports. It's an enterprise, connector-led sale. We're read-only, self-serve, and verify apps Aquera doesn't run as well as those it does. |
| [Stitchflow](https://www.stitchflow.com/pricing) | Stitchflow is a managed service that builds and maintains browser-backed provisioning plus spend intelligence, for under $5K per app per year (vendor claim). We don't touch apps or run browsers, so we cost a fraction and need far less trust. |
| [Zluri](https://www.zluri.com/eye-on-identity/deprovision-non-scim-apps-okta-offboarding) | Zluri bundles non-SCIM deprovisioning (HTTP actions, AI browser integrations, manual tasks) and user reconciliation inside a full SaaS-management and IGA platform. We sell only verification and chase-up, with no platform commitment. |
| [Cerby](https://www.cerby.com/blog/provisioning-and-deprovisioning-apps-without-scim) | Cerby automates lifecycle for 'disconnected apps' with no SCIM or API and plugs into Okta, aimed at enterprises. We stay out of the write path and serve the mid-market for whom that depth is overkill. |
| [Okta Lifecycle Management, Workflows and Identity Security Posture Management](https://www.okta.com/pricing/) | The bundled default: LCM provisions SCIM apps, Workflows can script API apps, and Okta ISPM scans for identity risks as a separate product. None of these checks apps Okta can't connect to. Okta extending ISPM to cheap orphan checks for non-integrated apps is our main bundling risk. |
| [Ticket plus spreadsheet (free)](https://www.stitchflow.com/blog/scim-tax-worst-offenders) | What most buyers do today, and what auditors often accept. We replace a quarterly manual reconciliation with per-leaver checks, but the buyer has to value catching misses sooner, not just passing the audit. |

**Differentiation:** Every other product here writes to apps and asks for admin trust; LeaverCheck only reads, so it works alongside whatever offboarding path the buyer already has (IdP SCIM, Scimify, Aquera, Workflows or a ticket) and checks it independently. Read-only tokens and CSV exports mean no browser agents, no stored admin passwords and a short security review. Per-leaver checks with chase-up close gaps in hours, not at the next quarterly review.

## Build

- Team: 2 engineers (one identity and integrations, one backend and data) + 1 founder-seller with a mid-market IT background
- Time to MVP: 4 months
- Hardest parts: Identity matching across apps with inconsistent identifiers (aliases, renamed emails, contractors on personal domains) without a flood of false positives; Finding a genuinely read-only scope in each target app; some apps only offer admin tokens, which we refuse or confine to export ingestion; Getting app owners outside IT to upload exports on schedule; if they don't, coverage of the long tail decays; Reaching SOC 2 Type II while holding employee directory data and read tokens, even though the blast radius is smaller than write access

## Pricing and business model

- **Model:** Per IdP user per month, unlimited apps and checks, with a monthly minimum; annual billing discount
- **Entry price:** $1/user/month billed annually (minimum $250/month), unlimited apps; free one-time orphan-account scan from CSV exports
- **Rationale:** Per-app pricing at $149-299 lost to Scimify's per-user, unlimited-apps model and couldn't be justified by labour savings on apps with no SCIM, so we switch to per-user pricing near Scimify's $0.90. A 500-user company pays about $6K a year, about 7% of what Okta Core Essentials costs at $14/user/month, and a fraction of Stitchflow's under-$5K-per-app figure for a single managed app. The buyer pays for risk evidence, not labour, so price has to stay low enough to buy on a card and pass a light security review. Developer-side per-connection prices ($59-79/month at SSOJet) show what a single sync connection is worth; we price the whole estate near one connection per 80 users.

| Comparable | Price |
|---|---|
| Okta Lifecycle Management | [Included in Core Essentials $14/user/month and Essentials $17/user/month; add-on on Starter $6/user/month; billed annually, $1,500 annual minimum](https://www.okta.com/pricing/) |
| Stitchflow | [Vendor claims under $5K per app per year; list price not public](https://www.stitchflow.com/blog/automate-scim-provisioning-without-enterprise-tier) |
| SSOJet | [$79 per connection/month billed monthly or $59 billed annually (SSO and SCIM each count as one)](https://ssojet.com/pricing/) |

## Go to market

- **First customers:** Ten Okta or Entra shops with 150-1,500 employees, a one-to-three-person IT team, a SOC 2 or ISO 27001 audit in the next six months, and 10 or more apps outside SCIM provisioning. Include at least three that already use Scimify, Aquera or Okta Workflows for non-SCIM apps, to test the 'verify any path' pitch.
- **Channel:** Founder-led sales opened by the free orphan-account scan (customer uploads user exports, gets a leftover-accounts report in a day), posts in Okta and Entra admin communities, and partnerships with SOC 2 audit firms and compliance-automation tools that want offboarding evidence. Seek integration or co-listing with write-side bridges such as Scimify rather than competing for the same OIN shelf.
- **Wedge:** The free scan: most buyers have never diffed their leavers against non-SCIM app user lists. A non-zero result sells the continuous per-leaver check.

## Risks

- Bundling: Okta ISPM, Okta Identity Governance, Aquera's Access Audit Reports and SaaS-management tools (Stitchflow, Zluri) already reconcile user lists for apps they connect. If Okta or a cheap bridge adds orphan checks for non-integrated apps, the gap closes.
- Willingness to pay is unproven: auditors often accept ticketed manual offboarding, and the input rates willingness to pay 2 of 5. Verification may be seen as a nice-to-have, and the price floor leaves little room for a long sales cycle.
- Coverage decay: apps with no read API depend on app owners uploading exports. If they don't, the product quietly covers fewer apps than the buyer thinks.
- Liability and claims: a missed or mismatched account could be blamed on us. Contracts and marketing must say 'checks run', never 'proof access is gone', with clear liability limits.
- Data protection: we process employee names, emails and app user lists as a GDPR processor and need DPAs, a sub-processor list and short retention; some apps only offer admin-scoped tokens, which we must refuse or isolate.
- Low ACV: about $3K-18K a year per customer. It works only if the scan converts and security reviews stay light; a services-heavy sale would sink the economics.

## Riskiest assumption

- **Assumption:** Mid-market IT teams on Okta or Entra find leftover accounts in non-SCIM apps often enough, and care enough, to pay about $1/user/month for continuous read-only leaver verification on top of whatever offboarding they already do.
- **Cheap test:** Over two weeks, offer 20 qualifying IT managers a free concierge orphan scan: they send the last 90 days of IdP deactivations plus user exports from 5-10 non-SCIM apps, and we diff them by hand in a spreadsheet. At the readout, ask for a paid pilot or LOI at $1/user/month.
- **Success signal:** At least 8 of 20 scans find one or more active accounts belonging to a user deactivated in the IdP more than 7 days earlier, and at least 5 companies sign an LOI or paid pilot at $1/user/month or more.

## Open questions

- How often do leftover accounts actually occur in non-SCIM apps at this size, and in which apps?
- For the top 12 target apps, is there a read-only scope that lists users and their status on the tiers buyers actually hold?
- Will app owners outside IT keep uploading exports, or does coverage need an automated export path per app?
- Will Scimify, Aquera or SOC 2 compliance tools partner with an independent verifier, or treat it as competitive?
- Do auditors give credit for per-leaver verification logs beyond what a ticket trail already earns?
- Is there a later, defensible path to a write side (closing the loop via the customer's existing bridge) that doesn't recreate the trust problem?

