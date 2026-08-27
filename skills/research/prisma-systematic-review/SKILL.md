---
name: prisma-systematic-review
description: "Run PRISMA systematic reviews with a 6-agent pipeline."
---

# PRISMA Systematic Review Pipeline

A multi-agent pipeline that conducts PRISMA 2020-compliant systematic reviews and meta-analyses. Six specialized subagents execute sequentially (with parallel optimization) to produce a complete review package with real tool access (web search, PDF parsing, R execution).

## Configuration Phase

Before spawning agents, collect from the user via clarify tool:

| Parameter | Options | Default |
|-----------|---------|---------|
| Research topic | Free text | *Required* |
| Review type | systematic-review, meta-analysis, scoping-review | systematic-review |
| Search mode | web-live (PubMed/web search), pdf-upload (analyze provided PDFs), both | web-live |
| Statistical approach | auto (agent decides), user-defined | auto |
| Effect measure | OR, RR, SMD, HR, MD, agent-decides | agent-decides |
| Model override | current-session, openrouter:provider/model | current-session |
| Output directory | Path | ~/prisma-review-{timestamp} |

### Topic Refinement
If the user provides a broad topic, the first agent (Protocol Specialist) refines it into a specific, answerable research question using PECOS framework. The user can override or approve before proceeding.

### Model Selection
If user chooses a specific model, document it. Each subagent inherits the session model by default. To override, include model preference in the delegation context.

## Pipeline Architecture

```
Stage 1: Protocol (PECOS Framework)
    ↓
Stage 2: Search Strategy (Boolean Strings + Optional Live Search)
    ↓
┌─────────────┬─────────────┬─────────────┐
│ Stage 3     │ Stage 4     │ Stage 5     │  ← PARALLEL
│ Screening   │ Extraction  │ Statistics  │
│ Rubric      │ Template    │ Plan + R    │
└─────────────┴─────────────┴─────────────┘
    ↓             ↓             ↓
Stage 6: PRISMA 2020 Manuscript Compilation
```

## Stage Details

### Stage 1: Protocol Development
**Agent**: Public Health Methodologist
**delegate_task goal**: Develop a comprehensive systematic review protocol with PECOS criteria
**Context**: Topic, review type, any user specifications
**Output**: Structured protocol with PECOS criteria, objectives, eligibility criteria, outcomes
**Deliverable**: `01_protocol.md`

Key protocol sections:
- Background and rationale
- Review question (formatted per PECOS)
- Population, Exposure/Intervention, Comparator, Outcomes, Study design
- Registration intent (PROSPERO)

### Stage 2: Search Strategy
**Agent**: Medical Librarian
**delegate_task goal**: Translate PECOS into Boolean search strings for PubMed, Embase, Cochrane, CINAHL and execute live searches following the Evidence-Grounded Search & Citation Methodology section (3b-A through 3b-E): prefer E-utilities API, decompose searches by component with verbatim query logging, complete citation metadata only.
**Context**: Protocol from Stage 1, search mode setting
**Output**: Database-specific search strings, gray literature strategy
**Deliverable**: `02_search_strategy.md` + optional `02_search_results.csv`

Search mode handling:
- **web-live**: Execute PubMed searches via web_search/fetch_url, retrieve real results, compile into CSV
- **pdf-upload**: Generate a PDF processing checklist, instruct user on PDF organization
- **both**: Do web search AND prepare PDF intake

### Stage 3: Screening Rubric (PARALLEL)
**Agent**: Review Screener
**Context**: Protocol from Stage 1
**Output**: Two-stage screening rubric (title/abstract + full-text) with decision tree
**Deliverable**: `03_screening_rubric.md`

### Stage 4: Data Extraction Template (PARALLEL)
**Agent**: Data Extraction & Bias Analyst
**Context**: Protocol from Stage 1, extraction_schema.json template
**Output**: Customized extraction schema, ROBINS-I assessment framework
**Deliverable**: `04_extraction_template.json` + `04_bias_assessment.md`

### Stage 5: Statistical Analysis Plan (PARALLEL)
**Agent**: Biostatistician
**Context**: Protocol outcomes, effect measure preference, statistical approach, meta_analysis.R template
**Output**: Analysis plan document + customized R script
**Deliverable**: `05_analysis_plan.md` + `05_meta_analysis.R`

### Stage 6: PRISMA Manuscript
**Agent**: Lead PRISMA Author
**Context**: ALL outputs from Stages 1-5
**Output**: Complete manuscript draft + PRISMA checklist
**Deliverable**: `06_manuscript_draft.md` + `06_prisma_checklist.md`

## Output Structure

```
~/prisma-review-{topic-slug}-{timestamp}/
├── 01_protocol.md
├── 02_search_strategy.md
├── 02_search_results.csv          (web-live mode)
├── 03_screening_rubric.md
├── 04_extraction_template.json
├── 04_bias_assessment.md
├── 05_analysis_plan.md
├── 05_meta_analysis.R
├── 06_manuscript_draft.md
├── 06_prisma_checklist.md
├── extracted_data.csv              (template for data entry)
└── README.md                       (pipeline summary + next steps)
```

