#!/usr/bin/env python3
"""Install this skill into the user-local Hermes skills directory."""
from __future__ import annotations

import argparse
import shutil
from pathlib import Path


def ignore(_src: str, names: list[str]) -> set[str]:
    return {n for n in names if n in {"__pycache__", ".pytest_cache", ".git", ".DS_Store"} or n.endswith(".pyc")}


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--destination", type=Path, default=Path.home() / ".hermes" / "skills" / "writing" / "ballotpedia-style-reviewer")
    ap.add_argument("--force", action="store_true")
    args = ap.parse_args()

    source = Path(__file__).resolve().parent.parent
    dest = args.destination.expanduser().resolve()
    if dest.exists():
        if not args.force:
            raise SystemExit(f"Destination exists: {dest}\nUse --force to replace it.")
        shutil.rmtree(dest)
    dest.parent.mkdir(parents=True, exist_ok=True)
    shutil.copytree(source, dest, ignore=ignore)
    print(f"Installed Ballotpedia Style Reviewer to {dest}")
    print("Start a new Hermes session so the skill index reloads.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
