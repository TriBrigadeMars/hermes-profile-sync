#!/usr/bin/env python3
"""Career Market Intelligence: local labor-market analysis for job seekers.

Core commands use only Python's standard library and SQLite.
"""
from __future__ import annotations

import argparse
import csv
import datetime as dt
import itertools
import json
import math
import os
import re
import sqlite3
import statistics
import sys
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any, Iterable

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_TAXONOMY = ROOT / "data" / "seed_skills.csv"
PROTECTED_FIELD_TERMS = {
    "race", "racial", "ethnicity", "ethnic", "gender", "sex", "age",
    "birth", "dob", "disability", "disabled", "religion", "religious",
    "national_origin", "pregnancy", "pregnant", "genetic",
    "sexual_orientation", "marital_status", "citizenship_status",
}

SCHEMA = """
PRAGMA foreign_keys=ON;
CREATE TABLE IF NOT EXISTS source_runs (
  id INTEGER PRIMARY KEY,
  source TEXT NOT NULL,
  kind TEXT NOT NULL,
  imported_at TEXT NOT NULL,
  source_date TEXT,
  notes TEXT
);
CREATE TABLE IF NOT EXISTS postings (
  id INTEGER PRIMARY KEY,
  source TEXT NOT NULL,
  external_id TEXT,
  title TEXT NOT NULL,
  normalized_title TEXT NOT NULL,
  company TEXT,
  location TEXT,
  industry TEXT,
  posted_date TEXT,
  description TEXT,
  years_experience REAL,
  education TEXT,
  UNIQUE(source, external_id)
);
CREATE INDEX IF NOT EXISTS idx_postings_title ON postings(normalized_title);
CREATE INDEX IF NOT EXISTS idx_postings_date ON postings(posted_date);
CREATE TABLE IF NOT EXISTS posting_skills (
  posting_id INTEGER NOT NULL REFERENCES postings(id) ON DELETE CASCADE,
  skill TEXT NOT NULL,
  extraction_method TEXT NOT NULL,
  PRIMARY KEY(posting_id, skill)
);
CREATE INDEX IF NOT EXISTS idx_posting_skills_skill ON posting_skills(skill);
CREATE TABLE IF NOT EXISTS outcomes (
  id INTEGER PRIMARY KEY,
  cohort TEXT NOT NULL,
  candidate_id TEXT,
  target_title TEXT NOT NULL,
  normalized_title TEXT NOT NULL,
  location TEXT,
  event_date TEXT,
  status TEXT,
  hired INTEGER NOT NULL DEFAULT 0,
  interview INTEGER,
  offer INTEGER,
  years_experience REAL,
  education TEXT
);
CREATE INDEX IF NOT EXISTS idx_outcomes_title ON outcomes(normalized_title);
CREATE TABLE IF NOT EXISTS outcome_skills (
  outcome_id INTEGER NOT NULL REFERENCES outcomes(id) ON DELETE CASCADE,
  skill TEXT NOT NULL,
  PRIMARY KEY(outcome_id, skill)
);
CREATE TABLE IF NOT EXISTS onet_occupations (
  code TEXT PRIMARY KEY,
  title TEXT NOT NULL
);
CREATE TABLE IF NOT EXISTS onet_attributes (
  id INTEGER PRIMARY KEY,
  code TEXT NOT NULL,
  kind TEXT NOT NULL,
  name TEXT NOT NULL,
  scale_name TEXT,
  data_value REAL,
  category TEXT,
  hot_technology INTEGER,
  in_demand INTEGER,
  FOREIGN KEY(code) REFERENCES onet_occupations(code)
);
CREATE INDEX IF NOT EXISTS idx_onet_attr_code ON onet_attributes(code);
CREATE TABLE IF NOT EXISTS oews (
  id INTEGER PRIMARY KEY,
  occ_code TEXT,
  occ_title TEXT,
  area_code TEXT,
  area_title TEXT,
  total_employment REAL,
  employment_prse REAL,
  hourly_mean REAL,
  annual_mean REAL,
  hourly_median REAL,
  annual_median REAL,
  source_date TEXT
);
CREATE INDEX IF NOT EXISTS idx_oews_occ ON oews(occ_code);
"""

FIELD_ALIASES = {
    "external_id": ["external_id", "id", "job_id", "posting_id", "requisition_id"],
    "title": ["title", "job_title", "position_title", "target_title"],
    "company": ["company", "employer", "organization", "organisation"],
    "location": ["location", "job_location", "city_state", "area"],
    "industry": ["industry", "sector"],
    "posted_date": ["posted_date", "date", "date_posted", "publication_date", "event_date"],
    "description": ["description", "job_description", "text", "body", "requirements"],
    "skills": ["skills", "skill_list", "keywords", "competencies"],
    "years_experience": ["years_experience", "experience_years", "years", "min_experience"],
    "education": ["education", "degree", "education_level"],
    "candidate_id": ["candidate_id", "applicant_id", "person_id", "record_id", "id"],
    "status": ["status", "application_status", "outcome"],
    "hired": ["hired", "is_hired", "hire"],
    "interview": ["interview", "interviewed", "is_interviewed"],
    "offer": ["offer", "offered", "is_offered"],
}

SENIORITY_MAP = {
    "sr": "senior", "sr.": "senior", "jr": "junior", "jr.": "junior",
    "lead": "lead", "principal": "principal", "staff": "staff",
}
TITLE_STOPWORDS = {"the", "a", "an", "of", "for", "and", "to", "in"}


def connect(db_path: str) -> sqlite3.Connection:
    p = Path(db_path).expanduser()
    p.parent.mkdir(parents=True, exist_ok=True)
    con = sqlite3.connect(str(p))
    con.row_factory = sqlite3.Row
    con.execute("PRAGMA foreign_keys=ON")
    return con


