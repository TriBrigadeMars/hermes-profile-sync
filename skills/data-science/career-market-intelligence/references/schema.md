# Input Schemas

## Job postings

CSV, JSON array, or JSONL. Field names are matched case-insensitively with common aliases.

Preferred fields:

- `id` or `external_id`
- `title` (required)
- `company`
- `location`
- `industry`
- `posted_date` (`YYYY-MM-DD` preferred)
- `description`
- `skills` (optional; delimiter may be comma, semicolon, or pipe)
- `years_experience` (optional numeric)
- `education` (optional)

If `skills` is absent, the local taxonomy in `data/seed_skills.csv` is matched against the description.

## Applicant outcomes

Use only lawful, appropriately de-identified data for job-seeker research. Preferred fields:

- `candidate_id` or anonymous record id
- `target_title` or `title` (required)
- `location`
- `event_date`
- `status` (`rejected`, `interview`, `offer`, `hired`, etc.)
- `hired` (optional boolean; derived from status if absent)
- `interview` (optional boolean)
- `offer` (optional boolean)
- `skills` (job-relevant skills only)
- `years_experience`
- `education`

Do not ingest protected traits for predictive recommendations.

## Candidate profile

Example:

```json
{
  "skills": ["SQL", "Python", "Power BI"],
  "years_experience": 6,
  "education": "Bachelor's degree",
  "evidence": {
    "SQL": "Built production reporting queries for 4 years",
    "Python": "Automated monthly analytics pipeline",
    "Power BI": "Owned executive dashboard suite"
  }
}
```

The `evidence` map is optional but recommended. A listed skill is treated as candidate-supplied evidence; the system must not add unlisted market-demand skills to the resume as claims.

## O*NET import directory

The importer looks for files whose names resemble:
- `Occupation Data.*`
- `Essential Skills.*`
- `Transferable Skills.*`
- `Software Skills.*`
- `Training and Experience.*`
- `Education.*`
- `Job Zones.*`

CSV, tab-delimited text, and JSON are supported by the core importer. XLSX can be converted to CSV first or read with an optional pandas/openpyxl workflow.

## OEWS import

The importer accepts a delimited text/CSV file and recognizes common current fields such as:
- `OCC_CODE`, `OCC_TITLE`
- `AREA`, `AREA_TITLE`
- `TOT_EMP`
- `EMP_PRSE`
- `H_MEAN`, `A_MEAN`
- `H_MEDIAN`, `A_MEDIAN`

Suppression symbols and unavailable values are preserved as nulls.
