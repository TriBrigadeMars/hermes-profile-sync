---
name: resume-builder
description: Build a truthful, ATS-readable resume from verified candidate evidence.
version: 0.1.0
author: Local contributor, Hermes Agent
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [career, resume, writing, ats]
    related_skills: [career-profile, resume-bullet-writer, resume-tailor, resume-ats-auditor]
---
# Resume Builder

Create a complete resume from candidate evidence. The resume is a factual marketing document, not a place to infer missing qualifications.

Read:
- `../_career-writing-shared/references/evidence-policy.md`
- `../_career-writing-shared/references/resume-principles.md`

## Procedure

1. Determine target role and intended resume type: general, targeted, executive, technical, academic/CV-like, or career-change.
2. Use only evidence supplied in the current task or the canonical career profile.
3. Select the most relevant evidence; do not force every career fact into the document.
4. Choose a clear section order appropriate to the target.
5. Write a summary only if it communicates specific supported positioning.
6. Build a skills section from evidenced skills; do not copy unsupported JD keywords.
7. Write experience bullets that distinguish action, scope, and outcome. Use metrics only when known.
8. Keep chronology and titles faithful to evidence.
9. Use standard, parseable headings and straightforward formatting.
10. Perform a final unsupported-claim pass before delivering.

## Required behavior for missing information

- Unknown metric: omit it or ask for it.
- Unknown tool: do not infer it.
- Ambiguous leadership: use the weakest accurate verb until clarified.
- Market-demand skill not evidenced: mark as gap, never insert.

## Completion criteria

- every candidate claim is evidence-backed;
- no fabricated metric, credential, date, tool, employer, or scope;
- role-relevant evidence appears earlier/more prominently than low-value material;
- output is readable without graphics or hidden text;
- no generic ATS score is reported.
