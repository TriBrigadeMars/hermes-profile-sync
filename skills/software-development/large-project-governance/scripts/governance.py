"""Large-Project Evaluation & Governance Framework - deterministic control-plane helpers.

Implements the 8 control primitives and supporting governance records described in
SKILL.md as pure, testable Python. No LLM calls; orchestrators call these
functions to enforce policy deterministically between agent steps.

Primitives:
  1. EvaluationContract      -> evaluation_contract_valid()
  2. TrajectoryContract      -> trajectory_contract_valid(), trajectory_violations()
  3. ActionProposal          -> action_proposal_valid()
  4. AuthorityPolicy         -> authority_requires_human(), safe_to_execute()
  5. ActionReceipt           -> action_receipt_valid()
  6. ProgressGuard           -> eval_progress_guard()
  7. ReviewRequest           -> review_request_valid(), build_disagreement_report()
  8. RegressionCase          -> regression_case_valid()

Governance records: DecisionRecord, AcceptanceRecord, ImprovementCandidate,
EvaluationDisagreementRecord, UncertaintySignal, CommandRiskAssessment.

Usage:
    python governance.py --check     # run the built-in self-tests

As a library:
    from governance import authority_requires_human, eval_progress_guard, acceptance_record_complete
"""
from __future__ import annotations

import hashlib
import json
import re
from dataclasses import asdict, dataclass, field
from enum import Enum
from typing import Any, Iterable


# --- Enums & shared types -------------------------------------------------

class Disposition(str, Enum):
    ACCEPTED = "ACCEPTED"
    PARTIALLY_ACCEPTED = "PARTIALLY_ACCEPTED"
    DEFERRED = "DEFERRED"
    REJECTED = "REJECTED"
    SUPERSEDED = "SUPERSEDED"


class GuardState(str, Enum):
    NORMAL = "NORMAL"
    WATCH = "WATCH"
    HUMAN_REVIEW_REQUIRED = "HUMAN_REVIEW_REQUIRED"


DEFAULT_REPAIR_CYCLES = 2
DEFAULT_MAX_IDENTICAL_TOOL_CALLS = 2
DEFAULT_MAX_IDENTICAL_FAILURES = 2
DEFAULT_MAX_NO_ARTIFACT_CHANGE = 2

HUMAN_APPROVED_ACTION_CATEGORIES = ("delete", "dependency_change", "credential_change")
AUTONOMOUS_ACTION_CATEGORIES = ("git", "network", "release")


def _filter_fields(cls, d):
    """Return only keys that match dataclass fields of cls."""
    return {k: v for k, v in d.items() if k in cls.__dataclass_fields__}


# === Primitive 1 - EvaluationContract =====================================

@dataclass
class EvaluationContract:
    task_id: str
    requirements: list = field(default_factory=list)
    dimensions: list = field(default_factory=list)
    deterministic_gates: list = field(default_factory=list)
    independent_evaluation_required: bool = True
    evidence_required: bool = True
    research_citations_required: bool = False

    @classmethod
    def from_dict(cls, d):
        return cls(**_filter_fields(cls, d))

    def to_dict(self):
        return asdict(self)

    def to_json(self, **kw):
        return json.dumps(self.to_dict(), indent=2, default=str, **kw)


def evaluation_contract_valid(contract):
    c = contract if isinstance(contract, EvaluationContract) else EvaluationContract.from_dict(contract)
    issues = []
    if not getattr(c, "task_id", ""):
        issues.append("task_id is required")
    if not getattr(c, "requirements", []):
        issues.append("requirements must name at least one REQ id")
    if not getattr(c, "dimensions", []):
        issues.append("dimensions must name at least one evaluation dimension")
    if c.independent_evaluation_required and not c.evidence_required:
        issues.append("independent evaluation requires evidence_required=True")
    return (not issues, issues)


# === Primitive 2 - TrajectoryContract =====================================