def init_db(con: sqlite3.Connection) -> None:
    con.executescript(SCHEMA)
    con.commit()


def normalize_title(title: str) -> str:
    text = title.lower().replace("&", " and ")
    text = re.sub(r"[^a-z0-9+#. ]+", " ", text)
    tokens = []
    for token in text.split():
        token = SENIORITY_MAP.get(token, token).strip(".")
        if token.endswith("ies") and len(token) > 4:
            token = token[:-3] + "y"
        elif token.endswith("s") and len(token) > 4 and not token.endswith("ss"):
            token = token[:-1]
        if token not in TITLE_STOPWORDS:
            tokens.append(token)
    return " ".join(tokens)


def title_similarity(a: str, b: str) -> float:
    ta, tb = set(normalize_title(a).split()), set(normalize_title(b).split())
    if not ta or not tb:
        return 0.0
    inter = len(ta & tb)
    return 2 * inter / (len(ta) + len(tb))


def parse_bool(v: Any) -> int | None:
    if v is None or v == "":
        return None
    if isinstance(v, bool):
        return int(v)
    s = str(v).strip().lower()
    if s in {"1", "true", "yes", "y", "hired", "offer", "offered", "interview", "interviewed"}:
        return 1
    if s in {"0", "false", "no", "n", "rejected", "declined"}:
        return 0
    return None


def parse_float(v: Any) -> float | None:
    if v is None or str(v).strip() in {"", "#", "**", "*", "NA", "N/A", "n/a", "-"}:
        return None
    try:
        return float(str(v).replace(",", "").replace("$", ""))
    except ValueError:
        return None


def parse_date(v: Any) -> str | None:
    if not v:
        return None
    s = str(v).strip()
    for fmt in ("%Y-%m-%d", "%Y/%m/%d", "%m/%d/%Y", "%Y-%m", "%m/%Y"):
        try:
            d = dt.datetime.strptime(s[:10] if fmt in {"%Y-%m-%d", "%Y/%m/%d", "%m/%d/%Y"} else s[:7], fmt)
            return d.date().isoformat()
        except ValueError:
            pass
    m = re.match(r"(\d{4})-(\d{2})", s)
    if m:
        return f"{m.group(1)}-{m.group(2)}-01"
    return None


def sniff_delimiter(path: Path) -> str:
    sample = path.read_text(encoding="utf-8-sig", errors="replace")[:8192]
    try:
        return csv.Sniffer().sniff(sample, delimiters=",\t|;").delimiter
    except csv.Error:
        return "\t" if "\t" in sample else ","


def load_records(path_str: str) -> list[dict[str, Any]]:
    path = Path(path_str).expanduser()
    suffix = path.suffix.lower()
    if suffix == ".jsonl":
        return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]
    if suffix == ".json":
        obj = json.loads(path.read_text(encoding="utf-8"))
        if isinstance(obj, list):
            return obj
        if isinstance(obj, dict):
            for key in ("items", "results", "data", "postings", "records"):
                if isinstance(obj.get(key), list):
                    return obj[key]
        raise ValueError("JSON must be an array or contain an items/results/data/postings/records array")
    delim = sniff_delimiter(path)
    with path.open("r", encoding="utf-8-sig", errors="replace", newline="") as f:
        return list(csv.DictReader(f, delimiter=delim))


def lower_key_map(row: dict[str, Any]) -> dict[str, str]:
    return {str(k).strip().lower(): k for k in row.keys()}


def pick(row: dict[str, Any], logical: str) -> Any:
    km = lower_key_map(row)
    for alias in FIELD_ALIASES.get(logical, [logical]):
        if alias.lower() in km:
            return row[km[alias.lower()]]
    return None


def validate_no_sensitive_columns(rows: list[dict[str, Any]]) -> list[str]:
    if not rows:
        return []
    flagged = set()
    for raw in rows[0].keys():
        col = str(raw).strip().lower()
        norm = re.sub(r"[^a-z0-9]+", "_", col).strip("_")
        tokens = set(norm.split("_"))
        if norm in PROTECTED_FIELD_TERMS or tokens & {"race","racial","ethnicity","ethnic","gender","sex","age","birth","dob","disability","disabled","religion","religious","pregnancy","pregnant","genetic"}:
            flagged.add(col)
        elif any(term in norm for term in ("national_origin","sexual_orientation","marital_status","citizenship_status")):
            flagged.add(col)
    return sorted(flagged)


def split_skill_field(v: Any) -> list[str]:
    if v is None:
        return []
    if isinstance(v, list):
        return [str(x).strip() for x in v if str(x).strip()]
    s = str(v).strip()
    if not s:
        return []
    parts = re.split(r"\s*[;|,]\s*", s)
    return [p.strip() for p in parts if p.strip()]


def load_taxonomy(path: Path = DEFAULT_TAXONOMY) -> tuple[dict[str, str], list[tuple[re.Pattern[str], str]]]:
    canonical: dict[str, str] = {}
    patterns: list[tuple[re.Pattern[str], str]] = []
    with path.open("r", encoding="utf-8-sig", newline="") as f:
        for row in csv.DictReader(f):
            skill = row["skill"].strip()
            aliases = [skill] + [a.strip() for a in row.get("aliases", "").split(";") if a.strip()]
            for alias in aliases:
                canonical[alias.lower()] = skill
                escaped = re.escape(alias.lower()).replace(r"\ ", r"\s+")
                patterns.append((re.compile(r"(?<![a-z0-9])" + escaped + r"(?![a-z0-9])", re.I), skill))
    # Longer phrases first reduces surprising overlap.
    patterns.sort(key=lambda x: len(x[0].pattern), reverse=True)
    return canonical, patterns


