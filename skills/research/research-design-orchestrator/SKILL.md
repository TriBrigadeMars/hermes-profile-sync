---
name: research-design-orchestrator
description: "Design a research study end-to-end via 4 interactive stages."
version: 1.0.0
author: Hermes Agent + Mars Cruz
license: MIT
metadata:
  hermes:
    tags: [research, study-design, methodology]
    related_skills: [prisma-systematic-review, research-question-framer, evaluation-method-selector, study-measures-and-sampling, study-protocol-builder]
---

# Research Study Design Orchestrator

## When to Use
Use when Mars wants to design a research study or evaluation from scratch — framing the question, choosing a methodology grounded in current research, planning measures/sampling, or compiling a full protocol.

**Sample-run mode:** when Mars says "run a sample study" without a real project, pick a common US oral-health or tobacco-control disparity, run all four stages autonomously (no clarify gates), generate both markdown and .docx, and clearly label the output as a demonstration.

Entry point for designing a research study from scratch. Runs FOUR stages interactively, asking Mars questions at every decision point. Each stage can also be run alone via its own skill (below).

## Audience Context
Mars Cruz, MPH, CHES — public health prevention/education/outreach researcher at CU Anschutz. Default lens: public health program evaluation, health education, community interventions. Still confirm scope — studies may be clinical, policy, or academic-theory oriented.

## Intake Questions (ask via clarify tool BEFORE anything else)

1. **Topic area** — free text. What is the health topic/population/problem?
2. **Study purpose** — choose: explore/describe | test an intervention | evaluate an existing program | measure prevalence/associations | other
3. **Stage of work** — new idea | pilot/feasibility planned | ready for full study | evaluating something already running
4. **Constraints** — funding/timeline/staffing realities, existing data sources, required deliverable (grant proposal section, IRB app, internal plan, thesis/dissertation chapter)
5. **Output format** — markdown only | .docx (Times New Roman 12pt double-spaced) | zip package (.md + .docx + .pptx summary)

Record answers; they flow into every stage's context.

## Pipeline

```
Stage 1: Question Framing      -> skill: research-question-framer
Stage 2: Methodology Selection -> skill: evaluation-method-selector   (live web research)
Stage 3: Measures & Sampling   -> skill: study-measures-and-sampling
Stage 4: Protocol Compilation  -> skill: study-protocol-builder       (.docx conversion here)
```

Run stages SEQUENTIALLY (Docker stability lesson from PRISMA runs). After each stage, show Mars a short summary and confirm before proceeding. If Mars corrects course mid-pipeline, carry the correction forward — never silently continue.

## Working Folder Convention
Create `~/study-design-{slug}-{timestamp}/` in the session workspace for intermediate files. Final deliverables go ONLY where Mars specifies (always ask; default offer C:\Users\cruzmars\Documents).

## Subagent Rules (from past-run lessons)
- Explicitly tell every delegate_task child: "Use the write_file tool to save your deliverable to {path}. Do not just print to stdout."
- Run children one at a time.
- List ALL prior-stage file paths in each child's context.
- Verify files exist with ls/search_files after each stage before moving on.

## Error Handling
- Web search fails in Stage 2: proceed with established methodology literature (CONSORT, TREND, RE-AIM, COREQ, MMAT) and clearly label recommendations as not verified against current publications.

## Journal-Weighted Search Policy (all live research in this pipeline)
Mars directive (2026-08): live searches MUST emphasize peer-reviewed research articles and journals even when paywalled. Target weighting: ~70% peer-reviewed journals/databases (PubMed, Cochrane, APA PsycInfo, SAGE/Elsevier/T&F methods journals), ~20% consensus/reporting standards tied to the literature (CONSORT, TREND, STROBE, COREQ, RE-AIM, MMAT), ≤10% gray literature (labeled). Paywalled is acceptable: cite from abstracts/summaries; never skip a relevant article because full text is gated. See `evaluation-method-selector` for the full table.
- Any stage failure: retry once with simplified context; always preserve partial output.
