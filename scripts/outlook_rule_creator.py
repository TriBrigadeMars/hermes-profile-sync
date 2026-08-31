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
from datetime import datetime


# ─── Constants ────────────────────────────────────────────────────────────────

OL_RULE_RECEIVE = 0


# ─── Plain English Parser ─────────────────────────────────────────────────────

class RuleParser:
    """Parse plain English rule descriptions into structured rule specs."""

    def parse(self, text: str) -> dict:
        text = text.strip().rstrip(".")
        spec = {
            "name": text[:60] + ("..." if len(text) > 60 else ""),
            "conditions": [],
            "actions": [],
            "exceptions": [],
        }
        main_text, exception_texts = self._split_exceptions(text)
        spec["conditions"] = self._parse_conditions(main_text)
        spec["actions"] = self._parse_actions(main_text)
        for exc_text in exception_texts:
            spec["exceptions"].extend(self._parse_conditions(exc_text))
        return spec

    def _split_exceptions(self, text: str) -> tuple:
        pattern = r"(?:,\s*)?(?:except\s+if|unless|but\s+not)\s+(.+?)(?:\s*$)"
        match = re.search(pattern, text, re.IGNORECASE)
        if match:
            return text[:match.start()].rstrip(" ,"), [match.group(1).strip()]
        return text, []

    def _parse_conditions(self, text: str) -> list:
        conditions = []

        # From domain — "from any @domain.com" (check BEFORE specific email/name)
        m = re.search(r"from\s+any\s+@([a-zA-Z0-9.\-]+\.[a-zA-Z]{2,})", text, re.IGNORECASE)
        if m:
            conditions.append({"type": "from_domain", "value": "@" + m.group(1)})

        # From (specific email) — skip if "any" precedes it
        m = re.search(
            r"from\s+(?!any\s+)(?:sender\s+(?:is|from)\s+)?['\"]?([a-zA-Z0-9._%+\-]+@[a-zA-Z0-9.\-]+\.[a-zA-Z]{2,})['\"]?",
            text, re.IGNORECASE
        )
        if m and not any(c["type"] == "from_domain" for c in conditions):
            conditions.append({"type": "from", "value": m.group(1)})

        # From (person name) — only if no email or domain already found
        if not any(c["type"] in ("from", "from_domain") for c in conditions):
            m = re.search(
                r"from\s+(?!any\s+)(?:sender\s+(?:is|from)\s+)?['\"]?([A-Z][a-zA-Z\s.]+)['\"]?",
                text, re.IGNORECASE
            )
            if m:
                name = m.group(1).strip()
                action_verbs = {"move", "copy", "categorize", "flag", "forward",
                                "reply", "mark", "delete", "except", "but", "unless"}
                if name.lower().split()[0] not in action_verbs:
                    conditions.append({"type": "from", "value": name})

        # Subject contains
        m = re.search(r"subject\s+(?:contains?|has)\s+['\"](.+?)['\"]", text, re.IGNORECASE)
        if m:
            conditions.append({"type": "subject_contains", "value": m.group(1)})
        else:
            m = re.search(
                r"subject\s+(?:contains?|has)\s+(.+?)(?:\s+(?:except|unless|but|to|as|for|and|with|in|on|or)(?:\s|$))",
                text, re.IGNORECASE
            )
            if m:
                conditions.append({"type": "subject_contains", "value": m.group(1).strip()})

        # "about <topic>" → subject contains
        if not any(c["type"] == "subject_contains" for c in conditions):
            m = re.search(r"about\s+['\"](.+?)['\"]", text, re.IGNORECASE)
            if m:
                conditions.append({"type": "subject_contains", "value": m.group(1)})
            else:
                m = re.search(
                    r"about\s+(.+?)(?:\s+(?:to|as|for|and|with|in|on|or|except|unless|but)(?:\s|$))",
                    text, re.IGNORECASE
                )
                if m:
                    val = m.group(1).strip()
                    action_verbs = {"move", "copy", "categorize", "flag", "forward",
                                    "reply", "mark", "delete"}
                    if val.lower() not in action_verbs:
                        conditions.append({"type": "subject_contains", "value": val})

        # Body contains
        m = re.search(r"body\s+(?:contains?|has)\s+['\"](.+?)['\"]", text, re.IGNORECASE)
        if not m:
            m = re.search(
                r"(?:the\s+)?body\s+(?:contains?|has)\s+(.+?)(?:\s+(?:except|unless|but|to|as|for|and|with|in|on|or)(?:\s|$))",
                text, re.IGNORECASE
            )
        if m:
            conditions.append({"type": "body_contains", "value": m.group(1).strip()})

        # Importance
        m = re.search(
            r"(?:importance|priority)\s+(?:is\s+)?(high|low|normal|urgent|important)",
            text, re.IGNORECASE
        )
        if m:
            imp = m.group(1).lower()
            val = "high" if imp in ("high", "urgent", "important") else ("low" if imp == "low" else "normal")
            conditions.append({"type": "importance", "value": val})

        # Only to me
        if re.search(r"(?:sent\s+)?only\s+to\s+me", text, re.IGNORECASE):
            conditions.append({"type": "only_to_me", "value": True})

        # With attachments
        if re.search(r"with\s+attachments?", text, re.IGNORECASE):
            conditions.append({"type": "has_attachment", "value": True})

        return conditions

    def _parse_actions(self, text: str) -> list:
        actions = []

        # Move to folder — match "move ... to <folder>" (quotes first, then bare name)
        m = re.search(
            r"move\s+(?:\w+\s+)*to\s+['\"](.+?)['\"]",
            text, re.IGNORECASE
        )
        if m:
            actions.append({"type": "move_to_folder", "value": m.group(1).strip()})
        else:
            # "Move emails from X to FolderName" — grab the final "to <name>" phrase
            # Also handles "Move emails from any @domain.com address to Shopping"
            m = re.search(
                r"move\s+.*?\bto\s+([A-Za-z][A-Za-z0-9_ /&\-]*?)(?:\s+(?:except|unless|but|and|or|,)|\s*$)",
                text, re.IGNORECASE
            )
            if m:
                val = m.group(1).strip().rstrip(" .,;")
                action_verbs = {"forward", "reply", "categorize", "flag", "delete", "mark"}
                if val.lower().split()[0] not in action_verbs:
                    actions.append({"type": "move_to_folder", "value": val})

        # Copy to folder
        m = re.search(r"copy\s+(?:them\s+)?to\s+['\"](.+?)['\"]", text, re.IGNORECASE)
        if m:
            actions.append({"type": "copy_to_folder", "value": m.group(1).strip()})

        # Categorize — "Categorize as X" or "Categorize ... as X"
        m = re.search(
            r"categoriz(?:e|y)\s+.*?\bas\s+['\"]?([A-Za-z0-9_ &\-]+?)['\"]?(?:\s*$|\s+(?:except|unless|but|and|or|,))",
            text, re.IGNORECASE
        )
        if m:
            actions.append({"type": "categorize", "value": m.group(1).strip().rstrip(" .,;")})

        # Flag
        if re.search(r"flag\s+(?:them|it)?(?:\s+for\s+follow[\s-]*up)?", text, re.IGNORECASE):
            actions.append({"type": "flag", "value": True})

        # Forward — "forward to X@Y" or "Forward emails from X to Y@Z"
        m = re.search(
            r"forward\s+.*?\bto\s+['\"]?([a-zA-Z0-9._%+\-]+@[a-zA-Z0-9.\-]+\.[a-zA-Z]{2,})['\"]?",
            text, re.IGNORECASE
        )
        if m:
            actions.append({"type": "forward_to", "value": m.group(1)})

        # Reply with
        m = re.search(r"reply\s+(?:with|using)\s+['\"](.+?)['\"]", text, re.IGNORECASE)
        if m:
            actions.append({"type": "reply_with", "value": m.group(1)})

        # Mark as read / unread — "mark ... as read" or "mark them as read"
        if re.search(r"mark\s+.*?\bas\s+read", text, re.IGNORECASE):
            actions.append({"type": "mark_as_read", "value": True})
        elif re.search(r"mark\s+.*?\bas\s+unread", text, re.IGNORECASE):
            actions.append({"type": "mark_as_unread", "value": True})

        # Delete
        if re.search(r"\bdelete\s+(?:them|it)?\b", text, re.IGNORECASE):
            actions.append({"type": "delete", "value": True})

        # Junk
        if re.search(r"move\s+(?:them\s+)?to\s+junk", text, re.IGNORECASE):
            actions.append({"type": "move_to_junk", "value": True})

        return actions