@dataclass
class TrajectoryContract:
    task_id: str
    required_skills: list = field(default_factory=list)
    permitted_skills: list = field(default_factory=list)
    required_tools: list = field(default_factory=list)
    forbidden_tools: list = field(default_factory=list)
    permitted_paths: list = field(default_factory=list)
    max_tool_calls: int = 30
    max_llm_calls: int = 12
    expected_stage_order: list = field(default_factory=list)
    allowed_side_effects: list = field(default_factory=list)

    @classmethod
    def from_dict(cls, d):
        return cls(**_filter_fields(cls, d))

    def to_dict(self):
        return asdict(self)


def trajectory_contract_valid(contract):
    t = contract if isinstance(contract, TrajectoryContract) else TrajectoryContract.from_dict(contract)
    issues = []
    if not getattr(t, "task_id", ""):
        issues.append("task_id is required")
    if t.max_tool_calls < 1:
        issues.append("max_tool_calls must be >= 1")
    if t.max_llm_calls < 1:
        issues.append("max_llm_calls must be >= 1")
    return (not issues, issues)


def trajectory_violations(contract, used_tools, used_skills, tool_calls, llm_calls):
    """Check an observed execution trace against the trajectory contract.
    Returns a list of human-readable violations (empty == compliant)."""
    t = contract if isinstance(contract, TrajectoryContract) else TrajectoryContract.from_dict(contract)
    v = []
    tools, skills = set(used_tools), set(used_skills)

    if t.forbidden_tools:
        hit = sorted(tools & set(t.forbidden_tools))
        if hit:
            v.append("forbidden tool(s) used: " + str(hit))
    if t.required_tools:
        missing = sorted(set(t.required_tools) - tools)
        if missing:
            v.append("required tool(s) never used: " + str(missing))
    if t.required_skills:
        missing = sorted(set(t.required_skills) - skills)
        if missing:
            v.append("required skill(s) never loaded: " + str(missing))
    if t.permitted_skills:
        unknown = sorted(s for s in skills if s not in t.permitted_skills and s not in t.required_skills)
        if unknown:
            v.append("skill(s) outside permitted set: " + str(unknown))
    if tool_calls > t.max_tool_calls:
        v.append("tool-call budget exceeded: {} > {}".format(tool_calls, t.max_tool_calls))
    if llm_calls > t.max_llm_calls:
        v.append("LLM-call budget exceeded: {} > {}".format(llm_calls, t.max_llm_calls))
    return v


# === Primitive 3 - ActionProposal =========================================

@dataclass
class ActionProposal:
    proposal_id: str
    task_id: str
    decision_id: str = ""
    category: str = ""
    action: str = ""
    arguments: dict = field(default_factory=dict)
    rationale: str = ""
    expected_impact: str = ""
    rollback: str = ""
    risk_severity: str = "low"

    @classmethod
    def from_dict(cls, d):
        return cls(**_filter_fields(cls, d))

    def to_dict(self):
        return asdict(self)


def action_proposal_valid(proposal):
    p = proposal if isinstance(proposal, ActionProposal) else ActionProposal.from_dict(proposal)
    issues = []
    if not getattr(p, "proposal_id", ""):
        issues.append("proposal_id is required")
    if not getattr(p, "task_id", ""):
        issues.append("task_id is required")
    if not getattr(p, "action", ""):
        issues.append("action is required")
    if not getattr(p, "rationale", ""):
        issues.append("rationale is required")
    if not getattr(p, "rollback", ""):
        issues.append("rollback plan is required (even if 'none')")
    return (not issues, issues)


# === Primitive 4 - AuthorityPolicy ========================================

def authority_requires_human(proposal, *, policy=None):
    """Decide whether an approved proposal needs human approval before execution.

    Default policy: human approval required for delete / dependency-change /
    credential-change + any critical-risk proposal; git/network/release are
    autonomous after preconditions. Unclassified consequential actions default
    to requiring human approval. Pass a custom *policy* to override:
    {"human": [...], "autonomous": [...]}.
    """
    p = proposal if isinstance(proposal, ActionProposal) else ActionProposal.from_dict(proposal)
    pol = policy or {
        "human": list(HUMAN_APPROVED_ACTION_CATEGORIES),
        "autonomous": list(AUTONOMOUS_ACTION_CATEGORIES),
    }
    cat = (p.category or "").lower()
    if cat in pol.get("human", []):
        return True
    if (p.risk_severity or "").lower() == "critical":
        return True
    if cat not in pol.get("autonomous", []):
        return True
    return False


