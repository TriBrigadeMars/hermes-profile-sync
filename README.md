# Hermes Profile Sync

Syncs Hermes Agent profiles across multiple machines via a private GitHub repo.

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

## Auto Sync (every 15 minutes)

**Windows Task Scheduler (recommended):**
1. Open Task Scheduler (`taskschd.msc`)
2. Create Basic Task → "Hermes Profile Sync"
3. Trigger: Daily → repeat every 15 minutes
4. Action: Start a program → `hermes-sync.bat`
5. Start in: `%LOCALAPPDATA%\hermes\sync`

**Git Bash cron (if running):**
```bash
crontab -e
# Add: */15 * * * * bash "$LOCALAPPDATA/hermes/sync/hermes-sync.sh" >> "$LOCALAPPDATA/hermes/sync/sync.log" 2>&1
```

## Manual Sync

```bash
bash "$LOCALAPPDATA/hermes/sync/hermes-sync.sh"
```

## What Gets Synced

- All **named** Hermes profiles (exported as `.tar.gz` archives)
- Includes: config, skills, memory, plugins per profile
- The `default` profile is NOT synced (it's the built-in root)

## What Does NOT Get Synced

- `default` profile (built-in, machine-specific)
- `.env` (API keys — never commit these)
- `auth.json` (OAuth tokens)
- `state.db` / `sessions/` (session history is machine-local)
- `logs/`

## Creating a Profile to Sync

```bash
hermes profile create my-agent
hermes profile use my-agent
# Configure it, add skills, etc.
bash "$LOCALAPPDATA/hermes/sync/hermes-sync.sh"  # Push it
```
