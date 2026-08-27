---
name: gimp-local
description: Automate GIMP locally through batch-safe workflows.
version: 1.0.0
author: Local User, Hermes Agent
license: MIT
platforms: [windows, macos, linux]
metadata:
  hermes:
    tags: [graphics, gimp, script-fu, batch, privacy, local]
    related_skills: []
    requires_toolsets: [terminal]
    config:
      - key: gimp.work_dir
        description: Local directory for GIMP Script-Fu jobs and outputs.
        default: "~/hermes-creative/gimp"
        prompt: GIMP local work directory
      - key: gimp.executable
        description: Optional explicit path to a GIMP console executable.
        default: ""
        prompt: GIMP console executable path (blank for auto-detect)
---
# GIMP Local Skill

Run privacy-first GIMP 3 automation through GIMP's native Script-Fu batch interpreter. Each job is a finite `.scm` file executed by a new GIMP batch process; this skill never uses Script-Fu Server, MCP, or a persistent listener.

## When to Use

- Use for deterministic local GIMP batch jobs, image transformations, repeatable PDB operations, exports, and offline processing.
- Use when the user wants GIMP itself to execute the operation rather than a separate image library.
- Use Script-Fu v3 conventions for newly authored jobs.
- Use the GIMP Procedure Browser or official GIMP 3 PDB documentation to verify procedure names/signatures before writing a new operation.
- Don't use GIMP's Script-Fu Server in this privacy profile.
- Don't invent a PDB signature from memory when an incorrect call could alter a source file.

## Prerequisites

- GIMP 3 installed locally.
- Python 3 for the Hermes-side launcher.
- A GIMP console executable discoverable by `scripts/gimp_batch.py`, or an explicit path.
- Read `references/scriptfu-v3.md` and `references/privacy-contract.md`.

## How to Run

Detect GIMP:

```bash
python "${HERMES_SKILL_DIR}/scripts/gimp_batch.py" detect
```

Dry-run a batch job:

```bash
python "${HERMES_SKILL_DIR}/scripts/gimp_batch.py" run JOB.scm --dry-run
```

Execute a finite Script-Fu job:

```bash
python "${HERMES_SKILL_DIR}/scripts/gimp_batch.py" run JOB.scm
```

Start from `templates/job-template.scm`. Replace its placeholder body only with PDB calls whose GIMP 3 signatures have been verified.

## Quick Reference

- `gimp_batch.py detect` — locate GIMP console executable.
- `gimp_batch.py run FILE.scm` — execute one Script-Fu file in batch mode.
- `templates/job-template.scm` — v3-dialect job skeleton.
- `templates/smoke-test.scm` — non-destructive message-only test.
- `references/scriptfu-v3.md` — GIMP 3 authoring rules.
- `references/privacy-contract.md` — prohibits Script-Fu Server/listeners.
- `references/sources.md` — documentation provenance for this version.

## Procedure

1. **Inspect inputs and define outputs.** Default to a distinct output path. Completion criterion: no source file will be overwritten unless the user explicitly requested it.
2. **Verify the required PDB calls.** Check GIMP 3 Procedure Browser or current GIMP developer documentation. Completion criterion: procedure names, argument order/types, and plugin keyword arguments are known rather than guessed.
3. **Write a finite Script-Fu job.** Begin from `job-template.scm`, call `script-fu-use-v3`, and avoid registration/server code for one-shot jobs. Completion criterion: the file contains no network/server procedure and has a clear final save/export/exit behavior when relevant.
4. **Dry-run the launcher.** Run `gimp_batch.py ... --dry-run`. Completion criterion: printed argv points to the intended local GIMP executable and exact job file.
5. **Execute.** Run the job as a new GIMP batch process. Completion criterion: process returns 0 and expected outputs exist.
6. **Verify.** Inspect output metadata and, for visual tasks, inspect the rendered image. Completion criterion: requested dimensions/format/appearance are met or discrepancies are reported.

## Pitfalls

- GIMP 3 changed many Script-Fu/PDB details from GIMP 2.x. Prefer the v3 dialect and current signatures.
- Script-Fu plugin procedures support keyword arguments; use them where documented to reduce signature-order fragility.
- `gimp-console` executable names vary by platform/package. The launcher tries common names but may need `--gimp PATH`.
- Do not use `plug-in-script-fu-server`; it is explicitly outside this skill's privacy model.
- Batch jobs can still be destructive if they save over source files. Use separate output paths by default.
- A successful batch exit does not prove visual correctness; inspect outputs.

## Verification

- Run `templates/smoke-test.scm`; successful output proves the batch interpreter is reachable without a server.
- `--dry-run` prints a finite local argv command.
- Job source contains no server/listener invocation.
- Expected output exists and has the requested file type/dimensions.
- Preserve the `.scm` job beside the output when reproducibility matters.
