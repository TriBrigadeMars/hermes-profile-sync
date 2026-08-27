---
name: public-health-evaluation-planning
description: "Design public health evaluation plans using CDC framework."
version: 0.1.0
author: Mars Cruz, Hermes Agent
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [public-health, evaluation, mixed-methods, clinical-trials, CDC-framework, program-evaluation]
    related_skills: [research-question-framer, grounded-citations, study-protocol-builder, research-design-orchestrator, qualitative-literature-review, apa-7-style-agent, docx]
---

# Public Health Evaluation Planning

Designs rigorous public health evaluation plans and research methodologies by synthesizing four authoritative frameworks: CDC's Program Evaluation Framework (2011/2024), Creswell's Mixed Methods Research (2nd Ed), Shih & Aisner's Clinical Trial Statistical Design (2nd Ed), and the CDC Evaluation Framework Action Guide (2026). Produces evaluation plans, logic models, methodology sections, and study designs grounded in these sources.

## When to Use

- User asks to design a program evaluation plan for a public health program
- User needs a logic model or theory of change for a health intervention
- User wants to choose between quantitative, qualitative, or mixed methods designs
- User needs help writing an evaluation purpose statement, aims, or research questions
- User asks about CDC's 6-step evaluation framework or how to apply it
- User needs guidance on clinical trial design, sample size, or statistical methodology
- User wants to embed mixed methods into an experiment, evaluation, or case study
- User asks about integration strategies (convergent, sequential, complex designs)
- User needs help with data collection methods, indicators, or evaluation matrices
- User asks about quality standards for mixed methods or evaluation studies

**Don't use for:** Pure literature reviews without evaluation design, non-health research methodology, or statistical analysis execution (use specific stats tools instead).

## Source Frameworks

### 0. California Tobacco Control Evaluation Center (TCEC) — State-Specific Layer

When evaluating **California tobacco control programs** (or programs funded by CTCP), overlay TCEC resources onto the CDC framework. TCEC provides standardized instruments, methods, and reporting expectations specific to California's 61 local lead agencies.

**Key TCEC Resources:**
- **Tobacco Purchase Surveys:** LATPS (post-sales-ban compliance), LAFTPS (flavored tobacco sales), YATPS (underage access via young adult secret shoppers) — standardized retail evaluation methods
- **Coalition Instruments:** Member Intake Form, Annual Satisfaction Survey, Youth Coalition Satisfaction Survey, Diversity Matrix, Asset Mapping — standardized coalition functioning assessment
- **Priority Population Data:** Publicly available datasets by race/ethnicity, LGBTQ+, income, mental health status, rural communities — for equity-disaggregated analysis
- **Participatory Data Analysis ("Data Parties"):** Community co-interpretation of findings — strengthens cultural humility and increases evaluation use
- **Evaluation Plan Types:** CTCP taxonomy — legislated/voluntary policy adoption, individual behavior change, other with/without measurable outcome
- **End-Use Strategizing:** Design evaluation methods with ultimate data use in mind; TCEC provides instrument templates for SHS, retail, community engagement, media, MUH, photovoice, policy record reviews
- **Process vs. Outcome Framework:** ALL CTCP objectives benefit from process evaluation; TCEC provides activity menus with timing guidance (pre/during/post-intervention)
- **Instrument ESSENTIALS:** Pre-validated instruments for coalitions, secondhand smoke, retail, community engagement, media, demographic questions
- **Tobacco Evaluator Alliance (TEA):** Peer network for evaluator peer review and benchmarking

**TCEC Website:** https://tobaccoeval.ucdavis.edu/evaluation-guide

**When to activate this layer:** Program is in California, funded by CTCP, or tobacco-control-specific. Otherwise, use CDC framework alone.

### 0b. International / East Asian Evaluation Traditions

When evaluating programs outside the US, comparing methodologies internationally, or when the user asks how efficacy is assessed in China/Korea/Hong Kong/Singapore, activate this layer.

**Attribution Logic by System:**
| System | Primary Question Asked | Evaluation Driver |
|--------|----------------------|-------------------|
| US/CDC | "Did the program cause change?" | Stakeholder utility + federal standards |
| China | "Were targets met?" | Central plan targets + cadre accountability |
| South Korea | "Did national indicators move?" | KHPI dashboards + standardized indicators |
| Hong Kong | "Did the policy change population behavior?" | Academic-led whole-population pre/post studies |
| Singapore | "Is this worth the money?" | Health technology assessment (HTA), cost-effectiveness/QALY |

**Methodological Profiles:**
- **China:** Top-down target responsibility system; heavy reliance on routine administrative reporting through China CDC hierarchy (upward data-smoothing risk); cross-sectional prevalence surveys dominate (GATS China); policy adoption evaluated as directive compliance, not community diffusion.
- **South Korea:** Quasi-governmental intermediary model structurally similar to CA (KHPI ≈ CTCP/TCEC); KNHANES + annual Community Health Survey backbone; single-payer claims data enables natural-experiment designs (pricing/packaging policies via interrupted time series).
- **Hong Kong:** Small-jurisdiction academic-partnership model (HKU SPH + COSH); biennial Youth Smoking Survey since 2003; true population-level natural experiments (2007 smoke-free law, tax increases, 2021 pack warnings) evaluated with census-like coverage.
- **Singapore:** Most centralized/evidence-proceduralized; MOH + HPB run programs; Agency for Care Effectiveness (ACE) anchors HTA-style systematic review and economic evaluation as the central analytic frame (NICE-like logic); limited institutional home for participatory/community evaluation.

**Cross-Cutting Lessons:**
1. Recognize which question the funding context is actually asking (causation vs. accountability vs. cost-effectiveness).
2. Administrative-reporting-dependent systems carry upward data-smoothing bias — add explicit data-quality sensitivity analyses (map onto Shih & Aisner missing-data/estimands machinery).
3. Single-payer/national insurance data enables stronger designs than fragmented US systems — watch for equivalent linkages (e.g., All-Payer Claims Databases) that upgrade feasible designs.

### 0c. Domain-Specific Layers (Lightweight)

Activate the matching domain layer when the program's subject matter fits. Each entry adjusts emphasis, adds canonical frameworks/data sources, and flags domain-specific pitfalls — but the CDC 6-step backbone and Step 3b evidence grounding always apply.

**Substance Use Prevention (SAMHSA SPF):**
- Framework: Strategic Prevention Framework — Assessment → Capacity → Planning → Implementation → Evaluation (+ Sustainability woven throughout)
- Emphasis: needs assessment via epidemiological data (NSDUH, YRBS, state ED/hospital data); logic models tied to intervening variables; fidelity vs. adaptation monitoring
- Data sources: NSDUH, SAMHSA's SPARS/Block Grant reporting, state epidemiological profiles
- Pitfall: SPF requires evaluation of *consequences* (consumption patterns + consequences), not just program activities

**Chronic Disease Prevention (CDC NCCDPHP):**
- Framework: NCCDPHP's four domains — epidemiology/surveillance, environmental approaches, health system interventions, community-clinical links
- Emphasis: population reach vs. clinical reach distinction; policy/systems/environmental (PSE) change metrics; WISEWOMAN/diabetes/self-management program evaluation norms
- Data sources: BRFSS, US Diabetes Surveillance System, NPCR/USCancerStats, HEDIS measures
- Pitfall: chronic disease outcomes take years — plan intermediate indicators (clinical quality measures, PSE adoption) or the evaluation will show "no effect"

