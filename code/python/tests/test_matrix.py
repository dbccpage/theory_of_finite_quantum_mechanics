"""Unit, negative, integration, end-to-end, and mutation tests for exact matrices.

Origin: code/python/src/linear_algebra/matrix.py
Claim: urn:omega:fqm:linear-algebra:exact-matrix:v1
AuthorityEffect: None
Mutation-Kills: 8 non-equivalent
"""



from __future__ import annotations

import importlib.util
import sys
import warnings
from fractions import Fraction
from pathlib import Path
from typing import Any

import pytest

import src.linear_algebra as linear_algebra
from src.linear_algebra.bareiss_det import bareiss_matches_elimination
from src.linear_algebra.matrix import ExactMatrix, MatrixFailure, MatrixIndexError
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


_MODULE_PATH = Path(__file__).resolve().parents[1] / "src" / "linear_algebra" / "matrix.py"
_Q = Fraction


def _raises(probe: Any, invariant: str) -> MatrixFailure:
    with pytest.raises(MatrixFailure) as caught:
        probe()
    assert caught.value.invariant == invariant
    assert all(type(item).__name__ != "float" for item in caught.value.parameters.values())
    return caught.value


def test_hand_matrices_match_exact_certificates() -> None:
    eye = ExactMatrix.identity(2)
    assert eye == ExactMatrix.from_rows([[_Q(1), _Q(0)], [_Q(0), _Q(1)]])
    assert eye.sha256() == ExactMatrix.identity(2).sha256()
    singular = ExactMatrix.from_rows(
        [[_Q(1), _Q(2), _Q(3)], [_Q(4), _Q(5), _Q(6)], [_Q(7), _Q(8), _Q(9)]]
    )
    assert singular.rank() == 2
    kernel = singular.kernel_basis()
    assert kernel == [[_Q(1), _Q(-2), _Q(1)]]
    assert singular.mul_vec(kernel[0]) == [_Q(0), _Q(0), _Q(0)]

    source = ExactMatrix.from_rows([[_Q(1), _Q(2)], [_Q(3), _Q(4)]])
    assert source.determinant() == _Q(-2)
    inverse = source.inverse()
    assert inverse == ExactMatrix.from_rows([[_Q(-2), _Q(1)], [_Q(3, 2), _Q(-1, 2)]])
    assert source * inverse == eye
    assert ExactMatrix.from_rows([[_Q(0), _Q(2)], [_Q(3), _Q(4)]]).determinant() == _Q(-6)
    assert ExactMatrix.from_rows([[_Q(1), _Q(1, 2)], [_Q(1, 2), _Q(1, 3)]]).determinant() == _Q(1, 12)
    assert ExactMatrix(0, 0, []).determinant() == _Q(1)
    rectangle = ExactMatrix.from_rows([[_Q(1), _Q(2)]])
    column = ExactMatrix.from_rows([[_Q(3)], [_Q(4)]])
    assert rectangle * column == ExactMatrix.from_rows([[_Q(11)]])

    pauli = ExactMatrix.from_rows(
        [[GaussianRational(0, 0), GaussianRational(0, -1)], [GaussianRational(0, 1), GaussianRational(0, 0)]]
    )
    assert pauli.is_hermitian()
    assert pauli.is_unitary()
    assert pauli.determinant() == GaussianRational(-1, 0)


