#!/usr/bin/env python3
"""Conservative local guardrails for professional-reframing drafts.

This tool does not decide whether a claim is true. It flags wording that often
adds scope, authority, causality, expertise, or corporate sludge so a human or
Hermes can verify it against source evidence.
"""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path

BUZZWORDS = {
    "results-driven": "generic self-evaluation",
    "dynamic leader": "generic status claim",
    "thought leader": "generic status claim",
    "proven track record": "generic self-evaluation",
    "passionate self-starter": "generic self-evaluation",
    "change agent": "generic status claim",
    "world-class": "vague superlative",
    "best-in-class": "vague superlative",
    "synergy": "often vague business jargon",
    "synergies": "often vague business jargon",
    "holistic": "often vague without defined scope",
    "robust": "often vague without a concrete property",
}

REVIEW_TERMS = {
    "leverage": "plain-language alternative may be clearer",
    "leveraged": "plain-language alternative may be clearer",
    "optimize": "verify what specifically improved",
    "optimized": "verify what specifically improved",
    "transformational": "verify material transformation",
    "strategic": "verify strategy-level scope",
    "innovative": "show the innovation rather than self-labeling",
}

HIGH_SCOPE_PATTERNS = {
    r"\bled\b": "leadership",
    r"\bleading\b": "leadership",
    r"\bowned\b": "ownership",
    r"\bownership\b": "ownership",
    r"\bmanaged\b": "management",
    r"\bdirected\b": "direction authority",
    r"\bspearheaded\b": "leadership",
    r"\bexecutive\b": "executive scope",
    r"\bc-suite\b": "executive exposure",
    r"\bboard[- ]facing\b": "board exposure",
    r"\benterprise[- ]wide\b": "enterprise scope",
    r"\borganization[- ]wide\b": "organization-wide scope",
    r"\bglobal\b": "global scope",
    r"\bp&l\b": "P&L responsibility",
    r"\bbudget owner\b": "budget ownership",
    r"\bexpert\b": "expertise level",
    r"\bexpertise\b": "expertise level",
    r"\bstrategic advisor\b": "strategic advisory authority",
}

CAUSAL_PATTERNS = {
    r"\bresulting in\b": "causal outcome",
    r"\bdrove\b": "causation/ownership",
    r"\bdriving\b": "causation/ownership",
    r"\bdelivered a?\s*\d": "quantified causal outcome",
    r"\bsaved\s+\$?\d": "quantified savings",
    r"\breduced\s+.*\d+%": "quantified reduction",
    r"\bincreased\s+.*\d+%": "quantified increase",
}


def read_text(path: str) -> str:
    return Path(path).read_text(encoding="utf-8")


def find_phrases(text: str, mapping: dict[str, str]) -> list[dict[str, str]]:
    low = text.lower()
    found = []
    for phrase, reason in mapping.items():
        if phrase in low:
            found.append({"phrase": phrase, "reason": reason})
    return found


def lint(text: str) -> dict:
    flags = []
    flags.extend({"type": "buzzword", **x} for x in find_phrases(text, BUZZWORDS))
    flags.extend({"type": "review", **x} for x in find_phrases(text, REVIEW_TERMS))

    for pattern, reason in HIGH_SCOPE_PATTERNS.items():
        if re.search(pattern, text, re.I):
            flags.append({"type": "scope-review", "phrase": pattern, "reason": reason})
    for pattern, reason in CAUSAL_PATTERNS.items():
        if re.search(pattern, text, re.I):
            flags.append({"type": "causality-review", "phrase": pattern, "reason": reason})

    long_sentences = []
    for sentence in re.split(r"(?<=[.!?])\s+", text.strip()):
        words = re.findall(r"\b\w+[\w'-]*\b", sentence)
        if len(words) > 35:
            long_sentences.append({"words": len(words), "text": sentence})

    if re.search(r"\bresponsible for\b", text, re.I):
        flags.append({
            "type": "style-review",
            "phrase": "responsible for",
            "reason": "consider a direct action verb if the evidence supports one",
        })

    return {"flags": flags, "long_sentences": long_sentences}


def compare(original: str, revised: str) -> dict:
    original_low = original.lower()
    introduced = []
    for pattern, reason in {**HIGH_SCOPE_PATTERNS, **CAUSAL_PATTERNS}.items():
        rev_match = re.search(pattern, revised, re.I)
        orig_match = re.search(pattern, original, re.I)
        if rev_match and not orig_match:
            introduced.append({
                "term": rev_match.group(0),
                "category": reason,
                "status": "REQUIRES_EVIDENCE",
            })

    # Detect newly introduced numerals, percentages, or dollar figures.
    num_re = re.compile(r"\$?\d+(?:\.\d+)?%?")
    orig_nums = set(num_re.findall(original))
    new_nums = sorted(set(num_re.findall(revised)) - orig_nums)
    for value in new_nums:
        introduced.append({
            "term": value,
            "category": "new quantified claim",
            "status": "REQUIRES_EVIDENCE",
        })

    return {
        "introduced_claim_risks": introduced,
        "revision_lint": lint(revised),
        "note": "Heuristic only: verify flags against the user's evidence.",
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    sub = parser.add_subparsers(dest="command", required=True)

    lint_p = sub.add_parser("lint")
    lint_p.add_argument("--file", required=True)
    lint_p.add_argument("--json", action="store_true")

    cmp_p = sub.add_parser("compare")
    cmp_p.add_argument("--original", required=True)
    cmp_p.add_argument("--revised", required=True)
    cmp_p.add_argument("--json", action="store_true")

    args = parser.parse_args()
    if args.command == "lint":
        result = lint(read_text(args.file))
    else:
        result = compare(read_text(args.original), read_text(args.revised))

    if getattr(args, "json", False):
        print(json.dumps(result, indent=2))
        return

    if args.command == "compare":
        print("CLAIM-DELTA REVIEW")
        risks = result["introduced_claim_risks"]
        if not risks:
            print("No high-risk scope/metric terms were newly introduced by the heuristic.")
        else:
            for item in risks:
                print(f"- {item['status']}: {item['term']} ({item['category']})")
        lint_result = result["revision_lint"]
    else:
        lint_result = result

    if lint_result["flags"]:
        print("\nWORDING REVIEW")
        for item in lint_result["flags"]:
            print(f"- {item['type']}: {item['phrase']} - {item['reason']}")
    if lint_result["long_sentences"]:
        print("\nLONG SENTENCES")
        for item in lint_result["long_sentences"]:
            print(f"- {item['words']} words: {item['text']}")


if __name__ == "__main__":
    main()