## Subagent Context Pattern

Each subagent receives:
```
RESEARCH TOPIC: {topic}
REVIEW TYPE: {type}
CONFIGURATION: {config}
PREVIOUS OUTPUTS: {prior_stage_deliverables}
YOUR TASK: {specific_stage_description}
OUTPUT FORMAT: {expected_structure}
```

Stages 3-5 receive Stages 1-2 outputs only. Stage 6 receives ALL outputs.

## PRISMA 2020 Compliance

Manuscript must address all 27 checklist items covering: title, abstract, rationale, objectives, eligibility, information sources, search strategy, selection process, data collection, risk of bias, effect measures, synthesis methods, reporting bias, certainty assessment, PRISMA flow diagram, study characteristics, results, discussion, conclusions, registration, funding.

## Verification (pre-delivery gates)

Before delivering any completed review package, verify ALL of:
- [ ] Every CSV record traces to a real tool-returned result; query log matches PRISMA flow numbers
- [ ] Reference lists contain COMPLETE author lists — no "et al.", no "& colleagues", no placeholder author forms
- [ ] Every reference includes volume, issue (where applicable), pages/article number, AND DOI/PMID/URL
- [ ] Evidence Table present with ≥1 source per major methodological component (or explicit gap statement)
- [ ] ≥25 qualifying research articles identified before screening concludes (or explicit shortfall justification)
- [ ] No fabricated included studies, effect sizes, or findings anywhere in the package — pending sections clearly labeled

## Error Handling

- Subagent failure: retry once with simplified context
- Web search failure: fall back to generating search strings only
- R code errors: report but continue to manuscript
- Always save partial results — never lose completed work

## Evidence-Grounded Search & Citation Methodology

Adopted from the `public-health-evaluation-planning` skill (Step 3b). These rules are MANDATORY for Stage 2 and any stage that cites literature.

### 3b-A. Prefer NCBI E-utilities over browser scraping
When searching PubMed/PMC live, use the E-utilities API instead of rendering pubmed.ncbi.nlm.nih.gov in a browser (browser rendering frequently times out):
```
https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi?db=pubmed&term=<urlencoded query>&retmax=20&sort=relevance&retmode=json
https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esummary.fcgi?db=pubmed&id=<comma-separated IDs>&retmode=json
```
Both are callable from terminal via Python urllib. Browser-based search is a fallback only. Extract DOI/PMID directly from esummary records rather than omitting identifiers.

### 3b-B. Decompose searches by methodological component
Do NOT run one blanket query set. Decompose the review question into its major components (population concept, intervention/exposure concept, outcome concepts, methods concept) and run MULTIPLE targeted search runs — one per component pairing — varying phrasing across runs. Log every executed query verbatim (string, database/source, date, raw-hit count) in 02_search_strategy.md so the PRISMA flow diagram numbers are auditable.

### 3b-C. Evidence Table required in the protocol/manuscript
Every methodological choice made by the pipeline (screening rubric thresholds, charting fields, synthesis approach, instrument selection) must be supported by at least one published methodological source where such support exists. Build an Evidence Table:

| Methodological Component | Supporting Source(s) | What It Supports | Relevance |
|---|---|---|---|

Handle gaps honestly: if no open-access support exists after 2–3 query variations, state that explicitly ("No OA source identified; rationale is [X]") rather than citing weak sources silently.

### 3b-D. Citation integrity (fabrication-adjacent behavior forbidden)
- **NEVER abbreviate author lists** as "et al." or "& colleagues" in reference lists. Every reference entry carries the COMPLETE author list as published (up to 20 authors; 21+ → first 19, ellipsis, final author). Retrieve full author names via E-utilities esummary or Crossref (`https://api.crossref.org/works/<doi>`) before including an entry. If full authors cannot be retrieved, either drop the source (noting why) or mark it `[AUTHORS INCOMPLETE — verify before use]` in bold.
- **Complete citation elements mandatory**: authors, year, sentence-case title, journal (Title Case italics), volume (italics), issue in parentheses whenever the journal uses issues, page range OR article number, and DOI as a live `https://doi.org/...` link (PMID/URL acceptable fallback). A missing volume/issue/pages/DOI fails verification.
- **Never invent records.** Every row of 02_search_results.csv must trace to a real tool-returned result. Search-agent outputs that contain plausible-but-unverifiable citations must be dropped, not kept.
- Every deliverable includes a full citation list covering ALL sources reviewed, verified against actual sources before inclusion.

### 3b-E. Minimum source floor for scoping reviews
A completed scoping review package should identify ≥25 qualifying candidate research articles before screening concludes (peer-reviewed research; government reports and websites count toward total citations but not this floor). If fewer than 25 exist after exhausting query variations, state the shortfall explicitly with justification (narrow topic, emerging field) rather than padding with tangential records.

## Save-Path Workflow

**IMPORTANT:** Before saving any deliverable (manuscript, article summaries, PRISMA output files), ask the user:
- "Where would you like me to save this? (e.g., C:\Users\cruzmars\Documents)"
- Wait for user response before saving to the specified location.
- If user does not specify, default to: C:\Users\cruzmars\Documents
