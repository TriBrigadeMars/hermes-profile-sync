#!/usr/bin/env python3
"""Local OCR-aware redaction planner/applier/verifier.

No network calls. OCR uses a local Tesseract executable and TSV output.
PDF redaction uses PyMuPDF. Raster redaction uses Pillow.
"""
from __future__ import annotations
import argparse, csv, hashlib, io, ipaddress, json, os, re, subprocess, sys, tempfile
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable, List, Tuple, Optional

IMAGE_EXTS = {".png", ".jpg", ".jpeg", ".tif", ".tiff", ".bmp", ".webp"}
PDF_EXTS = {".pdf"}

PATTERNS = {
    "EMAIL_ADDRESS": re.compile(r"\b[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,}\b", re.I),
    "US_SSN": re.compile(r"(?<!\d)(?!000|666|9\d\d)\d{3}[- ]?(?!00)\d{2}[- ]?(?!0000)\d{4}(?!\d)"),
    "PHONE_NUMBER": re.compile(r"(?<!\d)(?:\+?1[-.\s]?)?(?:\(?\d{3}\)?[-.\s])\d{3}[-.\s]\d{4}(?!\d)"),
    "IP_ADDRESS": re.compile(r"(?<!\w)(?:\d{1,3}\.){3}\d{1,3}(?!\w)"),
    "URL": re.compile(r"\b(?:https?://|www\.)[^\s<>()]+\b", re.I),
    "CREDIT_CARD_CANDIDATE": re.compile(r"(?<!\d)(?:\d[ -]*?){13,19}(?!\d)"),
    # FERPA / HIPAA identifier additions
    "ZIP_CODE": re.compile(r"\b\d{5}(?:-\d{4})?\b"),
    "DATE": re.compile(r"\b(?:\d{1,2}[/-]\d{1,2}[/-]\d{2,4}|\d{2,4}[/-]\d{1,2}[/-]\d{1,2})\b"),
    "DATE_OF_BIRTH": re.compile(
        r"\b(?:date\s*of\s*birth|dob|birth\s*date|born)\b[^A-Za-z0-9]\s*\d{1,2}[/-]\d{1,2}[/-]\d{2,4}",
        re.I),
    "VEHICLE_IDENTIFIER": re.compile(r"\b[A-HJ-NPR-Z0-9]{17}\b"),
    "ID_NUMBER": re.compile(
        r"\b(?:(?:medical\s*record|med\s*rec(?:ord)?|mrn|student\s*(?:id|identification)|account|acct|"
        r"beneficiary|license|licence|cert(?:ificate)?|serial)(?:\s*(?:no\.?|number|#|id))?[:\s.\-]*)"
        r"(?=[A-Z0-9\-]*\d)[A-Z0-9][A-Z0-9\-]{3,18}\b",
        re.I),
}

# Policy profiles: which entity types a `--policy` run includes. They filter the
# plan a reviewer approves; they do not turn detectors off.
POLICY_ENTITIES = {
    # FERPA: student education-record PII. Directory info (name, major, campus,
    # ZIP, e-mail, dates of attendance) is public unless the student opted out,
    # so those fields are left to a human decision rather than auto-redacted.
    "ferpa": {"US_SSN", "DATE_OF_BIRTH", "EMAIL_ADDRESS", "PHONE_NUMBER",
              "ID_NUMBER", "ZIP_CODE", "CREDIT_CARD", "PERSON"},
    # HIPAA: the format-detectable subset of the 18 identifiers.
    "hipaa": {"US_SSN", "PHONE_NUMBER", "EMAIL_ADDRESS", "IP_ADDRESS", "URL",
              "DATE", "DATE_OF_BIRTH", "ZIP_CODE", "ID_NUMBER",
              "VEHICLE_IDENTIFIER", "CREDIT_CARD", "PERSON"},
}

@dataclass
class Word:
    text: str
    left: int
    top: int
    width: int
    height: int
    conf: float
    start: int = 0
    end: int = 0


