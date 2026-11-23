# Gap report — 2026-11-23

732 need statements (from 2747 collected signals) grouped into 62 themes; 38 judged incoherent and excluded; 21 statements fit no theme.

**Gap score** = 0.3 × demand + 0.3 × supply gap + 0.25 × monetization + 0.15 × threat relevance. Supply gap weighs commercial crowdedness 60% and open-source supply 40%; monetization combines willingness to pay, the share of statements complaining about price or vendors, and bundling risk (decision D11). Each component is a percentile rank across themes (0–1), so scores are relative to this run, not absolute. Weights: [config/scoring.yaml](../../config/scoring.yaml).

**Stability** = how consistently a theme's statements cluster together across 3 other random seeds (1.0 = always). Treat themes below 0.5 as provisional.

**Paid-market data** (vendors, prices, gaps, willingness to pay) comes from a market researcher agent using web search, with a source link for every claim ([rubric](../docs/rubrics/market-research.md)). Prices change; check sources before relying on them.

**Fact-check** (round 1): an adversarial checker re-opened the sources for 72 vendor and willingness-to-pay claims; 35 are not fully supported by their cited source. Per-gap counts are shown below; details in [phase2/fact-check.json](phase2/fact-check.json).

## Ranking

| # | Gap | Score | Demand | Supply gap | Monetization | Threat | Crowdedness | Willingness to pay | Statements | Stability |
|---|---|---|---|---|---|---|---|---|---|---|
| 1 | [Managed SOC and MDR services procurement](#1-managed-soc-and-mdr-services-procurement) | **0.628** | 0.754 | 0.639 | 0.473 | 0.609 | 3/3 | 2/3 | 13 | 0.87 |
| 2 | [Permission gating for AI agent tool calls](#2-permission-gating-for-ai-agent-tool-calls) | **0.617** | 0.791 | 0.373 | 0.511 | 0.935 | 3/3 | 2/3 | 27 | 0.65 |
| 3 | [Authorization and auditing for MCP tool access](#3-authorization-and-auditing-for-mcp-tool-access) | **0.599** | 0.878 | 0.425 | 0.467 | 0.609 | 3/3 | 2/3 | 33 | 0.55 |
| 4 | [Affordable security programs for small businesses](#4-affordable-security-programs-for-small-businesses) | **0.596** | 0.683 | 0.65 | 0.668 | 0.196 | 3/3 | 2/3 | 16 | 0.8 |
| 5 | [User activity audit logging on servers](#5-user-activity-audit-logging-on-servers) | **0.59** | 0.802 | 0.413 | 0.538 | 0.609 | 3/3 | 2/3 | 22 | 0.76 |
| 6 | [Privileged access management procurement](#6-privileged-access-management-procurement) | **0.587** | 0.53 | 0.473 | 0.777 | 0.609 | 3/3 | 3/3 | 10 | 0.97 |
| 7 | [Third-party dependency vulnerability management](#7-third-party-dependency-vulnerability-management) | **0.581** | 0.628 | 0.442 | 0.478 | 0.935 | 3/3 | 2/3 | 12 | 0.85 |
| 8 | [Classified-approved mobile workstations for government](#8-classified-approved-mobile-workstations-for-government) | **0.534** | 0.393 | 0.655 | 0.761 | 0.196 | 3/3 | 3/3 | 6 | 0.7 |
| 9 | [Product cybersecurity regulation compliance for manufacturers](#9-product-cybersecurity-regulation-compliance-for-manufacturers) | **0.52** | 0.554 | 0.497 | 0.701 | 0.196 | 3/3 | 3/3 | 9 | 0.47 ⚠ |
| 10 | [Cloud security posture management configuration](#10-cloud-security-posture-management-configuration) | **0.518** | 0.248 | 0.54 | 0.761 | 0.609 | 3/3 | 3/3 | 8 | 0.53 |
| 11 | [Integrated EDR/XDR and SIEM deployment](#11-integrated-edrxdr-and-siem-deployment) | **0.505** | 0.335 | 0.565 | 0.576 | 0.609 | 3/3 | 3/3 | 5 | 1.0 |
| 12 | [SIEM log collection and noise filtering](#12-siem-log-collection-and-noise-filtering) | **0.5** | 0.472 | 0.483 | 0.489 | 0.609 | 3/3 | 2/3 | 11 | 0.94 |
| 13 | [Regulatory incident reporting and breach notification](#13-regulatory-incident-reporting-and-breach-notification) | **0.497** | 0.413 | 0.85 | 0.473 | 0.0 | 2/3 | 2/3 | 7 | 0.92 |
| 14 | [SBOM generation and publishing in builds](#14-sbom-generation-and-publishing-in-builds) | **0.474** | 0.633 | 0.453 | 0.228 | 0.609 | 3/3 | 1/3 | 22 | 0.68 |
| 15 | [Privileged access management procurement](#15-privileged-access-management-procurement) | **0.469** | 0.393 | 0.473 | 0.473 | 0.609 | 3/3 | 2/3 | 6 | 1.0 |
| 16 | [Secret detection in code and CI](#16-secret-detection-in-code-and-ci) | **0.457** | 0.296 | 0.326 | 0.522 | 0.935 | 3/3 | 2/3 | 9 | 0.57 |
| 17 | [SCIM user provisioning support for apps](#17-scim-user-provisioning-support-for-apps) | **0.451** | 0.465 | 0.465 | 0.571 | 0.196 | 3/3 | 2/3 | 11 | 0.78 |
| 18 | [Ransomware detection and recovery for file servers](#18-ransomware-detection-and-recovery-for-file-servers) | **0.446** | 0.261 | 0.47 | 0.348 | 0.935 | 3/3 | 2/3 | 7 | 1.0 |
| 19 | [PCI DSS compliance for web servers](#19-pci-dss-compliance-for-web-servers) | **0.443** | 0.696 | 0.566 | 0.141 | 0.196 | 3/3 | 1/3 | 17 | 0.53 |
| 20 | [SBOM dependency hierarchy and impact analysis](#20-sbom-dependency-hierarchy-and-impact-analysis) | **0.426** | 0.165 | 0.571 | 0.457 | 0.609 | 3/3 | 2/3 | 5 | 0.61 |
| 21 | [Cyber risk governance and disclosure compliance](#21-cyber-risk-governance-and-disclosure-compliance) | **0.418** | 0.452 | 0.449 | 0.473 | 0.196 | 3/3 | 2/3 | 8 | 0.92 |
| 22 | [Perimeter firewall refresh and licensing](#22-perimeter-firewall-refresh-and-licensing) | **0.415** | 0.535 | 0.357 | 0.473 | 0.196 | 3/3 | 2/3 | 8 | 1.0 |
| 23 | [Kubernetes pod security policy enforcement](#23-kubernetes-pod-security-policy-enforcement) | **0.375** | 0.304 | 0.523 | 0.141 | 0.609 | 3/3 | 1/3 | 7 | 0.86 |
| 24 | [CycloneDX SBOM and VEX support](#24-cyclonedx-sbom-and-vex-support) | **0.353** | 0.317 | 0.343 | 0.5 | 0.196 | 3/3 | 2/3 | 7 | 0.81 |

## 1. Managed SOC and MDR services procurement

> Spanish and Portuguese public bodies seek 24x7 managed SOC, MDR and SIEM/SOAR services with supporting cybersecurity platforms.

Gap score **0.628** · stability 0.87 · segments: open-discovery · keywords: del, el, la, 2026, 26, soc

- **Demand**: 13 need statements (13 buyer), total engagement 13, 100% from the last 2 years.
**Opportunity:** Paid demand is real but crowded and tender-driven: incumbents (Telefónica, Indra, S21sec, S2) hold ENS-certified SOCs and the state serves small councils. A startup fits only as a white-label/AI-SOC supplier to these integrators, not a direct bidder.

- **Open-source supply** (GitHub repositories for `managed soc mdr`): 7 repos, leader 0★, 7 of the top 10 pushed in the last year. Leading projects: [ammartiger/cavementech-services](https://github.com/ammartiger/cavementech-services) 0★, [ishandutta2007/Awesome-Managed-Threat-Hunting](https://github.com/ishandutta2007/Awesome-Managed-Threat-Hunting) 0★, [ishandutta2007/Awesome-Managed-Cloud-Consulting-Services](https://github.com/ishandutta2007/Awesome-Managed-Cloud-Consulting-Services) 0★.
- **Threat relevance** 2/3: 24x7 monitoring speeds detection of common intrusions, but is a procurement-level, indirect need. ATT&CK: [T1190 Exploit Public-Facing Application](https://attack.mitre.org/techniques/T1190), [T1133 External Remote Services](https://attack.mitre.org/techniques/T1133). NVD CVEs matching the query: 0.

**Paid market** — crowdedness 3/3, willingness to pay 2/3, bundling risk medium. ⚠ 1 claim(s) here not fully supported by their source (see fact-check).

| Vendor | Offering | Pricing | Sells to |
|---|---|---|---|
| [Telefónica Tech NextDefense](https://www.telefonicatech.com/en/cybersecurity) | MDR and managed SOC from 24/7 Madrid/Colombia operations centers, OT monitoring | [not public](https://socradar.io/blog/top-10-mssps-in-spain-in-2026/) | enterprise, public sector |
| [IndraMind Cybersecurity (Indra Group)](https://www.indramindcybersecurity.com/) | Sovereign managed SOC and Smart MDR AI-SOC agent for public and critical bodies | [not public](https://socradar.io/blog/top-10-mssps-in-spain-in-2026/) | public sector, defense, critical infrastructure |
| [S21sec (Thales)](https://www.s21sec.com/) | Managed SOC, MDR and DFIR from Madrid and Porto SOCs | [not public](https://socradar.io/blog/top-10-mssps-in-spain-in-2026/) | enterprise, regulated organizations (Spain and Portugal) |
| [S2 Grupo](https://s2grupo.es/) | IT and OT managed SOC and CERT services, National SOC Network founding member | [not public](https://socradar.io/blog/top-10-mssps-in-spain-in-2026/) | critical infrastructure, public sector |
| [Arctic Wolf MDR](https://aws.amazon.com/marketplace/pp/B09ZNWNF7T) | 24x7 MDR across network, endpoint and cloud with Concierge Security Team | [AWS Marketplace: MDR Basic up to 100 users $44,000 per 12 months; larger via private offer](https://aws.amazon.com/marketplace/pp/B09ZNWNF7T) | mid-market, enterprise |
| [CrowdStrike Falcon Complete](https://www.crowdstrike.com/en-us/pricing/) | 24/7 expert-led MDR on Falcon platform with breach prevention warranty | [not public (self-service Falcon tiers $7.99-$19.99/device/month exclude Complete)](https://www.crowdstrike.com/en-us/pricing/) | mid-market, enterprise |
| [UnderDefense MDR](https://underdefense.com/mdr-pricing/) | Per-asset MDR with unlimited investigations and 40-hour IR retainer | [from $11 per asset per month, annual contract; higher tiers by quote](https://underdefense.com/mdr-pricing/) | SMB, mid-market |
| [Microsoft Defender Experts Suite](https://www.microsoft.com/en-us/security/pricing/enterprise/featured-security-products) | Microsoft-run managed XDR, incident response and designated engineering | [per user per month, varies by plan; pre-purchase (price not published)](https://www.microsoft.com/en-us/security/pricing/enterprise/featured-security-products) | Microsoft 365 enterprise customers |

- **Willingness to pay**: Spanish tenders budget real money: Sagunto managed cybersecurity €369,836/2 years; Boadilla SOC platform €462,000/3 years; Cantabria health security office €1.95M/36 months. [source 1](https://ted.europa.eu/en/notice/-/detail/763467-2026) [source 2](https://ted.europa.eu/en/notice/-/detail/744958-2026) [source 3](https://ted.europa.eu/en/notice/-/detail/793260-2026)
- **Bundling risk (medium)**: The state's COCS-EELL already serves local entities under 50,000 residents via diputaciones and Microsoft sells managed XDR to E5 tenants, but larger bodies still tender paid 24x7 SOCs.
- **Users complaining about price or vendors**: 0% of statements.
- **Where paying customers are underserved**:
  - Mid-size councils outside the state COCS-EELL (under-50,000 residents) must tender their own SOC plus ENS governance office ([evidence](https://ted.europa.eu/en/notice/-/detail/763467-2026))
  - Buyers want SOC bundled with CISO-as-a-service and forensic hour banks, not standalone MDR tooling ([evidence](https://ted.europa.eu/en/notice/-/detail/803347-2026))
  - Public buyers need ENS-certified SOCs in the National SOC Network, which global MDRs without Spanish delivery lack ([evidence](https://socradar.io/blog/top-10-mssps-in-spain-in-2026/))
  - Global MDR entry tiers are USD per-user annual contracts (Arctic Wolf $44k/100 users), misfit for small public bodies ([evidence](https://aws.amazon.com/marketplace/pp/B09ZNWNF7T))

**Evidence** (13 need statements; top 8):

- [CP nº18/2026 - Aquisição de serviço de proteção Anti-DDoS](https://ted.europa.eu/en/notice/-/detail/814236-2026) — ted, 1 engagement, 2026
- [Servicio gestionado de ciberseguridad y CISOaaS y SOC 24x7 para Radiotelevisión del Principado de As](https://ted.europa.eu/en/notice/-/detail/803347-2026) — ted, 1 engagement, 2026
- [Acuerdo marco para la prestacion del servicio de oficina de seguridad para el Servicio Cantabro de S](https://ted.europa.eu/en/notice/-/detail/793260-2026) — ted, 1 engagement, 2026
- [Servicio de Fecha Secure Posture Management (DSPM) para Ferrocarriles de la Generalitat de Cataluña ](https://ted.europa.eu/en/notice/-/detail/786942-2026) — ted, 1 engagement, 2026
- [Contrato de servicio de Ciberseguridad Gestionada - OTC (SARA). Expte. 51/26-C.](https://ted.europa.eu/en/notice/-/detail/763467-2026) — ted, 1 engagement, 2026
- [Servicio de Plataforma de Ciberseguridad y Centro de Operaciones de Ciberseguridad (Hardware/Softwar](https://ted.europa.eu/en/notice/-/detail/744958-2026) — ted, 1 engagement, 2026
- [Contratación del suministro de licencias para la plataforma de detección y respuesta ante amenazas d](https://ted.europa.eu/en/notice/-/detail/695519-2026) — ted, 1 engagement, 2026
- [3026008621 / Aquisição de Firewall de Perímetro Externo MN e Renovação Subscrição Licenciamento Chec](https://ted.europa.eu/en/notice/-/detail/684427-2026) — ted, 1 engagement, 2026

## 2. Permission gating for AI agent tool calls

> Users of AI coding agents need per-tool permission rules, read-only modes and defences so prompt-injected content cannot trigger unsafe tool calls.

Gap score **0.617** · stability 0.65 · segments: ai-agent-security, open-discovery · keywords: agent, prompt, injection, agents, tool, ai

- **Demand**: 27 need statements (25 developer, 2 practitioner), total engagement 142, 93% from the last 2 years.
**Opportunity:** Crowded and consolidating (SentinelOne-Prompt, well-funded Pillar, Lasso, Runlayer) with free native and cloud controls. Narrow opening: cheap cross-agent policy enforcement for small and mid-size dev teams, including headless/CI agent runs, below enterprise annual commits.

- **Open-source supply** (GitHub repositories for `agent tool permissions`): 1202 repos, leader 5224★, 9 of the top 10 pushed in the last year. Leading projects: [ai-boost/awesome-harness-engineering](https://github.com/ai-boost/awesome-harness-engineering) 5224★, [withcoral/coral](https://github.com/withcoral/coral) 5027★, [aipotheosis-labs/aci](https://github.com/aipotheosis-labs/aci) 4940★.
- **Threat relevance** 3/3: Directly blocks prompt-injection-driven unsafe tool calls and exfiltration, an actively exploited agent attack path. ATT&CK: [T1698 Indirect Prompt Injection](https://attack.mitre.org/techniques/T1698), [T1699 Direct Prompt Injection](https://attack.mitre.org/techniques/T1699), [T1700 AI-Enabled Exfiltration](https://attack.mitre.org/techniques/T1700). NVD CVEs matching the query: 13.

**Paid market** — crowdedness 3/3, willingness to pay 2/3, bundling risk high. ⚠ 1 claim(s) here not fully supported by their source (see fact-check).

| Vendor | Offering | Pricing | Sells to |
|---|---|---|---|
| [Knostic Kirin](https://www.knostic.ai/coding-assistants-agents-mcp) | In-agent policy checks on every coding-agent tool call, MCP validation across Cursor, Claude Code, Copilot | [Free for 1-5 users; Team $15/user/month; Enterprise via sales](https://www.knostic.ai/pricing) | developers / SMB / mid-market |
| [Pillar Security (Pillar for AI Coding Agents)](https://www.pillar.security/blog/introducing-pillar-for-ai-coding-agents) | Discovers local coding agents, scans permissions/MCP configs, runtime detection of prompt injection and tool abuse | [AWS Marketplace: Pillar Security Platform $175,000/12 months](https://aws.amazon.com/marketplace/pp/prodview-xphnsjsox7vjw) | enterprise |
| [Lasso Security](https://www.lasso.security/use-cases/ai-coding-assistants) | Inspects coding-agent and MCP tool calls and scans tool outputs before the agent acts | [code-assistant price not public; AWS Marketplace annual commits $20,000 (GenAI Chatbots) and $50,000 (LLM gateway) per 12 months](https://aws.amazon.com/marketplace/pp/prodview-7ygm7pa3k5agg) | enterprise / mid-market |
| [Prompt Security (SentinelOne)](https://www.sentinelone.com/press/sentinelone-to-acquire-prompt-security-to-advance-genai-security/) | MCP gateway with allow/block/redact per call; covers AI code assistants like Cursor | [not public](https://www.sentinelone.com/press/sentinelone-to-acquire-prompt-security-to-advance-genai-security/) | enterprise |
| [Runlayer](https://www.securityweek.com/runlayer-raises-30-million-in-series-a-funding/) | MCP control layer watching every agent action, blocking suspicious calls, audit logs | [not public](https://techcrunch.com/2025/11/17/mcp-ai-agent-security-startup-runlayer-launches-with-8-unicorns-11m-from-khoslas-keith-rabois-and-felicis) | enterprise |
| [Invariant Labs Guardrails](https://invariantlabs.ai/blog/guardrails) | MCP/LLM proxy gateway enforcing deterministic contextual rules and tool-call restrictions | [not public](https://invariantlabs.ai/blog/guardrails) | developers / enterprise |
| [Amazon Bedrock AgentCore Policy](https://aws.amazon.com/bedrock/agentcore/pricing/) | Cedar policies check every agent tool call through AgentCore Gateway, allow or deny | [usage-based, per authorization request (rate not captured) plus per-token natural-language authoring](https://aws.amazon.com/about-aws/whats-new/2026/03/policy-amazon-bedrock-agentcore-generally-available) | developers / enterprise on AWS |
| [Docker MCP Gateway](https://docs.docker.com/ai/mcp-catalog-and-toolkit/mcp-gateway/) | Open-source MCP proxy running servers in restricted containers with access control and call tracing | [gateway open source; Docker AI Governance version invite-only, price not public](https://docs.docker.com/ai/mcp-catalog-and-toolkit/mcp-gateway/) | developers / enterprise |

- **Willingness to pay**: Public prices exist: Pillar platform $175,000/12 months and Lasso for GenAI Chatbots $20,000 annual commit (12 months) on AWS Marketplace, Knostic Kirin $15/user/month. [source 1](https://aws.amazon.com/marketplace/pp/prodview-xphnsjsox7vjw) [source 2](https://aws.amazon.com/marketplace/pp/prodview-7ygm7pa3k5agg) [source 3](https://www.knostic.ai/pricing)
- **Bundling risk (high)**: Agent vendors ship free permission rules and managed deny settings (Claude Code), AWS meters Cedar tool-call policy in AgentCore, and Microsoft and Docker give away open-source MCP policy gateways.
- **Users complaining about price or vendors**: 30% of statements: [feat: Tool Permission Gating System (per-tool rules + mode-b](https://github.com/NousResearch/hermes-agent/issues/21849), [CLI Schema - enforcing a security policy for AI agents](https://github.com/cli/cli/issues/12912), [[Bug]: Provider content-blocks (prompt injection / secret de](https://github.com/OpenHands/OpenHands/issues/19018).
- **Where paying customers are underserved**:
  - Enterprise platforms sell via large annual commits (Pillar $175k, Lasso $20k+); small teams have few paid options besides Knostic. ([evidence](https://aws.amazon.com/marketplace/pp/prodview-xphnsjsox7vjw))
  - Native agent permission rules are pattern-based; argument rules are bypassable by compound commands, pushing users to sandboxing. ([evidence](https://code.claude.com/docs/en/permissions.md))
  - Headless/non-interactive agent runs often auto-approve all tool calls, with no read-only or plan mode. ([evidence](https://github.com/google-antigravity/antigravity-cli/issues/45))
  - Per-call policy engines do not yet correlate sequences of individually allowed calls into malicious workflows. ([evidence](https://developer.microsoft.com/blog/securing-mcp-a-control-plane-for-agent-tool-execution/))

**Evidence** (27 need statements; top 8):

- [Curated memory roots (`MEMORY.md` / `USER.md`) are silently and permanently excluded from bootstrap ](https://github.com/openclaw/openclaw/issues/153426) — github, 21 engagement, 2026
- [Background task notifications trigger autonomous API calls — model responds as if it were the user](https://github.com/anthropics/claude-code/issues/39027) — github, 20 engagement, 2026
- [Proposal: Untrusted Annotation for Tool Responses](https://github.com/webmachinelearning/webmcp/issues/136) — github, 16 engagement, 2026
- [Feature request: read-only / plan-mode equivalent for non-interactive `-p` runs](https://github.com/google-antigravity/antigravity-cli/issues/45) — github, 14 engagement, 2026
- [[RFC] Architecture for Robust Agents: Implementing a "Discriminator Layer" Middleware](https://github.com/openclaw/openclaw/issues/9030) — github, 13 engagement, 2026
- [Detect remote administration tool (rat)](https://security.stackexchange.com/questions/165003/detect-remote-administration-tool-rat) — stackexchange, 9 engagement, 2017
- [Which tool to use to automate REST API pentest](https://security.stackexchange.com/questions/277069/which-tool-to-use-to-automate-rest-api-pentest) — stackexchange, 8 engagement, 2024
- [feat: Tool Permission Gating System (per-tool rules + mode-based fallback)](https://github.com/NousResearch/hermes-agent/issues/21849) — github, 7 engagement, 2026

## 3. Authorization and auditing for MCP tool access

> Teams adopting MCP servers struggle to scope tool permissions, give agents their own credentials, keep secrets out of tool inputs and audit tool calls.

Gap score **0.599** · stability 0.55 · segments: ai-agent-security, appsec-supply-chain, open-discovery, smb-security-ops · keywords: mcp, servers, mcp servers, mcp server, server, tool

- **Demand**: 33 need statements (32 developer, 1 practitioner), total engagement 173, 97% from the last 2 years.
**Opportunity:** Crowded and fast-bundling: funded gateways (Runlayer, MintMCP), identity incumbents (Auth0, Descope) and clouds (AWS, Cloudflare, Microsoft) all cover it. Only a narrow wedge remains, e.g. self-serve per-agent credentials and audit for mid-market teams across clouds.

- **Open-source supply** (GitHub repositories for `mcp server authorization`): 447 repos, leader 17675★, 7 of the top 10 pushed in the last year. Leading projects: [ory/hydra](https://github.com/ory/hydra) 17675★, [golf-mcp/golf](https://github.com/golf-mcp/golf) 842★, [NapthaAI/http-oauth-mcp-server](https://github.com/NapthaAI/http-oauth-mcp-server) 110★.
- **Threat relevance** 2/3: Scoped agent credentials and tool-call audit limit token theft and misuse; MCP abuse still emerging, not yet common. ATT&CK: [T1528 Steal Application Access Token](https://attack.mitre.org/techniques/T1528), [T1550.001 Application Access Token](https://attack.mitre.org/techniques/T1550/001), [T1078 Valid Accounts](https://attack.mitre.org/techniques/T1078). NVD CVEs matching the query: 68.

**Paid market** — crowdedness 3/3, willingness to pay 2/3, bundling risk high. ⚠ 1 claim(s) here not fully supported by their source (see fact-check).

| Vendor | Offering | Pricing | Sells to |
|---|---|---|---|
| [Runlayer](https://www.runlayer.com/) | MCP gateway, shadow-AI discovery, agent identity, session traces and governance for enterprises | [not public (custom quote, no self-serve)](https://www.truefoundry.com/blog/runlayer-pricing) | enterprise |
| [MintMCP (Mintive)](https://www.mintmcp.com/) | MCP gateway with OAuth/SSO, team permissions, audit trail of every MCP interaction, SIEM export | [not public (per-user quote plus usage-based platform fee)](https://www.mintmcp.com/pricing) | enterprise, mid-market |
| [Permit MCP Gateway (Permit.io)](https://docs.permit.io/permit-mcp-gateway/overview) | Proxy authorizing each MCP tool call per agent and person, consent, trust levels, decision logs | [Permit Community tier free (14-day log retention); paid tier prices not public](https://www.permit.io/pricing) | developers, mid-market, enterprise |
| [Descope Agentic Identity Hub](https://www.descope.com/) | OAuth for MCP servers, agent consent and token vault (outbound app tokens) | [Free (2,000 consents/tokens); Pro from $249/mo; Growth from $799/mo; $0.05 per extra consent/token](https://www.descope.com/pricing) | developers, SMB to mid-market |
| [Auth0 for AI Agents](https://auth0.com/pricing) | Auth for MCP, Token Vault for agent credentials, human confirmation of agent actions | [Free plan includes Auth for MCP and Token Vault (limit 2); paid-tier add-on price not public](https://auth0.com/pricing) | developers, SMB to enterprise |
| [TrueFoundry MCP Gateway](https://www.truefoundry.com/) | AI and MCP gateway with RBAC, tool approvals, virtual MCPs and audit logs | [Free tier; Pro $25 per user/month incl. 20K requests, $20 per extra 100K](https://www.truefoundry.com/pricing) | developers, mid-market |
| [Docker MCP Enterprise Gateway](https://docs.docker.com/ai/mcp-gateway/) | Adds SSO, per-tool group policy and SIEM audit events to the free MIT gateway | [not public (priced on request)](https://geekflare.com/open-source/docker-mcp-gateway/) | enterprise |
| [Cloudflare MCP server portals](https://developers.cloudflare.com/cloudflare-one/access-controls/ai-controls/mcp-portals/) | Single Access-protected endpoint for approved MCP servers, per-portal tool curation, Logpush to SIEM | [included for all Cloudflare customers; no separate price published](https://developers.cloudflare.com/changelog/post/2026-09-24-mcp-portals-ga/) | SMB to enterprise |

- **Willingness to pay**: Public paid tiers (TrueFoundry $25/user/mo, Descope $249-$799/mo) and Runlayer raising a $30M Series A (total funding $42M) for enterprise MCP governance show buyers pay; post-purchase complaints not found. [source 1](https://www.truefoundry.com/pricing) [source 2](https://www.descope.com/pricing) [source 3](https://www.securityweek.com/runlayer-raises-30-million-in-series-a-funding/)
- **Bundling risk (high)**: AWS AgentCore includes Identity at no extra charge via Gateway (Policy billed per authorization), Cloudflare MCP portals are available to all customers, and Docker's gateway is free MIT.
- **Users complaining about price or vendors**: 24% of statements: [Feature Request: Add wildcard support for MCP tool permissio](https://github.com/anthropics/claude-code/issues/6010), [[DOCS] governance and security guidance for MCP server adopt](https://github.com/anthropics/claude-code/issues/60246), [[RFC] Hardening MCP Tool Trust Boundaries (Sanitization, Out](https://github.com/langchain-ai/langchain/issues/40473).
- **Where paying customers are underserved**:
  - Leading MCP governance vendors (Runlayer, MintMCP) publish no prices and offer no self-serve; small teams cannot evaluate or buy ([evidence](https://www.truefoundry.com/blog/runlayer-pricing))
  - Free Docker MCP Gateway has one shared token; per-user access, per-tool policy and audit require a separate enterprise contract ([evidence](https://geekflare.com/open-source/docker-mcp-gateway/))
  - Azure APIM v2 tiers lack tool-level MCP control; dynamic tool lists cannot be governed by Agent 365 ([evidence](https://learn.microsoft.com/azure/api-management/agent-365))
  - External audit connectors and fine-grained authorization need Descope Growth ($799/mo); lower tiers keep audit 1 week-1 month ([evidence](https://www.descope.com/pricing))

**Evidence** (33 need statements; top 8):

- [SEP-1299: Server-Side Authorization Management with Client Session Binding](https://github.com/modelcontextprotocol/modelcontextprotocol/issues/1299) — github, 55 engagement, 2025
- [Feature Request: Add wildcard support for MCP tool permissions](https://github.com/anthropics/claude-code/issues/6010) — github, 16 engagement, 2025
- [SEP-1708: MCP Client-Brokered Filesystem Access](https://github.com/modelcontextprotocol/modelcontextprotocol/issues/1708) — github, 14 engagement, 2025
- [MCP Actions Backend Audit Logging](https://github.com/backstage/backstage/issues/32104) — github, 13 engagement, 2025
- [feat(scaffolder): passing secrets as raw input to the execute-template MCP tool is a security anti-p](https://github.com/backstage/backstage/issues/34728) — github, 10 engagement, 2026
- [[FEATURE] PreApiCall / PostApiCall hooks to prevent secret exfiltration to API providers and attacke](https://github.com/anthropics/claude-code/issues/39882) — github, 8 engagement, 2026
- [[Feature]: propagate per-run metadata from POST /v1/runs to MCP tools/call requests](https://github.com/NousResearch/hermes-agent/issues/64890) — github, 7 engagement, 2026
- [[feat] Per-agent MCP credentials: let each custom agent call an MCP server under its own identity](https://github.com/bytedance/deer-flow/issues/8125) — github, 7 engagement, 2026

## 4. Affordable security programs for small businesses

> Small businesses and nonprofits without IT staff struggle to run security audits, assessments, awareness training and SOC 2 or Cyber Essentials.

Gap score **0.596** · stability 0.8 · segments: identity-access, open-discovery · keywords: small, business, ask, hn security, small business, ask hn

- **Demand**: 16 need statements (1 developer, 15 practitioner), total engagement 199, 12% from the last 2 years.
**Opportunity:** Crowded, well-funded compliance-automation and training markets serve funded startups; the opening is a cheap, done-for-you program for sub-20-person firms and nonprofits without IT, likely sold through MSPs or bundled with certification.

- **Open-source supply** (GitHub repositories for `small business security compliance`): 41 repos, leader 83★, 3 of the top 10 pushed in the last year. Leading projects: [Rastaman4e/-1](https://github.com/Rastaman4e/-1) 83★, [NestieGuilas/Marketing-Platform-](https://github.com/NestieGuilas/Marketing-Platform-) 26★, [Tradewindfinance2/What-Lessons-has-COVID-19-Taught-Buyers-and-Suppliers](https://github.com/Tradewindfinance2/What-Lessons-has-COVID-19-Taught-Buyers-and-Suppliers) 5★.
- **Threat relevance** 1/3: Broad small-business audits and training; general hygiene with no specific technique link among candidates. NVD CVEs matching the query: 0.

**Paid market** — crowdedness 3/3, willingness to pay 2/3, bundling risk medium. ⚠ 2 claim(s) here not fully supported by their source (see fact-check).

| Vendor | Offering | Pricing | Sells to |
|---|---|---|---|
| [Vanta](https://www.vanta.com/) | Compliance automation for SOC 2, ISO 27001 and other frameworks | [no rate card on site; AWS Marketplace 12-month: Essentials from $14,000, Plus $21,500, Professional $23,000 (1-20 employees); audit extra](https://aws.amazon.com/marketplace/pp/prodview-5ophamrbfxt44) | startups to enterprise |
| [Drata](https://drata.com/) | Compliance automation platform for SOC 2, ISO 27001 with trust center | [quote on site; AWS Marketplace Foundation Package list price $15,000 for 1-50 FTE companies](https://aws.amazon.com/marketplace/pp/prodview-3xw4sjqv2pb22) | startups, mid-market |
| [Secureframe](https://secureframe.com/) | Compliance automation for SOC 2, ISO 27001, HIPAA and more | [Fundamentals starting at $7,500/year; higher tiers quote](https://secureframe.com/pricing) | startups, SMB, mid-market |
| [Sprinto](https://sprinto.com/) | GRC automation for SOC 2/ISO 27001 for cloud-native teams | [AWS Marketplace: Starter (SOC 2 or ISO 27001, up to 25 employees) $8,500; audit separate](https://aws.amazon.com/marketplace/pp/prodview-upzeowcpyofas) | startups, SMB |
| [Comp AI](https://trycomp.ai/) | AI compliance automation for SOC 2, ISO 27001, HIPAA, GDPR | [not public (quote by frameworks scoped)](https://trycomp.ai/pricing) | startups, SMB |
| [KnowBe4 Security Awareness Training](https://www.knowbe4.com/) | Security awareness training and simulated phishing | [per seat, 3-year term: SAT Foundation $2.40/seat/month at 25-50 seats (May 2026 MSRP); nonprofit discounts on request](https://knowbe4.com/pricing-security-awareness-training) | SMB to enterprise |
| [Huntress Managed Security Awareness Training](https://www.huntress.com/) | Managed awareness training and phishing simulation, largely sold via MSPs | [per active learner per month, billed annually; price not public](https://www.huntress.com/pricing/sat) | SMB via MSPs |
| [CyberSmart](https://cybersmart.co.uk/) | Cyber Essentials certification platform with device monitoring for UK small businesses | [quote; includes IASME certification fee (IASME fee from £320+VAT)](https://cybersmart.co.uk/plans) | SMB, micro businesses (UK) |

- **Willingness to pay**: Buyers pay public list prices: SOC 2/ISO platforms $4,500-$8,500 per 12 months on AWS Marketplace, Cyber Essentials from £320+VAT, awareness training $2.40/seat/month at 25-50 seats (3-year term). [source 1](https://aws.amazon.com/marketplace/pp/prodview-upzeowcpyofas) [source 2](https://www.ncsc.gov.uk/information/cyber-essentials) [source 3](https://knowbe4.com/pricing-security-awareness-training)
- **Bundling risk (medium)**: Clouds don't bundle SOC 2 automation, but governments give free prep (NCSC action plan, CISA scanning) and Microsoft bundles training in higher tiers.
- **Users complaining about price or vendors**: 44% of statements: [Ask HN: Security at my company is horrible, what can I do?](https://news.ycombinator.com/item?id=17840003), [Ask HN: Security audits. Worth it? Who's good?](https://news.ycombinator.com/item?id=23918219), [Phone Privacy for Small Business](https://security.stackexchange.com/questions/44863/phone-privacy-for-small-business).
- **Where paying customers are underserved**:
  - SOC 2 platforms start around $8.5k-$15k/year before a $10k-$50k audit; unaffordable for sub-10-person firms handling low-risk data ([evidence](https://aws.amazon.com/marketplace/pp/prodview-5ophamrbfxt44))
  - No-IT micro businesses and nonprofits lack a guided, done-for-you program; platforms assume an engineer to integrate and remediate ([evidence](https://security.stackexchange.com/questions/194368/soc-2-audit-for-small-business-6-employees-with-no-it-department))
  - Awareness training priced from 25-seat bands and 3-year terms; Microsoft phishing simulation locked to E5/Defender Plan 2 ([evidence](https://learn.microsoft.com/en-us/defender-office-365/attack-simulation-training-get-started))
  - SaaS vendors gate SSO behind enterprise tiers, inflating small-company security costs 3x-10x ([evidence](https://sso.tax/))

**Evidence** (16 need statements; top 8):

- [IT Audit checklist](https://serverfault.com/questions/142737/it-audit-checklist) — serverfault, 66 engagement, 2010
- [Ask HN: Security at my company is horrible, what can I do?](https://news.ycombinator.com/item?id=17840003) — hn, 24 engagement, 2018
- [Ask HN: Security audit for startup / OSS projects](https://news.ycombinator.com/item?id=25520219) — hn, 23 engagement, 2020
- [Ask HN: Security audits. Worth it? Who's good?](https://news.ycombinator.com/item?id=23918219) — hn, 19 engagement, 2020
- [Ask HN: Security Awareness Training](https://news.ycombinator.com/item?id=30288999) — hn, 17 engagement, 2022
- [Phone Privacy for Small Business](https://security.stackexchange.com/questions/44863/phone-privacy-for-small-business) — stackexchange, 17 engagement, 2013
- [SOC 2 audit for small business (6 employees) with no IT department](https://security.stackexchange.com/questions/194368/soc-2-audit-for-small-business-6-employees-with-no-it-department) — stackexchange, 14 engagement, 2018
- [Ask HN: Security assessment for small non-profit](https://news.ycombinator.com/item?id=16255598) — hn, 13 engagement, 2018

## 5. User activity audit logging on servers

> Admins struggle to capture and review who logged in and what they did on servers, databases, domain controllers and SaaS like Office 365.

Gap score **0.59** · stability 0.76 · segments: cloud-security, identity-access, open-discovery, smb-security-ops · keywords: audit, log, logs, logging, server, database

- **Demand**: 22 need statements (1 buyer, 3 developer, 18 practitioner), total engagement 412, 18% from the last 2 years.
**Opportunity:** Crowded, mature market (Netwrix, ManageEngine, Quest, Lepide, PAM vendors) with cloud-native logs bundled. Only narrow wedge: cheap, per-server-priced unified activity review plus long M365 retention for SMBs priced out of per-user tools.

- **Open-source supply** (GitHub repositories for `audit log monitoring`): 1345 repos, leader 5918★, 7 of the top 10 pushed in the last year. Leading projects: [spatie/laravel-activitylog](https://github.com/spatie/laravel-activitylog) 5918★, [brexhq/substation](https://github.com/brexhq/substation) 410★, [CodesWhat/drydock](https://github.com/CodesWhat/drydock) 280★.
- **Threat relevance** 2/3: Login and activity auditing helps detect valid-account misuse and lateral movement, mainly after the fact. ATT&CK: [T1078.002 Domain Accounts](https://attack.mitre.org/techniques/T1078/002), [T1021 Remote Services](https://attack.mitre.org/techniques/T1021), [T1136.002 Domain Account](https://attack.mitre.org/techniques/T1136/002). NVD CVEs matching the query: 4.

**Paid market** — crowdedness 3/3, willingness to pay 2/3, bundling risk medium. ⚠ 1 claim(s) here not fully supported by their source (see fact-check).

| Vendor | Offering | Pricing | Sells to |
|---|---|---|---|
| [Netwrix Auditor](https://netwrix.com) | Audits user activity and changes across AD, Entra ID, M365, file servers, Windows Server | [Essentials self-service from $20 per enabled AD user + cloud-only Entra ID user (up to 250 identities); larger estates quote-only](https://netwrix.com/en/buy-now) | SMB to enterprise |
| [ManageEngine ADAudit Plus](https://www.manageengine.com/products/active-directory-audit/) | AD, Azure AD, file server, member server and workstation logon/change auditing | [Annual per server: 2 DCs $595 Standard / $945 Professional; Azure AD tenant from $995; 2 Windows file servers $495](https://www.manageengine.com/products/active-directory-audit/pricing-details.html) | SMB / mid-market |
| [Quest Change Auditor](https://www.quest.com/products/change-auditor-for-active-directory) | Real-time who-changed-what auditing for AD, Entra ID, Exchange, SQL Server, file systems | [not public (licensed per enabled user account via resellers)](https://www.cdw.com/product/Quest-ChangeAuditor-for-Active-Directory-license/1616572) | enterprise |
| [Lepide Auditor (Lepide Data Security Platform)](https://www.lepide.com) | Change and activity auditing for AD, file servers, Entra ID and other platforms | [not public; quoted per user, per year, per platform (Core/Plus/Advanced tiers)](https://www.lepide.com/quoterequest.html) | SMB / mid-market |
| [Syteca (formerly Ekran System)](https://ekransystem.com) | Session recording and user activity monitoring on servers and desktops | [not public; licensed per monitored endpoint plus management panel](https://ekransystem.com/de/buy/licensing-scheme) | mid-market / enterprise |
| [Teleport](https://goteleport.com) | Infrastructure access with SSH, desktop, Kubernetes session recording and structured audit logs | [Billed on monthly active users and protected resources; list price not public](https://goteleport.com/_uploads/Teleport_Pricing_Guide_Rev_June_16_2026_5f41774f5e.pdf) | developers / mid-market / enterprise |
| [StrongDM](https://strongdm.com) | Privileged access proxy for servers and databases with session recording and audit trails | [Single per-user SKU, list price not public; AWS Marketplace lists $840 per additional user](https://aws.amazon.com/marketplace/pp/prodview-57vja26o4xz66) | mid-market / enterprise |
| [AdminDroid Office 365 Reporter](https://admindroid.com) | Microsoft 365 audit reporting with retention beyond native audit log window | [Free edition plus premium Standard/Pro editions with add-on packs; prices not public](https://admindroid.com/resources/pdf/product/microsoft365-management/licensing-faq.pdf?5110_18) | SMB / mid-market |

- **Willingness to pay**: Established auditing products publish prices SMBs buy (ADAudit Plus from $595/yr, Netwrix from $20/user); Netwrix Capterra reviewers mostly cite setup, reporting and usability issues; several praise its cost. [source 1](https://www.manageengine.com/products/active-directory-audit/pricing-details.html) [source 2](https://netwrix.com/en/buy-now) [source 3](https://capterra.com/p/164872/Netwrix-Auditor/reviews/)
- **Bundling risk (medium)**: Microsoft (Purview Audit, 180 days standard) and AWS (90-day free CloudTrail event history) bundle native logs, but unified cross-system on-prem server/DB/AD review is not given away.
- **Users complaining about price or vendors**: 9% of statements: [Ask HN: Running legacy IE/ActiveX clients without local admi](https://news.ycombinator.com/item?id=47486365), [Office365 Audit Log](https://serverfault.com/questions/966752/office365-audit-log).
- **Where paying customers are underserved**:
  - Per-enabled-user licensing becomes very expensive for organizations with thousands of AD accounts ([evidence](https://capterra.com/p/164872/Netwrix-Auditor/reviews/))
  - Microsoft 365 audit history beyond 180 days needs E5 or audit add-on per user; E3/Business tenants underserved ([evidence](https://learn.microsoft.com/purview/audit-log-retention-policies))
  - Each source (DCs, Entra tenants, file servers, workstations) is priced as a separate add-on, inflating mixed-estate cost ([evidence](https://www.manageengine.com/products/active-directory-audit/pricing-details.html))
  - Free Linux session recording (tlog) is unreliable for root and loses recordings on reboot by default ([evidence](https://docs.redhat.com/en/documentation/red_hat_enterprise_linux/8/html/recording_sessions/getting-started-with-session-recording_getting-started-with-session-recording))

**Evidence** (22 need statements; top 8):

- [Terminal Server Logging](https://serverfault.com/questions/13451/terminal-server-logging) — serverfault, 114 engagement, 2009
- [SIEM system, what are the benefits?](https://security.stackexchange.com/questions/9684/siem-system-what-are-the-benefits) — stackexchange, 64 engagement, 2011
- [SSH session logging](https://serverfault.com/questions/313234/ssh-session-logging) — serverfault, 52 engagement, 2011
- [local mysql was hacked with ransomware hack. How to check if database data was downloaded?](https://serverfault.com/questions/946620/local-mysql-was-hacked-with-ransomware-hack-how-to-check-if-database-data-was-d) — serverfault, 39 engagement, 2018
- [Ask HN: Running legacy IE/ActiveX clients without local admin rights?](https://news.ycombinator.com/item?id=47486365) — hn, 34 engagement, 2026
- [Ansible enable audit logging](https://serverfault.com/questions/887548/ansible-enable-audit-logging) — serverfault, 31 engagement, 2017
- [rancid like tool for config files](https://security.stackexchange.com/questions/33763/rancid-like-tool-for-config-files) — stackexchange, 18 engagement, 2013
- [Domain controller audit log](https://serverfault.com/questions/328968/domain-controller-audit-log) — serverfault, 16 engagement, 2011

## 6. Privileged access management procurement

> Organisations tender PAM systems to control and monitor privileged accounts and passwords, including licence renewals and support.

Gap score **0.587** · stability 0.97 · segments: identity-access, open-discovery, smb-security-ops · keywords: access management, privileged, access, privileged access, pam, management pam

- **Demand**: 10 need statements (8 buyer, 2 practitioner), total engagement 10, 40% from the last 2 years.
**Opportunity:** Crowded, consolidating market with strong spend. Only a narrow opening: transparent, quickly deployable PAM for small public-sector and mid-size buyers in tenders, or sovereign self-hosted EU offerings; competing against PAM360, Devolutions and JumpServer.

- **Open-source supply** (GitHub repositories for `privileged access management`): 298 repos, leader 36556★, 6 of the top 10 pushed in the last year. Leading projects: [hashicorp/vault](https://github.com/hashicorp/vault) 36556★, [jumpserver/jumpserver](https://github.com/jumpserver/jumpserver) 32011★, [Cloud-Architekt/AzurePrivilegedIAM](https://github.com/Cloud-Architekt/AzurePrivilegedIAM) 222★.
- **Threat relevance** 2/3: PAM controls privileged credentials and session monitoring, reducing valid-account abuse; procurement-oriented need. ATT&CK: [T1078 Valid Accounts](https://attack.mitre.org/techniques/T1078), [T1078.003 Local Accounts](https://attack.mitre.org/techniques/T1078/003), [T1098 Account Manipulation](https://attack.mitre.org/techniques/T1098). NVD CVEs matching the query: 954.

**Paid market** — crowdedness 3/3, willingness to pay 3/3, bundling risk medium. ⚠ 5 claim(s) here not fully supported by their source (see fact-check).

| Vendor | Offering | Pricing | Sells to |
|---|---|---|---|
| [CyberArk Privileged Access Manager (Palo Alto Networks)](https://www.cyberark.com) | Enterprise vaulting, rotation, session isolation and recording for privileged accounts | [not public (no list price on vendor site; a user reports ~EUR100K for 1,000 SaaS licences)](https://www.peerspot.com/questions/what-is-your-experience-regarding-pricing-and-costs-for-cyberark-privileged-access-manager) | enterprise |
| [Delinea Secret Server](https://delinea.com) | Enterprise-grade privileged vault with discovery, password rotation and session monitoring | [not public (contact sales / demo request)](https://delinea.com/products/secret-server) | enterprise |
| [ManageEngine PAM360 Cloud](https://www.manageengine.com/privileged-access-management/) | Cloud PAM: password vault, session management, privileged user auditing | [Per privileged user slabs: 10 users $1,800/yr, 100 users $17,970/yr; services extra](https://www.manageengine.com/privileged-access-management/cloud-pricing.html) | SMB / mid-market |
| [KeeperPAM](https://www.keepersecurity.com) | Cloud PAM on Keeper vault: session management, JIT elevation, vendor access | [not public (custom pricing via sales); PAM features are add-ons](https://www.keepersecurity.com/pricing/business-and-enterprise.html) | SMB / mid-market / enterprise |
| [Devolutions PAM](https://devolutions.net) | Account discovery, rotation, checkout approvals, JIT elevation, session recording | [$650 per user per year list for PAM package (store showed $325 offer); billed annually](https://store.devolutions.net/) | SMB / mid-market |
| [JumpServer Enterprise](https://www.jumpserver.com) | Self-hosted open-source bastion/PAM with commercial enterprise tiers | [Community free up to 5,000 assets; Enterprise tiers by asset count, price not public](https://www.jumpserver.com/pricing) | SMB / mid-market |
| [Teleport](https://goteleport.com) | Infrastructure access with JIT, session recording and audit for SSH, Kubernetes, databases | [Billed on monthly active users and protected resources; list price not public](https://goteleport.com/_uploads/Teleport_Pricing_Guide_Rev_June_16_2026_5f41774f5e.pdf) | developers / mid-market / enterprise |
| [Microsoft Entra ID P2 (PIM)](https://www.microsoft.com/en-us/security/business/microsoft-entra-pricing) | Just-in-time privileged role activation for Entra/Azure roles | [$10.00 per user/month paid yearly; select PIM in P2, full PIM in ID Governance](https://www.microsoft.com/en-us/security/business/microsoft-entra-pricing) | SMB / mid-market / enterprise |

- **Willingness to pay**: Devolutions lists packages at $48-650/user/year; CyberArk users call it very expensive yet keep paying; Palo Alto bought CyberArk for $2.3B cash plus 112M shares. [source 1](https://store.devolutions.net/) [source 2](https://www.peerspot.com/questions/what-is-your-experience-regarding-pricing-and-costs-for-cyberark-privileged-access-manager) [source 3](https://www.sec.gov/Archives/edgar/data/1327567/000132756726000005/panw-20260131.htm)
- **Bundling risk (medium)**: Entra ID P2 includes select PIM and AWS Session Manager is free on EC2, but cross-platform vaulting, rotation and session recording for on-prem estates remain paid.
- **Users complaining about price or vendors**: 10% of statements: [TR2694 - Service Provider to provide CyberArk Privileged Acc](https://ted.europa.eu/en/notice/-/detail/515870-2025).
- **Where paying customers are underserved**:
  - Small public bodies (~100 users) run full PAM tenders; leaders are quote-only with heavy implementation costs ([evidence](https://ted.europa.eu/en/notice/-/detail/707070-2024))
  - Opaque, quote-only pricing from leaders (CyberArk, KeeperPAM, Delinea) complicates budgeting and tender comparison ([evidence](https://www.keepersecurity.com/pricing/business-and-enterprise.html))
  - CyberArk renewals seen as expensive versus competitors, with hard budget justification; Palo Alto ownership adds packaging uncertainty ([evidence](https://www.peerspot.com/questions/what-is-your-experience-regarding-pricing-and-costs-for-cyberark-privileged-access-manager))
  - Session management, JIT and vendor access sold as add-ons above business tiers, raising SMB cost ([evidence](https://www.keepersecurity.com/pricing/business-and-enterprise.html))

**Evidence** (10 need statements; top 8):

- [Best Open-Source SIEM for Monitoring 100-150 Assets?](https://serverfault.com/questions/1171594/best-open-source-siem-for-monitoring-100-150-assets) — serverfault, 2 engagement, 2025
- [RFT for Renewal of Secure Email Gateway Environment](https://ted.europa.eu/en/notice/-/detail/735396-2026) — ted, 1 engagement, 2026
- [Multi-Component Security Monitoring System](https://ted.europa.eu/en/notice/-/detail/713005-2026) — ted, 1 engagement, 2026
- [TR2694 - Service Provider to provide CyberArk Privileged Access Management (PAM) licence re-seller L](https://ted.europa.eu/en/notice/-/detail/515870-2025) — ted, 1 engagement, 2025
- [Administration of Privileged Accesses (PAM)](https://ted.europa.eu/en/notice/-/detail/707070-2024) — ted, 1 engagement, 2024
- [Qualification phase: Privileged Access Management (PAM) Hemit HF](https://ted.europa.eu/en/notice/-/detail/419780-2024) — ted, 1 engagement, 2024
- [Privilege Access Management Software Solution](https://ted.europa.eu/en/notice/-/detail/385250-2024) — ted, 1 engagement, 2024
- [Prequalification - Privileged Access Management System (PAM)](https://ted.europa.eu/en/notice/-/detail/363169-2024) — ted, 1 engagement, 2024

## 7. Third-party dependency vulnerability management

> Developers struggle to track, scan and update vulnerable third-party dependencies in apps, containers and CI pipelines.

Gap score **0.581** · stability 0.85 · segments: appsec-supply-chain, open-discovery · keywords: vulnerability, security vulnerability, dependency, js, dependencies, vulnerabilities

- **Demand**: 12 need statements (1 buyer, 7 developer, 4 practitioner), total engagement 746, 50% from the last 2 years.
**Opportunity:** Crowded and heavily bundled; no opening for another scanner or hardened-image catalog (Minimus shut down amid free competition). Only narrow wedges remain: transitive-fix automation and source-less CI scanning for teams already paying incumbents.

- **Open-source supply** (GitHub repositories for `dependency vulnerability scanning`): 625 repos, leader 1532★, 8 of the top 10 pushed in the last year. Leading projects: [fossas/fossa-cli](https://github.com/fossas/fossa-cli) 1532★, [lunasec-io/lunasec](https://github.com/lunasec-io/lunasec) 1472★, [owasp-dep-scan/dep-scan](https://github.com/owasp-dep-scan/dep-scan) 1464★.
- **Threat relevance** 3/3: Tracking and patching vulnerable dependencies directly addresses compromised and exploited third-party components. ATT&CK: [T1195.001 Compromise Software Dependencies and Development Tools](https://attack.mitre.org/techniques/T1195/001), [T1588.006 Vulnerabilities](https://attack.mitre.org/techniques/T1588/006), [T1588.005 Exploits](https://attack.mitre.org/techniques/T1588/005). NVD CVEs matching the query: 1.

**Paid market** — crowdedness 3/3, willingness to pay 2/3, bundling risk high. ⚠ 1 claim(s) here not fully supported by their source (see fact-check).

| Vendor | Offering | Pricing | Sells to |
|---|---|---|---|
| [Snyk Open Source / Snyk Container](https://snyk.io/plans/) | Developer-first SCA and container scanning with fix PRs across repos and CI | [Free (Open Source 200 tests, Container 100 tests/month); Team from $25/month per contributing developer; Enterprise custom](https://snyk.io/plans/) | developers, SMB to enterprise |
| [GitHub Code Security (Dependabot)](https://github.blog/changelog/2025-04-01-github-advanced-security-is-here-for-github-team-organizations) | Dependabot alerts/updates plus premium dependency review bundled into GitHub | [Code Security $30/active committer/month; basic Dependabot included with GitHub](https://github.blog/changelog/2025-04-01-github-advanced-security-is-here-for-github-team-organizations) | GitHub-native teams, SMB to enterprise |
| [Sonatype Lifecycle / Repository Firewall](https://www.sonatype.com/product-pricing) | Dependency policy governance plus malicious/vulnerable package blocking at the repository proxy | [Firewall Cloud Pro from $4,800/year; Lifecycle cloud Pro from $1,200/year (credits); Enterprise custom](https://www.sonatype.com/product-pricing) | mid-market and enterprise, public sector |
| [JFrog Advanced Security (Xray)](https://jfrog.com/pricing/) | SCA, contextual and transitive analysis built into the Artifactory artifact registry | [not public; Advanced Security listed only on upper Enterprise tiers (Enterprise starts at $950/month)](https://jfrog.com/pricing/) | enterprise |
| [Docker Scout](https://www.docker.com/pricing/) | Container image vulnerability analysis, policy and remediation tied to Docker Hub | [Included in Docker plans: Personal $0 (1 repo), Pro $9-11/user/month (2 repos), Team $15-16/user/month (unlimited)](https://www.docker.com/pricing/) | developers, SMB |
| [Socket](https://socket.dev/pricing) | Dependency supply-chain security: malicious package detection and vulnerable dependency alerts | [Free tier; Team about $25/dev/month, 5-dev minimum (third-party reports)](https://toolradar.com/tools/socket-dev/pricing) | developers, SMB to enterprise |
| [Endor Labs](https://www.endorlabs.com/pricing) | SCA with function-level reachability and upgrade impact analysis to cut noise | [not public (per contributing developer, quote)](https://learn.microsoft.com/en-us/azure/defender-for-cloud/faq-endor-labs) | enterprise |
| [Chainguard (Containers, Libraries)](https://www.chainguard.dev/pricing) | Minimal low-CVE container images and rebuilt libraries replacing vulnerable upstream dependencies | [Free Starter (5 users, 5 images); Team paid by credit card, price not shown; Enterprise quote](https://www.chainguard.dev/pricing) | developers to enterprise |

- **Willingness to pay**: Buyers pay: Snyk Team from $25/dev/month, Sonatype Firewall from $4,800/year, and public tenders procure Sonatype Lifecycle and Firewall. [source 1](https://snyk.io/plans/) [source 2](https://www.sonatype.com/product-pricing) [source 3](https://ted.europa.eu/en/notice/-/detail/411742-2026)
- **Bundling risk (high)**: GitHub includes Dependabot, Docker includes Scout, AWS Inspector scans ECR and CI images per use, and Docker and Red Hat give hardened images away free.
- **Users complaining about price or vendors**: 25% of statements: [Ask HN: Which security vulnerability feeds should I Monitor?](https://news.ycombinator.com/item?id=12387694), [RFT for Sonatype Nexus Repository Manager, Lifecycle and Fir](https://ted.europa.eu/en/notice/-/detail/411742-2026), [Self-hosted Kali and BlackArch apt mirrors for supply chain ](https://github.com/Strike48-public/pick/issues/135).
- **Where paying customers are underserved**:
  - Update bots do not bump top-level packages to fix vulnerable transitive sub-dependencies ([evidence](https://github.com/renovatebot/renovate/issues/3080))
  - Low-tier repository firewall covers only npm, Maven, PyPI, NuGet; vulnerability and license blocking are Enterprise-only ([evidence](https://www.sonatype.com/product-pricing))
  - Teams want CI dependency scanning and SBOMs without granting vendors source-code access ([evidence](https://news.ycombinator.com/item?id=48944189))
  - Per-developer pricing causes sticker shock as teams grow to 30-50 developers ([evidence](https://dev.to/rahulxsingh/8-best-snyk-alternatives-for-developer-security-in-2026-326k))

**Evidence** (12 need statements; top 8):

- [How to handle security updates within Docker containers?](https://serverfault.com/questions/611082/how-to-handle-security-updates-within-docker-containers) — serverfault, 630 engagement, 2014
- [Update dependencies to resolve security vulnerabilities in sub-dependencies](https://github.com/renovatebot/renovate/issues/3080) — github, 48 engagement, 2019
- [Ask HN: Which security vulnerability feeds should I Monitor?](https://news.ycombinator.com/item?id=12387694) — hn, 21 engagement, 2016
- [Add a config option to disable proxying for all private packages (to shield against dependency confu](https://github.com/verdaccio/verdaccio/issues/2103) — github, 18 engagement, 2021
- [💬 RFC: Proposal to Remove `node-libs-browser` Dependency](https://github.com/backstage/backstage/issues/28740) — github, 15 engagement, 2025
- [web app 3rd party JS dependency vulnerability management](https://security.stackexchange.com/questions/245529/web-app-3rd-party-js-dependency-vulnerability-management) — stackexchange, 6 engagement, 2021
- [Ask HN: Best approach to dependency vulnerability scanning in CI?](https://news.ycombinator.com/item?id=48944189) — hn, 4 engagement, 2026
- [Support for Rust](https://github.com/arm/metis/issues/21) — github, 2 engagement, 2025

## 8. Classified-approved mobile workstations for government

> German agencies need VS-NfD-approved fully integrated mobile workstations and related cryptography-based services.

Gap score **0.534** · stability 0.7 · segments: open-discovery · keywords: vs, den, nur, bereitstellung, für, für den

- **Demand**: 6 need statements (6 buyer), total engagement 6, 100% from the last 2 years.
**Opportunity:** Real, large government spend, but a regulated oligopoly (secunet, genua/Bundesdruckerei, Rohde & Schwarz) behind multi-year BSI approvals. Only openings: integration/managed-service layer on approved components for Länder, police and classified-contract SMEs; not a new-product startup.

- **Open-source supply** (GitHub repositories for `secure mobile workstation`): 7 repos, leader 109★, 5 of the top 10 pushed in the last year. Leading projects: [swati1024/torrents](https://github.com/swati1024/torrents) 109★, [mdxedia/Awsome-Cash](https://github.com/mdxedia/Awsome-Cash) 37★, [MuhammadLutfiMuzakiiVY/flux-ai-terminal](https://github.com/MuhammadLutfiMuzakiiVY/flux-ai-terminal) 16★.
- **Threat relevance** 1/3: Certified secure workstations for classified data; procurement need with no clear candidate technique link. NVD CVEs matching the query: 0.

**Paid market** — crowdedness 3/3, willingness to pay 3/3, bundling risk low. ⚠ 1 claim(s) here not fully supported by their source (see fact-check).

| Vendor | Offering | Pricing | Sells to |
|---|---|---|---|
| [secunet SINA Workstation S](https://www.secunet.com/en/loesungen/sina-workstation-s) | BSI-approved notebook bundle (Lenovo ThinkPad) with VPN, disk encryption, parallel guest OSes | [not public (sold via government framework contracts)](https://www.bsi.bund.de/EN/Themen/Oeffentliche-Verwaltung/Zulassung/mobile_Arbeitsplaetze/mobileArbeitsplaetze.html) | enterprise (federal government, Bundeswehr, defence industry) |
| [genua VS-top](https://www.bundesdruckerei.de/en/newsroom/press-releases/genuconnect-vpn-software-client-now-bsi-approval) | BSI-approved security laptop with two separate runtime environments, VPN and disk encryption | [not public](https://www.bsi.bund.de/EN/Themen/Oeffentliche-Verwaltung/Zulassung/mobile_Arbeitsplaetze/mobileArbeitsplaetze.html) | enterprise (government, classified-contract companies) |
| [genua genusecure Suite (incl. HP Sure Station bundle)](https://platform.softwareone.com/product/genusecure/PCP-3750-7602) | Software suite making Windows notebooks VS-NfD compliant; sold pre-integrated with HP Sure Station | [not public](https://esut.de/2025/09/meldungen/63907/hochsicheres-notebook-mit-hp-sure-station-mit-genusecure/) | enterprise / mid-market (authorities, regulated companies) |
| [genua genucard](https://www.bsi.bund.de/EN/Themen/Oeffentliche-Verwaltung/Zulassung/mobile_Arbeitsplaetze/mobileArbeitsplaetze.html) | USB-attached VPN security device turning standard laptops into VS-NfD workstations | [not public](https://www.bsi.bund.de/EN/Themen/Oeffentliche-Verwaltung/Zulassung/mobile_Arbeitsplaetze/mobileArbeitsplaetze.html) | enterprise / mid-market |
| [Rohde & Schwarz Trusted Endpoint Suite](https://rohde-schwarz.com/br/_255608.html) | BSI-approved 'secure VS workplace' software for Windows laptops and tablets | [not public](https://esut.de/2022/09/meldungen/36599/trusted-endpoint-suite-vom-bsi-fuer-vs-nfd-zugelassen/) | enterprise (public institutions, private companies) |
| [NCP Secure VPN GovNet Box](https://www.bsi.bund.de/EN/Themen/Oeffentliche-Verwaltung/Zulassung/mobile_Arbeitsplaetze/mobileArbeitsplaetze.html) | USB-attached BSI-approved VPN box for VS-NfD mobile work | [not public](https://www.bsi.bund.de/EN/Themen/Oeffentliche-Verwaltung/Zulassung/mobile_Arbeitsplaetze/mobileArbeitsplaetze.html) | enterprise / mid-market |
| [ECOS Secure Boot Stick [SX]](https://www.genua.de/fileadmin/Loesungen/Downloads/ecos-secure-boot-stick-%5Bsx%5D-flyer-en.pdf) | Bootable USB stick providing VS-NfD workstation on PCs, tablets and Macs | [not public](https://www.bsi.bund.de/EN/Themen/Oeffentliche-Verwaltung/Zulassung/mobile_Arbeitsplaetze/mobileArbeitsplaetze.html) | mid-market / SMB (government, classified-contract firms) |

- **Willingness to pay**: 2021 Bundeswehr framework for the whole SINA product family ~EUR 874M over four years; secunet public-sector revenue EUR 412M in 2025; state police tendering up to 6,000 approved clients; BSI seeks more suppliers. [source 1](https://esut.de/2021/06/meldungen/28283/rahmenvertrag-sina-verlaengert/) [source 2](https://www.secunet.com/en/about-us/press/article/secunet-security-networks-veroeffentlicht-testierten-ge-schaeftsbericht-2025-und-bestaetigt-vorlaeufige-zahlen) [source 3](https://ted.europa.eu/en/notice/-/detail/735701-2026)
- **Bundling risk (low)**: VS-NfD use requires product-specific BSI approval; no OS or cloud vendor ships an approved VPN/disk-encryption stack free, and native BitLocker has no such approval.
- **Users complaining about price or vendors**: 0% of statements.
- **Where paying customers are underserved**:
  - Buyers must assemble approved VPN, disk encryption, hardware and integrator; demand for single-source, ready-to-use bundles ([evidence](https://esut.de/2025/09/meldungen/63907/hochsicheres-notebook-mit-hp-sure-station-mit-genusecure/))
  - BSI explicitly seeks more providers for supply security; few notebook bundles, dominated by secunet and genua ([evidence](https://www.bsi.bund.de/EN/Themen/Oeffentliche-Verwaltung/Zulassung/mobile_Arbeitsplaetze/mobileArbeitsplaetze.html))
  - Approved clients listed mainly for Windows 10/8/7; little choice for Mac, Linux or modern OS fleets ([evidence](https://www.bsi.bund.de/EN/Themen/Oeffentliche-Verwaltung/Zulassung/mobile_Arbeitsplaetze/mobileArbeitsplaetze.html))
  - Regional police tender for up to 6,000 VS-NfD clients re-published repeatedly, suggesting a hard-to-fill procurement ([evidence](https://ted.europa.eu/en/notice/-/detail/735701-2026))

**Evidence** (6 need statements; top 8):

- [Kryptographiebasierte Services](https://ted.europa.eu/en/notice/-/detail/789715-2026) — ted, 1 engagement, 2026
- [Bereitstellung VS-nfD (= Verschlusssache -nur für den Dienstebrauch) zugelassener mobiler Arbeitsplä](https://ted.europa.eu/en/notice/-/detail/735701-2026) — ted, 1 engagement, 2026
- [Bereitstellung VS-nfD (= Verschlusssache -nur für den Dienstebrauch) zugelassener mobiler Arbeitsplä](https://ted.europa.eu/en/notice/-/detail/711447-2026) — ted, 1 engagement, 2026
- [Kryptographiebasierte Services](https://ted.europa.eu/en/notice/-/detail/712641-2026) — ted, 1 engagement, 2026
- [Bereitstellung VS-nfD (= Verschlusssache -nur für den Dienstebrauch) zugelassener mobiler Arbeitsplä](https://ted.europa.eu/en/notice/-/detail/701345-2026) — ted, 1 engagement, 2026
- [Bereitstellung VS-nfD (= Verschlusssache -nur für den Dienstebrauch) zugelassener mobiler Arbeitsplä](https://ted.europa.eu/en/notice/-/detail/656196-2026) — ted, 1 engagement, 2026

## 9. Product cybersecurity regulation compliance for manufacturers

> Makers of software and connected or medical devices must meet CRA, RED, PSTI and FDA duties: SBOMs, vulnerability handling, disclosure, risk assessment.

Gap score **0.52** · stability 0.47 · segments: appsec-supply-chain, open-discovery · keywords: eu, vulnerabilities, product, components, act, effective

- **Demand**: 9 need statements (9 buyer), total engagement 9, 67% from the last 2 years.
**Opportunity:** Crowded at enterprise (Cybellum, Finite State, ONEKEY, Medcrypt) and among cheap SaaS-focused CRA tools; opening is affordable multi-regulation (CRA/RED/PSTI/FDA) compliance for small hardware and firmware makers.

- **Open-source supply** (GitHub repositories for `cyber resilience act`): 178 repos, leader 394★, 10 of the top 10 pushed in the last year. Leading projects: [kulkarnirohit123/cra-agent](https://github.com/kulkarnirohit123/cra-agent) 394★, [omonien/DX.Comply](https://github.com/omonien/DX.Comply) 60★, [cra-compliance-lab/awesome-cra-compliance](https://github.com/cra-compliance-lab/awesome-cra-compliance) 58★.
- **Threat relevance** 1/3: Regulatory duties for manufacturers; vulnerability handling helps somewhat, but mostly compliance work. ATT&CK: [T1588.006 Vulnerabilities](https://attack.mitre.org/techniques/T1588/006). NVD CVEs matching the query: 0.

**Paid market** — crowdedness 3/3, willingness to pay 3/3, bundling risk medium.

| Vendor | Offering | Pricing | Sells to |
|---|---|---|---|
| [Medcrypt Security Intelligence (incl. Helm)](https://www.medcrypt.com/) | FDA premarket documentation, threat modeling, submission audit, SBOM/vulnerability management, postmarket monitoring for medical devices | [Free readiness review; MSI from $35,000 per product line/year (typical first year $50-60k with pen test); Enterprise custom](https://www.medcrypt.com/pricing) | medical device manufacturers, mid-market to enterprise |
| [ONEKEY](https://www.onekey.com/) | Firmware analysis, SBOM, CVE monitoring and Compliance Wizard checking CRA / IEC 62443-4-2 | [not public (demo/quote; 'CRA Fast Start' package)](https://www.onekey.com/press-release/onekey-launches-cra-fast-start-to-help-manufacturers-prepare-for-eu-cyber-resilience-act) | enterprise and mid-market device/machine manufacturers |
| [Finite State](https://finitestate.io/) | Binary/firmware SBOM, exploitability prioritization, VEX and audit-ready compliance evidence for connected devices | [not public (contact sales; free trial listed)](https://finitestate.io/product-security/device-manufacturers) | enterprise device manufacturers |
| [Cybellum Product Security Platform](https://cybellum.com/) | Product security assessment, SBOM, vulnerability and compliance management for CRA and FDA | [not public](https://cybellum.com/resources-files/Complying_with_CRA_Cybellum_Web.pdf) | enterprise (automotive, medical, industrial) |
| [CRA Evidence](https://craevidence.com/) | CRA readiness tracking, monitored SBOMs, VEX, HBOM, ENISA reporting workflow, technical file export | [not public (Professional and Enterprise both custom)](https://craevidence.com/pricing) | SMB to mid-market manufacturers, importers |
| [sbomify](https://sbomify.com/) | SBOM hub, trust center, OSV/Dependency-Track scanning, CRA Compliance Wizard on paid tiers | [Free Community tier; Business reported at $159/month billed annually (third-party); Enterprise custom](https://www.itechguides.com/products/sbomify/) | developers, SMB software makers |
| [ConformOps](https://www.softwareadvice.com.au/software/692219/ConformOps) | Maps repo/SBOM evidence to CRA requirements, gap identification, traceable compliance workflow | [Free version; paid from EUR 99 one-time per assessment](https://www.softwareadvice.com.au/software/692219/ConformOps) | SMB software manufacturers |
| [CRA-Ready](https://www.capterra.com/p/10045966/CRA-Ready/) | CRA evidence store, SBOM generation, vulnerability monitoring, compliance workflow for SaaS SMBs | [From $49/month flat; Compliance Pro $99/month (3 repositories)](https://www.capterra.com/p/10045966/CRA-Ready/) | SMB software companies |

- **Willingness to pay**: Regulation-forced spend: Medcrypt lists $35k per product line/year, typical first-year $50-60k; many firms still expect not to be fully CRA-compliant by the 2027 deadline. [source 1](https://www.medcrypt.com/pricing) [source 2](https://www.linuxfoundation.org/blog/the-cra-readiness-reality-what-changed-and-what-didnt-between-2025-and-2026) [source 3](https://www.enisa.europa.eu/publications/sme-cra-survey-report)
- **Bundling risk (medium)**: SBOM export is free in GitHub and Amazon Inspector and AppSec suites add CRA modules, but risk assessment, disclosure and regulator reporting workflows are not bundled.
- **Users complaining about price or vendors**: 0% of statements.
- **Where paying customers are underserved**:
  - Full FDA compliance platforms start at $35k per product line; little in between for small device makers ([evidence](https://www.medcrypt.com/pricing))
  - Cheap CRA tools target SaaS repos, not firmware/hardware makers needing binary SBOMs and RED/PSTI coverage ([evidence](https://www.capterra.com/p/10045966/CRA-Ready/))
  - FDA-focused platforms lack EU MDR/CRA coverage; multi-regulation tracking per product still in development ([evidence](https://www.medcrypt.com/pricing))
  - SMEs cite cost, time and resources as main CRA barriers and ask for financial support ([evidence](https://www.enisa.europa.eu/publications/sme-cra-survey-report))

**Evidence** (9 need statements; top 8):

- [EU Cyber Resilience Act (Regulation (EU) 2024/2847): Draw up a software bill of materials in a commo](https://eur-lex.europa.eu/eli/reg/2024/2847/oj) — regulation, 1 engagement, 2027
- [EU Cyber Resilience Act (Regulation (EU) 2024/2847): Remediate vulnerabilities without delay through](https://eur-lex.europa.eu/eli/reg/2024/2847/oj) — regulation, 1 engagement, 2027
- [EU Cyber Resilience Act (Regulation (EU) 2024/2847): Put in place and enforce a coordinated vulnerab](https://eur-lex.europa.eu/eli/reg/2024/2847/oj) — regulation, 1 engagement, 2027
- [EU Cyber Resilience Act (Regulation (EU) 2024/2847): Exercise due diligence on third-party and open-](https://eur-lex.europa.eu/eli/reg/2024/2847/oj) — regulation, 1 engagement, 2027
- [EU Cyber Resilience Act (Regulation (EU) 2024/2847): Perform and document a cybersecurity risk asses](https://eur-lex.europa.eu/eli/reg/2024/2847/oj) — regulation, 1 engagement, 2027
- [EU Radio Equipment Directive cybersecurity delegated act (Delegated Regulation (EU) 2022/30, amended](https://eur-lex.europa.eu/eli/reg_del/2022/30/oj) — regulation, 1 engagement, 2025
- [UK Product Security and Telecommunications Infrastructure (Security Requirements for Relevant Connec](https://www.legislation.gov.uk/uksi/2023/1007/made) — regulation, 1 engagement, 2024
- [US FD&C Act section 524B — Ensuring cybersecurity of devices (21 U.S.C. 360n-2): Include a software ](https://www.govinfo.gov/content/pkg/USCODE-2023-title21/html/USCODE-2023-title21-chap9-subchapV-partA-sec360n-2.htm) — regulation, 1 engagement, 2023

## 10. Cloud security posture management configuration

> Cloud teams need multi-cloud CSPM, asset inventory and policy-as-code control over Defender plans, with fewer false positives.

Gap score **0.518** · stability 0.53 · segments: appsec-supply-chain, cloud-security, open-discovery · keywords: cspm, cloud, policy, microsoft, plan, configuration

- **Demand**: 8 need statements (5 developer, 3 practitioner), total engagement 33, 12% from the last 2 years.
**Opportunity:** Crowded, well-funded market with free native baselines; no broad CSPM opening. Only a narrow wedge: policy-as-code management of native security plan settings (e.g. Defender extensions) for multi-cloud platform teams, likely a feature, not a company.

- **Open-source supply** (GitHub repositories for `cspm cloud posture`): 228 repos, leader 3788★, 6 of the top 10 pushed in the last year. Leading projects: [aquasecurity/cloudsploit](https://github.com/aquasecurity/cloudsploit) 3788★, [turbot/powerpipe](https://github.com/turbot/powerpipe) 527★, [openraven/magpie](https://github.com/openraven/magpie) 206★.
- **Threat relevance** 2/3: Posture management closes cloud misconfigurations like exposed storage and open firewalls; preventive hygiene, indirect. ATT&CK: [T1530 Data from Cloud Storage](https://attack.mitre.org/techniques/T1530), [T1078.004 Cloud Accounts](https://attack.mitre.org/techniques/T1078/004), [T1686.001 Cloud Firewall](https://attack.mitre.org/techniques/T1686/001). NVD CVEs matching the query: 0.

**Paid market** — crowdedness 3/3, willingness to pay 3/3, bundling risk high. ⚠ 1 claim(s) here not fully supported by their source (see fact-check).

| Vendor | Offering | Pricing | Sells to |
|---|---|---|---|
| [Wiz](https://www.wiz.io) | Agentless CNAPP: CSPM, attack path analysis and security graph across AWS, Azure, GCP | [Annual contract; Wiz Essential $24,000 and Wiz Advanced $38,000 per 100 cloud workloads (AWS Marketplace)](https://aws.amazon.com/marketplace/pp/prodview-ibgbkrqusncsm) | enterprise / mid-market |
| [Microsoft Defender CSPM](https://azure.microsoft.com/en-us/pricing/details/defender-for-cloud/) | Advanced posture plan: attack paths, agentless scanning, multicloud; foundational CSPM is free | [Per billable resource (VMs, storage, DBs, serverless); current list price not shown on page; Foundational CSPM free](https://azure.microsoft.com/en-us/pricing/details/defender-for-cloud/) | enterprise / mid-market (Azure-centric) |
| [Palo Alto Networks Prisma Cloud](https://www.paloaltonetworks.com/prisma/cloud) | Credit-based CNAPP; Business Edition covers CSPM, compliance, custom policies, remediation | [Annual credit packs; Business Edition $9,000 per 100 credits, Enterprise $18,000 per 100 credits](https://redresscompliance.com/palo-alto-prisma-cloud-licensing-guide.html) | enterprise |
| [Orca Security](https://orca.security) | Agentless CNAPP with CSPM, vulnerability and risk prioritization across clouds | [not public (private offers); Vendr reports median $98,701/year (104 purchases)](https://www.vendr.com/marketplace/orca-security) | enterprise / mid-market |
| [Prowler Cloud](https://prowler.com) | Managed open-source-based CSPM, 2,500+ checks across AWS, GCP, Azure, M365, GitHub | [$99 per cloud account per month, or $79 billed annually; 50,000 resources pooled](https://prowler.com/pricing) | SMB / mid-market / developers |
| [Plerion](https://plerion.com) | CNAPP with asset inventory and posture, priced on combined cloud spend | [Priced on monthly AWS/Azure/GCP spend; AWS Marketplace contracts from $15,000/year](https://plerion.com/pricing) | mid-market |
| [Turbot Guardrails](https://turbot.com/guardrails) | Policy-as-code governance with 14,000+ policies and real-time multi-cloud enforcement | [$0.05 per control (one guardrail on one resource) per month, metered daily](https://turbot.com/guardrails/pricing) | enterprise / mid-market |
| [AWS Security Hub CSPM](https://aws.amazon.com/security-hub/cspm/) | AWS-native posture checks against CIS and AWS best-practice standards | [Per security check, tiered from $0.0010 per check; free trial per account/region](https://aws.amazon.com/security-hub/cspm/pricing) | all AWS customers |

- **Willingness to pay**: Buyers sign large annual contracts (Wiz $24k-38k per 100 workloads; Orca median $98,701/yr per Vendr, 104 purchases) and still file issues about missing policy-as-code control of paid Defender plans. [source 1](https://aws.amazon.com/marketplace/pp/prodview-ibgbkrqusncsm) [source 2](https://www.vendr.com/marketplace/orca-security) [source 3](https://github.com/Azure/Microsoft-Defender-for-Cloud/issues/735)
- **Bundling risk (high)**: Azure gives Foundational CSPM free across AWS/GCP, Google's Security Command Center Standard tier is free, and AWS Security Hub CSPM is cheap per check.
- **Users complaining about price or vendors**: 38% of statements: [SPIKE Looking for a multi-cloud CSPM](https://github.com/bcgov/cloud-pathfinder/issues/2008), [[Policy] Add custom policy for Microsoft Defender CSPM plan ](https://github.com/Azure/Microsoft-Defender-for-Cloud/issues/1039), [Setting MS Defender for Cloud plans by code (policy or bicep](https://github.com/Azure/Microsoft-Defender-for-Cloud/issues/735).
- **Where paying customers are underserved**:
  - Defender CSPM plan extensions can't be fully configured through built-in policy or Bicep; only pricing tier is exposed ([evidence](https://github.com/Azure/Microsoft-Defender-for-Cloud/issues/1039))
  - Cloud-native CSPMs are per-provider, so multi-cloud teams must pick one and pipe the others' data into it ([evidence](https://github.com/bcgov/cloud-pathfinder/issues/2008))
  - Leading CNAPPs start at tens of thousands per year, too costly for small multi-cloud teams ([evidence](https://aws.amazon.com/marketplace/pp/prodview-ibgbkrqusncsm))

**Evidence** (8 need statements; top 8):

- [Configuration to exclude packages being sent to OSS Index](https://github.com/digitalcoyote/NuGetDefense/issues/35) — github, 24 engagement, 2020
- [SPIKE Looking for a multi-cloud CSPM](https://github.com/bcgov/cloud-pathfinder/issues/2008) — github, 2 engagement, 2022
- [Managing MSP Tenants for Anti-Phishing Controls](https://serverfault.com/questions/988839/managing-msp-tenants-for-anti-phishing-controls) — serverfault, 2 engagement, 2019
- [HIPAA compliant BI reporting tool?](https://security.stackexchange.com/questions/192173/hipaa-compliant-bi-reporting-tool) — stackexchange, 2 engagement, 2018
- [CSPM False Positives](https://news.ycombinator.com/item?id=35776975) — hn, 1 engagement, 2023
- [[Policy] Add custom policy for Microsoft Defender CSPM plan with full extension configurability](https://github.com/Azure/Microsoft-Defender-for-Cloud/issues/1039) — github, 1 engagement, 2026
- [Setting MS Defender for Cloud plans by code (policy or bicep template) - only pricingTier available?](https://github.com/Azure/Microsoft-Defender-for-Cloud/issues/735) — github, 1 engagement, 2023
- [SPIKE: Asset inventory solution in AWS](https://github.com/bcgov/cloud-pathfinder/issues/1837) — github, 0 engagement, 2022

## Excluded as incoherent

| Theme | Keywords | Namer's reason |
|---|---|---|
| 1 | aws, iam, aws iam, role, amazon, roles | Per-tool IAM auth feature requests plus unrelated IAM usage questions. |
| 2 | en, managed, soc, siem soc, response, av | Only about half are SOC/MDR; rest are unrelated purchases. |
| 3 | et, la, des, le, en, solution | Grouped by French language; PAM/IAM, RSSI outsourcing and audits differ. |
| 5 | github, https, github com, feature, https github, com | Unrelated requests grouped by GitHub issue boilerplate. |
| 6 | phishing, email, emails, site, server, mail | Inbound filtering, domain abuse takedown and false-positive blocking differ. |
| 7 | pro, zakázky, je, předmětem, zakázky je, na | Grouped by language; products bought are unrelated. |
| 11 | und, der, lösung, die, eine, zu | Grouped by German language; PAM, XDR, MDM and consulting differ. |
| 13 | group, scim, sync, feature, add, user | Different identity and automation requests sharing provisioning words. |
| 17 | tools, tool, linux, malware, security, workspace | Unrelated tool requests sharing the word tool. |
| 18 | dostawa wdrożenie, dostawa, oraz, wdrożenie, urządzeń, zamówienia | One tender bundling several distinct security products. |
| 20 | vulnerability, bypass, analysis, attacks, database, having | Unrelated needs sharing vulnerability words. |
| 21 | xss, stored, network, deploy, ssh, private | Unrelated questions grouped by generic security words. |
| 23 | cargo, package, packages, workflows, arm64, audit | Varied package and scanner issues without one shared need. |
| 24 | este, al, complet, la, waf, date | Grouped by language; several distinct products tendered. |
| 25 | techniky, provozních, řešení, souvisejících, technologií, dodávka | Medical device security is under half; rest unrelated. |
| 26 | output, python, file, decrypt, tool, shell | Some agent tool scoping, but mostly unrelated items. |
| 28 | zajištění, je, systému, plnění, za, předmětem | SIEM, NDR, logging and PAM are distinct products. |
| 29 | ist, der, und, die, von, zur | Grouped by German language; products differ. |
| 31 | eu, ai, art, risk, systems, jurisdiction eu | Different obligations across regulations, not one need. |
| 32 | licencji, zakup, zamówienia, dla, wraz, przedmiotem | Grouped by procurement words; products unrelated. |
| 34 | mfa, authentication mfa, 200, essentials, gbps, 100 | Grouped by language; varied products. |
| 36 | opis przedmiotu, zamówienia zawiera, zawiera, zawiera załącznik, opis, szczegółowy opis | Shared boilerplate; content of the need is not shown. |
| 37 | rozwiązania, rozbudowa, miesięcy, 36, jest, oraz | Grouped by contract wording; products differ. |
| 38 | api, scoped, authentication, key, api key, client | Different auth features across unrelated products. |
| 39 | comments, community, issue, help, request, 2016 | Unrelated requests grouped by issue-tracker words. |
| 41 | keys, service account, account, cluster, gke, json | Only two share a need; rest unrelated. |
| 42 | groups, security groups, external, traffic, idp, metrics | Unrelated features sharing group and policy words. |
| 43 | wdrożenie, projektu, wraz ze, ze, gminie, cyberbezpieczeństwo | Bundled multi-product grant projects, not one need. |
| 47 | dla, komputerowego, sprzętu komputerowego, sprzętu, systemu, bezpieczeństwa | Hardware plus MDM and SOC licences, not one need. |
| 49 | dns, mail, response ndr, network detection, ndr, waf | Grouped by language; varied products. |
| 52 | prs, review, apk, question, does, completed | Unrelated developer workflow requests. |
| 53 | extensions, default, plugins, headers, security, override | Different products' default settings, no shared need. |
| 54 | markdown, request, feature, feature request, api key, suppression | Unrelated features grouped by request boilerplate. |
| 56 | version, job, error, vulnerability, 08, continue | Varied build and scanner issues without one need. |
| 57 | action, cr, mechanism, blob, openclaw, sign | Different auth features in unrelated products. |
| 58 | deny, unauthorized, default, bug, denies, excessive | Unrelated bugs sharing deny and unauthorized words. |
| 60 | qualified, regulation eu, regulation, eu, service, trust | Unrelated purchases and obligations. |
| 61 | die, zu, die universität, von, bundle, universität | Two unrelated tenders: pentests and a firewall. |

