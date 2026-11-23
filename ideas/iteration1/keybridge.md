# Keybridge

> Turns the static AWS and GCP keys your cross-cloud and GitHub Actions workloads still use into linted native-federation pull requests, run inside your cloud.

Opening `cross-cloud-workload-identity` (priority 3) · from AWS role credentials for workloads (theme 10, stability 0.41)

## Buyer and user

- **Buyer:** Head of platform / DevOps lead (at smaller firms the VP Engineering or the first security hire), usually after a SOC 2 or CSPM finding on long-lived keys they have not managed to close — Software and data companies with 50-1,000 employees that are AWS-primary and also use GCP for one or two services (BigQuery, Vertex AI, GKE) with GitHub Actions CI; GCP organisation created before May 2024 (so service-account key creation was not blocked by default); already run a CSPM, Prowler or IAM Access Analyzer that flags old keys, yet still carry in-use AWS IAM user keys and GCP JSON keys that cross the AWS-GCP or CI boundary because nobody has had the week it takes to wire federation and change the consumers.
- **User:** Platform and DevOps engineers who own the CI workflows, Kubernetes manifests and Terraform that connect workloads (GitHub Actions jobs, EKS/GKE pods, Lambdas, VMs) to AWS and GCP APIs, and who would review and merge the generated pull requests.

## Problem

Short-lived workload credentials are now free in AWS and GCP, and CSPMs already flag old keys, yet the keys stay: 59% of AWS IAM users still have an active key over a year old. Removing an in-use key that crosses AWS, GCP or CI means finding its consumer, writing per-pair trust configuration and changing the consumer's code or manifests. Tools lag the mechanisms, and paid fixes are per-workload brokers or enterprise NHI platforms.