def mask_value(entity: str, value: str) -> str:
    if entity == "EMAIL_ADDRESS":
        if "@" in value:
            a, b = value.split("@", 1)
            return (a[:1] + "***@" + b) if a else "***@" + b
    digits = re.sub(r"\D", "", value)
    if entity in {"US_SSN", "CREDIT_CARD", "PHONE_NUMBER"} and digits:
        return "***" + digits[-4:]
    if entity == "IP_ADDRESS":
        parts = value.split(".")
        return ".".join(parts[:1] + ["***", "***", parts[-1]]) if len(parts) == 4 else "[REDACTED_IP]"
    if entity == "URL":
        return "[REDACTED_URL]"
    if entity == "DATE":
        return "[REDACTED_DATE]"
    if entity == "DATE_OF_BIRTH":
        return "[REDACTED_DOB]"
    if entity == "VEHICLE_IDENTIFIER":
        return "[REDACTED_VIN]"
    if entity in {"ZIP_CODE", "ID_NUMBER"} and digits:
        return "***" + digits[-4:]

    return "[REDACTED]"


def luhn_ok(raw: str) -> bool:
    digits = [int(c) for c in re.sub(r"\D", "", raw)]
    if not (13 <= len(digits) <= 19): return False
    total = 0
    parity = len(digits) % 2
    for i, d in enumerate(digits):
        if i % 2 == parity:
            d *= 2
            if d > 9: d -= 9
        total += d
    return total % 10 == 0


def run_tesseract_tsv(image_path: Path, lang: str, tesseract_cmd: str) -> List[Word]:
    cmd = [tesseract_cmd, str(image_path), "stdout", "-l", lang, "tsv"]
    p = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    if p.returncode != 0:
        raise RuntimeError(f"Tesseract failed: {p.stderr.strip()}")
    rows = csv.DictReader(io.StringIO(p.stdout), delimiter="\t")
    words = []
    for r in rows:
        text = (r.get("text") or "").strip()
        if not text: continue
        try:
            conf = float(r.get("conf") or -1)
            words.append(Word(text, int(r["left"]), int(r["top"]), int(r["width"]), int(r["height"]), conf))
        except Exception:
            continue
    # Assign offsets in a normalized single-space stream.
    pos = 0
    for i, w in enumerate(words):
        if i: pos += 1
        w.start = pos
        pos += len(w.text)
        w.end = pos
    return words


def text_from_words(words: List[Word]) -> str:
    return " ".join(w.text for w in words)


def span_bbox(words: List[Word], start: int, end: int) -> Optional[Tuple[int,int,int,int,float]]:
    hit = [w for w in words if w.end > start and w.start < end]
    if not hit: return None
    l=min(w.left for w in hit); t=min(w.top for w in hit)
    r=max(w.left+w.width for w in hit); b=max(w.top+w.height for w in hit)
    confs=[w.conf for w in hit if w.conf >= 0]
    conf=sum(confs)/len(confs) if confs else -1.0
    return l,t,r,b,conf


def detect_spans(text: str, use_presidio: bool=False, entities: Optional[List[str]]=None,
                 allowed: Optional[set]=None):
    found=[]
    for et, pat in PATTERNS.items():
        for m in pat.finditer(text):
            val=m.group(0)
            if et == "CREDIT_CARD_CANDIDATE":
                if not luhn_ok(val): continue
                et2="CREDIT_CARD"
            elif et == "IP_ADDRESS":
                try: ipaddress.ip_address(val)
                except ValueError: continue
                et2=et
            else:
                et2=et
            if allowed is not None and et2 not in allowed:
                continue
            found.append((m.start(),m.end(),et2,val,1.0,"regex"))
    if use_presidio:
        try:
            from presidio_analyzer import AnalyzerEngine
            analyzer=AnalyzerEngine()
            kwargs={"text":text,"language":"en"}
            if entities: kwargs["entities"]=entities
            for res in analyzer.analyze(**kwargs):
                if allowed is not None and res.entity_type not in allowed:
                    continue
                found.append((res.start,res.end,res.entity_type,text[res.start:res.end],float(res.score),"presidio"))
        except Exception as e:
            raise RuntimeError(f"Presidio requested but unavailable/failed: {e}")
    # de-duplicate exact/near-exact spans by entity
    uniq={}
    for item in found:
        key=(item[0],item[1],item[2])
        if key not in uniq or item[4] > uniq[key][4]: uniq[key]=item
    return sorted(uniq.values(), key=lambda x:(x[0],x[1],x[2]))


