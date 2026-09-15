def generate_vba(spec: dict) -> str:
    """Generate VBA code for copy/paste into Outlook's VBA editor."""
    # KNOWN PARITY GAPS (do not implement without verifying the Outlook object model):
    #   conditions: "from_domain" (also unhandled by the COM layer — needs a fix there too)
    #   actions:    "reply_with", "mark_as_unread", "move_to_junk"
    # These have no confidently-verifiable VBA/COM property here; leave them.
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
        elif c["type"] == "importance":
            imp = {"high": 2, "low": 0}.get(c["value"], 1)
            lines += [
                f"    ' Condition: importance is '{c['value']}'",
                "    oRule.Conditions.Importance.Enabled = True",
                f"    oRule.Conditions.Importance.Importance = {imp}", "",
            ]
        elif c["type"] == "only_to_me":
            lines += [
                "    ' Condition: sent only to me",
                "    oRule.Conditions.OnlyToMe.Enabled = True", "",
            ]
        elif c["type"] == "has_attachment":
            lines += [
                "    ' Condition: has attachments",
                "    oRule.Conditions.HasAttachment.Enabled = True", "",
            ]
    for a in spec["actions"]:
        if a["type"] == "move_to_folder":
            lines += [
                f"    ' Action: move to '{a['value']}'",
                "    oRule.Actions.MoveToFolder.Enabled = True",
                f'    Set oRule.Actions.MoveToFolder.Folder = Application.Session.GetDefaultFolder(olFolderInbox).Folders("{a["value"]}")', "",
            ]
        elif a["type"] == "copy_to_folder":
            lines += [
                f"    ' Action: copy to '{a['value']}'",
                "    oRule.Actions.CopyToFolder.Enabled = True",
                f'    Set oRule.Actions.CopyToFolder.Folder = Application.Session.GetDefaultFolder(olFolderInbox).Folders("{a["value"]}")', "",
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
    for e in spec.get("exceptions", []):
        if e["type"] == "from":
            lines += [
                f"    ' Exception: sender is not '{e['value']}'",
                "    oRule.Exceptions.From.Enabled = True",
                f'    oRule.Exceptions.From.Recipients.Add ("{e["value"]}")',
                "    oRule.Exceptions.From.Recipients.ResolveAll", "",
            ]
        elif e["type"] == "subject_contains":
            lines += [
                f"    ' Exception: subject does not contain '{e['value']}'",
                "    oRule.Exceptions.Subject.Enabled = True",
                f'    oRule.Exceptions.Subject.Text = Array("{e["value"]}")', "",
            ]
        elif e["type"] == "body_contains":
            lines += [
                f"    ' Exception: body does not contain '{e['value']}'",
                "    oRule.Exceptions.Body.Enabled = True",
                f'    oRule.Exceptions.Body.Text = Array("{e["value"]}")', "",
            ]
    lines += ["    colRules.Save", "    MsgBox 'Rule created successfully!'", "End Sub"]
    return "\n".join(lines)


