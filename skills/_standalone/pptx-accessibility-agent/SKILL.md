---
name: pptx-accessibility-agent
version: 1.0.0
author: Mars Cruz
license: MIT
tags: [accessibility, pptx, powerpoint, section508, wcag, a11y]
related_skills: [docx-accessibility-agent, pdf-accessibility-agent, writing-style-agent, powerpoint-style-agent]
description: Review .pptx files for Section 508 and WCAG 2 compliance.
---
# PowerPoint Accessibility Agent

## Purpose
Review .pptx files for Section 508 (US Federal Standards) and WCAG 2 accessibility compliance.

## When to Use
Use this agent when reviewing internal documents, proposals, reports, or any .pptx file that needs to meet federal accessibility requirements or be usable by people with disabilities.

## Workflow

### Step 1: Load the Document
Read the .pptx file and extract its content.

### Step 2: Run Accessibility Checks
Apply Section 508 and WCAG 2 compliance criteria to the document.

### Step 3: Generate Review Report
Create a structured report with findings, severity ratings, and recommendations.

### Step 4: Produce an Edited Copy (Speaker Notes + Summary Slide)
**This is the core deliverable.** Produce a revised `.pptx` with remediation
suggestions embedded. Note: python-pptx 1.0.2 has NO comment API and PowerPoint has
NO track-changes feature, so the reliable mechanism is **speaker notes** + a final
**summary slide** listing every suggested edit so changes are visible on the slides.

Use the bundled helper `scripts/pptx_remediate.py` (VERIFIED with python-pptx 1.0.2):
- `add_note(slide, text)` — append a "REMEDIATION: …" line to the slide's speaker notes
- `add_summary_slide(prs, suggestions)` — add a closing "Suggested Changes Summary"
  slide enumerating all edits

Workflow:
1. Open the original `.pptx`.
2. For automatable fixes (adding a slide title, list formatting, alt text placeholders,
   reading-order reorder): apply them directly to shapes where possible.
3. For each judgment call (contrast, sensory characteristics, embedded media):
   `add_note()` on the affected slide + collect in the `add_summary_slide()` list.
4. Save as `<original>_remediated.pptx`.

(If you later need REAL PowerPoint comments, that requires hand-rolling
`/ppt/comments.xml` + `/ppt/commentAuthors.xml` OPC parts — python-pptx exposes none
of this; flag it to the user rather than silently skipping.)

### Step 5: Ask User for Save Path
**IMPORTANT:** Before saving the final products, ask the user:
- "Where would you like me to save the report and edited copy? (e.g., C:\Users\cruzmars\Documents)"
- Wait for user response before saving to the specified location.

### Step 6: Save and Deliver
Save all artifacts to the user-specified path and confirm completion.

## Compliance Areas

### Section 508 (Federal Standards)
- **Slide Title Hierarchy**: Every slide must have a title (Section 508 §1.3.1, WCAG 2.4.6). Screen readers use slide titles to navigate. The hierarchy is: Deck Title (Title layout) → Section Titles (Section layout) → Slide Titles (Title Content layout). No untitled slides except `blank` layouts.
- **Heading Structure**: Logical, hierarchical heading hierarchy (H1-H6) throughout the presentation
- **Form Fields**: Proper labeling for all form controls (labels, placeholders, error handling)
- **Table Accessibility**: Captions, column headers, sufficient contrast
- **Navigation**: Keyboard-navigable structure, logical reading order
- **Metadata**: Document properties, title, author, keywords
- **Alt Text**: Missing or incorrect alt text for images, charts, tables
- **Reading Order**: Correct reading order for screen readers

### WCAG 2.2 (Web Content Accessibility Guidelines, W3C Recommendation Dec 2024)

WCAG 2.2 is the governing standard behind Section 508. Full normative text lives in
`website-accessibility-agent/references/WCAG 2.2 Standards Dec 2024.txt`.

- **Non-text Content**: Alternative text for images, charts, diagrams (SC 1.1.1)
- **Contrast**: Minimum 4.5:1 for normal text, 3:1 for large text (SC 1.4.3)
- **Resizable Text**: Text must be scalable up to 200% without loss of functionality
- **Keyboard Navigation**: Full keyboard operability (SC 2.1.1)
- **Predictable Layout**: Consistent navigation and interaction patterns
- **Text Alternatives**: Sufficient text alternatives for non-text content

## Review Process
1. Parse the .pptx file using python-pptx
2. Check slide title hierarchy — every slide (except `blank`) must have a title; verify Title → Section → Slide Title progression
3. Check heading hierarchy (H1→H6 progression)
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
