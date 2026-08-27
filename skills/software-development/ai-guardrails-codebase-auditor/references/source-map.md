# Standards and Source Map

Accessed/assembled: 2026-08-25.

This file explains how external guidance shaped the skill. The mappings are design provenance, not a claim of formal certification or full conformance.

## Primary sources

### Hermes Agent skill system

- Hermes Agent, **Creating Skills**: https://hermes-agent.nousresearch.com/docs/developer-guide/creating-skills
- Hermes Agent, **Skills System**: https://hermes-agent.nousresearch.com/docs/user-guide/features/skills/
- Hermes Agent, **Working with Skills**: https://hermes-agent.nousresearch.com/docs/guides/work-with-skills
- Hermes Agent, **Built-in Tools Reference**: https://hermes-agent.nousresearch.com/docs/reference/tools-reference/

**Incorporated as:** the package uses a required `SKILL.md`, YAML frontmatter, `references/`, `templates/`, and `scripts/`; it relies on Hermes' terminal toolset; and bundled paths use `${HERMES_SKILL_DIR}` as documented.

### OWASP GenAI LLM Top 10 2026

- OWASP GenAI Security Project, **OWASP GenAI LLM Top 10 2026** (published 2026-08-03): https://genai.owasp.org/resource/owasp-genai-llm-top-10-2026/
- OWASP Top 10 for LLM and GenAI initiative: https://genai.owasp.org/initiatives/top-10-for-llm-and-genai/

**Incorporated as:** AG-01 prompt injection; AG-02 sensitive information disclosure; AG-05 improper output handling; AG-06 RAG/vector/embedding weaknesses; AG-08 data/model/supply-chain integrity; AG-10 misinformation/confabulation; AG-11 unbounded consumption. The skill intentionally maps findings to concrete code paths rather than mechanically producing one finding per OWASP category.

### OWASP Top 10 for Agentic Applications 2026

- OWASP GenAI Security Project, **OWASP Top 10 for Agentic Applications for 2026**: https://genai.owasp.org/resource/owasp-top-10-for-agentic-applications-for-2026/
- OWASP, **Securing Agentic Applications Guide 1.0**: https://genai.owasp.org/resource/securing-agentic-applications-guide-1-0/
- OWASP, **Agentic AI Threats and Mitigations**: https://genai.owasp.org/resource/agentic-ai-threats-and-mitigations/

**Incorporated as:** explicit agent/tool inventory; end-to-end action-path tracing; least privilege and excessive-agency checks; tool metadata/MCP trust analysis; persistent memory checks; multi-agent/delegation boundaries; human approval semantics; kill switches and operational controls.

### OWASP AI Testing Guide v1

- OWASP Foundation, **OWASP AI Testing Guide** (v1 announced 2025-11-26): https://owasp.org/www-project-ai-testing-guide/

**Incorporated as:** AG-14's repeatable trustworthiness/security testing approach, layer-aware testing, and the requirement to convert guardrail discoveries into regression tests rather than relying only on static review.

### NIST AI RMF and Generative AI Profile

- NIST, **Artificial Intelligence Risk Management Framework: Generative Artificial Intelligence Profile (NIST AI 600-1)**: https://www.nist.gov/publications/artificial-intelligence-risk-management-framework-generative-artificial-intelligence
- NIST, **AI RMF Playbook**: https://www.nist.gov/itl/ai-risk-management-framework/nist-ai-rmf-playbook

**Incorporated as:** the audit's lifecycle orientation; explicit scoping and risk context; separation of mapping/measurement from mitigation; documentation of residual risk and uncertainty; governance/monitoring/incident considerations; and a requirement to state coverage limitations rather than present a scan as proof of safety.

## Secondary / supporting sources

### OWASP GenAI data security and red-team resources

- **OWASP GenAI Data Security Risks & Mitigations 2026**: https://genai.owasp.org/resource/owasp-genai-data-security-risks-mitigations-2026/
- **AI Security Solutions Landscape for AI and Agentic Red Teaming Q2 2026**: https://genai.owasp.org/resource/ai-security-solutions-landscape-for-ai-and-agentic-red-teaming-q2-2026/

**Incorporated as:** stronger treatment of AI data lifecycle risks, poisoning/provenance, continuous testing, and red/purple-team-style verification of real guardrail boundaries.

## Control-to-source crosswalk

| Control | Primary provenance | How it appears in the audit |
|---|---|---|
| AG-01 Prompt Injection | OWASP LLM Top 10; OWASP Agentic guidance | Trace untrusted content into prompts/context, tools, state, and side effects |
| AG-02 Sensitive Disclosure | OWASP LLM Top 10; OWASP data security | Data minimization, secret handling, provider/log exposure, prompt confidentiality assumptions |
| AG-03 Excessive Agency | OWASP Agentic; OWASP LLM Top 10 lineage | Capability inventory, least privilege, deterministic constraints, approval gates |
| AG-04 Tool/MCP Integrity | OWASP Agentic guidance | Tool metadata trust, server allowlisting, confused-deputy and authorization analysis |
| AG-05 Output Handling | OWASP LLM Top 10 | Follow model output into interpreters/sinks and require sink-specific validation |
| AG-06 RAG/Vector | OWASP LLM Top 10; OWASP data security | Retrieval authorization, tenant filters, poisoning/provenance, instruction/data separation |
| AG-07 Memory | OWASP Agentic guidance | Persistence, poisoning, cross-session/tenant state, reset/rollback |
| AG-08 Supply Chain | OWASP LLM Top 10; Agentic guidance | Models/adapters/prompts/tools/skills provenance, pinning and trust controls |
| AG-09 Auth/Tenant | OWASP Agentic guidance; secure-design principle | Enforce identity/authorization outside the model and at resource boundaries |
| AG-10 Misinformation | OWASP LLM Top 10; NIST GenAI Profile | Consequence-based grounding, verification, abstention, human review |
| AG-11 Consumption | OWASP LLM Top 10 | Hard budgets for tokens, loops, retries, tools, retrieval and concurrency |
| AG-12 Monitoring/Incident | NIST AI RMF/Playbook; OWASP Agentic | Traceability, privacy-aware logging, anomaly signals, disable/revoke/rollback |
| AG-13 Human Oversight | OWASP Agentic; NIST AI RMF | Approval bound to exact consequential actions and changed arguments |
| AG-14 Testing | OWASP AI Testing Guide; NIST Measure | Repeatable adversarial/regression tests around deterministic and probabilistic controls |

## Interpretation rules

1. These sources inform audit questions; they do not replace code evidence.
2. A repository can be secure without implementing every suggested control if the associated risk is absent or otherwise mitigated.
3. A mapping does not mean OWASP or NIST endorses this skill.
4. NIST AI RMF materials are voluntary risk-management guidance, not a pass/fail certification checklist.
5. The skill should use the newest applicable standard available during an audit when the user asks for current-framework mapping, while clearly identifying version/date differences.
