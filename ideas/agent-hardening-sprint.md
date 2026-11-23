# Agent Hardening Sprint

> Fixed-fee red team of a small company's coding agents, MCP servers and CI agent jobs, then hardening through vendor-native managed settings, sandboxing and tested guardrails.

Opening `ai-agent-access-control` (priority 3) · from Permission gating for AI agent tool calls (theme 10, stability 0.65), Authorization and auditing for MCP tool access (theme 0, stability 0.55)

## Buyer and user

- **Buyer:** CTO / VP Engineering; co-signed by the SOC 2 or ISO 27001 evidence owner when a customer questionnaire or auditor has asked about AI coding tools — B2B SaaS company with 15-150 employees whose developers use Claude Code, Cursor or Copilot with MCP servers wired to GitHub, cloud and production data, and that runs agents in CI on issue/PR events; selling to enterprises and receiving security questionnaires about AI tooling; no in-house AppSec engineer. Best fit: already on Claude Teams/Enterprise, Cursor Enterprise or an MDM, so controls can be delivered centrally.
- **User:** Engineering leads and the platform/DevOps owner who receive the reproducible findings and apply the hardening; developers who work under the managed settings; the compliance owner who files the findings, the control description and the re-test results.

## Problem

Small companies adopted coding agents, MCP servers and CI agent jobs faster than they set rules for them. MCP tools are auto-approved, headless runs approve everything, secrets reach tool inputs, and nobody has tested whether a poisoned issue or tool output can make their agents act. Enterprise platforms sell through large annual commits and leading MCP governance vendors offer no self-serve. These companies need their real exposure shown and the cheap native controls set up correctly.

