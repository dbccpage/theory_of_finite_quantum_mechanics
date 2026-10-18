"""Unit, negative, integration, end-to-end, and mutation tests for the algebra laws.

Origin: code/python/src/linear_algebra/laws.py
Claim: urn:omega:fqm:linear-algebra:algebra-laws:v1
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
from src.linear_algebra.laws import (
    ExactMatrix,
    LawError,
    _require_product,
    _require_zero_defect,
    associator_defect,
    transpose_law_defect,
    witness_product_entry,
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


_MODULE_PATH = Path(__file__).resolve().parents[1] / "src" / "linear_algebra" / "laws.py"


def _left() -> ExactMatrix:
    return ExactMatrix.from_rows([[Fraction(1), Fraction(2)], [Fraction(0), Fraction(1)]])


def _right() -> ExactMatrix:
    return ExactMatrix.from_rows([[Fraction(3), Fraction(0)], [Fraction(4), Fraction(5)]])


def _assoc_left() -> ExactMatrix:
    return ExactMatrix.from_rows([[Fraction(1), Fraction(1)], [Fraction(0), Fraction(1)]])


def _assoc_mid() -> ExactMatrix:
    return ExactMatrix.from_rows([[Fraction(1), Fraction(0)], [Fraction(1), Fraction(1)]])


def _assoc_right() -> ExactMatrix:
    return ExactMatrix.from_rows([[Fraction(2), Fraction(0)], [Fraction(0), Fraction(3)]])


def _transposed_product() -> ExactMatrix:
    return ExactMatrix.from_rows([[Fraction(11), Fraction(4)], [Fraction(10), Fraction(5)]])


def _associated() -> ExactMatrix:
    return ExactMatrix.from_rows([[Fraction(4), Fraction(3)], [Fraction(2), Fraction(3)]])


def test_laws_match_the_hand_matrices() -> None:
    assert transpose_law_defect(_left(), _right()) == 0
    assert associator_defect(_assoc_left(), _assoc_mid(), _assoc_right()) == 0
    assert witness_product_entry() == 4
    assert (_left() * _right()).transpose() == _transposed_product()
    assert (_assoc_left() * _assoc_mid()) * _assoc_right() == _associated()
    assert type(witness_product_entry()) is Fraction


def test_negative_boundary_failures() -> None:
    with pytest.raises(LawError, match="float refused") as floated:
        transpose_law_defect(ExactMatrix.from_rows([[_probe("1.5")]]), ExactMatrix.from_rows([[Fraction(1)]]))
    assert floated.value.invariant == "float refused at the public boundary"
    assert floated.value.parameters["role"] == "entry[0]"
    assert type(floated.value) is LawError

    with pytest.raises(LawError, match="boolean refused where a rational") as boolean:
        transpose_law_defect(ExactMatrix.from_rows([[True]]), ExactMatrix.from_rows([[Fraction(1)]]))
    assert boolean.value.invariant == "boolean refused where a rational entry was required"

    with pytest.raises(LawError, match="Gaussian rational refused") as gaussian:
        transpose_law_defect(
            ExactMatrix.from_rows([[GaussianRational(0, 1)]]),
            ExactMatrix.from_rows([[Fraction(1)]]),
        )
    assert gaussian.value.parameters["role"] == "entry[0]"

    with pytest.raises(LawError, match="not an exact rational") as text:
        transpose_law_defect(ExactMatrix.from_rows([["1"]]), ExactMatrix.from_rows([[Fraction(1)]]))
    assert text.value.parameters["received"] == "str"

    shaped = ExactMatrix.from_rows([[Fraction(1)]])
    shaped.rows = True
    with pytest.raises(LawError, match="boolean refused where a matrix dimension") as dim_bool:
        transpose_law_defect(shaped, shaped)
    assert dim_bool.value.parameters["role"] == "rows"

    shaped = ExactMatrix.from_rows([[Fraction(1)]])
    shaped.rows = _probe("1.0")
    with pytest.raises(LawError, match="float refused") as dim_float:
        transpose_law_defect(shaped, ExactMatrix.from_rows([[Fraction(1)]]))
    assert dim_float.value.parameters["role"] == "rows"

    with pytest.raises(LawError, match="negative") as negative:
        transpose_law_defect(ExactMatrix(-1, 0, []), ExactMatrix(0, 0, []))
    assert negative.value.parameters["received"] == -1

    named = ExactMatrix.from_rows([[Fraction(1)]])
    named.cols = "1"
    with pytest.raises(LawError, match="not an integer") as named_error:
        transpose_law_defect(named, named)
    assert named_error.value.parameters["received"] == "str"

    with pytest.raises(LawError, match="not an ExactMatrix") as bare:
        transpose_law_defect("matrix", _left())
    assert bare.value.parameters["received"] == "str"

    mismatched = ExactMatrix.identity(2)
    mismatched.rows = 3
    mismatched.cols = 3
    with pytest.raises(LawError, match="data length") as length_error:
        transpose_law_defect(mismatched, ExactMatrix.identity(2))
    assert length_error.value.parameters["length"] == 4

    wide = ExactMatrix.from_rows([[Fraction(1), Fraction(2)]])
    with pytest.raises(LawError, match="cannot multiply") as shapes:
        transpose_law_defect(wide, ExactMatrix.from_rows([[Fraction(1)]]))
    assert shapes.value.parameters["role"] == "transpose"
    assert shapes.value.parameters["left_cols"] == 2

    with pytest.raises(LawError, match="cannot multiply") as assoc:
        associator_defect(_left(), ExactMatrix.from_rows([[Fraction(1)]]), _right())
    assert assoc.value.parameters["role"] == "associator-left"

    with pytest.raises(LawError, match="algebra-law defect") as defect:
        _require_zero_defect(Fraction(1), "witness")
    assert defect.value.parameters["defect"] == "1"

    with pytest.raises(LawError, match="cannot multiply") as product:
        _require_product(2, 1, "transpose")
    assert product.value.parameters["right_rows"] == 1


def test_integration_matches_matrix_transpose_and_product() -> None:
    root = Path(__file__).resolve().parents[3]
    source = (root / "code" / "python" / "src" / "linear_algebra" / "matrix.py").read_text(encoding="utf-8")
    assert "def __mul__" in source
    assert "def transpose" in source
    left = _left()
    right = _right()
    cited = right.transpose() * left.transpose()
    assert cited == _transposed_product()
    assert (left * right).transpose() == cited
    assert transpose_law_defect(left, right) == 0
    rectangular_left = ExactMatrix.from_rows(
        [[Fraction(1), Fraction(0), Fraction(1)], [Fraction(0), Fraction(1), Fraction(1)]]
    )
    rectangular_right = ExactMatrix.from_rows(
        [[Fraction(1), Fraction(2)], [Fraction(3), Fraction(0)], [Fraction(0), Fraction(4)]]
    )
    assert transpose_law_defect(rectangular_left, rectangular_right) == 0
    assert associator_defect(_assoc_left(), _assoc_mid(), _assoc_right()) == 0
    assert (_assoc_left() * _assoc_mid()) * _assoc_right() == _assoc_left() * (_assoc_mid() * _assoc_right())


def test_end_to_end_public_contract() -> None:
    package = linear_algebra.laws
    assert package.witness_product_entry() == 4
    assert package.transpose_law_defect(ExactMatrix.identity(2), ExactMatrix.identity(2)) == 0
    assert package.associator_defect(ExactMatrix.identity(1), ExactMatrix.identity(1), ExactMatrix.identity(1)) == 0
    empty = ExactMatrix(0, 0, [])
    assert package.transpose_law_defect(empty, empty) == 0
    tampered = ExactMatrix.identity(1)
    tampered.data[0] = _probe("0.25")
    with pytest.raises(LawError, match="float refused"):
        package.transpose_law_defect(tampered, tampered)


def test_origin_resolves_in_repo() -> None:
    root = Path(__file__).resolve().parents[3]
    matrix_source = root / "code" / "python" / "src" / "linear_algebra" / "matrix.py"
    assert matrix_source.is_file()
    text = matrix_source.read_text(encoding="utf-8")
    assert "def __mul__" in text
    assert "def transpose" in text
    source = _MODULE_PATH.read_text(encoding="utf-8")
    assert "AuthorityEffect: None" in source
    assert "urn:omega:fqm:linear-algebra:algebra-laws:v1" in source
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
        'if isinstance(value, GaussianRational):\n        raise _fail("Gaussian rational refused; algebra laws in this module are over Q", role=role)',
        'if isinstance(value, GaussianRational):\n        return value.real\n    if False:\n        raise _fail("Gaussian rational refused; algebra laws in this module are over Q", role=role)',
    ),
    (
        "boolean dimension admitted",
        'if type(value) is bool:\n        raise _fail("boolean refused where a matrix dimension was required", role=role)',
        'if type(value) is bool:\n        return 1\n    if False:\n        raise _fail("boolean refused where a matrix dimension was required", role=role)',
    ),
    (
        "transpose order swapped",
        "right_m.transpose() * left_m.transpose()",
        "left_m.transpose() * right_m.transpose()",
    ),
    (
        "associator factors swapped",
        "left_m * (mid_m * right_m)",
        "left_m * (right_m * mid_m)",
    ),
    (
        "shape check inverted",
        "if left_cols != right_rows:",
        "if left_cols == right_rows:",
    ),
    (
        "witness entry moved",
        "product.get(0, 1)",
        "product.get(1, 0)",
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
    transpose_defect = namespace["transpose_law_defect"]
    associator = namespace["associator_defect"]
    witness = namespace["witness_product_entry"]
    if not _all_hold((callable(transpose_defect), callable(associator), callable(witness),)):
        return False
    try:
        transpose = transpose_defect(_left(), _right())
        associated = associator(_assoc_left(), _assoc_mid(), _assoc_right())
        entry = witness()
    except error:
        return False
    return _all_hold((
transpose == 0,
associated == 0,
entry == 4,
))


def _bad_values_refused(namespace: dict[str, object], error: type[BaseException]) -> bool:
    transpose_defect = namespace["transpose_law_defect"]
    matrix = namespace["ExactMatrix"]
    gaussian = namespace["GaussianRational"]
    if not _all_hold((callable(transpose_defect), isinstance(matrix, type), callable(gaussian),)):
        return False
    build = getattr(matrix, "from_rows")
    if not callable(build):
        return False
    shaped = build([[Fraction(1)]])
    shaped.rows = True
    partner = build([[Fraction(1)]])
    probes = (
        (lambda: transpose_defect(build([[_probe("1.5")]]), partner), "float refused at the public boundary"),
        (lambda: transpose_defect(build([[True]]), partner), "boolean refused where a rational entry was required"),
        (
            lambda: transpose_defect(build([[gaussian(0, 1)]]), partner),
            "Gaussian rational refused; algebra laws in this module are over Q",
        ),
        (lambda: transpose_defect(shaped, partner), "boolean refused where a matrix dimension was required"),
    )
    for probe, invariant in probes:
        if _invariant(error, probe) != invariant:
            return False
    return True


def _oracle(namespace: dict[str, object]) -> bool:
    error_type = namespace["LawError"]
    if not _all_hold((isinstance(error_type, type), issubclass(error_type, BaseException),)):
        return False
    if not _known_values_hold(namespace, error_type):
        return False
    return _bad_values_refused(namespace, error_type)


def test_mutation_suite_kills_non_equivalent_mutants() -> None:
    source = _MODULE_PATH.read_text(encoding="utf-8")
    loaded: list[str] = []
    try:
        loaded.append("mutant_laws_baseline")
        baseline = _load_source(source, loaded[-1])
        assert _oracle(baseline) is True
        killed = 0
        for index, (name, old, new) in enumerate(_MUTANTS):
            count = source.count(old)
            assert count == 1, f"{name} matched {count} sites"
            module_name = f"mutant_laws_{index}"
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
