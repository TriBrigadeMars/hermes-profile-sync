---
name: apa-7-style-agent
version: 1.0.0
author: Hermes Agent
license: MIT
tags: [research, writing, apa, style-guide, citations, formatting, academic]
related_skills: [grounded-citations, humanizer, document-to-action-items, pdf, docx]
description: Audit and revise documents for APA 7th Edition compliance.
---
# APA 7 Style Agent

Audit any draft document for compliance with the APA Publication Manual, 7th Edition. Produces a structured revision report and a corrected document.

## When to Use

Use this skill when the user asks to:
- Format a paper in APA 7 style
- Audit or check a document for APA compliance
- Fix citations, references, headings, or formatting for APA 7
- Prepare a manuscript for submission to an APA-style journal
- Convert a paper to APA 7 format

## Workflow

### Step 1: Load and Inventory the Document

Read the entire document. Identify:
- Document type (empirical article, literature review, student paper, dissertation, meta-analysis, theoretical article, methodological article)
- Whether it is a professional manuscript or student paper
- Current citation format (if any)
- Current heading structure
- Presence/absence of required sections (title page, abstract, references, tables, figures)

### Step 2: Run APA 7 Audit

Apply all APA 7 compliance criteria to the document.

### Step 3: Generate Audit Report

Create a structured report with findings organized by category:
- CRITICAL (must fix)
- SHOULD FIX
- SUGGESTIONS

### Step 4: Produce an Edited Copy (with Track Changes + Comments)

