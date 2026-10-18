"""Unit, negative, integration, end-to-end, and mutation tests for the cross-sign certificate.

Origin: code/python/src/linear_algebra/ordered.py
Claim: urn:omega:fqm:h001:cross-sign-certificate:v1
AuthorityEffect: None
Mutation-Kills: 9 non-equivalent
"""



from __future__ import annotations

import importlib.util
import sys
import warnings
from fractions import Fraction
from pathlib import Path

import pytest

from src.linear_algebra.ordered import (
    OrderError,
    certify_cross_sign,
    compare,
    cross_sign,
    require_nondecreasing,
    sorted_fractions,
    sum_of_squares,
)
from src.linear_algebra.scalars import GaussianRational, q

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


_MODULE_PATH = Path(__file__).resolve().parents[1] / "src" / "linear_algebra" / "ordered.py"


def test_cross_sign_matches_gap() -> None:
    certificate = certify_cross_sign(1, 2, 1, 3)
    assert certificate.gap == Fraction(1, 1)
    assert certificate.sign == 1
    assert certificate.left_denominator == Fraction(2)
    assert cross_sign(1, 2, 1, 3) == 1
    assert compare(Fraction(1, 2), Fraction(1, 3)) == 1
    assert compare(Fraction(1, 3), Fraction(1, 2)) == -1
    assert compare(q(1, 2), q(2, 4)) == 0


def test_negative_denominator_is_normalized() -> None:
    certificate = certify_cross_sign(1, -2, 1, 1)
    assert certificate.left_numerator == Fraction(-1)
    assert certificate.left_denominator == Fraction(2)
    assert certificate.sign == -1
    assert certificate.gap < 0


def test_sum_of_squares_and_sort() -> None:
    witnessed = sum_of_squares([Fraction(1, 2), Fraction(1, 2)])
    assert witnessed == Fraction(1, 2)
    assert witnessed >= 0
    assert sorted_fractions([2, 0, Fraction(-1, 2)]) == [
        Fraction(-1, 2),
        Fraction(0),
        Fraction(2),
    ]
    assert require_nondecreasing([0, 1, 1]) == (Fraction(0), Fraction(1), Fraction(1))


def test_negative_boundary_failures() -> None:
    with pytest.raises(OrderError, match="float refused") as caught:
        cross_sign(_probe("1.0"), 1, 0, 1)
    assert caught.value.parameters["role"] == "left_numerator"
    assert caught.value.invariant == "float refused at the public boundary"

    with pytest.raises(OrderError, match="boolean refused") as caught:
        as_rational_bool()
    assert caught.value.parameters["role"] == "value"

    with pytest.raises(OrderError, match="Q\\(i\\) is outside") as caught:
        compare(GaussianRational(0, 1), 0)
    assert caught.value.invariant == "Q(i) is outside the order of Q"

    with pytest.raises(OrderError, match="nonzero denominator") as caught:
        cross_sign(1, 0, 1, 1)
    assert caught.value.parameters["role"] == "left_denominator"

    with pytest.raises(OrderError, match="length 2") as caught:
        cross_sign((1, 2, 3), 1, 1, 1)
    assert caught.value.parameters["length"] == 3

    with pytest.raises(OrderError, match="not an exact rational") as caught:
        sum_of_squares(["1/2"])
    assert caught.value.parameters["received"] == "str"

    with pytest.raises(OrderError, match="not nondecreasing") as caught:
        require_nondecreasing([2, 1])
    assert caught.value.parameters["index"] == 0
    assert caught.value.parameters["sign"] == 1


def test_negative_pair_and_sequence_failures() -> None:
    with pytest.raises(OrderError, match="boolean refused inside") as caught:
        cross_sign((True, 1), 1, 1, 1)
    assert caught.value.invariant == "boolean refused inside a rational pair"

    with pytest.raises(OrderError, match="exact integers") as caught:
        cross_sign((1, "2"), 1, 1, 1)
    assert caught.value.parameters["denominator_type"] == "str"

    with pytest.raises(OrderError, match="denominator is zero") as caught:
        cross_sign((1, 0), 1, 1, 1)
    assert caught.value.parameters["numerator"] == 1

    with pytest.raises(OrderError, match="finite sequence") as caught:
        sum_of_squares("1/2")
    assert caught.value.parameters["role"] == "squares"
    assert caught.value.parameters["received"] == "str"


def as_rational_bool() -> None:
    from src.linear_algebra.ordered import as_fraction

    as_fraction(True)


