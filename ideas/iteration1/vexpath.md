# VEXpath

> Self-hostable VEX decision engine for embedded device makers: turns Yocto build data, vendor CSAF and Dependency-Track findings into signed, evidence-backed per-release VEX.

Opening `cra-sbom-vex` (priority 1) · from Dependency context for vulnerability impact (theme 14, stability 0.73), CycloneDX SBOM output and attestation (theme 11, stability 1.0)

## Buyer and user

- **Buyer:** Head of product security / PSIRT lead; at smaller firms the VP Engineering or the quality/regulatory manager who owns CRA — EU-selling connected-device and industrial-equipment makers with 50-1,000 employees and 3-30 product lines whose firmware is built on Yocto/OpenEmbedded or another embedded Linux, already producing SBOMs and running self-hosted Dependency-Track or OE cve-check, and facing downstream OEM/operator requests for vulnerability status before CRA reporting (since 11 Sep 2026) and main obligations (11 Dec 2027). Software-only vendors on enterprise distros are a secondary segment.
- **User:** Product security engineers and firmware/release engineers who triage SBOM vulnerability findings per firmware release, record 'not affected' justifications, and hand machine-readable status to customers.

## Problem

Device makers can now produce SBOMs, but cannot cheaply turn them into defensible answers to 'is this shipped firmware release affected?'. Scanners flag every CVE without dependency-path, container or build context, vendor CSAF advisories can't be matched, and BOM and VEX drift apart. Embedded teams hold the evidence (patches, kernel config, CVE_STATUS) in their build, not in their triage tool. Commercial platforms that bridge this are quote-only or $18k+ per year.

