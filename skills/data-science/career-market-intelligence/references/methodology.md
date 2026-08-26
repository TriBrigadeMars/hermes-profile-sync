# Statistical Methodology

## Purpose

This skill is designed for descriptive labor-market analysis and job-seeker decision support. It is intentionally conservative about causal inference and individual prediction.

## Evidence classes

### DEMAND
Evidence that employers or occupational reference systems request or rate an attribute. Examples: share of matched postings mentioning SQL; O*NET importance rating for Critical Thinking.

Demand answers "what is requested?" It does not answer "what causes hiring?"

### OUTCOME-ASSOCIATED
Evidence from records that contain an outcome such as interview, offer, or hire plus job-relevant candidate attributes. The scripts compare rates among records with and without an attribute.

Association answers "what co-varies with observed outcomes in this dataset?" It may be confounded by seniority, occupation, geography, employer selection, measurement error, and who applied.

### CAUSAL
Reserve this label for credible research designs such as randomized interventions, strong natural experiments, or defensible quasi-experimental studies. The local scripts do not automatically establish causality.

## Posting prevalence

For a target corpus of N postings and skill s:

    prevalence(s) = postings mentioning s / N

The report uses a 95% Wilson interval for a binomial proportion. Wilson intervals behave better than normal approximations when proportions are near 0 or 1 or samples are modest.

## Demand lift

When a comparison corpus exists:

    lift(s) = target_prevalence(s) / comparison_prevalence(s)

A lift above 1 means the skill is more prevalent in the target market than the comparison corpus. It is a differentiation signal, not a causal effect. The script suppresses lift when comparison support is too small.

## Trend

The core implementation divides dated postings into earlier and later halves of the observed date range and reports percentage-point change. This is a descriptive trend indicator. It is not seasonally adjusted and should not be treated as a labor-market forecast.

## Skill co-occurrence

For skill pair (a, b):

    cooccurrence(a,b) = postings mentioning both a and b / N

Pairs can reveal market bundles, but frequent pairs may partly reflect title mix or employer duplication.

## Experience benchmarks

The parser recognizes common expressions such as "5+ years" and extracts the minimum stated years. These are requested-experience benchmarks from postings, not actual experience of successful hires.

## Outcome association

For a binary skill indicator and hire outcome:

    risk_with = hired_with_skill / records_with_skill
    risk_without = hired_without_skill / records_without_skill
    risk_difference = risk_with - risk_without
    risk_ratio = risk_with / risk_without

An approximate log risk-ratio confidence interval is produced when all required cells are nonzero. Odds ratios use a 0.5 Haldane-Anscombe correction when needed for numerical stability.

Default suppression:
- fewer than 50 outcome records overall;
- fewer than 10 records in either the with-skill or without-skill group.

These thresholds are guardrails, not proof of adequate statistical power.

## Selection bias

Job posting corpora overrepresent employers and sites present in the collection method. Applicant-outcome datasets overrepresent people who applied and organizations that supplied data. Professional profiles overrepresent people who maintain profiles. Never generalize beyond the sampled population without qualification.

## Multiple comparisons

When testing many skills, some associations will appear large by chance. The core report intentionally emphasizes effect sizes and confidence intervals rather than p-value fishing. For formal research, add a preregistered analysis plan and multiple-comparison correction.

## Candidate comparison

Candidate evidence is binary/structured input supplied by the user. Market prevalence determines prioritization only after evidence is confirmed. The decision rule is:

- high market demand + candidate evidence -> EMPHASIZE;
- high market demand + no evidence -> GAP / DO NOT CLAIM;
- low/moderate demand + candidate evidence -> SECONDARY unless the target JD elevates it.

## Prohibited inference

Do not estimate hireability using protected traits or proxies. Do not derive sensitive traits from names, photographs, addresses, schools, organizations, or writing style.