- A desktop app passed blanket --allowedTools for all user-registered MCP servers, so user-added servers got tool auto-approval in headless Claude runs. ([source](https://github.com/currentbits/solenta/issues/126))
- Wildcard subagents inherited all 16 MCP servers including mail-send and file-delete, and every MCP call default-allowed because the validator did not exist. ([source](https://github.com/akaszubski/autonomous-dev/issues/1549))
- Passing secrets as raw input to an MCP tool is a security anti-pattern found in a widely used developer platform. ([source](https://github.com/backstage/backstage/issues/34728))
- An MCP database server's 'read-only' mode could be bypassed (improper access control), so a configured safety mode did not hold. ([source](https://github.com/donghao1393/mcp-dbutils/issues/116))
- Users want hooks to stop secrets leaving the machine to the LLM provider and to attackers. ([source](https://github.com/anthropics/claude-code/issues/39882))
- A static capability audit of an MCP server found tools with no operation filtering and SQL tools accepting arbitrary DDL/DML. ([source](https://github.com/oracle/mcp/issues/164))
- Leading MCP governance vendors (Runlayer, MintMCP) publish no prices and offer no self-serve, so small teams cannot evaluate or buy. ([source](https://www.truefoundry.com/blog/runlayer-pricing))
- External audit connectors and fine-grained authorization require Descope Growth at $799/mo; lower tiers keep audit for 1 week to 1 month. ([source](https://www.descope.com/pricing))

## Why now

Coding agents now ship enforceable building blocks that small companies leave unconfigured: Claude Code server-managed settings (Teams/Enterprise) and MDM-delivered endpoint settings, native sandboxing, and blocking pre-tool hooks in Cursor, Copilot and Gemini CLI. GitHub Agentic Workflows makes read-only CI agents a documented pattern. OWASP's Top 10 for Agentic Applications (Dec 2025) gives buyers a reference list, and compliance platforms (Vanta AI governance, Drata AI Agent Governance, Aug 2026) are teaching SOC 2 buyers to ask about agents. SOC 2 still has no AI criteria, so this is customer-questionnaire pull, not a mandate. [1](https://code.claude.com/docs/en/server-managed-settings) [2](https://cursor.com/docs/agent/hooks) [3](https://docs.github.com/en/copilot/concepts/agents/coding-agent/about-hooks) [4](https://geminicli.com/docs/core/policy-engine/) [5](https://github.github.com/gh-aw/introduction/overview/) [6](https://genai.owasp.org/resource/owasp-top-10-for-agentic-applications-for-2026/) [7](https://www.vanta.com/products/ai-governance) [8](https://securitybrief.co.uk/story/drata-launches-ai-agent-governance-for-anthropic-users) [9](https://labs.cloudsecurityalliance.org/research/csa-research-note-soc2-ai-controls-gap-20260830-csa-styled/)

## MVP

- **Client-run inventory script that reports which agents, permission modes, hooks, MCP servers and CI agent jobs are in use, emitting only a summary (server names, permission modes, trigger types; no env values, tokens or code) that the client reviews before sharing; CI workflows also checked with zizmor** — Scopes the engagement in a day without the founder ever holding client secrets; reuses a maintained scanner for workflow risks (D7).
- **Prompt-injection red team run in a disposable environment: a fork of a real repo, scoped test tokens and the client's real MCP server versions or mock MCP servers, using a versioned private suite of 30+ injection cases (planted issues, poisoned files, malicious tool output, interpreter and script-file indirection). Production credentials only with written approval and least-privilege tokens** — The part no platform bundles and the founder's offensive skills fit; the disposable setup keeps liability and access requests manageable while reproducing the real agent configuration.
- **CI agent hardening: least-privilege GITHUB_TOKEN, no secrets on untrusted triggers, read-only agent jobs with writes through a separate gated step (GitHub Agentic Workflows pattern), plus a canary secret as a tripwire only** — The deterministic, low-liability fix for the main injection path; the canary is described as catching verbatim leaks only.
- **Hardening through vendor-native central controls: managed settings via Claude Teams/Enterprise or MDM (allowManagedHooksOnly, managed MCP allowlist), native sandbox with network egress allowlist, and fail-closed hooks using a maintained open-source command guard where the native rules fall short; no custom policy compiler** — Central, fail-closed delivery is what makes controls hold; native and maintained tools cut the upkeep a solo founder cannot carry across four agents.
- **Findings report with re-test results, a stated-bypass list for every guardrail, and a control description mapped to OWASP agentic risks that the client's auditor can evaluate; agent logs shipped to the client's own central store where one exists** — Gives the compliance owner an honest artefact for questionnaires without claiming a SOC 2 criterion or calling bypassable controls 'enforced'.
- **Quarterly re-test: re-run the injection suite against the client's setup after agent, MCP or workflow changes, with a short delta report** — Recurring revenue tied to testing, which a $15/user policy tool does not do, instead of selling policy upkeep that native settings and Kirin cover.

Out of scope for v1: Building a hosted SaaS platform or a cross-agent policy compiler in year one; Continuous runtime enforcement or dashboards (recommend Kirin, Vanta or the vendor's managed settings); Holding or reviewing client logs; 24/7 monitoring or incident response; Testing third-party MCP servers or SaaS APIs the client cannot authorise; Security of the client's own AI product (LLM app pentests); Formal SOC 2 audit, attestation or a statement that a criterion is met; Unsolicited scanning of or outreach about other companies' public repositories.

## Competition

| Competitor | How we differ |
|---|---|
| [Vanta AI governance (and the free agentic controls it publishes)](https://www.vanta.com/products/ai-governance) | Discovery, guardrails and evidence inside the SOC 2 platform the buyer already pays for; we do not compete on that. We red-team the client's real agent and CI setup and configure the native controls, and work as an implementation partner where Vanta is in place. |
| [Drata AI Agent Governance](https://securitybrief.co.uk/story/drata-launches-ai-agent-governance-for-anthropic-users) | Limited-availability proxy and evidence feed aimed at enterprises running Anthropic agents; no hands-on injection testing of developer toolchains or CI jobs. |
| [Knostic Kirin](https://www.knostic.ai/pricing) | Self-serve continuous policy and audit at $15/user/month; we recommend it for ongoing enforcement and sell what it does not do: adversarial testing, CI hardening and periodic re-tests. |
| [Coding-agent security boutiques (Christian Schneider assessment, Appsecco MCP pentests)](https://christian-schneider.net/consulting/coding-agent-security/) | Schneider's is an interview-based assessment and roadmap; Appsecco tests MCP servers. We run hands-on injection tests against the client's own agent, MCP and CI setup and install the fixes, at a published fixed price for small companies. |
| [Native managed settings plus free tools (zizmor, GitHub Agentic Workflows, open-source command guards)](https://code.claude.com/docs/en/server-managed-settings) | Free but someone has to choose, configure and test them against the client's real setup; we use them rather than replace them. |
| [Pillar Security / Lasso Security](https://www.lasso.security/use-cases/ai-coding-assistants) | Enterprise platforms bought through annual commits; we are a fixed-fee engagement priced for small companies. |
| [Runlayer / MintMCP](https://www.mintmcp.com/pricing) | Enterprise MCP gateways with quote-only pricing; we harden the setup without adding a gateway. |

**Differentiation:** A hands-on prompt-injection red team of the client's own coding agents, MCP servers and CI jobs, followed by hardening with vendor-native central controls and re-tests, at a published fixed price. Platforms (Vanta, Drata, Kirin) discover and enforce but do not attack your setup; boutiques interview or test MCP servers in isolation. We complement the platform the buyer already has. The asset is a private, growing injection-test suite and public research, not a policy kit.

## Build

- Team: 1 technical founder (solo, bootstrapped); white-label partners do their own selling; subcontract a tester only above 2 sprints per month
- Time to MVP: 3 months
- Hardest parts: Building credibility first: 2-3 public reproducible write-ups on coding-agent or CI-agent injection (ideally vendor-acknowledged findings) before selling, since the founder's track record is Windows detection and CTFs; Building the disposable test environment and the versioned injection suite (including interpreter and script-file indirection) so red teams are reproducible and safe in a 2-week sprint; Keeping hardening guidance and the test suite current as four agents change managed-settings, sandbox and hook semantics, including cloud and CI agent limitations; Engagement paperwork and cover: rules of engagement, authorisation letter, liability cap, DPA, and E&O/cyber insurance before the first sprint; Finding buyers without paid ads or an existing client base

## Pricing and business model

- **Model:** Fixed-fee red team and hardening sprint, then optional quarterly re-test; wholesale price for partner firms that resell it
- **Entry price:** $6,500 fixed fee for up to 25 developers and 3 CI repositories (2-week sprint: inventory, red team, CI hardening, native-control setup, re-test); quarterly re-test $1,800; partners buy at $5,000
- **Rationale:** Priced as a scoped assessment rather than a tool: well under enterprise annual commits (Lasso $20k+), about a year of Descope Growth, and in a different category from $15-25/user tools, which the concept recommends rather than undercuts. At about 2 sprints a month (realistic solo capacity) this grosses about $13k/month and covers insurance and a partner margin. Re-tests are priced on testing, not policy upkeep, so they do not compete with Kirin.

| Comparable | Price |
|---|---|
| Lasso Security | [AWS Marketplace annual commit $20,000 (GenAI Chatbots), $50,000 (LLM gateway)](https://aws.amazon.com/marketplace/pp/prodview-7ygm7pa3k5agg) |
| Descope Agentic Identity Hub | [Pro from $249/mo; Growth from $799/mo](https://www.descope.com/pricing) |
| Knostic Kirin | [Team $15/user/month](https://www.knostic.ai/pricing) |
| TrueFoundry MCP Gateway | [Pro $25 per user/month incl. 20K requests](https://www.truefoundry.com/pricing) |

## Go to market

- **First customers:** Ten 15-150 person B2B SaaS companies using coding agents with MCP servers and CI agent jobs that have a concrete trigger: an enterprise customer questionnaire item on AI coding tools, an auditor question, or an internal near-miss. Reached through the founder's contacts, readers of the public research, and two or three SOC 2 readiness, vCISO or small pentest firms that add the sprint as their 'AI coding tools' line item.
- **Channel:** Research-led and partner-led: public write-ups, a self-scan-only release of the inventory tool and BSides/meetup talks build credibility; small pentest, SOC 2 readiness and vCISO firms resell the sprint at the wholesale price (their margin about $1.5k); listing in compliance-platform partner directories where available. Vulnerabilities found in public projects during research go through a published, no-pitch private disclosure policy, never into sales.
- **Wedge:** A free, client-run self-scan plus a 30-minute walkthrough of its summary, ending with a fixed quote; or a one-repository CI-agent injection test as the first paid step for buyers unsure about granting red-team access.

## Risks

- Demand: SOC 2 has no AI criteria, so purchases depend on customer questionnaires, auditor questions or incidents; without them, small CTOs defer and deal flow is uneven.
- Bundling: Vanta, Drata and Kirin bundle discovery, guardrails and evidence, and agent vendors expand managed settings; the configuration part shrinks, leaving the red team and re-tests as the defensible core. No technical moat; reputation and the private test suite are the only assets.
- Credibility and capacity: an unknown solo founder competes with boutiques that already publish research; about 2 sprints a month caps revenue until partners or a second tester are added.
- Liability and data: injection tests can cause damage if production credentials are used; needs written authorisation, third-party exclusions, a liability cap, insurance, and testing in disposable environments by default. The founder must stay out of client logs, and command logging is employee monitoring that needs notice.
- Misrepresentation: guardrails are client-side and partly fail-open; they must be described with stated bypasses, never as 'enforced' or as meeting a SOC 2 criterion, or a client incident becomes a claim against the founder.
- Technical: hooks and command parsing do not stop interpreter or script indirection; real containment depends on sandboxing, egress limits and least-privilege tokens, which some clients will not adopt.

## Riskiest assumption

- **Assumption:** Enough 15-150 person SaaS companies have a concrete trigger (a customer questionnaire item, auditor question or near-miss about coding agents) to pay about $6,500 for a red team and hardening now, directly or through a partner firm.
- **Cheap test:** In two weeks: interview 10 SOC 2 readiness, vCISO or small pentest firms about how often clients get coding-agent or MCP questions and offer them the wholesale sprint; contact 20 CTOs from the founder's network and research readers, ask whether they have such a request in writing, and offer a pre-sold sprint with a $1,000 deposit.
- **Success signal:** At least 3 of 10 partner firms report clients with written coding-agent questions and 2 agree in writing to refer or resell, and at least 1 CTO pays a deposit at $6,500 (or 2 at the one-repository CI test).

## Open questions

- How fast will questionnaire and auditor questions about coding agents become routine, and in which customer segments first?
- Will Vanta or Drata partner programmes accept a solo implementation partner, or build their own red-team service?
- What share of target companies already have Claude Teams/Enterprise, Cursor Enterprise or MDM, so controls can be delivered centrally?
- Can E&O and cyber cover be bought at a cost the sprint price absorbs for a new solo firm?
- Can a later detection add-on (alerts on agent-spawned shells and MCP processes) use the founder's detection-engineering strength on mostly macOS/Linux fleets?
- Which repeated work, such as the injection suite, could become a self-serve product?