- Vault's AWS secrets engine lacked support for IAM Roles Anywhere, leaving workloads outside AWS without short-lived role credentials through the tool teams already pay for. ([source](https://github.com/hashicorp/vault/issues/16268))
- External Secrets v0.9.9 did not work with the new EKS Pod Identity Agent, which injects credentials through a different endpoint than IRSA; tool support trails each new AWS mechanism. ([source](https://github.com/external-secrets/external-secrets/issues/2951))
- Vault's client did not follow the AWS SDK default credential chain in IAM auth mode, so profile- and role-based setups failed. ([source](https://github.com/hashicorp/vault/issues/12568))
- Bun's S3 client could only be authorised with an explicit access key and secret, not the role credentials of the Lambda or Fargate runtime. ([source](https://github.com/oven-sh/bun/issues/22711))
- Users want the AWS SDK to pick up a role ARN with the environment credential provider for environments where web identity is not available. ([source](https://github.com/aws/aws-sdk-go-v2/issues/2867))
- Per-identity and per-client pricing scales with machine count (Infisical Pro $20-23/identity, Aembit $20/workload), penalising workload-heavy teams. ([source](https://dev.to/beton/infisical-pricing-teardown-2026-1ang))

## Why now

AWS added IAM outbound identity federation (STS GetWebIdentityToken, no additional cost), so AWS workloads can present short-lived JWTs to GCP and SaaS, and GCP workload identity federation accepts AWS identities; both halves of AWS-GCP keyless access are now free. Yet the backlog is not shrinking: Datadog's 2025 report finds 59% of AWS IAM users with an active key older than a year, unchanged since 2024, and GitGuardian counted 28.65 million new hardcoded secrets on public GitHub in 2025. Google now blocks service-account key creation by default only for organisations created on or after 3 May 2024, so older GCP estates keep their JSON keys. [1](https://aws.amazon.com/blogs/aws/simplify-access-to-external-services-using-aws-iam-outbound-identity-federation/) [2](https://cloud.google.com/iam/docs/workload-identity-federation-with-other-clouds) [3](https://www.datadoghq.com/state-of-cloud-security-2025/) [4](https://blog.gitguardian.com/the-state-of-secrets-sprawl-2026/) [5](https://docs.cloud.google.com/resource-manager/docs/secure-by-default-organizations)

## MVP

- **Self-hosted scanner (CLI, GitHub Action or Terraform-deployed job in the customer's own AWS account) that imports existing key findings (IAM credential report, IAM Access Analyzer, Prowler) and GCP service-account keys, and keeps only keys that are in use and cross the AWS-GCP or CI boundary. Nothing leaves the customer's environment; an optional opt-in summary sends counts only.** — Detection is already free and bundled, so v1 does not rebuild it; running in the customer's account removes the vendor-custody, log-export and GDPR-processor problems and shortens security review.
- **Consumer attribution with a confidence label: correlates CloudTrail management events (source IP, user agent, role), GitHub Actions runner ranges and workflow files that reference secret names (via a GitHub App with org Secrets read and Contents read, never admin:org), and GCP audit logs where enabled. Keys it cannot attribute are marked 'unknown' and get no cutover PR.** — GetAccessKeyLastUsed returns only date, service and region, so attribution must come from logs; being explicit about confidence is what makes a practitioner willing to merge.
- **Two-sided migration PRs for three supported paths only: GitHub Actions OIDC to AWS, GitHub Actions OIDC to GCP, and AWS workload to GCP via workload identity federation. Each change set covers the IAM/trust side (Terraform/OpenTofu) and the consumer side (workflow YAML permissions and auth step, Kubernetes service-account annotation, GCP credential-config file, removal of key env vars).** — A trust policy alone is half a migration; the consumer change is where teams stall and where breakage happens.
- **Mandatory policy-lint gate with published tests: blocks wildcard or missing GitHub 'sub' conditions, GCP AWS-provider pools without an attribute condition, missing audience restrictions, and runs IAM Access Analyzer policy validation on every generated AWS policy. PRs are never auto-merged.** — Federation must not replace a leaked key with an over-broad trust; strict, testable defaults are the safety case a security reviewer can check.
- **Shadow-mode cutover and monitoring: after merge, verifies in logs that the federated path is used and the key is idle for a set period before proposing deactivation; afterwards alerts when a new in-use boundary-crossing key appears and exports a dated per-estate record of keys found, replaced and remaining.** — Reduces the outage risk of deactivation and gives the platform lead a record for auditors, without claiming to certify any control.

Out of scope for v1: Azure/Entra, GitLab CI and on-prem (IAM Roles Anywhere needs a customer PKI); these come after the three AWS-GCP-GitHub paths are proven.; Our own credential helper or SDK shims; v1 points to the clouds' maintained helpers instead.; Keys held by third-party SaaS or platforms that cannot federate (e.g. tools that accept only an access key); flagged, not migrated.; Issuing credentials, a token broker in the request path or a credential-injecting proxy (Aembit's model).; Hosted multi-tenant scanning with cross-account roles into customer clouds, and any ingestion of customer logs on our side.; General secrets storage and rotation (Vault, Infisical, Akeyless), AI-agent identity, PAM, SPIFFE/SPIRE..

## Competition

| Competitor | How we differ |
|---|---|
| [Native cloud federation (AWS outbound identity federation, GitHub OIDC to AWS/GCP, GCP workload identity federation)](https://aws.amazon.com/blogs/aws/simplify-access-to-external-services-using-aws-iam-outbound-identity-federation/) | Free and what we configure, not replace. Each cloud documents only its own side; we write both sides plus the consumer change, linted, for the estate's actual keys. |
| [Free/bundled detection: IAM Access Analyzer unused-access findings, Prowler (open source)](https://hub.prowler.com/check/iam_rotate_access_key_90_days) | These find old and unused keys and recommend rotation or deactivation. We take their findings as input and do the remaining work for keys that are still in use: attribution and the two-sided federation change. |
| [Wiz (CSPM, owned by Google)](https://www.wiz.io/blog/how-to-get-rid-of-aws-access-keys-part-1-the-easy-wins) | Wiz finds keys on disk and in use and publishes the key-to-role playbook; it stops at the finding. We produce the change set. Wiz adding this is our biggest risk (see risks); we aim to be useful to Wiz customers, not to compete on detection. |
| [Aembit Workload IAM](https://aembit.io/faq/) | Aembit brokers access at $20/workload/month (Teams) with a free 10-workload tier and stays in the request path. We remove the key and leave only native federation, so nothing depends on us at runtime. |
| [Clutch Security](https://www.clutch.security/) | Clutch discovers and correlates non-human identities and secrets across cloud, SaaS, CI/CD and vaults, sold to enterprises. We do one narrow remediation job with a public, fixed price for mid-market teams. |
| [GitGuardian NHI Governance](https://www.gitguardian.com/nhi-governance) | Tracks secret consumers, rotation dates and stale secrets and semi-automates rotation. Rotation keeps a static key; we replace it with federation. |
| [Teleport Machine & Workload Identity](https://goteleport.com/pricing/guide/) | Bundled into Teleport Enterprise, billed per protected resource, quote-only, and requires running tbot. We need no new runtime component. |
| [Cyera Identity (formerly Oasis NHI Security Cloud)](https://aws.amazon.com/marketplace/pp/prodview-wl52yxutluvma) | Enterprise NHI discovery and posture from a $100,000/12-month starter pack. We are a fraction of that price and do remediation, not posture. |

**Differentiation:** Detection of old keys is already free; what is missing is closing the findings that are still in use. Keybridge takes existing findings, attributes each in-use AWS-GCP or CI key to its consumer with a stated confidence, and opens linted two-sided pull requests to free native federation. It runs in the customer's own account, leaves no broker in the request path and charges a fixed price per migration, not per workload.

## Build

- Team: 2 engineers (AWS/GCP IAM and Terraform depth) + 1 founder-seller; part-time security/compliance contractor for SOC 2 Type I
- Time to MVP: 5 months
- Hardest parts: Attributing in-use keys to consumers from CloudTrail and GCP audit logs when data events and GCP Data Access logs are off by default, and being honest when attribution is 'unknown'.; Generating correct consumer-side changes (workflow YAML, Kubernetes annotations, credential-config files) across repos the product does not own, so a merged PR does not break production.; Lint rules that catch over-broad trust (wildcard sub, unconditioned GCP AWS providers, missing audience) with no false sense of safety; keeping templates current as AWS and GCP change federation APIs.; Packaging the scanner so a mid-market security team can run it in their own account in under an hour.

## Pricing and business model

- **Model:** Fixed-price migration per estate plus a flat monitoring subscription by estate size; free self-hosted key report. Optional resale through DevOps consultancies.
- **Entry price:** Free self-hosted report; Migration $6,000 one-off per estate for up to 25 in-use boundary-crossing keys on the three supported paths ($150 per extra key); then Monitor $150/month flat for up to 100 AWS accounts and GCP projects.
- **Rationale:** The real alternative is doing it by hand, not Aembit: at our own estimate of about one engineer-day per in-use key (attribute, change both sides, verify, deactivate), 25 keys is roughly five engineer-weeks, so $6,000 is priced below that. Brokering the same 25 workloads on Aembit Teams list price would cost about $500/month for as long as the broker stays in place; per-identity secrets managers (Infisical Pro) store secrets rather than remove them. Pricing per migration matches a job that is mostly one-off, and a flat estate band avoids penalising AWS Organizations with many accounts. Year-one value per customer is about $7,800, which forces a low-touch motion (see risks). Enterprise NHI platforms (Cyera Identity at $100k/year) set the ceiling.

| Comparable | Price |
|---|---|
| Aembit Workload IAM | [Free up to 10 workloads; Teams from $20/workload/month](https://aembit.io/faq/) |
| Infisical | [Pro $20/identity/month billed annually ($23 monthly)](https://infisical.com/pricing.md) |
| Cyera Identity (Oasis) on AWS Marketplace | [Starter Pack $100,000 per 12 months](https://aws.amazon.com/marketplace/pp/prodview-wl52yxutluvma) |

## Go to market

- **First customers:** Ten 50-500 person AWS-primary SaaS or data companies using GCP for BigQuery, Vertex AI or GKE and GitHub Actions for CI, with a GCP organisation created before May 2024; each already has a CSPM or Prowler finding on long-lived keys that has stayed open for months, a platform team of 2-6 and no Vault or Teleport deployment.
- **Channel:** Free self-hosted report as a GitHub Action and CLI; content per migration path ('BigQuery from EKS without a JSON key'); resale and referral through DevOps consultancies and fractional platform teams who run migrations for SOC 2-bound startups; SOC 2 auditors and vCISOs as referrers. No cloud-marketplace listing in year one.
- **Wedge:** The free report answers a question the CSPM does not: which of your open key findings are still in use across AWS, GCP or CI, who uses them, and the PR that fixes each. It converts on the first merged, linted migration PR.

## Risks

- Bundling (high): Wiz (Google) already sees keys and their use in many target accounts and publishes the replacement playbook; a 'generate fix' feature there, or a native AWS/GCP federation wizard, would remove most of our value. Clutch, Astrix (to Cisco) and Cyera Identity can add migration playbooks to enterprise NHI suites.
- Small, shrinking problem: Datadog finds over half of old-key holders have not used them for 90+ days, which is hygiene CSPMs already handle; GCP blocks new service-account keys by default for organisations created since May 2024. In-use boundary-crossing keys may be only a handful per company.
- Weak economics: ~$7,800 first-year value and a mostly one-off job mean low retention after migration and little room for founder-led selling; the business only works if self-hosted install is self-serve and consultancies resell migrations.
- Technical and liability: wrong attribution or a generated consumer change can break production, and an over-broad trust can over-grant access. Mitigations are confidence labels, the lint gate, shadow-mode cutover, no auto-merge, and terms with a liability cap and no warranty of policy correctness; reports must not be marketed as compliance certification.
- Trust and supply chain: even self-hosted, the scanner and GitHub App sit near credentials; they need signed, reproducible releases, minimal permissions and a SOC 2 Type I before paid launch, which costs time and money for a three-person company.
- Thin demand signal: the input's evidence is AWS-only tool-lag issues filed by developers (theme stability 0.41); the cross-cloud need and the buyer's willingness to pay are inferred, not shown.

## Riskiest assumption

- **Assumption:** Mid-market AWS+GCP teams that already have CSPM key findings still carry enough in-use, boundary-crossing keys (not dead ones) that they will pay a fixed fee to have them migrated rather than do it themselves.
- **Cheap test:** Publish the read-only scanner as a script that runs in the customer's account and prints a local report; offer it to 40 platform leads from DevOps communities, the GitHub issues in the evidence and two DevOps consultancies. For those who run it, review the report with them and offer the $6,000 migration with a signed LOI or 50% deposit.
- **Success signal:** At least 10 of 40 run the script; the median report shows 10 or more in-use keys crossing AWS, GCP or CI that their CSPM finding has not closed for 3+ months; at least 3 sign an LOI or pay a deposit within two weeks; at least 2 security leads say they would approve the access model without escalation.

## Open questions

- How many in-use (not dead) boundary-crossing keys does a typical AWS+GCP mid-market estate have, and how many does attribution from default-on logs resolve?
- How many qualifying AWS-primary companies with a pre-2024 GCP organisation and GitHub Actions exist (bottom-up count needed before this can be sized)?
- Will DevOps consultancies resell a fixed-price migration, or treat it as work they would rather bill by the hour?
- Will buyers keep paying for monitoring after the migration, or is this a one-off product that should be priced entirely up front?
- How quickly will Wiz, AWS or Google ship a native 'fix this key with federation' flow?
- Can the HCP Vault per-client price (flagged as unverified) be confirmed from a primary source?

