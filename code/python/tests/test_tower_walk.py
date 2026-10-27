"""Unit, negative, integration, end-to-end, and mutation tests for the dyadic tower.

Origin: code/python/src/qm/tower_walk.py
Claim: urn:omega:fqm:tower:multiplicity-composition:v1
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

from src.combinatorics.finite_combinatorics import binomial_exact
from src.qm.tower_walk import TowerWalkError, cover_degree, main, multiplicity_composition, tower_degree_product

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


_MODULE_PATH = Path(__file__).resolve().parents[1] / "src" / "qm" / "tower_walk.py"


def test_multiplicity_and_tower_product() -> None:
    assert multiplicity_composition(1, 2, 2) == 4
    assert multiplicity_composition(1, 2, 3) == 6
    assert multiplicity_composition(0, 5, 7) == 0
    assert multiplicity_composition(8, 1, 1) == 8
    assert tower_degree_product() == 8
    assert type(tower_degree_product()) is int
    atoms = tuple(frozenset((index,)) for index in range(8))
    whole = (frozenset(range(8)),)
    assert cover_degree(whole, atoms) == 8


def test_negative_type_failures() -> None:
    with pytest.raises(TowerWalkError, match="float refused") as floated:
        multiplicity_composition(_probe("1.0"), 2, 2)
    assert floated.value.invariant == "float refused at the multiplicity boundary"
    assert floated.value.parameters["role"] == "base"
    assert type(floated.value) is TowerWalkError

    with pytest.raises(TowerWalkError, match="boolean refused") as boolean:
        multiplicity_composition(True, 2, 2)
    assert boolean.value.invariant == "boolean refused where a natural number was required"

    with pytest.raises(TowerWalkError, match="not an exact integer") as text:
        multiplicity_composition("1", 2, 2)
    assert text.value.parameters["received"] == "str"

    with pytest.raises(TowerWalkError, match="not an exact integer") as rational:
        multiplicity_composition(Fraction(2), 2, 2)
    assert rational.value.parameters["received"] == "Fraction"


def test_negative_shape_failures() -> None:
    with pytest.raises(TowerWalkError, match="negative") as negative:
        multiplicity_composition(-1, 2, 2)
    assert negative.value.parameters["received"] == -1

    coarse = (frozenset({0, 1}), frozenset({2}))
    fine = (frozenset({0}), frozenset({1}), frozenset({2}))
    with pytest.raises(TowerWalkError, match="does not divide") as divided:
        cover_degree(coarse, fine)
    assert divided.value.parameters["fine"] == 3
    assert divided.value.parameters["coarse"] == 2

    with pytest.raises(TowerWalkError, match="not a tuple") as listed:
        cover_degree([{0}], [{0}])
    assert listed.value.parameters["received"] == "list"

    with pytest.raises(TowerWalkError, match="blocks are empty"):
        cover_degree((), (frozenset({0}),))


def test_integration_matches_binomial_atom_count() -> None:
    root = Path(__file__).resolve().parents[3]
    source = (root / "lean4" / "RefinementSubsystemTower.lean").read_text(encoding="utf-8")
    assert "theorem multiplicity_composition" in source
    paired = multiplicity_composition(1, 2, 2)
    reached = multiplicity_composition(paired, 2, 1)
    assert paired == 4
    assert reached == 8
    assert reached == tower_degree_product()
    assert binomial_exact(tower_degree_product(), 1) == 8


def test_end_to_end_cli_prints_eight() -> None:
    buffer = io.StringIO()
    with redirect_stdout(buffer):
        code = main()
    assert code == 0
    assert buffer.getvalue().strip() == "8"
    assert tower_degree_product() == 8


def test_origin_resolves_in_repo() -> None:
    root = Path(__file__).resolve().parents[3]
    source = (root / "lean4" / "RefinementSubsystemTower.lean").read_text(encoding="utf-8")
    assert "theorem multiplicity_composition" in source
    text = _MODULE_PATH.read_text(encoding="utf-8")
    assert "AuthorityEffect: None" in text
    assert "urn:omega:fqm:tower:multiplicity-composition:v1" in text
    assert "Scope Fence:" in text


_MUTANTS: tuple[tuple[str, str, str], ...] = (
    (
        "float count admitted",
        "if isinstance(value, float):",
        "if False and isinstance(value, float):",
    ),
    (
        "boolean count admitted",
        "if type(value) is bool:",
        "if False and type(value) is bool:",
    ),
    ("negative count admitted", "if value < 0:", "if value < -1:"),
    ("readings check inverted", "if composed != stepped:", "if composed == stepped:"),
    (
        "composed product replaced by a sum",
        "(left_factor * right_factor) * base",
        "(left_factor + right_factor) * base",
    ),
    (
        "stepped product replaced by a sum",
        "right_factor * (left_factor * base)",
        "right_factor + (left_factor * base)",
    ),
    (
        "cover quotient flipped",
        "len(fine_blocks) // len(coarse_blocks)",
        "len(coarse_blocks) // len(fine_blocks)",
    ),
    (
        "divisibility check shifted",
        "len(fine_blocks) % len(coarse_blocks) != 0",
        "len(fine_blocks) % len(coarse_blocks) != -1",
    ),
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
    compose = namespace["multiplicity_composition"]
    tower = namespace["tower_degree_product"]
    if not _all_hold((callable(compose), callable(tower),)):
        return False
    try:
        values = (
            compose(1, 2, 2),
            compose(1, 2, 3),
            compose(0, 5, 7),
            compose(8, 1, 1),
            tower(),
        )
    except error:
        return False
    return values == (4, 6, 0, 8, 8)


def _bad_values_refused(namespace: dict[str, object], error: type[BaseException]) -> bool:
    compose = namespace["multiplicity_composition"]
    if not callable(compose):
        return False
    probes = (
        (lambda: compose(_probe("1.0"), 2, 2), "float refused at the multiplicity boundary"),
        (lambda: compose(True, 2, 2), "boolean refused where a natural number was required"),
        (lambda: compose(-1, 2, 2), "multiplicity count is negative"),
        (lambda: compose("1", 2, 2), "multiplicity count is not an exact integer"),
        (lambda: compose(Fraction(2), 2, 2), "multiplicity count is not an exact integer"),
    )
    for probe, invariant in probes:
        if _invariant(error, probe) != invariant:
            return False
    return True


def _oracle(namespace: dict[str, object]) -> bool:
    error_type = namespace["TowerWalkError"]
    if not _all_hold((isinstance(error_type, type), issubclass(error_type, BaseException),)):
        return False
    if not _known_values_hold(namespace, error_type):
        return False
    return _bad_values_refused(namespace, error_type)


def test_mutation_suite_kills_non_equivalent_mutants() -> None:
    source = _MODULE_PATH.read_text(encoding="utf-8")
    loaded: list[str] = []
    try:
        loaded.append("mutant_tower_walk_baseline")
        baseline = _load_source(source, loaded[-1])
        assert _oracle(baseline) is True
        killed = 0
        for index, (name, old, new) in enumerate(_MUTANTS):
            count = source.count(old)
            assert count == 1, f"{name} matched {count} sites"
            module_name = f"mutant_tower_walk_{index}"
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
