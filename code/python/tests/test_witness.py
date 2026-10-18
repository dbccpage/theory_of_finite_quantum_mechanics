"""Unit, negative, integration, end-to-end, and mutation tests for homology witnesses."""

from __future__ import annotations

import importlib.util
import sys
import warnings
from fractions import Fraction
from pathlib import Path

import pytest

from src.homology.carrier import Carrier
from src.homology.errors import DimensionMismatchError, NonZeroCompositionError, require_composition_zero
from src.homology.exact_carrier import triangle_betti, triangle_carrier
from src.homology.witness import HomologyWitness
from src.linear_algebra import ExactMatrix

_MODULE_PATH = Path(__file__).resolve().parents[1] / "src" / "homology" / "witness.py"


def _triangle() -> Carrier:
    delta0 = ExactMatrix.from_rows(
        [
            [Fraction(-1), Fraction(1), Fraction(0)],
            [Fraction(-1), Fraction(0), Fraction(1)],
            [Fraction(0), Fraction(-1), Fraction(1)],
        ]
    )
    delta1 = ExactMatrix.from_rows([[Fraction(1), Fraction(-1), Fraction(1)]])
    return Carrier(3, 3, 1, delta0, delta1)


def test_triangle_witness_matches_rank_nullity() -> None:
    carrier = _triangle()
    witness = HomologyWitness.from_carrier(carrier)
    assert witness.is_valid is True
    assert witness.dim_h1 == 0
    assert witness.dim_q1 == 1
    assert witness.carrier_hash == carrier.sha256()
    assert witness.dim_h1 == carrier.dim_h1()


def test_negative_witness_failures() -> None:
    floated = _triangle()
    floated.d0.data[0] = 1.0
    with pytest.raises(DimensionMismatchError, match="float refused") as float_error:
        HomologyWitness.from_carrier(floated)
    assert float_error.value.parameters["role"] == "d0[0]"

    boolean = _triangle()
    boolean.d1.data[0] = True
    with pytest.raises(DimensionMismatchError, match="boolean refused where a rational") as bool_error:
        HomologyWitness.from_carrier(boolean)
    assert bool_error.value.parameters["role"] == "d1[0]"

    flagged = _triangle()
    flagged.dim0 = True
    with pytest.raises(DimensionMismatchError, match="boolean refused where a dimension") as dim_bool:
        HomologyWitness.from_carrier(flagged)
    assert dim_bool.value.parameters["role"] == "dim0"

    with pytest.raises(DimensionMismatchError, match="expects a carrier") as bare:
        HomologyWitness.from_carrier("carrier")
    assert bare.value.parameters["received"] == "str"

    opened = _triangle()
    opened.d1.data[0] = Fraction(0)
    with pytest.raises(NonZeroCompositionError, match="do not compose to zero") as opened_error:
        HomologyWitness.from_carrier(opened)
    assert opened_error.value.parameters["defect"] == "2"

    reshaped = _triangle()
    reshaped.d0 = ExactMatrix.zeros(1, 1)
    with pytest.raises(DimensionMismatchError, match="shape does not match") as shape:
        HomologyWitness.from_carrier(reshaped)
    assert shape.value.parameters["role"] == "d0"


def test_integration_with_triangle_betti_and_composition() -> None:
    carrier = triangle_carrier()
    witness = HomologyWitness.from_carrier(carrier)
    rows0 = [carrier.d0.row(index) for index in range(carrier.d0.rows)]
    rows1 = [carrier.d1.row(index) for index in range(carrier.d1.rows)]
    assert require_composition_zero(rows1, rows0) == Fraction(0)
    _rank0, _rank1, betti = triangle_betti()
    assert witness.dim_h1 == betti
    assert witness.dim_q1 == carrier.dim_q1()


def test_end_to_end_public_contract() -> None:
    carrier = triangle_carrier()
    witness = HomologyWitness.from_carrier(carrier)
    assert witness.is_valid is True
    assert witness.carrier_hash == carrier.sha256()
    assert triangle_betti() == (2, 1, 0)
    tampered = triangle_carrier()
    tampered.d0.data[0] = 0.5
    with pytest.raises(DimensionMismatchError, match="float refused"):
        HomologyWitness.from_carrier(tampered)


