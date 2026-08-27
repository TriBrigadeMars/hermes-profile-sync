#!/usr/bin/env python3
import argparse, os, shutil, subprocess, sys
from pathlib import Path

def candidates(explicit=''):
    vals=[]
    if explicit: vals.append(explicit)
    names=['gimp-console-3.0','gimp-console','gimp-3.0','gimp']
    if sys.platform.startswith('win'):
        names=['gimp-console-3.0.exe','gimp-console.exe','gimp-3.0.exe','gimp.exe']
    for n in names:
        p=shutil.which(n)
        if p: vals.append(p)
    if sys.platform.startswith('win'):
        program_files=[os.environ.get('ProgramFiles'),os.environ.get('ProgramFiles(x86)')]
        for base in filter(None,program_files):
            vals += [str(Path(base)/'GIMP 3'/'bin'/'gimp-console-3.0.exe'),str(Path(base)/'GIMP 3'/'bin'/'gimp-3.0.exe')]
    elif sys.platform=='darwin':
        vals += ['/Applications/GIMP.app/Contents/MacOS/gimp-console','/Applications/GIMP.app/Contents/MacOS/gimp']
    else:
        vals += ['/usr/bin/gimp-console-3.0','/usr/bin/gimp-console','/usr/bin/gimp']
    seen=[]
    for v in vals:
        if v and v not in seen: seen.append(v)
    return seen

def detect(explicit=''):
    for c in candidates(explicit):
        p=Path(c).expanduser()
        if p.exists(): return str(p)
    raise SystemExit('GIMP console executable not found. Pass --gimp PATH or configure gimp.executable.')

def scheme_string(path):
    s=str(Path(path).expanduser().resolve()).replace('\\','/')
    return s.replace('"','\\"')

def main():
    ap=argparse.ArgumentParser(description='Run finite local GIMP 3 Script-Fu batch jobs without a server.')
    ap.add_argument('--gimp',default=os.environ.get('GIMP_EXE',''))
    sub=ap.add_subparsers(dest='cmd',required=True)
    sub.add_parser('detect')
    r=sub.add_parser('run'); r.add_argument('job'); r.add_argument('--dry-run',action='store_true')
    a=ap.parse_args(); exe=detect(a.gimp)
    if a.cmd=='detect': print(exe); return
    job=Path(a.job).expanduser().resolve()
    if not job.is_file(): raise SystemExit(f'job not found: {job}')
    expr=f'(load "{scheme_string(job)}")'
    cmd=[exe,'--batch-interpreter=plug-in-script-fu-eval',f'--batch={expr}']
    if a.dry_run:
        print(repr(cmd)); return
    cp=subprocess.run(cmd)
    raise SystemExit(cp.returncode)
if __name__=='__main__': main()
