"""Unit, negative, integration, end-to-end, and mutation tests for partial-pivoted LU."""

from __future__ import annotations

import importlib.util
import sys
import warnings
from fractions import Fraction
from pathlib import Path

import pytest

import src.linear_algebra as linear_algebra
from src.linear_algebra.elimination import (
    EliminationError,
    ExactMatrix,
    _require_unit_lower,
    plu_factor,
    witness_upper_entry,
)
from src.linear_algebra.scalars import GaussianRational

_MODULE_PATH = Path(__file__).resolve().parents[1] / "src" / "linear_algebra" / "elimination.py"


def _witness() -> ExactMatrix:
    return ExactMatrix.from_rows([[Fraction(1), Fraction(2)], [Fraction(3), Fraction(4)]])


def _perm() -> ExactMatrix:
    return ExactMatrix.from_rows([[Fraction(0), Fraction(1)], [Fraction(1), Fraction(0)]])


def _lower() -> ExactMatrix:
    return ExactMatrix.from_rows([[Fraction(1), Fraction(0)], [Fraction(1, 3), Fraction(1)]])


def _upper() -> ExactMatrix:
    return ExactMatrix.from_rows([[Fraction(3), Fraction(4)], [Fraction(0), Fraction(2, 3)]])


def test_plu_matches_the_hand_factors() -> None:
    assert witness_upper_entry() == Fraction(2, 3)
    assert type(witness_upper_entry()) is Fraction
    perm, lower, upper = plu_factor(_witness())
    assert perm == _perm()
    assert lower == _lower()
    assert upper == _upper()
    assert perm * _witness() == lower * upper
    swap = ExactMatrix.from_rows([[Fraction(0), Fraction(1)], [Fraction(1), Fraction(0)]])
    swap_perm, swap_lower, swap_upper = plu_factor(swap)
    assert swap_perm == _perm()
    assert swap_lower == ExactMatrix.identity(2)
    assert swap_upper == ExactMatrix.identity(2)
    single_perm, single_lower, single_upper = plu_factor(ExactMatrix.from_rows([[Fraction(7)]]))
    assert single_perm.get(0, 0) == 1
    assert single_lower.get(0, 0) == 1
    assert single_upper.get(0, 0) == 7
    empty_perm, empty_lower, empty_upper = plu_factor(ExactMatrix(0, 0, []))
    assert empty_perm.shape() == (0, 0)
    assert empty_lower.shape() == (0, 0)
    assert empty_upper.shape() == (0, 0)
    triple = ExactMatrix.from_rows(
        [
            [Fraction(0), Fraction(1), Fraction(1)],
            [Fraction(2), Fraction(0), Fraction(1)],
            [Fraction(1), Fraction(1), Fraction(0)],
        ]
    )
    triple_perm, triple_lower, triple_upper = plu_factor(triple)
    assert triple_perm * triple == triple_lower * triple_upper
    assert triple_lower.get(0, 0) == 1
    assert triple_upper.get(1, 0) == 0


