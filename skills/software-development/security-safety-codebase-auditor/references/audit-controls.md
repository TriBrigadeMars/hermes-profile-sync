# Security & Safety Audit Control Catalog

Use these controls as review questions, not as a mechanical compliance checklist. A control can be non-applicable, fully implemented, partially implemented, or absent. Findings require repository evidence and a realistic impact path.

## SS-01 Authentication, Sessions, Recovery, and Credential Lifecycle

**Objective:** ensure identities cannot be forged, sessions cannot be predictably stolen/replayed, and recovery paths do not become weaker alternate login mechanisms.

Inspect:
- password hashing and verification; password policy only where relevant to the application;
- session creation, rotation, expiry, revocation, logout, cookie attributes, token storage, and fixation resistance;
- API keys, bearer tokens, refresh tokens, OAuth/OIDC/SAML validation, issuer/audience/nonce/state/PKCE handling as applicable;
- MFA enrollment/recovery and privileged-step-up requirements;
- password reset, email/phone change, account linking, invitation, and magic-link flows;
- service-to-service identity and machine credential rotation.

Red flags:
- accepting unsigned/weakly validated tokens;
- long-lived bearer credentials without revocation or narrow scope;
- recovery links/tokens reusable after success;
- session IDs accepted from attacker-controlled URLs;
- security-sensitive identity changes without reauthentication;
- auth decisions based on client-supplied identity fields.

Safe tests:
- unit-test token claims and expiry behavior;
- verify session rotation after login/privilege change;
- replay synthetic recovery tokens in a local test environment.

## SS-02 Authorization, Ownership, Tenant Isolation, and Administration

**Objective:** every sensitive object/action is authorized server-side for the authenticated principal and tenant.

Inspect:
- route/middleware/service/data-layer permission enforcement;
- object ownership and tenant predicates in reads, writes, exports, searches, background jobs, and caches;
- role/permission evaluation and privilege escalation paths;
- admin/support impersonation, break-glass, and maintenance routes;
- batch endpoints and indirect references.

Red flags:
- authorization only in UI/client code;
- lookup-by-ID followed by no ownership/tenant check;
- tenant ID taken from request and trusted without binding to the principal;
- shared caches keyed without tenant/user context;
- privileged internal endpoint reachable through ordinary routing.

Safe tests:
- create two synthetic users/tenants and prove cross-object access is denied;
- unit-test every sensitive action with allow and deny cases.

## SS-03 Input Validation, Query Construction, Injection, and Unsafe Interpretation

**Objective:** untrusted input remains data, not executable syntax or interpreter control.

Inspect:
- SQL/NoSQL/query builders and raw query APIs;
- shell/process execution and argument construction;
- template engines and expression evaluators;
- LDAP/XPath/GraphQL filters where dynamically constructed;
- regex construction and catastrophic backtracking exposure;
- CSV/formula injection where exported data is opened by spreadsheet software;
- logging/terminal control-sequence injection where operationally relevant.

Red flags:
- string concatenation/interpolation into interpreters;
- dynamic evaluation of untrusted expressions;
- allowlists implemented after decoding/canonicalization in the wrong order;
- escaping used where parameterization/typed APIs exist.

Safe tests:
- use local synthetic payloads to prove parameter boundaries;
- test encoding/canonicalization edge cases without targeting external systems.

## SS-04 Browser and Client-Side Security

**Objective:** prevent script execution, forged state-changing requests, unsafe cross-origin access, redirect abuse, and client-side trust failures.

Inspect:
- context-appropriate output encoding and sanitization;
- CSP and dangerous bypasses where applicable;
- CSRF protections for cookie-authenticated state changes;
- CORS origin/method/header rules and credentialed requests;
- cookie `Secure`, `HttpOnly`, `SameSite`, scope, and lifetime;
- open redirects and URL validation;
- postMessage origin validation and DOM sinks;
- security headers appropriate to the application.

Red flags:
- raw HTML injection or unsafe DOM APIs with attacker data;
- wildcard/reflective CORS with credentials;
- state-changing GET requests;
- CSRF token not bound to session or not validated;
- redirects to arbitrary user-controlled URLs.

