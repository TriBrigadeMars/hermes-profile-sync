---
name: workflow-orchestrator
description: "Run multi-skill pipelines: plan, delegate, verify, package."
version: 1.0.0
author: Hermes Agent + Mars Cruz
license: MIT
metadata:
  hermes:
    tags: [workflow, orchestration, automation, research, documents]
    related_skills: [research-design-orchestrator, prisma-systematic-review]
---

# Workflow Orchestrator

## When to Use
Use when Mars asks to run a multi-step workflow that chains several skills/agents — e.g. literature review → analysis → document generation → packaging — or wants a custom pipeline built from the existing skill library.

## Intake (clarify tool)
1. **Goal** — free text.
2. **Skills/stages** — which known pipelines (research suite, PRISMA, docx/pptx/xlsx, apa-7-style-agent, grounded-citations, paralegal-assistant) or custom steps?
3. **Deliverable format** — .md | .docx | .pptx | .xlsx | zip package
4. **Save location** — always ask; default offer C:\Users\cruzmars\Documents
5. **Mode** — interactive (confirm between stages) or autonomous

## Pipeline Pattern

```
1. PLAN    - map goal to ordered skill stages (DAG); write plan.md
2. RUN     - one delegate_task per stage, sequential (Docker stability)
             each child context MUST include:
               - all prior-stage file paths
               - journal-weighted search policy (~70% peer-reviewed,
                 paywalled citable from abstracts, <=10% labeled gray lit)
               - "use write_file tool to save deliverable to {path};
                  do not just print to stdout"
3. VERIFY  - after EACH stage:
               - file exists and non-trivial size (>500 bytes)
               - if .docx: confirm real OOXML via python-docx re-open
                 (a prior subagent renamed markdown text to ".docx")
               - if script/math: re-run it yourself; sanity-check for
                 impossible patterns (e.g., uniform 100% power everywhere)
4. REVIEW  - short summary + clarify gate before next stage
5. PACKAGE - copy final files to Mars's chosen location; verify on disk
```

## Working Folder Convention
Create `~/workflow-{slug}-{timestamp}/` in the session workspace for intermediates. Final deliverables go ONLY where Mars specifies.

## Rules
- Run delegate_task children ONE at a time (sequential).
- Never trust a child's self-report of success - always verify on disk yourself.
- If a stage fails: retry once with simplified context, preserve partial output.
- Carry corrections forward: if Mars fixes course mid-pipeline, update the plan file and all downstream contexts - never silently continue.
- For scheduled/recurring versions of a pipeline, use cronjob with `context_from` chaining instead of delegate_task.
- List all available skills first (skills_list) before planning so no relevant skill is missed.

## Post-Stage Verification (v2 — Contract-Based)

After EVERY delegate_task stage, the orchestrator runs verification independently.
The child is NEVER asked "did it pass?" — the orchestrator collects artifacts and
checks them against the stage's declared contract.

### Architecture
- StageContract: declares outputs, preserves/may_modify, gates, effect_class
- ArtifactManifest: hash-verified output tracking (SHA-256)
- VerificationResult: PASS/WARN/FAIL/ERROR/NA with machine-readable evidence

### Gate reference (all in workflow-verification-v2/gates.py)
- Gate 0: artifact manifest (paths, existence, hashes, workspace containment)
- Gate 1a: DOCX integrity (ZIP/OOXML package validation, python-docx parse)
- Gate 1b: DOCX template policy (fonts, margins, headings — separate from integrity)
- Gate 2: power analysis sanity (controlled scenario families, Counter-aware monotonicity)
- Gate 3: citation integrity (Counter not set — catches duplicate reduction)
- Gate 3b: references exact (only for stages that promise frozen references)
- Gate 4: output-size budget (policy check, not invariant)
- Gate 5: accessibility preflight (NOT a Section 508 claim)
- Source fingerprinting: SHA-256 provenance chain across pipeline
- Source code integrity: py_compile check for Python scripts

### Usage
```python
import sys; sys.path.insert(0, '/path/to/workflow-verification-v2')
from models import StageContract, ArtifactManifest, Artifact, CONTRACTS
from gates import gate_0_manifest, gate_1a_docx_integrity, ...

# Load contract for this stage type
contract = CONTRACTS["style_pass"]

# After child returns, validate manifest
manifest = ArtifactManifest.from_json(child_output)
result = gate_0_manifest(manifest, workspace)
if result.status != "PASS":
    # handle failure — do NOT ask the child
```

### Failure handling
- PASS → proceed to next stage
- WARN → log, proceed with note to Mars
- FAIL → re-dispatch stage with specific gate failure in context (PURE/IDEMPOTENT only)
- ERROR → verification could not complete; escalate to Mars
- For SIDE_EFFECTING stages: do NOT auto-retry; create inspection/repair stage instead
