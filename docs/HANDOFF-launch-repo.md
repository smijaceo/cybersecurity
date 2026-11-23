# Handoff: the launch repository

**For:** the agent that will set up and run a new GitHub repository that takes a concept from
gapfinder and brings it to life: brand, copy, website, sales and validation assets.
**From:** gapfinder (this repository), 2026-11-23.
**Owner / PM:** the repository owner (solo technical founder; profile below).

---

## 1. Mission, and one thing to get right first

gapfinder finds unmet needs in the cybersecurity market and stress-tests startup concepts with
critic agents. The launch repo takes one concept and builds everything a real business needs to
face real buyers.

**The concepts are not proven yet.** The best two are rated *PROMISING* by a nine-critic panel
calibrated against real historical startups, but every critic raised the same open objection:
**no evidence yet from the named buyer.** So the launch repo works in this order:

1. **Validation launch first.** Brand, landing page, offer, outreach and interview kit, built to
   run each concept's *riskiest-assumption test* (defined in the brief) and measure its
   *success signal*. This is real, launch-quality work. It just serves the test first.
2. **Full launch only after the success signal is met.** That means the full site, sales
   collateral, content and channels. If the test fails, record it, send the result back to
   gapfinder and move to the next concept. A fast "no" is a good outcome.

Never present an unvalidated concept as an established company (no fake customers,
testimonials, logos, user counts or "trusted by").

## 2. Input: the launch brief

gapfinder exports one validated JSON bundle per concept:

```
python -m gapfinder export-brief <opening_id>   # in the gapfinder repo
→ exports/<slug>/brief.json   (schema: gapfinder.schemas.LaunchBrief)
→ exports/<slug>/README.md
```

`brief.json` contains:
- **`concept`**: name, one-liner, buyer and user, problem with evidence URLs, why-now sources,
  MVP, competitors, differentiation, build plan, pricing with sourced comparables, go-to-market,
  risks, riskiest assumption, cheap test, success signal, open questions, revision log.
- **`panel`**: verdict, per-lens scores, position against the historical companies.
- **`open_objections`**: the fatal and major objections still standing. Copy and offer must not
  pretend these away.
- **`change_my_mind`**: the evidence that would raise critics' scores. This is the validation
  plan.
- **`evidence_signals`**: real posts, tenders and regulations behind the need.
- **`flagged_claims`**: claims a fact-checker found unsupported. **Never reuse them.**
- **`founder`**: the founder profile (below).
- **`status`**: `unvalidated` → `validated` / `rejected` (set by validation results).

Copy the bundle into the launch repo as `briefs/<slug>/brief.json`, keeping
`gapfinder_commit` for traceability. Don't edit it; write derived work elsewhere.

### Available briefs (2026-11-23)

| Brief | Verdict | Founder fit | Offer | Recommended order |
|---|---|---|---|---|
| `safeguards-desk` | PROMISING (5.62) | 7/10 | FTC Safeguards Rule programme and testing for 3–20 person tax, CPA and mortgage offices: $490 setup + $179/month; $490 fixed-fee "Safeguards testing check" | **1st**: best founder fit, and its test can earn revenue |
| `agent-hardening-sprint` | PROMISING (5.75) | 6/10 | $6,500 two-week red-team and hardening sprint for 15–150 person SaaS teams using coding agents; $1,800 quarterly re-test; $5,000 partner price | 2nd |
| `quietwin` | WEAK (5.5) | 7/10 | Detection-mapped Windows logging packs for small MSSPs on Wazuh, $9/tenant/month | Not recommended without new evidence |

## 3. The founder (who the brand and offer must fit)

From `config/founder.yaml` in gapfinder (summarised, no name):
- MS in cybersecurity; CompTIA A+, Network+, Security+, PenTest+, CySA+, Project+.
- Hands-on: CTFs, Windows administration and internals, Kali/pentest tooling, Python and
  automation, Windows detection engineering (WEF + Sysmon logon detection).
- **No capital**, plenty of time, a few industry contacts, solo with no sales team.

Implications: free or near-free tooling; no paid ads without explicit approval; sales motions
one person can run (direct outreach, partners/MSPs, community, content); services-first is fine.
The founder's real credentials are a genuine trust asset for the About page. Use only what's
true and confirmed with the founder.

## 4. How the repo should work (same discipline as gapfinder)

gapfinder's conventions worked; reuse them:
- **`CLAUDE.md`**: working rules, including everything in section 8.
- **`docs/ROADMAP.md`**: phases with deliverables, exit criteria and status; the source of truth.
- **`docs/DECISIONS.md`**: every scope, brand or spend decision, with the PM's approval.
- **`docs/rubrics/`**: one rubric per agent step. **`.claude/agents/`**: one definition per
  agent, pointing at its rubric and a validation command.
- **`.claude/workflows/`**: saved workflows for repeatable runs, invoked by file path.
- **Schemas** (pydantic) for every structured agent output; tests (`pytest`) before every commit.
- Reuse maintained open-source tools before writing your own.

