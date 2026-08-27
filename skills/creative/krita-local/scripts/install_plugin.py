#!/usr/bin/env python3
import argparse, os, shutil, sys
from pathlib import Path

def default_target():
    if sys.platform.startswith('win'):
        base=os.environ.get('APPDATA')
        return Path(base)/'krita'/'pykrita' if base else None
    if sys.platform=='darwin': return Path.home()/'Library'/'Application Support'/'krita'/'pykrita'
    return Path.home()/'.local'/'share'/'krita'/'pykrita'

def main():
    ap=argparse.ArgumentParser(description='Install the bundled Hermes Local Jobs Krita plugin.')
    ap.add_argument('--target')
    a=ap.parse_args(); target=Path(a.target).expanduser() if a.target else default_target()
    if target is None: raise SystemExit('could not infer Krita pykrita directory; pass --target PATH')
    src=Path(__file__).resolve().parents[1]/'assets'
    target.mkdir(parents=True,exist_ok=True)
    shutil.copy2(src/'hermes_krita_local.desktop', target/'hermes_krita_local.desktop')
    dst=target/'hermes_krita_local'
    if dst.exists(): shutil.rmtree(dst)
    shutil.copytree(src/'hermes_krita_local',dst)
    print(f'installed plugin into {target}')
    print('Restart Krita and enable Hermes Local Jobs in the Python Plugin Manager.')
if __name__=='__main__': main()
