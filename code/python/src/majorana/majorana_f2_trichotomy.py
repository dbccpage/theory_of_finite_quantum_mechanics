"""
majorana_f2_trichotomy.py — GF(2) Cochain Complex, Residual Trichotomy & Tetron Carrier.

Origin: papers/core/majorana/the_majorana_problem.md
Claim: urn:omega:fqm:majorana:maj-c2-f2-trichotomy:v1
AuthorityEffect: None.

Mechanizes:
1. GF(2) matrix arithmetic, products, and Gaussian solves.
2. Discrete cochain complex coboundary nilpotency d1 * d0 = 0 (mod 2) with strict refusal.
3. Residual classification into Exact, ClosedResidual, or OpenObstruction (Claim MAJ-C2).
4. 2D Tetron-array carriers on Disk (H1=0), Cylinder (H1=1), and Torus (H1=2).
5. Norm equivalence on binary carriers: ||v||_p^p = wt(v) (Claim MAJ-C17).
6. Quotient mass coset weight Phi_1([r]) under declared caller budget.
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import Dict, List, Optional, Tuple
import numpy as np


# The host wire refuses a count above 1_000_000. 2**20 does not cross it.
_CLASSIFY_BUDGET = 1_000_000


class TrichotomyClass(Enum):
    EXACT = "Exact"
    CLOSED_RESIDUAL = "ClosedResidual"
    OPEN_OBSTRUCTION = "OpenObstruction"
    REPRESENTATION_INVALID = "RepresentationInvalid"


def _stored_bit(value: object) -> int:
    if isinstance(value, bool):
        return int(value)
    if isinstance(value, (int, np.integer)):
        return int(value) & 1
    raise TypeError("GF(2) entries must be integers, not floats")


def _vector_bits(vec: np.ndarray | Tuple[int, ...] | List[int]) -> List[int]:
    if isinstance(vec, np.ndarray):
        if vec.dtype.kind == "f":
            raise TypeError("GF(2) vectors must be integers, not floats")
        return [_stored_bit(value) for value in vec.reshape(-1).tolist()]
    return [_stored_bit(value) for value in vec]


@dataclass(frozen=True)
class GF2Matrix:
    """Public GF(2) carrier. Rank, products, and solves via exact modulo 2 arithmetic."""
    rows: int
    cols: int
    data: Tuple[Tuple[int, ...], ...]

    @classmethod
    def from_array(cls, arr: np.ndarray | List[List[int]]) -> GF2Matrix:
        if isinstance(arr, np.ndarray):
            if arr.ndim != 2:
                raise ValueError("GF(2) matrix must be two-dimensional")
            if arr.dtype.kind == "f":
                raise TypeError("GF(2) entries must be integers, not floats")
            raw = arr.tolist()
        else:
            raw = arr
        rows = []
        for row in raw:
            if isinstance(row, (str, bytes)):
                raise TypeError("GF(2) matrix row must be a sequence of bits")
            rows.append(tuple(_stored_bit(value) for value in row))
        cols = len(rows[0]) if rows else 0
        if any(len(row) != cols for row in rows):
            raise ValueError("All matrix rows must have equal length")
        return cls(rows=len(rows), cols=cols, data=tuple(rows))

    def to_array(self) -> np.ndarray:
        return np.array(self.data, dtype=int)

    def matmul(self, other: GF2Matrix) -> GF2Matrix:
        if self.cols != other.rows:
            raise ValueError(f"Shape mismatch: ({self.rows}, {self.cols}) x ({other.rows}, {other.cols})")
        res = []
        for r in range(self.rows):
            row_vals = []
            for c in range(other.cols):
                val = 0
                for k in range(self.cols):
                    val ^= (self.data[r][k] & other.data[k][c])
                row_vals.append(val & 1)
            res.append(tuple(row_vals))
        return GF2Matrix(rows=self.rows, cols=other.cols, data=tuple(res))

    def matvec(self, vec: Tuple[int, ...] | np.ndarray) -> np.ndarray:
        bits = _vector_bits(vec)
        if len(bits) != self.cols:
            raise ValueError(f"Vector length {len(bits)} does not match matrix columns {self.cols}")
        res = []
        for row in self.data:
            val = 0
            for a, b in zip(row, bits):
                val ^= (a & b)
            res.append(val & 1)
        return np.asarray(res, dtype=int)

    def rank(self) -> int:
        m = [list(r) for r in self.data]
        row = 0
        for col in range(self.cols):
            piv = None
            for r in range(row, self.rows):
                if m[r][col] == 1:
                    piv = r
                    break
            if piv is None:
                continue
            m[row], m[piv] = m[piv], m[row]
            for r in range(self.rows):
                if r != row and m[r][col] == 1:
                    for c in range(self.cols):
                        m[r][c] ^= m[row][c]
            row += 1
            if row == self.rows:
                break
        return row

    def solve(self, rhs: np.ndarray | Tuple[int, ...]) -> Optional[np.ndarray]:
        """Solve Ax = b over GF(2) via augmented Gaussian elimination."""
        bits = _vector_bits(rhs)
        if len(bits) != self.rows:
            return None
        m = [list(self.data[r]) + [bits[r]] for r in range(self.rows)]
        row = 0
        pivots = []
        for col in range(self.cols):
            piv = None
            for r in range(row, self.rows):
                if m[r][col] == 1:
                    piv = r
                    break
            if piv is None:
                continue
            m[row], m[piv] = m[piv], m[row]
            pivots.append((row, col))
            for r in range(self.rows):
                if r != row and m[r][col] == 1:
                    for c in range(self.cols + 1):
                        m[r][c] ^= m[row][c]
            row += 1
            if row == self.rows:
                break
        for r in range(self.rows):
            if all(m[r][c] == 0 for c in range(self.cols)) and m[r][self.cols] == 1:
                return None
        sol = [0] * self.cols
        for r, col in pivots:
            sol[col] = m[r][self.cols]
        return np.asarray(sol, dtype=int)


@dataclass
class F2CochainComplex:
    """Finite cochain complex C0 -> C1 -> C2 over GF(2)."""
    n0: int
    n1: int
    n2: int
    d0: GF2Matrix
    d1: GF2Matrix

    def is_nilpotent(self) -> bool:
        """Verify d1 * d0 = 0 (mod 2) by the matrix product."""
        prod = self.d1.matmul(self.d0)
        return all(bit == 0 for row in prod.data for bit in row)

    def betti_1(self) -> int:
        """dim H1 = (n1 - rank(d1)) - rank(d0)."""
        if not self.is_nilpotent():
            raise ValueError("Complex is not nilpotent; H1 is undefined.")
        rank_d0 = self.d0.rank()
        rank_d1 = self.d1.rank()
        dim_ker_d1 = self.n1 - rank_d1
        return dim_ker_d1 - rank_d0


def classify_residual(
    complex: F2CochainComplex,
    omega: np.ndarray | Tuple[int, ...]
) -> Tuple[TrichotomyClass, Dict[str, object]]:
    """
    Classify an edge residual into Exact, ClosedResidual, or OpenObstruction.
    A length mismatch or a complex with d1 * d0 != 0 is RepresentationInvalid.
    """
    bits = _vector_bits(omega)
    if not complex.is_nilpotent():
        return TrichotomyClass.REPRESENTATION_INVALID, {"reason": "d1 * d0 != 0"}
    if len(bits) != complex.n1:
        return TrichotomyClass.REPRESENTATION_INVALID, {"reason": f"length mismatch: {len(bits)} != {complex.n1}"}

    syndrome = complex.d1.matvec(bits).tolist()
    syndrome_wt = int(sum(syndrome))
    if syndrome_wt > 0:
        return TrichotomyClass.OPEN_OBSTRUCTION, {
            "syndrome": syndrome,
            "syndrome_weight": syndrome_wt,
        }

    alpha = complex.d0.solve(bits)
    if alpha is not None:
        alpha_bits = [int(entry) for entry in alpha]
        return TrichotomyClass.EXACT, {
            "gauge_potential": alpha_bits,
            "gauge_weight": int(sum(alpha_bits)),
        }

    return TrichotomyClass.CLOSED_RESIDUAL, {
        "homology_class": "non_trivial",
        "syndrome_weight": 0,
        "native_terminal": "ClosedResidual",
    }


@dataclass
class TetronCarrier:
    """Represents a 2D surface carrier of Majorana tetron cells."""
    topology: str
    rows: int
    cols: int
    complex: F2CochainComplex
    h1_dim: int
    code_distance: Optional[int]


def build_tetron_carrier(topology: str, rows: int, cols: int) -> TetronCarrier:
    """
    Construct a 2D surface carrier of Majorana tetron cells over GF(2).
    """
    topo = topology.strip().lower()
    if topo == "disk":
        wrap_r, wrap_c = False, False
        h1_dim = 0
        code_dist = None
    elif topo == "cylinder":
        wrap_r, wrap_c = False, True
        h1_dim = 1
        code_dist = rows + 1
    elif topo == "torus":
        wrap_r, wrap_c = True, True
        h1_dim = 2
        code_dist = min(rows, cols)
    else:
        raise ValueError(f"Unknown topology: {topology}")

    vrows = rows if wrap_r else rows + 1
    vcols = cols if wrap_c else cols + 1
    num_mzm = vrows * vcols

    def mzm(i: int, j: int) -> int:
        return (i % vrows) * vcols + (j % vcols)

    d0_rows: list[list[int]] = []

    def add_channel(u: int, v: int) -> int:
        row = [0] * num_mzm
        row[u] ^= 1
        row[v] ^= 1
        d0_rows.append(row)
        return len(d0_rows) - 1

    h_span = vcols if wrap_c else vcols - 1
    horizontal = [[-1] * h_span for _ in range(vrows)]
    for i in range(vrows):
        for j in range(h_span):
            horizontal[i][j] = add_channel(mzm(i, j), mzm(i, j + 1))

    v_span = vrows if wrap_r else vrows - 1
    vertical = [[-1] * vcols for _ in range(v_span)]
    for i in range(v_span):
        for j in range(vcols):
            vertical[i][j] = add_channel(mzm(i, j), mzm(i + 1, j))

    num_channels = len(d0_rows)

    d1_rows: list[list[int]] = []
    for i in range(rows):
        for j in range(cols):
            row = [0] * num_channels
            j_next = (j + 1) % vcols if wrap_c else j + 1
            i_next = (i + 1) % vrows if wrap_r else i + 1
            row[horizontal[i][j]] ^= 1
            row[vertical[i][j_next]] ^= 1
            row[horizontal[i_next][j]] ^= 1
            row[vertical[i][j]] ^= 1
            d1_rows.append(row)

    num_islands = len(d1_rows)

    d0 = GF2Matrix.from_array(d0_rows)
    d1 = GF2Matrix.from_array(d1_rows)

    return TetronCarrier(
        topology=topo,
        rows=rows,
        cols=cols,
        complex=F2CochainComplex(n0=num_mzm, n1=num_channels, n2=num_islands, d0=d0, d1=d1),
        h1_dim=h1_dim,
        code_distance=code_dist,
    )


def logical_representative(
    carrier: TetronCarrier,
    axis: str = "column",
    index: int = 0,
) -> np.ndarray:
    """
    Address one logical 1-cochain on the tetron channel layout.
    - axis='column': all horizontal channels in column slot `index`.
    - axis='row': all vertical channels in row slot `index`.
    """
    res = np.zeros(carrier.complex.n1, dtype=int)
    rows, cols = carrier.rows, carrier.cols
    h_rows = rows if carrier.topology == "torus" else rows + 1
    n_h = h_rows * cols

    if axis == "column":
        col_slot = index % cols
        for r in range(h_rows):
            h_idx = r * cols + col_slot
            res[h_idx] = 1
    elif axis == "row":
        row_slot = index % rows
        for c in range(cols):
            v_idx = n_h + (row_slot * cols + c)
            res[v_idx] = 1
    else:
        raise ValueError(f"axis must be 'row' or 'column', got {axis}")
    return res


def compute_coset_weight(
    cochain: F2CochainComplex,
    residual: np.ndarray,
    budget_max: int = 1_000_000
) -> Tuple[int, bool]:
    """
    Compute minimal Hamming weight Phi_1([r]) = min_{alpha} wt(residual ^ d0 * alpha)
    and exactness within budget_max.
    """
    bits = _vector_bits(residual)
    m = [list(r) for r in cochain.d0.data]
    pivots = []
    row = 0
    for col in range(cochain.d0.cols):
        piv = None
        for r in range(row, cochain.d0.rows):
            if m[r][col] == 1:
                piv = r
                break
        if piv is None:
            continue
        m[row], m[piv] = m[piv], m[row]
        pivots.append(col)
        for r in range(cochain.d0.rows):
            if r != row and m[r][col] == 1:
                for c in range(cochain.d0.cols):
                    m[r][c] ^= m[row][c]
        row += 1
        if row == cochain.d0.rows:
            break

    k = len(pivots)
    total_elements = 1 << k
    exact = True
    if total_elements > budget_max:
        exact = False
        limit = budget_max
    else:
        limit = total_elements

    basis_cols = [[cochain.d0.data[r][c] for r in range(cochain.d0.rows)] for c in pivots]

    min_wt = sum(bits)
    curr = list(bits)
    for mask in range(1, limit):
        diff = mask ^ (mask - 1)
        flipped = diff.bit_length() - 1
        if flipped < k:
            b_col = basis_cols[flipped]
            for r in range(cochain.d0.rows):
                curr[r] ^= b_col[r]
            wt = sum(curr)
            if wt < min_wt:
                min_wt = wt

    return min_wt, exact


def verify_norm_equivalence(vector: np.ndarray | List[int]) -> bool:
    """
    Verifies Theorem 6.1: on binary entries v in {0, 1}^n, ||v||_p^p = wt(v) for all p >= 1.
    """
    v = np.asarray(vector, dtype=int) % 2
    wt = int(np.sum(v))
    for p in (1, 2, 3, 4, 10):
        lp_norm_pow = int(np.sum(v ** p))
        if lp_norm_pow != wt:
            return False
    return True
