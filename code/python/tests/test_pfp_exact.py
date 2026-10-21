"""Tests for pfp_exact rational matrix operations and adversarial bounds."""
from fractions import Fraction as Q
import pytest

from src.qm.pfp_exact import (
    MAX_BITS,
    MAX_PRINCIPAL_MINOR_DIM,
    add,
    determinant,
    eye,
    is_psd,
    matrix,
    multiply,
    principal_minors,
    rank,
    rref,
    scalar,
    scale,
    solve_unique,
    tensor,
    trace,
    transpose,
)


def test_scalar_admission_and_bounds():
    assert scalar(1) == Q(1)
    assert scalar(Q(3, 5)) == Q(3, 5)
    assert scalar(-7) == Q(-7)

    # Rejection of float
    with pytest.raises(TypeError, match="float refused"):
        scalar(1.5)

    # Rejection of bool
    with pytest.raises(TypeError, match="boolean refused"):
        scalar(True)
    with pytest.raises(TypeError, match="boolean refused"):
        scalar(False)

    # Rejection of invalid types
    with pytest.raises(TypeError, match="exact integer or Fraction required"):
        scalar("1/2")

    # 1024-bit allowed
    ok_int = (1 << 1024) - 1
    assert scalar(ok_int) == Q(ok_int)

    # 1025-bit integer refused
    with pytest.raises(ValueError, match="integer exceeds 1024-bit limit"):
        scalar(1 << 1025)

    # 1025-bit rational numerator/denominator refused
    with pytest.raises(ValueError, match="rational component exceeds 1024-bit limit"):
        scalar(Q(1 << 1025, 1))

    with pytest.raises(ValueError, match="rational component exceeds 1024-bit limit"):
        scalar(Q(1, 1 << 1025))


def test_matrix_construction_and_refusals():
    m = matrix([[1, 2], [3, 4]])
    assert m == ((Q(1), Q(2)), (Q(3), Q(4)))

    # Empty matrix
    with pytest.raises(ValueError, match="nonempty rectangular matrix required"):
        matrix([])
    with pytest.raises(ValueError, match="nonempty rectangular matrix required"):
        matrix([[]])

    # Non-rectangular matrix
    with pytest.raises(ValueError, match="nonempty rectangular matrix required"):
        matrix([[1, 2], [3]])

    # Float in matrix
    with pytest.raises(TypeError, match="float refused"):
        matrix([[1, 2.0], [3, 4]])

    # Boolean in matrix
    with pytest.raises(TypeError, match="boolean refused"):
        matrix([[True, 0], [0, 1]])

    # 1025-bit int in matrix
    with pytest.raises(ValueError, match="1024-bit limit"):
        matrix([[1 << 1025, 0], [0, 1]])


def test_matrix_algebra():
    a = matrix([[1, 2], [3, 4]])
    b = matrix([[5, 6], [7, 8]])

    # Eye
    assert eye(2) == ((Q(1), Q(0)), (Q(0), Q(1)))
    with pytest.raises(ValueError, match="positive dimension required"):
        eye(0)
    with pytest.raises(ValueError, match="positive dimension required"):
        eye(-1)

    # Transpose
    assert transpose(a) == ((Q(1), Q(3)), (Q(2), Q(4)))

    # Scale
    assert scale(2, a) == ((Q(2), Q(4)), (Q(6), Q(8)))

    # Add
    assert add(a, b) == ((Q(6), Q(8)), (Q(10), Q(12)))
    with pytest.raises(ValueError, match="matrix shape mismatch"):
        add(a, eye(3))

    # Multiply
    assert multiply(a, eye(2)) == a
    assert multiply(a, b) == ((Q(19), Q(22)), (Q(43), Q(50)))
    with pytest.raises(ValueError, match="matrix product shape mismatch"):
        multiply(a, eye(3))

    # Trace
    assert trace(a) == Q(5)
    with pytest.raises(ValueError, match="square matrix required"):
        trace([[1, 2, 3], [4, 5, 6]])

    # Tensor
    t = tensor([[1, 0], [0, 1]], [[2]])
    assert t == ((Q(2), Q(0)), (Q(0), Q(2)))


def test_determinant_and_solve():
    a = matrix([[1, 2], [3, 4]])
    assert determinant(a) == Q(-2)

    sing = matrix([[1, 2], [2, 4]])
    assert determinant(sing) == Q(0)

    # Solve unique
    sol = solve_unique(a, [5, 11])
    assert sol == (Q(1), Q(2))

    with pytest.raises(ValueError, match="system has no unique solution"):
        solve_unique(sing, [1, 2])


def test_principal_minors_and_cap():
    m = matrix([[2, -1], [-1, 2]])
    pm = principal_minors(m)
    # Dimension 2 has ( ( (0,), 2 ), ( (1,), 2 ), ( (0, 1), 3 ) )
    assert len(pm) == 3

    # Asymmetric matrix raises ValueError
    with pytest.raises(ValueError, match="symmetric matrix required"):
        principal_minors([[1, 2], [3, 4]])

    # Dimension cap: 9x9 matrix exceeds MAX_PRINCIPAL_MINOR_DIM
    big = eye(MAX_PRINCIPAL_MINOR_DIM + 1)
    with pytest.raises(ValueError, match="exceeds principal minor evaluation envelope"):
        principal_minors(big)


def test_is_psd():
    # Positive definite
    assert is_psd([[2, -1], [-1, 2]]) is True
    assert is_psd([[4, 12, -16], [12, 37, -43], [-16, -43, 98]]) is True

    # Positive semidefinite (singular, e.g. projector or zero)
    assert is_psd([[1, 1], [1, 1]]) is True
    assert is_psd([[0, 0], [0, 0]]) is True
    assert is_psd([[1, 0, 0], [0, 0, 0], [0, 0, 0]]) is True

    # Indefinite
    assert is_psd([[1, 2], [2, 1]]) is False

    # Negative definite
    assert is_psd([[-1, 0], [0, -1]]) is False

    # Asymmetric
    with pytest.raises(ValueError, match="symmetric matrix required"):
        is_psd([[1, 2], [3, 4]])