**Maternal & Child Health (MCHB / Title V):**
- Framework: Life Course Perspective; Title V National Performance Measures structure; MCH Pyramid (direct services → enabling services → population-based services → infrastructure)
- Emphasis: performance measure logic (NPM/SPM), developmental stages across life course, family-centered and culturally competent evaluation
- Data sources: PRAMS, NSCH, Title V Maternal & Child Health Block Grant data, vital records
- Pitfall: outcomes span generations — use intermediate markers (prenatal care adequacy, safe sleep counseling rates) with life-course framing

**Environmental Health (HIA-centered):**
- Framework: Health Impact Assessment (NASEM minimum elements: screening, scoping, assessment, recommendations, reporting, monitoring); also exposure-assessment logic
- Emphasis: evaluating non-health policies for health effects; quantitative exposure modeling + qualitative community input; equity analysis by proximity/vulnerability
- Data sources: EPA AirNow/EJScreen, CDC Environmental Public Health Tracking Network, state environmental registries
- Pitfall: causal chains are long and confounded (policy → exposure → dose → effect) — be explicit about which link the evaluation can actually support

**Sexual & Reproductive Health (CDC DPSD/HIV prevention):**
- Framework: CDC's Division of Reproductive Health frameworks; HIV Prevention (High-Impact Prevention; DEBIs/PRISM efficacy-to-effectiveness logic); teen pregnancy prevention (TPP) evaluation standards
- Emphasis: intervention fidelity for evidence-based curricula; sensitivity in measuring stigmatized behaviors (ACASI/audio-CASI methods); clinic-level vs. community-level outcome tiers
- Data sources: NCHS Natality, YRBS sexual behavior items, NASTAD/ATLR surveillance, Title X family planning reporting
- Pitfall: social desirability bias in self-reported sensitive behaviors — require validated private-collection methods and triangulate

**Public Health Epidemiology:**
- Framework: outbreak/field investigation logic (CDC/CSTE); descriptive → analytic progression (person/place/time → hypothesis testing)
- Emphasis: study design selection (cohort, case-control, cross-sectional, ecologic); bias/confounding/effect modification audit; causation criteria (Hill)
- Data sources: notifiable disease systems (NNDSS), registry data, epi curves and rate standardization
- Pitfall: ecologic fallacy; small-cell suppression requirements when disaggregating rare outcomes

**Public Health Administration:**
- Framework: PHAB (Public Health Accreditation Board) domains; management-by-objectives; QI/PDSA cycles
- Emphasis: organizational capacity assessment, workforce metrics (PH WINS), fiscal stewardship, accreditation documentation standards
- Data sources: PHAB documentation, workforce surveys, budget/expenditure reports, customer satisfaction
- Pitfall: evaluating administrative functions needs process measures with defensible benchmarks, not borrowed health-outcome metrics

**Public Health Surveillance:**
- Framework: surveillance system evaluation per CDC's "Updated Guidelines for Evaluating Public Health Surveillance Systems" (2001) — simplicity, flexibility, data quality, acceptability, sensitivity, predictive value positive, representativeness, timeliness, stability
- Emphasis: the nine system attributes as the evaluation rubric itself; case definition audit; capture-recapture for completeness estimation
- Data sources: NNDSS, syndromic surveillance (NSSP BioSense), sentinel systems (ILINet), registry linkage
- Pitfall: PVP and sensitivity trade off against each other — evaluate the system's *intended use* first, then judge attributes against that purpose

**Activation rule:** match on program subject matter (e.g., tobacco = chronic disease + TCEC layer both active). Multiple layers may combine. When no layer matches, proceed with CDC framework alone.

### 4b. APA Publication Manual, 7th Edition (2020) — Academic Compliance Layer

**Canonical source:** *Publication Manual of the American Psychological Association* (7th ed., 2020), verified against the full manual text. For audit/remediation workflow details, defer to the `apa-7-style-agent` skill. This layer governs what evaluation deliverables must contain to be APA 7 compliant — especially the **Journal Article Reporting Standards (JARS)** in Chapter 3.

**JARS–Mixed Reporting Standards (APA 7 Table 3.3) — apply to every mixed methods manuscript this skill produces:**

| Manuscript Section | Required Elements |
|--------------------|-------------------|
| **Title** | Identify main variables/theory AND the populations; avoid words exclusively qualitative ("explore," "understand") or quantitative ("determinants," "correlates") |
| **Abstract** | State mixed methods design type, participant/data-source types, analytic strategy, main results, major implications; consider one MM-design keyword + one problem keyword |
| **Aims/Objectives** | State THREE types of goals — quantitative, qualitative, and mixed methods — ordered to reflect the design sequence. The MM aim describes results expected from where mixing/integration occurs |
| **Method: Design Overview** | Justify why MM fits the goals; identify and DEFINE the design type (convergent, explanatory sequential, exploratory sequential); name the QUAL approach and QUAN design within it; state added value of integration |
| **Participants/Data Sources** | Separate descriptions per data strand; order by procedure sequence; use an implementation-matrix table (data type × timing × source × aims); describe sources as open- vs. closed-ended information |
| **Researcher Description** | Reflexivity statement — how researchers' backgrounds/experiences influence the research (required because MM includes qualitative work) |
| **Sampling & Recruitment** | Separate sections for QUAL and QUAN sampling/recruitment, ordered per design |
| **Data Analysis** | SEPARATE sections for QUAN analysis, QUAL analysis, and MM analysis (the integration procedures specific to the design type) |
| **Validity/Integrity** | Quantitative validity + reliability; qualitative methodological integrity; MM validity/legitimacy — quality of inferences from the intersection of strands |
| **Results** | Subsections mirror design sequence; present integrated findings via joint-display tables/graphs or data transformation |
| **Discussion** | Mirrors design sequence; reflects specifically on implications of INTEGRATED findings |

**Other Chapter 2–13 requirements carried into this skill's outputs:** five-level heading system (Table 2.3; never an "Introduction" heading); recommended verb tenses (Table 4.1 — past/literature present for reporting); statistical abbreviations per Table 6.5; exact *p* values (2–3 decimals, no *.000*); italic statistics symbols vs. non-italic Greek letters; complete reference elements (§9.25–9.27: authors, year, sentence-case title, journal title case italics, volume italics + issue + pages/article number, DOI as live link); bias-free language (Ch. 5); APA table format (Table 7.1 component structure — no vertical borders, bold Arabic number, italic title).

**When this layer activates:** any manuscript, journal submission, thesis/dissertation chapter, or formal report the user marks as academic/APA. Program-facing briefs and slide decks need only the citation-format rules.

### 1. CDC Program Evaluation Framework (2011 Self-Study Guide + 2024/2026 Action Guide)

