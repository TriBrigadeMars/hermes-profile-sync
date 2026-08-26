---
name: career-gap-analyzer
description: Compare candidate evidence with a job description and optional labor-market data to distinguish strengths, partial matches, and development gaps.
version: 0.1.0
author: Local contributor, Hermes Agent
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [career, gaps, skills, labor-market]
    related_skills: [career-profile, job-description-analyzer, resume-tailor]
---
# Career Gap Analyzer

Distinguish what the candidate can already prove from what a job or broader market demands.

Read:
- `../_career-writing-shared/references/evidence-policy.md`
- `../_career-writing-shared/references/market-integration.md`

## Procedure

1. Compare each must-have and important preferred qualification against candidate evidence.
2. Classify:
   - `STRONG EVIDENCE`
   - `PARTIAL / ADJACENT EVIDENCE`
   - `GAP / DO NOT CLAIM`
   - `NEEDS CONFIRMATION`
3. If a market-intelligence report exists, identify which gaps are broadly demanded versus specific to this posting.
4. Keep development recommendations outside the resume unless completed and evidenced.
5. Prioritize gaps by job criticality and market relevance, not by arbitrary point totals.

## Deterministic helper

```bash
python ../_career-writing-shared/scripts/career_tools.py compare \
  --profile career-profile.json \
  --jd-analysis jd-analysis.json \
  --out gap-analysis.json
```

The helper performs literal term-to-evidence matching only; Hermes must assess semantic/transferable evidence.

## Do not

- calculate a personal hireability probability;
- use protected characteristics;
- convert an adjacent skill into an exact skill without evidence;
- put a learning recommendation into the resume as if already completed.
