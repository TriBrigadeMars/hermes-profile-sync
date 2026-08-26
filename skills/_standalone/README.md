# ocr-redaction-local

Privacy-first Hermes Agent skill for OCR-aware redaction of sensitive text in images and PDF documents.

The bundled scripts do not start servers or call remote APIs. Tesseract is used locally for OCR coordinates; PyMuPDF performs true PDF redaction; Pillow handles raster-image redaction. Microsoft Presidio support is optional and runs in-process when locally installed.

## Microsoft Presidio

Presidio (https://github.com/data-privacy-stack/presidio) is an MIT-licensed,
open-source library for detecting, redacting, masking, and anonymizing PII across
text, images, and structured data. It uses local NLP (spaCy) plus pattern matching,
and everything runs on this machine — no cloud PII API, no service fees.

This skill uses Presidio's in-process Python analyzer only (`presidio-analyzer`);
it never starts the Presidio HTTP server. Install it with:

```bash
python -m pip install -r "${HERMES_SKILL_DIR}/requirements-presidio-optional.txt"
python -m spacy download en_core_web_lg   # ~400 MB, one-time; offline afterwards
```

Then pass `--presidio` to `scan` / `scan-text` to add named-entity detection
(PERSON, LOCATION, ORGANIZATION, …). Both the FERPA and HIPAA policy profiles
admit `PERSON` so those detections flow into the plan for review.

See `SKILL.md` for Hermes workflow instructions and `references/methodology.md` for the local-skill design methodology.
