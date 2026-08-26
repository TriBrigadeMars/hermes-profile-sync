#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import re
import sys
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path

HERE = Path(__file__).resolve().parent
SHARED = HERE.parent
TERMS_FILE = SHARED / "data" / "skill_terms.txt"

STOPWORDS = {
    "a","an","and","are","as","at","be","by","for","from","has","have","in","is","it","of","on","or","our","that","the","their","this","to","we","will","with","you","your","years","year","role","job","work","working","team","teams","required","preferred","experience","skills","ability","including","using","within","across","responsible","responsibilities","candidate","candidates","position"
}

EDU_PATTERNS = {
    "high school": r"\bhigh school\b|\bged\b",
    "associate degree": r"\bassociate(?:'s)? degree\b|\ba\.a\.?\b|\ba\.s\.?\b",
    "bachelor's degree": r"\bbachelor(?:'s)? degree\b|\bb\.a\.?\b|\bb\.s\.?\b",
    "master's degree": r"\bmaster(?:'s)? degree\b|\bm\.a\.?\b|\bm\.s\.?\b|\bmba\b|\bm\.b\.a\.\b",
    "doctorate": r"\bdoctorate\b|\bph\.?d\.?\b|\bdoctoral degree\b",
}

SECTION_PATTERNS = {
    "experience": r"(?im)^\s*(professional\s+)?experience\s*$|^\s*work\s+experience\s*$",
    "education": r"(?im)^\s*education\s*$",
    "skills": r"(?im)^\s*(skills|technical skills|core competencies|competencies)\s*$",
}


def read_text(path: str | Path) -> str:
    return Path(path).read_text(encoding="utf-8", errors="replace")


def load_json(path: str | Path):
    return json.loads(read_text(path))


def write_json(path: str | Path, data) -> None:
    p = Path(path)
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def load_terms() -> list[str]:
    if not TERMS_FILE.exists():
        return []
    terms = []
    for line in TERMS_FILE.read_text(encoding="utf-8").splitlines():
        line = line.strip().lower()
        if line and not line.startswith("#"):
            terms.append(line)
    return sorted(set(terms), key=lambda x: (-len(x), x))


def phrase_present(text: str, phrase: str) -> bool:
    # Flexible whitespace but otherwise literal matching.
    pat = r"(?<![A-Za-z0-9])" + re.escape(phrase).replace(r"\ ", r"\s+") + r"(?![A-Za-z0-9])"
    return re.search(pat, text, flags=re.I) is not None


def extract_terms(text: str) -> list[str]:
    return [term for term in load_terms() if phrase_present(text, term)]


def evidence_blob(profile: dict) -> str:
    chunks = []
    for item in profile.get("evidence", []):
        if item.get("status") == "needs-confirmation":
            continue
        chunks.append(str(item.get("text", "")))
        chunks.extend(str(t) for t in item.get("tags", []))
    return "\n".join(chunks).lower()


def evidence_matches(profile: dict, term: str) -> list[str]:
    out = []
    for item in profile.get("evidence", []):
        if item.get("status") == "needs-confirmation":
            continue
        blob = " ".join([str(item.get("text", "")), *[str(t) for t in item.get("tags", [])]])
        if phrase_present(blob, term):
            out.append(item.get("id", "unknown"))
    return out


def validate_profile_data(profile: dict) -> list[str]:
    errors = []
    if not isinstance(profile, dict):
        return ["Profile root must be an object."]
    for field in ("schema_version", "candidate", "evidence"):
        if field not in profile:
            errors.append(f"Missing required field: {field}")
    if "evidence" in profile and not isinstance(profile["evidence"], list):
        errors.append("evidence must be a list")
        return errors
    ids = set()
    for i, item in enumerate(profile.get("evidence", []), start=1):
        if not isinstance(item, dict):
            errors.append(f"evidence[{i}] must be an object")
            continue
        for field in ("id", "type", "text", "status"):
            if not item.get(field):
                errors.append(f"evidence[{i}] missing {field}")
        eid = item.get("id")
        if eid in ids:
            errors.append(f"Duplicate evidence id: {eid}")
        if eid:
            ids.add(eid)
        if item.get("status") not in {"confirmed", "user-supplied", "document-derived", "needs-confirmation"}:
            errors.append(f"evidence[{i}] invalid status: {item.get('status')}")
    return errors


