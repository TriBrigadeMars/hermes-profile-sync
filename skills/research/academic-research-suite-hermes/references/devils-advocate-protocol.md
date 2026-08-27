# Devil's Advocate Protocol

## Purpose

The `devils_advocate_agent` and `devils_advocate_reviewer_agent` exist to challenge assumptions, detect logical fallacies, and surface the strongest counter-arguments. They operate as independent checkpoints throughout the pipeline.

## When Activated

- Deep Research: Phase 1 (RQ scoping), Phase 3 (synthesis), Phase 5 (review), Socratic Mode (Layers 2, 4)
- Paper Reviewer: Phase 1 (parallel review panel)
- Pipeline: Continuous advisory (non-blocking) + checkpoint gate (blocking)

## Checkpoint Rules

1. **Critical issues block progression**: If Devil's Advocate finds a CRITICAL issue, the current stage cannot PASS until addressed or explicitly acknowledged.
2. **Cannot be bypassed by consensus**: Even if all other agents/reviewers agree, a CRITICAL Devil's Advocate finding overrides.
3. **Must be specific**: Vague skepticism is not enough. Every challenge must identify: (a) the specific claim being challenged, (b) the logical flaw or missing evidence, (c) the strongest counter-argument or alternative explanation.

## Devil's Advocate Report Format

```
## Strongest Counter-Argument (200–300 words)
[State the single most powerful objection to the paper's core thesis]

## Issue List
### CRITICAL
1. [Issue] → [Evidence] → [Suggested remediation]
2. ...

### MAJOR
1. [Issue] → [Evidence] → [Suggested remediation]
2. ...

### MINOR
1. [Issue] → [Evidence] → [Suggested remediation]
2. ...

## Ignored Alternative Explanations
- [Alternative 1]: Why it was not addressed
- [Alternative 2]: Why it was not addressed

## Missing Stakeholder Perspectives
- [Perspective 1]: Whose voice is absent
- [Perspective 2]: Whose voice is absent

## Observations (Non-Defects)
- [Interesting pattern that is not a flaw but worth noting]
```

## Review Panel Iron Rules

- 5 reviewers (EIC + 3 peers + Devil's Advocate) review independently
- No cross-referencing between reviewers during Phase 1
- Synthesizer in Phase 2 can only cite specific Phase 1 reports, never fabricate
- Devil's Advocate CRITICAL issues → Editorial Decision cannot be Accept