**Six Steps:**
1. **Assess Context** (formerly Engage Stakeholders) — evaluability assessment, interest-holder mapping, place-based context, evaluation capacity, evaluator readiness
2. **Describe the Program** — logic model (inputs → activities → outputs → outcomes), narrative description, contextual factors, stage of development
3. **Focus the Evaluation Questions and Design** — purpose statement, evaluation type (formative/process/outcome/impact/economic), evaluation questions, design selection
4. **Gather Credible Evidence** — indicators, data collection methods/sources, data quality/quantity, instruments, protocols
5. **Generate and Support Conclusions** — data analysis plan, interpretation, recommendations, collaborative validation
6. **Act on Findings** — dissemination, communication strategy, follow-up, data-to-action cycles

**Cross-Cutting Actions (2024 update):**
- Engage collaboratively with interest holders
- Promote fair and just evaluation practices and outcomes
- Learn from and use insights throughout

**Evaluation Standards (Federal):**
- Relevance and Utility
- Rigor
- Independence and Objectivity
- Transparency
- Ethics

**Evaluation Types:**
| Type | Shows | When to Use |
|------|-------|-------------|
| Formative | Feasibility, appropriateness, acceptability | Before full implementation |
| Process/Implementation | Extent of implementation fidelity | During operations |
| Outcome | Achievement of intended goals | After implementation |
| Impact | Causal attribution | Comparing to counterfactual |
| Economic | Cost-effectiveness, cost-benefit | Policy/funding decisions |

### 2. Creswell Mixed Methods Research (2nd Ed, 2022)

**Definition:** A methodology where the investigator gathers both quantitative (closed-ended) and qualitative (open-ended) data, integrates the two, and draws metainferences from the integration that provide insight beyond either data type alone.

**Six Essential Characteristics:**
1. Collect and analyze both quantitative and qualitative data
2. Use rigorous quantitative and qualitative methods
3. Incorporate procedures within a mixed methods design
4. Integrate qualitative and quantitative data in the design
5. Draw metainferences from integration
6. Include a worldview and a theory

**Three Core Designs:**

| Design | Intent | Procedure | Integration |
|--------|--------|-----------|-------------|
| **Convergent** | Compare QUAN and QUAL results | Collect both simultaneously, merge, compare | Merging (side-by-side or joint display) |
| **Explanatory Sequential** | Explain QUAN results with QUAL data | QUAN first → QUAL follow-up | Connecting (QUAL explains QUAN) |
| **Exploratory Sequential** | Develop culturally sensitive measures | QUAL first → design instrument → test QUAN | Building (QUAL informs QUAN design) |

**Four Complex Designs (core designs embedded in frameworks):**
1. **Experimental/Intervention** — QUAL embedded before, during, or after a trial
2. **Participatory Action Research** — core designs threaded through social justice framework
3. **Multiple Case Study** — QUAN+QUAL data form or document cases
4. **Evaluation** — core designs embedded within evaluation phases

**Mixed Methods Questions (by design):**
- Convergent: "To what extent do the qualitative findings confirm the quantitative results?"
- Explanatory Sequential: "How do the qualitative data explain the quantitative results?"
- Exploratory Sequential: "To what extent do the qualitative findings provide a contextualized quantitative assessment?"
- Experimental: "How do the qualitative findings enhance interpretation of experimental outcomes?"
- Evaluation: "How do qualitative processes compare with quantitative outcomes?"

**Purpose Statement Script (Convergent):**
> In this study, [quantitative data] will be used to test the theory of [theory] that predicts that [IVs] will [direction] influence the [DVs] for [participants] at [site]. The [qualitative data type] will explore [central phenomenon] for [participants] at [site]. Both types of data will be merged for a complete understanding of the research problem.

**Purpose Statement Script (Explanatory Sequential):**
> This study will address [content aim]. An explanatory sequential mixed methods design will be used, involving collecting quantitative data first and then explaining the quantitative results with in-depth qualitative data. In the first phase, [instrument] data will be collected from [participants] at [site] to test [theory] to assess whether [IVs] relate to [DVs]. The second phase will explore [central phenomenon] with [participants] to understand surprising or contradictory quantitative results.

**Integration Intent & Procedures:**

| Design | Intent | Procedure |
|--------|--------|-----------|
| Convergent | Compare/match results | Merge side-by-side in joint display |
| Explanatory Sequential | Explain surprising results | Connect QUAL collection to QUAN results |
| Exploratory Sequential | Enhance cultural specificity | Build QUAN assessment from QUAL findings |
| Complex | Enhance framework/process | Embed QUAN+QUAL into framework |

**Joint Display Template (Convergent):**

| Quantitative Scores | Theme 1 | Theme 2 | Theme 3 | Theme 4 | Inferences |
|---------------------|---------|---------|---------|---------|------------|
| High | Quote | Quote | Quote | Quote | Insight |
| Medium | Quote | Quote | Quote | Quote | Insight |
| Low | Quote | Quote | Quote | Quote | Insight |
| **Inferences** | Insight | Insight | Insight | Insight | **Metainferences** |

