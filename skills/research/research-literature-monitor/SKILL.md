---
name: research-literature-monitor
description: "Monitor academic literature feeds (PubMed, Crossref, RSS)."
version: 1.0.0
author: Hermes Agent
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [research, literature, pubmed, crossref, rss, monitoring, cron, email-digest, academic]
    references: [references/literature-sources.md]
---

# Research Literature Monitor

Build automated feeds that alert you to newly published research from academic
journals, preprint servers, and literature databases. Unlike generic RSS
monitoring, literature sources frequently fragment across several access
mechanisms (native RSS, Crossref API, NCBI E-utilities, per-journal sitemaps),
so a working feed usually blends 2–3 of them depending on whether each
publisher blocks scripts.

## When to Use

- "Set up an RSS feed of academic journals" / "tell me about new public-health papers"
- Monitor a named journal or ISSN across publishers (WHO Bulletin, Lancet Global
  Health, BMJ Global Health, SAGE Open, MDPI IJERPH, Frontiers, Globalization & Health)
- Track recent literature matching topic keywords (e.g., Title IX, health equity,
  epidemiology, LGBTQ health) via PubMed.
- Adding a research feed to a job-hunting / news-digest email pipeline.

Don't use for: general web content or job boards (see `job-board-rss-monitor`,
`web-content-monitor`), or one-off paper lookups (use `arxiv` / direct search).

## Key Design Principles

- **Dedupe on a stable identifier** (PMID for PubMed, DOI for Crossref, URL for
  RSS) stored in a state JSON file; only new identifiers trigger an email.
- **Prefer a native RSS feed when accessible**, but be ready to fall back to an
  API when the publisher blocks requests (SAGE `journals.sagepub.com`, MDPI
  `www.mdpi.com`, Elsevier `thelancet.com` all sit behind Cloudflare and return
  403/HTML challenge instead of XML — do NOT waste time trying to beat it).
- **Email delivery via Gmail SMTP** (`smtplib`, port 587, STARTTLS, App Password).
  Send both an HTML body and a plain-text fallback.
- **Schedule with `cronjob`** using `no_agent=True` so the script runs standalone.

## Procedure — deciding the access method per journal

For each target journal, determine which source works (see
`references/literature-sources.md` for the ISSN table and exact URLs):

1. **Try the direct RSS feed** first. Confirm it returns XML by checking the body
   start for `<?xml` OR `<rss` OR `<feed` — many valid feeds (e.g. Al Jazeera)
   start with `<rss version="2.0">`, not `<?xml`. Check `Content-Type` contains
   `xml`/`rss`/`atom`.
2. **If blocked (403 / Cloudflare challenge / HTML back)**, use the **Crossref
   API** by ISSN:
   ```
   https://api.crossref.org/journals/{ISSN}/works?rows=N&filter=from-pub-date:YYYY-01-01
   ```
   Fields: `items[].title`, `.URL` (doi.org), `.link[]` (choose text/html or pdf),
   `.issued.date-parts`, `.abstract`.
   Find an ISSN via the works-query endpoint if unknown:
   ```
   https://api.crossref.org/works?query.bibliographic={journal name}&rows=1
   ```
   (read `ISSN` from the item; note the item structure varies — guard `.title`
   and `.URL` access).
3. **For PubMed topic feeds**, use NCBI E-utilities (see pitfall below for the
   date filter). `esearch` for PMIDs → `esummary` for details.

## Procedure — PubMed E-utilities feed

```
esearch:   https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi
           db=pubmed, term=<query> AND "<last 30 days>"[dp],
           retmode=json, retmax=N, sort=pub_date   → idlist (PMIDs)
esummary:  https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esummary.fcgi
           db=pubmed, id=<comma-separated PMIDs>, retmode=json → result keyed by PMID
```

Build article URL as `https://pubmed.ncbi.nlm.nih.gov/{pmid}/`. Send a
`User-Agent` with a contact email (NCBI requires an honest UA / contact).

Dedupe on **PMID** in the state file, not the URL.

## Pitfalls

- **PubMed relative-date filter MUST be quoted**: `"last 30 days"[dp]` returns
  results; `30 DAYS[dp]` (unquoted) silently returns **0**. This is the #1 cause
  of "found 0 articles" with an otherwise-valid query. Symptom: the same query
  without the date filter returns thousands of hits.
- **RSS validation**: don't require `<?xml`; accept `<rss` and `<feed` too.
- **Crossref item shape varies**: `.title` is a list, `.URL` is a string, and an
  item can be a dict with different keys per publisher. Wrap every field access
  in try/except so one malformed item doesn't kill the whole journal.
- **Cloudflare-protected publishers cannot be RSS-scraped reliably**: use the
  Crossref fallback rather than retrying HTTP with different headers. If even
  Crossref is unavailable, exclude the journal rather than leaving a broken feed.
- **`requests` may be absent from the cron/script Python** on a fresh box: install
  it once (`python3 -m pip install requests`) before both testing and scheduling;
  a previously working cron job that starts erroring after the interpreter changes
  is usually this, not a logic bug.
- **Environment/quota notes**: NCBI E-utilities rate-limits ~3 req/s without an
  API key — fine for one feed a day; batch PMID lookups into a single esummary.
- **Clear state files before a re-test** or the second run reports "no new items"
  because the first run set the baseline.

## Verification

- [ ] Each journal/source returns items (nonzero count) on first run
- [ ] State file created after first run; subsequent runs only report new IDs
- [ ] Email delivers with HTML + plain-text fallback
- [ ] cronjob created with `no_agent=True` and a sensible cadence
- [ ] Blocked publisher falls back to Crossref (check with `curl -sI` if unsure)

## Support Files

- `references/literature-sources.md` — working source map: ISSNs, publisher
  access methods, and exact feed/API URLs verified for a health-&social-science
  journal set.
- `scripts/research_monitor_template.py` — copy-and-customize Python feed that
  supports native RSS + Crossref-by-ISSN + PubMed E-utilities, with state-file
  dedup and Gmail SMTP delivery baked in.
