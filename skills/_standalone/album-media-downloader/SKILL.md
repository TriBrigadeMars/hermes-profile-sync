---
name: album-media-downloader
description: "Download all media from album/gallery page URLs."
version: 1.0.0
---

## When to Use

Trigger: the user provides one or more album/gallery URLs (`erome.com/a/<ID>` or similar) and wants all media downloaded. ALWAYS ASK where to save first (clarify tool); common default for Erome is `D:\Erome\Neeko\<album_id>\`.

# Album / Gallery Media Downloader

Downloads all media from one or more album or gallery pages (e.g. `https://www.erome.com/a/<ID>`), fully and verified.

## Critical lessons (don't skip)

1. **Match ALL extensions**: `.jpg`, `.jpeg`, `.png`, `.webp`, `.gif`, `.mp4`. Many galleries serve images as **`.jpeg`** via lazy-load — a `.jpg`-only regex silently misses nearly everything.
2. **Images often come from `data-src="..."` attributes** on `<img>` tags (lazy loading), not plain `src=`. Videos are usually in `<source src="...mp4">`.
3. **Skip `/thumbs/` URLs** — those are thumbnails.
4. **Strip the `?v=...` cache-buster** for filenames.
5. **Always send** a browser User-Agent and an appropriate `-e <site>/` referer when fetching media.
6. **Verify counts**: count media refs on the page vs files downloaded. If mismatched, re-check the HTML before reporting done.
7. Long downloads (>100 files or large videos): run with terminal `background=true` and `notify_on_complete=true`; foreground max timeout is 600s.
8. **ALWAYS ASK where to save before downloading** — use the `clarify` tool with suggested options (e.g. `D:\Erome\Neeko`, a new subfolder, or Other). Never assume a destination, even the default; confirm first unless the user explicitly named the folder in their request.
9. Mars's most common destination for Erome is `D:\Erome\Neeko` = Docker path `/host/d/Erome/Neeko/<album_id>/`.

## Workflow (Erome example)

```bash
UA="Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/126.0"
PAT='(data-src=")?https://[a-z0-9]+\.erome\.com/[^" ]+\.(jpg|jpeg|png|webp|gif|mp4)[^" ]*'
for id in ID1 ID2; do
  d="/host/d/Erome/Neeko/$id"; mkdir -p "$d"
  curl -sL -A "$UA" "https://www.erome.com/a/$id" -o /tmp/p_$id.html
  grep -oE "$PAT" /tmp/p_$id.html | sed 's/data-src="//' | sort -u | grep -v thumbs > "$d/urls.txt"
  echo "$id: $(wc -l < $d/urls.txt) media found"
  while read u; do
    f=$(basename "$u" | cut -d'?' -f1)
    [ -f "$d/$f" ] || curl -s -A "$UA" -e "https://www.erome.com/" -o "$d/$f" "$u"
  done < "$d/urls.txt"
  rm "$d/urls.txt"
  echo "$id done: $(ls $d|wc -l) files, $(du -sh $d|cut -f1)"
done
```

- Writes go directly to D: via `/host/d/...` (mounted). Staging then copying is also fine.
- For other gallery sites, adapt the `PAT` regex and base URL to the source's actual media link structure.
- Private/deleted albums return a page with no media links — report that honestly rather than assuming success.