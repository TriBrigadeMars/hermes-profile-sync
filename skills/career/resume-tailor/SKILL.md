---
name: resume-tailor
description: Tailor an existing resume to a target job by selecting, ordering, and phrasing only supported candidate evidence.
version: 0.1.0
author: Local contributor, Hermes Agent
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [career, resume, tailoring, job-description]
    related_skills: [job-description-analyzer, career-profile, resume-ats-auditor, career-gap-analyzer]
---
# Resume Tailor

Tailor by **selection, ordering, emphasis, and truthful terminology**, not by manufacturing qualifications.

Read:
- `../_career-writing-shared/references/evidence-policy.md`
- `../_career-writing-shared/references/resume-principles.md`
- `../_career-writing-shared/references/market-integration.md`

## Inputs

Prefer:
- candidate evidence profile;
- current resume;
- analyzed job description;
- optional `career-market-intelligence` report.

## Procedure

1. Map JD requirements and responsibilities to candidate evidence.
2. Classify each important target term as supported, adjacent/partial, or unsupported.
3. Reorder sections and bullets so the strongest supported match appears earlier.
4. Use JD terminology when it accurately describes the evidence.
5. Remove or compress low-relevance content before adding length.
6. Preserve truthful chronology, titles, scope, and outcomes.
7. For unsupported high-demand terms, create a `GAP / DO NOT CLAIM` note rather than adding the term.
8. Run the ATS auditor after tailoring.

## Market integration

If market data says a skill is common or rising:
- emphasize it only when candidate evidence supports it;
- otherwise keep it in the development-gap section outside the resume.

## Completion criteria

Return a tailored document plus a concise change summary explaining what was emphasized, de-emphasized, and left out due to missing evidence.
