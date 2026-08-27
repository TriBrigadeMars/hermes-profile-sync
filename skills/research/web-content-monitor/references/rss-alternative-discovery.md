# Sitemap Discovery Case Studies

## Case Study 1: Bandana.com

### Discovery chain
1. `https://bandana.com/sitemap.xml` → 404
2. `curl https://bandana.com/robots.txt | grep Sitemap` → `Sitemap: https://bandana.com/sitemaps/jobs/index.xml`
3. Sitemap index lists 256 sub-sitemaps: `/sitemaps/jobs/1.xml` through `/sitemaps/jobs/256.xml`
4. Each sub-sitemap contains job URLs in `/jobs/{uuid}` format
5. Job titles extracted by fetching each job page's `<title>` tag

### Key code pattern
```python
robots_resp = requests.get("https://bandana.com/robots.txt")
sitemap_index = re.search(r'Sitemap:\s*(https://bandana\.com/sitemaps/jobs/index\.xml)', robots_resp.text)
# Parse index → 256 sub-sitemaps → each lists /jobs/{uuid} URLs
# Fetch 20 sub-sitemaps as a representative sample
```

## Case Study 2: Idealist.org

### No RSS feed, but has a sitemap
- `https://www.idealist.org/sitemap-jobs-en-1.xml` — directly lists all English job postings
- Sitemap listed in the main sitemap at `/sitemap.xml`
- Job titles are embedded in URL slugs: `/{hash}-{title-company-location}`

### Key insight
Some sites put their content sitemaps directly accessible without robots.txt discovery.

## Case Study 3: Arena.run

### Dual approach needed
1. **Main site**: RSS feed at `https://arena.run/feed` (WordPress-generated, but appears empty)
2. **Job board**: Separate domain `careers.arena.run` powered by Getro platform
3. Getro sitemap at `https://careers.arena.run/sitemap.xml`

### Key insight
A single company may have multiple "sites" with different data sources. Check both the main domain and any subdomains the site links to.
