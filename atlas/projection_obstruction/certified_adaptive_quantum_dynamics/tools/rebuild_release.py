#!/usr/bin/env python3
"""Redirect to scripts/rebuild_release.py."""
import sys
from pathlib import Path

scripts_tool = Path(__file__).resolve().parent.parent / "scripts" / "rebuild_release.py"
exec(scripts_tool.read_text(encoding="utf-8"))