**This is the core deliverable.** For `.docx` manuscripts, produce a revised copy
where every APA 7 fix is applied as a **tracked change** (so the author can
Accept/Reject each edit in Word's Review pane) and/or a **margin comment** explaining
the rule behind each change.

Reuse the verified helper from the `docx-accessibility-agent` skill
(`scripts/docx_remediate.py` — copies into the docx skill; functions are
format-agnostic and work identically for APA remediation):
- `insert_tracked(paragraph, text)` — add corrected text as a tracked insertion (w:ins)
- `delete_tracked(paragraph, text)` — remove text as a tracked deletion (w:del/w:delText)
- `add_comment(document, run, text)` — attach a real Word comment citing the APA rule
  (e.g. "APA 7 §8.17: use 'et al.' from the first citation for 3+ authors").

Workflow for the edited copy:
1. Open the original manuscript.
2. Apply automatable APA fixes directly as tracked changes: heading levels, citation
   format (et al., & vs and, year placement), reference-list formatting (hanging
   indent, italics, DOI to https://doi.org form), numbers (0–9 spelled out), serial
   commas, title/sentence case.
3. For each non-automatable judgment call (bias-free language, block-quote placement,
   table/figure note ordering), attach an `add_comment` citing the specific APA section.
4. Save as `<original>_apa7_remediated.docx`.

For non-`.docx` sources (markdown, plain text), produce a fully corrected new document
instead, and note every change in the audit report so the author can diff.

### Step 5: Ask User for Save Path
**IMPORTANT:** Before saving the final products, ask the user:
- "Where would you like me to save the report and edited copy? (e.g., C:\Users\cruzmars\Documents)"
- Wait for user response before saving to the specified location.

### Step 6: Save and Deliver
Save all artifacts to the user-specified path and confirm completion.

## Audit Criteria

### Title Page Audit (Section 2.3–2.7)

**Professional title page must include:**
- Title in title case, bold, centered, upper half of page
- Author byline: first name, middle initial(s), last name — no titles (Dr., PhD) or degrees
- Affiliation: department and institution (no location for academic affiliations; city, state, country for nonacademic)
- Author note with four paragraphs: ORCID iDs, changes of affiliation, disclosures/acknowledgments, contact information
- Running head: ALL CAPS, max 50 characters, flush left on every page
- Page number: flush right on every page, starting at 1

**Student title page must include:**
- Title (same format as professional)
- Author byline
- Affiliation (university)
- Course number and name
- Instructor name
- Assignment due date (month day, year format)
- Page number
- NO running head (unless required by instructor)
- NO author note (unless requested)

### Abstract Audit (Section 2.9, 3.3)

- On its own page after title page (page 2)
- Label "Abstract" in bold title case, centered
- Single paragraph, no indentation, ≤250 words
- Must be accurate, nonevaluative, coherent, readable, concise
- Keywords: italic label "Keywords:" indented 0.5 in., lowercase (capitalize proper nouns), 3–5 terms, separated by commas, no period after last keyword

### Heading Levels Audit (Section 2.27)

APA 7 has exactly five heading levels:

| Level | Format |
|-------|--------|
| 1 | **Centered, Bold, Title Case** — text begins as new paragraph |
| 2 | **Flush Left, Bold, Title Case** — text begins as new paragraph |
| 3 | ***Flush Left, Bold Italic, Title Case*** — text begins as new paragraph |
| 4 | **Indented, Bold, Title Case, Ending With a Period.** Text begins on same line. |
| 5 | ***Indented, Bold Italic, Title Case, Ending With a Period.*** Text begins on same line. |

**Rules:**
- The paper title at the top of page 1 acts as a de facto Level 1 heading. Do NOT use an "Introduction" heading.
- Use only as many heading levels as needed (typically 3).
- Every section starts with the highest applicable level.
- At least two subsections at any level, or none (no lone subsection).
- Topics of equal importance get the same heading level.
- Do not label headings with numbers or letters.

### In-Text Citation Audit (Chapter 8)

**Author–date system (Section 8.10):**

| Authors | Parenthetical | Narrative |
|---------|--------------|-----------|
| 1 author | (Smith, 2020) | Smith (2020) |
| 2 authors | (Smith & Jones, 2020) | Smith and Jones (2020) |
| 3+ authors | (Smith et al., 2020) | Smith et al. (2020) |
| Group, first cite | (National Institute of Mental Health [NIMH], 2020) | National Institute of Mental Health (NIMH, 2020) |
| Group, subsequent | (NIMH, 2020) | NIMH (2020) |
| No author | (Title in Title Case, 2020) | "Title in Title Case" (2020) |
| No date | (Smith, n.d.) | Smith (n.d.) |

**Critical rules:**
- Use `&` in parenthetical citations, `and` in narrative citations
- For 3+ authors, ALWAYS use "et al." from the FIRST citation (7th ed. change from 6th)
- To avoid ambiguity with multiple 3+ author works shortening to the same form, write out enough names to distinguish
- Same author + same year: add lowercase letters (2020a, 2020b)
- Same surname different initials: include initials in all citations (J. M. Taylor, 2015; T. Taylor, 2014)
- Multiple works parenthetical: alphabetical order, semicolons between (Adams et al., 2019; Westinghouse, 2017)
- Use "as cited in" for secondary sources — only secondary source in reference list
- Personal communications (emails, interviews, etc.): cite in text only, NO reference list entry
- Translated/reprinted/republished: two dates (Freud, 1900/1953)
- Omit year in repeated narrative citations within the same paragraph (not parenthetical)
- Every in-text citation must have a reference list entry and vice versa (except personal communications)

### Reference List Audit (Chapter 9)

**Format (Section 9.43):**
- New page after text, before tables/figures/appendices
- Label "References" bold, centered
- Double-spaced throughout
- Hanging indent 0.5 in.
- Alphabetical by first author surname

**Four elements of every reference:** Author. (Date). Title. Source.

**Author element (Section 9.7–9.12):**
- Invert all individual authors: Last, A. A.
- Use `&` before final author
- Serial comma before `&` with 3+ authors
- Up to 20 authors listed; 21+ → first 19, ellipsis, last author
- One space between initials
- Group authors: spell out full name, no abbreviation in reference

**Date element (Section 9.13–9.17):**
- Enclosed in parentheses, followed by period: (2020).
- No date: (n.d.).
- In press: (in press).
- More specific dates when applicable: (2020, August 26).

**Title element (Section 9.18–9.22):**
- Works that stand alone (books, reports, webpages): italicized, sentence case
- Works that are part of a greater whole (journal articles, book chapters): not italicized, not quoted, sentence case
- Period at end (or ? / ! if title ends with one)

**Source element (Section 9.23–9.37):**
- Periodicals: *Journal Title, Volume*(Issue), Pages.
- Books/reports: Publisher Name.
- Edited chapters: In E. E. Editor (Ed.), *Book title* (pp. xx–xx). Publisher.
- DOIs: https://doi.org/xxxxx (as hyperlink, no period after)
- URLs: include for works from websites; do NOT include for works from most academic databases
- When author = publisher: omit publisher to avoid repetition

### Numbers Audit (Section 6.32–6.39)

- Use numerals for 10 and above
- Use words for zero through nine (except in abstract — same rules apply in 7th ed.)
- Always use numerals for: units of measurement, time, dates, ages, scores, points on a scale, exact money, statistical/mathematical functions, percentages, ratios
- Spell out numbers that begin a sentence, title, or heading
- Use combination for back-to-back modifiers: "two 7-point scales"
- Commas in numbers ≥1,000 (exceptions: page numbers, binary, serial numbers, degrees of freedom, acoustic frequencies)

### Statistics Audit (Section 6.40–6.45)

- Italicize statistical symbols: *M*, *SD*, *t*, *F*, *df*, *p*, *N*, *n*, *r*, *d*
- Greek letters NOT italicized: α, β, χ²
- Bold for vectors and matrices: **V**, **Σ**
- Standard type for abbreviations that are not variables: ANOVA, CI, SEM
- Report exact *p* values to 2–3 decimal places (e.g., *p* = .031); report *p* < .001 (not *p* = .000)
- Use leading zero before decimal when statistic CAN exceed 1: *t*(20) = 0.86, *d* = 0.70
- NO leading zero when statistic CANNOT exceed 1: *r*(24) = −.43, *p* = .028
- Report effect sizes with confidence intervals when possible
- Format: 95% CI [LL, UL]
- Use symbol with numerals: 4 cm, 30 kg; spell out without numerals: several kilograms
- One space after punctuation at end of sentence; one space after commas, colons, semicolons
- Use one space after period at end of sentence (7th ed. clarification)

### Bias-Free Language Audit (Chapter 5)

**General principles:**
- Describe at appropriate level of specificity
- Be sensitive to labels — use terms people use for themselves
- Acknowledge people's humanity — avoid adjectives as nouns ("the poor"), labels equating people with conditions ("schizophrenics")
- Use person-first OR identity-first language based on group preference
- Avoid false hierarchies ("normal" vs. "abnormal")
- Order of group presentation does not imply dominance

**Specific topics:**
- **Age**: exact ages/ranges preferred; "older adults" not "elderly" or "seniors"
- **Disability**: person-first ("person with paraplegia") or identity-first ("autistic person") per group preference; avoid "wheelchair bound," "special needs," "handicapable"
- **Gender**: "gender" for social construct, "sex" for biological; use singular "they"; avoid "he/she"; use "cisgender," "transgender" as adjectives
- **Race/Ethnicity**: capitalize Black, White; be specific (Mexican American not just Hispanic); no hyphens in multiword names ("Asian American" not "Asian-American")
- **Sexual orientation**: use "sexual orientation" not "sexual preference"; avoid "homosexual"; use specific terms (lesbian, gay, bisexual, queer)
- **Socioeconomic status**: provide specific income ranges, not just "low income"; avoid "the homeless" — use "people experiencing homelessness"

### Punctuation Audit (Section 6.1–6.10)

- **Serial comma**: REQUIRED before final item in series of 3+ ("height, width, and depth")
- **Comma after introductory phrases**: use after introductory phrases; optional if short
- **Comma with nonrestrictive clauses**: set off with commas; restrictive clauses: no commas
- **Semicolon**: between independent clauses without conjunction; before conjunctive adverbs (however, therefore); between items in a list that already contain commas
- **Colon**: after a grammatically complete introductory clause; capitalize first word after colon if what follows is a complete sentence
- **Em dash**: no spaces before or after; use judiciously
- **Quotation marks**: periods and commas INSIDE closing quotes; colons, semicolons outside
- **Parentheses**: end punctuation inside if complete sentence enclosed; outside if only part of sentence

### Capitalization Audit (Section 6.13–6.21)

- APA is a "down" style — lowercase unless specific reason to capitalize
- **Title case** for: titles of works in text, headings (all levels), periodical titles, table/figure titles, test/measure names
- **Sentence case** for: reference list entries, table column headings/entries/notes, figure notes
- Do NOT capitalize: diseases/disorders (except personal names within: Alzheimer's disease), therapies, theories, concepts, hypotheses, names of conditions/groups in experiments
- Capitalize: proper nouns, racial/ethnic groups, specific course names, nouns followed by numerals denoting series position (Table 1, Figure 3, Appendix B)

### Italics Audit (Section 6.22–6.23)

**Use italics for:**
- Key terms on first use (with definition)
- Titles of books, reports, webpages, and other standalone works
- Titles of periodicals
- Genera, species, varieties
- Letters used as statistical symbols or algebraic variables
- Volume numbers in reference lists
- Scale anchors (but not associated numbers)

**Do NOT use italics for:**
- Foreign words found in English dictionaries (a posteriori, et al., per se, zeitgeist)
- Chemical terms, trigonometric terms, Greek letters
- Mere emphasis (use syntax instead)

### Abbreviation Audit (Section 6.24–6.31)

- Define abbreviations on first use: spell out full term, abbreviation in parentheses
- After definition, use only the abbreviation
- Do NOT define: dictionary terms (AIDS, IQ), measurement abbreviations (cm, kg), time abbreviations (hr, min), Latin abbreviations in parentheses (e.g., i.e.), standard statistical abbreviations (*M*, *SD*, *F*, *t*)
- Plural abbreviations: add lowercase "s" without apostrophe (DOIs, URLs, IQs)
- In tables/figures: define abbreviations in each table/figure even if defined in text

### Tables and Figures Audit (Chapter 7)

**Tables:**
- Number: Arabic numeral, bold, flush left (Table 1)
- Title: italic title case, flush left, one double-spaced line below number
- Headings: sentence case, centered; stub heading flush left
- Body: single, 1.5, or double-spaced; centered entries (or left-aligned for readability)
- Notes order: general note, specific notes, probability notes — all flush left, double-spaced
- Borders: top and bottom, beneath column headings, above spanners only; NO vertical borders
- Confidence intervals reported for point estimates when possible
- Decimal alignment: same number of decimal places for comparable values

**Figures:**
- Number: Arabic numeral, bold, flush left (Figure 1)
- Title: italic title case, flush left
- Image: sans serif font 8–14 points, clear labels, sufficient contrast
- Legend: within or below image, title case
- Notes: same format as table notes

**Placement:** Either all after references on separate pages, or embedded after first callout in text. Double-spaced blank line between text and table/figure.

## Output Format

### APA 7 Audit Report

### CRITICAL (must fix)
- Section 3, ¶2: Missing page number in direct quotation (p. 47 required)
- Reference #7: Journal title should be italicized, not in quotation marks

### SHOULD FIX
- Heading Level 2 "Methods" should be "Method" (singular, per APA convention)
- Table 2: Missing general note defining abbreviations

### SUGGESTIONS
- Consider adding confidence intervals to effect size reports in Results
- Abstract exceeds 250 words (current: 287)

## Default Save Location
If user does not specify a path, default to: C:\Users\cruzmars\Documents\Hermes Research Output
**ALWAYS ask the user where to save before writing** — never assume the default.

## Accessibility Cross-Reference

When a document under audit is also intended for public/federal distribution, flag
these accessibility-adjacent writing conventions (full review belongs to the
accessibility agents — docx/pdf/pptx-accessibility-agent):

- **Alt-text prose**: image descriptions should follow the same concise, descriptive
  prose standards as captions (see `Intro to Alternative Text Section 508 Guide.txt`
  in pdf-accessibility-agent/references)
- **Plain language**: APA's clarity principles align with Section 508 plain-language
  guidance (active voice, short sentences, defined jargon)
- Note in the audit report when bias-free language (Chapter 5) and accessibility
  standards reinforce each other (person-first/identity-first language matches
  screen-reader-friendly phrasing)
