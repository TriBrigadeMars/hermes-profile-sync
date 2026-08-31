# Hermes Profile Sync

Syncs Hermes Agent profiles, scripts, and cron jobs across multiple machines via a private GitHub repo.

> **AI agents:** read [AGENTS.md](AGENTS.md) before working in this repo. Before
> committing changes to `custom-skills-inventory.md` or `skills/`, run
> `python3 scripts/verify_inventory.py` — CI fails on documented-vs-actual drift.

## What Gets Synced

| Item | Direction | How |
|---|---|---|
| **Named profiles** | Push & pull | `hermes profile export/import` (tarballs in `profiles/`) |
| **Custom skills** | Repo → local | `skills/<category>/<name>/SKILL.md` installed to `$HERMES_HOME/skills/` |
| **Memories** | Push & merge | `memories/MEMORY.md` + `memories/USER.md` — entries split on `§`, deduplicated by MD5 content hash, merged bidirectionally |
| **Pets** | Push & pull | `pets/<slug>/pet.json` + `spritesheet.webp` |
| **Scripts** | Repo → local | `scripts/` copied to `$HERMES_HOME/scripts/` |
| **Cron jobs** | Repo → local | Created via `hermes cron create` if not present |

### Memory sync details

Hermes stores global (default-profile) memories as plain Markdown in
`$HERMES_HOME/memories/MEMORY.md` and `USER.md`, with entries separated by `§`.

- **Push:** local memory files are copied to `memories/` in the repo before commit.
- **Merge (after pull):** remote entries are merged into local by splitting both
  files on `§`, deduplicating by MD5 hash of each entry's content, and writing
  the union back to the local file. This means memories from Machine A appear on
  Machine B and vice versa, with no duplicates and no overwrites.
- Named profiles have their own memory stores inside their tarballs — those sync
  via the profile export/import step.

## Setup (run on each machine)

```bash
# 1. Clone this repo into your Hermes sync directory
cd "$LOCALAPPDATA/hermes"
rm -rf sync
git clone https://github.com/TriBrigadeMars/hermes-profile-sync.git sync

# 2. Make the script executable (Git Bash / WSL)
chmod +x sync/hermes-sync.sh

# 3. Test it
bash sync/hermes-sync.sh
```

## Auto Sync (daily)

**Windows Task Scheduler (recommended):**

One command (includes the missed-start failsafe):
```bash
powershell -NoProfile -ExecutionPolicy Bypass -File "%LOCALAPPDATA%\hermes\sync\setup-scheduled-task.ps1"
```

This creates the "Hermes Profile Sync" task to run daily at 04:00 AM with
`StartWhenAvailable` enabled — so if the PC is asleep at 4 AM, the sync runs
as soon as the machine wakes instead of being skipped. It also runs on battery
and has a 15-minute execution limit. Idempotent; no admin needed.

`setup-other-machine.bat` runs this automatically as its final step.

To adjust the time: `... setup-scheduled-task.ps1 -Time "06:30"`

Manual Task Scheduler alternative:
1. Open Task Scheduler (`taskschd.msc`)
2. Create Basic Task → "Hermes Profile Sync"
3. Trigger: Daily → once at 04:00 AM (no repeat)
4. Action: Start a program → `hermes-sync.bat`
5. Start in: `%LOCALAPPDATA%\hermes\sync`
6. In task Properties → Settings, tick **"Run task as soon as possible after a scheduled start is missed"**

**Git Bash cron (if running):**
```bash
crontab -e
# Add: 0 4 * * * bash "$LOCALAPPDATA/hermes/sync/hermes-sync.sh" >> "$LOCALAPPDATA/hermes/sync/sync.log" 2>&1
```

## Manual Sync

**Windows (recommended — works from any terminal):**
```cmd
%LOCALAPPDATA%\hermes\sync\hermes-sync.bat
```

**Git Bash / WSL:**
```bash
cd "$LOCALAPPDATA/hermes/sync" && bash hermes-sync.sh
```

> **Troubleshooting:** If you get `No such file or directory`, `$LOCALAPPDATA`
> may not be set in your shell (common in `cmd.exe` or PowerShell, where the
> variable is `%LOCALAPPDATA%` or `$env:LOCALAPPDATA` respectively). Use the
> `.bat` wrapper above instead, or open Git Bash directly.

## What Gets Synced

