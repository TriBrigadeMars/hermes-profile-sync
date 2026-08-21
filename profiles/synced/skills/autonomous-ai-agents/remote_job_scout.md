# remote_job_scout

## Overview
Automated agent that continuously monitors academic job boards for remote/adjunct teaching positions in the US, filters for teaching roles, and generates a weekly RSS digest (`remote_adjunct_feed.rss`) with new opportunities.

## Purpose
- Scrape AcademicKeys RSS feed (primary source) and AcademicPositions sitemap (fallback)
- Filter for US-based, remote/adjunct teaching roles
- Aggregate into a clean weekly RSS feed
- Deliver via email (Gmail) and/or desktop notification

## Sources
- **AcademicKeys** – `https://www.academickeys.com/rss` (real RSS 2.0 feed)
- **AcademicPositions** – sitemap at `https://www.academicpositions.com/` (filtered by US + teaching roles)
- **HigherEdJobs** – blocked by bot protection; monitored via browser pass (optional)

## Fields Extracted
- Job title (position name)
- Institution (university/college)
- Department (if specified)
- Location (city/state)
- Type (adjunct, clinical, faculty, etc.)
- Posting date
- Link (direct job URL)
- Description (short summary)

## Schedule
- Daily scrape (midnight UTC)
- Digest generation (Monday 09:00 MST)
- Delivery (email + desktop notification)

## Implementation Notes
- Uses `hermes chat` with `hermes tool` calls to `curl`/`jq` for RSS parsing
- Stores state in `remote_job_scout` profile (isolated memory)
- Outputs `remote_adjunct_feed.rss` to `~/remote_adjunct_feed.rss`
- Integrates with `hermes-profile-sync` for cross-machine profile consistency

## Skill References
- `hermes-agent` (core framework)
- `hermes-profile-sync` (profile management)
- `remote_adjunct_digest.py` (existing generator)
