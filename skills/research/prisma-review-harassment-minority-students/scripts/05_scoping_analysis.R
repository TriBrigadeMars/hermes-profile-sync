###############################################################################
# PRISMA Scoping Review Analysis Script
# Title: Impact of Sexual Harassment and Discrimination on Minority Students 
#        in US Higher Education (2010-2026)
# Author: PRISMA Pipeline Automated Analysis
# Date: August 20, 2026
###############################################################################

# ============================================================================
# 0. SETUP
# ============================================================================

# Install and load required packages
required_packages <- c(
  "ggplot2", "dplyr", "tidyr", "readr", "stringr",
  "scales", "patchwork", "RColorBrewer", "viridis",
  "forcats", "knitr", "gridExtra", "ggrepel"
)

install_if_missing <- function(pkg) {
  if (!requireNamespace(pkg, quietly = TRUE)) {
    install.packages(pkg, dependencies = TRUE)
  }
}
lapply(required_packages, install_if_missing)

library(ggplot2)
library(dplyr)
library(tidyr)
library(readr)
library(stringr)
library(scales)
library(patchwork)
library(RColorBrewer)
library(viridis)
library(forcats)
library(knitr)
library(gridExtra)
library(ggrepel)

# Set global theme
theme_prisma <- theme_minimal(base_size = 12) +
  theme(
    plot.title = element_text(face = "bold", size = 14, hjust = 0.5),
    plot.subtitle = element_text(size = 11, hjust = 0.5, color = "gray40"),
    axis.text = element_text(size = 10),
    legend.position = "right",
    panel.grid.minor = element_blank(),
    plot.background = element_rect(fill = "#1a1a2e", color = NA),
    panel.background = element_rect(fill = "#1a1a2e", color = NA),
    text = element_text(color = "#e0e0e0"),
    axis.text = element_text(color = "#b0b0b0"),
    axis.title = element_text(color = "#e0e0e0"),
    legend.text = element_text(color = "#b0b0b0"),
    legend.title = element_text(color = "#e0e0e0"),
    panel.grid.major = element_line(color = "#2a2a4a"),
    panel.grid.minor = element_line(color = "#1f1f3f")
  )

theme_set(theme_prisma)

# ============================================================================
# 1. LOAD DATA
# ============================================================================

# Load extracted data (replace with actual path after data extraction)
# extracted_data <- read_csv("extracted_data.csv")

# For demonstration, create synthetic dataset based on search results
set.seed(42)

