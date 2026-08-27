# GovernmentJobs.com / NEOGOV Endpoint Notes

Session-verified details for monitoring GovernmentJobs.com career portals (powered by NEOGOV).

## No public RSS or API

Probed and rejected (all fail):
- `/careers/<agency>/rss`, `/careers/<agency>.rss`, `/rss?agency=<agency>` → 404 or redirect to NotFound
- `/careers/<agency>/jobs.json`, `/jobs?page=1` with Accept JSON → 404/500 HTML error page
- Legacy `agency.governmentjobs.com/<agency>/default.cfm` → 301 redirects to the modern `/careers/<agency>` page
- `robots.txt`: allows only major search bots; `User-agent: * Disallow: /`
- Known XHR names like `/careers/Home/GetJobs`, `/home/loadJobs`, `/careers/Home/SearchByKeyword` → 302 to /Error/NotFound or empty responses

## How the site actually loads jobs

The careers pages are Knockout.js SPAs. The job list is fetched via **XHR returning rendered HTML fragments** (not JSON):

1. Fetch any page JS bundle referenced by the target page (`/bundles/scripts/AgencyPages/search?v=...`).
2. Grep the bundle for `ajaxGet(` calls and URL-building constants.
3. The key constant: `var SEARCH_AGENCY_JOBS_URL = AgencyPages.routePrefix + '/home/index';` where `routePrefix: /careers`.

### Working endpoints (verified 2026-08)

**Agency portal (per-state/per-org listings):**
```
GET https://www.governmentjobs.com/careers/home/index?agency=<agency>&page=N
Headers: X-Requested-With: XMLHttpRequest
         Referer: https://www.governmentjobs.com/careers/<agency>
```
- Returns HTML fragment with ~10 jobs/page, newest first (PostingDate desc default)
- `<agency>` is the slug from the portal URL, e.g. `colorado` from `/careers/colorado`

**National cross-agency search (~3,000 agencies):**
```
GET https://www.governmentjobs.com/jobs?location=Denver%2C+CO&keyword=<kw>&page=1
Headers: same as above; Referer: https://www.governmentjobs.com/jobs
```
- One keyword per query — run multiple searches for multiple terms and dedupe
- Response includes total count in text: `N jobs found. Page 1. Showing items 1 - 10`
- Cookies from first visiting the page normally help; use a requests.Session

## Response formats (two distinct layouts)

### Agency portal format
```html
<h3 class="job-item-link-container">
  <a aria-label="..." class="item-details-link"
     href="/careers/colorado/jobs/5439842/highway-maintenance-specialist...">Title</a>
</h3>
<ul class="list-meta">
  <li>Denver Metro, CO</li>                          <!-- location -->
  <li>Full Time <span>-</span> $59,460.00 - $95,124.00 Annually</li>
  <li>Department: Department of Natural Resources</li>
</ul>
<div class="list-entry">description...</div>
```
Parse: `<h3[^>]*>` (has a class — bare `<h3>` fails), then `<ul class="list-meta">(.*?)</ul>` as tail; first `<li>` = location, `Department:` = org.

### National search format
```html
<li class="job-item" data-job-id="5428950-0" data-job-isfeatured="False" role="presentation">
  ...
  <a class="job-details-link" href="/jobs/5428950-0/public-health-promotions-manager">Title</a>
  ...
  <div class="primaryInfo job-organization">City and County of Broomfield</div>
  <div class="primaryInfo"><span class="job-location">Health &amp; Human Services, CO</span></div>
  <div class="primaryInfo">FT Exempt | $112,278.40 - $151,923.20 Annually | Closes in 1 day</div>
</li>
```

## Regex lessons learned (cost several debug iterations)

1. **Backreference inside its own capture group is an error.** `(data-job-id="(\d+-\d+)".*?href="/jobs/\2/...")` raises `cannot refer to an open group at position N`. Capture the numeric id separately and backreference that: `data-job-id="(\d+)-\d+".*?href="/jobs/\1-`.
2. **Even with a valid backref, a single global finditer over the whole document mis-pairs entries** (greedy `.*?` across entry boundaries matches the wrong id). Robust approach: `re.split(r'(?=<li class="job-item")', html)` then `re.match` each block against an anchored per-entry pattern.
3. **Tag assumptions must be verified against raw HTML.** The agency format's `<h3>` carries `class="job-item-link-container"`; requiring literal `<h3>` matched 0 of 10 entries. Always dump a sample entry (`html[idxs[0]:idxs[1]]`) before finalizing patterns.
4. Test iteratively: fetch real HTML, count matches at each stage (`data-job-id` count → piecewise regex counts → full match count) to isolate which part fails.
