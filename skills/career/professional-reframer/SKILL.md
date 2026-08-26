---
name: professional-reframer
description: Reframe real work experience into clear, credible, business-legible language for LinkedIn and other professional contexts without inflating scope, authority, outcomes, or expertise.
version: 0.1.0
author: Local contributor, Hermes Agent
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [career, linkedin, writing, professional-branding, experience, reframing]
    related_skills: [career-profile, job-description-analyzer, career-market-intelligence, resume-builder, resume-tailor]
---
# Professional Reframer

Turn truthful experience into professional language that is easier for corporate readers, recruiters, hiring managers, and LinkedIn audiences to understand.

The objective is **professional reframing, not corporate-speak generation**.

Core rule:

> Change the framing, not the facts.

Read these references when relevant:
- `references/methodology.md`
- `references/claim-integrity.md`
- `references/responsibility-calibration.md`
- `references/business-function-taxonomy.md`
- `references/anti-corporate-sludge.md`
- LinkedIn tasks: `references/linkedin-headline.md`, `references/linkedin-about.md`, `references/linkedin-experience.md`
- Story-heavy tasks: `references/storytelling.md`
- Concision pass: `references/brevity-and-clarity.md`
- Target-role language: `references/keyword-integration.md`

## Default behavior

When the user supplies work experience and asks to make it more professional, corporate, polished, LinkedIn-ready, business-oriented, or executive-sounding:

1. Extract the factual claims first.
2. Identify the business functions the facts genuinely demonstrate.
3. Calibrate responsibility and authority.
4. Identify supported impact, scale, stakeholders, systems, and outcomes.
5. Tailor emphasis to the intended audience or target role if supplied.
6. Rewrite in concise, human professional language.
7. Perform a claim-delta audit before returning the revision.

Do **not** increase seniority merely because the user asks for stronger language.

## Primary modes

### Professional Reframe
Translate informal, task-level, technical, academic, public-sector, nonprofit, frontline, or operational descriptions into recognizable business functions while keeping the original meaning.

### LinkedIn Reframe
Apply professional reframing plus LinkedIn-specific audience, headline, About, Experience, scanning, and keyword guidance.

### Find the Business Value
Do not rewrite yet. Explain what organizational functions, stakeholders, problems, and outcomes the user's work may represent. Mark uncertain interpretations as questions.

### Strengthen With Evidence
Identify where verified scope, volume, stakeholders, metrics, outcomes, tools, or decisions would materially strengthen the description. Ask targeted questions instead of inventing details.

### De-Jargon
Retain legitimate business concepts while removing inflated, vague, clichéd, or status-signaling language.

### Explain the Rewrite
Return the revision and a concise explanation of material wording choices, including any stronger wording deliberately avoided because evidence was insufficient.

## Reframing depth

Use the least aggressive level that meets the request.

- **Light:** polish clarity and diction; preserve structure.
- **Professional:** translate tasks into supported business functions and clarify purpose/impact.
- **LinkedIn:** professional framing + scannability + target audience + relevant keywords + human voice.
- **Narrative:** add concise context, challenge, response, outcome, or learning where supported.
- **Executive-evidence-only:** use strategic/executive framing only when facts demonstrate decision authority, organizational ownership, strategy formation, material resource responsibility, or executive influence.

Never treat these levels as permission to exaggerate.

## Evidence classes

Classify material claims internally as:

- **CONFIRMED:** directly supplied by the user or canonical career profile.
- **SUPPORTED INTERPRETATION:** a business-function label reasonably entailed by confirmed facts.
- **NEEDS CONFIRMATION:** plausible but not established.
- **UNSUPPORTED:** must not appear as a candidate claim.

Examples:

- "showed new hires how to use the database" -> `user training` or `onboarding support` can be a supported interpretation.
- "answered questions from coworkers" -> `stakeholder management` is not automatically supported.
- "helped with a project" -> `led the project` is unsupported.