def test_negative_boundary_failures() -> None:
    with pytest.raises(EliminationError, match="float refused") as floated:
        plu_factor(ExactMatrix.from_rows([[1.5]]))
    assert floated.value.invariant == "float refused at the public boundary"
    assert floated.value.parameters["role"] == "entry[0]"
    assert type(floated.value) is EliminationError

    with pytest.raises(EliminationError, match="boolean refused where a rational") as boolean:
        plu_factor(ExactMatrix.from_rows([[True]]))
    assert boolean.value.invariant == "boolean refused where a rational entry was required"

    with pytest.raises(EliminationError, match="Gaussian rational refused") as gaussian:
        plu_factor(ExactMatrix.from_rows([[GaussianRational(0, 1)]]))
    assert gaussian.value.parameters["role"] == "entry[0]"

    with pytest.raises(EliminationError, match="not an exact rational") as text:
        plu_factor(ExactMatrix.from_rows([["1"]]))
    assert text.value.parameters["received"] == "str"

    shaped = ExactMatrix.from_rows([[Fraction(1)]])
    shaped.rows = True
    with pytest.raises(EliminationError, match="boolean refused where a matrix dimension") as dim_bool:
        plu_factor(shaped)
    assert dim_bool.value.parameters["role"] == "rows"

    shaped = ExactMatrix.from_rows([[Fraction(1)]])
    shaped.rows = 1.0
    with pytest.raises(EliminationError, match="float refused") as dim_float:
        plu_factor(shaped)
    assert dim_float.value.parameters["role"] == "rows"

    with pytest.raises(EliminationError, match="negative") as negative:
        plu_factor(ExactMatrix(-1, 0, []))
    assert negative.value.parameters["received"] == -1

    named = ExactMatrix.from_rows([[Fraction(1)]])
    named.cols = "1"
    with pytest.raises(EliminationError, match="not an integer") as named_error:
        plu_factor(named)
    assert named_error.value.parameters["received"] == "str"

    with pytest.raises(EliminationError, match="not an ExactMatrix") as bare:
        plu_factor("matrix")  # type: ignore[arg-type]
    assert bare.value.parameters["received"] == "str"

    mismatched = ExactMatrix.identity(2)
    mismatched.rows = 3
    mismatched.cols = 3
    with pytest.raises(EliminationError, match="data length") as length_error:
        plu_factor(mismatched)
    assert length_error.value.parameters["length"] == 4

    wide = ExactMatrix.from_rows([[Fraction(1), Fraction(2)]])
    with pytest.raises(EliminationError, match="square") as rectangular:
        plu_factor(wide)
    assert rectangular.value.parameters["cols"] == 2

    singular = ExactMatrix.from_rows([[Fraction(1), Fraction(2)], [Fraction(2), Fraction(4)]])
    with pytest.raises(EliminationError, match="singular") as halted:
        plu_factor(singular)
    assert halted.value.parameters["column"] == 1

    zero = ExactMatrix.from_rows([[Fraction(0), Fraction(0)], [Fraction(0), Fraction(0)]])
    with pytest.raises(EliminationError, match="singular") as first:
        plu_factor(zero)
    assert first.value.parameters["column"] == 0

    with pytest.raises(EliminationError, match="not unit triangular") as diagonal:
        _require_unit_lower(ExactMatrix.from_rows([[Fraction(2), Fraction(0)], [Fraction(0), Fraction(1)]]))
    assert diagonal.value.parameters["index"] == 0

    with pytest.raises(EliminationError, match="upper entry") as upper:
        _require_unit_lower(ExactMatrix.from_rows([[Fraction(1), Fraction(4)], [Fraction(0), Fraction(1)]]))
    assert upper.value.parameters["col"] == 1


def test_integration_matches_rust_lu_sentence_and_matrix_product() -> None:
    root = Path(__file__).resolve().parents[3]
    source = (root / "code" / "rust" / "src" / "mub" / "omega_native" / "mub6_smale_sentry.rs").read_text(
        encoding="utf-8"
    )
    assert "P * A = L * U" in source
    assert "L has ones on diagonal" in source
    perm, lower, upper = plu_factor(_witness())
    assert perm * _witness() == lower * upper
    assert lower.get(0, 0) == 1
    assert lower.get(1, 1) == 1
    assert upper == _upper()


def test_end_to_end_public_contract() -> None:
    package = linear_algebra.elimination
    assert package.witness_upper_entry() == Fraction(2, 3)
    perm, lower, upper = package.plu_factor(ExactMatrix.identity(2))
    assert perm == ExactMatrix.identity(2)
    assert lower == ExactMatrix.identity(2)
    assert upper == ExactMatrix.identity(2)
    tampered = ExactMatrix.from_rows([[Fraction(1)]])
    tampered.data[0] = 0.25
    with pytest.raises(EliminationError, match="float refused"):
        package.plu_factor(tampered)


def test_origin_resolves_in_repo() -> None:
    root = Path(__file__).resolve().parents[3]
    origin = root / "code" / "rust" / "src" / "mub" / "omega_native" / "mub6_smale_sentry.rs"
    assert origin.is_file()
    text = origin.read_text(encoding="utf-8")
    assert "P * A = L * U" in text
    source = _MODULE_PATH.read_text(encoding="utf-8")
    assert "AuthorityEffect: None" in source
    assert "urn:omega:fqm:linear-algebra:partial-pivoted-lu:v1" in source
    assert "Scope Fence:" in source