## SS-05 SSRF, Outbound Requests, Webhooks, and Egress

**Objective:** attacker-controlled destinations cannot reach internal, metadata, loopback, privileged, or otherwise prohibited networks/services.

Inspect:
- URL parsing, redirect following, DNS resolution, proxy behavior, scheme handling, and IP-range checks;
- webhook callbacks, import-from-URL, image/document fetchers, package/plugin downloaders, and URL previews;
- cloud metadata defenses and network egress policy;
- credentials automatically attached to outbound requests.

Red flags:
- blocklists without post-resolution validation;
- checking hostname before redirects but not after;
- allowing non-HTTP schemes unexpectedly;
- forwarding sensitive headers to user-selected destinations.

Safe tests:
- mock DNS/HTTP locally and test loopback/private/link-local denial;
- verify redirects are revalidated.

## SS-06 Files, Paths, Uploads, Archives, and Temporary Storage

**Objective:** untrusted file names/content cannot escape intended storage, overwrite sensitive files, execute unexpectedly, or consume unbounded resources.

Inspect:
- path joining/canonicalization and root containment;
- upload size/type validation and content sniffing;
- archive extraction (`zip`, `tar`) and traversal/symlink handling;
- temp-file creation and permissions;
- download/content-disposition behavior;
- file permissions and cleanup;
- image/document/media processors and decompression limits.

Red flags:
- user-supplied absolute paths;
- extraction without containment checks;
- predictable temp names;
- executing or serving uploads from privileged/origin-equivalent locations;
- trusting extensions alone.

Safe tests:
- extract synthetic traversal/symlink archives into a temporary sandbox;
- verify all resulting paths remain under the intended root.

## SS-07 Deserialization, Dynamic Code, Commands, Templates, and Plugins

**Objective:** untrusted data cannot instantiate dangerous objects, load code, alter execution logic, or cross a plugin boundary with excessive privilege.

Inspect:
- native/object deserialization formats and gadget-prone libraries;
- `eval`/dynamic execution/reflection;
- subprocess/shell APIs;
- server-side template compilation/evaluation;
- plugin/module loading paths and signatures;
- YAML/XML parser options and entity/constructor behavior.

Red flags:
- deserializing attacker-controlled opaque objects;
- shell=True or equivalent with untrusted input;
- loading modules/plugins from writable directories;
- unsafe YAML constructors or XML external entities enabled.

## SS-08 Secrets, Cryptography, Key Management, Randomness, TLS, and Token Integrity

**Objective:** secrets and cryptographic identities are protected with established primitives and lifecycle controls.

Inspect:
- hard-coded secrets, example credentials, generated files, CI logs, and debug output;
- password hashing, key derivation, encryption/authentication modes, signing, verification, and nonce/IV generation;
- TLS certificate/hostname validation and insecure overrides;
- key storage, rotation, scoping, separation of signing/encryption duties, and recovery;
- randomness sources for security tokens.

Red flags:
- custom cryptographic constructions;
- obsolete/insecure algorithms for security purposes;
- disabled certificate verification;
- predictable randomness;
- long-lived secrets shared broadly across environments.

Report secret locations without reproducing values.

## SS-09 Sensitive Data Lifecycle and Privacy Boundaries

**Objective:** sensitive data is collected, stored, transmitted, cached, logged, retained, exported, and deleted consistently with the application's security requirements.

Inspect:
- data classification implied by fields and schemas;
- encryption in transit/at rest where threat model requires it;
- logs, analytics, traces, crash reports, backups, caches, search indexes, and exports;
- retention/deletion flows and replicas;
- tenant/user separation in data stores and background processing;
- mass export and bulk-query protections.

Red flags:
- secrets/tokens/passwords in logs;
- sensitive responses cached publicly/shared;
- deletion that leaves retrievable secondary copies without documented intent;
- broad exports without authorization/audit controls.

## SS-10 Dependencies, Build Integrity, Provenance, and Software Supply Chain

**Objective:** source, dependencies, build inputs, and released artifacts have controlled provenance and integrity.

