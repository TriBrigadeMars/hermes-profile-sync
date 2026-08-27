---
name: study-measures-and-sampling
description: "Pick validated measures, sampling plan, and sample size."
version: 1.0.0
author: Hermes Agent + Mars Cruz
license: MIT
metadata:
  hermes:
    tags: [research, measurement, sampling, instruments]
    related_skills: [research-design-orchestrator]
---

# Stage 3: Measures & Sampling Planner

## When to Use
Use once the research question and methodology exist (Stages 1–2 of `research-design-orchestrator`, or provided directly) to operationalize variables and plan recruitment.

## Intake (clarify tool)
1. Confirm chosen design + primary/secondary outcomes from Stage 2.
2. Population details: recruitment setting, expected availability, literacy/language needs (Spanish?), incentives feasible.
3. Measurement preferences: validated scales preferred? Wearables/administrative data available? Qualitative acceptable for which outcomes?
4. Analysis software Mars will use (R, SPSS, Stata?) — affects power-script deliverable.

## Journal-Weighted Evidence Rule
Same policy as `evaluation-method-selector`: when citing psychometric properties, feasibility benchmarks, effect sizes, or response-rate norms, weight peer-reviewed validation studies ~70%+ (paywalled abstracts acceptable and citable); label any gray-literature basis. Verify instrument citations are real before including.

## Work Performed
1. **Measures table** per outcome: construct, instrument name, # items, scoring, reliability/validity stats WITH citation (validation population), administration burden, cost/licensing notes, reading level.
2. **Sampling plan**: frame, technique (simple/stratified/cluster/purposive/convenience-with-limits), inclusion/exclusion criteria, recruitment channels matched to the population.
3. **Sample size**: compute with real formulas in Python — power analysis for quantitative designs; saturation guidance (e.g., Guest et al. lineage) for qualitative. Show all assumptions explicitly so they can be defended at IRB.
4. **Retention & bias mitigation**: anticipated attrition, mitigation tactics, missing-data approach.

## Deliverable
`03_measures_and_sampling.md` (+ `03_power_analysis.py` script that can be rerun with changed assumptions). Ask save location when standalone.

## Rules
- delegate_task children one at a time; require write_file usage.
- If a validated instrument is proprietary/costly, flag licensing lead time in the plan.
