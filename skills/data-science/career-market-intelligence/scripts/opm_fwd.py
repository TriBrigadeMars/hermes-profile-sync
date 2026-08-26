#!/usr/bin/env python3
"""Minimal local adapter for OPM Federal Workforce Data (FWD).

Listing and download use only stdlib. Parquet summary requires pandas+pyarrow.
"""
from __future__ import annotations
import argparse, json, os, sys, urllib.request
from pathlib import Path

BASE="https://data.opm.gov/api/v1/files"
CACHE=Path(os.environ.get("OPM_FWD_CACHE", Path.home()/".cache"/"career-market-intelligence"/"opm-fwd"))


def get_json(url: str):
    req=urllib.request.Request(url,headers={"User-Agent":"career-market-intelligence/0.1"})
    with urllib.request.urlopen(req,timeout=60) as r: return json.load(r)


def listing(dataset: str):
    return get_json(f"{BASE}/{dataset}")


def current_entry(dataset: str, year: int|None=None, month: int|None=None):
    data=listing(dataset)
    items=data if isinstance(data,list) else data.get("files",data.get("data",[]))
    cand=[]
    for x in items:
        y=int(x.get("year",0)); m=int(x.get("month",0))
        if year and y!=year: continue
        if month and m!=month: continue
        if x.get("current") is False: continue
        cand.append(x)
    if not cand: raise SystemExit("No matching current OPM FWD file found")
    cand.sort(key=lambda x:(int(x.get("year",0)),int(x.get("month",0)),int(x.get("version",0))),reverse=True)
    return cand[0]


def cmd_latest(a): print(json.dumps(current_entry(a.dataset),indent=2))

def cmd_download(a):
    e=current_entry(a.dataset,a.year,a.month)
    y=int(e["year"]); m=int(e["month"]); v=int(e["version"])
    CACHE.mkdir(parents=True,exist_ok=True)
    out=Path(a.out).expanduser() if a.out else CACHE/f"{a.dataset}_{y}{m:02d}_v{v}.parquet"
    url=f"{BASE}/{a.dataset}/{y}/{m:02d}/{v}/download"
    req=urllib.request.Request(url,headers={"User-Agent":"career-market-intelligence/0.1"})
    with urllib.request.urlopen(req,timeout=120) as r, out.open("wb") as f:
        while True:
            b=r.read(1024*1024)
            if not b: break
            f.write(b)
    print(out)

def cmd_summary(a):
    try: import pandas as pd
    except ImportError: raise SystemExit("summary requires: python -m pip install pandas pyarrow")
    df=pd.read_parquet(Path(a.input).expanduser())
    print(f"rows={len(df):,} columns={len(df.columns)}")
    cols=[c for c in [a.by,"occupational_series","agency","grade","education_level","duty_station_state"] if c and c in df.columns]
    if a.series and "occupational_series" in df.columns:
        vals={str(x).strip() for x in a.series.split(",")}; df=df[df["occupational_series"].astype(str).isin(vals)]
    if a.by:
        if a.by not in df.columns: raise SystemExit(f"Unknown --by column. Available examples: {', '.join(cols[:10])}")
        if "count" in df.columns:
            out=df.groupby(a.by,dropna=False)["count"].sum().sort_values(ascending=False).head(a.top)
        else: out=df[a.by].value_counts(dropna=False).head(a.top)
        print(out.to_string())
    else:
        print(df.head(a.top).to_string(index=False))

def main():
    p=argparse.ArgumentParser(description="OPM Federal Workforce Data adapter")
    sp=p.add_subparsers(dest="cmd",required=True)
    for name in ("employment","accessions","separations"): pass
    s=sp.add_parser("latest"); s.add_argument("dataset",choices=["employment","accessions","separations"]); s.set_defaults(func=cmd_latest)
    s=sp.add_parser("download"); s.add_argument("dataset",choices=["employment","accessions","separations"]); s.add_argument("--year",type=int); s.add_argument("--month",type=int); s.add_argument("--out"); s.set_defaults(func=cmd_download)
    s=sp.add_parser("summary"); s.add_argument("--input",required=True); s.add_argument("--series"); s.add_argument("--by"); s.add_argument("--top",type=int,default=20); s.set_defaults(func=cmd_summary)
    a=p.parse_args(); a.func(a)
if __name__=="__main__": main()
