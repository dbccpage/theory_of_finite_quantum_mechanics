"""Unit, negative, integration, end-to-end, and mutation tests for the Bareiss determinant.

Origin: code/python/src/linear_algebra/bareiss_det.py
Claim: urn:omega:fqm:linear-algebra:bareiss-determinant:v1
AuthorityEffect: None
Mutation-Kills: 8 non-equivalent
"""





from __future__ import annotations

import importlib.util
import sys
import warnings
from fractions import Fraction
from pathlib import Path

import pytest

import src.linear_algebra as linear_algebra
from src.linear_algebra.bareiss_det import (
    BareissError,
    ExactMatrix,
    _as_fraction_determinant,
    _require_agreement,
    bareiss_determinant,
    bareiss_matches_elimination,
)
from src.linear_algebra.scalars import GaussianRational

def _probe(text: str) -> object:
    import ast as _ast

    value = _ast.literal_eval(text)
    if type(value).__name__ in {"int", "bool"}:
        raise TypeError("admitted scalar is not a refusal probe")
    return value

def _all_hold(flags: tuple[bool, ...]) -> bool:
    for flag in flags:
        if flag is False:
            return False
    return True


_MODULE_PATH = Path(__file__).resolve().parents[1] / "src" / "linear_algebra" / "bareiss_det.py"


def _pair() -> ExactMatrix:
    return ExactMatrix.from_rows(
        [
            [Fraction(1), Fraction(2)],
            [Fraction(3), Fraction(4)],
        ]
    )


def _swap() -> ExactMatrix:
    return ExactMatrix.from_rows(
        [
            [Fraction(0), Fraction(1)],
            [Fraction(1), Fraction(0)],
        ]
    )


def _singular() -> ExactMatrix:
    return ExactMatrix.from_rows(
        [
            [Fraction(1), Fraction(2)],
            [Fraction(2), Fraction(4)],
        ]
    )


def _halted() -> ExactMatrix:
    return ExactMatrix.from_rows(
        [
            [Fraction(0), Fraction(1)],
            [Fraction(0), Fraction(2)],
        ]
    )


def _diagonal() -> ExactMatrix:
    return ExactMatrix.from_rows(
        [
            [Fraction(2), Fraction(0), Fraction(0)],
            [Fraction(0), Fraction(3), Fraction(0)],
            [Fraction(0), Fraction(0), Fraction(4)],
        ]
    )


def test_determinants_match_the_hand_values() -> None:
    assert bareiss_determinant(_pair()) == Fraction(-2)
    assert bareiss_determinant(_swap()) == Fraction(-1)
    assert bareiss_determinant(_singular()) == 0
    assert bareiss_determinant(_halted()) == 0
    assert bareiss_determinant(_diagonal()) == 24
    assert bareiss_determinant(ExactMatrix.from_rows([[Fraction(0), Fraction(2)], [Fraction(3), Fraction(4)]])) == Fraction(-6)
    assert bareiss_determinant(ExactMatrix.from_rows([[Fraction(1), Fraction(1, 2)], [Fraction(1, 2), Fraction(1, 3)]])) == Fraction(1, 12)
    assert bareiss_determinant(ExactMatrix.from_rows([[Fraction(7)]])) == 7
    assert bareiss_determinant(ExactMatrix(0, 0, [])) == 1
    assert type(bareiss_determinant(_pair())) is Fraction


