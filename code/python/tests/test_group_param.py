"""Unit, negative, integration, end-to-end, and mutation tests for the boost numerator.

Origin: code/python/src/qm/group_param.py
Claim: urn:omega:fqm:group:boost-numerator-det:v1
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

from src.qm.finite_witness import pair_residual
from src.qm.group_param import (
    GroupParamError,
    boost_numerator_det,
    main,
    pauli_trace,
    shear_parameter,
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


_MODULE_PATH = Path(__file__).resolve().parents[1] / "src" / "qm" / "group_param.py"
_OTHER = ((1, 2), (3, 4))


def test_determinant_and_trace_match_the_theorems() -> None:
    assert boost_numerator_det() == 16
    assert boost_numerator_det(_OTHER) == -2
    assert pauli_trace() == 0
    assert pauli_trace(((2, 0), (0, 3))) == 5
    assert shear_parameter() == Fraction(22, 15)
    assert type(boost_numerator_det()) is int
    assert type(shear_parameter()) is Fraction


def test_negative_type_failures() -> None:
    with pytest.raises(GroupParamError, match="float refused") as floated:
        boost_numerator_det(((_probe("1.0"), 0), (0, 1)))
    assert floated.value.invariant == "float refused at the matrix boundary"
    assert floated.value.parameters["role"] == "row0"
    assert type(floated.value) is GroupParamError

    with pytest.raises(GroupParamError, match="boolean refused") as boolean:
        pauli_trace(((True, 0), (0, 1)))
    assert boolean.value.invariant == "boolean refused where an integer entry was required"

    with pytest.raises(GroupParamError, match="not an integer") as text:
        boost_numerator_det((("5", 0), (0, 1)))
    assert text.value.parameters["received"] == "str"


def test_negative_shape_failures() -> None:
    with pytest.raises(GroupParamError, match="not a pair") as wide:
        boost_numerator_det(((1, 2, 3), (0, 1)))
    assert wide.value.parameters["length"] == 3

    with pytest.raises(GroupParamError, match="not 2 by 2") as short:
        boost_numerator_det(((1, 0),))
    assert short.value.parameters["length"] == 1

    with pytest.raises(GroupParamError, match="not a tuple") as listed:
        boost_numerator_det([(1, 0), (0, 1)])
    assert listed.value.parameters["received"] == "list"

    with pytest.raises(GroupParamError, match="not a tuple") as row:
        boost_numerator_det(("row", (0, 1)))
    assert row.value.parameters["role"] == "row0"


def test_integration_matches_eigenpair_product() -> None:
    root = Path(__file__).resolve().parents[3]
    source = (root / "lean4" / "GroupParameter.lean").read_text(encoding="utf-8")
    assert "theorem b1_numerator_det" in source
    assert "theorem pauli_z_trace_zero" in source
    upper = pair_residual(((5, 3), (3, 5)), (1, 1), 8)
    lower = pair_residual(((5, 3), (3, 5)), (1, -1), 2)
    assert upper == 0
    assert lower == 0
    assert boost_numerator_det() == 8 * 2
    assert pauli_trace() == 0


def test_end_to_end_cli_prints_sixteen() -> None:
    stdout = io.StringIO()
    with redirect_stdout(stdout):
        code = main()
    assert code == 0
    assert stdout.getvalue() == "16\n"


def test_origin_resolves_in_repo() -> None:
    source = _MODULE_PATH.read_text(encoding="utf-8")
    assert "Origin: lean4/GroupParameter.lean theorem b1_numerator_det" in source
    assert "Claim: urn:omega:fqm:group:boost-numerator-det:v1" in source
    assert "AuthorityEffect: None" in source
    assert "Scope Fence:" in source


_MUTANTS: tuple[tuple[str, str, str], ...] = (
    (
        "float entry admitted",
        "if isinstance(value, float):",
        "if False and isinstance(value, float):",
    ),
    (
        "boolean entry admitted",
        "if type(value) is bool:",
        "if False and type(value) is bool:",
    ),
    ("row length check dropped", "len(row) != 2", "len(row) != -1"),
    (
        "determinant sign flipped",
        "rows[0][0] * rows[1][1] - rows[0][1] * rows[1][0]",
        "rows[0][0] * rows[1][1] + rows[0][1] * rows[1][0]",
    ),
    (
        "trace sign flipped",
        "rows[0][0] + rows[1][1]",
        "rows[0][0] - rows[1][1]",
    ),
    (
        "determinant check inverted",
        "if matrix is None and value != _DETERMINANT:",
        "if matrix is None and value == _DETERMINANT:",
    ),
    (
        "shear entry sign flipped",
        "Fraction(1) * right + left * Fraction(1)",
        "Fraction(1) * right - left * Fraction(1)",
    ),
    (
        "tuple check inverted",
        "not isinstance(matrix, tuple)",
        "isinstance(matrix, tuple)",
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
    determinant = namespace["boost_numerator_det"]
    trace = namespace["pauli_trace"]
    shear = namespace["shear_parameter"]
    if not _all_hold((callable(determinant), callable(trace), callable(shear),)):
        return False
    try:
        values = (
            determinant(),
            determinant(_OTHER),
            trace(),
            trace(((2, 0), (0, 3))),
            shear(),
        )
    except error:
        return False
    return values == (16, -2, 0, 5, Fraction(22, 15))


def _bad_values_refused(namespace: dict[str, object], error: type[BaseException]) -> bool:
    determinant = namespace["boost_numerator_det"]
    trace = namespace["pauli_trace"]
    if not _all_hold((callable(determinant), callable(trace),)):
        return False
    probes = (
        (lambda: determinant(((_probe("1.0"), 0), (0, 1))), "float refused at the matrix boundary"),
        (lambda: trace(((True, 0), (0, 1))), "boolean refused where an integer entry was required"),
        (lambda: determinant((("5", 0), (0, 1))), "matrix entry is not an integer"),
        (lambda: determinant(((1, 2, 3), (0, 1))), "matrix row is not a pair"),
        (lambda: determinant(((1, 0),)), "matrix is not 2 by 2"),
        (lambda: determinant([(1, 0), (0, 1)]), "matrix is not a tuple"),
    )
    for probe, invariant in probes:
        if _invariant(error, probe) != invariant:
            return False
    return True


def _oracle(namespace: dict[str, object]) -> bool:
    error_type = namespace["GroupParamError"]
    if not _all_hold((isinstance(error_type, type), issubclass(error_type, BaseException),)):
        return False
    if not _known_values_hold(namespace, error_type):
        return False
    return _bad_values_refused(namespace, error_type)


def test_mutation_suite_kills_non_equivalent_mutants() -> None:
    source = _MODULE_PATH.read_text(encoding="utf-8")
    loaded: list[str] = []
    try:
        loaded.append("mutant_group_param_baseline")
        baseline = _load_source(source, loaded[-1])
        assert _oracle(baseline) is True
        killed = 0
        for index, (name, old, new) in enumerate(_MUTANTS):
            count = source.count(old)
            assert count == 1, f"{name} matched {count} sites"
            module_name = f"mutant_group_param_{index}"
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
