import importlib.util, pathlib, tempfile
P=pathlib.Path(__file__).parents[1]/"scripts"/"ocr_redact.py"
spec=importlib.util.spec_from_file_location("ocr_redact",P); m=importlib.util.module_from_spec(spec); import sys; sys.modules["ocr_redact"]=m; spec.loader.exec_module(m)

def spans(text, allowed=None, presidio=False):
    return m.detect_spans(text, use_presidio=presidio, allowed=allowed)

def test_luhn():
    assert m.luhn_ok("4111 1111 1111 1111")
    assert not m.luhn_ok("4111 1111 1111 1112")

def test_detect_structured():
    text="Email jane@example.com SSN 123-45-6789 card 4111 1111 1111 1111"
    types={x[2] for x in m.detect_spans(text)}
    assert "EMAIL_ADDRESS" in types
    assert "US_SSN" in types
    assert "CREDIT_CARD" in types

def test_masking():
    assert "6789" in m.mask_value("US_SSN","123-45-6789")
    assert "j***@example.com" == m.mask_value("EMAIL_ADDRESS","jane@example.com")
    assert "[REDACTED_VIN]" == m.mask_value("VEHICLE_IDENTIFIER","1HGCM82633A004352")
    assert "[REDACTED_DOB]" == m.mask_value("DATE_OF_BIRTH","date of birth: 04/12/1987")
    assert "[REDACTED_DATE]" == m.mask_value("DATE","1/28/2026")
    assert "1245" in m.mask_value("ID_NUMBER","MRN 771245")

def test_hipaa_18_identifiers_detectable():
    # Covers the format-detectable subset of the HIPAA 18 identifiers.
    text=("DOB 04/12/1987 MRN 7712458 v 80204 Phone (303) 555-0199 "
          "email jane@example.com SSN 123-45-6789 VIN 1HGCM82633A004352 "
          "IP 10.0.0.1 url https://example.com acct 99887766")
    det=spans(text)
    got={x[2] for x in det}
    for want in ("DATE_OF_BIRTH","ID_NUMBER","ZIP_CODE","PHONE_NUMBER","EMAIL_ADDRESS",
                 "US_SSN","VEHICLE_IDENTIFIER","IP_ADDRESS","URL"):
        assert want in got, f"missing {want}"

def test_id_number_context_required():
    # A bare all-digit run without a context label should not be flagged as ID_NUMBER.
    det=spans("Account 99887766 serial 44882")
    got={x[2] for x in det}
    assert "ID_NUMBER" in got
    # 'serial killer' must not be treated as an identifier (no digit after label).
    assert "ID_NUMBER" not in {x[2] for x in spans("the serial killer fled")}

def test_ferpa_policy_filters():
    # FERPA profile: DOB/SSN/phone/email in scope; generic DATE excluded (dates of attendance are directory info).
    allowed=m.POLICY_ENTITIES["ferpa"]
    text="DOB 01/15/2001 SSN 123-45-6789 1/28/2026 (303) 555-0111"
    det=spans(text, allowed=allowed)
    types={x[2] for x in det}
    assert "DATE_OF_BIRTH" in types
    assert "US_SSN" in types
    assert "PHONE_NUMBER" in types
    assert "DATE" not in types, "FERPA should exclude generic DATE"

def test_hipaa_policy_filters():
    # HIPAA profile includes generic DATE (person-related dates are PHI) and VIN.
    allowed=m.POLICY_ENTITIES["hipaa"]
    det=spans("DOB 04/12/1987 1/28/2026 VIN 1HGCM82633A004352", allowed=allowed)
    types={x[2] for x in det}
    assert "DATE" in types
    assert "DATE_OF_BIRTH" in types
    assert "VEHICLE_IDENTIFIER" in types

def test_policy_person_allows_presidio():
    # Both profiles admit PERSON so --presidio can report names into the plan.
    assert "PERSON" in m.POLICY_ENTITIES["ferpa"]
    assert "PERSON" in m.POLICY_ENTITIES["hipaa"]

def test_scan_pdf_text_over_native_layer():
    # Build a tiny PDF whose text layer contains a FERPA/HIPAA identifier and
    # confirm the native-text pass finds it without OCR.
    try:
        import pymupdf
    except ImportError:
        import fitz as pymupdf
    with tempfile.TemporaryDirectory() as td:
        pdf=pathlib.Path(td)/"doc.pdf"
        d=pymupdf.open(); page=d.new_page(); page.insert_text((72,100),"Student ID 900123456 SSN 123-45-6789"); d.save(str(pdf)); d.close()
        dets,warns=m.scan_pdf_text(pdf,"eng","tesseract",allowed=m.POLICY_ENTITIES["ferpa"])
        types={x["entity_type"] for x in dets}
        assert "ID_NUMBER" in types, types
        assert "US_SSN" in types

def run_all():
    for n,v in sorted(list(globals().items())):
        if n.startswith("test_") and callable(v):
            v(); print(f"PASS {n}")

if __name__=="__main__":
    run_all()