## Hard claim-integrity rules

Do not invent or silently upgrade:

- leadership or people management;
- ownership or decision authority;
- budgets, savings, revenue, percentages, counts, or time reductions;
- organization-wide, enterprise-wide, global, or executive scope;
- strategy creation from strategy execution/support;
- proficiency or expertise from tool usage;
- certifications, credentials, degrees, titles, or promotions;
- client-facing responsibility from internal collaboration;
- project/program management from simple participation;
- measurable impact where only activity is known.

Never automatically transform:

- helped -> led
- participated -> drove
- supported -> owned
- contributed -> directed
- used -> expert in
- organized -> managed
- suggested -> advised executives
- trained coworkers -> led organizational change

If a stronger term may be accurate, ask or mark `NEEDS CONFIRMATION`.

## Core pipeline: Evidence -> Function -> Impact -> Relevance -> Voice

### 1. Evidence
List or mentally extract only what is known: action, object, audience, scope, tool, challenge, decision, outcome, frequency, and scale.

### 2. Function
Map concrete work to recognizable organizational functions. Use `references/business-function-taxonomy.md`.

Do not replace ordinary verbs merely to sound corporate. Prefer the clearest accurate term.

### 3. Impact
Ask "why did this work matter?" Use verified outcomes when present. If missing, write accurately without a metric or ask for one.

### 4. Relevance
If a target role, job description, or labor-market report exists, emphasize supported concepts that matter to that audience. Market demand changes prominence, not truth.

### 5. Voice
Write for a smart, busy human. Prefer active verbs, concrete nouns, short sentences, clear hierarchy, and natural professional language. Remove jargon that does not add meaning.

## Claim-delta audit

Before finalizing, compare the revision with the evidence.

Flag any newly introduced concept involving:
- ownership;
- leadership;
- strategic authority;
- executive exposure;
- scale;
- financial impact;
- quantified result;
- expertise;
- enterprise/global reach;
- direct responsibility for an outcome.

If not supported, remove it or ask for confirmation.

The local helper can provide a conservative second check:

```bash
python scripts/reframe_guard.py compare --original original.txt --revised revised.txt
```

It is a heuristic warning system, not a factual verifier.

## LinkedIn-specific rules

### Headline
Make the professional value legible quickly. Prefer some combination of:
- function/specialty;
- who or what the person supports;
- credible outcome/value;
- target-relevant keywords.

Do not fill a headline with self-evaluative adjectives or generic status claims.

### About
Use a human professional voice, usually first person. Front-load the professional through-line and audience value. Add selective proof and specialties. Avoid an autobiography and avoid a copied resume summary.

### Experience
Treat each role as a concise professional micro-case study when evidence allows:
1. role purpose;
2. scope/context;
3. selected actions and impact;
4. optional challenge/learning or notable transformation.

Do not force storytelling into every entry. Recent and target-relevant roles deserve more detail.

## Keyword integration

Keywords are descriptors, not decorations.

Use a target keyword only when:
1. the evidence demonstrates the underlying function; and
2. the phrase accurately names that work.

If `career-market-intelligence` says a concept is in demand but evidence does not support it, classify it as a development gap outside the LinkedIn copy.

## Output defaults

For a simple reframe request, return:

**Reframed version**

Then, only when useful:

**What changed**
- business function clarified;
- impact made explicit;
- jargon removed;
- unsupported stronger claim avoided.

For ambiguous high-value claims, add:

**Could strengthen if confirmed**
- one or more specific questions.

Do not bury the requested rewrite under a long methodology explanation.

## Quality test

A successful rewrite should be:

- more legible to a business audience;
- at least as truthful as the original;
- specific enough to convey function;
- concise enough to scan;
- free of empty corporate sludge;
- appropriately confident without pretending to be more senior;
- recognizably human.

If the revision sounds like a generic consulting website, revise it again.
