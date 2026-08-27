#!/usr/bin/env python3
"""
Template: Job Board RSS Monitor

This is a starting template for monitoring job boards without RSS feeds.
Copy it to ~/.hermes/scripts/ and customize for your target site.

Usage:
  1. Copy this file to ~/.hermes/scripts/my_site_jobs_monitor.py
  2. Update SITEMAP_URL, JOB_URL_PATTERN, STATE_FILE_NAME
  3. Adjust the parse_job_title function for your site's URL format
  4. Create a cronjob with: script="my_site_jobs_monitor.py", no_agent=True
"""
import json
import os
import re
import requests
import sys
from datetime import datetime

# === CONFIGURATION - CUSTOMIZE THESE FOR YOUR TARGET SITE ===

STATE_FILE_NAME = "template_jobs_state.json"
SITEMAP_URL = "https://example.com/sitemaps/jobs/index.xml"  # Update this
JOB_URL_PATTERN = r'/jobs/[a-f0-9-]+'  # Regex to match job URLs on your site
MAX_NEW_TO_REPORT = 15  # Cap on how many new jobs to list per run

# === END CONFIGURATION ===

STATE_FILE = os.path.expanduser(f"~/AppData/Local/hermes/scripts/{STATE_FILE_NAME}")
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Language": "en-US,en;q=0.5",
    "Connection": "keep-alive",
}

def load_state():
    """Load previously seen job URLs from state file."""
    if os.path.exists(STATE_FILE):
        try:
            with open(STATE_FILE, 'r') as f:
                return set(json.load(f))
        except (json.JSONDecodeError, IOError):
            return set()
    return set()

def save_state(items):
    """Save current job URLs as baseline for next check."""
    os.makedirs(os.path.dirname(STATE_FILE), exist_ok=True)
    with open(STATE_FILE, 'w') as f:
        json.dump(list(items), f)

def parse_sitemap_urls(sitemap_url):
    """Parse job listing URLs from a sitemap."""
    try:
        resp = requests.get(sitemap_url, headers=HEADERS, timeout=15)
        if resp.status_code != 200:
            return set()
        urls = re.findall(r'<loc>\s*(.*?)\s*</loc>', resp.text, re.IGNORECASE)
        urls = [u.strip() for u in urls if u.strip()]
        return set(urls)
    except Exception:
        return set()

def discover_sitemaps():
    """Discover sub-sitemaps from a sitemap index."""
    try:
        resp = requests.get(SITEMAP_URL, headers=HEADERS, timeout=15)
        if resp.status_code != 200:
            return []

        sub_sitemaps = re.findall(r'<loc>\s*(.*?)\s*</loc>', resp.text, re.IGNORECASE)
        sub_sitemaps = [s.strip() for s in sub_sitemaps if s.strip()]

        # Sort by numeric index if pattern contains numbers
        def sort_key(url):
            m = re.search(r'/(\d+)\.xml', url)
            return int(m.group(1)) if m else 999999
        sub_sitemaps.sort(key=sort_key)
        return sub_sitemaps
    except Exception:
        return []

def sample_sitemaps(sub_sitemaps, max_count=20):
    """Sample sub-sitemaps: first N + periodic from full range."""
    if len(sub_sitemaps) <= max_count:
        return list(range(len(sub_sitemaps)))

    indices = list(range(min(max_count, len(sub_sitemaps))))
    step = max(1, len(sub_sitemaps) // 10)
    for i in range(0, len(sub_sitemaps), step):
        if i not in indices:
            indices.append(i)
    return list(set(indices))[:max_count]

def parse_job_title(url):
    """Extract a readable title from a job URL. Override for your site."""
    # Option A: Parse from slug (for slug-based URLs)
    # match = re.search(r'/jobs/[^-]+-(.+)$', url)
    # return match.group(1).replace('-', ' ').strip() if match else url

    # Option B: Fetch page and extract <title> (for UUID-based URLs)
    try:
        resp = requests.get(url, headers=HEADERS, timeout=10)
        if resp.status_code == 200:
            title_match = re.search(r'<title>([^<]+)', resp.text)
            if title_match:
                title = title_match.group(1).strip()
                # Remove common suffixes
                title = re.sub(r'\s*\|.*$', '', title).strip()
                return title
            # Try og:title
            og_match = re.search(r'property="og:title"\s+content="([^"]+)"', resp.text)
            if og_match:
                return og_match.group(1).strip()
    except Exception:
        pass
    return url

def filter_job_urls(urls):
    """Filter URLs to only job listing pages."""
    pattern = re.compile(JOB_URL_PATTERN, re.IGNORECASE)
    return {u for u in urls if pattern.search(u)}

def main():
    seen_jobs = load_state()

    # Step 1: Discover sitemaps
    sub_sitemaps = discover_sitemaps()

    if not sub_sitemaps:
        # Fallback: try the sitemap URL directly
        all_urls = parse_sitemap_urls(SITEMAP_URL)
    else:
        # Step 2: Sample and parse sub-sitemaps
        indices = sample_sitemaps(sub_sitemaps)
        all_urls = set()
        for idx in indices:
            sitemap_url = sub_sitemaps[idx]
            urls = parse_sitemap_urls(sitemap_url)
            all_urls.update(urls)

    # Step 3: Filter for job URLs
    if all_urls:
        job_urls = filter_job_urls(all_urls)
    else:
        job_urls = set()

    # Step 4: Detect new jobs
    new_job_urls = job_urls - seen_jobs

    if new_job_urls:
        print(f"💼 **New Job Postings** (as of {datetime.now().strftime('%Y-%m-%d %H:%M')})\n")

        count = 0
        for url in sorted(new_job_urls):
            if count >= MAX_NEW_TO_REPORT:
                break
            title = parse_job_title(url)
            print(f"• **{title}**")
            print(f"  🔗 {url}")
            print()
            count += 1

        remaining = len(new_job_urls) - MAX_NEW_TO_REPORT
        if remaining > 0:
            print(f"...and {remaining} more new job postings.")

        print(f"\n📊 Total new postings found: {len(new_job_urls)}")
        print("\n✅ State updated. Next check scheduled.")

        save_state(job_urls)
    else:
        print("no_change")

if __name__ == "__main__":
    main()
