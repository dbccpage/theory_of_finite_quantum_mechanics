"""Tests for scripts/gleason_lean_audit.py: Unicode identifiers survive, and the verifier fails closed."""
from __future__ import annotations

import hashlib
import json
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent))
import gleason_lean_audit as audit  # noqa: E402

MODULE_SOURCE = {
    "BornGaussianParallelogramRigidity": "namespace BornFinite.GaussianTomography\n\ntheorem alg_one : True := trivial\n\nend BornFinite.GaussianTomography\n",
    "GleasonRealSphere": "namespace GleasonReal\n/-- doc with a fake `theorem not_here` inside -/\nlemma real_one : True := trivial\n-- theorem commented_out : False := sorry\nend GleasonReal\n",
    "GleasonComplexSphere": "namespace GleasonComplex\nstructure Frame where\n  x : Nat\n@[simp] lemma simp_one : True := trivial\nend GleasonComplex\n",
    "GleasonGaussianBridge": (
        "namespace BornFinite.GleasonBridge\n"
        "noncomputable def f₀ (x : Nat) : Nat := x\n"
        "def ι (x : Nat) : Nat := x\n"
        "lemma nonZero_of_ι_ne_zero : True := trivial\n"
        "theorem F_ι : True := trivial\n"
        "def C₁ : Nat := 1\n"
        "section Helpers\n"
        "lemma inner_helper : True := trivial\n"
        "end Helpers\n"
        "private lemma hidden : True := trivial\n"
        "instance : Inhabited Nat := ⟨0⟩\n"
        "theorem born_of_uniformlyRayContinuous : True := trivial\n"
        "lemma zero_sub' : True := trivial\n"
        "end BornFinite.GleasonBridge\n"
    ),
    "GleasonBornCompletion": (
        "namespace BornFinite.BornCompletion\nnoncomputable section\n"
        "def Qc (x : Nat) : Nat := x\n"
        "theorem isUniformlyRayContinuous_quadRay : True := trivial\n"
        "end\nend BornFinite.BornCompletion\n"
    ),
}


def make_root(tmp_path: Path, sources: dict[str, str] | None = None) -> Path:
    root = tmp_path / "repo"
    (root / "lean4").mkdir(parents=True)
    (root / "dag" / "research").mkdir(parents=True)
    for name, text in (sources or MODULE_SOURCE).items():
        (root / audit.module_path(name)).write_text(text, encoding="utf-8")
    for dep in audit.DEPENDENCIES:
        (root / audit.module_path(dep)).write_text(f"-- {dep}\n", encoding="utf-8")
    (root / "lean4/lean-toolchain").write_text("leanprover/lean4:v4.35.0\n", encoding="utf-8")
    (root / "lean4/lake-manifest.json").write_text("{}\n", encoding="utf-8")
    (root / "lean4/lakefile.lean").write_text("-- lakefile\n", encoding="utf-8")
    return root


def good_output(root: Path) -> str:
    lines = []
    for names in audit.inventory(root).values():
        for n in names:
            lines.append(f"'{n}' depends on axioms: [propext, Classical.choice,\n Quot.sound]")
    return "\n".join(lines) + "\n"


def expectation(root: Path) -> dict:
    return {
        "schema_version": audit.SCHEMA,
        "allowed_axioms": list(audit.ALLOWED_AXIOMS),
        "pins": audit.pins(root),
        "declarations": audit.inventory(root),
    }


def test_inventory_keeps_unicode_identifiers_and_scopes(tmp_path: Path) -> None:
    root = make_root(tmp_path)
    inv = audit.inventory(root)
    bridge = inv["GleasonGaussianBridge"]
    assert "BornFinite.GleasonBridge.f₀" in bridge
    assert "BornFinite.GleasonBridge.ι" in bridge
    assert "BornFinite.GleasonBridge.nonZero_of_ι_ne_zero" in bridge
    assert "BornFinite.GleasonBridge.F_ι" in bridge
    assert "BornFinite.GleasonBridge.C₁" in bridge
    assert "BornFinite.GleasonBridge.zero_sub'" in bridge
    # a section does not change the namespace prefix
    assert "BornFinite.GleasonBridge.inner_helper" in bridge
    # private and anonymous-instance declarations are not exported bindings
    assert not any("hidden" in n for n in bridge)
    assert not any(n.endswith(":") for n in bridge)
    # no truncation: every name is a complete identifier, none repeated
    assert len(set(bridge)) == len(bridge)
    assert not any(n.endswith("_") for n in bridge)
    # comments and docstrings never contribute declarations
    assert inv["GleasonRealSphere"] == ["GleasonReal.real_one"]
    assert inv["GleasonComplexSphere"] == ["GleasonComplex.Frame", "GleasonComplex.simp_one"]
    # an anonymous `section ... end` inside a namespace does not disturb the prefix
    assert inv["GleasonBornCompletion"] == [
        "BornFinite.BornCompletion.Qc", "BornFinite.BornCompletion.isUniformlyRayContinuous_quadRay"]


