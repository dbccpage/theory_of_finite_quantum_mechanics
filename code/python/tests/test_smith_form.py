"""Unit, negative, integration, end-to-end, and mutation tests for Smith form.

Origin: code/python/src/linear_algebra/smith_form.py
Claim: urn:omega:fqm:linear-algebra:smith-normal-form:v1
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
from src.linear_algebra.matrix import ExactMatrix
from src.linear_algebra.scalars import GaussianRational
from src.linear_algebra.smith_form import (
    SmithFormError,
    _Board,
    _charge_step,
    _quotient,
    _require_divisibility,
    _require_product,
    _require_unimodular,
    invariant_factors,
    smith_normal_form,
    witness_diagonal_sum,
)

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


_MODULE_PATH = Path(__file__).resolve().parents[1] / "src" / "linear_algebra" / "smith_form.py"


def _witness() -> ExactMatrix:
    return ExactMatrix.from_rows([[Fraction(2), Fraction(4)], [Fraction(2), Fraction(6)]])


def _witness_diagonal() -> ExactMatrix:
    return ExactMatrix.from_rows([[Fraction(2), Fraction(0)], [Fraction(0), Fraction(2)]])


def _witness_left() -> ExactMatrix:
    return ExactMatrix.from_rows([[Fraction(1), Fraction(0)], [Fraction(-1), Fraction(1)]])


def _witness_right() -> ExactMatrix:
    return ExactMatrix.from_rows([[Fraction(1), Fraction(-2)], [Fraction(0), Fraction(1)]])


def test_smith_matches_the_hand_factors() -> None:
    assert witness_diagonal_sum() == 4
    assert type(witness_diagonal_sum()) is Fraction
    diagonal, left, right = smith_normal_form(_witness())
    assert diagonal == _witness_diagonal()
    assert left == _witness_left()
    assert right == _witness_right()
    assert left * _witness() * right == diagonal
    assert invariant_factors(_witness()) == (Fraction(2), Fraction(2))
    swapped = ExactMatrix.from_rows([[Fraction(4), Fraction(0)], [Fraction(0), Fraction(2)]])
    swap_diagonal, swap_left, swap_right = smith_normal_form(swapped)
    assert swap_diagonal.get(0, 0) == 2
    assert swap_diagonal.get(1, 1) == 4
    assert swap_diagonal.get(0, 1) == 0
    assert swap_left * swapped * swap_right == swap_diagonal
    assert abs(swap_left.determinant()) == 1
    assert abs(swap_right.determinant()) == 1
    fractional = ExactMatrix.from_rows(
        [
            [Fraction(1, 2), Fraction(1, 3)],
            [Fraction(1, 3), Fraction(1, 2)],
        ]
    )
    fraction_diagonal, fraction_left, fraction_right = smith_normal_form(fractional)
    assert fraction_diagonal.get(0, 0) == Fraction(1, 6)
    assert fraction_diagonal.get(1, 1) == Fraction(5, 6)
    assert fraction_left * fractional * fraction_right == fraction_diagonal
    single_diagonal, single_left, single_right = smith_normal_form(ExactMatrix.from_rows([[Fraction(7)]]))
    assert single_diagonal.get(0, 0) == 7
    assert single_left.get(0, 0) == 1
    assert single_right.get(0, 0) == 1
    packed = ExactMatrix.from_rows([[Fraction(4), Fraction(2)], [Fraction(2), Fraction(2)]])
    packed_diagonal, packed_left, packed_right = smith_normal_form(packed)
    assert invariant_factors(packed) == (Fraction(2), Fraction(2))
    assert packed_left * packed * packed_right == packed_diagonal
    column = ExactMatrix.from_rows([[Fraction(2)], [Fraction(4)], [Fraction(6)]])
    column_diagonal, column_left, column_right = smith_normal_form(column)
    assert column_diagonal.get(0, 0) == 2
    assert column_diagonal.get(1, 0) == 0
    assert column_diagonal.get(2, 0) == 0
    assert column_left * column * column_right == column_diagonal
    zero = ExactMatrix.from_rows([[Fraction(0), Fraction(0)], [Fraction(0), Fraction(0)]])
    zero_diagonal, zero_left, zero_right = smith_normal_form(zero)
    assert invariant_factors(zero) == (Fraction(0), Fraction(0))
    assert zero_left * zero * zero_right == zero_diagonal
    tail = ExactMatrix.from_rows([[Fraction(0), Fraction(0)], [Fraction(0), Fraction(5)]])
    assert invariant_factors(tail) == (Fraction(5), Fraction(0))
    empty_diagonal, empty_left, empty_right = smith_normal_form(ExactMatrix(0, 0, []))
    assert empty_diagonal.shape() == (0, 0)
    assert empty_left.determinant() == 1
    assert empty_right.determinant() == 1
    wide_diagonal, wide_left, wide_right = smith_normal_form(ExactMatrix(0, 2, []))
    assert wide_diagonal.shape() == (0, 2)
    assert wide_left.shape() == (0, 0)
    assert wide_right == ExactMatrix.identity(2)
    tall_diagonal, tall_left, tall_right = smith_normal_form(ExactMatrix(2, 0, []))
    assert tall_diagonal.shape() == (2, 0)
    assert tall_left == ExactMatrix.identity(2)
    assert tall_right.shape() == (0, 0)


def test_negative_boundary_failures() -> None:
    with pytest.raises(SmithFormError, match="float refused") as floated:
        smith_normal_form(ExactMatrix.from_rows([[_probe("1.5")]]))
    assert floated.value.invariant == "float refused at the public boundary"
    assert floated.value.parameters["role"] == "entry[0,0]"

    with pytest.raises(SmithFormError, match="boolean refused") as boolean_entry:
        smith_normal_form(ExactMatrix.from_rows([[True]]))
    assert boolean_entry.value.invariant == "boolean refused where a rational entry was required"

    with pytest.raises(SmithFormError, match="Gaussian") as gaussian:
        smith_normal_form(ExactMatrix.from_rows([[GaussianRational(0, 1)]]))
    assert gaussian.value.invariant == "Gaussian rational refused; Smith form in this module is over Q"
    assert gaussian.value.parameters["role"] == "entry[0,0]"

    with pytest.raises(SmithFormError, match="not an exact rational") as text:
        smith_normal_form(ExactMatrix.from_rows([["2"]]))
    assert text.value.parameters["received"] == "str"

    shaped = ExactMatrix.identity(2)
    shaped.rows = True
    with pytest.raises(SmithFormError, match="boolean refused") as boolean_dimension:
        smith_normal_form(shaped)
    assert boolean_dimension.value.invariant == "boolean refused where a matrix dimension was required"

    shaped_float = ExactMatrix.identity(2)
    shaped_float.rows = _probe("1.0")
    with pytest.raises(SmithFormError, match="float refused") as float_dimension:
        smith_normal_form(shaped_float)
    assert float_dimension.value.parameters["role"] == "rows"

    with pytest.raises(SmithFormError, match="negative") as negative:
        smith_normal_form(ExactMatrix(-1, 0, []))
    assert negative.value.parameters["received"] == -1

    shaped_text = ExactMatrix.identity(2)
    shaped_text.cols = "1"
    with pytest.raises(SmithFormError, match="not an integer") as text_dimension:
        smith_normal_form(shaped_text)
    assert text_dimension.value.parameters["received"] == "str"

    with pytest.raises(SmithFormError, match="exact matrix") as foreign:
        smith_normal_form("matrix")
    assert foreign.value.parameters["received"] == "str"

    stretched = ExactMatrix.identity(2)
    stretched.rows = 3
    stretched.cols = 3
    with pytest.raises(SmithFormError, match="data length") as length:
        smith_normal_form(stretched)
    assert length.value.parameters["length"] == 4

    with pytest.raises(SmithFormError, match="elimination bound") as bound:
        _charge_step(_Board([[1]], [[1]], [[1]], 1, 1, 3, 2))
    assert bound.value.parameters["steps"] == 4
    assert bound.value.parameters["limit"] == 2

    with pytest.raises(SmithFormError, match="pivot is zero") as pivot:
        _quotient(3, 0)
    assert pivot.value.parameters["entry"] == 3

    with pytest.raises(SmithFormError, match="negative") as signed:
        _require_divisibility([-1])
    assert signed.value.parameters["entry"] == -1

    with pytest.raises(SmithFormError, match="follows a zero") as trailing:
        _require_divisibility([0, 5])
    assert trailing.value.parameters["entry"] == 5

    with pytest.raises(SmithFormError, match="divisibility") as division:
        _require_divisibility([4, 2])
    assert division.value.parameters["left"] == 4
    assert division.value.parameters["right"] == 2

    with pytest.raises(SmithFormError, match="U\\*A\\*V") as product:
        _require_product(
            ExactMatrix.from_rows([[Fraction(1)]]),
            ExactMatrix.from_rows([[Fraction(2)]]),
            ExactMatrix.from_rows([[Fraction(1)]]),
            ExactMatrix.from_rows([[Fraction(1)]]),
        )
    assert product.value.invariant == "constructed factors do not satisfy U*A*V = D"

    with pytest.raises(SmithFormError, match="not ±1") as unimodular:
        _require_unimodular(ExactMatrix.from_rows([[Fraction(2), Fraction(0)], [Fraction(0), Fraction(1)]]), "U")
    assert unimodular.value.parameters["role"] == "U"
    assert unimodular.value.parameters["determinant"] == "2"


def test_integration_matches_rust_smith_sentence() -> None:
    root = Path(__file__).resolve().parents[3]
    source = (root / "code" / "rust" / "src" / "linear_algebra" / "smith_form.rs").read_text(encoding="utf-8")
    assert 'DEFAULT_SNF_PIVOT_ITERATION_LIMIT' in source
    assert 'DEFAULT_SNF_PIVOT_ITERATION_LIMIT' in source
    assert 'DEFAULT_SNF_PIVOT_ITERATION_LIMIT' in source
    diagonal, left, right = smith_normal_form(_witness())
    assert left * _witness() * right == diagonal
    assert invariant_factors(_witness()) == (Fraction(2), Fraction(2))


def test_end_to_end_public_contract() -> None:
    assert linear_algebra.exported_smith_trace() == 4
    package = linear_algebra.smith_form
    assert package.witness_diagonal_sum() == 4
    diagonal, left, right = package.smith_normal_form(ExactMatrix.identity(2))
    assert diagonal == ExactMatrix.identity(2)
    assert left == ExactMatrix.identity(2)
    assert right == ExactMatrix.identity(2)
    tampered = ExactMatrix.from_rows([[Fraction(1)]])
    tampered.data[0] = _probe("0.25")
    with pytest.raises(SmithFormError, match="float refused"):
        package.smith_normal_form(tampered)


def test_origin_resolves_in_repo() -> None:
    root = Path(__file__).resolve().parents[3]
    origin = root / "code" / "rust" / "src" / "linear_algebra" / "smith_form.rs"
    assert origin.is_file()
    text = origin.read_text(encoding="utf-8")
    assert 'DEFAULT_SNF_PIVOT_ITERATION_LIMIT' in text
    source = _MODULE_PATH.read_text(encoding="utf-8")
    assert "AuthorityEffect: None" in source
    assert "urn:omega:fqm:linear-algebra:smith-normal-form:v1" in source
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
        'if isinstance(value, GaussianRational):\n        raise _fail("Gaussian rational refused; Smith form in this module is over Q", role=role)',
        'if isinstance(value, GaussianRational):\n        return value.real\n    if False:\n        raise _fail("Gaussian rational refused; Smith form in this module is over Q", role=role)',
    ),
    (
        "boolean dimension admitted",
        'if type(value) is bool:\n        raise _fail("boolean refused where a matrix dimension was required", role=role)',
        'if type(value) is bool:\n        return 1\n    if False:\n        raise _fail("boolean refused where a matrix dimension was required", role=role)',
    ),
    (
        "pivot comparison inverted",
        "return abs(work[row][col]) < abs(work[pivot_row][pivot_col])",
        "return abs(work[row][col]) > abs(work[pivot_row][pivot_col])",
    ),
    (
        "elimination sign dropped",
        "return -(entry // pivot)",
        "return entry // pivot",
    ),
    (
        "divisibility comparison inverted",
        "if previous != 0 and entry % previous != 0:",
        "if previous != 0 and entry % previous == 0:",
    ),
    (
        "factor check inverted",
        "if left * original * right != diagonal:",
        "if left * original * right == diagonal:",
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
    witness = namespace["witness_diagonal_sum"]
    factor = namespace["smith_normal_form"]
    matrix = namespace["ExactMatrix"]
    if not _all_hold((callable(witness), callable(factor), isinstance(matrix, type),)):
        return False
    build = getattr(matrix, "from_rows")
    if not callable(build):
        return False
    try:
        total = witness()
        diagonal, left, right = factor(build([[Fraction(2), Fraction(4)], [Fraction(2), Fraction(6)]]))
        swapped, _, _ = factor(build([[Fraction(4), Fraction(0)], [Fraction(0), Fraction(2)]]))
        fractional, _, _ = factor(
            build(
                [
                    [Fraction(1, 2), Fraction(1, 3)],
                    [Fraction(1, 3), Fraction(1, 2)],
                ]
            )
        )
    except error:
        return False
    if not _all_hold((isinstance(diagonal, ExactMatrix), isinstance(left, ExactMatrix), isinstance(right, ExactMatrix),)):
        return False
    if not _all_hold((isinstance(swapped, ExactMatrix), isinstance(fractional, ExactMatrix),)):
        return False
    return _all_hold((
total == 4,
type(total) is Fraction,
diagonal.get(0, 0) == 2,
diagonal.get(1, 1) == 2,
diagonal.get(0, 1) == 0,
swapped.get(0, 0) == 2,
swapped.get(1, 1) == 4,
fractional.get(0, 0) == Fraction(1, 6),
fractional.get(1, 1) == Fraction(5, 6),
))


def _bad_values_refused(namespace: dict[str, object], error: type[BaseException]) -> bool:
    factor = namespace["smith_normal_form"]
    matrix = namespace["ExactMatrix"]
    gaussian = namespace["GaussianRational"]
    if not _all_hold((callable(factor), isinstance(matrix, type), callable(gaussian),)):
        return False
    build = getattr(matrix, "from_rows")
    identity = getattr(matrix, "identity")
    if not _all_hold((callable(build), callable(identity),)):
        return False
    shaped = identity(2)
    shaped.rows = True
    probes = (
        (lambda: factor(build([[_probe("1.5")]])), "float refused at the public boundary"),
        (lambda: factor(build([[True]])), "boolean refused where a rational entry was required"),
        (
            lambda: factor(build([[gaussian(0, 1)]])),
            "Gaussian rational refused; Smith form in this module is over Q",
        ),
        (lambda: factor(shaped), "boolean refused where a matrix dimension was required"),
    )
    for probe, invariant in probes:
        if _invariant(error, probe) != invariant:
            return False
    return True


def _oracle(namespace: dict[str, object]) -> bool:
    error_type = namespace["SmithFormError"]
    if not _all_hold((isinstance(error_type, type), issubclass(error_type, BaseException),)):
        return False
    if not _known_values_hold(namespace, error_type):
        return False
    return _bad_values_refused(namespace, error_type)


def test_mutation_suite_kills_non_equivalent_mutants() -> None:
    source = _MODULE_PATH.read_text(encoding="utf-8")
    loaded: list[str] = []
    try:
        loaded.append("mutant_smith_baseline")
        baseline = _load_source(source, loaded[-1])
        assert _oracle(baseline) is True
        killed = 0
        for index, (name, old, new) in enumerate(_MUTANTS):
            count = source.count(old)
            assert count == 1, f"{name} matched {count} sites"
            module_name = f"mutant_smith_{index}"
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
