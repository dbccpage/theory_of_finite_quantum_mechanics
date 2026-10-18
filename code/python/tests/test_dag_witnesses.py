"""Unit, negative, integration, end-to-end, and mutation tests for the diamond order."""

from __future__ import annotations

import importlib.util
import io
import sys
import warnings
from contextlib import redirect_stdout
from pathlib import Path

import pytest

from src.general_relativity.causal_set import CausalSet
from src.qm.dag_witnesses import DagWitnessError, backward_edge_count, certified_diamond, main

_MODULE_PATH = Path(__file__).resolve().parents[1] / "src" / "qm" / "dag_witnesses.py"


def test_diamond_backward_count_is_zero() -> None:
    assert backward_edge_count() == 0
    assert backward_edge_count(((2, 0),), (2, 0, 1)) == 0
    assert backward_edge_count(((0, 1),), (0, 1)) == 0
    assert certified_diamond() == 0
    assert type(backward_edge_count()) is int


def test_negative_type_failures() -> None:
    with pytest.raises(DagWitnessError, match="float refused") as floated:
        backward_edge_count(((1.0, 0),), (0, 1))
    assert floated.value.invariant == "float refused at the vertex boundary"
    assert floated.value.parameters["index"] == 0
    assert type(floated.value) is DagWitnessError

    with pytest.raises(DagWitnessError, match="boolean refused") as boolean:
        backward_edge_count(((True, 0),), (0, 1))
    assert boolean.value.invariant == "boolean refused where an integer vertex was required"

    with pytest.raises(DagWitnessError, match="not an exact integer") as text:
        backward_edge_count((("0", 1),), (0, 1))
    assert text.value.parameters["received"] == "str"


def test_negative_shape_failures() -> None:
    with pytest.raises(DagWitnessError, match="has a cycle") as cycle:
        backward_edge_count(((0, 1), (1, 0)), (0, 1))
    assert cycle.value.parameters["visited"] == 0

    with pytest.raises(DagWitnessError, match="leaves the vertex set") as outside:
        backward_edge_count(((0, 4),), (0, 1))
    assert outside.value.parameters["target"] == 4

    with pytest.raises(DagWitnessError, match="not a tuple") as listed:
        backward_edge_count([(0, 1)], (0, 1))
    assert listed.value.parameters["received"] == "list"

    with pytest.raises(DagWitnessError, match="not a pair") as short:
        backward_edge_count(((0,),), (0,))
    assert short.value.parameters["index"] == 0

    with pytest.raises(DagWitnessError, match="duplicated") as duplicate:
        backward_edge_count((), (0, 0))
    assert duplicate.value.parameters["vertex"] == 0


def test_integration_matches_causal_poset() -> None:
    root = Path(__file__).resolve().parents[3]
    source = (root / "lean4" / "CausalOrder.lean").read_text(encoding="utf-8")
    assert "theorem c2_past_common" in source
    assert "theorem c2_future_common" in source
    assert "theorem c2_causal_0_3" in source
    assert "theorem c2_spacelike_1_2" in source
    poset = CausalSet.from_relations(4, [(0, 1), (0, 2), (1, 3), (2, 3)])
    assert poset.spacelike(1, 2) is True
    assert poset.order.less(0, 3) is True
    assert backward_edge_count() == 0
    assert certified_diamond() == 0


def test_end_to_end_cli_prints_zero() -> None:
    buffer = io.StringIO()
    with redirect_stdout(buffer):
        code = main()
    assert code == 0
    assert buffer.getvalue().strip() == "0"
    assert certified_diamond() == 0


def test_origin_resolves_in_repo() -> None:
    root = Path(__file__).resolve().parents[3]
    source = (root / "lean4" / "CausalOrder.lean").read_text(encoding="utf-8")
    assert "theorem c2_past_common" in source
    text = _MODULE_PATH.read_text(encoding="utf-8")
    assert "AuthorityEffect: None" in text
    assert "urn:omega:fqm:dag:diamond-backward-count:v1" in text
    assert "Scope Fence:" in text


_MUTANTS: tuple[tuple[str, str, str], ...] = (
    (
        "float vertex admitted",
        "if isinstance(value, float):",
        "if False and isinstance(value, float):",
    ),
    (
        "boolean vertex admitted",
        "if type(value) is bool:",
        "if False and type(value) is bool:",
    ),
    ("tuple check inverted", "not isinstance(values, tuple)", "isinstance(values, tuple)"),
    ("cycle check dropped", "len(order) != len(vertices)", "len(order) != -1"),
    (
        "backward comparison flipped",
        "position[source] >= position[target]",
        "position[source] < position[target]",
    ),
    ("indegree counts the source", "counts[target] += 1", "counts[source] += 1"),
    ("release skips the source", "if origin != source:", "if origin == source:"),
    (
        "endpoint check dropped",
        "if source not in counts or target not in counts:",
        "if False and (source not in counts or target not in counts):",
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
    count = namespace["backward_edge_count"]
    certified = namespace["certified_diamond"]
    if not callable(count) or not callable(certified):
        return False
    try:
        values = (
            count(),
            count(((2, 0),), (2, 0, 1)),
            count(((0, 1),), (0, 1)),
            certified(),
        )
    except error:
        return False
    return values == (0, 0, 0, 0)


def _bad_values_refused(namespace: dict[str, object], error: type[BaseException]) -> bool:
    count = namespace["backward_edge_count"]
    if not callable(count):
        return False
    probes = (
        (lambda: count(((1.0, 0),), (0, 1)), "float refused at the vertex boundary"),
        (lambda: count(((True, 0),), (0, 1)), "boolean refused where an integer vertex was required"),
        (lambda: count((("0", 1),), (0, 1)), "vertex is not an exact integer"),
        (lambda: count(((0, 1), (1, 0)), (0, 1)), "the relation has a cycle"),
        (lambda: count(((0, 4),), (0, 1)), "edge leaves the vertex set"),
        (lambda: count([(0, 1)], (0, 1)), "values are not a tuple"),
        (lambda: count(((0,),), (0,)), "edge is not a pair"),
    )
    for probe, invariant in probes:
        if _invariant(error, probe) != invariant:
            return False
    return True


def _oracle(namespace: dict[str, object]) -> bool:
    error_type = namespace["DagWitnessError"]
    if not isinstance(error_type, type) or not issubclass(error_type, BaseException):
        return False
    if not _known_values_hold(namespace, error_type):
        return False
    return _bad_values_refused(namespace, error_type)


def test_mutation_suite_kills_non_equivalent_mutants() -> None:
    source = _MODULE_PATH.read_text(encoding="utf-8")
    loaded: list[str] = []
    try:
        loaded.append("mutant_dag_witnesses_baseline")
        baseline = _load_source(source, loaded[-1])
        assert _oracle(baseline) is True
        killed = 0
        for index, (name, old, new) in enumerate(_MUTANTS):
            count = source.count(old)
            assert count == 1, f"{name} matched {count} sites"
            module_name = f"mutant_dag_witnesses_{index}"
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
