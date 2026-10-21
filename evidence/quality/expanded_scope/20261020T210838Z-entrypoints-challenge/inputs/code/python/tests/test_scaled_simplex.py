"""Unit, negative, integration, end-to-end, and mutation tests for scaled separators.

Origin: code/python/src/finite_probability/__init__.py
Claim: urn:omega:fqm:simplex:scaled-integer-separator:v1
AuthorityEffect: None
Mutation-Kills: 8 non-equivalent
"""



from __future__ import annotations

import importlib.util
import io
import sys
import warnings
from contextlib import redirect_stdout
from pathlib import Path

import pytest

from src.finite_probability import (
    ScaledSimplexError,
    integer_mass,
    main,
    scaled_simplex_witness,
)
from src.linear_algebra.ordered import compare

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


_MODULE_PATH = Path(__file__).resolve().parents[1] / "src" / "finite_probability" / "__init__.py"


def test_named_separators_match_the_theorem() -> None:
    assert scaled_simplex_witness() == 1
    assert integer_mass((1, 0)) == 1
    assert integer_mass((-1, 2)) == 1
    assert integer_mass((1, 1)) == 2
    assert integer_mass((3, 4)) == 7
    assert type(scaled_simplex_witness()) is int
    assert type(integer_mass((1, 0))) is int


def test_negative_type_failures() -> None:
    with pytest.raises(ScaledSimplexError, match="float refused") as floated:
        integer_mass((_probe("1.0"), 0))
    assert floated.value.invariant == "float refused at the weight boundary"
    assert floated.value.parameters["role"] == "false"
    assert type(floated.value) is ScaledSimplexError

    with pytest.raises(ScaledSimplexError, match="boolean refused") as boolean:
        integer_mass((True, 0))
    assert boolean.value.invariant == "boolean refused where an integer weight was required"

    with pytest.raises(ScaledSimplexError, match="not an integer") as text:
        integer_mass((1, "0"))
    assert text.value.parameters["received"] == "str"


def test_negative_shape_failures() -> None:
    with pytest.raises(ScaledSimplexError, match="not a Bool pair") as short:
        integer_mass((1,))
    assert short.value.parameters["length"] == 1

    with pytest.raises(ScaledSimplexError, match="not a Bool pair") as long:
        integer_mass((1, 0, 0))
    assert long.value.parameters["length"] == 3

    with pytest.raises(ScaledSimplexError, match="not a tuple") as listed:
        integer_mass([1, 0])
    assert listed.value.parameters["received"] == "list"


def test_integration_matches_ordered_compare() -> None:
    root = Path(__file__).resolve().parents[3]
    source = (root / "lean4" / "H001ProbabilitySimplex.lean").read_text(encoding="utf-8")
    assert "theorem probability_simplex" in source
    assert "theorem signed_mass_one" in source
    assert "theorem double_mass_two" in source
    assert "theorem l1dist_self" in source
    assert compare(integer_mass((1, 0)), 1) == 0
    assert compare(integer_mass((1, 1)), 1) != 0
    assert scaled_simplex_witness() == 1


def test_end_to_end_cli_prints_one() -> None:
    stdout = io.StringIO()
    with redirect_stdout(stdout):
        code = main()
    assert code == 0
    assert stdout.getvalue() == "1\n"


def test_origin_resolves_in_repo() -> None:
    source = _MODULE_PATH.read_text(encoding="utf-8")
    assert "Origin: lean4/H001ProbabilitySimplex.lean theorem probability_simplex" in source
    assert "Claim: urn:omega:fqm:simplex:scaled-integer-separator:v1" in source
    assert "AuthorityEffect: None" in source
    assert "Scope Fence:" in source


_MUTANTS: tuple[tuple[str, str, str], ...] = (
    (
        "float weight admitted",
        "if isinstance(value, float):",
        "if False and isinstance(value, float):",
    ),
    (
        "boolean weight admitted",
        "if type(value) is bool:",
        "if False and type(value) is bool:",
    ),
    ("pair length check dropped", "len(entries) != 2", "len(entries) != -1"),
    (
        "mass difference substituted",
        "return pair[0] + pair[1]",
        "return pair[0] - pair[1]",
    ),
    ("point mass check inverted", "if mass != 1:", "if mass == 1:"),
    (
        "signed nonnegativity inverted",
        "if pair[0] >= 0 and pair[1] >= 0:",
        "if pair[0] < 0 or pair[1] < 0:",
    ),
    ("self gap uses the other weight", "pair[0] - pair[0]", "pair[0] - pair[1]"),
    ("tuple check inverted", "not isinstance(weights, tuple)", "isinstance(weights, tuple)"),
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
    witness = namespace["scaled_simplex_witness"]
    mass = namespace["integer_mass"]
    if not _all_hold((callable(witness), callable(mass),)):
        return False
    try:
        values = (witness(), mass((1, 0)), mass((-1, 2)), mass((1, 1)), mass((3, 4)))
    except error:
        return False
    return values == (1, 1, 1, 2, 7)


def _bad_values_refused(namespace: dict[str, object], error: type[BaseException]) -> bool:
    mass = namespace["integer_mass"]
    if not callable(mass):
        return False
    probes = (
        (lambda: mass((_probe("1.0"), 0)), "float refused at the weight boundary"),
        (lambda: mass((True, 0)), "boolean refused where an integer weight was required"),
        (lambda: mass((1, 0, 0)), "weights are not a Bool pair"),
        (lambda: mass([1, 0]), "weights are not a tuple"),
        (lambda: mass((1, "0")), "weight is not an integer"),
    )
    for probe, invariant in probes:
        if _invariant(error, probe) != invariant:
            return False
    return True


def _oracle(namespace: dict[str, object]) -> bool:
    error_type = namespace["ScaledSimplexError"]
    if not _all_hold((isinstance(error_type, type), issubclass(error_type, BaseException),)):
        return False
    if not _known_values_hold(namespace, error_type):
        return False
    return _bad_values_refused(namespace, error_type)


def test_mutation_suite_kills_non_equivalent_mutants() -> None:
    source = _MODULE_PATH.read_text(encoding="utf-8")
    loaded: list[str] = []
    try:
        loaded.append("mutant_scaled_simplex_baseline")
        baseline = _load_source(source, loaded[-1])
        assert _oracle(baseline) is True
        killed = 0
        for index, (name, old, new) in enumerate(_MUTANTS):
            count = source.count(old)
            assert count == 1, f"{name} matched {count} sites"
            module_name = f"mutant_scaled_simplex_{index}"
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
