# Hermes Profile Sync

Syncs Hermes Agent profiles across multiple machines via a private GitHub repo.

## Setup (run on each machine)

```bash
# 1. Clone this repo into your Hermes sync directory
cd "$LOCALAPPDATA/hermes"
rm -rf sync
git clone https://github.com/oe-marscruz/hermes-profile-sync.git sync

# 2. Make the script executable (Git Bash / WSL)
chmod +x sync/hermes-sync.sh

# 3. Test it
bash sync/hermes-sync.sh
```

## Auto Sync (every 15 minutes)

**Option A — Git Bash cron (if running):**
```bash
crontab -e
# Add: */15 * * * * bash "$LOCALAPPDATA/hermes/sync/hermes-sync.sh" >> "$LOCALAPPDATA/hermes/sync/sync.log" 2>&1
```

**Option B — Windows Task Scheduler:**
1. Open Task Scheduler
2. Create Basic Task → "Hermes Profile Sync"
3. Trigger: Every 15 minutes
4. Action: Start a program → `hermes-sync.bat`
5. Start in: `%LOCALAPPDATA%\hermes\sync`

## Manual Sync

```bash
bash "$LOCALAPPDATA/hermes/sync/hermes-sync.sh"
```

## What Gets Synced

- All Hermes profiles (exported as `.tar.gz` archives)
- Includes: config, skills, memory, plugins per profile

## What Does NOT Get Synced

- `.env` (API keys — never commit these)
- `auth.json` (OAuth tokens)
- `state.db` / `sessions/` (session history is machine-local)
- `logs/`
