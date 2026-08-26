# Local installation notes

1. Install Tesseract OCR using your operating system's package manager or approved local software distribution process.
2. Install Python dependencies into a local virtual environment if desired:

   `python -m pip install -r requirements-core.txt`

3. Optional named-entity detection via **Microsoft Presidio** (https://github.com/data-privacy-stack/presidio):

   `python -m pip install -r requirements-presidio-optional.txt`
   `python -m spacy download en_core_web_lg`   # ~400 MB, one-time; offline after

   Presidio commonly needs a compatible local NLP model. Keep that model local; this skill does not require or start the Presidio HTTP server.
4. Run `python scripts/check_dependencies.py`.
5. Copy the entire `ocr-redaction-local` directory under `~/.hermes/skills/` (optionally inside a category directory), or install it through your normal trusted Hermes skill workflow.

Dependencies are not installed automatically by the skill.
