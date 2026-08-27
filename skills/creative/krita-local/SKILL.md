---
name: krita-local
description: Automate Krita locally without network services.
version: 1.0.0
author: Local User, Hermes Agent
license: MIT
platforms: [windows, macos, linux]
metadata:
  hermes:
    tags: [graphics, krita, painting, layers, privacy, local]
    related_skills: []
    requires_toolsets: [terminal]
    config:
      - key: krita.work_dir
        description: Local directory for Krita jobs and exports.
        default: "~/hermes-creative/krita"
        prompt: Krita local work directory
      - key: krita.executable
        description: Optional explicit path to the Krita executable.
        default: ""
        prompt: Krita executable path (blank for auto-detect)
---
# Krita Local Skill

Use Krita through its local command-line export interface and an optional, manually-triggered Python plugin. The plugin reads one JSON job from disk only when the user invokes its Krita menu action; it does not watch folders, listen on ports, or communicate over a network.

## When to Use

- Use for local KRA export/conversion, animation sequence export, document/layer housekeeping, repeatable export jobs, and privacy-sensitive workflows.
- Use when a KRA document must remain the editable source of truth.
- Use the CLI path for deterministic file conversion/export that Krita natively supports.
- Use the optional plugin path when the task requires document/layer actions not exposed by the CLI.
- Don't use the plugin path for freehand painting, brush simulation, arbitrary pixel edits, or unsupported Krita API calls unless the plugin is deliberately extended and tested first.
- Don't start a server or filesystem watcher.

## Prerequisites

- Krita installed locally.
- Python 3 for Hermes-side helper scripts.
- For plugin jobs: install and enable the bundled `Hermes Local Jobs` Python plugin; see `references/plugin-setup.md`.
- Read `references/privacy-contract.md` before extending the plugin.

## How to Run

Detect Krita and show the exact command without executing:

```bash
python "${HERMES_SKILL_DIR}/scripts/krita_cli.py" detect
python "${HERMES_SKILL_DIR}/scripts/krita_cli.py" export INPUT.kra OUTPUT.png --dry-run
```

Perform a local export:

```bash
python "${HERMES_SKILL_DIR}/scripts/krita_cli.py" export INPUT.kra OUTPUT.png
```

Animation sequence export:

```bash
python "${HERMES_SKILL_DIR}/scripts/krita_cli.py" export-sequence INPUT.kra OUTPUT_PREFIX.png
```

Create a plugin job:

```bash
python "${HERMES_SKILL_DIR}/scripts/krita_job.py" --job-file JOB.json --operation document_info
```

The user then deliberately runs **Tools > Scripts > Hermes Local: Run Job** in Krita.

## Quick Reference

- `krita_cli.py detect` — locate Krita.
- `krita_cli.py export IN OUT` — native Krita CLI export.
- `krita_cli.py export-sequence IN OUT` — native animation sequence export.
- `krita_job.py` — create a local JSON plugin job.
- `scripts/install_plugin.py` — install plugin files into the user Krita `pykrita` directory.
- `templates/job.example.json` — job schema examples.
- `references/plugin-setup.md` — installation and activation.
- `references/privacy-contract.md` — no-network invariants.
- `references/sources.md` — documentation provenance for this version.
- `assets/hermes_krita_local.desktop` — Krita plugin descriptor.
- `assets/hermes_krita_local/__init__.py` — plugin package entry point.
- `assets/hermes_krita_local/plugin.py` — manually-triggered local job runner.

## Procedure

1. **Choose CLI or plugin mode.** Use CLI for export/conversion; plugin mode for supported document/layer actions. Completion criterion: the selected mode can perform every requested operation without inventing an API.
2. **Preserve the source.** Default to a new output path. Completion criterion: no source KRA will be overwritten unless the user explicitly requested it.
3. **CLI mode:** run `krita_cli.py ... --dry-run`, inspect the command, then execute without `--dry-run`. Completion criterion: process exits 0 and output exists.
4. **Plugin mode:** create exactly one JSON job at a user-visible path. Completion criterion: job validates against `templates/job.example.json` patterns and contains only allowlisted operations.
5. **User-trigger execution:** tell the user to run the `Hermes Local: Run Job` action inside Krita. Completion criterion: the plugin writes a sibling `.result.json` file reporting success/failure.
6. **Verify artifacts.** Check output files exist and, when feasible, use image metadata/vision to verify dimensions and visual intent. Completion criterion: result matches requested deliverable or differences are listed.

## Pitfalls

- Krita's CLI is strong for exports but is not a general remote-control interface.
- The bundled plugin is intentionally narrow: `document_info`, `create_layer`, `rename_layer`, `set_visibility`, `save`, `save_as`, and `export`.
- Layer lookup by name can be ambiguous; prefer unique layer names.
- The plugin does not auto-run jobs. That manual trigger is a privacy and safety feature.
- Do not add a polling loop, socket, localhost web server, or automatic file watcher when extending this skill.
- Krita resource locations differ by OS; use `install_plugin.py --target PATH` if auto-detection is wrong.

## Verification

- `python "${HERMES_SKILL_DIR}/scripts/krita_cli.py" detect` finds an executable or reports a clear failure.
- `--dry-run` prints an argument-vector command without invoking Krita.
- Plugin source passes Python syntax compilation.
- A test plugin job writes `.result.json` only after a deliberate in-app menu action.
- Exported files are separate from source files by default.
