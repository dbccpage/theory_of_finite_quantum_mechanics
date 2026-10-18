"""Unit, negative, integration, end-to-end, and mutation tests for the rotation determinant."""

from __future__ import annotations

import importlib.util
import io
import sys
import warnings
from contextlib import redirect_stdout
from pathlib import Path

import pytest

from src.qm.evidence_routes import EvidenceRouteError, main, rotation_numerator_det, route_digest_length
from src.qm.group_param import boost_numerator_det

_MODULE_PATH = Path(__file__).resolve().parents[1] / "src" / "qm" / "evidence_routes.py"
_OTHER = ((1, 2, 0), (3, 4, 0), (0, 0, 1))


def test_rotation_determinant_is_125() -> None:
    assert rotation_numerator_det() == 125
    assert rotation_numerator_det(_OTHER) == -2
    assert route_digest_length() == 32
    assert type(rotation_numerator_det()) is int
    assert type(route_digest_length()) is int


def test_negative_type_failures() -> None:
    with pytest.raises(EvidenceRouteError, match="float refused") as floated:
        rotation_numerator_det(((1.0, 0, 0), (0, 1, 0), (0, 0, 1)))
    assert floated.value.invariant == "float refused at the matrix boundary"
    assert floated.value.parameters["role"] == "row0"
    assert type(floated.value) is EvidenceRouteError

    with pytest.raises(EvidenceRouteError, match="boolean refused") as boolean:
        rotation_numerator_det(((True, 0, 0), (0, 1, 0), (0, 0, 1)))
    assert boolean.value.invariant == "boolean refused where an integer entry was required"

    with pytest.raises(EvidenceRouteError, match="not an integer") as text:
        rotation_numerator_det((("3", 0, 0), (0, 1, 0), (0, 0, 1)))
    assert text.value.parameters["received"] == "str"


def test_negative_shape_failures() -> None:
    with pytest.raises(EvidenceRouteError, match="not a triple") as wide:
        rotation_numerator_det(((1, 2, 3, 4), (0, 1, 0), (0, 0, 1)))
    assert wide.value.parameters["length"] == 4

    with pytest.raises(EvidenceRouteError, match="not 3 by 3") as short:
        rotation_numerator_det(((1, 0, 0), (0, 1, 0)))
    assert short.value.parameters["length"] == 2

    with pytest.raises(EvidenceRouteError, match="not a tuple") as listed:
        rotation_numerator_det([(1, 0, 0), (0, 1, 0), (0, 0, 1)])
    assert listed.value.parameters["received"] == "list"


def test_integration_matches_block_minor() -> None:
    root = Path(__file__).resolve().parents[3]
    source = (root / "lean4" / "GroupParameter.lean").read_text(encoding="utf-8")
    assert "theorem pyth_rot_numerator_det" in source
    minor = boost_numerator_det(((3, -4), (4, 3)))
    assert minor == 25
    assert rotation_numerator_det() == minor * 5
    assert route_digest_length() == 32


def test_end_to_end_cli_prints_125() -> None:
    stdout = io.StringIO()
    with redirect_stdout(stdout):
        code = main()
    assert code == 0
    assert stdout.getvalue() == "125\n"


def test_origin_resolves_in_repo() -> None:
    source = _MODULE_PATH.read_text(encoding="utf-8")
    assert "Origin: lean4/GroupParameter.lean theorem pyth_rot_numerator_det" in source
    assert "Claim: urn:omega:fqm:route:pythagorean-rotation-det:v1" in source
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
    ("row length check dropped", "len(row) != 3", "len(row) != -1"),
    (
        "cofactor sign flipped",
        "return first - second + third",
        "return first + second + third",
    ),
    (
        "determinant check inverted",
        "if matrix is None and value != _DETERMINANT:",
        "if matrix is None and value == _DETERMINANT:",
    ),
    (
        "tuple check inverted",
        "not isinstance(matrix, tuple)",
        "isinstance(matrix, tuple)",
    ),
    (
        "digest rebuild inverted",
        "if parent != rebuilt:",
        "if parent == rebuilt:",
    ),
    ("digest length shifted", "return len(parent)", "return len(parent) - 1"),
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
    determinant = namespace["rotation_numerator_det"]
    digest = namespace["route_digest_length"]
    if not callable(determinant) or not callable(digest):
        return False
    try:
        values = (determinant(), determinant(_OTHER), digest())
    except error:
        return False
    return values == (125, -2, 32)


def _bad_values_refused(namespace: dict[str, object], error: type[BaseException]) -> bool:
    determinant = namespace["rotation_numerator_det"]
    if not callable(determinant):
        return False
    probes = (
        (lambda: determinant(((1.0, 0, 0), (0, 1, 0), (0, 0, 1))), "float refused at the matrix boundary"),
        (lambda: determinant(((True, 0, 0), (0, 1, 0), (0, 0, 1))), "boolean refused where an integer entry was required"),
        (lambda: determinant((("3", 0, 0), (0, 1, 0), (0, 0, 1))), "matrix entry is not an integer"),
        (lambda: determinant(((1, 2, 3, 4), (0, 1, 0), (0, 0, 1))), "matrix row is not a triple"),
        (lambda: determinant(((1, 0, 0), (0, 1, 0))), "matrix is not 3 by 3"),
        (lambda: determinant([(1, 0, 0), (0, 1, 0), (0, 0, 1)]), "matrix is not a tuple"),
    )
    for probe, invariant in probes:
        if _invariant(error, probe) != invariant:
            return False
    return True


def _oracle(namespace: dict[str, object]) -> bool:
    error_type = namespace["EvidenceRouteError"]
    if not isinstance(error_type, type) or not issubclass(error_type, BaseException):
        return False
    if not _known_values_hold(namespace, error_type):
        return False
    return _bad_values_refused(namespace, error_type)


def test_mutation_suite_kills_non_equivalent_mutants() -> None:
    source = _MODULE_PATH.read_text(encoding="utf-8")
    loaded: list[str] = []
    try:
        loaded.append("mutant_evidence_routes_baseline")
        baseline = _load_source(source, loaded[-1])
        assert _oracle(baseline) is True
        killed = 0
        for index, (name, old, new) in enumerate(_MUTANTS):
            count = source.count(old)
            assert count == 1, f"{name} matched {count} sites"
            module_name = f"mutant_evidence_routes_{index}"
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
