#!/usr/bin/env python3
"""One-shot corpus validation for literature-review source collections.

Replaces the per-dimension ad-hoc audit round (years / DOIs / author format /
types / summaries / floor) with ONE script run producing ONE report.

Usage:
    python validate_corpus.py <corpus.json> [corpus2.json ...] [--floor 25] [--min-year 2000] [--dois N]

Checks per record:
  1. Schema — required fields present, authors is a list of "Lastname, A. A." strings
  2. Year   — parses year from ANY string field (venue strings hide years);
              flags < min-year or unparseable; keeps legitimate "n.d." web sources
  3. Authors — inverted format, no "& "-prefixed fragments, no bare initials,
              no double periods ("M.."), flags org-style names for citation-form check
  4. Type   — must be peer-reviewed | newspaper/trade | guideline/report
  5. Summary — >=60 chars (real content summary, not provenance junk)
  6. Identifier — doi_or_url present (https://doi.org/ preferred)

Report flags:
  FLOOR     — per-file count vs --floor (research+news articles vs guideline/report)
  DOI LIVE  — random sample of N DOIs checked against api.crossref.org (retries
              transient timeouts once before flagging)

Exit code 0 = all files pass; 1 = failures found (list printed).
"""
import sys, json, os, re, random, argparse, hashlib
import urllib.request

REQUIRED = ["authors", "year", "title", "journal", "doi_or_url", "type", "summary"]
TYPES = {"peer-reviewed", "newspaper/trade", "guideline/report"}
INIT_RE = re.compile(r"^[A-Z](\.\s?[A-Z])*\.?$")
ORG_HINTS = ["office", "council", "commission", "administration", "association",
             "organization", "organisation", "academy", "institute", "network",
             "evidence", "government", "board", "who", "osha", "cdc", "nih",
             "university", "clinicaltrials", "initiative", "congress", "college",
             "department", "agency", "ministry", "foundation", "collaborative",
             "pharmacy times", "says no more", "hestia", "nihr", "tuc", "ena",
             "cap today", "labcorp", "centers for disease control", "britbrief",
             "trades union"]

def parse_year(rec):
    """Find a 4-digit year in any field value; handles '2025a'-style suffix years."""
    y = rec.get("year")
    if isinstance(y, int):
        return y
    if isinstance(y, str):
        m = re.match(r"^\s*((?:19|20)\d{2})[abc]?\s*$", y)
        if m:
            return int(m.group(1))
    for v in rec.values():
        if isinstance(v, str):
            m = re.search(r"\b(19|20)\d{2}\b", v)
            if m:
                return int(m.group(0))
    return None

def check_authors(authors):
    issues = []
    if isinstance(authors, str):
        return ["authors is a plain string, not a list"]
    if not isinstance(authors, list):
        return ["authors missing or not a list"]
    for a in authors:
        if not isinstance(a, str) or not a.strip():
            issues.append(f"empty/non-string author: {a!r}")
            continue
        a = a.strip()
        if a.startswith("& "):
            issues.append(f"'& '-prefixed fragment: {a!r}")
        if ".." in a:
            issues.append(f"double period: {a!r}")
        if INIT_RE.match(a):
            issues.append(f"bare initials as author: {a!r}")
        if "," not in a and not any(h in a.lower() for h in ORG_HINTS):
            issues.append(f"no comma — maybe surname-only (verify org vs person): {a!r}")
    return issues

