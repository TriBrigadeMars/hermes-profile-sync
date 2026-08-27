# Literature Source Map — verified access methods for a health & social-science journal set

Concrete, verified endpoints for monitoring a set of public-health / social-science
journals (build time: Aug 2026). Access method chosen per publisher because several
sit behind Cloudflare bot protection that defeats plain HTTP RSS scraping.

## Access-method summary

| Journal | ISSN | Publisher | Working access | Notes |
|---|---|---|---|---|
| Bulletin of the WHO | 0042-9686 (also 1564-0604) | WHO Press | Crossref API | no usable public RSS |
| The Lancet Global Health | 2214-109X | Elsevier | Crossref API | thelancet.com behind Cloudflare (403) |
| Globalization and Health | 1475-9276 | Springer/BMC | Crossref API | BMC `/articles/rss` 301s to HTML |
| BMJ Global Health | 2059-7908 | BMJ | Native RSS `https://gh.bmj.com/rss.xml` | worked directly |
| Frontiers | (varies per journal) | Frontiers | Native RSS `https://www.frontiersin.org/journals/{slug}/rss` | per-journal slug; e.g. `public-health` |
| SAGE Open | 2158-2440 | SAGE | Crossref API | sagepub.com behind Cloudflare |
| IJERPH (MDPI) | 1660-4601 | MDPI | Crossref API | mdpi.com returns Access Denied on RSS |

## Crossref by-ISSN pattern

```
GET https://api.crossref.org/journals/{ISSN}/works?rows=N&filter=from-pub-date:YYYY-01-01
```

- Response: `message.items[]` with `title` (list), `URL` (doi.org string),
  `link[]` (pick `content-type` == application/pdf or text/html), `issued.date-parts`,
  `abstract`.
- The journals/works endpoint 404s if the ISSN is wrong — verify ISSN first via:
  ```
  GET https://api.crossref.org/works?query.bibliographic={journal name}&rows=1
  ```
  Read `ISSN` from the returned item. NOTE: that query may return the *wrong*
  (multidisciplinary) journal for generic names like "Frontiers" — search the
  exact journal title.
- Crossref rate-limits politely; one `.json()` fetch per journal per run is ample.

## PubMed E-utilities (topic/author feeds)

```
esearch:  eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi
          db=pubmed, term=<query> AND "<last 30 days>"[dp], retmode=json,
          retmax=N, sort=pub_date   -> esearchresult.idlist  (PMIDs)
esummary: eutils.ncbi.nlm.nih.gov/entrez/eutils/esummary.fcgi
          db=pubmed, id=<csv PMIDs>, retmode=json            -> result keyed by PMID
```

- Article URL = `https://pubmed.ncbi.nlm.nih.gov/{pmid}/`
- Send `User-Agent` containing a contact email (NCBI policy).
- Dedupe on PMID (not URL).
- Batch all PMIDs into ONE esummary call; ~3 req/s throttle without an API key
  (fine for a daily feed).
- **CRITICAL**: relative date filter must be quoted → `"last 30 days"[dp]`.
  Unquoted `30 DAYS[dp]` silently returns 0 results. Verify by running the query
  without the date filter and confirming it has hits, then re-adding it.

## Native RSS verification

Some feeds don't start with `<?xml` (e.g. Al Jazeera starts `<rss version="2.0">`).
Accept `<?xml` OR `<rss` OR `<feed` at body start; check `Content-Type` for
`xml`/`rss`/`atom`. When a homepage or `robots.txt` won't reveal a feed, probe
common paths: `/feed`, `/rss`, `/rss.xml`, `/feed.xml`, `/atom.xml`.

Frontiers per-journal RSS: `https://www.frontiersin.org/journals/{slug}/rss`
(e.g. `public-health`, `psychology`, `medicine` — all return 200). There is no
single all-Frontiers RSS; choose the journal slug matching the subfield.

## When to drop a source instead of fighting it

- Elsevier (thelancet.com), SAGE (journals.sagepub.com), MDPI (mdpi.com): all sit
  behind Cloudflare. RSS returns 403 / "Just a moment…" / "Access Denied".
  Do NOT burn turns retrying headers — go straight to Crossref.
- SF Chronicle (`sfchronicle.com`): Next.js migration removed RSS entirely and its
  homepage/sitemap aren't bot-friendly. Exclude rather than maintain a broken feed.