- Dependency-Track users ask for CSAF advisory ingestion because CPE is not granular enough to tell which part of a vendor product (e.g. RHEL) is affected. ([source](https://github.com/DependencyTrack/dependency-track/issues/2353))
- Users ask to show the parent (root) dependency through which a vulnerable component is pulled in, so impact can be judged. ([source](https://github.com/ICTU/quality-time/issues/8687))
- Teams analysing Trivy-Operator SBOMs in Dependency-Track cannot associate findings with the container they came from. ([source](https://github.com/takumakume/sbomreport-to-dependencytrack/issues/11))
- Some vulnerabilities only apply when a dependency is direct rather than transitive, so SBOMs need dependency hierarchy to judge exposure. ([source](https://github.com/oracle/graal/issues/7729))
- Dependency-Track manages BOM and VEX as separate entities, forcing a multi-step, wait-and-poll automation to keep them in sync. ([source](https://github.com/DependencyTrack/dependency-track/issues/1872))
- Maintainers want a standard way to tell downstream users how an upstream advisory impacts their crate/binaries. ([source](https://github.com/rustsec/rustsec/issues/505))
- SBOM-based vulnerability management yields noisy results and VEX workflows to suppress false positives remain immature. ([source](https://arxiv.org/html/2511.20313))
- Commercial SBOM management with VEX is sold as annual contracts of $18,000 (10 active developers) to $100,000 (100). ([source](https://aws.amazon.com/marketplace/pp/prodview-n6mc7symiq2rm))

## Why now

CRA reporting obligations have applied since 11 September 2026 (24h early warning and 72h notification once a manufacturer becomes aware of an actively exploited vulnerability in its product), and main obligations apply from 11 December 2027. Article 14(8) asks manufacturers to inform impacted users, where appropriate, in a structured, machine-readable format, which VEX/CSAF satisfies; the CRA itself mandates neither format. Germany's BSI TR-03183 gives SBOM and vulnerability-report guidance aimed at less mature manufacturers. Tooling has also matured enough to build on: Dependency-Track 5.1 now exports component-level VEX and mirrors CISA/EU KEV, and OpenEmbedded's vex class emits build-time vulnerability status (CVE_STATUS) per image, but nothing joins the two into reviewed, per-release decisions. [1](https://commission.europa.eu/news-and-media/news/safer-and-more-secure-digital-products-2026-09-11_en) [2](https://www.bsi.bund.de/EN/Themen/Unternehmen-und-Organisationen/Standards-und-Zertifizierung/Technische-Richtlinien/TR-nach-Thema-sortiert/tr03183/TR-03183_node.html) [3](https://prighter.com/resources/laws/cyber-resilience-act/articles/article-14) [4](https://dependencytrack.org/news/dependency-track-5-1) [5](https://raw.githubusercontent.com/openembedded/openembedded-core/master/meta/classes/vex.bbclass)

## MVP

- **Per-release ingest from Dependency-Track (API) or CycloneDX/SPDX upload, plus OpenEmbedded build artefacts (vex.bbclass image JSON with CVE_STATUS, applied patches, kernel .config), with dependency path and container/image of origin per finding.** — Brings the build-time evidence embedded teams already have next to the findings, and keeps their scanners and Dependency-Track.
- **Evidence rules that propose (never apply) VEX statuses, each with its proof attached: CVE_STATUS patched/not-applicable, kernel option disabled (code_not_present), fixed upstream version, Red Hat CSAF VEX matched through a binary-to-source-RPM mapping, other vendor CSAF only where it carries PURLs. KEV listing raises queue priority only.** — Cuts noise on embedded stacks where vendor CSAF is absent, and makes every suggestion auditable rather than a black-box match.
- **Decision ledger: per release, affected / not_affected / fixed / under_investigation with CISA justification, mandatory named reviewer sign-off, a record of which suggestions were automated, and conservative invalidation (any change to component version, dependency path or build-config hash re-opens an inherited decision).** — Reuse across releases is where small teams save time; invalidation makes reuse safe for documents customers and authorities rely on.
- **Write-back and export: push decisions into Dependency-Track's analysis so DT stays the team's source of truth, and export CycloneDX VEX and CSAF 2.0 VEX matched to the release SBOM, signed with the customer's own key, for publishing on the customer's site, sbomify or a CRA suite. Private by default; nothing is published by VEXpath.** — Fixes BOM/VEX drift and avoids a second triage tool, while leaving publication and disclosure timing with the manufacturer.

Out of scope for v1: Hosted customer advisory portal / CSAF trusted-provider hosting (export only; partner with sbomify or CRA suites); Article 14 reporting workflow and ENISA Single Reporting Platform submission (left to CRA suites such as CVD Portal; we export a status summary they can use); SBOM generation, binary/firmware analysis and code-level reachability (integrate Syft, Trivy, cdxgen, OE; leave binaries to ONEKEY/Finite State); Multi-tenant SaaS: v1 ships as a self-hosted container next to Dependency-Track; EU single-tenant hosting only for design partners; Licence compliance, conformity assessment and technical-file authoring; any claim of CRA conformity.

## Competition

| Competitor | How we differ |
|---|---|
| [OWASP Dependency-Track 5.1 (free, self-hosted)](https://dependencytrack.org/news/dependency-track-5-1) | 5.1 added component-level VEX export/import and KEV, and CSAF mirroring is in funded development. We build on it, writing decisions back into DT, and add what it doesn't plan: build-config evidence from Yocto, safe cross-release invalidation, customer-key signing. If DT ships CSAF matching we consume it. |
| [OpenEmbedded/Yocto vex class and cve-check (free)](https://raw.githubusercontent.com/openembedded/openembedded-core/master/meta/classes/vex.bbclass) | Emits build-time CVE status per image but no triage workflow, review, cross-release ledger or CycloneDX/CSAF VEX tied to the shipped SBOM. We are its consumer, not its replacement. |
| [SecObserve (free, open source)](https://secobserve.github.io/SecObserve/integrations/vex) | A capable general vulnerability-management tool with CSAF/CycloneDX/OpenVEX import-export per product and branch. It is another source of truth beside DT and has no embedded build evidence or invalidation rules; we target teams that want to stay in DT. |
| [AboutCode DejaCode / CRAVEX (free, open source)](https://aboutcode.org/docs/getting_started/cravex/) | SME-oriented CRA/SBOM+VEX application centred on product and licence inventory. We specialise in evidence-backed triage on embedded firmware and offer a supported commercial licence. |
| [Self-serve CRA suites: CVD Portal, CRA Evidence, CRA-Ready](https://cvdportal.com/pricing) | They sell the whole CRA process (Art. 14 reporting, SBOM registry, CSAF export, conformity) from EUR 1,188/yr. Their VEX is manual authoring on SBOM-level findings. We are the triage engine that feeds them, sold beside them, not instead. |
| [sbomify](https://sbomify.com/pricing/) | SBOM hub with DT/OSV scanning, CRA wizard and trust center at $159/month. It owns publishing; we own the decision before it. Integration target first, rival if it adds triage. |
| [Interlynk, Anchore Enterprise, ArmorCode, Manifest, Cybeats](https://aws.amazon.com/marketplace/pp/prodview-n6mc7symiq2rm) | Enterprise SBOM/VEX platforms from $18k-$50k/yr or quote-only, SaaS-first and priced per developer or deal. We are self-hosted, per product, with public pricing for mid-size firmware teams. |
| [Finite State / ONEKEY](https://finitestate.io/sbom-management) | Binary/firmware analysis with exploit context, quote-only. Complementary: we take their or any scanner's findings and manage per-release decisions. |

**Differentiation:** VEXpath is a triage engine, not another CRA suite or SBOM hub. It runs next to the Dependency-Track a device maker already has, reads the evidence that lives in its Yocto build, proposes VEX statuses with proof attached, re-opens decisions when a release changes, and hands signed VEX to whatever publishes it. Free tools hold findings; suites hold paperwork; enterprise platforms cost $18k+. Nobody affordable turns embedded build evidence into reviewed VEX.

## Build

- Team: 2 engineers (one embedded Linux/Yocto, one with CycloneDX/CSAF and Dependency-Track API experience) + 1 founder-seller with product-security/PSIRT background
- Time to MVP: 6 months
- Hardest parts: Reading build evidence reliably across Yocto releases and BSP layers (CVE_STATUS reasons, patch metadata, kernel config to CVE mapping) and tying it to scanner PURLs; Vendor CSAF matching where it exists: Red Hat VEX identifies source RPMs (arch=src) while scanners list binary RPMs, and its format changed in 2026; most other vendor CSAF (e.g. Siemens) has no PURLs; A conservative, tested invalidation rule for inherited decisions so a stale not_affected is never exported; Two-way sync with Dependency-Track analysis state without conflicts or overwriting analysts' work; Shipping a self-hosted product (upgrades, offline vulnerability data, customer-key signing) that small teams can run

## Pricing and business model

- **Model:** Annual licence per product line (one firmware/product family with its maintained release branches; defined by SBOM project root), unlimited users, self-hosted container; EU single-tenant hosting as a paid option. Quoted in EUR excl. VAT.
- **Entry price:** EUR 290/month billed annually (EUR 3,480/year) for up to 5 product lines, self-hosted; EUR 49 per additional product line per month with no tier cap; EU single-tenant hosting +EUR 150/month
- **Rationale:** Priced as an add-on beside a EUR 1,188-3,588 CRA suite or a $159/month SBOM hub, not as a replacement for them, so the whole CRA stack stays well under Interlynk's smallest $18k contract and within card or grant-funded budgets. Self-hosting removes multi-tenant hosting cost. Uncapped per-product pricing lets revenue grow with portfolios. The low ACV only works with product-led and partner-led acquisition; founder-led selling is reserved for ten design partners.

| Comparable | Price |
|---|---|
| sbomify Business | [$159/month billed annually ($199 billed monthly)](https://sbomify.com/pricing/) |
| Interlynk (AWS SBOM Manager SaaS) | [$18,000/year (10 active developers) to $100,000/year (100)](https://aws.amazon.com/marketplace/pp/prodview-n6mc7symiq2rm) |
| Anchore Enterprise | [$34,500 (Cloud Image) to $50,000 (Helm) per 12 months, plus $15,000 Essential support plan](https://aws.amazon.com/marketplace/pp/prodview-ilkug4gdyavdq) |
| Docker Scout Team | [$9 per repo/month](https://www.docker.com/?p=40309) |

## Go to market

- **First customers:** Ten EU (DACH/Nordics/Benelux first) industrial-automation, building-tech and IoT makers with 50-500 staff, firmware on Yocto/embedded Linux, already running Dependency-Track or OE cve-check, with a named CRA owner and at least one downstream OEM or operator asking for vulnerability status or VEX. Signed as paid design partners with a data-handling agreement.
- **Channel:** Product-led through an Apache-licensed 'oe-vex-to-dependency-track' importer published in the Yocto/OpenEmbedded and Dependency-Track communities, with self-serve trial and card/online-quote purchase; integrations and referral margin with CRA suites and SBOM hubs (CVD Portal, sbomify) and embedded-Linux/CRA consultancies who resell; founder-led sales only for the design partners. No notified bodies (independence).
- **Wedge:** The free importer pushes the build's own CVE_STATUS into Dependency-Track and reports how many findings remain open. The paid engine then works the remainder (kernel config, patches, vendor CSAF, invalidation, signed export) and shows the additional cut, with evidence, on the buyer's own data.

## Risks

- Bundling: Dependency-Track 5.1 already exports component-level VEX and tracks KEV, CSAF ingestion is funded and in progress, and OpenEmbedded already emits build-time VEX. If DT adds matching and better OE import, our value narrows to evidence rules, invalidation and signing; we build on DT and contribute upstream rather than compete with it.
- Crowding: free SecObserve and DejaCode/CRAVEX cover VEX authoring, and cheap CRA suites (CVD Portal from EUR 1,188/yr, CRA Evidence, CRA-Ready, sbomify) list VEX or CSAF export. Buyers may see VEX as a suite checkbox; we win only if triage depth on embedded firmware visibly saves engineer time, or through partner distribution. Funded enterprise vendors could also add a self-serve tier.
- Weak, late demand and costly acquisition: problem evidence is developer feature requests, not buyer budgets; the CRA mandates neither VEX nor CSAF; many makers will wait for an OEM customer or December 2027; and a EUR 3.5k ACV cannot carry multi-stakeholder Mittelstand sales, so product-led and partner channels must work or CAC payback fails.
- Technical: the noise cut on embedded stacks is unproven; vendor CSAF is sparse or lacks PURLs, Red Hat changed its VEX format in 2026, and build-evidence rules may resolve fewer findings than the demo suggests.
- Liability and data custody: a wrong exported not_affected can tell operators not to patch. Mitigations are mandatory human sign-off, logged automation, customer-key signing, contractual liability caps and professional-indemnity insurance, but EU product-liability rules for software may limit contractual caps. Hosted customers will require EU hosting and ISO 27001; self-hosting reduces but does not remove this.
- Regulatory: harmonised standards and ENISA formats are not final and may not reference VEX/CSAF; marketing must sell Art. 14(8) machine-readable user information and customer demand, never conformity.

## Riskiest assumption

- **Assumption:** On real Yocto/embedded-Linux firmware SBOMs, evidence rules resolve a large share of the findings that Dependency-Track 5.1 plus OpenEmbedded's own CVE_STATUS leave open, without wrong not_affected calls, and that saving is worth EUR 290/month to mid-size device makers.
- **Cheap test:** In 2 weeks, without building the product: (a) from 15 discovery calls with CRA owners at 50-500-person EU device makers (sourced via Yocto/OE and Dependency-Track communities and a CRA consultancy), collect 5 firmware SBOM + build-artefact sets under NDA, processed on the prospect's premises or an isolated laptop; apply the rules by hand with scripts and have the prospect's engineer review every not_affected; (b) at the end of each call show the result or a mock and ask for a paid design-partner LOI at the entry price.
- **Success signal:** In at least 3 of 5 data sets, 30%+ of findings left open after DT 5.1 + CVE_STATUS are resolved with documented evidence and zero wrong not_affected on review; and at least 4 of 15 sign a LOI at EUR 290/month or more, with at least 3 accepting self-hosted deployment and naming who approves the spend.

## Open questions

- Do CRA harmonised standards, market surveillance authorities or downstream OEMs expect VEX/CSAF specifically, or will any documented vulnerability handling do?
- How much of the residual noise on typical Yocto/RTOS firmware is resolvable from build evidence versus needing reachability or binary analysis?
- Will Dependency-Track's CSAF work (#2353) include matching, and on what timeline; could VEXpath contribute it or be the reference integration?
- Will CVD Portal, sbomify or similar suites integrate or resell a triage engine, or build VEX triage themselves?
- How many EU device makers fit the profile (50-1,000 staff, embedded Linux, SBOMs, a named CRA owner)? Likely a few thousand; needs sizing from industry-association data.
- Who owns the budget in a 200-person device maker: product security, quality/regulatory or engineering; and can it be bought on a card or via SECURE grant funding?
- Do the top vendor CSAF trusted providers' terms allow commercial ingestion and matching (we link rather than republish)?
- Is the per-product-line unit (SBOM project root) clear enough to avoid tier disputes?