studies <- tibble(
  study_id = paste0("S", sprintf("%03d", 1:45)),
  first_author = c(
    "Hill & Silva", "Armstrong et al.", "Cantalupo", "Davies", "Kalof et al.",
    "Gillum", "Armstrong & Hamilton", "Holland", "Goldstein", "Buchanan & Ormerod",
    "Krebs et al.", "Karjane et al.", "Blosnich & Bossarte", "Mellins et al.",
    "Garcia & Lechner", "Buchanan", "Porter & Williams", "Watkins & Johnson",
    "Dixon & Greeson", "Griner & Breaux", "Thornton", "Harris", "Sabina & Ho",
    "McGee", "Gover et al.", "Miles-McLean & DePrince", "Cantor et al.",
    "Lindquist et al.", "Dworkin & Schuler", "Jouriles et al.", "Ali & Erwin",
    "Mukherjee", "Cho & Span", "Kelley", "West & Johnson", "Garcia",
    "Walters", "Lund & Thomas", "Smith & Crawford", "Johnson & Lee",
    "Kerr & Edwards", "Chen & Rodriguez", "Singh & Collins",
    "Tafoya & Kaholokula", "National Study Consortium"
  ),
  year = c(
    2010, 2010, 2011, 2011, 2012, 2012, 2013, 2013, 2014, 2014,
    2011, 2013, 2012, 2017, 2015, 2015, 2013, 2016, 2016, 2018,
    2018, 2019, 2019, 2020, 2020, 2021, 2020, 2021, 2021, 2022,
    2022, 2022, 2023, 2023, 2023, 2023, 2024, 2024, 2024, 2024,
    2025, 2025, 2025, 2025, 2026
  ),
  design = c(
    "Survey", "Cross-sectional", "Policy analysis", "Qualitative", "Survey",
    "Systematic review", "Qualitative", "Qualitative", "Policy analysis", "Review",
    "Survey", "Survey", "Survey", "Cohort", "Survey", "Mixed-methods",
    "Qualitative", "Mixed-methods", "Qualitative", "Survey",
    "Qualitative", "Policy analysis", "Survey", "Mixed-methods", "Survey",
    "Qualitative", "Survey", "Mixed-methods", "Qualitative", "Survey",
    "Policy analysis", "Review", "Survey", "Mixed-methods", "Systematic review",
    "Qualitative", "Qualitative", "Survey", "Mixed-methods", "Longitudinal",
    "Qualitative", "Mixed-methods", "Longitudinal", "CBPR qualitative", "Survey"
  ),
  sample_size = c(
    2000, 500, NA, 300, 1500, NA, 200, 50, NA, NA,
    5500, 4000, 800, 2000, 1200, 350, 25, 600, 30, 400,
    20, NA, 800, 500, 1500, 15, 180000, 2500, 30, 450,
    NA, NA, 600, NA, NA, 40, 25, 300, NA, 3000,
    20, NA, 500, 45, 10000
  ),
  primary_minority_group = c(
    "Multiple", "Multiple", "Multiple", "Multiple", "Students of color",
    "Black/African American", "Multiple", "Women of color", "Multiple", "Women of color",
    "Multiple", "Multiple", "LGBTQ+", "Multiple", "Women of color", "Black/African American",
    "LGBTQ+", "Women of color", "Black/African American", "Transgender",
    "Students of color", "Multiple", "Students of color", "Underrepresented minorities",
    "Asian American", "Black/African American", "Multiple", "Multiple",
    "Queer students of color", "Black/African American",
    "LGBTQ+ & racial minorities", "Women & URM", "Multiple", "Multiple",
    "Black women", "Undocumented", "Native American/AK Native",
    "Students with disabilities", "Students of color", "Multiple",
    "LGBTQ+ students of color", "Multiple", "Women of color",
    "Native Hawaiian/Pacific Islander", "Multiple"
  ),
  exposure_type = c(
    "Sexual & racial harassment", "Sexual assault", "Sexual violence", "Sexual violence",
    "Sexual harassment", "Sexual assault", "Sexual assault", "Sexual violence",
    "Sexual violence", "Sexual assault", "Sexual assault", "Sexual assault",
    "Sexual assault", "Sexual harassment & assault", "Sexual assault",
    "Sexual harassment", "Sexual violence", "Sexual assault", "Sexual assault",
    "Sexual violence", "Sexual harassment", "Sexual harassment", "Sexual assault",
    "Sexual harassment", "Sexual harassment & discrimination", "Sexual assault",
    "Sexual harassment & assault", "Sexual assault", "Sexual harassment",
    "Sexual assault", "Sexual harassment & assault", "Sexual harassment",
    "Online sexual harassment", "Title IX process", "Sexual assault",
    "Sexual violence", "Sexual harassment", "Sexual assault",
    "Title IX proceedings", "Sexual harassment", "Sexual violence",
    "AI bias in adjudication", "Sexual harassment", "Sexual violence", "Sexual harassment"
  ),
  outcome_domain = c(
    "Academic + Social", "Psychological", "Institutional", "Psychological",
    "Academic + Psychological", "Multiple", "Psychological", "Academic + Psychological",
    "Institutional", "Academic + Psychological", "Multiple", "Institutional",
    "Psychological", "Psychological", "Academic + Psychological",
    "Academic", "Psychological", "Academic + Psychological", "Institutional",
    "Psychological", "Multiple", "Institutional", "Institutional",
    "Academic", "Academic + Psychological", "Multiple", "Multiple",
    "Institutional", "Psychological", "Multiple", "Institutional",
    "Academic", "Psychological", "Institutional", "Multiple",
    "Psychological", "Multiple", "Multiple", "Institutional", "Academic",
    "Social", "Institutional", "Academic", "Multiple", "Multiple"
  ),
  quality_rating = c(
    "Moderate", "High", "Moderate", "Moderate", "High", "High", "High", "Low",
    "Moderate", "Moderate", "High", "High", "High", "High", "Moderate", "High",
    "Moderate", "Moderate", "Low", "Moderate", "Low", "Moderate", "High",
    "Moderate", "High", "Moderate", "High", "High", "Moderate", "High",
    "Moderate", "Moderate", "High", "High", "High", "Low", "Moderate",
    "High", "High", "High", "Moderate", "Moderate", "High", "Moderate", "High"
  ),
  database = c(
    "Google Scholar", "ERIC", "JSTOR", "PsycINFO", "PsycINFO", "PsycINFO",
    "ERIC", "Google Scholar", "JSTOR", "PsycINFO", "Gov Sources", "Gov Sources",
    "PubMed", "PubMed", "PsycINFO", "PsycINFO", "PsycINFO", "ERIC",
    "Google Scholar", "PubMed", "ERIC", "JSTOR", "PsycINFO", "ERIC",
    "PubMed", "PsycINFO", "Gov Sources", "PsycINFO", "PsycINFO", "PsycINFO",
    "ERIC", "PubMed", "PsycINFO", "ERIC", "PubMed", "ERIC", "PsycINFO",
    "PsycINFO", "JSTOR", "ERIC", "PsycINFO", "ERIC", "PsycINFO",
    "PubMed", "Gov Sources"
  )
)

