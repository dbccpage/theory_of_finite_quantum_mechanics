"""Unit, negative, integration, end-to-end, and mutation tests for the purity expression gap.

Origin: code/python/src/qm/entropy_solver.py
Claim: urn:omega:fqm:entropy:purity-expression-gap:v1
AuthorityEffect: None
Mutation-Kills: 9 non-equivalent
"""





from __future__ import annotations

import importlib.util
import io
import sys
import warnings
from contextlib import redirect_stdout
from fractions import Fraction
from pathlib import Path

import pytest

from src.bin.entropy_cli import collision_probability as cli_collision
from src.qm.entropy_solver import EntropySolverError, certified_purity, main, purity_gap

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


_MODULE_PATH = Path(__file__).resolve().parents[1] / "src" / "qm" / "entropy_solver.py"
_FIXTURE = (Fraction(1, 2), Fraction(1, 3), Fraction(1, 6))


def test_fixture_and_integer_purity() -> None:
    assert purity_gap(_FIXTURE) == Fraction(7, 18)
    assert purity_gap((1,)) == Fraction(1)
    assert purity_gap((1, 0)) == Fraction(1)
    assert purity_gap((Fraction(1, 2), Fraction(1, 2))) == Fraction(1, 2)
    assert purity_gap((2, 3, 5)) == Fraction(19, 50)
    assert certified_purity() == Fraction(7, 18)
    assert type(purity_gap((1,))) is Fraction


def test_negative_type_failures() -> None:
    with pytest.raises(EntropySolverError, match="float refused") as floated:
        purity_gap((_probe("1.0"), 0))
    assert floated.value.invariant == "float refused at the purity boundary"
    assert floated.value.parameters["index"] == 0
    assert type(floated.value) is EntropySolverError

    with pytest.raises(EntropySolverError, match="boolean refused") as boolean:
        purity_gap((True,))
    assert boolean.value.invariant == "boolean refused where a rational weight was required"

    with pytest.raises(EntropySolverError, match="negative") as negative:
        purity_gap((Fraction(-1, 2), Fraction(1, 2)))
    assert negative.value.parameters["received"] == "-1/2"

    with pytest.raises(EntropySolverError, match="not an exact rational") as text:
        purity_gap(("1",))
    assert text.value.parameters["received"] == "str"


def test_negative_shape_failures() -> None:
    with pytest.raises(EntropySolverError, match="not a tuple") as listed:
        purity_gap([1, 0])
    assert listed.value.parameters["received"] == "list"

    with pytest.raises(EntropySolverError, match="empty"):
        purity_gap(())

    with pytest.raises(EntropySolverError, match="zero mass") as mass:
        purity_gap((0, 0))
    assert mass.value.parameters["total"] == "0"

    with pytest.raises(EntropySolverError, match="zero mass") as single:
        purity_gap((0,))
    assert single.value.parameters["total"] == "0"

    with pytest.raises(EntropySolverError, match="not a tuple"):
        purity_gap("10")


def test_integration_matches_diagonal_purity() -> None:
    root = Path(__file__).resolve().parents[3]
    source = (root / "lean4" / "DerivationDagQMClosure.lean").read_text(encoding="utf-8")
    assert "def purityDiag3" in source
    assert "theorem qm020_thm4_hilbert_lift_redundancy" in source
    w0, w1, w2 = 2, 3, 5
    diagonal = w0 * w0 + w1 * w1 + w2 * w2
    expanded = diagonal + 2 * (w0 * w1 + w1 * w2 + w2 * w0)
    mass = w0 + w1 + w2
    assert diagonal == 38
    assert expanded == mass * mass
    assert diagonal < expanded
    normalized = (Fraction(w0, mass), Fraction(w1, mass), Fraction(w2, mass))
    assert purity_gap((w0, w1, w2)) == Fraction(diagonal, mass * mass)
    assert purity_gap((w0, w1, w2)) == cli_collision(normalized)


