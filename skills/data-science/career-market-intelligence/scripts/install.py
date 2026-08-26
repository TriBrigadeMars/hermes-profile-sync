#!/usr/bin/env python3
from __future__ import annotations
import argparse, shutil
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]

def main():
    p=argparse.ArgumentParser(description="Install this skill into a Hermes user skills directory")
    p.add_argument("--target",default=str(Path.home()/".hermes"/"skills"/"data-science"/"career-market-intelligence"))
    p.add_argument("--force",action="store_true")
    a=p.parse_args(); target=Path(a.target).expanduser().resolve()
    if target.exists():
        if not a.force: raise SystemExit(f"Target exists: {target}. Use --force to replace it.")
        shutil.rmtree(target)
    ignore=shutil.ignore_patterns("__pycache__","*.pyc","*.db","*.sqlite","*.zip")
    shutil.copytree(ROOT,target,ignore=ignore)
    print(f"Installed to {target}")
    print("Start a new Hermes session so the skill index reloads.")
if __name__=="__main__": main()