def safe_to_execute(proposal, *, approved=False, preconditions_passed=False, policy=None):
    """Full authority gate: returns (may_execute, reason)."""
    p = proposal if isinstance(proposal, ActionProposal) else ActionProposal.from_dict(proposal)
    if not approved:
        return False, "not approved"
    if authority_requires_human(p, policy=policy):
        return False, "human approval required"
    if not preconditions_passed:
        return False, "automated preconditions not passed"
    return True, "authorized"


# === Primitive 5 - ActionReceipt ==========================================

@dataclass
class ActionReceipt:
    receipt_id: str
    proposal_id: str
    tool: str = ""
    arguments: dict = field(default_factory=dict)
    result: dict = field(default_factory=dict)
    exit_code: int | None = None
    external_ids: dict = field(default_factory=dict)
    artifact_sha256: dict = field(default_factory=dict)
    postcondition_ok: bool | None = None
    note: str = ""

    @classmethod
    def from_dict(cls, d):
        return cls(**_filter_fields(cls, d))

    def to_dict(self):
        return asdict(self)


def action_receipt_valid(receipt):
    """Validate that an ActionReceipt is complete. A receipt whose postcondition
    check is False is a FAILED action, regardless of a 0 exit code."""
    r = receipt if isinstance(receipt, ActionReceipt) else ActionReceipt.from_dict(receipt)
    issues = []
    if not getattr(r, "receipt_id", ""):
        issues.append("receipt_id is required")
    if not getattr(r, "proposal_id", ""):
        issues.append("proposal_id is required")
    if not getattr(r, "tool", ""):
        issues.append("tool is required")
    if r.postcondition_ok is None:
        issues.append("postcondition_ok must be set (executed != succeeded)")
    return (not issues, issues)


# === Primitive 6 - ProgressGuard ==========================================

@dataclass
class ProgressGuardState:
    task_id: str = ""
    identical_tool_call_count: int = 0
    identical_failure_count: int = 0
    no_artifact_change_cycles: int = 0
    repair_cycles: int = 0

    def to_dict(self):
        return asdict(self)


def eval_progress_guard(state, *, max_identical_tool_calls=DEFAULT_MAX_IDENTICAL_TOOL_CALLS,
                        max_identical_failures=DEFAULT_MAX_IDENTICAL_FAILURES,
                        max_no_artifact_change=DEFAULT_MAX_NO_ARTIFACT_CHANGE,
                        max_repair_cycles=DEFAULT_REPAIR_CYCLES):
    """Detect loops / no-progress without an LLM call.

    Returns:
      NORMAL                  - all counts below thresholds
      WATCH                   - one threshold nearly tripped (informational)
      HUMAN_REVIEW_REQUIRED   - a default threshold exceeded
    """
    s = state if isinstance(state, ProgressGuardState) else ProgressGuardState(**_filter_fields(ProgressGuardState, state))
    tripped = (
        s.identical_tool_call_count > max_identical_tool_calls
        or s.identical_failure_count > max_identical_failures
        or s.no_artifact_change_cycles > max_no_artifact_change
        or s.repair_cycles > max_repair_cycles
    )
    if tripped:
        return GuardState.HUMAN_REVIEW_REQUIRED

    near = (
        s.identical_tool_call_count == max_identical_tool_calls
        or s.identical_failure_count == max_identical_failures
        or s.no_artifact_change_cycles == max_no_artifact_change
        or s.repair_cycles == max_repair_cycles
    )
    return GuardState.WATCH if near else GuardState.NORMAL


# === Primitive 7 - ReviewRequest + disagreement report ====================

@dataclass
class ReviewRequest:
    review_id: str
    task_id: str
    reason: str
    plain_language_summary: str = ""
    evidence: list = field(default_factory=list)
    decision_needed: str = ""
    severity: str = "medium"
    technical_references: list = field(default_factory=list)

    @classmethod
    def from_dict(cls, d):
        return cls(**_filter_fields(cls, d))

    def to_dict(self):
        return asdict(self)


