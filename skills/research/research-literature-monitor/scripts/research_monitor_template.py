#!/usr/bin/env python3
"""
Research Literature Monitor — template.

Sources supported:
  - native RSS        (journal["type"] == "rss", journal["rss_url"])
  - Crossref by ISSN  (journal["type"] == "crossref", journal["issn"])
  - PubMed E-utilities(feed["type"] == "pubmed", feed["query"])

Dedupes on a stable id (RSS/Crossref: URL/DOI; PubMed: PMID) via a JSON state
file, then emails a styled HTML + plain-text digest via Gmail SMTP.

Usage: set SCRIPTS_DIR, SMTP creds, and the JOURNAL/FEED list, then run directly
or wire to cronjob(no_agent=True). Copy & customize per project.
"""
import json
import os
import re
import requests
import smtplib
from datetime import datetime
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from xml.etree import ElementTree as ET

SCRIPTS_DIR = "/c/Users/cruzmars/AppData/Local/hermes/scripts"
STATE_FILE = os.path.join(SCRIPTS_DIR, "research_state.json")

HEADERS = {
    "User-Agent": "Mozilla/5.0 (research-monitor; mailto:you@example.com)",
    "Accept": "application/rss+xml,application/atom+xml,application/xml;q=0.9,*/*;q=0.8",
}

SMTP_HOST, SMTP_PORT = "smtp.gmail.com", 587
SMTP_USER = "you@gmail.com"
SMTP_PASSWORD = os.environ.get("HERMES_GMAIL_PASSWORD", "PUT_YOUR_APP_PASSWORD")
EMAIL_TO = "you@gmail.com"

# A journal can use rss OR crossref. PubMed topic feeds are separate entries.
JOURNALS = [
    {"name": "BMJ Global Health", "type": "rss",
     "rss_url": "https://gh.bmj.com/rss.xml", "max_items": 8},
    {"name": "SAGE Open", "type": "crossref", "issn": "2158-2440",
     "max_items": 8},
    {"name": "Globalization and Health", "type": "crossref", "issn": "1475-9276",
     "max_items": 8},
]

PUBMED_FEEDS = [
    {"name": "Public Health Recent", "max_items": 20,
     "query": '(public health[tiab] OR health equity[tiab] OR Title IX[tiab]) '
              'AND "last 30 days"[dp]'},   # NOTE quoted date filter
]


def load_state():
    if os.path.exists(STATE_FILE):
        try:
            with open(STATE_FILE) as f:
                return json.load(f)
        except (ValueError, OSError):
            return {}
    return {}


def save_state(state):
    os.makedirs(os.path.dirname(STATE_FILE), exist_ok=True)
    with open(STATE_FILE, "w") as f:
        json.dump(state, f, indent=2, default=str)


def send_email(subject, body_html, body_text=None):
    msg = MIMEMultipart("alternative")
    msg["From"], msg["To"], msg["Subject"] = SMTP_USER, EMAIL_TO, subject
    if body_text is None:
        body_text = re.sub(r"<[^>]+>", "", body_html)
    msg.attach(MIMEText(body_text, "plain"))
    msg.attach(MIMEText(body_html, "html"))
    try:
        s = smtplib.SMTP(SMTP_HOST, SMTP_PORT)
        s.starttls(); s.login(SMTP_USER, SMTP_PASSWORD)
        s.sendmail(SMTP_USER, EMAIL_TO, msg.as_string()); s.quit()
        return True
    except Exception as e:
        print(f"Email error: {e}")
        return False


def fetch_rss(rss_url, max_items):
    out = []
    try:
        r = requests.get(rss_url, headers=HEADERS, timeout=20)
        r.raise_for_status()
        txt = r.text.lower()
        if not (txt.startswith("<?xml") or "<rss" in txt[:100] or "<feed" in txt[:100]):
            return out
        root = ET.fromstring(r.text)
        for it in root.findall(".//item"):
            t = it.find("title"); l = it.find("link"); d = it.find("pubDate")
            title = (t.text or "Untitled").strip() if t is not None else "Untitled"
            url = (l.text or "").strip() if l is not None else ""
            date = (d.text or "").strip() if d is not None else ""
            out.append({"title": title, "url": url, "date": date})
            if len(out) >= max_items:
                break
    except Exception as e:
        print(f"RSS error {rss_url}: {e}")
    return out


def fetch_crossref(issn, max_items):
    out = []
    url = f"https://api.crossref.org/journals/{issn}/works"
    try:
        r = requests.get(url, headers=HEADERS, params={
            "rows": max_items, "filter": "from-pub-date:2025-01-01"}, timeout=20)
        r.raise_for_status()
        for it in r.json()["message"]["items"]:
            try:
                title = (it.get("title") or [""])[0]
                link = it.get("URL", "")
                date = ""
                parts = (it.get("issued") or {}).get("date-parts") or []
                if parts:
                    date = "-".join(str(p) for p in parts[0])
                out.append({"title": title, "url": link, "date": date})
            except Exception:
                continue  # one malformed item must not kill the journal
    except Exception as e:
        print(f"Crossref error {issn}: {e}")
    return out


def fetch_pubmed(feed):
    params = {"db": "pubmed", "term": feed["query"], "retmode": "json",
              "retmax": feed["max_items"], "sort": "pub_date"}
    r = requests.get("https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi",
                     headers=HEADERS, params=params, timeout=30)
    pmids = r.json()["esearchresult"]["idlist"]
    if not pmids:
        return []
    es = requests.get("https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esummary.fcgi",
                      headers=HEADERS, params={"db": "pubmed",
                                               "id": ",".join(pmids),
                                               "retmode": "json"}, timeout=30)
    res = es.json()["result"]
    out = []
    for pmid in pmids:
        it = res.get(pmid)
        if not it or "title" not in it:
            continue
        out.append({"id": pmid, "title": re.sub(r"<[^>]+>", "", it["title"]),
                    "url": f"https://pubmed.ncbi.nlm.nih.gov/{pmid}/"})
    return out


def main():
    state = load_state()
    digest = {}

    for j in JOURNALS:
        arts = (fetch_rss(j["rss_url"], j["max_items"]) if j["type"] == "rss"
                else fetch_crossref(j["issn"], j["max_items"]))
        key = f"seen_{j['name']}"
        seen = set(state.get(key, []))
        new = [a for a in arts if a["url"] and a["url"] not in seen]
        state[key] = list(seen.union(a["url"] for a in arts))[-500:]
        digest[j["name"]] = new

    for f in PUBMED_FEEDS:
        arts = fetch_pubmed(f)
        key = f"seen_pm_{f['name']}"
        seen = set(state.get(key, []))
        new = [a for a in arts if a["id"] not in seen]
        state[key] = list(seen.union(a["id"] for a in arts))[-500:]
        digest[f["name"]] = new

    save_state(state)
    total = sum(len(v) for v in digest.values())
    if total == 0:
        print("no_change")
        return

    text = ["📚 Research Digest", f"Total new: {total}", ""]
    for name, arts in digest.items():
        if arts:
            text.append(f"{name} — {len(arts)}")
            for a in arts:
                text.append(f"  • {a['title']}")
                text.append(f"    {a['url']}")
    body = "\n".join(text)
    print(f"Sent to {EMAIL_TO}" if send_email(
        f"📚 Research Digest ({total} new)", "<pre>" + body + "</pre>", body)
        else "Email failed")


if __name__ == "__main__":
    main()
