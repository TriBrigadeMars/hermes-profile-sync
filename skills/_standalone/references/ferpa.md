# FERPA policy profile

Reference: https://ferpa.iu.edu/basics/index.html

## What is protected

The Family Educational Rights and Privacy Act protects the privacy of **student
education records** — records directly related to a student and maintained by an
institution or its agent (electronic files, paper, email, fax, notes, etc.).

Education records include *personally identifiable information (PII)* and
bio-demographic data, such as:

- Social Security number
- Date of birth
- Student ID / institutional identification
- Ethnicity, gender, relationship information
- Test scores, GPA, graded papers, exams, transcripts
- Advising notes
- Financial aid information

Any institution receiving funds under U.S. Department of Education programs is
bound by FERPA. FERPA rights transfer from parents to the student once the student
attends a post-secondary institution. A **disciplinary / investigative report**
about a student is an education record and is protected, not directory information.

## Directory information (PUBLIC — usually *not* redacted)

Institutions may release directory information without written consent unless the
student has opted out ("blocked"). At most institutions directory information
includes: name, hometown (city, state, ZIP), institutional e-mail, dates of
attendance, admission/enrollment status, campus/school/college/division/major,
class standing, degrees and awards, activities, and athletic information.

So: **do not auto-redact directory-type fields** (name, major, campus, dates of
attendance) when you know the student has not exercised a FERPA block — and
recognize that a policy decision is required. A redaction skill cannot know whether
a given student opted out; raise it for the user.

## Running it

```bash
python "${HERMES_SKILL_DIR}/scripts/ocr_redact.py" scan input.pdf \
  --policy ferpa --output plan.json --dpi 200

# Native-text investigative/education documents:
python "${HERMES_SKILL_DIR}/scripts/ocr_redact.py" scan-text input.pdf \
  --policy ferpa --output plan-text.json
```

The FERPA profile targets: SSN, date of birth, student/institutional ID
(`ID_NUMBER` context), ZIP, phone/fax, e-mail, credit-card candidates, and names
(via Presidio `PERSON`, or manually when parties are identified by name).

## Notes and limits

- **Directory info vs. opt-out is a policy question, not a detection question.**
  Surface directory-type fields for a human decision rather than silently
  redacting or retaining them.
- Academic content that is *not* directory info (transcripts, GPAs, exam scores,
  advising notes, disciplinary records, financial aid) should be redacted as
  protected PII when it appears.
- The `--policy ferpa` profile intentionally excludes the generic `DATE`
  recognizer (dates of attendance are directory information). Only
  `DATE_OF_BIRTH` is redacted. A `--policy hipaa` scan is called for when the
  record also contains clinical/admission dates.
- Student health records are subject to **FERPA**, not HIPAA.
- A passing automated pass is **not** a FERPA compliance certification.