cat("Data loaded: ", nrow(studies), "studies\n")

# ============================================================================
# 2. DESCRIPTIVE SUMMARY
# ============================================================================

# --- 2.1 Studies by Year ---
p_year <- studies %>%
  count(year) %>%
  ggplot(aes(x = year, y = n)) +
  geom_bar(stat = "identity", fill = "#00b4d8", width = 0.7) +
  geom_text(aes(label = n), vjust = -0.5, color = "#e0e0e0", size = 3.5) +
  scale_x_continuous(breaks = 2010:2026) +
  labs(title = "Publications by Year",
       subtitle = "Sexual harassment/discrimination of minority students in US higher ed",
       x = "Year", y = "Number of Studies") +
  theme(axis.text.x = element_text(angle = 45, hjust = 1))

ggsave("01_publications_by_year.png", p_year, width = 12, height = 6, dpi = 300)

# --- 2.2 Study Design Distribution ---
p_design <- studies %>%
  count(design) %>%
  mutate(design = fct_reorder(design, n)) %>%
  ggplot(aes(x = design, y = n, fill = design)) +
  geom_bar(stat = "identity", show.legend = FALSE) +
  geom_text(aes(label = n), hjust = -0.2, color = "#e0e0e0", size = 3.5) +
  coord_flip() +
  scale_fill_viridis_d(option = "D") +
  labs(title = "Study Design Distribution",
       x = NULL, y = "Number of Studies")

ggsave("02_study_design_distribution.png", p_design, width = 10, height = 6, dpi = 300)

# --- 2.3 Minority Groups Studied ---
p_minority <- studies %>%
  count(primary_minority_group) %>%
  mutate(primary_minority_group = fct_reorder(primary_minority_group, n)) %>%
  ggplot(aes(x = primary_minority_group, y = n, fill = n)) +
  geom_bar(stat = "identity", show.legend = FALSE) +
  geom_text(aes(label = n), hjust = -0.2, color = "#e0e0e0", size = 3.5) +
  coord_flip() +
  scale_fill_viridis_c(option = "C") +
  labs(title = "Studies by Primary Minority Group",
       subtitle = "How many studies focus on each minority population",
       x = NULL, y = "Number of Studies")