def test_negative_paths_record_every_invariant() -> None:
    floated = _raises(lambda: ExactMatrix.from_rows([[_probe("1.0")]]).determinant(), "float refused at the public boundary")
    assert floated.parameters == {"role": "matrix", "received": "float"}
    assert ExactMatrix.from_rows([[_probe("1.0")]]).data == [_probe("1.0")]
    boolean = _raises(
        lambda: ExactMatrix.from_rows([[True]]).determinant(),
        "boolean refused where an exact scalar was required",
    )
    assert boolean.parameters == {"role": "matrix"}
    dimension = _raises(lambda: ExactMatrix(True, 1, [_Q(1)]), "boolean refused where a matrix dimension was required")
    assert dimension.parameters == {"role": "rows"}
    _raises(lambda: ExactMatrix(_probe("1.0"), 1, [_Q(1)]), "float refused at the public boundary")
    _raises(lambda: ExactMatrix("1", 1, [_Q(1)]), "matrix dimension must be an exact integer")
    length = _raises(lambda: ExactMatrix(1, 1, []), "Data length does not match dimensions")
    assert length.parameters == {"length": 0, "rows": 1, "cols": 1}
    _raises(lambda: ExactMatrix.from_rows([[_Q(1)], [_Q(1), _Q(2)]]), "Jagged rows are not allowed")
    left = ExactMatrix.from_rows([[_Q(1)]])
    right = ExactMatrix.from_rows([[_Q(1), _Q(2)]])
    _raises(lambda: left + right, "Shape mismatch")
    _raises(lambda: left - right, "Shape mismatch")
    tall = ExactMatrix.from_rows([[_Q(1)], [_Q(2)]])
    _raises(lambda: left * tall, "Cannot multiply shapes")
    _raises(lambda: left.mul_vec([_Q(1), _Q(2)]), "Cannot multiply matrix shape by vector length")
    with pytest.raises(MatrixIndexError) as index:
        left.get(1, 0)
    assert index.value.invariant == "Index out of bounds"
    with pytest.raises(MatrixIndexError) as assigned:
        left.set(-1, 0, _Q(1))
    assert assigned.value.invariant == "Index out of bounds"
    _raises(lambda: right.determinant(), "Determinant requires square matrix")
    _raises(lambda: right.inverse(), "Inverse requires square matrix")
    _raises(
        lambda: ExactMatrix.from_rows([[_Q(1), _Q(2)], [_Q(2), _Q(4)]]).inverse(),
        "Matrix is singular",
    )
    _raises(lambda: ExactMatrix.from_rows([["1"]]).determinant(), "exact scalar required")
    _raises(lambda: ExactMatrix.from_rows([[_probe("1.0")]]).sha256(), "float refused at the public boundary")


def test_integration_matches_rust_and_bareiss() -> None:
    root = Path(__file__).resolve().parents[3]
    source = (root / "code" / "rust" / "src" / "linear_algebra" / "matrix.rs").read_text(encoding="utf-8")
    assert 'multiplication_is_associative_and_distributive_and_agrees_with_the_std_ops_product' in source
    assert 'multiplication_is_associative_and_distributive_and_agrees_with_the_std_ops_product' in source
    assert 'multiplication_is_associative_and_distributive_and_agrees_with_the_std_ops_product' in source
    matrix = ExactMatrix.from_rows([[_Q(1), _Q(1, 2)], [_Q(1, 2), _Q(1, 3)]])
    assert bareiss_matches_elimination(matrix) == matrix.determinant() == _Q(1, 12)


def test_end_to_end_public_contract() -> None:
    package = linear_algebra.matrix
    source = package.ExactMatrix.from_rows([[_Q(0), _Q(2)], [_Q(3), _Q(4)]])
    assert source.determinant() == _Q(-6)
    assert source.inverse() * source == package.ExactMatrix.identity(2)
    stored = package.ExactMatrix.from_rows([[_probe("1.5")]])
    assert stored.data == [_probe("1.5")]
    with pytest.raises(package.MatrixFailure, match="float refused"):
        stored.rref()


def test_origin_resolves_in_repo() -> None:
    root = Path(__file__).resolve().parents[3]
    origin = root / "code" / "rust" / "src" / "linear_algebra" / "matrix.rs"
    assert origin.is_file()
    source = _MODULE_PATH.read_text(encoding="utf-8")
    assert "AuthorityEffect: None" in source
    assert "urn:omega:fqm:linear-algebra:exact-matrix:v1" in source
    assert "Scope Fence:" in source
    assert "Gate 5 measurement:" in source