def cmd_init_profile(args) -> int:
    profile = {
        "schema_version": "1.0",
        "candidate": {"name": args.name or "", "location": "", "email": "", "phone": "", "links": []},
        "evidence": [],
        "preferences": {},
        "metadata": {"created_at": datetime.now(timezone.utc).isoformat(), "updated_at": datetime.now(timezone.utc).isoformat()},
    }
    write_json(args.out, profile)
    print(args.out)
    return 0


def next_evidence_id(profile: dict) -> str:
    nums = []
    for item in profile.get("evidence", []):
        m = re.fullmatch(r"E(\d+)", str(item.get("id", "")))
        if m:
            nums.append(int(m.group(1)))
    return f"E{(max(nums) + 1 if nums else 1):04d}"


def cmd_add_evidence(args) -> int:
    profile = load_json(args.profile)
    errors = validate_profile_data(profile)
    if errors:
        print("Cannot modify invalid profile:", file=sys.stderr)
        for e in errors:
            print(f"- {e}", file=sys.stderr)
        return 2
    tags = [t.strip() for t in (args.tags or "").split(",") if t.strip()]
    item = {
        "id": args.id or next_evidence_id(profile),
        "type": args.type,
        "text": args.text.strip(),
        "tags": tags,
        "source": args.source or "user",
        "status": args.status,
        "notes": args.notes or "",
    }
    profile["evidence"].append(item)
    profile.setdefault("metadata", {})["updated_at"] = datetime.now(timezone.utc).isoformat()
    write_json(args.profile, profile)
    print(item["id"])
    return 0


def cmd_validate_profile(args) -> int:
    profile = load_json(args.profile)
    errors = validate_profile_data(profile)
    if errors:
        print("INVALID")
        for e in errors:
            print(f"- {e}")
        return 1
    print(f"VALID: {len(profile.get('evidence', []))} evidence items")
    return 0


def top_terms(text: str, n: int = 25) -> list[dict]:
    words = re.findall(r"[A-Za-z][A-Za-z0-9+#.\-/]{2,}", text.lower())
    c = Counter(w for w in words if w not in STOPWORDS and not w.isdigit())
    return [{"term": term, "count": count} for term, count in c.most_common(n)]


def analyze_jd_text(text: str) -> dict:
    lower = text.lower()
    skills = extract_terms(text)
    years = []
    year_re = re.compile(r"\b(?P<low>\d{1,2})(?:\s*[-–]\s*(?P<high>\d{1,2}))?\+?\s+years?(?:\s+of)?\s+(?:relevant\s+)?experience\b", re.I)
    for m in year_re.finditer(text):
        years.append({"text": m.group(0), "min_years": int(m.group("low")), "max_years": int(m.group("high")) if m.group("high") else None})
    education = [label for label, pat in EDU_PATTERNS.items() if re.search(pat, lower, flags=re.I)]
    certs = []
    for term in ("pmp", "cissp", "cpa", "rn", "jd", "bar admission", "security+", "aws certified", "scrum master"):
        if phrase_present(text, term):
            certs.append(term)
    return {
        "analysis_type": "deterministic_term_inventory",
        "note": "This inventory supports, but does not replace, Hermes semantic job-description analysis.",
        "skills_and_tools": skills,
        "experience_mentions": years,
        "education_mentions": education,
        "credential_mentions": sorted(set(certs)),
        "frequent_terms": top_terms(text),
        "character_count": len(text),
    }


def cmd_analyze_jd(args) -> int:
    data = analyze_jd_text(read_text(args.jd))
    if args.out:
        write_json(args.out, data)
        print(args.out)
    else:
        print(json.dumps(data, indent=2))
    return 0


def cmd_compare(args) -> int:
    profile = load_json(args.profile)
    errors = validate_profile_data(profile)
    if errors:
        for e in errors:
            print(e, file=sys.stderr)
        return 2
    jd = load_json(args.jd_analysis)
    supported = []
    gaps = []
    for term in jd.get("skills_and_tools", []):
        matches = evidence_matches(profile, term)
        if matches:
            supported.append({"term": term, "evidence_ids": matches, "classification": "CANDIDATE-EVIDENCED"})
        else:
            gaps.append({"term": term, "evidence_ids": [], "classification": "GAP / DO NOT CLAIM"})
    result = {
        "supported": supported,
        "gaps": gaps,
        "experience_mentions_in_jd": jd.get("experience_mentions", []),
        "education_mentions_in_jd": jd.get("education_mentions", []),
        "note": "A gap is not evidence of candidate deficiency; it means this profile does not currently evidence the term.",
    }
    if args.out:
        write_json(args.out, result)
        print(args.out)
    else:
        print(json.dumps(result, indent=2))
    return 0


