User's OpenRouter workspace runs a Guardrails policy (Model & Provider Access) allowing only Fireworks, Baseten, Google Vertex, Google AI Studio, Z.ai, Moonshot AI, CoreWeave, Crusoe, Amazon Bedrock — most other OpenRouter models 404 ("guardrail restrictions"). GET /api/v1/models is key-scoped: 141 allowed vs 465 public. The GUI picker's OpenRouter row mirrors that eligibility (109 chat/tool models after curation) via model_catalog.providers.openrouter.url → $HERMES_HOME/model_catalog_override.json, refreshed weekly by $HERMES_HOME/scripts/refresh_openrouter_catalog.py (cron 05201b4e9e35, Mon 9am, no_agent, deliver local); the duplicate `providers.openrouter-custom` entry is disabled, and auxiliary.* + fallback_providers point at openrouter/z-ai/glm-5.3-flash.§

Delegation: user prefers full source-text context for subagents, lean parallelism, explicit schemas, one validation script, verified deliverable paths, and z-ai/glm-5.3-flash for cost-effective bulk literature work.§

User has a `life-coach` Hermes profile (provisioned 2026-09-08) for personal coaching — isolated from the research/default profile, model deepseek/deepseek-v4-pro. Confidential wellness data lives in that profile's `coach/profile.json`; treat as sensitive and never surface it in this agent's titles/summaries/web queries.§

Personal shopping habit: hunts new/used fashion deals (Gymshark, adidas NMD Hu, Under Armour, mesh dresses) from reference photos across eBay/Amazon/Depop/Mercari; wants cheapest-first cross-site results with direct listing links.§

Marketplace searches on this host: Browserbase `browse` CLI absent and global npm installs blocked — use browser_exec with local Chrome instead; user approves 'Allow remote debugging?' popups when asked.