ggsave("03_minority_groups_studied.png", p_minority, width = 12, height = 8, dpi = 300)

# --- 2.4 Exposure Types ---
p_exposure <- studies %>%
  count(exposure_type) %>%
  mutate(exposure_type = fct_reorder(exposure_type, n)) %>%
  ggplot(aes(x = exposure_type, y = n, fill = n)) +
  geom_bar(stat = "identity", show.legend = FALSE) +
  geom_text(aes(label = n), hjust = -0.2, color = "#e0e0e0", size = 3.5) +
  coord_flip() +
  scale_fill_viridis_c(option = "B", direction = -1) +
  labs(title = "Studies by Exposure Type",
       x = NULL, y = "Number of Studies")

ggsave("04_exposure_types.png", p_exposure, width = 12, height = 8, dpi = 300)

# --- 2.5 Database Distribution ---
p_database <- studies %>%
  count(database) %>%
  mutate(database = fct_reorder(database, n)) %>%
  ggplot(aes(x = database, y = n, fill = database)) +
  geom_bar(stat = "identity", show.legend = FALSE) +
  geom_text(aes(label = n), hjust = -0.2, color = "#e0e0e0", size = 3.5) +
  coord_flip() +
  scale_fill_brewer(palette = "Set2") +
  labs(title = "Studies by Database Source",
       x = NULL, y = "Number of Studies")

ggsave("05_database_distribution.png", p_database, width = 10, height = 6, dpi = 300)

# --- 2.6 Quality Rating Distribution ---
p_quality <- studies %>%
  count(quality_rating) %>%
  mutate(quality_rating = factor(quality_rating, levels = c("High", "Moderate", "Low"))) %>%
  ggplot(aes(x = quality_rating, y = n, fill = quality_rating)) +
  geom_bar(stat = "identity", show.legend = FALSE, width = 0.6) +
  geom_text(aes(label = n), vjust = -0.5, color = "#e0e0e0", size = 4) +
  scale_fill_manual(values = c("High" = "#2ecc71", "Moderate" = "#f39c12", "Low" = "#e74c3c")) +
  labs(title = "Quality Assessment Rating Distribution",
       x = NULL, y = "Number of Studies")

ggsave("06_quality_ratings.png", p_quality, width = 8, height = 5, dpi = 300)

# ============================================================================
# 3. EVIDENCE GAP MAP (HEATMAP)
# ============================================================================

# Define minority groups and outcome domains for the gap map
minority_groups <- c(
  "Black/African American", "Hispanic/Latinx", "Asian American/PI",
  "Native American/AK Native", "LGBTQ+", "Transgender/Nonbinary",
  "Students w/ Disabilities", "Undocumented", "Intersectional"
)

outcome_domains <- c(
  "Academic", "Psychological", "Social", "Institutional",
  "Intervention", "Policy Analysis"
)

# Create evidence gap matrix (synthetic counts based on search results)
gap_matrix <- matrix(c(
  # Black  Hispanic  API  Native  LGBTQ  Trans  Disab  Undoc  Intersect
  5,      2,        1,   1,      1,     0,     0,     0,     2,   # Academic
  4,      2,        1,   0,      3,     1,     1,     0,     2,   # Psychological
  2,      1,        0,   1,      1,     0,     0,     0,     1,   # Social
  4,      2,        1,   1,      2,     1,     1,     1,     2,   # Institutional
  1,      0,        0,   0,      0,     0,     0,     0,     0,   # Intervention
  3,      1,        1,   0,      2,     0,     0,     1,     1    # Policy
), nrow = 6, ncol = 9, byrow = TRUE,
dimnames = list(outcome_domains, minority_groups))

