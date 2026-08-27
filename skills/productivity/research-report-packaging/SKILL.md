---
name: research-report-packaging
description: Convert research md to .docx, audit a11y, package.
version: 1.0.0
author: Hermes Agent
license: MIT
tags: [docx, accessibility, section-508, research, packaging, markdown]
category: productivity
related_skills: [docx, docx-accessibility-agent, apa-7-style-agent]
metadata:
  hermes:
    tags: [docx, accessibility, section-508, research, packaging, markdown]
    related_skills: [docx, docx-accessibility-agent, apa-7-style-agent]
---

# Research Report Packaging

Convert a styled markdown synthesis into a properly formatted Word document, run accessibility checks, and package the final deliverable set.

## When to Use

- The user has a markdown research report/synthesis that needs to become a .docx deliverable.
- You need to verify a .docx is a genuine OOXML package (not just renamed markdown).
- You need a Section 508 / WCAG 2 accessibility audit for a text-based document.
- You're packaging multiple deliverables (scan, synthesis, audit notes, final .docx) into a target directory.

## Prerequisites

- Python 3.10+ with `python-docx` installed: `pip install python-docx`
- `file` command (standard on Linux/macOS; available in Docker)

## Workflow

### Step 1: Convert Markdown to .docx

**Use a custom python-docx script** — NOT the `docx_create.py` JSON-spec approach — when the markdown has rich inline formatting (italic journal names, bold text, mixed formatting within paragraphs). The JSON spec requires pre-parsing into a block structure, which is cumbersome for inline-heavy content.

Required formatting:
- Arial 12pt throughout (body text)
- Double-spaced body (`WD_LINE_SPACING.DOUBLE`)
- 1-inch margins all sides
- **Title** style for the document title (one per document, distinct from Heading 1)
- **Heading 1** for major sections (Introduction, Methods, Results, Discussion, References)
- **Heading 2** for subsections within a Heading 1 section
- **Heading 3** for sub-subsections within a Heading 2 section
- Never skip heading levels (e.g., Heading 1 → Heading 3)
- References: italic journal names preserved (markdown `*Journal*` → python-docx italic runs)
- Exclude any HTML comments (e.g., `<!--style-pass-notes-->`)

**APA 7 Heading Format (§2.27):**

| Level | Format |
|-------|--------|
| Title | Centered, Bold, Title Case |
| 1 | Centered, Bold, Title Case |
| 2 | Flush Left, Bold, Title Case |
| 3 | Flush Left, Bold Italic, Title Case |

**Rules:** The paper title at the top of page 1 acts as a de facto Level 1 heading. Do NOT use an "Introduction" heading. At least two subsections at any level, or none.

See `references/md-to-docx-conversion.md` for the conversion pattern. See `references/crossref-verification.md` for the Crossref API workflow to verify sources and generate APA 7 citations.

### Step 2: Verify OOXML Integrity

Run these checks immediately after conversion:

```bash
# 1. File command must say "Microsoft Word 2007+"
file output.docx

# 2. Re-open with python-docx and print:
#    - Paragraph count
#    - Font consistency (all Times New Roman)
#    - Line spacing (all DOUBLE)
#    - Table count
#    - Margins (1 inch all sides)
#    - Document title and language
```

If `file` does NOT say "Microsoft Word 2007+", the file is corrupted or not a real .docx — reconvert.

### Step 3: Section 508 Accessibility Audit

For text-only documents (no images, no tables), the audit is straightforward:

| Check | Section 508 | WCAG 2.2 | How to Verify |
|-------|-------------|----------|---------------|
| Heading hierarchy | §1.3.1 | 2.4.6 | No skipped levels (Title → H1 → H2 → H3); at least two subsections per level or none |
| Document title | §1.3.1 | — | `doc.core_properties.title` set |
| Language | — | 3.1.1 | `doc.core_properties.language` set (e.g., "en-US") |
| Reading order | §1.3.2 | 1.3.2 | Sequential paragraph order; no floating text boxes |
| Alt text (images) | §1.1.1 | 1.1.1 | N/A if no images |
| Table accessibility | §1.3.1 | 1.3.1 | N/A if no tables |
| Color contrast | §1.4.3 | 1.4.3 | Black on white = 21:1 (pass); avoid colored text |
| Font consistency | — | 1.4.4 | All text Arial 12pt; scalable to 200% without loss |

Save audit results as `06_accessibility_audit.md`.

### Step 4: Copy Deliverables to Target

Copy all workflow files to the target directory:
```
01_evidence_scan.md       (raw evidence table)
02_synthesis.md           (original synthesis)
03_synthesis_apa7.md      (APA-7 corrected)
03_apa_audit_notes.md     (audit log)
04_synthesis_final.md     (styled final)
05_lgbtq_nicotine_report.docx  (Word document)
06_accessibility_audit.md (508 audit)
```

Verify with `ls -la` and report byte sizes.

### Step 5: Generate Summary Report

Create a summary with:
- All files copied and their sizes
- OOXML verification result
- Accessibility check summary (pass/fail with issues)
- Items needing user attention (truncated author lists, "verify at publisher" DOIs, etc.)

## Pitfalls

1. **Markdown italic parsing in references**: References use `*Journal Name*` for italics. The conversion script must split on `*` and alternate between normal and italic runs. Do NOT use a simple `run.italic = True` on the whole paragraph — it would italicize author names too.

2. **HTML comment exclusion**: Markdown files often end with `<!--style-pass-notes-->` or similar comments. These must be stripped before conversion — they are not content.

3. **Heading style override.** python-docx's default heading styles may use Calibri or other fonts. After adding headings, iterate over runs and set `run.font.name = 'Arial'` and `run.font.color.rgb = RGBColor(0, 0, 0)`.

4. **Line spacing on headings**: Set `para.paragraph_format.line_spacing_rule = WD_LINE_SPACING.DOUBLE` on heading paragraphs too — the style default may not propagate.

5. **Truncated author lists**: When the source scan has `et al.` due to truncation, retain as-is and flag in the summary for the user to verify.

6. **Hanging indents**: python-docx does not easily support hanging indents for References. Note this in the summary — the user may need to apply manually in Word.

## Verification

After packaging:
1. `file output.docx` → "Microsoft Word 2007+"
2. python-docx re-open → correct paragraph count, fonts, spacing
3. Accessibility audit → all checks pass (or issues documented)
4. All files present in target directory with expected sizes
