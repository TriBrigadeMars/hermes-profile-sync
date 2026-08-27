---
name: security-safety-codebase-auditor
description: Audit codebases for conventional application security, software
  supply-chain, deployment, abuse-resistance, and fail-safe design risks.
version: 1.0.0
author: Custom
license: MIT
platforms: [ macos, linux, windows ]
metadata:
  hermes:
    tags:
      [
        application-security,
        code-audit,
        secure-by-design,
        supply-chain,
        threat-modeling,
        safety
      ]
    category: software-development
    requires_toolsets: [ terminal ]
---
# Security & Safety Codebase Auditor

## When to Use

Use this skill when the user asks to audit, review, assess, threat-model, or harden a software repository for conventional security or software-safety weaknesses: authentication, authorization, tenant isolation, injection, unsafe parsing, secrets, cryptography, file handling, SSRF, supply chain, CI/CD, deployment configuration, logging, exceptional conditions, resource exhaustion, business-logic abuse, unsafe privileged actions, or insecure defaults.

This skill is deliberately complementary to an AI/LLM guardrails audit. If the repository contains LLMs, RAG, agents, MCP/tool use, model-controlled actions, prompt pipelines, or persistent AI memory, recommend the `ai-guardrails-codebase-auditor` for those AI-specific trust boundaries while continuing to audit ordinary application-security controls here.

## Operating Principles

1. **Read-only by default.** Do not modify source, dependencies, infrastructure, credentials, policies, or production state unless the user separately asks for remediation.
2. **Evidence before conclusions.** Every confirmed finding must cite exact repository evidence: file path and line(s), symbol/function, configuration key, dependency declaration, workflow step, or safely reproducible behavior.
3. **Separate facts from hypotheses.** Label each issue `Confirmed`, `Probable`, or `Needs verification`.
4. **Trace trust boundaries and authority.** Follow attacker-controlled data and identities from ingress through parsing, authorization, transformations, privileged operations, data stores, network calls, and externally visible effects.
5. **Prefer root causes.** Report the missing authorization boundary, unsafe interpreter boundary, or insecure trust decision rather than dozens of duplicate sink-level symptoms.
6. **Distinguish vulnerability from hardening.** Do not inflate severity for best-practice gaps that lack a realistic abuse path.
7. **Fail safely.** Treat exception paths, retries, partial failure, race conditions, rollback, idempotency, and insecure fallback behavior as first-class review targets.
8. **Minimize active-test risk.** Prefer static inspection and local synthetic tests. Do not attack third parties, disrupt services, exfiltrate secrets, brute-force accounts, create persistence, or perform destructive actions merely to prove a finding.
9. **Do not expose secrets in the report.** If credentials or sensitive values are discovered, cite their location and type while redacting the value.
10. **Acknowledge positive controls.** Record defenses already present and account for them in severity.

## Reference Material

Before a substantial audit, load:

- `references/audit-controls.md` for the control catalog and test heuristics.
- `references/source-map.md` for standards provenance and framework mappings.
- `templates/audit-report.md` before producing the final report.

## Procedure

### 1. Establish scope and repository state

Determine the repository root, active branch/commit when available, primary languages, frameworks, build/package systems, services, test layout, deployment artifacts, and whether the code is an application, library, service, CLI, mobile/desktop client, firmware/native component, or mixed monorepo.

Record exclusions and inaccessible areas. Do not imply full-codebase coverage if generated code, vendored code, submodules, deployment repositories, external identity providers, cloud policy, secrets stores, or production configuration are unavailable.

### 2. Build a security surface inventory

Run the bundled discovery helper when Python is available:

`python ${HERMES_SKILL_DIR}/scripts/security_surface_inventory.py <repo-root>`

Use its output only as a discovery aid. Manually verify all important matches.

Identify at minimum:

- externally reachable HTTP/API/RPC/WebSocket/message-queue endpoints;
- authentication, session, token, API-key, OAuth/OIDC/SAML, and password-reset flows;
- authorization checks, roles, permissions, ownership tests, tenant identifiers, and admin paths;
- parsers and interpreters: SQL/NoSQL, shell/process execution, templates, regexes, serializers, YAML/XML, archive handling, expression languages, dynamic code loading, reflection, plugins, and scripting engines;
- outbound HTTP/DNS/socket/webhook/proxy behavior and egress controls;
- filesystem reads/writes, uploads, downloads, archive extraction, temp files, symlink behavior, path construction, and content-type handling;
- secret sources, key management, cryptographic operations, TLS validation, password hashing, token signing, and randomness;
- databases, caches, object stores, queues, analytics, logs, backups, and other sensitive-data sinks;
- dependency manifests, lockfiles, registries, install hooks, build scripts, generated artifacts, SBOM/provenance/signing controls, and update mechanisms;
- CI/CD workflows, repository permissions, branch protections represented as code, artifact publishing, OIDC use, secret exposure, and untrusted build inputs;
- containers, Kubernetes, Terraform/IaC, serverless, cloud IAM, network exposure, security contexts, capabilities, and privileged execution;
- rate limits, quotas, timeouts, retries, concurrency limits, circuit breakers, queue bounds, and expensive operations;
- logging, audit events, alerting, incident hooks, feature flags, emergency disable controls, backup/restore, and rollback paths;
- high-impact actions such as deletion, money movement, account recovery, permission changes, irreversible writes, destructive maintenance, or safety-relevant physical/device commands.