Inspect:
- manifests/lockfiles, package registries, dependency sources, install hooks, git dependencies, mutable tags/branches, and checksums;
- SBOM generation and vulnerability-management evidence;
- artifact signing/verification and provenance attestations;
- build isolation, reproducibility expectations, and release provenance;
- source-review/branch controls represented in repository configuration;
- vendored binaries, downloaded tools, containers/base images, and update channels.

Red flags:
- dependencies fetched from arbitrary mutable URLs without integrity checks;
- production artifacts built on developer workstations without provenance where stronger guarantees are needed;
- release signatures created by the same broadly exposed environment that consumes untrusted input;
- floating container tags for security-sensitive deployments;
- package publishing credentials broadly available to ordinary CI jobs.

Use SLSA concepts to reason about source/build provenance; do not claim a formal SLSA level unless the evidence supports every requirement.

## SS-11 CI/CD, Repository Automation, and Release Controls

**Objective:** untrusted contributors and build inputs cannot obtain privileged tokens, alter protected artifacts, or bypass review/release gates.

Inspect:
- workflow triggers and permissions;
- fork/pull-request behavior and checkout of attacker-controlled code;
- use of secrets/OIDC tokens in privileged jobs;
- pinned actions/plugins and reusable workflows;
- environment protection, reviewers, artifact promotion, and publish steps;
- cache poisoning and artifact substitution risks;
- generated release notes/scripts that execute content.

Red flags:
- privileged workflow executes pull-request code before trust boundary;
- write-all default permissions;
- mutable third-party workflow/action references;
- production deploy/publish from unreviewed branches;
- secret-bearing jobs consuming attacker-controlled artifacts/caches.

## SS-12 Configuration, Containers, IaC, Cloud/IAM, and Secure Defaults

**Objective:** deployed systems start secure, expose only necessary surfaces, and run with least privilege.

Inspect:
- debug/development flags and default credentials;
- network listeners and public exposure;
- cloud IAM roles/policies, service accounts, Kubernetes RBAC, security contexts, container capabilities, host mounts, privileged mode, and root execution;
- Terraform/IaC security groups, public buckets/databases, encryption, logging, and secret handling;
- environment separation and feature flags;
- default CORS/auth/security settings.

Red flags:
- `0.0.0.0` listeners for administrative services without compensating controls;
- wildcard IAM permissions;
- privileged containers or Docker socket mounts without necessity;
- debug endpoints enabled in production configurations;
- insecure defaults requiring each customer/operator to harden manually.

## SS-13 Logging, Auditability, Alerting, and Forensics

**Objective:** meaningful security events are observable without leaking sensitive data, and logs can support investigation.

Inspect:
- authentication/authorization failures, sensitive changes, admin actions, key events, security-setting changes, exports, releases, and destructive actions;
- actor identity, target, timestamp, outcome, correlation/request IDs, and source context;
- tamper resistance/centralization where appropriate;
- alerting hooks and incident response integration;
- log redaction and access controls.

Red flags:
- critical admin/security actions leave no audit trail;
- logs contain credentials/session tokens;
- user-controlled fields can forge log structure or terminal output;
- alerts depend only on application success logs and miss denied/failed attacks.

## SS-14 Exceptional Conditions, Fail-Safe Behavior, Rollback, and Recovery

**Objective:** failures do not silently disable security, corrupt state, duplicate side effects, or leave the system in an unsafe partially completed condition.

Inspect:
- error handlers, catch-all exceptions, default/fallback branches, timeout handling, circuit breakers, transaction boundaries, retries, compensation logic, and startup validation;
- authorization/policy service failure behavior;
- partial database/external-service writes;
- backup/restore and rollback tooling;
- feature flag and emergency disable paths.

Red flags:
- `except: allow` / policy timeout implies permit;
- transaction failure after one irreversible external side effect with blind retry;
- swallowed exceptions around signature/authentication verification;
- recovery mode bypasses normal authorization without strong controls.

OWASP Top 10:2025 explicitly elevates mishandling exceptional conditions as a major risk family; examine these paths rather than reviewing only happy-path code.

## SS-15 Resource Exhaustion, Quotas, Rate Limits, and Algorithmic Complexity

