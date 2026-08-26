---
name: resume-ats-auditor
description: Audit a resume for ATS readability, truthful keyword alignment, parsing risks, and evidence gaps without inventing an ATS score.
version: 0.1.0
author: Local contributor, Hermes Agent
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [career, resume, ats, audit]
    related_skills: [resume-builder, resume-tailor, job-description-analyzer, career-profile]
---
# Resume ATS Auditor

Review for likely parsing/readability problems and role terminology, while acknowledging that an employer's actual ATS rules are usually unknown.

Read `../_career-writing-shared/references/evidence-policy.md` and `../_career-writing-shared/references/resume-principles.md`.

## Audit categories

1. **Parsing/readability**: standard headings, coherent chronology, critical content in ordinary text, sensible abbreviations.
2. **JD terminology**: important job terms present or absent.
3. **Evidence support**: terms in the resume that are not supported by the supplied profile.
4. **Keyword integrity**: no stuffing, hidden keywords, or unnatural repetition.
5. **Clarity**: vague self-promotion, duty-only bullets, ambiguous scope.
6. **Completeness**: required application facts the user expects to include.

## Local preflight

```bash
python ../_career-writing-shared/scripts/career_tools.py ats-lint \
  --resume resume.txt \
  --jd job-description.txt \
  --profile career-profile.json
```

## Output contract

Use:
- `PASS`
- `MUST REVIEW`
- `SHOULD IMPROVE`
- `GAP / DO NOT CLAIM`

Report textual keyword presence as descriptive coverage only. Never label it "ATS score," "match probability," or "chance of interview."
