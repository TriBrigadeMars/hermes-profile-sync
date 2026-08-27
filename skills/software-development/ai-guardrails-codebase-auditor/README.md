# AI Guardrails Codebase Auditor for Hermes Agent

A read-only-by-default Hermes skill for auditing LLM, RAG, agentic, tool/MCP, and AI-enabled codebases for guardrail failures and AI-specific security/safety risks.

## Install

Copy the `ai-guardrails-codebase-auditor` directory into a Hermes skills directory, for example:

```bash
mkdir -p ~/.hermes/skills/software-development
cp -R ai-guardrails-codebase-auditor ~/.hermes/skills/software-development/
```

Hermes also supports project-local skills under `<project-root>/.hermes/skills/` and `<project-root>/.agents/skills/`; project-local skills require explicit trust in Hermes.

Then start Hermes and request an audit, for example:

```text
Use the ai-guardrails-codebase-auditor skill to audit this repository. Prioritize prompt injection, excessive agency, RAG tenant isolation, memory poisoning, tool/MCP trust, and high-impact output sinks.
```

## Package contents

- `SKILL.md` — operational instructions Hermes loads on demand.
- `references/audit-controls.md` — 14 implementation-oriented audit control families.
- `references/source-map.md` — external standards, URLs, and control-to-source crosswalk.
- `templates/audit-report.md` — structured final audit format.
- `scripts/ai_surface_inventory.py` — optional read-only standard-library discovery helper.

## Design goals

- Evidence-based findings tied to exact repository paths/lines/symbols.
- End-to-end attack-path analysis rather than keyword-only scanning.
- Deterministic authorization and least privilege outside the model.
- Explicit treatment of indirect prompt injection, agent/tool authority, MCP/tool metadata, RAG, persistent memory, output sinks, tenant isolation, budgets, approvals, monitoring, and regression testing.
- Separation of confirmed findings, probable risks, and verification gaps.
- Non-destructive validation by default.

## References

See `references/source-map.md`. Primary design inputs include current Hermes skill-authoring documentation, OWASP GenAI LLM Top 10 2026, OWASP Top 10 for Agentic Applications 2026, OWASP AI Testing Guide v1, and NIST AI RMF / NIST AI 600-1.
