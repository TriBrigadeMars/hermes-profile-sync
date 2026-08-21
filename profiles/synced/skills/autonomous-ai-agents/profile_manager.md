# profile_manager

## Overview
Manages Hermes Agent profiles across machines — creates, updates, rotates, and syncs credentials (SMTP, API keys) between profiles. Ensures consistent authentication across your three workstations.

## Purpose
- Create new Hermes profiles with isolated configs
- Rotate SMTP credentials (Gmail App Passwords) monthly
- Sync credentials between profiles (so one master credential set works everywhere)
- Enforce profile isolation (no cross-contamination of memory/tools)

## Profiles
- **remote_job_scout** – job-scanning agent (this one)
- **administrator** – system-level tools (cron, file management, desktop plugins)
- **developer** – coding/ML agents (if you add code agents later)

## Workflow
1. `hermes profile create <name>` – scaffolds a new profile with default config
2. `hermes profile update <name>` – applies a YAML config (credentials, tools, memory)
3. `hermes profile sync <name1> <name2>` – copies credentials from one profile to another
4. `hermes profile rotate <name>` – rotates SMTP credentials (Gmail App Password)

## Integration
- Triggered by `hermes job_scout` (when new jobs found)
- Triggered by `hermes profile_sync` (periodic credential rotation)
- Cross-profile communication via `hermes agent` linking

## Credential Management
- SMTP: Gmail App Password (16-char, rotated monthly)
- API Keys: GitHub, OpenRouter, etc. (rotated quarterly)
- Storage: Encrypted in `~/.hermes/credentials/` (encrypted via Hermes's secret store)

## Skill References
- `hermes-agent` (core framework)
- `hermes-profile-sync` (profile orchestration)
- `remote_adjunct_digest.py` (digest generation)
