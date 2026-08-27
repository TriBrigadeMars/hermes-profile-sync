#!/usr/bin/env python3
import argparse, os, shutil, subprocess, sys
from pathlib import Path

def candidates(explicit=''):
    vals=[]
    if explicit: vals.append(explicit)
    for n in ('krita','krita.exe'):
        p=shutil.which(n)
        if p: vals.append(p)
    if sys.platform.startswith('win'):
        vals += [r'C:\Program Files\Krita (x64)\bin\krita.exe', r'C:\Program Files\Krita\bin\krita.exe']
    elif sys.platform=='darwin':
        vals += ['/Applications/krita.app/Contents/MacOS/krita','/Applications/Krita.app/Contents/MacOS/krita']
    else:
        vals += ['/usr/bin/krita','/usr/local/bin/krita']
    seen=[]
    for v in vals:
        if v and v not in seen: seen.append(v)
    return seen

def detect(explicit=''):
    for c in candidates(explicit):
        p=Path(c).expanduser()
        if p.exists(): return str(p)
    raise SystemExit('Krita executable not found. Pass --krita PATH or configure krita.executable.')

def run_cmd(cmd,dry):
    if dry:
        print(repr(cmd)); return 0
    cp=subprocess.run(cmd)
    return cp.returncode

def main():
    ap=argparse.ArgumentParser(description='Privacy-first wrapper for Krita native CLI exports.')
    ap.add_argument('--krita',default=os.environ.get('KRITA_EXE',''))
    sub=ap.add_subparsers(dest='cmd',required=True)
    sub.add_parser('detect')
    e=sub.add_parser('export'); e.add_argument('input'); e.add_argument('output'); e.add_argument('--dry-run',action='store_true')
    s=sub.add_parser('export-sequence'); s.add_argument('input'); s.add_argument('output'); s.add_argument('--dry-run',action='store_true')
    a=ap.parse_args(); exe=detect(a.krita)
    if a.cmd=='detect': print(exe); return
    inp=str(Path(a.input).expanduser().resolve()); out=str(Path(a.output).expanduser().resolve())
    if Path(inp)==Path(out): raise SystemExit('refusing to overwrite input path')
    if a.cmd=='export': cmd=[exe,inp,'--export','--export-filename',out]
    else: cmd=[exe,'--export-sequence','--export-filename',out,inp]
    raise SystemExit(run_cmd(cmd,a.dry_run))
if __name__=='__main__': main()
