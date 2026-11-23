# Safeguards Desk

> Verified FTC Safeguards program for small tax, mortgage and accounting offices: read-only Microsoft 365 checks, required scans and tests, and evidence from real configuration.

Opening `smb-compliance-reporting` (priority 2) · from Regulatory incident reporting and breach notification (theme 50, stability 0.92), Affordable security programs for small businesses (theme 12, stability 0.8)

## Buyer and user

- **Buyer:** Owner or managing partner of the practice (usually the firm's designated 'Qualified Individual'); in the partner channel, the owner of an MSP that serves accounting and mortgage offices and resells the program — US tax, bookkeeping/CPA and mortgage-broker offices with 3-20 staff on Microsoft 365 (Google Workspace later), no in-house security staff, holding customer information on 5,000 or more consumers, e.g. an established tax office keeping several years of returns or a broker keeping loan files. Above that line 16 CFR 314.6 no longer exempts them from the written risk assessment, the IR plan, annual penetration testing plus six-monthly vulnerability assessments (absent continuous monitoring) and the annual report to the board, duties a template WISP does not perform. Offices below 5,000 consumers are a cheaper secondary tier that is honestly labelled as good practice beyond the legal minimum.
- **User:** The owner or office manager reviews the monthly findings email and signs off the annual report; the firm's outside IT person or MSP fixes the findings; the founder runs scans, the annual test and the tabletop.

## Problem

Small non-bank financial firms must run a Safeguards program, and once they hold data on 5,000+ consumers they must also do a written risk assessment, an IR plan, annual penetration tests with six-monthly vulnerability scans, and a yearly report. Tax-pro WISP vendors sell documents and bundlers sell endpoint MDR, but nobody verifies the Microsoft 365 tenant or delivers the required testing at small-office prices. Assurance is owner self-attestation; SOC 2 platforms and audits assume engineers and budgets these offices lack.

- The FTC Safeguards Rule requires covered non-bank financial institutions to keep an information security program, including monitoring and logging of user activity, continuous monitoring or annual penetration tests plus six-monthly vulnerability assessments, and FTC notice within 30 days of a notification event involving 500+ consumers. ([source](https://www.ecfr.gov/current/title-16/chapter-I/subchapter-C/part-314/section-314.4))
- A small-company operator looking for a security audit finds providers have gone 'full-enterprise' and asks for services that are not enterprise-focused. ([source](https://news.ycombinator.com/item?id=25520219))
- A 'one man show' facing an audit cannot find a usable checklist and the auditors provide none. ([source](https://serverfault.com/questions/142737/it-audit-checklist))
- A 6-person firm with no IT department is asked by a client for a SOC 2 Type II audit and sees no way to meet it. ([source](https://security.stackexchange.com/questions/194368/soc-2-audit-for-small-business-6-employees-with-no-it-department))
- A ~10-person organisation wants a professional assessment of its online accounts (email, cloud documents) so they cannot be hijacked. ([source](https://news.ycombinator.com/item?id=16255598))
- SOC 2 platforms start around $8.5k-$15k/year before the audit, unaffordable for sub-10-person firms. ([source](https://aws.amazon.com/marketplace/pp/prodview-5ophamrbfxt44))
- Amended SEC Regulation S-P requires an incident response program and notice to affected individuals within 30 days, extending a comparable duty to small advisers. ([source](https://www.federalregister.gov/documents/2024/06/03/2024-11116/regulation-s-p-privacy-of-consumer-financial-information-and-safeguarding-customer-information))

## Why now

The amended Safeguards Rule's FTC breach notice took effect on 13 May 2024 and the IRS and Security Summit keep telling tax pros that a written plan is required by law, so owners now buy WISPs: Verito sells a custom WISP at $499 for the first year and then $999 a year, and ACE charges a flat $699. Tax-industry channels now also bundle endpoint MDR with a WISP (SBTPG with Watch Cloud), and insurers sell tax-pro cyber cover with breach response from $297 a year. What the market still lacks is verification and the 314.4(d)(2) testing that firms above 5,000 consumers owe. That is exactly the gap a technical founder can fill and MSPs that serve these offices cannot staff. Reg S-P reached smaller covered institutions on 3 June 2026, a second segment with a similar duty. [1](https://www.hoganlovells.com/en/publications/ftc-amends-safeguards-rule-to-require-non-banking-financial-institutions-to-report-data-breaches) [2](https://www.irs.gov/newsroom/irs-security-summit-remind-tax-pros-they-need-a-written-information-security-plan-to-protect-client-data) [3](https://verito.com/buy-wisp-d) [4](https://www.acecloudhosting.com/written-information-security-plan/) [5](https://www.sbtpg.com/all-in-one-cybersecurity/) [6](https://www.ptin.org/insurance/cyber) [7](https://www.ecfr.gov/api/renderer/v1/content/enhanced/current/title-16?part=314&section=314.6) [8](https://datamatters.sidley.com/2026/04/30/u-s-sec-regulation-s-p-compliance-deadline-approaching-for-smaller-entities/)

## MVP

- **Obligation scoping at onboarding: a short questionnaire (consumer count, data held, systems, vendors, insurer) that tells the firm which 314.4 duties apply, and marks those that the 314.6 exemption for under 5,000 consumers lifts, before any sale is made.** — Answers the critics' main legal point: the program is sold for what the law actually requires of that firm, and good practice is labelled as such.
- **Read-only Microsoft 365 posture monitor (Graph and Exchange Online, admin-consented app, no mailbox content read): MFA coverage, accounts of leavers and inactive users, external mail forwarding and inbox rules, new admin roles, and risky sign-ins where the tenant's licence exposes them; monthly findings email with fix guides for the firm's IT person or MSP.** — Replaces owner self-attestation with evidence from real configuration and covers the business-email-compromise path that hits these offices most; plays to the founder's Windows/M365 skills.
- **Six-monthly external vulnerability scan plus an annual founder-run penetration test of the office's internet-facing services and M365 tenant (scoped, written authorization), with a dated report filed as 314.4(d)(2) evidence.** — A legal duty for firms above 5,000 consumers without continuous monitoring, which WISP-document vendors and template sellers do not deliver; it uses the founder's offensive-testing credentials.
- **Tailored WISP, risk assessment and IR plan generated from the scoping answers and the monitor's findings, regenerated when findings change, plus the annual report to the owner/board (314.4(i)).** — The document stays tied to what is actually configured, which a one-off or yearly-revised WISP cannot do.
- **Incident first-hour card instead of a reportability engine: on suspicion, it tells the owner to call the cyber insurer's hotline or counsel first, records only facts (who noticed what and when, systems affected) for handoff to the breach coach, and lists the steps counsel will direct: IRS Stakeholder Liaison, state tax agencies, state AGs, and the FTC form if 500+ consumers are involved.** — Keeps reportability decisions with counsel and under privilege, avoids conflicting with the insurer, and adds the IRS steps tax pros need. The card is included free, not sold as the differentiator.
- **Partner console for MSPs: multi-client view of findings and evidence, white-label reports.** — Lets MSPs that already handle endpoints sell the compliance and testing layer they cannot staff, giving the solo founder distribution.

Out of scope for v1: Deciding reportability or giving legal advice; reportability is presumed and goes to counsel or the insurer's breach coach; Endpoint MDR/EDR, backup or 24/7 SOC (left to the MSP or bundles such as Watch Cloud; we verify and document, not replace); Running hardening changes in client tenants without a separate written change authorization; Notification letters, call centres or credit monitoring (Kroll/Experian-type services via insurer); Storing client SSNs, tax returns or mailbox content; SOC 2/ISO 27001 certification, NIS2; Reg S-P only as a later segment; Google Workspace checks in v1.

## Competition

| Competitor | How we differ |
|---|---|
| [Santa Barbara Tax Products Group with Watch Cloud Cyber Security](https://www.sbtpg.com/all-in-one-cybersecurity/) | Bundles MDR, backup, VPN and a WISP (custom and annually updated at the top tier) per device, payable from refund-transfer fees. It is endpoint security sold through the bank-product channel. We do not compete on endpoints: we verify M365 configuration and deliver the (d)(2) scans and tests, and can sit beside a Watch Cloud or MSP stack as its evidence layer. |
| [Verito VeritShield WISP](https://verito.com/buy-wisp-d) | Custom tax-pro WISP at $499 for the first year, then $999/year, with unlimited updates. It is a document service. We cost more but include continuous tenant checks, six-monthly scans and an annual test, which a document does not. |
| [ACE Cloud Hosting managed WISP](https://www.acecloudhosting.com/written-information-security-plan/) | Flat $699 custom WISP tied to their hosting. It is hosting-neutral for us, and our WISP is regenerated from live findings rather than written once. |
| [PTIN.org tax-pro cyber insurance programs](https://www.ptin.org/insurance/cyber) | $297-$697/year cover with pre-breach legal access and breach response. It is a complement, not a rival: our first-hour card hands off to the insurer's hotline, and evidence of controls can support underwriting. We aim to be the insurer's referral, not its substitute. |
| [IRS Publication 5708 free WISP template](https://www.irs.gov/newsroom/irs-security-summit-remind-tax-pros-they-need-a-written-information-security-plan-to-protect-client-data) | Free and adequate for firms under 5,000 consumers that only need the document; we do not pretend otherwise and target firms that also owe testing. |
| [MSPs with compliance-as-a-service tooling (e.g. ScalePad ControlMap)](https://scalepad.com/controlmap/pricing) | Generic GRC tooling that assumes the MSP writes the program and does testing. We are a vertical Safeguards module plus pen-test delivery that an MSP resells; we partner with MSPs rather than replace them. |
| [Secureframe / Vanta / Drata](https://secureframe.com/pricing) | SOC 2/ISO automation from $7,500/year for funded tech firms; not what a tax office compares against, listed only as the ceiling. |

**Differentiation:** Every tax-pro competitor sells a document, insurance or endpoint tools; none checks the Microsoft 365 tenant where these offices get breached, or delivers the scans and pen test that firms above 5,000 consumers legally owe. A credentialed tester does both at small-office prices, scopes duties honestly by the 314.6 threshold, and resells through MSPs and alongside insurers instead of fighting their distribution.

## Build

- Team: 1 technical founder (builds the monitor and reports, runs scans, tests and tabletops); a contract lawyer for terms, handoff wording and the 314.4(f) service-provider agreement; no hires until about 40 Program clients
- Time to MVP: 3 months
- Hardest parts: Securing the vendor itself: a read-only multi-tenant M365 app holding findings for many financial firms needs least-privilege consent, per-tenant isolation, MFA, audit logging and a documented program of its own that clients' 314.4(f) oversight will accept; Signal coverage per M365 licence: some Graph data (sign-in logs, registration details) may depend on the tenant's Entra ID licence, so checks must degrade cleanly on Business Basic/Standard tenants; Keeping founder hours per Program client at or under ~8 a year (two scans, one test, one tabletop, report) so margins hold at $179/month; Liability: scoped test authorizations, a liability cap, and E&O/cyber cover priced before the first test; Winning MSP partners who will expose their clients to a third party's findings about their own work

## Pricing and business model

- **Model:** Two tiers by legal obligation, annual subscription; MSPs buy wholesale at about 30% off and resell
- **Entry price:** Program tier (firms with 5,000+ consumers): $490 setup + $179/month billed annually, up to 20 users, including continuous M365 checks, two external scans, one annual pen test, a tabletop and the annual report. Core tier (under 5,000): $39/month, monitor and WISP only.
- **Rationale:** Program costs about $2,150 a year, more than Verito's $999 WISP or a $297-$697 insurance plan (see competitors), so it is sold on what those do not do: legally required testing and verified configuration. It stays far below SOC 2 platforms and typical standalone pen-test engagements. Around 40 Program clients come to about $86k ARR, which needs far fewer sales than the 150 clients in the earlier version. Core is the low-touch tier for firms that only owe the document and is priced near awareness-training spend.

| Comparable | Price |
|---|---|
| Secureframe Fundamentals | [starting at $7,500/year](https://secureframe.com/pricing) |
| Sprinto Starter (AWS Marketplace) | [$8,500 per 12 months, up to 25 employees; audit separate](https://aws.amazon.com/marketplace/pp/prodview-upzeowcpyofas) |
| KnowBe4 Security Awareness Training | [SAT Foundation $2.40/seat/month at 25-50 seats, 3-year term](https://knowbe4.com/pricing-security-awareness-training) |
| Cyber Essentials (IASME certification fee) | [from £320 + VAT](https://www.ncsc.gov.uk/information/cyber-essentials) |

## Go to market

- **First customers:** Ten firms above the 5,000-consumer line: small mortgage brokers and lenders (selling all year, unlike tax offices) and established tax/CPA offices with 5-20 staff on Microsoft 365. At least half come through two or three MSPs that serve accounting and mortgage offices and lack security-testing staff, and the rest from direct outreach in May-December.
- **Channel:** Partner-first: MSPs resell the Program as their compliance and testing layer (wholesale pricing, white-label reports); then approaches to tax-pro cyber insurance programs and state tax-practitioner associations for referrals; a free 'which Safeguards duties apply to you' scoping tool and a free external scan as top-of-funnel; direct founder sales as a supplement, not the core.
- **Wedge:** Annual pen test plus six-monthly vulnerability assessments under 314.4(d)(2) for firms with 5,000+ consumers: a concrete legal duty with a dated deliverable that WISP vendors and bundles do not provide, and that the founder's PenTest+ background makes credible.

## Risks

- Bundling: SBTPG/Watch Cloud, Verito and hosting or MSP vendors already sell the WISP and endpoint security through channels the owner already uses and could add scans or a tenant check; our defence is testing delivery and the MSP partnership, which is thin and relationship-based rather than a product moat.
- Demand: no tax-office or mortgage-broker owner in the input asks for verification or testing, and low FTC enforcement against small firms may keep them on a $999 WISP plus insurance; the 5,000-consumer segment may be smaller or less aware of the duty than assumed.
- Liability and legal: running tests on client systems, holding findings for many financial firms and anything that reads as reportability advice expose a solo founder; we need a liability cap, E&O/cyber cover, written authorizations and counsel-reviewed wording, and claims stay within what 314.4 and 314.6 say.
- Channel risk: MSPs may see findings about their own clients' tenants as a threat, and insurers may not refer; without partners, founder-led sales to seasonal tax offices is slow.
- Technical: M365 API and licence limits may reduce signal on cheaper tenants, and a breach of the vendor's own platform would cascade to every client.
- Scale: testing and tabletops are founder hours; beyond ~40-60 Program clients the founder needs contract testers or MSP-delivered testing.

## Riskiest assumption

- **Assumption:** Small financial offices above 5,000 consumers, or MSPs on their behalf, will pay about $2k/year for verified configuration and 314.4(d)(2) testing on top of the WISP and cyber insurance they already buy.
- **Cheap test:** In two weeks, without building software: offer 15 MSPs that serve accounting or mortgage offices a white-label pilot, and email 40 mortgage brokers and established tax offices a fixed-fee $490 'Safeguards testing check' (manual external scan plus a read-only M365 review delivered by hand). In 10 owner calls, ask about consumer count, insurer questionnaires and whether anyone has asked for proof of testing.
- **Success signal:** At least 3 paid $490 checks or 1 MSP letter of intent covering 10+ client offices, and at least 4 of 10 owners above 5,000 consumers saying they have no annual test or vulnerability assessment and would pay to have one.

## Open questions

- How many small tax, CPA and mortgage offices actually hold data on 5,000+ consumers, and do they know it?
- Is FTC or state AG enforcement reaching sub-20-person firms, and do cyber insurers' questionnaires now ask for testing evidence?
- Will an insurer program such as PTIN.org's or a tax-practitioner association refer or co-market the program?
- Does a founder-run test on a small office satisfy 314.4(d)(2) in a regulator's eyes, and what scope is reasonable?
- Do MSPs serving these offices see the program as a resellable add-on or as a third party grading their work?
- Should small SEC-registered advisers under Reg S-P (compliance since 3 June 2026) be the second segment, and how much of the program carries over?
- What E&O/cyber premium and contract terms does a solo tester need, and does it fit the price?

