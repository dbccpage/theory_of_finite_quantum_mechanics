from __future__ import annotations

import importlib.util
from pathlib import Path
import sys


ROOT = Path(__file__).resolve().parents[2]
SCRIPT = (
    ROOT
    / ".agents"
    / "skills"
    / "ooutwire"
    / "prompt-civilization-v0-drafts"
    / "auto-antiskill"
    / "scripts"
    / "auto_antiskill.py"
)


def _module():
    spec = importlib.util.spec_from_file_location("tested_auto_antiskill", SCRIPT)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_auto_antiskill_refuses_admission_command() -> None:
    module = _module()
    original = list(sys.argv)
    try:
        sys.argv = [str(SCRIPT), "admit", "--output", "ignored.json"]
        try:
            module.main()
        except SystemExit as exc:
            assert "permits" in str(exc)
        else:
            raise AssertionError("auto-antiskill accepted an admit command")
    finally:
        sys.argv = original


def test_auto_antiskill_refuses_protected_output_path() -> None:
    module = _module()
    protected = ROOT / ".agents" / "anti_skills" / "admitted" / "registry.json"
    before = protected.read_bytes()
    original = list(sys.argv)
    try:
        sys.argv = [
            str(SCRIPT),
            "mine-candidates",
            "--episodes",
            "unused.json",
            "--output",
            str(protected),
        ]
        try:
            module.main()
        except SystemExit as exc:
            assert "ooutwire" in str(exc)
        else:
            raise AssertionError("auto-antiskill accepted a protected output")
    finally:
        sys.argv = original
    assert protected.read_bytes() == before


def test_auto_antiskill_requires_explicit_candidate_output() -> None:
    module = _module()
    original = list(sys.argv)
    try:
        sys.argv = [str(SCRIPT), "segment-dialogue", "--source", "unused.txt"]
        try:
            module.main()
        except SystemExit as exc:
            assert "requires --output" in str(exc)
        else:
            raise AssertionError("auto-antiskill accepted an implicit output")
    finally:
        sys.argv = original


def test_pending_skills_are_inert_drafts_outside_live_discovery() -> None:
    for skill_name in ("auto-antiskill", "omega-prompt"):
        for host in (".agents", ".claude", ".codex", ".grok"):
            assert not (ROOT / host / "skills" / skill_name / "SKILL.md").exists()

        packet = (
            ROOT
            / ".agents"
            / "skills"
            / "ooutwire"
            / "prompt-civilization-v0-drafts"
            / skill_name
        )
        assert not any(path.name == "SKILL.md" for path in packet.rglob("*"))
        assert not any(path.name == "openai.yaml" for path in packet.rglob("*"))
        text = (packet / "DRAFT.md").read_text(encoding="utf-8")
        assert 'version: "0.1.0"' in text
        assert "authority_effect_ceiling: None" in text
        assert "status: Draft" in text
        assert "admission: pending" in text
        assert "../../../_shared/constraints.md" in text
