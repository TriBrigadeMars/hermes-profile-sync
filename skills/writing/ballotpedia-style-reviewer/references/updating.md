# Updating the Source Snapshots

The skill is intentionally local-first. The bundled source PDFs are snapshots supplied by the user, and Ballotpedia's guide states that its editorial guidance evolves over time.

## Replace a Ballotpedia Style Guide snapshot

1. Replace `sources/ballotpedia-style-guide.pdf` with the newer authorized copy.
2. If `pdftotext` is installed, run:
   ```bash
   python scripts/extract_style_guide.py sources/ballotpedia-style-guide.pdf references/ballotpedia-style-guide-full.txt
   ```
3. Review `references/quick-reference.md` for rules that changed materially.
4. Update `sources/manifest.json` with the new snapshot date and checksum.
5. Run the tests.

## Bias taxonomy / NPOV snapshots

The supplied copies are image-based PDFs and do not contain reliably extractable text. This package therefore uses curated operational digests in:
- `references/bias-taxonomy.md`
- `references/neutrality-principles.md`

When replacing those source PDFs, compare the new documents manually and update the digests if the policy text changed. Do not rely on silent OCR to update policy rules.

## Precedence after an update

Keep the same hierarchy unless the user explicitly changes it:
1. Ballotpedia Style Guide
2. Ballotpedia bias taxonomy
3. Wikipedia NPOV as complementary guidance
