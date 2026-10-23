"""MUR publication Lean does not ship vacuous True theorems or OPEN stubs."""

from __future__ import annotations

from pathlib import Path

LEAN = Path(__file__).resolve().parents[2] / "lean4"
SOUNDNESS = LEAN / "L03P01T06Soundness.lean"
WRAPPER = LEAN / "Core.lean"
LAKE = LEAN / "lakefile.lean"
L02 = LEAN / "L02TerminalNonBypass.lean"


def test_soundness_wrapper_binds_l02_not_true_trivial() -> None:
    soundness = SOUNDNESS.read_text(encoding="utf-8")
    l02 = L02.read_text(encoding="utf-8")
    assert "True := by" not in soundness
    assert "by\n  trivial" not in soundness
    assert "terminal_non_bypass_soundness" not in soundness
    assert "chi_alone_does_not_imply_target_authority" in soundness
    assert "theorem chi_alone_does_not_imply_target_authority" in l02


def test_programme_wrapper_drops_open_unit_placeholder() -> None:
    wrapper = WRAPPER.read_text(encoding="utf-8")
    lake = LAKE.read_text(encoding="utf-8")
    assert "T02T07Instances" not in wrapper
    assert "T02T07Instances" not in lake
    assert "Algebra" in wrapper
    assert "L02TerminalNonBypass" in wrapper
