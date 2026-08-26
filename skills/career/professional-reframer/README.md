# Professional Reframer for Hermes

**Version 0.1.0**

A local-first Hermes skill for translating truthful work experience into clear, credible, business-legible LinkedIn and professional language without turning it into corporate jargon or inflating responsibility.

## What it does

- professional reframing of informal work descriptions;
- LinkedIn headline, About, and Experience rewriting;
- business-function identification;
- impact framing;
- responsibility/seniority calibration;
- target-role keyword integration when supported by evidence;
- anti-buzzword / anti-corporate-sludge editing;
- explanation mode;
- claim-delta checks for newly introduced leadership, ownership, scope, causality, expertise, and metrics.

## Philosophy

The transformation pipeline is:

`Evidence -> Business Function -> Impact -> Relevance -> Voice -> Claim-Delta Audit`

The governing rule is:

**Change the framing, not the facts.**

The skill does not equate "professional" with "jargon-heavy." It favors precise business concepts when they genuinely name the work and plain language when they do not.

## Reframing modes

- **Professional Reframe**
- **LinkedIn Reframe**
- **Find the Business Value**
- **Strengthen With Evidence**
- **De-Jargon**
- **Explain the Rewrite**

Reframing depth can be Light, Professional, LinkedIn, Narrative, or Executive-evidence-only.

## Optional integrations

The skill can consume outputs from:

- `career-profile` - canonical evidence source;
- `job-description-analyzer` - target requirements and terminology;
- `career-market-intelligence` - market-demand context;
- `resume-builder` / `resume-tailor` - reuse of verified candidate evidence.

Market data is allowed to change **emphasis**, never candidate truth.

## Local claim-delta helper

Lint a draft:

```bash
python scripts/reframe_guard.py lint --file draft.txt
```

Compare source and revision:

```bash
python scripts/reframe_guard.py compare --original original.txt --revised revised.txt
```

The helper is intentionally conservative. It is not an AI verifier and cannot determine truth. It flags wording that should be checked against evidence.

## Install

```bash
python install.py
```

Default location:

`~/.hermes/skills/career/professional-reframer/`

Start a new Hermes session after installation so the skill index reloads.

To test installation without touching your normal Hermes directory:

```bash
python install.py --dest /tmp/hermes-test/professional-reframer
```

## Tests

```bash
python -m unittest discover -s tests -v
```

## Source methodology

The skill's editorial philosophy was distilled from three user-provided books:

- *Smart Brevity: The Power of Saying More with Less*
- *60 Days to LinkedIn Mastery*
- *Talk Like TED*

The books are not distributed with the package. See `THIRD_PARTY_NOTICES.md`.

## License

Original code and skill materials: MIT. Third-party books and their content retain their original copyrights.
