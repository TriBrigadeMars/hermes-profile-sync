# Stage 3 — Screening Rubric

## Overview
Two-stage screening process based on JBI scoping review methodology:
1. **Stage 1**: Title and Abstract Screening
2. **Stage 2**: Full-Text Screening

Each stage uses standardized inclusion/exclusion criteria with documented decision rationale.

---

## Stage 1: Title and Abstract Screening

### Screening Tool
Covidence, Rayyan, or equivalent systematic review screening software.

### Screening Team
- **Primary Screener**: Reviews all records independently
- **Second Screener**: Reviews 20% random sample for inter-rater reliability
- **Conflict Resolution**: Discussion-based; unresolved conflicts escalated to third reviewer

### Inclusion Criteria Checklist (Title/Abstract)

| # | Criterion | YES/NO | Notes |
|---|-----------|--------|-------|
| 1 | Study involves U.S. colleges/universities | | |
| 2 | Study includes minority students (racial/ethnic, gender identity, sexual orientation, disability) | | |
| 3 | Study examines sexual harassment and/or discrimination | | |
| 4 | Study reports outcomes (academic, psychological, social, institutional) | | |
| 5 | Published 2010-2026 | | |
| 6 | Published in English | | |
| 7 | Peer-reviewed, dissertation, or government/institutional report | | |

### Decision Rule (Stage 1)
- **INCLUDE**: Criteria 1–4 = YES (criteria 5–7 verified from metadata)
- **EXCLUDE**: Any of criteria 1–4 = NO
- **UNSURE**: Mark for full-text review if uncertain about any criterion

---

## Stage 2: Full-Text Screening

### Full-Text Retrieval
1. Search institutional library holdings
2. Interlibrary loan (ILL) requests
3. Direct author contact for unpublished works
4. Document reasons for non-retrieval (PRISMA flow diagram)

### Full-Text Inclusion/Exclusion Decision Tree

```
START: Full-text article retrieved
│
├── Criterion 1: U.S. Higher Education Setting?
│   ├── YES → Continue
│   ├── NO → EXCLUDE (reason: non-US or non-higher ed)
│   └── MIXED → Continue if ≥50% US higher ed
│
├── Criterion 2: Minority Population Represented?
│   ├── YES → Continue
│   ├── NO → EXCLUDE (reason: no minority subgroup data)
│   └── PARTIAL → Continue if minority subgroup analyzable
│
├── Criterion 3: Sexual Harassment/Discrimination Exposure?
│   ├── YES → Continue
│   ├── NO → EXCLUDE (reason: no harassment/discrimination exposure)
│   └── INDIRECT → Continue if harassment/discrimination is substantive component
│
├── Criterion 4: Outcomes Measured?
│   ├── YES → Continue
│   ├── NO → EXCLUDE (reason: no measurable outcomes)
│   └── MINIMAL → Continue if any outcome data reported
│
├── Criterion 5: Sufficient Data?
│   ├── YES → INCLUDE
│   └── NO → EXCLUDE (reason: insufficient data for extraction)
│
└── DECISION: INCLUDE or EXCLUDE with documented reason
```

---

## Exclusion Categories for PRISMA Flow Diagram

| Exclusion Category | Code | Description | PRISMA Category |
|-------------------|------|-------------|-----------------|
| **Wrong population** | WP | No minority students or non-U.S./non-higher ed setting | Stage 1 |
| **Wrong exposure** | WE | No sexual harassment or discrimination component | Stage 1 |
| **Wrong outcome** | WO | No academic, psychological, social, or institutional outcomes | Stage 1 |
| **Wrong setting** | WS | Non-U.S. institution | Stage 1 |
| **Wrong publication type** | WPT | Editorials, commentaries, non-peer-reviewed without data | Stage 1 |
| **Wrong time period** | WTP | Published before 2010 | Stage 1 |
| **Non-English** | NE | Non-English publication | Stage 1 |
| **Duplicate** | DUP | Duplicate record | Stage 1 |
| **Insufficient data** | ID | Full text reviewed but insufficient data for extraction | Stage 2 |
| **Not obtainable** | NO | Full text not obtainable despite ILL/author contact | Stage 2 |
| **Wrong study design** | WSD | Narrative/opinion without original data | Stage 2 |

---

## Inter-Rater Reliability

### Metrics
- **Cohen's Kappa** (κ): Target ≥ 0.80 (substantial agreement)
- **Percent Agreement**: Target ≥ 90%
- **Disagreement Rate**: Document and analyze sources of disagreement

### Calibration Process
1. Both screeners independently screen first 25 records
2. Meet to discuss discrepancies and refine criteria
3. Screen next 25 records independently
4. Calculate inter-rater reliability
5. If κ ≥ 0.80, proceed with primary screener completing remaining records
6. If κ < 0.80, conduct additional calibration rounds

---

## Screening Documentation Template

### Per-Record Documentation
| Field | Content |
|-------|---------|
| Record ID | Database-specific identifier |
| Title | Full title |
| Authors | Author list |
| Year | Publication year |
| Database | Source database |
| Screener | Name of screener |
| Decision | INCLUDE / EXCLUDE / UNSURE |
| Stage | Stage 1 (title/abstract) or Stage 2 (full-text) |
| Exclusion Reason | If excluded, specific category code |
| Exclusion Detail | Brief explanation |
| Notes | Any additional notes |
| Conflict Resolution | If applicable, how conflict was resolved |

---

## PRISMA Flow Diagram Template

```
┌─────────────────────────────────────────────────┐
│        Records identified through searching      │
│                                                   │
│  PubMed: [n]  ERIC: [n]  PsycINFO: [n]          │
│  Ed Source: [n]  JSTOR: [n]  Google Scholar: [n] │
│  Scopus: [n]  Gray Lit: [n]                      │
│  Total: [n]                                       │
└─────────────────────────────────────────────────┘
                    │
                    ▼
┌─────────────────────────────────────────────────┐
│   Records after duplicates removed: [n]          │
└─────────────────────────────────────────────────┘
                    │
                    ▼
┌─────────────────────────────────────────────────┐
│        Records screened (title/abstract)         │
│              n = [total records]                 │
│                                                   │
│  Excluded: [n]                                   │
│    Wrong population: [n]                         │
│    Wrong exposure: [n]                           │
│    Wrong outcome: [n]                            │
│    Wrong setting: [n]                            │
│    Wrong publication type: [n]                   │
│    Wrong time period: [n]                        │
│    Non-English: [n]                              │
└─────────────────────────────────────────────────┘
                    │
                    ▼
┌─────────────────────────────────────────────────┐
│       Full-text articles assessed                │
│              n = [remaining]                     │
│                                                   │
│  Full-text excluded: [n]                         │
│    Insufficient data: [n]                        │
│    Not obtainable: [n]                           │
│    Wrong study design: [n]                       │
│    Wrong population (confirmed): [n]             │
│    Wrong exposure (confirmed): [n]               │
└─────────────────────────────────────────────────┘
                    │
                    ▼
┌─────────────────────────────────────────────────┐
│        Studies included in scoping review        │
│              n = [final included]                │
└─────────────────────────────────────────────────┘
```

---

## Screening Timeline

| Phase | Duration | Activities |
|-------|----------|------------|
| Calibration | 1 week | Screen first 50 records together, calculate κ |
| Stage 1 Screening | 2 weeks | Primary screener: all records; second screener: 20% sample |
| Full-text retrieval | 1 week | Library, ILL, author contact |
| Stage 2 Screening | 1 week | Primary screener: all; second screener: 20% sample |
| Conflict resolution | 3 days | Resolve all conflicts through discussion |