def canonicalize_skills(skills: Iterable[str], canonical: dict[str, str]) -> set[str]:
    out = set()
    for s in skills:
        key = s.strip().lower()
        if not key:
            continue
        out.add(canonical.get(key, s.strip()))
    return out


def extract_skills(text: str, patterns: list[tuple[re.Pattern[str], str]]) -> set[str]:
    if not text:
        return set()
    return {skill for pat, skill in patterns if pat.search(text)}


EXP_RE = re.compile(r"(?<!\d)(\d{1,2})(?:\s*[-–]\s*\d{1,2})?\s*\+?\s*(?:years?|yrs?)(?:\s+of)?\s+(?:relevant\s+)?experience", re.I)
EXP_RE2 = re.compile(r"(?:minimum|min\.?|at least)\s+(\d{1,2})\s*\+?\s*(?:years?|yrs?)", re.I)


def infer_years_experience(text: str) -> float | None:
    values = [int(x) for x in EXP_RE.findall(text or "")] + [int(x) for x in EXP_RE2.findall(text or "")]
    return float(min(values)) if values else None


def infer_education(text: str) -> str | None:
    t = (text or "").lower()
    checks = [
        ("Doctorate", ["ph.d", "phd", "doctorate", "doctoral degree"]),
        ("Master's", ["master's", "masters degree", "master degree", "m.s.", "mba"]),
        ("Bachelor's", ["bachelor's", "bachelors degree", "bachelor degree", "b.s.", "b.a."]),
        ("Associate", ["associate degree", "associate's"]),
        ("High school", ["high school diploma", "ged"]),
    ]
    for label, terms in checks:
        if any(term in t for term in terms):
            return label
    return None


def import_postings(args: argparse.Namespace) -> None:
    con = connect(args.db); init_db(con)
    rows = load_records(args.input)
    canonical, patterns = load_taxonomy(Path(args.taxonomy) if args.taxonomy else DEFAULT_TAXONOMY)
    inserted = updated = skipped = 0
    for i, row in enumerate(rows, 1):
        title = str(pick(row, "title") or "").strip()
        if not title:
            skipped += 1; continue
        description = str(pick(row, "description") or "")
        ext = str(pick(row, "external_id") or f"row-{i}")
        given_skills = canonicalize_skills(split_skill_field(pick(row, "skills")), canonical)
        skills = given_skills or extract_skills(description, patterns)
        years = parse_float(pick(row, "years_experience"))
        if years is None:
            years = infer_years_experience(description)
        education = str(pick(row, "education") or "").strip() or infer_education(description)
        vals = (args.source, ext, title, normalize_title(title), str(pick(row,"company") or "").strip() or None,
                str(pick(row,"location") or "").strip() or None, str(pick(row,"industry") or "").strip() or None,
                parse_date(pick(row,"posted_date")), description or None, years, education)
        try:
            cur = con.execute("""INSERT INTO postings(source,external_id,title,normalized_title,company,location,industry,posted_date,description,years_experience,education)
                VALUES(?,?,?,?,?,?,?,?,?,?,?)""", vals)
            pid = cur.lastrowid; inserted += 1
        except sqlite3.IntegrityError:
            con.execute("""UPDATE postings SET title=?,normalized_title=?,company=?,location=?,industry=?,posted_date=?,description=?,years_experience=?,education=?
                WHERE source=? AND external_id=?""",
                (title, normalize_title(title), vals[4], vals[5], vals[6], vals[7], vals[8], vals[9], vals[10], args.source, ext))
            pid = con.execute("SELECT id FROM postings WHERE source=? AND external_id=?", (args.source,ext)).fetchone()[0]
            con.execute("DELETE FROM posting_skills WHERE posting_id=?", (pid,)); updated += 1
        method = "provided" if given_skills else "taxonomy"
        con.executemany("INSERT OR IGNORE INTO posting_skills(posting_id,skill,extraction_method) VALUES(?,?,?)", [(pid,s,method) for s in sorted(skills)])
    con.execute("INSERT INTO source_runs(source,kind,imported_at,source_date,notes) VALUES(?,?,?,?,?)",
                (args.source,"postings",dt.datetime.now(dt.timezone.utc).isoformat(),args.source_date,f"input={Path(args.input).name}; rows={len(rows)}"))
    con.commit()
    print(json.dumps({"rows":len(rows),"inserted":inserted,"updated":updated,"skipped":skipped,"source":args.source}, indent=2))


def import_outcomes(args: argparse.Namespace) -> None:
    con = connect(args.db); init_db(con)
    rows = load_records(args.input)
    sensitive = validate_no_sensitive_columns(rows)
    if sensitive and not args.allow_sensitive_columns:
        raise SystemExit("Refusing outcome import because sensitive/protected-looking columns were detected: " + ", ".join(sensitive) + ". Remove them or pass --allow-sensitive-columns only to store a file after reviewing it; such columns are still ignored by this skill.")
    canonical, patterns = load_taxonomy(Path(args.taxonomy) if args.taxonomy else DEFAULT_TAXONOMY)
    inserted = skipped = 0
    for row in rows:
        title = str(pick(row,"title") or "").strip()
        if not title:
            skipped += 1; continue
        status = str(pick(row,"status") or "").strip()
        hired = parse_bool(pick(row,"hired"))
        if hired is None:
            hired = 1 if status.lower() in {"hired","accepted","started","joined"} else 0
        interview = parse_bool(pick(row,"interview"))
        offer = parse_bool(pick(row,"offer"))
        given = canonicalize_skills(split_skill_field(pick(row,"skills")), canonical)
        desc = str(pick(row,"description") or "")
        skills = given or extract_skills(desc, patterns)
        cur = con.execute("""INSERT INTO outcomes(cohort,candidate_id,target_title,normalized_title,location,event_date,status,hired,interview,offer,years_experience,education)
            VALUES(?,?,?,?,?,?,?,?,?,?,?,?)""",
            (args.cohort, str(pick(row,"candidate_id") or "").strip() or None, title, normalize_title(title), str(pick(row,"location") or "").strip() or None,
             parse_date(pick(row,"posted_date")), status or None, hired, interview, offer, parse_float(pick(row,"years_experience")), str(pick(row,"education") or "").strip() or None))
        oid = cur.lastrowid
        con.executemany("INSERT OR IGNORE INTO outcome_skills(outcome_id,skill) VALUES(?,?)", [(oid,s) for s in sorted(skills)])
        inserted += 1
    con.execute("INSERT INTO source_runs(source,kind,imported_at,notes) VALUES(?,?,?,?)",
                (args.cohort,"outcomes",dt.datetime.now(dt.timezone.utc).isoformat(),f"input={Path(args.input).name}; rows={len(rows)}"))
    con.commit()
    print(json.dumps({"rows":len(rows),"inserted":inserted,"skipped":skipped,"cohort":args.cohort,"ignored_sensitive_columns":sensitive}, indent=2))


