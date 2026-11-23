# SCIMbridge

> A hosted SCIM endpoint for each SaaS app that lacks SCIM, so Okta or Entra provisions and deprovisions it like any other app.

Opening `buyer-side-provisioning` (priority 2) · from SCIM user provisioning for applications (theme 3, stability 0.52)

## Buyer and user

- **Buyer:** Head of IT / IT manager (often also owns security and SOC 2 evidence) — Companies with 150-1,500 employees, typically tech or professional services, already running Okta (Core Essentials or above, where Lifecycle Management is included) or Microsoft Entra ID provisioning for their SCIM apps. They have 5-20 apps that either have no SCIM or lock it behind an enterprise tier they won't buy, and no budget or headcount for a full identity governance platform.
- **User:** The one to three IT admins who run joiner/mover/leaver work in Okta or Entra and today log in to each non-SCIM app by hand to add or remove users.

## Problem

IdP provisioning only reaches apps that expose SCIM, and many don't: one vendor analysis of 721 SaaS apps found 43% paywall SCIM behind enterprise tiers and 57% have none. For those apps, admins add and remove users by hand, which is slow and error-prone. Offboarding misses leave orphaned accounts active after a user is deactivated in the IdP. The workarounds are per-app Okta Workflows scripts that someone has to maintain, or buying a full SaaS-management or governance platform.