**Quality Standards (Creswell's checklist):**
- Abstract mentions specific mixed methods design
- Title is neutral (not QUAN or QUAL flavored)
- Problem cites need for both data types
- Aims include QUAN, QUAL, and mixed methods statements
- Design identified, defined, and diagrammed
- Philosophy and theory positioned
- Sampling discussed for QUAN, QUAL, and mixed methods
- Data analysis has separate QUAN, QUAL, and integration sections
- Joint display included for integration results
- Metainferences drawn from integration
- Value of mixed methods stated explicitly
- Validity addressed for QUAN, QUAL, and the design
- Ethical issues identified for each component

### 3. Shih & Aisner — Clinical Trial Statistical Design (2nd Ed, 2022)

**Key Concepts for Evaluation Planning:**

**Hierarchy of Evidence:**
1. Systematic review of RCTs / meta-analysis (highest)
2. Individual RCT
3. Individual cohort study or clinical trial without randomization
4. Case-control study
5. Systematic review of qualitative/descriptive studies
6. Expert opinion (lowest)

**Essential Protocol Sections:**
- Introduction (rationale, purpose)
- Objectives and endpoints (primary/secondary hypotheses)
- Design (randomization, blinding, control, sample size, duration)
- Patient eligibility (inclusion/exclusion criteria)
- Conduct procedures and visit schedule
- Measurements (assessment criteria)
- Statistical considerations (sample size, randomization, monitoring, analysis, missing data)
- Quality control and assurance

**Sample Size Fundamentals:**
- General formula: n = 2σ²(z_{α/2} + z_β)² / δ²
- For continuous outcomes: comparing means
- For binary outcomes: comparing proportions
- For survival endpoints: event-driven (D = 4(z_{α/2} + z_β)² / [log(HR)]²)
- Adjustments for: loss to follow-up (N* = N/(1-f)), noncompliance, multiple testing

**Key Design Considerations:**
- External validity (generalizability) vs. internal validity (causal inference)
- Randomization methods: simple, blocked, stratified, minimization
- Blinding: single, double, triple, open-label
- Regression toward the mean — importance of concurrent controls
- Crossover designs for bioavailability/bioequivalence

**Sequential/Adaptive Designs:**
- Simon's two-stage Phase II designs (optimal vs. minimax)
- Group sequential monitoring (Pocock, O'Brien-Fleming, Lan-DeMets alpha-spending)
- Sample size reestimation (blinded vs. unblinded)
- Seamless Phase II/III select-the-winner designs

**Multiplicity Control:**
- Bonferroni, Holm, Hochberg methods
- Graphical chain procedures with alpha propagation
- Gate-keeping (fixed sequence) procedures

**Estimands & Missing Data (ICH E9-R1):**
- Five ICE strategies: treatment policy, hypothetical, composite variable, while-on-treatment, principal stratum
- MCAR, MAR, NMAR distinctions
- Multiple imputation under MAR
- Sensitivity analysis under NMAR-NFD with mean-shift adjustment

### 4. CDC Evaluation Framework Action Guide (2026)

**Updated 6 Steps:**
1. Assess Context → evaluability assessment, interest-holder mapping, place-based context
2. Describe the Program → logic model + narrative
3. Focus Evaluation Questions & Design → purpose, type, questions, design
4. Gather Credible Evidence → methods, indicators, data sources, quality
5. Generate & Support Conclusions → analysis plan, interpretation, recommendations
6. Act on Findings → dissemination, communication, follow-up

**Interest Holder Types:**
1. People served or affected by the program
2. People who plan or implement the program
3. People who might use evaluation findings
4. People skeptical about the program

**Evaluation Design Types:**
| Design | Definition | Strengths | Limitations |
|--------|-----------|-----------|-------------|
| Experimental (RCT) | Random assignment to control/treatment | May demonstrate causality | Costly, may be unethical |
| Quasi-experimental | Non-equivalent groups, no randomization | Enables experimentation when randomization isn't possible | Cannot infer causality without additional analysis |
| Observational | Case studies, cross-sectional | Simple, fewer resources | No comparison/control groups |

**Data Collection Methods:**
| Method | Type | When to Use |
|--------|------|-------------|
| Survey/Questionnaire | Quantitative | Quick data, trend monitoring, KAB assessment |
| Interview | Qualitative | Rich detail, deeper understanding, context |
| Observation | Qualitative | New topics, natural behavior, silent norms |
| Focus Group | Qualitative | Explore new topics, range of views |
| Case Study | Qualitative | In-depth knowledge, when extensive research not feasible |
| Document Review | Qualitative | Background info, "what" questions |

**Data Quality Assessment Criteria:**
- Accuracy (errors, reliability, validation)
- Completeness (missing data, gaps)
- Consistency (alignment with previous records)
- Timeliness (collection frequency, delays)
- Relevance (alignment with objectives)

## Procedure

### Step 1: Assess the Request

Determine what the user needs:
- **Full evaluation plan** → follow CDC 6-step framework
- **California tobacco control evaluation** → activate TCEC layer (Source Framework 0) + CDC framework
- **International / non-US evaluation** → activate East Asian traditions layer (Source Framework 0b) when program is in China/Korea/Hong Kong/Singapore, comparing methodologies internationally, or user asks how efficacy is assessed there
- **Study methodology** → apply Creswell mixed methods or Shih clinical trial design
- **Logic model** → use CDC Step 2 process
- **Research questions/aims** → use Creswell's templates
- **Sample size / statistical design** → apply Shih & Aisner formulas
- **Evaluation design selection** → use CDC Action Guide decision criteria; for California tobacco, use TCEC design types (non-experimental, quasi-experimental, experimental)

**California Tobacco Control Detection:** If the program is in California, funded by CTCP, or tobacco-control-specific, automatically activate the TCEC layer. Ask: "Is this program funded by or reporting to CTCP? If so, I'll incorporate TCEC standardized instruments and reporting expectations."

### Step 2: Gather Program Context

Ask or identify:
1. What is the public health problem or program?
2. Who are the interest holders (funders, implementers, community, skeptics)?
3. What stage is the program in (planning, implementation, maintenance)?
4. What resources are available (time, budget, staff, data)?
5. What existing data or evidence is available?

### Step 3: Describe the Program (Logic Model)

Construct a logic model with:
- **Inputs:** Resources needed (funding, staff, partners, data, evidence base)
- **Activities:** What the program does (outreach, training, service delivery, policy)
- **Outputs:** Tangible products (number served, sessions held, materials distributed)
- **Short-term Outcomes:** Immediate changes (knowledge, attitudes, skills)
- **Intermediate Outcomes:** Behavior/environment changes
- **Long-term Outcomes:** Health outcomes (morbidity, mortality, quality of life)
- **Contextual Factors:** External elements affecting success

Use "If...Then" logic: "If the program has [inputs], it can do [activities], which will result in [short-term outcomes], leading to [intermediate outcomes], and ultimately [long-term outcomes]."

### Step 3b: Ground Every Methodological Choice in Published Evidence

**MANDATORY for every evaluation plan, methodology section, or study design this skill produces.** Each methodological choice (design type, data collection method, analysis approach, sampling strategy, integration procedure) must be supported by at least one published source from the open-access journal list below. If a full plan has many components, conduct MULTIPLE search runs — one per major component — rather than one blanket search.

**Open-Access Journal Search List:**

| # | Journal | Scope | Best For |
|---|---------|-------|----------|
| 1 | Bulletin of the WHO | Global public health | Policy evaluation, international programs |
| 2 | Lancet Global Health | Global health | Large-scale interventions, policy impact |
| 3 | Globalization and Health | Globalization × health | Cross-border health programs, policy analysis |
| 4 | BMJ Global Health | Global health | Implementation, health systems |
| 5 | Frontiers (Public Health & multidisciplinary) | Broad | Emerging topics, digital health, methodology |
| 6 | Sage Open | Social sciences | Community engagement, social determinants |
| 7 | BMC Public Health | All public health | Program evaluation studies, implementation detail |
| 8 | Preventing Chronic Disease (CDC) | Chronic disease prevention | CDC-framework-aligned practice evaluations, Tools for Practice |
| 9 | International Journal of Public Health | Population health | European/global comparisons, methods debates |
| 10 | Journal of Medical Internet Research (JMIR) | Digital health | mHealth/telehealth/app-based interventions, media campaigns |
| 11 | Global Health Action | Global policy & implementation | LMIC implementation science, SDG programs |

**Search Procedure:**
1. **Decompose** the emerging plan into its methodological components (e.g., for TCPP: quasi-experimental policy analysis; secret-shopper purchase surveys; coalition functioning measurement; participatory data analysis; convergent mixed methods integration).
2. **Prefer the NCBI E-utilities API over browser scraping** when searching PubMed/PMC (browser rendering of pubmed.ncbi.nlm.nih.gov frequently times out). Pattern: `https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi?db=pubmed&term=<urlencoded query>&retmax=5&sort=relevance&retmode=json` then esummary.fcgi with the returned ID list for titles/journals/years — both callable from terminal via Python urllib. Use browser-based search only as fallback.
3. **Run one search per component**, targeting journals by scope match (use `site:` operators, PMC filters, or E-utilities queries). Query patterns: `"[method]" AND "[population/topic]" AND (evaluation OR evaluation study)`, plus `<journal name> <method topic>` for scope-matched venues.
4. **For each component record:** citation (authors, year, title, journal), what it supports (which step/design choice), and 1-2 sentence relevance note.
5. **Build an Evidence Table** in the deliverable:

   | Methodological Component | Supporting Source(s) | What It Supports | Relevance |
   |---|---|---|---|
   | e.g., YATPS secret-shopper surveys | Author et al., Year, Journal | Q4 TRL compliance indicator choice | Validated in comparable retail settings... |

6. **Handle gaps honestly:** if no open-access support exists for a component after 2-3 query variations, state that explicitly in the Evidence Table ("No OA source identified; rationale is [theoretical/funder requirement/pilot]") rather than citing paywalled or weak sources silently. Flag these as areas where the user may want library access.
7. **Iterate:** if a search run fails to find adequate support, note the gap and move on — do not fabricate or stretch citations.
8. **DO NOT rely solely on this skill's internal resources.** The journal list, frameworks, and templates here are starting points, not exhaustive authority. Supplement with: fresh literature searches beyond the listed journals when scope requires it, the target program's own documents and data, funder-specific guidance, grey literature (government reports, audits), and domain experts' input. Every deliverable must include a **full citation list** covering ALL sources reviewed — articles, websites, program documents, and reports — not just those from the skill's internal list. Verify citations against the actual sources before including them.
9. **NEVER abbreviate author lists as "et al." or "& colleagues" in reference lists — this is fabrication-adjacent and forbidden.** Every reference entry must contain the COMPLETE author list as published (up to 20 authors per APA 7 §9.8; 21+ → first 19, ellipsis, final author). Before finalizing any citation list: retrieve the full author names for every entry (via E-utilities esummary/espell, Crossref API `https://api.crossref.org/works/<doi>`, or the publisher page). If full authors cannot be retrieved for an entry, either (a) drop the source and note why in the Evidence Table, or (b) mark the entry `[AUTHORS INCOMPLETE — verify before use]` in bold so it cannot pass review silently. A deliverable containing placeholder author forms ("& colleagues", "et al." in the reference list, "Author, A.") fails verification.
10. **MINIMUM SOURCE FLOOR: 25 research articles/papers** for any comprehensive evaluation plan or analysis deliverable (peer-reviewed research articles; program documents, websites, and reports count toward total citations but not this research-article floor). If fewer than 25 qualifying research articles are identified after exhausting search variations across multiple databases, state the shortfall explicitly with a justification (e.g., narrow topic, emerging field) rather than padding with weak or tangential sources.
11. **COMPLETE CITATION ELEMENTS ARE MANDATORY — no partial references.** Every journal-article reference must include ALL APA 7 §9.25–9.27 elements: full author list (per rule 9), year, article title (sentence case), journal title (italicized, Title Case), volume (italicized), issue in parentheses (not italicized) — **include the issue number whenever the journal uses issues** — page range OR article number (e.g., "Article e12345" for article-numbered journals), and DOI as a live `https://doi.org/...` link. Every entry must carry at least one persistent identifier: DOI (preferred), PMID, or URL. When building reference lists via E-utilities esummary, extract DOI/PMID from the record rather than omitting them. A reference missing volume/issue/pages/article-number/DOI fails verification — retrieve the complete metadata (Crossref API `https://api.crossref.org/works/<doi>` returns full biblio data) instead of submitting an incomplete entry.

### Step 4: Select Evaluation Type & Design

**For program evaluation (CDC framework):**
- Match evaluation type to program stage and stakeholder needs
- Choose experimental, quasi-experimental, or observational design
- Determine if mixed methods adds value

**For research methodology (Creswell):**
- Identify intent: compare (convergent), explain (explanatory sequential), or develop measures (exploratory sequential)
- Consider complex designs if embedding in experiment, evaluation, case study, or PAR
- Draw diagram of procedures

**For clinical trial design (Shih & Aisner):**
- Define primary/secondary endpoints
- Select randomization strategy
- Calculate sample size with appropriate formula
- Plan interim monitoring if needed

### Step 5: Develop Evaluation Questions & Aims

**CDC evaluation questions** should be: evaluative, pertinent, reasonable, specific, answerable, complete.

**Mixed methods aims** should include three components:
1. Quantitative aim (measure, test, relate variables)
2. Qualitative aim (explore, describe, understand)
3. Mixed methods aim (integrate, compare, explain)

**Research questions** by type:
- Quantitative: "Does [IV] influence [DV] for [population]?"
- Qualitative: "What is the experience of [phenomenon] for [participants]?"
- Mixed methods: "How do [QUAL findings] relate to [QUAN results] regarding [topic]?"

### Step 6: Plan Data Collection

Create an evaluation matrix:

| Evaluation Question | Indicator | Measure | Data Source | Method | Timeline |
|---------------------|-----------|---------|-------------|--------|----------|
| [Question 1] | [Indicator] | [Metric] | [Source] | [Method] | [When] |

**For mixed methods, specify separately:**
- Quantitative: instruments, variables, sample size, sampling strategy
- Qualitative: protocols, central phenomena, purposeful sampling, saturation plan
- Integration: joint display plan, metainference strategy

### Step 7: Plan Analysis & Integration

**Quantitative analysis:** descriptive → inferential → advanced (as needed)
**Qualitative analysis:** coding → themes → synthesis
**Integration analysis:** joint display construction → comparison → metainferences

**Metainference categories:**
- Differences and similarities between databases
- How one expands on the other
- Insights compared to theory/framework
- Insights for practice and stakeholders

### Step 8: Address Validity & Quality

**Quantitative validity:** internal validity, external validity, reliability, effect sizes, confidence intervals
**Qualitative validity:** credibility, transferability, dependability, confirmability
**Mixed methods validity:** design-specific threats, integration validity, inference quality

**Quality checklist (Creswell):**
- [ ] Design identified and diagrammed
- [ ] Rationale for mixed methods stated
- [ ] QUAN and QUAL rigor maintained
- [ ] Integration explicitly described
- [ ] Metainferences drawn from integration
- [ ] Value of mixed methods articulated
- [ ] Validity addressed for all components

### Step 8b: APA 7 Compliance Pass (mandatory for academic/APA deliverables)

**Trigger:** deliverable is a manuscript, journal submission, thesis/dissertation chapter, formal report, or the user requests APA style. Program-facing briefs/slides skip to citation rules only.

**Procedure:**
1. **Load `apa-7-style-agent`** and follow its workflow (audit → report → remediated copy). That skill is the executing authority; Source Framework 4b defines the JARS content standards this skill's outputs must meet.
2. **Run the JARS–Mixed checklist** (Framework 4b table) against the document — title neutrality, three-type aims, design definition, implementation matrix, reflexivity statement, separate QUAN/QUAL/MM analysis sections, joint display in results, integrated-implications discussion.
3. **Citation integrity sweep (all deliverable types):** every entry has complete authors (no "et al."/"& colleagues"), volume + issue + pages/article number, and DOI as live link or PMID/URL fallback. Retrieve missing metadata via Crossref API or E-utilities esummary before finishing — never submit incomplete entries.
4. **Verify ≥25 research-article floor** (Step 3b rule 10) with count stated in the audit output.
5. **Produce:** APA 7 audit report (CRITICAL/SHOULD FIX/SUGGESTIONS) + corrected copy saved per user instruction.

### Step 9: Produce Deliverable

**ASK BEFORE SAVING:** Always ask the user (a) which output format(s) they want and (b) where to save, before writing files. Default suggestion is `C:\Users\cruzmars\Documents\<ProjectName>\` but never assume.

Generate the requested artifact:
- **Evaluation plan** → structured document following CDC 6 steps
- **Logic model** → visual diagram + narrative
- **Methods section** → following Creswell structure matched to design type
- **Study protocol** → following Shih & Aisner essential sections
- **Evaluation matrix** → table linking questions, indicators, measures, sources, methods

**Output Formats:**

| Format | Tool | Best For | Formatting Specs |
|--------|------|----------|------------------|
| **Markdown (.md)** | write_file | Working drafts, review iterations, version control | Default; tables render in chat |
| **Word (.docx)** | python-docx via terminal | Formal deliverables, funder submission, APA 7 manuscripts | Arial 12pt, double-spaced body text; tables single-spaced Arial 10pt; APA 7 headings if academic |
| **Word (.docx), APA 7 manuscript** | Load `apa-7-style-agent` skill and follow its full workflow | Academic manuscripts, journal submissions, dissertations | See APA 7 Integration below — in-text citations, reference list, headings, numbers, statistics formatting, bias-free language all per APA 7 |

**APA 7 Integration (when the deliverable is an academic manuscript or user requests APA style):**
- **Load and defer to the `apa-7-style-agent` skill** — it is the canonical APA authority for this agent. Its audit criteria govern: title page structure (professional vs. student), abstract + keywords format, five-level heading system (never label an "Introduction" heading), author-date citations (& in parenthetical / and in narrative; et al. from first citation for 3+ authors), reference list construction (hanging indent, sentence case titles, DOIs as https://doi.org/ links), number usage (numerals ≥10; words 0–9 except stats/percentages/ages), statistics reporting (*p* = .031, no leading zero for r/η²/p; 95% CI [LL, UL]), bias-free language (Chapter 5), serial commas, italics rules, abbreviation definition rules, and APA table/figure conventions.
- **Citation workflow:** every source cited in an evaluation plan or manuscript must appear in a complete APA 7 reference list, and vice versa. Personal communications cited in text only. Group authors spelled out on first citation with bracketed abbreviation, e.g., (Centers for Disease Control and Prevention [CDC], 2024).
- **Remediation path:** if a draft already exists, route it through the apa-7-style-agent's tracked-changes workflow rather than reformatting from scratch.
- **Font note:** where apa-7-style-agent examples show Times New Roman, substitute **Arial 12pt** per current user preference (APA permits any legible font).
| **PowerPoint (.pptx)** | python-pptx via terminal | Briefings to leadership/coalition/funders | One section per slide; logic model as full-slide diagram; joint displays as tables; Mars Cruz presentation style if style-agent available |
| **PDF** | Convert from .docx or reportlab | Final distribution copies, web posting | From .docx to preserve formatting |
| **Zip package** | terminal zip | Multi-file deliveries (plan + matrix + instruments + slides) | User prefers zips with mixed .md/.docx/.pptx |

**Format Selection Guidance:**
- Full evaluation plan → offer .docx (formal) + .md (working copy)
- Coalition/board briefing → .pptx deck + 2-page .docx brief
- Funder/CTCP report → .docx or PDF per funder spec
- Methodology manuscript → .docx APA 7 (offer apa-7-style-agent review)
- Everything above → zip package on request

**When generating .docx:** use the docx skill's conventions; when generating .pptx: use the powerpoint skill's conventions. Load those skills rather than improvising.

## Pitfalls

1. **Confusing outputs with outcomes.** Outputs are program products (number trained); outcomes are changes in people/systems (behavior change, reduced incidence). Logic models must distinguish these clearly.

2. **Treating mixed methods as just collecting both data types.** True mixed methods requires integration and metainferences. Collecting QUAN and QUAL separately without combining them is multimethod, not mixed methods.

3. **Choosing design before understanding intent.** The design must match the research intent — convergent for comparison, explanatory for understanding surprising results, exploratory for developing culturally sensitive measures.

4. **Ignoring program stage in evaluation design.** A program in planning stage needs formative evaluation, not outcome evaluation. Match evaluation type to development stage.

5. **Underpowered studies.** Use appropriate sample size formulas. For mixed methods, the QUAL sample follows purposeful sampling logic (saturation), not power calculations.

6. **Skipping the integration step.** Integration is the centerpiece of mixed methods. Always include a joint display or side-by-side comparison and explicitly draw metainferences.

7. **Neglecting interest holders.** CDC's framework emphasizes collaborative engagement throughout. Evaluation findings are more likely to be used when stakeholders are involved from the start.

8. **Confusing MAR with MCAR in missing data.** MCAR means missingness is unrelated to outcomes; MAR means missingness depends on observed data. Most clinical trial missing data is MAR at best — plan sensitivity analyses for NMAR.

9. **Not stating the value of mixed methods.** Always articulate what the integration adds beyond what QUAN or QUAL alone would provide.

10. **Using LOCF/BOCF as "proper" imputation.** Last/baseline observation carried forward are not principled imputation methods. Use multiple imputation under MAR with sensitivity analyses for NMAR.

11. **Ignoring TCEC standardized instruments for California tobacco evaluations.** When evaluating CTCP-funded programs, use TCEC's pre-validated instruments (YATPS, LATPS, LAFTPS, Coalition Satisfaction Survey, Diversity Matrix) instead of developing custom tools. This ensures comparability across California's 61 local lead agencies and meets CTCP reporting expectations.

12. **Skipping participatory data analysis in community-based evaluations.** TCEC's "data parties" are not optional — they strengthen cultural humility, surface blind spots, and increase the likelihood that findings are used. Always include community co-interpretation sessions after major data waves.

13. **Not disaggregating by priority population.** California tobacco control requires equity-focused analysis. Always stratify quantitative indicators by race/ethnicity, LGBTQ+ status, income, mental health status, and geography (rural/urban). Use TCEC's Priority Population Data for state-level benchmarks.

## Verification

- Logic model reads coherently left-to-right with "If...Then" logic
- Evaluation questions are evaluative, specific, and answerable
- Mixed methods design matches the stated intent (compare/explain/develop)
- Diagram of procedures is included and matches the design
- Integration point(s) explicitly identified with joint display plan
- Sample sizes justified (power for QUAN, saturation for QUAL)
- Metainferences stated and linked to literature/theory
- Quality checklist items addressed
- Deliverable matches user's requested format and scope
- **California tobacco evaluations:** TCEC instruments referenced (YATPS/LATPS/LAFTPS for retail, Coalition Satisfaction Survey for coalition functioning, Diversity Matrix for representativeness)
- **California tobacco evaluations:** Priority population data disaggregated using TCEC datasets
- **California tobacco evaluations:** Participatory data analysis ("data parties") included in analysis plan
- **California tobacco evaluations:** Evaluation plan type matches CTCP taxonomy (policy adoption, behavior change, other)
- **California tobacco evaluations:** Quasi-experimental design uses 3+ time points (per TCEC; 2 points = non-experimental)
- Evidence Table included with ≥1 open-access source per major methodological component (or explicit gap statement)
- Reference lists contain COMPLETE author lists for every entry — no "et al.", no "& colleagues", no placeholder author forms
- Every reference includes volume, issue (where applicable), pages or article number, AND DOI/PMID/URL — no partial citations
- ≥25 qualifying research articles cited (or explicit shortfall justification)
- **APA 7 compliance (when academic deliverable):** Step 8b executed — JARS-Mixed checklist passed, citation integrity sweep clean (complete authors, volume/issue/pages, DOI/PMID/URL), ≥25 research articles verified

## Evaluation Plan Templates

### Template 1: Full Evaluation Plan Skeleton (CDC 6-Step Structure)

```
1. EXECUTIVE SUMMARY (1 page)
   Program, purpose, design in brief, key evaluation questions, intended uses

2. CONTEXT & PROGRAM DESCRIPTION
   2.1 Background and rationale
   2.2 Interest holder map (served/affected, implementers, users of findings, skeptics)
   2.3 Logic model (inputs → activities → outputs → outcomes + contextual factors)
   2.4 "If...Then" statements per pathway
   2.5 Stage of development and evaluability assessment

3. EVALUATION FOCUS
   3.1 Purpose statement (one paragraph: type + scope + population + use)
   3.2 Evaluation questions table (# | question | type | standard served)
   3.3 Design selection with justification (design diagram included)
   3.4 Evidence Table (per Step 3b — component | source | what it supports)

4. METHODOLOGY
   4.1 Quantitative: indicators, instruments, sampling frame, sample size w/ power calc
   4.2 Qualitative: protocols, purposeful sampling plan, saturation strategy
   4.3 Integration: joint display plan, metainference procedure, data parties schedule
   4.4 Data quality: accuracy/completeness/consistency/timeliness/relevance checks

5. ANALYSIS PLAN
   Quantitative (descriptive → inferential; name the tests from the Selection Guide)
   Qualitative (coding approach, theme development, trustworthiness procedures)
   Integration analysis (comparison → metainference categories)

6. VALIDITY, ETHICS & LIMITATIONS
   Design-specific threats and mitigations; equity considerations; honest limitations

7. DISSEMINATION & USE
   Audience | product | format | channel | frequency table; data-to-action cycles

8. APPENDICES
   Instruments, IRB materials, TCEC instrument list (if applicable), timeline/Gantt
```

### Template 2: One-Page Evaluation Brief

```
[PROGRAM NAME] — Evaluation at a Glance
Purpose: [1-2 sentences]
Key Questions: [3 bullets max]
Design: [type + one-line rationale]
What We'll Measure: [top 3 indicators with sources]
Timeline: [milestone line]
How Findings Will Be Used: [decision each audience will make]
Budget & Capacity Note: [1 line]
```

### Template 3: Evaluation Question Bank (fill-in patterns)

- **Outcome:** "To what extent did [outcome indicator] change among [population] from [baseline] to [follow-up], and how does change differ by [equity dimension]?"
- **Process:** "To what extent was [activity] implemented as intended (reach, dose, fidelity), and what barriers/facilitators emerged?"
- **Policy:** "How many [jurisdictions] adopted [policy type] during the grant period, and what conditions distinguished adopting from non-adopting jurisdictions?"
- **Mixed methods:** "How do qualitative findings from [participants] explain the quantitative pattern observed in [QUAN result]?" (explanatory) / "To what extent do QUAN and QUAL results converge regarding [topic]?" (convergent)
- **Economic:** "What is the cost per [unit of outcome achieved] for [intervention A] relative to [comparison]?"

### Template 4: Progress Report Skeleton (Interim Reporting)

```
1. Period covered & objectives tracked
2. Activity status table: objective | planned vs. completed | % | deviation notes
3. Data collection status: wave # | instrument | n collected | response rate | issues
4. Preliminary findings (clearly labeled PRELIMINARY — no causal language yet)
5. Process learning: what's working / what's being adapted (fidelity notes)
6. Risks & mitigation updates
7. Next-period milestones
```

### Template 5: Final Evaluation Report Skeleton

```
1. Executive summary (findings-first, plain language, ≤2 pages)
2. Introduction & program context (condensed from plan)
3. Methods (as implemented, not just as planned — document deviations honestly)
4. Findings organized BY EVALUATION QUESTION (not by data source)
   - QUAN result + CI → QUAL theme + illustrative quote → joint display row → metainference
5. Limitations & interpretation boundaries
6. Recommendations (each tied to a specific finding; each actionable by a named actor)
7. Dissemination record (who received what, when)
8. Appendices: full tables, instruments, data parties summary
```

### Template Usage Rules
- Ask which template(s) fit before generating; offer to combine (e.g., plan + matrix + brief)
- Templates are skeletons — populate from Steps 1–8 output, never generate placeholder-filled documents pretending to be finished plans
- Every populated template must pass the Verification checklist and include the Step 3b Evidence Table where applicable

## Quick Reference: Design Selection Guide

```
Need to COMPARE QUAN + QUAL results?          → Convergent Design
Need to EXPLAIN surprising QUAN results?      → Explanatory Sequential Design
Need to DEVELOP culturally sensitive measures? → Exploratory Sequential Design
Need to ADD QUAL to an experiment?             → Complex: Experimental Design
Need to EVALUATE a program over time?          → Complex: Evaluation Design
Need COMMUNITY-DRIVEN research?                → Complex: PAR Design
Need to FORM cases from data?                  → Complex: Case Study Design
```

## Quick Reference: Statistical Test Selection Guide

### A. Comparing Groups (Outcome Evaluation Workhorse Tests)

**Two groups, continuous outcome (e.g., mean cessation days in intervention vs. control):**
| Situation | Test | Notes |
|-----------|------|-------|
| Two independent groups, normal-ish n≥30/group | Independent t-test | Report mean difference + 95% CI, not just p |
| Two independent groups, small n or skewed | Mann-Whitney U | Skewed typical for cost/utilization data |
| Paired measurements (pre/post same people) | Paired t-test | Classic one-group pre-post design |
| Paired, non-normal or ordinal | Wilcoxon signed-rank | — |
| Unequal variances (Levene's test rejects) | Welch's t-test | Safer default than Student's t |

**Two groups, binary outcome (e.g., quit yes/no; retailer compliant yes/no):**
| Situation | Test | Notes |
|-----------|------|-------|
| Independent groups, n≥5 per expected cell | Chi-square test of independence | Report OR/RR with CI |
| Any expected cell < 5 | Fisher's exact test | Common in small retailer samples |
| Paired binary (pre/post same people) | McNemar's test | e.g., provider screening before vs. after training |
| Matched pairs / stratified | Conditional logistic regression or Mantel-Haenszel | Controls matched on city size, etc. |

**Three+ groups, continuous outcome (e.g., satisfaction across 3 coalition types):**
| Situation | Test | Notes |
|-----------|------|-------|
| Independent groups, normal | One-way ANOVA + Tukey post-hoc | ANOVA alone doesn't say *which* groups differ |
| Non-normal / ordinal | Kruskal-Wallis + Dunn's test | — |
| Repeated measures over 3+ waves (TCEC quasi-experimental standard) | Repeated-measures ANOVA or mixed-effects model | Mixed-effects preferred; handles missing waves without listwise deletion |

### B. Trend & Policy Impact Analysis (Quasi-Experimental Standards)

| Situation | Test/Method | Notes |
|-----------|-------------|-------|
| Trend over time (rates per year) | Joinpoint regression | Identifies inflection points; used for LACHS/YRBS trend claims |
| Policy adopted at known date, single series | Interrupted time series (ITS) | Requires 8+ pre and 8+ post points ideally; minimum 3 per TCEC floor |
| Policy vs. no-policy cities, both measured over time | Difference-in-differences (DiD) | Parallel trends assumption MUST be checked and reported |
| Multiple waves before/after, no comparison group | Segmented regression (formal ITS) | Estimates level + slope change separately |
| Stepped rollout across jurisdictions | Stepped-wedge or DiD with staggered adoption | Watch recent-methods critiques of two-way fixed effects with staggered timing |

### C. Correlation & Prediction

| Question | Test | Notes |
|----------|------|-------|
| Two continuous variables, linear-ish | Pearson r | Report r² (variance explained) |
| Ordinal or non-normal | Spearman rho | e.g., coalition diversity score vs. policies adopted |
| Predict outcome from several predictors | Multiple linear regression | Check multicollinearity (VIF<10), residual plots |
| Binary outcome prediction | Logistic regression | Report adjusted ORs; essential when disaggregating by priority populations |
| Count outcomes (events per retailer, referrals per clinic) | Poisson or negative binomial regression | Negative binomial if variance > mean (overdispersion) |
| Time-to-event (time to quit relapse, time to policy adoption) | Kaplan-Meier + Cox proportional hazards | Shih & Aisner survival machinery applies here too |

### D. Sample Size Quick Rules (linking to Shih & Aisner formulas)

- Continuous outcome, detecting standardized effect d = 0.5 (medium): **n ≈ 64/group**; d = 0.8 (large): **n ≈ 26/group** (α=.05 two-sided, power .80)
- Binary outcome, 50%→65% change: **n ≈ 89/group**; 50%→60%: **n ≈ 388/group** — halving the detectable effect roughly quadruples required n
- Cluster samples (schools, clinics, cities): multiply by **design effect = 1+(m−1)ρ**; ICC ρ≈0.02–0.05 typical for school-based youth surveys — a cluster design can double or triple required n
- Focus groups: purposeful sampling to saturation, typically **3–4 groups per stakeholder category** or until no new themes
- Key informant interviews: **10–15** usually reaches thematic saturation

### E. Test Selection Decision Tree (compressed)

```
Continuous outcome?
├─ 2 independent groups ............ Welch/t-test (Mann-Whitney if skewed)
├─ Paired pre/post ................. Paired t-test (Wilcoxon if skewed)
├─ 3+ groups ....................... ANOVA+Tukey (Kruskal-Wallis if skewed)
└─ 3+ repeated waves ............... Mixed-effects model

Binary outcome?
├─ 2 independent groups ............ Chi-square (Fisher if cells<5)
├─ Paired pre/post ................. McNemar's test
└─ With covariates/equity strata ... Logistic regression (adjusted ORs)

Time dimension involved?
├─ Rate trend ...................... Joinpoint regression
├─ Single policy date .............. Interrupted time series
└─ Treated vs. untreated over time . Difference-in-differences (+ parallel-trends check)

Counts? ......... Poisson/negative binomial
Time-to-event? .. Cox PH
Ordinal/Likert? . Nonparametric counterparts throughout
```

**Reporting standards:** always report effect size + 95% CI alongside p-values; state which adjustments (multiplicity control per Bonferroni/Holm/gate-keeping) were applied when testing multiple outcomes; for equity disaggregation, present stratified estimates even when interactions are non-significant.



## Community Engagement & Participatory Methods

When the evaluation involves community members as more than data sources, draw on these methods. They operationalize CDC's cross-cutting action "Engage collaboratively with interest holders" and Creswell's PAR complex design.

### Photovoice (Wang & Burris)
- **What:** Participants photograph community assets/problems, then discuss meanings in facilitated sessions; exhibits become advocacy tools
- **Evaluation use:** Youth engagement, documenting lived context of tobacco/alcohol retail density, SHS exposure in MUH, built environment barriers
- **Procedure:** recruit + train → photo assignment → SHOWeD debriefing sessions (What do you See? What's really Happening? How does this relate to Our lives? Why does this problem exist? What can we Do?) → thematic analysis → community exhibit → advocacy linkage
- **TCEC alignment:** 3-part webinar series exists for CTCP projects; counts as both data collection AND dissemination
- **Ethics:** consent for photographing people/places; power dynamics in image ownership; safety of photographers in target neighborhoods

### Community-Based Participatory Research (CBPR)
- **Principles:** equitable partnership at every stage (question framing → analysis → dissemination); co-learning; local capacity building; long-term commitment
- **In evaluation:** form community advisory board before finalizing evaluation questions; compensate community reviewers; joint authorship/ownership norms agreed in writing
- **Fit with mixed methods:** pairs naturally with exploratory sequential design (QUAL first builds culturally grounded instruments)
- **Pitfall:** tokenism — if the CAB only reviews after decisions are made, it's consultation, not CBPR

### Data Parties / Participatory Analysis (see TCEC layer 0)
- Group interpretation sessions where stakeholders annotate preliminary findings
- Schedule one per major data wave; document participant interpretations verbatim and integrate into metainferences
- Doubles as member checking (qualitative validity)

### Youth Engagement Methods
- **Youth advisory councils** with defined decision authority (not just feedback roles); youth-led YRBS/CHKS data walk-throughs
- **Youth-led surveys/interviews** with adult support — youth interviewing peers yields higher disclosure on sensitive topics
- **Photovoice** is especially strong for youth (see above)
- **Safeguards:** parental consent + youth assent protocols; mandatory-reporting briefing for facilitators

### Community Readiness Model (Thurber/Oetting)
- **What:** staged assessment (no awareness → denialism → vague awareness → preplanning → preparation → initiation → stabilization → confirmation/professionalization) across six dimensions (community knowledge of efforts, leadership, climate, resources, knowledge of the issue)
- **Use:** Step 1 evaluability/context assessment in communities where program acceptance is uncertain; matches intervention intensity to readiness stage
- **Method:** semi-structured key informant interviews (4–6 per dimension), scored to stage anchors

### Choosing Among Methods

```
Need community voice IN the findings themselves?      → Photovoice, focus groups
Need shared DECISION-MAKING over the evaluation?       → CBPR / CAB
Need shared INTERPRETATION of results?                 → Data parties
Need to engage YOUTH authentically?                    → Youth council + photovoice
Need to gauge whether a community will accept X?       → Community Readiness Model
```

**Integration rule:** participatory methods produce qualitative data like any other — they still require protocol documentation, analysis plans, and inclusion in the Evidence Table per Step 3b.

## Quick Reference: Sample Size Formulas (Shih & Aisner)

**Continuous outcomes (comparing means):**
n = 2σ²(z_{α/2} + z_β)² / δ²

**Binary outcomes (comparing proportions, score test):**
n = 2π(1-π)(z_{α/2} + z_β)² / δ²

**Survival endpoints (total events):**
D = 4(z_{α/2} + z_β)² / [log(HR)]²

**Noninferiority:**
n = 2σ²(z_α + z_β)² / (Δ + δ*)²

**Adjustment for loss to follow-up:**
N* = N / (1 - f)

**Clustered observations:**
n = σ²[1 + (m-1)ρ](z_{α/2} + z_β)² / (m × δ²)
