"""Unit, negative, integration, end-to-end, and mutation tests for the price cycle."""

from __future__ import annotations

import importlib.util
import io
import sys
import warnings
from contextlib import redirect_stdout
from fractions import Fraction
from pathlib import Path

import pytest

from src.qm.causal_prices import CausalPriceError, additive_holonomy, certified_cycle, cycle_price_defect, main
from src.qm.obstruction_calc import face_obstruction

_MODULE_PATH = Path(__file__).resolve().parents[1] / "src" / "qm" / "causal_prices.py"
_FIXTURE = (Fraction(1), Fraction(2, 3), Fraction(4, 5))


def test_closed_cycle_defect_is_zero() -> None:
    assert cycle_price_defect() == Fraction(0)
    assert cycle_price_defect(_FIXTURE) == Fraction(0)
    assert cycle_price_defect((2, 3)) == Fraction(0)
    assert cycle_price_defect((5,)) == Fraction(0)
    assert additive_holonomy(_FIXTURE) == Fraction(0)
    assert additive_holonomy((2, 3)) == Fraction(0)
    assert certified_cycle() == Fraction(0)
    assert type(cycle_price_defect((2, 3))) is Fraction


def test_negative_type_failures() -> None:
    with pytest.raises(CausalPriceError, match="float refused") as floated:
        cycle_price_defect((1.0, 2))
    assert floated.value.invariant == "float refused at the price boundary"
    assert floated.value.parameters["index"] == 0
    assert type(floated.value) is CausalPriceError

    with pytest.raises(CausalPriceError, match="boolean refused") as boolean:
        cycle_price_defect((True, 2))
    assert boolean.value.invariant == "boolean refused where a rational price was required"

    with pytest.raises(CausalPriceError, match="not an exact rational") as text:
        cycle_price_defect(("1", 2))
    assert text.value.parameters["received"] == "str"


def test_negative_shape_failures() -> None:
    with pytest.raises(CausalPriceError, match="prices are empty") as empty:
        cycle_price_defect(())
    assert empty.value.invariant == "prices are empty"

    with pytest.raises(CausalPriceError, match="not positive") as negative:
        cycle_price_defect((Fraction(-1), Fraction(2)))
    assert negative.value.parameters["received"] == "-1"

    with pytest.raises(CausalPriceError, match="not positive") as zero:
        additive_holonomy((0, 1))
    assert zero.value.parameters["index"] == 0

    with pytest.raises(CausalPriceError, match="not a tuple") as listed:
        cycle_price_defect([1, 2])
    assert listed.value.parameters["received"] == "list"


def test_integration_matches_triangle_holonomy() -> None:
    root = Path(__file__).resolve().parents[3]
    source = (root / "lean4" / "CoboundaryHolonomy.lean").read_text(encoding="utf-8")
    assert "theorem coboundary_closed_cycle_zero" in source
    assert "theorem coboundary_vertex_path_telescoping" in source
    assert "def coboundary" in source
    holonomy = additive_holonomy(_FIXTURE)
    face = face_obstruction(_FIXTURE)
    assert holonomy == Fraction(0)
    assert face == Fraction(0)
    assert holonomy == face
    assert cycle_price_defect(_FIXTURE) == Fraction(0)


def test_end_to_end_cli_prints_zero() -> None:
    buffer = io.StringIO()
    with redirect_stdout(buffer):
        code = main()
    assert code == 0
    assert buffer.getvalue().strip() == "0"
    assert certified_cycle() == Fraction(0)


def test_origin_resolves_in_repo() -> None:
    root = Path(__file__).resolve().parents[3]
    source = (root / "lean4" / "CoboundaryHolonomy.lean").read_text(encoding="utf-8")
    assert "theorem coboundary_closed_cycle_zero" in source
    text = _MODULE_PATH.read_text(encoding="utf-8")
    assert "AuthorityEffect: None" in text
    assert "urn:omega:fqm:price:cycle-defect:v1" in text
    assert "Scope Fence:" in text


_MUTANTS: tuple[tuple[str, str, str], ...] = (
    (
        "float price admitted",
        "if isinstance(value, float):",
        "if False and isinstance(value, float):",
    ),
    (
        "boolean price admitted",
        "if type(value) is bool:",
        "if False and type(value) is bool:",
    ),
    ("tuple check inverted", "not isinstance(prices, tuple)", "isinstance(prices, tuple)"),
    ("empty check dropped", "len(prices) == 0", "len(prices) == -1"),
    ("nonpositive price admitted", "if price <= 0:", "if price < -1:"),
    ("ratio keeps only the next price", "return nxt / current", "return nxt"),
    ("closing ratio keeps the first price", "return prices[0] / prices[0]", "return prices[0]"),
    ("difference keeps only the next price", "return nxt - current", "return nxt"),
)


def _load_source(source: str, name: str) -> dict[str, object]:
    spec = importlib.util.spec_from_loader(name, loader=None)
    if spec is None:
        raise RuntimeError("could not allocate a mutant module spec")
    module = importlib.util.module_from_spec(spec)
    module.__package__ = "src.qm"
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
    defect = namespace["cycle_price_defect"]
    holonomy = namespace["additive_holonomy"]
    certified = namespace["certified_cycle"]
    if not callable(defect) or not callable(holonomy) or not callable(certified):
        return False
    try:
        values = (
            defect(),
            defect(_FIXTURE),
            defect((2, 3)),
            defect((5,)),
            holonomy(_FIXTURE),
            holonomy((2, 3)),
            certified(),
        )
    except error:
        return False
    return values == (Fraction(0), Fraction(0), Fraction(0), Fraction(0), Fraction(0), Fraction(0), Fraction(0))


def _bad_values_refused(namespace: dict[str, object], error: type[BaseException]) -> bool:
    defect = namespace["cycle_price_defect"]
    if not callable(defect):
        return False
    probes = (
        (lambda: defect((1.0, 2)), "float refused at the price boundary"),
        (lambda: defect((True, 2)), "boolean refused where a rational price was required"),
        (lambda: defect(("1", 2)), "price is not an exact rational"),
        (lambda: defect(()), "prices are empty"),
        (lambda: defect((Fraction(-1), Fraction(2))), "price is not positive"),
        (lambda: defect((0, 1)), "price is not positive"),
        (lambda: defect([1, 2]), "prices are not a tuple"),
    )
    for probe, invariant in probes:
        if _invariant(error, probe) != invariant:
            return False
    return True


def _oracle(namespace: dict[str, object]) -> bool:
    error_type = namespace["CausalPriceError"]
    if not isinstance(error_type, type) or not issubclass(error_type, BaseException):
        return False
    if not _known_values_hold(namespace, error_type):
        return False
    return _bad_values_refused(namespace, error_type)


def test_mutation_suite_kills_non_equivalent_mutants() -> None:
    source = _MODULE_PATH.read_text(encoding="utf-8")
    loaded: list[str] = []
    try:
        loaded.append("mutant_causal_prices_baseline")
        baseline = _load_source(source, loaded[-1])
        assert _oracle(baseline) is True
        killed = 0
        for index, (name, old, new) in enumerate(_MUTANTS):
            count = source.count(old)
            assert count == 1, f"{name} matched {count} sites"
            module_name = f"mutant_causal_prices_{index}"
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
