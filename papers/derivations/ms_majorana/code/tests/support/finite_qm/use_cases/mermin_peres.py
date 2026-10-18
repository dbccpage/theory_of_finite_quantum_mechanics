# AuthorityEffect: None.
from __future__ import annotations
import numpy as np

# Pauli matrices
I2 = np.eye(2, dtype=complex)
SIGMA_X = np.array([[0, 1], [1, 0]], dtype=complex)
SIGMA_Y = np.array([[0, -1j], [1j, 0]], dtype=complex)
SIGMA_Z = np.array([[1, 0], [0, -1]], dtype=complex)
I4 = np.eye(4, dtype=complex)

def construct_mermin_peres_grid() -> list[list[np.ndarray]]:
    """Constructs the 3x3 Mermin-Peres magic square of observables on C^4."""
    row1 = [
        np.kron(SIGMA_X, I2),
        np.kron(I2, SIGMA_X),
        np.kron(SIGMA_X, SIGMA_X),
    ]
    row2 = [
        np.kron(I2, SIGMA_Z),
        np.kron(SIGMA_Z, I2),
        np.kron(SIGMA_Z, SIGMA_Z),
    ]
    row3 = [
        np.kron(SIGMA_X, SIGMA_Z),
        np.kron(SIGMA_Z, SIGMA_X),
        np.kron(SIGMA_Y, SIGMA_Y),
    ]
    return [row1, row2, row3]

def verify_mermin_peres_parity() -> bool:
    """Verifies that row products equal +I4 and column products equal (+I4, +I4, -I4)."""
    grid = construct_mermin_peres_grid()

    # Verify rows commute and product to +I4
    for r in range(3):
        # pairwise commutation
        for i in range(3):
            for j in range(3):
                comm = grid[r][i] @ grid[r][j] - grid[r][j] @ grid[r][i]
                if not np.allclose(comm, 0, atol=1e-12):
                    return False
        row_prod = grid[r][0] @ grid[r][1] @ grid[r][2]
        if not np.allclose(row_prod, I4, atol=1e-12):
            return False

    # Verify columns commute and product to +I4, +I4, -I4
    for c in range(3):
        # pairwise commutation
        for i in range(3):
            for j in range(3):
                comm = grid[i][c] @ grid[j][c] - grid[j][c] @ grid[i][c]
                if not np.allclose(comm, 0, atol=1e-12):
                    return False
        col_prod = grid[0][c] @ grid[1][c] @ grid[2][c]
        expected = I4 if c < 2 else -I4
        if not np.allclose(col_prod, expected, atol=1e-12):
            return False

    return True

__all__ = ['I2', 'I4', 'SIGMA_X', 'SIGMA_Y', 'SIGMA_Z', 'construct_mermin_peres_grid', 'verify_mermin_peres_parity']
