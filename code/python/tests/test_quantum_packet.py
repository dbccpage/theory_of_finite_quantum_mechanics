"""Unit, negative, integration, end-to-end, and mutation tests for the packet norm.

Origin: code/python/src/qm/quantum_packet.py
Claim: urn:omega:fqm:packet:pythagorean-norm:v1
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

from src.qm.entropy_bounds import collision_probability
from src.qm.quantum_packet import QuantumPacketError, certified_packet_norm, main, packet_norm

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


_MODULE_PATH = Path(__file__).resolve().parents[1] / "src" / "qm" / "quantum_packet.py"
_FIXTURE = (Fraction(3, 5), Fraction(4, 5))


def test_pythagorean_pair_has_unit_norm() -> None:
    assert packet_norm(_FIXTURE) == Fraction(1)
    assert packet_norm((1, 0)) == Fraction(1)
    assert packet_norm((1, 1)) == Fraction(2)
    assert packet_norm((Fraction(-3, 5), Fraction(4, 5))) == Fraction(1)
    assert packet_norm((0, 0)) == Fraction(0)
    assert certified_packet_norm() == Fraction(1)
    assert type(packet_norm(_FIXTURE)) is Fraction


def test_negative_type_failures() -> None:
    with pytest.raises(QuantumPacketError, match="float refused") as floated:
        packet_norm((_probe("1.0"), 0))
    assert floated.value.invariant == "float refused at the packet boundary"
    assert floated.value.parameters["index"] == 0
    assert type(floated.value) is QuantumPacketError

    with pytest.raises(QuantumPacketError, match="boolean refused") as boolean:
        packet_norm((True, 0))
    assert boolean.value.invariant == "boolean refused where a rational amplitude was required"

    with pytest.raises(QuantumPacketError, match="not an exact rational") as text:
        packet_norm(("3/5", Fraction(4, 5)))
    assert text.value.parameters["received"] == "str"

    with pytest.raises(QuantumPacketError, match="1024-bit limit"):
        packet_norm((1 << 1025, 0))

    with pytest.raises(QuantumPacketError, match="1024-bit limit"):
        packet_norm((Fraction(1 << 1025, 1), 0))


def test_negative_shape_failures() -> None:
    with pytest.raises(QuantumPacketError, match="not a tuple") as listed:
        packet_norm([Fraction(3, 5), Fraction(4, 5)])
    assert listed.value.parameters["received"] == "list"

    with pytest.raises(QuantumPacketError, match="not a pair") as short:
        packet_norm((1,))
    assert short.value.parameters["length"] == 1

    with pytest.raises(QuantumPacketError, match="not a pair") as long:
        packet_norm((1, 0, 0))
    assert long.value.parameters["length"] == 3

    with pytest.raises(QuantumPacketError, match="not a tuple"):
        packet_norm("35")


def test_integration_matches_pythagorean_ray() -> None:
    root = Path(__file__).resolve().parents[3]
    finite = (root / "lean4" / "FiniteQM.lean").read_text(encoding="utf-8")
    damping = (root / "lean4" / "FiniteQFTAndGravity.lean").read_text(encoding="utf-8")
    assert "theorem unit_sphere_pythagorean_ray_witness" in finite
    assert "theorem phase_damping_trace_preserving" in damping
    assert "theorem phase_damping_triples" in damping
    assert 3 * 3 + 4 * 4 == 5 * 5
    assert packet_norm(_FIXTURE) == Fraction(3 * 3 + 4 * 4, 5 * 5)
    squares = (Fraction(9, 25), Fraction(16, 25), Fraction(0))
    assert collision_probability(squares) == Fraction(337, 625)


def test_end_to_end_cli_prints_one() -> None:
    buffer = io.StringIO()
    with redirect_stdout(buffer):
        code = main()
    assert code == 0
    assert buffer.getvalue().strip() == "1"
    assert certified_packet_norm() == Fraction(1)


def test_origin_resolves_in_repo() -> None:
    root = Path(__file__).resolve().parents[3]
    finite = (root / "lean4" / "FiniteQM.lean").read_text(encoding="utf-8")
    damping = (root / "lean4" / "FiniteQFTAndGravity.lean").read_text(encoding="utf-8")
    assert "theorem unit_sphere_pythagorean_ray_witness" in finite
    assert "theorem phase_damping_triples" in damping
    text = _MODULE_PATH.read_text(encoding="utf-8")
    assert "AuthorityEffect: None" in text
    assert "urn:omega:fqm:packet:pythagorean-norm:v1" in text
    assert "Scope Fence:" in text


_MUTANTS: tuple[tuple[str, str, str], ...] = (
    (
        "float amplitude admitted",
        "if issubclass(type(value), float):",
        "if issubclass(type(value), float):\n        return Fraction(0)\n    if False:",
    ),
    (
        "boolean amplitude admitted",
        "if type(value) is bool:",
        "if type(value) is bool:\n        return Fraction(1)\n    if False:",
    ),
    ("pair length admitted", "len(amplitudes) != _WIDTH", "len(amplitudes) != -1"),
    ("tuple check inverted", "not isinstance(amplitudes, tuple)", "isinstance(amplitudes, tuple)"),
    ("direct square replaced by the amplitude", "return value * value", "return value"),
    ("born square replaced by the amplitude", "first = left * left", "first = left"),
    ("agreement check inverted", "if direct != born:", "if direct == born:"),
    ("unit constant shifted", "_UNIT = Fraction(1)", "_UNIT = Fraction(2)"),
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
    norm = namespace["packet_norm"]
    certified = namespace["certified_packet_norm"]
    if not _all_hold((callable(norm), callable(certified),)):
        return False
    try:
        unit = norm(_FIXTURE)
        axis = norm((1, 0))
        both = norm((1, 1))
        signed = norm((Fraction(-3, 5), Fraction(4, 5)))
        zero = norm((0, 0))
        checked = certified()
    except error:
        return False
    actual = (unit, axis, both, signed, zero, checked)
    expected = (Fraction(1), Fraction(1), Fraction(2), Fraction(1), Fraction(0), Fraction(1))
    return actual == expected


def _bad_values_refused(namespace: dict[str, object], error: type[BaseException]) -> bool:
    norm = namespace["packet_norm"]
    if not callable(norm):
        return False
    probes = (
        (lambda: norm((_probe("1.0"), 0)), "float refused at the packet boundary"),
        (lambda: norm((True, 0)), "boolean refused where a rational amplitude was required"),
        (lambda: norm(("3/5", 0)), "packet amplitude is not an exact rational"),
        (lambda: norm((1, 0, 0)), "packet amplitudes are not a pair"),
        (lambda: norm([1, 0]), "packet amplitudes are not a tuple"),
        (lambda: norm((1,)), "packet amplitudes are not a pair"),
    )
    for probe, invariant in probes:
        if _invariant(error, probe) != invariant:
            return False
    return True


def _oracle(namespace: dict[str, object]) -> bool:
    error_type = namespace["QuantumPacketError"]
    if not _all_hold((isinstance(error_type, type), issubclass(error_type, BaseException),)):
        return False
    if not _known_values_hold(namespace, error_type):
        return False
    return _bad_values_refused(namespace, error_type)


def test_mutation_suite_kills_non_equivalent_mutants() -> None:
    source = _MODULE_PATH.read_text(encoding="utf-8")
    loaded: list[str] = []
    try:
        loaded.append("mutant_quantum_packet_baseline")
        baseline = _load_source(source, loaded[-1])
        assert _oracle(baseline) is True
        killed = 0
        for index, (name, old, new) in enumerate(_MUTANTS):
            count = source.count(old)
            assert count == 1, f"{name} matched {count} sites"
            module_name = f"mutant_quantum_packet_{index}"
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