_MUTANTS: tuple[tuple[str, str, str], ...] = (
    (
        "float admitted",
        'if isinstance(value, float):\n        raise _fail("float refused at the public boundary", role=role, received="float")',
        'if isinstance(value, float):\n        return\n    if False:\n        raise _fail("float refused at the public boundary", role=role, received="float")',
    ),
    (
        "boolean entry admitted",
        'if type(value) is bool:\n        raise _fail("boolean refused where a rational entry was required", role=role)',
        'if type(value) is bool:\n        return Fraction(1)\n    if False:\n        raise _fail("boolean refused where a rational entry was required", role=role)',
    ),
    (
        "Gaussian entry admitted",
        'if isinstance(value, GaussianRational):\n        raise _fail("Gaussian rational refused; PLU in this module is over Q", role=role)',
        'if isinstance(value, GaussianRational):\n        return value.real\n    if False:\n        raise _fail("Gaussian rational refused; PLU in this module is over Q", role=role)',
    ),
    (
        "boolean dimension admitted",
        'if type(value) is bool:\n        raise _fail("boolean refused where a matrix dimension was required", role=role)',
        'if type(value) is bool:\n        return 1\n    if False:\n        raise _fail("boolean refused where a matrix dimension was required", role=role)',
    ),
    (
        "pivot comparison inverted",
        "if size > pivot_size:",
        "if size < pivot_size:",
    ),
    (
        "multiplier inverted",
        "factor = current[row][column] / pivot",
        "factor = pivot / current[row][column]",
    ),
    (
        "permutation bits flipped",
        "if origin[row] == column:",
        "if origin[row] != column:",
    ),
    (
        "factor check inverted",
        "if perm * original != lower * upper:",
        "if perm * original == lower * upper:",
    ),
)


def _load_source(source: str, name: str) -> dict[str, object]:
    spec = importlib.util.spec_from_loader(name, loader=None)
    if spec is None:
        raise RuntimeError("could not allocate a mutant module spec")
    module = importlib.util.module_from_spec(spec)
    module.__package__ = "src.linear_algebra"
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
    witness = namespace["witness_upper_entry"]
    factor = namespace["plu_factor"]
    matrix = namespace["ExactMatrix"]
    if not callable(witness) or not callable(factor) or not isinstance(matrix, type):
        return False
    build = getattr(matrix, "from_rows")
    if not callable(build):
        return False
    try:
        entry = witness()
        perm, lower, upper = factor(build([[Fraction(0), Fraction(1)], [Fraction(1), Fraction(0)]]))
    except error:
        return False
    if not isinstance(upper, ExactMatrix) or not isinstance(perm, ExactMatrix) or not isinstance(lower, ExactMatrix):
        return False
    return bool(entry == Fraction(2, 3) and upper.get(0, 0) == 1 and upper.get(1, 1) == 1 and lower.get(1, 0) == 0)


def _bad_values_refused(namespace: dict[str, object], error: type[BaseException]) -> bool:
    factor = namespace["plu_factor"]
    matrix = namespace["ExactMatrix"]
    gaussian = namespace["GaussianRational"]
    if not callable(factor) or not isinstance(matrix, type) or not callable(gaussian):
        return False
    build = getattr(matrix, "from_rows")
    if not callable(build):
        return False
    shaped = build([[Fraction(1)]])
    shaped.rows = True
    probes = (
        (lambda: factor(build([[1.5]])), "float refused at the public boundary"),
        (lambda: factor(build([[True]])), "boolean refused where a rational entry was required"),
        (
            lambda: factor(build([[gaussian(0, 1)]])),
            "Gaussian rational refused; PLU in this module is over Q",
        ),
        (lambda: factor(shaped), "boolean refused where a matrix dimension was required"),
    )
    for probe, invariant in probes:
        if _invariant(error, probe) != invariant:
            return False
    return True


def _oracle(namespace: dict[str, object]) -> bool:
    error_type = namespace["EliminationError"]
    if not isinstance(error_type, type) or not issubclass(error_type, BaseException):
        return False
    if not _known_values_hold(namespace, error_type):
        return False
    return _bad_values_refused(namespace, error_type)


def test_mutation_suite_kills_non_equivalent_mutants() -> None:
    source = _MODULE_PATH.read_text(encoding="utf-8")
    loaded: list[str] = []
    try:
        loaded.append("mutant_plu_baseline")
        baseline = _load_source(source, loaded[-1])
        assert _oracle(baseline) is True
        killed = 0
        for index, (name, old, new) in enumerate(_MUTANTS):
            count = source.count(old)
            assert count == 1, f"{name} matched {count} sites"
            module_name = f"mutant_plu_{index}"
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
