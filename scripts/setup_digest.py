#!/usr/bin/env python3
"""
Setup script for Academic Journal Digest on a new machine.
Run: python scripts/setup_digest.py
"""
import subprocess
import sys
import os
import shutil

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
HERMES_HOME = os.environ.get("HERMES_HOME", os.path.expanduser("~/.hermes"))
SCRIPTS_DEST = os.path.join(HERMES_HOME, "scripts")

def main():
    print("=== Academic Journal Digest Setup ===\n")

    # 1. Install feedparser
    print("1. Installing feedparser...")
    subprocess.run([sys.executable, "-m", "pip", "install", "feedparser", "-q"], check=True)
    print("   OK\n")

    # 2. Copy scripts to ~/.hermes/scripts/
    print("2. Copying scripts to Hermes scripts dir...")
    os.makedirs(SCRIPTS_DEST, exist_ok=True)
    for fname in ["academic_digest.py", "mail.py"]:
        src = os.path.join(SCRIPT_DIR, fname)
        dst = os.path.join(SCRIPTS_DEST, fname)
        shutil.copy2(src, dst)
        print(f"   {fname} -> {dst}")

    # 3. Check for Gmail credentials
    env_path = os.path.join(HERMES_HOME, ".env")
    print(f"\n3. Checking Gmail credentials in {env_path}...")
    if os.path.exists(env_path):
        with open(env_path) as f:
            content = f.read()
        if "GMAIL_USER" in content and "GMAIL_APP_PASSWORD" in content:
            print("   OK — Gmail credentials found\n")
        else:
            print("   WARNING: Gmail credentials missing. Add to .env:")
            print("     GMAIL_USER=nalcs.mika@gmail.com")
            print("     GMAIL_APP_PASSWORD=<your-app-password>\n")
    else:
        print(f"   WARNING: {env_path} not found. Create it with Gmail credentials.\n")

    # 4. Test run
    print("4. Test run (dry run)...")
    script = os.path.join(SCRIPTS_DEST, "academic_digest.py")
    result = subprocess.run([sys.executable, script], capture_output=True, text=True, timeout=120)
    print(result.stdout)
    if result.returncode != 0:
        print(f"   ERROR: {result.stderr}")
    else:
        print("   OK — digest sent successfully\n")

    print("=== Setup complete ===")
    print("To set up the cron job, run in Hermes:")
    print('  cronjob create --schedule "0 9 */14 * *" --prompt "Run academic_digest.py"')

if __name__ == "__main__":
    main()
