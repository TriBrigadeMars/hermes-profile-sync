#!/usr/bin/env python3
import argparse, json
from pathlib import Path

def ts(seconds):
    if seconds < 0:
        raise ValueError("negative timestamp")
    ms = int(round(float(seconds) * 1000))
    h, rem = divmod(ms, 3600000)
    m, rem = divmod(rem, 60000)
    s, ms = divmod(rem, 1000)
    return f"{h:02d}:{m:02d}:{s:02d},{ms:03d}"

def main():
    ap = argparse.ArgumentParser(description="Create SRT from [{start,end,text}, ...] JSON.")
    ap.add_argument("input")
    ap.add_argument("--output", required=True)
    args = ap.parse_args()
    cues = json.loads(Path(args.input).read_text(encoding="utf-8"))
    out=[]; prev=-1.0
    for i, cue in enumerate(cues, 1):
        start=float(cue["start"]); end=float(cue["end"]); text=str(cue["text"]).strip()
        if start < prev:
            raise SystemExit(f"cue {i} starts before the previous cue")
        if end <= start:
            raise SystemExit(f"cue {i} has end <= start")
        if not text:
            raise SystemExit(f"cue {i} has empty text")
        out += [str(i), f"{ts(start)} --> {ts(end)}", text, ""]
        prev=start
    Path(args.output).write_text("\n".join(out), encoding="utf-8")
    print(f"wrote {args.output} ({len(cues)} cues)")

if __name__ == "__main__":
    main()
