---
name: academic-research-suite-hermes
description: Use when conducting academic research, literature reviews, paper drafting, peer-review simulation, research integrity checks, or end-to-end research-to-publication planning. Provides structured modes for scoping, bibliography, synthesis, writing, revision, reviewer-response, and final verification while requiring explicit source-grounding and human confirmation for high-stakes claims.
version: 1.1.0
author: yanyintingyou; adapted from Imbad0202/academic-research-skills
license: CC-BY-NC-4.0
metadata:
  hermes:
    category: research
    tags: [academic, research, literature-review, paper-writing, peer-review, citation-audit, reproducibility]
    related_skills: [arxiv, academic-writing-assistant, ocr-and-documents]
  compatibility:
    agents: [Hermes, Claude Code, Codex, Cursor, OpenAI Agents, generic-agent]
---

# Academic Research Suite — Agent Skill

## Overview

This skill turns an AI coding/research agent into a disciplined academic research assistant. It is designed for literature review, research design, manuscript drafting, peer-review simulation, revision planning, citation checking, and final research-integrity review.

Core principle: **the agent assists; the human researcher remains responsible for research questions, methodology, interpretation, and final claims.** The skill must not invent citations, fabricate results, or silently skip verification.

## When to Use

Use this skill when the user asks for:

- Literature review, systematic review, PRISMA-style screening, or annotated bibliography
- Research question refinement, conceptual framework, or methodology design
- Academic paper outline, section drafting, abstract, introduction, literature review, or conclusion
- Peer-review simulation, reviewer-response drafting, or revision planning
- Citation consistency checks, claim-evidence mapping, or source verification
- End-to-end research-to-publication workflow planning

Do **not** use this skill for:

- Pure coding/debugging tasks with no research component
- Casual web search without scholarly synthesis
- Final factual claims that cannot be traced to real sources
- Medical/legal/financial advice without explicit uncertainty and source checks

## Operating Modes

Choose the smallest useful mode. If the user is uncertain, start with `socratic` or `plan` instead of producing a full paper.

- `socratic`: clarify the topic, scope, research question, feasibility, and contribution.
- `quick-brief`: produce a short source-grounded research brief.
- `literature-review`: search, screen, cluster, synthesize, and identify gaps.
- `systematic-review-plan`: design protocol, inclusion/exclusion criteria, search strings, and extraction schema.
- `paper-plan`: create title options, abstract skeleton, section outline, argument map, and evidence needs.
- `draft-section`: draft one manuscript section from verified notes/sources.
- `full-draft`: draft a complete manuscript only after source corpus and methodology are clear.
- `peer-review`: simulate multi-perspective journal review without rewriting the manuscript.
- `revision-coach`: parse reviewer comments into a revision roadmap and response-letter structure.
- `integrity-audit`: verify references, citation-to-claim alignment, data/figure claims, and unresolved limitations.

## Required Workflow

1. **Clarify task and scope**
   - Identify field, target output, language, citation style, target journal/venue if any, and deadline constraints.
   - Ask only for missing information that materially changes the output.

2. **Collect or verify sources**
   - Prefer first-party scholarly sources: journal articles, books, working papers, official datasets, and replication packages.
   - For every cited source, preserve enough metadata: author, year, title, venue, DOI/URL, and access date when relevant.
   - If tools are available, use them to verify current metadata rather than relying on memory.

3. **Build a claim-evidence map**
   - Separate facts, interpretations, hypotheses, and recommendations.
   - Mark each substantive claim with one or more supporting sources.
   - Flag unsupported claims instead of hiding uncertainty.

4. **Draft or review**
   - Use formal academic style unless the user requests otherwise.
   - Keep citations close to the claims they support.
   - Avoid generic AI phrases, exaggerated novelty claims, and unsupported causal language.

5. **Run integrity checks before final output**
   - No fabricated references.
   - No citation without a matching claim.
   - No claim whose scope exceeds the evidence.
   - Methods, data, and limitations are explicit.
   - If output is a paper or review, include unresolved issues and next steps.

## Academic Quality Rules

- Use cautious causal language unless identification is credible.
- Distinguish correlation, mechanism, causal identification, and policy implication.
- For empirical work, state sample period, unit of observation, variables, identification strategy, and robustness expectations.
- For literature reviews, separate schools of thought, methods, findings, contradictions, and gaps.
- For peer review, be critical but constructive; give actionable fixes.
- For bilingual work, preserve technical terms and ensure Chinese and English abstracts are semantically aligned.

## Citation and Source Integrity

When citing literature in prose, prefer this style when enough metadata is available:

- `Author (Year, Journal)` for inline discussion.
- Full reference list only when the source metadata has been checked.

Never create fake DOI, page number, journal name, volume, issue, or author list. If metadata is incomplete, write `metadata incomplete` and explain what must be verified.

For high-stakes claims, use a three-layer anchor when possible:

1. Exact quote or extracted passage
2. Page, section, table, figure, or paragraph location
3. Explanation of how the source supports the claim

## Peer-Review Simulation

For `peer-review`, produce independent reports from these perspectives:

