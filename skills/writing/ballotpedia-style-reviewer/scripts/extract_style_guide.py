#!/usr/bin/env python3
"""Extract text from an updated Ballotpedia Style Guide PDF using local pdftotext."""
from __future__ import annotations

import argparse
import shutil
import subprocess
from pathlib import Path


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("pdf", type=Path)
    ap.add_argument("output", type=Path)
    args = ap.parse_args()

    exe = shutil.which("pdftotext")
    if not exe:
        raise SystemExit("pdftotext is not installed; refusing to fall back to OCR automatically")
    if not args.pdf.exists():
        raise SystemExit(f"PDF not found: {args.pdf}")
    args.output.parent.mkdir(parents=True, exist_ok=True)
    subprocess.run([exe, str(args.pdf), str(args.output)], check=True)
    if not args.output.exists() or args.output.stat().st_size < 1000:
        raise SystemExit("Extraction produced little or no text; inspect the PDF manually rather than relying on automatic OCR")
    print(f"Extracted {args.pdf} -> {args.output} ({args.output.stat().st_size} bytes)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
