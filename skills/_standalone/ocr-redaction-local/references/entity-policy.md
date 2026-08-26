# Entity Policy

## Default structured entities

The deterministic detector supports:

- EMAIL_ADDRESS
- US_SSN
- PHONE_NUMBER
- CREDIT_CARD (Luhn-valid candidate only)
- IP_ADDRESS
- URL
- ZIP_CODE
- DATE (generic date-like token; person-relevance must be reviewed)
- DATE_OF_BIRTH (birth-date labels: DOB / date of birth / born)
- VEHICLE_IDENTIFIER (VIN shape)
- ID_NUMBER (context-anchored: medical record, MRN, student ID, account, beneficiary, license/certificate, serial)

These recognizers are intentionally conservative and are not a complete
regulatory taxonomy. Several (ZIP_CODE, DATE, ID_NUMBER) over-flag on purpose and
rely on the human review step to separate true identifiers from document
metadata.

## Optional Presidio entities

When `presidio-analyzer` and its local NLP dependencies are installed, `--presidio`
can add recognizers supported by the local Presidio configuration, commonly
including PERSON, LOCATION, ORGANIZATION and additional structured identifiers.

Presidio is **Microsoft Presidio** — an MIT-licensed, open-source library for
detecting, redacting, masking, and anonymizing PII across text, images, and
structured data. It uses local NLP (spaCy) plus pattern matching and runs entirely
in-process on this machine. Source and docs: https://github.com/data-privacy-stack/presidio.

The skill uses Presidio as an in-process Python library (`presidio-analyzer`).
It must not launch the Presidio HTTP server.

## Policy profiles

A `--policy <name>` selects which entity types are included in a plan, so a job
can focus on the identifiers a framework actually protects. Profiles do not
suppress detection; they filter the plan a reviewer approves.

### `ferpa` — student education records

Targets PII from student education records. Directory information (name, major,
campus, ZIP, e-mail, dates of attendance) is public unless the student has opted
out, so those fields are intentionally left to a human decision rather than
silently redacted.

- Included: `US_SSN`, `DATE_OF_BIRTH`, `EMAIL_ADDRESS`, `PHONE_NUMBER`,
  `ID_NUMBER` (student/institutional IDs), `ZIP_CODE`, `CREDIT_CARD`, `PERSON`.
- Excluded: generic `DATE` (dates of attendance are directory information).
- See `ferpa.md`.

### `hipaa` — PHI / 18 identifiers

Targets the format-detectable subset of the HIPAA 18 identifiers when the content
is associated with health care. See `hipaa.md` for the full 18-identifier table.

- Included: `US_SSN`, `PHONE_NUMBER` (phone+fax), `EMAIL_ADDRESS`, `IP_ADDRESS`,
  `URL`, `DATE`, `DATE_OF_BIRTH`, `ZIP_CODE`, `ID_NUMBER` (MRN, beneficiary,
  account, license, serial), `VEHICLE_IDENTIFIER`, `CREDIT_CARD`, `PERSON`.
- Not OCR-detectable (manual box required): signatures, faces, biometrics,
  street addresses, barcodes/QR.
- `DATE` over-flags: not every date on a page is a person-related PHI date;
  a reviewer must decide.

### Default (no `--policy`)

All deterministic entity types above plus Presidio entities if enabled.

## Custom policies

For a compliance-specific derivative, define:

1. exact entity categories;
2. jurisdiction/country where relevant;
3. deterministic validation rules (checksums, formats, context words);
4. minimum detection confidence;
5. required handling action: redact, mask, tokenize, or manual review;
6. whether metadata, annotations, attachments, form fields, signatures, faces, barcodes, or QR codes are in scope;
7. mandatory verification steps and evidence to retain.

A policy profile should support compliance workflows but must not claim that the
skill alone establishes legal compliance.