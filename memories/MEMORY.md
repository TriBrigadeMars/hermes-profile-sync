Delegation: lock JSON schemas; combine collect+summary; define acronyms; one validation script; pre-test docx builders; batch API calls; verify child deliverable paths.
§
QIQA project: outputs to Desktop\...\Hermes Output QIQA Project. Gemma 4 E4B + Unsloth XPU/Arc B580. User learning ML — plain-language guides.
§
RATE-LIMIT RULE: User requires slow, sequential downloads (15–30s between requests) for any bulk internet fetching — university network, fears IP flagging by security. Always set and confirm a rate limit before bulk downloads.
§
Redaction Automation System: ...\Automated Redaction\. Pipeline v2 (2026-09-02): idempotent resume, stable job IDs (zip hash + config fingerprint), state/processed.json manifest, msvcrt lock, write-verify-rename, verification_policy.ROUTABLE. Tests 53 pass. file-intake-pipeline skill USER-OWNED, outdated.
MD stage (2026-09-04): cron 'redacted-files-to-markdown' (ecee0257e57e, * * * * *, no_agent, deliver local) → scripts/redacted_files_to_markdown.py → venv scripts/redaction_md_venv (markitdown 0.1.7) → scripts/redacted_md_impl.py. Converts pdf/docx/txt/md/csv/json/xml (+pptx/xlsx/html); images & scan-only PDFs skipped-logged (no OCR). State+conversion.log in 'Redacted File to Markdown' dest. Collision: stem__ext.md. Source untouched.
§
Windows Hermes skills install under HERMES_HOME/skills/ (C:\Users\cruzmars\AppData\Local\hermes\skills), not ~/.hermes/skills. Nested skill ZIPs: inspect safely, validate frontmatter, back up differing live files, verify discovery.
§
Multi-topic lit review: procedure in multi-topic-literature-review skill (sequential subagents, absolute paths, APA 7, sleep-3 rate limit, md2docx preflight).
§
Webapp done-claims need a real browser check — curl-200 success can hide blank pages. OpenRouter gemini-2.0-flash-001 dead → gemini-3.8-flash.
§
File Cleanup Report (dup-detector v2): read-only scanner → weekly xlsx in Documents\File Cleanup Reports (only write). Scans ONLY Pictures, Downloads, Documents, Desktop, Videos. Allowlist: dups/stale only .docx .xlsx .pptx .pdf .mp4 .mp3 .jpg .jpeg .png .webp .md .ics; others still count for folder emptiness. Cron 9001d5dd6951 Sun 9am no_agent; needs gateway.