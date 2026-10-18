"""Unit, negative, integration, end-to-end, and mutation tests for the rational commutant."""

from __future__ import annotations

import importlib.util
import sys
import warnings
from fractions import Fraction
from pathlib import Path

import pytest

import src.linear_algebra as linear_algebra
from src.linear_algebra.commutant import (
    CommutantError,
    ExactMatrix,
    _basis_matrix,
    _require_commuting,
    commutant_basis,
    commutant_dimension,
)
from src.linear_algebra.scalars import GaussianRational

_MODULE_PATH = Path(__file__).resolve().parents[1] / "src" / "linear_algebra" / "commutant.py"


def _diagonal() -> ExactMatrix:
    return ExactMatrix.from_rows(
        [
            [Fraction(1), Fraction(0)],
            [Fraction(0), Fraction(2)],
        ]
    )


def _rotation() -> ExactMatrix:
    return ExactMatrix.from_rows(
        [
            [Fraction(0), Fraction(1)],
            [Fraction(-1), Fraction(0)],
        ]
    )


def _off_diagonal() -> ExactMatrix:
    return ExactMatrix.from_rows(
        [
            [Fraction(0), Fraction(1)],
            [Fraction(0), Fraction(0)],
        ]
    )


def _independent(basis: list[ExactMatrix]) -> bool:
    if not basis:
        return True
    rows = [list(element.data) for element in basis]
    return ExactMatrix.from_rows(rows).rank() == len(basis)


def _all_commute(basis: list[ExactMatrix], source: ExactMatrix) -> bool:
    for element in basis:
        if element * source != source * element:
            return False
    return True


def test_nonscalar_plane_has_dimension_two() -> None:
    diagonal = commutant_basis(_diagonal())
    rotation = commutant_basis(_rotation())
    assert commutant_dimension(_diagonal()) == 2
    assert commutant_dimension(_rotation()) == 2
    assert len(diagonal) == 2
    assert len(rotation) == 2
    assert _all_commute(diagonal, _diagonal())
    assert _all_commute(rotation, _rotation())
    assert _independent(diagonal)
    assert _independent(rotation)
    assert commutant_dimension(ExactMatrix.from_rows([[Fraction(5)]])) == 1
    assert commutant_dimension(ExactMatrix.identity(2)) == 4
    assert type(diagonal[0].get(0, 0)) is Fraction


def test_negative_boundary_failures() -> None:
    with pytest.raises(CommutantError, match="float refused") as floated:
        commutant_dimension(ExactMatrix.from_rows([[1.5]]))
    assert floated.value.invariant == "float refused at the public boundary"
    assert floated.value.parameters["role"] == "entry[0]"
    assert type(floated.value) is CommutantError

    with pytest.raises(CommutantError, match="boolean refused where a rational") as boolean:
        commutant_dimension(ExactMatrix.from_rows([[True]]))
    assert boolean.value.invariant == "boolean refused where a rational entry was required"

    with pytest.raises(CommutantError, match="Gaussian rational refused") as gaussian:
        commutant_dimension(ExactMatrix.from_rows([[GaussianRational(0, 1)]]))
    assert gaussian.value.parameters["role"] == "entry[0]"

    with pytest.raises(CommutantError, match="not an exact rational") as text:
        commutant_dimension(ExactMatrix.from_rows([["1"]]))
    assert text.value.parameters["received"] == "str"

    shaped = ExactMatrix.from_rows([[Fraction(1)]])
    shaped.rows = True
    with pytest.raises(CommutantError, match="boolean refused where a matrix dimension") as dim_bool:
        commutant_dimension(shaped)
    assert dim_bool.value.parameters["role"] == "rows"

    shaped = ExactMatrix.from_rows([[Fraction(1)]])
    shaped.rows = 1.0
    with pytest.raises(CommutantError, match="float refused") as dim_float:
        commutant_dimension(shaped)
    assert dim_float.value.parameters["role"] == "rows"

    with pytest.raises(CommutantError, match="negative") as negative:
        commutant_dimension(ExactMatrix(-1, 0, []))
    assert negative.value.parameters["received"] == -1

    named = ExactMatrix.from_rows([[Fraction(1)]])
    named.rows = "1"
    with pytest.raises(CommutantError, match="not an integer") as named_error:
        commutant_dimension(named)
    assert named_error.value.parameters["received"] == "str"

    with pytest.raises(CommutantError, match="not an ExactMatrix") as bare:
        commutant_dimension("matrix")  # type: ignore[arg-type]
    assert bare.value.parameters["received"] == "str"

    with pytest.raises(CommutantError, match="square") as wide:
        commutant_dimension(ExactMatrix.from_rows([[Fraction(1), Fraction(2)]]))
    assert wide.value.parameters["cols"] == 2

    mismatched = ExactMatrix.identity(2)
    mismatched.rows = 3
    mismatched.cols = 3
    with pytest.raises(CommutantError, match="data length") as length_error:
        commutant_dimension(mismatched)
    assert length_error.value.parameters["length"] == 4

    with pytest.raises(CommutantError, match="not n squared") as short:
        _basis_matrix(1, [])
    assert short.value.parameters["length"] == 0

    with pytest.raises(CommutantError, match="does not commute") as commuting:
        _require_commuting(_off_diagonal(), _diagonal())
    assert commuting.value.parameters["rows"] == 2


