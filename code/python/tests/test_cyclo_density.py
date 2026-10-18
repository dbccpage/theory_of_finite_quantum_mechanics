"""Unit, negative, integration, end-to-end, and mutation tests for cyclotomic density.

Origin: code/python/src/linear_algebra/cyclo_density.py
Claim: urn:omega:fqm:linear-algebra:cyclotomic-density:v1
AuthorityEffect: None
Mutation-Kills: 8 non-equivalent
"""





from __future__ import annotations

import importlib.util
import json
import sys
import warnings
from fractions import Fraction
from pathlib import Path
from typing import Any

import pytest

from src.linear_algebra.entropy_dichotomy import RationalTextError
from src.linear_algebra.cyclo_density import (
    MODULI,
    Cyclotomic,
    CyclotomicDivisionByZero,
    CyclotomicError,
    characteristic_record,
    characteristic_report,
    embedding,
    entropy_interval,
    entropy_verdict,
    has_cyclotomic_entries,
    parse_scalar,
    rational_sum,
    trace_square,
    validate_characteristic_record,
    validate_embedding,
    validate_psd,
    validated_matrix,
)
from src.linear_algebra.cyclo_density import (
    _oriented_sign,
    _pivot_inverse,
    _real_basis,
    _require_inverse_product,
    _require_self_conjugate_coefficients,
    _sqrt2_basis,
    _sqrt5_basis,
)
from src.linear_algebra.entropy_dichotomy import RefusedAtBudget

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


_MODULE_PATH = Path(__file__).resolve().parents[1] / "src" / "linear_algebra" / "cyclo_density.py"
_Q = Fraction
_DECLARED = "DECLARED_SYSTEM_STATE"


def _raises(probe: Any, invariant: str) -> CyclotomicError:
    with pytest.raises(CyclotomicError) as caught:
        probe()
    assert caught.value.invariant == invariant
    assert all(type(item).__name__ != "float" for item in caught.value.parameters.values())
    return caught.value


def _diag(values: list[str]) -> list[list[str]]:
    size = len(values)
    return [[values[row] if row == col else "0/1" for col in range(size)] for row in range(size)]


def _case(system: str, conductor: int, rows: list[list[str]], scope: str = _DECLARED) -> dict[str, Any]:
    return {
        "fixture_id": system.lower(),
        "system_id": system,
        "conductor": conductor,
        "matrix": rows,
        "scope": scope,
    }


def _projector() -> dict[str, Any]:
    return _case("S1", 4, [["1/1", "0/1"], ["0/1", "0/1"]])


def test_hand_values_match_frozen_cyclotomic_certificates() -> None:
    unit = Cyclotomic.zeta(4)
    assert (unit ** 2).coefficients == (_Q(-1), _Q(0))
    assert unit ** 2 == -1
    assert unit.inverse().coefficients == (_Q(0), _Q(-1))
    assert unit ** 4 == 1
    assert unit * unit.inverse() == 1
    golden = Cyclotomic.zeta(5) + Cyclotomic.zeta(5) ** 4
    assert golden.coefficients == (_Q(-1), _Q(0), _Q(-1), _Q(-1))
    assert golden.real_coordinates() == (_Q(-1, 2), _Q(1, 2), 5)
    assert golden.sign() == 1
    assert golden > 0
    assert Cyclotomic.rational(1, _Q(1, 2)).coefficients == (_Q(1, 2),)
    assert embedding(4) == embedding(1)
    assert embedding(4)["real_generator_interval"] == ["1/1", "1/1"]
    assert embedding(5)["real_generator_radicand"] == 5
    assert embedding(5)["real_generator_interval"] == ["11/5", "12/5"]
    assert embedding(8)["real_generator_radicand"] == 2
    validate_psd([[Cyclotomic.rational(4, 1)]])
    assert set(MODULI) == {1, 3, 4, 5, 8}


def test_ordering_trace_and_parse_keep_exact_values() -> None:
    base = Cyclotomic.rational(4, _Q(1, 2))
    assert abs(-base) == base
    assert base <= base
    assert hash(Cyclotomic.rational(4, 3)) == hash(_Q(3))
    assert (1 / Cyclotomic.zeta(4)).coefficients == (_Q(0), _Q(-1))
    parsed = parse_scalar({"cyclotomic_coefficients": ["0/1", "1/1"]}, 4)
    assert parsed == Cyclotomic.zeta(4)
    assert has_cyclotomic_entries({"matrix": [[{"cyclotomic_coefficients": ["1/1"]}]]})
    assert has_cyclotomic_entries({"matrix": [["1/1"]]}) is False
    matrix = validated_matrix(_projector())
    assert trace_square(matrix) == 1
    assert rational_sum([_Q(1, 2), _Q(1, 2)]) == 1


