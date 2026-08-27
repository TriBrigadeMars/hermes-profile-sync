---
name: hermes-skill-installation
description: Install custom skills from zip, folder, or git and sync.
version: 0.1.0
author: oe-marscruz (oe-marscruz), Hermes Agent
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [skills, installation, sync, zip, deployment, custom-skills]
    related_skills: [hermes-agent-skill-authoring]
---

# Custom Skill Installation

Install third-party or locally-packaged Hermes skills from zip archives, folders, or git repos into the local skills directory, and optionally sync them across machines via the hermes-profile-sync repository.

## When to Use

- User provides a `.zip` file, folder, or git URL containing a Hermes skill.
- User asks to "install this skill" from an attachment or local file.
- User wants to ensure installed skills are synced to other machines via the profile-sync repo.
- A skill package includes an `install.py` — run it, but verify the destination path first.

Don't use for:
- Skills already installed in the hub (`hermes skills install official/...`). Use `setup_mcp` for MCP servers.
- Editing the source of an installed skill. Use `skill_manage(action='patch')` instead.

## Prerequisites

- The skill zip/folder must contain a `SKILL.md` with valid YAML frontmatter.
- On Windows, the skills directory is `$LOCALAPPDATA/hermes/skills/`, NOT `~/.hermes/skills/`.

## Procedure

### 1. Extract the zip (if applicable)

```bash
cd "$LOCALAPPDATA/Temp" && mkdir -p skill-install && cd skill-install
unzip -o "$HOME/Downloads/<filename>.zip" -d .
```

### 2. Inspect the package

- Read `SKILL.md` to confirm valid frontmatter (`name`, `description`, `version`).
- Check for an `install.py` — most skill packages ship one.
- Note the intended destination from the installer (usually `~/.hermes/skills/<category>/<name>/`).
- Accept any security prompts or end-user license agreements if present.

### 3. Run the installer with the correct path

**Windows path pitfall (CRITICAL):** Most skill installers default to `~/.hermes/skills/`, which resolves to `C:\Users\<user>\.hermes\skills\` on Windows. The actual Hermes skills directory is `$LOCALAPPDATA/hermes/skills/`. You MUST pass the correct destination explicitly:

```bash
# Single skill with install.py
python scripts/install.py --destination "$LOCALAPPDATA/hermes/skills/<category>/<name>"

# Multi-skill suite with install_all.py
python install_all.py --skills-root "$LOCALAPPDATA/hermes/skills" [--force]

