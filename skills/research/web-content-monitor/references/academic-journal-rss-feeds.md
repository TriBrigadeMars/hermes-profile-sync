# Academic Journal RSS Feed Discovery Notes

## Session: Aug 15, 2026

### Feed URLs Discovered

#### Working RSS Feeds
- **Financial Times World**: `https://www.ft.com/rss/world`
- **Courier Newsroom**: `https://couriernewsroom.com/feed/`
- **404 Media**: `https://www.404media.co/feed/`
- **Al Jazeera English**: `https://www.aljazeera.com/xml/rss/all.xml`
  - Note: starts with `<rss version="2.0">` not `<?xml` — don't validate on `<?xml` only
- **Jacobin**: `https://jacobin.com/feed/`
- **Novara Media**: `https://novaramedia.com/feed/`
- **BMJ Global Health**: `https://gh.bmj.com/rss.xml`
- **Frontiers**: `https://www.frontiersin.org/journals/{journal-slug}/rss`
  - Journal slugs: `public-health`, `psychology`, `medicine`, `neuroscience`, etc.
  - Returns full RSS — no Cloudflare protection on Frontiers RSS endpoints
- **SAGE Open**: No working RSS (Cloudflare blocked). Use Crossref API with ISSN `2158-2440`
- **IJERPH (MDPI)**: No working RSS (Cloudflare blocked). Use Crossref API with ISSN `1660-4601`

#### Cloudflare-Blocked (use Crossref API fallback)
| Journal | ISSN | Crossref API URL |
|---|---|---|
| Bulletin of the WHO | 0042-9686 | `https://api.crossref.org/journals/0042-9686/works` |
| The Lancet Global Health | 2214-109X | `https://api.crossref.org/journals/2214-109X/works` |
| Globalization and Health | 1475-9276 | `https://api.crossref.org/journals/1475-9276/works` |
| BMJ Global Health | 2059-7908 | `https://api.crossref.org/journals/2059-7908/works` |
| SAGE Open | 2158-2440 | `https://api.crossref.org/journals/2158-2440/works` |
| IJERPH | 1660-4601 | `https://api.crossref.org/journals/1660-4601/works` |

### Key Techniques

1. **Crossref API** (`api.crossref.org`): Returns JSON with article titles, DOIs, abstracts, publication dates. Free, no auth required. Use `filter=from-pub-date:YYYY-MM-DD` and `rows=N`.

2. **Frontiers journal-level RSS**: Navigate to `https://www.frontiersin.org/journals/{journal}/rss` for each journal. Each journal has its own RSS feed, not a single multidisciplinary one.

3. **Homepages blocked by Cloudflare** (SAGE, MDPI): The homepage HTML returns a Cloudflare challenge page. Can't auto-discover RSS from homepage HTML. Must use known feed URLs or Crossref API.

4. **RSS format validation**: Some valid feeds start with `<rss version="2.0">` instead of `<?xml version="1.0"?>`. Check for both patterns, plus `<feed` for Atom feeds.

5. **BMJ hybrid approach**: BMJ RSS (`https://gh.bmj.com/rss.xml`) works, but if it stops working, Crossref fallback is available with ISSN `2059-7908`.
