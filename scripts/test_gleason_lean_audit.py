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
    "BornGaussianParallelogramRigidity": (
        "namespace BornFinite.GaussianTomography\n\n"
        "  theorem alg_one : True := trivial\n\n"
        "end BornFinite.GaussianTomography\n"
    ),
    "GleasonRealSphere": (
        "namespace GleasonReal\n"
        "/-- doc with a fake `theorem not_here` and\n"
        "  /- nested `lemma also_not_here : True := trivial` -/\n"
        "inside -/\n"
        "lemma real_one : True := trivial\n"
        "-- theorem commented_out : False := sorry\n"
        "end GleasonReal\n"
    ),
    "GleasonComplexSphere": (
        "  namespace GleasonComplex\n"
        "  structure Frame where\n"
        "    x : Nat\n"
        "  @[simp] lemma simp_one : True := trivial\n"
        "  @[ext]\n"
        "  protected theorem ext_two : True := trivial\n"
        "  end GleasonComplex\n"
    ),
    "GleasonGaussianBridge": (
        "namespace BornFinite.GleasonBridge\n"
        "noncomputable def f₀ (x : Nat) : Nat := x\n"
        "def ι (x : Nat) : Nat := x\n"
        "lemma nonZero_of_ι_ne_zero : True := trivial\n"
        "theorem F_ι : True := trivial\n"
        "def C₁ : Nat := 1\n"
        "  section Helpers\n"
        "    lemma inner_helper : True := trivial\n"
        "    section Deep\n"
        "      lemma deep_helper : True := trivial\n"
        "    end Deep\n"
        "    lemma after_deep : True := trivial\n"
        "  end Helpers\n"
        "lemma after_helpers : True := trivial\n"
        "private @[simp] lemma hidden : True := trivial\n"
        "instance : Inhabited Nat := ⟨0⟩\n"
        "instance (n : Nat) : Nonempty Nat := ⟨n⟩\n"
        "scoped instance named_inst : Nonempty Bool := ⟨true⟩\n"
        "theorem born_of_uniformlyRayContinuous : True := trivial\n"
        "lemma zero_sub' : True := trivial\n"
        "end BornFinite.GleasonBridge\n"
    ),
    "GleasonBornCompletion": (
        "namespace BornFinite.BornCompletion\n"
        "  noncomputable section\n"
        "    def Qc (x : Nat) : Nat := x\n"
        "    theorem isUniformlyRayContinuous_quadRay : True := trivial\n"
        "  end\n"
        "  theorem after_noncomputable_section : True := trivial\n"
        "end BornFinite.BornCompletion\n"
    ),
    "BornGaussianFiniteModel": (
        "namespace BornFinite.GaussianFiniteModel\n"
        "  theorem finite_model_one : True := trivial\n"
        "end BornFinite.GaussianFiniteModel\n"
    ),
}

