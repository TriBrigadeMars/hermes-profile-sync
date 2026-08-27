---
name: rss_feed_monitoring
description: RSS feed monitoring for arXiv, news, and job boards.
---

# RSS Feed Monitoring & Distribution

## Overview
Standard workflow for RSS feed monitoring and email distribution.

## Core Components
- **Academic Journals** – `academic_rss_monitor.py` fetches arXiv feeds (physics, math, CS, stats, bio, eng, chem, envsci)
- **News Digests** – `news_digest.py` aggregates public news feeds
- **Job Boards** – `job_hunting_feed.py` tracks Idealist, Arena, Bandana

## Cron Schedules
- **Academic Journals** – Every 14 days at 07:00 UTC (`91f25fafc626`)
- **News Digest** – Every 7 days at 08:00 UTC (`74f0ddd998d7`)
- **PubMed Research** – Every 14 days at 06:00 UTC (`b14e1619b8b9`)

## Setup
1. Place `academic_rss_monitor.py` in `scripts/`
2. Run once: `hermes gateway run --feed=academic_rss_monitor --format=email --to=nalcs.mika@gmail.com`
3. Add cron: `hermes cron job add --name=91f25fafc626 --command=... --schedule=0 7 * * 1`
4. Test: `hermes cron job run 91f25fafc626`

## Troubleshooting
- Gateway not starting? Run `hermes gateway start`
- Missing cron? Re-add with `hermes cron job add`
- No email? Verify `--to` address and gateway logs
