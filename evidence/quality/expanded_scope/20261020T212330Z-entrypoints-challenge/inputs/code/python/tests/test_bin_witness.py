"""Unit, negative, integration, end-to-end, and mutation tests for the bin ray.

Origin: code/python/src/bin/__init__.py
Claim: urn:omega:fqm:bin:pythagorean-ray:v1
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

from src.bin import BinWitnessError, bin_two_square, main, ray_power_two
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


_MODULE_PATH = Path(__file__).resolve().parents[1] / "src" / "bin" / "__init__.py"
_RAY = (Fraction(3, 5), Fraction(4, 5), Fraction(0))


def test_pythagorean_ray_matches_the_theorem() -> None:
    assert bin_two_square() == Fraction(1)
    assert ray_power_two() == Fraction(1)
    assert ray_power_two((1, 2, 2)) == Fraction(9)
    assert ray_power_two((0, 0, 0)) == Fraction(0)
    assert type(bin_two_square()) is Fraction


def test_negative_type_failures() -> None:
    with pytest.raises(BinWitnessError, match="float refused") as floated:
        ray_power_two((_probe("0.6"), Fraction(4, 5), 0))
    assert floated.value.invariant == "float refused at the ray boundary"
    assert floated.value.parameters["index"] == 0
    assert type(floated.value) is BinWitnessError

    with pytest.raises(BinWitnessError, match="boolean refused") as boolean:
        ray_power_two((True, 0, 0))
    assert boolean.value.invariant == "boolean refused where a rational amplitude was required"

    with pytest.raises(BinWitnessError, match="not an exact rational") as text:
        ray_power_two(("3/5", Fraction(4, 5), 0))
    assert text.value.parameters["received"] == "str"


def test_negative_shape_failures() -> None:
    with pytest.raises(BinWitnessError, match="not three") as short:
        ray_power_two((Fraction(3, 5), Fraction(4, 5)))
    assert short.value.parameters["length"] == 2

    with pytest.raises(BinWitnessError, match="not three") as long:
        ray_power_two((1, 2, 3, 4))
    assert long.value.parameters["length"] == 4

    with pytest.raises(BinWitnessError, match="not a tuple") as listed:
        ray_power_two([1, 2, 3])
    assert listed.value.parameters["received"] == "list"


def test_integration_matches_packet_norm() -> None:
    root = Path(__file__).resolve().parents[3]
    source = (root / "lean4" / "FiniteQM.lean").read_text(encoding="utf-8")
    assert "theorem unit_sphere_pythagorean_ray_witness" in source
    pair = packet_norm((Fraction(3, 5), Fraction(4, 5)))
    assert pair == Fraction(1)
    assert ray_power_two() == pair
    assert bin_two_square() == pair


def test_end_to_end_cli_prints_one() -> None:
    stdout = io.StringIO()
    with redirect_stdout(stdout):
        code = main()
    assert code == 0
    assert stdout.getvalue() == "1\n"


def test_origin_resolves_in_repo() -> None:
    source = _MODULE_PATH.read_text(encoding="utf-8")
    assert "Origin: lean4/FiniteQM.lean theorem unit_sphere_pythagorean_ray_witness" in source
    assert "Claim: urn:omega:fqm:bin:pythagorean-ray:v1" in source
    assert "AuthorityEffect: None" in source
    assert "Scope Fence:" in source


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
        "square product widened",
        "return value * value",
        "return value + value",
    ),
    (
        "fourth constant shifted",
        "_FOURTH = Fraction(337, 625)",
        "_FOURTH = Fraction(337, 626)",
    ),
    (
        "degree relation inverted",
        "if fourth != _UNIT - 2 * cross:",
        "if fourth == _UNIT - 2 * cross:",
    ),
    ("tuple check inverted", "not issubclass(type(amplitudes), tuple)", "issubclass(type(amplitudes), tuple)"),
)


def _load_source(source: str, name: str) -> dict[str, object]:
    spec = importlib.util.spec_from_loader(name, loader=None)
    if spec is None:
        raise RuntimeError("could not allocate a mutant module spec")
    module = importlib.util.module_from_spec(spec)
    module.__package__ = "src.bin"
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
    power = namespace["ray_power_two"]
    witness = namespace["bin_two_square"]
    if not _all_hold((callable(power), callable(witness),)):
        return False
    try:
        values = (witness(), power(), power((1, 2, 2)), power((0, 0, 0)))
    except error:
        return False
    return values == (Fraction(1), Fraction(1), Fraction(9), Fraction(0))


def _bad_values_refused(namespace: dict[str, object], error: type[BaseException]) -> bool:
    power = namespace["ray_power_two"]
    if not callable(power):
        return False
    probes = (
        (lambda: power((_probe("0.6"), Fraction(4, 5), 0)), "float refused at the ray boundary"),
        (lambda: power((True, 0, 0)), "boolean refused where a rational amplitude was required"),
        (lambda: power(("3/5", Fraction(4, 5), 0)), "ray amplitude is not an exact rational"),
        (lambda: power((Fraction(3, 5), Fraction(4, 5))), "ray amplitudes are not three"),
        (lambda: power((1, 2, 3, 4)), "ray amplitudes are not three"),
        (lambda: power([1, 2, 3]), "ray amplitudes are not a tuple"),
    )
    for probe, invariant in probes:
        if _invariant(error, probe) != invariant:
            return False
    return True


def _oracle(namespace: dict[str, object]) -> bool:
    error_type = namespace["BinWitnessError"]
    if not _all_hold((isinstance(error_type, type), issubclass(error_type, BaseException),)):
        return False
    if not _known_values_hold(namespace, error_type):
        return False
    return _bad_values_refused(namespace, error_type)


def test_mutation_suite_kills_non_equivalent_mutants() -> None:
    source = _MODULE_PATH.read_text(encoding="utf-8")
    loaded: list[str] = []
    try:
        loaded.append("mutant_bin_witness_baseline")
        baseline = _load_source(source, loaded[-1])
        assert _oracle(baseline) is True
        killed = 0
        for index, (name, old, new) in enumerate(_MUTANTS):
            count = source.count(old)
            assert count == 1, f"{name} matched {count} sites"
            module_name = f"mutant_bin_witness_{index}"
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
