# Hermes Profile Sync

Syncs Hermes Agent profiles, scripts, and cron jobs across multiple machines via a private GitHub repo.

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
1. Open Task Scheduler (`taskschd.msc`)
2. Create Basic Task → "Hermes Profile Sync"
3. Trigger: Daily → once at 04:00 AM (no repeat)
4. Action: Start a program → `hermes-sync.bat`
5. Start in: `%LOCALAPPDATA%\hermes\sync`

**Git Bash cron (if running):**
```bash
crontab -e
# Add: 0 4 * * * bash "$LOCALAPPDATA/hermes/sync/hermes-sync.sh" >> "$LOCALAPPDATA/hermes/sync/sync.log" 2>&1
```

## Manual Sync

```bash
bash "$LOCALAPPDATA/hermes/sync/hermes-sync.sh"
```

## What Gets Synced

- All **named** Hermes profiles (exported as `.tar.gz` archives)
- Includes: config, skills, memory, plugins per profile
- The `default` profile is NOT synced (it's the built-in root)
- **Scripts** (`academic_digest.py`, `mail.py`, `setup_digest.py`, `cron_config.json`) — copied to `~/.hermes/scripts/`
- **Cron jobs** — academic digest cron created automatically if missing

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

## Creating a Profile to Sync

```bash
hermes profile create my-agent
hermes profile use my-agent
# Configure it, add skills, etc.
bash "$LOCALAPPDATA/hermes/sync/hermes-sync.sh"  # Push it
```
