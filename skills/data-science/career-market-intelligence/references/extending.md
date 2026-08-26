# Extending and "Training" the Skill

This package is designed to improve through **data augmentation and rule/taxonomy updates**, not by fine-tuning the underlying language model.

## 1. Extend the skill taxonomy

Copy `data/seed_skills.csv`, add occupation-specific skills, credentials, tools, methods, or experience signals, then pass the custom file:

```bash
python scripts/cmi.py import-postings \
  --db data/market.db \
  --input jobs.csv \
  --source corpus \
  --taxonomy /path/to/custom_skills.csv
```

Keep aliases specific enough to avoid false positives. Specialized taxonomies can represent credentials and experience signals such as `PMP`, `clinical trials`, `budget management`, `SOC 2`, or `grant writing`.

## 2. Add new market observations over time

`import-postings` is incremental by `(source, external_id)`. Re-importing a known posting updates it rather than duplicating it. Keep dated snapshots from legitimate sources so trend analysis reflects real changes.

## 3. Add outcome evidence

`import-outcomes` accepts de-identified applicant records containing job-relevant features and an observed status/hire outcome. This is the only local input that supports `P(hire | attribute)`-style descriptive rates. It still does not prove causality.

For useful outcome analysis, collect unsuccessful as well as successful applicants from comparable roles. A dataset containing only incumbents cannot estimate an applicant hire rate.

## 4. Add provider adapters

A provider adapter should transform external records into the schemas in `references/schema.md`. Keep credentials outside SKILL.md, obey rate limits and licenses, and store provenance/source dates in the local database.

Recommended adapter contract:

```text
provider -> normalized posting/outcome records -> cmi.py import -> SQLite -> analysis
```

Do not make the statistical engine depend on a single commercial provider.

## 5. Change statistical thresholds deliberately

The CLI exposes title-match and outcome sample thresholds. Tighten rather than loosen them when possible. If formal inference is needed, extend the analysis with a documented study design, covariate controls, multiple-comparison handling, and validation on held-out data.

## 6. Keep resume claims separate from market demand

Market data can change **what gets emphasized**, but it cannot create qualifications. Candidate evidence remains the source of truth for resume claims.
