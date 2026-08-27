---
name: web-media-download
description: "Use when bulk-downloading images/videos from a webpage URL."
version: 1.0.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [download, scraping, media, curl]
---

# Web Media Download

**When to use:** the user gives one or more webpage URLs and wants the embedded photos/videos saved to a local folder.

Bulk-download photos and videos embedded in a public webpage (galleries, albums) to a folder on the user's machine.

## Workflow

1. Fetch the page HTML with curl using a browser User-Agent:
   `curl -sL -A "Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/126.0" "<url>" -o /tmp/page.html`
2. Extract media URLs, then dedupe and strip thumbnails:
   `grep -oE 'https://[^"]+\.(jpg|jpeg|png|webp|mp4)[^"]*' page.html | sort -u | grep -v thumbs`
3. **Also check lazy-load attributes** — many sites don't put media in plain `src`:
   `grep -oE 'data-src="[^"]+\.(jpg|jpeg|mp4)[^"]*"' page.html`
4. Download each file with a Referer header (hotlink protection is common):
   `curl -s -A "$UA" -e "<page-url>" -o "$file" "$url"`
   Strip query strings (`?v=...`) from filenames; skip files that already exist for resumability.
5. VERIFY before reporting success: check file counts against the extracted link count,
   spot-check with `file <name>` (valid JPEG/MP4), flag any file <10KB as suspicious.

## Pitfalls

- Extension regex must include `.jpeg`, not just `.jpg` — some CDNs mix them (cost one full retry).
- Some sites serve different markup per request; if 0 links extracted, re-fetch and grep for
  `data-src`/`data-[a-z]+=` attributes before concluding the album is empty/private.
- Long batch downloads: run via terminal(background=true, notify_on_complete=true) — foreground caps at 600s.
- For YouTube/social platforms use yt-dlp instead of HTML scraping.
- Login/paywall-protected content: stop and ask the user; never handle credentials.

## File delivery (Windows host via Docker)

- Host drives are mounted at `/host/<letter>` (e.g. `/host/c/Users/cruzmars/Downloads`, `/host/d/...`).
  Write directly there — no need to stage on C: first if `/host/d` exists (`ls /host/` to check).
- Ask the user where to save when not specified; default suggestion is their Downloads folder.
- If a drive is missing from `/host/`, add it under `terminal.docker_volumes` in config.yaml and restart Hermes.
  Edit the YAML directly so it is a real list — a quoted string is silently ignored (no volumes get mounted):

      ```yaml
      docker_volumes:
        - 'C:\:/host/c'
        - 'D:\:/host/d'
      ```

  If you use `hermes config set terminal.docker_volumes ...`, pass a JSON list (e.g. `["D:\\:/host/d"]`),
  never a Python-style literal like `['D:\:/host/d']` — that gets stored as a string and the drive
  is never mounted into the container.
