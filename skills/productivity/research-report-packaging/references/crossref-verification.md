# Crossref Verification Workflow for Literature Reviews

When producing literature reviews with APA 7 citations, verify every source against Crossref (the canonical DOI/metadata registry) before including it in the deliverable. Subagent self-reports are NOT trustworthy for factual claims — always verify.

## Why Crossref

- Crossref is the authoritative registry for DOIs and bibliographic metadata
- It returns canonical title, authors, venue, year, and DOI for any registered work
- Free API, no authentication required for basic use
- Resolves both journal articles and conference papers with DOIs

## API Endpoints

| Query | Endpoint | Returns |
|-------|----------|---------|
| By DOI | `https://api.crossref.org/works/{doi}` | Single record |
| By title | `https://api.crossref.org/works?query.bibliographic={title}&rows=5` | Ranked matches |
| By author | `https://api.crossref.org/works?query.author={name}&rows=10` | Author's works |

## Verification Script Pattern

```python
import json, urllib.request, urllib.parse, re

CR = "https://api.crossref.org"

def cr_get(url, timeout=25):
    req = urllib.request.Request(url, headers={"User-Agent": "hermes-litreview/1.0 (mailto:research@example.com)"})
    try:
        with urllib.request.urlopen(req, timeout=timeout) as r:
            return json.loads(r.read())
    except Exception:
        return None

def cr_doi(doi):
    d = urllib.parse.quote(doi.strip(), safe="/")
    j = cr_get(f"{CR}/works/{d}")
    return j["message"] if j and "message" in j else None

def cr_title(title, rows=5):
    q = urllib.parse.quote(title)
    j = cr_get(f"{CR}/works?query.bibliographic={q}&rows={rows}&select=DOI,title,author,issued,container-title,type,publisher")
    if not j: return []
    return j.get("message", {}).get("items", [])

def extract(msg):
    title = (msg.get("title") or [""])[0]
    year = None
    dp = msg.get("issued", {}).get("date-parts", [[None]])
    if dp and dp[0]: year = dp[0][0]
    authors = []
    for a in msg.get("author", [])[:25]:
        fam = a.get("family", "")
        giv = a.get("given", "")
        if fam: authors.append(f"{fam}, {giv}".strip(", "))
    venue = (msg.get("container-title") or [""])[0] or msg.get("publisher", "")
    doi = msg.get("DOI", "")
    return {"title": title, "year": year, "authors": authors, "venue": venue, "doi": doi}

def best_match(items, query_title):
    qwords = set(re.findall(r'\w+', query_title.lower()))
    best, best_score = None, 0
    for it in items:
        t = ((it.get("title") or [""])[0]).lower()
        score = len(qwords & set(re.findall(r'\w+', t)))
        if score > best_score:
            best, best_score = it, score
    return best if best_score >= 3 else None
```

## Workflow

1. **Collect candidate sources** from subagents, web_search, or arXiv
2. **For each candidate with a DOI**: resolve via `cr_doi(doi)` — if it returns metadata, the DOI is real
3. **For each candidate without a DOI**: search via `cr_title(title)` and pick the best match
4. **Extract canonical metadata**: title, authors (Last, First), year, venue, DOI
5. **Format APA 7 citations** from the verified metadata — never from subagent self-reports
6. **Rate-limit**: sleep 0.3-0.5s between Crossref calls to be polite

## Pitfalls

- **Never trust subagent DOIs.** Subagents frequently hallucinate DOIs (e.g., `10.48550/arXiv.3114.11462` — the prefix is wrong). Always verify against Crossref.
- **arXiv DOIs use DataCite, not Crossref.** `10.48550/arXiv.XXXX.XXXX` won't resolve via Crossref. Use the arXiv API (`http://export.arxiv.org/api/query?id_list=XXXX`) or web_search instead.
- **Title matching is fuzzy.** Crossref's query.bibliographic returns ranked results; use `best_match()` to pick the closest match by word overlap. A match score < 3 words is likely wrong.
- **Garbled author names.** Subagent output often has corrupted author names (e.g., "Evan Choi J" instead of "Choi, J. H."). Always use Crossref's canonical author list.
- **Rate limiting.** Crossref returns HTTP 429 if you exceed ~1 req/sec. Add `time.sleep(0.4)` between calls.
- **Missing DOIs.** Not all papers have DOIs (SSRN working papers, law reviews, institutional reports). For those, verify the URL via web_extract and mark DOI as "none" in the citation.

## APA 7 Citation Format from Crossref Data

```
Author, A. A., & Author, B. B. (Year). Title of article. *Journal Name*, *Volume*(Issue), Pages. https://doi.org/xxxxx
```

- Authors: `Last, First` from Crossref's `author.family` and `author.given`
- Year: from `issued.date-parts[0][0]`
- Title: from `title[0]` (sentence case)
- Venue: from `container-title[0]` (italicize in output)
- DOI: from `DOI` field (prefix with `https://doi.org/`)
