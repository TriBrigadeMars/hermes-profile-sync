#!/usr/bin/env python3
"""verify_inventory.py — Guardrail against documented-vs-actual skill drift.

Checks (see AGENTS.md):
  1. Every skill documented in custom-skills-inventory.md has a skills/**/SKILL.md.
  2. Every skills/**/SKILL.md folder is documented in the inventory.
  3. Each SKILL.md front-matter `name:` matches its folder name.
  4. With --local: every skill installed in the local Hermes home is in the
     repo (warns — local-only skills indicate a pending sync).

Exit codes: 0 = pass, 1 = failure. Run before committing inventory changes.
"""

from __future__ import annotations

import os
import re
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
INVENTORY = REPO_ROOT / "custom-skills-inventory.md"
SKILLS_DIR = REPO_ROOT / "skills"

# Inventory table rows look like:  | `skill-name` | Purpose ... |
TABLE_ROW = re.compile(r"^\|\s*`([a-z0-9][a-z0-9_-]*)`\s*\|", re.MULTILINE)


def resolve_hermes_home() -> Path | None:
    """Resolve the Hermes home the same way hermes-sync.sh does."""
    home = os.environ.get("HERMES_HOME")
    if home:
        return Path(home)
    localappdata = os.environ.get("LOCALAPPDATA")
    if localappdata and (Path(localappdata) / "hermes").is_dir():
        return Path(localappdata) / "hermes"
    fallback = Path.home() / ".hermes"
    return fallback if fallback.is_dir() else None


def documented_skills() -> set[str]:
    return set(TABLE_ROW.findall(INVENTORY.read_text(encoding="utf-8")))


def repo_skills() -> dict[str, Path]:
    """Map skill folder name -> SKILL.md path for every skills/**/SKILL.md."""
    found: dict[str, Path] = {}
    for skill_md in sorted(SKILLS_DIR.rglob("SKILL.md")):
        found[skill_md.parent.name] = skill_md
    return found


def front_matter_name(path: Path) -> str | None:
    text = path.read_text(encoding="utf-8", errors="replace")
    match = re.match(r"^---\s*\n(.*?)\n---", text, re.DOTALL)
    if not match:
        return None
    name = re.search(r"^name:\s*([^\s#]+)", match.group(1), re.MULTILINE)
    return name.group(1).strip().strip("'\"") if name else None


def main() -> int:
    failures: list[str] = []
    warnings: list[str] = []

    if not INVENTORY.is_file():
        failures.append(f"Inventory file not found: {INVENTORY}")
        print("\n".join(failures), file=sys.stderr)
        return 1

    docs = documented_skills()
    have = repo_skills()

    # Check 1: documented but no code
    for name in sorted(docs - have.keys()):
        failures.append(f"documented in inventory but no skills/ folder: {name}")

    # Check 2: code but not documented
    for name in sorted(have.keys() - docs):
        failures.append(f"skills/ folder not documented in inventory: {name}")

    # Check 3: SKILL.md front-matter name must match folder name
    for name, path in have.items():
        fm = front_matter_name(path)
        if fm is None:
            failures.append(f"{path}: no front matter / no name field")
        elif fm != name:
            failures.append(f"{path}: front-matter name '{fm}' != folder name '{name}'")

    # Check 4 (warning only): local skills missing from the repo
    if "--local" in sys.argv:
        hermes_home = resolve_hermes_home()
        local_dir = hermes_home / "skills" if hermes_home else None
        if local_dir and local_dir.is_dir():
            local_names = {p.parent.name for p in local_dir.rglob("SKILL.md")}
            only_local = sorted(local_names - docs - set(have.keys()))
            for name in only_local:
                warnings.append(
                    f"installed locally at {local_dir} but absent from repo: {name}"
                )
            if not only_local:
                warnings.append("local installation fully covered by the repo")
        else:
            warnings.append("no local Hermes skills directory found (skipped --local check)")

    print(f"Documented skills: {len(docs)}")
    print(f"Skills in repo:    {len(have)}")

    for w in warnings:
        print(f"WARNING: {w}")
    if failures:
        print("\nFAILED:")
        for f in failures:
            print(f"  - {f}")
        print("\nSee AGENTS.md sections 2-3. Fix the mismatch before committing.")
        return 1

    print("All checks passed.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