def read_delimited(path: Path) -> list[dict[str, Any]]:
    return load_records(str(path))


def find_file(directory: Path, stems: list[str], excludes: list[str] | None = None) -> Path | None:
    excludes = [x.lower() for x in (excludes or [])]
    files = sorted(directory.rglob("*"))
    for p in files:
        if not p.is_file() or p.suffix.lower() not in {".csv", ".txt", ".tsv", ".json"}:
            continue
        low = p.stem.lower().replace("_", " ")
        if any(x in low for x in excludes):
            continue
        if any(stem.lower() in low for stem in stems):
            return p
    return None


def row_get_ci(row: dict[str, Any], *names: str) -> Any:
    km = {str(k).strip().lower(): k for k in row}
    for name in names:
        if name.lower() in km:
            return row[km[name.lower()]]
    return None


def import_onet(args: argparse.Namespace) -> None:
    con = connect(args.db); init_db(con)
    d = Path(args.directory).expanduser()
    occ_file = find_file(d, ["occupation data"])
    if not occ_file:
        raise SystemExit("Could not find an O*NET Occupation Data CSV/TXT file in the directory.")
    occ_rows = read_delimited(occ_file)
    for r in occ_rows:
        code = str(row_get_ci(r,"O*NET-SOC Code","onetsoc_code") or "").strip()
        title = str(row_get_ci(r,"Title","title") or "").strip()
        if code and title:
            con.execute("INSERT OR REPLACE INTO onet_occupations(code,title) VALUES(?,?)", (code,title))
    con.execute("DELETE FROM onet_attributes")
    specs = [
        ("essential_skill", ["essential skills"]),
        ("transferable_skill", ["transferable skills"]),
        ("software_skill", ["software skills", "technology skills"]),
        ("training_experience", ["training and experience"]),
        ("education", ["education"]),
        ("job_zone", ["job zones"]),
    ]
    counts = {}
    for kind, stems in specs:
        excludes = ["categor"] if kind in {"education", "training_experience"} else (["reference"] if kind == "job_zone" else [])
        p = find_file(d, stems, excludes=excludes)
        if not p:
            continue
        n = 0
        for r in read_delimited(p):
            code = str(row_get_ci(r,"O*NET-SOC Code","onetsoc_code") or "").strip()
            if not code:
                continue
            name = str(row_get_ci(r,"Element Name","element_name","Workplace Example","workplace_example","Job Zone","job_zone") or "").strip()
            if kind == "software_skill":
                name = str(row_get_ci(r,"Workplace Example","workplace_example") or name).strip()
            if kind == "job_zone":
                name = "Job Zone"
            if not name:
                continue
            scale = str(row_get_ci(r,"Scale Name","scale_name") or "").strip() or None
            value = parse_float(row_get_ci(r,"Data Value","data_value","Job Zone","job_zone"))
            category = str(row_get_ci(r,"Category","category") or "").strip() or None
            hot = 1 if str(row_get_ci(r,"Hot Technology","hot_technology") or "").strip().upper()=="Y" else 0
            demand = 1 if str(row_get_ci(r,"In Demand","in_demand") or "").strip().upper()=="Y" else 0
            con.execute("INSERT INTO onet_attributes(code,kind,name,scale_name,data_value,category,hot_technology,in_demand) VALUES(?,?,?,?,?,?,?,?)",
                        (code,kind,name,scale,value,category,hot,demand))
            n += 1
        counts[kind] = n
    con.execute("INSERT INTO source_runs(source,kind,imported_at,notes) VALUES(?,?,?,?)",
                ("O*NET local import","onet",dt.datetime.now(dt.timezone.utc).isoformat(),f"directory={d}; counts={json.dumps(counts)}"))
    con.commit()
    print(json.dumps({"occupations":len(occ_rows),"attributes":counts}, indent=2))


