from __future__ import annotations

import numpy as np

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

def _pauli_product(left, right):
    """Multiply phase-Paulis (phase mod 4, x bits, z bits) on two qubits."""
    phase = (left[0] + right[0] + 2 * sum(left[2][i] * right[1][i] for i in range(2))) % 4
    x_bits = tuple(left[1][i] ^ right[1][i] for i in range(2))
    z_bits = tuple(left[2][i] ^ right[2][i] for i in range(2))
    return (phase, x_bits, z_bits)


def _symplectic(left, right) -> int:
    total = 0
    for index in range(2):
        total += left[1][index] * right[2][index] + right[1][index] * left[2][index]
    return total % 2


def verify_mermin_peres_parity() -> bool:
    """Row products are +I and the column products are +I, +I, -I.

    Each observable is (phase, X bits, Z bits) on two qubits. Y = iXZ has phase 1.
    """
    identity = (0, (0, 0), (0, 0))
    xx = (0, (1, 1), (0, 0))
    xi = (0, (1, 0), (0, 0))
    ix = (0, (0, 1), (0, 0))
    iz = (0, (0, 0), (0, 1))
    zi = (0, (0, 0), (1, 0))
    zz = (0, (0, 0), (1, 1))
    xz = (0, (1, 0), (0, 1))
    zx = (0, (0, 1), (1, 0))
    yy = (2, (1, 1), (1, 1))
    y = (1, (1,), (1,))
    del yy
    grid = (
        (xi, ix, xx),
        (iz, zi, zz),
        (xz, zx, None),
    )
    yy = _pauli_product((1, (1, 0), (1, 0)), (1, (0, 1), (0, 1)))
    grid = (grid[0], grid[1], (xz, zx, yy))
    del y
    minus_identity = (2, (0, 0), (0, 0))
    expected_columns = (identity, identity, minus_identity)
    for row in grid:
        for left in row:
            for right in row:
                if _symplectic(left, right) != 0:
                    return False
        product = _pauli_product(_pauli_product(row[0], row[1]), row[2])
        if product != identity:
            return False
    for column in range(3):
        entries = (grid[0][column], grid[1][column], grid[2][column])
        for left in entries:
            for right in entries:
                if _symplectic(left, right) != 0:
                    return False
        product = _pauli_product(_pauli_product(entries[0], entries[1]), entries[2])
        if product != expected_columns[column]:
            return False
    return True

__all__ = ['I2', 'I4', 'SIGMA_X', 'SIGMA_Y', 'SIGMA_Z', 'construct_mermin_peres_grid', 'verify_mermin_peres_parity']
