# Agent Hardening Sprint

> Fixed-fee sprint that red-teams a small company's coding agents, MCP servers and CI agent runs, then installs an enforced tool policy and audit trail.

Opening `ai-agent-access-control` (priority 3) · from Permission gating for AI agent tool calls (theme 10, stability 0.65), Authorization and auditing for MCP tool access (theme 0, stability 0.55)

## Buyer and user

- **Buyer:** CTO / VP Engineering, or the person who owns SOC 2 or ISO 27001 evidence — B2B SaaS company with 15-150 employees, developers using Claude Code, Cursor or Copilot with MCP servers wired to GitHub, cloud and production data; preparing for or maintaining SOC 2 and receiving customer questionnaires asking how AI coding tools are controlled; no in-house AppSec engineer.
- **User:** The CTO and engineering leads who receive the findings report and policy pack; developers who work under the installed policy; the compliance owner who files the audit evidence.

## Problem

Small companies adopted coding agents and MCP servers faster than they set rules for them. Permissions are per-developer, MCP tools are auto-approved, headless CI runs auto-approve everything, secrets reach tool inputs, and there is no audit trail. Enterprise platforms sell through large annual commits; leading MCP governance vendors offer no self-serve. These companies need someone to find the real exposure and set up controls they can show an auditor.

