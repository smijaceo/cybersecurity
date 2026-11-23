# VEXpath

> Hosted SBOM impact and VEX/CSAF workbench that tells mid-size product makers which CVEs actually affect each shipped release, priced for CRA compliance.

Opening `cra-sbom-vex` (priority 1) · from Dependency context for vulnerability impact (theme 14, stability 0.73), CycloneDX SBOM output and attestation (theme 11, stability 1.0)

## Buyer and user

- **Buyer:** Head of product security / PSIRT lead (often the VP Engineering or quality/regulatory manager at smaller firms) — EU-selling software vendors and connected-device / industrial equipment makers with 50-1,000 employees and 3-30 product lines; already generating SBOMs (Syft, CycloneDX plugins, Trivy) and often running self-hosted Dependency-Track, but with no answer for publishing VEX/CSAF advisories and documenting vulnerability handling before CRA reporting (since 11 Sep 2026) and main obligations (11 Dec 2027).
- **User:** Product security engineers and release/firmware engineers who triage SBOM vulnerability findings per release, write 'not affected' justifications, and publish customer-facing advisories.

## Problem

Mid-size manufacturers can now produce SBOMs, but cannot cheaply turn them into defensible answers to 'is our shipped release affected?'. Free Dependency-Track flags every CVE without parent-component, container or vendor-advisory context, cannot ingest vendor CSAF advisories, and treats BOM and VEX as separate uploads. Commercial platforms that do this are quote-only or $18k-$50k+ per year. Under the CRA, teams must handle vulnerabilities per product and report exploited ones within 24 hours, so noisy, unexplained findings become a compliance cost.