def import_oews(args: argparse.Namespace) -> None:
    con = connect(args.db); init_db(con)
    rows = load_records(args.input)
    if args.replace:
        con.execute("DELETE FROM oews")
    n = 0
    for r in rows:
        occ_code = str(row_get_ci(r,"OCC_CODE","occ_code") or "").strip() or None
        occ_title = str(row_get_ci(r,"OCC_TITLE","occ_title") or "").strip() or None
        if not occ_code and not occ_title:
            continue
        con.execute("""INSERT INTO oews(occ_code,occ_title,area_code,area_title,total_employment,employment_prse,hourly_mean,annual_mean,hourly_median,annual_median,source_date)
          VALUES(?,?,?,?,?,?,?,?,?,?,?)""", (
            occ_code, occ_title,
            str(row_get_ci(r,"AREA","area") or "").strip() or None,
            str(row_get_ci(r,"AREA_TITLE","area_title") or "").strip() or None,
            parse_float(row_get_ci(r,"TOT_EMP","total_employment")), parse_float(row_get_ci(r,"EMP_PRSE","employment_prse")),
            parse_float(row_get_ci(r,"H_MEAN","hourly_mean")), parse_float(row_get_ci(r,"A_MEAN","annual_mean")),
            parse_float(row_get_ci(r,"H_MEDIAN","hourly_median")), parse_float(row_get_ci(r,"A_MEDIAN","annual_median")), args.source_date
        )); n += 1
    con.execute("INSERT INTO source_runs(source,kind,imported_at,source_date,notes) VALUES(?,?,?,?,?)",
                (args.source,"oews",dt.datetime.now(dt.timezone.utc).isoformat(),args.source_date,f"input={Path(args.input).name}; rows={n}"))
    con.commit(); print(json.dumps({"imported":n,"source":args.source}, indent=2))


def wilson(k: int, n: int, z: float=1.96) -> tuple[float,float]:
    if n == 0: return (0.0,0.0)
    p = k/n
    den = 1 + z*z/n
    center = (p + z*z/(2*n))/den
    half = z*math.sqrt((p*(1-p)+z*z/(4*n))/n)/den
    return max(0,center-half), min(1,center+half)


def percentile(values: list[float], p: float) -> float | None:
    if not values: return None
    xs=sorted(values)
    if len(xs)==1: return xs[0]
    i=(len(xs)-1)*p
    lo=math.floor(i); hi=math.ceil(i)
    if lo==hi: return xs[lo]
    return xs[lo]*(hi-i)+xs[hi]*(i-lo)


def confidence_label(n: int) -> str:
    return "HIGH" if n >= 100 else "MEDIUM" if n >= 30 else "LOW"


def matched_postings(con: sqlite3.Connection, title: str, location: str|None, industry: str|None, since: str|None, threshold: float) -> tuple[list[sqlite3.Row], list[sqlite3.Row]]:
    rows = con.execute("SELECT * FROM postings").fetchall()
    target=[]; comp=[]
    for r in rows:
        if since and (not r["posted_date"] or r["posted_date"] < since):
            continue
        if location and location.lower() not in (r["location"] or "").lower():
            continue
        if industry and industry.lower() not in (r["industry"] or "").lower():
            continue
        sim=title_similarity(title,r["title"])
        (target if sim>=threshold else comp).append(r)
    return target, comp


def skills_for_ids(con: sqlite3.Connection, table: str, fk: str, ids: list[int]) -> dict[int,set[str]]:
    out=defaultdict(set)
    if not ids: return out
    for start in range(0,len(ids),900):
        batch=ids[start:start+900]
        qs=",".join("?"*len(batch))
        for r in con.execute(f"SELECT {fk}, skill FROM {table} WHERE {fk} IN ({qs})", batch):
            out[int(r[0])].add(r[1])
    return out


def occupation_match(con: sqlite3.Connection, title: str) -> dict[str,Any]|None:
    occs=con.execute("SELECT code,title FROM onet_occupations").fetchall()
    if not occs: return None
    best=max(occs,key=lambda r:title_similarity(title,r["title"]))
    score=title_similarity(title,best["title"])
    attrs=con.execute("SELECT * FROM onet_attributes WHERE code=?",(best["code"],)).fetchall()
    essential=[]; software=[]; training=[]
    # For scaled skill records keep maximum numeric value for each name.
    by_name={}
    for a in attrs:
        if a["kind"] in {"essential_skill","transferable_skill"}:
            key=(a["kind"],a["name"])
            cur=by_name.get(key)
            if cur is None or (a["data_value"] or -1) > (cur["data_value"] or -1): by_name[key]=a
        elif a["kind"]=="software_skill": software.append({"name":a["name"],"hot":bool(a["hot_technology"]),"in_demand":bool(a["in_demand"])})
        elif a["kind"] in {"training_experience","education","job_zone"}: training.append({"kind":a["kind"],"name":a["name"],"value":a["data_value"],"category":a["category"],"scale":a["scale_name"]})
    for a in by_name.values(): essential.append({"name":a["name"],"value":a["data_value"],"scale":a["scale_name"],"kind":a["kind"]})
    essential.sort(key=lambda x:(x["value"] is not None,x["value"] or -1),reverse=True)
    software.sort(key=lambda x:(x["in_demand"],x["hot"],x["name"]),reverse=True)
    return {"code":best["code"],"title":best["title"],"similarity":score,"skills":essential[:15],"software":software[:20],"training":training[:20]}