# ─── Outlook COM Interface ─────────────────────────────────────────────────────

class OutlookRuleCreator:
    """Create Outlook rules via COM automation."""

    def __init__(self):
        self.outlook = None
        self.ns = None

    def connect(self) -> bool:
        try:
            import win32com.client
            # Try Dispatch first (works from any process context)
            try:
                self.outlook = win32com.client.Dispatch("Outlook.Application")
                self.ns = self.outlook.GetNamespace("MAPI")
                return True
            except Exception:
                pass
            # Fallback: GetActiveObject (only works from same context)
            try:
                self.outlook = win32com.client.GetActiveObject("Outlook.Application")
                self.ns = self.outlook.GetNamespace("MAPI")
                return True
            except Exception:
                pass
            # Fallback: EnsureDispatch (generates type lib cache)
            try:
                self.outlook = win32com.client.gencache.EnsureDispatch("Outlook.Application")
                self.ns = self.outlook.GetNamespace("MAPI")
                return True
            except Exception as e:
                raise e
        except Exception as e:
            print(f"Error: Could not connect to Outlook — {e}", file=sys.stderr)
            print("Make sure Outlook Desktop (Classic) is running and signed in.", file=sys.stderr)
            return False

    def get_rules(self) -> list:
        if not self.connect():
            return []
        try:
            rules = self.ns.DefaultStore.GetRules()
            return [{"name": r.Name, "enabled": r.Enabled, "execution_order": r.ExecutionOrder} for r in rules]
        except Exception as e:
            print(f"Error reading rules: {e}", file=sys.stderr)
            return []

    def create_rule(self, spec: dict, dry_run: bool = False) -> dict:
        if not self.connect():
            return {"success": False, "error": "Could not connect to Outlook"}

        name = spec.get("name", f"Rule {datetime.now().strftime('%Y%m%d_%H%M%S')}")
        conditions = spec.get("conditions", [])
        actions = spec.get("actions", [])
        exceptions = spec.get("exceptions", [])

        if not conditions:
            return {"success": False, "error": "No conditions — would match ALL emails"}
        if not actions:
            return {"success": False, "error": "No actions — rule would do nothing"}

        result = {"success": True, "dry_run": dry_run, "name": name,
                  "conditions": conditions, "actions": actions, "exceptions": exceptions}

        if dry_run:
            return result

        try:
            rules = self.ns.DefaultStore.GetRules()
            rule = rules.Create(name, OL_RULE_RECEIVE)
            for c in conditions:
                self._apply_condition(rule, c)
            for a in actions:
                self._apply_action(rule, a)
            for e in exceptions:
                self._apply_condition(rule, e, is_exception=True)
            rules.Save()
            result["message"] = f"Rule '{name}' created with {len(conditions)} condition(s) and {len(actions)} action(s)."
        except Exception as e:
            result["success"] = False
            result["error"] = str(e)
        return result

    def _apply_condition(self, rule, cond: dict, is_exception: bool = False):
        target = rule.Exceptions if is_exception else rule.Conditions
        ct = cond["type"]
        v = cond.get("value", "")

        if ct == "from":
            c = target.From
            c.Enabled = True
            c.Recipients.Add(str(v))
            c.Recipients.ResolveAll()
        elif ct == "subject_contains":
            c = target.Subject
            c.Enabled = True
            c.Text = [str(v)]
        elif ct == "body_contains":
            c = target.Body
            c.Enabled = True
            c.Text = [str(v)]
        elif ct == "importance":
            c = target.Importance
            c.Enabled = True
            c.Importance = {"high": 2, "low": 0}.get(v, 1)
        elif ct == "only_to_me":
            target.OnlyToMe.Enabled = True
        elif ct == "has_attachment":
            target.HasAttachment.Enabled = True

    def _apply_action(self, rule, act: dict):
        at = act["type"]
        v = act.get("value", "")

        if at == "move_to_folder":
            folder = self._find_folder(str(v))
            if not folder:
                try:
                    inbox = self.ns.GetDefaultFolder(6)
                    folder = inbox.Folders.Add(str(v))
                except Exception as e:
                    print(f"Warning: Could not create folder '{v}': {e}", file=sys.stderr)
                    return
            rule.Actions.MoveToFolder.Enabled = True
            rule.Actions.MoveToFolder.Folder = folder
        elif at == "copy_to_folder":
            folder = self._find_folder(str(v))
            if folder:
                rule.Actions.CopyToFolder.Enabled = True
                rule.Actions.CopyToFolder.Folder = folder
        elif at == "categorize":
            rule.Actions.Categorize.Enabled = True
            rule.Actions.Categorize.Categories.Add(str(v))
        elif at == "flag":
            rule.Actions.Flag.Enabled = True
            rule.Actions.Flag.FlagStatus = 1
        elif at == "forward_to":
            rule.Actions.Forward.Enabled = True
            rule.Actions.Forward.Recipients.Add(str(v))
            rule.Actions.Forward.Recipients.ResolveAll()
        elif at == "reply_with":
            rule.Actions.Reply.Enabled = True
            rule.Actions.Reply.Text = str(v)
        elif at == "mark_as_read":
            rule.Actions.MarkAsRead.Enabled = True
        elif at == "mark_as_unread":
            rule.Actions.MarkAsUnread.Enabled = True
        elif at == "delete":
            rule.Actions.Delete.Enabled = True
        elif at == "move_to_junk":
            try:
                junk = self.ns.GetDefaultFolder(23)
                rule.Actions.MoveToFolder.Enabled = True
                rule.Actions.MoveToFolder.Folder = junk
            except Exception:
                pass

    def _find_folder(self, name: str):
        try:
            inbox = self.ns.GetDefaultFolder(6)
            for folder in inbox.Folders:
                if folder.Name.lower() == name.lower():
                    return folder
            if "/" in name:
                current = inbox
                for part in name.split("/"):
                    found = False
                    for folder in current.Folders:
                        if folder.Name.lower() == part.strip().lower():
                            current = folder
                            found = True
                            break
                    if not found:
                        return None
                return current
        except Exception:
            pass
        return None


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


