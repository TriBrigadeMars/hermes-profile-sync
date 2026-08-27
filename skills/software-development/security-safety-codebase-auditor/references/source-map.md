# Standards and Source Map

Accessed/assembled: 2026-08-25.

This file explains how external guidance shaped the skill. These mappings are design provenance, not a claim of formal certification, compliance, or endorsement.

## Primary sources

### Hermes Agent skill system

- Hermes Agent, **Creating Skills**: https://hermes-agent.nousresearch.com/docs/developer-guide/creating-skills
- Hermes Agent, **Skills System**: https://hermes-agent.nousresearch.com/docs/user-guide/features/skills/
- Hermes Agent, **Working with Skills**: https://hermes-agent.nousresearch.com/docs/guides/work-with-skills
- Hermes Agent, **Built-in Tools Reference**: https://hermes-agent.nousresearch.com/docs/reference/tools-reference/

**Incorporated as:** this package follows the Hermes skill structure with `SKILL.md`, YAML frontmatter, `references/`, `templates/`, and `scripts/`; it uses the terminal toolset and references bundled files through `${HERMES_SKILL_DIR}`.

### OWASP Application Security Verification Standard (ASVS) 5.0.0

- OWASP Foundation, **Application Security Verification Standard**: https://owasp.org/www-project-application-security-verification-standard/
- Latest stable version stated by OWASP: **5.0.0**, released 2025-05-30.

**Incorporated as:** ASVS is the primary technical verification baseline. It drove the skill's requirement to inspect concrete, testable application controls rather than rely on generic vulnerability categories. It especially informs authentication, authorization, encoding/injection prevention, data protection, communications, API, file, cryptographic, configuration, and logging review. The skill intentionally does not reproduce ASVS requirement text or claim a formal ASVS level.

### OWASP Top 10:2025

- OWASP Foundation, **OWASP Top 10:2025**: https://owasp.org/Top10/2025/

Current categories at the time this skill was assembled include Broken Access Control, Security Misconfiguration, Software Supply Chain Failures, Cryptographic Failures, Injection, Insecure Design, Authentication Failures, Software or Data Integrity Failures, Security Logging and Alerting Failures, and Mishandling of Exceptional Conditions.

**Incorporated as:** the current Top 10 shapes prioritization and keeps exceptional/failure paths, supply chain, secure design, logging, and integrity in scope rather than focusing only on classic injection/authentication flaws.

### CWE Top 25 Most Dangerous Software Weaknesses 2025

- MITRE CWE, **2025 CWE Top 25**: https://cwe.mitre.org/top25/archive/2025/2025_cwe_top25.html
- Current Top 25 project page: https://cwe.mitre.org/top25/

**Incorporated as:** the audit explicitly looks for common implementation weaknesses represented in current vulnerability data, including XSS, SQL injection, CSRF, missing/incorrect authorization, path traversal, OS/code injection, unsafe file upload, untrusted deserialization, improper input validation, sensitive-information exposure, missing authentication, SSRF, and unbounded resource allocation. For native code, it also checks memory-corruption classes.

### NIST SP 800-218 Secure Software Development Framework (SSDF) 1.1

- NIST CSRC, **SP 800-218 SSDF Version 1.1 (Final)**: https://csrc.nist.gov/pubs/sp/800/218/final
- NIST SSDF project: https://csrc.nist.gov/Projects/ssdf

**Version note:** NIST published an initial public draft of SSDF 1.2 (SP 800-218 Rev. 1) on 2025-12-17, but as of 2026-08-25 the NIST SSDF publications page still lists 1.2 as **Draft** and 1.1 as **Final**. This skill therefore uses 1.1 as the normative NIST baseline and treats 1.2 only as future-facing context.

**Incorporated as:** SS-19 and the overall workflow emphasize secure-development practices across preparation, protected development environments, secure production, vulnerability response, root-cause prevention, and repeatable evidence. The skill does not infer organizational SSDF conformance from repository code alone.

### CISA Secure by Design

- CISA and international partners, **Shifting the Balance of Cybersecurity Risk: Principles and Approaches for Secure by Design Software**: https://www.cisa.gov/resources-tools/resources/secure-by-design
- CISA/FBI, **Product Security Bad Practices** update (2025): https://www.cisa.gov/news-events/alerts/2025/01/17/cisa-and-fbi-release-updated-guidance-product-security-bad-practices
- CISA, **The Case for Memory Safe Roadmaps**: https://www.cisa.gov/resources-tools/resources/case-memory-safe-roadmaps

**Incorporated as:** prioritize secure defaults, manufacturer/developer ownership of security outcomes, reduction of entire vulnerability classes, least privilege, strong authentication, elimination of default credentials, safe update/patch behavior, and memory-safe languages or prioritized mitigation/migration for high-risk native code. SS-17 and SS-18 treat catastrophic failure and unsafe high-impact operation design as engineering concerns rather than mere user-configuration problems.

### SLSA 1.2

- SLSA, **Version 1.2 Approved Specification**: https://slsa.dev/spec/v1.2/
- SLSA, **Source Track Requirements**: https://slsa.dev/spec/v1.2/source-requirements
- SLSA, **Build Track Basics**: https://slsa.dev/spec/v1.2/build-track-basics
- SLSA, **Threats and Mitigations**: https://slsa.dev/spec/v1.2/threats

SLSA 1.2 was released on 2025-11-24 and is the current approved specification at assembly time. It includes both Build and Source tracks.