# Multi-skill with --target flag
python scripts/install.py --target "$LOCALAPPDATA/hermes/skills/<category>/<name>"
```

Common flag names: `--destination`, `--dest`, `--target`, `--skills-root`. Read the installer source first to confirm which flag it uses.

If no installer exists, manually copy the skill directory:

```bash
mkdir -p "$LOCALAPPDATA/hermes/skills/<category>/<name>"
cp -r <extracted-skill>/* "$LOCALAPPDATA/hermes/skills/<category>/<name>/"
```

### 4. Verify installation

```bash
ls "$LOCALAPPDATA/hermes/skills/<category>/<name>/"
wc -c "$LOCALAPPDATA/hermes/skills/<category>/<name>/SKILL.md"
```

Confirm:
- `SKILL.md` exists and is non-empty.
- `references/`, `scripts/`, `data/`, `sources/` directories have content where expected.
- Any PDFs or source files are non-zero.

Then verify Hermes recognizes it: call `skills_list` and confirm the skill appears with the correct category.

### 5. Clean up temp extraction

```bash
rm -rf "$LOCALAPPDATA/Temp/skill-install"
```

### 6. Sync to other machines (optional)

If the user maintains a profile-sync repo, add the newly installed skills for cross-machine deployment:

```bash
SYNC_DIR="$LOCALAPPDATA/hermes/sync"
mkdir -p "$SYNC_DIR/skills/<category>"
cp -r "$LOCALAPPDATA/hermes/skills/<category>/<name>" "$SYNC_DIR/skills/<category>/"
```

Then run the full sync:

```bash
cd "$SYNC_DIR" && bash hermes-sync.sh
```

Update `custom-skills-inventory.md` in the sync repo to reflect the new skills.

## Pitfalls

1. **`~/.hermes/skills/` on Windows does NOT resolve to the right place.** On Windows, `~` expands to `C:\Users\<user>`, so `~/.hermes/skills/` becomes `C:\Users\cruzmars\.hermes\skills\` — a directory that may not exist or may be stale. The real skills directory is `$LOCALAPPDATA/hermes/skills/`. Always check with `echo "$LOCALAPPDATA/hermes/skills"` before running any installer.

2. **Install scripts use inconsistent flag names.** Some use `--destination`, some `--dest`, some `--target`, some `--skills-root`. One package (`hermes-career-application-suite`) used `--skills-root` at the top level and `--dest`/`--target` in its sub-installers. Read the script source (`scripts/install.py` or the top-level `install.py`) before running to confirm the right flag.

3. **Bundled skills cannot be overwritten without `--force`.** If a skill name collides with an installed one, the installer will error. Use `--force` only when you intend to replace it.

4. **Zip extractors may create nested directories.** A zip like `ballotpedia-style-reviewer-v0.1.0.zip` may extract to `ballotpedia-skill/ballotpedia-style-reviewer/` — check the actual depth before running the installer.

5. **Multi-skill suite installers create inconsistent nesting.** The `hermes-career-application-suite` installed skills to `career/resume-builder/resume-builder/SKILL.md` (double-nested). Always verify the actual directory structure after running `install_all.py`:
   ```bash
   find "$LOCALAPPDATA/hermes/skills/<category>" -name SKILL.md | head -20
   ```
   If you see `<skill>/<skill>/SKILL.md` doubling, the install worked but the structure is non-canonical — Hermes still finds it via max-depth search.

6. **PDF source files can be large.** The Ballotpedia skill was 15.3 MB because of 3 PDFs. Consider `.gitattributes` LFS for the sync repo if committed file sizes become a problem, or warn the user about KB impact in the sync push.

7. **Empty files in archives.** The `bp_style_lint.py` was 0 bytes in the source zip itself. Always run `wc -c` on key scripts after extraction to catch packaging errors before troubleshooting runtime failures.

8. **Identifying custom vs bundled skills.** Use `$LOCALAPPDATA/hermes/skills/.bundled_manifest` to diff installed skills against the bundled set:
   ```bash
   cut -d: -f1 "$LOCALAPPDATA/hermes/skills/.bundled_manifest" | sort > /tmp/bundled.txt
   find "$LOCALAPPDATA/hermes/skills" -maxdepth 4 -name SKILL.md | \
     grep -v '\.hub/' | xargs -I{} basename "$(dirname {})" | sort -u > /tmp/installed.txt
   comm -23 /tmp/installed.txt /tmp/bundled.txt
   ```

## Sync Repo Conventions

When syncing custom skills across machines via a git-backed sync repo (e.g., `hermes-profile-sync`), use this structure:

```
skills/
  <category>/              # career/, writing/, data-science/
    <skill-name>/
      SKILL.md
      references/
      ...
  _standalone/
    <skill-name>/          # Skills with no category prefix
      SKILL.md
      ...
```

**Standalone skills** (like `ocr-redaction-local`) go in `skills/_standalone/<skill-name>/`. The sync script handles these separately since they install to `$HERMES_HOME/skills/<name>/` not `$HERMES_HOME/skills/<category>/<name>/`.

**Category-level stray files:** When `cp -r` copies a single-file skill into a category dir, it may land as `<category>/SKILL.md` instead of `<category>/<name>/SKILL.md`. Verify directory structure after batch-copying and restructure if needed.

**Sync script update checklist:** After adding new skills:
- Verify `hermes-sync.sh` handles both categorized and `_standalone` skills
- Update `custom-skills-inventory.md` with new entries and updated counts
- Update `README.md` if new sync patterns were introduced

## Verification

After installation:
- `skills_list` shows the skill under the correct category name.
- `skill_view(name='<skill-name>')` loads the full SKILL.md successfully.
- Key reference/data files have non-zero size.
- If synced, `cd "$LOCALAPPDATA/hermes/sync" && git status` shows the new files and the push succeeds.