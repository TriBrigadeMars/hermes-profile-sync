---
name: ai-guardrails-codebase-auditor
description: Audit AI codebases for guardrail and agentic security risks.
version: 1.0.0
author: Custom
license: MIT
platforms: [ macos, linux, windows ]
metadata:
  hermes:
    tags: [ ai-security, guardrails, llm, agents, prompt-injection, audit ]
    category: software-development
    requires_toolsets: [ terminal ]
---
# AI Guardrails Codebase Auditor

## When to Use

Use this skill when the user asks to audit, review, assess, threat-model, or harden a codebase that includes LLMs, generative AI, RAG, agents, MCP/tool use, model gateways, prompt pipelines, memory, retrieval, or AI-mediated actions.

Use it for AI-specific guardrail and trust-boundary analysis. Do not substitute it for a conventional application-security audit; recommend a separate security audit when ordinary auth, network, dependency, cryptographic, or infrastructure vulnerabilities require full treatment.

## Operating Principles

1. **Read-only by default.** Do not modify application code, configuration, prompts, policies, dependencies, or infrastructure unless the user separately asks for remediation.
2. **Evidence before conclusions.** Every confirmed finding must cite exact repository evidence: file path and line(s), symbol/function, configuration key, or reproducible behavior.
3. **Separate fact from inference.** Label each issue `Confirmed`, `Probable`, or `Needs verification`.
4. **Trace data and authority, not keywords alone.** Follow untrusted content from ingress through model context, retrieval, memory, tool selection, tool arguments, output handling, and side effects.
5. **Treat the model as an untrusted decision component.** Prompts are behavioral guidance, not authorization boundaries. Sensitive secrets must not rely on prompt confidentiality.
6. **Prioritize exploit chains.** A weak prompt is more serious when it can reach privileged tools, secrets, mutable memory, or irreversible actions.
7. **Avoid generic warnings.** Do not report "LLMs can hallucinate" unless the codebase creates a concrete impact path and the report identifies it.
8. **Minimize active testing risk.** Do not invoke destructive tools, send real messages, mutate production data, make purchases, change permissions, exfiltrate secrets, or attack third parties. Prefer static inspection and non-destructive local tests.

## Reference Material

Before a substantial audit, load:

- `references/audit-controls.md` for the control catalog and test heuristics.
- `references/source-map.md` when explaining standards provenance or mapping a finding to external guidance.
- `templates/audit-report.md` before producing the final report.

## Procedure

### 1. Establish scope and repository state

Determine the repository root, active branch/commit when available, primary languages, frameworks, test layout, and whether the code appears to be application code, library code, agent infrastructure, or a mixed monorepo.

Record important exclusions or inaccessible areas. Do not imply full-codebase coverage if large directories, generated code, external services, or deployment configuration are unavailable.

### 2. Build an AI surface inventory

Run the bundled inventory helper when Python is available:

`python ${HERMES_SKILL_DIR}/scripts/ai_surface_inventory.py <repo-root>`

Use its output only as a discovery aid. Manually verify important matches.

Identify at minimum:

- model/provider clients and gateways;
- system/developer prompt construction and prompt templates;
- user-controlled and third-party content entering model context;
- RAG loaders, vector stores, embedding pipelines, document parsers, web/browser/email/file ingestion;
- agent loops, planners, routers, subagents, multi-agent messaging, retries, reflection, and delegation;
- tool/function/MCP definitions, descriptions, argument schemas, allowlists, and execution adapters;
- credentials, environment variables, tokens, tenant/user identity, and authorization context exposed to AI components;
- persistent memory, conversation state, caches, scratchpads, checkpoints, and shared stores;
- model output sinks: shell/SQL/code execution, HTML/Markdown rendering, API calls, messages, filesystem writes, database mutations, payments, IAM changes, or other consequential actions;
- moderation, policy engines, classifiers, output schemas, validators, approval gates, rate/cost limits, logging, and incident controls.

### 3. Draw trust boundaries and action paths

Create a concise textual data-flow map:

`source -> transformation/retrieval -> model context -> model decision/output -> validator/policy -> tool/action -> external effect`

Mark each boundary as trusted, partially trusted, or untrusted. Explicitly distinguish **data** from **instructions** wherever external content can enter prompts or agent state.

For each consequential capability, answer:

- Who is the real authenticated principal?
- What can the model choose?
- What does deterministic code validate?
- What permissions does the invoked tool actually possess?
- Is user intent reconfirmed before high-impact actions?
- Can content from one tenant/session/user influence another?

### 4. Audit against the control catalog

Use `references/audit-controls.md` and test all applicable families:

