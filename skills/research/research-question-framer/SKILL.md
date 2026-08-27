---
name: research-question-framer
description: "Turn a broad topic into an answerable research question."
version: 1.0.0
author: Hermes Agent + Mars Cruz
license: MIT
metadata:
  hermes:
    tags: [research, study-design, question-framing]
    related_skills: [research-design-orchestrator]
---

# Stage 1: Research Question Framer

## When to Use
Use when Mars has a topic area or vague idea and needs it sharpened into specific, answerable research/evaluation questions. Runs standalone or as Stage 1 of `research-design-orchestrator`.

## Interactive Interview (via clarify tool — ask before doing anything)

Ask in rounds, not all at once. Adapt follow-ups to answers.

Round 1 — Scope:
- What is the health problem or topic, in your own words?
- Who is the population of interest? (age, geography, setting — e.g., campus, clinic, community)
- What do you already know about the problem (prior data, anecdotes, mandates)?

Round 2 — Intent:
- What would change or improve if this study went perfectly?
- Who is the audience for findings (funders, CU Anschutz leadership, community partners, journals)?
- Is there a theory or model you're expected to use (SCT, SEM, Diffusion of Innovations), or open?

Round 3 — Refinement:
Present 2–3 candidate research questions using the framework best fitting intent:
- **PICO(T)** — intervention/effectiveness studies
- **CIMO** (Context, Intervention, Mechanism, Outcome) — program evaluation
- **SPIDER** — qualitative/mixed methods
- **PSCo** (Population, Situation, Comparison) — descriptive/prevalence

For each candidate show: primary question, 1–3 secondary questions, and what decision the answer would inform. Mars picks one or edits; iterate until approved.

## Deliverable
`01_research_questions.md` containing: background paragraph, final primary + secondary questions, chosen framework with element mapping, target audience, and explicit scope boundaries (what is OUT of scope). Save to the working folder from the orchestrator, or ask Mars where to save when running standalone.

## Rules
- Tell any delegate_task child explicitly: use write_file to save the deliverable; never just print to stdout.
- Never finalize a question without Mars's explicit approval.
- Keep language plain enough for a community advisory board to read.
