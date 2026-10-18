"""Unit, negative, integration, end-to-end, and mutation tests for the two-by-two minor."""

from __future__ import annotations

import importlib.util
import sys
import warnings
from fractions import Fraction
from pathlib import Path

import pytest

import src.linear_algebra as linear_algebra
from src.linear_algebra.scalars import GaussianRational
from src.linear_algebra.test_support import (
    ExactMatrix,
    FixtureError,
    _require_zero_defect,
    empty_determinant,
    hilbert_entry,
    hilbert_matrix,
    hilbert_minor_defect,
    minor_determinant,
    sample_determinant,
    witness_minor,
)

_MODULE_PATH = Path(__file__).resolve().parents[1] / "src" / "linear_algebra" / "test_support.py"


def test_minor_matches_the_hand_values() -> None:
    assert witness_minor() == -2
    assert type(witness_minor()) is Fraction
    assert sample_determinant() == -2
    assert empty_determinant() == 1
    assert hilbert_entry(0, 0) == 1
    assert hilbert_entry(0, 1) == Fraction(1, 2)
    assert hilbert_entry(1, 1) == Fraction(1, 3)
    assert hilbert_minor_defect() == 0
    hilbert = hilbert_matrix(2)
    assert hilbert.get(0, 1) == Fraction(1, 2)
    assert hilbert.get(1, 1) == Fraction(1, 3)
    other = ExactMatrix.from_rows([[Fraction(2), Fraction(3)], [Fraction(5), Fraction(7)]])
    assert minor_determinant(other) == -1
    assert other.determinant() == -1
    assert hilbert_matrix(1).get(0, 0) == 1


def test_negative_boundary_failures() -> None:
    with pytest.raises(FixtureError, match="float refused") as floated:
        hilbert_entry(1.5, 0)
    assert floated.value.invariant == "float refused at the public boundary"
    assert floated.value.parameters["role"] == "row"
    assert type(floated.value) is FixtureError

    with pytest.raises(FixtureError, match="Hilbert index") as boolean:
        hilbert_entry(True, 0)
    assert boolean.value.invariant == "boolean refused where a Hilbert index was required"

    with pytest.raises(FixtureError, match="negative") as negative:
        hilbert_entry(-1, 0)
    assert negative.value.parameters["received"] == -1

    with pytest.raises(FixtureError, match="not an integer") as named:
        hilbert_entry("0", 0)
    assert named.value.parameters["received"] == "str"

    with pytest.raises(FixtureError, match="Hilbert size") as sized:
        hilbert_matrix(True)
    assert sized.value.invariant == "boolean refused where a Hilbert size was required"

    with pytest.raises(FixtureError, match="positive") as zero_size:
        hilbert_matrix(0)
    assert zero_size.value.parameters["received"] == 0

    partner = ExactMatrix.from_rows([[Fraction(1)]])
    with pytest.raises(FixtureError, match="two rows") as short:
        minor_determinant(partner)
    assert short.value.parameters["rows"] == 1

    wide = ExactMatrix.from_rows([[Fraction(1), Fraction(2), Fraction(3)], [Fraction(4), Fraction(5), Fraction(6)]])
    with pytest.raises(FixtureError, match="two columns") as columns:
        minor_determinant(wide)
    assert columns.value.parameters["cols"] == 3

    with pytest.raises(FixtureError, match="Gaussian rational refused") as gaussian:
        minor_determinant(ExactMatrix.from_rows([[GaussianRational(0, 1), Fraction(0)], [Fraction(0), Fraction(1)]]))
    assert gaussian.value.parameters["role"] == "entry[0]"

    with pytest.raises(FixtureError, match="boolean refused where a rational") as entry_bool:
        minor_determinant(ExactMatrix.from_rows([[True, Fraction(0)], [Fraction(0), Fraction(1)]]))
    assert entry_bool.value.invariant == "boolean refused where a rational entry was required"

    with pytest.raises(FixtureError, match="not an exact rational") as text:
        minor_determinant(ExactMatrix.from_rows([["1", Fraction(0)], [Fraction(0), Fraction(1)]]))
    assert text.value.parameters["received"] == "str"

    shaped = ExactMatrix.from_rows([[Fraction(1), Fraction(0)], [Fraction(0), Fraction(1)]])
    shaped.rows = True
    with pytest.raises(FixtureError, match="boolean refused where a matrix dimension") as dim_bool:
        minor_determinant(shaped)
    assert dim_bool.value.parameters["role"] == "rows"

    shaped = sample_matrix_copy()
    shaped.rows = 1.0
    with pytest.raises(FixtureError, match="float refused") as dim_float:
        minor_determinant(shaped)
    assert dim_float.value.parameters["role"] == "rows"

    with pytest.raises(FixtureError, match="negative") as shape:
        minor_determinant(ExactMatrix(-1, 0, []))
    assert shape.value.parameters["received"] == -1

    named_shape = sample_matrix_copy()
    named_shape.cols = "2"
    with pytest.raises(FixtureError, match="not an integer") as named_dim:
        minor_determinant(named_shape)
    assert named_dim.value.parameters["received"] == "str"

    with pytest.raises(FixtureError, match="not an ExactMatrix") as bare:
        minor_determinant("matrix")  # type: ignore[arg-type]
    assert bare.value.parameters["received"] == "str"

    mismatched = sample_matrix_copy()
    mismatched.rows = 3
    mismatched.cols = 3
    with pytest.raises(FixtureError, match="data length") as length_error:
        minor_determinant(mismatched)
    assert length_error.value.parameters["length"] == 4

    with pytest.raises(FixtureError, match="minor defect") as defect:
        _require_zero_defect(Fraction(1), "hilbert")
    assert defect.value.parameters["defect"] == "1"