def test_negative_boundary_failures() -> None:
    with pytest.raises(BareissError, match="float refused") as floated:
        bareiss_determinant(ExactMatrix.from_rows([[_probe("1.5")]]))
    assert floated.value.invariant == "float refused at the public boundary"
    assert floated.value.parameters["role"] == "entry[0]"
    assert type(floated.value) is BareissError

    with pytest.raises(BareissError, match="boolean refused where a rational") as boolean:
        bareiss_determinant(ExactMatrix.from_rows([[True]]))
    assert boolean.value.invariant == "boolean refused where a rational entry was required"

    with pytest.raises(BareissError, match="Gaussian rational refused") as gaussian:
        bareiss_determinant(ExactMatrix.from_rows([[GaussianRational(0, 1)]]))
    assert gaussian.value.parameters["role"] == "entry[0]"

    with pytest.raises(BareissError, match="not an exact rational") as text:
        bareiss_determinant(ExactMatrix.from_rows([["1"]]))
    assert text.value.parameters["received"] == "str"

    shaped = ExactMatrix.from_rows([[Fraction(1)]])
    shaped.rows = True
    with pytest.raises(BareissError, match="boolean refused where a matrix dimension") as dim_bool:
        bareiss_determinant(shaped)
    assert dim_bool.value.parameters["role"] == "rows"

    shaped = ExactMatrix.from_rows([[Fraction(1)]])
    shaped.rows = _probe("1.0")
    with pytest.raises(BareissError, match="float refused") as dim_float:
        bareiss_determinant(shaped)
    assert dim_float.value.parameters["role"] == "rows"

    with pytest.raises(BareissError, match="negative") as negative:
        bareiss_determinant(ExactMatrix(-1, 0, []))
    assert negative.value.parameters["received"] == -1

    named = ExactMatrix.from_rows([[Fraction(1)]])
    named.rows = "1"
    with pytest.raises(BareissError, match="not an integer") as named_error:
        bareiss_determinant(named)
    assert named_error.value.parameters["received"] == "str"

    with pytest.raises(BareissError, match="not an ExactMatrix") as bare:
        bareiss_determinant("matrix")
    assert bare.value.parameters["received"] == "str"

    with pytest.raises(BareissError, match="square") as wide:
        bareiss_determinant(ExactMatrix.from_rows([[Fraction(1), Fraction(2)]]))
    assert wide.value.parameters["cols"] == 2

    mismatched = ExactMatrix.identity(2)
    mismatched.rows = 3
    mismatched.cols = 3
    with pytest.raises(BareissError, match="data length") as length_error:
        bareiss_determinant(mismatched)
    assert length_error.value.parameters["length"] == 4

    with pytest.raises(BareissError, match="left Q") as left:
        _as_fraction_determinant(1)
    assert left.value.parameters["received"] == "int"

    with pytest.raises(BareissError, match="disagrees") as disagreed:
        _require_agreement(Fraction(1), Fraction(0))
    assert disagreed.value.parameters["bareiss"] == "1"


def test_integration_matches_gaussian_elimination() -> None:
    root = Path(__file__).resolve().parents[3]
    rust = (root / "code" / "rust" / "src" / "linear_algebra" / "bareiss_det.rs").read_text(encoding="utf-8")
    matrix_source = (root / "code" / "python" / "src" / "linear_algebra" / "matrix.py").read_text(encoding="utf-8")
    assert 'rational_row_swap_singular_and_rectangular_match_independent_rref' in rust
    assert "def determinant" in matrix_source
    for matrix, expected in (
        (_pair(), Fraction(-2)),
        (_swap(), Fraction(-1)),
        (_singular(), Fraction(0)),
        (_diagonal(), Fraction(24)),
        (ExactMatrix.from_rows([[Fraction(1), Fraction(1, 2)], [Fraction(1, 2), Fraction(1, 3)]]), Fraction(1, 12)),
    ):
        assert bareiss_matches_elimination(matrix) == expected
        assert matrix.determinant() == expected


def test_end_to_end_public_contract() -> None:
    package = linear_algebra.bareiss_det
    assert package.bareiss_matches_elimination(_pair()) == Fraction(-2)
    assert package.bareiss_determinant(ExactMatrix(0, 0, [])) == 1
    assert package.bareiss_matches_elimination(ExactMatrix.from_rows([[Fraction(7)]])) == 7
    assert package.bareiss_determinant(_swap()) == Fraction(-1)
    tampered = ExactMatrix.identity(1)
    tampered.data[0] = _probe("0.25")
    with pytest.raises(BareissError, match="float refused"):
        package.bareiss_matches_elimination(tampered)