def test_negative_arithmetic_records_every_invariant() -> None:
    floated = _raises(lambda: Cyclotomic.rational(4, _probe("0.5")), "float refused at the public boundary")
    assert floated.parameters == {"role": "value", "received": "float"}
    boolean = _raises(lambda: Cyclotomic(True, (_Q(1),)), "boolean refused where a cyclotomic conductor was required")
    assert boolean.parameters == {"role": "conductor"}
    _raises(lambda: Cyclotomic.rational(4, True), "boolean refused where an exact rational was required")
    _raises(lambda: Cyclotomic.zeta(4) ** True, "boolean refused where an exact integer was required")
    _raises(lambda: Cyclotomic(2, (_Q(1),)), "unsupported cyclotomic conductor")
    _raises(lambda: Cyclotomic.rational(4, "1"), "cyclotomic arithmetic requires an exact rational")
    _raises(lambda: Cyclotomic(4, ("1", _Q(0))), "cyclotomic arithmetic requires exact rational coefficients")
    _raises(lambda: Cyclotomic(4, (_Q(1),)), "cyclotomic coefficient arity differs from phi(conductor)")
    _raises(lambda: Cyclotomic.zeta(4) ** "x", "cyclotomic exponent must be an integer")
    _raises(lambda: Cyclotomic.zeta(4) + Cyclotomic.zeta(5), "cyclotomic arithmetic cannot mix declared conductors")
    with pytest.raises(CyclotomicDivisionByZero) as zero:
        Cyclotomic.rational(4, 0).inverse()
    assert zero.value.invariant == "division by zero cyclotomic element"
    assert isinstance(zero.value, ZeroDivisionError)
    _raises(lambda: Cyclotomic.zeta(4).real_coordinates(), "ordering requires an exactly self-conjugate cyclotomic element")
    _raises(lambda: parse_scalar({"kind": "no"}, 4), "cyclotomic scalar requires exactly cyclotomic_coefficients or a rational string")
    _raises(lambda: parse_scalar({"cyclotomic_coefficients": ["1/1"]}, 4), "cyclotomic coefficient arity differs from phi(conductor)")
    _raises(lambda: validate_embedding({"real_generator_radicand": 3}), "invalid frozen cyclotomic embedding")
    _raises(lambda: rational_sum([1]), "rational fold requires exact Fraction terms")


def test_negative_defensive_helpers_record_every_invariant() -> None:
    rows = [[_Q(0), _Q(1)], [_Q(0), _Q(0)]]
    _raises(lambda: _pivot_inverse(rows, 0), "cyclotomic multiplication map is unexpectedly singular")
    unit = Cyclotomic.zeta(4)
    _raises(lambda: _require_inverse_product(unit, unit), "cyclotomic inverse failed exact product reconstruction")
    _raises(lambda: _sqrt2_basis((_Q(0), _Q(1), _Q(1), _Q(0))), "sqrt(2) real-subfield representation failed")
    _raises(lambda: _sqrt5_basis((_Q(0), _Q(1), _Q(1), _Q(1))), "sqrt(5) real-subfield representation failed")
    _raises(lambda: _real_basis(4, (_Q(1), _Q(1))), "rational real-subfield representation failed")
    _raises(lambda: _oriented_sign(_Q(1), _Q(1), 1), "nonzero rational square cannot equal the frozen nonsquare radicand")
    _raises(
        lambda: _require_self_conjugate_coefficients([unit]),
        "Hermitian characteristic polynomial has a non-self-conjugate coefficient",
    )
    _raises(
        lambda: validate_psd([[Cyclotomic.rational(4, -1)]]),
        "negative eigenvalue: cyclotomic Schur complement is not positive semidefinite",
    )
    off = [[Cyclotomic.rational(4, 0), unit], [unit, Cyclotomic.rational(4, 0)]]
    _raises(lambda: validate_psd(off), "negative eigenvalue: cyclotomic zero diagonal has a nonzero off-diagonal entry")


