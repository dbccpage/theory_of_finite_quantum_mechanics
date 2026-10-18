"""Unit, negative, integration, end-to-end, and mutation tests for spectral binding.

Origin: code/python/src/linear_algebra/spectral_factors.py
Claim: urn:omega:fqm:linear-algebra:spectral-factor-binding:v1
AuthorityEffect: None
Mutation-Kills: 8 non-equivalent
"""



from __future__ import annotations

import copy
import importlib.util
import io
import json
import sys
import warnings
from pathlib import Path
from typing import Any

import pytest

import src.linear_algebra as linear_algebra
from src.linear_algebra.entropy_dichotomy import fixtures
from src.linear_algebra.spectral_factors import (
    SpectralBindingError,
    bind_spectral_factors,
    dispatch,
    validate_spectral_factor_binding,
)
from src.linear_algebra import spectral_factors

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


_MODULE_PATH = Path(__file__).resolve().parents[1] / "src" / "linear_algebra" / "spectral_factors.py"

PURE: dict[str, Any] = {
    "fixture_id": "s1_pure",
    "system_id": "S1",
    "conductor": 4,
    "matrix": [["1/1", "0/1"], ["0/1", "0/1"]],
    "scope": "DECLARED_SYSTEM_STATE",
}
MIXED: dict[str, Any] = {
    "fixture_id": "s1_mixed_half",
    "system_id": "S1",
    "conductor": 4,
    "matrix": [["1/2", "0/1"], ["0/1", "1/2"]],
    "scope": "DECLARED_SYSTEM_STATE",
}
SQRT2: dict[str, Any] = {
    "fixture_id": "s1_sqrt2",
    "system_id": "S1",
    "conductor": 4,
    "matrix": [["5/8", "1/8"], ["1/8", "3/8"]],
    "scope": "DECLARED_SYSTEM_STATE",
}


def _assignments(certificate: dict[str, Any]) -> list[tuple[Any, Any, Any]]:
    rows = certificate["root_assignments"]
    assert isinstance(rows, list)
    return [(row["root_index"], row["factor_index"], row["multiplicity"]) for row in rows]


def test_hand_bindings_for_rational_and_quadratic_spectra() -> None:
    pure = bind_spectral_factors(PURE)
    assert pure["schema"] == "spectral_factor_binding_v1"
    assert pure["authority_effect"] == "None"
    assert pure["coefficient_field"] == "Q"
    assert pure["real_generator_radicand"] == 0
    assert pure["characteristic_polynomial"] == [["1/1", "0/1"], ["-1/1", "0/1"], ["0/1", "0/1"]]
    assert pure["factorization"]["factors"] == [
        {"polynomial": [["1/1", "0/1"], ["-1/1", "0/1"]], "multiplicity": 1},
        {"polynomial": [["1/1", "0/1"], ["0/1", "0/1"]], "multiplicity": 1},
    ]
    assert _assignments(pure) == [(0, 1, 1), (1, 0, 1)]
    assert pure["factor_root_counts"] == [1, 1]
    assert pure["carrier_transport"]["carrier_degree_over_real_field"] == 2
    assert pure["carrier_transport"]["all_roots_real"] is True
    validate_spectral_factor_binding(PURE, pure)

    mixed = bind_spectral_factors(MIXED)
    assert mixed["factorization"]["factors"] == [
        {"polynomial": [["1/1", "0/1"], ["-1/2", "0/1"]], "multiplicity": 2},
    ]
    assert _assignments(mixed) == [(0, 0, 2)]
    assert mixed["factor_root_counts"] == [1]
    validate_spectral_factor_binding(MIXED, mixed)

    algebraic = bind_spectral_factors(SQRT2)
    assert algebraic["characteristic_polynomial"][2] == ["7/32", "0/1"]
    assert _assignments(algebraic) == [(0, 0, 1), (1, 0, 1)]
    assert algebraic["factor_root_counts"] == [2]
    validate_spectral_factor_binding(SQRT2, algebraic)


