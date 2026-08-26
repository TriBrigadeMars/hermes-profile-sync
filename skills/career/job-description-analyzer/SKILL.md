---
name: job-description-analyzer
description: Analyze a job description into requirements, responsibilities, terminology, seniority, and performance signals.
version: 0.1.0
author: Local contributor, Hermes Agent
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [career, resume, job-description, analysis]
    related_skills: [resume-tailor, career-gap-analyzer, cover-letter-writer]
---
# Job Description Analyzer

Analyze the employer's posting without confusing employer requirements with candidate qualifications.

Read `../_career-writing-shared/references/jd-analysis-contract.md`.

## Procedure

1. Identify the target title, organization, location, and seniority if stated.
2. Separate explicit `must_have` requirements from `preferred` qualifications.
3. Extract responsibilities and recurring work themes.
4. Identify tools, methods, credentials, domain terms, and measurable performance signals.
5. Identify seniority markers: years, ownership, decision authority, people management, budget scope, client responsibility, etc.
6. Mark ambiguous language rather than over-interpreting it.
7. Produce a concise role brief for downstream skills.

## Deterministic preflight

```bash
python ../_career-writing-shared/scripts/career_tools.py analyze-jd --jd job-description.txt --out jd-analysis.json
```

The script only inventories recognizable terms, years, education, and frequent words. Hermes must still perform semantic categorization.

## Output contract

Return:
- target role;
- must-have qualifications;
- preferred qualifications;
- responsibilities;
- tools/skills;
- seniority signals;
- performance signals;
- domain vocabulary;
- ambiguities/questions.

Do not produce a candidate-fit score in this skill.
