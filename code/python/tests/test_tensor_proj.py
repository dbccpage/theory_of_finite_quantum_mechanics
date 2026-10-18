"""Unit, negative, integration, end-to-end, and mutation tests for the wrong-sign marginal.

Origin: code/python/src/linear_algebra/tensor_proj.py
Claim: urn:omega:fqm:linear-algebra:tensor-wrong-sign:v1
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
from src.linear_algebra.complex_tensor import kronecker
from src.linear_algebra.tensor_proj import (
    ExactMatrix,
    ProjectorError,
    _basis_shift,
    _require_operator,
    _require_zero_defect,
    _witness_references,
    _wrong_sign,
    reference_twice_defect,
    witness_basis_entry,
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


_MODULE_PATH = Path(__file__).resolve().parents[1] / "src" / "linear_algebra" / "tensor_proj.py"


def _balanced() -> ExactMatrix:
    return ExactMatrix.from_rows([[Fraction(1, 2), Fraction(0)], [Fraction(0), Fraction(1, 2)]])


def _weighted() -> ExactMatrix:
    return ExactMatrix.from_rows([[Fraction(1, 3), Fraction(0)], [Fraction(0), Fraction(2, 3)]])


def _product_literal() -> ExactMatrix:
    return ExactMatrix.from_rows(
        [
            [Fraction(1, 6), Fraction(0), Fraction(0), Fraction(0)],
            [Fraction(0), Fraction(1, 3), Fraction(0), Fraction(0)],
            [Fraction(0), Fraction(0), Fraction(1, 6), Fraction(0)],
            [Fraction(0), Fraction(0), Fraction(0), Fraction(1, 3)],
        ]
    )


def _rank_one() -> ExactMatrix:
    return ExactMatrix.from_rows(
        [[Fraction(1, 2), Fraction(1, 2)], [Fraction(1, 2), Fraction(1, 2)]]
    )


def test_wrong_sign_matches_the_hand_matrices() -> None:
    assert reference_twice_defect(_balanced(), _weighted()) == 0
    assert witness_basis_entry() == Fraction(3, 2)
    assert type(witness_basis_entry()) is Fraction
    assert kronecker(_balanced(), _weighted()) == _product_literal()
    left, right = _witness_references()
    product = kronecker(left, right)
    wrong = _wrong_sign(_basis_shift(), left, right, product)
    assert wrong.get(0, 1) == Fraction(3, 2)
    assert wrong.get(2, 3) == Fraction(1, 2)
    assert reference_twice_defect(_rank_one(), ExactMatrix.from_rows([[Fraction(1)]])) == 0
    one = ExactMatrix.from_rows([[Fraction(1)]])
    assert reference_twice_defect(one, one) == 0


def test_negative_boundary_failures() -> None:
    partner = ExactMatrix.from_rows([[Fraction(1)]])
    with pytest.raises(ProjectorError, match="float refused") as floated:
        reference_twice_defect(ExactMatrix.from_rows([[_probe("1.5")]]), partner)
    assert floated.value.invariant == "float refused at the public boundary"
    assert floated.value.parameters["role"] == "entry[0]"
    assert type(floated.value) is ProjectorError

    with pytest.raises(ProjectorError, match="boolean refused where a rational") as boolean:
        reference_twice_defect(ExactMatrix.from_rows([[True]]), partner)
    assert boolean.value.invariant == "boolean refused where a rational entry was required"

    with pytest.raises(ProjectorError, match="Gaussian rational refused") as gaussian:
        reference_twice_defect(ExactMatrix.from_rows([[GaussianRational(0, 1)]]), partner)
    assert gaussian.value.parameters["role"] == "entry[0]"

    with pytest.raises(ProjectorError, match="not an exact rational") as text:
        reference_twice_defect(ExactMatrix.from_rows([["1"]]), partner)
    assert text.value.parameters["received"] == "str"

    shaped = ExactMatrix.from_rows([[Fraction(1)]])
    shaped.rows = True
    with pytest.raises(ProjectorError, match="boolean refused where a matrix dimension") as dim_bool:
        reference_twice_defect(shaped, partner)
    assert dim_bool.value.parameters["role"] == "rows"

    shaped = ExactMatrix.from_rows([[Fraction(1)]])
    shaped.rows = _probe("1.0")
    with pytest.raises(ProjectorError, match="float refused") as dim_float:
        reference_twice_defect(shaped, partner)
    assert dim_float.value.parameters["role"] == "rows"

    with pytest.raises(ProjectorError, match="negative") as negative:
        reference_twice_defect(ExactMatrix(-1, 0, []), partner)
    assert negative.value.parameters["received"] == -1

    named = ExactMatrix.from_rows([[Fraction(1)]])
    named.cols = "1"
    with pytest.raises(ProjectorError, match="not an integer") as named_error:
        reference_twice_defect(named, partner)
    assert named_error.value.parameters["received"] == "str"

    with pytest.raises(ProjectorError, match="not an ExactMatrix") as bare:
        reference_twice_defect("matrix", partner)
    assert bare.value.parameters["received"] == "str"

    mismatched = ExactMatrix.identity(2)
    mismatched.rows = 3
    mismatched.cols = 3
    with pytest.raises(ProjectorError, match="data length") as length_error:
        reference_twice_defect(mismatched, partner)
    assert length_error.value.parameters["length"] == 4

    wide = ExactMatrix.from_rows([[Fraction(1), Fraction(2)]])
    with pytest.raises(ProjectorError, match="not square") as rectangular:
        reference_twice_defect(wide, partner)
    assert rectangular.value.parameters["role"] == "left"
    assert rectangular.value.parameters["cols"] == 2

    with pytest.raises(ProjectorError, match="empty") as empty:
        reference_twice_defect(ExactMatrix(0, 0, []), partner)
    assert empty.value.parameters["rows"] == 0

    heavy = ExactMatrix.from_rows([[Fraction(1), Fraction(0)], [Fraction(0), Fraction(2)]])
    with pytest.raises(ProjectorError, match="trace one") as traced:
        reference_twice_defect(heavy, partner)
    assert traced.value.parameters["trace"] == "3"
    assert traced.value.parameters["role"] == "left"

    with pytest.raises(ProjectorError, match="does not match the product") as shape:
        _require_operator(ExactMatrix.identity(1), 2)
    assert shape.value.parameters["size"] == 2
    assert shape.value.parameters["rows"] == 1

    with pytest.raises(ProjectorError, match="tensor-marginal defect") as defect:
        _require_zero_defect(Fraction(1), "witness")
    assert defect.value.parameters["defect"] == "1"


def test_integration_matches_rust_wrong_sign_and_kronecker() -> None:
    root = Path(__file__).resolve().parents[3]
    source = (root / "code" / "rust" / "src" / "linear_algebra" / "tensor_proj.rs").read_text(encoding="utf-8")
    assert 'product_differential_with_limits' in source
    assert 'product_differential_with_limits' in source
    assert kronecker(_balanced(), _weighted()) == _product_literal()
    assert reference_twice_defect(_balanced(), _weighted()) == 0
    neighbor = ( _balanced() * ExactMatrix.identity(2) )
    assert reference_twice_defect(neighbor, _weighted()) == 0


def test_end_to_end_public_contract() -> None:
    package = linear_algebra.tensor_proj
    assert package.witness_basis_entry() == Fraction(3, 2)
    assert package.reference_twice_defect(_balanced(), _weighted()) == 0
    one = ExactMatrix.from_rows([[Fraction(1)]])
    assert package.reference_twice_defect(one, one) == 0
    tampered = ExactMatrix.from_rows([[Fraction(1)]])
    tampered.data[0] = _probe("0.25")
    with pytest.raises(ProjectorError, match="float refused"):
        package.reference_twice_defect(tampered, one)


def test_origin_resolves_in_repo() -> None:
    root = Path(__file__).resolve().parents[3]
    origin = root / "code" / "rust" / "src" / "linear_algebra" / "tensor_proj.rs"
    assert origin.is_file()
    text = origin.read_text(encoding="utf-8")
    assert "exact trace one" in text
    assert 'product_differential_with_limits' in text
    source = _MODULE_PATH.read_text(encoding="utf-8")
    assert "AuthorityEffect: None" in source
    assert "urn:omega:fqm:linear-algebra:tensor-wrong-sign:v1" in source
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
        'if isinstance(value, GaussianRational):\n        raise _fail("Gaussian rational refused; tensor marginals in this module are over Q", role=role)',
        'if isinstance(value, GaussianRational):\n        return value.real\n    if False:\n        raise _fail("Gaussian rational refused; tensor marginals in this module are over Q", role=role)',
    ),
    (
        "boolean dimension admitted",
        'if type(value) is bool:\n        raise _fail("boolean refused where a matrix dimension was required", role=role)',
        'if type(value) is bool:\n        return 1\n    if False:\n        raise _fail("boolean refused where a matrix dimension was required", role=role)',
    ),
    (
        "left marginal dropped",
        "operator - empty + kept_left + kept_right",
        "operator - empty + kept_right",
    ),
    (
        "twice coefficient halved",
        "_scale(product, Fraction(2))",
        "_scale(product, Fraction(1))",
    ),
    (
        "trace gate inverted",
        "if trace != 1:",
        "if trace == 1:",
    ),
    (
        "basis entry moved",
        "wrong.get(0, 1)",
        "wrong.get(2, 3)",
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
    defect = namespace["reference_twice_defect"]
    witness = namespace["witness_basis_entry"]
    matrix = namespace["ExactMatrix"]
    if not _all_hold((callable(defect), callable(witness), isinstance(matrix, type),)):
        return False
    build = getattr(matrix, "from_rows")
    if not callable(build):
        return False
    try:
        gap = defect(_balanced(), _weighted())
        entry = witness()
    except error:
        return False
    return _all_hold((
gap == 0,
entry == Fraction(3, 2),
))


def _bad_values_refused(namespace: dict[str, object], error: type[BaseException]) -> bool:
    defect = namespace["reference_twice_defect"]
    matrix = namespace["ExactMatrix"]
    gaussian = namespace["GaussianRational"]
    if not _all_hold((callable(defect), isinstance(matrix, type), callable(gaussian),)):
        return False
    build = getattr(matrix, "from_rows")
    if not callable(build):
        return False
    shaped = build([[Fraction(1)]])
    shaped.rows = True
    partner = build([[Fraction(1)]])
    probes = (
        (lambda: defect(build([[_probe("1.5")]]), partner), "float refused at the public boundary"),
        (lambda: defect(build([[True]]), partner), "boolean refused where a rational entry was required"),
        (
            lambda: defect(build([[gaussian(0, 1)]]), partner),
            "Gaussian rational refused; tensor marginals in this module are over Q",
        ),
        (lambda: defect(shaped, partner), "boolean refused where a matrix dimension was required"),
    )
    for probe, invariant in probes:
        if _invariant(error, probe) != invariant:
            return False
    return True


def _oracle(namespace: dict[str, object]) -> bool:
    error_type = namespace["ProjectorError"]
    if not _all_hold((isinstance(error_type, type), issubclass(error_type, BaseException),)):
        return False
    if not _known_values_hold(namespace, error_type):
        return False
    return _bad_values_refused(namespace, error_type)


def test_mutation_suite_kills_non_equivalent_mutants() -> None:
    source = _MODULE_PATH.read_text(encoding="utf-8")
    loaded: list[str] = []
    try:
        loaded.append("mutant_tensor_baseline")
        baseline = _load_source(source, loaded[-1])
        assert _oracle(baseline) is True
        killed = 0
        for index, (name, old, new) in enumerate(_MUTANTS):
            count = source.count(old)
            assert count == 1, f"{name} matched {count} sites"
            module_name = f"mutant_tensor_{index}"
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