def review_request_valid(req):
    r = req if isinstance(req, ReviewRequest) else ReviewRequest.from_dict(req)
    issues = []
    if not getattr(r, "review_id", ""):
        issues.append("review_id is required")
    if not getattr(r, "task_id", ""):
        issues.append("task_id is required")
    if not getattr(r, "reason", ""):
        issues.append("reason is required")
    if not getattr(r, "decision_needed", ""):
        issues.append("decision_needed must state exactly what the human decides")
    return (not issues, issues)


def build_disagreement_report(*, subject, evaluator_a, evaluator_b,
                              a_position, b_position, a_evidence, b_evidence,
                              agreements, disagreement_points, decision_needed):
    """Produce the plain-language evaluator-disagreement report required by policy.
    No jargon required to read; technical reports can be appended as references."""
    lines = [
        "# Evaluator Disagreement - Human Review Required",
        "",
        "**Under review:** " + str(subject),
        "",
        "**" + str(evaluator_a) + " position (plain language):** " + str(a_position),
        "- Evidence: " + str(a_evidence),
        "",
        "**" + str(evaluator_b) + " position (plain language):** " + str(b_position),
        "- Evidence: " + str(b_evidence),
        "",
        "**Where they agree:**",
    ]
    if agreements:
        lines += ["- " + str(a) for a in agreements]
    else:
        lines.append("- (independent disagreement - see below)")
    lines.append("")
    lines.append("**Exact points of disagreement:**")
    if disagreement_points:
        lines += ["- " + str(p) for p in disagreement_points]
    else:
        lines.append("- (see positions above)")
    lines.append("")
    lines.append("**Decision needed from you:** " + str(decision_needed))
    return "\n".join(lines)


# === Primitive 8 - RegressionCase =========================================

@dataclass
class RegressionCase:
    case_id: str
    originating_task: str
    failure_type: str
    fixture: str = ""
    expected_behavior: str = ""
    missed_component: str = ""
    fix_proof_criteria: str = ""

    @classmethod
    def from_dict(cls, d):
        return cls(**_filter_fields(cls, d))

    def to_dict(self):
        return asdict(self)


def regression_case_valid(case):
    c = case if isinstance(case, RegressionCase) else RegressionCase.from_dict(case)
    issues = []
    if not getattr(c, "case_id", ""):
        issues.append("case_id is required")
    if not getattr(c, "originating_task", ""):
        issues.append("originating_task is required")
    if not getattr(c, "expected_behavior", ""):
        issues.append("expected_behavior is required (the regression target)")
    return (not issues, issues)


# === Governance records ===================================================

# --- DecisionRecord -------------------------------------------------------

@dataclass
class DecisionRecord:
    decision_id: str
    task_id: str
    evaluation_id: str = ""
    recommendation_id: str = ""
    disposition: str = "ACCEPTED"
    rationale: str = ""
    evidence: list = field(default_factory=list)
    governing_rules: list = field(default_factory=list)
    risk_of_rejection: str = "low"

    @classmethod
    def from_dict(cls, d):
        return cls(**_filter_fields(cls, d))

    def to_dict(self):
        return asdict(self)


def decision_record_requires_rationale(rec):
    """Any disposition other than straightforward ACCEPTED requires recorded reasoning."""
    r = rec if isinstance(rec, DecisionRecord) else DecisionRecord.from_dict(rec)
    return (r.disposition or "").upper() != "ACCEPTED"


def decision_record_valid(rec):
    r = rec if isinstance(rec, DecisionRecord) else DecisionRecord.from_dict(rec)
    issues = []
    if not getattr(r, "decision_id", ""):
        issues.append("decision_id is required")
    if not getattr(r, "task_id", ""):
        issues.append("task_id is required")
    if decision_record_requires_rationale(r) and not r.rationale:
        issues.append("non-ACCEPTED disposition requires a rationale")
    return (not issues, issues)


# --- AcceptanceRecord -----------------------------------------------------

@dataclass
class AcceptanceRecord:
    task_id: str
    status: str = "PASS"
    requirements: list = field(default_factory=list)
    deterministic_gates: str = ""
    independent_evaluation: str = ""
    execution_log: str = ""
    citations: dict = field(default_factory=dict)
    final_artifacts: list = field(default_factory=list)
    orchestrator_decision: str = ""
    research_task: bool = False

    @classmethod
    def from_dict(cls, d):
        return cls(**_filter_fields(cls, d))

    def to_dict(self):
        return asdict(self)