def test_origin_resolves_in_repo() -> None:
    root = Path(__file__).resolve().parents[3]
    lean = (root / "lean4" / "FiniteCochain.lean").read_text(encoding="utf-8")
    assert "theorem d1_d0_zero" in lean
    source = _MODULE_PATH.read_text(encoding="utf-8")
    assert "AuthorityEffect: None" in source
    assert "urn:omega:fqm:homology:witness-rank-nullity:v1" in source
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
    (
        "defect shifted by one",
        'defect += abs(_rational(entry, f"product[{index}]"))',
        'defect += abs(_rational(entry, f"product[{index}]")) + 1',
    ),
    (
        "homology dimension shifted by one",
        "return (dim1 - rank1) - rank0",
        "return (dim1 - rank1) - rank0 + 1",
    ),
    (
        "digest separator changed",
        'f"{dim0},{dim1},{dim2}:"',
        'f"{dim0};{dim1};{dim2}:"',
    ),
    ("validity flag forced false", "is_valid=True", "is_valid=False"),
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


def _triangle_carrier(namespace: dict[str, object]) -> Carrier:
    carrier_type = namespace["Carrier"]
    matrix_type = namespace["ExactMatrix"]
    factory = getattr(matrix_type, "from_rows", None)
    if not isinstance(carrier_type, type) or not callable(factory):
        raise RuntimeError("triangle carrier is not constructible")
    delta0 = factory(
        [
            [Fraction(-1), Fraction(1), Fraction(0)],
            [Fraction(-1), Fraction(0), Fraction(1)],
            [Fraction(0), Fraction(-1), Fraction(1)],
        ]
    )
    delta1 = factory([[Fraction(1), Fraction(-1), Fraction(1)]])
    built = carrier_type(3, 3, 1, delta0, delta1)
    if not isinstance(built, Carrier):
        raise RuntimeError("triangle carrier was not a Carrier")
    return built


def _known_values_hold(namespace: dict[str, object], error: type[BaseException]) -> bool:
    witness_type = namespace["HomologyWitness"]
    factory = getattr(witness_type, "from_carrier", None)
    if not isinstance(witness_type, type) or not callable(factory):
        return False
    try:
        carrier = _triangle_carrier(namespace)
        witness = factory(carrier)
    except error:
        return False
    if witness.is_valid is not True or witness.dim_h1 != 0 or witness.dim_q1 != 1:
        return False
    if witness.carrier_hash != carrier.sha256():
        return False
    return True


def _bad_values_refused(namespace: dict[str, object]) -> bool:
    mismatch = namespace["DimensionMismatchError"]
    nonzero = namespace["NonZeroCompositionError"]
    witness_type = namespace["HomologyWitness"]
    factory = getattr(witness_type, "from_carrier", None)
    if not isinstance(mismatch, type) or not isinstance(nonzero, type) or not callable(factory):
        return False
    floated = _triangle_carrier(namespace)
    floated.d0.data[0] = 1.0
    boolean = _triangle_carrier(namespace)
    boolean.d1.data[0] = True
    flagged = _triangle_carrier(namespace)
    flagged.dim0 = True
    opened = _triangle_carrier(namespace)
    opened.d1.data[0] = Fraction(0)
    expected = (
        (mismatch, lambda: factory(floated), "float refused at the public boundary"),
        (mismatch, lambda: factory(boolean), "boolean refused where a rational was required"),
        (mismatch, lambda: factory(flagged), "boolean refused where a dimension was required"),
        (mismatch, lambda: factory("carrier"), "witness expects a carrier"),
        (nonzero, lambda: factory(opened), "witness coboundaries do not compose to zero"),
    )
    for error, probe, invariant in expected:
        if _invariant(error, probe) != invariant:
            return False
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
        loaded.append("mutant_witness_baseline")
        baseline = _load_source(source, loaded[-1])
        assert _oracle(baseline) is True
        killed = 0
        for index, (name, old, new) in enumerate(_MUTANTS):
            count = source.count(old)
            assert count == 1, f"{name} matched {count} sites"
            module_name = f"mutant_witness_{index}"
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
