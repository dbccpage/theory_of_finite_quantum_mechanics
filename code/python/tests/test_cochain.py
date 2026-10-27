"""Unit, negative, integration, end-to-end, and mutation tests for the cochain pairing.

Origin: code/python/src/homology/cochain.py
Claim: urn:omega:fqm:homology:triangle-cochain-pairing:v1
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

from src.homology.chain import Chain
from src.homology.cochain import Cochain, coboundary_square, coboundary_values, pairing
from src.homology.coboundary import triangle_coboundary_defect
from src.homology.errors import DimensionMismatchError

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


_MODULE_PATH = Path(__file__).resolve().parents[1] / "src" / "homology" / "cochain.py"
_EDGE = [Fraction(-1), Fraction(-1), Fraction(0)]
_FACE = [Fraction(0)]


def test_pairing_is_additive_and_square_vanishes() -> None:
    left = Cochain(1, (Fraction(2), Fraction(0)))
    right = Cochain(1, (Fraction(0), Fraction(5)))
    summed = Cochain(1, (Fraction(2), Fraction(5)))
    chain = Chain(1, (Fraction(3), Fraction(4)))
    assert pairing(left, chain) + pairing(right, chain) == pairing(summed, chain)
    first = Chain(1, (Fraction(3), Fraction(0)))
    second = Chain(1, (Fraction(0), Fraction(4)))
    assert pairing(summed, first) + pairing(summed, second) == pairing(summed, chain)
    assert pairing(Cochain(1, (Fraction(2),)), Chain(1, (Fraction(3),))) == Fraction(6)
    assert Cochain(0, (Fraction(1), Fraction(1))).total() == Fraction(2)
    assert coboundary_values((1, 0, 0)) == _EDGE
    assert coboundary_square((1, 0, 0)) == _FACE


def test_negative_cochain_failures() -> None:
    with pytest.raises(DimensionMismatchError, match="float refused") as floated:
        coboundary_values((_probe("1.0"), 0, 0))
    assert floated.value.parameters["role"] == "vertex[0]"

    with pytest.raises(DimensionMismatchError, match="boolean refused") as boolean:
        coboundary_values(cast(tuple[object, ...], (True, 0, 0)))
    assert boolean.value.parameters["role"] == "vertex[0]"

    with pytest.raises(DimensionMismatchError, match="not an exact rational") as text:
        coboundary_values(("1", 0, 0))
    assert text.value.parameters["received"] == "str"

    with pytest.raises(DimensionMismatchError, match="must be a sequence") as raw:
        coboundary_values("123")
    assert raw.value.parameters["received"] == "str"

    with pytest.raises(DimensionMismatchError, match="length 3") as length:
        coboundary_values((1, 0))
    assert length.value.parameters["length"] == 2

    with pytest.raises(DimensionMismatchError, match="nonnegative int") as dim:
        Cochain(cast(int, True), ())
    assert dim.value.parameters["received"] == "bool"

    with pytest.raises(DimensionMismatchError, match="nonnegative int") as negative:
        Cochain(-1, ())
    assert negative.value.parameters["received"] == "int"

    with pytest.raises(DimensionMismatchError, match="dimensions differ") as dimensions:
        pairing(Cochain(0, (Fraction(1),)), Chain(1, (Fraction(1),)))
    assert dimensions.value.parameters["cochain_dim"] == 0

    with pytest.raises(DimensionMismatchError, match="lengths differ") as lengths:
        pairing(Cochain(1, (Fraction(1),)), Chain(1, (Fraction(1), Fraction(0))))
    assert lengths.value.parameters["cochain_length"] == 1


def test_integration_with_coboundary_neighbor() -> None:
    assert triangle_coboundary_defect() == Fraction(0)
    assert coboundary_square((1, -1, 1)) == _FACE
    assert pairing(Cochain(1, (Fraction(1), Fraction(0), Fraction(0))), Chain(1, (Fraction(1), Fraction(-1), Fraction(1)))) == Fraction(1)


def test_end_to_end_public_contract() -> None:
    assert coboundary_square((Fraction(1, 2), 0, Fraction(-3, 2))) == _FACE
    with pytest.raises(DimensionMismatchError, match="float refused") as caught:
        Cochain(0, cast(tuple[Fraction, ...], (_probe("0.5"),)))
    assert caught.value.parameters["role"] == "coeff[0]"


def test_origin_resolves_in_repo() -> None:
    root = Path(__file__).resolve().parents[3]
    lean = (root / "lean4" / "TriangleNetworkComplexCarrier.lean").read_text(encoding="utf-8")
    assert "theorem eval_pairing_left_additive" in lean
    assert "theorem eval_pairing_right_additive" in lean
    source = _MODULE_PATH.read_text(encoding="utf-8")
    assert "AuthorityEffect: None" in source
    assert "urn:omega:fqm:homology:triangle-cochain-pairing:v1" in source
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
    ("length check inverted", "if len(parsed) != delta0.cols:", "if len(parsed) == delta0.cols:"),
    ("pairing product negated", "total += alpha * coeff", "total -= alpha * coeff"),
    ("negative dimension accepted", "or dim < 0:", "or dim < -1:"),
    ("string accepted as coefficients", "isinstance(values, (str, bytes)) or ", ""),
    ("dimension check inverted", "if cochain.dim != chain.dim:", "if cochain.dim == chain.dim:"),
    ("coefficient total subtracted", "total += coeff", "total -= coeff"),
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
    cochain = namespace["Cochain"]
    chain = namespace["Chain"]
    pair = namespace["pairing"]
    values = namespace["coboundary_values"]
    square = namespace["coboundary_square"]
    if not _all_hold((isinstance(cochain, type), isinstance(chain, type),)):
        return False
    if not _all_hold((callable(pair), callable(values), callable(square),)):
        return False
    try:
        paired = pair(cochain(1, (2,)), chain(1, (3,)))
        total = cochain(0, (1, 1)).total()
        image = values((1, 0, 0))
        face = square((1, 0, 0))
    except error:
        return False
    if paired != Fraction(6) or total != Fraction(2):
        return False
    image_ok = image == _EDGE
    face_ok = face == _FACE
    if image_ok is True and face_ok is True:
        return True
    return False


def _bad_values_refused(namespace: dict[str, object], error: type[BaseException]) -> bool:
    cochain = namespace["Cochain"]
    chain = namespace["Chain"]
    pair = namespace["pairing"]
    values = namespace["coboundary_values"]
    if not _all_hold((isinstance(cochain, type), isinstance(chain, type), callable(pair), callable(values),)):
        return False
    expected = (
        (lambda: values((_probe("1.0"), 0, 0)), "float refused at the public boundary"),
        (lambda: values((True, 0, 0)), "boolean refused where a rational was required"),
        (lambda: values("123"), "coefficients must be a sequence"),
        (lambda: values((1, 0)), "triangle 0-cochain has length 3"),
        (lambda: cochain(-1, ()), "cochain dimension must be a nonnegative int"),
        (lambda: pair(cochain(0, (1,)), chain(1, (1,))), "cochain and chain dimensions differ"),
    )
    for probe, invariant in expected:
        if _invariant(error, probe) != invariant:
            return False
    return True


def _oracle(namespace: dict[str, object]) -> bool:
    error_type = namespace["DimensionMismatchError"]
    if not _all_hold((isinstance(error_type, type), issubclass(error_type, BaseException),)):
        return False
    if not _known_values_hold(namespace, error_type):
        return False
    return _bad_values_refused(namespace, error_type)


def test_mutation_suite_kills_non_equivalent_mutants() -> None:
    source = _MODULE_PATH.read_text(encoding="utf-8")
    loaded: list[str] = []
    try:
        loaded.append("mutant_cochain_baseline")
        baseline = _load_source(source, loaded[-1])
        assert _oracle(baseline) is True
        killed = 0
        for index, (name, old, new) in enumerate(_MUTANTS):
            count = source.count(old)
            assert count == 1, f"{name} matched {count} sites"
            module_name = f"mutant_cochain_{index}"
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
