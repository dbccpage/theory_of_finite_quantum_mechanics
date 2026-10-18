"""Unit, negative, integration, end-to-end, and mutation tests for the payload checksum.

Origin: code/python/src/qm/packet_protocol.py
Claim: urn:omega:fqm:packet:payload-checksum:v1
AuthorityEffect: None
Mutation-Kills: 9 non-equivalent
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

from src.qm.packet_protocol import PacketProtocolError, certified_checksum, main, payload_checksum
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


_MODULE_PATH = Path(__file__).resolve().parents[1] / "src" / "qm" / "packet_protocol.py"
_FIXTURE = (Fraction(1, 2), Fraction(1, 3), Fraction(1, 7))


def test_fixture_checksum_is_forty_one_forty_seconds() -> None:
    assert payload_checksum(_FIXTURE) == Fraction(41, 42)
    assert payload_checksum((1,)) == Fraction(1)
    assert payload_checksum((1, 2)) == Fraction(3)
    assert payload_checksum((Fraction(1, 2),)) == Fraction(1, 2)
    assert certified_checksum() == Fraction(41, 42)
    assert type(payload_checksum((1,))) is Fraction


def test_negative_type_failures() -> None:
    with pytest.raises(PacketProtocolError, match="float refused") as floated:
        payload_checksum((_probe("1.0"), 1))
    assert floated.value.invariant == "float refused at the payload boundary"
    assert floated.value.parameters["index"] == 0
    assert type(floated.value) is PacketProtocolError

    with pytest.raises(PacketProtocolError, match="boolean refused") as boolean:
        payload_checksum((True,))
    assert boolean.value.invariant == "boolean refused where a rational entry was required"

    with pytest.raises(PacketProtocolError, match="not positive") as zero:
        payload_checksum((0, 1))
    assert zero.value.parameters["received"] == "0"

    with pytest.raises(PacketProtocolError, match="not positive") as negative:
        payload_checksum((Fraction(-1, 2), Fraction(1, 2)))
    assert negative.value.parameters["received"] == "-1/2"


def test_negative_shape_failures() -> None:
    with pytest.raises(PacketProtocolError, match="not an exact rational") as text:
        payload_checksum(("1",))
    assert text.value.parameters["received"] == "str"

    with pytest.raises(PacketProtocolError, match="not a tuple") as listed:
        payload_checksum([1, 2])
    assert listed.value.parameters["received"] == "list"

    with pytest.raises(PacketProtocolError, match="empty"):
        payload_checksum(())

    with pytest.raises(PacketProtocolError, match="not a tuple"):
        payload_checksum("12")


def test_integration_matches_associated_sum() -> None:
    root = Path(__file__).resolve().parents[3]
    source = (root / "lean4" / "H001Rats.lean").read_text(encoding="utf-8")
    assert "theorem padd_assoc" in source
    assert "theorem fadd_assoc" in source
    left = (Fraction(1, 2) + Fraction(1, 3)) + Fraction(1, 7)
    right = Fraction(1, 2) + (Fraction(1, 3) + Fraction(1, 7))
    assert left == right
    assert left == Fraction(41, 42)
    assert payload_checksum(_FIXTURE) == left
    pair = (Fraction(3, 5), Fraction(4, 5))
    assert payload_checksum(pair) == Fraction(7, 5)
    assert packet_norm(pair) == Fraction(1)


def test_end_to_end_cli_prints_checksum() -> None:
    buffer = io.StringIO()
    with redirect_stdout(buffer):
        code = main()
    assert code == 0
    assert buffer.getvalue().strip() == "41/42"
    assert certified_checksum() == Fraction(41, 42)


def test_origin_resolves_in_repo() -> None:
    root = Path(__file__).resolve().parents[3]
    source = (root / "lean4" / "H001Rats.lean").read_text(encoding="utf-8")
    assert "theorem padd_assoc" in source
    assert "theorem fadd_assoc" in source
    text = _MODULE_PATH.read_text(encoding="utf-8")
    assert "AuthorityEffect: None" in text
    assert "urn:omega:fqm:packet:payload-checksum:v1" in text
    assert "Scope Fence:" in text


_MUTANTS: tuple[tuple[str, str, str], ...] = (
    (
        "float entry admitted",
        "if isinstance(value, float):",
        "if isinstance(value, float):\n        return Fraction(0)\n    if False:",
    ),
    (
        "boolean entry admitted",
        "if type(value) is bool:",
        "if type(value) is bool:\n        return Fraction(1)\n    if False:",
    ),
    ("nonpositive entry admitted", "if entry <= 0:", "if entry < -1:"),
    ("empty payload admitted", "len(entries) == 0", "len(entries) == -1"),
    ("tuple check inverted", "not isinstance(entries, tuple)", "isinstance(entries, tuple)"),
    ("left fold keeps only the last entry", "total = total + entry", "total = entry"),
    ("right fold keeps only the current entry", "total = entry + total", "total = entry"),
    ("fold check inverted", "if left != right:", "if left == right:"),
    ("checksum constant shifted", "_CHECKSUM = Fraction(41, 42)", "_CHECKSUM = Fraction(1, 2)"),
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
    checksum = namespace["payload_checksum"]
    certified = namespace["certified_checksum"]
    if not _all_hold((callable(checksum), callable(certified),)):
        return False
    try:
        fixture = checksum(_FIXTURE)
        point = checksum((1,))
        pair = checksum((1, 2))
        half = checksum((Fraction(1, 2),))
        signed = certified()
    except error:
        return False
    actual = (fixture, point, pair, half, signed)
    expected = (Fraction(41, 42), Fraction(1), Fraction(3), Fraction(1, 2), Fraction(41, 42))
    return actual == expected


def _bad_values_refused(namespace: dict[str, object], error: type[BaseException]) -> bool:
    checksum = namespace["payload_checksum"]
    if not callable(checksum):
        return False
    probes = (
        (lambda: checksum((_probe("1.0"), 1)), "float refused at the payload boundary"),
        (lambda: checksum((True,)), "boolean refused where a rational entry was required"),
        (lambda: checksum((0, 1)), "payload entry is not positive"),
        (lambda: checksum((-1, 2)), "payload entry is not positive"),
        (lambda: checksum(()), "payload entries are empty"),
        (lambda: checksum([1, 2]), "payload entries are not a tuple"),
        (lambda: checksum(("1",)), "payload entry is not an exact rational"),
    )
    for probe, invariant in probes:
        if _invariant(error, probe) != invariant:
            return False
    return True


def _oracle(namespace: dict[str, object]) -> bool:
    error_type = namespace["PacketProtocolError"]
    if not _all_hold((isinstance(error_type, type), issubclass(error_type, BaseException),)):
        return False
    if not _known_values_hold(namespace, error_type):
        return False
    return _bad_values_refused(namespace, error_type)


def test_mutation_suite_kills_non_equivalent_mutants() -> None:
    source = _MODULE_PATH.read_text(encoding="utf-8")
    loaded: list[str] = []
    try:
        loaded.append("mutant_packet_protocol_baseline")
        baseline = _load_source(source, loaded[-1])
        assert _oracle(baseline) is True
        killed = 0
        for index, (name, old, new) in enumerate(_MUTANTS):
            count = source.count(old)
            assert count == 1, f"{name} matched {count} sites"
            module_name = f"mutant_packet_protocol_{index}"
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