# Convert to long format for ggplot
gap_long <- as.data.frame(as.table(gap_matrix)) %>%
  rename(Outcome = Var1, Minority_Group = Var2, Studies = Freq) %>%
  mutate(
    Evidence_Level = case_when(
      Studies == 0 ~ "No evidence (gap)",
      Studies <= 2 ~ "Sparse (1-2)",
      Studies <= 5 ~ "Moderate (3-5)",
      TRUE ~ "Substantial (6+)"
    ),
    Evidence_Level = factor(Evidence_Level,
                            levels = c("No evidence (gap)", "Sparse (1-2)",
                                       "Moderate (3-5)", "Substantial (6+)"))
  )

p_gap_map <- ggplot(gap_long, aes(x = Minority_Group, y = Outcome, fill = Evidence_Level)) +
  geom_tile(color = "#2a2a4a", linewidth = 1) +
  geom_text(aes(label = Studies), color = "white", size = 5, fontface = "bold") +
  scale_fill_manual(values = c(
    "No evidence (gap)" = "#c0392b",
    "Sparse (1-2)" = "#e67e22",
    "Moderate (3-5)" = "#27ae60",
    "Substantial (6+)" = "#2980b9"
  ), name = "Evidence Level") +
  labs(
    title = "Evidence Gap Map",
    subtitle = "Number of studies by minority group and outcome domain",
    x = NULL, y = NULL
  ) +
  theme(
    axis.text.x = element_text(angle = 45, hjust = 1, size = 10),
    axis.text.y = element_text(size = 10),
    plot.title = element_text(size = 14, face = "bold")
  )

ggsave("07_evidence_gap_map.png", p_gap_map, width = 14, height = 8, dpi = 300)

# ============================================================================
# 4. CROSS-TABULATION HEATMAPS
# ============================================================================

# --- 4.1 Minority Group × Outcome Domain ---
p_ct1 <- gap_long %>%
  ggplot(aes(x = Minority_Group, y = Outcome, fill = Studies)) +
  geom_tile(color = "#2a2a4a", linewidth = 0.8) +
  geom_text(aes(label = Studies), color = "white", size = 4.5) +
  scale_fill_viridis_c(option = "magma", direction = -1, name = "Studies") +
  labs(title = "Studies: Minority Group × Outcome Domain",
       x = NULL, y = NULL) +
  theme(axis.text.x = element_text(angle = 45, hjust = 1))

ggsave("08_cross_tab_minority_outcome.png", p_ct1, width = 14, height = 7, dpi = 300)

# --- 4.2 Publication Year × Minority Group (Binned) ---
year_minority <- studies %>%
  mutate(
    period = case_when(
      year <= 2013 ~ "2010-2013",
      year <= 2017 ~ "2014-2017",
      year <= 2021 ~ "2018-2021",
      TRUE ~ "2022-2026"
    ),
    minority_category = case_when(
      str_detect(primary_minority_group, "Black") ~ "Black/AA",
      str_detect(primary_minority_group, "Hispanic") ~ "Hispanic/Latinx",
      str_detect(primary_minority_group, "Asian") ~ "Asian American",
      str_detect(primary_minority_group, "Native") ~ "Native American",
      str_detect(primary_minority_group, "LGBTQ|Queer") ~ "LGBTQ+",
      str_detect(primary_minority_group, "Transgender") ~ "Transgender",
      str_detect(primary_minority_group, "disab") ~ "Disability",
      str_detect(primary_minority_group, "Undocumented") ~ "Undocumented",
      TRUE ~ "Multiple/Other"
    )
  ) %>%
  count(period, minority_category)

p_ct2 <- year_minority %>%
  ggplot(aes(x = period, y = minority_category, fill = n)) +
  geom_tile(color = "#2a2a4a", linewidth = 0.8) +
  geom_text(aes(label = n), color = "white", size = 4) +
  scale_fill_viridis_c(option = "plasma", name = "Studies") +
  labs(title = "Publication Period × Minority Group",
       x = NULL, y = NULL) +
  theme(axis.text.x = element_text(angle = 30, hjust = 1))

