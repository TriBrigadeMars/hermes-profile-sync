# CourtListener API v4 Quick Reference

Base: `https://www.courtlistener.com/api/rest/v4/`

## Search endpoint
`GET /search/?q=<query>&type=<type>&order_by=score desc`

| type | searches |
|------|----------|
| `o`  | opinion clusters (case law) |
| `r`  | RECAP filings (docket entries, briefs incl. amicus) |
| `d`  | dockets |
| `p`  | judges |
| `oa` | oral arguments |

## Useful filters
- `court=scotus` (also: `scotus`, `ca9`, `dcd`, etc. — see /api/rest/v4/courts/)
- `filed_after=YYYY-MM-DD` / `filed_before=YYYY-MM-DD`
- `stat_Errata=on`, `order_by=dateFiled desc`

## Key fields in results
- `caseName`, `citation[]`, `neutralCite`, `dateFiled`, `docketNumber`
- `absolute_url` — link for reports
- `opinions[].download_url` — PDF of the opinion
- RECAP results: `description`, `filepath_local`, `entry_number`

## Rate limits
- Anonymous: ~100 requests/hour per IP.
- Free account token raises limits: register at
  https://www.courtlistener.com/profile/signups/ then pass header:
  `Authorization: Token <TOKEN>`
- Store tokens in env/config — never hardcode in scripts.

## Other endpoints
- `/dockets/<id>/` — full docket sheet (auth required)
- `/clusters/<id>/` — opinion cluster metadata
- `/courts/` — court ID list
- `/recap-query/` — PACER-originated filing lookup

## Companion sources
- Caselaw Access Project: `https://api.case.law/v1/cases/?search=<q>`
- GovInfo US Courts Opinions: `https://api.govinfo.gov` (needs free key)
- SCOTUS filings: https://www.supremecourt.gov/oral-argument/argument-transcripts
  and case dockets under /cases/
