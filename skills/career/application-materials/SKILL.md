---
name: application-materials
description: Orchestrate evidence profile, job analysis, resume tailoring, ATS review, cover-letter writing, and gap analysis for a complete job application package.
version: 0.1.0
author: Local contributor, Hermes Agent
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [career, applications, resume, cover-letter, workflow]
    related_skills: [career-profile, job-description-analyzer, resume-builder, resume-tailor, resume-ats-auditor, cover-letter-writer, career-gap-analyzer]
---
# Application Materials Orchestrator

Use this skill when the user wants a coherent application package rather than one isolated document.

## Workflow

1. **Evidence** — invoke `career-profile`; validate candidate facts.
2. **Role analysis** — invoke `job-description-analyzer`.
3. **Gap analysis** — invoke `career-gap-analyzer`; optionally consume `career-market-intelligence`.
4. **Resume** — use `resume-builder` for a new document or `resume-tailor` for an existing one.
5. **Bullets** — invoke `resume-bullet-writer` where experience needs stronger concise phrasing.
6. **Audit** — invoke `resume-ats-auditor` and correct supported issues.
7. **Cover letter** — invoke `cover-letter-writer` using evidence complementary to the final resume.
8. **Consistency pass** — verify dates, titles, terminology, metrics, and claims agree across all materials.

## Package-level truth rules

- A fact appearing in one document must not contradict another.
- A JD or market term can guide emphasis but cannot create a candidate qualification.
- Unknown metrics remain unknown.
- Do not add a certification as "in progress" unless the user actually states that it is in progress.
- Do not create organization-specific praise from generic assumptions.

## Final output

When requested, deliver:
- tailored resume;
- cover letter;
- concise gap/development notes kept separate from application documents;
- optional ATS audit summary;
- optional evidence/claim traceability table for the user's review.