def test_integration_matches_the_cited_m2_span() -> None:
    root = Path(__file__).resolve().parents[3]
    rust = (root / "code" / "rust" / "src" / "linear_algebra" / "commutant.rs").read_text(encoding="utf-8")
    lean = (root / "lean4" / "CommutingObservables.lean").read_text(encoding="utf-8")
    assert "row-major matrix coordinates" in rust
    assert "span{I, A}" in lean
    source = _diagonal()
    basis = commutant_basis(source)
    assert commutant_dimension(source) == 2
    assert _all_commute(basis, source)
    assert _independent(basis)
    coordinates = ExactMatrix.from_rows(
        [
            [Fraction(basis[0].get(0, 0)), Fraction(basis[1].get(0, 0))],
            [Fraction(basis[0].get(1, 1)), Fraction(basis[1].get(1, 1))],
        ]
    )
    assert coordinates.determinant() != 0
    assert basis[0].get(0, 1) == 0
    assert basis[0].get(1, 0) == 0
    identity = ExactMatrix.identity(2)
    assert commutant_dimension(identity) == 4
    assert len(commutant_basis(identity)) == 4


def test_end_to_end_public_contract() -> None:
    package = linear_algebra.commutant
    assert package.commutant_dimension(_rotation()) == 2
    assert package.commutant_dimension(ExactMatrix(0, 0, [])) == 0
    assert package.commutant_basis(ExactMatrix(0, 0, [])) == []
    scalar = package.commutant_basis(ExactMatrix.from_rows([[Fraction(5)]]))
    assert len(scalar) == 1
    assert scalar[0] == ExactMatrix.from_rows([[Fraction(1)]])
    tampered = ExactMatrix.identity(1)
    tampered.data[0] = 0.25
    with pytest.raises(CommutantError, match="float refused"):
        package.commutant_dimension(tampered)


