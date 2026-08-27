#!/usr/bin/env python3
"""Read-only security surface inventory helper for the Hermes audit skill.

This tool finds security-relevant files and code patterns. Matches are discovery
leads only; they are not vulnerability findings and must be manually verified.
"""

from __future__ import annotations

import argparse
import json
import os
import re
import sys
from collections import Counter, defaultdict
from dataclasses import dataclass, asdict
from pathlib import Path
from typing import Iterable

MAX_FILE_BYTES = 1_500_000
MAX_MATCHES_PER_RULE = 80

SKIP_DIRS = {
    ".git", ".hg", ".svn", ".idea", ".vscode", "node_modules", "vendor",
    "dist", "build", "target", ".next", ".nuxt", ".cache", "coverage",
    "__pycache__", ".venv", "venv", "env", ".tox", ".mypy_cache",
    ".pytest_cache", ".terraform", ".gradle", "Pods", "DerivedData",
}

TEXT_EXTENSIONS = {
    ".py", ".pyi", ".js", ".jsx", ".ts", ".tsx", ".mjs", ".cjs",
    ".java", ".kt", ".kts", ".go", ".rs", ".c", ".h", ".cc", ".cpp",
    ".cxx", ".hpp", ".cs", ".php", ".rb", ".swift", ".scala", ".sh",
    ".bash", ".zsh", ".ps1", ".sql", ".graphql", ".gql", ".html",
    ".htm", ".vue", ".svelte", ".xml", ".yaml", ".yml", ".json",
    ".toml", ".ini", ".cfg", ".conf", ".properties", ".gradle",
    ".tf", ".tfvars", ".hcl", ".dockerfile", ".md", ".txt",
}

SPECIAL_FILENAMES = {
    "Dockerfile", "Containerfile", "Makefile", "Gemfile", "Gemfile.lock",
    "Rakefile", "Pipfile", "Pipfile.lock", "poetry.lock", "pyproject.toml",
    "requirements.txt", "package.json", "package-lock.json", "npm-shrinkwrap.json",
    "yarn.lock", "pnpm-lock.yaml", "go.mod", "go.sum", "Cargo.toml",
    "Cargo.lock", "pom.xml", "build.gradle", "build.gradle.kts", "composer.json",
    "composer.lock", "gradlew", "gradlew.bat", "mix.exs", "mix.lock",
}

FILE_CATEGORIES = {
    "dependency/build manifests": re.compile(
        r"^(package(-lock)?\.json|npm-shrinkwrap\.json|yarn\.lock|pnpm-lock\.yaml|"
        r"requirements.*\.txt|pyproject\.toml|poetry\.lock|Pipfile(\.lock)?|"
        r"Gemfile(\.lock)?|go\.(mod|sum)|Cargo\.(toml|lock)|pom\.xml|"
        r"build\.gradle(\.kts)?|composer\.(json|lock)|mix\.(exs|lock))$", re.I
    ),
    "containers": re.compile(r"^(Dockerfile|Containerfile)(\..*)?$", re.I),
    "terraform/iac": re.compile(r".*\.(tf|tfvars|hcl)$", re.I),
    "kubernetes": re.compile(r".*\.(ya?ml)$", re.I),
    "environment/secrets config": re.compile(r"^(\.env.*|.*secret.*|.*credential.*|.*keys?.*)$", re.I),
}

