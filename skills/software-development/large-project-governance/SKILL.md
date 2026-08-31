---
name: large-project-governance
description: "Governance control-plane for multi-agent project builds."
version: 1.0.0
author: Mars Cruz + Hermes Agent
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [governance, orchestration, evaluation, control, multi-agent, verification]
    related_skills: [workflow-orchestrator, merge-reconciler, requesting-code-review]
    category: software-development
---

# Large-Project Evaluation & Governance Framework

## When to Use
Use for **substantial multi-agent work** — any task that spawns producer agents, has side-effecting steps (git, network, filesystem, dependency changes), or where an independent evaluator should judge the result before acceptance. This is the shared control plane for the `workflow-orchestrator` pipeline. Ignore for trivial single-step asks.

## Core Principle
> **No evidence → no PASS. No agent approves its own work.**
> The evaluator recommends; the orchestrator decides; authority policy controls whether an approved decision may be executed.

Lifecycle: `contract → produce → validate → evaluate → decide → refine → re-evaluate → authorize → execute → verify → accept → learn`

## The 8 Control Primitives (implemented in `scripts/governance.py`)
These are **deterministic helpers / schemas + workflow state**, not router skills.

| # | Primitive | What it does | Helper |
|---|-----------|--------------|--------|
| 1 | **EvaluationContract** | Declares what an independent evaluator must judge, rubric, evidence needs, PASS/REFINE/escalate conditions | `evaluation_contract_valid` |
| 2 | **TrajectoryContract** | Permitted/required process — tools, skills, ordering, budgets, side-effect constraints (catches right-answer-wrong-process) | `trajectory_contract_valid`, `trajectory_violations` |
| 3 | **ActionProposal** | Separates proposing a consequential action from executing it (action, args, rationale, impact, rollback) | `action_proposal_valid` |
| 4 | **AuthorityPolicy** | Decides if an approved proposal may run autonomously vs. needs human approval | `authority_requires_human` |
| 5 | **ActionReceipt** | Records what actually happened + postcondition verification; executed ≠ succeeded | `action_receipt_valid` |
| 6 | **ProgressGuard** | Detects loops / no-progress without another LLM call (repair count, identical tool calls) | `eval_progress_guard` |
| 7 | **ReviewRequest** | Durable human-review state for uncertainty / protected actions / repeated failure / evaluator-disagreement | `review_request_valid`, `build_disagreement_report` |
| 8 | **RegressionCase** | Turns meaningful failures into persistent future tests (originating task, fixture, expected behavior, missed component) | `regression_case_valid` |

## Governance Records (also in `scripts/governance.py`)
- **DecisionRecord** — orchestrator's disposition of evaluator recommendations; never silently ignore one.
- **AcceptanceRecord** — REQUIRED for final PASS; maps every requirement to evidence, gates, evaluation, execution log, hashes, citations. `acceptance_record_complete()`
- **ImprovementCandidate** — out-of-scope improvement, recorded for later; **never implemented in current task**.
- **EvaluationDisagreementRecord** — conflicting evaluator positions → human review.
- **UncertaintySignal** — contradictory requires, missing input, multiple interpretations, insufficient evidence, unresolved architecture.
- **CommandRiskAssessment** — evaluate shell/npx command batches before execution; large/damaging local activity surfaced to human even if agent believes it's safe.

## Default Governance Profile (override only with explicit project policy)
1. Operate autonomously unless a subagent shows material uncertainty or planned shell/npx activity could plausibly damage the computer.
2. If automated checks pass but independent evaluation finds mediocre/substandard work → send to refinement.
3. Evaluators provide evidence + recommendations; orchestrator makes the workflow decision.
4. If orchestrator rejects/departs from evaluator advice → record a DecisionRecord explaining why.
5. Original producer repairs its own work by default (context/cost).
6. **After two failed repair cycles → stop, escalate to human.**
7. **Human approval required before:** deleting files, changing dependencies, changing credentials.
8. Git commits/pushes/merges/releases/network calls may be autonomous after automated preconditions pass.
9. Spend extra tokens on independent evaluation for substantive work.
10. A PASS needs an execution log + requirement-by-requirement evidence; research also needs citations.
11. Out-of-scope improvements → flagged for later, not built in-task.
12. Meaningful failures → regression/evaluation cases.
13. Material evaluator disagreement → human with plain-language of both positions.
Priority order: **(1) prevent incorrect output → (2) prevent drift from original requirements → (3) prevent unsafe/unintended actions.** Hard authority gates remain mandatory regardless of ranking.

## Wiring with workflow-orchestrator
- `workflow-orchestrator` owns control flow. Its v2 contract system (`StageContract`, `ArtifactManifest`, `VerificationResult`, gates) provides the **deterministic validation** layer.
- This framework adds the **evaluation + authority + acceptance** layer on top: independent EvaluationContract on top of gates, AuthorityPolicy before side-effecting Execute, ActionReceipt after, and AcceptanceRecord to promote PASS.
- Run `scripts/governance.py --check` after writing governance artifacts to validate them.

## Usage Example
```python
import sys; sys.path.insert(0, "<this-skill-dir>/scripts>")
from governance import (
    evaluation_contract_valid, action_proposal_valid,
    authority_requires_human, eval_progress_guard,
    acceptance_record_complete, build_disagreement_report,
)

# authority gate before a side effect
proposal = {...}; if authority_requires_human(proposal): -> ReviewRequest else -> execute
```

## Verification
- [ ] installed under `software-development/large-project-governance`.
- [ ] `governance.py --check` passes its self-tests.
- [ ] `skill_view(name='large-project-governance')` returns `readness_status: available` with scripts + templates listed.