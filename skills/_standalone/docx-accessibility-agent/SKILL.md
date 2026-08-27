---
name: docx-accessibility-agent
version: 1.0.0
author: Mars Cruz
license: MIT
tags: [accessibility, docx, section508, wcag, a11y]
related_skills: [writing-style-agent, powerpoint-style-agent]
description: Review .docx files for Section 508 and WCAG 2 compliance.
---
# Docx Accessibility Agent

## Purpose
Review .docx files for Section 508 (US Federal Standards) and WCAG 2 accessibility compliance.

## When to Use
Use this agent when reviewing internal documents, proposals, reports, or any .docx file that needs to meet federal accessibility requirements or be usable by people with disabilities.

## Workflow

### Step 1: Load the Document
Read the .docx file and extract its content.

### Step 2: Run Accessibility Checks
Apply Section 508 and WCAG 2 compliance criteria to the document.

### Step 3: Generate Review Report
Create a structured report with findings, severity ratings, and recommendations.

### Step 4: Produce an Edited Copy (with Track Changes + Comments)
**This is the core deliverable.** Produce a revised `.docx` where every recommended
fix is applied as a **tracked change** (so the author can Accept/Reject each edit in
Word's Review pane) and/or a **margin comment** explaining the "why" of each change.

Use the bundled helper `scripts/docx_remediate.py` (VERIFIED with python-docx 1.2.0):
- `insert_tracked(paragraph, text)` — add corrected text as a tracked *insertion* (w:ins)
- `delete_tracked(paragraph, text)` — remove text as a tracked *deletion* (w:del/w:delText)
- `add_comment(document, run, text)` — attach a real Word comment (comments.xml part +
  w:commentRangeStart/End + w:commentReference)

Workflow for the edited copy:
1. Open the original `.docx`.
2. For automatable fixes (headings, alt text, descriptive links, list formatting,
   metadata): apply them directly as tracked changes so Word surfaces each edit.
3. For each non-automatable judgment call (contrast, reading order, bias-free
   wording): attach a `add_comment` explaining what to change and why.
4. Save as `<original>_remediated.docx`.

Final output = THREE artifacts: (a) review report `.md`, (b) remediated `.docx`
with tracked changes, (c) a plain suggestions list inline in the report.

### Step 5: Ask User for Save Path
**IMPORTANT:** Before saving the final products, ask the user:
- "Where would you like me to save the report and edited copy? (e.g., C:\Users\cruzmars\Documents)"
- Wait for user response before saving to the specified location.

### Step 6: Save and Deliver
Save all artifacts to the user-specified path and confirm completion.

## Compliance Areas

### Section 508 (Federal Standards)
- **Heading Structure**: Logical, hierarchical heading hierarchy (H1-H6) throughout the document
- **Form Fields**: Proper labeling for all form controls (labels, placeholders, error handling)
- **Table Accessibility**: Captions, column headers, sufficient contrast
- **Navigation**: Keyboard-navigable structure, logical reading order
- **Metadata**: Document properties, title, author, keywords
- **Alt Text**: Missing or incorrect alt text for images, charts, tables
- **Reading Order**: Correct reading order for screen readers

### WCAG 2.2 (Web Content Accessibility Guidelines, W3C Recommendation Dec 2024)

WCAG 2.2 is the governing standard behind Section 508. Full normative text lives in
`website-accessibility-agent/references/WCAG 2.2 Standards Dec 2024.txt`.

- **Non-text Content**: Alternative text for images, charts, diagrams
- **Contrast**: Minimum 4.5:1 for normal text, 3:1 for large text (SC 1.4.3)
- **Resizable Text**: Text must be scalable up to 200% without loss of functionality
- **Keyboard Navigation**: Full keyboard operability (SC 2.1.1)
- **Predictable Layout**: Consistent navigation and interaction patterns
- **Text Alternatives**: Sufficient text alternatives for non-text content

## Review Process
1. Parse the .docx file using python-docx
2. Check heading hierarchy (H1→H6 progression)
3. Validate form field labels and error handling
4. Scan for missing alt text on images/charts
5. Measure color contrast for text and UI elements
6. Verify keyboard navigation flow
7. Report findings with line/paragraph references

## Output Format
- Summary of compliance status (Pass/Fail/Needs Improvement)
- Specific violations with file/line references
- Actionable recommendations
- Severity rating (Critical/High/Medium/Low)

## Default Save Location
If user does not specify a path, default to: C:\Users\cruzmars\Documents\Hermes Research Output
**ALWAYS ask the user where to save before writing** — never assume the default.
