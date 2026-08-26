---
name: outlook-agents
description: "Manage Outlook calendar: daily briefs, conflict detection."
version: 0.1.0
author: User
license: MIT
platforms: [windows, linux, macos]
metadata:
  hermes:
    tags: [outlook, calendar, email, scheduling, agents, microsoft, graph-api]
---

# Outlook Agents

AI-powered Microsoft Outlook calendar management through Microsoft Graph API. Five specialized agents: Fetch, Classify, Schedule, Conflict, Notify.

## Setup

1. Register Azure AD app: `python ~/outlook-agents/scripts/setup.py --guide`
2. Save credentials: `python ~/outlook-agents/scripts/setup.py --client-id YOUR_ID --tenant-id YOUR_TENANT`
3. Install deps: `pip install -r ~/outlook-agents/requirements.txt`
4. First auth: `python ~/outlook-agents/orchestrator.py today`

## Commands

All commands run from `~/outlook-agents`:

```bash
python orchestrator.py daily              # Full daily brief
python orchestrator.py today              # Quick today check
python orchestrator.py weekly             # Weekly summary
python orchestrator.py find-slot --duration 30  # Find free slot
python orchestrator.py conflicts          # Check conflicts
python orchestrator.py search "query"     # Search events
python orchestrator.py create --subject "X" --start "ISO" --end "ISO"
python orchestrator.py emails             # Recent emails
```

Add `--json-output` to any command for structured JSON.

## Cron Scheduling

```bash
# Morning brief at 8:30 AM weekdays
hermes cron create --name "outlook-daily" --schedule "30 8 * * 1-5" \
  --command "cd ~/outlook-agents && python orchestrator.py daily"
```

## Configuration

Edit `~/outlook-agents/config/settings.yaml` for work hours, timezone, classification rules, scheduling preferences.

## Pitfalls

1. "Allow public client flows" must be ON in Azure AD app
2. Admin consent needed for work/school accounts
3. Delete `~/.outlook-agents/token_cache.json` to force re-auth
4. Set correct timezone in settings.yaml
