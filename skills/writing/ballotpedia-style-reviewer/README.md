# Ballotpedia Style Reviewer — Hermes Skill

A local-first editorial review skill built from three supplied reference documents:

1. **Ballotpedia's Style Guide** — controlling source for house style and usage.
2. **Ballotpedia: How we categorize bias** — controlling source for Ballotpedia's bias taxonomy.
3. **Wikipedia: Neutral point of view** — complementary guidance for due weight, attribution, false balance, source prominence, and structural neutrality.

The skill is designed to **review prose and recommend revisions**, not automatically rewrite a writer's work by default.

## What it reviews

- neutral/encyclopedic tone;
- editorializing, loaded language, factive verbs, scare quotes, weasel words, and speech-tribe terminology;
- attribution and the distinction between source voice and writer voice;
- competing narratives, due weight, placement, protagonist selection, and article structure;
- clarity, specificity, active/passive voice, sentence construction, and diction;
- Ballotpedia-specific spelling, capitalization, political titles and affiliations, dates, numerals, quotations, lists, and footnotes;
- topic-specific terminology when the supplied style guide contains a dedicated entry.

## Review philosophy

The review uses Ballotpedia's four stated principles as its top-level lens:

- **Credibility** — neutral, fact-based, clearly attributed writing.
- **Consistency** — uniform editorial choices and parallel treatment.
- **Clarity** — straightforward, accessible, specific prose.
- **Cachet** — polished presentation and thoughtful explanatory devices.

Neutrality and attribution issues are prioritized over commas and spelling.

## Install

Unzip the package and run:

```bash
python scripts/install.py
```

Default destination:

```text
~/.hermes/skills/writing/ballotpedia-style-reviewer/
```

Start a new Hermes session after installation so the skill index reloads.

## Example requests in Hermes

```text
Review this draft for Ballotpedia style. Give recommendations only; do not rewrite it.
```

```text
Run an annotated Ballotpedia style and neutrality review of this article. Prioritize diction, factive verbs, speech-tribe terminology, and structural bias.
```

```text
Review this BP News draft against the supplied Ballotpedia guide. Identify MUST FIX issues and provide concise replacement wording.
```

```text
Check this article's structure for competing narratives, due weight, placement bias, and protagonist selection. Tell me what you cannot determine without the source list.
```

## Deterministic preflight linter

The package includes a standard-library-only lexical linter:

```bash
python scripts/bp_style_lint.py article.txt --context general
```

BP News:

```bash
python scripts/bp_style_lint.py article.txt --context news --format json
```

The linter flags candidate issues such as:

- disfavored spellings/forms (`e-mail`, `bi-partisan`, `comprised of`);
- numeral/percent/date conventions;
- relative dates;
- selected Ballotpedia speech-tribe terms;
- possible factive verbs and weasel wording;
- selected topic-specific terminology requiring contextual review.

It deliberately **does not** calculate a bias or neutrality score. It also cannot determine due weight, source diversity, factual accuracy, quotation fidelity, or omitted narratives.

## Source files

Exact source snapshots are retained under `sources/` for provenance. For fast text search, the text-bearing Ballotpedia Style Guide is also extracted into:

```text
references/ballotpedia-style-guide-full.txt
```

A lightweight entry/page index is available at:

```text
references/style-entry-index.tsv
```

Fast lookup:

```bash
grep -in "Political affiliation" references/ballotpedia-style-guide-full.txt | head
```

## Review output

Default reviews contain:

1. Editorial assessment
2. Priority revisions
3. Suggested wording
4. Structural and sourcing notes
5. Mechanical/style notes
6. Editor questions, when unresolved context exists

Severity labels:

- `MUST FIX`
- `SHOULD FIX`
- `NEEDS CONTEXT`
- `OPTIONAL`

## Updating the guide

See `references/updating.md`. A helper can re-extract a newer text-bearing Ballotpedia Style Guide PDF using local `pdftotext`:

```bash
python scripts/extract_style_guide.py sources/ballotpedia-style-guide.pdf references/ballotpedia-style-guide-full.txt
python scripts/build_style_index.py references/ballotpedia-style-guide-full.txt references/style-entry-index.tsv
```

The supplied bias-taxonomy and Wikipedia PDFs are image-based snapshots, so their curated digests should be reviewed manually when those sources change rather than silently regenerated through OCR.

## Tests

```bash
python -m unittest discover -s tests -v
```

## Licensing/source notice

Original helper code is MIT licensed. The bundled source PDFs and their underlying text are not relicensed by this package. See `THIRD_PARTY_NOTICES.md`.
