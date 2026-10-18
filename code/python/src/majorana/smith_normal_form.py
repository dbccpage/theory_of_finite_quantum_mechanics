from __future__ import annotations
"""Integer Smith Normal Form S = U A V over Z."""

from dataclasses import dataclass
import numpy as np


@dataclass
class SmithNormalFormResult:
    S: np.ndarray  
    U: np.ndarray  
    V: np.ndarray  


try:
    import cypari  # type: ignore
    _HAS_CYPARI = True
except ImportError:
    _HAS_CYPARI = False


def _egcd(a: int, b: int) -> tuple[int, int, int]:
    """Extended Euclidean Algorithm: returns (g, x, y) such that a*x + b*y = g."""
    if b == 0:
        return (abs(a), 1 if a >= 0 else -1, 0)
    g, x1, y1 = _egcd(b, a % b)
    x = y1
    y = x1 - (a // b) * y1
    return (g, x, y)


def compute_smith_normal_form(matrix: np.ndarray) -> SmithNormalFormResult:
    """Computes exact integer Smith Normal Form S = U A V over Z.
    
    Dispatches to PARI/GP (cypari matsnf) if installed, otherwise uses
    the exact list-of-lists Extended Euclidean reference solver.
    """
    m, n = matrix.shape
    if m == 0 or n == 0:
        return SmithNormalFormResult(
            S=np.zeros((m, n), dtype=int),
            U=np.eye(m, dtype=int),
            V=np.eye(n, dtype=int),
        )

    if _HAS_CYPARI and min(m, n) > 16:
        try:
            pari_m = cypari.pari.matrix(m, n, matrix.flatten().tolist())
            res = pari_m.matsnf(1)  
            U = np.array(res[0], dtype=int)
            V = np.array(res[1], dtype=int)
            S_diag = np.array(res[2], dtype=int)
            S = np.zeros((m, n), dtype=int)
            for i, val in enumerate(S_diag):
                if i < min(m, n):
                    S[i, i] = val
            return SmithNormalFormResult(S=S, U=U, V=V)
        except Exception:
            pass  

    A = [[int(matrix[i, j]) for j in range(n)] for i in range(m)]
    U = [[1 if i == j else 0 for j in range(m)] for i in range(m)]
    V = [[1 if i == j else 0 for j in range(n)] for i in range(n)]

    r = min(m, n)

    for k in range(r):
        while True:
            min_val = None
            pivot_pos = None
            for i in range(k, m):
                for j in range(k, n):
                    val = abs(A[i][j])
                    if val != 0 and (min_val is None or val < min_val):
                        min_val = val
                        pivot_pos = (i, j)

            if pivot_pos is None:
                break

            pi, pj = pivot_pos
            if pi != k:
                A[pi], A[k] = A[k], A[pi]
                U[pi], U[k] = U[k], U[pi]
            if pj != k:
                for row in A:
                    row[pj], row[k] = row[k], row[pj]
                for row in V:
                    row[pj], row[k] = row[k], row[pj]

            if A[k][k] < 0:
                A[k] = [-x for x in A[k]]
                U[k] = [-x for x in U[k]]

            changed = False

            for i in range(k + 1, m):
                if A[i][k] != 0:
                    g, x, y = _egcd(A[k][k], A[i][k])
                    q1 = A[k][k] // g
                    q2 = A[i][k] // g
                    row_k, row_i = A[k][:], A[i][:]
                    A[k] = [x * rk + y * ri for rk, ri in zip(row_k, row_i)]
                    A[i] = [-q2 * rk + q1 * ri for rk, ri in zip(row_k, row_i)]

                    u_k, u_i = U[k][:], U[i][:]
                    U[k] = [x * uk + y * ui for uk, ui in zip(u_k, u_i)]
                    U[i] = [-q2 * uk + q1 * ui for uk, ui in zip(u_k, u_i)]
                    changed = True

            for j in range(k + 1, n):
                if A[k][j] != 0:
                    g, x, y = _egcd(A[k][k], A[k][j])
                    q1 = A[k][k] // g
                    q2 = A[k][j] // g
                    for row in A:
                        val_k, val_j = row[k], row[j]
                        row[k] = x * val_k + y * val_j
                        row[j] = -q2 * val_k + q1 * val_j

                    for row in V:
                        val_k, val_j = row[k], row[j]
                        row[k] = x * val_k + y * val_j
                        row[j] = -q2 * val_k + q1 * val_j
                    changed = True

            divides_all = True
            for i in range(k + 1, m):
                for j in range(k + 1, n):
                    if A[i][j] != 0 and A[i][j] % A[k][k] != 0:
                        for col in range(n):
                            A[k][col] += A[i][col]
                        for col in range(m):
                            U[k][col] += U[i][col]
                        divides_all = False
                        changed = True
                        break
                if not divides_all:
                    break

            if not changed and divides_all:
                break

    rank = sum(1 for i in range(r) if A[i][i] != 0)
    for k in range(rank - 1):
        if A[k + 1][k + 1] % A[k][k] != 0:
            for col in range(n):
                A[k][col] += A[k + 1][col]
            for col in range(m):
                U[k][col] += U[k + 1][col]

            g, x, y = _egcd(A[k][k], A[k][k + 1])
            q1, q2 = A[k][k] // g, A[k][k + 1] // g
            for row in A:
                val_k, val_j = row[k], row[k + 1]
                row[k] = x * val_k + y * val_j
                row[k + 1] = -q2 * val_k + q1 * val_j
            for row in V:
                val_k, val_j = row[k], row[k + 1]
                row[k] = x * val_k + y * val_j
                row[k + 1] = -q2 * val_k + q1 * val_j

            if A[k + 1][k] != 0:
                g, x, y = _egcd(A[k][k], A[k + 1][k])
                q1, q2 = A[k][k] // g, A[k + 1][k] // g
                row_k, row_i = A[k][:], A[k + 1][:]
                A[k] = [x * rk + y * ri for rk, ri in zip(row_k, row_i)]
                A[k + 1] = [-q2 * rk + q1 * ri for rk, ri in zip(row_k, row_i)]
                u_k, u_i = U[k][:], U[k + 1][:]
                U[k] = [x * uk + y * ui for uk, ui in zip(u_k, u_i)]
                U[k + 1] = [-q2 * uk + q1 * ui for uk, ui in zip(u_k, u_i)]

    for i in range(r):
        if A[i][i] < 0:
            A[i][i] = -A[i][i]
            U[i] = [-x for x in U[i]]

    return SmithNormalFormResult(
        S=np.array(A, dtype=int),
        U=np.array(U, dtype=int),
        V=np.array(V, dtype=int),
    )



from dataclasses import dataclass  
from enum import Enum  
from typing import Any  


class _RustSurfaceMeta(type):
    def __getattr__(cls, name: str) -> Any:
        if name.startswith("__") and name.endswith("__"):
            raise AttributeError(name)

        def unavailable(*args: Any, **kwargs: Any) -> Any:
            raise NotImplementedError(
                f"Behavioral method {cls.__name__}.{name} is not ported"
            )

        return unavailable


class _RustSurfaceObject(metaclass=_RustSurfaceMeta):
    def __getattr__(self, name: str) -> Any:
        if name.startswith("__") and name.endswith("__"):
            raise AttributeError(name)

        def unavailable(*args: Any, **kwargs: Any) -> Any:
            raise NotImplementedError(
                f"Behavioral method {type(self).__name__}.{name} is not ported"
            )

        return unavailable


TorsionError = Enum(
    "TorsionError",
    {
        "NonIntegerEntry": "NonIntegerEntry",
        "EntryCeiling": "EntryCeiling",
        "OverflowCeiling": "OverflowCeiling",
        "InvalidDegree": "InvalidDegree",
    },
    type=str,
)
TorsionError.__doc__ = "Structural mirror of Rust ``TorsionError`` variants."


def invariant_factors(*args: Any, **kwargs: Any) -> Any:
    """Structural mirror of Rust callable ``invariant_factors``."""

    raise NotImplementedError(
        "Behavioral port not implemented; Rust authority: omega_engine/crates/omega_homology/src/smith_normal_form.rs::invariant_factors"
    )


def torsion_coefficients(*args: Any, **kwargs: Any) -> Any:
    """Structural mirror of Rust callable ``torsion_coefficients``."""

    raise NotImplementedError(
        "Behavioral port not implemented; Rust authority: omega_engine/crates/omega_homology/src/smith_normal_form.rs::torsion_coefficients"
    )




