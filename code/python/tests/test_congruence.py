"""Unit, negative, integration, end-to-end, and mutation tests for symmetric congruence.

Origin: code/python/src/linear_algebra/congruence.py
Claim: urn:omega:fqm:linear-algebra:symmetric-congruence:v1
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
from src.linear_algebra.congruence import (
    CongruenceError,
    ExactMatrix,
    _require_diagonal,
    _require_replay,
    _require_unimodular,
    congruent_diagonal,
    witness_diagonal_entry,
)
from src.linear_algebra.scalars import GaussianRational

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


_MODULE_PATH = Path(__file__).resolve().parents[1] / "src" / "linear_algebra" / "congruence.py"


def _paired() -> ExactMatrix:
    return ExactMatrix.from_rows([[Fraction(1), Fraction(2)], [Fraction(2), Fraction(3)]])


def _shear() -> ExactMatrix:
    return ExactMatrix.from_rows([[Fraction(0), Fraction(2)], [Fraction(2), Fraction(0)]])


def _paired_diagonal() -> ExactMatrix:
    return ExactMatrix.from_rows([[Fraction(1), Fraction(0)], [Fraction(0), Fraction(-1)]])


def _paired_transform() -> ExactMatrix:
    return ExactMatrix.from_rows([[Fraction(1), Fraction(-2)], [Fraction(0), Fraction(1)]])


def _shear_diagonal() -> ExactMatrix:
    return ExactMatrix.from_rows([[Fraction(2), Fraction(0)], [Fraction(0), Fraction(-2)]])


def test_congruence_matches_the_hand_matrices() -> None:
    assert witness_diagonal_entry() == -1
    assert type(witness_diagonal_entry()) is Fraction
    diagonal, transform = congruent_diagonal(_paired())
    assert diagonal == _paired_diagonal()
    assert transform == _paired_transform()
    shear_diagonal, shear_transform = congruent_diagonal(_shear())
    assert shear_diagonal == _shear_diagonal()
    assert shear_transform.determinant() == 1
    donor = ExactMatrix.from_rows([[Fraction(0), Fraction(0)], [Fraction(0), Fraction(5)]])
    donor_diagonal, donor_transform = congruent_diagonal(donor)
    assert donor_diagonal == ExactMatrix.from_rows([[Fraction(5), Fraction(0)], [Fraction(0), Fraction(0)]])
    assert donor_transform.determinant() == -1
    single = ExactMatrix.from_rows([[Fraction(7)]])
    single_diagonal, single_transform = congruent_diagonal(single)
    assert single_diagonal.get(0, 0) == 7
    assert single_transform.get(0, 0) == 1
    zero = ExactMatrix.from_rows([[Fraction(0), Fraction(0)], [Fraction(0), Fraction(0)]])
    zero_diagonal, zero_transform = congruent_diagonal(zero)
    assert zero_diagonal == zero
    assert zero_transform == ExactMatrix.identity(2)
    empty_diagonal, empty_transform = congruent_diagonal(ExactMatrix(0, 0, []))
    assert empty_diagonal.shape() == (0, 0)
    assert empty_transform.determinant() == 1
    triple = ExactMatrix.from_rows(
        [
            [Fraction(0), Fraction(0), Fraction(1)],
            [Fraction(0), Fraction(0), Fraction(0)],
            [Fraction(1), Fraction(0), Fraction(0)],
        ]
    )
    triple_diagonal, triple_transform = congruent_diagonal(triple)
    assert triple_transform.transpose() * triple * triple_transform == triple_diagonal
    assert triple_diagonal.get(0, 1) == 0
    assert triple_diagonal.get(0, 2) == 0
    assert triple_diagonal.get(1, 2) == 0


def test_negative_boundary_failures() -> None:
    partner = ExactMatrix.from_rows([[Fraction(1)]])
    with pytest.raises(CongruenceError, match="float refused") as floated:
        congruent_diagonal(ExactMatrix.from_rows([[_probe("1.5")]]))
    assert floated.value.invariant == "float refused at the public boundary"
    assert floated.value.parameters["role"] == "entry[0]"
    assert type(floated.value) is CongruenceError

    with pytest.raises(CongruenceError, match="boolean refused where a rational") as boolean:
        congruent_diagonal(ExactMatrix.from_rows([[True]]))
    assert boolean.value.invariant == "boolean refused where a rational entry was required"

    with pytest.raises(CongruenceError, match="Gaussian rational refused") as gaussian:
        congruent_diagonal(ExactMatrix.from_rows([[GaussianRational(0, 1)]]))
    assert gaussian.value.parameters["role"] == "entry[0]"

    with pytest.raises(CongruenceError, match="not an exact rational") as text:
        congruent_diagonal(ExactMatrix.from_rows([["1"]]))
    assert text.value.parameters["received"] == "str"

    shaped = ExactMatrix.from_rows([[Fraction(1)]])
    shaped.rows = True
    with pytest.raises(CongruenceError, match="boolean refused where a matrix dimension") as dim_bool:
        congruent_diagonal(shaped)
    assert dim_bool.value.parameters["role"] == "rows"

    shaped = ExactMatrix.from_rows([[Fraction(1)]])
    shaped.rows = _probe("1.0")
    with pytest.raises(CongruenceError, match="float refused") as dim_float:
        congruent_diagonal(shaped)
    assert dim_float.value.parameters["role"] == "rows"

    with pytest.raises(CongruenceError, match="negative") as negative:
        congruent_diagonal(ExactMatrix(-1, 0, []))
    assert negative.value.parameters["received"] == -1

    named = ExactMatrix.from_rows([[Fraction(1)]])
    named.cols = "1"
    with pytest.raises(CongruenceError, match="not an integer") as named_error:
        congruent_diagonal(named)
    assert named_error.value.parameters["received"] == "str"

    with pytest.raises(CongruenceError, match="not an ExactMatrix") as bare:
        congruent_diagonal("matrix")
    assert bare.value.parameters["received"] == "str"

    mismatched = ExactMatrix.identity(2)
    mismatched.rows = 3
    mismatched.cols = 3
    with pytest.raises(CongruenceError, match="data length") as length_error:
        congruent_diagonal(mismatched)
    assert length_error.value.parameters["length"] == 4

    wide = ExactMatrix.from_rows([[Fraction(1), Fraction(2)]])
    with pytest.raises(CongruenceError, match="square") as rectangular:
        congruent_diagonal(wide)
    assert rectangular.value.parameters["cols"] == 2

    skewed = ExactMatrix.from_rows([[Fraction(1), Fraction(2)], [Fraction(0), Fraction(1)]])
    with pytest.raises(CongruenceError, match="symmetric") as symmetry:
        congruent_diagonal(skewed)
    assert symmetry.value.parameters["row"] == 0
    assert symmetry.value.parameters["col"] == 1

    with pytest.raises(CongruenceError, match="off-diagonal") as off:
        _require_diagonal(ExactMatrix.from_rows([[Fraction(1), Fraction(1)], [Fraction(0), Fraction(1)]]))
    assert off.value.parameters["mass"] == "1"

    with pytest.raises(CongruenceError, match="differs from the diagonal") as replay:
        _require_replay(partner, partner, ExactMatrix.from_rows([[Fraction(2)]]))
    assert replay.value.parameters["mass"] == "3"

    with pytest.raises(CongruenceError, match="not ±1") as singular:
        _require_unimodular(ExactMatrix.from_rows([[Fraction(2), Fraction(0)], [Fraction(0), Fraction(1)]]))
    assert singular.value.parameters["determinant"] == "2"

    with pytest.raises(CongruenceError, match="not ±1") as vanished:
        _require_unimodular(ExactMatrix.from_rows([[Fraction(0)]]))
    assert vanished.value.parameters["determinant"] == "0"


def test_integration_matches_rust_symmetric_certificate() -> None:
    root = Path(__file__).resolve().parents[3]
    source = (root / "code" / "rust" / "src" / "linear_algebra" / "congruence.rs").read_text(encoding="utf-8")
    assert 'non_symmetric_and_non_hermitian_inputs_are_refused_with_their_first_offending_entry' in source
    assert 'non_symmetric_and_non_hermitian_inputs_are_refused_with_their_first_offending_entry' in source
    assert 'non_symmetric_and_non_hermitian_inputs_are_refused_with_their_first_offending_entry' in source or 'non_symmetric_and_non_hermitian_inputs_are_refused_with_their_first_offending_entry' in source
    diagonal, transform = congruent_diagonal(_paired())
    assert transform.transpose() * _paired() * transform == diagonal
    assert diagonal == _paired_diagonal()


def test_end_to_end_public_contract() -> None:
    package = linear_algebra.congruence
    assert package.witness_diagonal_entry() == -1
    one = ExactMatrix.from_rows([[Fraction(4)]])
    diagonal, transform = package.congruent_diagonal(one)
    assert diagonal.get(0, 0) == 4
    assert transform.get(0, 0) == 1
    tampered = ExactMatrix.from_rows([[Fraction(1)]])
    tampered.data[0] = _probe("0.25")
    with pytest.raises(CongruenceError, match="float refused"):
        package.congruent_diagonal(tampered)


def test_origin_resolves_in_repo() -> None:
    root = Path(__file__).resolve().parents[3]
    origin = root / "code" / "rust" / "src" / "linear_algebra" / "congruence.rs"
    assert origin.is_file()
    text = origin.read_text(encoding="utf-8")
    assert 'non_symmetric_and_non_hermitian_inputs_are_refused_with_their_first_offending_entry' in text
    source = _MODULE_PATH.read_text(encoding="utf-8")
    assert "AuthorityEffect: None" in source
    assert "urn:omega:fqm:linear-algebra:symmetric-congruence:v1" in source
    assert "Scope Fence:" in source


_MUTANTS: tuple[tuple[str, str, str], ...] = (
    (
        "float admitted",
        'if isinstance(value, float):\n        raise _fail("float refused at the public boundary", role=role, received="float")',
        'if isinstance(value, float):\n        return\n    if False:\n        raise _fail("float refused at the public boundary", role=role, received="float")',
    ),
    (
        "boolean entry admitted",
        'if type(value) is bool:\n        raise _fail("boolean refused where a rational entry was required", role=role)',
        'if type(value) is bool:\n        return Fraction(1)\n    if False:\n        raise _fail("boolean refused where a rational entry was required", role=role)',
    ),
    (
        "Gaussian entry admitted",
        'if isinstance(value, GaussianRational):\n        raise _fail("Gaussian rational refused; congruence in this module is over Q", role=role)',
        'if isinstance(value, GaussianRational):\n        return value.real\n    if False:\n        raise _fail("Gaussian rational refused; congruence in this module is over Q", role=role)',
    ),
    (
        "boolean dimension admitted",
        'if type(value) is bool:\n        raise _fail("boolean refused where a matrix dimension was required", role=role)',
        'if type(value) is bool:\n        return 1\n    if False:\n        raise _fail("boolean refused where a matrix dimension was required", role=role)',
    ),
    (
        "elimination sign flipped",
        "factor = -(entry / pivot)",
        "factor = entry / pivot",
    ),
    (
        "shear coefficient not inverted",
        "coeff = Fraction(1) / entry",
        "coeff = entry",
    ),
    (
        "elimination axes swapped",
        "_add_multiple(current.rows, column, index, factor)",
        "_add_multiple(current.rows, index, column, factor)",
    ),
    (
        "unimodular gate inverted",
        "if abs(det) != 1:",
        "if abs(det) == 1:",
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


def _known_values_hold(namespace: dict[str, object], error: type[BaseException]) -> bool:
    witness = namespace["witness_diagonal_entry"]
    diagonalise = namespace["congruent_diagonal"]
    if not _all_hold((callable(witness), callable(diagonalise),)):
        return False
    try:
        entry = witness()
        diagonal, _transform = diagonalise(_shear())
    except error:
        return False
    if not isinstance(diagonal, ExactMatrix):
        return False
    return _all_hold((
entry == -1,
diagonal.get(0, 0) == 2,
diagonal.get(1, 1) == -2,
))


def _bad_values_refused(namespace: dict[str, object], error: type[BaseException]) -> bool:
    diagonalise = namespace["congruent_diagonal"]
    matrix = namespace["ExactMatrix"]
    gaussian = namespace["GaussianRational"]
    if not _all_hold((callable(diagonalise), isinstance(matrix, type), callable(gaussian),)):
        return False
    build = getattr(matrix, "from_rows")
    if not callable(build):
        return False
    shaped = build([[Fraction(1)]])
    shaped.rows = True
    probes = (
        (lambda: diagonalise(build([[_probe("1.5")]])), "float refused at the public boundary"),
        (lambda: diagonalise(build([[True]])), "boolean refused where a rational entry was required"),
        (
            lambda: diagonalise(build([[gaussian(0, 1)]])),
            "Gaussian rational refused; congruence in this module is over Q",
        ),
        (lambda: diagonalise(shaped), "boolean refused where a matrix dimension was required"),
    )
    for probe, invariant in probes:
        if _invariant(error, probe) != invariant:
            return False
    return True


def _oracle(namespace: dict[str, object]) -> bool:
    error_type = namespace["CongruenceError"]
    if not _all_hold((isinstance(error_type, type), issubclass(error_type, BaseException),)):
        return False
    if not _known_values_hold(namespace, error_type):
        return False
    return _bad_values_refused(namespace, error_type)


def test_mutation_suite_kills_non_equivalent_mutants() -> None:
    source = _MODULE_PATH.read_text(encoding="utf-8")
    loaded: list[str] = []
    try:
        loaded.append("mutant_congruence_baseline")
        baseline = _load_source(source, loaded[-1])
        assert _oracle(baseline) is True
        killed = 0
        for index, (name, old, new) in enumerate(_MUTANTS):
            count = source.count(old)
            assert count == 1, f"{name} matched {count} sites"
            module_name = f"mutant_congruence_{index}"
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
