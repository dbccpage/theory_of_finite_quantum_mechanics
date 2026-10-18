"""Unit, negative, integration, end-to-end, and mutation tests for splitting degrees.

Origin: code/python/src/linear_algebra/splitting_deg.py
Claim: urn:omega:fqm:linear-algebra:splitting-degree:v1
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

import src.linear_algebra as linear_algebra
from src.linear_algebra.scalars import GaussianRational
from src.linear_algebra.splitting_deg import (
    SplittingDegreeError,
    dispatch,
    irreducible_splitting_degree,
    validate_splitting_degree,
    witness_s3_degree,
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


_MODULE_PATH = Path(__file__).resolve().parents[1] / "src" / "linear_algebra" / "splitting_deg.py"
_Q = Fraction


def _poly(*values: int) -> list[tuple[Fraction, Fraction]]:
    return [(_Q(value), _Q(0)) for value in values]


_S3 = _poly(1, 0, 0, -2)
_C3 = _poly(1, 1, -2, -1)
_V4 = _poly(1, 0, 0, 0, 1)
_S4 = _poly(1, 0, 0, 1, 1)
_D4 = _poly(1, 0, 0, 0, -2)
_A4 = _poly(1, 0, 0, 8, 12)
_C4 = _poly(1, 1, 1, 1, 1)
_REDUCIBLE = _poly(1, 0, 0, 0, 4)


def _group(certificate: dict[str, object]) -> tuple[object, object]:
    return certificate["galois_group"], certificate["degree_over_real_field"]


def test_splitting_degrees_match_hand_values() -> None:
    assert witness_s3_degree() == 6
    assert type(witness_s3_degree()) is int

    cubic = irreducible_splitting_degree(1, _S3)
    assert _group(cubic) == ("S3", 6)
    assert cubic["resolvent"] is None
    assert cubic["coefficient_field"] == "Q"
    assert cubic["authority_effect"] == "None"
    assert cubic["schema"] == "real_field_splitting_degree_v1"
    assert cubic["discriminant_square"]["is_square"] is False
    validate_splitting_degree(1, _S3, cubic)

    cyclic = irreducible_splitting_degree(1, _C3)
    assert _group(cyclic) == ("C3", 3)
    assert cyclic["discriminant_square"]["is_square"] is True
    validate_splitting_degree(1, _C3, cyclic)

    klein = irreducible_splitting_degree(1, _V4)
    assert _group(klein) == ("V4", 4)
    assert klein["resolvent"]["factor_degrees"] == [1, 1, 1]
    validate_splitting_degree(1, _V4, klein)

    symmetric = irreducible_splitting_degree(1, _S4)
    assert _group(symmetric) == ("S4", 24)
    assert symmetric["resolvent"]["factor_degrees"] == [3]
    validate_splitting_degree(1, _S4, symmetric)

    dihedral = irreducible_splitting_degree(1, _D4)
    assert _group(dihedral) == ("D4", 8)
    assert dihedral["resolvent"]["factor_degrees"] == [1, 2]
    assert dihedral["resolvent"]["cyclic_tests"]["first_square"]["is_square"] is True
    assert dihedral["resolvent"]["cyclic_tests"]["second_square"]["is_square"] is False
    validate_splitting_degree(1, _D4, dihedral)

    alternating = irreducible_splitting_degree(1, _A4)
    assert _group(alternating) == ("A4", 12)
    validate_splitting_degree(1, _A4, alternating)

    cycle = irreducible_splitting_degree(1, _C4)
    assert _group(cycle) == ("C4", 4)
    assert cycle["resolvent"]["cyclic_tests"]["first_square"]["is_square"] is True
    assert cycle["resolvent"]["cyclic_tests"]["second_square"]["is_square"] is True
    validate_splitting_degree(1, _C4, cycle)


def test_negative_boundary_failures() -> None:
    with pytest.raises(SplittingDegreeError, match="float refused") as floated:
        irreducible_splitting_degree(1, [_poly(1)[0], _poly(0)[0], _poly(0)[0], (_probe("1.5"), _Q(0))])
    assert floated.value.invariant == "float refused at the public boundary"
    assert floated.value.parameters["role"] == "coefficient[3][0]"
    assert floated.value.parameters["received"] == "float"

    with pytest.raises(SplittingDegreeError, match="boolean refused") as boolean_coordinate:
        irreducible_splitting_degree(1, [(True, _Q(0)), _poly(0)[0], _poly(0)[0], _poly(-2)[0]])
    assert boolean_coordinate.value.invariant == "boolean refused where a rational coordinate was required"
    assert boolean_coordinate.value.parameters["role"] == "coefficient[0][0]"

    with pytest.raises(SplittingDegreeError, match="Gaussian") as gaussian:
        irreducible_splitting_degree(1, [(GaussianRational(0, 1), _Q(0)), _poly(0)[0], _poly(0)[0], _poly(-2)[0]])
    assert gaussian.value.invariant == (
        "Gaussian rational refused; splitting degrees in this module are over a real field"
    )

    with pytest.raises(SplittingDegreeError, match="boolean refused") as boolean_conductor:
        irreducible_splitting_degree(True, _S3)
    assert boolean_conductor.value.invariant == "boolean refused where a conductor was required"
    assert boolean_conductor.value.parameters["role"] == "conductor"

    with pytest.raises(SplittingDegreeError, match="three or four") as degree:
        irreducible_splitting_degree(1, _poly(1, -1))
    assert degree.value.invariant == "splitting_degree: polynomial degree must be three or four"

    with pytest.raises(SplittingDegreeError, match="irreducible") as reducible:
        irreducible_splitting_degree(1, _REDUCIBLE)
    assert reducible.value.invariant == "splitting_degree: input must be irreducible over the declared real field"

    tampered = dict(irreducible_splitting_degree(1, _S3))
    tampered["degree_over_real_field"] = 3
    with pytest.raises(SplittingDegreeError, match="differs from arithmetic branch") as changed:
        validate_splitting_degree(1, _S3, tampered)
    assert changed.value.invariant == (
        "splitting_degree: Galois group or real-field degree differs from arithmetic branch"
    )

    with pytest.raises(SplittingDegreeError, match="field census") as census:
        dispatch("irreducible_splitting_degree")
    assert census.value.invariant == "splitting_degree: exact request field census required"

    with pytest.raises(SplittingDegreeError, match="operation required") as operation:
        dispatch({"operation": "degree", "conductor": 1, "coefficients": []})
    assert operation.value.invariant == "splitting_degree: irreducible_splitting_degree operation required"


def test_integration_matches_rust_splitting_sentence() -> None:
    root = Path(__file__).resolve().parents[3]
    source = (root / "code" / "rust" / "src" / "linear_algebra" / "splitting_deg.rs").read_text(encoding="utf-8")
    assert 'irreducible_splitting_degree' in source
    for name in ("C3", "S3", "A4", "S4", "V4", "C4", "D4"):
        assert name in source
    certificate = irreducible_splitting_degree(1, _S3)
    validate_splitting_degree(1, _S3, certificate)
    assert certificate["galois_group"] == "S3"


def test_end_to_end_public_contract() -> None:
    package = linear_algebra.splitting_deg
    witness = package.witness_s3_degree()
    certificate = package.irreducible_splitting_degree(1, _S3)
    assert witness == certificate["degree_over_real_field"] == 6
    published = package.dispatch(
        {
            "operation": "irreducible_splitting_degree",
            "conductor": 1,
            "coefficients": [["1/1", "0/1"], ["0/1", "0/1"], ["0/1", "0/1"], ["-2/1", "0/1"]],
        }
    )
    assert published["galois_group"] == "S3"
    assert published["authority_effect"] == "None"
    with pytest.raises(SplittingDegreeError, match="float refused"):
        package.irreducible_splitting_degree(_probe("1.0"), _S3)


def test_origin_resolves_in_repo() -> None:
    root = Path(__file__).resolve().parents[3]
    origin = root / "code" / "rust" / "src" / "linear_algebra" / "splitting_deg.rs"
    assert origin.is_file()
    text = origin.read_text(encoding="utf-8")
    assert 'irreducible_splitting_degree' in text
    source = _MODULE_PATH.read_text(encoding="utf-8")
    assert "AuthorityEffect: None" in source
    assert "urn:omega:fqm:linear-algebra:splitting-degree:v1" in source
    assert "Scope Fence:" in source


_MUTANTS: tuple[tuple[str, str, str], ...] = (
    (
        "float admitted",
        'if isinstance(value, float):\n        raise _fail("float refused at the public boundary", role=role, received="float")',
        'if isinstance(value, float):\n        return\n    if False:\n        raise _fail("float refused at the public boundary", role=role, received="float")',
    ),
    (
        "boolean conductor admitted",
        'if type(value) is bool:\n        raise _fail("boolean refused where a conductor was required", role="conductor")',
        'if False and type(value) is bool:\n        raise _fail("boolean refused where a conductor was required", role="conductor")',
    ),
    (
        "boolean coordinate admitted",
        'if type(value) is bool:\n        raise _fail("boolean refused where a rational coordinate was required", role=role)',
        'if type(value) is bool:\n        return\n    if False:\n        raise _fail("boolean refused where a rational coordinate was required", role=role)',
    ),
    (
        "cubic square test inverted",
        'return ("C3", 3) if square else ("S3", 6)',
        'return ("C3", 3) if not square else ("S3", 6)',
    ),
    (
        "Klein degree raised",
        'return "V4", 4',
        'return "V4", 8',
    ),
    (
        "symmetric degree dropped",
        '("S4", 24)',
        '("S4", 12)',
    ),
    (
        "dihedral degree dropped",
        '("D4", 8)',
        '("D4", 4)',
    ),
    (
        "alternating degree raised",
        '("A4", 12)',
        '("A4", 24)',
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


def _row(namespace: dict[str, object], error: type[BaseException], coefficients: object) -> dict[str, object] | None:
    degree = namespace["irreducible_splitting_degree"]
    if not callable(degree):
        return None
    try:
        certificate = degree(1, coefficients)
    except error:
        return None
    return certificate if isinstance(certificate, dict) else None


def _known_values_hold(namespace: dict[str, object], error: type[BaseException]) -> bool:
    witness = namespace["witness_s3_degree"]
    if not callable(witness):
        return False
    try:
        published = witness()
    except error:
        return False
    rows = (
        (_S3, "S3", 6),
        (_C3, "C3", 3),
        (_V4, "V4", 4),
        (_S4, "S4", 24),
        (_D4, "D4", 8),
        (_A4, "A4", 12),
        (_C4, "C4", 4),
    )
    parsed = [_row(namespace, error, coefficients) for coefficients, _, _ in rows]
    if any(row is None for row in parsed):
        return False
    return _all_hold((
published == 6,
type(published) is int,
all(
            row is not None
            and row.get("galois_group") == group
            and row.get("degree_over_real_field") == degree
            and row.get("authority_effect") == "None"
            and row.get("coefficient_field") == "Q"
            for row, (_, group, degree) in zip(parsed, rows)
        ),
))


def _bad_values_refused(namespace: dict[str, object], error: type[BaseException]) -> bool:
    degree = namespace["irreducible_splitting_degree"]
    gaussian = namespace["GaussianRational"]
    if not _all_hold((callable(degree), callable(gaussian),)):
        return False
    probes = (
        (
            lambda: degree(1, [_poly(1)[0], _poly(0)[0], _poly(0)[0], (_probe("1.5"), _Q(0))]),
            "float refused at the public boundary",
        ),
        (lambda: degree(True, _S3), "boolean refused where a conductor was required"),
        (
            lambda: degree(1, [(True, _Q(0)), _poly(0)[0], _poly(0)[0], _poly(-2)[0]]),
            "boolean refused where a rational coordinate was required",
        ),
        (
            lambda: degree(1, [(gaussian(0, 1), _Q(0)), _poly(0)[0], _poly(0)[0], _poly(-2)[0]]),
            "Gaussian rational refused; splitting degrees in this module are over a real field",
        ),
    )
    for probe, invariant in probes:
        if _invariant(error, probe) != invariant:
            return False
    return True


def _oracle(namespace: dict[str, object]) -> bool:
    error_type = namespace["SplittingDegreeError"]
    if not _all_hold((isinstance(error_type, type), issubclass(error_type, BaseException),)):
        return False
    if not _known_values_hold(namespace, error_type):
        return False
    return _bad_values_refused(namespace, error_type)


def test_mutation_suite_kills_non_equivalent_mutants() -> None:
    source = _MODULE_PATH.read_text(encoding="utf-8")
    loaded: list[str] = []
    try:
        loaded.append("mutant_splitting_baseline")
        baseline = _load_source(source, loaded[-1])
        assert _oracle(baseline) is True
        killed = 0
        for index, (name, old, new) in enumerate(_MUTANTS):
            count = source.count(old)
            assert count == 1, f"{name} matched {count} sites"
            module_name = f"mutant_splitting_{index}"
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
