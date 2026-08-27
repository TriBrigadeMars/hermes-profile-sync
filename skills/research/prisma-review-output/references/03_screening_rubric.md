# Screening Rubric for Scoping Review

## Overview
Two-stage screening process following Arksey & O'Malley (2005) and JBI methodology:
- **Stage 1**: Title and abstract screening
- **Stage 2**: Full-text screening

Both stages require independent screening by two reviewers with conflict resolution.

---

## Stage 1: Title and Abstract Screening

### Decision Rule
For each record, reviewers classify as: **INCLUDE**, **EXCLUDE**, or **MAYBE**.

### Inclusion Criteria (All Must Be Met)
| # | Criterion | Question |
|---|-----------|----------|
| 1 | Population | Does the study include minority-group students in U.S. higher education? |
| 2 | Exposure | Does the study address disability-related and/or pregnancy-related discrimination, bias, or barriers? |
| 3 | Outcomes | Does the study report on academic, psychological, social, or institutional outcomes? |
| 4 | Timeframe | Was the study published between 2010 and 2026? |
| 5 | Setting | Is the study conducted in U.S. postsecondary education? |
| 6 | Design | Is this an empirical study (quantitative, qualitative, or mixed-methods)? |

### Decision Tree for Title/Abstract Screening

```
START
  │
  ├─ Is it published between 2010-2026?
  │   └─ NO → EXCLUDE (Reason: Outside timeframe)
  │
  ├─ Is it in English?
  │   └─ NO → EXCLUDE (Reason: Language)
  │
  ├─ Is it set in U.S. higher education?
  │   └─ NO → EXCLUDE (Reason: Outside U.S.)
  │
  ├─ Does it include minority-group populations (racial/ethnic, gender, LGBTQ+, etc.)?
  │   └─ NO → EXCLUDE (Reason: No minority population)
  │
  ├─ Does it address disability and/or pregnancy-related discrimination?
  │   └─ NO → EXCLUDE (Reason: No relevant exposure)
  │
  ├─ Is it an empirical study?
  │   └─ NO → EXCLUDE (Reason: Not empirical)
  │
  ├─ Does it report outcomes related to discrimination?
  │   └─ NO → EXCLUDE (Reason: No relevant outcomes)
  │
  └─ ALL criteria met → INCLUDE
```

### Exclusion Categories for Title/Abstract (PRISMA Flow Diagram)

| Code | Exclusion Reason | Definition |
|------|-----------------|------------|
| E1 | Outside timeframe | Published before 2010 |
| E2 | Non-English | Not published in English |
| E3 | Outside U.S. | Not conducted in U.S. higher education |
| E4 | No minority population | Does not include minority-group students |
| E5 | No relevant exposure | Does not address disability or pregnancy discrimination |
| E6 | Not empirical | Opinion, editorial, theoretical commentary without empirical data |
| E7 | No relevant outcomes | Does not report on discrimination-related outcomes |
| E8 | Wrong setting | K-12 or workplace setting, not higher education |
| E9 | Population mismatch | Focuses exclusively on faculty, staff, or administrators |

### Screening Agreement
- **Target**: ≥80% agreement between reviewers at Stage 1
- **Resolution**: Disagreements resolved through discussion; persistent disagreements adjudicated by third reviewer
- **Calibration**: Reviewers pilot-screen first 25 records together to calibrate

---

## Stage 2: Full-Text Screening

### Inclusion Criteria (All Must Be Met)

| # | Criterion | Detailed Description |
|---|-----------|---------------------|
| 1 | Population | Study explicitly includes minority-group students (racial/ethnic, LGBTQ+, first-generation, or other minority status) who have disabilities or are pregnant/parenting |
| 2 | Exposure | Study examines disability-related and/or pregnancy-related discrimination, barriers, bias, harassment, or marginalization |
| 3 | Outcomes | Study reports at least one outcome in the domains of academic performance, psychological well-being, social integration, or institutional response |
| 4 | Design | Study uses a systematic empirical methodology (survey, interview, case study, ethnography, secondary data analysis, experimental, quasi-experimental) |
| 5 | Setting | Study conducted at 2-year or 4-year postsecondary institution(s) in the U.S. |
| 6 | Data | Study provides sufficient data to characterize findings (even if qualitative) |
| 7 | Population specification | Study provides demographic information allowing identification of minority-group participants |