def outcome_associations(con: sqlite3.Connection, title: str, location: str|None, threshold: float, min_total: int=50, min_group: int=10) -> dict[str,Any]:
    rows=con.execute("SELECT * FROM outcomes").fetchall()
    matched=[]
    for r in rows:
        if location and location.lower() not in (r["location"] or "").lower(): continue
        if title_similarity(title,r["target_title"])>=threshold: matched.append(r)
    n=len(matched)
    if n<min_total:
        return {"n":n,"suppressed":True,"reason":f"fewer than {min_total} matched outcome records","skills":[],"experience_bands":[],"education_groups":[]}
    smap=skills_for_ids(con,"outcome_skills","outcome_id",[r["id"] for r in matched])
    allskills=sorted(set().union(*(smap.get(r["id"],set()) for r in matched))) if matched else []
    results=[]
    for s in allskills:
        with_s=[r for r in matched if s in smap.get(r["id"],set())]
        without=[r for r in matched if s not in smap.get(r["id"],set())]
        if len(with_s)<min_group or len(without)<min_group: continue
        hw=sum(r["hired"] for r in with_s); hn=sum(r["hired"] for r in without)
        rw=hw/len(with_s); rn=hn/len(without)
        rr=(rw/rn) if rn>0 else None
        rd=rw-rn
        # Haldane-Anscombe corrected odds ratio.
        a=hw+0.5; b=len(with_s)-hw+0.5; c=hn+0.5; d=len(without)-hn+0.5
        odds=(a*d)/(b*c)
        ci=None
        if hw>0 and hn>0 and rw<1 and rn<1 and rr:
            se=math.sqrt((1/hw)-(1/len(with_s))+(1/hn)-(1/len(without)))
            ci=(math.exp(math.log(rr)-1.96*se),math.exp(math.log(rr)+1.96*se))
        results.append({"skill":s,"with_n":len(with_s),"without_n":len(without),"hire_with":rw,"hire_without":rn,"risk_difference":rd,"risk_ratio":rr,"risk_ratio_ci":ci,"odds_ratio":odds})
    results.sort(key=lambda x:abs(x["risk_difference"]),reverse=True)
    # Structured experience benchmarks: observed hire rates by predeclared bands.
    bands=[("0-2",0,3),("3-5",3,6),("6-10",6,11),("11+",11,float("inf"))]
    experience_bands=[]
    for label,lo,hi in bands:
        grp=[r for r in matched if r["years_experience"] is not None and lo <= r["years_experience"] < hi]
        if len(grp) >= min_group:
            experience_bands.append({"band":label,"n":len(grp),"hire_rate":sum(r["hired"] for r in grp)/len(grp)})
    education_groups=[]
    ed_groups=defaultdict(list)
    for r in matched:
        if r["education"]: ed_groups[str(r["education"]).strip()].append(r)
    for label,grp in ed_groups.items():
        if len(grp) >= min_group:
            education_groups.append({"education":label,"n":len(grp),"hire_rate":sum(r["hired"] for r in grp)/len(grp)})
    education_groups.sort(key=lambda x:x["n"],reverse=True)
    return {"n":n,"suppressed":False,"skills":results[:25],"experience_bands":experience_bands,"education_groups":education_groups}


def oews_match(con: sqlite3.Connection, title: str, location: str|None) -> list[dict[str,Any]]:
    rows=con.execute("SELECT * FROM oews").fetchall()
    scored=[]
    for r in rows:
        if not r["occ_title"]: continue
        if location and location.lower() not in (r["area_title"] or "").lower(): continue
        sim=title_similarity(title,r["occ_title"])
        if sim>=0.65:
            scored.append((sim,r))
    scored.sort(key=lambda x:(x[0],x[1]["total_employment"] or 0),reverse=True)
    return [dict(r)|{"title_similarity":sim} for sim,r in scored[:5]]


def analyze(args: argparse.Namespace) -> None:
    con=connect(args.db); init_db(con)
    since=parse_date(args.since) if args.since else None
    target, comp=matched_postings(con,args.title,args.location,args.industry,since,args.title_threshold)
    ids=[r["id"] for r in target]; cids=[r["id"] for r in comp]
    smap=skills_for_ids(con,"posting_skills","posting_id",ids); cmap=skills_for_ids(con,"posting_skills","posting_id",cids)
    counts=Counter(s for pid in ids for s in smap.get(pid,set()))
    ccounts=Counter(s for pid in cids for s in cmap.get(pid,set()))
    skill_stats=[]
    for skill,k in counts.most_common():
        p=k/len(target) if target else 0
        lo,hi=wilson(k,len(target))
        ck=ccounts.get(skill,0); cp=ck/len(comp) if comp else 0
        lift=(p/cp) if len(comp)>=20 and cp>0 else None
        skill_stats.append({"skill":skill,"count":k,"prevalence":p,"ci":[lo,hi],"comparison_count":ck,"comparison_prevalence":cp,"lift":lift})
    # Pair co-occurrence from top 30 skills.
    top={x["skill"] for x in skill_stats[:30]}; pairs=Counter()
    for pid in ids:
        ss=sorted(smap.get(pid,set()) & top)
        for pair in itertools.combinations(ss,2): pairs[pair]+=1
    bundles=[{"skills":list(p),"count":n,"prevalence":n/len(target)} for p,n in pairs.most_common(15)] if target else []
    # Experience and education benchmarks.
    years=[r["years_experience"] for r in target if r["years_experience"] is not None]
    ed=Counter(r["education"] for r in target if r["education"])
    # Trend: split dated rows by midpoint date.
    dated=[r for r in target if r["posted_date"]]
    trend={}
    if len(dated)>=20:
        dated=sorted(dated,key=lambda r:r["posted_date"]); mid=len(dated)//2; early=dated[:mid]; late=dated[mid:]
        emap=skills_for_ids(con,"posting_skills","posting_id",[r["id"] for r in early]); lmap=skills_for_ids(con,"posting_skills","posting_id",[r["id"] for r in late])
        ec=Counter(s for r in early for s in emap.get(r["id"],set())); lc=Counter(s for r in late for s in lmap.get(r["id"],set()))
        for skill in top:
            ep=ec.get(skill,0)/len(early); lp=lc.get(skill,0)/len(late)
            trend[skill]={"early":ep,"late":lp,"pp_change":lp-ep}
    om=occupation_match(con,args.title)
    outcome=outcome_associations(con,args.title,args.location,args.title_threshold,args.min_outcome_total,args.min_outcome_group)
    wage=oews_match(con,args.title,args.location)
    candidate=None
    if args.candidate:
        candidate=json.loads(Path(args.candidate).expanduser().read_text(encoding="utf-8"))
        canonical,_=load_taxonomy(Path(args.taxonomy) if args.taxonomy else DEFAULT_TAXONOMY)
        cskills=canonicalize_skills(candidate.get("skills",[]),canonical)
        evidence={canonical.get(k.lower(),k):v for k,v in candidate.get("evidence",{}).items()}
        comparisons=[]
        for s in skill_stats[:30]:
            has=s["skill"] in cskills
            if has and s["prevalence"]>=0.35: action="EMPHASIZE"
            elif has: action="SECONDARY"
            else: action="GAP / DO NOT CLAIM"
            comparisons.append({"skill":s["skill"],"market_prevalence":s["prevalence"],"candidate_evidenced":has,"evidence":evidence.get(s["skill"]),"action":action})
        candidate={"skills":sorted(cskills),"years_experience":candidate.get("years_experience"),"education":candidate.get("education"),"comparison":comparisons}
    dates=[r["posted_date"] for r in target if r["posted_date"]]
    sources=Counter(r["source"] for r in target)
    result={
        "generated_at":dt.datetime.now(dt.timezone.utc).isoformat(),
        "target":{"title":args.title,"location":args.location,"industry":args.industry,"since":since,"title_threshold":args.title_threshold},
        "postings":{"n":len(target),"comparison_n":len(comp),"confidence":confidence_label(len(target)),"date_min":min(dates) if dates else None,"date_max":max(dates) if dates else None,"sources":dict(sources),"skills":skill_stats[:50],"bundles":bundles,"trend":trend,"experience":{"n":len(years),"median":statistics.median(years) if years else None,"p25":percentile(years,.25),"p75":percentile(years,.75)},"education":dict(ed.most_common())},
        "onet":om,"oews":wage,"outcomes":outcome,"candidate":candidate,
        "limitations":[
            "Posting prevalence measures employer demand, not individual hiring probability.",
            "Outcome associations are observational and may be confounded; they are not causal effects.",
            "Title matching is lexical and should be reviewed when adjacent occupations share words.",
            "Source coverage, duplicate employers, missing dates, and extraction quality can bias estimates.",
            "No unsupported market-demand skill should be presented as a candidate qualification."
        ]
    }
    text=json.dumps(result,indent=2,ensure_ascii=False) if args.json else render_markdown(result)
    if args.out:
        Path(args.out).expanduser().write_text(text,encoding="utf-8")
        print(f"Wrote {args.out}")
    else:
        print(text)


