import sys
from datetime import datetime

OL_RULE_RECEIVE = 0


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

    # NOTE: "from_domain" conditions are parsed but not applied here (see parity gaps in outlook_vba.py).
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


