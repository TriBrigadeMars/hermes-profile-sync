#!/usr/bin/env python3
"""
Academic Journals Digest — Biweekly Email
Fetches recent articles from ~14 OA journals (global, de-emphasize US/CA).
Generates email body in grouped-by-journal format with clickable links.
Sends via mail.py to nalcs.mika@gmail.com.
"""
import feedparser
import subprocess
import sys
import os
import re
from datetime import datetime

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
RECIPIENT = "nalcs.mika@gmail.com"

JOURNALS = [
    # Public Health (global, Asia/Europe preferred)
    ("Lancet Global Health", "https://www.thelancet.com/rssfeed/lanplh_current.xml", "Global"),
    ("Lancet Public Health", "https://www.thelancet.com/rssfeed/lanpub_current.xml", "Global"),
    ("Lancet Regional Health — Western Pacific", "https://www.thelancet.com/rssfeed/lanwpc_current.xml", "Asia-Pacific"),
    ("Lancet Digital Health", "https://www.thelancet.com/rssfeed/landig_current.xml", "Global"),
    ("BMJ Global Health", "https://gh.bmj.com/rss/current.xml", "Global"),
    ("Annals, Academy of Medicine Singapore", "https://www.annals.edu.sg/rss", "Singapore"),
    ("J Formosan Medical Association", "https://rss.sciencedirect.com/publication/science/09296646", "Taiwan"),
    # AI / LLM
    ("Nature Machine Intelligence", "https://www.nature.com/natmachintell.rss", "Global"),
    ("Nature Computational Science", "https://www.nature.com/natcomputsci.rss", "Global"),
    ("Light: Science & Applications", "https://www.nature.com/lsa.rss", "China"),
    # Data Engineering / Multidisciplinary
    ("Nature Communications", "https://www.nature.com/ncomms.rss", "Global"),
    ("Scientific Reports", "https://www.nature.com/srep.rss", "Global"),
    ("Communications Physics", "https://www.nature.com/commsphys.rss", "Global"),
    ("Nature Electronics", "https://www.nature.com/natelectron.rss", "Global"),
]

MAX_PER_JOURNAL = 10


def fetch_all():
    results = {}
    for name, url, region in JOURNALS:
        try:
            d = feedparser.parse(url)
            articles = []
            for entry in d.entries[:MAX_PER_JOURNAL]:
                title = entry.get("title", "").strip()
                link = entry.get("link", "").strip()
                if not title or not link:
                    continue
                pub_date = ""
                for attr in ("published_parsed", "updated_parsed"):
                    t = getattr(entry, attr, None)
                    if t:
                        try:
                            pub_date = datetime(*t[:6]).strftime("%Y-%m-%d")
                        except Exception:
                            pass
                        break
                summary = re.sub(r"<[^>]+>", "", entry.get("summary", entry.get("description", ""))).strip()
                if len(summary) > 300:
                    summary = summary[:297] + "..."
                articles.append({"title": title, "link": link, "date": pub_date, "summary": summary})
            if articles:
                results[name] = {"region": region, "articles": articles}
        except Exception as e:
            print(f"WARN: {name}: {e}", file=sys.stderr)
    return results


def build_digest(results):
    date_str = datetime.now().strftime("%B %d, %Y")
    total = sum(len(r["articles"]) for r in results.values())

    # Plain text
    lines = [
        f"Academic Journals Digest — {date_str} ({total} articles)",
        "=" * 60,
        "Biweekly digest from open-access journals (Asia & Europe preferred)",
        "",
    ]

    # HTML
    h = []
    h.append(f"""<html><head><meta charset="utf-8"><style>
body {{ font-family:Georgia,'Times New Roman',serif; max-width:820px; margin:0 auto; padding:20px; color:#1a1a1a; background:#fff; }}
h1 {{ border-bottom:2px solid #222; padding-bottom:6px; font-size:22px; }}
h2 {{ margin:28px 0 4px; border-bottom:1px solid #ddd; padding-bottom:3px; font-size:16px; color:#222; }}
h2 span {{ color:#777; font-size:12px; font-weight:normal; }}
.art {{ margin:8px 0 12px; padding-left:12px; border-left:3px solid #e0e0e0; }}
.art a {{ color:#0066cc; text-decoration:none; font-size:14px; }}
.art a:hover {{ text-decoration:underline; }}
.art .meta {{ color:#999; font-size:11px; margin:2px 0 0; }}
.art .sum {{ color:#555; font-size:12px; margin:3px 0 0; line-height:1.4; }}
.footer {{ border-top:1px solid #ddd; margin-top:30px; padding-top:8px; color:#999; font-size:11px; }}
</style></head><body>
<h1>Academic Journals Digest — {date_str}</h1>
<p style="color:#666;font-size:13px">Biweekly digest from open-access journals ({total} articles) · Asia &amp; Europe preferred</p>
""")

    for name, data in results.items():
        arts = data["articles"]
        region = data["region"]
        lines.append(f"  {name} ({region}) · {len(arts)} new")
        lines.append("")
        h.append(f'<h2>{name} <span>({region}) · {len(arts)} new</span></h2>')
        for i, a in enumerate(arts, 1):
            d = f" · {a['date']}" if a["date"] else ""
            lines.append(f"    {i}. {a['title']}{d}")
            lines.append(f"       {a['link']}")
            if a["summary"]:
                lines.append(f"       {a['summary'][:200]}")
            lines.append("")
            sum_html = a["summary"][:200].replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;") if a["summary"] else ""
            h.append(f"""<div class="art">
  <a href="{a['link']}">{a['title']}</a>
  <p class="meta">{a['date']}{d}</p>
  {'<p class="sum">' + sum_html + '</p>' if sum_html else ''}
</div>""")
        lines.append("")

    h.append(f'<p class="footer">Total articles: {total} · Generated by Hermes Agent</p></body></html>')
    lines.append(f"Total articles: {total}")
    lines.append("Generated by Hermes Agent")

    return "\n".join(lines), "\n".join(h)


def send(plain, html):
    date_str = datetime.now().strftime("%B %d, %Y")
    total_lines = [l for l in plain.split("\n") if "Total articles:" in l]
    total = total_lines[0] if total_lines else ""
    subject = f"Academic Journals Digest — {date_str} ({total})"

    plain_path = os.path.join(SCRIPT_DIR, "_digest_plain.txt")
    html_path = os.path.join(SCRIPT_DIR, "_digest.html")
    with open(plain_path, "w", encoding="utf-8") as f:
        f.write(plain)
    with open(html_path, "w", encoding="utf-8") as f:
        f.write(html)

    mail_py = os.path.join(SCRIPT_DIR, "mail.py")
    cmd = [sys.executable, mail_py,
           "--to", RECIPIENT,
           "--subject", subject,
           "--body-file", plain_path,
           "--html-file", html_path]
    result = subprocess.run(cmd, capture_output=True, text=True, timeout=60)
    print(result.stdout.strip())
    if result.stderr:
        print(result.stderr.strip(), file=sys.stderr)
    return result.returncode == 0


if __name__ == "__main__":
    print(f"Fetching from {len(JOURNALS)} journals...")
    results = fetch_all()
    print(f"Articles from {len(results)} journals:")
    for name, data in results.items():
        print(f"  {name}: {len(data['articles'])} articles")
    plain, html = build_digest(results)
    ok = send(plain, html)
    if ok:
        print("Digest sent successfully.")
    else:
        print("Digest send FAILED.", file=sys.stderr)
