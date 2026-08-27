---
name: hermes-model-management
description: "Use when adding, removing, or aliasing LLM models in Hermes."
version: "1.0"
author: "hermes-curator"
tags: [hermes, config, models, openrouter, catalog]
metadata:
  hermes:
    tags: [hermes, config, models, openrouter, catalog]
    related_skills: [hermes-agent]
---

# Hermes Model Management

## When to Use

- User asks to add a new LLM to Hermes or the desktop GUI picker
- User wants to create a short alias for a model
- User wants to change the default model or fallback chain
- User asks to remove or reorder models in the picker

Add, remove, or update LLM models in Hermes so they appear in the desktop GUI picker and CLI.

## Key Files

| File | Purpose |
|------|---------|
| `C:\Users\cruzmars\AppData\Local\hermes\config.yaml` | Main config — aliases, default model, fallback chain |
| `C:\Users\cruzmars\AppData\Local\hermes\model_catalog_override.json` | Curated model list shown in the GUI picker |

The catalog JSON is referenced from config.yaml at:
```yaml
model_catalog:
  providers:
    openrouter:
      url:
        file:///C:/Users/cruzmars/AppData/Local/hermes/model_catalog_override.json
```

## Adding a New Model

### Step 1: Add to model_catalog_override.json

The JSON has a `providers` object. Each provider (e.g. `openrouter`, `nous`) has a `models` array. Add an entry to **every provider** that should offer the model:

```json
{
  "id": "provider/model-name",
  "description": "short badge text shown in picker"
}
```

- `description` is optional — shown as a badge in the GUI picker (e.g. "free", "recommended", "multimodal, 1M ctx").
- Set `"default": true` on at most one model per provider to make it the silent default.
- Place new entries near related models (same provider/family) for readability.

### Step 2: Add aliases in config.yaml (optional but recommended)

Under `model.aliases`, add short names that map to `provider/model-id`:

```yaml
model:
  aliases:
    glm-flash: openrouter/z-ai/glm-5.3-flash
    qwen-flash: openrouter/qwen/qwen3.8-flash
```

Aliases let users switch models by typing the short name in the GUI or CLI.

### Step 3: Verify

- Validate JSON: `python3 -c "import json; json.load(open('path/to/catalog.json'))"`
- Grep for the new model IDs to confirm placement in both providers
- Restart Hermes or start a new session for changes to take effect

## Pitfalls

- **Both providers**: If you only add to `openrouter` but not `nous` (or vice versa), the model won't appear when using that provider. Add to all relevant providers.
- **JSON trailing commas**: The catalog is strict JSON — no trailing commas. Use a linter or `json.load()` to validate after editing.
- **Alias format**: Aliases map to `provider/model-id` (e.g. `openrouter/z-ai/glm-5.3-flash`), not just the model ID.
- **Restart required**: Config changes don't hot-reload — a new session or app restart is needed.
- **Model ID must match OpenRouter exactly**: Use the ID from the OpenRouter model page URL (e.g. `z-ai/glm-5.3-flash` from `openrouter.ai/z-ai/glm-5.3-flash`).

## Removing a Model

Reverse the steps: remove from the catalog JSON (all providers) and remove any aliases. Validate JSON after.
