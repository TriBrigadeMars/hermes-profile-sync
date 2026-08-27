#!/usr/bin/env python3
import argparse, json, re
from pathlib import Path

TC_RE = re.compile(r"^(\d{2}):(\d{2}):(\d{2}):(\d{2})$")

def tc_to_frames(tc, fps):
    m = TC_RE.match(tc)
    if not m:
        raise ValueError(f"invalid timecode: {tc}")
    h, mnt, s, f = map(int, m.groups())
    if mnt >= 60 or s >= 60 or f >= fps:
        raise ValueError(f"timecode out of range for {fps} fps: {tc}")
    return (((h * 60) + mnt) * 60 + s) * fps + f

def reel_name(value):
    s = re.sub(r"[^A-Za-z0-9_]", "_", str(value).upper())
    return (s or "AX")[:8]

def main():
    ap = argparse.ArgumentParser(description="Build a conservative CMX3600 EDL from JSON.")
    ap.add_argument("plan")
    ap.add_argument("--output", required=True)
    args = ap.parse_args()
    data = json.loads(Path(args.plan).read_text(encoding="utf-8"))
    fps = int(data["fps"])
    if fps not in (24, 25, 30, 50, 60):
        raise SystemExit("fps must be nominal 24, 25, 30, 50, or 60 for this v1 helper")
    events = data.get("events", [])
    if not events:
        raise SystemExit("plan contains no events")
    lines = [f"TITLE: {data.get('title', 'HERMES EDIT')}", "FCM: NON-DROP FRAME", ""]
    last_record_out = None
    for idx, ev in enumerate(events, 1):
        for key in ("source_in", "source_out", "record_in", "record_out"):
            if key not in ev:
                raise SystemExit(f"event {idx} missing {key}")
        si = tc_to_frames(ev["source_in"], fps)
        so = tc_to_frames(ev["source_out"], fps)
        ri = tc_to_frames(ev["record_in"], fps)
        ro = tc_to_frames(ev["record_out"], fps)
        if so <= si or ro <= ri:
            raise SystemExit(f"event {idx} has non-positive duration")
        if (so - si) != (ro - ri):
            raise SystemExit(f"event {idx} source and record durations differ")
        if last_record_out is not None and ri < last_record_out:
            raise SystemExit(f"event {idx} overlaps the prior record event")
        last_record_out = ro
        track = str(ev.get("track", "V"))[:2]
        trans = str(ev.get("transition", "C")).upper()
        if trans != "C":
            raise SystemExit(f"event {idx}: v1 helper only supports cut transition C")
        lines.append(f"{idx:03d}  {reel_name(ev.get('reel', 'AX')):<8} {track:<4} {trans:<3} {ev['source_in']} {ev['source_out']} {ev['record_in']} {ev['record_out']}")
        if ev.get("comment"):
            lines.append(f"* {str(ev['comment']).replace(chr(10), ' ')}")
    Path(args.output).write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"wrote {args.output} ({len(events)} events)")

if __name__ == "__main__":
    main()
