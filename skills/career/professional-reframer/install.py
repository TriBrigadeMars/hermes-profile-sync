#!/usr/bin/env python3
from __future__ import annotations

import argparse
import os
import shutil
from pathlib import Path


def main() -> None:
    parser = argparse.ArgumentParser(description="Install professional-reframer for Hermes.")
    parser.add_argument(
        "--dest",
        default=str(Path.home() / ".hermes" / "skills" / "career" / "professional-reframer"),
        help="Installation directory",
    )
    args = parser.parse_args()

    src = Path(__file__).resolve().parent
    dest = Path(os.path.expanduser(args.dest)).resolve()
    dest.parent.mkdir(parents=True, exist_ok=True)
    if dest.exists():
        shutil.rmtree(dest)
    shutil.copytree(src, dest, ignore=shutil.ignore_patterns("__pycache__", ".pytest_cache"))
    print(f"Installed professional-reframer to {dest}")
    print("Start a new Hermes session so the skill index can reload.")


if __name__ == "__main__":
    main()
