---
name: website-accessibility-agent
version: 1.0.0
author: Mars Cruz
license: MIT
tags: [accessibility, wcag, wcag22, website, web, audit, section508, a11y]
related_skills: [docx-accessibility-agent, pdf-accessibility-agent, pptx-accessibility-agent, social-media-accessibility-agent, email-accessibility-agent]
description: Audit websites against WCAG 2.2 accessibility standards.
---

# Website Accessibility Agent

## Purpose
Audit live websites and web content against WCAG 2.2 (W3C Recommendation, 12 December 2024) — the standard underlying Section 508 — producing a criterion-by-criterion compliance report with severity ratings.

## When to Use
Use this agent when the user asks to:
- Audit a website or web page for accessibility
- Check WCAG 2.2 / Section 508 compliance of a site
- Prepare for an accessibility audit or VPAT/ACR documentation
- Review new web content before publication

## Workflow

1. **Fetch and inventory** the target page(s) — use browser tools to load each page.
2. **Run automated checks** via JavaScript evaluation in the live DOM (see checks below).
3. **Flag manual-check items** — WCAG has criteria automation cannot judge; list them with instructions.
4. **Produce the audit report** — pass/fail per criterion, severity, remediation guidance.
5. Ask the user where to save the deliverable before saving.
6. Save to the user-specified location.

## Save-Path Workflow

**IMPORTANT:** Before saving any deliverable, ask the user:
- "Where would you like me to save this? (e.g., C:\Users\cruzmars\Documents)"
- Wait for user response before saving to the specified location.
- If user does not specify, default to: C:\Users\cruzmars\Documents

## The Four Principles

Every audit is organized under WCAG's four principles (remember: **POUR**):

1. **Perceivable** — information/UI components must be presentable to users in ways they can perceive
2. **Operable** — UI components and navigation must be operable
3. **Understandable** — information and UI operation must be understandable
4. **Robust** — content must be robust enough for assistive technologies

## Automated Checks (runnable in live DOM)

### Perceivable
- All `<img>` have `alt` attributes (or `alt=""` + decorative intent)
- Images of text avoided; text contrast ratio ≥ 4.5:1 normal, ≥ 3:1 large text (18pt/14pt bold)
- `<video>` elements have captions track; `<audio>` has transcript link
- Page has `<html lang>` attribute set correctly

### Operable
- All functionality keyboard-operable: no positive `tabindex`, interactive elements are natively focusable
- Focus visible: check focus styles not removed (`outline: none` without replacement)
- Skip link present for bypassing repeated navigation
- `<title>` descriptive; headings (`h1`–`h6`) in logical order without skips
- Links have discernible text (no empty anchors); link purpose clear from text or context
- Timing adjustable: check for meta refresh / auto-redirect
- No content flashing more than 3 times per second

### Understandable
- `<html lang>` matches content language; language changes marked with `lang` on spans
- Forms: every input has associated `<label>` (or aria-label); required fields indicated in text not color alone
- Error identification: forms should surface errors in text near the field
- Navigation consistent across pages; repeated components identified consistently
- No automatic context change on focus without warning

### Robust
- Custom widgets have appropriate ARIA roles/states (`role=`, `aria-expanded`, etc.)
- Name, role, value available for all UI components
- Status messages use `aria-live` regions

### Sample JS probe (run via js/browser tools)
```javascript
(() => {
  const imgs = [...document.images];
  const noAlt = imgs.filter(i => !i.hasAttribute('alt')).length;
  const inputs = [...document.querySelectorAll('input:not([type=hidden]), select, textarea')];
  const unlabeled = inputs.filter(el =>
    !(el.labels && el.labels.length) &&
    !el.getAttribute('aria-label') &&
    !el.getAttribute('aria-labelledby')
  ).length;
  const h1s = document.querySelectorAll('h1').length;
  const headings = [...document.querySelectorAll('h1,h2,h3,h4,h5,h6')].map(h => +h.tagName[1]);
  let skips = 0;
  for (let i = 1; i < headings.length; i++) if (headings[i] - headings[i-1] > 1) skips++;
  const lang = document.documentElement.getAttribute('lang');
  const title = document.title;
  return {imagesTotal: imgs.length, imagesNoAlt: noAlt,
          inputsTotal: inputs.length, inputsUnlabeled: unlabeled,
          h1Count: h1s, headingSkips: skips, htmlLang: lang, title};
})()
```

## Manual Checks (flag for human review)

These cannot be judged by code alone — list them with step-by-step instructions:

- **Keyboard-only navigation walk-through** (SC 2.1.1, 2.4.3): tab through the page; verify logical order and no traps
- **Focus visibility** (SC 2.4.7, 2.4.11–13 *new in 2.2*): confirm focus indicator visible and not obscured by sticky headers/footers
- **Screen reader spot-check**: headings list sensible; form labels announced; dynamic updates announced
- **Contrast verification**: use Colour Contrast Analyser on sampled foreground/background pairs (automated probes can miss gradients/images behind text)
- **Target size** (SC 2.5.8 *new in 2.2*): interactive targets ≥ 24×24 CSS px
- **Dragging alternatives** (SC 2.5.7 *new in 2.2*): any drag action has a non-drag alternative
- **Consistent Help** (SC 3.2.6 *new in 2.2*) and **Accessible Authentication** (SC 3.3.8–3.3.9 *new in 2.2*: no cognitive-function tests unless alternative provided)
- **Error suggestion quality** (SC 3.3.3): are error messages actionable?

## WCAG 2.2 New Success Criteria (vs 2.1) — highlight these in audits

| SC | Name | Level |
|----|------|-------|
| 2.4.11 | Focus Not Obscured (Minimum) | AA |
| 2.4.12 | Focus Not Obscured (Enhanced) | AAA |
| 2.4.13 | Focus Appearance | AAA |
| 2.5.7 | Dragging Movements | AA |
| 2.5.8 | Target Size (Minimum) | AA |
| 3.2.6 | Consistent Help | A |
| 3.3.7 | Redundant Entry | A |
| 3.3.8 | Accessible Authentication (Minimum) | AA |
| 3.3.9 | Accessible Authentication (Enhanced) | AAA |

Note: SC 4.1.1 (Parsing) was removed/obsolete in WCAG 2.2 — do not report it as a failure.

## Conformance Levels

- **A** — minimum; site fails if any A criterion fails
- **AA** — the standard most laws/regulations require (including Section 508); audit target
- **AAA** — enhanced; report but do not treat as failure

Report format: for each criterion checked, record level, result (Pass/Fail/N/A/Manual), evidence (element count/screenshot/description), and fix recommendation.

## References
- `references/WCAG 2.2 Standards Dec 2024.txt` — full normative W3C text (all principles, guidelines, success criteria, conformance requirements)

## Output Format

```
# WCAG 2.2 Accessibility Audit — <site/page>
## Summary
- Pages audited: N
- Automated checks: X passed / Y failed
- Manual checks flagged: Z
- Conformance estimate: Passes at Level A/AA / Does not pass

## Findings by Principle (P-O-U-R)
Per criterion: [Level] [Pass/Fail/Manual] Criterion name
  Evidence: ...
  Fix: ...
  Severity: Critical/High/Medium/Low

## New-in-2.2 Spotlight
Results for the nine new success criteria

## Manual Test Instructions
Step-by-step for items requiring human judgment
```
