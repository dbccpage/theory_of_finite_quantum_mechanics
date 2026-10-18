"""Unit, negative, integration, end-to-end, and mutation tests for the Fin 2 failure.

Origin: code/python/src/qm/observer_functor.py
Claim: urn:omega:fqm:observer:fin2-identity-failure:v1
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

from src.linear_algebra.ordered import compare
from src.qm.observer_functor import ObserverFunctorError, composition_defect, identity_failure, main

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


_MODULE_PATH = Path(__file__).resolve().parents[1] / "src" / "qm" / "observer_functor.py"


def test_identity_failure_is_the_named_witness() -> None:
    assert identity_failure() == 1
    assert identity_failure(0, 2) == 1
    assert identity_failure(1, 2) == 0
    assert identity_failure(0, 0) == 0
    assert composition_defect() == Fraction(13, 6)
    assert type(identity_failure()) is int
    assert type(composition_defect()) is Fraction


def test_negative_type_failures() -> None:
    with pytest.raises(ObserverFunctorError, match="float refused") as floated:
        identity_failure(_probe("1.0"), 1)
    assert floated.value.invariant == "float refused at the point boundary"
    assert floated.value.parameters["role"] == "left"
    assert type(floated.value) is ObserverFunctorError

    with pytest.raises(ObserverFunctorError, match="boolean refused") as boolean:
        identity_failure(True, 1)
    assert boolean.value.invariant == "boolean refused where an integer point was required"

    with pytest.raises(ObserverFunctorError, match="not an integer") as text:
        identity_failure("0", 1)
    assert text.value.parameters["received"] == "str"


def test_negative_shape_failures() -> None:
    with pytest.raises(ObserverFunctorError, match="not an integer") as pair:
        identity_failure((0, 1), 1)
    assert pair.value.parameters["received"] == "tuple"

    with pytest.raises(ObserverFunctorError, match="float refused") as right:
        identity_failure(0, _probe("1.5"))
    assert right.value.parameters["role"] == "right"

    assert identity_failure(-1, 0) == 1
    assert identity_failure(2, 3) == 0


def test_integration_matches_point_order() -> None:
    root = Path(__file__).resolve().parents[3]
    source = (root / "lean4" / "WorldObserverFunctoriality.lean").read_text(encoding="utf-8")
    assert "theorem fin2_source_zero" in source
    assert "theorem fin2_target_nonzero" in source
    assert "theorem fin2_failure_coordinatewise_minimal" in source
    assert compare(0, 1) != 0
    assert identity_failure() == 1
    assert identity_failure(0, 0) == 0
    assert composition_defect() == Fraction(13, 6)


def test_end_to_end_cli_prints_one() -> None:
    stdout = io.StringIO()
    with redirect_stdout(stdout):
        code = main()
    assert code == 0
    assert stdout.getvalue() == "1\n"


def test_origin_resolves_in_repo() -> None:
    source = _MODULE_PATH.read_text(encoding="utf-8")
    assert "Origin: lean4/WorldObserverFunctoriality.lean theorem fin2_source_zero" in source
    assert "Claim: urn:omega:fqm:observer:fin2-identity-failure:v1" in source
    assert "AuthorityEffect: None" in source
    assert "Scope Fence:" in source


_MUTANTS: tuple[tuple[str, str, str], ...] = (
    (
        "float point admitted",
        "if isinstance(value, float):",
        "if False and isinstance(value, float):",
    ),
    (
        "boolean point admitted",
        "if type(value) is bool:",
        "if False and type(value) is bool:",
    ),
    (
        "integer check inverted",
        "if type(value) is not int:",
        "if type(value) is int:",
    ),
    ("constant observation flipped", "_SOURCE_AGREE = False", "_SOURCE_AGREE = True"),
    ("separating predicate flipped", "return point != 0", "return point == 0"),
    ("named images inverted", "if source == target:", "if source != target:"),
    ("general order tightened", "source != target", "source > target"),
    (
        "trace product sign flipped",
        "row[0] * left + row[1] * right",
        "row[0] * left - row[1] * right",
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
    failure = namespace["identity_failure"]
    trace = namespace["composition_defect"]
    if not _all_hold((callable(failure), callable(trace),)):
        return False
    try:
        values = (failure(), failure(0, 2), failure(1, 2), failure(0, 0), trace())
    except error:
        return False
    return values == (1, 1, 0, 0, Fraction(13, 6))


def _bad_values_refused(namespace: dict[str, object], error: type[BaseException]) -> bool:
    failure = namespace["identity_failure"]
    if not callable(failure):
        return False
    probes = (
        (lambda: failure(_probe("1.0"), 1), "float refused at the point boundary"),
        (lambda: failure(True, 1), "boolean refused where an integer point was required"),
        (lambda: failure("0", 1), "point is not an integer"),
        (lambda: failure((0, 1), 1), "point is not an integer"),
        (lambda: failure(0, _probe("1.5")), "float refused at the point boundary"),
    )
    for probe, invariant in probes:
        if _invariant(error, probe) != invariant:
            return False
    return True


def _oracle(namespace: dict[str, object]) -> bool:
    error_type = namespace["ObserverFunctorError"]
    if not _all_hold((isinstance(error_type, type), issubclass(error_type, BaseException),)):
        return False
    if not _known_values_hold(namespace, error_type):
        return False
    return _bad_values_refused(namespace, error_type)


def test_mutation_suite_kills_non_equivalent_mutants() -> None:
    source = _MODULE_PATH.read_text(encoding="utf-8")
    loaded: list[str] = []
    try:
        loaded.append("mutant_observer_functor_baseline")
        baseline = _load_source(source, loaded[-1])
        assert _oracle(baseline) is True
        killed = 0
        for index, (name, old, new) in enumerate(_MUTANTS):
            count = source.count(old)
            assert count == 1, f"{name} matched {count} sites"
            module_name = f"mutant_observer_functor_{index}"
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