- Vendor analysis of 721 SaaS apps: 42-43% lock SCIM behind enterprise tiers and 57% offer no SCIM at all (Stitchflow's own data). ([source](https://www.stitchflow.com/blog/scim-tax-worst-offenders))
- Postman users report that provisioning and de-provisioning users is a manual process and ask for SCIM. ([source](https://github.com/postmanlabs/postman-app-support/issues/6235))
- An Okta administrator says SCIM provisioning support is the key thing they need from an IdP, beyond SSO. ([source](https://news.ycombinator.com/item?id=35644662))
- Tracecat admins have to invite each new user, wait for them to sign up, then add them to the workspace by hand. ([source](https://github.com/TracecatHQ/tracecat/issues/1031))
- Okta's entry Starter suite ($6/user/month) lacks Lifecycle Management; IdP-side SCIM provisioning needs an add-on or an upgrade to Core Essentials ($14/user/month). ([source](https://www.okta.com/pricing/))
- Even where SCIM exists, it can break on real directory data: Postman's SCIM won't provision Azure groups whose names contain periods. ([source](https://github.com/postmanlabs/postman-app-support/issues/12551))

## Why now

Mid-market companies already pay for an IdP provisioning engine, such as Okta Lifecycle Management in Core Essentials at $14/user/month. That engine only reaches SCIM apps, and Stitchflow's data says most apps either paywall SCIM (for example, GitHub Team $4 versus Enterprise Cloud $21) or don't offer it at all. Entra's provisioning service can drive any SCIM endpoint a third party builds. Entra Lifecycle Workflows, by contrast, need an Entra ID Governance or Entra Suite license. Browser agents that can operate admin UIs reliably are now shipping commercially in Stitchflow and Zluri, which shows both that the approach works and that buyers want it. Those offerings come bundled in services-led SaaS-management platforms, which leaves room for a self-serve, IdP-native product at a lower price. [1](https://www.stitchflow.com/blog/automate-scim-provisioning-without-enterprise-tier) [2](https://www.okta.com/pricing/) [3](https://learn.microsoft.com/en-us/entra/identity/app-provisioning/use-scim-to-provision-users-and-groups) [4](https://learn.microsoft.com/en-us/entra/id-governance/what-are-lifecycle-workflows) [5](https://www.stitchflow.com/pricing) [6](https://www.zluri.com/eye-on-identity/deprovision-non-scim-apps-okta-offboarding)

## MVP

- **A hosted SCIM 2.0 endpoint per connected app (Users: create, update, deactivate; basic Groups), registered in Okta or Entra as a custom SCIM app** — The IdP stays the system of record, keeps its own assignment rules and audit log, and admins don't learn a new workflow tool
- **API-backed connectors for the 25 most common non-SCIM or SCIM-paywalled apps, translating SCIM calls to each app's admin REST API** — Most apps without SCIM still have a user-management API, and API calls are the cheapest and most reliable path
- **A browser-agent fallback for apps with no usable admin API, running headless in an isolated per-tenant worker, with screenshots as evidence** — This covers the long tail that API connectors can't reach and is the reason a buyer can't just script it in Okta Workflows
- **Deprovisioning verification and an orphan-account report that diffs each app's user list against IdP assignments every night** — Deprovisioning is where the security value is, and auditors want proof that access was removed, not just a log that a request was sent
- **Failure handling: a retry queue, a Slack or email alert, and a manual-task fallback assigned to the app owner when automation fails** — UI changes and MFA prompts will break automation, so a silent failure is worse than no product
- **Credential vault for app admin credentials, using a per-tenant KMS key and scoped service accounts** — We hold admin access to the customer's apps, so the security bar decides whether we get bought

Out of scope for v1: SaaS spend management, shadow-IT discovery and license optimisation (Stitchflow's, Zluri's and Lumos's turf); Access requests, approvals and access reviews (IGA); Our own identity provider or SSO; On-prem and legacy apps, and an on-prem agent; Developer-side SCIM for app builders (WorkOS, Stytch, SSOJet, and Auth0/Clerk, which bundle it free); Google Workspace, JumpCloud and other IdPs (v2 at the earliest).

## Competition

| Competitor | How we differ |
|---|---|
| [Stitchflow](https://www.stitchflow.com/pricing) | Stitchflow audits the app stack, builds and maintains each integration as a service, and bundles spend intelligence, for under $5K per app per year (vendor claim). We're self-serve, provisioning only, and IdP-native (a SCIM endpoint, not a separate workflow engine), at about a third to half the price per app. |
| [Zluri](https://www.zluri.com/eye-on-identity/deprovision-non-scim-apps-okta-offboarding) | Zluri covers non-SCIM deprovisioning with HTTP actions, AI browser integrations and manual tasks inside a full SaaS-management and IGA platform with its own playbooks. We sell just the bridge, keep Okta or Entra as the control plane, and price per app with no platform commitment. |
| [Lumos](https://www.lumos.com/pricing) | Lumos sells agentic identity governance (JML automation, access reviews, 300+ integrations) through demos, aimed at larger IT orgs. We're a narrow, inexpensive add-on for teams that aren't ready for an IGA purchase. |
| [Okta Lifecycle Management + Okta Workflows](https://www.okta.com/pricing/) | This is the bundled default, but it only provisions SCIM apps; non-SCIM apps need a hand-built Workflows flow per app, and those flows can't reach apps that have no API. We plug into LCM as ordinary SCIM apps and maintain the connectors ourselves. |
| [Microsoft Entra provisioning + Lifecycle Workflows](https://learn.microsoft.com/en-us/entra/id-governance/what-are-lifecycle-workflows) | Entra provisioning drives SCIM endpoints, and Lifecycle Workflows (which need an ID Governance or Entra Suite license) can call Logic Apps that the customer builds. We are the SCIM endpoint, with no Logic Apps to write and no governance license required for the per-app connector. |
| [Self-hosted SCIM gateway (jelhub/scimgateway, open source)](https://github.com/jelhub/scimgateway) | This is the free do-it-yourself route: a SCIM gateway with plugins the customer writes and hosts. We're hosted, maintain the per-app connectors, and add a browser fallback, verification and alerting. |

**Differentiation:** The IdP the buyer already owns stays the single control plane: each non-SCIM app becomes a normal SCIM app in Okta or Entra. Buyers don't have to adopt a SaaS-management platform, sit through a services engagement or write per-app Workflows. Pricing is self-serve per app, below Stitchflow's per-app price and far below most enterprise-tier SCIM upgrades. Nightly verification shows the account is actually gone, which is the audit evidence IT needs.

## Build

- Team: 2 engineers (one identity/SCIM, one browser automation and infra) + 1 founder-seller with mid-market IT background
- Time to MVP: 5 months
- Hardest parts: Keeping browser-agent connectors working through vendor UI changes, MFA prompts and bot detection, at a maintenance cost that per-app pricing can absorb; Meeting the security bar for holding admin credentials to customers' apps (SOC 2 Type II early, tenant isolation, credential scoping); SCIM conformance quirks across Okta and Entra clients (PATCH semantics, group handling, soft deactivate vs delete); Mapping each app's own idea of a role, seat and license onto SCIM attributes without surprising admins

## Pricing and business model

- **Model:** Per connected app per month, self-serve, with a higher tier for apps reached by browser agent; annual discount
- **Entry price:** $149/month per API-backed app or $299/month per browser-backed app; 30-day free trial on the first app
- **Rationale:** At $1.8K-$3.6K per app per year we sit below Stitchflow's claimed under-$5K per app and far below a typical SCIM-tier upgrade. On Stitchflow's figures, GitHub Team at $4 versus Enterprise Cloud at $21 per seat is a $17 per-seat uplift, so the bridge pays off at about 9 seats (API-backed) or about 18 (browser-backed). Okta LCM at $14/user/month shows buyers already pay for provisioning, so the bridge extends a purchase they've made. Developer-side per-connection prices ($79-$125/month) anchor what a single provisioning connection is worth.

| Comparable | Price |
|---|---|
| Stitchflow | [Vendor claims under $5K per app per year; list price not public](https://www.stitchflow.com/blog/automate-scim-provisioning-without-enterprise-tier) |
| Okta Lifecycle Management | [Included in Core Essentials $14/user/month and Essentials $17/user/month; add-on on Starter $6/user/month; billed annually, $1,500 annual minimum](https://www.okta.com/pricing/) |
| SSOJet | [$79 per connection/month billed monthly or $59 billed annually (SSO and SCIM each count as one)](https://ssojet.com/pricing/) |
| Stytch | [5 SSO/SCIM connections free, then $125 per connection/month](https://stytch.com/pricing?vertical=B2B) |

## Go to market

- **First customers:** Ten Okta (Core Essentials or above) or Entra shops with 150-1,500 employees, a one-to-three-person IT team, an upcoming or recent SOC 2 or ISO 27001 audit, and at least five apps provisioned by hand. Likely mostly Series B-D tech companies, where IT admins are active in public admin communities.
- **Channel:** Founder-led sales plus content and community: a public, regularly updated SCIM-availability directory per app (which tier, which price) to rank on searches such as '<app> SCIM'; posts in Okta and Entra admin communities; and listings in the Okta Integration Network and the Entra app gallery once connectors are stable.
- **Wedge:** Offboarding first: deprovisioning plus nightly orphan-account verification for the buyer's three riskiest non-SCIM apps, sold as audit evidence. Expand to onboarding and more apps once the connectors have proved reliable.

## Risks

- Crowding: Stitchflow and Zluri already ship browser-backed provisioning for non-SCIM apps, and Lumos and other IGA vendors are adding agentic automation. If they release a cheap self-serve tier, our price wedge closes.
- Bundling: IdPs (Okta Workflows, Entra Lifecycle Workflows and Logic Apps) or app vendors lowering their SCIM paywall could shrink the gap. The input rates bundling risk high for SCIM generally, though so far the bundling is on the developer side (Auth0, Clerk).
- Technical: browser connectors break on UI changes, MFA and bot defenses. Per-app maintenance cost may exceed $149-299/month on the long tail, which squeezes margins.
- Contractual: automating an app's admin UI or using its API to avoid an enterprise tier may breach that vendor's terms of service, and vendors could block it or threaten the customer.
- Trust: holding admin credentials for customers' apps makes us a high-value target. One incident would end the company, and security reviews will lengthen sales cycles.
- Unverified willingness to pay: the evidence shows buyers pay for IdP suites and enterprise tiers, but there's no verified evidence that mid-market IT will buy a standalone per-app bridge.

## Riskiest assumption

- **Assumption:** Mid-market IT teams on Okta or Entra will pay about $149-299 per app per month for a self-serve SCIM bridge, rather than living with manual offboarding, writing Okta Workflows, upgrading the app's tier, or buying Stitchflow or Zluri.
- **Cheap test:** Over two weeks, run a landing page with the per-app price and a 'reserve your first three apps' pre-order (refundable $149 deposit), and promote it in Okta and Entra admin communities and on LinkedIn to IT managers at 150-1,500-person companies. In parallel, hold 20 problem interviews in which each admin lists their manually provisioned apps and what they pay today.
- **Success signal:** At least 10 of 20 interviewees name three or more manually provisioned apps they'd connect at the stated price, and at least 5 paid deposits or signed letters of intent at $149/app/month or more.

## Open questions

- Which 25 apps make up most of the non-SCIM and SCIM-paywalled demand among Okta and Entra mid-market customers? The Stitchflow data isn't public in full.
- How much does each browser connector cost to maintain per month in practice, and what share of apps can be served by API alone?
- Do app vendors' terms of service allow third-party automation of admin UIs, and will any vendor actively block it?
- Is Okta Starter (no Lifecycle Management) a large enough segment to justify our own lightweight lifecycle trigger later?
- Will Okta or Microsoft list a bridge like this in their integration catalogues, or treat it as competitive?
- Do buyers accept a cloud-hosted browser agent, or do they require a locally run one, as Stitchflow offers?

