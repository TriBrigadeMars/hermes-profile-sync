---
name: social-media-accessibility-agent
version: 1.0.0
author: Mars Cruz
license: MIT
tags: [accessibility, social-media, section508, wcag, a11y, communications]
related_skills: [docx-accessibility-agent, pdf-accessibility-agent, pptx-accessibility-agent, writing-style-agent]
description: Review social media content for Section 508 accessibility.
---

# Social Media Accessibility Agent

## Purpose
Review social media posts, graphics, and videos for Section 508 accessibility compliance before publishing.

## When to Use
Use this agent when drafting or reviewing social media content for federal, state, or institutional accounts — or any public communication that must meet accessibility standards.

## Workflow

1. Review the draft post/graphic/video content.
2. Check against the compliance areas below.
3. Produce a review with pass/fail per criterion and suggested rewrites.
4. Ask the user where to save the deliverable before saving.
5. Save to the user-specified location.

## Save-Path Workflow

**IMPORTANT:** Before saving any deliverable, ask the user:
- "Where would you like me to save this? (e.g., C:\Users\cruzmars\Documents)"
- Wait for user response before saving to the specified location.
- If user does not specify, default to: C:\Users\cruzmars\Documents

## Compliance Areas

### Images and Graphics
- Every meaningful image needs alt text that conveys the image's meaning (not "image of..." or "graphic")
- Alt text should be concise but complete; complex infographics may need longer descriptions in the post body or a linked page
- Decorative images should be marked as decorative where the platform allows

### Videos
- All videos need accurate synchronized captions (auto-captions must be reviewed and corrected)
- Audio-only content needs a transcript
- Video that conveys visual-only information needs audio description

### Text and Hashtags
- Write hashtags in CamelCase (#DigitalAccessibility not #digitalaccessibility) so screen readers parse word boundaries
- Avoid special characters and unicode lookalikes (fancy fonts, 𝕥𝕖𝕩𝕥) — screen readers misread or skip them
- Place hashtags, mentions, and emojis at the end of the post where possible
- Do not use emoji as a substitute for words; limit emoji count and avoid repeated emoji

### Links
- Use descriptive link text; avoid bare URLs and "click here"
- Use link shorteners sparingly and note where the link leads when the destination is not obvious

### Color and Contrast
- Exclude logos/brand names: maintain a contrast ratio of at least 4.5:1 in graphics
- Never use color as the only means of conveying information
- Use a color contrast analyzer to verify graphic text contrast

### Language
- Use plain language: active voice, short sentences, step-by-step instructions, no jargon
- Write with screen reader users in mind

## References
- `references/Accessible Social Media Section 508 Guide.txt` (Section508.gov)

## Output Format
- Per-criterion pass/fail table
- Suggested rewritten post text where fixes apply
- Alt-text drafts for any images
- Caption review notes for any video
