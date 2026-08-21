# Hermes Profile Sync — Model Catalog Reference

This file documents the OpenRouter API models included in the synced profile's `model_catalog_override.json`.

## Added Models (commit d1eb49c)

- `thinkingmachines/inkling:free` — Free tier; active in current session (used for this conversation)
- `meta/muse-spark-1.2-contributor` — Contributor-tier; available via OpenRouter

## How the sync works

- `model_catalog_override.json` is bundled inside the profile archive (`profiles/synced/`)
- `hermes-sync.sh` pushes/pulls the archive to/from https://github.com/TriBrigadeMars/hermes-profile-sync
- `hermes agent config.yaml` points `model_catalog.providers.openrouter.url` to this file
- All 3 machines get the same model list after running the sync

## What does NOT sync (security)

- `.env` (OpenRouter API keys — never committed)
- `auth.json` (OAuth tokens — machine-local)
- `state.db` (session history — machine-local)