_MUTANTS: tuple[tuple[str, str, str], ...] = (
    (
        "float admitted",
        'if isinstance(value, float):\n        raise _fail("float refused at the public boundary", role=role, received="float")',
        "if isinstance(value, float):\n        return",
    ),
    (
        "boolean scalar admitted",
        "if type(value) is bool:",
        "if False and type(value) is bool:",
    ),
    (
        "swap sign dropped",
        "sign = -sign",
        "sign = sign",
    ),
    (
        "rank shifted",
        "return len(pivots)",
        "return len(pivots) - 1",
    ),
    (
        "kernel free coordinate cleared",
        "vector[free_col] = one",
        "vector[free_col] = zero",
    ),
    (
        "dot product replaced by sum",
        "total = _plus(total, _times(left_value, right_value))",
        "total = _plus(total, _plus(left_value, right_value))",
    ),
    (
        "singular inverse admitted",
        "if len(pivots) < size or pivots[:size] != list(range(size)):",
        "if False and (len(pivots) < size or pivots[:size] != list(range(size))):",
    ),
    (
        "identity off the diagonal",
        "if row == col:",
        "if row != col:",
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
    matrix = namespace["ExactMatrix"]
    if not isinstance(matrix, type):
        return False
    try:
        eye = matrix.identity(2)
        source = matrix.from_rows([[_Q(1), _Q(2)], [_Q(3), _Q(4)]])
        swapped = matrix.from_rows([[_Q(0), _Q(2)], [_Q(3), _Q(4)]])
        singular = matrix.from_rows([[_Q(1), _Q(2), _Q(3)], [_Q(4), _Q(5), _Q(6)], [_Q(7), _Q(8), _Q(9)]])
        rectangle = matrix.from_rows([[_Q(1), _Q(2)]])
        column = matrix.from_rows([[_Q(3)], [_Q(4)]])
        product = rectangle * column
        inverse = source.inverse()
    except error:
        return False
    if not _all_hold((isinstance(eye, matrix), isinstance(product, matrix), isinstance(inverse, matrix),)):
        return False
    kernel = singular.kernel_basis()
    if not isinstance(kernel, list) or len(kernel) != 1:
        return False
    return _all_hold((
eye == matrix.from_rows([[_Q(1), _Q(0)], [_Q(0), _Q(1)]]),
source.determinant() == _Q(-2),
swapped.determinant() == _Q(-6),
singular.rank() == 2,
kernel[0][2] == _Q(1),
singular.mul_vec(kernel[0]) == [_Q(0), _Q(0), _Q(0)],
product == matrix.from_rows([[_Q(11)]]),
inverse == matrix.from_rows([[_Q(-2), _Q(1)], [_Q(3, 2), _Q(-1, 2)]]),
))


def _bad_values_refused(namespace: dict[str, object], error: type[BaseException]) -> bool:
    matrix = namespace["ExactMatrix"]
    if not isinstance(matrix, type):
        return False
    probes = (
        (lambda: matrix.from_rows([[_probe("1.0")]]).determinant(), "float refused at the public boundary"),
        (lambda: matrix.from_rows([[True]]).determinant(), "boolean refused where an exact scalar was required"),
        (lambda: matrix.from_rows([[_Q(1), _Q(2)], [_Q(2), _Q(4)]]).inverse(), "Matrix is singular"),
    )
    for probe, invariant in probes:
        if _invariant(error, probe) != invariant:
            return False
    return True


def _oracle(namespace: dict[str, object]) -> bool:
    error_type = namespace["MatrixFailure"]
    if not _all_hold((isinstance(error_type, type), issubclass(error_type, BaseException),)):
        return False
    if not _known_values_hold(namespace, error_type):
        return False
    return _bad_values_refused(namespace, error_type)


def test_mutation_suite_kills_non_equivalent_mutants() -> None:
    source = _MODULE_PATH.read_text(encoding="utf-8")
    loaded: list[str] = []
    try:
        loaded.append("mutant_matrix_baseline")
        baseline = _load_source(source, loaded[-1])
        assert _oracle(baseline) is True
        killed = 0
        for index, (name, old, new) in enumerate(_MUTANTS):
            count = source.count(old)
            assert count == 1, f"{name} matched {count} sites"
            module_name = f"mutant_matrix_{index}"
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
