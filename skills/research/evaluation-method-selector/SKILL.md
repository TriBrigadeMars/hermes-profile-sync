---
name: evaluation-method-selector
description: "Pick a study methodology grounded in current journals."
version: 1.0.0
author: Hermes Agent + Mars Cruz
license: MIT
metadata:
  hermes:
    tags: [research, methodology, evaluation, evidence-review]
    related_skills: [research-design-orchestrator, grounded-citations]
---

# Stage 2: Evaluation Methodology Selector

## When to Use
Use after the research question is framed (or directly with a known question) to select the best evaluation/study methodology, grounded in CURRENT published methodological research via live web search. Runs standalone or as Stage 2 of `research-design-orchestrator`.

## Intake (clarify tool)
1. Confirm the research question(s) from Stage 1 output (paste or restate).
2. Practical constraints: sample reachability, timeline, budget tier (pilot vs funded), randomization feasibility, IRB posture.
3. Preference signal: does Mars lean quantitative / qualitative / mixed / undecided?

## Journal-Weighted Search Strategy (REQUIRED — Mars directive, 2026-08)

Live web research MUST emphasize peer-reviewed research articles and journals, EVEN WHEN PAYWALLED:

| Weight | Source class | Examples |
|---|---|---|
| High (~70%) | Peer-reviewed journals & databases | PubMed/MEDLINE, Cochrane Library, APA PsycInfo-indexed, *American Journal of Evaluation*, *Evaluation Review*, *Health Education Research*, *Social Science & Medicine*, *Implementation Science*, SAGE/JSTOR/Elsevier/Taylor & Francis |
| Medium (~20%) | Consensus/reporting standards tied to the literature | CONSORT, TREND, STROBE, COREQ, RE-AIM.org, MMAT |
| Low (~10%) | Gray literature | Only to fill gaps; must be labeled as such |

Rules:
- **PAYWALLS ARE OKAY.** Abstracts, structured summaries, and cited findings are acceptable evidence; cite the article regardless of access level. NEVER skip an article because full text is gated.
- Prefer articles from the last ~7 years for methodological trends; classic foundational citations (Campbell & Stanley, etc.) are exempt from recency.
- For every recommended design, capture: author(s), year, journal, DOI/URL, and the specific methodological claim it supports.
- If web search fails entirely: proceed using established frameworks (CONSORT/TREND/RE-AIM/MMAT/COREQ) and CLEARLY label all recommendations as NOT verified against current publications.

## Method Decision Logic

Map question type → candidate designs, then narrow by constraints:
- Causal/intervention → RCT, cluster RCT, quasi-experimental (stepped-wedge, difference-in-differences, interrupted time series)
- Program evaluation → logic model + RE-AIM, pre/post with comparison, developmental evaluation
- Exploratory/meaning → qualitative (interviews, focus groups, photovoice), COREQ standards
- Prevalence/association → cross-sectional survey, secondary data analysis
- Process understanding → mixed methods convergent/explanatory sequential, MMAT quality appraisal

Always present the top 2–3 viable designs as a comparison table: strengths, threats to validity, cost/timeline fit, evidence base from the search, and YOUR recommendation with justification. Mars makes the final call via clarify.

## Deliverable
`02_methodology_selection.md`: chosen design + rationale, comparison table, annotated source list (author/year/journal/DOI/claim), limitations acknowledged, and reporting-standard checklist to adopt. Ask where to save if running standalone.

## Rules
- Every methodology claim must trace to a real searched source — no invented citations. Verify DOIs resolve when possible.
- Run delegate_task children ONE at a time; instruct them to use write_file for outputs.
