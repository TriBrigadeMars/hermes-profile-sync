import subprocess, sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]

def test_launcher_parses():
    cp=subprocess.run([sys.executable,'-m','py_compile',str(ROOT/'scripts'/'gimp_batch.py')],capture_output=True,text=True)
    assert cp.returncode==0, cp.stderr

def test_no_server_in_smoke():
    text=(ROOT/'templates'/'smoke-test.scm').read_text()
    assert 'script-fu-server' not in text
