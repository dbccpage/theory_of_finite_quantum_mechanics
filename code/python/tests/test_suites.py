"""Unit, negative, integration, end-to-end, and mutation tests for the named suites.

Origin: code/python/src/qm/suites.py
Claim: urn:omega:fqm:suite:named-norm:v1
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

from src.qm.quantum_packet import packet_norm
from src.qm.suites import SuiteError, main, ray_norm, run_local_suite, witness_gap

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


_MODULE_PATH = Path(__file__).resolve().parents[1] / "src" / "qm" / "suites.py"
_RAY = (Fraction(3, 5), Fraction(4, 5), Fraction(0))


def test_named_suites_match_their_closed_forms() -> None:
    assert ray_norm(_RAY) == Fraction(1)
    assert ray_norm((1, 2, 2)) == Fraction(9)
    assert witness_gap(_RAY) == Fraction(0)
    assert witness_gap((1, 2, 2)) == Fraction(0)
    assert run_local_suite("norm") == Fraction(1)
    assert run_local_suite("cycle") == Fraction(1)
    assert type(run_local_suite("norm")) is Fraction


def test_negative_type_failures() -> None:
    with pytest.raises(SuiteError, match="float refused") as floated:
        ray_norm((_probe("0.6"), Fraction(4, 5), 0))
    assert floated.value.invariant == "float refused at the ray boundary"
    assert floated.value.parameters["index"] == 0
    assert type(floated.value) is SuiteError

    with pytest.raises(SuiteError, match="boolean refused") as boolean:
        ray_norm((True, 0, 0))
    assert boolean.value.invariant == "boolean refused where a rational amplitude was required"

    with pytest.raises(SuiteError, match="not an exact rational") as text:
        ray_norm(("3/5", Fraction(4, 5), 0))
    assert text.value.parameters["received"] == "str"

    with pytest.raises(SuiteError, match="not a string") as named:
        run_local_suite(1)
    assert named.value.parameters["received"] == "int"


def test_negative_shape_failures() -> None:
    with pytest.raises(SuiteError, match="not three") as short:
        ray_norm((Fraction(3, 5), Fraction(4, 5)))
    assert short.value.parameters["length"] == 2

    with pytest.raises(SuiteError, match="not three") as long:
        witness_gap((1, 2, 3, 4))
    assert long.value.parameters["length"] == 4

    with pytest.raises(SuiteError, match="not a tuple") as listed:
        ray_norm([1, 2, 3])
    assert listed.value.parameters["received"] == "list"

    with pytest.raises(SuiteError, match="unknown suite") as unknown:
        run_local_suite("shear")
    assert unknown.value.parameters["name"] == "shear"


def test_integration_matches_packet_norm() -> None:
    root = Path(__file__).resolve().parents[3]
    source = (root / "lean4" / "FiniteQM.lean").read_text(encoding="utf-8")
    assert "theorem unit_sphere_pythagorean_ray_witness" in source
    assert "theorem p2_sq_eq_p4_add_two_p22" in source
    pair = packet_norm((Fraction(3, 5), Fraction(4, 5)))
    assert pair == Fraction(1)
    assert run_local_suite("norm") == pair
    assert witness_gap(_RAY) == Fraction(0)
    assert run_local_suite("cycle") == Fraction(1)


def test_end_to_end_cli_prints_one() -> None:
    buffer = io.StringIO()
    with redirect_stdout(buffer):
        code = main()
    assert code == 0
    assert buffer.getvalue().strip() == "1"
    assert run_local_suite("norm") == Fraction(1)


def test_origin_resolves_in_repo() -> None:
    root = Path(__file__).resolve().parents[3]
    source = (root / "lean4" / "FiniteQM.lean").read_text(encoding="utf-8")
    assert "theorem unit_sphere_pythagorean_ray_witness" in source
    text = _MODULE_PATH.read_text(encoding="utf-8")
    assert "AuthorityEffect: None" in text
    assert "urn:omega:fqm:suite:named-norm:v1" in text
    assert "Scope Fence:" in text


_MUTANTS: tuple[tuple[str, str, str], ...] = (
    (
        "float amplitude admitted",
        "if isinstance(value, float):",
        "if False and isinstance(value, float):",
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
    ("degree check inverted", "if left != right:", "if left == right:"),
    ("norm name shifted", 'if checked == "norm":', 'if checked == "norms":'),
    (
        "cycle factor shifted",
        "Fraction(2, 3) * Fraction(3, 5) * Fraction(5, 2)",
        "Fraction(2, 3) * Fraction(3, 5) * Fraction(5, 3)",
    ),
    ("tuple check inverted", "not isinstance(amplitudes, tuple)", "isinstance(amplitudes, tuple)"),
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
    norm = namespace["ray_norm"]
    gap = namespace["witness_gap"]
    suite = namespace["run_local_suite"]
    if not _all_hold((callable(norm), callable(gap), callable(suite),)):
        return False
    try:
        values = (
            norm(_RAY),
            norm((1, 2, 2)),
            gap(_RAY),
            gap((1, 2, 2)),
            suite("norm"),
            suite("cycle"),
        )
    except error:
        return False
    return values == (Fraction(1), Fraction(9), Fraction(0), Fraction(0), Fraction(1), Fraction(1))


def _bad_values_refused(namespace: dict[str, object], error: type[BaseException]) -> bool:
    norm = namespace["ray_norm"]
    gap = namespace["witness_gap"]
    suite = namespace["run_local_suite"]
    if not _all_hold((callable(norm), callable(gap), callable(suite),)):
        return False
    probes = (
        (lambda: norm((_probe("0.6"), Fraction(4, 5), 0)), "float refused at the ray boundary"),
        (lambda: norm((True, 0, 0)), "boolean refused where a rational amplitude was required"),
        (lambda: norm(("3/5", Fraction(4, 5), 0)), "ray amplitude is not an exact rational"),
        (lambda: norm((Fraction(3, 5), Fraction(4, 5))), "ray amplitudes are not three"),
        (lambda: gap((1, 2, 3, 4)), "ray amplitudes are not three"),
        (lambda: norm([1, 2, 3]), "ray amplitudes are not a tuple"),
        (lambda: suite("shear"), "unknown suite"),
    )
    for probe, invariant in probes:
        if _invariant(error, probe) != invariant:
            return False
    return True


def _oracle(namespace: dict[str, object]) -> bool:
    error_type = namespace["SuiteError"]
    if not _all_hold((isinstance(error_type, type), issubclass(error_type, BaseException),)):
        return False
    if not _known_values_hold(namespace, error_type):
        return False
    return _bad_values_refused(namespace, error_type)


def test_mutation_suite_kills_non_equivalent_mutants() -> None:
    source = _MODULE_PATH.read_text(encoding="utf-8")
    loaded: list[str] = []
    try:
        loaded.append("mutant_suites_baseline")
        baseline = _load_source(source, loaded[-1])
        assert _oracle(baseline) is True
        killed = 0
        for index, (name, old, new) in enumerate(_MUTANTS):
            count = source.count(old)
            assert count == 1, f"{name} matched {count} sites"
            module_name = f"mutant_suites_{index}"
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