- Dependency-Track users ask for CSAF advisory ingestion because CPE is not granular enough to tell which part of a vendor product (e.g. RHEL) is affected. ([source](https://github.com/DependencyTrack/dependency-track/issues/2353))
- Users ask to show the parent (root) dependency through which a vulnerable component is pulled in, so impact can be judged. ([source](https://github.com/ICTU/quality-time/issues/8687))
- Teams analysing Trivy-Operator SBOMs in Dependency-Track cannot associate findings with the container they came from. ([source](https://github.com/takumakume/sbomreport-to-dependencytrack/issues/11))
- Some vulnerabilities only apply when a dependency is direct rather than transitive, so SBOMs need dependency hierarchy to judge exposure. ([source](https://github.com/oracle/graal/issues/7729))
- Dependency-Track manages BOM and VEX as separate entities, forcing a multi-step, wait-and-poll automation to keep them in sync. ([source](https://github.com/DependencyTrack/dependency-track/issues/1872))
- Maintainers want a standard way to tell downstream users how an upstream advisory impacts their crate/binaries. ([source](https://github.com/rustsec/rustsec/issues/505))
- SBOM-based vulnerability management yields noisy results and VEX workflows to suppress false positives remain immature. ([source](https://arxiv.org/html/2511.20313))
- Commercial SBOM management with VEX is sold as annual contracts of $18,000 (10 active developers) to $100,000 (100). ([source](https://aws.amazon.com/marketplace/pp/prodview-n6mc7symiq2rm))

## Why now

The EU Cyber Resilience Act's reporting obligations applied from 11 September 2026: manufacturers must send an early warning within 24 hours and a notification within 72 hours for actively exploited vulnerabilities, for all products on the EU market including those already sold. Its main obligations apply from 11 December 2027, leaving roughly a year to put vulnerability handling in place. Germany's BSI already publishes TR-03183 guidance, with a dedicated SBOM part (v2.1.0, with CycloneDX/SPDX field mapping) and a vulnerability reports part, aimed at manufacturers without mature security processes - exactly this buyer. [1](https://commission.europa.eu/news-and-media/news/safer-and-more-secure-digital-products-2026-09-11_en) [2](https://www.bsi.bund.de/EN/Themen/Unternehmen-und-Organisationen/Standards-und-Zertifizierung/Technische-Richtlinien/TR-nach-Thema-sortiert/tr03183/TR-03183_node.html)

## MVP

- **Per-release SBOM ingest (CycloneDX/SPDX via CI action or API, plus import from an existing Dependency-Track instance) with full dependency-path view: root component, direct vs transitive, container/image of origin.** — Gives the parent-component and container context users ask Dependency-Track for, and keeps teams' existing scanners and DT investment.
- **Vendor CSAF advisory ingestion (Red Hat, Oracle, Siemens and other CSAF trusted providers) matched to SBOM components by PURL, overriding CPE-level false matches.** — The most-engaged unmet request in the input; directly removes noise for device makers built on commercial distros.
- **VEX triage workbench: queue of findings per release, status (affected / not_affected / fixed / under_investigation) with CISA-style justification picker, inherit-decision-across-releases, and reviewer sign-off.** — Turns noisy findings into recorded decisions; reuse across releases is where small teams save time.
- **Atomic publishing: export a release's SBOM plus matching CycloneDX VEX and CSAF 2.0 VEX/advisory documents, signed, to a hosted customer portal or the vendor's own site.** — Solves the BOM/VEX sync problem and gives customers and authorities a machine-readable answer.
- **CRA evidence pack: per product, a timestamped log of vulnerabilities, decisions and fix releases, plus a 24h/72h exploited-vulnerability draft triggered by a KEV listing.** — Maps the work to the compliance deadline the buyer is paying to meet.

Out of scope for v1: SBOM generation and binary/firmware analysis (integrate Syft, Trivy, cdxgen; leave binaries to ONEKEY/Finite State); Code-level reachability analysis; Direct submission to the ENISA Single Reporting Platform (drafts only until its API is stable); Licence compliance, full CRA conformity assessment and technical-file authoring; On-premise deployment.

## Competition

| Competitor | How we differ |
|---|---|
| [OWASP Dependency-Track (free, self-hosted)](https://github.com/DependencyTrack/dependency-track) | We import from it rather than replace it, and add what it lacks: vendor CSAF matching, parent/container context, atomic SBOM+VEX publishing, hosting and support. |
| [sbomify](https://sbomify.com/pricing/) | sbomify is an SBOM publishing hub and trust center with a CRA wizard, scanning via OSV/Dependency-Track. We focus on the triage step before publishing: impact analysis, CSAF matching and VEX authoring. Likely partner or acquirer as much as rival. |
| [Interlynk (SBOM Manager on AWS Marketplace)](https://aws.amazon.com/marketplace/pp/prodview-n6mc7symiq2rm) | Interlynk prices by active developers from $18k/year. We price per product with public self-serve pricing well under that, for teams with few developers per product line. |
| [Anchore Enterprise](https://anchore.com/pricing/) | Anchore is a scanning and policy platform at $34.5k-$50k/year plus support. We don't scan; we sit on any scanner's output and specialise in VEX/CSAF and CRA evidence. |
| [Manifest / Cybeats SBOM Studio / Finite State](https://finitestate.io/sbom-management) | Quote-only enterprise platforms aimed at large medical and connected-device makers. We serve the mid-size tail they don't sell to, with self-serve onboarding. |
| [Bundled cloud/registry SBOM features (AWS Inspector SBOM export, Docker Scout, GitHub attestations, JFrog Xray)](https://docs.aws.amazon.com/inspector/latest/user/sbom-export.html) | They generate or attach SBOMs inside one platform. None produces cross-vendor, per-release VEX/CSAF decisions for customers and regulators. |

**Differentiation:** VEXpath is the only option priced and built for a mid-size manufacturer's real job: deciding, per shipped release, which CVEs matter and publishing that decision as VEX/CSAF. It keeps existing scanners and Dependency-Track, adds vendor-CSAF matching and dependency-path context to cut noise, and prices per product with self-serve onboarding, between free tools and $18k-$50k quote-led platforms.

## Build

- Team: 2 engineers (one with CycloneDX/CSAF standards experience) + 1 founder-seller with product-security/PSIRT background
- Time to MVP: 5 months
- Hardest parts: Reliable PURL matching between SBOM components and vendor CSAF product trees, which use inconsistent product identifiers; Carrying VEX decisions across releases safely: knowing when a dependency-path change invalidates an earlier 'not_affected'; Normalising messy real-world SBOMs (missing dependency graphs, mixed CycloneDX/SPDX versions, container layers); Keeping pace with CRA harmonised standards and ENISA reporting-platform formats that are still being finalised

## Pricing and business model

- **Model:** Annual SaaS subscription per product line (a product with its supported release branches), unlimited users; tiers by product count
- **Entry price:** $490/month billed annually (~$5,900/year) for up to 5 products; $1,490/month for up to 25 products
- **Rationale:** Per-product pricing matches how CRA obligations attach (per product) and how mid-size makers think about cost, unlike per-developer pricing that punishes small firmware teams. The entry tier sits about 3x above sbomify Business, justified by triage and CSAF matching rather than publishing alone, and at roughly a third of Interlynk's smallest $18k contract, low enough for a team-lead card or a small purchase order without procurement.

| Comparable | Price |
|---|---|
| sbomify Business | [$159/month billed annually ($199 billed monthly)](https://sbomify.com/pricing/) |
| Interlynk (AWS SBOM Manager SaaS) | [$18,000/year (10 active developers) to $100,000/year (100)](https://aws.amazon.com/marketplace/pp/prodview-n6mc7symiq2rm) |
| Anchore Enterprise | [$34,500 (Cloud Image) to $50,000 (Helm) per 12 months, plus $15,000 Essential support plan](https://aws.amazon.com/marketplace/pp/prodview-ilkug4gdyavdq) |
| Docker Scout Team | [$9 per repo/month](https://www.docker.com/?p=40309) |

## Go to market

- **First customers:** Ten EU (DACH/Nordics/Benelux first) industrial-automation, building-tech and IoT makers and B2B software vendors with 50-500 staff, already running Dependency-Track or Trivy, with a named person newly responsible for CRA, and with downstream OEM customers already requesting SBOM/VEX.
- **Channel:** Founder-led sales into the Dependency-Track and CycloneDX communities (an open-source CSAF-to-Dependency-Track bridge as lead magnet), CRA webinars with industry associations (e.g. ZVEI, VDMA) and partnerships with CRA consultancies and notified bodies who need a tool to recommend.
- **Wedge:** Free 'VEX in a day' import: connect an existing Dependency-Track instance, auto-resolve findings using vendor CSAF advisories, and show the noise cut (e.g. '412 findings to 37 that need a decision') before asking for payment.

## Risks

- Crowding from below and above: sbomify already offers a CRA wizard and Dependency-Track scanning at $159/month, and funded vendors (Anchore, Interlynk, Manifest, ArmorCode) can add self-serve tiers as CRA demand grows.
- Bundling: Dependency-Track may add CSAF ingestion and atomic BOM+VEX upload (both are open feature requests), and SCA suites or GitHub could ship VEX authoring, removing the core noise-reduction story.
- Deadline-driven demand: many mid-size makers may defer spending until late 2027 or until a customer or market surveillance authority forces it, giving lumpy, late revenue.
- Regulatory uncertainty: CRA harmonised standards and ENISA platform formats are not final; if they don't require VEX/CSAF specifically, the compliance hook weakens to 'nice to have'.
- Technical: vendor CSAF coverage is uneven outside large vendors (Red Hat, Oracle, Siemens), so noise reduction may be much smaller for typical embedded stacks than the demo suggests.
- Liability: customers relying on our 'not_affected' auto-suggestions in regulator-facing documents could blame us for wrong calls; decisions must stay human-signed.

## Riskiest assumption

- **Assumption:** Mid-size EU manufacturers will pay ~$6k/year now (before December 2027) for VEX/CSAF triage on top of free Dependency-Track, rather than living with noise or buying a cheaper publishing tool like sbomify.
- **Cheap test:** Over 2 weeks, run 15 discovery calls with CRA owners at 50-500-person EU device/software makers sourced from Dependency-Track/CycloneDX community channels and an industry-association CRA webinar; show a clickable mock and one manual 'noise cut' on their own exported Dependency-Track findings, then ask for a paid pilot letter of intent at the entry price.
- **Success signal:** At least 4 of 15 sign a pilot LOI at $490/month or more, and at least 8 confirm an existing VEX/advisory request from a customer or a named budget for CRA tooling before end of 2027.

## Open questions

- Do CRA harmonised standards or market surveillance authorities expect VEX/CSAF specifically, or will any documented vulnerability handling do?
- How much does vendor CSAF matching actually cut findings on typical embedded Linux / RTOS stacks versus enterprise distros?
- Does sbomify (or another SBOM hub) already plan VEX authoring, making it a competitor rather than a partner?
- Are Dependency-Track's CSAF (#2353) and atomic BOM+VEX (#1872) requests still open, and on its roadmap?
- Who owns the budget in a 200-person device maker: product security, quality/regulatory or engineering?
- Is per-product pricing understood by buyers, given how product lines and release branches vary?

