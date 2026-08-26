# Data Sources and Provenance

Last reviewed: 2026-08-26.

## O*NET database

Official source: https://www.onetcenter.org/database.html
License information: https://www.onetonline.org/help/license

Recommended uses:
- occupation mapping;
- essential and transferable skills;
- software/technology examples;
- education, training, work experience, tasks, and work activities.

The O*NET 31.0 database is downloadable in tabular and machine-readable formats. Preserve attribution when redistributing transformed O*NET-derived data. O*NET occupational ratings are occupational baselines, not hiring-outcome statistics.

## Bureau of Labor Statistics

OEWS tables: https://www.bls.gov/oes/tables.htm
Employment Projections: https://www.bls.gov/emp/
Top skills by detailed occupation: https://www.bls.gov/emp/tables/top-skills-by-detailed-occupation.htm
Developer API: https://www.bls.gov/developers/

Recommended uses:
- employment levels and concentration;
- wages by occupation and geography;
- projected growth and openings;
- typical education/training benchmarks.

Do not infer that higher projected growth means an individual applicant is more likely to be hired.

## OPM Federal Workforce Data

Public data endpoint: https://data.opm.gov/
OPM datasets: https://www.opm.gov/data/

Recommended uses:
- federal accessions (hires/onboarding events);
- separations;
- employment headcount;
- federal occupational series, grade/pay, agency, and geography benchmarks.

Scope all conclusions to the federal civilian workforce. The optional `scripts/opm_fwd.py` adapter follows the public FWD file-list/download pattern and caches downloads locally.

## USAJOBS

Developer portal: https://developer.usajobs.gov/
Search tutorial: https://developer.usajobs.gov/tutorials/search-jobs

Recommended use: current federal vacancy demand. Search requires the user's own API key and request headers. Do not embed or redistribute user credentials.

## Private-sector postings

Use only data the user has a right to analyze: public/open datasets, licensed APIs, organization-owned exports, or user-provided files. Do not bypass robots, authentication, paywalls, rate limits, or terms of service.

Store at minimum:
- source;
- external posting ID if available;
- title;
- date;
- location;
- description or extracted skills;
- collection timestamp.

## Licensed providers

Providers such as Lightcast or Revelio Labs may support richer job-posting, workforce-profile, or transition analyses. Treat them as optional adapters. Do not ship proprietary data in this skill, and do not claim compatibility without testing the provider's current schema and license.

## Source quality hierarchy

For occupational definitions and official statistics, prefer official government sources. For current employer demand, prefer recent vacancy data with transparent collection provenance. For hiring-outcome associations, prefer datasets containing both successful and unsuccessful applicants for the same or comparable roles rather than only profiles of incumbents.
