---
name: job-board-rss-monitor
description: "Monitor job boards without RSS feeds via sitemap discovery. Consolidated multi-site support."
version: 1.3.0
author: Hermes Agent
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [Jobs, RSS, Monitoring, Sitemap, Cron, Scraping, Consolidation]
    references: [references/job-board-sitemap-monitoring.md, references/governmentjobs-neogov-endpoints.md]
    scripts: [scripts/job_board_monitor_template.py]
---

# Job Board RSS Monitor

Generate RSS-style job alerts from job boards and career sites that **do not** expose public RSS/Atom feeds. Works with Next.js apps, WordPress job boards, Getro-powered career sites, NEOGOV/GovernmentJobs.com portals, and custom job listing platforms by discovering their sitemap structure (or reverse-engineering their SPA endpoints) and tracking new postings via state files.

## When to Use

- "Notify me of new jobs on Idealist.org"
- "Watch Arena.run for new political campaign jobs"
- "Track Bandana.com job postings daily"
- "Set up job alerts for sites without RSS feeds"
- "Watch GovernmentJobs.com / NEOGOV-powered public-sector portals (state, county, city agencies)"
- Any career/job board whose RSS discovery (`/feed`, `/rss`, `<link rel="alternate">`) returns nothing or an empty channel.
- Monitoring 2+ job boards together (use consolidated script pattern)

Don't use for: sites that already have functioning RSS feeds (use `blogwatcher` instead), or one-off manual job searches (use direct `web_search`/`web_extract`).

## Prerequisites

- `curl` or `requests` (Python) for HTTP fetching
- A writable directory for state files under `~/.hermes/scripts/`
- `cronjob` tool for scheduling recurring checks
- `python3` for running scripts (standard library only)

A reusable template script is provided at `scripts/job_board_monitor_template.py` — copy and customize it for each new job board.

## Consolidated Multi-Source Monitoring

When monitoring 2+ job boards together, prefer one consolidated script over separate scripts per site:

```python
# Each source has its own check function returning a list of new jobs
idealist_jobs = check_idealist()    # sitemap → slug URLs
arena_jobs = check_arena()           # RSS + Getro sitemap → mixed URLs
bandana_jobs = check_bandana()       # robots.txt → sub-sitemaps → UUID URLs

all_new_jobs = idealist_jobs + arena_jobs + bandana_jobs
if all_new_jobs:
    print(format_digest(all_new_jobs))
else:
    print("no_change")
```

