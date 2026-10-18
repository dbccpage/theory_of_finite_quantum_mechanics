"""Unit, negative, integration, end-to-end, and mutation tests for carriers.

Origin: code/python/src/homology/carrier.py
Claim: urn:omega:fqm:homology:carrier-coboundary-square:v1
AuthorityEffect: None
Mutation-Kills: 8 non-equivalent
"""





from __future__ import annotations

import importlib.util
import sys
import warnings
from fractions import Fraction
from pathlib import Path
from typing import cast

import pytest

from src.homology.carrier import Carrier
from src.homology.coboundary import triangle_coboundaries
from src.homology.errors import DimensionMismatchError, NonZeroCompositionError, require_composition_zero
from src.homology.witness import HomologyWitness
from src.linear_algebra import ExactMatrix

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


_MODULE_PATH = Path(__file__).resolve().parents[1] / "src" / "homology" / "carrier.py"


def _triangle() -> tuple[ExactMatrix, ExactMatrix]:
    delta0 = ExactMatrix.from_rows(
        [
            [Fraction(-1), Fraction(1), Fraction(0)],
            [Fraction(-1), Fraction(0), Fraction(1)],
            [Fraction(0), Fraction(-1), Fraction(1)],
        ]
    )
    delta1 = ExactMatrix.from_rows([[Fraction(1), Fraction(-1), Fraction(1)]])
    return delta0, delta1


def test_triangle_carrier_rank_nullity() -> None:
    delta0, delta1 = _triangle()
    carrier = Carrier(3, 3, 1, delta0, delta1, [Fraction(1), Fraction(1), Fraction(1)])
    assert carrier.dimensions() == (3, 3, 1)
    assert carrier.rank_d0() == 2
    assert carrier.rank_d1() == 1
    assert carrier.dim_q1() == 1
    assert carrier.dim_h1() == 0
    assert carrier.weights == (Fraction(1), Fraction(1), Fraction(1))
    assert carrier.sha256() == Carrier(3, 3, 1, delta0, delta1).sha256()


def test_negative_carrier_failures() -> None:
    delta0, delta1 = _triangle()
    floated = ExactMatrix.from_rows([[_probe("1.0")]])
    zero = ExactMatrix.from_rows([[Fraction(0)]])
    with pytest.raises(DimensionMismatchError, match="float refused") as float_error:
        Carrier(1, 1, 1, floated, zero)
    assert float_error.value.parameters["role"] == "d0[0]"

    boolean = ExactMatrix.from_rows([[True]])
    with pytest.raises(DimensionMismatchError, match="boolean refused where a rational") as bool_error:
        Carrier(1, 1, 1, boolean, zero)
    assert bool_error.value.parameters["role"] == "d0[0]"

    with pytest.raises(DimensionMismatchError, match="boolean refused where a dimension") as dim_bool:
        Carrier(True, 3, 1, delta0, delta1)
    assert dim_bool.value.parameters["role"] == "dim0"

    with pytest.raises(DimensionMismatchError, match="dimension is negative") as negative:
        Carrier(-1, 3, 1, delta0, delta1)
    assert negative.value.parameters["received"] == -1

    with pytest.raises(DimensionMismatchError, match="shape does not match") as shape:
        Carrier(2, 3, 1, delta0, delta1)
    assert shape.value.parameters["expected_cols"] == 2

    with pytest.raises(DimensionMismatchError, match="exact matrices") as bare:
        Carrier(3, 3, 1, cast(object, ((1, 0),)), delta1)
    assert bare.value.parameters["received"] == "tuple"

    opened = ExactMatrix.from_rows([[Fraction(1), Fraction(1), Fraction(1)]])
    with pytest.raises(NonZeroCompositionError, match="do not compose to zero") as opened_error:
        Carrier(3, 3, 1, delta0, opened)
    assert opened_error.value.parameters["defect"] == "4"

    with pytest.raises(DimensionMismatchError, match="weights must be a sequence") as text:
        Carrier(3, 3, 1, delta0, delta1, "abc")
    assert text.value.parameters["received"] == "str"

    with pytest.raises(DimensionMismatchError, match="float refused") as weight_float:
        Carrier(3, 3, 1, delta0, delta1, [_probe("1.5")])
    assert weight_float.value.parameters["role"] == "weight[0]"


def test_integration_with_witness_and_composition() -> None:
    delta0, delta1 = triangle_coboundaries()
    carrier = Carrier(3, 3, 1, delta0, delta1)
    rows0 = [delta0.row(index) for index in range(delta0.rows)]
    rows1 = [delta1.row(index) for index in range(delta1.rows)]
    assert require_composition_zero(rows1, rows0) == Fraction(0)
    witness = HomologyWitness.from_carrier(carrier)
    assert witness.is_valid is True
    assert witness.dim_h1 == carrier.dim_h1()
    assert witness.carrier_hash == carrier.sha256()


def test_end_to_end_public_contract() -> None:
    edge = ExactMatrix.from_rows(
        [
            [Fraction(-1), Fraction(1), Fraction(0)],
            [Fraction(0), Fraction(-1), Fraction(1)],
            [Fraction(1), Fraction(0), Fraction(-1)],
        ]
    )
    face = ExactMatrix.from_rows([[Fraction(1), Fraction(1), Fraction(1)]])
    carrier = Carrier(3, 3, 1, edge, face, [Fraction(1), Fraction(1), Fraction(1)])
    assert carrier.rank_d0() == 2
    assert carrier.rank_d1() == 1
    assert carrier.dim_h1() == 0
    with pytest.raises(DimensionMismatchError, match="float refused"):
        Carrier(1, 1, 1, ExactMatrix.from_rows([[_probe("0.5")]]), ExactMatrix.from_rows([[Fraction(0)]]))


