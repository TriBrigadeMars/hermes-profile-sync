---
name: study-protocol-builder
description: "Compile the full study protocol with .docx conversion."
version: 1.0.0
author: Hermes Agent + Mars Cruz
license: MIT
metadata:
  hermes:
    tags: [research, protocol, irb, documentation]
    related_skills: [research-design-orchestrator, apa-7-style-agent]
---

# Stage 4: Study Protocol Builder

## When to Use
Use when Stages 1–3 are complete (files exist) to compile everything into one coherent protocol document suitable for IRB drafting, grant sections, or internal planning.

## Intake (clarify tool)
1. Purpose of document: IRB application draft | grant proposal section | internal operations plan | thesis/dissertation chapter.
2. Format: markdown only | .docx (Arial 12pt double-spaced — Mars's standard) | zip package (.md + .docx + .pptx summary).
3. Any style requirement: APA 7 (offer `apa-7-style-agent` pass) or plain professional.

In an autonomous/sample run: assume internal operations plan format, generate BOTH markdown and .docx, and note that Mars can request APA formatting after review.

## Compilation Steps
1. Locate ALL prior-stage files (`01_*`, `02_*`, `03_*`). If any are missing, stop rather than inventing content.
2. Assemble protocol with standard sections: Title; Background & Significance; Specific Aims/Research Questions; Design & Methods; Measures; Sampling & Recruitment; Analysis Plan; Human Subjects Protections (consent, confidentiality, COI); Timeline & Milestones; Limitations; Dissemination Plan; References (from Stage 2/3 citation lists only).
3. Reconcile inconsistencies between stages — list every reconciliation made.
3. Generate .docx via python-docx with Arial 12pt double-spaced when requested. Use proper heading hierarchy:
   - **Title** style for the document title (one per document, centered, bold, title case)
   - **Heading 1** for major sections (centered, bold, title case)
   - **Heading 2** for subsections (flush left, bold, title case)
   - **Heading 3** for sub-subsections (flush left, bold italic, title case)
   - Never skip levels. Set `doc.core_properties.title` and `doc.core_properties.language` for accessibility.

## Save-Path Workflow (MANDATORY)
Before saving ANY final deliverable outside the working folder, ask Mars: "Where would you like me to save this?" Default offer: C:\Users\cruzmars\Documents\Hermes Research Output. Wait for the answer.

## Verification
After writing: ls the destination, confirm file sizes are nonzero, and for .docx re-open with python-docx to confirm it parses. Report verification results.

## Rules
- delegate_task children one at a time; require write_file usage and give them ALL file paths.
- References must come only from prior-stage verified lists — no new uncited claims.