def generate_vba(spec: dict) -> str:
    """Generate VBA code for copy/paste into Outlook's VBA editor."""
    lines = [
        "' === Auto-generated Outlook Rule VBA Code ===",
        f"' Rule: {spec['name']}",
        "' Paste into Outlook VBA editor (Alt+F11)",
        "",
        "Sub CreateRule()",
        "    Dim colRules As Outlook.Rules",
        "    Dim oRule As Outlook.Rule",
        "    Set colRules = Application.Session.DefaultStore.GetRules()",
        f'    Set oRule = colRules.Create("{spec["name"]}", olRuleReceive)',
        "",
    ]
    for c in spec["conditions"]:
        if c["type"] == "from":
            lines += [
                f"    ' Condition: sender is '{c['value']}'",
                "    oRule.Conditions.From.Enabled = True",
                f'    oRule.Conditions.From.Recipients.Add ("{c["value"]}")',
                "    oRule.Conditions.From.Recipients.ResolveAll", "",
            ]
        elif c["type"] == "subject_contains":
            lines += [
                f"    ' Condition: subject contains '{c['value']}'",
                "    oRule.Conditions.Subject.Enabled = True",
                f'    oRule.Conditions.Subject.Text = Array("{c["value"]}")', "",
            ]
        elif c["type"] == "body_contains":
            lines += [
                f"    ' Condition: body contains '{c['value']}'",
                "    oRule.Conditions.Body.Enabled = True",
                f'    oRule.Conditions.Body.Text = Array("{c["value"]}")', "",
            ]
    for a in spec["actions"]:
        if a["type"] == "move_to_folder":
            lines += [
                f"    ' Action: move to '{a['value']}'",
                "    oRule.Actions.MoveToFolder.Enabled = True",
                f'    Set oRule.Actions.MoveToFolder.Folder = Application.Session.GetDefaultFolder(olFolderInbox).Folders("{a["value"]}")', "",
            ]
        elif a["type"] == "categorize":
            lines += [
                f"    ' Action: categorize as '{a['value']}'",
                "    oRule.Actions.Categorize.Enabled = True",
                f'    oRule.Actions.Categorize.Categories.Add ("{a["value"]}")', "",
            ]
        elif a["type"] == "forward_to":
            lines += [
                f"    ' Action: forward to '{a['value']}'",
                "    oRule.Actions.Forward.Enabled = True",
                f'    oRule.Actions.Forward.Recipients.Add ("{a["value"]}")',
                "    oRule.Actions.Forward.Recipients.ResolveAll", "",
            ]
        elif a["type"] == "delete":
            lines += ["    ' Action: delete", "    oRule.Actions.Delete.Enabled = True", ""]
        elif a["type"] == "mark_as_read":
            lines += ["    ' Action: mark as read", "    oRule.Actions.MarkAsRead.Enabled = True", ""]
        elif a["type"] == "flag":
            lines += ["    ' Action: flag for follow-up", "    oRule.Actions.Flag.Enabled = True", "    oRule.Actions.Flag.FlagStatus = 1", ""]
    lines += ["    colRules.Save", "    MsgBox 'Rule created successfully!'", "End Sub"]
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