def test_integration_with_scalar_neighbor() -> None:
    """Half plus half is one, using the neighboring exact scalar constructor."""
    total = q(1, 2) + q(1, 2)
    certificate = certify_cross_sign(total.numerator, total.denominator, 1, 1)
    assert certificate.gap == 0
    assert certificate.sign == 0
    assert sum_of_squares([q(1, 2), q(1, 2)]) == q(1, 2)


def test_end_to_end_public_contract() -> None:
    assert cross_sign((1, 2), (1, 1), (1, 3), (1, 1)) == 1
    with pytest.raises(OrderError, match="float refused") as caught:
        sorted_fractions([_probe("1.5"), 0])
    assert caught.value.parameters["role"] == "values[0]"


def test_origin_resolves_in_repo() -> None:
    root = Path(__file__).resolve().parents[3]
    lean = (root / "lean4" / "H001Rats.lean").read_text(encoding="utf-8")
    assert "def qrel" in lean
    assert "qrel_equivalence" in lean
    source = _MODULE_PATH.read_text(encoding="utf-8")
    assert "AuthorityEffect: None" in source
    assert "urn:omega:fqm:h001:cross-sign-certificate:v1" in source
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
        "gaussian real part admitted",
        "if isinstance(value, GaussianRational):",
        "if isinstance(value, GaussianRational):\n        return value.real\n    if False:",
    ),
    ("gap sign flipped", " - left_denominator * right_numerator", " + left_denominator * right_numerator"),
    ("zero denominator accepted", "if denominator == 0:", "if denominator != 0:"),
    ("negative denominator not flipped", "return (-numerator, -denominator)", "return (numerator, denominator)"),
    ("squares subtracted", "total += square", "total -= square"),
    (
        "sort comparison inverted",
        "while slot > 0 and compare(ordered[slot - 1], current) > 0:",
        "while slot > 0 and compare(ordered[slot - 1], current) < 0:",
    ),
    ("nondecreasing check inverted", "if sign > 0:", "if sign < 0:"),
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


def _raises(error: type[BaseException], probe: object) -> bool:
    if not callable(probe):
        return False
    try:
        probe()
    except error:
        return True
    return False


def _callables_ready(namespace: dict[str, object]) -> bool:
    names = ("cross_sign", "sum_of_squares", "sorted_fractions", "require_nondecreasing")
    for name in names:
        if not callable(namespace[name]):
            return False
    return True


def _known_values_hold(namespace: dict[str, object], error: type[BaseException]) -> bool:
    cross = namespace["cross_sign"]
    squares = namespace["sum_of_squares"]
    sort = namespace["sorted_fractions"]
    if not _all_hold((callable(cross), callable(squares), callable(sort),)):
        return False
    try:
        if cross(1, 2, 1, 3) != 1 or squares([1, 2]) != Fraction(5):
            return False
        if sort([2, 0, 1]) != [Fraction(0), Fraction(1), Fraction(2)]:
            return False
        if cross(1, -2, 1, 1) != -1:
            return False
    except error:
        return False
    return True


def _bad_values_refused(namespace: dict[str, object], error: type[BaseException]) -> bool:
    cross = namespace["cross_sign"]
    monotone = namespace["require_nondecreasing"]
    gaussian = namespace["GaussianRational"]
    if not _all_hold((callable(cross), callable(monotone), isinstance(gaussian, type),)):
        return False
    probes = (
        lambda: cross(_probe("1.0"), 1, 1, 1),
        lambda: cross(True, 1, 1, 1),
        lambda: cross(gaussian(0, 1), 1, 1, 1),
        lambda: cross(1, 0, 1, 1),
        lambda: monotone([2, 1]),
    )
    for probe in probes:
        if not _raises(error, probe):
            return False
    return True


def _oracle(namespace: dict[str, object]) -> bool:
    error_type = namespace["OrderError"]
    gaussian = namespace["GaussianRational"]
    if not _callables_ready(namespace):
        return False
    if not _all_hold((isinstance(error_type, type), issubclass(error_type, BaseException),)):
        return False
    if not isinstance(gaussian, type):
        return False
    if not _known_values_hold(namespace, error_type):
        return False
    return _bad_values_refused(namespace, error_type)


def test_mutation_suite_kills_non_equivalent_mutants() -> None:
    source = _MODULE_PATH.read_text(encoding="utf-8")
    loaded: list[str] = []
    try:
        loaded.append("mutant_order_baseline")
        baseline = _load_source(source, loaded[-1])
        assert _oracle(baseline) is True
        killed = 0
        for index, (name, old, new) in enumerate(_MUTANTS):
            count = source.count(old)
            assert count == 1, f"{name} matched {count} sites"
            module_name = f"mutant_order_{index}"
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
