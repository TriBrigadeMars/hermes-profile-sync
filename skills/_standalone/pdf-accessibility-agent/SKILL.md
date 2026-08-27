---
name: pdf-accessibility-agent
version: 1.0.0
author: Mars Cruz
license: MIT
tags: [accessibility, pdf, section508, wcag, a11y]
related_skills: [docx-accessibility-agent, writing-style-agent]
description: Review .pdf files for Section 508 and WCAG 2 compliance.
---
# PDF Accessibility Agent

## Purpose
Review .pdf files for Section 508 (US Federal Standards) and WCAG 2 accessibility compliance.

## When to Use
Use this agent when reviewing internal documents, reports, or any .pdf file that needs to meet federal accessibility requirements or be usable by people with disabilities.

## Workflow

### Step 1: Load the Document
Read the .pdf file and extract its content.

### Step 2: Run Accessibility Checks
Apply Section 508 and WCAG 2 compliance criteria to the document.

### Step 3: Generate Review Report
Create a structured report with findings, severity ratings, and recommendations.

### Step 4: Produce an Edited Copy (Annotations + Metadata Fixes)
**This is the core deliverable.** Produce a revised `.pdf` where automatable fixes are
applied and non-automatable issues are flagged as sticky-note annotations.

Use the bundled helper `scripts/pdf_remediate.py` (VERIFIED with PyMuPDF 1.28.2):
- `fix_metadata(doc, title, author, subject)` — set Title/Subject/Author + set Initial
  View to show Document Title (fixes the #1 Section 508 PDF failure: empty metadata)
- `add_note(page, point, text)` — yellow sticky note anchored at (x, y) PDF points
- `add_highlight(page, rect)` — highlight a region needing attention

Workflow:
1. Open the original `.pdf` with pymupdf.
2. Apply automatable fixes directly: metadata (title/subject/author), Initial View.
3. For every non-automatable issue (alt text on figures, reading order, table tag
   structure, contrast), add a sticky-note annotation at the affected location.
4. Save as `<original>_remediated.pdf`.

IMPORTANT LIMITATION — be honest with the user: true PDF tag-structure repair
(adding </H1> tags, <Alt> text on <Figure> tags, re-ordering the logical reading
order) cannot be done with fidelity in code — that requires Adobe Acrobat DC Pro.
This script handles the automatable fixes and flags the rest; list any Acrobat-only
remediation steps explicitly in the review report.

### Step 5: Ask User for Save Path
**IMPORTANT:** Before saving the final products, ask the user:
- "Where would you like me to save the report and edited copy? (e.g., C:\Users\cruzmars\Documents)"
- Wait for user response before saving to the specified location.

### Step 6: Save and Deliver
Save all artifacts to the user-specified path and confirm completion.

## Compliance Areas

### Section 508 (Federal Standards)
- **Heading Structure**: Logical, hierarchical heading hierarchy (H1-H6) in PDF
- **Form Field Labeling**: Proper labeling for form fields in PDF forms
- **Table Accessibility**: Captions, column headers, sufficient contrast in PDF
- **Navigation**: Keyboard-navigable PDF structure, logical reading order
- **Metadata**: Document properties, title, author, keywords
- **Alt Text**: Missing or incorrect alt text for images, charts, diagrams in PDF
- **Reading Order**: Correct reading order for screen readers

### WCAG 2.2 (Web Content Accessibility Guidelines, W3C Recommendation Dec 2024)

WCAG 2.2 is the governing standard behind Section 508. Full normative text lives in
`website-accessibility-agent/references/WCAG 2.2 Standards Dec 2024.txt`.

- **Non-text Content**: Alternative text for images, charts, diagrams in PDF
- **Contrast**: Minimum 4.5:1 for normal text, 3:1 for large text in PDF (SC 1.4.3)
- **Scalable Text**: Text must be legible at 200% zoom without loss of functionality
- **Keyboard Navigation**: Full keyboard operability for PDF forms and navigation (SC 2.1.1)
- **Predictable Layout**: Consistent navigation and interaction patterns in PDF
- **Text Alternatives**: Sufficient text alternatives for non-text content in PDF

## Review Process
1. Parse the .pdf file using PyPDF/PdfMiner or similar tool
2. Check heading hierarchy (H1→H6 progression) in PDF outline
3. Validate form field labels and error handling in PDF forms
4. Scan for missing alt text on images, charts, diagrams
5. Measure color contrast for text and UI elements in PDF
6. Verify keyboard navigation flow for PDF forms
7. Report findings with line/paragraph references

## Output Format
- Summary of compliance status (Pass/Fail/Needs Improvement)
- Specific violations with file/line references
- Actionable recommendations
- Severity rating (Critical/High/Medium/Low)

## Default Save Location
If user does not specify a path, save to: C:\Users\cruzmars\Documents