def detection_record(idx, page, entity, val, bbox, coord_space, ocr_conf, det_conf, source):
    return {
        "id": f"d{idx:05d}", "page": page, "entity_type": entity, "source": source,
        "bbox": [round(float(x),3) for x in bbox], "coordinate_space": coord_space,
        "ocr_confidence": None if ocr_conf < 0 else round(float(ocr_conf),2),
        "detector_confidence": round(float(det_conf),3),
        "preview": mask_value(entity,val),
        "sha256": hashlib.sha256(val.encode("utf-8")).hexdigest(),
        "action": "redact"
    }


def scan_image(path: Path, lang: str, tesseract_cmd: str, use_presidio=False, entities=None, allowed=None):
    words=run_tesseract_tsv(path, lang, tesseract_cmd)
    text=text_from_words(words)
    dets=[]
    idx=1
    for s,e,et,val,score,src in detect_spans(text,use_presidio,entities,allowed):
        bb=span_bbox(words,s,e)
        if not bb: continue
        l,t,r,b,conf=bb
        dets.append(detection_record(idx,1,et,val,(l,t,r,b),"image_pixels",conf,score,"ocr-"+src)); idx+=1
    return dets, []


def require_pymupdf():
    try:
        import pymupdf
        return pymupdf
    except ImportError:
        try:
            import fitz as pymupdf
            return pymupdf
        except ImportError:
            raise RuntimeError("PyMuPDF is required for PDF operations")


def scan_pdf(path: Path, dpi: int, lang: str, tesseract_cmd: str, use_presidio=False, entities=None, allowed=None):
    pymupdf=require_pymupdf(); doc=pymupdf.open(path)
    dets=[]; warnings=[]; idx=1
    scale=dpi/72.0
    with tempfile.TemporaryDirectory(prefix="ocr-redact-") as td:
        for pno,page in enumerate(doc, start=1):
            pix=page.get_pixmap(matrix=pymupdf.Matrix(scale,scale), alpha=False)
            img=Path(td)/f"page-{pno}.png"; pix.save(str(img))
            try:
                words=run_tesseract_tsv(img,lang,tesseract_cmd)
            except Exception as e:
                warnings.append(f"Page {pno}: OCR failed: {e}"); continue
            text=text_from_words(words)
            for s,e,et,val,score,src in detect_spans(text,use_presidio,entities,allowed):
                bb=span_bbox(words,s,e)
                if not bb: continue
                l,t,r,b,conf=bb
                pdfbb=(l/scale,t/scale,r/scale,b/scale)
                dets.append(detection_record(idx,pno,et,val,pdfbb,"pdf_points",conf,score,"ocr-"+src)); idx+=1
    doc.close(); return dets,warnings


