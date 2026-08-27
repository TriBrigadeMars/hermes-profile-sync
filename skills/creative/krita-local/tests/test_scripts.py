import subprocess, sys, tempfile
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]

def test_job_writer():
    with tempfile.TemporaryDirectory() as d:
        out=Path(d)/'job.json'
        cp=subprocess.run([sys.executable,str(ROOT/'scripts'/'krita_job.py'),'--job-file',str(out),'--operation','document_info'],capture_output=True,text=True)
        assert cp.returncode==0 and out.exists()

def test_plugin_parses():
    cp=subprocess.run([sys.executable,'-m','py_compile',str(ROOT/'assets'/'hermes_krita_local'/'plugin.py')],capture_output=True,text=True)
    assert cp.returncode==0, cp.stderr
