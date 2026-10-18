"""Unit, negative, integration, end-to-end, and mutation tests for the phase fiber.

Origin: code/python/src/qm/report_fiber.py
Claim: urn:omega:fqm:fiber:relative-phase-count:v1
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

from src.linear_algebra.ordered import sum_of_squares
from src.qm.report_fiber import ReportFiberError, main, phase_weight, relative_fiber_size

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


_MODULE_PATH = Path(__file__).resolve().parents[1] / "src" / "qm" / "report_fiber.py"
_PSI1 = ((1, 0), (1, 0))
_PSI2 = ((1, 0), (-1, 0))
_TURNED = ((0, 1), (0, 1))
_REAL = ((1, 0), (1, 0))


def test_named_fiber_has_two_distinct_vectors() -> None:
    assert relative_fiber_size() == 2
    assert relative_fiber_size(_TURNED, _REAL) == 2
    assert phase_weight((0, 1)) == 1
    assert phase_weight((3, 4)) == 25
    assert phase_weight((1, 0)) == 1
    assert type(relative_fiber_size()) is int


def test_negative_type_failures() -> None:
    with pytest.raises(ReportFiberError, match="float refused") as floated:
        relative_fiber_size(((_probe("1.0"), 0), (1, 0)), _PSI2)
    assert floated.value.invariant == "float refused at the gaussian boundary"
    assert floated.value.parameters["role"] == "false"
    assert type(floated.value) is ReportFiberError

    with pytest.raises(ReportFiberError, match="boolean refused") as boolean:
        phase_weight((True, 0))
    assert boolean.value.invariant == "boolean refused where an integer part was required"

    with pytest.raises(ReportFiberError, match="not an integer") as text:
        phase_weight(("1", 0))
    assert text.value.parameters["received"] == "str"


def test_negative_shape_failures() -> None:
    with pytest.raises(ReportFiberError, match="not a pair") as wide:
        phase_weight((1, 0, 9))
    assert wide.value.parameters["length"] == 3

    with pytest.raises(ReportFiberError, match="not a pair") as short:
        relative_fiber_size(((1, 0),), _PSI2)
    assert short.value.parameters["length"] == 1

    with pytest.raises(ReportFiberError, match="not a tuple") as listed:
        relative_fiber_size([_PSI1[0], _PSI1[1]], _PSI2)
    assert listed.value.parameters["received"] == "list"

    with pytest.raises(ReportFiberError, match="not distinct") as same:
        relative_fiber_size(_PSI1, _PSI1)
    assert same.value.invariant == "vectors are not distinct"


def test_integration_matches_sum_of_squares() -> None:
    root = Path(__file__).resolve().parents[3]
    fiber = (root / "lean4" / "QuotientFiber.lean").read_text(encoding="utf-8")
    blind = (root / "lean4" / "PhaseBlindPresentation.lean").read_text(encoding="utf-8")
    assert "theorem psi1_psi2_in_same_fiber" in fiber
    assert "theorem psi1_psi2_distinct" in fiber
    assert "theorem fiber_exceeds_global_gauge_orbit" in fiber
    assert "theorem global_phase_blind" in blind
    assert phase_weight((3, 4)) == sum_of_squares((3, 4))
    assert phase_weight((1, 0)) == sum_of_squares((1, 0))
    assert relative_fiber_size() == 2


def test_end_to_end_cli_prints_two() -> None:
    stdout = io.StringIO()
    with redirect_stdout(stdout):
        code = main()
    assert code == 0
    assert stdout.getvalue() == "2\n"


def test_origin_resolves_in_repo() -> None:
    source = _MODULE_PATH.read_text(encoding="utf-8")
    assert "Origin: lean4/QuotientFiber.lean theorem psi1_psi2_in_same_fiber" in source
    assert "Claim: urn:omega:fqm:fiber:relative-phase-count:v1" in source
    assert "AuthorityEffect: None" in source
    assert "Scope Fence:" in source


_MUTANTS: tuple[tuple[str, str, str], ...] = (
    (
        "float part admitted",
        "if isinstance(value, float):",
        "if False and isinstance(value, float):",
    ),
    (
        "boolean part admitted",
        "if type(value) is bool:",
        "if False and type(value) is bool:",
    ),
    ("pair length check dropped", "len(pair) != 2", "len(pair) != -1"),
    (
        "square sum sign flipped",
        "real * real + imag * imag",
        "real * real - imag * imag",
    ),
    ("distinct check inverted", "if first == second:", "if first != second:"),
    (
        "weight check inverted",
        "if _weights(first) != _weights(second):",
        "if _weights(first) == _weights(second):",
    ),
    (
        "scalar gap inverted",
        "if vector[0] == vector[1]:",
        "if vector[0] != vector[1]:",
    ),
    (
        "vector tuple check inverted",
        "not isinstance(vector, tuple)",
        "isinstance(vector, tuple)",
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
    size = namespace["relative_fiber_size"]
    weight = namespace["phase_weight"]
    if not _all_hold((callable(size), callable(weight),)):
        return False
    try:
        values = (
            size(),
            size(_TURNED, _REAL),
            weight((0, 1)),
            weight((3, 4)),
            weight((1, 0)),
        )
    except error:
        return False
    return values == (2, 2, 1, 25, 1)


def _bad_values_refused(namespace: dict[str, object], error: type[BaseException]) -> bool:
    size = namespace["relative_fiber_size"]
    weight = namespace["phase_weight"]
    if not _all_hold((callable(size), callable(weight),)):
        return False
    probes = (
        (lambda: size(((_probe("1.0"), 0), (1, 0)), _PSI2), "float refused at the gaussian boundary"),
        (lambda: weight((True, 0)), "boolean refused where an integer part was required"),
        (lambda: weight(("1", 0)), "gaussian part is not an integer"),
        (lambda: weight((1, 0, 9)), "gaussian integer is not a pair"),
        (lambda: size(((1, 0),), _PSI2), "amplitude vector is not a pair"),
        (lambda: size([_PSI1[0], _PSI1[1]], _PSI2), "amplitude vector is not a tuple"),
        (lambda: size(_PSI1, _PSI1), "vectors are not distinct"),
        (lambda: size(((2, 0), (0, 0)), _PSI1), "phase-blind weights differ"),
    )
    for probe, invariant in probes:
        if _invariant(error, probe) != invariant:
            return False
    return True


def _oracle(namespace: dict[str, object]) -> bool:
    error_type = namespace["ReportFiberError"]
    if not _all_hold((isinstance(error_type, type), issubclass(error_type, BaseException),)):
        return False
    if not _known_values_hold(namespace, error_type):
        return False
    return _bad_values_refused(namespace, error_type)


def test_mutation_suite_kills_non_equivalent_mutants() -> None:
    source = _MODULE_PATH.read_text(encoding="utf-8")
    loaded: list[str] = []
    try:
        loaded.append("mutant_report_fiber_baseline")
        baseline = _load_source(source, loaded[-1])
        assert _oracle(baseline) is True
        killed = 0
        for index, (name, old, new) in enumerate(_MUTANTS):
            count = source.count(old)
            assert count == 1, f"{name} matched {count} sites"
            module_name = f"mutant_report_fiber_{index}"
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
