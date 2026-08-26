# HIPAA policy profile

Reference: https://cphs.berkeley.edu/hipaa/hipaa18.html

## What is PHI

Protected Health Information (PHI) is any information in the medical record or
designated record set that can be used to identify an individual and that was
created, used, or disclosed in the course of providing a health care service
(diagnosis, treatment, payment, or health-care operations).

Two things must both be true before information is PHI:

1. It can identify an individual, AND
2. It is associated with or derived from a health-care service event and/or
   entered into a medical record.

**Health information by itself, without any of the 18 identifiers, is NOT PHI.**
(e.g. a table of vital signs with no identifiers is not PHI; the same data plus
a medical record number makes the whole set PHI.)

**Research Health Information (RHI)** kept only in a researcher's records and not
entered into a medical record or used for treatment/payment/operations is not covered
by HIPAA (though other human-subjects protections still apply).

## The 18 identifiers (with this skill's mapping)

| # | Identifier | Detectable here? | Entity type |
|---|---|---|---|
| 1 | Names | Via local Presidio (PERSON), or a manual box when the party is referred to by role | `PERSON` (presidio) / manual |
| 2 | Geographic subdivisions smaller than a State (street addr, city, county, precinct, zip & geocodes) | ZIP codes only. Street addresses are unreliable from OCR; add a manual box. Note the 3-digit zip >20,000-people exception. | `ZIP_CODE` |
| 3 | Dates directly related to an individual (birth, admission, discharge, death; ages over 89) | Date-like tokens. NOT every date on a page is PHI — review each; only person-related clinical/demographic dates count. | `DATE`, `DATE_OF_BIRTH` |
| 4 | Phone numbers | Yes | `PHONE_NUMBER` |
| 5 | Fax numbers | Same digit shape as phone | `PHONE_NUMBER` |
| 6 | E-mail addresses | Yes | `EMAIL_ADDRESS` |
| 7 | Social Security numbers | Yes | `US_SSN` |
| 8 | Medical record numbers | Context-anchored (MRN / Medical Record) | `ID_NUMBER` |
| 9 | Health plan beneficiary numbers | Context-anchored (Beneficiary) | `ID_NUMBER` |
| 10 | Account numbers | Context-anchored (Account / Acct) | `ID_NUMBER` |
| 11 | Certificate / license numbers | Context-anchored (License / Cert) | `ID_NUMBER` |
| 12 | Vehicle identifiers & serial numbers (incl. license plates) | VIN shape (17 chars) | `VEHICLE_IDENTIFIER` |
| 13 | Device identifiers & serial numbers | Context-anchored (Serial / Device) | `ID_NUMBER` |
| 14 | URLs | Yes | `URL` |
| 15 | IP addresses | Yes | `IP_ADDRESS` |
| 16 | Biometric identifiers (finger/voice prints) | Not OCR-detectable — manual box | manual |
| 17 | Full-face photos & comparable images | Not OCR-text-detectable — manual box / image detector | manual |
| 18 | Any other unique identifying number/characteristic/code | Covered by the context-anchored `ID_NUMBER` + review | `ID_NUMBER` |

## Running it

```bash
python "${HERMES_SKILL_DIR}/scripts/ocr_redact.py" scan input.pdf \
  --policy hipaa --output plan.json --dpi 200
```

For a mostly-native-text health document, add a text-layer pass:

```bash
python "${HERMES_SKILL_DIR}/scripts/ocr_redact.py" scan-text input.pdf \
  --policy hipaa --output plan-text.json
```

Detection is additive: review the merged plan, add manual boxes for identifiers
that are not format-detectable (names without Presidio, signatures, faces, VOIP
biometrics, street addresses), then apply.

## Cautions / limits

- **Not every date is PHI.** Filing/admission-to-study dates are not necessarily
  treatment dates. The `DATE` recognizer over-flags on purpose; a human reviewer
  must decide which dates are "directly related to an individual."
- Signature blocks, faces, photographs, and barcodes require separate detectors
  or manual boxes; OCR alone is not sufficient.
- A passing automated pass is **not** a HIPAA compliance certification. It is a
  tool output to be reviewed by a person with authority over the data.
- Student health records may instead be FERPA records — see `ferpa.md`.
- When a policy requires preservation of full primary-key columns (e.g., an ID
  needed for re-linkage), tokenization may be preferred over redaction; this
  skill's default stored value is a SHA-256 fingerprint, never the plaintext.