def ats_lint(resume: str, jd: str | None = None, profile: dict | None = None) -> dict:
    findings = []
    for name, pat in SECTION_PATTERNS.items():
        if not re.search(pat, resume):
            findings.append({"severity": "review", "type": "section", "message": f"No standard {name} heading detected."})
    if len(resume) < 600:
        findings.append({"severity": "review", "type": "content", "message": "Resume text is unusually short; confirm that extraction captured the full document."})
    if len(resume) > 14000:
        findings.append({"severity": "review", "type": "length", "message": "Resume text is long; consider whether all content is role-relevant."})
    if re.search(r"\b(responsible for|duties included)\b", resume, flags=re.I):
        findings.append({"severity": "suggestion", "type": "prose", "message": "Some bullets may lead with generic duty phrases; consider stronger specific actions when evidence permits."})
    if re.search(r"\b(results[- ]driven|dynamic professional|rockstar|guru|ninja)\b", resume, flags=re.I):
        findings.append({"severity": "suggestion", "type": "diction", "message": "Generic self-promotional language detected; replace with concrete evidence."})
    jd_skills = extract_terms(jd or "") if jd else []
    resume_skills = extract_terms(resume)
    coverage = None
    if jd_skills:
        present = [s for s in jd_skills if s in resume_skills]
        missing = [s for s in jd_skills if s not in resume_skills]
        coverage = {
            "jd_terms_detected": jd_skills,
            "resume_terms_present": present,
            "resume_terms_absent": missing,
            "textual_presence_ratio": round(len(present) / len(jd_skills), 3) if jd_skills else None,
            "warning": "Textual presence is not an ATS score and missing terms should only be added when candidate evidence supports them.",
        }
    unsupported = []
    if profile is not None:
        for term in resume_skills:
            if not evidence_matches(profile, term):
                unsupported.append(term)
        if unsupported:
            findings.append({"severity": "must-review", "type": "evidence", "message": "Resume contains recognized skill terms not evidenced by the supplied profile.", "terms": unsupported})
    return {"findings": findings, "keyword_coverage": coverage, "recognized_resume_terms": resume_skills, "unsupported_recognized_terms": unsupported}


def cmd_ats_lint(args) -> int:
    resume = read_text(args.resume)
    jd = read_text(args.jd) if args.jd else None
    profile = load_json(args.profile) if args.profile else None
    result = ats_lint(resume, jd, profile)
    if args.out:
        write_json(args.out, result)
        print(args.out)
    else:
        print(json.dumps(result, indent=2))
    return 0


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(description="Local helpers for Hermes Career Writing Suite")
    sub = p.add_subparsers(dest="command", required=True)

    sp = sub.add_parser("init-profile")
    sp.add_argument("--out", required=True)
    sp.add_argument("--name")
    sp.set_defaults(func=cmd_init_profile)

    sp = sub.add_parser("add-evidence")
    sp.add_argument("--profile", required=True)
    sp.add_argument("--type", required=True)
    sp.add_argument("--text", required=True)
    sp.add_argument("--tags")
    sp.add_argument("--source")
    sp.add_argument("--status", default="user-supplied", choices=["confirmed", "user-supplied", "document-derived", "needs-confirmation"])
    sp.add_argument("--notes")
    sp.add_argument("--id")
    sp.set_defaults(func=cmd_add_evidence)

    sp = sub.add_parser("validate-profile")
    sp.add_argument("--profile", required=True)
    sp.set_defaults(func=cmd_validate_profile)

    sp = sub.add_parser("analyze-jd")
    sp.add_argument("--jd", required=True)
    sp.add_argument("--out")
    sp.set_defaults(func=cmd_analyze_jd)

    sp = sub.add_parser("compare")
    sp.add_argument("--profile", required=True)
    sp.add_argument("--jd-analysis", required=True)
    sp.add_argument("--out")
    sp.set_defaults(func=cmd_compare)

    sp = sub.add_parser("ats-lint")
    sp.add_argument("--resume", required=True)
    sp.add_argument("--jd")
    sp.add_argument("--profile")
    sp.add_argument("--out")
    sp.set_defaults(func=cmd_ats_lint)
    return p


def main() -> int:
    args = build_parser().parse_args()
    return int(args.func(args))


if __name__ == "__main__":
    raise SystemExit(main())
