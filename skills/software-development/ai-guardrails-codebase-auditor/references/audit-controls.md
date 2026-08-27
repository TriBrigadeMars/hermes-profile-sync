# AI Guardrails Audit Control Catalog

This catalog converts external AI security/safety guidance into code-review questions. It is deliberately implementation-focused: use the source map for provenance, but treat repository evidence as the basis for findings.

## AG-01 Prompt Injection & Instruction/Data Separation

Look for direct and indirect untrusted content inserted into system/developer prompts, agent scratchpads, retrieved context, tool results, multimodal context, or conversation history.

Check whether external text is clearly treated as data rather than trusted instructions; whether higher-trust policy is deterministically enforced; whether remote content can influence tool selection or privileged arguments; and whether prompt injection can cross user/tenant boundaries.

Red flags: string concatenation of trusted instructions and untrusted content; "ignore instructions in documents" as the only defense; autonomous browsing/email/file agents with privileged tools; untrusted content copied into persistent memory.

## AG-02 Sensitive Information Disclosure

Trace secrets, credentials, private prompts, PII, tenant data, proprietary documents, hidden chain/context, and backend responses into model context and outputs.

Check minimization, redaction, tenant scoping, provider data policies/configuration, log hygiene, and whether the application mistakenly assumes system prompts are confidential.

Red flags: API secrets in prompts; authorization rules encoded only in hidden prompts; full database records sent to models when a small projection would suffice.

## AG-03 Excessive Agency & Least Privilege

Inventory every model-selectable tool/action and the credentials behind it. Determine whether the tool has more permission, scope, destinations, or parameters than required.

Check contextual human approval for irreversible/high-impact actions and whether approvals bind to the exact proposed action/arguments rather than a vague task.

Red flags: generic shell/HTTP/SQL tools; wildcard destinations; admin/service credentials; model-generated recipient/account/path/command accepted without policy validation.

## AG-04 Tool/MCP Integrity & Confused Deputy

Treat tool names, descriptions, schemas, server instructions, tool results, and dynamically discovered capabilities as untrusted or semi-trusted inputs unless provenance is strong.

Check server allowlists, pinned identities/versions, capability scoping, authorization at the resource server, schema validation, destination restrictions, and resistance to malicious tool metadata that attempts to redirect the agent.

Red flags: auto-trusting newly discovered MCP servers/tools; auth decisions based on model interpretation; privileged client credentials usable across users without downstream authorization.

## AG-05 Improper Output Handling

Trace model output into interpreters and sinks: shell, SQL, templates, HTML/Markdown, JavaScript, code execution, deserialization, filesystem paths, URLs, API parameters, email headers, or policy expressions.

Require typed schemas where practical and deterministic validation/escaping appropriate to the sink.

Red flags: `eval`, `exec`, shell interpolation, raw model SQL against write-capable DBs, rendered model HTML with unsafe features, model-created URLs fetched without SSRF restrictions.

## AG-06 RAG / Vector / Embedding Controls

Inspect ingestion provenance, document authorization, chunk metadata, tenant filters, retrieval filters, update/delete propagation, poisoning controls, and whether retrieved text is allowed to act as instruction.

Red flags: global vector namespace for multi-tenant data; client-supplied metadata filters trusted without server enforcement; web/file ingestion with no provenance; retrieved secrets unnecessarily placed in context.

## AG-07 Memory & Persistent State Safety

Identify long-term memory, summaries, user profiles, vector memories, checkpoints, shared scratchpads, and agent-to-agent state.

Check who may write/read/delete memory, whether untrusted instructions can persist, tenant/session isolation, provenance, TTL/retention, user review, and safe reset/rollback.

Red flags: model autonomously deciding durable memory; shared memory across principals; retrieved/tool text persisted verbatim as trusted facts/instructions.

## AG-08 Data, Model & AI Supply-Chain Integrity

Inspect model sources, adapters, checkpoints, prompt packages, datasets, embedding models, remote code, plugins/skills/tools, and model-serving dependencies.

Check provenance, pinning, hashes/signatures where available, review gates, sandboxing, trust labels, and update controls.

Red flags: loading untrusted model repositories with remote code enabled; silent model/prompt/tool updates; unreviewed external skill instructions granted terminal/network authority.

## AG-09 Identity, Authorization & Tenant Boundaries

Verify that application identity and authorization are enforced by deterministic application/resource-server code, not inferred by the model.

Check object-level authorization on retrieved records and tool targets; delegation/impersonation; user-vs-service credential separation; tenant propagation through queues, memory, RAG, and asynchronous tasks.

Red flags: "the model knows which tenant it is serving"; trusting model-selected record IDs; broad service account with no per-user policy check.

## AG-10 Misinformation / Confabulation Impact Controls

Apply only where incorrect model output can cause consequential decisions or actions.

Check grounding, provenance/citations, confidence handling, deterministic calculations, external verification for high-impact facts, safe abstention, and human review.

Red flags: model-generated medical/legal/financial/operational decisions executed automatically; invented identifiers used for transactions; unverified model assertions changing system state.

## AG-11 Unbounded Consumption & Agent Loops

Inspect token limits, request size, context growth, recursive calls, retries, parallel subagents, tool-call counts, retrieval fan-out, expensive modalities, and per-user/tenant budgets.

Check hard ceilings, timeout/cancellation, exponential retry behavior, idempotency, rate limits, cost observability, and attacker-controlled amplification.

Red flags: `while`/recursive agent loops with model-controlled termination only; unlimited retries; user input controlling huge retrieval/tool fan-out.

## AG-12 Logging, Monitoring, Privacy & Incident Controls

Check structured security logs for model/tool decisions and approvals without over-logging secrets or raw sensitive prompts.

Look for traceability from user request to model call to tool action; anomaly monitoring; guardrail failure signals; emergency disable/kill switch; credential revocation; rollback; safe audit retention.

Red flags: irreversible actions with no audit trail; full raw prompts containing secrets in general logs; inability to disable a compromised tool/model quickly.

## AG-13 Human Oversight & Approval Semantics

For consequential actions, inspect whether approval happens after the exact action is assembled and before execution.

Approval UI/API should communicate target, operation, important arguments, side effects, and ideally the originating user intent. Re-approval should be required if material arguments change.

Red flags: blanket "allow agent" approval; confirmation before model chooses final recipient/amount/command; approval token reusable for unrelated actions.

## AG-14 Guardrail Evaluations & Regression Testing

Look for repeatable tests covering direct/indirect prompt injection, policy bypass, tool misuse, data leakage, RAG isolation, memory poisoning, dangerous output sinks, and approval bypasses relevant to the architecture.

Prefer deterministic assertions around security boundaries plus model-behavior evaluations for probabilistic layers. Verify tests are run in CI or another repeatable gate where appropriate.

Red flags: only happy-path LLM tests; one-time red-team notebook with no regression suite; tests that judge prompt wording but never validate actual tool side effects or authorization.