def test_negative_boundary_and_certificate_failures() -> None:
    floated = copy.deepcopy(PURE)
    floated["matrix"][0][0] = _probe("1.5")
    with pytest.raises(SpectralBindingError, match="float refused") as float_error:
        bind_spectral_factors(floated)
    assert float_error.value.invariant == "float refused at the public boundary"
    assert float_error.value.parameters == {"role": "input", "received": "float"}

    published = bind_spectral_factors(PURE)
    boolean = copy.deepcopy(published)
    boolean["root_assignments"][0]["multiplicity"] = True
    with pytest.raises(SpectralBindingError, match="boolean refused") as boolean_error:
        validate_spectral_factor_binding(PURE, boolean)
    assert boolean_error.value.parameters["role"] == "multiplicity"

    with pytest.raises(SpectralBindingError, match="typed input object required"):
        bind_spectral_factors(["not", "a", "case"])

    with pytest.raises(SpectralBindingError, match="exact result field census required"):
        validate_spectral_factor_binding(PURE, {})

    renamed = copy.deepcopy(published)
    renamed["schema"] = "other"
    with pytest.raises(SpectralBindingError, match="metadata or coefficient-field binding differs") as schema:
        validate_spectral_factor_binding(PURE, renamed)
    assert schema.value.parameters["field"] == "schema"

    rebound = copy.deepcopy(published)
    rebound["input"] = copy.deepcopy(MIXED)
    with pytest.raises(SpectralBindingError, match="original typed input binding differs"):
        validate_spectral_factor_binding(PURE, rebound)

    short = copy.deepcopy(published)
    short["root_assignments"] = [published["root_assignments"][0]]
    with pytest.raises(SpectralBindingError, match="root assignment census differs") as census:
        validate_spectral_factor_binding(PURE, short)
    assert census.value.parameters == {"rows": 1, "expected": 2}

    counted = copy.deepcopy(published)
    counted["factor_root_counts"] = [2, 0]
    with pytest.raises(SpectralBindingError, match="factor distinct-root census differs"):
        validate_spectral_factor_binding(PURE, counted)

    counted["factor_root_counts"] = [True, 1]
    with pytest.raises(SpectralBindingError, match="boolean refused") as count_bool:
        validate_spectral_factor_binding(PURE, counted)
    assert count_bool.value.parameters["role"] == "factor_root_count"

    transported = copy.deepcopy(published)
    transported["carrier_transport"]["all_roots_real"] = False
    with pytest.raises(SpectralBindingError, match="carrier transport premise differs") as transport:
        validate_spectral_factor_binding(PURE, transported)
    assert transport.value.parameters["field"] == "all_roots_real"

    with pytest.raises(SpectralBindingError, match="operation required") as operation:
        dispatch({"operation": "degree", "input": PURE})
    assert operation.value.parameters["received"] == "str"

    with pytest.raises(ValueError, match="system missing") as neighbor:
        bad = copy.deepcopy(PURE)
        bad["system_id"] = "NOPE"
        bind_spectral_factors(bad)
    assert not isinstance(neighbor.value, SpectralBindingError)


def test_helper_invariants_have_measured_parameters() -> None:
    with pytest.raises(SpectralBindingError, match="non-scalar Unicode") as surrogate:
        spectral_factors._json_types("\ud800", "text")
    assert surrogate.value.parameters["role"] == "text"
    with pytest.raises(SpectralBindingError, match="keys must be strings"):
        spectral_factors._json_types({1: "a"}, "object")
    with pytest.raises(SpectralBindingError, match="exactly one irreducible factor owner") as owners:
        spectral_factors._one_owner([0, 1])
    assert owners.value.parameters["owners"] == 2
    with pytest.raises(SpectralBindingError, match="multiplicity differs"):
        spectral_factors._require_factor_multiplicity({"multiplicity": 1}, 2)
    with pytest.raises(SpectralBindingError, match="weighted factor root census differs") as weighted:
        spectral_factors._require_weighted([2], [{"multiplicity": 2}], 2)
    assert weighted.value.parameters == {"total": 4, "dimension": 2}
    with pytest.raises(SpectralBindingError, match="exact factor list required") as rows:
        spectral_factors._factor_row_list({"factors": "no"})
    assert rows.value.parameters["received"] == "str"
    with pytest.raises(SpectralBindingError, match="not self-conjugate") as conjugate:
        spectral_factors._coefficient(5, 5, spectral_factors.field.Cyclotomic.zeta(5))
    assert conjugate.value.invariant == "spectral_binding: characteristic coefficient is not self-conjugate"