def test_end_to_end_cli_prints_seven_eighteenths() -> None:
    buffer = io.StringIO()
    with redirect_stdout(buffer):
        code = main()
    assert code == 0
    assert buffer.getvalue().strip() == "7/18"
    assert certified_purity() == Fraction(7, 18)


def test_origin_resolves_in_repo() -> None:
    root = Path(__file__).resolve().parents[3]
    source = (root / "lean4" / "DerivationDagQMClosure.lean").read_text(encoding="utf-8")
    assert "def purityDiag3" in source
    assert "theorem qm020_thm4_hilbert_lift_redundancy" in source
    text = _MODULE_PATH.read_text(encoding="utf-8")
    assert "AuthorityEffect: None" in text
    assert "urn:omega:fqm:entropy:purity-expression-gap:v1" in text
    assert "Scope Fence:" in text


_MUTANTS: tuple[tuple[str, str, str], ...] = (
    (
        "float weight admitted",
        "if isinstance(value, float):",
        "if isinstance(value, float):\n        return Fraction(0)\n    if False:",
    ),
    (
        "boolean weight admitted",
        "if type(value) is bool:",
        "if type(value) is bool:\n        return Fraction(1)\n    if False:",
    ),
    ("negative weight admitted", "if weight < 0:", "if weight < -1:"),
    ("empty vector admitted", "len(weights) == 0", "len(weights) == -1"),
    ("tuple check inverted", "not isinstance(weights, tuple)", "isinstance(weights, tuple)"),
    ("square replaced by the weight", "return weight * weight", "return weight"),
    ("normalized square replaced by the weight", "total += scaled * scaled", "total += scaled"),
    ("mass check inverted", "if total == 0:", "if total != 0:"),
    ("gap check inverted", "if gap != 0:", "if gap == 0:"),
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
    purity = namespace["purity_gap"]
    certified = namespace["certified_purity"]
    if not _all_hold((callable(purity), callable(certified),)):
        return False
    try:
        fixture = purity(_FIXTURE)
        point = purity((1,))
        pure = purity((1, 0))
        fair = purity((Fraction(1, 2), Fraction(1, 2)))
        weights = purity((2, 3, 5))
        signed = certified()
    except error:
        return False
    actual = (fixture, point, pure, fair, weights, signed)
    expected = (
        Fraction(7, 18),
        Fraction(1),
        Fraction(1),
        Fraction(1, 2),
        Fraction(19, 50),
        Fraction(7, 18),
    )
    return actual == expected


def _bad_values_refused(namespace: dict[str, object], error: type[BaseException]) -> bool:
    purity = namespace["purity_gap"]
    if not callable(purity):
        return False
    probes = (
        (lambda: purity((_probe("1.0"), 0)), "float refused at the purity boundary"),
        (lambda: purity((True,)), "boolean refused where a rational weight was required"),
        (lambda: purity((-1, 2)), "purity weight is negative"),
        (lambda: purity(()), "purity weights are empty"),
        (lambda: purity((0, 0)), "purity weights have zero mass"),
        (lambda: purity([1, 0]), "purity weights are not a tuple"),
        (lambda: purity(("1",)), "purity weight is not an exact rational"),
    )
    for probe, invariant in probes:
        if _invariant(error, probe) != invariant:
            return False
    return True


def _oracle(namespace: dict[str, object]) -> bool:
    error_type = namespace["EntropySolverError"]
    if not _all_hold((isinstance(error_type, type), issubclass(error_type, BaseException),)):
        return False
    if not _known_values_hold(namespace, error_type):
        return False
    return _bad_values_refused(namespace, error_type)


def test_mutation_suite_kills_non_equivalent_mutants() -> None:
    source = _MODULE_PATH.read_text(encoding="utf-8")
    loaded: list[str] = []
    try:
        loaded.append("mutant_entropy_solver_baseline")
        baseline = _load_source(source, loaded[-1])
        assert _oracle(baseline) is True
        killed = 0
        for index, (name, old, new) in enumerate(_MUTANTS):
            count = source.count(old)
            assert count == 1, f"{name} matched {count} sites"
            module_name = f"mutant_entropy_solver_{index}"
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
