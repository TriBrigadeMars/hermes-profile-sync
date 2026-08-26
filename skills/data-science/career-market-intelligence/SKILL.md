---
name: career-market-intelligence
description: Analyze labor-market evidence for career decisions.
version: 0.1.0
author: Local contributor, Hermes Agent
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [career, labor-market, resume, statistics, hiring]
    related_skills: []
---
# Career Market Intelligence Skill

This skill analyzes labor-market evidence for a target role and converts the results into truthful resume and career strategy. It is local-first: the core analysis uses Python's standard library and SQLite, while optional adapters can ingest public O*NET, BLS/OEWS, OPM FWD, USAJOBS, licensed labor-market data, or user-supplied datasets.

The skill must keep three evidence classes separate: **demand evidence** from postings, **outcome-associated evidence** from applicant/hire records, and **causal evidence** from credible causal research. Never present demand or association as proof that a skill causes hiring.

## When to Use

Use when the user asks:
- which skills, credentials, experiences, or benchmarks matter for a target job;
- what current postings statistically request for a title, location, industry, or seniority;
- how a candidate compares with a labor-market benchmark;
- which truthful resume claims deserve greater emphasis;
- whether a credential or skill appears to be a market gap;
- for federal roles, what OPM hiring data shows about actual accessions.

Don't use for:
- deciding whom an employer should hire;
- ranking candidates for employment decisions;
- inferring protected or sensitive characteristics;
- claiming a causal hiring advantage from observational posting/profile data;
- inserting a skill, credential, or experience the candidate cannot evidence.

## Prerequisites

Core mode requires Python 3.10+ and no third-party packages.

Optional OPM Parquet analysis requires:

```bash
python -m pip install pandas pyarrow
```

Optional XLSX import convenience requires:

```bash
python -m pip install pandas openpyxl
```

No paid API is required for core local analysis. USAJOBS search requires the user's own USAJOBS API key. Licensed providers must be configured separately and their license terms respected.

## How to Run

From this skill directory, initialize a local database:

```bash
python scripts/cmi.py init --db data/market.db
```

Ingest a CSV or JSON/JSONL corpus of job postings:

```bash
python scripts/cmi.py import-postings \
  --db data/market.db \
  --input /path/to/postings.csv \
  --source public-corpus
```

Analyze a target role:

```bash
python scripts/cmi.py analyze \
  --db data/market.db \
  --title "Senior Data Analyst" \
  --location "Denver" \
  --candidate /path/to/candidate.json \
  --out report.md
```

If a legitimate applicant-outcome dataset is available, ingest it separately:

```bash
python scripts/cmi.py import-outcomes \
  --db data/market.db \
  --input /path/to/outcomes.csv \
  --cohort internal-study
```

Then rerun `analyze`; outcome associations are reported only when minimum sample thresholds are met.

## Quick Reference

```bash
python scripts/cmi.py init --db data/market.db
python scripts/cmi.py import-postings --db data/market.db --input jobs.csv --source corpus-name
python scripts/cmi.py import-outcomes --db data/market.db --input outcomes.csv --cohort study-name
python scripts/cmi.py import-onet --db data/market.db --directory /path/to/ONET-db
python scripts/cmi.py import-oews --db data/market.db --input /path/to/oews.txt
python scripts/cmi.py analyze --db data/market.db --title "Data Analyst" --out report.md
python scripts/cmi.py analyze --db data/market.db --title "Data Analyst" --json --out report.json
python scripts/opm_fwd.py latest accessions
python scripts/opm_fwd.py download accessions --year 2026 --month 5
python -m unittest discover -s tests -v
```

## Procedure

1. **Define the target market.** Resolve title, seniority, geography, industry, and time window. If the user gives only a title, analyze the broad market and explicitly label it broad. Completion criterion: the report states the exact filters used.

2. **Establish source provenance.** Prefer official/open sources for occupational baselines and lawfully obtained vacancy/outcome data for current demand. Record source, collection date, and sample count. Completion criterion: every metric family in the report names its evidence class and source.

3. **Map the occupation.** If O*NET data is loaded, match the title to the closest O*NET-SOC occupation and use O*NET skill/technology/experience fields as an occupational baseline, not as hiring-outcome evidence. Completion criterion: mapping is shown with its title and code or explicitly marked unavailable.

4. **Measure posting demand.** Compute skill prevalence, Wilson confidence intervals, target-vs-comparison lift, recent trend, co-occurrence bundles, requested experience, and education mentions. Completion criterion: sample size and date range accompany all posting statistics.

5. **Analyze outcomes only if valid outcome data exists.** Calculate hire-rate differences, risk ratios, odds ratios, and confidence intervals for non-sensitive candidate attributes. Suppress unstable estimates below thresholds. Completion criterion: results are labeled `OUTCOME-ASSOCIATED`, never `CAUSAL`, unless causal evidence comes from a separate credible study.