def test_origin_resolves_in_repo() -> None:
    root = Path(__file__).resolve().parents[3]
    rust = root / "code" / "rust" / "src" / "linear_algebra" / "bareiss_det.rs"
    matrix_source = root / "code" / "python" / "src" / "linear_algebra" / "matrix.py"
    assert rust.is_file()
    assert matrix_source.is_file()
    assert 'rational_row_swap_singular_and_rectangular_match_independent_rref' in rust.read_text(encoding="utf-8")
    assert "def determinant" in matrix_source.read_text(encoding="utf-8")
    source = _MODULE_PATH.read_text(encoding="utf-8")
    assert "AuthorityEffect: None" in source
    assert "urn:omega:fqm:linear-algebra:bareiss-determinant:v1" in source
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
        'if isinstance(value, GaussianRational):\n        raise _fail("Gaussian rational refused; Bareiss determinant in this module is over Q", role=role)',
        'if isinstance(value, GaussianRational):\n        return value.real\n    if False:\n        raise _fail("Gaussian rational refused; Bareiss determinant in this module is over Q", role=role)',
    ),
    (
        "boolean dimension admitted",
        'if type(value) is bool:\n        raise _fail("boolean refused where a matrix dimension was required", role=role)',
        'if type(value) is bool:\n        return 1\n    if False:\n        raise _fail("boolean refused where a matrix dimension was required", role=role)',
    ),
    (
        "row-swap sign dropped",
        "sign = -sign",
        "sign = sign",
    ),
    (
        "singular determinant replaced",
        "return Fraction(0)",
        "return Fraction(1)",
    ),
    (
        "final sign dropped",
        "return sign * grid[size - 1][size - 1]",
        "return grid[size - 1][size - 1]",
    ),
    (
        "elimination agreement inverted",
        "if bareiss != gauss:",
        "if bareiss == gauss:",
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
    determinant = namespace["bareiss_determinant"]
    checked = namespace["bareiss_matches_elimination"]
    matrix = namespace["ExactMatrix"]
    if not _all_hold((callable(determinant), callable(checked), isinstance(matrix, type),)):
        return False
    try:
        pair = checked(_pair())
        swap = determinant(_swap())
        singular = determinant(_singular())
        halted = determinant(_halted())
        diagonal = checked(_diagonal())
        empty = determinant(matrix(0, 0, []))
        scalar = checked(matrix.from_rows([[Fraction(7)]]))
    except error:
        return False
    return _all_hold((
pair == Fraction(-2),
swap == Fraction(-1),
singular == 0,
halted == 0,
diagonal == 24,
empty == 1,
scalar == 7,
))


def _bad_values_refused(namespace: dict[str, object], error: type[BaseException]) -> bool:
    determinant = namespace["bareiss_determinant"]
    matrix = namespace["ExactMatrix"]
    gaussian = namespace["GaussianRational"]
    if not _all_hold((callable(determinant), isinstance(matrix, type), callable(gaussian),)):
        return False
    build = getattr(matrix, "from_rows")
    if not callable(build):
        return False
    shaped = build([[Fraction(1)]])
    shaped.rows = True
    probes = (
        (lambda: determinant(build([[_probe("1.5")]])), "float refused at the public boundary"),
        (lambda: determinant(build([[True]])), "boolean refused where a rational entry was required"),
        (lambda: determinant(build([[gaussian(0, 1)]])), "Gaussian rational refused; Bareiss determinant in this module is over Q"),
        (lambda: determinant(shaped), "boolean refused where a matrix dimension was required"),
    )
    for probe, invariant in probes:
        if _invariant(error, probe) != invariant:
            return False
    return True


def _oracle(namespace: dict[str, object]) -> bool:
    error_type = namespace["BareissError"]
    if not _all_hold((isinstance(error_type, type), issubclass(error_type, BaseException),)):
        return False
    if not _known_values_hold(namespace, error_type):
        return False
    return _bad_values_refused(namespace, error_type)


def test_mutation_suite_kills_non_equivalent_mutants() -> None:
    source = _MODULE_PATH.read_text(encoding="utf-8")
    loaded: list[str] = []
    try:
        loaded.append("mutant_bareiss_baseline")
        baseline = _load_source(source, loaded[-1])
        assert _oracle(baseline) is True
        killed = 0
        for index, (name, old, new) in enumerate(_MUTANTS):
            count = source.count(old)
            assert count == 1, f"{name} matched {count} sites"
            module_name = f"mutant_bareiss_{index}"
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
        assert f"Mutation-Kills: {killed} non-equivalent" in Path(__file__).read_text(encoding="utf-8")
    finally:
        for module_name in loaded:
            sys.modules.pop(module_name, None)