# Independent ground-truth inventory for MODULE_SOURCE (never computed via audit.inventory).
EXPECTED_DECLARATIONS: dict[str, list[str]] = {
    "BornGaussianParallelogramRigidity": [
        "BornFinite.GaussianTomography.alg_one",
    ],
    "GleasonRealSphere": [
        "GleasonReal.real_one",
    ],
    "GleasonComplexSphere": [
        "GleasonComplex.Frame",
        "GleasonComplex.simp_one",
        "GleasonComplex.ext_two",
    ],
    "GleasonGaussianBridge": [
        "BornFinite.GleasonBridge.f₀",
        "BornFinite.GleasonBridge.ι",
        "BornFinite.GleasonBridge.nonZero_of_ι_ne_zero",
        "BornFinite.GleasonBridge.F_ι",
        "BornFinite.GleasonBridge.C₁",
        "BornFinite.GleasonBridge.inner_helper",
        "BornFinite.GleasonBridge.deep_helper",
        "BornFinite.GleasonBridge.after_deep",
        "BornFinite.GleasonBridge.after_helpers",
        "BornFinite.GleasonBridge.named_inst",
        "BornFinite.GleasonBridge.born_of_uniformlyRayContinuous",
        "BornFinite.GleasonBridge.zero_sub'",
    ],
    "GleasonBornCompletion": [
        "BornFinite.BornCompletion.Qc",
        "BornFinite.BornCompletion.isUniformlyRayContinuous_quadRay",
        "BornFinite.BornCompletion.after_noncomputable_section",
    ],
    "BornGaussianFiniteModel": [
        "BornFinite.GaussianFiniteModel.finite_model_one",
    ],
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


def good_output(
    declarations: dict[str, list[str]] | None = None,
    *,
    include_compiler_decls: bool = True,
) -> str:
    decls = EXPECTED_DECLARATIONS if declarations is None else declarations
    lines = []
    for mod, names in decls.items():
        for n in names:
            lines.append(f"'{n}' depends on axioms: [propext, Classical.choice,\n Quot.sound]")
        if include_compiler_decls:
            for n in names:
                lines.append(f"COMPILER_DECL:{mod}:{n}")
    return "\n".join(lines) + "\n"


def expectation(root: Path, declarations: dict[str, list[str]] | None = None) -> dict:
    decls = {k: list(v) for k, v in (EXPECTED_DECLARATIONS if declarations is None else declarations).items()}
    return {
        "schema_version": audit.SCHEMA,
        "allowed_axioms": list(audit.ALLOWED_AXIOMS),
        "pins": audit.pins(root),
        "declarations": decls,
    }


def test_review_reproducer_indented_theorem_is_discovered_and_enforced(tmp_path: Path) -> None:
    reproducer = (
        "namespace ReviewExample\n"
        "  theorem indented : True := trivial\n"
        "end ReviewExample\n"
    )
    assert audit.inventory_of(reproducer) == ["ReviewExample.indented"]

    sources = dict(MODULE_SOURCE)
    sources["GleasonRealSphere"] = reproducer
    root = make_root(tmp_path, sources)
    independent_decls = dict(EXPECTED_DECLARATIONS)
    independent_decls["GleasonRealSphere"] = ["ReviewExample.indented"]
    exp = expectation(root, independent_decls)

    # Omitting the report for ReviewExample.indented must fail verification.
    omitted_decls = dict(independent_decls)
    omitted_decls["GleasonRealSphere"] = []
    out_without_indented = good_output(omitted_decls)
    errors = audit.verify(root, out_without_indented, exp)
    assert "missing report: ReviewExample.indented" in errors

    # Even if an expectation file were forged with an empty inventory for that module, verify rejects it.
    forged_exp = expectation(root, omitted_decls)
    forged_errors = audit.verify(root, out_without_indented, forged_exp)
    assert "empty expected declaration inventory: GleasonRealSphere" in forged_errors
    assert any(e.startswith("declaration inventory differs") for e in forged_errors)


def test_inventory_keeps_unicode_identifiers_and_scopes(tmp_path: Path) -> None:
    root = make_root(tmp_path)
    inv = audit.inventory(root)
    assert inv == EXPECTED_DECLARATIONS
    bridge = inv["GleasonGaussianBridge"]
    assert "BornFinite.GleasonBridge.f₀" in bridge
    assert "BornFinite.GleasonBridge.ι" in bridge
    assert "BornFinite.GleasonBridge.nonZero_of_ι_ne_zero" in bridge
    assert "BornFinite.GleasonBridge.F_ι" in bridge
    assert "BornFinite.GleasonBridge.C₁" in bridge
    assert "BornFinite.GleasonBridge.zero_sub'" in bridge
    # sections (including nested sections) do not change the namespace prefix
    assert "BornFinite.GleasonBridge.inner_helper" in bridge
    assert "BornFinite.GleasonBridge.deep_helper" in bridge
    assert "BornFinite.GleasonBridge.after_deep" in bridge
    assert "BornFinite.GleasonBridge.after_helpers" in bridge
    # private and anonymous-instance declarations are not exported bindings, named instances are
    assert not any("hidden" in n for n in bridge)
    assert not any(n.endswith(":") for n in bridge)
    assert "BornFinite.GleasonBridge.named_inst" in bridge
    # no truncation: every name is a complete identifier, none repeated
    assert len(set(bridge)) == len(bridge)
    assert not any(n.endswith("_") for n in bridge)
    # comments and docstrings never contribute declarations
    assert inv["GleasonRealSphere"] == ["GleasonReal.real_one"]
    assert inv["GleasonComplexSphere"] == [
        "GleasonComplex.Frame",
        "GleasonComplex.simp_one",
        "GleasonComplex.ext_two",
    ]
    # an anonymous `noncomputable section ... end` inside a namespace does not pop the namespace
    assert inv["GleasonBornCompletion"] == [
        "BornFinite.BornCompletion.Qc",
        "BornFinite.BornCompletion.isUniformlyRayContinuous_quadRay",
        "BornFinite.BornCompletion.after_noncomputable_section",
    ]


def test_attributes_modifiers_and_nested_scopes_variants() -> None:
    src = (
        "namespace Outer\n"
        "  namespace Inner.Sub\n"
        "    @[simp, norm_cast]\n"
        "    noncomputable @[ext] protected def d₁' : Nat := 1\n"
        "    section\n"
        "      local instance inst_local : Inhabited Nat := ⟨0⟩\n"
        "      class inductive ClsProp : Prop where\n"
        "    end\n"
        "    abbrev abb_after_anon : Nat := 2\n"
        "  end Sub\n"
        "  theorem after_sub : True := trivial\n"
        "end Outer.Inner\n"
    )
    assert audit.inventory_of(src) == [
        "Outer.Inner.Sub.d₁'",
        "Outer.Inner.Sub.inst_local",
        "Outer.Inner.Sub.ClsProp",
        "Outer.Inner.Sub.abb_after_anon",
        "Outer.Inner.after_sub",
    ]


@pytest.mark.parametrize(
    "bad_source",
    [
        # Unclosed namespace at EOF
        "namespace OpenOnly\ntheorem a : True := trivial\n",
        # Unclosed anonymous section at EOF
        "namespace A\nsection\ntheorem a : True := trivial\nend A\n",
        # Anonymous `end` trying to close a named namespace
        "namespace A\ntheorem a : True := trivial\nend\n",
        # Mismatched `end` name
        "namespace A\nsection B\ntheorem a : True := trivial\nend C\nend A\n",
        # Extra unmatched `end`
        "namespace A\ntheorem a : True := trivial\nend A\nend A\n",
        # Declaration name split onto next line (unsupported syntax must fail visibly)
        "namespace A\ntheorem\n  split_name : True := trivial\nend A\n",
        # Two commands on one line
        "namespace A\ntheorem a : True := trivial theorem b : True := trivial\nend A\n",
        # Dangling attribute at EOF
        "namespace A\ntheorem a : True := trivial\nend A\n@[simp]\n",
        # Unclosed attribute bracket
        "namespace A\n@[simp lemma a : True := trivial\nend A\n",
        # Unclosed block comment
        "namespace A\ntheorem a : True := trivial\n/- unclosed comment\nend A\n",
    ],
)
def test_unsupported_or_malformed_syntax_fails_visibly(bad_source: str) -> None:
    with pytest.raises(SystemExit):
        audit.inventory_of(bad_source)


def test_empty_module_inventory_fails(tmp_path: Path) -> None:
    sources = dict(MODULE_SOURCE)
    sources["GleasonRealSphere"] = "-- only comments, no declarations\n"
    root = make_root(tmp_path, sources)
    with pytest.raises(SystemExit, match="empty declaration inventory"):
        audit.inventory(root)
    errors = audit.verify(root, good_output(), expectation(root))
    assert any("empty declaration inventory" in e for e in errors)


def test_duplicate_names_are_an_error(tmp_path: Path) -> None:
    sources = dict(MODULE_SOURCE)
    sources["GleasonRealSphere"] = "namespace GleasonReal\nlemma a : True := trivial\nlemma a : True := trivial\nend GleasonReal\n"
    root = make_root(tmp_path, sources)
    with pytest.raises(SystemExit):
        audit.inventory(root)


def test_good_output_passes(tmp_path: Path) -> None:
    root = make_root(tmp_path)
    assert audit.verify(root, good_output(), expectation(root)) == []


def test_missing_report_fails(tmp_path: Path) -> None:
    root = make_root(tmp_path)
    out = good_output().replace(
        "'BornFinite.GleasonBridge.F_ι' depends on axioms: [propext, Classical.choice,\n Quot.sound]\n", ""
    )
    errors = audit.verify(root, out, expectation(root))
    assert any(e == "missing report: BornFinite.GleasonBridge.F_ι" for e in errors)


def test_contradictory_and_identical_duplicate_reports_fail(tmp_path: Path) -> None:
    root = make_root(tmp_path)
    exp = expectation(root)
    # Contradictory duplicate: first report has sorryAx, second tries to mask it with propext only.
    contradictory_out = (
        "'GleasonReal.real_one' depends on axioms: [propext, sorryAx]\n" + good_output()
    )
    errors = audit.verify(root, contradictory_out, exp)
    assert "contradictory duplicate reports for GleasonReal.real_one" in errors
    assert "unexpected axioms for GleasonReal.real_one: ['sorryAx']" in errors

    # Identical duplicate report is also flagged.
    identical_out = (
        "'GleasonReal.real_one' depends on axioms: [propext, Classical.choice, Quot.sound]\n" + good_output()
    )
    dup_errors = audit.verify(root, identical_out, exp)
    assert "duplicate report for GleasonReal.real_one" in dup_errors


def test_unexpected_extra_report_fails(tmp_path: Path) -> None:
    root = make_root(tmp_path)
    out = good_output() + "'GleasonReal.unrecorded' does not depend on any axioms\n"
    errors = audit.verify(root, out, expectation(root))
    assert "unexpected report: GleasonReal.unrecorded" in errors


def test_stale_source_fails(tmp_path: Path) -> None:
    root = make_root(tmp_path)
    exp = expectation(root)
    out = good_output()
    path = root / audit.module_path("BornGaussianTomographyReduction")
    path.write_text(path.read_text(encoding="utf-8") + "-- edited\n", encoding="utf-8")
    errors = audit.verify(root, out, exp)
    assert "stale source pin: lean4/BornGaussianTomographyReduction.lean" in errors


def test_changed_inventory_fails(tmp_path: Path) -> None:
    root = make_root(tmp_path)
    exp = expectation(root)
    path = root / audit.module_path("GleasonRealSphere")
    path.write_text(
        "namespace GleasonReal\nlemma real_one : True := trivial\nlemma real_two : True := trivial\nend GleasonReal\n",
        encoding="utf-8",
    )
    out = good_output()
    errors = audit.verify(root, out, exp)
    assert any(e.startswith("declaration inventory differs") for e in errors)
    assert "stale source pin: lean4/GleasonRealSphere.lean" in errors


def test_unexpected_axiom_fails(tmp_path: Path) -> None:
    root = make_root(tmp_path)
    out = good_output().replace(
        "'GleasonReal.real_one' depends on axioms: [propext, Classical.choice,\n Quot.sound]",
        "'GleasonReal.real_one' depends on axioms: [propext, sorryAx]",
    )
    errors = audit.verify(root, out, expectation(root))
    assert "unexpected axioms for GleasonReal.real_one: ['sorryAx']" in errors


def test_error_line_and_forbidden_token_in_module_or_dependency_fail(tmp_path: Path) -> None:
    sources = dict(MODULE_SOURCE)
    sources["GleasonComplexSphere"] = "namespace GleasonComplex\nlemma bad : False := sorry\nend GleasonComplex\n"
    root = make_root(tmp_path, sources)
    (root / audit.module_path("BornGaussRat")).write_text(
        "import UnpinnedLocalModule\n-- dependency with native_decide\ndef d : Bool := by native_decide\n",
        encoding="utf-8",
    )
    exp = expectation(root, audit.inventory(root))
    out = good_output(exp["declarations"]) + "GleasonAudit.lean:3:0: error: unknown constant\n"
    errors = audit.verify(root, out, exp)
    assert "forbidden token: GleasonComplexSphere: sorry" in errors
    assert "forbidden token: BornGaussRat: native_decide" in errors
    assert "unpinned import: BornGaussRat: UnpinnedLocalModule" in errors
    assert "Lean output contains an error line" in errors


def test_incomplete_expectation_declarations_fail(tmp_path: Path) -> None:
    root = make_root(tmp_path)
    exp = expectation(root)
    exp["declarations"].pop("GleasonBornCompletion")
    errors = audit.verify(root, good_output(), exp)
    assert "expectation declarations missing required modules" in errors


def test_compiler_declaration_mismatch_in_output_fails(tmp_path: Path) -> None:
    root = make_root(tmp_path)
    exp = expectation(root)
    # Simulate the Lean compiler discovering an additional declaration in GleasonRealSphere
    # that was not in the expectation.
    out = good_output() + "COMPILER_DECL:GleasonRealSphere:GleasonReal.indented_extra\n"
    errors = audit.verify(root, out, exp)
    assert "compiler declaration inventory differs for GleasonRealSphere" in errors


def test_missing_or_duplicate_compiler_declarations_fail(tmp_path: Path) -> None:
    root = make_root(tmp_path)
    exp = expectation(root)
    out_missing = good_output(include_compiler_decls=False)
    errors_missing = audit.verify(root, out_missing, exp)
    for mod in audit.MODULES:
        assert f"compiler declaration inventory differs for {mod}" in errors_missing

    out_dupe = (
        good_output()
        + "COMPILER_DECL:GleasonRealSphere:GleasonReal.real_one\n"
        + "COMPILER_DECL:UnexpectedMod:Foo.bar\n"
    )
    errors_dupe = audit.verify(root, out_dupe, exp)
    assert "duplicate compiler declaration in GleasonRealSphere" in errors_dupe
    assert "unexpected compiler declaration module: UnexpectedMod" in errors_dupe


def test_dangling_attribute_before_section_or_mutual_and_nonstandard_imports_fail(tmp_path: Path) -> None:
    for kw in ("section S\nend S\n", "noncomputable section\nend\n", "mutual\nend\n"):
        with pytest.raises(SystemExit, match="dangling attribute"):
            audit.inventory_of(f"@[simp]\n{kw}")

    root = make_root(tmp_path)
    (root / audit.module_path("BornGaussRat")).write_text(
        "import all UnpinnedModule\n-- sorryAx check\n",
        encoding="utf-8",
    )
    (root / audit.module_path("GleasonRealSphere")).write_text(
        MODULE_SOURCE["GleasonRealSphere"] + "\n-- reference to sorryAx outside comment:\n-- wait\n",
        encoding="utf-8",
    )
    exp = expectation(root)
    errors = audit.verify(root, good_output(), exp)
    assert "unpinned import: BornGaussRat: import all UnpinnedModule" in errors


def test_emit_includes_compiler_environment_check(tmp_path: Path) -> None:
    root = make_root(tmp_path)
    target = root / "lean4/.audit/GleasonAudit.lean"
    count = audit.emit(root, target)
    assert count == sum(len(v) for v in EXPECTED_DECLARATIONS.values())
    emitted = target.read_text(encoding="utf-8")
    assert "import Lean" in emitted
    assert "COMPILER_DECL:" in emitted
    assert "#print axioms BornFinite.BornCompletion.after_noncomputable_section" in emitted


def test_update_then_verify_round_trip(tmp_path: Path, capsys: pytest.CaptureFixture[str]) -> None:
    root = make_root(tmp_path)
    out_path = tmp_path / "audit.txt"
    out_path.write_text(good_output(), encoding="utf-8")
    assert audit.main(["--root", str(root), "update", "--lean-output", str(out_path)]) == 0
    written = json.loads((root / audit.EXPECTATION).read_text(encoding="utf-8"))
    assert written["schema_version"] == audit.SCHEMA
    assert written["declarations"] == EXPECTED_DECLARATIONS
    assert written["pins"]["lean4/GleasonGaussianBridge.lean"] == hashlib.sha256(
        (root / "lean4/GleasonGaussianBridge.lean").read_bytes()
    ).hexdigest()
    assert audit.main(["--root", str(root), "verify", "--lean-output", str(out_path)]) == 0
    capsys.readouterr()
    # a missing expectation file is itself a failure, never a silent pass
    (root / audit.EXPECTATION).unlink()
    assert audit.main(["--root", str(root), "verify", "--lean-output", str(out_path)]) == 1
