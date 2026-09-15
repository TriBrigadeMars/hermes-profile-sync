import re

# Stop-word guard used by the heuristic parser. Deliberately a superset of the
# three previously-inline sets so the guards are uniform and slightly conservative.
ACTION_VERBS = {
    "move", "copy", "categorize", "flag", "forward",
    "reply", "mark", "delete", "except", "but", "unless",
}


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
                if name.lower().split()[0] not in ACTION_VERBS:
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
                    if val.lower() not in ACTION_VERBS:
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
                if val.lower().split()[0] not in ACTION_VERBS:
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