# Deliberately broad indicators. They identify review surfaces, not confirmed bugs.
RULES = [
    ("auth/session", re.compile(
        r"\b(authenticate|authorization|authorize|login|logout|session|jwt|oauth|oidc|saml|"
        r"password|passcode|mfa|totp|refresh[_-]?token|access[_-]?token)\b", re.I)),
    ("authorization/tenant", re.compile(
        r"\b(permission|role|admin|owner(ship)?|tenant[_-]?id|organization[_-]?id|org[_-]?id|"
        r"rbac|acl|policy|is_admin|can_access|can_edit|can_delete)\b", re.I)),
    ("sql/query", re.compile(
        r"\b(execute|executemany|rawQuery|raw_query|createQuery|queryRaw|execRaw|"
        r"SELECT\s+.+\s+FROM|INSERT\s+INTO|UPDATE\s+.+\s+SET|DELETE\s+FROM)\b", re.I)),
    ("command/code execution", re.compile(
        r"\b(eval|exec|system|popen|spawn|execFile|subprocess|ProcessBuilder|Runtime\.getRuntime|"
        r"child_process|shell\s*=\s*True|os\.command|Command::new)\b", re.I)),
    ("deserialization/parser", re.compile(
        r"\b(pickle\.loads?|yaml\.load|ObjectInputStream|unserialize|Marshal\.load|"
        r"BinaryFormatter|from_yaml|XMLDecoder|DocumentBuilderFactory|SAXParserFactory)\b", re.I)),
    ("outbound network/ssrf", re.compile(
        r"\b(requests\.(get|post|put|delete|request)|httpx\.|urllib\.request|fetch\(|axios\.|"
        r"http\.Get|http\.NewRequest|URLSession|HttpClient|RestTemplate|WebClient|curl\b|wget\b|"
        r"webhook|callback[_-]?url|proxy[_-]?url)\b", re.I)),
    ("file/path/archive", re.compile(
        r"(?:\bopen\s*\(|\breadFile\b|\bwriteFile\b|\bcreateReadStream\b|\bcreateWriteStream\b|"
        r"\bsendFile\b|\bsend_file\b|\bPath\s*\(|\bfilepath\.|\bos\.path\.|\bZipFile\b|"
        r"\bTarFile\b|\btarfile\b|\bzipfile\b|\bextractall\b|\bunzip\b|\bupload\b|\bmultipart\b)", re.I)),
    ("crypto/secrets", re.compile(
        r"\b(secret|api[_-]?key|private[_-]?key|client[_-]?secret|password|passwd|token|"
        r"encrypt|decrypt|cipher|hmac|sha1|md5|bcrypt|argon2|scrypt|pbkdf2|random|rand\(|"
        r"verify_ssl|rejectUnauthorized|InsecureSkipVerify|CERT_NONE)\b", re.I)),
    ("logging/audit", re.compile(
        r"\b(log(ger|ging)?|audit|security[_-]?event|trace|telemetry|alert|sentry|datadog|splunk)\b", re.I)),
    ("resource limits/retries", re.compile(
        r"\b(rate[_-]?limit|quota|timeout|retry|retries|backoff|concurrency|semaphore|queue|"
        r"max[_-]?(size|length|bytes|requests|connections|workers)|circuit[_-]?breaker)\b", re.I)),
    ("high-impact operations", re.compile(
        r"\b(delete|destroy|purge|drop|truncate|revoke|rotate|deploy|publish|release|refund|"
        r"transfer|withdraw|permission|grant|impersonat|sudo|wipe|reset[_-]?(all|account|database))\b", re.I)),
    ("native/unsafe memory", re.compile(
        r"\b(unsafe\s*\{|memcpy|memmove|strcpy|strcat|sprintf|gets\(|malloc\(|free\(|"
        r"extern\s+\"C\"|ffi|cgo|unsafe\.Pointer)\b", re.I)),
]

CI_PATH_MARKERS = (
    ".github/workflows/", ".gitlab-ci.yml", ".circleci/", "Jenkinsfile",
    "azure-pipelines", "bitbucket-pipelines", ".buildkite/",
)

IAC_PATH_MARKERS = (
    "terraform", "k8s", "kubernetes", "helm", "charts", "deploy", "deployment",
    "infrastructure", "infra", "docker-compose", "compose.yml", "compose.yaml",
)

@dataclass
class Match:
    rule: str
    path: str
    line: int
    snippet: str


def is_skipped(path: Path) -> bool:
    return any(part in SKIP_DIRS for part in path.parts)


def is_candidate_file(path: Path) -> bool:
    name = path.name
    if name in SPECIAL_FILENAMES:
        return True
    if path.suffix.lower() in TEXT_EXTENSIONS:
        return True
    if name.startswith(".env"):
        return True
    if any(marker.lower() in path.as_posix().lower() for marker in CI_PATH_MARKERS):
        return True
    return False


def iter_files(root: Path) -> Iterable[Path]:
    for current_root, dirs, files in os.walk(root):
        current = Path(current_root)
        dirs[:] = [d for d in dirs if d not in SKIP_DIRS]
        for name in files:
            path = current / name
            if is_skipped(path) or not is_candidate_file(path):
                continue
            try:
                if path.stat().st_size > MAX_FILE_BYTES:
                    continue
            except OSError:
                continue
            yield path


