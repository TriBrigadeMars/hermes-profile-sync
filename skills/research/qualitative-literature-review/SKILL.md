---
name: qualitative-literature-review
description: "Batch qualitative lit reviews with iterative theme tracking."
---

# Qualitative Literature Review

A workflow for conducting qualitative literature reviews when the user provides research articles (as markdown, PDFs, or files) in multiple batches. Unlike the PRISMA systematic review pipeline (which uses 6 subagents for formal systematic reviews), this is a **single-agent iterative workflow** suited for narrative/synthesizing reviews where the user provides the source material directly.

## When to Use

- User provides 10+ articles across multiple batches and wants a qualitative review
- User is NOT doing a formal PRISMA systematic review (no PROSPERO registration, no formal screening protocol)
- User wants a narrative synthesis with themes, not a meta-analysis with effect sizes
- User has already curated the articles (they're providing them, not asking you to search)

## Workflow

### Phase 1: Batch Ingestion (per batch)

For each batch the user provides:

1. **Read all articles** in the batch. For each, produce a structured digest:

```
### Article N: Author (Year) — Short Title

| Field | Summary |
|-------|---------|
| **Type** | Study design (qualitative, quantitative, framework, policy, etc.) |
| **Key Finding(s)** | 2-3 bullet points of most important results |
| **Methods** | Brief description if applicable |
| **Relevance to Review** | How this connects to the review's central question |
```

2. **Update cross-cutting themes table** after each batch. This is the CORE analytical artifact:

```
| Theme | Batch 1 | Batch 2 | Batch 3 | Refined Insight |
|-------|---------|---------|---------|-----------------|
| Theme name | Articles supporting | New articles | New articles | Evolved understanding |
```

- New themes may emerge with each batch — add them
- Existing themes may split or merge — note this
- Each theme should have a clear "Refined Insight" that evolves as evidence accumulates

3. **Report to user** with the digest and updated themes table. Ask for the next batch.

### Phase 2: Synthesis (after all batches)

Once all batches are ingested, write the qualitative review manuscript:

**Standard structure:**
1. **Abstract** — 200-300 words summarizing scope, methods, key findings, and recommendations
2. **Introduction** — Problem scope, prevalence data, consequences, review purpose
3. **Theoretical Frameworks** — 2-3 guiding frameworks (e.g., SEM, prevention science, intersectionality)
4. **Current Landscape** — Regulatory context, policy history, compliance-vs-prevention tension
5. **What Works** — Evidence-based strategies with specific program names and effect sizes
6. **Persistent Gaps** — 4-6 challenges identified across the literature
7. **Lessons Learned / Recommendations** — 6-10 evidence-based recommendations, each citing specific studies
8. **Conclusion** — Synthesis paragraph + call to action
9. **References** — Full APA 7 reference list

**Writing conventions:**
- Use formal academic prose but keep it accessible
- Every claim should cite at least one source from the ingested articles
- Recommendations should be numbered and actionable
- The cross-cutting themes table directly informs the "What Works" and "Gaps" sections

### Phase 3: Supplementary Search (optional)

If the user wants additional sources, search the web for:
- Recent (last 2-3 years) systematic reviews or meta-analyses on the topic
- Federal reports or technical packages (CDC, DOJ, DOE)
- Landmark studies the existing articles reference but weren't provided

## Pitfalls

- **Don't wait for all batches to start tracking themes.** Update the themes table after EACH batch — this is what makes the synthesis iterative rather than a flat list.
- **Don't produce a simple annotated bibliography.** The value is in the cross-cutting themes and synthesis, not in summarizing articles one by one.
- **Duplicate articles across batches** — watch for this. If the same article appears twice (different filenames, same content), note it and skip the duplicate.
- **The themes table is the analytical backbone.** If you lose it or don't update it, the final synthesis will read as disconnected summaries rather than a coherent review.
- **Large file writes** — if the `write_file` tool isn't available, use `execute_code` with Python to write files in chunks. The `write_file` function in `skill_manage` writes skill support files only, not arbitrary output files.
- **Context compaction risk** — for very long reviews (20+ articles), the article digests can exceed context limits. Keep digests concise (5-7 rows per article table). The full article text is already in context via file injection; the digest is for cross-referencing, not replication.

## Output Files

```
/research/
├── qualitative_review_{topic_slug}.md     # Final manuscript
├── article_digests.md                     # All digests across batches (optional)
└── cross_cutting_themes.md                # Final themes table (optional)
```

## Differences from PRISMA Pipeline

| Aspect | PRISMA Pipeline | This Workflow |
|--------|----------------|---------------|
| Agents | 6 subagents, sequential | 1 agent, iterative |
| Sources | Web search + PDF upload | User-provided files |
| Output | Meta-analysis + effect sizes | Narrative synthesis |
| Structure | Formal PRISMA checklist | Flexible academic review |
| Screening | Two-stage protocol | User pre-curated |
| Statistics | R meta-analysis code | Qualitative themes |

## Save-Path Workflow

**IMPORTANT:** Before saving any deliverable (literature review, thematic synthesis, article summaries), ask the user:
- "Where would you like me to save this? (e.g., C:\Users\cruzmars\Documents)"
- Wait for user response before saving to the specified location.
- If user does not specify, default to: C:\Users\cruzmars\Documents
