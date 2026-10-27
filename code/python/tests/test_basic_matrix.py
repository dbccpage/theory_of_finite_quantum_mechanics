"""Unit, negative, integration, end-to-end, and mutation tests for identity_trace.

Origin: code/python/src/linear_algebra/basic_matrix.py
Claim: urn:omega:fqm:linear-algebra:identity-trace:v1
AuthorityEffect: None
Mutation-Kills: 8 non-equivalent
"""





from __future__ import annotations

import importlib.util
import sys
import warnings
from fractions import Fraction
from pathlib import Path

import pytest

from src.linear_algebra.basic_matrix import (
    ExactMatrix,
    IdentityTraceError,
    MatrixError,
    _require_diagonal,
    _sum_diagonal,
    identity_trace,
)

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


_MODULE_PATH = Path(__file__).resolve().parents[1] / "src" / "linear_algebra" / "basic_matrix.py"


def test_identity_trace_matches_dimension_on_cited_sizes() -> None:
    assert identity_trace(2) == Fraction(2)
    assert identity_trace(3) == Fraction(3)
    assert type(identity_trace(2)) is Fraction


def test_negative_boundary_failures() -> None:
    with pytest.raises(IdentityTraceError, match="float refused") as floated:
        identity_trace(_probe("1.0"))
    assert floated.value.invariant == "float refused at the public boundary"
    assert floated.value.parameters["role"] == "size"
    assert type(floated.value) is IdentityTraceError
    assert isinstance(floated.value, MatrixError)

    with pytest.raises(IdentityTraceError, match="boolean refused") as boolean:
        identity_trace(True)
    assert boolean.value.invariant == "boolean refused where an integer size was required"

    with pytest.raises(IdentityTraceError, match="negative") as negative:
        identity_trace(-1)
    assert negative.value.parameters["received"] == -1

    with pytest.raises(IdentityTraceError, match="not an integer") as text:
        identity_trace("2")
    assert text.value.parameters["received"] == "str"

    with pytest.raises(IdentityTraceError, match="float refused on the identity diagonal") as diagonal:
        _require_diagonal(_probe("1.5"), 0)
    assert diagonal.value.parameters["index"] == 0

    with pytest.raises(IdentityTraceError, match="boolean refused on the identity diagonal"):
        _require_diagonal(False, 1)

    with pytest.raises(IdentityTraceError, match="not an exact rational"):
        _require_diagonal("1", 0)

    eye = ExactMatrix.identity(1)
    eye.data[0] = _probe("0.25")
    with pytest.raises(IdentityTraceError, match="float refused on the identity diagonal"):
        _sum_diagonal(eye)


def test_integration_matches_cited_lean_traces() -> None:
    root = Path(__file__).resolve().parents[3]
    scaled = (root / "lean4" / "ContinuumLiftBoundary.lean").read_text(encoding="utf-8")
    eye = (root / "lean4" / "StoneVonNeumannObstruction.lean").read_text(encoding="utf-8")
    assert "theorem trace_scalar_identity" in scaled
    assert "theorem tr_eye3_nonzero" in eye
    assert identity_trace(2) == Fraction(2 * 1)
    assert identity_trace(3) == Fraction(3)
    assert identity_trace(3) != 0


def test_end_to_end_unproven_sizes_stay_exact() -> None:
    assert identity_trace(0) == Fraction(0)
    assert identity_trace(1) == Fraction(1)
    assert identity_trace(4) == Fraction(4)
    assert ExactMatrix.identity(4).rows == 4


def test_origin_resolves_in_repo() -> None:
    root = Path(__file__).resolve().parents[3]
    scaled = (root / "lean4" / "ContinuumLiftBoundary.lean").read_text(encoding="utf-8")
    eye = (root / "lean4" / "StoneVonNeumannObstruction.lean").read_text(encoding="utf-8")
    assert "theorem trace_scalar_identity" in scaled
    assert "theorem tr_eye3_nonzero" in eye
    source = _MODULE_PATH.read_text(encoding="utf-8")
    assert "AuthorityEffect: None" in source
    assert "urn:omega:fqm:linear-algebra:identity-trace:v1" in source
    assert "Scope Fence:" in source


_MUTANTS: tuple[tuple[str, str, str], ...] = (
    (
        "float size admitted",
        "if isinstance(value, float):",
        "if isinstance(value, float):\n        return\n    if False:",
    ),
    (
        "boolean size admitted",
        "if type(value) is bool:",
        "if type(value) is bool:\n        return 1\n    if False:",
    ),
    ("integer size check inverted", "if type(value) is int:", "if type(value) is not int:"),
    ("negative size admitted", "if size < 0:", "if size < -1:"),
    (
        "diagonal float admitted",
        "if type(entry) is float:",
        "if type(entry) is float:\n        return Fraction(0)\n    if False:",
    ),
    (
        "diagonal boolean admitted",
        "if type(entry) is bool:",
        "if type(entry) is bool:\n        return Fraction(1)\n    if False:",
    ),
    ("trace check inverted", "if total != expected:", "if total == expected:"),
    ("expected dimension shifted", "expected = Fraction(size)", "expected = Fraction(size + 1)"),
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
    trace = namespace["identity_trace"]
    if not callable(trace):
        return False
    try:
        zero = trace(0)
        two = trace(2)
        three = trace(3)
        four = trace(4)
    except error:
        return False
    return _all_hold((
zero == Fraction(0),
two == Fraction(2),
three == Fraction(3),
four == Fraction(4),
))


def _bad_values_refused(namespace: dict[str, object], error: type[BaseException]) -> bool:
    trace = namespace["identity_trace"]
    diagonal = namespace["_require_diagonal"]
    summer = namespace["_sum_diagonal"]
    matrix = namespace["ExactMatrix"]
    if not _all_hold((callable(trace), callable(diagonal), callable(summer), isinstance(matrix, type),)):
        return False
    probes = (
        (lambda: trace(_probe("1.0")), "float refused at the public boundary"),
        (lambda: trace(True), "boolean refused where an integer size was required"),
        (lambda: trace(-1), "identity size is negative"),
        (lambda: trace("2"), "identity size is not an integer"),
        (lambda: diagonal(_probe("1.5"), 0), "float refused on the identity diagonal"),
        (lambda: diagonal(True, 1), "boolean refused on the identity diagonal"),
    )
    for probe, invariant in probes:
        if _invariant(error, probe) != invariant:
            return False
    build = getattr(matrix, "identity")
    if not callable(build):
        return False
    eye = build(1)
    eye.data[0] = _probe("0.5")
    if _invariant(error, lambda: summer(eye)) != "float refused on the identity diagonal":
        return False
    eye.data[0] = False
    if _invariant(error, lambda: summer(eye)) != "boolean refused on the identity diagonal":
        return False
    return True


def _oracle(namespace: dict[str, object]) -> bool:
    error_type = namespace["IdentityTraceError"]
    if not _all_hold((isinstance(error_type, type), issubclass(error_type, BaseException),)):
        return False
    if not _known_values_hold(namespace, error_type):
        return False
    return _bad_values_refused(namespace, error_type)


def test_mutation_suite_kills_non_equivalent_mutants() -> None:
    source = _MODULE_PATH.read_text(encoding="utf-8")
    loaded: list[str] = []
    try:
        loaded.append("mutant_basic_matrix_baseline")
        baseline = _load_source(source, loaded[-1])
        assert _oracle(baseline) is True
        killed = 0
        for index, (name, old, new) in enumerate(_MUTANTS):
            count = source.count(old)
            assert count == 1, f"{name} matched {count} sites"
            module_name = f"mutant_basic_matrix_{index}"
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