def read_text(path: Path) -> str | None:
    try:
        data = path.read_bytes()
    except OSError:
        return None
    if b"\x00" in data[:4096]:
        return None
    try:
        return data.decode("utf-8")
    except UnicodeDecodeError:
        return data.decode("utf-8", errors="replace")


def sanitize_snippet(line: str) -> str:
    text = line.strip()
    # Avoid printing likely credential values from assignments while keeping context.
    text = re.sub(
        r"(?i)(secret|password|passwd|api[_-]?key|private[_-]?key|client[_-]?secret|token)\s*[:=]\s*[^,;\s]+",
        r"\1=<redacted>",
        text,
    )
    return text[:220]


def classify_files(root: Path, files: list[Path]) -> dict[str, list[str]]:
    out: dict[str, list[str]] = defaultdict(list)
    for path in files:
        rel = path.relative_to(root).as_posix()
        name = path.name
        for category, rx in FILE_CATEGORIES.items():
            if rx.match(name):
                out[category].append(rel)
        low = rel.lower()
        if any(marker.lower() in low for marker in CI_PATH_MARKERS):
            out["ci/cd workflows"].append(rel)
        if any(marker in low for marker in IAC_PATH_MARKERS):
            out["deployment/iac paths"].append(rel)
    return {k: sorted(set(v)) for k, v in sorted(out.items())}


def scan(root: Path) -> dict:
    files = list(iter_files(root))
    matches: list[Match] = []
    counts = Counter()

    for path in files:
        text = read_text(path)
        if text is None:
            continue
        rel = path.relative_to(root).as_posix()
        for line_no, line in enumerate(text.splitlines(), 1):
            for rule, rx in RULES:
                if counts[rule] >= MAX_MATCHES_PER_RULE:
                    continue
                if rx.search(line):
                    counts[rule] += 1
                    matches.append(Match(rule, rel, line_no, sanitize_snippet(line)))

    by_rule: dict[str, list[dict]] = defaultdict(list)
    for m in matches:
        by_rule[m.rule].append(asdict(m))

    extension_counts = Counter((p.suffix.lower() or p.name) for p in files)
    return {
        "root": str(root),
        "files_scanned": len(files),
        "file_type_counts": dict(extension_counts.most_common(20)),
        "security_relevant_files": classify_files(root, files),
        "match_counts": dict(sorted(counts.items())),
        "matches": dict(sorted(by_rule.items())),
        "disclaimer": "Discovery leads only. Manually verify each match before reporting a security finding.",
    }


def print_text(result: dict) -> None:
    print("Security Surface Inventory")
    print("==========================")
    print(f"Root: {result['root']}")
    print(f"Files scanned: {result['files_scanned']}")
    print("\nRelevant files")
    print("--------------")
    relevant = result["security_relevant_files"]
    if not relevant:
        print("(none identified by filename/path heuristics)")
    for category, paths in relevant.items():
        print(f"\n[{category}]")
        for path in paths[:60]:
            print(f"  - {path}")
        if len(paths) > 60:
            print(f"  ... {len(paths) - 60} more")

    print("\nPattern leads")
    print("-------------")
    matches = result["matches"]
    if not matches:
        print("(none)")
    for rule, items in matches.items():
        print(f"\n[{rule}] {len(items)} match(es)")
        for item in items[:30]:
            print(f"  {item['path']}:{item['line']}: {item['snippet']}")
        if len(items) > 30:
            print(f"  ... {len(items) - 30} more")

    print("\nNOTE: Matches are discovery leads, not vulnerability findings. Manually verify them.")


def main() -> int:
    parser = argparse.ArgumentParser(description="Read-only security surface inventory for a source repository")
    parser.add_argument("root", nargs="?", default=".", help="repository root (default: current directory)")
    parser.add_argument("--json", action="store_true", help="emit JSON instead of human-readable text")
    args = parser.parse_args()

    root = Path(args.root).expanduser().resolve()
    if not root.exists() or not root.is_dir():
        print(f"error: not a directory: {root}", file=sys.stderr)
        return 2

    result = scan(root)
    if args.json:
        print(json.dumps(result, indent=2, sort_keys=True))
    else:
        print_text(result)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
