"""Unit, negative, integration, end-to-end, and mutation tests for the Kronecker law.

Origin: code/python/src/linear_algebra/complex_tensor.py
Claim: urn:omega:fqm:linear-algebra:kronecker-mixed-product:v1
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
from src.linear_algebra.complex_tensor import (
    ExactMatrix,
    TensorError,
    _require_product,
    _require_zero_defect,
    kronecker,
    mixed_product_defect,
    trace_product_defect,
    witness_block_entry,
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


_MODULE_PATH = Path(__file__).resolve().parents[1] / "src" / "linear_algebra" / "complex_tensor.py"


def _block_left() -> ExactMatrix:
    return ExactMatrix.from_rows(
        [
            [Fraction(1), Fraction(2), Fraction(0)],
            [Fraction(0), Fraction(1), Fraction(3)],
        ]
    )


def _block_right() -> ExactMatrix:
    return ExactMatrix.from_rows(
        [
            [Fraction(1), Fraction(0)],
            [Fraction(4), Fraction(5)],
            [Fraction(0), Fraction(1)],
        ]
    )


def _mixed() -> tuple[ExactMatrix, ExactMatrix, ExactMatrix, ExactMatrix]:
    first = ExactMatrix.from_rows([[Fraction(1), Fraction(1)], [Fraction(0), Fraction(1)]])
    second = ExactMatrix.from_rows([[Fraction(2), Fraction(0)], [Fraction(0), Fraction(3)]])
    third = ExactMatrix.from_rows([[Fraction(1), Fraction(0)], [Fraction(1), Fraction(1)]])
    fourth = ExactMatrix.from_rows([[Fraction(1), Fraction(1)], [Fraction(0), Fraction(1)]])
    return first, second, third, fourth


def _trace_pair() -> tuple[ExactMatrix, ExactMatrix]:
    left = ExactMatrix.from_rows([[Fraction(1), Fraction(2)], [Fraction(3), Fraction(4)]])
    right = ExactMatrix.from_rows([[Fraction(1), Fraction(0)], [Fraction(0), Fraction(1, 3)]])
    return left, right


def _mixed_literal() -> ExactMatrix:
    return ExactMatrix.from_rows(
        [
            [Fraction(4), Fraction(4), Fraction(2), Fraction(2)],
            [Fraction(0), Fraction(6), Fraction(0), Fraction(3)],
            [Fraction(2), Fraction(2), Fraction(2), Fraction(2)],
            [Fraction(0), Fraction(3), Fraction(0), Fraction(3)],
        ]
    )


def _trace_literal() -> ExactMatrix:
    return ExactMatrix.from_rows(
        [
            [Fraction(1), Fraction(0), Fraction(2), Fraction(0)],
            [Fraction(0), Fraction(1, 3), Fraction(0), Fraction(2, 3)],
            [Fraction(3), Fraction(0), Fraction(4), Fraction(0)],
            [Fraction(0), Fraction(1), Fraction(0), Fraction(4, 3)],
        ]
    )


def test_kronecker_matches_the_hand_matrices() -> None:
    assert witness_block_entry() == 1
    assert type(witness_block_entry()) is Fraction
    assert kronecker(_block_left(), _block_right()).get(2, 1) == 1
    first, second, third, fourth = _mixed()
    assert mixed_product_defect(first, second, third, fourth) == 0
    assert kronecker(first * third, second * fourth) == _mixed_literal()
    left, right = _trace_pair()
    assert trace_product_defect(left, right) == 0
    assert kronecker(left, right) == _trace_literal()
    assert kronecker(ExactMatrix(0, 2, []), ExactMatrix.identity(3)).shape() == (0, 6)
    assert trace_product_defect(ExactMatrix(0, 0, []), ExactMatrix(0, 0, [])) == 0


def test_negative_boundary_failures() -> None:
    partner = ExactMatrix.from_rows([[Fraction(1)]])
    with pytest.raises(TensorError, match="float refused") as floated:
        kronecker(ExactMatrix.from_rows([[_probe("1.5")]]), partner)
    assert floated.value.invariant == "float refused at the public boundary"
    assert floated.value.parameters["role"] == "entry[0]"
    assert type(floated.value) is TensorError

    with pytest.raises(TensorError, match="boolean refused where a rational") as boolean:
        kronecker(ExactMatrix.from_rows([[True]]), partner)
    assert boolean.value.invariant == "boolean refused where a rational entry was required"

    with pytest.raises(TensorError, match="Gaussian rational refused") as gaussian:
        kronecker(ExactMatrix.from_rows([[GaussianRational(0, 1)]]), partner)
    assert gaussian.value.parameters["role"] == "entry[0]"

    with pytest.raises(TensorError, match="not an exact rational") as text:
        kronecker(ExactMatrix.from_rows([["1"]]), partner)
    assert text.value.parameters["received"] == "str"

    shaped = ExactMatrix.from_rows([[Fraction(1)]])
    shaped.rows = True
    with pytest.raises(TensorError, match="boolean refused where a matrix dimension") as dim_bool:
        kronecker(shaped, partner)
    assert dim_bool.value.parameters["role"] == "rows"

    shaped = ExactMatrix.from_rows([[Fraction(1)]])
    shaped.rows = _probe("1.0")
    with pytest.raises(TensorError, match="float refused") as dim_float:
        kronecker(shaped, partner)
    assert dim_float.value.parameters["role"] == "rows"

    with pytest.raises(TensorError, match="negative") as negative:
        kronecker(ExactMatrix(-1, 0, []), ExactMatrix(0, 0, []))
    assert negative.value.parameters["received"] == -1

    named = ExactMatrix.from_rows([[Fraction(1)]])
    named.cols = "1"
    with pytest.raises(TensorError, match="not an integer") as named_error:
        kronecker(named, partner)
    assert named_error.value.parameters["received"] == "str"

    with pytest.raises(TensorError, match="not an ExactMatrix") as bare:
        kronecker("matrix", partner)
    assert bare.value.parameters["received"] == "str"

    mismatched = ExactMatrix.identity(2)
    mismatched.rows = 3
    mismatched.cols = 3
    with pytest.raises(TensorError, match="data length") as length_error:
        kronecker(mismatched, partner)
    assert length_error.value.parameters["length"] == 4

    wide = ExactMatrix.from_rows([[Fraction(1), Fraction(2)]])
    with pytest.raises(TensorError, match="cannot multiply") as shapes:
        mixed_product_defect(wide, partner, partner, partner)
    assert shapes.value.parameters["role"] == "mixed-left"
    assert shapes.value.parameters["left_cols"] == 2

    with pytest.raises(TensorError, match="cannot multiply") as right_shapes:
        mixed_product_defect(partner, wide, partner, partner)
    assert right_shapes.value.parameters["role"] == "mixed-right"

    with pytest.raises(TensorError, match="not square") as rectangular:
        trace_product_defect(wide, partner)
    assert rectangular.value.parameters["role"] == "left"

    with pytest.raises(TensorError, match="Kronecker defect") as defect:
        _require_zero_defect(Fraction(1), "witness")
    assert defect.value.parameters["defect"] == "1"

    with pytest.raises(TensorError, match="cannot multiply") as product:
        _require_product(2, 1, "mixed-left")
    assert product.value.parameters["right_rows"] == 1


def test_integration_matches_matrix_product_and_rust_statement() -> None:
    root = Path(__file__).resolve().parents[3]
    source = (root / "code" / "rust" / "src" / "linear_algebra" / "matrix.rs").read_text(encoding="utf-8")
    assert 'multiplication_is_associative_and_distributive_and_agrees_with_the_std_ops_product' in source
    assert 'multiplication_is_associative_and_distributive_and_agrees_with_the_std_ops_product' in source
    assert 'multiplication_is_associative_and_distributive_and_agrees_with_the_std_ops_product' in source
    first, second, third, fourth = _mixed()
    cited = (first * third)
    neighbor = cited * ExactMatrix.identity(cited.rows)
    assert neighbor == first * third
    assert kronecker(first, second) * kronecker(third, fourth) == _mixed_literal()
    assert mixed_product_defect(first, second, third, fourth) == 0


def test_end_to_end_public_contract() -> None:
    package = linear_algebra.complex_tensor
    assert package.witness_block_entry() == 1
    assert package.trace_product_defect(ExactMatrix.identity(1), ExactMatrix.identity(1)) == 0
    assert package.mixed_product_defect(
        ExactMatrix.identity(1),
        ExactMatrix.identity(1),
        ExactMatrix.identity(1),
        ExactMatrix.identity(1),
    ) == 0
    tampered = ExactMatrix.identity(1)
    tampered.data[0] = _probe("0.25")
    with pytest.raises(TensorError, match="float refused"):
        package.kronecker(tampered, tampered)


def test_origin_resolves_in_repo() -> None:
    root = Path(__file__).resolve().parents[3]
    origin = root / "code" / "rust" / "src" / "linear_algebra" / "matrix.rs"
    assert origin.is_file()
    text = origin.read_text(encoding="utf-8")
    assert "pub fn kronecker" in text
    assert 'multiplication_is_associative_and_distributive_and_agrees_with_the_std_ops_product' in text
    source = _MODULE_PATH.read_text(encoding="utf-8")
    assert "AuthorityEffect: None" in source
    assert "urn:omega:fqm:linear-algebra:kronecker-mixed-product:v1" in source
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
        'if isinstance(value, GaussianRational):\n        raise _fail("Gaussian rational refused; the Kronecker product in this module is over Q", role=role)',
        'if isinstance(value, GaussianRational):\n        return value.real\n    if False:\n        raise _fail("Gaussian rational refused; the Kronecker product in this module is over Q", role=role)',
    ),
    (
        "boolean dimension admitted",
        'if type(value) is bool:\n        raise _fail("boolean refused where a matrix dimension was required", role=role)',
        'if type(value) is bool:\n        return 1\n    if False:\n        raise _fail("boolean refused where a matrix dimension was required", role=role)',
    ),
    (
        "block row split",
        "k = row % right_rows",
        "k = row // right_rows",
    ),
    (
        "mixed factors swapped",
        "kronecker(a_m * c_m, b_m * d_m)",
        "kronecker(b_m * d_m, a_m * c_m)",
    ),
    (
        "trace product became a sum",
        "left_trace * right_trace",
        "left_trace + right_trace",
    ),
    (
        "shape check inverted",
        "if left_cols != right_rows:",
        "if left_cols == right_rows:",
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
    witness = namespace["witness_block_entry"]
    mixed = namespace["mixed_product_defect"]
    traced = namespace["trace_product_defect"]
    if not _all_hold((callable(witness), callable(mixed), callable(traced),)):
        return False
    first, second, third, fourth = _mixed()
    left, right = _trace_pair()
    try:
        entry = witness()
        defect = mixed(first, second, third, fourth)
        trace_gap = traced(left, right)
    except error:
        return False
    return _all_hold((
entry == 1,
defect == 0,
trace_gap == 0,
))


def _bad_values_refused(namespace: dict[str, object], error: type[BaseException]) -> bool:
    product = namespace["kronecker"]
    matrix = namespace["ExactMatrix"]
    gaussian = namespace["GaussianRational"]
    if not _all_hold((callable(product), isinstance(matrix, type), callable(gaussian),)):
        return False
    build = getattr(matrix, "from_rows")
    if not callable(build):
        return False
    shaped = build([[Fraction(1)]])
    shaped.rows = True
    partner = build([[Fraction(1)]])
    probes = (
        (lambda: product(build([[_probe("1.5")]]), partner), "float refused at the public boundary"),
        (lambda: product(build([[True]]), partner), "boolean refused where a rational entry was required"),
        (
            lambda: product(build([[gaussian(0, 1)]]), partner),
            "Gaussian rational refused; the Kronecker product in this module is over Q",
        ),
        (lambda: product(shaped, partner), "boolean refused where a matrix dimension was required"),
    )
    for probe, invariant in probes:
        if _invariant(error, probe) != invariant:
            return False
    return True


def _oracle(namespace: dict[str, object]) -> bool:
    error_type = namespace["TensorError"]
    if not _all_hold((isinstance(error_type, type), issubclass(error_type, BaseException),)):
        return False
    if not _known_values_hold(namespace, error_type):
        return False
    return _bad_values_refused(namespace, error_type)


def test_mutation_suite_kills_non_equivalent_mutants() -> None:
    source = _MODULE_PATH.read_text(encoding="utf-8")
    loaded: list[str] = []
    try:
        loaded.append("mutant_kronecker_baseline")
        baseline = _load_source(source, loaded[-1])
        assert _oracle(baseline) is True
        killed = 0
        for index, (name, old, new) in enumerate(_MUTANTS):
            count = source.count(old)
            assert count == 1, f"{name} matched {count} sites"
            module_name = f"mutant_kronecker_{index}"
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