def acceptance_record_complete(rec):
    """Determine whether an AcceptanceRecord qualifies as a final PASS.

    Requires: status == PASS, every requirement has its own status==PASS and
    >=1 evidence item, gates + independent evaluation recorded, an execution log,
    and (for research) citation evidence for substantive claims.
    """
    r = rec if isinstance(rec, AcceptanceRecord) else AcceptanceRecord.from_dict(rec)
    issues = []
    if r.status != "PASS":
        issues.append("status must be 'PASS' for final acceptance, got " + repr(r.status))
    if not r.deterministic_gates.strip():
        issues.append("deterministic_gates verdict is required")
    if not r.independent_evaluation.strip():
        issues.append("independent_evaluation verdict is required")
    if not r.execution_log.strip():
        issues.append("execution_log must reference the execution record")
    for req in r.requirements:
        rid = req.get("id", "?") if isinstance(req, dict) else "?"
        if not isinstance(req, dict):
            issues.append("requirement entries must be dicts")
            continue
        if req.get("status") != "PASS":
            issues.append("requirement " + str(rid) + " not marked PASS")
        elif not req.get("evidence"):
            issues.append("requirement " + str(rid) + " has no evidence")
    if r.research_task and not r.citations.get("evidence"):
        issues.append("research task requires citation evidence")
    return (not issues, issues)


# --- ImprovementCandidate -------------------------------------------------

@dataclass
class ImprovementCandidate:
    candidate_id: str
    task_id: str
    description: str
    rationale: str
    deferred_to: str = ""
    prohibited_in_current_task: bool = True

    @classmethod
    def from_dict(cls, d):
        return cls(**_filter_fields(cls, d))

    def to_dict(self):
        return asdict(self)


def improvement_candidate_valid(cand):
    c = cand if isinstance(cand, ImprovementCandidate) else ImprovementCandidate.from_dict(cand)
    issues = []
    if not getattr(c, "candidate_id", ""):
        issues.append("candidate_id is required")
    if not getattr(c, "description", ""):
        issues.append("description is required")
    return (not issues, issues)


# --- EvaluationDisagreementRecord -----------------------------------------

@dataclass
class EvaluationDisagreementRecord:
    disagreement_id: str
    subject: str
    positions: list = field(default_factory=list)
    agreements: list = field(default_factory=list)
    human_review_requested: bool = True

    @classmethod
    def from_dict(cls, d):
        return cls(**_filter_fields(cls, d))

    def to_dict(self):
        return asdict(self)


def eval_disagreement_valid(rec):
    r = rec if isinstance(rec, EvaluationDisagreementRecord) else EvaluationDisagreementRecord.from_dict(rec)
    issues = []
    if not getattr(r, "disagreement_id", ""):
        issues.append("disagreement_id is required")
    if len(r.positions) < 2:
        issues.append("need at least two positions to record a disagreement")
    return (not issues, issues)


# --- UncertaintySignal ----------------------------------------------------

@dataclass
class UncertaintySignal:
    signal_id: str
    task_id: str
    causes: list = field(default_factory=list)
    description: str = ""
    timestamp: str = ""

    @classmethod
    def from_dict(cls, d):
        return cls(**_filter_fields(cls, d))

    def to_dict(self):
        return asdict(self)


def uncertainty_signal_valid(sig):
    s = sig if isinstance(sig, UncertaintySignal) else UncertaintySignal.from_dict(sig)
    issues = []
    if not getattr(s, "signal_id", ""):
        issues.append("signal_id is required")
    if not getattr(s, "causes", []):
        issues.append("at least one cause is required")
    return (not issues, issues)


# --- CommandRiskAssessment ------------------------------------------------

_DAMAGE_PATTERNS = re.compile(
    r"(rm\s+-rf?\s*[^\s]|del\s+/[fs]|format|mkfs|wipe|shutdown"
    r"|sudo\s+rm|dd\s+if=|git\s+push\s+-f|git\s+reset\s+--hard"
    r"|pip\s+install|npm\s+install|choco\s+install|winget\s+install)",
    re.IGNORECASE,
)