- Editor-in-Chief: fit, originality, contribution, publishability
- Methods reviewer: identification, measurement, statistics, reproducibility
- Domain reviewer: theory, literature positioning, contribution
- Robustness reviewer: alternative explanations, sensitivity, data limitations
- Devil's advocate: strongest objections and failure modes

Then synthesize:

- Decision: accept / minor revision / major revision / reject / not enough information
- Top 3 blocking issues
- Revision roadmap
- Must-fix vs nice-to-have items

Review mode is read-only: do not rewrite the manuscript unless the user explicitly asks for revision.

## Output Templates

### Literature Review Brief

```markdown
# Literature Review Brief: <topic>

## Research Question
...

## Search Scope
- Databases/tools:
- Keywords:
- Inclusion criteria:
- Exclusion criteria:

## Main Streams of Literature
1. ...
2. ...

## Key Findings
- Claim — source(s) — confidence

## Contradictions and Gaps
...

## Implications for This Project
...

## Sources to Verify Further
...
```

### Integrity Audit

```markdown
# Research Integrity Audit

## Summary Verdict
Pass / Pass with warnings / Fail

## Citation Audit
- Verified:
- Incomplete metadata:
- Unsupported or overextended claims:

## Methods/Data Audit
- Sample and variables clear?
- Identification credible?
- Robustness needed?

## Required Fixes Before Submission
1. ...
```

## .docx Output Formatting

When producing .docx deliverables from this skill's outputs, follow these standards:

### Heading Hierarchy (APA 7 §2.27 + Section 508 §1.3.1)

Use Word's built-in styles to create a navigable, accessible outline:

| Style | Use | APA 7 Format |
|-------|-----|--------------|
| **Title** | Document title (one per document) | Centered, Bold, Title Case |
| **Heading 1** | Major sections (Introduction, Methods, Results, Discussion, References) | Centered, Bold, Title Case |
| **Heading 2** | Subsections within a Heading 1 | Flush Left, Bold, Title Case |
| **Heading 3** | Sub-subsections within a Heading 2 | Flush Left, Bold Italic, Title Case |

**Rules:**
- Never skip levels (e.g., Heading 1 → Heading 3).
- At least two subsections at any level, or none (no lone subsection).
- The Title style is distinct from Heading 1 — use it for the document's name, not for section headings.
- The paper title at the top of page 1 acts as a de facto Level 1 heading; do NOT use an "Introduction" heading (APA 7 convention).

### Font and Spacing
- Arial 12pt throughout (body text and headings).
- Double-spaced body and headings (`WD_LINE_SPACING.DOUBLE`).
- 1-inch margins all sides.

### Accessibility Compliance (Section 508 / WCAG 2.2)
- **Document title:** Set `doc.core_properties.title` to the document's name.
- **Language:** Set `doc.core_properties.language = "en-US"`.
- **Heading hierarchy:** No skipped levels; screen readers use headings to navigate.
- **Reading order:** Sequential paragraph order; no floating text boxes.
- **Color contrast:** Black on white (21:1 ratio) — avoid colored text.

## Compatibility Notes for Agents

- **Hermes**: copy `skills/research/academic-research-suite-hermes/` into `~/.hermes/skills/research/` or keep this repository as a skill tap if supported.
- **Claude Code**: the repository-level compatibility adapter points Claude to this `SKILL.md`.
- **Codex / OpenAI agents**: `agent instruction file` points Codex-style agents to this `SKILL.md`.
- **Cursor**: `IDE rule adapter directory/academic-research-suite.mdc` and `Cursor rule adapter` provide Cursor-compatible loading hints.
- **Generic agents**: use the root `SKILL.md` as the canonical instruction file.

## Supporting Reference Protocols

This skill also ships optional reference protocols under `references/`:

- `devils-advocate-protocol.md` — structured assumption challenge and counter-argument review.
- `integrity-verification-protocol.md` — blocking citation, data, and claim-integrity audit.
- `socratic-mode-protocol.md` — guided research-question refinement workflow.
- `writing-quality-checklist.md` — academic style and AI-writing anti-pattern checks.

Use these references when the task needs deeper rigor than the compact workflow above.

## Common Pitfalls

1. **Fabricated citations** — never cite a paper unless it was provided or verified.
2. **Over-scoping** — a broad topic should first become a focused research question.
3. **Sycophantic revision** — do not accept every reviewer/user suggestion uncritically; assess trade-offs.
4. **Methods hand-waving** — empirical papers require variables, sample, model, identification, and limitations.
5. **Review-mode rewriting** — peer review should diagnose before rewriting.
6. **No audit trail** — preserve source metadata, search terms, and unresolved uncertainties.

## Verification Checklist

- [ ] User intent and output type identified
- [ ] Research scope and assumptions explicit
- [ ] Sources are real, traceable, and sufficiently described
- [ ] Main claims have evidence anchors or are flagged as unsupported
- [ ] Methods/data limitations are stated where relevant
- [ ] Review/revision outputs distinguish must-fix from optional improvements
- [ ] Final answer includes unresolved risks rather than hiding them