def test_duplicate_names_are_an_error(tmp_path: Path) -> None:
    sources = dict(MODULE_SOURCE)
    sources["GleasonRealSphere"] = "namespace GleasonReal\nlemma a : True := trivial\nlemma a : True := trivial\nend GleasonReal\n"
    root = make_root(tmp_path, sources)
    with pytest.raises(SystemExit):
        audit.inventory(root)


def test_good_output_passes(tmp_path: Path) -> None:
    root = make_root(tmp_path)
    assert audit.verify(root, good_output(root), expectation(root)) == []


def test_missing_report_fails(tmp_path: Path) -> None:
    root = make_root(tmp_path)
    out = good_output(root).replace("'BornFinite.GleasonBridge.F_ι' depends on axioms: [propext, Classical.choice,\n Quot.sound]\n", "")
    errors = audit.verify(root, out, expectation(root))
    assert any(e == "missing report: BornFinite.GleasonBridge.F_ι" for e in errors)


def test_stale_source_fails(tmp_path: Path) -> None:
    root = make_root(tmp_path)
    exp = expectation(root)
    out = good_output(root)
    path = root / audit.module_path("BornGaussianTomographyReduction")
    path.write_text(path.read_text(encoding="utf-8") + "-- edited\n", encoding="utf-8")
    errors = audit.verify(root, out, exp)
    assert "stale source pin: lean4/BornGaussianTomographyReduction.lean" in errors


def test_changed_inventory_fails(tmp_path: Path) -> None:
    root = make_root(tmp_path)
    exp = expectation(root)
    path = root / audit.module_path("GleasonRealSphere")
    path.write_text(path.read_text(encoding="utf-8") + "lemma real_two : True := trivial\n", encoding="utf-8")
    out = good_output(root)
    errors = audit.verify(root, out, exp)
    assert any(e.startswith("declaration inventory differs") for e in errors)
    assert "stale source pin: lean4/GleasonRealSphere.lean" in errors


def test_unexpected_axiom_fails(tmp_path: Path) -> None:
    root = make_root(tmp_path)
    out = good_output(root).replace(
        "'GleasonReal.real_one' depends on axioms: [propext, Classical.choice,\n Quot.sound]",
        "'GleasonReal.real_one' depends on axioms: [propext, sorryAx]",
    )
    errors = audit.verify(root, out, expectation(root))
    assert "unexpected axioms for GleasonReal.real_one: ['sorryAx']" in errors


def test_error_line_and_forbidden_token_fail(tmp_path: Path) -> None:
    sources = dict(MODULE_SOURCE)
    sources["GleasonComplexSphere"] = "namespace GleasonComplex\nlemma bad : False := sorry\nend GleasonComplex\n"
    root = make_root(tmp_path, sources)
    exp = expectation(root)
    out = good_output(root) + "GleasonAudit.lean:3:0: error: unknown constant\n"
    errors = audit.verify(root, out, exp)
    assert "forbidden token: GleasonComplexSphere: sorry" in errors
    assert "Lean output contains an error line" in errors


def test_update_then_verify_round_trip(tmp_path: Path, capsys: pytest.CaptureFixture[str]) -> None:
    root = make_root(tmp_path)
    out_path = tmp_path / "audit.txt"
    out_path.write_text(good_output(root), encoding="utf-8")
    assert audit.main(["--root", str(root), "update", "--lean-output", str(out_path)]) == 0
    written = json.loads((root / audit.EXPECTATION).read_text(encoding="utf-8"))
    assert written["schema_version"] == audit.SCHEMA
    assert written["pins"]["lean4/GleasonGaussianBridge.lean"] == hashlib.sha256(
        (root / "lean4/GleasonGaussianBridge.lean").read_bytes()).hexdigest()
    assert audit.main(["--root", str(root), "verify", "--lean-output", str(out_path)]) == 0
    capsys.readouterr()
    # a missing expectation file is itself a failure, never a silent pass
    (root / audit.EXPECTATION).unlink()
    assert audit.main(["--root", str(root), "verify", "--lean-output", str(out_path)]) == 1