### Exclusion Criteria for Full-Text

| # | Criterion | Rationale |
|---|-----------|-----------|
| 1 | Insufficient data | Abstract/summary only, no methods or results reported |
| 2 | Population mismatch | Participants not identifiable as minority-group students, or not identified as disabled/pregnant/parenting |
| 3 | Wrong setting | K-12, workplace, clinical setting only (not postsecondary) |
| 4 | Duplicate data | Same data reported in another included study (retain more complete version) |
| 5 | No original data | Review articles, meta-analyses, or secondary analyses without new data (flag as background references) |

### Full-Text Decision Tree

```
START
  │
  ├─ Can we access the full text?
  │   └─ NO → Seek through ILL or author contact. If unavailable → EXCLUDE
  │
  ├─ Does the study include identifiable minority-group students
  │   who have disabilities or are pregnant/parenting?
  │   └─ NO → EXCLUDE (Reason: Population mismatch)
  │
  ├─ Does the study examine disability and/or pregnancy-related
  │   discrimination, barriers, or bias?
  │   └─ NO → EXCLUDE (Reason: No relevant exposure)
  │
  ├─ Does the study report empirical findings on outcomes?
  │   └─ NO → EXCLUDE (Reason: No empirical outcomes)
  │
  ├─ Is the study conducted at U.S. postsecondary institutions?
  │   └─ NO → EXCLUDE (Reason: Wrong setting)
  │
  ├─ Does the study report sufficient data?
  │   └─ NO → EXCLUDE (Reason: Insufficient data)
  │
  └─ ALL criteria met → INCLUDE for data extraction
```

### Full-Text Exclusion Categories (PRISMA Flow Diagram)

| Code | Exclusion Reason |
|------|-----------------|
| FT1 | Full text not obtainable |
| FT2 | Population mismatch |
| FT3 | No relevant exposure |
| FT4 | No empirical outcomes |
| FT5 | Wrong setting |
| FT6 | Duplicate data |
| FT7 | Insufficient data |
| FT8 | Review/secondary analysis (no new data) |

---

## Screening Documentation

### Required Fields per Record
| Field | Description |
|-------|-------------|
| Record ID | Database-specific identifier |
| Title | Full title |
| Author(s) | First author et al. |
| Year | Publication year |
| Screener | Reviewer name/initials |
| Stage | 1 (title/abstract) or 2 (full-text) |
| Decision | INCLUDE / EXCLUDE / MAYBE |
| Exclusion Code | If excluded, code from tables above |
| Notes | Rationale for decision, especially for MAYBE/EXcluded |
| Resolution | For disagreements: consensus / third reviewer |

### Screening Tools
- **Primary**: Covidence (recommended) or Rayyan
- **Backup**: Zotero with custom tags
- **Conflict resolution**: Discussion-based, documented in screening log

---

## PRISMA-ScR Flow Diagram Numbers

After screening, populate the PRISMA-ScR flow diagram:

```
Records identified (n = )
  ├─ Database A (n = )
  ├─ Database B (n = )
  ├─ Database C (n = )
  └─ Other sources (n = )

Records after duplicates removed (n = )

Records screened at title/abstract (n = )
  └─ Records excluded (n = )
      ├─ E1: Outside timeframe (n = )
      ├─ E2: Non-English (n = )
      ├─ E3: Outside U.S. (n = )
      ├─ E4: No minority population (n = )
      ├─ E5: No relevant exposure (n = )
      ├─ E6: Not empirical (n = )
      ├─ E7: No relevant outcomes (n = )
      └─ E8: Wrong setting (n = )

Full-text articles assessed (n = )
  └─ Full-text articles excluded (n = )
      ├─ FT1: Not obtainable (n = )
      ├─ FT2: Population mismatch (n = )
      ├─ FT3: No relevant exposure (n = )
      ├─ FT4: No empirical outcomes (n = )
      ├─ FT5: Wrong setting (n = )
      ├─ FT6: Duplicate data (n = )
      └─ FT7: Insufficient data (n = )

Studies included in scoping review (n = )
```