_DESTRUCTIVE_PATTERNS = re.compile(
    r"(rm\s+-rf|del\s+/[fs]|format|mkfs|wipe|shutdown|dd\s+if=)",
    re.IGNORECASE,
)


@dataclass
class CommandRiskAssessment:
    assessment_id: str
    commands: list = field(default_factory=list)
    damage_potential: str = "low"
    surface_to_human: bool = False
    rationale: str = ""

    @classmethod
    def from_dict(cls, d):
        return cls(**_filter_fields(cls, d))

    def to_dict(self):
        return asdict(self)


def assess_command_risk(commands, *, rationale=""):
    """Heuristically surface command batches with destructive potential for human review."""
    cmds = list(commands)
    joined = "\n".join(cmds)
    if _DAMAGE_PATTERNS.search(joined):
        if _DESTRUCTIVE_PATTERNS.search(joined):
            damage = "high"
        else:
            damage = "medium"
    else:
        damage = "low"
    return CommandRiskAssessment(
        assessment_id=hashlib.md5(joined.encode()).hexdigest()[:12],
        commands=cmds,
        damage_potential=damage,
        surface_to_human=damage in ("high", "medium"),
        rationale=rationale,
    )


def command_risk_valid(assess):
    a = assess if isinstance(assess, CommandRiskAssessment) else CommandRiskAssessment.from_dict(assess)
    issues = []
    if not getattr(a, "commands", []):
        issues.append("at least one command is required")
    if a.damage_potential not in ("low", "medium", "high"):
        issues.append("damage_potential must be low|medium|high")
    if a.damage_potential in ("medium", "high") and not a.surface_to_human:
        issues.append("medium/high damage potential must surface to human")
    return (not issues, issues)


# === Self-test ============================================================

