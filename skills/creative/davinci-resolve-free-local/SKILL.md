---
name: davinci-resolve-free-local
description: Prepare Resolve Free edits through local file interchange.
version: 1.0.0
author: Local User, Hermes Agent
license: MIT
platforms: [windows, macos, linux]
metadata:
  hermes:
    tags: [video, davinci-resolve, editing, privacy, local]
    related_skills: []
    requires_toolsets: [terminal]
    config:
      - key: davinci_free.work_dir
        description: Local directory for generated Resolve interchange files.
        default: "~/hermes-creative/davinci"
        prompt: Resolve Free local work directory
---
# DaVinci Resolve Free Local Skill

Prepare files and edit decisions for DaVinci Resolve Free without MCP, network bridges, or external Resolve scripting. This skill treats Resolve Free as a user-controlled application and uses deterministic local interchange files around it.

## When to Use

- Use when the user has **DaVinci Resolve Free** and wants Hermes to prepare an edit, subtitle file, media inventory, cut list, or importable timeline decisions.
- Use for transcript-driven rough cuts, selects, silence-removal plans, shot lists, subtitle generation, and render verification.
- Use when privacy requirements prohibit MCP servers, localhost bridges, sockets, or remote-control services.
- Use when Hermes can prepare files but the user will perform the final import/click inside Resolve.
- Don't use for direct live control of the Resolve UI, Color page, Fusion page, Fairlight mixer, render queue, or timeline through the external Resolve API.
- Don't claim Resolve Free exposes Studio's external scripting preference.

## Prerequisites

- DaVinci Resolve Free installed locally.
- Python 3 for bundled helper scripts.
- Optional: `ffprobe` from FFmpeg for media inspection and output verification.
- Read `references/limitations.md` before promising automation.
- Read `references/interchange.md` before generating an EDL or subtitle package.

## How to Run

Use Hermes' `terminal` tool. Always invoke bundled scripts through `${HERMES_SKILL_DIR}`.

Media manifest:

```bash
python "${HERMES_SKILL_DIR}/scripts/media_manifest.py" INPUT_OR_FOLDER --output manifest.json
```

Build a CMX3600 EDL:

```bash
python "${HERMES_SKILL_DIR}/scripts/cmx3600.py" edit-plan.json --output rough-cut.edl
```

Build subtitles:

```bash
python "${HERMES_SKILL_DIR}/scripts/srt_from_json.py" subtitles.json --output captions.srt
```

All scripts support `--help`. Do not overwrite a user's source media or Resolve project.

## Quick Reference

- `media_manifest.py PATH --output FILE` — inspect media with `ffprobe`.
- `cmx3600.py PLAN --output FILE` — create a non-drop-frame CMX3600 EDL.
- `srt_from_json.py INPUT --output FILE` — create/validate SRT from timestamped JSON.
- `templates/edit-plan.example.json` — EDL plan schema.
- `templates/subtitles.example.json` — subtitle schema.
- `references/limitations.md` — Resolve Free capability boundary.
- `references/interchange.md` — import/export workflow and timecode rules.
- `references/sources.md` — documentation provenance for this version.

## Procedure

1. **Confirm edition and desired deliverable.** Treat the application as Resolve Free unless the user explicitly says Studio. Completion criterion: the planned workflow contains no external Resolve API call or network bridge.
2. **Inventory source media.** If `ffprobe` is available, run `media_manifest.py`; otherwise collect filenames, frame rate, duration, and start timecode from user-provided metadata. Completion criterion: every clip referenced by the edit plan maps to an existing source file or a clearly identified placeholder.
3. **Create a non-destructive edit plan.** Represent every edit as source reel/clip, source in/out, record in/out, track, and transition. Prefer cuts in v1. Completion criterion: no edit has negative duration, overlapping record time unless intentional, or an out point before its in point.
4. **Generate interchange.** Use `cmx3600.py` for a simple video cut list. For workflows that exceed CMX3600, produce a human-readable edit plan instead of inventing unsupported interchange syntax. Completion criterion: the helper exits successfully and the generated EDL has sequential events.
5. **Generate subtitles separately.** Use `srt_from_json.py` for captions/subtitles. Completion criterion: cues are ordered, non-negative, and have start < end.
6. **Hand off to Resolve Free.** Tell the user exactly which generated file to import through Resolve's timeline/subtitle import workflow. Do not claim the import happened unless the user or a later file confirms it. Completion criterion: the user has an importable artifact plus concise import instructions.
7. **Verify after export.** If the user provides a rendered file, run `media_manifest.py` or `ffprobe` to check duration, frame rate, dimensions, streams, and codec. Completion criterion: reported output properties match the requested delivery target or discrepancies are clearly listed.

## Pitfalls

- Resolve Free does not expose Studio's **External Scripting Using: Local/Network** control surface. Do not attempt `DaVinciResolveScript.scriptapp("Resolve")` from an outside process as the core workflow.
- Do not create or recommend a localhost bridge merely to bypass the Free-edition boundary; that violates this skill's privacy contract.
- CMX3600 is intentionally limited. It is suitable for straightforward cuts but not a lossless representation of every Resolve feature.
- This v1 EDL helper uses non-drop timecode and a nominal integer timebase. For 23.976 material use nominal 24 fps timecode only when the project/source convention actually matches.
- Reel names in CMX3600 are short and compatibility-sensitive. The helper normalizes them; preserve a separate manifest that maps reels to full filenames.
- Never delete, trim, transcode, or overwrite source media unless the user explicitly requests it and a backup/output path is specified.
- If the user requests direct in-app automation, explain the Free-edition boundary and offer a generated in-app script or manual procedure, but do not imply Hermes can launch it externally.

## Verification

- Run the helper script with `--help` and confirm it exits 0.
- Generate the bundled example EDL and inspect that event numbers are sequential and source/record durations match.
- Generate the bundled example SRT and confirm timestamps are monotonic.
- If `ffprobe` is installed, verify every referenced source before creating final interchange.
- Final response must distinguish **prepared**, **imported by user**, and **verified after render** states.
