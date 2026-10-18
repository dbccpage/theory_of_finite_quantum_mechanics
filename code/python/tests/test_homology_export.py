"""Unit, negative, integration, end-to-end, and mutation tests for the homology export."""

from __future__ import annotations

import importlib.util
import sys
import warnings
from fractions import Fraction
from pathlib import Path

import pytest

import src.homology as homology
from src.homology.boundary import triangle_boundary_defect
from src.homology.errors import DimensionMismatchError, NonZeroCompositionError
from src.homology.exact_carrier import triangle_betti

_MODULE_PATH = Path(__file__).resolve().parents[1] / "src" / "homology" / "__init__.py"


def test_exported_sum_is_four() -> None:
    assert homology.exported_triangle_rank_sum() == 4
    assert "exported_triangle_rank_sum" in homology.__all__
    assert homology.triangle_betti is triangle_betti


def test_negative_export_failures(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(homology, "triangle_betti", lambda: (1.0, 1, 0))
    with pytest.raises(DimensionMismatchError, match="float refused") as float_error:
        homology.exported_triangle_rank_sum()
    assert float_error.value.parameters["role"] == "rank0"

    monkeypatch.setattr(homology, "triangle_betti", lambda: (True, 1, 0))
    with pytest.raises(DimensionMismatchError, match="boolean refused where an integer") as bool_error:
        homology.exported_triangle_rank_sum()
    assert bool_error.value.parameters["role"] == "rank0"

    monkeypatch.setattr(homology, "triangle_betti", lambda: (0, 0, 3))
    with pytest.raises(DimensionMismatchError, match="not \\(2, 1, 0\\)") as triple:
        homology.exported_triangle_rank_sum()
    assert triple.value.parameters["betti"] == 3

    monkeypatch.setattr(homology, "triangle_betti", triangle_betti)
    monkeypatch.setattr(homology, "triangle_boundary_defect", lambda: Fraction(2))
    with pytest.raises(NonZeroCompositionError, match="has a defect") as defect:
        homology.exported_triangle_rank_sum()
    assert defect.value.parameters["defect"] == "2"

    monkeypatch.setattr(homology, "triangle_boundary_defect", triangle_boundary_defect)
    monkeypatch.setattr(homology, "triangle_betti", lambda: (2, 1))
    with pytest.raises(DimensionMismatchError, match="not a triple") as short:
        homology.exported_triangle_rank_sum()
    assert short.value.parameters["received"] == "tuple"


def test_integration_with_betti_and_boundary() -> None:
    rank0, rank1, betti = triangle_betti()
    defect = triangle_boundary_defect()
    assert (rank0, rank1, betti) == (2, 1, 0)
    assert defect == Fraction(0)
    assert homology.exported_triangle_rank_sum() == rank0 + rank1 + betti + 1


def test_end_to_end_public_contract(monkeypatch: pytest.MonkeyPatch) -> None:
    from src.homology import exported_triangle_rank_sum

    assert exported_triangle_rank_sum() == 4
    monkeypatch.setattr(homology, "triangle_boundary_defect", lambda: 0.5)
    with pytest.raises(DimensionMismatchError, match="float refused"):
        exported_triangle_rank_sum()


def test_origin_resolves_in_repo() -> None:
    root = Path(__file__).resolve().parents[3]
    cochain = (root / "lean4" / "FiniteCochain.lean").read_text(encoding="utf-8")
    grammar = (root / "lean4" / "CellGrammar.lean").read_text(encoding="utf-8")
    assert "theorem d1_d0_zero" in cochain
    assert "boundarySquare" in grammar
    source = _MODULE_PATH.read_text(encoding="utf-8")
    assert "AuthorityEffect: None" in source
    assert "urn:omega:fqm:homology:exported-triangle-rank-sum:v1" in source
    assert "Scope Fence:" in source


_MUTANTS: tuple[tuple[str, str, str], ...] = (
    (
        "float admitted",
        "if isinstance(value, float):",
        "if isinstance(value, float):\n        return\n    if False:",
    ),
    (
        "boolean count admitted",
        "if isinstance(value, bool):",
        "if isinstance(value, bool):\n        return\n    if False:",
    ),
    (
        "Betti check inverted",
        "if (rank0, rank1, betti) != _FILLED_BETTI:",
        "if (rank0, rank1, betti) == _FILLED_BETTI:",
    ),
    ("square check inverted", "if defect != 0:", "if defect == 0:"),
    ("expected Betti shifted", "_FILLED_BETTI = (2, 1, 0)", "_FILLED_BETTI = (2, 1, 1)"),
    ("closure bit cleared", "return 1", "return 0"),
    (
        "sum shifted by one",
        "return rank0 + rank1 + betti + _closure_bit(defect)",
        "return rank0 + rank1 + betti + _closure_bit(defect) + 1",
    ),
    ("triple length shifted", "len(value) != 3", "len(value) != 4"),
)


def _load_source(source: str, name: str) -> dict[str, object]:
    spec = importlib.util.spec_from_loader(name, loader=None)
    if spec is None:
        raise RuntimeError("could not allocate a mutant module spec")
    module = importlib.util.module_from_spec(spec)
    module.__package__ = "src.homology"
    sys.modules[name] = module
    with warnings.catch_warnings():
        warnings.filterwarnings("ignore", message="__package__ != __spec__.parent", category=DeprecationWarning)
        exec(compile(source, name + ".py", "exec"), module.__dict__)
    return module.__dict__


def _invariant(error: type[BaseException], probe: object) -> str | None:
    if not callable(probe):
        return None
    try:
        probe()
    except error as caught:
        invariant = getattr(caught, "invariant", None)
        return invariant if isinstance(invariant, str) else None
    return None


def _known_values_hold(namespace: dict[str, object], error: type[BaseException]) -> bool:
    exported = namespace["exported_triangle_rank_sum"]
    if not callable(exported):
        return False
    try:
        measured = exported()
    except error:
        return False
    return bool(measured == 4)


def _bad_values_refused(namespace: dict[str, object]) -> bool:
    mismatch = namespace["DimensionMismatchError"]
    nonzero = namespace["NonZeroCompositionError"]
    exported = namespace["exported_triangle_rank_sum"]
    if not isinstance(mismatch, type) or not isinstance(nonzero, type) or not callable(exported):
        return False
    original_betti = namespace["triangle_betti"]
    original_defect = namespace["triangle_boundary_defect"]
    probes = (
        (mismatch, lambda: (1.0, 1, 0), original_defect, "float refused at the public boundary"),
        (mismatch, lambda: (True, 1, 0), original_defect, "boolean refused where an integer was required"),
        (mismatch, lambda: (0, 0, 3), original_defect, "triangle Betti triple is not (2, 1, 0)"),
        (nonzero, original_betti, lambda: Fraction(2), "triangle boundary square has a defect"),
        (mismatch, lambda: (2, 1), original_defect, "triangle Betti certificate is not a triple"),
    )
    for error, betti, defect, invariant in probes:
        namespace["triangle_betti"] = betti
        namespace["triangle_boundary_defect"] = defect
        if _invariant(error, exported) != invariant:
            namespace["triangle_betti"] = original_betti
            namespace["triangle_boundary_defect"] = original_defect
            return False
    namespace["triangle_betti"] = original_betti
    namespace["triangle_boundary_defect"] = original_defect
    return True


def _oracle(namespace: dict[str, object]) -> bool:
    error_type = namespace["DimensionMismatchError"]
    if not isinstance(error_type, type) or not issubclass(error_type, BaseException):
        return False
    if not _known_values_hold(namespace, error_type):
        return False
    return _bad_values_refused(namespace)


def test_mutation_suite_kills_non_equivalent_mutants() -> None:
    source = _MODULE_PATH.read_text(encoding="utf-8")
    loaded: list[str] = []
    try:
        loaded.append("mutant_homology_export_baseline")
        baseline = _load_source(source, loaded[-1])
        assert _oracle(baseline) is True
        killed = 0
        for index, (name, old, new) in enumerate(_MUTANTS):
            count = source.count(old)
            assert count == 1, f"{name} matched {count} sites"
            module_name = f"mutant_homology_export_{index}"
            loaded.append(module_name)
            try:
                namespace = _load_source(source.replace(old, new, 1), module_name)
                survived = _oracle(namespace)
            except Exception:
                survived = False
            assert survived is False, name
            killed += 1
        assert killed == len(_MUTANTS)
        assert f"Mutation-Kills: {killed} non-equivalent" in source
    finally:
        for module_name in loaded:
            sys.modules.pop(module_name, None)
