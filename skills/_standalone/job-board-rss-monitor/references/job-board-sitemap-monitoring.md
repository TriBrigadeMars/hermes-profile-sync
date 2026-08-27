# Job Board Sitemap Monitoring — Session Notes

## Pattern Discovered: Sitemap Discovery Path

### Bandana.com (Next.js, UUID-based job URLs)
1. `robots.txt` → `Sitemap: https://bandana.com/sitemaps/jobs/index.xml`
2. sitemap index → 256 sub-sitemaps: `jobs/1.xml` through `jobs/256.xml`
3. Each sub-sitemap → job URLs like `https://bandana.com/jobs/{uuid}`
4. Titles must be fetched from individual job pages (UUID URLs have no slug)
5. **Lesson**: Check `robots.txt` first — it's the most reliable way to find hidden sitemap indexes

### Idealist.org (slug-based job URLs)
1. No RSS feed available
2. `https://www.idealist.org/sitemap.xml` → contains links to sub-sitemaps
3. `sitemap-jobs-en-1.xml` → job listing URLs directly
4. URL format: `https://www.idealist.org/en/{type}/{hash}-{title-company-location}`
5. **Lesson**: Sitemap at `/sitemap.xml` links to categorized sub-sitemaps — look for job-specific ones

### Arena.run (WordPress main site + Getro job board)
1. Main site RSS: `https://arena.run/feed` — channel exists but EMPTY (no items)
2. Job board on separate subdomain: `https://careers.arena.run` (Getro platform)
3. Careers sitemap: `https://careers.arena.run/sitemap.xml`
4. Job URL format: `https://careers.arena.run/companies/{id}/jobs/{id}-{title}`
5. **Lesson**: Empty RSS channel often indicates a separate job board subdomain. Follow the "careers" link.

## Common URL Patterns

| Pattern | Filter regex | Title extraction |
|---|---|---|
| UUID-based (`/jobs/{uuid}`) | `/jobs/[a-f0-9-]{36}$` | Fetch page → `<title>` or `og:title` |
| Slug-based (`/type/{hash}-{slug}`) | `/[a-z]+-job/[a-f0-9]+-.+` | Parse slug after hash, split on hyphens |
| Getro-style (`/companies/{id}/jobs/{id}-{slug}`) | `/companies/.*/jobs/.*` | Parse slug after second hyphen group |

## Watchdog Pattern

Scripts use `no_change` as a sentinel output:
```python
if new_jobs:
    print(digest)
    save_state(current_urls)
else:
    print("no_change")  # Suppresses cron delivery
```

## Performance Notes

- Bandana: 256 sub-sitemaps, ~236K total jobs — must sample (first 20 + periodic)
- Idealist: single sitemap, ~2,680 jobs — can check all
- Arena: small RSS feed + Getro sitemap — check both, lightweight

## Scripts Created

1. `idealist_jobs_monitor.py` — sitemap-based, slug URL pattern
2. `arena_jobs_monitor.py` — RSS + Getro sitemap, dual source check
3. `bandana_jobs_monitor.py` — robots.txt → sitemap index → sub-sitemaps, UUID URLs + HTML title fetch

## Cron Jobs Created

| Job ID | Name | Script | Schedule |
|---|---|---|---|
| `8d64da194fb3` | Idealist Job Postings Monitor | `idealist_jobs_monitor.py` | every 2h |
| `8fdfc5d42772` | Arena.run Job Postings Monitor | `arena_jobs_monitor.py` | every 2h |
| `5051a5730331` | Bandana.com Job Postings Monitor | `bandana_jobs_monitor.py` | every 2h |

## Key Technical Details

### State Management
- State files: `~/.hermes/scripts/{site}_jobs_state.json`
- Stored as JSON list (Python set serialized)
- Updated only on successful fetch
- Survives across cron runs

### HTTP Headers
```python
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Language": "en-US,en;q=0.5",
    "Connection": "keep-alive",
}
```

### Regex Patterns for XML Parsing
```python
# Extract URLs from sitemap
urls = re.findall(r'<loc>\s*(.*?)\s*</loc>', resp.text, re.IGNORECASE)

# Extract sub-sitemap URLs from index
sub_sitemaps = re.findall(r'<loc>\s*(.*?)\s*</loc>', resp.text, re.IGNORECASE)

# Check robots.txt for sitemap
sitemap_index = re.search(r'https://[^/]+/sitemaps/[^/]+/index\.xml', robots_text)
```

## XML Namespace Gotchas (ElementTree)

When using `xml.etree.ElementTree` to parse sitemaps, **many publishers use a default XML namespace** (`xmlns="http://www.sitemaps.org/schemas/sitemap/0.9"`). This causes all `findall('.//loc')` calls to silently return empty results.

### The Problem
```python
# Idealist sitemap starts with:
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">

# This returns EMPTY because the namespace changes the tag name:
root.findall('.//loc')  # ❌ Returns []
root.findall('.//url')  # ❌ Returns []
```

### The Fix
```python
from xml.etree import ElementTree as ET

root = ET.fromstring(resp.text)
# Detect namespace from root tag
ns_match = re.match(r'\{([^}]+)\}', root.tag)
ns = ns_match.group(1) if ns_match else ''
ns_prefix = f'{{{ns}}}' if ns else ''

# Now findall works with the namespace prefix:
urls = root.findall(f'.//{ns_prefix}url')  # ✅ Works
for entry in urls:
    loc = entry.find(f'{ns_prefix}loc')
    if loc is not None and loc.text:
        page_url = loc.text.strip()
```

### Alternative: Strip namespaces entirely (simpler)
```python
# If you only need <loc> text, use regex instead:
urls = re.findall(r'<loc>\s*(.*?)\s*</loc>', resp.text, re.IGNORECASE)
```

## RSS/Atom Feed Validation Gotchas

### The Problem
Not all RSS feeds start with `<?xml`. Some valid feeds begin directly with `<rss>` or `<feed>`.

| Feed | Starts with | Issue |
|---|---|---|
| Al Jazeera | `<rss version="2.0">` | `<?xml` check incorrectly rejects |
| Many WordPress feeds | `<?xml ...>` | Works fine |
| Some Atom feeds | `<feed xmlns=...>` | `<?xml` check incorrectly rejects |

### The Fix
```python
# ❌ Too strict — rejects valid feeds
if '<?xml' in resp.text.lower():

# ✅ Robust — accepts all valid feed formats
if '<?xml' in text.lower() or '<rss' in text.lower() or '<feed' in text.lower():
```

## Next.js Sites Without RSS

Modern Next.js sites (like SF Chronicle) may have **no RSS feeds at all** — all paths (`/feed`, `/rss`, `/rss.xml`) return 404 HTML pages. These sites typically have sitemaps as `sitemapindex` files pointing to numbered sub-sitemaps.

### Discovery pattern:
1. Check `robots.txt` for sitemap URLs
2. If sitemap is a `sitemapindex` (has `<sitemap>` not `<url>` entries), parse sub-sieve URLs
3. Fetch individual sub-sitemaps (e.g., `/sitemap/16140000-16145000.xml`)
4. Parse `<url><loc>` entries from sub-sitemaps for article URLs

### When to give up:
If a site has no working RSS feed AND no parseable sitemap, **exclude it** from the monitoring list. Leaving broken feeds causes script errors and wasted network requests on every poll cycle.