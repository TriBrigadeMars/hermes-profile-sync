---
name: powerpoint-style-agent
description: Create PowerPoint presentations in Mars Cruz's style.
version: 1.0.0
author: hermes
license: MIT
metadata:
  hermes:
    tags: [powerpoint, presentations, training, slides, OE]
    related_skills: [writing-style-agent, apa-7-style-agent, ap-stylebook-agent]
---

# PowerPoint Presentation Agent — Mars Cruz Style

## When to Use

Use this agent when creating, drafting, or reviewing PowerPoint presentations that should match Mars Cruz's training and presentation style. Trigger when user asks to build a PPTX, create slides, or draft a training deck.

## Purpose

Generate PowerPoint presentations that match the structure, tone, and pedagogical approach Mars Cruz uses in Office of Equity trainings at CU Anschutz.

## Deck Architecture (consistent across all 11 decks analyzed)

### Slide 1 — Title Slide
- Training/presentation name (large, centered)
- "Presented By Mars Cruz, MPH, CHES"
- Title: "Prevention, Education, and Outreach Coordinator"
- Office: "Office of Equity"
- Email: mars.cruz@cuanschutz.edu
- Website: https://www.ucdenver.edu/offices/equity

### Slide 2 or 3 — Meet the Prevention Team
- "Hello! My name is Mars Cruz, my pronouns are she/they"
- Background: "Before moving to Colorado for this role I served as a Health Education Specialist and Communicable Disease Investigator for Merced County Dept. of Public Health and Fresno County Dept. of Public Health respectively."
- Personal touch: "Loki the Cat is my wonderful child."
- Disclaimer: "I am not a lawyer. Nothing I say should be construed as legal advice."

### Slide 2 or 3 — Presentation Agenda
- Numbered list (1., 2., 3.)
- Sometimes with sub-bullets (a., b.)
- Always at the start

### Closing Slide — Always
- "Thank You For Listening!"
- Full contact block (name, credentials, title, office, email)
- Co-presenter info if applicable

## Slide Title Hierarchy

Every deck follows a three-level title hierarchy:

| Level | Layout | Purpose | Example |
|-------|--------|---------|---------|
| **Deck Title** | `title` | Opening slide — presentation name, presenter, date | "Sexual Misconduct Prevention Training" |
| **Section Title** | `section` | Divider before each major topic — section name + brief description | "Understanding the Continuum of Behavior" |
| **Slide Title** | `title_content` | Each content slide — fragment, not sentence | "Key Definitions" |

**Rules:**
- The `title` layout is used **once** (first slide). It carries the deck name and subtitle (presenter credentials, date, tagline).
- `section` layouts are used **before each major topic shift**. They serve as navigation landmarks for screen readers.
- Every `title_content` and `two_content` slide **must have a title** — no untitled slides.
- Subtitle text goes **only** on `title` and `section` layouts — not on content slides.
- Slide titles are **fragments**: "Myth vs. Fact" not "Let's look at some myths and facts."

## Slide Types & When to Use Them

### 1. Content Slide (most common)
- **Layout:** `title_content`
- Bold header (fragment, not sentence)
- Bullet points or numbered list below
- Brief explanations, not paragraphs
- Example: "Intentional Incivility / 1. Common Behaviors / a. Double standards..."

### 2. Audience Poll Slide
- **Layout:** `title_only` (question as title, no body text)
- Question centered on slide
- "When you hear the phrase [X], what comes to mind?"
- "In one or two sentences, describe to me [concept]?"
- "How many of us have heard of [topic]?"
- No bullet points — just the question

### 3. Myth/Fact Slide
- **Layout:** `two_content` or `title_content` with stacked bullets
- Two-column or stacked format
- "Myth: [common misconception]"
- "Fact: [correction]"
- Used for: sexual misconduct, protected-class discrimination, consent

### 4. Framework Slide
- **Layout:** `title_content` or `blank` (for custom shapes/matrices)
- 2x2 matrix or continuum
- Examples: "Low Impact / High Impact / Individual / Organizational"
- "Respectful → Disrespectful → Abusive → Unlawful → Assaultive"
- "Perceived Respect / Organizational Performance"

### 5. Scenario/Case Study Slide
- **Layout:** `title_content`
- Describe situation plainly
- "At Company A, Senior PI John Smith had been reported to HR..."
- Follow with discussion prompts (numbered)
- Real cases: "California Civil Rights Department v. Activision Blizzard (2023)"