- Teams adopting MCP in Claude Code get single-developer setup docs but no governance or security guidance for team adoption. ([source](https://github.com/anthropics/claude-code/issues/60246))
- Wildcard subagents inherited all 16 MCP servers including mail-send and file-delete, and every MCP call default-allowed because the validator did not exist. ([source](https://github.com/akaszubski/autonomous-dev/issues/1549))
- Passing secrets as raw input to an MCP tool is a security anti-pattern found in a widely used developer platform. ([source](https://github.com/backstage/backstage/issues/34728))
- Users want hooks to stop secrets leaving the machine to the LLM provider and to attackers. ([source](https://github.com/anthropics/claude-code/issues/39882))
- A static capability audit of an MCP server found tools with no operation filtering and SQL tools accepting arbitrary DDL/DML. ([source](https://github.com/oracle/mcp/issues/164))
- Leading MCP governance vendors (Runlayer, MintMCP) publish no prices and offer no self-serve, so small teams cannot evaluate or buy. ([source](https://www.truefoundry.com/blog/runlayer-pricing))
- External audit connectors and fine-grained authorization require Descope Growth at $799/mo; lower tiers keep audit for 1 week to 1 month. ([source](https://www.descope.com/pricing))
- In non-interactive -p runs the Antigravity CLI auto-approves all tool calls including write_file, making it unsafe for automation that processes untrusted input. ([source](https://github.com/google-antigravity/antigravity-cli/issues/45))

## Why now

All major coding agents now expose enforceable pre-tool-call hooks or policy engines (Claude Code, Cursor, Copilot, Gemini CLI), so a consultant can install real controls with free building blocks instead of selling a platform. OWASP's Top 10 for Agentic Applications (Dec 2025) gives auditors and buyers a reference list to ask about, and clouds (AWS AgentCore Policy GA, March 2026) are normalising per-tool-call authorization as an expected control. [1](https://genai.owasp.org/resource/owasp-top-10-for-agentic-applications-for-2026/) [2](https://code.claude.com/docs/en/hooks) [3](https://cursor.com/docs/agent/hooks) [4](https://docs.github.com/en/copilot/concepts/agents/coding-agent/about-hooks) [5](https://geminicli.com/docs/core/policy-engine/) [6](https://aws.amazon.com/about-aws/whats-new/2026/03/policy-amazon-bedrock-agentcore-generally-available)

## MVP

- **Inventory script (run by the client) that collects each developer's agent configs, permission rules, hooks and MCP server list, plus a workflow scanner that flags CI agent steps triggered by untrusted events with write permissions or secrets; secrets stripped** — Most teams do not know which agents, MCP servers and CI agent jobs are in use; this scopes the engagement in a day.
- **Hands-on prompt-injection red team: planted issues, poisoned files and malicious MCP tool output against the client's real agent setup, documented as reproducible findings** — Turns abstract risk into evidence a CTO acts on; uses the founder's offensive-testing skills.
- **Policy pack: one YAML policy compiled into each agent's native hooks/managed settings by open-source hook scripts that parse commands (shell AST) rather than match strings** — Delivers enforced controls with free building blocks and closes the compound-command bypass of pattern-based native rules.
- **CI agent hardening: read-only default for headless runs, automatic downgrade to read-only when job input is untrusted issue/PR text, and a canary secret that fails the run if it appears in tool input or output** — Headless runs auto-approve tool calls with nobody watching; this targets the main injection path deterministically.
- **Audit logging from hooks into the client's existing log store, plus a control narrative mapped to OWASP agentic risks and SOC 2 change-management evidence** — The compliance owner gets something to file and show customers.
- **Monthly retainer: policy updates as agents change, review of blocked-call logs, re-test after new MCP servers** — Recurring revenue and the data to later productise the most repeated work.

Out of scope for v1: Building a hosted SaaS platform in year one; 24/7 monitoring or incident response; Security of the client's own AI product (LLM app pentests) beyond the developer toolchain; Enterprise-wide rollouts over 300 developers; Formal SOC 2 audit or attestation.

## Competition

| Competitor | How we differ |
|---|---|
| [Knostic Kirin](https://www.knostic.ai/pricing) | A self-serve tool for scanning and policy; we deliver a tested setup, red-team findings and audit evidence, and can recommend Kirin where it fits. |
| [Native agent permissions and managed settings](https://code.claude.com/docs/en/permissions.md) | Free but someone has to design, test and maintain the rules across agents; that is the service. |
| [Docker MCP Gateway (open source)](https://docs.docker.com/ai/mcp-catalog-and-toolkit/mcp-gateway/) | Free container isolation for MCP servers with no per-user policy or audit without the enterprise version; we can recommend it alongside the hook policy, which also covers shell and file tools. |
| [Pillar Security / Lasso Security](https://www.lasso.security/use-cases/ai-coding-assistants) | Enterprise platforms bought through annual commits; we are a fixed-fee engagement priced for small companies. |
| [Runlayer / MintMCP](https://www.mintmcp.com/pricing) | Enterprise MCP gateways with unpublished, quote-only pricing; we set up controls without a new gateway. |
| [General pentest and vCISO firms](https://genai.owasp.org/resource/owasp-top-10-for-agentic-applications-for-2026/) | Usually test the product, not the developer toolchain; we specialise in coding-agent and MCP exposure with a reusable policy kit. |

**Differentiation:** A narrow specialist service with a productised kit: inventory and CI workflow scan, real prompt-injection tests against the client's own agents, and enforced controls installed through native hooks at a fixed price, with audit evidence for a SOC 2 auditor. No platform licence or gateway. The open-source kit, one compiled policy refined across engagements, is the seed of a later product.

## Build

- Team: 1 technical founder (solo, bootstrapped); subcontract a second tester only once demand exceeds 2 engagements per month
- Time to MVP: 1 months
- Hardest parts: Building credibility in AI-agent security quickly, since the founder's track record is Windows detection and CTFs rather than LLM tooling; Making the red-team phase reproducible and safe on clients' real repos and credentials; Keeping the hook-based policy kit and its shell-command parser current across four fast-changing agents and their headless modes, without false positives; Finding buyers without paid ads or an existing client base

## Pricing and business model

- **Model:** Fixed-fee assessment and setup, then optional monthly retainer
- **Entry price:** $3,500 fixed fee for up to 25 developers (2-week sprint: inventory, red team, policy pack, audit setup); retainer $400/month
- **Rationale:** Well under enterprise annual commits (Lasso $20k+) and comparable to a year of Descope Growth, but one-off and tied to evidence the buyer needs now. Three to four sprints a month plus a handful of retainers reaches a solo founder's income target in months, with near-zero running cost.

| Comparable | Price |
|---|---|
| Lasso Security | [AWS Marketplace annual commit $20,000 (GenAI Chatbots), $50,000 (LLM gateway)](https://aws.amazon.com/marketplace/pp/prodview-7ygm7pa3k5agg) |
| Descope Agentic Identity Hub | [Pro from $249/mo; Growth from $799/mo](https://www.descope.com/pricing) |
| Knostic Kirin | [Team $15/user/month](https://www.knostic.ai/pricing) |
| TrueFoundry MCP Gateway | [Pro $25 per user/month incl. 20K requests](https://www.truefoundry.com/pricing) |

## Go to market

- **First customers:** Ten 15-150 person B2B SaaS companies that use coding agents with MCP servers and are in a SOC 2 cycle or answering enterprise customer questionnaires about AI tooling; reached first through the founder's few industry contacts, then through referrals from SOC 2 readiness consultants and vCISOs who lack agent expertise.
- **Channel:** Founder-led: public red-team write-ups and talks at local security meetups and BSides; partnerships with SOC 2 readiness consultants/vCISOs who resell the sprint; LinkedIn outreach to CTOs; and outbound to companies whose public repositories run agents on untrusted issue/PR events, found with the workflow scanner and sent a short exposure note.
- **Wedge:** A free 30-minute 'agent exposure check' using the inventory script, ending with a one-page list of the three worst findings and a quote for the sprint.

## Risks

- Services do not scale and depend entirely on the founder's time; productising the kit later may take longer than planned.
- Credibility: buyers may prefer established AppSec firms; the founder must build public proof (write-ups, open-source kit) before deals close.
- Bundling: as agent vendors ship organisation-wide managed policies and dashboards, the setup work shrinks and the buyer may do it alone.
- Demand risk: small companies may treat agent security as a low priority until an incident or an auditor forces it.
- Liability: red-teaming clients' real agents with production credentials could cause damage; needs scoped rules of engagement and insurance. CI controls run in the same runner as the agent and are a guardrail, not a sandbox, and must be sold as such.

## Riskiest assumption

- **Assumption:** CTOs or compliance owners at 15-150 person SaaS companies will pay a few thousand dollars now for coding-agent and MCP hardening, before an incident or explicit auditor requirement.
- **Cheap test:** Offer the free agent exposure check to 30 companies via the founder's contacts, two SOC 2 consultants and LinkedIn; run the checks with the inventory script and quote the $3,500 sprint at the end of each.
- **Success signal:** At least 8 checks booked and at least 2 signed sprints (or deposits) within 2 weeks.

## Open questions

- Do SOC 2 auditors and enterprise questionnaires already ask specific questions about coding agents, or is this still optional?
- Which work is repeated across engagements and could become a product (variant v1 or v2)?
- Will SOC 2 consultants partner or see this as competition?
- How long will it take the founder to build recognised credibility in AI-agent security?
- Is unattended CI agent hardening a strong enough pain on its own to lead the sale, or only an add-on to the developer-laptop work?

