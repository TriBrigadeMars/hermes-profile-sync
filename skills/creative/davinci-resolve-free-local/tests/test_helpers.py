import json, subprocess, sys, tempfile
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]

def run(script,*args):
    return subprocess.run([sys.executable,str(ROOT/'scripts'/script),*map(str,args)],capture_output=True,text=True)

def test_example_edl():
    with tempfile.TemporaryDirectory() as d:
        out=Path(d)/'x.edl'
        cp=run('cmx3600.py',ROOT/'templates/edit-plan.example.json','--output',out)
        assert cp.returncode==0, cp.stderr
        text=out.read_text()
        assert '001' in text and '002' in text and 'FCM: NON-DROP FRAME' in text

def test_example_srt():
    with tempfile.TemporaryDirectory() as d:
        out=Path(d)/'x.srt'
        cp=run('srt_from_json.py',ROOT/'templates/subtitles.example.json','--output',out)
        assert cp.returncode==0, cp.stderr
        assert '-->' in out.read_text()