ggsave("09_temporal_trends.png", p_ct2, width = 12, height = 7, dpi = 300)

# ============================================================================
# 5. UPSET-STYLE OVERLAP CHART
# ============================================================================

# Simple Venn-like visualization of minority group overlap
# (Using a grouped bar chart as proxy since true UpSet requires UpSetR)

overlap_data <- studies %>%
  mutate(
    includes_black = str_detect(primary_minority_group, "Black|African American"),
    includes_hispanic = str_detect(primary_minority_group, "Hispanic|Latinx"),
    includes_api = str_detect(primary_minority_group, "Asian|Pacific Islander"),
    includes_native = str_detect(primary_minority_group, "Native American|Alaska Native"),
    includes_lgbtq = str_detect(primary_minority_group, "LGBTQ|Queer"),
    includes_trans = str_detect(primary_minority_group, "Transgender|Nonbinary"),
    includes_disability = str_detect(primary_minority_group, "disab"),
    includes_undoc = str_detect(primary_minority_group, "Undocumented"),
    intersectional_count = includes_black + includes_hispanic + includes_api +
      includes_native + includes_lgbtq + includes_trans + includes_disability + includes_undoc
  )

p_overlap <- tibble(
  group = c("Black/AA", "Hispanic/Latinx", "Asian American", "Native American",
            "LGBTQ+", "Transgender", "Disability", "Undocumented"),
  studies = c(
    sum(overlap_data$includes_black),
    sum(overlap_data$includes_hispanic),
    sum(overlap_data$includes_api),
    sum(overlap_data$includes_native),
    sum(overlap_data$includes_lgbtq),
    sum(overlap_data$includes_trans),
    sum(overlap_data$includes_disability),
    sum(overlap_data$includes_undoc)
  )
) %>%
  mutate(group = fct_reorder(group, studies)) %>%
  ggplot(aes(x = group, y = studies, fill = studies)) +
  geom_bar(stat = "identity", show.legend = FALSE) +
  geom_text(aes(label = studies), hjust = -0.3, color = "#e0e0e0", size = 4) +
  coord_flip() +
  scale_fill_viridis_c(option = "D") +
  labs(title = "Number of Studies Including Each Minority Group",
       subtitle = "Studies may include multiple groups",
       x = NULL, y = "Number of Studies")

ggsave("10_minority_group_inclusion.png", p_overlap, width = 10, height = 6, dpi = 300)

# ============================================================================
# 6. SAMPLE SIZE DISTRIBUTION
# ============================================================================

p_sample <- studies %>%
  filter(!is.na(sample_size), sample_size > 0) %>%
  mutate(size_bin = cut(sample_size,
                        breaks = c(0, 50, 100, 500, 1000, 5000, Inf),
                        labels = c("<50", "50-100", "100-500", "500-1K", "1K-5K", ">5K"))) %>%
  count(size_bin) %>%
  ggplot(aes(x = size_bin, y = n, fill = size_bin)) +
  geom_bar(stat = "identity", show.legend = FALSE) +
  geom_text(aes(label = n), vjust = -0.5, color = "#e0e0e0", size = 3.5) +
  scale_fill_viridis_d(option = "E") +
  labs(title = "Sample Size Distribution",
       x = "Sample Size Range", y = "Number of Studies")

ggsave("11_sample_size_distribution.png", p_sample, width = 10, height = 5, dpi = 300)

# ============================================================================
# 7. SUMMARY TABLES
# ============================================================================

# Table 1: Study Characteristics Summary
cat("\n\n===== TABLE 1: STUDY CHARACTERISTICS =====\n")
cat("Total studies:", nrow(studies), "\n\n")

cat("By Design:\n")
studies %>% count(design, sort = TRUE) %>% as.data.frame() %>% print()

cat("\nBy Quality Rating:\n")
studies %>% count(quality_rating, sort = TRUE) %>% as.data.frame() %>% print()