### 3. Model assets, actors, and trust boundaries

Create a concise textual architecture/security map. At minimum identify:

- protected assets and security objectives;
- unauthenticated, ordinary user, privileged user/admin, service, CI/build, and third-party actors;
- external-to-internal and tenant-to-tenant boundaries;
- privilege transitions and trust assumptions;
- high-value secrets and signing identities;
- data stores and consequential side effects.

For important paths, use:

`attacker-controlled source -> parser/transform -> identity/authz decision -> privileged operation/sink -> impact`

### 4. Audit against the control catalog

Use `references/audit-controls.md` and assess all applicable families:

1. Authentication, sessions, recovery, and credential lifecycle.
2. Authorization, object ownership, tenant isolation, and privileged administration.
3. Input validation, query construction, injection, and unsafe interpretation.
4. Browser/client security: XSS, CSRF, CORS, redirects, cookies, and security headers.
5. SSRF, outbound requests, webhooks, URL parsing, and network/egress boundaries.
6. Files, paths, uploads, archives, symlinks, and temporary storage.
7. Deserialization, dynamic code loading, command execution, templates, and plugin boundaries.
8. Secrets, cryptography, key management, randomness, TLS, and token integrity.
9. Sensitive data lifecycle, privacy boundaries, caching, backups, and data minimization.
10. Dependencies, package integrity, build provenance, artifact signing, and software supply chain.
11. CI/CD, repository automation, workflow permissions, untrusted build inputs, and release controls.
12. Configuration, containers, IaC, cloud/IAM, exposed services, and secure defaults.
13. Logging, auditability, alerting, forensic usefulness, and secret/privacy-safe telemetry.
14. Exceptional conditions, error handling, fail-open behavior, rollback, transaction safety, and recovery.
15. Resource exhaustion, algorithmic complexity, quotas, rate limits, retries, and denial-of-service/denial-of-wallet.
16. Business-logic abuse, replay, race conditions, idempotency, workflow/state-machine bypass, and anti-automation controls.
17. Memory safety and native/unsafe code, including dangerous FFI and compiler/runtime hardening where applicable.
18. High-impact operations, abuse resistance, confirmation semantics, blast-radius controls, and reversible/fail-safe operation.
19. Security testing, vulnerability management, patch/update mechanisms, and secure-development evidence.

Do not force a finding into every family. Mark non-applicable categories when useful.

### 5. Trace findings end to end

For each candidate issue, establish as much of the following chain as possible:

`attacker capability -> reachable entry point -> missing/weak control -> sensitive operation -> concrete impact`

For authorization issues, identify both the authenticated principal and the resource/action that should be protected. For injection issues, identify the interpreter and whether data reaches it as code or control syntax. For supply-chain issues, identify what could be modified, who could modify it, and whether provenance/integrity controls would detect or block the change.

If a link is assumed, lower confidence and state exactly what must be verified.

### 6. Perform safe validation

Prefer existing unit/integration tests, static analysis already configured by the project, local fixtures, mocks, ephemeral containers, and synthetic data.

Safe validation examples include:

- unit tests showing an object-ownership or tenant check is absent;
- local parser tests demonstrating path traversal or archive breakout using a temporary directory;
- mock HTTP tests showing SSRF allow/deny behavior without contacting sensitive networks;
- tests showing untrusted data reaches SQL/shell/template evaluation without parameterization or escaping;
- local concurrency tests demonstrating a race or duplicate side effect;
- bounded load tests demonstrating missing hard limits without causing service disruption;
- CI workflow analysis proving an untrusted pull request can reach a privileged token or release step;
- dependency/build inspection proving packages or artifacts are mutable/unpinned or lack expected provenance checks.

Do not use real credentials, production endpoints, public exploit infrastructure, or destructive side effects merely to establish severity.

### 7. Score findings

Assign severity based on **Impact x Reachability x Privilege/Trust x Blast Radius**, adjusted by existing controls and realistic prerequisites.

