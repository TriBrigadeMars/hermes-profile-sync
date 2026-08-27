# Integrity Verification Protocol

## Purpose

Blocking verification gate applied at Stage 2.5 (pre-review) and Stage 4.5 (pre-finalization). Ensures reference accuracy, citation integrity, data validity, originality, and claim fidelity before the paper proceeds to review or publication.

## 5-Phase Verification

### Phase 1: Reference Existence
- Every reference in the bibliography must be accessible (DOI resolves, URL reachable, or physical source locatable)
- Flag: Broken DOIs, 404 URLs, paywalled sources without institutional access noted
- Tool: `web_extract` for URL checks, `mcp_arxiv_get_abstract` for arXiv papers

### Phase 2: Citation Accuracy
- In-text citations must match the bibliography
- Citation format must conform to declared style (APA 7.0 / Chicago / MLA / IEEE / Vancouver)
- No missing citations for claims marked as requiring support
- No orphaned bibliography entries (cited in text but missing from bib, or vice versa)

### Phase 3: Data & Figure Integrity
- All data points traceable to stated source
- Figure captions match figure content
- Statistical claims match source values (within rounding tolerance)
- No uncredited reproduction of figures/tables

### Phase 4: Originality Screening
- Proper attribution for all quoted/paraphrased material
- Distinction between source claims and author's original claims clearly marked
- AI-assisted text flagged per venue requirements
- Plagiarism risk assessment (red-flag verbatim passages)

### Phase 5: Claims Verification
- Every empirical claim has a source anchor
- Every theoretical claim is either (a) attributed to originator, or (b) explicitly framed as author's argument
- No conflation of correlation and causation without appropriate hedging
- Confidence levels match evidence strength

## 7-Mode AI Research Failure Mode Checklist

For each of the following, verify NONE are present:

1. **Implementation bugs**: Method description does not match claimed procedure
2. **Hallucinated results**: Statistics, findings, or numbers not in cited sources
3. **Citation hallucinations**: References that do not exist or do not support the claim
4. **Frame-lock**: Ignoring contradictory evidence or alternative interpretations
5. **Sycophancy**: Uncritical adoption of user preferences against evidence
6. **Methodology fabrication**: Described methods that were not actually performed
7. **Overgeneralization**: Claims exceeding the scope of the evidence presented

## Gate Rules

- Stage 2.5: FAIL → fix and re-verify (max 3 rounds) → PASS → proceed to Stage 3
- Stage 4.5: Must achieve **zero issues** from scratch. Any issue blocks Stage 5.
- Output: Integrity report with per-phase PASS/FAIL, issue list with severity (CRITICAL/MAJOR/MINOR), and remediation instructions.
