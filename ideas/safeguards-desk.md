# Safeguards Desk

> Done-for-you FTC Safeguards program and 30-day breach-reporting clock for 1-20 person tax, bookkeeping and mortgage-broker offices, delivered by one practitioner.

Opening `smb-compliance-reporting` (priority 2) · from Regulatory incident reporting and breach notification (theme 50, stability 0.92), Affordable security programs for small businesses (theme 12, stability 0.8)

## Buyer and user

- **Buyer:** Owner or managing partner of the practice (often also the firm's designated 'Qualified Individual' under the Safeguards Rule) — US tax-preparation, bookkeeping/accounting and small mortgage-broker or lending offices with 1-20 staff, no in-house IT (an outside IT person or MSP at most), handling SSNs and bank data. They must keep a written information security plan (the IRS reminds tax pros of this every year) and, since May 2024, report notification events affecting 500+ consumers to the FTC within 30 days of discovery. Most hold a downloaded template they have never tested.
- **User:** The owner or office manager: completes the guided annual review, keeps the asset and vendor list current, and opens an incident in the reporting clock when something goes wrong, then signs off the one-page incident summary.

## Problem

Small non-bank financial firms are legally on the hook for a written security program and an FTC breach report, but have no IT staff and cannot justify $7.5k-$15k/year compliance platforms built for funded SaaS startups. Free templates give them a document, not a program: no risk assessment of their real setup, no tested incident plan, and no one to tell them on day one whether an incident is reportable and by when. Enterprise breach-decisioning tools are quote-only.

- The FTC Safeguards Rule requires covered non-bank financial institutions (e.g. tax preparers, mortgage brokers) to notify the FTC within 30 days of discovering a security event involving 500+ consumers. ([source](https://www.ecfr.gov/current/title-16/chapter-I/subchapter-C/part-314/section-314.4))
- A 6-person firm with no IT department is asked by a client for a SOC 2 Type II audit and sees no way to meet it. ([source](https://security.stackexchange.com/questions/194368/soc-2-audit-for-small-business-6-employees-with-no-it-department))
- A 'one man show' facing an audit cannot find a usable checklist and the auditors provide none. ([source](https://serverfault.com/questions/142737/it-audit-checklist))
- Security awareness training is increasingly demanded by regulators and underwriters, and small firms struggle to find something decent. ([source](https://news.ycombinator.com/item?id=30288999))
- SOC 2 platforms start around $8.5k-$15k/year before the audit, unaffordable for sub-10-person firms handling low-risk data. ([source](https://aws.amazon.com/marketplace/pp/prodview-5ophamrbfxt44))
- Enterprise breach-decisioning tools are quote-only; there is no self-serve product for small FTC-covered firms. ([source](https://www.capterra.com/p/187954/RADAR/))
- Amended SEC Regulation S-P requires notifying affected individuals within 30 days and expects service providers to notify the covered institution within 72 hours, extending the same kind of clock to small advisers. ([source](https://www.federalregister.gov/documents/2024/06/03/2024-11116/regulation-s-p-privacy-of-consumer-financial-information-and-safeguarding-customer-information))

## Why now

The FTC's amended Safeguards Rule took effect on 13 May 2024: notification events involving unencrypted customer information of 500+ consumers must be reported to the FTC no later than 30 days after discovery, and 'discovery' is the first day any employee or agent knows of it, so the clock starts earlier than many owners assume. The IRS and Security Summit keep reminding tax and accounting professionals that federal law requires a written information security plan and point to the FTC reporting duty, while managed-WISP offers aimed at tax pros (Rightworks, ACE Cloud Hosting at a flat $699) show owners already pay to have the document written for them, though not for an ongoing, tested program. A second small-firm clock follows: amended SEC Regulation S-P reaches smaller covered institutions such as small RIAs on 3 June 2026, with its own 30-day customer-notice duty. [1](https://www.hoganlovells.com/en/publications/ftc-amends-safeguards-rule-to-require-non-banking-financial-institutions-to-report-data-breaches) [2](https://www.irs.gov/newsroom/irs-security-summit-remind-tax-pros-they-need-a-written-information-security-plan-to-protect-client-data) [3](https://www.acecloudhosting.com/written-information-security-plan/) [4](https://www.rightworks.com/?p=32699) [5](https://datamatters.sidley.com/2026/04/30/u-s-sec-regulation-s-p-compliance-deadline-approaching-for-smaller-entities/)

## MVP

- **90-minute remote onboarding (screen-share) that inventories devices, Microsoft 365/Google accounts, tax software and vendors, checks MFA and backups, and produces a firm-specific WISP and risk assessment mapped to 16 CFR 314.4.** — Turns the template into a plan that matches the office; the founder's Windows administration skills make the review credible and fast.
- **Incident reporting clock: one form starts a case, records the discovery date, asks the reportability questions (customer information? encrypted? key compromised? how many consumers?) and records each answer with its reasoning, shows the FTC 30-day deadline plus the state breach notices to check, and pre-fills a draft of the FTC report fields.** — The moment of panic is when owners need help most and where templates are silent; documented reasoning protects the owner if the decision is questioned later.
- **Audit-ready incident record and owner sign-off: a timeline of decisions, who approved them and what was filed when, ending in a one-page summary the owner signs; onboarding captures the escalation tree (who decides, who files, counsel, cyber insurer and breach-coach contacts, applicable state laws).** — Examiners and insurers ask what was done and when; having the contacts and roles set before an incident means the first day goes to deciding, not searching.
- **Tested incident response plan: a 30-minute annual tabletop run by the founder over video, with the result logged as evidence.** — The rule asks for a program that is tested and updated, not only written.
- **Annual review and quarterly reminder emails (MFA still on, leavers removed, backups restored), with an evidence folder the owner can show an examiner, insurer or client.** — Keeps the plan alive and justifies a recurring fee.
- **Optional Microsoft 365 / Windows hardening checklist with scripts (PowerShell) the owner's IT person or the founder can run.** — Concrete fixes beyond paperwork, in the founder's strongest domain.

Out of scope for v1: Acting as the firm's legal counsel or deciding final reportability (the tool prepares, the owner and counsel decide); Mailing notification letters, call centres or credit monitoring (refer to Kroll/Experian-type services via insurer); SOC 2 or ISO 27001 certification; 24/7 monitoring or MDR; NIS2, SEC Reg S-P and other non-FTC regimes in v1.

## Competition

| Competitor | How we differ |
|---|---|
| [IRS Publication 5708 free WISP template](https://www.irs.gov/newsroom/irs-security-summit-remind-tax-pros-they-need-a-written-information-security-plan-to-protect-client-data) | Free and good, but a fill-in template; we tailor it to the office, test it yearly and add the breach-reporting clock. |
| [Rightworks managed WISP](https://www.rightworks.com/?p=32699) | Writes the WISP so the preparer can renew their PTIN; we sell an ongoing program (reviews, tabletop, incident clock), not a one-off document. |
| [ACE Cloud Hosting managed WISP](https://www.acecloudhosting.com/written-information-security-plan/) | Flat $699 custom WISP tied to their hosting brand; we are hosting-neutral and stay with the firm after the document is done, especially during an incident. |
| [ComplyAuto](https://complyauto.com/) | Strong FTC Safeguards platform but built for auto dealerships; we target tax, bookkeeping and mortgage-broker offices it does not serve. |
| [Secureframe / Vanta / Drata](https://secureframe.com/pricing) | SOC 2/ISO automation from $7,500/year that assumes engineers and cloud integrations; we are a few hundred dollars a year for firms with no IT. |
| [Local MSPs with compliance-as-a-service tooling](https://scalepad.com/controlmap/pricing) | Many tax offices have no MSP or one that does not do compliance; later we can white-label to such MSPs. |

**Differentiation:** A practitioner-delivered program priced for a 3-person tax office: tailored WISP plus a tested incident plan, yearly review and an FTC 30-day clock for the day something goes wrong. Cheaper than any compliance platform, more alive than a $699 document, and focused on the regulation these firms actually face rather than SOC 2.

## Build

- Team: 1 technical founder (delivers onboarding and tabletops, builds the small web app); no hires until about 40 clients
- Time to MVP: 1 months
- Hardest parts: Getting reportability guidance right without giving legal advice; needs careful wording and a lawyer-reviewed decision tree; Keeping delivery time per client under ~3 hours a year so services margin holds; Reaching owners through tax-season noise: selling must happen May-December; State breach-notification laws vary; v1 lists them to check rather than deciding them

## Pricing and business model

- **Model:** Productized service with a software subscription: one-time setup plus annual subscription; incident support hours billed only above an included allowance
- **Entry price:** $590 setup + $49/month (billed annually) for an office of up to 10 staff, including one tabletop and 2 hours of incident support per year
- **Rationale:** Below the $7.5k-$15k/year compliance platforms by an order of magnitude and comparable to per-seat awareness training for a small office, while recurring revenue (≈$1,180 first year) beats a one-off $699 WISP. Ten clients cover a modest founder income floor in the first quarter; 150 clients ≈ $90k ARR.

| Comparable | Price |
|---|---|
| Secureframe Fundamentals | [starting at $7,500/year](https://secureframe.com/pricing) |
| Sprinto Starter (AWS Marketplace) | [$8,500 per 12 months, up to 25 employees; audit separate](https://aws.amazon.com/marketplace/pp/prodview-upzeowcpyofas) |
| KnowBe4 Security Awareness Training | [SAT Foundation $2.40/seat/month at 25-50 seats, 3-year term](https://knowbe4.com/pricing-security-awareness-training) |
| Cyber Essentials (IASME certification fee) | [from £320 + VAT](https://www.ncsc.gov.uk/information/cyber-essentials) |

## Go to market

- **First customers:** Ten independent tax-preparation and bookkeeping offices with 1-10 staff, owner-operated, using desktop tax software and Microsoft 365, reached through the founder's contacts, local enrolled-agent and state tax-practitioner association chapters, and tax-pro forums; at least two small mortgage brokers as a second segment test.
- **Channel:** Founder-led direct sales: a free FTC 30-day deadline calculator and 20-minute 'is your WISP real?' check as top-of-funnel, webinars for practitioner associations, content on the FTC 30-day rule; later white-label to MSPs that serve accounting firms and run their clients' incidents.
- **Wedge:** The annual WISP attestation at PTIN renewal and the FTC 30-day reporting rule: a concrete deadline owners already worry about, sold off-season (May-December).

## Risks

- Bundling and price pressure: free IRS template, $49-$699 template sellers and hosting/software vendors adding WISPs may cap what owners pay; the bet is that the incident clock and live program justify a subscription.
- Liability and unauthorized-practice risk if reportability guidance is read as legal advice; requires clear disclaimers, counsel review and E&O/cyber insurance.
- Services-heavy model may not scale past ~150 clients without hiring or an MSP channel.
- Seasonality: tax offices are unreachable January-April, shrinking the selling window.
- Regulatory: enforcement intensity of the Safeguards Rule against tiny firms is uncertain; low perceived enforcement weakens urgency.

## Riskiest assumption

- **Assumption:** Small tax and bookkeeping offices that already have a template WISP will pay a recurring fee (≈$50/month) for a tailored, tested program and incident-reporting help, rather than a one-off document.
- **Cheap test:** Run a landing page and offer at two practitioner-association meetings or newsletters plus 50 direct emails to local offices, offering the setup+subscription with a refundable $100 deposit; do 10 discovery calls asking what they did after their last suspicious email or lost laptop.
- **Success signal:** At least 5 paid deposits (or 3 signed annual agreements) within 2 weeks, and at least 6 of 10 interviewees saying they would not know whether or when to report to the FTC.

## Open questions

- How many small non-bank firms have actually reported to the FTC since May 2024, and is enforcement reaching sub-20-person offices?
- Will cyber insurers or tax-software vendors refer or subsidize the program?
- Can the founder legally act as an outsourced 'Qualified Individual', and what insurance is needed?
- What share of offices already have an MSP that would rather resell this than compete with it?
- Should small SEC-registered advisers (Reg S-P smaller-entity compliance date 3 June 2026, 30-day customer notice) be the second segment after tax offices, and how much of the program carries over?
- How often does the cyber insurer's breach coach take over the incident, and should the product hand off to it rather than compete?