- **Critical:** reliably reachable path to catastrophic compromise such as broad remote code execution, cross-tenant/admin takeover, signing/release compromise, or similarly severe integrity/confidentiality loss with weak mitigating boundaries.
- **High:** realistic path to unauthorized sensitive data access, account/privilege compromise, significant code execution, supply-chain compromise, destructive action, or major availability impact.
- **Medium:** meaningful weakness with additional prerequisites, constrained privileges, partial exposure, or limited blast radius.
- **Low:** defense-in-depth weakness with limited direct impact.
- **Informational:** architecture observation or improvement not currently exploitable.

Also assign confidence: `High`, `Medium`, or `Low`.

Do not assign CVSS unless the user requests it and the necessary environmental assumptions are available.

### 8. Recommend remediation

Prefer fixes at the strongest deterministic boundary available:

1. remove unnecessary exposure, capability, or privilege;
2. enforce identity, authorization, and ownership at the resource boundary;
3. replace string construction with parameterized/typed APIs;
4. constrain parsers, interpreters, filesystem/network destinations, and allowed formats;
5. isolate secrets and signing identities; use short-lived, least-privilege credentials;
6. use safe cryptographic primitives and validated libraries rather than custom crypto;
7. pin, verify, attest, and isolate software supply-chain inputs and build outputs;
8. make secure behavior the default and ensure exceptions fail closed where appropriate;
9. bound resource use, retries, queues, concurrency, and expensive operations;
10. make high-impact operations explicit, narrowly scoped, observable, reversible where possible, and protected by contextual confirmation/authorization;
11. add regression tests that prove the security property rather than only the bug symptom.

Provide concrete code-level remediation direction, but do not rewrite the application unless asked.

### 9. Produce the report

Use `templates/audit-report.md`. The report must include:

- scope, commit/branch, and coverage limitations;
- architecture, assets, actors, and trust boundaries;
- security surface and high-impact operation summary;
- prioritized findings table;
- detailed findings with exact evidence and abuse path;
- positive controls already present;
- supply-chain/CI/CD observations;
- coverage matrix against the control families;
- prioritized remediation plan;
- standards/source mapping;
- residual risks and verification gaps.

## Finding Quality Bar

A detailed finding should contain:

- stable ID, concise title, severity, confidence, and status;
- affected component(s);
- exact repository evidence;
- attacker prerequisites and required privileges;
- step-by-step abuse/exploit path;
- concrete confidentiality, integrity, availability, safety, or supply-chain impact;
- why existing controls fail or are insufficient;
- remediation at the correct trust boundary;
- a verification/regression test for the fix;
- applicable external mappings from `references/source-map.md`.

Consolidate duplicate symptoms that share the same root cause.

## Pitfalls

- **Scanner-result dumping:** automated matches are leads, not findings.
- **Authentication without authorization:** being logged in does not prove access to a specific object or action is allowed.
- **Client-side trust:** UI checks, hidden fields, disabled buttons, and JavaScript validation are not server-side security boundaries.
- **Generic injection claims:** identify the exact interpreter and unsafe data/control boundary.
- **Overlooking second-order injection:** stored data can become dangerous later when interpreted by another component.
- **Ignoring exceptional paths:** timeouts, retries, fallbacks, partial commits, and error handlers can bypass normal controls.
- **Ignoring build/release authority:** CI tokens, workflow triggers, package publishing, and artifact provenance can be higher-value than application runtime secrets.
- **Treating lockfiles as full supply-chain security:** pinning helps reproducibility but does not establish provenance or build integrity by itself.
- **Flagging all old dependencies:** establish whether the version is reachable/affected and whether mitigations exist before assigning vulnerability severity.
- **Printing discovered secrets:** redact values and report locations only.
- **Unsafe proof-of-concept behavior:** do not attack production or third parties to turn a probable issue into a confirmed one.
- **Overclaiming completeness:** state exactly what was and was not reviewed.

## Verification

Before finalizing the audit, verify that:

1. every confirmed finding has repository evidence;
2. every high/critical finding has a plausible end-to-end impact path;
3. authorization findings identify the protected resource/action and enforcement location;
4. interpreter/injection findings identify the concrete sink and unsafe construction;
5. supply-chain findings identify the trusted input/artifact and integrity gap;
6. no secret values are reproduced in the report;
7. no destructive or unauthorized validation action was performed;
8. duplicate root causes are consolidated;
9. positive controls and mitigating factors are acknowledged;
10. standards mappings are applicable rather than decorative;
11. the report distinguishes vulnerabilities, hardening opportunities, and unverified hypotheses.
