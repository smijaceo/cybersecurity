# Gap report — 2026-11-23

225 need statements (from 1137 collected signals) grouped into 16 themes; 8 judged incoherent and excluded; 13 statements fit no theme.

**Gap score** = 0.3 × demand + 0.3 × supply gap + 0.25 × monetization + 0.15 × threat relevance. Supply gap weighs commercial crowdedness 60% and open-source supply 40%; monetization combines willingness to pay, the share of statements complaining about price or vendors, and bundling risk (decision D11). Each component is a percentile rank across themes (0–1), so scores are relative to this run, not absolute. Weights: [config/scoring.yaml](../../config/scoring.yaml).

**Stability** = how consistently a theme's statements cluster together across 3 other random seeds (1.0 = always). Treat themes below 0.5 as provisional.

**Paid-market data** (vendors, prices, gaps, willingness to pay) comes from a market researcher agent using web search, with a source link for every claim ([rubric](../docs/rubrics/market-research.md)). Prices change; check sources before relying on them.

**Fact-check** (round 3): an adversarial checker re-opened the sources for 24 vendor and willingness-to-pay claims; 12 are not fully supported by their cited source. Per-gap counts are shown below; details in [phase2/fact-check.json](phase2/fact-check.json).

## Ranking

| # | Gap | Score | Demand | Supply gap | Monetization | Threat | Crowdedness | Willingness to pay | Statements | Stability |
|---|---|---|---|---|---|---|---|---|---|---|
| 1 | [Remediating vulnerable third-party dependencies](#1-remediating-vulnerable-third-party-dependencies) | **0.63** | 0.757 | 0.389 | 0.589 | 0.929 | 3/3 | 2/3 | 18 | 0.76 |
| 2 | [AWS role credentials for workloads](#2-aws-role-credentials-for-workloads) | **0.606** | 0.571 | 0.523 | 0.554 | 0.929 | 3/3 | 2/3 | 11 | 0.41 ⚠ |
| 3 | [SCIM user provisioning for applications](#3-scim-user-provisioning-for-applications) | **0.501** | 0.7 | 0.383 | 0.446 | 0.429 | 3/3 | 2/3 | 23 | 0.52 |
| 4 | [Dependency context for vulnerability impact](#4-dependency-context-for-vulnerability-impact) | **0.49** | 0.036 | 0.831 | 0.661 | 0.429 | 2/3 | 2/3 | 6 | 0.73 |
| 5 | [Managing SIEM log noise and ingestion](#5-managing-siem-log-noise-and-ingestion) | **0.473** | 0.214 | 0.597 | 0.661 | 0.429 | 3/3 | 2/3 | 7 | 0.51 |
| 6 | [CycloneDX SBOM output and attestation](#6-cyclonedx-sbom-output-and-attestation) | **0.454** | 0.307 | 0.566 | 0.768 | 0.0 | 2/3 | 2/3 | 6 | 1.0 |
| 7 | [SBOM generation across build ecosystems](#7-sbom-generation-across-build-ecosystems) | **0.443** | 0.786 | 0.371 | 0.125 | 0.429 | 3/3 | 1/3 | 31 | 0.74 |
| 8 | [IAM-based authentication in AWS service clients](#8-iam-based-authentication-in-aws-service-clients) | **0.404** | 0.629 | 0.34 | 0.196 | 0.429 | 3/3 | 1/3 | 15 | 0.47 ⚠ |

## 1. Remediating vulnerable third-party dependencies

> Developers and security engineers struggle to detect, prioritize and quickly update vulnerable direct and transitive dependencies, including faster patching despite release-age delays.

Gap score **0.63** · stability 0.76 · segments: appsec-supply-chain, cloud-security, smb-security-ops · keywords: vulnerability, security, dependency, dependencies, update, dependency vulnerability

- **Demand**: 18 need statements, total engagement 252, 50% from the last 2 years.
**Opportunity:** Crowded, bundled market; no opening for another scanner. Narrow wedge: fixing the stuck cases (transitive conflicts, no-fix CVEs, cooldown-bypass policy) sold to teams already paying Snyk/GitHub, but Seal and Endor already target this.

- **Open-source supply** (GitHub repositories for `dependency vulnerability remediation`): 154 repos, leader 1999★, 10 of the top 10 pushed in the last year. Leading projects: [pyupio/safety](https://github.com/pyupio/safety) 1999★, [OWASP/cve-lite-cli](https://github.com/OWASP/cve-lite-cli) 801★, [Hamdy910/sentinel-diff-guard](https://github.com/Hamdy910/sentinel-diff-guard) 68★.
- **Threat relevance** 3/3: Exploiting known-vulnerable third-party libraries is a common, actively exploited path; faster patching closes it directly. ATT&CK: [T1068 Exploitation for Privilege Escalation](https://attack.mitre.org/techniques/T1068), [T1499.004 Application or System Exploitation](https://attack.mitre.org/techniques/T1499/004). NVD CVEs matching the query: 3.

**Paid market** — crowdedness 3/3, willingness to pay 2/3, bundling risk high. ⚠ 3 claim(s) here not fully supported by their source (see fact-check).

| Vendor | Offering | Pricing | Sells to |
|---|---|---|---|
| [Snyk Open Source](https://snyk.io/pricing/) | Developer-first SCA with fix PRs for direct and transitive dependencies | [Free tier; Team $25/contributing dev/month, 5-dev minimum, up to 10 contributing devs; Enterprise custom](https://snyk.io/start/team) | developers, SMB to enterprise |
| [GitHub Code Security (Dependabot)](https://github.blog/changelog/2025-04-01-github-advanced-security-is-here-for-github-team-organizations) | Dependabot alerts/updates plus premium dependency review bundled into GitHub | [Code Security $30/active committer/month; basic Dependabot included with GitHub](https://github.blog/changelog/2025-04-01-github-advanced-security-is-here-for-github-team-organizations) | GitHub-native teams, SMB to enterprise |
| [Mend Renovate Enterprise / Mend SCA](https://www.mend.io/?p=1196) | Automated dependency update PRs incl. transitive deps, merge confidence, SaaS or self-hosted | [Renovate Enterprise: an AWS Marketplace listing shows '100 CDs, $25,000.00'; the contract term is not confirmed and the listing did not load. Mend prices per Contributing Developer (pricing page FAQ). Mend SCA not public](https://www.mend.io/pricing/) | mid-market and enterprise |
| [Endor Labs](https://www.endorlabs.com/pricing) | SCA with function-level reachability and upgrade impact analysis to cut noise | [not public (per contributing developer, quote)](https://learn.microsoft.com/en-us/azure/defender-for-cloud/faq-endor-labs) | enterprise |
| [Socket](https://socket.dev/pricing) | Dependency supply-chain security: malicious package detection and vulnerable dependency alerts | [Free tier; Team about $25/dev/month, 5-dev minimum (third-party reports)](https://toolradar.com/tools/socket-dev/pricing) | developers, SMB to enterprise |
| [Semgrep Supply Chain](https://semgrep.dev/pricing) | SCA with reachability analysis bundled with Semgrep code scanning | [Free up to 10 contributors; $30-40/contributor/month (sources conflict)](https://semgrep.dev/docs/usage-and-billing) | developers, mid-market |
| [Aikido Security](https://www.aikido.dev/pricing) | All-in-one AppSec platform incl. SCA with reachability and AutoFix | [Free for 2 users; paid from about $300-350/month for 10 users (sources conflict)](https://codeant.ai/blogs/aikido-security-pricing) | SMB and startups |
| [Seal Security](https://appsecsanta.com/seal-security) | Backported patched library versions for unfixable or transitive vulnerable dependencies | [not public](https://www.helpnetsecurity.com/2024/02/14/seal-security-funding-7-4-million/) | mid-market and enterprise |

- **Willingness to pay**: Published SCA list prices cluster around $25-30/developer/month: Snyk Team $25/contributing dev/month, GitHub Code Security $30/active committer/month. Mend prices Renovate Enterprise per contributing developer, but publishes no confirmed list price. Buyers pay, but switch on price, and free Dependabot sets a low baseline. [source 1](https://snyk.io/start/team) [source 2](https://github.blog/changelog/2025-04-01-github-advanced-security-is-here-for-github-team-organizations) [source 3](https://www.mend.io/pricing/)
- **Bundling risk (high)**: GitHub includes Dependabot alerts and security updates with the platform and sells Code Security add-ons, so baseline detect-and-bump is effectively free.
- **Users complaining about price or vendors**: 28% of statements: [Add support for European Union Vulnerability Database (EUVD)](https://github.com/DependencyTrack/dependency-track/issues/4863), [Explore container security scanning signals for update candi](https://github.com/magrhino/wudup/issues/410), [Self-hosted Kali and BlackArch apt mirrors for supply chain ](https://github.com/Strike48-public/pick/issues/135).
- **Where paying customers are underserved**:
  - Transitive vulns blocked by parent version ranges or missing lockfile entries get no automatic fix PR ([evidence](https://docs.github.com/en/enterprise-cloud@latest/code-security/reference/supply-chain-security/troubleshoot-dependabot/vulnerability-detection))
  - Per-developer pricing causes sticker shock as teams grow to 30-50 developers ([evidence](https://dev.to/rahulxsingh/8-best-snyk-alternatives-for-developer-security-in-2026-326k))
  - Reachability and AutoFix locked to paid/enterprise tiers; free tiers only alert ([evidence](https://www.g2.com/products/semgrep-supply-chain/pricing))
  - No policy to fast-track security fixes past release-age cooldowns used against supply-chain attacks ([evidence](https://github.com/oven-sh/bun/issues/26065))

**Evidence** (18 need statements; top 8):

- [Add support for European Union Vulnerability Database (EUVD)](https://github.com/DependencyTrack/dependency-track/issues/4863) — github, 58 engagement, 2025
- [Provide good container securityContext by default for each chart](https://github.com/falcosecurity/charts/issues/481) — github, 51 engagement, 2023
- [Update dependencies to resolve security vulnerabilities in sub-dependencies](https://github.com/renovatebot/renovate/issues/3080) — github, 48 engagement, 2019
- [Add a config option to disable proxying for all private packages (to shield against dependency confu](https://github.com/verdaccio/verdaccio/issues/2103) — github, 18 engagement, 2021
- [vm2 Sandbox Escape vulnerability](https://github.com/release-it/release-it/issues/1024) — github, 16 engagement, 2023
- [[FEATURE] Include a NetworkPolicy to secure communication inside of Longhorn](https://github.com/longhorn/longhorn/issues/1805) — github, 15 engagement, 2020
- [💬 RFC: Proposal to Remove `node-libs-browser` Dependency](https://github.com/backstage/backstage/issues/28740) — github, 15 engagement, 2025
- [Option to bypass minimumReleaseAge when the update fixes a vulnerability](https://github.com/oven-sh/bun/issues/26065) — github, 14 engagement, 2026

## 2. AWS role credentials for workloads

> Engineers running workloads in EKS, Lambda or outside AWS struggle to get tools to use role-based, short-lived credentials via the default chain instead of static or expiring keys.

Gap score **0.606** · stability 0.41 · segments: cloud-security · keywords: aws, environment, roles, role, iam, credential

- **Demand**: 11 need statements, total engagement 361, 18% from the last 2 years.
**Opportunity:** AWS-only role credentials are free and native; paid money sits in multi-cloud workload identity/NHI platforms, already crowded and consolidating (Cyera-Oasis, Palo Alto-CyberArk). A narrow opening: cheap self-serve cross-cloud workload identity for mid-market teams, priced against per-identity Vault/Infisical bills and Aembit's $20/workload Teams tier.

- **Open-source supply** (GitHub repositories for `aws credential provider`): 80 repos, leader 709★, 5 of the top 10 pushed in the last year. Leading projects: [aws/aws-workload-credentials-provider](https://github.com/aws/aws-workload-credentials-provider) 709★, [jenkinsci/aws-secrets-manager-credentials-provider-plugin](https://github.com/jenkinsci/aws-secrets-manager-credentials-provider-plugin) 65★, [61418/boto3-refresh-session](https://github.com/61418/boto3-refresh-session) 53★.
- **Threat relevance** 3/3: Leaked static AWS keys are a top cloud breach path; role-based short-lived credentials remove them. No candidate fits. NVD CVEs matching the query: 12.

**Paid market** — crowdedness 3/3, willingness to pay 2/3, bundling risk high. ⚠ 1 claim(s) here not fully supported by their source (see fact-check).

| Vendor | Offering | Pricing | Sells to |
|---|---|---|---|
| [Aembit Workload IAM](https://aembit.io/pricing/) | Workload IAM: secretless, policy-based access using native cloud identities across clouds | [free Starter tier (10 workloads or 3 AI agents); Teams starts at $20/workload/month (workloads) and $20/agent/month (agentic AI), per Aembit's FAQ; Enterprise priced by scale](https://aembit.io/faq/) | mid-market / enterprise |
| [Teleport Machine & Workload Identity](https://goteleport.com/about/newsroom/press-releases/teleport-unveils-machine-and-workload-identity-solution/) | Short-lived certificates and workload identity for machines, CI/CD and services | [not public (MWI bundled in Enterprise Standard; each tbot instance billed as a Teleport Protected Resource, hourly-averaged; no separate per-MWI price)](https://goteleport.com/pricing/guide/) | mid-market / enterprise |
| [Defakto (formerly SPIRL)](https://www.kuppingercole.com/research/rs81394/rising-star-defakto) | SPIFFE-based non-human identity platform issuing short-lived workload identities | [not public (subscription)](https://www.securityweek.com/defakto-raises-30-million-for-non-human-iam-platform/) | enterprise |
| [HCP Vault Dedicated (HashiCorp/IBM)](https://hashicorp.com/pricing/all) | Secrets manager with dynamic short-lived AWS credentials via AWS secrets engine | [hourly cluster fee plus ~$112.17/client/month (Standard and Plus tiers, official HashiCorp price list)](https://hashicorp.com/pricing/all) | mid-market / enterprise |
| [Akeyless](https://www.akeyless.io/?p=1547) | SaaS secrets and machine identity with workload identity federation across clouds | [free 5 clients; paid tiers not public](https://www.akeyless.io/?p=1547) | mid-market / enterprise |
| [Infisical](https://infisical.com/pricing) | Open-core secrets and machine identity with AWS IAM role-based auth | [free tier; Pro $20/identity/month billed annually ($23 monthly); Advanced $40 annually](https://infisical.com/pricing.md) | SMB / developers / mid-market |
| [Oasis NHI Security Cloud (now Cyera Identity)](https://aws.amazon.com/marketplace/pp/prodview-wl52yxutluvma) | Non-human identity discovery, posture and lifecycle management; Oasis acquired by Cyera (~$1B, 2026) and operates as Cyera Identity | [AWS Marketplace 'Cyera Identity (Oasis) Starter Pack' $100,000/12 months (legacy Oasis-branded listing showed $50,000/12 months)](https://aws.amazon.com/marketplace/pp/prodview-wl52yxutluvma) | enterprise |
| [CyberArk (Palo Alto Networks)](https://paloaltonetworks.com/company/press/2026/palo-alto-networks-completes-acquisition-of-cyberark-to-secure-the-ai-era) | Machine identity, secrets management and PAM, now part of Palo Alto platform | [not public](https://www.softwarereviews.com/vendor-technology-notes/palo-alto-networks-completes-cyberark-deal-expanding-zero-trust-to-machine-identity) | enterprise |

- **Willingness to pay**: Established paid products with public prices: HCP Vault Dedicated ~$112.17/client/month (Standard, official price list), Aembit Teams from $20/workload/month (Aembit FAQ), Cyera Identity (Oasis) Starter Pack $100,000/12 months on AWS Marketplace. [source 1](https://hashicorp.com/pricing/all) [source 2](https://aembit.io/faq/) [source 3](https://aws.amazon.com/marketplace/pp/prodview-wl52yxutluvma)
- **Bundling risk (high)**: AWS gives IRSA, EKS Pod Identity and IAM Roles Anywhere (no service charge) plus SDK default-chain support for free, covering the core in-AWS and off-AWS need.
- **Users complaining about price or vendors**: 18% of statements: [[AWS] Support the new EKS Pod Identity Agent](https://github.com/external-secrets/external-secrets/issues/2951), [Enable specific role assumption in ProviderConfig](https://github.com/crossplane-contrib/provider-aws/issues/606).
- **Where paying customers are underserved**:
  - Per-identity/per-client pricing scales with machine count, punishing workload-heavy teams (Infisical Pro $20-23/identity, HCP Vault ~$112/client, Aembit $20/workload). ([evidence](https://dev.to/beton/infisical-pricing-teardown-2026-1ang))
  - Paid secrets tools lag new AWS mechanisms: Vault lacked IAM Roles Anywhere; External Secrets broke on EKS Pod Identity. ([evidence](https://github.com/hashicorp/vault/issues/16268))
  - Workload identity is mostly sold as quote-only or large enterprise bundles (Teleport TPR-metered Enterprise, Defakto, Cyera Identity $100k/12-month starter); Aembit Teams at $20/workload is the main self-serve exception. ([evidence](https://goteleport.com/pricing/guide/))
  - Consolidation (CyberArk to Palo Alto, Astrix to Cisco) leaves buyers wary of standalone NHI vendor roadmaps. ([evidence](https://startwithidentity.com/vendors/ai-identity/aembit/))

**Evidence** (11 need statements; top 8):

- [Obtain credentials from `cli/cache` json file](https://github.com/aws/aws-sdk-go/issues/3186) — github, 104 engagement, 2020
- [[AWS] Support the new EKS Pod Identity Agent](https://github.com/external-secrets/external-secrets/issues/2951) — github, 69 engagement, 2023
- [Support AWS_ROLE_ARN Environment Variable with Environment Credential Provider](https://github.com/aws/aws-sdk-go-v2/issues/2867) — github, 44 engagement, 2019
- [Would you mind clarifying how to add additional Roles/Users to the AWS AUTH during EKS provisioning](https://github.com/terraform-aws-modules/terraform-aws-eks/issues/1901) — github, 35 engagement, 2022
- [Support AWS IAM Roles Anywhere for AWS Secrets Engine](https://github.com/hashicorp/vault/issues/16268) — github, 27 engagement, 2022
- [S3 Client to be able to inherit IAM permissions from runtime / environment](https://github.com/oven-sh/bun/issues/22711) — github, 19 engagement, 2025
- [AWS ECR Permanent Credentials Feature Request](https://github.com/runpod/runpod-python/issues/415) — github, 18 engagement, 2025
- [Using env var in vault agent conf](https://github.com/hashicorp/vault/issues/11571) — github, 14 engagement, 2021

## 3. SCIM user provisioning for applications

> Admins of SaaS and self-hosted apps struggle with manual user provisioning and deprovisioning because products lack SCIM support for IdPs like Okta and Azure AD.

Gap score **0.501** · stability 0.52 · segments: appsec-supply-chain, cloud-security, identity-access · keywords: scim, provisioning, user, support, api, feature

- **Demand**: 23 need statements, total engagement 147, 48% from the last 2 years.
**Opportunity:** Developer-side SCIM is crowded and being bundled free by Auth0/Clerk; little room. A narrower opening: buyer-side provisioning for apps without SCIM or with enterprise-locked SCIM (Stitchflow's niche), sold to mid-market IT teams.

- **Open-source supply** (GitHub repositories for `scim provisioning`): 244 repos, leader 2269★, 9 of the top 10 pushed in the last year. Leading projects: [ory/polis](https://github.com/ory/polis) 2269★, [jelhub/scimgateway](https://github.com/jelhub/scimgateway) 232★, [AzureAD/SCIMReferenceCode](https://github.com/AzureAD/SCIMReferenceCode) 193★.
- **Threat relevance** 2/3: Prompt deprovisioning removes orphaned accounts attackers reuse; no candidate covers valid-account abuse. NVD CVEs matching the query: 5.

**Paid market** — crowdedness 3/3, willingness to pay 2/3, bundling risk high. ⚠ 2 claim(s) here not fully supported by their source (see fact-check).

| Vendor | Offering | Pricing | Sells to |
|---|---|---|---|
| [WorkOS](https://workos.com) | Enterprise SSO and Directory Sync (SCIM) APIs for B2B SaaS developers | [Per connection: $125/mo for connections 1-15, falling to $65 at 51-100; SSO and SCIM billed as separate connections](https://workos.com/pricing) | developers (B2B SaaS selling upmarket) |
| [Stytch](https://stytch.com) | B2B auth platform with SSO and SCIM connections from one shared pool | [Pay-as-you-go: 5 SSO/SCIM connections free (shared pool), then $125 per connection/month; annual contract also sold via AWS Marketplace (see wtp_sources)](https://stytch.com/pricing?vertical=B2B) | developers / B2B SaaS |
| [SSOJet](https://ssojet.com) | Low-cost enterprise SSO and SCIM layer for SaaS apps | [Business: $79 per connection/month billed monthly or $59 billed annually (2-4 connections; SSO and SCIM each count as one); volume discounts above; older listings show a $99/mo base structure](https://ssojet.com/pricing/) | SMB / startup SaaS developers |
| [Ory Polis (formerly BoxyHQ SAML Jackson)](https://www.ory.com/polis) | Open-source enterprise SSO and SCIM 2.0 directory sync, self-host or managed | [Open source self-hosted; managed/enterprise usage-based, price not public](https://www.ory.com/blog/introducing-ory-polis-for-enterprise-single-sign-on) | developers / self-hosting SaaS |
| [Auth0 (Okta)](https://auth0.com) | CIAM platform with B2B enterprise connections and inbound SCIM | [Free B2B tier includes 1 SSO connection plus SCIM (Feb 2026); B2B Essentials from $150/mo at 500 MAU; extra connections $100/mo](https://clerk.com/articles/auth-platforms-with-sso-and-scim-in-the-base-tier-2) | developers / mid-market to enterprise |
| [Clerk](https://clerk.com) | Developer auth platform bundling SCIM with enterprise connections | [Pro $25/mo with one enterprise connection; SCIM bundled at no extra charge (vendor-authored source)](https://clerk.com/articles/auth-platforms-with-sso-and-scim-in-the-base-tier) | developers / startups |
| [Stitchflow](https://www.stitchflow.com) | Provisions apps lacking SCIM via browser automation tied to Okta/Entra | [Vendor claims under $5K per app per year; list price not public](https://www.stitchflow.com/blog/automate-scim-provisioning-without-enterprise-tier) | mid-market IT teams (app buyers) |
| [Okta Lifecycle Management](https://www.okta.com/products/lifecycle-management/) | IdP-side automated provisioning/deprovisioning to SCIM-enabled apps | [Included in Core Essentials ($14/user/month), Essentials ($17/user/month) and higher Workforce suites; add-on on Starter ($6/user/month), add-on price not public; billed annually, $1,500 annual minimum](https://www.okta.com/pricing/) | mid-market / enterprise IT |

- **Willingness to pay**: SaaS developers pay published per-connection prices: Stytch $125/mo after 5 free, or a $25,000/yr contract on AWS Marketplace; WorkOS and SSOJet per-connection prices are in the vendor rows. IT buyers pay enterprise-tier upgrades or Okta Workforce suites that include Lifecycle Management (Core Essentials $14 or Essentials $17 per user/month, billed annually, $1,500 minimum; on the $6 Starter suite it is an add-on), but resent the SSO/SCIM tax. [source 1](https://stytch.com/pricing?vertical=B2B) [source 2](https://aws.amazon.com/marketplace/pp/prodview-mk7ac2kpntwec) [source 3](https://www.okta.com/pricing/)
- **Bundling risk (high)**: Auth platforms now give SCIM away (Auth0 free B2B tier with SCIM, Clerk bundles it on Pro), compressing standalone SCIM-as-a-service pricing toward zero.
- **Users complaining about price or vendors**: 13% of statements: [E88 Additional authentication options](https://github.com/Chris-Wolfgang/wms/issues/735), [SCIM - Will not provision groups with special chars other th](https://github.com/postmanlabs/postman-app-support/issues/12551), [feature: SCIM Support for Decentralized Collaboration](https://github.com/penpot/penpot/issues/8152).
- **Where paying customers are underserved**:
  - App buyers: 42-43% of 721 SaaS apps lock SCIM behind enterprise tiers; 57% offer no SCIM at all ([evidence](https://www.stitchflow.com/blog/scim-tax-worst-offenders))
  - Per-connection pricing bills SSO and SCIM separately, ~$250/mo per enterprise customer, painful for low-ACV SaaS ([evidence](https://www.activepieces.com/blog/workos-pricing-what-each-connection-costs-2026))
  - Okta's entry Starter suite ($6/user/month) lacks Lifecycle Management; IdP-side SCIM provisioning needs an add-on or an upgrade to Core Essentials ($14/user/month) or above ([evidence](https://www.okta.com/pricing/))
  - Self-hosted/open-source auth stacks (SuperTokens, FusionAuth, better-auth) still lack native SCIM support ([evidence](https://github.com/supertokens/supertokens-core/issues/1009))

**Evidence** (23 need statements; top 8):

- [[Feature] SCIM support](https://github.com/FusionAuth/fusionauth-issues/issues/106) — github, 41 engagement, 2019
- [SCIM Provisioning on SSO Plugin](https://github.com/better-auth/better-auth/issues/3276) — github, 38 engagement, 2025
- [Implement SCIM](https://github.com/go-vikunja/vikunja/issues/1399) — github, 11 engagement, 2025
- [Add SCIM support to provision and manage user accounts in Postman.](https://github.com/postmanlabs/postman-app-support/issues/6235) — github, 9 engagement, 2019
- [feat: Data Access Workflow](https://github.com/open-metadata/OpenMetadata/issues/12713) — github, 8 engagement, 2023
- [Unable to turn on SCIM via the okta API from reading the docs](https://github.com/okta/okta-developer-docs/issues/5130) — github, 8 engagement, 2024
- [Implement Additional Validation for SCIM Server](https://github.com/FusionAuth/fusionauth-issues/issues/2695) — github, 7 engagement, 2024
- [[feature]: Add workspaces to group projects and share members across them](https://github.com/croffasia/itsaplan/issues/258) — github, 7 engagement, 2026

## 4. Dependency context for vulnerability impact

> Teams analyzing SBOMs and advisories struggle to tell how a vulnerability affects their product because reports lack dependency hierarchy, parent component, container and vendor advisory context.

Gap score **0.49** · stability 0.73 · segments: appsec-supply-chain · keywords: dependency, dependency track, track, reports, impact, component

- **Demand**: 6 need statements, total engagement 83, 0% from the last 2 years.
**Opportunity:** Real but competitive opening: an affordable hosted SBOM impact/VEX layer (CSAF ingestion, dependency paths, container mapping) for mid-size software and device vendors preparing for CRA's Dec 2027 SBOM duty, between free Dependency-Track and enterprise quote-only platforms.

- **Open-source supply** (GitHub repositories for `vulnerability impact analysis`): 295 repos, leader 65★, 5 of the top 10 pushed in the last year. Leading projects: [alexdevassy/AI-Powered-Vulnerability-Impact-Analyzer](https://github.com/alexdevassy/AI-Powered-Vulnerability-Impact-Analyzer) 65★, [pchukwuemeka424/Machine-Learning-and-Morphometric-Analysis-for-Runoff-Dynamics-Enhancing-Flood](https://github.com/pchukwuemeka424/Machine-Learning-and-Morphometric-Analysis-for-Runoff-Dynamics-Enhancing-Flood) 54★, [Mario-Kart-Felix/solar-wind-hacker-book](https://github.com/Mario-Kart-Felix/solar-wind-hacker-book) 24★.
- **Threat relevance** 2/3: Dependency context speeds triage of vulnerable or compromised components, an indirect exposure reduction. ATT&CK: [T1195.001 Compromise Software Dependencies and Development Tools](https://attack.mitre.org/techniques/T1195/001). NVD CVEs matching the query: 28.

**Paid market** — crowdedness 2/3, willingness to pay 2/3, bundling risk medium. ⚠ 1 claim(s) here not fully supported by their source (see fact-check).

| Vendor | Offering | Pricing | Sells to |
|---|---|---|---|
| [Anchore Enterprise](https://anchore.com/pricing/) | SBOM generation and management with vulnerability scanning, risk scoring and VEX annotations | [AWS Marketplace 12-month contracts: $50,000 (Helm deployment), $34,500 (Cloud Image); Essential support plan $15,000](https://aws.amazon.com/marketplace/pp/prodview-ilkug4gdyavdq) | enterprise, public sector |
| [Manifest](https://g2.com/products/manifest-cyber-manifest/pricing) | SBOM and VEX management separating theoretical CVEs from actual product exposure | [not public](https://prnewswire.com/news-releases/manifest-inks-multi-year-sbom-deal-with-publicly-traded-medical-device-manufacturer-302156852.html) | enterprise; medical device makers (one disclosed multi-year deal) |
| [Interlynk](https://aws.amazon.com/marketplace/pp/prodview-n6mc7symiq2rm) | SBOM management and vulnerability tracking across products | [AWS Marketplace contracts by active developers: $18,000 (10), $36,000 (25), $60,000 (50), $100,000 (100)](https://aws.amazon.com/marketplace/pp/prodview-n6mc7symiq2rm) | mid-market software vendors |
| [Cybeats SBOM Studio](https://www.cybeats.com/sbom-studio.) | SBOM aggregation, vulnerability disposition workflow, VEX import/generation and sharing | [not public; subscription by monitored SBOMs/products, not seats](https://www.gartner.com/reviews/product/sbom-studio) | enterprise, manufacturers |
| [Finite State](https://finitestate.io/sbom-management) | Build-derived SBOMs enriched with exploit context, VEX and CRA compliance packages | [not public](https://finitestate.io/sbom-management) | connected-device manufacturers |
| [JFrog Xray (Transitive SBOM)](https://docs.jfrog.com/security/docs/transitive-sbom) | Dependency graph tree view showing direct vs transitive components from artifacts/SBOMs | [not public in sources found](https://docs.jfrog.com/security/docs/transitive-sbom) | enterprise |
| [ArmorCode](https://helpnetsecurity.com/2026/06/17/armorcode-agentic-ai-platform-cra-capabilities/) | Continuous SBOM and VEX management for CRA product manufacturers | [not public](https://helpnetsecurity.com/2026/06/17/armorcode-agentic-ai-platform-cra-capabilities/) | enterprise |
| [ONEKEY](https://www.onekey.com/resource/dependency-track-alternative) | Firmware SBOM and vulnerability analysis with compliance mapping, Dependency-Track alternative | [not public](https://www.onekey.com/resource/dependency-track-alternative) | embedded and IoT manufacturers |

- **Willingness to pay**: Public AWS Marketplace prices: Interlynk SBOM contracts $18k-$100k by active developers; Anchore Enterprise $34.5k-$50k per 12 months. Manifest signed a three-year device-maker deal (value undisclosed). [source 1](https://aws.amazon.com/marketplace/pp/prodview-n6mc7symiq2rm) [source 2](https://aws.amazon.com/marketplace/pp/prodview-ilkug4gdyavdq) [source 3](https://commission.europa.eu/news-and-media/news/safer-and-more-secure-digital-products-2026-09-11_en)
- **Bundling risk (medium)**: AWS Inspector exports SBOMs free and JFrog/SCA suites add graph views, but cross-vendor VEX/CSAF product-impact analysis is not given away by clouds.
- **Users complaining about price or vendors**: 17% of statements: [Feature: documenting external/extraneous dependencies](https://github.com/CycloneDX/specification/issues/321).
- **Where paying customers are underserved**:
  - Teams on free Dependency-Track lack parent-component, container and vendor-advisory context; commercial tools are enterprise quote-only ([evidence](https://github.com/ICTU/quality-time/issues/8687))
  - Dependency-Track has no vendor-managed cloud with support and no reachability; no affordable hosted upgrade path ([evidence](https://www.reversinglabs.com/blog/owasp-dependency-track-update-key-changes-and-limitations-on-software-risk-management?menu=hide))
  - Ingesting vendor CSAF advisories to match against SBOMs is missing in common tooling ([evidence](https://github.com/DependencyTrack/dependency-track/issues/2353))
  - Transitive dependency graph views only work on some input types (bundled artifacts) ([evidence](https://docs.jfrog.com/security/docs/transitive-sbom))

**Evidence** (6 need statements; top 8):

- [Add support for advisories defined in CSAF](https://github.com/DependencyTrack/dependency-track/issues/2353) — github, 43 engagement, 2023
- [Feature: documenting external/extraneous dependencies](https://github.com/CycloneDX/specification/issues/321) — github, 24 engagement, 2023
- [Native Image --enable-sbom option generates SBOM with dependency references and hierarchy](https://github.com/oracle/graal/issues/7729) — github, 7 engagement, 2023
- [Wishlist / inquiry: "advisory impact" standard.](https://github.com/rustsec/rustsec/issues/505) — github, 6 engagement, 2022
- [Display which parent dependency the current dependency is part of in Dependency-Track](https://github.com/ICTU/quality-time/issues/8687) — github, 2 engagement, 2024
- [Trivy Operator Sbom Reports on Dependency track visualisation based on Container](https://github.com/takumakume/sbomreport-to-dependencytrack/issues/11) — github, 1 engagement, 2024

## 5. Managing SIEM log noise and ingestion

> Small security teams struggle to filter noisy logs, enrich and monitor log feeds, and turn SIEM alerts into processed actions without high cost.

Gap score **0.473** · stability 0.51 · segments: smb-security-ops · keywords: siem, messages, pre, real, logs, events

- **Demand**: 7 need statements, total engagement 92, 14% from the last 2 years.
**Opportunity:** Crowded, well-funded enterprise market rapidly being bundled into SIEMs. Only a thin opening: self-serve, transparently priced, low-ops log reduction for small teams or MSSPs on Sentinel/Elastic/Wazuh, likely low ACV.

- **Open-source supply** (GitHub repositories for `siem log filtering`): 52 repos, leader 328★, 4 of the top 10 pushed in the last year. Leading projects: [jmasarweh/UniFi-Insights-Plus](https://github.com/jmasarweh/UniFi-Insights-Plus) 328★, [lprat/logstash-plugins](https://github.com/lprat/logstash-plugins) 10★, [sanesecurityguy/opnsense-ruleset-for-wazuh](https://github.com/sanesecurityguy/opnsense-ruleset-for-wazuh) 9★.
- **Threat relevance** 2/3: Feed monitoring can catch disabled logging; noise reduction aids detection broadly but indirectly. ATT&CK: [T1685.002 Disable or Modify Cloud Log](https://attack.mitre.org/techniques/T1685/002), [T1685.001 Disable or Modify Windows Event Log](https://attack.mitre.org/techniques/T1685/001). NVD CVEs matching the query: 0.

**Paid market** — crowdedness 3/3, willingness to pay 2/3, bundling risk high. ⚠ 2 claim(s) here not fully supported by their source (see fact-check).

| Vendor | Offering | Pricing | Sells to |
|---|---|---|---|
| [Cribl Stream](https://cribl.io) | Telemetry pipeline to filter, reduce, enrich and route logs before SIEM | [Cribl.Cloud free up to 1 TB/day; paid Stream ingest credits ~$0.27/GB (Standard, up to 5 TB/day) to $0.32/GB (Enterprise), $1 per credit, plus worker infrastructure](https://cribl.io/pricing/) | enterprise / large SOC |
| [DataBahn](https://www.databahn.ai) | Security data pipeline; vendor-reported claims of up to 60% lower SIEM ingestion costs (Microsoft Sentinel integration) and 40-50% telemetry reduction | [not public](https://tfir.io/databahn-microsoft-sentinel-security-data-pipeline/) | enterprise |
| [Tenzir](https://tenzir.com) | Security-focused pipeline engine (TQL) for SIEM, cloud and data cost optimization | [Open-source edition free; commercial editions not public](https://cybersectools.com/compare/edge-delta-security-data-pipelines-vs-tenzir-tql) | security teams with data-engineering skills |
| [Edge Delta Security Data Pipelines](https://edgedelta.com/product/security-data-pipelines) | Edge-processed security pipelines with silent-source detection | [not public (free trial)](https://edgedelta.com/company/blog/introducing-edge-delta-security-data-pipelines) | mid-market / enterprise |
| [Monad](https://www.monad.com) | Security data ingestion and pipeline platform | [not public on vendor site (AWS Marketplace listings exist, tier figures unverified)](https://cybersectools.com/compare/monad-vs-edge-delta-security-data-pipelines) | mid-market / enterprise |
| [Observo AI (SentinelOne)](https://www.sentinelone.com) | AI-native telemetry pipeline to enrich, summarize and route data; acquired by SentinelOne | [not public](https://sentinelone.com/press/sentinelone-to-acquire-observo-ai) | enterprise |
| [Onum (CrowdStrike)](https://www.crowdstrike.com) | Real-time telemetry pipeline feeding Falcon Next-Gen SIEM; acquired by CrowdStrike | [not public](https://ir.crowdstrike.com/news-releases/news-release-details/crowdstrike-agrees-acquire-onum-supercharge-falcon-next-gen-siem) | enterprise |
| [Splunk Edge Processor](https://www.splunk.com) | Filter, mask, transform and route data before Splunk indexing | [Included with Splunk Cloud Platform at no additional cost](https://www.splunk.com/en_us/blog/platform/introducing-edge-processor-next-gen-data-transformation) | Splunk customers (enterprise) |

- **Willingness to pay**: Enterprises pay per-GB pipeline fees (Cribl.Cloud ~$0.27-0.32/GB in credits above a free tier of up to 1 TB/day) to cut SIEM bills, and SIEM/XDR vendors buy pipeline startups (e.g. CrowdStrike agreed to acquire Onum); but PeerSpot reviewers call Cribl costly as volume scales and ask for pricing tiers by enterprise size or data volume (one small-scale user finds pricing good), and the generous free tier caps what small teams would pay. [source 1](https://cribl.io/pricing/) [source 2](https://ir.crowdstrike.com/news-releases/news-release-details/crowdstrike-agrees-acquire-onum-supercharge-falcon-next-gen-siem) [source 3](https://www.peerspot.com/products/cribl-reviews/page-3)
- **Bundling risk (high)**: SIEM vendors bundle or buy pipelines: Splunk Edge Processor is free with Splunk Cloud, CrowdStrike bought Onum, SentinelOne bought Observo, Sentinel added cheap data-lake tiers.
- **Users complaining about price or vendors**: 43% of statements: [Are SIEM and NIDS/HIDS complementary?](https://security.stackexchange.com/questions/133218/are-siem-and-nids-hids-complementary), [DNS Processor for Ingest Pipelines](https://github.com/elastic/elasticsearch/issues/91624), [[FEATURE] Real-time SIEM integration with automatic alert pr](https://github.com/ZainGuard/InvestigAI/issues/4).
- **Where paying customers are underserved**:
  - Cribl's volume-based pricing draws reviewer complaints (costly as data volume scales; 'charges for everything it sees rather than everything it processes'); a reviewer asks for pricing options based on enterprise size or data volume ([evidence](https://www.peerspot.com/products/cribl-reviews/page-3))
  - Pipeline tools need data-engineering effort to build and maintain; fit large SOCs, not small teams ([evidence](https://betterstack.com/community/comparisons/sumo-logic-vs-cribl/))
  - Most security pipeline vendors publish no pricing; contact-sales only, blocking self-serve small-team buyers ([evidence](https://cybersectools.com/compare/monad-vs-edge-delta-security-data-pipelines))
  - Independent pipelines being absorbed by SIEM/XDR vendors, reducing vendor-neutral options ([evidence](https://softwareanalyst.substack.com/p/the-convergence-of-siems-and-data))

**Evidence** (7 need statements; top 8):

- [SIEM log pre-filtering question](https://security.stackexchange.com/questions/41068/siem-log-pre-filtering-question) — stackexchange, 29 engagement, 2013
- [Are SIEM and NIDS/HIDS complementary?](https://security.stackexchange.com/questions/133218/are-siem-and-nids-hids-complementary) — stackexchange, 17 engagement, 2016
- [DNS Processor for Ingest Pipelines](https://github.com/elastic/elasticsearch/issues/91624) — github, 16 engagement, 2022
- [SIEM Alien Vault recommended method for muting noise](https://security.stackexchange.com/questions/161782/siem-alien-vault-recommended-method-for-muting-noise) — stackexchange, 16 engagement, 2017
- [Feature request: Support for heartbeat messages for outputs](https://github.com/falcosecurity/falcosidekick/issues/278) — github, 14 engagement, 2021
- [Collecting Attacker Feeds](https://github.com/telekom-security/tpotce/issues/1545) — github, 0 engagement, 2024
- [[FEATURE] Real-time SIEM integration with automatic alert processing](https://github.com/ZainGuard/InvestigAI/issues/4) — github, 0 engagement, 2025

## 6. CycloneDX SBOM output and attestation

> Supply-chain teams want tools to emit and accept CycloneDX SBOMs (and VEX) and tie them to releases through attestations.

Gap score **0.454** · stability 1.0 · segments: appsec-supply-chain · keywords: cyclonedx, spdx, sbom, bom, vex, v1

- **Demand**: 6 need statements, total engagement 114, 50% from the last 2 years.
**Opportunity:** Modest opening: SBOM+VEX lifecycle management for SMB manufacturers facing EU CRA (Dec 2027) and FDA 524B, with transparent pricing. Crowded with funded specialists (Anchore, Manifest, Interlynk); attestation alone is bundled by GitHub/Docker.

- **Open-source supply** (GitHub repositories for `cyclonedx sbom`): 1005 repos, leader 9950★, 10 of the top 10 pushed in the last year. Leading projects: [anchore/syft](https://github.com/anchore/syft) 9950★, [DependencyTrack/dependency-track](https://github.com/DependencyTrack/dependency-track) 4499★, [aboutcode-org/scancode-toolkit](https://github.com/aboutcode-org/scancode-toolkit) 2678★.
- **Threat relevance** 1/3: SBOM format support and attestations are mostly compliance and interoperability; candidates are unrelated. NVD CVEs matching the query: 2.

**Paid market** — crowdedness 2/3, willingness to pay 2/3, bundling risk medium. ⚠ 1 claim(s) here not fully supported by their source (see fact-check).

| Vendor | Offering | Pricing | Sells to |
|---|---|---|---|
| [Anchore Enterprise](https://anchore.com/) | SBOM storage, CycloneDX/SPDX import-export, policy and compliance reporting | [AWS Marketplace 12-month contract dimensions, no single list price: Enterprise Helm deployment $50,000; Enterprise Cloud Image (single host) $34,500; Essential Customer Success Plan add-on $15,000; custom pricing available](https://aws.amazon.com/marketplace/pp/prodview-ilkug4gdyavdq) | enterprise, public sector |
| [Interlynk](https://interlynk.io/) | SBOM automation platform: storage, monitoring, VEX and policy enforcement | [free Community tier; AWS Marketplace 12-month SaaS contracts by active developers: $18,000 (10), $36,000 (25), $60,000 (50), $100,000 (100)](https://aws.amazon.com/marketplace/pp/prodview-n6mc7symiq2rm) | SMB to enterprise, device makers |
| [sbomify](https://sbomify.com/) | Open-source SBOM hub for publishing and sharing SBOMs with customers | [Community $0; Business $159/month billed annually ($199 billed monthly); Enterprise tier listed without public price](https://sbomify.com/pricing/) | SMB, software vendors |
| [Manifest](https://www.manifestcyber.com/) | SBOM and AIBOM ingestion, management and FDA compliance workflows | [not public](https://prnewswire.com/news-releases/manifest-inks-multi-year-sbom-deal-with-publicly-traded-medical-device-manufacturer-302156852.html) | enterprise, medical devices |
| [Sonatype SBOM Manager](https://www.sonatype.com/) | SBOM management and vulnerability tracking for produced and consumed software | [not public (contract-based on AWS Marketplace)](https://www.g2.com/products/sonatype-sbom-manager/reviews) | enterprise |
| [Cybeats SBOM Studio](https://www.cybeats.com/product/sbom-studio) | SBOM management, sharing and vulnerability monitoring | [not public (quote)](https://www.g2.com/products/cybeats/pricing) | enterprise, device manufacturers |
| [ReversingLabs Spectra Assure](https://www.reversinglabs.com/products/spectra-assure) | SBOM import/export (incl. CycloneDX variants) with binary risk analysis | [quote; tiers by SBOM import volume](https://www.rfp.wiki/vendors/reversinglabs) | enterprise |
| [Docker Scout](https://docs.docker.com/scout/) | Uses build-time SBOM attestations on images for policy and vulnerability analysis | [free tier; Team $9 per repo/month](https://www.docker.com/?p=40309) | developers, SMB to enterprise |

- **Willingness to pay**: Public list prices: Anchore Enterprise $34,500-$50,000/year plus $15,000 support plan; Interlynk $18k-$100k/year by active developers; sbomify Business $159/month billed annually. [source 1](https://aws.amazon.com/marketplace/pp/prodview-ilkug4gdyavdq) [source 2](https://aws.amazon.com/marketplace/pp/prodview-n6mc7symiq2rm) [source 3](https://sbomify.com/pricing/)
- **Bundling risk (medium)**: GitHub and Docker already bundle SBOM attestations at build, but cross-vendor SBOM/VEX lifecycle management and regulator-facing workflows are not given away by platforms.
- **Users complaining about price or vendors**: 33% of statements: [Provide CycloneDX SBOM as an alternative to SPDX SBOM](https://github.com/goharbor/harbor/issues/21444), [Add support for Cyclonedx as a predicate type](https://github.com/in-toto/attestation/issues/82).
- **Where paying customers are underserved**:
  - Artifact attestations for private repos require GitHub Enterprise Cloud; smaller teams can't tie SBOMs to releases cheaply ([evidence](https://docs.github.com/en/code-security/concepts/supply-chain-security/supply-chain-security))
  - Management platforms mostly quote-only; few transparent-priced options for small manufacturers facing CRA SBOM duties ([evidence](https://fossid.com/articles/sbom-implementation-eu-cyber-resilience-act-cra/))
  - Inspector exports only CycloneDX 1.4; bundled exports lag current CycloneDX spec and VEX ([evidence](https://docs.aws.amazon.com/inspector/latest/user/sbom-export.html))
  - SBOM-based vulnerability management yields noisy results; VEX workflow to suppress false positives remains immature ([evidence](https://arxiv.org/html/2511.20313))

**Evidence** (6 need statements; top 8):

- [Provide CycloneDX SBOM as an alternative to SPDX SBOM](https://github.com/goharbor/harbor/issues/21444) — github, 31 engagement, 2025
- [Add support for Cyclonedx as a predicate type](https://github.com/in-toto/attestation/issues/82) — github, 27 engagement, 2022
- [support generating an additional SBOM file based on CycloneDX format](https://github.com/goreleaser/goreleaser/issues/2808) — github, 25 engagement, 2022
- [Give the possibility to atomically upload a SBOM with related VEX](https://github.com/DependencyTrack/dependency-track/issues/1872) — github, 24 engagement, 2022
- [Add support for CycloneDX v1.7 schema](https://github.com/CycloneDX/cyclonedx-gradle-plugin/issues/832) — github, 7 engagement, 2026
- [feat(loxel): attest release DMGs, update zips and the SBOM with GitHub artifact attestations](https://github.com/bizimind/loxel/issues/1360) — github, 0 engagement, 2026

## 7. SBOM generation across build ecosystems

> Maintainers and compliance-driven teams struggle to generate, sign, assemble and publish accurate SBOMs from their package managers and container builds to meet regulatory guidance.

Gap score **0.443** · stability 0.74 · segments: appsec-supply-chain · keywords: sbom, sboms, tool, package, packages, software

- **Demand**: 31 need statements, total engagement 222, 35% from the last 2 years.
**Opportunity:** Not a standalone business: generation is commoditized by OSS (Syft) and bundled by GitHub, Docker and AWS Inspector. Only an accuracy/verification layer for hard ecosystems (C/C++, binaries, hand-installed packages) might sell to regulated device makers.

- **Open-source supply** (GitHub repositories for `sbom generation`): 310 repos, leader 1464★, 9 of the top 10 pushed in the last year. Leading projects: [owasp-dep-scan/dep-scan](https://github.com/owasp-dep-scan/dep-scan) 1464★, [NuGuardAI/nuguard](https://github.com/NuGuardAI/nuguard) 72★, [demcon/cmake-sbom](https://github.com/demcon/cmake-sbom) 65★.
- **Threat relevance** 2/3: Component inventory speeds response to compromised dependencies, but SBOM generation itself prevents nothing. ATT&CK: [T1195.001 Compromise Software Dependencies and Development Tools](https://attack.mitre.org/techniques/T1195/001), [T1195.002 Compromise Software Supply Chain](https://attack.mitre.org/techniques/T1195/002). NVD CVEs matching the query: 0.

**Paid market** — crowdedness 3/3, willingness to pay 1/3, bundling risk high. ⚠ 1 claim(s) here not fully supported by their source (see fact-check).

| Vendor | Offering | Pricing | Sells to |
|---|---|---|---|
| [Anchore Enterprise](https://anchore.com/) | SBOM generation (Syft-based), storage and policy for containers and CI | [AWS Marketplace 12-month contracts: Cloud Image (single host) $34,500; Helm deployment $50,000; Essential Customer Success Plan add-on $15,000](https://aws.amazon.com/marketplace/pp/prodview-ilkug4gdyavdq) | enterprise, public sector |
| [Docker Scout](https://docs.docker.com/scout/) | Generates/indexes image SBOMs and build attestations; vulnerability and policy views | [bundled in Docker subscriptions: Personal $0 (1 Scout repo), Pro $9-11/user/mo (2 repos), Team $15-16/user/mo and Business $24/user/mo (unlimited Scout repos)](https://www.docker.com/pricing/) | developers, SMB to enterprise |
| [Snyk (SBOM export)](https://snyk.io/) | CycloneDX/SPDX SBOM export for monitored open-source and container projects | [Enterprise plan only; contact sales](https://docs.snyk.io/developer-tools/snyk-cli/commands/sbom) | enterprise |
| [FOSSA](https://fossa.com/) | SCA and license compliance with SBOM generation and export | [free tier plus Business tier; amount not verified](https://fossa.com/blog/fossa-business-tier/) | SMB to enterprise |
| [ReversingLabs Spectra Assure](https://www.reversinglabs.com/products/spectra-assure) | Binary analysis producing SBOMs and risk reports for built packages | [quote; volume-based tiers, 14-day trial](https://reversinglabs.com/pricing/software-supply-chain-security) | enterprise, software producers |
| [SOOS](https://soos.io/) | SCA with SBOM generation and management | [Community $0; Core SCA $99/month per TrustRadius](https://www.trustradius.com/products/soos/pricing) | SMB, developers |

- **Willingness to pay**: Paid SBOM platforms list prices (Anchore $34,500/yr per host on AWS Marketplace; Snyk export Enterprise-only), but GitHub exports SBOMs on its free dependency graph, undercutting paying for generation alone. [source 1](https://aws.amazon.com/marketplace/pp/prodview-ilkug4gdyavdq) [source 2](https://docs.snyk.io/developer-tools/snyk-cli/commands/sbom) [source 3](https://docs.github.com/en/code-security/how-tos/secure-your-supply-chain/establish-provenance-and-integrity/exporting-a-software-bill-of-materials-for-your-repository)
- **Bundling risk (high)**: GitHub exports SBOMs from its dependency graph and AWS Inspector exports CycloneDX/SPDX to S3 for its (paid) scanning customers, with no separate export charge on its pricing page; Docker Scout is free for 1 repo.
- **Users complaining about price or vendors**: 13% of statements: [Generate CycloneDX SBOM file from vcpkg](https://github.com/microsoft/vcpkg/issues/30461), [Add ability to customize 3rd party licences output](https://github.com/angular/angular-cli/issues/26272), [Adding purl to generated SBOM](https://github.com/microsoft/vcpkg/issues/39254).
- **Where paying customers are underserved**:
  - Generators disagree and omit dependencies; no vendor sells verified-accurate SBOMs across ecosystems ([evidence](https://cs.ucr.edu/~heng/pubs/sbom-dsn24.pdf))
  - 30-70% of manually installed packages in Docker images missed by common SBOM tools ([evidence](https://arxiv.org/pdf/2606.13966))
  - SBOM export locked to Snyk Enterprise; SMBs needing compliance SBOMs pay enterprise prices ([evidence](https://docs.snyk.io/developer-tools/snyk-cli/commands/sbom))
  - Binary/commercial-component SBOM coverage gated to higher ReversingLabs tiers; C/C++ builds poorly served ([evidence](https://www.rfp.wiki/vendors/reversinglabs))

**Evidence** (31 need statements; top 8):

- [sign SBOMs through cosign tool right after generated it through bom tool](https://github.com/kubernetes/release/issues/2286) — github, 36 engagement, 2021
- [[Feature Request]: generating SBOMs for container images while building them](https://github.com/docker/roadmap/issues/274) — github, 33 engagement, 2021
- [pip should record the original index url or find links url of the package](https://github.com/pypa/pip/issues/10736) — github, 14 engagement, 2021
- [[IDEA] Publish Software Bill of Materials (SBOM)](https://github.com/nextgenhealthcare/connect/issues/5852) — github, 13 engagement, 2023
- [Support attestations as artifacts in SPDX 3.1](https://github.com/spdx/spdx-3-model/issues/594) — github, 13 engagement, 2024
- [Feature: Allow one sbom to be the primary document in assemble action](https://github.com/interlynk-io/sbomasm/issues/128) — github, 11 engagement, 2024
- [Ask HN: Open-source SBOM generation tools?](https://news.ycombinator.com/item?id=32227594) — hn, 11 engagement, 2022
- [Generate CycloneDX SBOM file from vcpkg](https://github.com/microsoft/vcpkg/issues/30461) — github, 10 engagement, 2023

## 8. IAM-based authentication in AWS service clients

> Cloud teams moving off static passwords and keys find their clients and tools can't authenticate to RDS, MSK, Redshift, API Gateway or ArgoCD with short-lived AWS IAM credentials.

Gap score **0.404** · stability 0.47 · segments: cloud-security, identity-access · keywords: iam, aws, authentication, auth, amazon, com

- **Demand**: 15 need statements, total engagement 314, 27% from the last 2 years.
**Opportunity:** Little standalone opening: the need is client-library plumbing that AWS and open source fill for free. Money only exists inside broader access-proxy platforms (Teleport, StrongDM), a crowded segment; at most a developer-tool feature, not a startup.

- **Open-source supply** (GitHub repositories for `aws iam authentication`): 474 repos, leader 2338★, 5 of the top 10 pushed in the last year. Leading projects: [kubernetes-sigs/aws-iam-authenticator](https://github.com/kubernetes-sigs/aws-iam-authenticator) 2338★, [otterize/intents-operator](https://github.com/otterize/intents-operator) 313★, [joshuamkite/terraform-aws-ssh-bastion-service](https://github.com/joshuamkite/terraform-aws-ssh-bastion-service) 212★.
- **Threat relevance** 2/3: Short-lived IAM tokens replace static database and service passwords, shrinking the window for stolen-credential reuse. ATT&CK: [T1550.001 Application Access Token](https://attack.mitre.org/techniques/T1550/001). NVD CVEs matching the query: 6.

**Paid market** — crowdedness 3/3, willingness to pay 1/3, bundling risk high. ⚠ 1 claim(s) here not fully supported by their source (see fact-check).

| Vendor | Offering | Pricing | Sells to |
|---|---|---|---|
| [Amazon RDS Proxy](https://aws.amazon.com/rds/proxy/) | Managed DB proxy, now with end-to-end IAM authentication for RDS/Aurora MySQL and PostgreSQL | [usage-based, per vCPU-hour (or per ACU-hour for Aurora Serverless), region-dependent](https://aws.amazon.com/rds/proxy/pricing/) | developers / all AWS customers |
| [Teleport (Database Access / Machine & Workload Identity)](https://goteleport.com/docs/ver/17.x/enroll-resources/database-access/enroll-aws-databases/rds.md) | Identity-aware proxy that uses IAM auth to RDS, issuing short-lived credentials | [not public (quote-based; usage-based on monthly active users and Teleport Protected Resources, with each tbot machine-identity instance counted as a TPR, no separate per-MWI price)](https://goteleport.com/_uploads/Teleport_Pricing_Guide_Rev_June_16_2026_5f41774f5e.pdf) | mid-market / enterprise |
| [StrongDM](https://strongdm.com/pricing) | Infrastructure access proxy for databases, servers and Kubernetes with credential brokering | [per user; third-party listings ~$50/user/month, AWS Marketplace Essentials $840/user/year](https://www.g2.com/products/strongdm/pricing) | mid-market / enterprise |
| [hoop.dev](https://hoop.dev/blog/an-identity-aware-proxy-for-aws-rds-using-iam-authentication) | Identity-aware access gateway for databases including AWS RDS with IAM authentication | [not public](https://hoop.dev/blog/an-identity-aware-proxy-for-aws-rds-using-iam-authentication) | developers / SMB |
| [Aembit Workload IAM](https://aembit.io/pricing/) | Secretless workload-to-service access with credential injection and access policies | [free Starter (10 workloads); Teams/Enterprise price not confirmed on vendor page](https://docs.aembit.io/get-started/signup-options/) | mid-market / enterprise |

- **Willingness to pay**: Buyers pay for broad access platforms: Vendr's StrongDM page (fetched 2026-11-23) reports a median of ~$36k/yr based on 86 purchases, with smaller teams (10-25 users) at roughly $25k-$60k/yr. IAM itself is usable at no additional charge per AWS's RDS docs, so the per-client auth plumbing has no paid line item to displace. [source 1](https://www.vendr.com/marketplace/strongdm) [source 2](https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/UsingWithRDS.IAM.html)
- **Bundling risk (high)**: AWS already ships IAM auth for RDS/MSK/Redshift/API Gateway plus free open-source signers in every major language and RDS Proxy, so remaining gaps get closed by AWS or OSS maintainers.
- **Users complaining about price or vendors**: 13% of statements: [Support IAM Authentication from ArgoCD clients](https://github.com/argoproj/argo-cd/issues/481), [Azure : add support for Bleu Sovereign Cloud](https://github.com/prowler-cloud/prowler/issues/13248).
- **Where paying customers are underserved**:
  - Popular third-party clients and ORMs (Prisma, kafka-go, ArgoCD) lack native AWS IAM auth; vendors don't sell client-side fixes. ([evidence](https://github.com/prisma/orm/issues/6587))
  - RDS IAM auth caps around 200 new connections/second; the AWS workaround, RDS Proxy, adds per-vCPU cost. ([evidence](https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/UsingWithRDS.IAMDBAuth.html))
  - Access proxies that broker IAM DB auth (Teleport, StrongDM) are quote-based or seat-minimum, heavy for small teams. ([evidence](https://www.capterra.co.uk/software/181859/strongdm))
  - API Gateway IAM (SigV4) invocation from generic tooling relies on per-tool support that is often missing. ([evidence](https://github.com/aws/aws-tools-for-powershell/issues/180))

**Evidence** (15 need statements; top 8):

- [Support for IAM Roles (Instance Profile/IRSA) for Authentication](https://github.com/opensearch-project/logstash-output-opensearch/issues/96) — github, 70 engagement, 2021
- [Support IAM Authentication to AWS RDS](https://github.com/prisma/orm/issues/6587) — github, 69 engagement, 2021
- [SASL: Support AWS_MSK_IAM mechanism](https://github.com/segmentio/kafka-go/issues/661) — github, 31 engagement, 2021
- [Support scoped-API token based authentication with Cloudflare](https://github.com/cert-manager/cert-manager/issues/2036) — github, 28 engagement, 2019
- [Support use of cleartext auth plugin](https://github.com/HeidiSQL/HeidiSQL/issues/296) — github, 25 engagement, 2018
- [Redshift Serverless IAM Auth Support](https://github.com/aws/aws-toolkit-jetbrains/issues/3498) — github, 20 engagement, 2023
- [Support IAM Authentication from ArgoCD clients](https://github.com/argoproj/argo-cd/issues/481) — github, 19 engagement, 2018
- [Invoke API Gateway with IAM Auth request signing](https://github.com/aws/aws-tools-for-powershell/issues/180) — github, 19 engagement, 2020

## Excluded as incoherent

| Theme | Keywords | Namer's reason |
|---|---|---|
| 1 | secrets, secret, scanning, github, ci, tokens | Only about four statements concern secret scanning; rest are unrelated requests. |
| 4 | issue, feature, github, request, https, github com | Grouped by GitHub issue template text; needs are all different. |
| 5 | policy, cspm, security, groups, controller, feature request | Cloud config requests to different tools with distinct asks. |
| 6 | kubernetes, pod, security, kubernetes io, io, io docs | Pod security forms a minority; SIEM and SCIM items unrelated. |
| 9 | cargo, package, images, audit, file, env | Scanning-related but distinct asks across different tools; one off-topic. |
| 12 | 10, network, siem, ip, browser, logs | Loosely network-related but each asks for a different capability. |
| 13 | people, report, secure, data, access, looking | Grouped by generic words; needs span unrelated domains. |
| 15 | yml, evaluate, p3, sast, research, repo | Different supply-chain issues; no single product addresses most. |

