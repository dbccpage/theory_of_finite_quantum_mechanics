"""Unit, negative, integration, end-to-end, and mutation tests for the pseudoinverse.

Origin: code/python/src/linear_algebra/pseudoinverse.py
Claim: urn:omega:fqm:linear-algebra:moore-penrose:v1
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
from src.linear_algebra.pseudoinverse import (
    ExactMatrix,
    PseudoinverseError,
    _require_column_formula,
    _require_data_length,
    _require_factorization,
    _require_inverse,
    _require_reflexive,
    _require_symmetric,
    _require_triple,
    moore_penrose,
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


_MODULE_PATH = Path(__file__).resolve().parents[1] / "src" / "linear_algebra" / "pseudoinverse.py"


def _column_full() -> ExactMatrix:
    return ExactMatrix.from_rows(
        [
            [Fraction(1), Fraction(0)],
            [Fraction(0), Fraction(1)],
            [Fraction(1), Fraction(1)],
        ]
    )


def _rank_one() -> ExactMatrix:
    return ExactMatrix.from_rows(
        [
            [Fraction(1), Fraction(2)],
            [Fraction(2), Fraction(4)],
        ]
    )


def _expected_column_full() -> ExactMatrix:
    third = Fraction(1, 3)
    return ExactMatrix.from_rows(
        [
            [Fraction(2, 3), -third, third],
            [-third, Fraction(2, 3), third],
        ]
    )


def _expected_rank_one() -> ExactMatrix:
    return ExactMatrix.from_rows(
        [
            [Fraction(1, 25), Fraction(2, 25)],
            [Fraction(2, 25), Fraction(4, 25)],
        ]
    )


def test_penrose_values_are_exact_fractions() -> None:
    column = moore_penrose(_column_full())
    rank_one = moore_penrose(_rank_one())
    eye = moore_penrose(ExactMatrix.identity(2))
    assert column == _expected_column_full()
    assert rank_one == _expected_rank_one()
    assert eye == ExactMatrix.identity(2)
    assert type(column.get(0, 0)) is Fraction
    assert column * _column_full() == ExactMatrix.identity(2)


def test_negative_boundary_failures() -> None:
    with pytest.raises(PseudoinverseError, match="float refused") as floated:
        moore_penrose(ExactMatrix.from_rows([[_probe("1.5")]]))
    assert floated.value.invariant == "float refused at the public boundary"
    assert floated.value.parameters["role"] == "entry[0]"
    assert type(floated.value) is PseudoinverseError

    with pytest.raises(PseudoinverseError, match="boolean refused where a rational") as boolean:
        moore_penrose(ExactMatrix.from_rows([[True]]))
    assert boolean.value.invariant == "boolean refused where a rational entry was required"

    gaussian = ExactMatrix.from_rows([[GaussianRational(0, 1)]])
    with pytest.raises(PseudoinverseError, match="Gaussian rational refused") as gaussian_error:
        moore_penrose(gaussian)
    assert gaussian_error.value.parameters["role"] == "entry[0]"

    with pytest.raises(PseudoinverseError, match="not an exact rational") as text:
        moore_penrose(ExactMatrix.from_rows([["1"]]))
    assert text.value.parameters["received"] == "str"

    shaped = ExactMatrix.from_rows([[Fraction(1)]])
    shaped.rows = True
    with pytest.raises(PseudoinverseError, match="boolean refused where a matrix dimension") as dim_bool:
        moore_penrose(shaped)
    assert dim_bool.value.parameters["role"] == "rows"

    shaped = ExactMatrix.from_rows([[Fraction(1)]])
    shaped.rows = _probe("1.0")
    with pytest.raises(PseudoinverseError, match="float refused") as dim_float:
        moore_penrose(shaped)
    assert dim_float.value.parameters["role"] == "rows"

    with pytest.raises(PseudoinverseError, match="negative") as negative:
        moore_penrose(ExactMatrix(-1, 0, []))
    assert negative.value.parameters["received"] == -1

    named = ExactMatrix.from_rows([[Fraction(1)]])
    named.rows = "1"
    with pytest.raises(PseudoinverseError, match="not an integer") as named_error:
        moore_penrose(named)
    assert named_error.value.parameters["received"] == "str"

    with pytest.raises(PseudoinverseError, match="not an ExactMatrix") as bare:
        moore_penrose("matrix")
    assert bare.value.parameters["received"] == "str"

    mismatched = ExactMatrix.identity(2)
    mismatched.rows = 1
    with pytest.raises(PseudoinverseError, match="data length") as length_error:
        moore_penrose(mismatched)
    assert length_error.value.parameters["length"] == 4

    source = ExactMatrix.from_rows([[Fraction(1)]])
    image = ExactMatrix.from_rows([[Fraction(0)]])
    with pytest.raises(PseudoinverseError, match="do not rebuild") as rebuilt:
        _require_factorization(source, image, ExactMatrix.identity(1))
    assert rebuilt.value.parameters["rank"] == 1

    singular = ExactMatrix.from_rows(
        [
            [Fraction(1), Fraction(2)],
            [Fraction(2), Fraction(4)],
        ]
    )
    with pytest.raises(PseudoinverseError, match="Gram matrix was singular") as gram:
        _require_inverse(singular, "F^T F")
    assert gram.value.parameters["role"] == "F^T F"

    with pytest.raises(PseudoinverseError, match="A A\\+ A = A failed") as triple:
        _require_triple(source, ExactMatrix.from_rows([[Fraction(0)]]))
    assert triple.value.parameters["rows"] == 1

    with pytest.raises(PseudoinverseError, match="A\\+ A A\\+ = A\\+ failed") as reflexive:
        _require_reflexive(source, ExactMatrix.from_rows([[Fraction(2)]]))
    assert reflexive.value.parameters["rows"] == 1

    tilted = ExactMatrix.from_rows(
        [
            [Fraction(1), Fraction(1)],
            [Fraction(0), Fraction(1)],
        ]
    )
    with pytest.raises(PseudoinverseError, match="not symmetric") as tilted_error:
        _require_symmetric(tilted, "A A+")
    assert tilted_error.value.parameters["role"] == "A A+"

    with pytest.raises(PseudoinverseError, match="not \\(A\\^T A\\)") as formula:
        _require_column_formula(source, ExactMatrix.from_rows([[Fraction(0)]]), 1)
    assert formula.value.parameters["cols"] == 1

    with pytest.raises(PseudoinverseError, match="data length"):
        _require_data_length(source, 2, 2)


def test_integration_matches_cited_left_inverse() -> None:
    root = Path(__file__).resolve().parents[3]
    note = (root / "papers" / "core" / "mub6" / "artifacts" / "knowledge" / "category_moore_penrose_least_squares_annihilation.md").read_text(encoding="utf-8")
    paper = (root / "papers" / "core" / "mub6" / "mub6.md").read_text(encoding="utf-8")
    assert "(J^T J)^{-1} J^T" in note
    assert "preconditioner is not defined there" in paper
    source = _column_full()
    gram = source.transpose() * source
    cited = gram.inverse() * source.transpose()
    assert moore_penrose(source) == cited
    assert cited == _expected_column_full()
    assert "rank 184" in paper


def test_end_to_end_public_contract() -> None:
    package = linear_algebra.pseudoinverse
    assert package.moore_penrose(ExactMatrix.from_rows([[Fraction(2)]])) == ExactMatrix.from_rows([[Fraction(1, 2)]])
    zero = package.moore_penrose(ExactMatrix.zeros(2, 3))
    assert zero == ExactMatrix.zeros(3, 2)
    assert type(zero.get(0, 0)) is Fraction
    empty = package.moore_penrose(ExactMatrix(0, 2, []))
    assert empty.rows == 2
    assert empty.cols == 0
    thin = package.moore_penrose(ExactMatrix(2, 0, []))
    assert thin.rows == 0
    assert thin.cols == 2
    tampered = ExactMatrix.identity(1)
    tampered.data[0] = _probe("0.25")
    with pytest.raises(PseudoinverseError, match="float refused"):
        package.moore_penrose(tampered)


def test_origin_resolves_in_repo() -> None:
    root = Path(__file__).resolve().parents[3]
    note = (root / "papers" / "core" / "mub6" / "artifacts" / "knowledge" / "category_moore_penrose_least_squares_annihilation.md").read_text(encoding="utf-8")
    paper = (root / "papers" / "core" / "mub6" / "mub6.md").read_text(encoding="utf-8")
    assert "(J^T J)^{-1} J^T" in note
    assert "preconditioner is not defined there" in paper
    source = _MODULE_PATH.read_text(encoding="utf-8")
    assert "AuthorityEffect: None" in source
    assert "urn:omega:fqm:linear-algebra:moore-penrose:v1" in source
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
        'if isinstance(value, GaussianRational):\n        raise _fail("Gaussian rational refused; pseudoinverse in this module is over Q", role=role)',
        'if isinstance(value, GaussianRational):\n        return value.real\n    if False:\n        raise _fail("Gaussian rational refused; pseudoinverse in this module is over Q", role=role)',
    ),
    (
        "boolean dimension admitted",
        'if type(value) is bool:\n        raise _fail("boolean refused where a matrix dimension was required", role=role)',
        'if type(value) is bool:\n        return 1\n    if False:\n        raise _fail("boolean refused where a matrix dimension was required", role=role)',
    ),
    (
        "factorization check inverted",
        "if image * coordinates != source:",
        "if image * coordinates == source:",
    ),
    (
        "Penrose triple inverted",
        "if source * pseudo * source != source:",
        "if source * pseudo * source == source:",
    ),
    (
        "Penrose reflexive inverted",
        "if pseudo * source * pseudo != pseudo:",
        "if pseudo * source * pseudo == pseudo:",
    ),
    (
        "column-rank formula inverted",
        "if pseudo != cited:",
        "if pseudo == cited:",
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
    certify = namespace["moore_penrose"]
    matrix = namespace["ExactMatrix"]
    if not _all_hold((callable(certify), isinstance(matrix, type),)):
        return False
    try:
        column = certify(_column_full())
        rank_one = certify(_rank_one())
        eye = certify(matrix.identity(2))
        zero = certify(matrix.zeros(2, 3))
        scalar = certify(matrix.from_rows([[Fraction(2)]]))
    except error:
        return False
    return _all_hold((
column == _expected_column_full(),
rank_one == _expected_rank_one(),
eye == matrix.identity(2),
zero == matrix.zeros(3, 2),
scalar == matrix.from_rows([[Fraction(1, 2)]]),
))


def _bad_values_refused(namespace: dict[str, object], error: type[BaseException]) -> bool:
    certify = namespace["moore_penrose"]
    matrix = namespace["ExactMatrix"]
    gaussian = namespace["GaussianRational"]
    if not _all_hold((callable(certify), isinstance(matrix, type), callable(gaussian),)):
        return False
    build = getattr(matrix, "from_rows")
    if not callable(build):
        return False
    shaped = build([[Fraction(1)]])
    shaped.rows = True
    probes = (
        (lambda: certify(build([[_probe("1.5")]])), "float refused at the public boundary"),
        (lambda: certify(build([[True]])), "boolean refused where a rational entry was required"),
        (lambda: certify(build([[gaussian(0, 1)]])), "Gaussian rational refused; pseudoinverse in this module is over Q"),
        (lambda: certify(shaped), "boolean refused where a matrix dimension was required"),
    )
    for probe, invariant in probes:
        if _invariant(error, probe) != invariant:
            return False
    return True


def _oracle(namespace: dict[str, object]) -> bool:
    error_type = namespace["PseudoinverseError"]
    if not _all_hold((isinstance(error_type, type), issubclass(error_type, BaseException),)):
        return False
    if not _known_values_hold(namespace, error_type):
        return False
    return _bad_values_refused(namespace, error_type)


def test_mutation_suite_kills_non_equivalent_mutants() -> None:
    source = _MODULE_PATH.read_text(encoding="utf-8")
    loaded: list[str] = []
    try:
        loaded.append("mutant_pseudoinverse_baseline")
        baseline = _load_source(source, loaded[-1])
        assert _oracle(baseline) is True
        killed = 0
        for index, (name, old, new) in enumerate(_MUTANTS):
            count = source.count(old)
            assert count == 1, f"{name} matched {count} sites"
            module_name = f"mutant_pseudoinverse_{index}"
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
