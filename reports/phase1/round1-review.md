# Phase 1 review — round 1

Labels from the relevance judge (Claude Code subagent) using [docs/rubrics/relevance.md](../docs/rubrics/relevance.md). Pass = on-segment rate ≥ threshold. `need` is the baseline for the Phase 2 filter.

| Segment | Sampled | On-segment | Need | Result |
|---|---|---|---|---|
| cloud-security | 20 | 13 (65%) | 5 | pass |
| appsec-supply-chain | 20 | 18 (90%) | 7 | pass |
| identity-access | 20 | 7 (35%) | 1 | FAIL |
| smb-security-ops | 20 | 12 (60%) | 6 | pass |

## cloud-security

| # | Source | Eng. | Title | Seg. | Need | Judge's reason |
|---|---|---|---|---|---|---|
| 1 | github | 1806 | [macOS 11 Big Sur compatibility on Apple Silicon](https://github.com/Homebrew/brew/issues/7857) | n | n | macOS/Homebrew compatibility, not cloud security |
| 2 | hn | 344 | [AWS IAM is having issues again](https://news.ycombinator.com/item?id=24498678) | n | n | AWS IAM service outage, not posture or IAM sprawl |
| 3 | hn | 342 | [AWS IAM Roles, a tale of unnecessary complexity](https://news.ycombinator.com/item?id=33566419) | y | y | Complaint about unnecessary complexity of AWS IAM roles |
| 4 | hn | 320 | [Awsviz.dev simplifying AWS IAM policies](https://news.ycombinator.com/item?id=40922740) | y | n | Tool launch for simplifying IAM policies |
| 5 | hn | 318 | [Kubernetes Security Assessment [pdf]](https://news.ycombinator.com/item?id=20655017) | y | n | Kubernetes security assessment document, no stated gap |
| 6 | github | 306 | [[FEATURE] Support Amazon Bedrock as backend for Claude Desktop / Cowork](https://github.com/anthropics/claude-code/issues/32668) | n | n | Claude Desktop backend request, not cloud security |
| 7 | hn | 256 | [AWS IAM Policies in a Nutshell](https://news.ycombinator.com/item?id=13940771) | y | n | IAM policy explainer/tutorial |
| 8 | hn | 256 | [Kubernetes Security – Best Practice Guide](https://news.ycombinator.com/item?id=16764743) | y | n | Kubernetes security best-practice guide |
| 9 | hn | 212 | [Kubernetes Security Best Practices](https://news.ycombinator.com/item?id=18906788) | y | n | Kubernetes security best-practice guide |
| 10 | hn | 132 | [Show HN: Policy_sentry, an AWS IAM Least Privilege Policy Generator](https://news.ycombinator.com/item?id=21262954) | y | n | Show HN launch of least-privilege policy generator |
| 11 | hn | 105 | [An AWS IAM Security Tooling Reference](https://news.ycombinator.com/item?id=41350151) | y | n | Reference list of IAM security tools |
| 12 | hn | 105 | [AWS IAM having issues yet again](https://news.ycombinator.com/item?id=24656111) | n | n | AWS IAM service outage, not posture or IAM sprawl |
| 13 | github | 104 | [Obtain credentials from `cli/cache` json file](https://github.com/aws/aws-sdk-go/issues/3186) | y | y | Feature request: IAM authenticator support for AWS SSO credentials |
| 14 | github | 84 | [StorageBrowser RFC](https://github.com/aws-amplify/amplify-ui/issues/5731) | n | n | S3 storage browser UI component RFC |
| 15 | github | 75 | [Kubernetes Hardening Guide](https://github.com/kubernetes/sig-security/issues/30) | y | n | Proposal to write a hardening guide, documentation work |
| 16 | github | 72 | [Terragrunt Stack Dependencies](https://github.com/gruntwork-io/terragrunt/issues/5663) | n | n | Terragrunt configuration feature, not security |
| 17 | github | 70 | [Support for IAM Roles (Instance Profile/IRSA) for Authentication](https://github.com/opensearch-project/logstash-output-opensearch/issues/96) | y | y | Request for IAM role auth to avoid static credentials |
| 18 | github | 69 | [Support IAM Authentication to AWS RDS](https://github.com/prisma/orm/issues/6587) | y | y | Request for AWS IAM database authentication support |
| 19 | github | 69 | [[AWS] Support the new EKS Pod Identity Agent](https://github.com/external-secrets/external-secrets/issues/2951) | y | y | Secrets operator lacks EKS Pod Identity support |
| 20 | github | 60 | [[Sandbox] kube-burner](https://github.com/cncf/sandbox/issues/57) | n | n | Kubernetes performance tool sandbox application |

## appsec-supply-chain

| # | Source | Eng. | Title | Seg. | Need | Judge's reason |
|---|---|---|---|---|---|---|
| 1 | hn | 212 | [Microsoft open sources Salus software bill of materials (SBOM) generation tool](https://news.ycombinator.com/item?id=32104805) | y | n | News: Microsoft open-sources SBOM tool |
| 2 | hn | 199 | [Firmware Software Bill of Materials (SBoM) Proposal](https://news.ycombinator.com/item?id=38248758) | y | n | SBOM proposal announcement, no stated pain |
| 3 | hn | 175 | [Open source projects could sell SBOM fragments](https://news.ycombinator.com/item?id=43080378) | y | n | Opinion piece on SBOM business model |
| 4 | github | 91 | [Rust Roadmap](https://github.com/pnpm/pnpm/issues/11633) | n | n | Package manager Rust roadmap |
| 5 | github | 58 | [Add support for European Union Vulnerability Database (EUVD)](https://github.com/DependencyTrack/dependency-track/issues/4863) | y | y | Request for EUVD vulnerability source in Dependency-Track |
| 6 | github | 49 | [Tag a new version with the security fix](https://github.com/matthew-andrews/isomorphic-fetch/issues/191) | y | n | Request to tag release, not a missing capability |
| 7 | github | 48 | [Update dependencies to resolve security vulnerabilities in sub-dependencies](https://github.com/renovatebot/renovate/issues/3080) | y | y | Renovate lacks PRs fixing vulnerable sub-dependencies |
| 8 | github | 43 | [Add support for advisories defined in CSAF](https://github.com/DependencyTrack/dependency-track/issues/2353) | y | y | Missing CSAF advisory support; CPE not granular enough |
| 9 | github | 38 | [Containerize](https://github.com/nextcloud/nextcloudpi/issues/1589) | n | n | Containerizing NextcloudPi, not security |
| 10 | hn | 37 | [What an SBOM Can Do for You](https://news.ycombinator.com/item?id=29954947) | y | n | Explainer article on SBOM benefits |
| 11 | github | 36 | [sign SBOMs through cosign tool right after generated it through bom tool](https://github.com/kubernetes/release/issues/2286) | y | y | Request to sign SBOMs at generation time |
| 12 | github | 33 | [[Feature Request]: generating SBOMs for container images while building them](https://github.com/docker/roadmap/issues/274) | y | y | Feature request: SBOM generation in docker bake |
| 13 | github | 31 | [Provide CycloneDX SBOM as an alternative to SPDX SBOM](https://github.com/goharbor/harbor/issues/21444) | y | y | Request for CycloneDX SBOM output in Harbor |
| 14 | hn | 29 | [The Minimum Elements for a Software Bill of Materials (SBOM)](https://news.ycombinator.com/item?id=27815159) | y | n | Guidance document on SBOM minimum elements |
| 15 | github | 27 | [Add support for Cyclonedx as a predicate type](https://github.com/in-toto/attestation/issues/82) | y | y | Request for CycloneDX predicate type in in-toto |
| 16 | hn | 22 | [Show HN: Free secrets scanning for unlimited private GitHub repos](https://news.ycombinator.com/item?id=31355692) | y | n | Product launch of secrets scanning tool |
| 17 | hn | 22 | [The SBOM Frenzy Is Premature](https://news.ycombinator.com/item?id=33072821) | y | n | Opinion article on SBOM, title only |
| 18 | hn | 21 | [SBOM 101 – All the questions you were afraid to ask Software Bill of Materials](https://news.ycombinator.com/item?id=32565979) | y | n | SBOM introductory explainer |
| 19 | hn | 19 | [Show HN: Sighthound - open-source vulnerability scanner for source code](https://news.ycombinator.com/item?id=48847577) | y | n | Launch of open-source code vulnerability scanner |
| 20 | hn | 14 | [Why automate secrets scanning throughout your SDLC?](https://news.ycombinator.com/item?id=24649022) | y | n | Article promoting secrets scanning automation |

## identity-access

| # | Source | Eng. | Title | Seg. | Need | Judge's reason |
|---|---|---|---|---|---|---|
| 1 | hn | 323 | [Show HN: Skip the SSO Tax, access your user data with OSS](https://news.ycombinator.com/item?id=35524328) | y | n | Product launch, though motivated by SSO tax |
| 2 | hn | 183 | [An admittedly wandering defense of the SSO tax](https://news.ycombinator.com/item?id=41303844) | y | n | Opinion essay defending SSO tax |
| 3 | hn | 162 | [Launch HN: Idemeum (YC S21) – Passwordless access to apps and infrastructure](https://news.ycombinator.com/item?id=33346183) | y | n | Product launch of passwordless/PAM platform |
| 4 | hn | 137 | [Launch HN: AccessOwl (YC S22) – Automating SaaS Provisioning and Permissioning](https://news.ycombinator.com/item?id=32422871) | y | n | Product launch of SaaS provisioning tool |
| 5 | hn | 109 | [JumpServer: Open-Source Privileged Access Management](https://news.ycombinator.com/item?id=48723677) | y | n | Announcement of open-source PAM tool |
| 6 | hn | 105 | [Show HN: Shadow IT Scan – Uncover SaaS Apps, Users and Risky OAuth Scopes](https://news.ycombinator.com/item?id=41118468) | y | n | Product launch of shadow IT/OAuth scanner |
| 7 | hn | 94 | [Ask HN: What's your checklist for when you hand your laptop in for repair?](https://news.ycombinator.com/item?id=33231141) | n | n | Personal laptop repair privacy checklist |
| 8 | github | 86 | [A non hostile response](https://github.com/microsoft/vscode/issues/87468) | n | n | VSCode community discussion, not identity |
| 9 | hn | 70 | [ChaosDB: Unauthorized Privileged Access to Microsoft Azure Cosmos DB](https://news.ycombinator.com/item?id=28327661) | n | n | Cosmos DB vulnerability news |
| 10 | github | 66 | [[BUG] Claude Code Web Cannot Use gh CLI Commands (Permission Denied)](https://github.com/anthropics/claude-code/issues/11139) | n | n | Claude Code gh CLI bug report |
| 11 | github | 62 | [Access Reviews](https://github.com/hashicorp/terraform-provider-azuread/issues/927) | y | y | Feature request: manage Azure AD access reviews in Terraform |
| 12 | hn | 55 | [Attack Gave Chinese Hackers Privileged Access to U.S. Systems](https://news.ycombinator.com/item?id=9751683) | n | n | News about hacking attack |
| 13 | hn | 50 | [Tokyo Xtreme Racer Early Access Review: We Are So Back](https://news.ycombinator.com/item?id=43039140) | n | n | Video game review |
| 14 | github | 47 | [Run Docker container as non-root user](https://github.com/garethgeorge/backrest/issues/476) | n | n | Docker container user mapping request |
| 15 | github | 44 | [[Sandbox] Kaniko](https://github.com/cncf/sandbox/issues/88) | n | n | Kaniko CNCF sandbox application |
| 16 | github | 42 | [Revoke Certificates](https://github.com/cert-manager/cert-manager/issues/4747) | n | n | Certificate revocation feature, not identity access |
| 17 | github | 41 | [DP#17 - Localview: A Decentralized Yelp service](https://github.com/district0x/district-proposals/issues/17) | n | n | Decentralized review app proposal |
| 18 | github | 38 | [Proposal: Migrate Agones to the Linux Foundation](https://github.com/agones-dev/agones/issues/4304) | n | n | Game server project foundation migration |
| 19 | github | 37 | [AL-1563: Phase 25 Donor Dashboard Depth — implementation specification](https://github.com/Asymmetric-al/core/issues/1563) | n | n | Product specification unrelated to security |
| 20 | github | 34 | [Technical overview on how we can auto-update the search engine](https://github.com/meilisearch/meilisearch/issues/2570) | n | n | Search engine upgrade design |

## smb-security-ops

| # | Source | Eng. | Title | Seg. | Need | Judge's reason |
|---|---|---|---|---|---|---|
| 1 | stackexchange | 211 | [ELK Stack as a SIEM - First steps](https://security.stackexchange.com/questions/101296/elk-stack-as-a-siem-first-steps) | y | n | Learning how to set up ELK as SIEM |
| 2 | hn | 193 | [Launch HN: Matano (YC W23) – Open-Source Security Lake Platform (SIEM) for AWS](https://news.ycombinator.com/item?id=34505603) | y | n | Launch of low-cost SIEM alternative |
| 3 | hn | 187 | [Show HN: Panther v1.0 – Open Source, Cloud-Native SIEM](https://news.ycombinator.com/item?id=22686913) | y | n | Launch of open-source SIEM |
| 4 | hn | 163 | [Red Team's SIEM](https://news.ycombinator.com/item?id=19151271) | n | n | Title only, red team tooling unclear |
| 5 | stackexchange | 151 | [SIEM Question: Excessive Firewall Denies / Rule Edit Question](https://security.stackexchange.com/questions/103242/siem-question-excessive-firewall-denies-rule-edit-question) | y | y | Struggling to reduce noisy SIEM alerts |
| 6 | hn | 115 | [Elastic SIEM – Security Information and Event Management](https://news.ycombinator.com/item?id=20278139) | y | n | SIEM product announcement |
| 7 | stackexchange | 68 | [Log information for SIEM auditing in Linux](https://security.stackexchange.com/questions/71228/log-information-for-siem-auditing-in-linux) | y | n | How-to question on Linux event types |
| 8 | stackexchange | 64 | [SIEM system, what are the benefits?](https://security.stackexchange.com/questions/9684/siem-system-what-are-the-benefits) | y | y | Asks whether a tool exists for login anomaly detection |
| 9 | stackexchange | 45 | [SIEM and Windows Event Logs](https://security.stackexchange.com/questions/5275/siem-and-windows-event-logs) | y | n | General question on Windows logs for SIEM |
| 10 | stackexchange | 42 | [Detecting Tor Browser using SIEM](https://security.stackexchange.com/questions/158124/detecting-tor-browser-using-siem) | y | y | Cannot keep Tor node list synced in QRadar |
| 11 | hn | 41 | [Fortinet removes SSH and database backdoors from its SIEM product](https://news.ycombinator.com/item?id=22159847) | n | n | Vendor backdoor news |
| 12 | stackexchange | 32 | [Traditional SIEM in Kubernetes environments](https://security.stackexchange.com/questions/268250/traditional-siem-in-kubernetes-environments) | y | y | Traditional SIEM approach unclear for Kubernetes nodes |
| 13 | github | 31 | [Don't index so many saved object fields](https://github.com/elastic/kibana/issues/43673) | n | n | Kibana internal field mapping cleanup |
| 14 | stackexchange | 31 | [Datasets dedicated for SIEM systems](https://security.stackexchange.com/questions/195798/datasets-dedicated-for-siem-systems) | n | n | Request for research datasets, not operations |
| 15 | stackexchange | 29 | [SIEM log pre-filtering question](https://security.stackexchange.com/questions/41068/siem-log-pre-filtering-question) | y | y | SIEM cost pressure forces log pre-filtering |
| 16 | github | 26 | [Invoke-Obfuscation](https://github.com/SigmaHQ/sigma/issues/1009) | n | n | Offensive tool catalog entry |
| 17 | stackexchange | 21 | [SIEM: Monitoring End Users and DHCP IP assigning issue](https://security.stackexchange.com/questions/148912/siem-monitoring-end-users-and-dhcp-ip-assigning-issue) | y | y | SIEM cannot correlate DHCP IP reassignment |
| 18 | github | 17 | [[Infra UI] Show non-metric details on node detail page](https://github.com/elastic/kibana/issues/42689) | n | n | Infrastructure UI metadata request |
| 19 | github | 16 | [DNS Processor for Ingest Pipelines](https://github.com/elastic/elasticsearch/issues/91624) | n | n | Ingest pipeline DNS processor, data platform feature |
| 20 | github | 16 | [[Bug] [auditbeat] [winlogbeat] Running `setup` with `setup.ilm.check_exists: false` create](https://github.com/elastic/beats/issues/21725) | n | n | Beats mapping bug report |

