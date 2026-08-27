# PRISMA Systematic Review Pipeline — Output README

## Review Information

| Field | Value |
|-------|-------|
| **Topic** | {TOPIC} |
| **Review Type** | {TYPE} |
| **Search Mode** | {MODE} |
| **Date Generated** | {DATE} |
| **Pipeline Version** | Hermes PRISMA Pipeline v1.0 |

## Files in This Directory

| File | Description | Agent |
|------|-------------|-------|
| `01_protocol.md` | PECOS framework & review protocol | Protocol Specialist |
| `02_search_strategy.md` | Boolean search strings per database | Medical Librarian |
| `02_search_results.csv` | Retrieved study records (web-live mode) | Medical Librarian |
| `03_screening_rubric.md` | Inclusion/exclusion screening criteria | Review Screener |
| `04_extraction_template.json` | Data extraction form (JSON schema) | Extraction Analyst |
| `04_bias_assessment.md` | Risk of bias assessment framework | Extraction Analyst |
| `05_analysis_plan.md` | Statistical analysis plan | Biostatistician |
| `05_meta_analysis.R` | Runnable R script for meta-analysis | Biostatistician |
| `06_manuscript_draft.md` | PRISMA 2020 manuscript draft | Lead Author |
| `06_prisma_checklist.md` | PRISMA 2020 compliance checklist | Lead Author |
| `extracted_data.csv` | Data extraction template (CSV) | Pipeline |

## Next Steps

### 1. Review the Protocol
- [ ] Verify PECOS criteria are accurate
- [ ] Consider PROSPERO registration (https://www.crd.york.ac.uk/prospero/)

### 2. Execute the Search
- [ ] Copy search strings into PubMed, Embase, Cochrane, CINAHL
- [ ] Import results into reference manager (Zotero, EndNote, Covidence)
- [ ] Run de-duplication

### 3. Screen Studies
- [ ] Title/abstract screening (2 independent reviewers recommended)
- [ ] Full-text screening with documented exclusion reasons
- [ ] Record PRISMA flow diagram numbers

### 4. Extract Data
- [ ] Use extraction_template.json as your extraction form
- [ ] Pilot on 3-5 studies first, refine form
- [ ] Dual extraction recommended for critical outcomes

### 5. Run Meta-Analysis
- [ ] Populate extracted_data.csv with actual study data
- [ ] Install R and required packages (metafor, ggplot2)
- [ ] Run `Rscript 05_meta_analysis.R`
- [ ] Review forest plot, funnel plot, heterogeneity statistics

### 6. Complete Manuscript
- [ ] Fill in actual results in manuscript draft
- [ ] Verify all 27 PRISMA items are addressed
- [ ] Add PRISMA flow diagram with real numbers
- [ ] Peer review before submission

## R Requirements

```r
install.packages(c("metafor", "ggplot2", "dplyr", "readr"))
```

Run: `Rscript 05_meta_analysis.R` from this directory.
