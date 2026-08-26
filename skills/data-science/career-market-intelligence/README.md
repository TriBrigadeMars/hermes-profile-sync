# Career Market Intelligence — Hermes Skill

A local-first Hermes skill for analyzing which job-relevant skills, experiences, credentials, and benchmarks are most prevalent in a target labor market, and—when legitimate applicant-outcome data exists—which attributes are statistically associated with observed outcomes.

It is built for **job-seeker research and resume strategy**, not automated employment decisions.

## What makes it different

The skill refuses to collapse labor-market evidence into a fake "hireability" or "ATS" score. It keeps these categories distinct:

- **DEMAND** — what postings or occupational sources request;
- **OUTCOME-ASSOCIATED** — what correlates with hires/interviews/offers in a supplied outcome dataset;
- **CAUSAL** — only evidence from a study design capable of supporting causal claims;
- **CANDIDATE-EVIDENCED** — qualifications the candidate can actually support;
- **GAP / DO NOT CLAIM** — desirable market attributes the candidate has not evidenced.

## Install in Hermes

Unzip this folder, then run:

```bash
python scripts/install.py
```

The default destination is:

```text
~/.hermes/skills/data-science/career-market-intelligence/
```

Start a new Hermes session after installation so the skill index reloads.

## Core usage

```bash
python scripts/cmi.py init --db data/market.db
python scripts/cmi.py import-postings --db data/market.db --input jobs.csv --source my-corpus
python scripts/cmi.py analyze --db data/market.db --title "Senior Data Analyst" --location "Denver" --out report.md
```

Add a candidate profile:

```bash
python scripts/cmi.py analyze \
  --db data/market.db \
  --title "Senior Data Analyst" \
  --location "Denver" \
  --candidate examples/candidate.json \
  --out report.md
```

## Supported data layers

The package ships no government or proprietary dataset. It provides import/adaptation paths for:

1. current or historical job-posting corpora supplied by the user;
2. O*NET occupational data downloaded from the official O*NET Resource Center;
3. BLS OEWS delimited exports for wages/employment;
4. OPM Federal Workforce Data via the included public API adapter;
5. de-identified applicant-outcome datasets with job-relevant attributes;
6. optional licensed labor-market datasets through future adapters.

See `references/data-sources.md` and `references/schema.md`.

## Statistical outputs

For job postings, the core engine calculates:

- skill prevalence;
- 95% Wilson intervals;
- target-vs-comparison prevalence lift;
- early-vs-late trend change;
- common skill-pair bundles;
- requested-experience median and quartiles;
- education mentions.

For valid outcome datasets it can calculate:

- hire rate with vs. without a skill;
- risk difference;
- risk ratio and approximate confidence interval;
- odds ratio;
- automatic suppression for small groups.

These are observational associations, not automatic causal estimates.

## Data format

See `references/schema.md`. Postings can be CSV, JSON, or JSONL. A `skills` field is ideal; when it is absent, the local seed taxonomy is matched against the description. Replace or extend `data/seed_skills.csv` for specialized professions.

## O*NET

After downloading and extracting a current O*NET tabular database release:

```bash
python scripts/cmi.py import-onet --db data/market.db --directory /path/to/onet-files
```

The importer looks for occupation, essential/transferable skill, software skill, training/experience, education, and job-zone files.

## BLS OEWS

For a delimited OEWS export containing the standard occupation/area/wage fields:

```bash
python scripts/cmi.py import-oews \
  --db data/market.db \
  --input oews_data.txt \
  --source-date 2025-05 \
  --replace
```

## OPM Federal Workforce Data

List the latest public accessions file:

```bash
python scripts/opm_fwd.py latest accessions
```

Download it to the local cache:

```bash
python scripts/opm_fwd.py download accessions --year 2026 --month 5
```

Inspect/group a Parquet file after installing optional pandas/pyarrow:

```bash
python scripts/opm_fwd.py summary --input /path/to/accessions.parquet --by occupational_series
```

## Outcome data safety

The importer rejects datasets containing columns whose names appear to encode protected/sensitive traits. The override exists only for reviewed storage compatibility; the core analysis still does not use those fields.

Do not use this project to rank or screen applicants for an employer. Do not use protected characteristics or proxies to predict employment outcomes.

## Test

```bash
python -m unittest discover -s tests -v
```

## License

Skill code and original documentation: MIT. External datasets retain their own licenses and attribution requirements; see `references/data-sources.md`.