def test_origin_resolves_in_repo() -> None:
    root = Path(__file__).resolve().parents[3]
    lean = (root / "lean4" / "CellGrammar.lean").read_text(encoding="utf-8")
    assert "boundarySquare_implies_cochain" in lean
    assert "d0Carrier" in lean
    source = _MODULE_PATH.read_text(encoding="utf-8")
    assert "AuthorityEffect: None" in source
    assert "urn:omega:fqm:homology:carrier-coboundary-square:v1" in source
    assert "Scope Fence:" in source


_MUTANTS: tuple[tuple[str, str, str], ...] = (
    (
        "float admitted",
        "if isinstance(value, float):",
        "if isinstance(value, float):\n        return Fraction(value)\n    if False:",
    ),
    (
        "boolean admitted as an integer",
        "if isinstance(value, bool):",
        "if isinstance(value, bool):\n        return Fraction(int(value))\n    if False:",
    ),
    ("dimension boolean admitted", "if type(value) is bool:", "if False and type(value) is bool:"),
    ("square check inverted", "if defect != 0:", "if defect == 0:"),
    ("negative dimension accepted", "if value < 0:", "if value < -1:"),
    (
        "shape check inverted",
        "if matrix.rows != rows or matrix.cols != cols:",
        "if matrix.rows == rows and matrix.cols == cols:",
    ),
    (
        "defect shifted by one",
        'defect += abs(_rational(entry, f"product[{index}]"))',
        'defect += abs(_rational(entry, f"product[{index}]")) + 1',
    ),
    (
        "homology dimension shifted by one",
        "return (self.dim1 - self.rank_d1()) - self.rank_d0()",
        "return (self.dim1 - self.rank_d1()) - self.rank_d0() + 1",
    ),
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


def _triangle_matrices(factory: object) -> tuple[object, object]:
    if not callable(factory):
        raise RuntimeError("matrix factory is not callable")
    delta0 = factory(
        [
            [Fraction(-1), Fraction(1), Fraction(0)],
            [Fraction(-1), Fraction(0), Fraction(1)],
            [Fraction(0), Fraction(-1), Fraction(1)],
        ]
    )
    delta1 = factory([[Fraction(1), Fraction(-1), Fraction(1)]])
    return delta0, delta1


def _known_values_hold(namespace: dict[str, object], error: type[BaseException]) -> bool:
    carrier_type = namespace["Carrier"]
    matrix_type = namespace["ExactMatrix"]
    factory = getattr(matrix_type, "from_rows", None)
    if not _all_hold((isinstance(carrier_type, type), callable(factory),)):
        return False
    try:
        delta0, delta1 = _triangle_matrices(factory)
        built = carrier_type(3, 3, 1, delta0, delta1)
        weighted = carrier_type(3, 3, 1, delta0, delta1, [Fraction(1), Fraction(0), Fraction(1)])
    except error:
        return False
    if built.dimensions() != (3, 3, 1) or built.dim_h1() != 0 or built.dim_q1() != 1:
        return False
    if built.rank_d0() != 2 or built.rank_d1() != 1:
        return False
    if weighted.sha256() != built.sha256() or weighted.weights != (Fraction(1), Fraction(0), Fraction(1)):
        return False
    return True


def _bad_values_refused(namespace: dict[str, object]) -> bool:
    mismatch = namespace["DimensionMismatchError"]
    nonzero = namespace["NonZeroCompositionError"]
    carrier_type = namespace["Carrier"]
    matrix_type = namespace["ExactMatrix"]
    factory = getattr(matrix_type, "from_rows", None)
    if not _all_hold((isinstance(mismatch, type), isinstance(nonzero, type), isinstance(carrier_type, type),)):
        return False
    if not callable(factory):
        return False
    delta0, delta1 = _triangle_matrices(factory)
    floated = factory([[_probe("1.0")]])
    boolean = factory([[True]])
    zero = factory([[Fraction(0)]])
    opened = factory([[Fraction(1), Fraction(1), Fraction(1)]])
    expected = (
        (mismatch, lambda: carrier_type(1, 1, 1, floated, zero), "float refused at the public boundary"),
        (mismatch, lambda: carrier_type(1, 1, 1, boolean, zero), "boolean refused where a rational was required"),
        (mismatch, lambda: carrier_type(True, 3, 1, delta0, delta1), "boolean refused where a dimension was required"),
        (mismatch, lambda: carrier_type(-1, 3, 1, delta0, delta1), "dimension is negative"),
        (mismatch, lambda: carrier_type(2, 3, 1, delta0, delta1), "carrier matrix shape does not match dimensions"),
        (nonzero, lambda: carrier_type(3, 3, 1, delta0, opened), "carrier coboundaries do not compose to zero"),
    )
    for error, probe, invariant in expected:
        if _invariant(error, probe) != invariant:
            return False
    return True


def _oracle(namespace: dict[str, object]) -> bool:
    error_type = namespace["DimensionMismatchError"]
    if not _all_hold((isinstance(error_type, type), issubclass(error_type, BaseException),)):
        return False
    if not _known_values_hold(namespace, error_type):
        return False
    return _bad_values_refused(namespace)


def test_mutation_suite_kills_non_equivalent_mutants() -> None:
    source = _MODULE_PATH.read_text(encoding="utf-8")
    loaded: list[str] = []
    try:
        loaded.append("mutant_carrier_baseline")
        baseline = _load_source(source, loaded[-1])
        assert _oracle(baseline) is True
        killed = 0
        for index, (name, old, new) in enumerate(_MUTANTS):
            count = source.count(old)
            assert count == 1, f"{name} matched {count} sites"
            module_name = f"mutant_carrier_{index}"
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
