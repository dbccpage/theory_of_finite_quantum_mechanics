from __future__ import annotations

from fractions import Fraction
from typing import Any, Sequence, Union


class Cyclotomic16:
    """Exact field representation for Q(e^{i*pi/8}), the 16th cyclotomic field.

    The minimal polynomial of zeta_16 = e^{i*pi/8} is x^8 + 1 = 0 over Q.
    Therefore, the field is represented as an 8-dimensional vector space over Q
    with basis {1, zeta, zeta^2, ..., zeta^7}.
    All coefficients are represented as exact fractions.
    """

    def __init__(self, coeffs: Sequence[Union[Fraction, int, str, None]] | None = None):
        if coeffs is None:
            self.coeffs = [Fraction(0)] * 8
        else:
            c_list = list(coeffs)
            if len(c_list) < 8:
                c_list += [0] * (8 - len(c_list))
            self.coeffs = []
            for x in c_list[:8]:
                if isinstance(x, float):
                    raise TypeError("Exact algebra cyclotomic coefficients cannot be binary floats.")
                self.coeffs.append(Fraction(x) if x is not None else Fraction(0))

    def __add__(self, other: Cyclotomic16 | int | Fraction) -> Cyclotomic16:
        if isinstance(other, (int, Fraction)):
            other = Cyclotomic16([other] + [0] * 7)
        return Cyclotomic16([a + b for a, b in zip(self.coeffs, other.coeffs)])

    def __radd__(self, other: int | Fraction) -> Cyclotomic16:
        return self.__add__(other)

    def __sub__(self, other: Cyclotomic16 | int | Fraction) -> Cyclotomic16:
        if isinstance(other, (int, Fraction)):
            other = Cyclotomic16([other] + [0] * 7)
        return Cyclotomic16([a - b for a, b in zip(self.coeffs, other.coeffs)])

    def __rsub__(self, other: int | Fraction) -> Cyclotomic16:
        return Cyclotomic16([other] + [0] * 7).__sub__(self)

    def __mul__(self, other: Cyclotomic16 | int | Fraction) -> Cyclotomic16:
        if isinstance(other, (int, Fraction)):
            return Cyclotomic16([c * other for c in self.coeffs])

        prod = [Fraction(0)] * 15
        for j in range(8):
            for k in range(8):
                prod[j + k] += self.coeffs[j] * other.coeffs[k]

        reduced = [Fraction(0)] * 8
        for r in range(8):
            reduced[r] = prod[r] - prod[r + 8] if r + 8 < 15 else prod[r]

        return Cyclotomic16(reduced)

    def __rmul__(self, other: int | Fraction) -> Cyclotomic16:
        return self.__mul__(other)

    def __truediv__(self, other: int | Fraction) -> Cyclotomic16:
        div = Fraction(other)
        return Cyclotomic16([c / div for c in self.coeffs])

    def __eq__(self, other: Any) -> bool:
        if not isinstance(other, Cyclotomic16):
            if isinstance(other, (int, Fraction)):
                other = Cyclotomic16([other] + [0] * 7)
            else:
                return False
        return self.coeffs == other.coeffs

    def __repr__(self) -> str:
        basis_strs = []
        for i, val in enumerate(self.coeffs):
            if val != 0:
                if i == 0:
                    basis_strs.append(f"{val}")
                elif i == 1:
                    basis_strs.append(f"{val}*zeta")
                else:
                    basis_strs.append(f"{val}*zeta^{i}")
        if not basis_strs:
            return "0"
        return " + ".join(basis_strs).replace(" + -", " - ")



ONE = Cyclotomic16([1, 0, 0, 0, 0, 0, 0, 0])
ZERO = Cyclotomic16([0, 0, 0, 0, 0, 0, 0, 0])
ZETA = Cyclotomic16([0, 1, 0, 0, 0, 0, 0, 0])
I_IMAG = Cyclotomic16([0, 0, 0, 0, 1, 0, 0, 0])
SQRT2 = Cyclotomic16([0, 0, 1, 0, 0, 0, -1, 0])
ONE_OVER_SQRT2 = Cyclotomic16([0, 0, Fraction(1, 2), 0, 0, 0, Fraction(-1, 2), 0])