def sample_matrix_copy() -> ExactMatrix:
    return ExactMatrix.from_rows([[Fraction(1), Fraction(2)], [Fraction(3), Fraction(4)]])


def test_integration_matches_matrix_determinant_and_rust_empty_case() -> None:
    root = Path(__file__).resolve().parents[3]
    rust = (root / "code" / "rust" / "src" / "linear_algebra" / "elimination.rs").read_text(encoding="utf-8")
    python = (root / "code" / "python" / "src" / "linear_algebra" / "matrix.py").read_text(encoding="utf-8")
    assert "The determinant of a square matrix (`1` for the empty matrix)." in rust
    assert "def determinant" in python
    witness = sample_matrix_copy()
    assert witness.determinant() == -2
    assert minor_determinant(witness) == witness.determinant()
    assert ExactMatrix(0, 0, []).determinant() == 1
    hilbert = ExactMatrix.from_rows(
        [[Fraction(1), Fraction(1, 2)], [Fraction(1, 2), Fraction(1, 3)]]
    )
    assert hilbert.determinant() == Fraction(1, 12)
    assert hilbert_minor_defect() == 0


def test_end_to_end_public_contract() -> None:
    package = linear_algebra.test_support
    assert package.witness_minor() == -2
    assert package.empty_determinant() == 1
    assert package.hilbert_matrix(2).get(0, 0) == 1
    tampered = sample_matrix_copy()
    tampered.data[0] = 0.25
    with pytest.raises(FixtureError, match="float refused"):
        package.minor_determinant(tampered)


def test_origin_resolves_in_repo() -> None:
    root = Path(__file__).resolve().parents[3]
    matrix = root / "code" / "python" / "src" / "linear_algebra" / "matrix.py"
    rust = root / "code" / "rust" / "src" / "linear_algebra" / "elimination.rs"
    assert matrix.is_file()
    assert rust.is_file()
    assert "1` for the empty matrix" in rust.read_text(encoding="utf-8")
    source = _MODULE_PATH.read_text(encoding="utf-8")
    assert "AuthorityEffect: None" in source
    assert "urn:omega:fqm:linear-algebra:two-by-two-minor:v1" in source
    assert "Scope Fence:" in source


