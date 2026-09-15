"""
Outlook Rule Creator — Plain English to Outlook Rules
=====================================================

Creates Outlook rules via COM automation from plain English descriptions.
No cloud APIs, no Azure — just your local Outlook desktop.

Usage:
    python outlook_rule_creator.py --describe "Move emails from newsletter@example.com to Newsletters"
    python outlook_rule_creator.py --create "Move emails from newsletter@example.com to Newsletters"
    python outlook_rule_creator.py --list
    python outlook_rule_creator.py --create "Flag emails with subject containing deadline" --dry-run
    python outlook_rule_creator.py --vba "Move emails from any @amazon.com address to Shopping"

    Interactive mode (no args):
    python outlook_rule_creator.py

License: MIT
"""

import re
import sys
import json
import argparse
from outlook_parse import RuleParser
from outlook_com import OutlookRuleCreator
from outlook_vba import generate_vba


# ─── Output Formatters ─────────────────────────────────────────────────────────

def fmt_condition(c: dict) -> str:
    labels = {
        "from":             f"Sender is '{c['value']}'",
        "from_domain":      f"Sender domain is '{c['value']}'",
        "subject_contains": f"Subject contains '{c['value']}'",
        "body_contains":    f"Body contains '{c['value']}'",
        "importance":       f"Importance is {c['value']}",
        "only_to_me":       "Sent only to me",
        "has_attachment":   "Has attachments",
    }
    return labels.get(c["type"], f"{c['type']}: {c.get('value', '')}")


def fmt_action(a: dict) -> str:
    labels = {
        "move_to_folder": f"Move to folder '{a['value']}'",
        "copy_to_folder": f"Copy to folder '{a['value']}'",
        "categorize":     f"Categorize as '{a['value']}'",
        "flag":           "Flag for follow-up",
        "forward_to":     f"Forward to '{a['value']}'",
        "reply_with":     f"Reply with '{a['value']}'",
        "mark_as_read":   "Mark as read",
        "mark_as_unread": "Mark as unread",
        "delete":         "Delete",
        "move_to_junk":   "Move to Junk",
    }
    return labels.get(a["type"], f"{a['type']}: {a.get('value', '')}")


def format_summary(spec: dict, result: dict = None) -> str:
    lines = [
        "=" * 60,
        f"RULE: {spec['name']}",
        "=" * 60,
        "",
        "Conditions:",
    ]
    for i, c in enumerate(spec["conditions"] or [("none", "")], 1):
        lines.append(f"  {i}. {fmt_condition(c) if c != ('none', '') else '(none)'}")
    lines.append("")
    lines.append("Actions:")
    for i, a in enumerate(spec["actions"] or [("none", "")], 1):
        lines.append(f"  {i}. {fmt_action(a) if a != ('none', '') else '(none)'}")
    if spec.get("exceptions"):
        lines.append("")
        lines.append("Exceptions:")
        for i, e in enumerate(spec["exceptions"], 1):
            lines.append(f"  {i}. {fmt_condition(e)}")
    if result:
        lines.append("")
        if result.get("dry_run"):
            lines.append("Status: DRY RUN — rule NOT applied to Outlook")
        elif result.get("success"):
            lines.append(f"Status: {result.get('message', 'Created successfully')}")
        else:
            lines.append(f"Status: FAILED — {result.get('error', 'Unknown error')}")
    lines.append("=" * 60)
    return "\n".join(lines)


# ─── CLI ──────────────────────────────────────────────────────────────────────

def main():
    ap = argparse.ArgumentParser(
        description="Create Outlook rules from plain English descriptions",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s --describe "Move emails from newsletter@example.com to Newsletters"
  %(prog)s --create "Flag emails from boss@company.com with subject containing deadline"
  %(prog)s --create "Categorize emails about invoice as Finance" --dry-run
  %(prog)s --list
  %(prog)s --vba "Move emails from any @amazon.com address to Shopping"
        """,
    )
    ap.add_argument("--create", "-c", help="Create a rule from plain English")
    ap.add_argument("--describe", "-d", help="Describe what a rule would do (no changes)")
    ap.add_argument("--list", "-l", action="store_true", help="List existing Outlook rules")
    ap.add_argument("--vba", "-v", help="Generate VBA code for a rule")
    ap.add_argument("--dry-run", action="store_true", help="Show what would happen without creating")
    ap.add_argument("--json", action="store_true", help="Output as JSON")
    ap.add_argument("--interactive", "-i", action="store_true", help="Interactive mode")
    args = ap.parse_args()

    parser_obj = RuleParser()

    # Interactive / no args
    if len(sys.argv) == 1 or args.interactive:
        print("Outlook Rule Creator — Interactive Mode")
        print("Describe your rule in plain English, or type 'quit' to exit.\n")
        while True:
            try:
                text = input("Rule> ").strip()
            except (EOFError, KeyboardInterrupt):
                print("\nGoodbye."); break
            if not text or text.lower() in ("quit", "exit", "q"):
                print("Goodbye."); break
            spec = parser_obj.parse(text)
            creator = OutlookRuleCreator()
            if creator.connect():
                result = creator.create_rule(spec, dry_run=True)
                print(format_summary(spec, result)); print()
                try:
                    confirm = input("Create this rule? [y/N/dry-run] ").strip().lower()
                except (EOFError, KeyboardInterrupt):
                    print("\nCancelled."); break
                if confirm == "y":
                    result = creator.create_rule(spec, dry_run=False)
                    print(format_summary(spec, result)); print()
                elif confirm == "dry-run":
                    print("(Dry run only — rule not created)\n")
                else:
                    print("(Skipped)\n")
        return

    if args.list:
        creator = OutlookRuleCreator()
        if creator.connect():
            rules = creator.get_rules()
            if not rules:
                print("No rules found.")
            else:
                print(f"{'#':<4} {'Name':<40} {'Enabled':<10} {'Order':<6}")
                print("-" * 60)
                for i, r in enumerate(rules, 1):
                    print(f"{i:<4} {r['name']:<40} {'Yes' if r['enabled'] else 'No':<10} {r['execution_order']:<6}")
        return

    if args.describe:
        spec = parser_obj.parse(args.describe)
        print(json.dumps(spec, indent=2) if args.json else format_summary(spec, {"dry_run": True}))
        return

    if args.vba:
        print(generate_vba(parser_obj.parse(args.vba)))
        return

    if args.create:
        spec = parser_obj.parse(args.create)
        creator = OutlookRuleCreator()
        if not creator.connect():
            sys.exit(1)
        if not spec["conditions"]:
            print("Warning: No conditions — would match ALL incoming emails.", file=sys.stderr); sys.exit(1)
        if not spec["actions"]:
            print("Warning: No actions — rule would do nothing.", file=sys.stderr); sys.exit(1)

        result = creator.create_rule(spec, dry_run=True)
        if args.json:
            print(json.dumps({"spec": spec, "result": result, "vba_code": generate_vba(spec)}, indent=2))
        else:
            print(format_summary(spec, result)); print()
            if not args.dry_run:
                try:
                    confirm = input("Create this rule in Outlook? [y/N] ").strip().lower()
                except (EOFError, KeyboardInterrupt):
                    print("\nCancelled."); sys.exit(0)
                if confirm != "y":
                    print("Cancelled."); sys.exit(0)
                result = creator.create_rule(spec, dry_run=False)
                print(format_summary(spec, result))
        return

    ap.print_help()


if __name__ == "__main__":
    main()
