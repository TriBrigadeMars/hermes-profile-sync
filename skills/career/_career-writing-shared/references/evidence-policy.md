# Candidate Evidence Policy

## Purpose

Every affirmative statement about the candidate must be grounded in candidate evidence. A job description, labor-market report, or model inference is never evidence that the candidate possesses a qualification.

## Evidence statuses

- `confirmed`: explicitly verified by the user.
- `user-supplied`: directly provided by the user and usable unless contradicted.
- `document-derived`: extracted from a candidate document; use conservatively and preserve uncertainty if extraction is ambiguous.
- `needs-confirmation`: do not turn into an affirmative claim until confirmed.

## Claim rules

1. Do not invent employers, dates, titles, degrees, certifications, metrics, technologies, scope, team size, budgets, or outcomes.
2. Do not upgrade weak evidence into stronger claims. "Supported a migration" does not become "led a migration" without evidence.
3. Do not infer a skill merely because a role commonly requires it.
4. If a useful metric is missing, either write the bullet without a metric or ask the user for the metric.
5. Preserve distinctions between participation, ownership, management, leadership, design, implementation, and approval authority.
6. If multiple evidence items conflict, flag the conflict rather than choosing the more impressive version.
7. A market gap is a development recommendation, never resume content.

## Traceability

When feasible, keep an internal mapping from each resume/cover-letter claim to one or more evidence IDs. The final user-facing document does not need to display the IDs unless requested.
