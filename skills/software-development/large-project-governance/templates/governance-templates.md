# Governance Templates

Copy these YAML templates into your workflow artifacts. Each corresponds to a
dataclass + validator in `scripts/governance.py`.

## 1. EvaluationContract

```yaml
evaluation_contract:
  task_id: TASK-001
  requirements: [REQ-01, REQ-02]
  dimensions: [correctness, requirements_fidelity, quality]
  deterministic_gates: [gate_0_manifest, gate_1a_docx_integrity]
  independent_evaluation_required: true
  evidence_required: true
  research_citations_required: false
```

## 2. TrajectoryContract

```yaml
trajectory_contract:
  task_id: TASK-001
  required_skills: [docx]
  permitted_skills: [docx, pdf, xlsx]
  required_tools: [write_file]
  forbidden_tools: [eval]
  permitted_paths: ["workspace/output/"]
  max_tool_calls: 30
  max_llm_calls: 12
  expected_stage_order: [plan, produce, validate, evaluate, decide]
  allowed_side_effects: []
```

## 3. ActionProposal

```yaml
action_proposal:
  proposal_id: PROP-001
  task_id: TASK-001
  decision_id: DEC-001
  category: git           # delete | dependency_change | credential_change | git | network | release | ""
  action: "git push origin main"
  arguments:
    repo: origin
    branch: main
  rationale: "Deploy approved changes to remote"
  expected_impact: "Remote main branch updated; CI triggered"
  rollback: "git reset --hard HEAD~1 && git push -f"
  risk_severity: low      # low | medium | high | critical
```

## 4. AuthorityPolicy (default — override per project)

```yaml
authority_policy:
  human_approval_required:
    - delete
    - dependency_change
    - credential_change
  autonomous_after_preconditions:
    - git
    - network
    - release
  critical_always_human: true
  unclassified_defaults_human: true
```

## 5. ActionReceipt

```yaml
action_receipt:
  receipt_id: RCPT-001
  proposal_id: PROP-001
  tool: terminal
  arguments:
    command: "git push origin main"
  result:
    exit_code: 0
    stdout: "Everything up-to-date"
  exit_code: 0
  external_ids:
    commit_sha: "abc123"
  artifact_sha256:
    output_report: "e3b0c44298fc1c149afbf4c8996fb92427ae41e4..."
  postcondition_ok: true
  note: ""
```

## 6. ProgressGuardState

```yaml
progress_guard:
  task_id: TASK-001
  identical_tool_call_count: 0
  identical_failure_count: 0
  no_artifact_change_cycles: 0
  repair_cycles: 0
# thresholds (defaults):
#   max_identical_tool_calls: 2
#   max_identical_failures: 2
#   max_no_artifact_change_cycles: 2
#   max_repair_cycles: 2
```

## 7. ReviewRequest

```yaml
review_request:
  review_id: REV-001
  task_id: TASK-001
  reason: EVALUATOR_DISAGREEMENT   # UNCERTAINTY | PROTECTED_ACTION | REPEATED_FAILURE | EVALUATOR_DISAGREEMENT
  plain_language_summary: |
    Two evaluators disagree on whether the synthesis section has sufficient
    citations. Evaluator A says it's fine; Evaluator B says 3 claims lack
    sources. You need to decide whether to accept or send back for repair.
  evidence:
    - "evaluator_a_report.md"
    - "evaluator_b_report.md"
    - "gate_3_citation_integrity.json"
  decision_needed: "Adjudicate whether claims X, Y, Z require citations"
  severity: medium
  technical_references:
    - "verification_result_gate3.json"
```

## 8. RegressionCase

```yaml
regression_case:
  case_id: REG-001
  originating_task: TASK-001
  failure_type: EVALUATOR_MISS    # BUG | EVALUATOR_MISS | FAILED_ASSUMPTION | PROCESS_FAILURE | RECURRING_DEFECT
  fixture: "tests/fixtures/synthesis_missing_citation.md"
  expected_behavior: "gate_3_citation_integrity flags missing citations as FAIL"
  missed_component: "citation extractor regex did not match (Author, Year) without comma"
  fix_proof_criteria: "Re-run gate_3 on fixture; must return FAIL with issue listing the missing citation"
```

## Governance Records

### DecisionRecord

```yaml
decision_record:
  decision_id: DEC-001
  task_id: TASK-001
  evaluation_id: EVAL-001
  recommendation_id: REC-01
  disposition: PARTIALLY_ACCEPTED  # ACCEPTED | PARTIALLY_ACCEPTED | DEFERRED | REJECTED | SUPERSEDED
  rationale: "Correctness findings accepted; quality suggestion deferred to next sprint"
  evidence: ["evaluator_report.md", "gate_results.json"]
  governing_rules: ["correctness > quality", "out-of-scope → ImprovementCandidate"]
  risk_of_rejection: low
```

### AcceptanceRecord

```yaml
acceptance_record:
  task_id: TASK-001
  status: PASS
  requirements:
    - id: REQ-01
      status: PASS
      evidence: ["gate_0_manifest.json", "evaluator_report.md"]
    - id: REQ-02
      status: PASS
      evidence: ["gate_1a_docx_integrity.json"]
  deterministic_gates: PASS
  independent_evaluation: PASS
  execution_log: "EXEC-TASK-001"
  citations:
    required: false
    evidence: []
  final_artifacts:
    - path: "output/report.docx"
      sha256: "e3b0c44298fc1c149afbf4c8996fb92427ae41e4..."
  orchestrator_decision: DEC-001
  research_task: false
```

### ImprovementCandidate

```yaml
improvement_candidate:
  candidate_id: IMP-001
  task_id: TASK-001
  description: "Add caching to the citation extraction step"
  rationale: "Current extraction takes 3s per document; caching would reduce to <0.5s"
  deferred_to: "Next sprint backlog"
  prohibited_in_current_task: true
```

### UncertaintySignal

```yaml
uncertainty_signal:
  signal_id: UNC-001
  task_id: TASK-001
  causes:
    - contradictory_requirements   # contradictory_requirements | missing_required_input | multiple_interpretations | insufficient_evidence | unresolved_architecture
    - insufficient_evidence
  description: "REQ-01 asks for 'comprehensive coverage' but scope budget limits to 10 sources"
  timestamp: "2026-08-31T19:49:00Z"
```

### CommandRiskAssessment

```yaml
command_risk_assessment:
  assessment_id: auto            # auto-generated MD5 hash of joined commands
  commands:
    - "rm -rf /tmp/scratch"
    - "pip install numpy"
  damage_potential: high          # auto-assessed: low | medium | high
  surface_to_human: true
  rationale: "Batch includes destructive rm -rf and dependency change"
```