def test_integration_matches_rust_binding_sentence() -> None:
    root = Path(__file__).resolve().parents[3]
    source = (root / "code" / "rust" / "src" / "linear_algebra" / "spectral_factors.rs").read_text(encoding="utf-8")
    assert 'validate_spectral_factor_binding' in source
    assert 'validate_spectral_factor_binding' in source
    certificate = bind_spectral_factors(PURE)
    validate_spectral_factor_binding(PURE, certificate)
    assert certificate["carrier_transport"]["root_field"] == "E_ALL_CHARACTERISTIC_ROOTS"


def test_end_to_end_public_contract(monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]) -> None:
    package = linear_algebra.spectral_factors
    published = package.dispatch({"operation": "bind_spectral_factors", "input": PURE})
    package.validate_spectral_factor_binding(PURE, published)
    assert published["schema"] == package.SCHEMA
    for case in fixtures():
        certificate = package.bind_spectral_factors(case)
        package.validate_spectral_factor_binding(case, certificate)
        degree = 1 if case["conductor"] == 1 else 2
        assert certificate["carrier_transport"]["carrier_degree_over_real_field"] == degree
        assert certificate["carrier_transport"]["all_roots_real"] is True

    monkeypatch.setattr(sys, "argv", ["spectral_factors.py", "--extra"])
    assert package.main() == 2
    assert "stdin request only" in capsys.readouterr().err

    payload = json.dumps({"operation": "bind_spectral_factors", "input": PURE}).encode("ascii")
    monkeypatch.setattr(sys, "argv", ["spectral_factors.py"])
    monkeypatch.setattr(sys, "stdin", io.TextIOWrapper(io.BytesIO(payload), encoding="ascii"))
    assert package.main() == 0
    stdout = capsys.readouterr().out
    assert json.loads(stdout)["authority_effect"] == "None"

    floated = b'{"operation":"bind_spectral_factors","input":1.5}'
    monkeypatch.setattr(sys, "stdin", io.TextIOWrapper(io.BytesIO(floated), encoding="ascii"))
    assert package.main() == 2
    assert "inexact JSON number forbidden" in capsys.readouterr().err


def test_origin_resolves_in_repo() -> None:
    root = Path(__file__).resolve().parents[3]
    origin = root / "code" / "rust" / "src" / "linear_algebra" / "spectral_factors.rs"
    assert origin.is_file()
    text = origin.read_text(encoding="utf-8")
    assert 'validate_spectral_factor_binding' in text
    source = _MODULE_PATH.read_text(encoding="utf-8")
    assert "AuthorityEffect: None" in source
    assert "urn:omega:fqm:linear-algebra:spectral-factor-binding:v1" in source
    assert "Scope Fence:" in source