def _self_check():
    """Run built-in self-tests covering every primitive and record."""
    lines = []
    failures = []

    # 1. EvaluationContract
    c = EvaluationContract(task_id="TASK-001", requirements=["REQ-01", "REQ-02"],
                           dimensions=["correctness"])
    ok, iss = evaluation_contract_valid(c)
    lines.append("1. evaluation_contract_valid: valid={} issues={}".format(ok, iss))
    if not ok:
        failures.append("evaluation_contract_valid")

    # 2. TrajectoryContract + violations
    tc = TrajectoryContract(task_id="T-1", forbidden_tools=["eval"],
                            required_skills=["docx"], max_tool_calls=5)
    ok2, iss2 = trajectory_contract_valid(tc)
    vn = trajectory_violations(tc, used_tools=["write_file", "eval"],
                               used_skills=[], tool_calls=6, llm_calls=2)
    lines.append("2. trajectory_contract_valid: valid={} issues={}".format(ok2, iss2))
    lines.append("   trajectory_violations: {}".format(vn))
    if not ok2:
        failures.append("trajectory_contract_valid")
    if len(vn) != 3:
        failures.append("trajectory_violations expected 3 issues got {}".format(len(vn)))

    # 3. ActionProposal
    p = ActionProposal(proposal_id="P-1", task_id="T-1", category="delete",
                       action="rm -rf /tmp/x", rationale="clean scratch", rollback="none")
    ok3, iss3 = action_proposal_valid(p)
    lines.append("3. action_proposal_valid: valid={} issues={}".format(ok3, iss3))
    if not ok3:
        failures.append("action_proposal_valid")

    # 4. AuthorityPolicy
    requires_human_delete = authority_requires_human(p)
    p_git = ActionProposal(proposal_id="P-2", task_id="T-1", category="git",
                           action="git push", rationale="deploy", rollback="git reset")
    requires_human_git = authority_requires_human(p_git)
    p_unknown = ActionProposal(proposal_id="P-3", task_id="T-1", category="",
                               action="custom", rationale="test", rollback="none")
    requires_human_unknown = authority_requires_human(p_unknown)
    can_exec, reason = safe_to_execute(p_git, approved=True, preconditions_passed=True)
    lines.append("4. authority: delete={} git={} unknown={} safe_to_execute(git)=({},{})".format(
        requires_human_delete, requires_human_git, requires_human_unknown, can_exec, reason))
    if not requires_human_delete:
        failures.append("authority delete should require human")
    if requires_human_git:
        failures.append("authority git should be autonomous")
    if not requires_human_unknown:
        failures.append("authority unclassified should require human")
    if not can_exec:
        failures.append("safe_to_execute git should be True")

    # 5. ActionReceipt
    ar = ActionReceipt(receipt_id="R-1", proposal_id="P-1", tool="terminal",
                       postcondition_ok=True)
    ok5, iss5 = action_receipt_valid(ar)
    lines.append("5. action_receipt_valid: valid={} issues={}".format(ok5, iss5))
    if not ok5:
        failures.append("action_receipt_valid")

    # 6. ProgressGuard
    pg_normal = ProgressGuardState(repair_cycles=0)
    pg_watch = ProgressGuardState(repair_cycles=2)
    pg_tripped = ProgressGuardState(repair_cycles=3)
    lines.append("6. progress_guard: normal={} watch={} tripped={}".format(
        eval_progress_guard(pg_normal).value,
        eval_progress_guard(pg_watch).value,
        eval_progress_guard(pg_tripped).value))
    if eval_progress_guard(pg_normal) != GuardState.NORMAL:
        failures.append("progress_guard normal")
    if eval_progress_guard(pg_watch) != GuardState.WATCH:
        failures.append("progress_guard watch")
    if eval_progress_guard(pg_tripped) != GuardState.HUMAN_REVIEW_REQUIRED:
        failures.append("progress_guard tripped")

    # 7. ReviewRequest + disagreement report
    rr = ReviewRequest(review_id="RR-1", task_id="T-1", reason="EVALUATOR_DISAGREEMENT",
                       decision_needed="Adjudicate citation completeness")
    ok7, iss7 = review_request_valid(rr)
    report = build_disagreement_report(
        subject="Synthesis", evaluator_a="EvA", evaluator_b="EvB",
        a_position="Looks good", b_position="Missing citation",
        a_evidence=["manual rev"], b_evidence=["gate3"],
        agreements=["scope"],
        disagreement_points=["citation completeness"],
        decision_needed="Adjudicate")
    lines.append("7. review_request_valid: valid={} issues={}".format(ok7, iss7))
    lines.append("   disagreement_report length: {}".format(len(report)))
    if not ok7:
        failures.append("review_request_valid")
    if len(report) < 100:
        failures.append("disagreement report too short")

    # 8. RegressionCase
    rc = RegressionCase(case_id="RC-1", originating_task="T-1",
                        failure_type="BUG", expected_behavior="output matches input")
    ok8, iss8 = regression_case_valid(rc)
    lines.append("8. regression_case_valid: valid={} issues={}".format(ok8, iss8))
    if not ok8:
        failures.append("regression_case_valid")

    # Governance records: DecisionRecord
    dr = DecisionRecord(decision_id="D-1", task_id="T-1", disposition="REJECTED",
                        rationale="insufficient evidence")
    ok_d, iss_d = decision_record_valid(dr)
    lines.append("   decision_record_valid: valid={} issues={}".format(ok_d, iss_d))
    if not ok_d:
        failures.append("decision_record_valid")

    # AcceptanceRecord (PASS)
    ar_pass = AcceptanceRecord(
        task_id="T-1", status="PASS", deterministic_gates="PASS",
        independent_evaluation="PASS", execution_log="EXEC-1",
        requirements=[{"id": "REQ-01", "status": "PASS", "evidence": ["gate0"]}])
    ok_a, iss_a = acceptance_record_complete(ar_pass)
    lines.append("   acceptance_record_complete: valid={} issues={}".format(ok_a, iss_a))
    if not ok_a:
        failures.append("acceptance_record_complete: " + str(iss_a))

    # AcceptanceRecord (FAIL - missing evidence)
    ar_fail = AcceptanceRecord(
        task_id="T-2", status="PASS", deterministic_gates="PASS",
        independent_evaluation="PASS", execution_log="EXEC-2",
        requirements=[{"id": "REQ-01", "status": "PASS", "evidence": []}])
    ok_af, iss_af = acceptance_record_complete(ar_fail)
    lines.append("   acceptance_record_complete(fail): valid={} issues={}".format(ok_af, iss_af))
    if ok_af:
        failures.append("acceptance_record should fail on missing evidence")

    # AcceptanceRecord (research needs citations)
    ar_res = AcceptanceRecord(
        task_id="T-3", status="PASS", deterministic_gates="PASS",
        independent_evaluation="PASS", execution_log="EXEC-3", research_task=True,
        requirements=[{"id": "REQ-01", "status": "PASS", "evidence": ["gate0"]}])
    ok_ar, iss_ar = acceptance_record_complete(ar_res)
    lines.append("   acceptance_record_complete(research): valid={} issues={}".format(ok_ar, iss_ar))
    if ok_ar:
        failures.append("acceptance_record should fail on missing citations for research")

    # ImprovementCandidate
    ic = ImprovementCandidate(candidate_id="IC-1", task_id="T-1",
                              description="add caching", rationale="speed")
    ok_i, iss_i = improvement_candidate_valid(ic)
    lines.append("   improvement_candidate_valid: valid={} issues={}".format(ok_i, iss_i))
    if not ok_i:
        failures.append("improvement_candidate_valid")

    # CommandRiskAssessment
    cra_safe = assess_command_risk(["ls", "cat file.txt"])
    cra_destruct = assess_command_risk(["rm -rf /tmp/scratch"])
    cra_install = assess_command_risk(["pip install numpy"])
    ok_c1, _ = command_risk_valid(cra_safe)
    ok_c2, _ = command_risk_valid(cra_destruct)
    ok_c3, _ = command_risk_valid(cra_install)
    lines.append("   command_risk: safe={} destruct(damage={},human={}) install(damage={},human={})".format(
        ok_c1, cra_destruct.damage_potential, cra_destruct.surface_to_human,
        cra_install.damage_potential, cra_install.surface_to_human))
    if not ok_c1 or not ok_c2 or not ok_c3:
        failures.append("command_risk_valid")
    if cra_safe.damage_potential != "low":
        failures.append("ls should be low risk")
    if cra_destruct.damage_potential != "high":
        failures.append("rm -rf should be high risk")
    if cra_install.damage_potential != "medium":
        failures.append("pip install should be medium risk")
    if not cra_destruct.surface_to_human:
        failures.append("rm -rf should surface to human")

    lines.append("")
    if failures:
        lines.append("FAILURES: " + str(failures))
    else:
        lines.append("ALL SELF-TESTS PASSED")
    return "\n".join(lines)