**Objective:** untrusted users cannot consume unbounded CPU, memory, storage, bandwidth, external-service cost, threads, file descriptors, or queue capacity.

Inspect:
- request/body/upload/decompression limits;
- per-user/tenant/IP/action rate limits where appropriate;
- pagination/batch/query complexity limits;
- regex/parser complexity;
- retry/timeout/concurrency/queue bounds;
- expensive cryptographic/media/data transformations;
- account creation, password reset, email/SMS/webhook and third-party billing amplification.

Red flags:
- unbounded loops over attacker-controlled collection sizes;
- unlimited fan-out or recursive fetch;
- no hard request/response size cap;
- retries multiply expensive downstream actions;
- rate limits only in the UI/client.

## SS-16 Business Logic, Replay, Race Conditions, State Machines, and Anti-Automation

**Objective:** the intended workflow and invariants hold under concurrency, retries, replay, reordered requests, and malicious sequencing.

Inspect:
- payments/credits/coupons/inventory/limits;
- account state transitions and recovery;
- idempotency keys and replay protection;
- TOCTOU races, optimistic/pessimistic locking, uniqueness constraints, and atomicity;
- multi-step authorization where state can change between check and use;
- abuse of bulk operations and automation.

Red flags:
- check-then-act without atomic enforcement;
- one-time token accepted multiple times concurrently;
- client controls authoritative state-machine transitions;
- side effects retried without idempotency.

## SS-17 Memory Safety and Native/Unsafe Code

**Objective:** memory-unsafe components receive risk-proportionate scrutiny and hardening.

Apply when C/C++/unsafe Rust/FFI/native extensions, embedded code, parsers, drivers, or high-privilege native components are present.

Inspect:
- bounds, lifetime, ownership, integer conversions/overflows, format strings, and unsafe blocks;
- FFI assumptions and validation at language boundaries;
- compiler/runtime hardening flags, sanitizers, fuzzing, and tests;
- network-facing and cryptographic native code priority.

Red flags:
- parsing attacker-controlled binary data in high-privilege memory-unsafe code without fuzzing/sanitizer evidence;
- disabling language/runtime safety without documented need;
- unsafe FFI trusting lengths/pointers from external data.

CISA's Secure by Design guidance encourages memory-safe languages for new code and prioritized migration/hardening of exposed or sensitive components. Treat migration as risk reduction, not an automatic vulnerability finding.

## SS-18 High-Impact Operations, Abuse Resistance, and Reversible Safety

**Objective:** destructive or consequential capabilities are narrowly authorized, hard to trigger accidentally, observable, bounded, and reversible where practical.

Inspect:
- delete/purge/reset/revoke/rotate/publish/deploy/transfer/refund/permission-change actions;
- bulk and recursive operations;
- dry-run/preview support;
- exact-target confirmations and step-up authorization;
- blast-radius limits and per-operation scopes;
- rollback, backups, restore verification, and emergency stop controls.

Red flags:
- one broad credential can irreversibly affect all tenants/resources;
- confirmation UI is not bound to the final server-side action/parameters;
- safety interlocks exist only in clients/scripts;
- bulk destructive operations have no bounds or audit trail.

This family is broader than vulnerability prevention: it evaluates whether legitimate privileged operations can fail catastrophically or be abused beyond intended scope.

## SS-19 Security Testing, Vulnerability Management, Patching, and Secure Development

**Objective:** security properties are continuously checked and known defects can be fixed/distributed safely.

Inspect:
- unit/integration tests for authz, parsing, security invariants, and failure paths;
- SAST/secret/dependency/container/IaC scanning where appropriate;
- fuzzing/sanitizers for risky parsers/native code;
- vulnerability intake, advisory process, supported versions, patch/update mechanism, and rollback;
- branch/review protections represented as code/config where visible;
- root-cause regression tests after security fixes.

Red flags:
- no test cases for critical authorization boundaries;
- update mechanism accepts unsigned/unverified artifacts where integrity matters;
- known-vulnerable dependency remains reachable with no mitigation/plan;
- release process cannot quickly revoke/replace compromised artifacts.

Use NIST SSDF to frame lifecycle practices, but do not claim SSDF conformance from repository evidence alone.