_MUTANTS: tuple[tuple[str, str, str], ...] = (
    (
        "float admitted",
        'if isinstance(value, float):\n        raise _fail("float refused at the public boundary", role=role, received="float")',
        'if isinstance(value, float):\n        return\n    if False:\n        raise _fail("float refused at the public boundary", role=role, received="float")',
    ),
    (
        "boolean counter admitted",
        'if type(value) is bool:\n        raise _fail("boolean refused where an exact integer was required", role=role)',
        'if False and type(value) is bool:\n        raise _fail("boolean refused where an exact integer was required", role=role)',
    ),
    (
        "carrier degree flipped",
        "degree = 1 if conductor == 1 else 2",
        "degree = 2 if conductor == 1 else 1",
    ),
    (
        "owner census inverted",
        "if len(owners) != 1:",
        "if len(owners) == 1:",
    ),
    (
        "factor multiplicity inverted",
        'if row["multiplicity"] != multiplicity:',
        'if row["multiplicity"] == multiplicity:',
    ),
    (
        "schema renamed",
        'SCHEMA = "spectral_factor_binding_v1"',
        'SCHEMA = "spectral_factor_binding_v2"',
    ),
    (
        "reality premise dropped",
        '"all_roots_real": True,',
        '"all_roots_real": False,',
    ),
    (
        "weighted census inverted",
        "if total != dimension:",
        "if total == dimension:",
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


def _rows(certificate: object) -> list[tuple[object, object, object]] | None:
    if not isinstance(certificate, dict):
        return None
    rows = certificate.get("root_assignments")
    if not isinstance(rows, list):
        return None
    parsed: list[tuple[object, object, object]] = []
    for row in rows:
        if not isinstance(row, dict):
            return None
        parsed.append((row.get("root_index"), row.get("factor_index"), row.get("multiplicity")))
    return parsed


def _known_values_hold(namespace: dict[str, object], error: type[BaseException]) -> bool:
    produce = namespace["bind_spectral_factors"]
    verify = namespace["validate_spectral_factor_binding"]
    if not _all_hold((callable(produce), callable(verify),)):
        return False
    try:
        pure = produce(PURE)
        mixed = produce(MIXED)
        algebraic = produce(SQRT2)
        verify(PURE, pure)
        verify(MIXED, mixed)
        verify(SQRT2, algebraic)
    except error:
        return False
    pure_rows = _rows(pure)
    mixed_rows = _rows(mixed)
    algebraic_rows = _rows(algebraic)
    if pure_rows is None or mixed_rows is None or algebraic_rows is None:
        return False
    if not _all_hold((isinstance(pure, dict), isinstance(mixed, dict), isinstance(algebraic, dict),)):
        return False
    pure_transport = pure.get("carrier_transport")
    if not isinstance(pure_transport, dict):
        return False
    return _all_hold((
pure.get("schema") == "spectral_factor_binding_v1",
pure.get("authority_effect") == "None",
pure_rows == [(0, 1, 1), (1, 0, 1)],
pure.get("factor_root_counts") == [1, 1],
pure_transport.get("carrier_degree_over_real_field") == 2,
pure_transport.get("all_roots_real") is True,
mixed_rows == [(0, 0, 2)],
mixed.get("factor_root_counts") == [1],
algebraic_rows == [(0, 0, 1), (1, 0, 1)],
algebraic.get("factor_root_counts") == [2],
))


def _bad_values_refused(namespace: dict[str, object], error: type[BaseException]) -> bool:
    produce = namespace["bind_spectral_factors"]
    verify = namespace["validate_spectral_factor_binding"]
    if not _all_hold((callable(produce), callable(verify),)):
        return False
    floated = copy.deepcopy(PURE)
    floated["matrix"][0][0] = _probe("1.5")
    try:
        published = produce(PURE)
    except error:
        return False
    if not isinstance(published, dict):
        return False
    boolean = copy.deepcopy(published)
    assignments = boolean.get("root_assignments")
    if not _all_hold((isinstance(assignments, list), assignments, isinstance(assignments[0], dict),)):
        return False
    assignments[0]["multiplicity"] = True
    probes = (
        (lambda: produce(floated), "float refused at the public boundary"),
        (lambda: verify(PURE, boolean), "boolean refused where an exact integer was required"),
    )
    for probe, invariant in probes:
        if _invariant(error, probe) != invariant:
            return False
    return True


def _oracle(namespace: dict[str, object]) -> bool:
    error_type = namespace["SpectralBindingError"]
    if not _all_hold((isinstance(error_type, type), issubclass(error_type, BaseException),)):
        return False
    if not _known_values_hold(namespace, error_type):
        return False
    return _bad_values_refused(namespace, error_type)


def test_mutation_suite_kills_non_equivalent_mutants() -> None:
    source = _MODULE_PATH.read_text(encoding="utf-8")
    loaded: list[str] = []
    try:
        loaded.append("mutant_spectral_baseline")
        baseline = _load_source(source, loaded[-1])
        assert _oracle(baseline) is True
        killed = 0
        for index, (name, old, new) in enumerate(_MUTANTS):
            count = source.count(old)
            assert count == 1, f"{name} matched {count} sites"
            module_name = f"mutant_spectral_{index}"
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