def scan_pdf_text(path: Path, lang: str, tesseract_cmd: str, use_presidio=False, entities=None, allowed=None):
    """Detect FERPA/HIPAA identifiers in the native text layer of a PDF.

    Many education/health documents carry identifiers as real text, not pixels.
    OCR is not needed here; PyMuPDF supplies word rectangles directly. The
    tesseract_cmd argument is unused but kept for interface parity.
    """
    pymupdf=require_pymupdf(); doc=pymupdf.open(path)
    dets=[]; warnings=[]; idx=1
    for pno,page in enumerate(doc, start=1):
        words=sorted(page.get_text("words", sort=True), key=lambda w:(w[0],w[1]))
        if not words:
            warnings.append(f"Page {pno}: no extractable text"); continue
        # Rebuild a single-space stream with per-word start offsets so regex
        # spans map back onto word rectangles (mirrors the OCR path).
        seq=[]; parts=[]; pos=0
        for w in words:
            seq.append((w,pos)); parts.append(w[4]); pos += len(w[4])+1
        text=" ".join(parts)
        for s,e,et,val,score,src in detect_spans(text,use_presidio,entities,allowed):
            hit=[w for (w,ws) in seq if ws < e and ws+len(w[4]) > s]
            if not hit: continue
            l=min(w[0] for w in hit); t=min(w[1] for w in hit)
            r=max(w[2] for w in hit); b=max(w[3] for w in hit)
            dets.append(detection_record(idx,pno,et,val,(l,t,r,b),"pdf_points",-1.0,score,"text-"+src)); idx+=1
    doc.close(); return dets,warnings


def scan(path: Path, output: Path, dpi: int, lang: str, tesseract_cmd: str, use_presidio: bool, entities, allowed=None):
    ext=path.suffix.lower()
    if ext in PDF_EXTS:
        dets,warnings=scan_pdf(path,dpi,lang,tesseract_cmd,use_presidio,entities,allowed); typ="pdf"
    elif ext in IMAGE_EXTS:
        dets,warnings=scan_image(path,lang,tesseract_cmd,use_presidio,entities,allowed); typ="image"
    else: raise RuntimeError(f"Unsupported input type: {ext}")
    plan=plan_document(path,typ,dpi,lang,use_presidio,dets,warnings)
    output.write_text(json.dumps(plan,indent=2),encoding="utf-8")
    return len(dets), warnings


def scan_text(path: Path, output: Path, dpi: int, lang: str, tesseract_cmd: str, use_presidio: bool, entities, allowed=None):
    if path.suffix.lower() not in PDF_EXTS:
        raise RuntimeError("scan-text requires a PDF input")
    dets,warnings=scan_pdf_text(path,lang,tesseract_cmd,use_presidio,entities,allowed)
    plan=plan_document(path,"pdf",dpi,lang,use_presidio,dets,warnings)
    output.write_text(json.dumps(plan,indent=2),encoding="utf-8")
    return len(dets), warnings


def plan_document(path: Path, typ: str, dpi: int, lang: str, use_presidio: bool, dets, warnings):
    return {"schema_version":1,"source":{"name":path.name,"type":typ},
            "settings":{"dpi":dpi,"ocr_language":lang,"presidio":use_presidio},
            "detections":dets,"warnings":warnings}


def apply_image(inp: Path, plan: dict, out: Path):
    from PIL import Image, ImageDraw
    img=Image.open(inp).convert("RGB"); draw=ImageDraw.Draw(img)
    for d in plan.get("detections",[]):
        if d.get("action")!="redact" or d.get("coordinate_space")!="image_pixels": continue
        l,t,r,b=d["bbox"]; draw.rectangle([l,t,r,b], fill="black")
    img.save(out)


def apply_pdf(inp: Path, plan: dict, out: Path):
    pymupdf=require_pymupdf(); doc=pymupdf.open(inp)
    bypage={}
    for d in plan.get("detections",[]):
        if d.get("action")!="redact" or d.get("coordinate_space")!="pdf_points": continue
        bypage.setdefault(int(d["page"]),[]).append(d)
    for pno, ds in bypage.items():
        if pno < 1 or pno > len(doc): raise RuntimeError(f"Plan page out of range: {pno}")
        page=doc[pno-1]
        for d in ds:
            rect=pymupdf.Rect(*d["bbox"])
            page.add_redact_annot(rect, fill=(0,0,0), cross_out=False)
        # defaults remove text and blank overlapping image pixels.
        page.apply_redactions()
    doc.save(out, garbage=4, deflate=True)
    doc.close()