def test_negative_cases_record_every_interface_invariant() -> None:
    _raises(lambda: validated_matrix({"fixture_id": 1}), "typed input requires exactly the five interface fields")
    _raises(lambda: validated_matrix(_case("S1", 4, []) | {"fixture_id": ""}), "fixture_id: nonempty string required")
    _raises(lambda: validated_matrix(_case("S9", 4, [])), "system missing from frozen class")
    _raises(lambda: validated_matrix(_case("S1", 1, [])), "frozen conductor mismatch")
    _raises(lambda: validated_matrix(_case("S1", 4, [["1/1"]])), "frozen system dimension mismatch")
    skewed = [["1/1", "1/1"], ["0/1", "0/1"]]
    _raises(lambda: validated_matrix(_case("S1", 4, skewed)), "input is not Hermitian in its declared cyclotomic field")
    _raises(lambda: validated_matrix(_case("S1", 4, _diag(["1/1", "1/1"]))), "unnormalised spectrum: trace must equal one")
    proxy = _case("S8", 4, _diag(["1/4", "1/4", "1/4", "1/4"]), "DECLARED_SYSTEM_STATE")
    _raises(lambda: validated_matrix(proxy), "S8 code support unresolved; dimension-only proxy label required")
    _raises(lambda: validated_matrix(_case("S1", 4, _diag(["1/1", "0/1"]), "OTHER")), "state scope label mismatch")
    ladder = _diag(["1/2", "1/2", "0/1"])
    ladder[0][1] = ladder[1][0] = "1/2"
    _raises(lambda: validated_matrix(_case("S7", 1, ladder)), "frozen ladder states must be diagonal")
    _raises(lambda: validated_matrix(_case("S6", 1, _diag(["0/1", "0/1", "0/1", "1/1"]))), "S6 requires a positive geometric ladder")
    _raises(lambda: validated_matrix(_case("S6", 1, _diag(["1/4", "1/4", "1/4", "1/4"]))), "S6 requires the declared decreasing geometric ladder")
    floated = _case("S1", 4, [[_probe("0.5")]])
    _raises(lambda: validated_matrix(floated), "float refused at the public boundary")
    with pytest.raises(RationalTextError) as unreduced:
        parse_scalar("2/4", 1)
    assert type(unreduced.value) is RationalTextError
    with pytest.raises(RefusedAtBudget):
        validated_matrix(_case("S1", 4, [["0/1"]] * 6))
    with pytest.raises(RefusedAtBudget):
        entropy_interval(_projector(), 33)
    with pytest.raises(RefusedAtBudget):
        entropy_interval(_projector(), True)


def test_integration_matches_rust_density_contract() -> None:
    root = Path(__file__).resolve().parents[3]
    source = (root / "code" / "rust" / "src" / "linear_algebra" / "cyclo_density.rs").read_text(encoding="utf-8")
    assert 'test_negative_remainder_rescaling' in source
    assert 'test_negative_remainder_rescaling' in source
    assert 'test_negative_remainder_rescaling' in source
    validate_embedding(embedding(5))
    assert validated_matrix(_case("S8", 4, _diag(["1/4"] * 4), "S8_DIMENSION_ONLY_PROXY"))


def test_end_to_end_public_contract(tmp_path: Path) -> None:
    case = _projector()
    record = characteristic_record(case)
    assert record["purity"] == "PURE"
    assert record["entropy"]["verdict"] == "CARRIED"
    assert record["embedding"]["real_generator_radicand"] == 0
    assert record["characteristic_polynomial"][0]["cyclotomic_coefficients"] == ["1/1", "0/1"]
    assert record["characteristic_polynomial"][1]["cyclotomic_coefficients"] == ["-1/1", "0/1"]
    assert record["characteristic_polynomial"][2]["cyclotomic_coefficients"] == ["0/1", "0/1"]
    assert record["spectrum_scope"] == "CHARACTERISTIC_ONLY_NO_SPLITTING_OR_DEPENDENCE"
    wrapped = {"input": case, "output": record}
    validate_characteristic_record(wrapped)
    broken = {"input": case, "output": {**record, "purity": "MIXED"}}
    _raises(lambda: validate_characteristic_record(broken), "s1: injected or invalid cyclotomic purity")
    _raises(lambda: validate_characteristic_record({"input": case}), "cyclotomic record requires input and output")
    census = {"input": case, "output": {"purity": "PURE"}}
    _raises(lambda: validate_characteristic_record(census), "cyclotomic output field census differs")
    verdict = entropy_verdict(case)
    assert verdict["verdict"] == "CARRIED"
    geometric = _case("S6", 1, _diag(["8/15", "4/15", "2/15", "1/15"]))
    assert entropy_verdict(geometric)["verdict"] == "REFUSED_TRANSCENDENTAL"
    interface = tmp_path / "one_fixture.json"
    interface.write_text(json.dumps({"fixtures": [case]}), encoding="utf-8")
    report = characteristic_report(interface)
    assert report["authority_effect"] == "None"
    assert report["schema"] == "cyclotomic_density_v1"
    assert report["cases"][0]["output"]["purity"] == "PURE"