**Incorporated as:** SS-10 and SS-11 inspect source-control trust, branch/review protections, provenance, hosted/hardened builds, artifact integrity, build isolation, attestations, and release verification. The skill must never claim a SLSA level unless every applicable requirement for that level is actually supported by evidence.

## Supporting sources

### OWASP Cheat Sheet Series

- OWASP Cheat Sheet Series: https://cheatsheetseries.owasp.org/

**Incorporated as:** implementation-level remediation guidance for focused topics such as authentication, authorization, session management, CSRF, XSS prevention, SSRF prevention, file upload, secrets management, cryptographic storage, logging, and secure headers. Use the relevant current cheat sheet when a concrete remediation needs more detail.

### OWASP API Security Top 10

- OWASP API Security Project: https://owasp.org/www-project-api-security/

**Incorporated as:** API-specific abuse paths such as object/function authorization failures, resource consumption, server-side request forgery, inventory/exposure issues, and unsafe consumption of third-party APIs are explicitly considered in SS-02, SS-05, SS-15, and architecture inventory.

## Control-to-source crosswalk

| Control | Primary provenance | How it appears in the audit |
|---|---|---|
| SS-01 Authentication/Sessions | OWASP ASVS 5.0; OWASP Top 10:2025 | Validate identity proof, token/session lifecycle, recovery, MFA and service identities |
| SS-02 Authorization/Tenants | OWASP ASVS 5.0; OWASP Top 10:2025; CWE Top 25 | Resource/action authorization, ownership, tenant predicates, admin boundaries |
| SS-03 Injection/Interpretation | OWASP ASVS 5.0; OWASP Top 10:2025; CWE Top 25 | Follow untrusted data into SQL, shell, templates, expressions and other interpreters |
| SS-04 Browser/Client | OWASP ASVS 5.0; CWE Top 25 | XSS, CSRF, CORS, cookie and redirect/security-header review |
| SS-05 SSRF/Egress | OWASP ASVS 5.0; CWE Top 25; OWASP API Security | Destination validation, redirects, DNS/IP checks, sensitive header forwarding |
| SS-06 Files/Archives | OWASP ASVS 5.0; CWE Top 25 | Path containment, upload validation, archive extraction, temp-file safety |
| SS-07 Deserialization/Dynamic Code | OWASP ASVS 5.0; CWE Top 25 | Dangerous object reconstruction, code/command execution, plugin and parser boundaries |
| SS-08 Secrets/Crypto | OWASP ASVS 5.0; OWASP Top 10:2025 | Secret lifecycle, approved primitives, randomness, TLS and signing/token integrity |
| SS-09 Data Lifecycle | OWASP ASVS 5.0; CISA Secure by Design | Minimize/protect sensitive data across stores, logs, caches, backups and exports |
| SS-10 Supply Chain | OWASP Top 10:2025; NIST SSDF; SLSA 1.2 | Dependency/source/build provenance, integrity, signing, pinning and artifact trust |
| SS-11 CI/CD | NIST SSDF; SLSA 1.2; CISA Secure by Design | Workflow permissions, untrusted build inputs, protected releases, privileged tokens |
| SS-12 Config/Cloud/IaC | OWASP Top 10:2025; ASVS 5.0; CISA Secure by Design | Secure defaults, least privilege, exposure, containers, IAM and production hardening |
| SS-13 Logging/Alerting | OWASP Top 10:2025; ASVS 5.0; NIST SSDF | Security-event coverage, audit trail quality, safe telemetry and incident signals |
| SS-14 Exceptional Conditions | OWASP Top 10:2025; ASVS 5.0 | Fail-safe error handling, policy-service failure, transactions, rollback and recovery |
| SS-15 Resource Exhaustion | CWE Top 25; OWASP API Security; ASVS 5.0 | Hard quotas and bounds for requests, concurrency, retries, queues and expensive actions |
| SS-16 Business Logic/Races | ASVS 5.0; OWASP secure-design principles | Replay, state-machine bypass, TOCTOU, idempotency and invariant enforcement |
| SS-17 Memory Safety | CWE Top 25; CISA Secure by Design | Native/unsafe code scrutiny, sanitizers/fuzzing, memory-safe language prioritization |
| SS-18 High-Impact Safety | CISA Secure by Design; OWASP Insecure Design | Narrow authority, exact confirmation, blast-radius limits, observability and reversibility |
| SS-19 Testing/Vulnerability Mgmt | NIST SSDF; ASVS 5.0; CISA Secure by Design | Regression tests, scanning/fuzzing where appropriate, patch/update and root-cause prevention |

## Interpretation rules

1. Frameworks inform review questions; repository evidence determines findings.
2. OWASP Top 10 and CWE Top 25 are prioritization inputs, not complete verification standards.
3. ASVS is used as a technical-control reference, not as a certification claim.
4. NIST SSDF is a lifecycle framework; repository inspection alone cannot establish organizational conformance.
5. SLSA levels must not be claimed from partial evidence.
6. CISA Secure by Design guidance is used to favor secure defaults and elimination of vulnerability classes; it does not automatically make every deviation a vulnerability.
7. Use the newest applicable framework version when a user requests current mapping, and explicitly note version/date differences.
8. If this audit discovers AI-specific trust boundaries, cross-reference the companion AI guardrails skill rather than stretching conventional controls into model-specific claims.
