"""Majorana GF(2) parity diagnostic classifier / receipt, and cyclotomic ring Z[zeta_16].

Authority fence:
- AuthorityEffect: None on every emitted certificate.
- Not a CODA_GTLA / sweep / CODA authority terminalizer; does not mint CertifiedAuthority.
- Does not promote FOC ExactRepair or any other terminal status.
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import Optional, Sequence

AUTHORITY_FENCE = (
    "AuthorityEffect None; not PROVED; not GlobalGreen; not physical Majorana; "
    "GF(2) diagnostic only."
)


class GF2ScheduleStatus(str, Enum):
    Exact = "Exact"
    ClosedResidual = "ClosedResidual"
    OpenObstruction = "OpenObstruction"


@dataclass(frozen=True)
class Cyclotomic16Element:
    """Element of Z[zeta_16] mod (zeta^8 + 1) with 8 integer coefficients."""
    coeffs: tuple[int, ...]  # length 8

    def __post_init__(self) -> None:
        if len(self.coeffs) != 8:
            raise ValueError("Cyclotomic16Element requires exactly 8 coefficients")

    @classmethod
    def zero(cls) -> Cyclotomic16Element:
        return cls((0,) * 8)

    @classmethod
    def one(cls) -> Cyclotomic16Element:
        return cls((1,) + (0,) * 7)

    @classmethod
    def zeta(cls) -> Cyclotomic16Element:
        return cls((0, 1) + (0,) * 6)

    @classmethod
    def from_int(cls, n: int) -> Cyclotomic16Element:
        return cls((n,) + (0,) * 7)

    def add(self, other: Cyclotomic16Element) -> Cyclotomic16Element:
        return Cyclotomic16Element(tuple(a + b for a, b in zip(self.coeffs, other.coeffs)))

    def multiply(self, other: Cyclotomic16Element) -> Cyclotomic16Element:
        # Multiply polynomials and reduce modulo zeta^8 + 1 (zeta^8 = -1)
        raw = [0] * 15
        for i in range(8):
            for j in range(8):
                raw[i + j] += self.coeffs[i] * other.coeffs[j]
        res = [raw[k] - raw[k + 8] for k in range(7)]
        res.append(raw[7])
        return Cyclotomic16Element(tuple(res))

    def power(self, exponent: int) -> Cyclotomic16Element:
        if exponent < 0:
            raise ValueError("Negative exponents not supported in Z[zeta_16]")
        result = Cyclotomic16Element.one()
        base = self
        curr = exponent
        while curr > 0:
            if curr % 2 == 1:
                result = result.multiply(base)
            base = base.multiply(base)
            curr //= 2
        return result


@dataclass(frozen=True)
class GF2Matrix:
    rows: int
    cols: int
    data: tuple[tuple[int, ...], ...]

    @classmethod
    def zeros(cls, rows: int, cols: int) -> GF2Matrix:
        return cls(rows, cols, tuple((0,) * cols for _ in range(rows)))

    @classmethod
    def from_data(cls, data: Sequence[Sequence[int]]) -> GF2Matrix:
        rows = len(data)
        if rows == 0:
            return cls(0, 0, ())
        cols = max(len(r) for r in data)
        norm_data = []
        for r in data:
            row_list = [(x % 2) for x in r]
            if len(row_list) < cols:
                row_list.extend([0] * (cols - len(row_list)))
            norm_data.append(tuple(row_list))
        return cls(rows, cols, tuple(norm_data))

    def multiply_vector(self, v: Sequence[int]) -> list[int]:
        if len(v) != self.cols:
            raise ValueError(f"Vector length {len(v)} != matrix cols {self.cols}")
        res = []
        for row in self.data:
            acc = 0
            for a, b in zip(row, v):
                acc ^= (a & (b % 2))
            res.append(acc & 1)
        return res

    def row_reduce(self) -> tuple[GF2Matrix, list[int], int]:
        m = [list(r) for r in self.data]
        pivot_cols = []
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
            pivot_cols.append(col)
            for r in range(self.rows):
                if r != row and m[r][col] == 1:
                    for c in range(self.cols):
                        m[r][c] ^= m[row][c]
            row += 1
            if row == self.rows:
                break
        return GF2Matrix.from_data(m), pivot_cols, len(pivot_cols)

    def rank(self) -> int:
        _, _, r = self.row_reduce()
        return r

    @classmethod
    def from_array(cls, arr: Sequence[Sequence[int]]) -> GF2Matrix:
        return cls.from_data(arr)

    def to_array(self) -> list[list[int]]:
        return [list(r) for r in self.data]

    def shape(self) -> tuple[int, int]:
        return self.rows, self.cols

    def matvec(self, v: Sequence[int]) -> list[int]:
        return self.multiply_vector(v)

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
        return GF2Matrix(self.rows, other.cols, tuple(res))

    def transpose(self) -> GF2Matrix:
        if self.rows == 0:
            return GF2Matrix(0, 0, ())
        res = tuple(tuple(self.data[r][c] for r in range(self.rows)) for c in range(self.cols))
        return GF2Matrix(self.cols, self.rows, res)

    def solve(self, rhs: Sequence[int]) -> Optional[list[int]]:
        return Gf2CocycleClassifier.solve_coboundary(self, rhs)


@dataclass
class Gf2ScheduleReceipt:
    schedule_status: GF2ScheduleStatus
    boundary_valid: bool
    exact_solution_found: bool
    coboundary_solution: Optional[list[int]]
    face_syndrome: list[int]
    notes: str
    authority_effect: str = "None"


class Gf2CocycleClassifier:
    @staticmethod
    def verify_boundary(d0: GF2Matrix, d1: GF2Matrix) -> bool:
        if d0.rows != d1.cols:
            return False
        # Check d1 * d0 == 0 mod 2
        for col_idx in range(d0.cols):
            col_v = [d0.data[r][col_idx] for r in range(d0.rows)]
            product = d1.multiply_vector(col_v)
            if any(x != 0 for x in product):
                return False
        return True

    @staticmethod
    def solve_coboundary(d0: GF2Matrix, omega: Sequence[int]) -> Optional[list[int]]:
        """Solve d0 * x = omega mod 2 via augmented Gaussian elimination."""
        if len(omega) != d0.rows:
            return None
        aug_data = [list(d0.data[r]) + [omega[r] % 2] for r in range(d0.rows)]
        aug = GF2Matrix.from_data(aug_data)
        reduced, pivots, _ = aug.row_reduce()
        # Check for inconsistency: row with 0s and last col 1
        for row in reduced.data:
            if all(row[c] == 0 for c in range(d0.cols)) and row[d0.cols] == 1:
                return None
        # Back-substitute
        sol = [0] * d0.cols
        for r, col in enumerate(pivots):
            if col < d0.cols:
                sol[col] = reduced.data[r][d0.cols]
        return sol

    @classmethod
    def classify(
        cls, d0: GF2Matrix, d1: GF2Matrix, omega: Sequence[int]
    ) -> Gf2ScheduleReceipt:
        if not cls.verify_boundary(d0, d1):
            raise ValueError("Boundary condition d1 * d0 == 0 mod 2 broken or invalid complex shape")
        if len(omega) != d0.rows or len(omega) != d1.cols:
            raise ValueError(f"Omega length {len(omega)} incompatible with complex edges {d0.rows}")
        syndrome = d1.multiply_vector(omega)
        if any(s != 0 for s in syndrome):
            return Gf2ScheduleReceipt(
                schedule_status=GF2ScheduleStatus.OpenObstruction,
                boundary_valid=True,
                exact_solution_found=False,
                coboundary_solution=None,
                face_syndrome=syndrome,
                notes="open parity obstruction: non-zero face syndrome",
            )
        sol = cls.solve_coboundary(d0, omega)
        if sol is not None:
            return Gf2ScheduleReceipt(
                schedule_status=GF2ScheduleStatus.Exact,
                boundary_valid=True,
                exact_solution_found=True,
                coboundary_solution=sol,
                face_syndrome=syndrome,
                notes="exact coboundary solution found",
            )
        return Gf2ScheduleReceipt(
            schedule_status=GF2ScheduleStatus.ClosedResidual,
            boundary_valid=True,
            exact_solution_found=False,
            coboundary_solution=None,
            face_syndrome=syndrome,
            notes="closed residual parity: d1 omega = 0 but not in image d0",
        )
