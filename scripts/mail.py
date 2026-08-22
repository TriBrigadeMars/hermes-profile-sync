#!/usr/bin/env python3
"""
Hermes Email Sender — Gmail SMTP via smtplib
Usage:
  python mail.py --to recipient@example.com --subject "Subject" --body "Body text" [--attach /path/to/file]
  python mail.py --to recipient@example.com --subject "Subject" --body-file /path/to/body.txt [--html-file /path/to/body.html] [--attach /path/to/file]
Credentials: set GMAIL_USER and GMAIL_APP_PASSWORD in ~/.hermes/.env
"""
import smtplib
import argparse
import os
import sys
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
from pathlib import Path

HERMES_HOME = os.environ.get("HERMES_HOME", os.path.expanduser("~/.hermes"))
env_path = os.path.join(HERMES_HOME, ".env")

def load_env(path):
    if not os.path.exists(path):
        return
    with open(path) as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith("#") and "=" in line:
                key, val = line.split("=", 1)
                os.environ.setdefault(key.strip(), val.strip())

load_env(env_path)

GMAIL_USER = os.environ.get("GMAIL_USER", "")
GMAIL_APP_PASSWORD = os.environ.get("GMAIL_APP_PASSWORD", "")

def send_email(to, subject, body, html_body=None, attachments=None):
    if not GMAIL_USER or not GMAIL_APP_PASSWORD:
        print("ERROR: GMAIL_USER and/or GMAIL_APP_PASSWORD not set in ~/.hermes/.env", file=sys.stderr)
        sys.exit(1)

    msg = MIMEMultipart("alternative")
    msg["From"] = GMAIL_USER
    msg["To"] = to
    msg["Subject"] = subject
    msg.attach(MIMEText(body, "plain"))
    if html_body:
        msg.attach(MIMEText(html_body, "html"))

    for filepath in (attachments or []):
        p = Path(filepath)
        if not p.exists():
            print(f"WARNING: attachment not found: {filepath}", file=sys.stderr)
            continue
        with open(p, "rb") as f:
            part = MIMEBase("application", "octet-stream")
            part.set_payload(f.read())
            encoders.encode_base64(part)
            part.add_header("Content-Disposition", f'attachment; filename="{p.name}"')
            msg.attach(part)

    try:
        with smtplib.SMTP("smtp.gmail.com", 587) as server:
            server.starttls()
            server.login(GMAIL_USER, GMAIL_APP_PASSWORD)
            server.send_message(msg)
        print(f"OK: email sent to {to} — subject: {subject}")
        return True
    except Exception as e:
        print(f"ERROR: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--to", required=True)
    parser.add_argument("--subject", required=True)
    parser.add_argument("--body", default=None, help="Plain text body (inline)")
    parser.add_argument("--body-file", default=None, help="Plain text body from file")
    parser.add_argument("--html-file", default=None, help="HTML body from file")
    parser.add_argument("--attach", nargs="*", default=[])
    args = parser.parse_args()

    body = args.body
    if args.body_file:
        with open(args.body_file, encoding="utf-8") as f:
            body = f.read()
    if not body:
        print("ERROR: need --body or --body-file", file=sys.stderr)
        sys.exit(1)

    html = None
    if args.html_file:
        with open(args.html_file, encoding="utf-8") as f:
            html = f.read()

    send_email(args.to, args.subject, body, html, args.attach)
