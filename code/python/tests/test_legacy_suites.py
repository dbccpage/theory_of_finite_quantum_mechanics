"""Unit, negative, integration, end-to-end, and mutation tests for the ray suite.

Origin: code/python/src/qm/legacy_suites.py
Claim: urn:omega:fqm:suite:pythagorean-ray:v1
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

from src.qm.legacy_suites import LegacySuiteError, certified_ray, main, polynomial_gap, suite_pass_count
from src.qm.quantum_packet import packet_norm

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


_MODULE_PATH = Path(__file__).resolve().parents[1] / "src" / "qm" / "legacy_suites.py"
_RAY = (Fraction(3, 5), Fraction(4, 5), Fraction(0))


def test_ray_witness_and_suite_count() -> None:
    assert polynomial_gap(_RAY) == Fraction(0)
    assert polynomial_gap((1, 2, 2)) == Fraction(0)
    assert polynomial_gap((0, 0, 0)) == Fraction(0)
    assert certified_ray() == Fraction(1)
    assert suite_pass_count() == 3
    assert type(certified_ray()) is Fraction
    assert type(suite_pass_count()) is int


def test_negative_type_failures() -> None:
    with pytest.raises(LegacySuiteError, match="float refused") as floated:
        polynomial_gap((_probe("0.6"), Fraction(4, 5), 0))
    assert floated.value.invariant == "float refused at the ray boundary"
    assert floated.value.parameters["index"] == 0
    assert type(floated.value) is LegacySuiteError

    with pytest.raises(LegacySuiteError, match="boolean refused") as boolean:
        polynomial_gap((True, 0, 0))
    assert boolean.value.invariant == "boolean refused where a rational amplitude was required"

    with pytest.raises(LegacySuiteError, match="not an exact rational") as text:
        polynomial_gap(("3/5", Fraction(4, 5), 0))
    assert text.value.parameters["received"] == "str"

    with pytest.raises(LegacySuiteError, match="1024-bit limit"):
        polynomial_gap((1 << 1025, 0, 0))

    with pytest.raises(LegacySuiteError, match="1024-bit limit"):
        polynomial_gap((Fraction(1 << 1025, 1), 0, 0))


def test_negative_shape_failures() -> None:
    with pytest.raises(LegacySuiteError, match="not three") as short:
        polynomial_gap((Fraction(3, 5), Fraction(4, 5)))
    assert short.value.parameters["length"] == 2

    with pytest.raises(LegacySuiteError, match="not three") as long:
        polynomial_gap((1, 2, 3, 4))
    assert long.value.parameters["length"] == 4

    with pytest.raises(LegacySuiteError, match="not a tuple") as listed:
        polynomial_gap([1, 2, 3])
    assert listed.value.parameters["received"] == "list"

    with pytest.raises(LegacySuiteError, match="not a tuple"):
        polynomial_gap("345")


def test_integration_matches_packet_norm() -> None:
    root = Path(__file__).resolve().parents[3]
    source = (root / "lean4" / "FiniteQM.lean").read_text(encoding="utf-8")
    assert "theorem unit_sphere_pythagorean_ray_witness" in source
    assert "theorem p2_sq_eq_p4_add_two_p22" in source
    pair = packet_norm((Fraction(3, 5), Fraction(4, 5)))
    assert pair == Fraction(1)
    assert certified_ray() == pair
    assert polynomial_gap(_RAY) == Fraction(0)
    assert suite_pass_count() == 3


def test_end_to_end_cli_prints_one() -> None:
    buffer = io.StringIO()
    with redirect_stdout(buffer):
        code = main()
    assert code == 0
    assert buffer.getvalue().strip() == "1"
    assert certified_ray() == Fraction(1)


def test_origin_resolves_in_repo() -> None:
    root = Path(__file__).resolve().parents[3]
    source = (root / "lean4" / "FiniteQM.lean").read_text(encoding="utf-8")
    assert "theorem unit_sphere_pythagorean_ray_witness" in source
    text = _MODULE_PATH.read_text(encoding="utf-8")
    assert "AuthorityEffect: None" in text
    assert "urn:omega:fqm:suite:pythagorean-ray:v1" in text
    assert "Scope Fence:" in text


_MUTANTS: tuple[tuple[str, str, str], ...] = (
    (
        "float amplitude admitted",
        "if issubclass(type(value), float):",
        "if False and issubclass(type(value), float):",
    ),
    (
        "boolean amplitude admitted",
        "if type(value) is bool:",
        "if False and type(value) is bool:",
    ),
    ("three-amplitude check dropped", "len(amplitudes) != 3", "len(amplitudes) != -1"),
    (
        "quadratic sum sign flipped",
        "_square(x_pos) + _square(y_pos) + _square(z_pos)",
        "_square(x_pos) + _square(y_pos) - _square(z_pos)",
    ),
    (
        "cross term sign flipped",
        "_square(y_pos) * _square(z_pos)",
        "_square(y_pos) + _square(z_pos)",
    ),
    ("degree check inverted", "if left != right:", "if left == right:"),
    (
        "cycle factor shifted",
        "Fraction(2, 3) * Fraction(3, 5) * Fraction(5, 2)",
        "Fraction(2, 3) * Fraction(3, 5) * Fraction(5, 3)",
    ),
    (
        "shear sum replaced by a difference",
        "Fraction(2, 3) + Fraction(4, 5)",
        "Fraction(2, 3) - Fraction(4, 5)",
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
    gap = namespace["polynomial_gap"]
    certified = namespace["certified_ray"]
    suite = namespace["suite_pass_count"]
    if not _all_hold((callable(gap), callable(certified), callable(suite),)):
        return False
    try:
        values = (
            gap(_RAY),
            gap((1, 2, 2)),
            gap((0, 0, 0)),
            certified(),
            suite(),
        )
    except error:
        return False
    return values == (Fraction(0), Fraction(0), Fraction(0), Fraction(1), 3)


def _bad_values_refused(namespace: dict[str, object], error: type[BaseException]) -> bool:
    gap = namespace["polynomial_gap"]
    if not callable(gap):
        return False
    probes = (
        (lambda: gap((_probe("0.6"), Fraction(4, 5), 0)), "float refused at the ray boundary"),
        (lambda: gap((True, 0, 0)), "boolean refused where a rational amplitude was required"),
        (lambda: gap(("3/5", Fraction(4, 5), 0)), "ray amplitude is not an exact rational"),
        (lambda: gap((Fraction(3, 5), Fraction(4, 5))), "ray amplitudes are not three"),
        (lambda: gap((1, 2, 3, 4)), "ray amplitudes are not three"),
        (lambda: gap([1, 2, 3]), "ray amplitudes are not a tuple"),
    )
    for probe, invariant in probes:
        if _invariant(error, probe) != invariant:
            return False
    return True


def _oracle(namespace: dict[str, object]) -> bool:
    error_type = namespace["LegacySuiteError"]
    if not _all_hold((isinstance(error_type, type), issubclass(error_type, BaseException),)):
        return False
    if not _known_values_hold(namespace, error_type):
        return False
    return _bad_values_refused(namespace, error_type)


def test_mutation_suite_kills_non_equivalent_mutants() -> None:
    source = _MODULE_PATH.read_text(encoding="utf-8")
    loaded: list[str] = []
    try:
        loaded.append("mutant_legacy_suites_baseline")
        baseline = _load_source(source, loaded[-1])
        assert _oracle(baseline) is True
        killed = 0
        for index, (name, old, new) in enumerate(_MUTANTS):
            count = source.count(old)
            assert count == 1, f"{name} matched {count} sites"
            module_name = f"mutant_legacy_suites_{index}"
            loaded.append(module_name)
            mutated = source.replace(old, new, 1)
            # Invalid Python is not a behavioral mutation kill.
            compile(mutated, module_name + ".py", "exec")
            try:
                namespace = _load_source(mutated, module_name)
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