def apply(inp: Path, plan_path: Path, out: Path):
    if inp.resolve()==out.resolve(): raise RuntimeError("Refusing to overwrite the source")
    plan=json.loads(plan_path.read_text(encoding="utf-8"))
    ext=inp.suffix.lower()
    if ext in PDF_EXTS: apply_pdf(inp,plan,out)
    elif ext in IMAGE_EXTS: apply_image(inp,plan,out)
    else: raise RuntimeError(f"Unsupported input type: {ext}")


def verify(inp: Path, report: Path, dpi: int, lang: str, tesseract_cmd: str, use_presidio: bool, entities, allowed=None):
    tmp=report.with_suffix(report.suffix+".scan.tmp")
    try:
        count,warnings=scan(inp,tmp,dpi,lang,tesseract_cmd,use_presidio,entities,allowed)
        plan=json.loads(tmp.read_text(encoding="utf-8"))
        result={"status":"PASS" if count==0 and not warnings else "NEEDS_REVIEW",
                "remaining_detection_count":count,"remaining_detections":plan["detections"],"warnings":warnings}
        report.write_text(json.dumps(result,indent=2),encoding="utf-8")
        return result
    finally:
        if tmp.exists(): tmp.unlink()


def main():
    ap=argparse.ArgumentParser(description="Local OCR-aware redaction for images and PDFs")
    sub=ap.add_subparsers(dest="cmd",required=True)
    def common(p):
        p.add_argument("input",type=Path); p.add_argument("--dpi",type=int,default=200)
        p.add_argument("--language",default="eng"); p.add_argument("--tesseract-cmd",default=os.environ.get("TESSERACT_CMD","tesseract"))
        p.add_argument("--presidio",action="store_true"); p.add_argument("--presidio-entity",action="append",dest="entities")
        p.add_argument("--policy",choices=sorted(POLICY_ENTITIES),help="Policy profile (ferpa|hipaa) used to filter the plan")
    s=sub.add_parser("scan"); common(s); s.add_argument("--output",type=Path,required=True)
    st=sub.add_parser("scan-text"); common(st); st.add_argument("--output",type=Path,required=True)
    a=sub.add_parser("apply"); a.add_argument("input",type=Path); a.add_argument("--plan",type=Path,required=True); a.add_argument("--output",type=Path,required=True)
    v=sub.add_parser("verify"); common(v); v.add_argument("--report",type=Path,required=True)
    args=ap.parse_args()
    try:
        allowed = POLICY_ENTITIES.get(args.policy) if getattr(args,"policy",None) else None
        if args.cmd=="scan":
            count,w=scan(args.input,args.output,args.dpi,args.language,args.tesseract_cmd,args.presidio,args.entities,allowed)
            print(json.dumps({"status":"PLANNED","detections":count,"warnings":w,"plan":str(args.output),"policy":args.policy},indent=2))
        elif args.cmd=="scan-text":
            count,w=scan_text(args.input,args.output,args.dpi,args.language,args.tesseract_cmd,args.presidio,args.entities,allowed)
            print(json.dumps({"status":"PLANNED","detections":count,"warnings":w,"plan":str(args.output),"policy":args.policy},indent=2))
        elif args.cmd=="apply":
            apply(args.input,args.plan,args.output); print(json.dumps({"status":"APPLIED","output":str(args.output)},indent=2))
        else:
            result=verify(args.input,args.report,args.dpi,args.language,args.tesseract_cmd,args.presidio,args.entities,allowed); print(json.dumps(result,indent=2))
            if result["status"]!="PASS": sys.exit(3)
    except Exception as e:
        print(json.dumps({"status":"ERROR","error":str(e)},indent=2),file=sys.stderr); sys.exit(2)

if __name__=="__main__": main()
