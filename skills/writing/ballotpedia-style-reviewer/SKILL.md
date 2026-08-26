---
name: ballotpedia-style-reviewer
description: Review prose, diction, neutrality, structure, and editorial mechanics against the supplied Ballotpedia Style Guide and bias framework.
version: 0.1.0
author: Local contributor, Hermes Agent
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [writing, editing, style-guide, neutrality, journalism, ballotpedia]
    related_skills: []
---
# Ballotpedia Style Reviewer

Use this skill to review written content and recommend changes that bring it closer to the supplied Ballotpedia editorial standards. The default task is **editorial review**, not wholesale rewriting. Preserve the writer's factual claims, sourcing boundaries, and substantive meaning unless the user explicitly asks for a rewrite.

## Source hierarchy

Read `references/source-hierarchy.md` before resolving any conflict.

1. **Ballotpedia's Style Guide** is the controlling source for editorial style, terminology, mechanics, and usage.
2. **Ballotpedia: How we categorize bias** is the controlling source for Ballotpedia-specific neutrality risks and bias labels.
3. **Wikipedia: Neutral point of view** is complementary guidance for due weight, attribution, structural neutrality, and false balance. It must not override a Ballotpedia rule.

The source snapshots bundled with this skill are in `sources/`. A text extraction of the Ballotpedia Style Guide is in `references/ballotpedia-style-guide-full.txt` for fast local searching.

## When to use

Use this skill when the user asks to:
- review an article, news post, profile, section, paragraph, memo, or draft for Ballotpedia style;
- identify biased, loaded, editorial, factive, vague, or speech-tribe wording;
- improve clarity, diction, sentence construction, active voice, or encyclopedic tone;
- assess whether article structure gives appropriate prominence to competing narratives;
- check capitalization, dates, numerals, quotations, political titles/affiliations, terminology, or footnotes against the supplied guide;
- receive line-level recommendations rather than a replacement draft.

Do not use this skill as a fact-checker unless the user also supplies sources or explicitly asks for external verification. Do not claim that an article is fully neutral merely because no lexical violations were found.

## Review modes

### 1. `audit` — default
Provide recommendations without rewriting the whole piece.

### 2. `annotated`
Give line- or passage-level comments with suggested replacement wording where useful.

### 3. `rewrite-plan`
Provide a prioritized revision plan and replacement snippets, but not a full rewritten document.

### 4. `rewrite`
Only use when the user explicitly requests a rewritten version. Preserve meaning and sourcing; do not introduce facts, assertions, or viewpoints absent from the source text.

## Core procedure

1. **Identify document context.** Determine whether the text is a Ballotpedia article, BP News item, profile, footnote-heavy page, or another format. If unknown, use general article rules and note that context-specific rules may remain.
2. **Preserve the source text.** Do not silently alter quotations, factual claims, statistics, names, or sourcing. Quoted material is not rewritten to conform to Ballotpedia house style.
3. **Run deterministic lint when practical.** For files or longer drafts, run:
   ```bash
   python scripts/bp_style_lint.py INPUT --context general --format json
   ```
   Use `--context news` for BP News. Treat script output as candidate issues, not final editorial judgment.
4. **Review neutrality first.** Read `references/bias-taxonomy.md` and assess editorializing, loaded language, factive verbs, competing narratives, labeling, speech-tribe terminology, attribution, placement, protagonist selection, prediction language, source selection, and weasel wording.
5. **Review structural neutrality.** Read `references/neutrality-principles.md`. Check due weight, relative prominence, section organization, source attribution, and false balance. Do not demand equal space for every view merely for symmetry.
6. **Review prose and diction.** Favor straightforward, accessible, specific language. Prefer facts over evaluative descriptors. Flag unnecessary jargon, vague modifiers, euphemisms, ambiguous antecedents, excessive passive voice, and sentence structures that obscure the actor.
7. **Review Ballotpedia usage and mechanics.** Consult `references/quick-reference.md` and search `references/ballotpedia-style-guide-full.txt` for exact entries when needed. Give the exact entry name when possible.
8. **Distinguish assessable from unassessable risks.** Source-selection bias cannot be conclusively assessed without a source list; photo-selection bias cannot be assessed without images; story-selection bias may require a broader corpus. Mark such items `NEEDS CONTEXT`, not `PASS` or `FAIL`.
9. **Prioritize recommendations.** Use the severity labels below. Do not bury neutrality issues beneath punctuation edits.
10. **Give actionable revisions.** For each material issue, identify the passage, name the rule/risk, explain why it matters, and suggest a concrete revision or reporting action.

## Severity labels

Use these labels consistently:

- `MUST FIX` — direct conflict with a clear Ballotpedia rule, clear attribution problem, or strong neutrality risk.
- `SHOULD FIX` — substantial clarity, precision, consistency, or structural improvement.
- `NEEDS CONTEXT` — depends on sources, surrounding coverage, quotation status, official terminology, or article type.
- `OPTIONAL` — polish that improves readability or cachet without correcting a clear violation.

Do not assign a numeric neutrality, bias, or compliance score. A single number can conceal high-impact problems and imply precision the sources do not support.