6. **Compare the candidate to the market.** Treat candidate data as evidence, not a license to infer. Classify high-demand evidenced skills as `EMPHASIZE`; high-demand unsupported skills as `GAP / DO NOT CLAIM`; lower-demand evidenced skills as `SECONDARY`. Completion criterion: no unsupported qualification appears as a resume recommendation.

7. **Report uncertainty.** Include sample size, missingness, source limitations, time coverage, and selection-bias warnings. Completion criterion: the report contains a limitations section and a confidence label.

8. **Translate into resume strategy.** Recommend ordering, prominence, terminology, and evidence selection only. Never fabricate experience or optimize around protected characteristics. Completion criterion: each recommended resume skill maps to candidate evidence or is clearly labeled a development gap.

## Evidence Rules

Use these labels exactly:

- `DEMAND`: observed in job postings or occupational requirement data.
- `OUTCOME-ASSOCIATED`: statistically associated with interviews/offers/hires in an outcome dataset.
- `CAUSAL`: supported by a study design that credibly estimates a causal effect.
- `CANDIDATE-EVIDENCED`: supplied or verified candidate capability.
- `GAP / DO NOT CLAIM`: demanded by the market but not evidenced by the candidate.

Never report a numeric probability that a particular person will be hired. Aggregate rates are permitted when the underlying dataset supports them and the denominator is shown.

## Sensitive-Attribute Guardrails

Do not use protected or sensitive characteristics to recommend resume changes, calculate a person's hireability, or advise an employer. Exclude fields such as race, ethnicity, sex, gender, age, disability, religion, national origin, pregnancy, genetic information, sexual orientation, and comparable protected characteristics from predictive recommendations. Treat veteran status cautiously: it can matter under specific public-sector preference rules, but it must not be generalized into private-sector hireability scoring.

Do not use ZIP code, school, name, or similar variables as covert proxies for protected characteristics. Prefer job-relevant, auditable features: demonstrated skills, experience, credentials, work samples, responsibilities, and measurable outcomes.

## Statistical Interpretation

Read `references/methodology.md` before interpreting outcome associations or small samples. Minimum defaults in the scripts are conservative:
- posting prevalence: flag `LOW` confidence below 30 matched postings;
- outcome association: suppress below 50 total observations or when either exposed/unexposed group has fewer than 10 observations;
- avoid lift claims when the comparison prevalence is based on fewer than 20 postings;
- always show the denominator.

Do not equate `P(skill | hired)` with `P(hired | skill)`. Do not interpret correlation as causation. Do not combine heterogeneous sources into a single opaque "ATS" or "hireability" score.

## Data Sources

Read `references/data-sources.md` before downloading or publishing third-party data. The recommended open-data stack is:
- O*NET database for occupational skills, software, training/experience, and task baselines;
- BLS OEWS and Employment Projections for wages, employment, growth, openings, and education benchmarks;
- OPM Federal Workforce Data for observed federal accessions/separations/headcount;
- USAJOBS for current federal vacancy demand;
- lawfully obtained public or user-provided vacancy corpora for private-sector demand;
- optional licensed workforce/profile datasets for broader observed-transition analysis.

## Pitfalls

1. **Keyword frequency is not hiring probability.** Call it demand prevalence.
2. **Profiles of people in a role are not rejected-applicant controls.** Call them entrant/incumbent benchmarks.
3. **A required skill can have little differentiation.** High prevalence may indicate a baseline requirement rather than a competitive advantage.
4. **Small samples create unstable lifts.** Suppress or downgrade confidence.
5. **Title matching can mix occupations.** Inspect matched titles and narrow filters when needed.
6. **Scraped data can violate site terms or be biased.** Prefer official APIs, licensed datasets, or user-provided exports.
7. **Market demand changes.** Include collection dates and favor recent windows for fast-moving skills.
8. **A gap is not permission to fabricate.** Recommend learning or alternate evidence, not insertion.
9. **Federal outcomes are not the private market.** Keep OPM findings scoped to federal employment.
10. **Do not automate employment decisions.** This skill is for job-seeker research and aggregate labor-market analysis.

## Verification

- [ ] `SKILL.md` has valid YAML frontmatter and a non-empty body.
- [ ] `python scripts/cmi.py init --db <temp.db>` succeeds.
- [ ] Synthetic posting import and analysis complete without third-party packages.
- [ ] Outcome associations are suppressed below configured sample thresholds.
- [ ] Candidate skills absent from evidence are labeled `GAP / DO NOT CLAIM`.
- [ ] Reports distinguish `DEMAND`, `OUTCOME-ASSOCIATED`, and `CAUSAL` evidence.
- [ ] Source dates, denominators, and limitations are present.
- [ ] `python -m unittest discover -s tests -v` passes.