def pct(x: float|None) -> str:
    return "—" if x is None else f"{x*100:.1f}%"


def num(x: float|None, digits:int=1) -> str:
    return "—" if x is None else f"{x:.{digits}f}"


def money(x: float|None) -> str:
    return "—" if x is None else f"${x:,.0f}"


def render_markdown(r: dict[str,Any]) -> str:
    t=r["target"]; p=r["postings"]
    lines=["# Career Market Intelligence Report","",f"Generated: {r['generated_at']}","",
           "## Target definition","",f"- Title: **{t['title']}**",f"- Location: **{t['location'] or 'Broad / not filtered'}**",f"- Industry: **{t['industry'] or 'Broad / not filtered'}**",f"- Since: **{t['since'] or 'All loaded dates'}**",f"- Lexical title-match threshold: **{t['title_threshold']:.2f}**","",
           "## Evidence inventory","",f"- DEMAND matched postings: **{p['n']}** ({p['confidence']} descriptive confidence)",f"- Comparison postings: **{p['comparison_n']}**",f"- Posting dates: **{p['date_min'] or 'unknown'} to {p['date_max'] or 'unknown'}**",f"- Sources: **{', '.join(f'{k} ({v})' for k,v in p['sources'].items()) or 'none'}**","-"]
    if r.get("onet"):
        o=r["onet"]; lines += ["","## O*NET occupational baseline","",f"Mapped to **{o['title']} ({o['code']})**; lexical similarity {o['similarity']:.2f}.","","This is **DEMAND / occupational-baseline evidence**, not hiring-outcome evidence.",""]
        if o["skills"]:
            lines += ["Top imported skill attributes:",""]
            for x in o["skills"][:10]: lines.append(f"- {x['name']} — {x['scale'] or 'rating'} {num(x['value'],2)}")
        if o["software"]:
            lines += ["","Highlighted software examples:",""]
            for x in o["software"][:10]: lines.append(f"- {x['name']}" + (" — in-demand" if x['in_demand'] else "") + ("; hot technology" if x['hot'] else ""))
    lines += ["","## DEMAND: skills in matched postings","", "| Skill | Mentions | Prevalence | 95% CI | Comparison | Lift | Trend |", "|---|---:|---:|---:|---:|---:|---:|"]
    for s in p["skills"][:25]:
        tr=p["trend"].get(s["skill"],{}).get("pp_change")
        lines.append(f"| {s['skill']} | {s['count']} | {pct(s['prevalence'])} | {pct(s['ci'][0])}–{pct(s['ci'][1])} | {pct(s['comparison_prevalence']) if p['comparison_n'] else '—'} | {num(s['lift'],2)} | {('+' if tr is not None and tr>=0 else '') + (f'{tr*100:.1f} pp' if tr is not None else '—')} |")
    if p["bundles"]:
        lines += ["","## DEMAND: common skill bundles",""]
        for b in p["bundles"][:10]: lines.append(f"- {' + '.join(b['skills'])}: {b['count']} postings ({pct(b['prevalence'])})")
    lines += ["","## DEMAND: experience and education benchmarks",""]
    e=p["experience"]
    lines += [f"- Requested years detected in {e['n']} postings; median **{num(e['median'])} years**, middle 50% **{num(e['p25'])}–{num(e['p75'])} years**."]
    if p["education"]:
        lines.append("- Education mentions: " + ", ".join(f"{k}: {v}" for k,v in p["education"].items()))
    else: lines.append("- Education mentions: insufficient structured/detected data.")
    if r.get("oews"):
        lines += ["","## Official wage/employment benchmarks (OEWS import)",""]
        for x in r["oews"]:
            lines.append(f"- {x.get('occ_title')} — {x.get('area_title') or 'area unspecified'}: employment {num(x.get('total_employment'),0)}, median annual wage {money(x.get('annual_median'))}, mean annual wage {money(x.get('annual_mean'))}.")
    out=r["outcomes"]
    lines += ["","## OUTCOME-ASSOCIATED evidence",""]
    if out["suppressed"]:
        lines.append(f"Suppressed: **{out['reason']}** (matched outcome N={out['n']}).")
    elif not out["skills"]:
        lines.append(f"Matched outcome N={out['n']}, but no skill comparison met group-size thresholds.")
    else:
        lines += [f"Matched outcome records: **{out['n']}**. These are observational associations, not causal effects.","", "| Skill | With skill N | Hire rate | Without skill N | Hire rate | Difference | Risk ratio (95% CI) |", "|---|---:|---:|---:|---:|---:|---:|"]
        for x in out["skills"][:15]:
            ci=x["risk_ratio_ci"]; rr=(f"{x['risk_ratio']:.2f}" if x['risk_ratio'] is not None else "—")
            if ci: rr += f" ({ci[0]:.2f}–{ci[1]:.2f})"
            lines.append(f"| {x['skill']} | {x['with_n']} | {pct(x['hire_with'])} | {x['without_n']} | {pct(x['hire_without'])} | {x['risk_difference']*100:+.1f} pp | {rr} |")
        if out.get("experience_bands"):
            lines += ["","Observed hire rates by experience band (same outcome corpus):",""]
            for x in out["experience_bands"]: lines.append(f"- {x['band']} years: {pct(x['hire_rate'])} (N={x['n']})")
        if out.get("education_groups"):
            lines += ["","Observed hire rates by recorded education group (same outcome corpus):",""]
            for x in out["education_groups"]: lines.append(f"- {x['education']}: {pct(x['hire_rate'])} (N={x['n']})")
    c=r.get("candidate")
    if c:
        lines += ["","## Candidate-to-market comparison","", "| Skill | Market demand | Candidate evidence | Action |", "|---|---:|---|---|"]
        for x in c["comparison"][:25]:
            ev=("Yes" + (f" — {x['evidence']}" if x.get('evidence') else "")) if x["candidate_evidenced"] else "No"
            lines.append(f"| {x['skill']} | {pct(x['market_prevalence'])} | {ev} | **{x['action']}** |")
        lines += ["","### Resume implications","", "- Put **EMPHASIZE** skills near the top only when the resume can show concrete evidence or achievements.", "- Keep **SECONDARY** skills available for role-specific tailoring.", "- Treat **GAP / DO NOT CLAIM** items as learning or evidence-development opportunities; do not insert them as qualifications."]
    lines += ["","## Interpretation rules","", "- **DEMAND** means requested or observed in postings/occupational baselines.", "- **OUTCOME-ASSOCIATED** means correlated with an observed outcome in the supplied dataset.", "- **CAUSAL** requires separate credible causal evidence; this report does not infer causality automatically.", "- This report does **not** estimate an individual's probability of being hired.","","## Limitations",""]
    lines += [f"- {x}" for x in r["limitations"]]
    return "\n".join(lines)+"\n"