def test_origin_resolves_in_repo() -> None:
    root = Path(__file__).resolve().parents[3]
    rust = root / "code" / "rust" / "src" / "linear_algebra" / "commutant.rs"
    lean = root / "lean4" / "CommutingObservables.lean"
    assert rust.is_file()
    assert lean.is_file()
    assert "row-major matrix coordinates" in rust.read_text(encoding="utf-8")
    assert "span{I, A}" in lean.read_text(encoding="utf-8")
    source = _MODULE_PATH.read_text(encoding="utf-8")
    assert "AuthorityEffect: None" in source
    assert "urn:omega:fqm:linear-algebra:commutant:v1" in source
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
        'if isinstance(value, GaussianRational):\n        raise _fail("Gaussian rational refused; commutant in this module is over Q", role=role)',
        'if isinstance(value, GaussianRational):\n        return value.real\n    if False:\n        raise _fail("Gaussian rational refused; commutant in this module is over Q", role=role)',
    ),
    (
        "boolean dimension admitted",
        'if type(value) is bool:\n        raise _fail("boolean refused where a matrix dimension was required", role=role)',
        'if type(value) is bool:\n        return 1\n    if False:\n        raise _fail("boolean refused where a matrix dimension was required", role=role)',
    ),
    (
        "commutator cancelled",
        "return left * right - right * left",
        "return left * right - left * right",
    ),
    (
        "matrix unit zeroed",
        "data[row * size + col] = Fraction(1)",
        "data[row * size + col] = Fraction(0)",
    ),
    (
        "commuting recheck inverted",
        "if not _commutes(element, source):",
        "if _commutes(element, source):",
    ),
    (
        "dimension incremented",
        "return len(basis)",
        "return len(basis) + 1",
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
    dimension = namespace["commutant_dimension"]
    basis_of = namespace["commutant_basis"]
    matrix = namespace["ExactMatrix"]
    if not callable(dimension) or not callable(basis_of) or not isinstance(matrix, type):
        return False
    diagonal = _diagonal()
    try:
        diagonal_dimension = dimension(diagonal)
        rotation_dimension = dimension(_rotation())
        scalar_dimension = dimension(matrix.from_rows([[Fraction(5)]]))
        identity_dimension = dimension(matrix.identity(2))
        empty_dimension = dimension(matrix(0, 0, []))
        basis = basis_of(diagonal)
    except error:
        return False
    if not isinstance(diagonal_dimension, int) or not isinstance(basis, list):
        return False
    return bool(
        diagonal_dimension == 2
        and rotation_dimension == 2
        and scalar_dimension == 1
        and identity_dimension == 4
        and empty_dimension == 0
        and len(basis) == 2
        and _all_commute(basis, diagonal)
    )


def _bad_values_refused(namespace: dict[str, object], error: type[BaseException]) -> bool:
    dimension = namespace["commutant_dimension"]
    matrix = namespace["ExactMatrix"]
    gaussian = namespace["GaussianRational"]
    if not callable(dimension) or not isinstance(matrix, type) or not callable(gaussian):
        return False
    build = getattr(matrix, "from_rows")
    if not callable(build):
        return False
    shaped = build([[Fraction(1)]])
    shaped.rows = True
    probes = (
        (lambda: dimension(build([[1.5]])), "float refused at the public boundary"),
        (lambda: dimension(build([[True]])), "boolean refused where a rational entry was required"),
        (lambda: dimension(build([[gaussian(0, 1)]])), "Gaussian rational refused; commutant in this module is over Q"),
        (lambda: dimension(shaped), "boolean refused where a matrix dimension was required"),
    )
    for probe, invariant in probes:
        if _invariant(error, probe) != invariant:
            return False
    return True


def _oracle(namespace: dict[str, object]) -> bool:
    error_type = namespace["CommutantError"]
    if not isinstance(error_type, type) or not issubclass(error_type, BaseException):
        return False
    if not _known_values_hold(namespace, error_type):
        return False
    return _bad_values_refused(namespace, error_type)


def test_mutation_suite_kills_non_equivalent_mutants() -> None:
    source = _MODULE_PATH.read_text(encoding="utf-8")
    loaded: list[str] = []
    try:
        loaded.append("mutant_commutant_baseline")
        baseline = _load_source(source, loaded[-1])
        assert _oracle(baseline) is True
        killed = 0
        for index, (name, old, new) in enumerate(_MUTANTS):
            count = source.count(old)
            assert count == 1, f"{name} matched {count} sites"
            module_name = f"mutant_commutant_{index}"
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
