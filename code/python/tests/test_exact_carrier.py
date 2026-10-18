"""Unit, negative, integration, end-to-end, and mutation tests for the triangle carrier.

Origin: code/python/src/homology/exact_carrier.py
Claim: urn:omega:fqm:homology:filled-triangle-betti:v1
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

from src.homology import exported_triangle_rank_sum
from src.homology.carrier import Carrier
from src.homology.coboundary import triangle_coboundaries
from src.homology.errors import DimensionMismatchError, require_composition_zero
from src.homology.exact_carrier import (
    ExactCarrier,
    require_triangle_betti,
    triangle_betti,
    triangle_carrier,
)
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


_MODULE_PATH = Path(__file__).resolve().parents[1] / "src" / "homology" / "exact_carrier.py"


def test_filled_triangle_betti_is_two_one_zero() -> None:
    carrier = triangle_carrier()
    assert ExactCarrier is Carrier
    assert carrier.dimensions() == (3, 3, 1)
    assert triangle_betti() == (2, 1, 0)
    assert require_triangle_betti(carrier) == (carrier.rank_d0(), carrier.rank_d1(), carrier.dim_h1())


def test_negative_triangle_betti_failures() -> None:
    floated = triangle_carrier()
    floated.d0.data[0] = _probe("1.0")
    with pytest.raises(DimensionMismatchError, match="float refused") as float_error:
        require_triangle_betti(floated)
    assert float_error.value.parameters["role"] == "d0[0]"

    boolean = triangle_carrier()
    boolean.d1.data[0] = True
    with pytest.raises(DimensionMismatchError, match="boolean refused") as bool_error:
        require_triangle_betti(boolean)
    assert bool_error.value.parameters["role"] == "d1[0]"

    with pytest.raises(DimensionMismatchError, match="expects a carrier") as bare:
        require_triangle_betti("triangle")
    assert bare.value.parameters["received"] == "str"

    small = Carrier(1, 1, 1, ExactMatrix.zeros(1, 1), ExactMatrix.zeros(1, 1))
    with pytest.raises(DimensionMismatchError, match="dimensions are not") as shape:
        require_triangle_betti(small)
    assert shape.value.parameters["dim0"] == 1

    hollow = Carrier(3, 3, 1, ExactMatrix.zeros(3, 3), ExactMatrix.zeros(1, 3))
    with pytest.raises(DimensionMismatchError, match="not \\(2, 1, 0\\)") as opened:
        require_triangle_betti(hollow)
    assert opened.value.parameters["rank0"] == 0
    assert opened.value.parameters["rank1"] == 0
    assert opened.value.parameters["betti"] == 3


def test_integration_with_coboundary_and_composition() -> None:
    delta0, delta1 = triangle_coboundaries()
    carrier = triangle_carrier()
    assert list(carrier.d0.data) == list(delta0.data)
    assert list(carrier.d1.data) == list(delta1.data)
    rows0 = [delta0.row(index) for index in range(delta0.rows)]
    rows1 = [delta1.row(index) for index in range(delta1.rows)]
    assert require_composition_zero(rows1, rows0) == Fraction(0)
    assert carrier.dim_h1() == 0


def test_end_to_end_public_contract() -> None:
    assert triangle_betti() == (2, 1, 0)
    assert exported_triangle_rank_sum() == 4
    tampered = triangle_carrier()
    tampered.d0.data[0] = _probe("0.5")
    with pytest.raises(DimensionMismatchError, match="float refused"):
        require_triangle_betti(tampered)


def test_origin_resolves_in_repo() -> None:
    root = Path(__file__).resolve().parents[3]
    lean = (root / "lean4" / "FiniteCochain.lean").read_text(encoding="utf-8")
    assert "theorem d1_d0_zero" in lean
    source = _MODULE_PATH.read_text(encoding="utf-8")
    assert "AuthorityEffect: None" in source
    assert "urn:omega:fqm:homology:filled-triangle-betti:v1" in source
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
    (
        "Betti check inverted",
        "if rank0 != 2 or rank1 != 1 or betti != 0:",
        "if rank0 == 2 and rank1 == 1 and betti == 0:",
    ),
    ("rank d0 threshold shifted", "rank0 != 2", "rank0 != 3"),
    ("rank d1 threshold shifted", "rank1 != 1", "rank1 != 0"),
    ("Betti threshold shifted", "betti != 0", "betti != 1"),
    (
        "carrier dimensions swapped",
        "return Carrier(3, 3, 1, delta0, delta1)",
        "return Carrier(1, 3, 3, delta0, delta1)",
    ),
    (
        "d0 entries not rechecked",
        '_rational(entry, f"d0[{index}]")',
        "entry",
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


def _known_values_hold(namespace: dict[str, object], error: type[BaseException]) -> bool:
    betti_fn = namespace["triangle_betti"]
    carrier_fn = namespace["triangle_carrier"]
    require = namespace["require_triangle_betti"]
    alias = namespace["ExactCarrier"]
    carrier_type = namespace["Carrier"]
    if not _all_hold((callable(betti_fn), callable(carrier_fn), callable(require),)):
        return False
    if alias is not carrier_type:
        return False
    try:
        triple = betti_fn()
        carrier = carrier_fn()
        checked = require(carrier)
    except error:
        return False
    if triple != (2, 1, 0) or checked != (2, 1, 0):
        return False
    if carrier.rank_d0() != 2 or carrier.rank_d1() != 1 or carrier.dim_h1() != 0:
        return False
    return True


def _bad_values_refused(namespace: dict[str, object]) -> bool:
    mismatch = namespace["DimensionMismatchError"]
    require = namespace["require_triangle_betti"]
    carrier_fn = namespace["triangle_carrier"]
    carrier_type = namespace["Carrier"]
    if not _all_hold((isinstance(mismatch, type), callable(require), callable(carrier_fn),)):
        return False
    if not isinstance(carrier_type, type):
        return False
    floated = carrier_fn()
    floated.d0.data[0] = _probe("1.0")
    boolean = carrier_fn()
    boolean.d1.data[0] = True
    hollow = carrier_type(3, 3, 1, ExactMatrix.zeros(3, 3), ExactMatrix.zeros(1, 3))
    small = carrier_type(1, 1, 1, ExactMatrix.zeros(1, 1), ExactMatrix.zeros(1, 1))
    expected = (
        (mismatch, lambda: require(floated), "float refused at the public boundary"),
        (mismatch, lambda: require(boolean), "boolean refused where a rational was required"),
        (mismatch, lambda: require("triangle"), "triangle Betti expects a carrier"),
        (mismatch, lambda: require(small), "triangle carrier dimensions are not (3, 3, 1)"),
        (mismatch, lambda: require(hollow), "triangle Betti triple is not (2, 1, 0)"),
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
        loaded.append("mutant_exact_carrier_baseline")
        baseline = _load_source(source, loaded[-1])
        assert _oracle(baseline) is True
        killed = 0
        for index, (name, old, new) in enumerate(_MUTANTS):
            count = source.count(old)
            assert count == 1, f"{name} matched {count} sites"
            module_name = f"mutant_exact_carrier_{index}"
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
