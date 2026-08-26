---
name: career-profile
description: Build and maintain a canonical evidence profile for truthful resume and cover-letter writing.
version: 0.1.0
author: Local contributor, Hermes Agent
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [career, resume, evidence, profile]
    related_skills: [job-description-analyzer, resume-builder, cover-letter-writer, career-gap-analyzer]
---
# Career Profile

Use this skill to turn user-supplied career facts into a canonical evidence base that downstream writing skills can safely reuse.

Read `../_career-writing-shared/references/evidence-policy.md` before creating or updating claims.

## When to use

Use when the user wants to:
- create a reusable career profile;
- consolidate multiple resumes, notes, portfolios, or career-history documents;
- verify what can safely be claimed in future applications;
- add a new achievement, skill, credential, project, or role to their evidence base.

## Procedure

1. Collect candidate facts from the user's supplied materials or statements.
2. Preserve source wording when uncertainty matters; do not silently infer missing dates, scope, metrics, technologies, or authority.
3. Normalize each usable fact into a discrete evidence item with a stable ID.
4. Assign one status: `confirmed`, `user-supplied`, `document-derived`, or `needs-confirmation`.
5. Add tags that make later matching easier, but do not use tags to strengthen the claim.
6. Flag contradictions or ambiguous chronology for user review.
7. Keep personally sensitive information out unless necessary for the requested application material.

## Local helper

Create a profile:

```bash
python ../_career-writing-shared/scripts/career_tools.py init-profile --out career-profile.json
```

Add evidence:

```bash
python ../_career-writing-shared/scripts/career_tools.py add-evidence \
  --profile career-profile.json \
  --type achievement \
  --text "..." \
  --tags "..."
```

Validate:

```bash
python ../_career-writing-shared/scripts/career_tools.py validate-profile --profile career-profile.json
```

## Completion criteria

- every affirmative downstream claim can map to one or more evidence items;
- no `needs-confirmation` item is presented as established fact;
- contradictions are surfaced, not resolved by choosing the more impressive version;
- no job-description or market term has been inserted into the profile without candidate evidence.