def cmd_init(args: argparse.Namespace) -> None:
    con=connect(args.db); init_db(con); print(f"Initialized {Path(args.db).expanduser()}")


def build_parser() -> argparse.ArgumentParser:
    p=argparse.ArgumentParser(description="Local labor-market analysis for job seekers")
    sub=p.add_subparsers(dest="cmd",required=True)
    s=sub.add_parser("init"); s.add_argument("--db",required=True); s.set_defaults(func=cmd_init)
    s=sub.add_parser("import-postings"); s.add_argument("--db",required=True); s.add_argument("--input",required=True); s.add_argument("--source",required=True); s.add_argument("--source-date"); s.add_argument("--taxonomy"); s.set_defaults(func=import_postings)
    s=sub.add_parser("import-outcomes"); s.add_argument("--db",required=True); s.add_argument("--input",required=True); s.add_argument("--cohort",required=True); s.add_argument("--taxonomy"); s.add_argument("--allow-sensitive-columns",action="store_true"); s.set_defaults(func=import_outcomes)
    s=sub.add_parser("import-onet"); s.add_argument("--db",required=True); s.add_argument("--directory",required=True); s.set_defaults(func=import_onet)
    s=sub.add_parser("import-oews"); s.add_argument("--db",required=True); s.add_argument("--input",required=True); s.add_argument("--source",default="BLS OEWS"); s.add_argument("--source-date"); s.add_argument("--replace",action="store_true"); s.set_defaults(func=import_oews)
    s=sub.add_parser("analyze"); s.add_argument("--db",required=True); s.add_argument("--title",required=True); s.add_argument("--location"); s.add_argument("--industry"); s.add_argument("--since"); s.add_argument("--candidate"); s.add_argument("--taxonomy"); s.add_argument("--title-threshold",type=float,default=.67); s.add_argument("--min-outcome-total",type=int,default=50); s.add_argument("--min-outcome-group",type=int,default=10); s.add_argument("--json",action="store_true"); s.add_argument("--out"); s.set_defaults(func=analyze)
    return p


def main() -> None:
    args=build_parser().parse_args(); args.func(args)

if __name__=="__main__": main()
