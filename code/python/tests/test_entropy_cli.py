"""Unit, negative, integration, end-to-end, and mutation tests for the CLI collision sum.

Origin: code/python/src/bin/entropy_cli.py
Claim: urn:omega:fqm:entropy:cli-collision-gap:v1
AuthorityEffect: None
Mutation-Kills: 8 non-equivalent
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

from src.bin.entropy_cli import ParityError, collision_probability, main, parity_gap

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


_MODULE_PATH = Path(__file__).resolve().parents[1] / "src" / "bin" / "entropy_cli.py"


def test_pure_and_fair_collisions() -> None:
    assert collision_probability((1, 0)) == Fraction(1)
    assert collision_probability((Fraction(1, 2), Fraction(1, 2))) == Fraction(1, 2)
    assert parity_gap() == Fraction(1, 2)
    assert type(collision_probability((1,))) is Fraction


def test_negative_boundary_failures() -> None:
    with pytest.raises(ParityError, match="float refused") as floated:
        collision_probability((_probe("1.0"), 0))
    assert floated.value.invariant == "float refused at the parity boundary"
    assert floated.value.parameters["index"] == 0
    assert type(floated.value) is ParityError

    with pytest.raises(ParityError, match="boolean refused") as boolean:
        collision_probability((True, 0))
    assert boolean.value.invariant == "boolean refused where a rational weight was required"

    with pytest.raises(ParityError, match="negative") as negative:
        collision_probability((-1, 2))
    assert negative.value.parameters["received"] == "-1"

    with pytest.raises(ParityError, match="not an exact rational") as text:
        collision_probability(("1",))
    assert text.value.parameters["received"] == "str"

    with pytest.raises(ParityError, match="not a tuple") as listed:
        collision_probability([1, 0])
    assert listed.value.parameters["received"] == "list"

    with pytest.raises(ParityError, match="empty"):
        collision_probability(())

    with pytest.raises(ParityError, match="do not sum to one") as mass:
        collision_probability((2,))
    assert mass.value.parameters["total"] == "2"

    with pytest.raises(ParityError, match="not a tuple"):
        collision_probability("10")


def test_integration_matches_scaled_purity_deficit() -> None:
    root = Path(__file__).resolve().parents[3]
    source = (root / "lean4" / "DerivationDagQMClosure.lean").read_text(encoding="utf-8")
    assert "theorem fq_entropy_renyi_purity_dichotomy_and_qm122_six_import_drop_one_census" in source
    assert "theorem fq_embedding_relativity_and_entropy_baker_dichotomy_closure" in source
    dimension = 2
    numerator = 1
    deficit = dimension * dimension - (numerator * numerator + (dimension - numerator) * (dimension - numerator))
    assert deficit == 2 * (dimension * numerator - numerator * numerator)
    fair = (Fraction(numerator, dimension), Fraction(dimension - numerator, dimension))
    assert collision_probability(fair) == Fraction(1, 2)
    assert collision_probability((1, 0)) - collision_probability(fair) == Fraction(1, 2)
    assert parity_gap() == Fraction(1, 2)


def test_end_to_end_cli_prints_half() -> None:
    buffer = io.StringIO()
    with redirect_stdout(buffer):
        code = main()
    assert code == 0
    assert buffer.getvalue().strip() == "1/2"
    assert collision_probability((1, 0, 0)) == Fraction(1)
    assert collision_probability((Fraction(1, 3), Fraction(1, 3), Fraction(1, 3))) == Fraction(1, 3)


def test_origin_resolves_in_repo() -> None:
    root = Path(__file__).resolve().parents[3]
    source = (root / "lean4" / "DerivationDagQMClosure.lean").read_text(encoding="utf-8")
    assert "theorem fq_entropy_renyi_purity_dichotomy_and_qm122_six_import_drop_one_census" in source
    assert "theorem fq_embedding_relativity_and_entropy_baker_dichotomy_closure" in source
    text = _MODULE_PATH.read_text(encoding="utf-8")
    assert "AuthorityEffect: None" in text
    assert "urn:omega:fqm:entropy:cli-collision-gap:v1" in text
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
    ("mass check inverted", "if total != 1:", "if total == 1:"),
    ("empty vector admitted", "len(weights) == 0", "len(weights) == -1"),
    ("tuple check inverted", "not isinstance(weights, tuple)", "isinstance(weights, tuple)"),
    ("square replaced by the weight", "total += weight * weight", "total += weight"),
    ("gap constant shifted", "_GAP = Fraction(1, 2)", "_GAP = Fraction(1, 3)"),
)


def _load_source(source: str, name: str) -> dict[str, object]:
    spec = importlib.util.spec_from_loader(name, loader=None)
    if spec is None:
        raise RuntimeError("could not allocate a mutant module spec")
    module = importlib.util.module_from_spec(spec)
    module.__package__ = "src.bin"
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
    collision = namespace["collision_probability"]
    gap = namespace["parity_gap"]
    if not _all_hold((callable(collision), callable(gap),)):
        return False
    try:
        pure = collision((1, 0))
        fair = collision((Fraction(1, 2), Fraction(1, 2)))
        point = collision((1,))
        measured = gap()
    except error:
        return False
    return _all_hold((
pure == Fraction(1),
fair == Fraction(1, 2),
point == Fraction(1),
measured == Fraction(1, 2),
))


def _bad_values_refused(namespace: dict[str, object], error: type[BaseException]) -> bool:
    collision = namespace["collision_probability"]
    if not callable(collision):
        return False
    probes = (
        (lambda: collision((_probe("1.0"), 0)), "float refused at the parity boundary"),
        (lambda: collision((True, 0)), "boolean refused where a rational weight was required"),
        (lambda: collision((-1, 2)), "parity weight is negative"),
        (lambda: collision(()), "parity weights are empty"),
        (lambda: collision((2,)), "parity weights do not sum to one"),
        (lambda: collision([1, 0]), "parity weights are not a tuple"),
        (lambda: collision(("1",)), "parity weight is not an exact rational"),
    )
    for probe, invariant in probes:
        if _invariant(error, probe) != invariant:
            return False
    return True


def _oracle(namespace: dict[str, object]) -> bool:
    error_type = namespace["ParityError"]
    if not _all_hold((isinstance(error_type, type), issubclass(error_type, BaseException),)):
        return False
    if not _known_values_hold(namespace, error_type):
        return False
    return _bad_values_refused(namespace, error_type)


def test_mutation_suite_kills_non_equivalent_mutants() -> None:
    source = _MODULE_PATH.read_text(encoding="utf-8")
    loaded: list[str] = []
    try:
        loaded.append("mutant_entropy_cli_baseline")
        baseline = _load_source(source, loaded[-1])
        assert _oracle(baseline) is True
        killed = 0
        for index, (name, old, new) in enumerate(_MUTANTS):
            count = source.count(old)
            assert count == 1, f"{name} matched {count} sites"
            module_name = f"mutant_entropy_cli_{index}"
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
