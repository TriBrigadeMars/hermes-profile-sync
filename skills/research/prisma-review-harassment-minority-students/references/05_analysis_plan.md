# Stage 5 — Analysis Plan

## Overview
As a scoping review, the primary analytical goal is to **map the breadth and depth of evidence** rather than to synthesize effect sizes (as in a systematic review/meta-analysis). The analysis follows JBI scoping review methodology (Peters et al., 2020) and Arksey & O'Malley's (2005) framework for collating and summarizing findings.

---

## 1. Descriptive Numerical Summary

### 1.1 Study Characteristics Summary
A descriptive numerical summary will chart:

| Variable | Categories | Chart Type |
|----------|-----------|------------|
| Publication year | 2010–2026 (by year) | Line graph / bar chart |
| Study design | Cross-sectional, longitudinal, qualitative, mixed-methods, etc. | Bar chart |
| Geographic region | Northeast, Southeast, Midwest, Southwest, West, National | Map / bar chart |
| Institution type | 4-year public, 4-year private, 2-year, HBCU, HSI, etc. | Stacked bar chart |
| Sample size | Binned (<100, 100–500, 500–1000, >1000) | Histogram |
| Minority group studied | Racial/ethnic, LGBTQ+, disability, intersectional | Bar chart |
| Exposure type | Sexual harassment, assault, racial discrimination, intersectional | Bar chart |
| Outcome type | Academic, psychological, social, institutional | Bar chart |
| Quality rating | HIGH, MODERATE, LOW | Pie chart |
| Database source | PubMed, ERIC, PsycINFO, etc. | Bar chart |

### 1.2 Frequency Tables
- Frequency of each minority group studied
- Frequency of each exposure type
- Frequency of each outcome domain
- Frequency of each study design
- Cross-tabulation: minority group × outcome type
- Cross-tabulation: exposure type × minority group

---

## 2. Thematic Analysis

### 2.1 Approach
Thematic analysis follows Braun & Clarke's (2006) six-phase method applied to the extracted data:

1. **Familiarization**: Read all extracted data and key findings
2. **Initial coding**: Generate codes from key findings, minority-specific findings, intersectional findings
3. **Theme search**: Collate codes into candidate themes
4. **Theme review**: Check themes against coded extracts and full dataset
5. **Theme definition**: Name and define each theme
6. **Report production**: Select compelling extract examples, relate themes to research questions

### 2.2 Preliminary Theme Structure

#### Theme 1: Disproportionate Burden
- Minority students experience higher rates of sexual harassment and discrimination
- Intersectional identities compound vulnerability
- Specific forms of harassment (e.g., racialized sexual harassment) unique to minority students

#### Theme 2: Academic Consequences
- GPA decline, course withdrawal, degree incompletion
- Differential attrition by race/ethnicity and gender
- STEM pipeline effects for minority women
- Graduate education barriers

#### Theme 3: Psychological and Health Impact
- Elevated depression, anxiety, PTSD among minority survivors
- Substance use as coping mechanism
- Suicidal ideation and self-harm
- Compounding effects of racial trauma and sexual trauma

#### Theme 4: Social and Relational Effects
- Social isolation and withdrawal
- Distrust of institutions and peers
- Community-level impacts for minority student organizations
- Help-seeking barriers specific to minority communities

#### Theme 5: Institutional Responses and Failures
- Inadequate Title IX enforcement for minority students
- Reporting barriers (fear of retaliation, distrust, cultural factors)
- Institutional racism in adjudication processes
- Gaps in culturally responsive support services

#### Theme 6: Intersectionality as Framework
- Need for intersectional approaches to research and policy
- Current evidence insufficient for understanding intersectional experiences
- Methodological challenges of intersectional research

#### Theme 7: Interventions and Prevention
- Limited culturally adapted prevention programs
- Bystander intervention programs rarely tested with minority populations
- Promising practices in community-based and culturally grounded approaches

---

## 3. Evidence Gap Mapping

### 3.1 Gap Map Matrix
Create an evidence gap map (EGM) cross-referencing:

**Rows** = Minority Groups:
- Black/African American students
- Hispanic/Latinx students
- Asian American/Pacific Islander students
- Native American/Alaska Native students
- LGBTQ+ students
- Transgender/nonbinary students
- Students with disabilities
- Undocumented students
- Intersectional identities

**Columns** = Outcome Domains:
- Academic outcomes
- Psychological outcomes
- Social outcomes
- Institutional outcomes
- Intervention effectiveness
- Policy analysis

**Cell Values** = Number of studies (with color-coding):
- Red (0): No evidence — critical gap
- Yellow (1–2): Sparse evidence
- Green (3–5): Moderate evidence
- Dark green (6+): Substantial evidence

### 3.2 Gap Identification
- Identify cells with zero or minimal evidence
- Prioritize gaps by population vulnerability and policy relevance
- Recommend future research directions

---

## 4. Cross-Tabulation Analyses

| Analysis | Rows | Columns | Purpose |
|----------|------|---------|---------|
| CT-1 | Minority group | Study design | Methodological diversity by population |
| CT-2 | Minority group | Outcome domain | Outcome coverage by population |
| CT-3 | Exposure type | Outcome domain | Outcome coverage by exposure |
| CT-4 | Institution type | Minority group | Setting representation by population |
| CT-5 | Publication year | Minority group | Temporal trends in population focus |
| CT-6 | Publication year | Quality rating | Quality trends over time |

---

## 5. Visualizations

All visualizations will be produced in R using ggplot2 with a consistent theme (dark-themed or publication-ready).

### 5.1 Required Visualizations
1. **PRISMA Flow Diagram**: Study selection process
2. **Publication Timeline**: Studies by year (bar chart)
3. **Study Design Distribution**: Pie/donut chart
4. **Minority Group Coverage**: Horizontal bar chart
5. **Exposure Type Distribution**: Horizontal bar chart
6. **Outcome Domain Heatmap**: Minority group × Outcome domain matrix
7. **Evidence Gap Map**: Color-coded heatmap
8. **Geographic Distribution**: US map with study locations
9. **Quality Rating Distribution**: Stacked bar by study design
10. **Venn/UpSet Diagram**: Overlap of minority groups studied

---

## 6. Data Synthesis Narrative

The final synthesis will:
1. Describe the extent and nature of the evidence base
2. Identify patterns across studies (common findings, contradictions)
3. Map evidence gaps systematically
4. Identify methodological trends and limitations
5. Provide recommendations for future research, policy, and practice
6. Relate findings to the legislative context (Title IX, Title VI, Clery Act, VAWA)

---

## References

Arksey, H., & O'Malley, L. (2005). Scoping studies: Towards a methodological framework. *International Journal of Social Research Methodology*, *8*(1), 19–32.

Braun, V., & Clarke, V. (2006). Using thematic analysis in psychology. *Qualitative Research in Psychology*, *3*(2), 77–101.

Peters, M. D. J., et al. (2020). Chapter 11: Scoping reviews. In *JBI Manual for Evidence Synthesis*.