Suggested repo name: **`launchpad`** (or `venture-launcher`). Suggested layout:

```
briefs/<slug>/brief.json              # imported from gapfinder, never edited
ventures/<slug>/
  positioning.md                      # L1
  brand/  (names.json, logo/*.svg, palette.json, typography.md, voice.md)   # L2
  copy/   (site/*.md, one-pager.md, outreach/*.md, interview-guide.md, proposal.md)  # L3
  site/   (website source, or a link to the hosted site repo)                # L4
  validation/ (targets.csv, results.jsonl, weekly-review.md)                 # L5
  claims-ledger.jsonl                 # every public factual claim → its source
launchpad/ (python package: schemas, checks, CLI)
docs/ .claude/ tests/
```

## 5. Phases

Each phase ends at a gate the founder approves. Record approvals in DECISIONS.md.

### L0 — Setup
Repo, CLAUDE.md, ROADMAP, DECISIONS, schemas, tests, cloud environment (copy gapfinder's
environment pattern: a setup script that installs the package). Import the chosen brief.
**Exit:** `pytest` passes; brief imported and validated.

### L1 — Positioning
From the brief only: ideal customer profile, the top three pains in buyers' words (with evidence
URLs), current alternatives (including "do nothing" and DIY), the one-sentence value
proposition, the offer and price, and answers to every open objection (or an honest "we don't
know yet, the test will tell us").
**Exit:** positioning approved by the founder; every claim traceable to the brief.

### L2 — Brand
- **Name:** 10–20 candidates (own ideas plus Shopify `generate-business-names`). Shortlist 3–5.
  Check `.com` and alternatives with Shopify `generate-domain-names`, which checks availability
  live and returns purchase links. **The founder buys the domain**, the agent never does. The
  founder runs a trademark search (USPTO TESS / EUIPO) on finalists. Check social handles.
- **Logo:** Higgsfield `generate_image` with `gpt_image_2_6` and `output_format: "svg"` for
  vector marks (or PNG for exploration). **Get a cost estimate first** (`estimate_image_cost`)
  and let the founder choose between free allowance and credits. Produce 3 directions × 2
  variants, then a wordmark, icon, favicon and social avatar. Light and dark versions.
- **Palette, typography, voice:** an accessible palette (WCAG AA contrast, checked by script),
  Google Fonts pairings, and a voice guide written for the buyer (a tax-office owner is not a
  CISO).
- No resemblance to competitors' names, logos or trade dress.
**Exit:** founder picks name, logo and palette; domain registered by the founder.

### L3 — Copy
Homepage, offer page (e.g. the $490 Safeguards check), pricing, About (true founder
credentials), FAQ, privacy policy and terms (templates, flagged for legal review), one-page
PDF, outreach emails and LinkedIn messages, call/interview guide, and a proposal / statement-of-
work template.
- **Claims checker (adversarial agent):** every factual claim must appear in
  `claims-ledger.jsonl` with a source from the brief or a primary text (e.g. 16 CFR 314 for
  the FTC Safeguards Rule). Unsupported or `flagged_claims` content blocks publishing.
- **Buyer-reader panel:** simulated buyer personas from the brief read the page and report what
  they understood, what they'd object to, and whether they'd act. Label results as simulated;
  they improve clarity, they are not validation.
- Not allowed: invented testimonials, customer logos, statistics without a source, "FTC
  approved/certified", guarantees of compliance. Add a "not legal advice" note where relevant.
**Exit:** claims check passes with zero unsupported claims; founder approves copy.

### L4 — Website
Two good options; the founder picks (record in DECISIONS):
- **A. Higgsfield website builder.** `create_website` with `type: "website"` (no Higgsfield
  sign-in) creates a React 19 + TanStack Start site on Cloudflare Workers with its own git
  repo. Load `get_workflow_instructions {workflow: "website-builder-flow"}` first, edit through
  `website_repo_access` + `sandbox_exec`, ship with `deploy_website` (live URL; redeploy after
  every change). **Don't call `publish_website`**, which lists the site on Higgsfield's
  community feed; a B2B security brand doesn't belong there unless the founder asks. Check how
  custom domains work before choosing.
- **B. Static site in the launch repo** (e.g. Astro) on GitHub Pages or Cloudflare Pages: free,
  versioned with everything else, custom domain straightforward.

Requirements either way: fast, mobile-first, accessible (WCAG AA), SEO basics, Open Graph
image, privacy-friendly analytics, a clear primary call to action tied to the success signal
(book a call / buy the $490 check / join the pilot list), a booking link (e.g. Cal.com free
tier) and a payment link (e.g. Stripe Payment Link; **the founder creates the accounts**).
Verify with Playwright screenshots at phone and desktop widths and a Lighthouse run (Chromium
is pre-installed in cloud sessions).
**Exit:** site live on the founder's domain; Lighthouse ≥ 90 for performance, accessibility,
SEO; founder approval.

### L5 — Validation (gapfinder's Phase 5)
Run the brief's riskiest-assumption test exactly, against its success signal.
- **Target list:** public business directories and professional listings, used within their
  terms. Business contact details only; record the source of each row. Respect CAN-SPAM, GDPR
  and the platforms' rules. No scraping where terms forbid it.
- **Outreach:** written by agents, **sent only by the founder.** Create Gmail drafts (Gmail
  connector) for the founder to review and send; never send automatically. Small, personal
  batches.
- **Interviews:** guide from L3; notes logged per call.
- **Results:** `validation/results.jsonl` (schema: contact type, channel, date, response, signal
  reached yes/no, quote, follow-up), plus a weekly review against the success signal.
- **Feed back:** when the test ends, write the outcome to the brief's status and send a summary
  back to gapfinder (a `validation/` file the PM copies across), so the next iteration learns
  from real buyers.
**Exit:** success signal met → L6, or not met → documented "no", next brief.

### L6 — Full launch (only after validation)
Expand the site, case study (with written client permission), sales collateral, content
calendar (LinkedIn and posts the founder can sustain), partner/MSP programme, and onboarding
and delivery playbooks for the service. Paid channels only with an approved budget.

## 6. Tools available in these sessions (verify at start; availability changes)

| Need | Tool | Notes |
|---|---|---|
| Name ideas | Shopify `generate-business-names` | No trademark or registry check: the founder verifies |
| Domain availability and price | Shopify `generate-domain-names` | Live availability; purchase links; the founder buys |
| Logo, icons, OG images | Higgsfield `generate_image` (`gpt_image_2_6`, SVG/PNG) | Costs credits or allowance; estimate first; the founder chooses |
| Website build and hosting | Higgsfield `create_website` / `deploy_website` | Plain `website` type; don't publish to the feed |
| Short product or explainer video | Higgsfield video tools | Later (L6), only with budget approval |
| Outreach drafts | Gmail connector (`create_draft`) | Drafts only; the founder sends |
| Shareable review pages | Claude Artifacts | Private by default; good for brand boards and copy review |
| Web research | WebSearch / WebFetch; or gapfinder's `python -m gapfinder fetch [--render] URL` | WebFetch can't reach some hosts in cloud sessions; the fetch command works |
| Screenshots, Lighthouse | Playwright + pre-installed Chromium | Phone and desktop widths |

## 7. Agents to define (each with a rubric and schema)

positioning-strategist · brand-namer · logo-designer · brand-critic · copywriter ·
claims-checker (adversarial) · buyer-reader (simulated persona panel) · site-builder ·
site-qa (Playwright + Lighthouse) · outreach-writer · validation-analyst.

## 8. Guardrails (put these in the launch repo's CLAUDE.md)

- **Spending:** no purchases, subscriptions, paid generations or ads without the founder's
  explicit approval for that specific spend. Show the estimate first.
- **Outward actions:** no emails sent, posts published, forms submitted or accounts created on
  the founder's behalf. Prepare drafts and links; the founder acts.
- **Truthful marketing:** every public claim sourced (claims ledger); no fabricated
  testimonials, customer logos, metrics or certifications; nothing from `flagged_claims`.
- **No impersonation:** don't copy competitors' names, branding, page layouts or copy.
- **Security services need written authorisation.** Any testing (pen tests, red teaming,
  scans), including during pilots, requires a signed scope and authorisation letter before
  work starts. Include templates; the founder gets them legally reviewed.
- **Needs a lawyer and the founder, not an agent:** business entity, contracts/SOW terms,
  liability limits, professional and cyber liability insurance (important for security
  services), privacy policy, and regulatory wording (FTC, SEC, NIS2).
- **Privacy:** business contacts only, sourced and minimal; delete on request.
- **Honest status:** the site may say "now taking pilot clients"; never imply an established
  customer base before there is one.

## 9. Starter prompt for the next agent

> You're setting up a new repository, `launchpad`, that turns validated cybersecurity startup
> concepts from my gapfinder repo into real businesses. Read
> `docs/HANDOFF-launch-repo.md` in the gapfinder repo (smijaceo/cybersecurity, or its renamed
> successor) and follow it. Start with L0 (repo setup with CLAUDE.md, ROADMAP, DECISIONS,
> schemas, tests) and import the `safeguards-desk` brief from gapfinder's
> `exports/safeguards-desk/brief.json`. Then propose the L1 positioning for my approval. Follow
> the guardrails in section 8: no spending, sending, publishing or account creation without my
> explicit approval.

**Session setup for the next agent:** create the empty repository on GitHub first (this
session's tools can't create repos), then start a cloud session with both repositories
attached: the new one with write access, gapfinder for reading briefs. Reuse the
`cybersecurity` cloud environment (unrestricted web access) or create one for the launch repo.
