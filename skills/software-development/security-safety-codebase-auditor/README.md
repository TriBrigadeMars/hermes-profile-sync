# Security & Safety Codebase Auditor for Hermes Agent

A read-only-by-default Hermes skill for conventional application-security, software supply-chain, deployment, abuse-resistance, and fail-safe codebase review.

It is designed to complement the separate `ai-guardrails-codebase-auditor`: use this skill for ordinary security engineering and the AI skill for model/agent-specific trust boundaries.

## Install

Copy the `security-safety-codebase-auditor` directory into a Hermes skills directory, for example:

```bash
mkdir -p ~/.hermes/skills/software-development
cp -R security-safety-codebase-auditor ~/.hermes/skills/software-development/
```

Hermes also supports project-local skills under `<project-root>/.hermes/skills/` and `<project-root>/.agents/skills/`; project-local skills require explicit trust in Hermes.

Then ask Hermes to use it, for example:

```text
Use the security-safety-codebase-auditor skill to audit this repository. Prioritize authorization and tenant isolation, injection/unsafe interpretation, SSRF and file handling, secrets/crypto, CI/CD and supply-chain integrity, failure paths, resource exhaustion, and high-impact operations.
```

## Package contents

- `SKILL.md` - operational audit instructions.
- `references/audit-controls.md` - 19 implementation-oriented control families.
- `references/source-map.md` - external standards, URLs, version notes, and control-to-source crosswalk.
- `templates/audit-report.md` - structured final audit report.
- `scripts/security_surface_inventory.py` - optional read-only standard-library discovery helper.

## Design goals

- exact code/config evidence for confirmed findings;
- end-to-end attack/abuse-path analysis rather than scanner-result dumping;
- explicit authentication vs. authorization separation and tenant-boundary review;
- interpreter/sink analysis for injection and unsafe parsing;
- CI/CD, dependency, provenance, artifact and release-authority review;
- failure-path, rollback, idempotency, rate-limit and resource-bound analysis;
- explicit high-impact-operation and blast-radius safety checks;
- separation of confirmed vulnerabilities, probable risks, hardening opportunities, and verification gaps;
- non-destructive validation by default;
- redaction of secret values.

## Reference baseline

See `references/source-map.md`. Primary design inputs are OWASP ASVS 5.0.0, OWASP Top 10:2025, CWE Top 25:2025, NIST SSDF 1.1 (final), CISA Secure by Design guidance, and SLSA 1.2.
