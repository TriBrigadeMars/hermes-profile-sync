#!/usr/bin/env python3
import argparse, json, shutil, subprocess
from pathlib import Path

VIDEO_EXT={'.mov','.mp4','.mxf','.mkv','.avi','.m4v','.webm','.wav','.mp3','.aac','.flac'}

def iter_files(path):
    p=Path(path)
    if p.is_file(): return [p]
    return sorted(x for x in p.rglob('*') if x.is_file() and x.suffix.lower() in VIDEO_EXT)

def main():
    ap=argparse.ArgumentParser(description='Create a local media manifest using ffprobe.')
    ap.add_argument('path'); ap.add_argument('--output', required=True); ap.add_argument('--ffprobe', default='ffprobe')
    args=ap.parse_args()
    exe=shutil.which(args.ffprobe) if not Path(args.ffprobe).exists() else args.ffprobe
    if not exe: raise SystemExit('ffprobe not found; install FFmpeg or pass --ffprobe PATH')
    result=[]
    for f in iter_files(args.path):
        cp=subprocess.run([str(exe),'-v','error','-show_format','-show_streams','-of','json',str(f)],capture_output=True,text=True)
        if cp.returncode:
            result.append({'path':str(f),'error':cp.stderr.strip()}); continue
        data=json.loads(cp.stdout or '{}')
        result.append({'path':str(f),'probe':data})
    Path(args.output).write_text(json.dumps({'files':result},indent=2),encoding='utf-8')
    print(f'wrote {args.output} ({len(result)} files)')

if __name__=='__main__': main()