## Required review dimensions

Use the four Ballotpedia guiding principles as an organizing lens:

### Credibility
- neutrality and fact-based phrasing;
- clear attribution;
- no unsupported assertion, weasel wording, or editorial recommendation;
- careful use of ideological and partisan labels;
- accurate distinction between writer voice and source voice.

### Consistency
- consistent capitalization, punctuation, names, titles, party affiliations, lists, dates, numbers, and terminology;
- consistent treatment of comparable people, groups, and viewpoints.

### Clarity
- straightforward prose and plain language;
- specific descriptions rather than speech-tribe shorthand;
- active voice when it improves identification of the actor;
- precise time references, quantities, and definitions.

### Cachet
- polished phrasing without decorative bias;
- useful explanatory notes/tooltips where appropriate;
- restrained formatting and professional presentation.

## Neutrality checks

Read `references/bias-taxonomy.md` for the 25-category Ballotpedia framework. At minimum, review:

- cherry-picking and failure to capture competing narratives;
- editorializing and explicit recommendations;
- factive verbs and unclear attribution;
- ideological labeling, labeling bias, inappropriate descriptors, and loaded language;
- speech-tribe terminology and scare quotes;
- source selection, placement, protagonist selection, prediction, coatrack, and story-selection risks;
- unsubstantiated news and weasel words.

When a possible problem depends on evidence outside the submitted text, state exactly what additional material is needed to assess it.

## Structural review rules

Use `references/neutrality-principles.md` as a complementary check:

- Represent significant viewpoints in proportion to their prominence in reliable sourcing, not by artificial 50/50 symmetry.
- Avoid section structures that turn an article into a back-and-forth debate or imply that minority and majority views have identical weight.
- Integrate disagreements into the narrative where possible and attribute contested claims.
- Avoid a section or lede that implicitly establishes one person, party, or viewpoint as the story's protagonist without factual justification.
- Check whether important countervailing context is buried while favorable or unfavorable information is foregrounded.

## Diction and prose rules

- Prefer specific, descriptive language to labels carrying praise, blame, ideology, or emotional force.
- Use `said`, `stated`, or `wrote` for disputed opinions when a factive verb would presuppose truth.
- Remove or substantiate vague phrases such as `many experts say` or `research has shown`.
- Avoid scare quotes and the phrase `so-called`.
- Prefer active voice when it identifies a relevant actor; passive voice is acceptable when the actor is unknown, irrelevant, or already understood.
- Do not modify direct quotations merely to fit Ballotpedia style.

## Output format

Unless the user requests something else, return:

### Editorial assessment
Two to five sentences identifying the most important strengths/risks without giving a numeric score.

### Priority revisions
A table with columns:

| Location | Severity | Dimension | Rule / bias category | Recommendation |
|---|---|---|---|---|

Order issues by editorial impact: neutrality/attribution first, structure second, diction/prose third, mechanics last.

### Suggested wording
For issues where wording is the main problem, show concise `Current` and `Suggested` text. Do not rewrite passages whose correction requires new factual reporting; instead specify the information or source needed.

### Structural and sourcing notes
Discuss due weight, competing narratives, placement, lede, section order, source diversity, and any limits on what can be assessed from the supplied material.

### Mechanical/style notes
Group lower-level style-guide corrections such as dates, numerals, capitalization, titles, punctuation, and preferred spellings.

### Editor questions
List unresolved issues requiring source verification, official terminology, or editorial judgment. Omit this section when there are none.

## Exact-rule lookup

When uncertain about a Ballotpedia-specific usage rule, search the extracted guide rather than improvising:

```bash
grep -in "SEARCH TERM" references/ballotpedia-style-guide-full.txt | head -n 20
```

Common high-value entries are summarized in `references/quick-reference.md`, but the full extracted guide is the preferred source for exact edge cases.

## Deterministic linter limits

`scripts/bp_style_lint.py` is intentionally conservative. It can flag lexical and formatting candidates such as `e-mail`, `comprised of`, relative dates, selected speech-tribe terms, and possible factive/weasel language. It cannot determine:
- whether a viewpoint received due weight;
- whether a source set is ideologically imbalanced;
- whether a descriptor is factually justified;
- whether a legal/formal name requires otherwise disfavored terminology;
- whether a quotation spans multiple lines or has been faithfully transcribed;
- whether omitted information constitutes cherry-picking.

Hermes must make the final review from context and label uncertainty.

## Verification checklist

Before finishing a review, verify:

- [ ] Ballotpedia Style Guide controlled any conflicting usage question.
- [ ] Neutrality risks were reviewed before minor mechanics.
- [ ] Direct quotations were not silently restyled.
- [ ] Contested claims are attributed rather than stated in writer voice where required.
- [ ] Speech-tribe or loaded terminology is either replaced with specific language or clearly attributed when the guide permits it.
- [ ] Competing narratives and due weight were considered without imposing false balance.
- [ ] Source/photo/story-selection issues are not declared resolved when the necessary evidence was not supplied.
- [ ] Recommendations preserve the writer's substantive meaning unless new reporting is explicitly requested.
- [ ] The review does not claim a numeric neutrality/compliance score.