Key design: each source maintains its OWN state file (so partial failures don't corrupt all state), but output is merged into a single digest.

## Procedure — Setup (foreground, once)

### 1. Discover the sitemap structure

Not all job boards expose sitemaps the same way. Try these in order:

**Step 1 — Check `robots.txt`:**

```bash
curl -s https://example.com/robots.txt | grep -i sitemap
```

This often reveals hidden sitemap indexes (e.g., `https://bandana.com/sitemaps/jobs/index.xml`).

**Step 2 — Check common sitemap paths:**

```bash
curl -s -o /dev/null -w "%{http_code}" https://example.com/sitemap.xml
curl -s -o /dev/null -w "%{http_code}" https://example.com/sitemap_index.xml
curl -s -o /dev/null -w "%{http_code}" https://example.com/sitemap
```

**Step 3 — If no sitemap, check RSS/Atom feeds:**

```bash
curl -s -L https://example.com/feed | head -5
curl -s -L https://example.com/rss | head -5
```

Also search the homepage HTML:

```bash
curl -s https://example.com/ | grep -oiE '(href|src)="[^"]*(rss|feed|atom)[^"]*"'
```

**Step 4 — For WordPress or Getro-powered sites, check known endpoints:**

- WordPress: `https://example.com/feed/` or `https://subdomain.example.com/feed/`
- Getro: `https://careers.example.com/sitemap.xml` or check the main site for a "careers" link
- Next.js: Check `robots.txt` for sitemap URLs; try `/sitemaps/{type}/index.xml`

**Step 5 — SPA/JS-rendered sites with no feed AND no sitemap:** reverse-engineer the frontend's XHR endpoints. Fetch the page's JS bundles (`src="/bundles/..."`), grep them for `ajaxGet(`/`ajaxPost(` calls and URL-building constants — the real data endpoint is almost always discoverable there. This is how GovernmentJobs.com/NEOGOV works; see `references/governmentjobs-neogov-endpoints.md` for the full worked example including endpoint formats, headers, and regex pitfalls.

### 2. Inspect the URL format

Job URLs fall into three patterns — identify which one the target uses:

| Pattern | Example | Title extraction |
|---|---|---|
| UUID-based | `https://bandana.com/jobs/0696ffdc-ff76-40a6-a906-37742d78232a` | Fetch page HTML → parse `<title>` |
| Slug-based | `https://www.idealist.org/en/nonprofit-job/{hash}-{title-company-location}` | Parse slug after hash prefix |
| Getro-style | `https://careers.arena.run/companies/{id}/jobs/{id}-{title}` | Parse slug after second segment |

SPA endpoints may return rendered HTML fragments rather than JSON — parse the fragment's entry structure directly (see the NEOGOV reference for two real layout examples).

### 3. Create the monitoring script

Write a Python script in `~/.hermes/scripts/` that:

1. Loads state from a JSON file (set of previously seen URLs)
2. Fetches the sitemap(s) and parses URLs using regex
3. Compares current URLs against saved state
4. For new URLs: fetches titles (if UUIDs) and formats as a digest
5. Updates state file
6. Prints digest if new items found, or `no_change` if none (watchdog pattern)

See `references/job-board-sitemap-monitoring.md` for the full template and three real implementations as examples.

**Minimal script skeleton:**

```python
#!/usr/bin/env python3
import json, os, re, requests
from datetime import datetime

STATE_FILE = os.path.expanduser("~/AppData/Local/hermes/scripts/site_jobs_state.json")
SITEMAP_URL = "https://example.com/sitemaps/jobs/index.xml"

def load_state():
    if os.path.exists(STATE_FILE):
        with open(STATE_FILE) as f:
            return set(json.load(f))
    return set()

def save_state(items):
    with open(STATE_FILE, 'w') as f:
        json.dump(list(items), f)

# 1. Fetch sitemap index
resp = requests.get(SITEMAP_URL, headers={"User-Agent": "Mozilla/5.0"})
sub_sitemaps = re.findall(r'<loc>\s*(.*?)\s*</loc>', resp.text, re.IGNORECASE)

# 2. Parse sub-sitemaps for job URLs
all_urls = set()
for sm_url in sub_sitemaps:
    sm_resp = requests.get(sm_url.strip(), headers={"User-Agent": "Mozilla/5.0"})
    urls = re.findall(r'<loc>\s*(.*?)\s*</loc>', sm_resp.text, re.IGNORECASE)
    job_urls = [u.strip() for u in urls if '/jobs/' in u]  # Adapt filter per site
    all_urls.update(job_urls)

# 3. Compare against state
seen = load_state()
new = all_urls - seen

# 4. Report or stay silent
if new:
    print(f"New jobs found ({datetime.now()}):\n")
    for url in sorted(new)[:15]:
        print(f"• {url}")
    save_state(all_urls)
else:
    print("no_change")
```

### 4. Create the cron job

```python
cronjob(action="create",
        schedule="0 9 * * *",
        script="consolidated_jobs_monitor.py",
        no_agent=True,
        deliver="telegram")
```

The `no_agent=True` flag means the script runs directly (no LLM). When there are new jobs, the script's stdout is delivered. When it prints `no_change`, nothing is sent (watchdog suppression).

## Procedure — Tick (each scheduled run)

### 1. Fetch and parse sitemaps

For sites with many sub-sitemaps (e.g., 256), sample strategically:

```python
# Check first N sub-sitemaps + periodic sampling across the full range
indices = list(range(min(20, len(sub_sitemaps))))
step = max(1, len(sub_sitemaps) // 10)
for i in range(0, len(sub_sitemaps), step):
    if i not in indices:
        indices.append(i)
```

### 2. Extract job URLs

Filter based on the site's URL pattern:

```python
# UUID-based: https://site.com/jobs/{uuid}
job_urls = [u for u in urls if re.match(r'https?://[^/]+/jobs/[a-f0-9-]+', u)]

# Slug-based: https://site.com/en/{type}/{hash}-{slug}
job_urls = [u for u in urls if '/nonprofit-job/' in u or '/consultant-job/' in u]

# Getro-style: https://careers.site.com/companies/{id}/jobs/{id}-{slug}
job_urls = [u for u in urls if '/companies/' in u and '/jobs/' in u]
```

### 3. Detect new entries and report

```python
new_jobs = current_urls - seen_jobs

if new_jobs:
    for url in list(new_jobs)[:15]:
        title = extract_from_slug(url)  # or fetch_title(url) for UUID sites
        print(f"• **{title}** — {url}")
    save_state(current_urls)
else:
    print("no_change")  # Watchdog pattern: silent when nothing new
```

## Pitfalls

- **Sampling fatigue**: With 256+ sub-sitemaps, checking all on every tick is slow. Sample strategically: first 20 + periodic from the full range.
- **Title extraction for UUID URLs**: UUID-based job URLs (like `bandana.com/jobs/{uuid}`) require fetching the individual page HTML to get the job title. This adds latency — batch or limit title fetches.
- **Sitemap not in robots.txt**: Some sites have sitemaps not declared in `robots.txt`. Try `sitemap.xml`, `sitemap_index.xml`, and `sitemap` directly if the robots.txt search fails.
- **Empty RSS channels**: Some sites have an RSS endpoint that returns a valid channel with zero items. If the feed is empty, look for a separate job board subdomain (common pattern).
- **Rate limiting**: Fetching many sub-sitemaps + individual job pages can trigger rate limits. Add small delays between requests.
- **State file bloat**: State files grow as URLs accumulate. Consider pruning by date if needed, but be careful not to miss reappeared job postings.
- **Site redesigns**: URL patterns and sitemap structures change. Review the script periodically.
- **No-agent mode**: When using `no_agent=True` in cronjob, the script must handle all logic itself. No LLM is available to reason about results.
- **State file contamination**: When testing, always clear state files before re-running. Otherwise the second run shows "no_change" because the first run set the baseline.
- **Bandana URL filtering**: The sitemap contains sub-sitemap URLs AND job listing URLs. Filter for `jobs/{uuid}` pattern BEFORE saving to state, not after — otherwise you save 236K non-job URLs.
- **XML namespace handling in sitemaps**: Many sitemaps (including Idealist.org) use the default namespace `xmlns="http://www.sitemaps.org/schemas/sitemap/0.9"`. When using `xml.etree.ElementTree`, this causes `findall('.//url')` to return empty results because the tag becomes `{http://www.sitemaps.org/schemas/sitemap/0.9}url`. Either strip namespaces from tags, or use the namespace prefix in findall (e.g., `findall('.//{namespace}url')`). **Always check for namespaces when a sitemap returns 0 URLs despite valid XML.**
- **RSS/Atom validation**: Not all RSS feeds start with `<?xml` — some valid feeds begin directly with `<rss>` or `<feed>`. Checking only for `<?xml` causes valid feeds to be rejected. Always also check for `<rss` and `<feed` at the start of the response. This particularly affects Al Jazeera's feed which starts with `<rss version="2.0"`.
- **Next.js sites with no RSS**: Some modern sites (like SF Chronicle) have migrated to Next.js and removed all RSS feeds, returning 404 for `/feed`, `/rss`, etc. Their sitemap may be a `sitemapindex` pointing to numbered sub-sitemaps (e.g., `/sitemap/16140000-16145000.xml`). Parse the sitemap index first, then fetch individual sub-sitemaps. If a site has no working RSS or sitemap, exclude it rather than leaving a broken feed in the rotation.
- **SPA reverse-engineering regex traps** (NEOGOV case): (1) a regex backreference cannot refer to a group opened inside the same match attempt — capture ids separately; (2) a global `finditer` with `.*?` across entry boundaries mis-pairs ids — split the document on entry boundaries and match each block individually; (3) verify tag assumptions against raw HTML dumps (e.g. `<h3 class="...">` vs bare `<h3>`) before finalizing patterns.

## Verification

- [ ] Script runs without errors and finds the sitemap structure
- [ ] State file is created/updated after each run
- [ ] New jobs detected on first run, `no_change` on subsequent runs until new jobs appear
- [ ] Title extraction works correctly for the site's URL format
- [ ] Cron job fires on schedule and delivers results to the intended destination
- [ ] `no_change` output suppresses delivery (watchdog pattern working)
- [ ] Consolidated script handles partial failures gracefully (one source down doesn't block others)

## URL Pattern Quick Reference

| Site | Sitemap URL | Job URL Pattern | Title Source |
|---|---|---|---|
| Idealist.org | `sitemap-jobs-en-1.xml` | `/en/{type}/{hash}-{slug}` | Parse slug |
| Arena.run careers | Getro platform | `/companies/{id}/jobs/{id}-{slug}` | Parse slug |
| Bandana.com | `/sitemaps/jobs/index.xml` → `jobs/{N}.xml` | `/jobs/{uuid}` | Fetch page HTML |
| GovernmentJobs.com | No sitemap/RSS — SPA XHR endpoints | `/careers/{agency}/jobs/{id}/{slug}` or `/jobs/{id}-{n}/{slug}` | Parse HTML fragment (see reference) |