# === CLI entry / module guard =============================================

if __name__ == "__main__":
    import sys
    if "--check" in sys.argv:
        print("--- governance.py self-check ---")
        print(_self_check())
        print("--- done ---")
    else:
        print("governance.py - run with --check for self-tests")


__all__ = [
    "Disposition", "GuardState",
    "DEFAULT_REPAIR_CYCLES", "DEFAULT_MAX_IDENTICAL_TOOL_CALLS",
    "DEFAULT_MAX_IDENTICAL_FAILURES", "DEFAULT_MAX_NO_ARTIFACT_CHANGE",
    "HUMAN_APPROVED_ACTION_CATEGORIES", "AUTONOMOUS_ACTION_CATEGORIES",
    "EvaluationContract", "evaluation_contract_valid",
    "TrajectoryContract", "trajectory_contract_valid", "trajectory_violations",
    "ActionProposal", "action_proposal_valid",
    "authority_requires_human", "safe_to_execute",
    "ActionReceipt", "action_receipt_valid",
    "ProgressGuardState", "eval_progress_guard",
    "ReviewRequest", "review_request_valid", "build_disagreement_report",
    "RegressionCase", "regression_case_valid",
    "DecisionRecord", "decision_record_requires_rationale", "decision_record_valid",
    "AcceptanceRecord", "acceptance_record_complete",
    "ImprovementCandidate", "improvement_candidate_valid",
    "EvaluationDisagreementRecord", "eval_disagreement_valid",
    "UncertaintySignal", "uncertainty_signal_valid",
    "CommandRiskAssessment", "assess_command_risk", "command_risk_valid",
]
