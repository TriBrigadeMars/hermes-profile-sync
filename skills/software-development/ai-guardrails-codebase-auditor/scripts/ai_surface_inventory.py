#!/usr/bin/env python3
"""Read-only AI surface inventory helper for Hermes AI guardrails audits.

Uses only the Python standard library. It searches text-like repository files for
AI/agent/security-relevant indicators and prints paths + line numbers. This is a
discovery aid, not a vulnerability scanner; findings require manual verification.
"""
from __future__ import annotations

import os
import re
import sys
from pathlib import Path

SKIP_DIRS = {
    ".git", ".hg", ".svn", "node_modules", "vendor", ".venv", "venv",
    "dist", "build", ".next", ".cache", "coverage", "target", "__pycache__",
}
MAX_BYTES = 2_000_000

GROUPS = {
    "model_clients": [
        r"openai", r"anthropic", r"bedrock", r"vertexai", r"vertex_ai", r"gemini",
        r"ollama", r"vllm", r"litellm", r"langchain", r"llamaindex", r"llama_index",
    ],
    "prompts": [
        r"system[_ -]?prompt", r"developer[_ -]?prompt", r"prompt[_ -]?template",
        r"role\s*[:=]\s*[\"']system", r"messages\s*=",
    ],
    "agents_tools_mcp": [
        r"tool[_ -]?call", r"function[_ -]?call", r"tools\s*=", r"agent", r"subagent",
        r"mcp", r"model context protocol", r"execute[_ -]?tool", r"invoke[_ -]?tool",
    ],
    "rag_embeddings_memory": [
        r"embedding", r"vector(store|db|_store)?", r"retriev", r"rag\b", r"chroma",
        r"pinecone", r"weaviate", r"qdrant", r"faiss", r"memory", r"checkpoint",
    ],
    "guardrails_policy": [
        r"guardrail", r"moderation", r"policy", r"allowlist", r"denylist", r"approval",
        r"human[_ -]?in[_ -]?the[_ -]?loop", r"schema", r"validate", r"sanitize",
    ],
    "dangerous_sinks": [
        r"subprocess", r"os\.system", r"shell\s*=\s*true", r"exec\(", r"eval\(",
        r"cursor\.execute", r"execute\(.*sql", r"requests\.(get|post|put|delete|patch)",
        r"fetch\(", r"axios\.", r"write_file", r"writeFile", r"send_email", r"sendMessage",
    ],
    "secrets_identity": [
        r"api[_ -]?key", r"secret", r"token", r"credential", r"authorization",
        r"tenant[_ -]?id", r"user[_ -]?id", r"service[_ -]?account", r"oauth",
    ],
    "budgets_loops": [
        r"max[_ -]?(tokens|iterations|steps|retries|tool_calls)", r"timeout", r"rate[_ -]?limit",
        r"while\s+true", r"for\s+.*range\(", r"retry", r"backoff",
    ],
}

COMPILED = {k: re.compile("|".join(v), re.IGNORECASE) for k, v in GROUPS.items()}


def text_candidate(path: Path) -> bool:
    try:
        if path.stat().st_size > MAX_BYTES:
            return False
        with path.open("rb") as f:
            chunk = f.read(4096)
        return b"\x00" not in chunk
    except OSError:
        return False


def walk(root: Path):
    for base, dirs, files in os.walk(root):
        dirs[:] = [d for d in dirs if d not in SKIP_DIRS]
        for name in files:
            p = Path(base) / name
            if text_candidate(p):
                yield p


def main() -> int:
    if len(sys.argv) != 2:
        print("usage: ai_surface_inventory.py <repo-root>", file=sys.stderr)
        return 2
    root = Path(sys.argv[1]).expanduser().resolve()
    if not root.is_dir():
        print(f"not a directory: {root}", file=sys.stderr)
        return 2

    results = {k: [] for k in GROUPS}
    for path in walk(root):
        try:
            lines = path.read_text(encoding="utf-8", errors="ignore").splitlines()
        except OSError:
            continue
        rel = path.relative_to(root)
        for lineno, line in enumerate(lines, 1):
            clipped = line.strip()
            if len(clipped) > 220:
                clipped = clipped[:217] + "..."
            for group, rx in COMPILED.items():
                if rx.search(line):
                    results[group].append((str(rel), lineno, clipped))

    for group, matches in results.items():
        print(f"\n## {group} ({len(matches)} matches)")
        for rel, lineno, line in matches[:200]:
            print(f"{rel}:{lineno}: {line}")
        if len(matches) > 200:
            print(f"... {len(matches) - 200} additional matches omitted")

    print("\nNOTE: Inventory matches are discovery signals, not findings. Manually verify all important paths.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