class ExactMatrix:
    """Exact Matrix class over Cyclotomic16 entries."""

    def __init__(self, data: Sequence[Sequence[Cyclotomic16]]):
        self.data = [[x for x in row] for row in data]
        self.rows = len(self.data)
        self.cols = len(self.data[0]) if self.rows > 0 else 0

    def __getitem__(self, index: int) -> list[Cyclotomic16]:
        return self.data[index]

    def __mul__(self, other: ExactMatrix) -> ExactMatrix:
        if self.cols != other.rows:
            raise ValueError(
                f"Dimension mismatch for exact matrix multiplication: {self.cols} != {other.rows}"
            )
        prod = []
        for r in range(self.rows):
            row_prod = []
            for c in range(other.cols):
                val = ZERO
                for k in range(self.cols):
                    val = val + self.data[r][k] * other.data[k][c]
                row_prod.append(val)
            prod.append(row_prod)
        return ExactMatrix(prod)

    def __eq__(self, other: Any) -> bool:
        if not isinstance(other, ExactMatrix):
            return False
        if self.rows != other.rows or self.cols != other.cols:
            return False
        for r in range(self.rows):
            for c in range(self.cols):
                if self.data[r][c] != other.data[r][c]:
                    return False
        return True

    def __repr__(self) -> str:
        return f"ExactMatrix({self.data})"



def verify_ising_braid_relation() -> bool:
    """Verify the exact Yang-Baxter braid relation B_1 * B_2 * B_1 = B_2 * B_1 * B_2.

    B_1 = R = [[e^{-i*pi/8}, 0], [0, e^{3i*pi/8}]]
    B_2 = F * R * F, where F = 1/sqrt(2) * [[1, 1], [1, -1]]
    """
    r11 = Cyclotomic16([0, 0, 0, 0, 0, 0, 0, -1])
    r22 = Cyclotomic16([0, 0, 0, 1, 0, 0, 0, 0])

    R = ExactMatrix([
        [r11, ZERO],
        [ZERO, r22]
    ])

    f_val = ONE_OVER_SQRT2
    minus_f_val = ZERO - ONE_OVER_SQRT2

    F = ExactMatrix([
        [f_val, f_val],
        [f_val, minus_f_val]
    ])

    B1 = R
    B2 = F * R * F

    LHS = B1 * B2 * B1
    RHS = B2 * B1 * B2

    return LHS == RHS


def verify_fusion_associativity() -> bool:
    """Verify fusion associativity: F^2 = I."""
    f_val = ONE_OVER_SQRT2
    minus_f_val = ZERO - ONE_OVER_SQRT2

    F = ExactMatrix([
        [f_val, f_val],
        [f_val, minus_f_val]
    ])

    I = ExactMatrix([
        [ONE, ZERO],
        [ZERO, ONE]
    ])

    return F * F == I


def verify_ising_sigma_hexagon_specialization() -> bool:
    """Verify the exact Hexagon equations relating braiding and fusion.

    R_d * F_de * R_e = sum_g F_dg * R_g * F_ge
    where:
      R^(sigma sigma)_1 = e^{-i*pi/8} = zeta^{15} = -zeta^7
      R^(sigma sigma)_psi = e^{3i*pi/8} = zeta^3
      R^(1 sigma)_sigma = 1
      R^(psi sigma)_sigma = -i = -zeta^4
    """
    r_ss = [
        Cyclotomic16([0, 0, 0, 0, 0, 0, 0, -1]),
        Cyclotomic16([0, 0, 0, 1, 0, 0, 0, 0])
    ]

    r_gs = [
        ONE,
        Cyclotomic16([0, 0, 0, 0, -1, 0, 0, 0])
    ]

    f_val = ONE_OVER_SQRT2
    minus_f_val = ZERO - ONE_OVER_SQRT2

    F = [
        [f_val, f_val],
        [f_val, minus_f_val]
    ]

    for d in (0, 1):
        for e in (0, 1):
            LHS = r_ss[d] * F[d][e] * r_ss[e]
            RHS = ZERO
            for g in (0, 1):
                RHS = RHS + F[d][g] * r_gs[g] * F[g][e]
            if LHS != RHS:
                return False

    return True