def validate_file(path, floor, min_year, n_dois):
    recs = json.load(open(path, encoding="utf-8"))
    if isinstance(recs, dict):
        # unwrap common container shapes
        for k in ("sources", "records", "items"):
            if k in recs and isinstance(recs[k], list):
                recs = recs[k]
                break
        else:
            if "corpora" in recs:
                out = []
                for prof in recs["corpora"].values():
                    if isinstance(prof, dict) and isinstance(prof.get("sources"), list):
                        out.extend(prof["sources"])
                recs = out
    problems = {"schema": [], "year": [], "authors": [], "type": [], "summary": [], "id": []}
    for i, r in enumerate(recs):
        t = (r.get("title") or "?")[:50]
        # 1. schema
        missing = [f for f in REQUIRED if f not in r]
        if missing:
            problems["schema"].append(f"[{i}] {t}: missing {missing}")
        # 2. year
        y = parse_year(r)
        if y is None:
            if str(r.get("year", "")).strip() == "n.d." or not r.get("year"):
                pass  # legitimate undated web source
            else:
                problems["year"].append(f"[{i}] {t}: no parseable year")
        elif y < min_year:
            problems["year"].append(f"[{i}] {t}: year {y} < {min_year}")
        # 3. authors
        for iss in check_authors(r.get("authors")):
            problems["authors"].append(f"[{i}] {t}: {iss}")
        # 4. type
        if r.get("type") not in TYPES:
            problems["type"].append(f"[{i}] {t}: bad type {r.get('type')!r}")
        # 5. summary
        if len((r.get("summary") or "").strip()) < 60:
            problems["summary"].append(f"[{i}] {t}: summary too short/missing")
        # 6. identifier
        if not (r.get("doi_or_url") or "").strip():
            problems["id"].append(f"[{i}] {t}: no doi_or_url")
    # floor: research + news articles vs guideline/report
    n_research = sum(1 for r in recs if r.get("type") in ("peer-reviewed", "newspaper/trade"))
    n_total = len(recs)
    floor_ok = n_research >= floor or n_total >= floor
    # DOI liveness sample
    dois = [r.get("doi_or_url") for r in recs
            if str(r.get("doi_or_url", "")).startswith("https://doi.org/")]
    sampled = random.sample(dois, min(n_dois, len(dois))) if dois else []
    dead = []
    for doi in sampled:
        ok = False
        for attempt in range(2):  # one retry for transient timeouts
            try:
                req = urllib.request.Request(doi.replace("doi.org/", "doi.org/api/") if False else
                                             "https://api.crossref.org/works/" + doi.rsplit("/", 1)[-1]
                                             if False else doi.replace("https://doi.org/", "https://api.crossref.org/works/"),
                                             headers={"User-Agent": "corpus-validator/1.0"})
                with urllib.request.urlopen(req, timeout=15) as resp:
                    if resp.status == 200:
                        ok = True
                        break
            except Exception:
                continue
        if not ok:
            dead.append(doi)
    return {
        "file": os.path.basename(path),
        "total": n_total,
        "research_news": n_research,
        "guideline": n_total - n_research,
        "floor_ok": floor_ok,
        "dois_checked": len(sampled),
        "dois_dead": dead,
        "problems": problems,
    }

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("files", nargs="+")
    ap.add_argument("--floor", type=int, default=25)
    ap.add_argument("--min-year", type=int, default=2000)
    ap.add_argument("--dois", type=int, default=5, help="DOI liveness sample size per file")
    args = ap.parse_args()

    failures = 0
    for path in args.files:
        try:
            rep = validate_file(path, args.floor, args.min_year, args.dois)
        except Exception as e:
            print(f"== {path}: LOAD FAILED: {e}")
            failures += 1
            continue
        status = "PASS" if (rep["floor_ok"] and not any(rep["problems"].values()) and not rep["dois_dead"]) else "FAIL"
        print(f"== {rep['file']}: {status}  (total={rep['total']}, research/news={rep['research_news']}, guideline={rep['guideline']})")
        if not rep["floor_ok"]:
            print(f"   FLOOR: only {rep['research_news']} research/news articles vs floor {args.floor}")
            failures += 1
        for cat, probs in rep["problems"].items():
            for p in probs:
                print(f"   {cat.upper()}: {p}")
                failures += 1
        for d in rep["dois_dead"]:
            print(f"   DOI DEAD (after retry): {d}")
            failures += 1
    sys.exit(1 if failures else 0)

if __name__ == "__main__":
    main()
