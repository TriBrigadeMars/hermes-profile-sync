r"""Canonical Hermes-home resolution shared by all repo tooling.

Mirrors AGENTS.md section 1. Precedence:
  1. $HERMES_HOME if set and non-empty
  2. $LOCALAPPDATA\hermes on Windows
  3. ~/.hermes otherwise
Always returns a Path; callers decide whether existence matters.
"""

from __future__ import annotations

import os
from pathlib import Path


def resolve_hermes_home() -> Path:
    env = os.environ.get("HERMES_HOME")
    if env:
        return Path(env)
    localappdata = os.environ.get("LOCALAPPDATA")
    if localappdata:
        return Path(localappdata) / "hermes"
    return Path.home() / ".hermes"