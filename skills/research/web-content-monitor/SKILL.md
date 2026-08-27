---
name: web-content-monitor
description: "Monitor websites without RSS feeds via sitemap discovery."
version: 1.0.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [RSS, Monitoring, Sitemaps, Email-Digests, Cron]
---

# Web Content Monitor (No RSS Required)

Monitor websites that lack native RSS/Atom feeds by discovering their sitemap structure and building custom email digests. When a site has no public feed, you can often find structured content via `robots.txt` → sitemap index → sub-sitemaps → item URLs.

## When to Use

- "I want to track new job postings from site X, but they don't have an RSS feed"
- "Monitor a website for new articles/items and email me daily"
- "Track new listings on a site that only has HTML pages"
- "Monitor academic journals for new publications (Crossref API fallback)"

## When to Use — Academic Journals

When monitoring academic journals, try the journal's RSS feed first. If the publisher is behind Cloudflare/WAF protection (SAGE, MDPI, Frontiers), the RSS endpoint will return an HTML challenge page instead of XML. In that case, fall back to the **Crossref REST API** using the journal's ISSN:

```bash
curl "https://api.crossref.org/journals/{ISSN}/works?rows=10&filter=from-pub-date:2025-01-01"
```

Common ISSNs for major journals (verify via Crossref search if unsure):

| Journal | ISSN | Publisher |
|---|---|---|
| Bulletin of the WHO | 0042-9686 | WHO Press |
| The Lancet Global Health | 2214-109X | Elsevier |
| Globalization and Health | 1475-9276 | SpringerOpen |
| BMJ Global Health | 2059-7908 | BMJ |
| SAGE Open | 2158-2440 | SAGE |
| IJERPH | 1660-4601 | MDPI |

For Frontiers journals, use their journal-level RSS:
`https://www.frontiersin.org/journals/{journal-slug}/rss` (e.g., `public-health`, `psychology`, `medicine`).

## Prerequisites

- Python 3 with `requests` library
- Cron job capability (via Hermes `cronjob`)
- SMTP credentials for email delivery (or use Hermes gateway)

## Discovery Workflow

### 1. Check standard RSS endpoints first
Try: `/feed`, `/rss`, `/feed.xml`, `/rss.xml`, `/atom.xml`, `/api/rss`, `/sitemap.xml`

### 2. Discover sitemaps via robots.txt
```bash
curl -s https://example.com/robots.txt | grep -i "Sitemap:"
```

### 3. Parse sitemap index → sub-sitemaps
If the sitemap is an index, parse `<loc>` entries to find numbered sub-sitemaps.

### 4. Extract item URLs
Fetch sub-sitemaps, extract `<loc>` entries, filter for content URLs.

### 5. Extract titles (when URLs are UUIDs)
When item URLs are UUIDs like `/jobs/{uuid}`, fetch the page and extract `<title>` or `og:title`.

## Script Pattern

Create a Python script that:
1. Discovers sitemaps via robots.txt or standard endpoints
2. Parses sub-sitemaps for item URLs
3. Tracks seen URLs in a JSON state file
4. Reports only new items
5. Optionally sends email via SMTP

**For RSS feeds**: First try known feed URLs, then auto-discover from `<link rel="alternate">` tags in the homepage HTML. For journals behind Cloudflare, use Crossref API by ISSN as a fallback.

**Hybrid pattern** (RSS + Crossref API): Define journals with `type: "rss"` or `type: "crossref"` fields — fetch RSS when available, fall back to Crossref API using the journal's ISSN.

## State Management

- Store as JSON list of URL strings in `~/AppData/Local/hermes/scripts/<source>_state.json`
- Always save ALL current URLs (not just new ones) to prevent false positives
- Use full URL as the state key

## Scheduling

```
cronjob(action="create", schedule="0 9 * * *", script="monitor.py", no_agent=True)
```

## Email Delivery

**Direct SMTP**: Use Python `smtplib` in the script. Gmail requires an App Password (https://myaccount.google.com/apppasswords).

**Hermes gateway**: Set `deliver` on the cron job — `telegram`, `discord`, `all`, or `local`.

## Pitfalls

- Rate limits: add `time.sleep(0.5)` between requests
- Pagination: sample first N sub-sitemaps, not all
- HTML entities: use `html.unescape()` on scraped titles
- Don't overwrite last-known-good state with error pages
- Save state after every run (even no-change) to prevent drift
- **RSS validation**: Not all valid RSS feeds start with `<?xml` — some (like Al Jazeera) begin with `<rss version="2.0">`. Checking only for `<?xml` causes valid feeds to be rejected. Always also check for `<rss` and `<feed` at the start of the response.
- Cloudflare/WAF on publishers (SAGE, MDPI, Frontiers): RSS endpoints return 403 with an HTML challenge. Fall back to the **Crossref REST API** with the journal's ISSN instead of retrying the blocked URL.

## References

- `references/rss-alternative-discovery.md` — sitemap discovery case studies
- `references/academic-journal-rss-feeds.md` — RSS feed URLs and Crossref API ISSNs for major journals (SAGE, MDPI, Frontiers, BMJ, Lancet, WHO Bulletin)
- `templates/digest-html-template.html` — reusable HTML email template