_MUTANTS: tuple[tuple[str, str, str], ...] = (
    (
        "float admitted",
        'if isinstance(value, float):\n        raise _fail("float refused at the public boundary", role=role, received="float")',
        'if isinstance(value, float):\n        return\n    if False:\n        raise _fail("float refused at the public boundary", role=role, received="float")',
    ),
    (
        "boolean index admitted",
        'if type(value) is bool:\n        raise _fail("boolean refused where a Hilbert index was required", role=role)',
        'if type(value) is bool:\n        return 0\n    if False:\n        raise _fail("boolean refused where a Hilbert index was required", role=role)',
    ),
    (
        "Gaussian entry admitted",
        'if isinstance(value, GaussianRational):\n        raise _fail("Gaussian rational refused; the two-by-two minor in this module is over Q", role=role)',
        'if isinstance(value, GaussianRational):\n        return value.real\n    if False:\n        raise _fail("Gaussian rational refused; the two-by-two minor in this module is over Q", role=role)',
    ),
    (
        "minor sign flipped",
        "return a * d - b * c",
        "return a * d + b * c",
    ),
    (
        "Hilbert denominator shifted",
        "return Fraction(1, i + j + 1)",
        "return Fraction(1, i + j + 2)",
    ),
    (
        "empty determinant gate inverted",
        "if declared != 1:",
        "if declared == 1:",
    ),
    (
        "minor comparison inverted",
        "if by_minors != declared:",
        "if by_minors == declared:",
    ),
    (
        "Hilbert size gate inverted",
        "if value < 1:",
        "if value > 1:",
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
    witness = namespace["witness_minor"]
    entry = namespace["hilbert_entry"]
    matrix = namespace["hilbert_matrix"]
    empty = namespace["empty_determinant"]
    if not callable(witness) or not callable(entry) or not callable(matrix) or not callable(empty):
        return False
    try:
        minor = witness()
        corner = entry(0, 0)
        neighbor = entry(0, 1)
        built = matrix(2)
        vacant = empty()
    except error:
        return False
    if not isinstance(built, ExactMatrix):
        return False
    return bool(minor == -2 and corner == 1 and neighbor == Fraction(1, 2) and built.get(1, 1) == Fraction(1, 3) and vacant == 1)


def _bad_values_refused(namespace: dict[str, object], error: type[BaseException]) -> bool:
    entry = namespace["hilbert_entry"]
    product = namespace["minor_determinant"]
    sized = namespace["hilbert_matrix"]
    matrix = namespace["ExactMatrix"]
    gaussian = namespace["GaussianRational"]
    if not callable(entry) or not callable(product) or not callable(sized):
        return False
    if not isinstance(matrix, type) or not callable(gaussian):
        return False
    build = getattr(matrix, "from_rows")
    if not callable(build):
        return False
    probes = (
        (lambda: entry(1.5, 0), "float refused at the public boundary"),
        (lambda: entry(True, 0), "boolean refused where a Hilbert index was required"),
        (
            lambda: product(build([[gaussian(0, 1), Fraction(0)], [Fraction(0), Fraction(1)]])),
            "Gaussian rational refused; the two-by-two minor in this module is over Q",
        ),
        (lambda: sized(True), "boolean refused where a Hilbert size was required"),
    )
    for probe, invariant in probes:
        if _invariant(error, probe) != invariant:
            return False
    return True


def _oracle(namespace: dict[str, object]) -> bool:
    error_type = namespace["FixtureError"]
    if not isinstance(error_type, type) or not issubclass(error_type, BaseException):
        return False
    if not _known_values_hold(namespace, error_type):
        return False
    return _bad_values_refused(namespace, error_type)


def test_mutation_suite_kills_non_equivalent_mutants() -> None:
    source = _MODULE_PATH.read_text(encoding="utf-8")
    loaded: list[str] = []
    try:
        loaded.append("mutant_minor_baseline")
        baseline = _load_source(source, loaded[-1])
        assert _oracle(baseline) is True
        killed = 0
        for index, (name, old, new) in enumerate(_MUTANTS):
            count = source.count(old)
            assert count == 1, f"{name} matched {count} sites"
            module_name = f"mutant_minor_{index}"
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
