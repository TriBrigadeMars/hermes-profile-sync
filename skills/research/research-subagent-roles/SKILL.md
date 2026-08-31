---
name: research-subagent-roles
description: "Use when delegating research pipeline work to subagents."
version: 1.0.0
author: Mars Cruz, Hermes Agent
license: MIT
metadata:
  hermes:
    category: research
    tags: [delegation, subagents, literature-review, validation, apa7, orchestration]
    related_skills: [multi-topic-literature-review, delegated-literature-collection, public-health-evaluation-planning, prisma-systematic-review, apa-7-style-agent, grounded-citations]
---

# Research Subagent Role Library

Shared role definitions and executable tooling for ANY research skill that fans
work out to subagents. Orchestrator skills (multi-topic-literature-review,
prisma-systematic-review, public-health-evaluation-planning Step 3b) reference
this skill instead of re-inventing role specs, schemas, and validators.

## When to Use

- Dispatching delegate_task subagents for source collection, corpus validation,
  synthesis writing, or APA document packaging
- Validating a returned source corpus before building anything downstream
- Building APA 7 .docx literature-review packages

## The Five Roles

### 1. Collector (source collection + summarization in ONE pass)

Never split collection and summarization into separate dispatches — the collector
fetches abstracts and writes summaries in the same run.

Goal template (fill brackets, keep everything else verbatim):

```
Collect and verify >=[N] on-topic sources for: "[TOPIC — SPELL OUT EVERY ACRONYM]".

SCOPE: [broad/strict]. Include: [categories]. FORBIDDEN (off-topic, will be purged): [named categories].
Date window: [2000 or later; prefer 2010-present]. NOTHING before [YEAR], even foundational items.

VERIFICATION (mandatory, no fabrication): verify each peer-reviewed record via NCBI
E-utilities (esearch/esummary/efetch, https://eutils.ncbi.nlm.nih.gov/entrez/eutils/)
or Crossref (https://api.crossref.org/works/<doi>); verify each web/trade item by
fetching the live page. Drop any record you cannot verify — never guess metadata.

FOR EVERY SOURCE write a 3-5 sentence factual summary from the retrieved abstract
(purpose, design/sample, key findings with exact figures).

DELIVERABLE: write to [PATH]/sources.json — JSON array, each object EXACTLY:
{"authors": ["Lastname, A. A.", ...], "year": 2020, "title": "...", "journal": "...",
 "volume": "...", "issue": "...", "pages": "...", "doi_or_url": "https://doi.org/...",
 "pmid": "...", "type": "peer-reviewed"|"newspaper/trade"|"guideline/report",
 "summary": "3-5 sentences"}
Also write [PATH]/abstract.md (4-6 sentence review abstract).
Final message: exact count, type breakdown, gaps. Do not fabricate.
```

### 2. Corpus Auditor (validation — parent runs this, or one dedicated subagent)

Run `scripts/validate_corpus.py` — ONE script, all checks, one report. Never run
separate ad-hoc checks per dimension. See the script's docstring for usage.

### 3. Synthesis Writer

Goal template additions beyond the topic brief:

```
CITATION DISCIPLINE (critical): every factual claim carries an APA 7 in-text
citation. 3+ authors: "Firstauthor et al., year" from the FIRST citation (APA 7
§8.17) — never spell out full author lists in narrative citations. Same-author-
same-year works: assign a/b suffixes ALPHABETICALLY BY TITLE. Cite ONLY sources
present in sources.json — never from memory. Mechanically verify every in-text
citation against the corpus before finishing, and report any corpus source you
did not cite and why. Ground all claims in the sources' summary fields; exact
figures only as stated; cautious causal language ("suggests", "is associated with").
```

### 4. Evidence-Grounding Collector (public-health evaluation Step 3b variant)

Same as Collector, but: one search run PER methodological component (not one
blanket query), each record must state which design/method choice it supports,
and the deliverable is an Evidence Table row set (component | source | what it
supports | relevance) instead of a plain corpus. Floor: >=1 open-access source
per major methodological component, with explicit gap statements where none exists.

### 5. APA Packager

Run `scripts/build_apa_docx.py` — the pre-tested builder. NEVER hand-build docx
pipelines per project. Smoke-test with 2 dummy sources before real corpora arrive
(the builder's page-number field and author-period handling are pre-fixed; a
smoke test catches any regression in seconds).

## Efficiency Rules (mandatory for all dispatches)

1. Lock the JSON schema in every delegation goal (field names + types verbatim).
2. Combine collection + summarization in one pass.
3. Spell out acronyms and list forbidden off-topic categories by name.
4. One validation script run — not per-dimension ad-hoc checks.
5. Pre-test output builders with dummy data while collectors still run.
6. Batch API lookups (Crossref/PubMed) in one Python loop, never one curl per item.
7. Front-load style rules (et al., a/b suffixes) in the writer's goal.

## Verification (before building downstream artifacts)

- [ ] validate_corpus.py passes on every corpus (or failures documented + fixed)
- [ ] Source floor met per topic (or shortfall documented honestly)
- [ ] Zero records outside date window; zero contaminated records
- [ ] Synthesis citations mechanically cross-checked against corpus (both directions)
- [ ] Smoke-tested docx build before the real run

## Scripts

- `scripts/validate_corpus.py` — one-shot corpus validation (schema, years,
  author format, type labels, summaries, DOI liveness sample, floor counts)
- `scripts/build_apa_docx.py` — APA 7 .docx packager (title page, abstract,
  synthesis body, hanging-indent references, annotated bibliography)

## Pitfalls

- Collector self-reports are not evidence — validate the FILES, not the message.
- Years hide in venue strings ("Innovations in Pharmacy, 2013;4(1)") — the
  validator parses years from all string fields; a naive record["year"] check
  silently zeroes corpora.
- esummary JSON can contain control characters — parse with strict=False or use
  efetch rettype=medline tagged fields.
- Org authors must match their in-text citation form (e.g., "Home Office",
  "NIHR Evidence") or the reference list and citations will diverge.
- Transient Crossref timeouts are not failures — retry before dropping a DOI.