1. Prompt injection and instruction/data separation.
2. Sensitive information disclosure and prompt-secret assumptions.
3. Tool use, excessive agency, least privilege, and approval gates.
4. Tool/MCP metadata poisoning, tool selection integrity, and confused-deputy risks.
5. Improper model-output handling and downstream injection.
6. RAG, vector, embedding, retrieval authorization, and provenance weaknesses.
7. Memory poisoning, cross-session contamination, and unsafe persistence.
8. Data/model/supply-chain poisoning and untrusted AI artifacts.
9. Identity, tenant boundaries, authorization propagation, and policy enforcement outside the model.
10. Misinformation/confabulation impact controls for consequential decisions.
11. Unbounded consumption, loops, retries, token/tool budgets, and denial-of-wallet paths.
12. Logging, privacy, auditability, security monitoring, rollback, kill switches, and incident response hooks.
13. Human oversight and confirmation for irreversible or high-impact actions.
14. Evaluation/red-team coverage and regression tests for guardrails.

Do not force a finding into every category. Mark non-applicable areas explicitly when useful.

### 5. Trace candidate findings to impact

For every candidate issue, establish as much of this chain as possible:

`attacker-controlled input -> AI interpretation/state change -> missing/weak control -> privileged capability or unsafe sink -> realistic impact`

A finding is stronger when the chain is visible in code. If one link is assumed, lower confidence and identify the exact verification needed.

### 6. Perform safe validation

Prefer existing unit/integration tests and local fixtures. When active validation is appropriate, use synthetic data and local/non-production targets.

Safe examples include:

- tests proving retrieved documents can override instructions;
- unit tests showing tool arguments lack deterministic validation;
- mock-tool tests showing an approval gate can be bypassed;
- local test data showing retrieval crosses tenant boundaries;
- output-handling tests demonstrating generated HTML/SQL/shell fragments reach unsafe sinks;
- bounded loop tests proving missing iteration/token/tool-call caps.

Do not use real credentials or cause external side effects merely to demonstrate a finding.

### 7. Score findings

Assign severity based on **Impact x Reachability x Privilege**, adjusted by existing controls.

- **Critical:** reliably reachable path to severe cross-tenant compromise, high-value secret exposure, arbitrary privileged action/code execution, or similarly catastrophic impact with weak/no human boundary.
- **High:** realistic path to consequential unauthorized action, sensitive disclosure, durable poisoning, or material integrity failure.
- **Medium:** meaningful weakness requiring additional preconditions, limited privilege, or constrained impact.
- **Low:** defense-in-depth gap with limited direct impact.
- **Informational:** architecture observation or improvement that is not currently exploitable.

Also assign confidence: `High`, `Medium`, or `Low`.

### 8. Recommend remediation

For each finding, recommend controls at the strongest deterministic boundary available. Prefer, in order:

1. remove unnecessary capability/privilege;
2. enforce authorization and policy in non-LLM code;
3. constrain tool schemas/parameters and destinations;
4. isolate untrusted data from instruction channels;
5. require contextual human approval for high-impact actions;
6. validate/sanitize model output before downstream interpretation;
7. add provenance, tenant filters, memory hygiene, budgets, monitoring, and regression tests;
8. use prompting as defense-in-depth, never as the sole security boundary.

Provide a concrete code-level remediation direction, but do not rewrite the application unless asked.

### 9. Produce the report

Use `templates/audit-report.md`. The report must include:

- scope and coverage limitations;
- architecture/AI surface summary;
- trust-boundary and capability summary;
- prioritized findings table;
- detailed findings with evidence and attack path;
- positive controls already present;
- coverage matrix against the audit-control families;
- prioritized remediation plan;
- standards/source mapping;
- residual risks and verification gaps.

## Finding Quality Bar

A detailed finding should contain:

- stable ID, concise title, severity, confidence, and status;
- affected component(s);
- exact evidence;
- attacker prerequisites;
- step-by-step exploit/abuse path;
- concrete impact;
- why current controls fail or are insufficient;
- remediation at the correct trust boundary;
- verification test for the fix;
- applicable external mappings from `references/source-map.md`.

Avoid duplicate findings that share the same root cause. Prefer one root-cause finding with multiple affected paths.

## Pitfalls

- **Keyword-only auditing:** AI libraries may be wrapped behind internal abstractions. Trace call graphs and configuration.
- **Prompt-centric security:** do not recommend "strengthen the system prompt" as the primary fix for authorization or secret protection.
- **Treating all prompt injection as equal:** severity depends on reachable authority and downstream sinks.
- **Assuming tool descriptions are trusted:** tool/MCP metadata can itself become an instruction channel.
- **Ignoring indirect input:** web pages, emails, files, retrieved documents, database text, issue comments, and tool results can all carry adversarial instructions.
- **Ignoring persistence:** memory and vector stores can turn one malicious input into a durable attack.
- **Reporting theoretical model behavior without code impact:** tie model uncertainty to an actual consequential decision path.
- **Overclaiming completeness:** state what was not tested.

## Verification

Before finalizing the audit, verify that:

1. every confirmed finding has repository evidence;
2. every high/critical finding has a plausible end-to-end impact path;
3. authorization recommendations are enforced outside the LLM;
4. no destructive or unauthorized test action was performed;
5. duplicate root causes are consolidated;
6. positive controls are acknowledged;
7. source mappings are applicable rather than decorative;
8. the final report distinguishes observed facts, inferred risks, and untested hypotheses.