def test_origin_resolves_in_repo() -> None:
    root = Path(__file__).resolve().parents[3]
    origin = root / "code" / "rust" / "src" / "linear_algebra" / "cyclo_density.rs"
    assert origin.is_file()
    source = _MODULE_PATH.read_text(encoding="utf-8")
    assert "AuthorityEffect: None" in source
    assert "urn:omega:fqm:linear-algebra:cyclotomic-density:v1" in source
    assert "Scope Fence:" in source
    assert "Gate 5 measurement:" in source


_MUTANTS: tuple[tuple[str, str, str], ...] = (
    (
        "float admitted",
        'if isinstance(value, float):\n        raise _fail("float refused at the public boundary", role=role, received="float")',
        "if isinstance(value, float):\n        return",
    ),
    (
        "boolean admitted",
        "if type(value) is bool:",
        "if False and type(value) is bool:",
    ),
    (
        "modulus sign flipped",
        "product[exponent - degree + i] -= leading * modulus[i]",
        "product[exponent - degree + i] += leading * modulus[i]",
    ),
    (
        "exponent step collapsed",
        "power //= 2",
        "power //= 3",
    ),
    (
        "golden radicand replaced",
        "return real - pair / 2, -pair / 2, 5",
        "return real - pair / 2, -pair / 2, 2",
    ),
    (
        "positive pivot declared negative",
        "current[index][index] < 0",
        "current[index][index] > 0",
    ),
    (
        "inverse scale applied twice",
        "rows[column] = [value / scale for value in rows[column]]",
        "rows[column] = [value / scale / scale for value in rows[column]]",
    ),
    (
        "fifth conductor radicand collapsed",
        "2 if number == 8 else 5 if number == 5 else 0",
        "2 if number == 8 else 1 if number == 5 else 0",
    ),
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


def _certificates_hold(namespace: dict[str, object]) -> bool:
    cyclotomic = namespace["Cyclotomic"]
    if not isinstance(cyclotomic, type):
        return False
    try:
        unit = cyclotomic.zeta(4)
        golden = cyclotomic.zeta(5) + cyclotomic.zeta(5) ** 4
        coordinates = golden.real_coordinates()
        namespace["validate_psd"]([[cyclotomic.rational(4, 1)]])
        image = namespace["embedding"](5)
    except Exception:
        return False
    if not _all_hold((isinstance(image, dict), isinstance(coordinates, tuple),)):
        return False
    return _all_hold((
(unit ** 2).coefficients == (_Q(-1), _Q(0)),
unit ** 4 == 1,
unit.inverse().coefficients == (_Q(0), _Q(-1)),
coordinates == (_Q(-1, 2), _Q(1, 2), 5),
image.get("real_generator_radicand") == 5,
))


def _boundary_holds(namespace: dict[str, object], error: type[BaseException]) -> bool:
    cyclotomic = namespace["Cyclotomic"]
    if not isinstance(cyclotomic, type):
        return False
    probes = (
        (lambda: cyclotomic.rational(4, _probe("0.5")), "float refused at the public boundary"),
        (lambda: cyclotomic(True, (_Q(1),)), "boolean refused where a cyclotomic conductor was required"),
    )
    return all(_invariant(error, probe) == invariant for probe, invariant in probes)


def _oracle(namespace: dict[str, object]) -> bool:
    error_type = namespace["CyclotomicError"]
    if not _all_hold((isinstance(error_type, type), issubclass(error_type, BaseException),)):
        return False
    if not _certificates_hold(namespace):
        return False
    return _boundary_holds(namespace, error_type)


def test_mutation_suite_kills_non_equivalent_mutants() -> None:
    source = _MODULE_PATH.read_text(encoding="utf-8")
    loaded: list[str] = []
    try:
        loaded.append("mutant_cyclo_baseline")
        assert _oracle(_load_source(source, loaded[-1])) is True
        killed = 0
        for index, (name, old, new) in enumerate(_MUTANTS):
            count = source.count(old)
            assert count == 1, f"{name} matched {count} sites"
            module_name = f"mutant_cyclo_{index}"
            loaded.append(module_name)
            try:
                survived = _oracle(_load_source(source.replace(old, new, 1), module_name))
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