### 6. Resource Directory Slide
- **Layout:** `title_content` or `two_content` (for side-by-side resources)
- Office/Resource name as header
- What they do (1-2 lines)
- Contact info (email, phone, website)
- "This is not an exhaustive list..."

### 7. Flowchart/Process Slide
- **Layout:** `blank` (custom shapes for flowchart)
- Visual decision tree
- "OE receives a report → Is it within jurisdiction? → Yes/No branches"
- Simple branching logic

### 8. Reflection/Closing Slide
- **Layout:** `title_only` (question as title)
- "What is A Change You Hope To Take Away or See from This Training?"
- Sub-prompts: "Is it mindset-related?" "How can staff see this change?"
- "Any Questions or Comments?"

### 9. Break Slide
- **Layout:** `title_only`
- "Let's take a quick break!"
- Humanizing options: snack, water, restroom, stretch
- Light tone, numbered list

### 10. Disclaimer/Legal Slide
- **Layout:** `title_content`
- Numbered disclaimers (1. I am not a lawyer, 2. My opinions are my own, 3. Fictional resemblance)
- Data consent notices for focus groups
- Prerequisites for advanced trainings

## Pedagogical Patterns

### Engagement Sequence (typical flow)
1. Poll question → audience responds
2. Content delivery → frameworks, lists, definitions
3. Myth/Fact → debunk misconceptions
4. Scenario → apply knowledge
5. Discussion prompts → "What do you think?"
6. Takeaways → "What will you change?"

### Audience Adaptations
- **Students**: Personal conduct focus, "Being a Responsible Student"
- **Employees**: Mandatory reporting focus, "Being a Responsible Employee"
- **Leadership**: Pitch deck format, USP, ROI, organizational impact
- **Department-specific**: Simplified language, adapted examples (e.g., SODM version)

### Transitions Between Sections
- "Speaking of [topic].." (conversational bridge)
- "So, what are the proposed changes?" (direct question)
- "Moving Forward?" (next steps)
- "What is to be done?" (call to action)

## Voice & Tone

- **Conversational but authoritative** — "Hello! My name is Mars" not "Good evening, esteemed colleagues"
- **Self-deprecating humor** — "I am not a lawyer. That is important because..." [cat photo]
- **Direct language** — "Being an unpleasant, even rude, individual is not illegal."
- **Inclusive framing** — "How can we ensure actual dialogue?"
- **Action-oriented** — "Start small, start tangible, ask for external help"
- **Plain-language definitions** — avoids jargon, explains legal concepts simply

## Recurring Frameworks

1. **Shared pool of knowledge** — collaborative learning concept
2. **20/80 rule** — invest in lower-risk, higher-agency activities
3. **Continuum of Behavior** — Respectful → Unlawful → Assaultive
4. **Coaching Model** — Set Tone → Be Specific → Identify Gap → Consequences → Ask & Plan → Reset
5. **2x2 matrices** — Individual/Organizational × Low/High Impact
6. **Myth/Fact** — debunk misconceptions directly
7. **"Why the history lesson?"** — connect past to present relevance

## Slide Writing Rules

1. **Fragments, not sentences** — "Multilingual and Accessible Online Trainings" not "We are working on..."
2. **Bold headers** with brief explanations below
3. **Numbered lists** for processes, sequences, steps
4. **Bulleted lists** for examples, options, categories
5. **Em dashes and colons** for emphasis
6. **No paragraphs** — if it needs a paragraph, split across slides
7. **Mix formal policy language and casual tone** within same deck

## Technical Notes

- Use python-pptx for generation
- Title slide: centered, large font
- Content slides: left-aligned, clean layout
- Contact slide: consistent formatting with all credentials
- Include QR codes when referencing companion documents
- Include feedback form links when appropriate

## Usage

When creating a presentation for Mars:
1. Determine audience (students, employees, leadership, department-specific)
2. Select appropriate deck architecture
3. Open with title slide + Meet the Prevention Team
4. Build content using appropriate slide types
5. Include audience engagement moments (polls, scenarios, reflection)
6. Close with "Thank You For Listening!" + contact block
7. Match voice: conversational, direct, inclusive, action-oriented

## Save-Path Workflow

**IMPORTANT:** Before saving any deliverable (PowerPoint deck, slide report, revised presentation), ask the user:
- "Where would you like me to save this? (e.g., C:\Users\cruzmars\Documents)"
- Wait for user response before saving to the specified location.
- If user does not specify, default to: C:\Users\cruzmars\Documents\Hermes Research Output