- All **named** Hermes profiles (exported as `.tar.gz` archives)
- Includes: config, skills, memory, plugins per profile
- The `default` profile is NOT synced (it's the built-in root)
- **Pets** (petdex mascots — including hatched/generated pets like Mackenzie) — `pets/<slug>/` with `pet.json` + `spritesheet.webp`
- **Scripts** (`academic_digest.py`, `mail.py`, `setup_digest.py`, `cron_config.json`) — copied to `~/.hermes/scripts/`
- **Cron jobs** — academic digest cron created automatically if missing
- **Custom skills** — full SKILL.md + references, scripts, data, and source files for custom skills under `skills/<category>/<name>/` (e.g. `skills/career/resume-builder/`, `skills/writing/ballotpedia-style-reviewer/`); installed into `~/.hermes/skills/` on each machine
- **Synced skills** — curated skills under `profiles/synced/skills/<category>/` (see below)

### Synced Skills (Bionic Desktop)

The current skillset from this Bionic/Hermes desktop installation lives under `profiles/synced/skills/bionic/`:

- `create-skill.md` — Create reusable guidance to perform certain tasks
- `document-processing-and-graphics.md` — Create, read, edit, and redline documents; diagrams, charts, and visualizations
- `install-skill.md` — Install a skill from a file, a folder, or a URL
- `introspection.md` — Introspect the local Bionic/Hermes installation
- `power-point-processing.md` — Create, read, edit PowerPoint files
- `skill-management.md` — Create, install, uninstall, or remove skills

Each file preserves the full `SKILL.md` content (including front matter) from the source installation.

## What Does NOT Get Synced

- `default` profile (built-in, machine-specific)
- `.env` (API keys — never commit these)
- `auth.json` (OAuth tokens)
- `state.db` / `sessions/` (session history is machine-local)
- `logs/`

## Academic Journal Digest

A biweekly email digest of 14 open-access journals in Public Health, AI/LLM, and Data Engineering. Asia/Europe preferred; US/Canada de-emphasized.

**Journals:**
- Lancet Global Health, Public Health, Regional Health WP, Digital Health
- BMJ Global Health
- Annals, Academy of Medicine Singapore
- J Formosan Medical Association (Taiwan)
- Nature Machine Intelligence, Computational Science
- Light: Science & Applications (China)
- Nature Communications, Scientific Reports, Communications Physics, Nature Electronics

**Files:**
- `scripts/academic_digest.py` — Main digest script (fetches RSS, builds email)
- `scripts/mail.py` — Gmail SMTP sender (reads credentials from `~/.hermes/.env`)
- `scripts/setup_digest.py` — One-command setup for new machines
- `scripts/cron_config.json` — Job metadata

**Setup on a new machine:**
```bash
python scripts/setup_digest.py
```

**Manual run:**
```bash
python ~/.hermes/scripts/academic_digest.py
```

**Cron:** Every 14 days at 09:00 MST. Created automatically by `hermes-sync.sh`.

## Local-Only Outlook MCP Server

A local MCP server that connects to the Outlook Desktop app via Windows COM automation — no cloud APIs, no Azure AD, no OAuth tokens. All data stays on your machine.

**Requirements:**
- Windows 10/11
- Outlook Desktop (Classic) — the `OUTLOOK.EXE` from Microsoft 365/Office (not the "new" Outlook)
- Python 3.10+

**Setup on a new machine:**

```bash
# 1. Create a dedicated venv (isolated from Hermes' internal packages)
python -m venv "$LOCALAPPDATA/hermes/mcp-outlook-venv"

# 2. Install mega-outlook-mcp + pinned mcp v1 (needed for FastMCP compatibility)
"$LOCALAPPDATA/hermes/mcp-outlook-venv/Scripts/pip.exe" install mega-outlook-mcp
"$LOCALAPPDATA/hermes/mcp-outlook-venv/Scripts/pip.exe" install "mcp>=1.2.0,<2.0.0"

# 3. Register with Hermes
hermes mcp add outlook --command "$LOCALAPPDATA/hermes/mcp-outlook-venv/Scripts/mega-outlook-mcp.exe" --connect-timeout 60

# 4. Restart Hermes Agent
```

**64 tools available** — email (24), folders (6), calendar (7), contacts/tasks/notes (9), account info (4), Exchange-specific (11), utility (3). Includes composite tools like `outlook_summarize_inbox`, `outlook_extract_action_items`, `outlook_meeting_prep`.

**Outlook Rule Creator** (`scripts/outlook_rule_creator.py`): creates Outlook rules from plain English descriptions. No MCP server needed — standalone script.

```bash
# Describe a rule (no changes)
python ~/.hermes/scripts/outlook_rule_creator.py --describe "Move emails from newsletter@example.com to Newsletters"

# Create a rule (asks for confirmation)
python ~/.hermes/scripts/outlook_rule_creator.py --create "Categorize emails about invoice as Finance"

# Generate VBA code for copy/paste
python ~/.hermes/scripts/outlook_rule_creator.py --vba "Move emails from any @amazon.com address to Shopping"
```

**Important notes:**
- The `mega-outlook-mcp` package requires `mcp<2.0.0` (uses `FastMCP` API). Hermes' internal `mcp` package is v2.0.0+ — that's why a separate venv is used.
- Outlook must be running and signed in when the MCP server starts.
- The MCP server spawns on-demand per conversation; nothing runs in the background.

## Creating a Profile to Sync

```bash
hermes profile create my-agent
hermes profile use my-agent
# Configure it, add skills, etc.
bash "$LOCALAPPDATA/hermes/sync/hermes-sync.sh"  # Push it
```