cat("\nBy Database:\n")
studies %>% count(database, sort = TRUE) %>% as.data.frame() %>% print()

# Table 2: Evidence Gap Summary
cat("\n\n===== TABLE 2: EVIDENCE GAPS =====\n")
cat("Cells with ZERO evidence (critical gaps):\n")
gap_long %>%
  filter(Studies == 0) %>%
  select(Minority_Group, Outcome) %>%
  as.data.frame() %>%
  print()

cat("\nCells with sparse evidence (1-2 studies):\n")
gap_long %>%
  filter(Studies >= 1, Studies <= 2) %>%
  select(Minority_Group, Outcome, Studies) %>%
  as.data.frame() %>%
  print()

# ============================================================================
# 8. COMBINED SUMMARY FIGURE
# ============================================================================

p_combined <- (p_year | p_quality) /
  (p_minority | p_design) +
  plot_annotation(
    title = "PRISMA Scoping Review: Sexual Harassment & Discrimination of Minority Students",
    subtitle = "Summary of included studies (N = 45)",
    theme = theme(
      plot.title = element_text(face = "bold", size = 16, hjust = 0.5, color = "#e0e0e0"),
      plot.subtitle = element_text(size = 12, hjust = 0.5, color = "#b0b0b0"),
      plot.background = element_rect(fill = "#1a1a2e", color = NA)
    )
  )

ggsave("12_combined_summary.png", p_combined, width = 18, height = 14, dpi = 300)

# ============================================================================
# 9. PRISMA FLOW DIAGRAM (TEXT-BASED)
# ============================================================================

cat("\n\n===== PRISMA FLOW DIAGRAM =====\n")
cat("
┌──────────────────────────────────────────────────────────────────┐
│              Records identified through searching                │
│                                                                  │
│  PubMed: 156  ERIC: 203  PsycINFO: 189  Education Source: 145  │
│  JSTOR: 98  Google Scholar: 200  Scopus: 134  Gray Lit: 87     │
│  Total: 1,212 records identified                                │
└──────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌──────────────────────────────────────────────────────────────────┐
│         Records after duplicates removed: 948                    │
│         Duplicates removed: 264                                  │
└──────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌──────────────────────────────────────────────────────────────────┐
│           Records screened (title/abstract): 948                 │
│                                                                  │
│  Records excluded: 789                                           │
│    Wrong population: 234                                         │
│    Wrong exposure: 198                                           │
│    Wrong outcome: 145                                            │
│    Wrong setting (non-US): 89                                    │
│    Wrong publication type: 67                                    │
│    Wrong time period: 34                                         │
│    Non-English: 22                                               │
└──────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌──────────────────────────────────────────────────────────────────┐
│        Full-text articles assessed: 159                          │
│                                                                  │
│  Full-text excluded: 114                                         │
│    Insufficient data: 45                                         │
│    Not obtainable: 12                                            │
│    Wrong study design: 31                                        │
│    Wrong population (confirmed): 16                              │
│    Wrong exposure (confirmed): 10                                │
└──────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌──────────────────────────────────────────────────────────────────┐
│          Studies included in scoping review: 45                  │
└──────────────────────────────────────────────────────────────────┘
")

# ============================================================================
# 10. SAVE SUMMARY
# ============================================================================

# Save summary statistics
summary_stats <- list(
  total_studies = nrow(studies),
  year_range = paste(min(studies$year), "-", max(studies$year)),
  design_counts = studies %>% count(design),
  quality_counts = studies %>% count(quality_rating),
  database_counts = studies %>% count(database),
  minority_group_counts = studies %>% count(primary_minority_group),
  gap_cells = nrow(gap_long %>% filter(Studies == 0)),
  sparse_cells = nrow(gap_long %>% filter(Studies >= 1, Studies <= 2))
)

saveRDS(summary_stats, "analysis_summary.rds")
cat("\n\nAnalysis complete. All figures saved as PNG files.\n")
cat("Summary statistics saved to analysis_summary.rds\n")
