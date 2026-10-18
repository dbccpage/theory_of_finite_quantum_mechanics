"""Unit, negative, integration, end-to-end, and mutation tests for the half simplex."""

from __future__ import annotations

import importlib.util
import io
import sys
import warnings
from contextlib import redirect_stdout
from fractions import Fraction
from pathlib import Path

import pytest

from src.finite_probability import scaled_simplex_witness
from src.finite_probability.simplex import (
    ProbabilitySimplex,
    SimplexError,
    half_simplex_mass,
    main,
)

_MODULE_PATH = Path(__file__).resolve().parents[1] / "src" / "finite_probability" / "simplex.py"


def test_half_weights_match_the_theorem() -> None:
    assert half_simplex_mass() == Fraction(1)
    assert ProbabilitySimplex.uniform(2)[0] == Fraction(1, 2)
    assert ProbabilitySimplex.uniform(2)[1] == Fraction(1, 2)
    assert ProbabilitySimplex.dirac(3, 1)[1] == Fraction(1)
    assert type(half_simplex_mass()) is Fraction


def test_negative_type_failures() -> None:
    with pytest.raises(SimplexError, match="float refused") as floated:
        ProbabilitySimplex([0.5, 0.5])
    assert floated.value.invariant == "float refused at the simplex boundary"
    assert floated.value.parameters["role"] == "distribution[0]"
    assert type(floated.value) is SimplexError

    with pytest.raises(SimplexError, match="boolean refused") as boolean:
        ProbabilitySimplex([True, False])
    assert boolean.value.invariant == "boolean refused where an exact rational was required"

    with pytest.raises(SimplexError, match="not an exact rational") as text:
        ProbabilitySimplex(["1/2", Fraction(1, 2)])
    assert text.value.parameters["received"] == "str"


def test_negative_shape_failures() -> None:
    with pytest.raises(SimplexError, match="masses are empty") as empty:
        ProbabilitySimplex([])
    assert empty.value.invariant == "masses are empty"

    with pytest.raises(SimplexError, match="not a sequence") as text:
        ProbabilitySimplex("ab")
    assert text.value.parameters["received"] == "str"

    with pytest.raises(SimplexError, match="mass is not one") as heavy:
        ProbabilitySimplex([Fraction(1, 2), Fraction(1, 2), Fraction(1, 2)])
    assert heavy.value.parameters["total"] == "3/2"

    with pytest.raises(SimplexError, match="mass is negative") as signed:
        ProbabilitySimplex([-Fraction(1, 2), Fraction(3, 2)])
    assert signed.value.parameters["mass"] == "-1/2"


def test_integration_matches_scaled_separator() -> None:
    root = Path(__file__).resolve().parents[3]
    source = (root / "lean4" / "H001Rats.lean").read_text(encoding="utf-8")
    assert "theorem fractional_half_simplex" in source
    assert "theorem uniform_half_mass" in source
    assert "theorem half_add_half" in source
    assert half_simplex_mass() == Fraction(1)
    assert scaled_simplex_witness() == 1
    assert type(half_simplex_mass()) is Fraction
    assert type(scaled_simplex_witness()) is int


def test_end_to_end_cli_prints_one() -> None:
    stdout = io.StringIO()
    with redirect_stdout(stdout):
        code = main()
    assert code == 0
    assert stdout.getvalue() == "1\n"


def test_origin_resolves_in_repo() -> None:
    source = _MODULE_PATH.read_text(encoding="utf-8")
    assert "Origin: lean4/H001Rats.lean theorem fractional_half_simplex" in source
    assert "Claim: urn:omega:fqm:simplex:fractional-half:v1" in source
    assert "AuthorityEffect: None" in source
    assert "Scope Fence:" in source


_MUTANTS: tuple[tuple[str, str, str], ...] = (
    (
        "float mass admitted",
        "if isinstance(value, float):",
        "if False and isinstance(value, float):",
    ),
    (
        "boolean mass admitted",
        "if type(value) is bool:",
        "if False and type(value) is bool:",
    ),
    (
        "half equality inverted",
        "if mass != Fraction(1, 2):",
        "if mass == Fraction(1, 2):",
    ),
    (
        "collapsed half check inverted",
        "if mass == 0 or mass == 1:",
        "if mass != 0 and mass != 1:",
    ),
    ("half sum replaced by difference", "total = left + right", "total = left - right"),
    ("nonnegative check inverted", "if mass < 0:", "if mass >= 0:"),
    (
        "unit total check inverted",
        "if total != Fraction(1):",
        "if total == Fraction(1):",
    ),
    (
        "sequence check inverted",
        "not isinstance(values, (list, tuple))",
        "isinstance(values, (list, tuple))",
    ),
)


def _load_source(source: str, name: str) -> dict[str, object]:
    spec = importlib.util.spec_from_loader(name, loader=None)
    if spec is None:
        raise RuntimeError("could not allocate a mutant module spec")
    module = importlib.util.module_from_spec(spec)
    module.__package__ = "src.finite_probability"
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
    half = namespace["half_simplex_mass"]
    simplex = namespace["ProbabilitySimplex"]
    uniform_of = getattr(simplex, "uniform", None)
    dirac_at = getattr(simplex, "dirac", None)
    if not callable(half) or not callable(uniform_of) or not callable(dirac_at):
        return False
    try:
        uniform = uniform_of(2)
        dirac = dirac_at(3, 1)
        values = (half(), uniform[0], dirac[1])
    except error:
        return False
    return values == (Fraction(1), Fraction(1, 2), Fraction(1))


def _bad_values_refused(namespace: dict[str, object], error: type[BaseException]) -> bool:
    simplex = namespace["ProbabilitySimplex"]
    if not isinstance(simplex, type):
        return False
    probes = (
        (lambda: simplex([0.5, 0.5]), "float refused at the simplex boundary"),
        (lambda: simplex([True, False]), "boolean refused where an exact rational was required"),
        (lambda: simplex("ab"), "masses are not a sequence"),
        (lambda: simplex([]), "masses are empty"),
        (lambda: simplex([Fraction(1, 2), Fraction(1, 2), Fraction(1, 2)]), "mass is not one"),
        (lambda: simplex([-Fraction(1, 2), Fraction(3, 2)]), "mass is negative"),
    )
    for probe, invariant in probes:
        if _invariant(error, probe) != invariant:
            return False
    return True


def _oracle(namespace: dict[str, object]) -> bool:
    error_type = namespace["SimplexError"]
    if not isinstance(error_type, type) or not issubclass(error_type, BaseException):
        return False
    if not _known_values_hold(namespace, error_type):
        return False
    return _bad_values_refused(namespace, error_type)


def test_mutation_suite_kills_non_equivalent_mutants() -> None:
    source = _MODULE_PATH.read_text(encoding="utf-8")
    loaded: list[str] = []
    try:
        loaded.append("mutant_half_simplex_baseline")
        baseline = _load_source(source, loaded[-1])
        assert _oracle(baseline) is True
        killed = 0
        for index, (name, old, new) in enumerate(_MUTANTS):
            count = source.count(old)
            assert count == 1, f"{name} matched {count} sites"
            module_name = f"mutant_half_simplex_{index}"
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
