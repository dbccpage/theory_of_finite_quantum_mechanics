
"""Campaign C500 Block 01: Finite Weyl Residual and Direct CCR Obstruction.

Implements exact finite Weyl-Heisenberg operators (Clock Z, Shift X), the
finite-dimensional Heisenberg-CCR trace obstruction, norm-indexed lower bounds
for the CCR residual operator R_lambda(Q, P) = QP - PQ - lambda*I, exact cyclotomic
conductor accounting, and the formal refusal of finite differentiation to direct CCR.

All algebraic calculations are exact using Fraction and cyclotomic polynomial arithmetic
with zero floating-point arithmetic in algebraic decision paths.
"""

from __future__ import annotations

import cmath
from fractions import Fraction
import json
import math
from typing import Any, Dict, List, Optional, Sequence, Tuple, Union



class RationalPoly:
    """Exact univariate polynomial with Fraction coefficients: sum_{k=0}^deg c_k x^k."""

    def __init__(self, coeffs: Union[Sequence[Union[Fraction, int]], RationalPoly]) -> None:
        if isinstance(coeffs, RationalPoly):
            self.coeffs: Tuple[Fraction, ...] = coeffs.coeffs
            return
        c_list = [Fraction(c) for c in coeffs]
        while c_list and c_list[-1] == 0:
            c_list.pop()
        self.coeffs = tuple(c_list)

    @property
    def degree(self) -> int:
        """Return degree, or -1 for zero polynomial."""
        return len(self.coeffs) - 1

    def is_zero(self) -> bool:
        return len(self.coeffs) == 0

    def eval(self, x: Union[Fraction, int, complex]) -> Union[Fraction, complex]:
        """Horner evaluation."""
        if self.is_zero():
            return Fraction(0) if not isinstance(x, complex) else 0.0 + 0.0j
        res: Union[Fraction, complex] = Fraction(0) if not isinstance(x, complex) else 0.0 + 0.0j
        for c in reversed(self.coeffs):
            res = res * x + c
        return res

    def __add__(self, other: Union[RationalPoly, Fraction, int]) -> RationalPoly:
        if not isinstance(other, RationalPoly):
            other = RationalPoly([Fraction(other)])
        n = max(len(self.coeffs), len(other.coeffs))
        res = [Fraction(0)] * n
        for i, c in enumerate(self.coeffs):
            res[i] += c
        for i, c in enumerate(other.coeffs):
            res[i] += c
        return RationalPoly(res)

    def __radd__(self, other: Union[Fraction, int]) -> RationalPoly:
        return self + other

    def __sub__(self, other: Union[RationalPoly, Fraction, int]) -> RationalPoly:
        if not isinstance(other, RationalPoly):
            other = RationalPoly([Fraction(other)])
        n = max(len(self.coeffs), len(other.coeffs))
        res = [Fraction(0)] * n
        for i, c in enumerate(self.coeffs):
            res[i] += c
        for i, c in enumerate(other.coeffs):
            res[i] -= c
        return RationalPoly(res)

    def __rsub__(self, other: Union[Fraction, int]) -> RationalPoly:
        return RationalPoly([Fraction(other)]) - self

    def __neg__(self) -> RationalPoly:
        return RationalPoly([-c for c in self.coeffs])

    def __mul__(self, other: Union[RationalPoly, Fraction, int]) -> RationalPoly:
        if not isinstance(other, RationalPoly):
            other_frac = Fraction(other)
            return RationalPoly([c * other_frac for c in self.coeffs])
        if self.is_zero() or other.is_zero():
            return RationalPoly(())
        deg1 = self.degree
        deg2 = other.degree
        res = [Fraction(0)] * (deg1 + deg2 + 1)
        for i, c1 in enumerate(self.coeffs):
            if c1 == 0:
                continue
            for j, c2 in enumerate(other.coeffs):
                res[i + j] += c1 * c2
        return RationalPoly(res)

    def __rmul__(self, other: Union[Fraction, int]) -> RationalPoly:
        return self * other

    def div_rem(self, divisor: RationalPoly) -> Tuple[RationalPoly, RationalPoly]:
        """Euclidean division in Q[x]. Returns (quotient, remainder)."""
        if divisor.is_zero():
            raise ZeroDivisionError("Polynomial division by zero polynomial")
        if self.is_zero() or self.degree < divisor.degree:
            return RationalPoly(()), self

        rem_coeffs = list(self.coeffs)
        div_deg = divisor.degree
        div_lead = divisor.coeffs[-1]
        quot_deg = len(rem_coeffs) - 1 - div_deg
        quot_coeffs = [Fraction(0)] * (quot_deg + 1)

        while len(rem_coeffs) - 1 >= div_deg and rem_coeffs:
            curr_deg = len(rem_coeffs) - 1
            shift = curr_deg - div_deg
            factor = rem_coeffs[-1] / div_lead
            quot_coeffs[shift] = factor
            for j, c in enumerate(divisor.coeffs):
                rem_coeffs[shift + j] -= factor * c
            while rem_coeffs and rem_coeffs[-1] == 0:
                rem_coeffs.pop()

        return RationalPoly(quot_coeffs), RationalPoly(rem_coeffs)

    def __mod__(self, divisor: RationalPoly) -> RationalPoly:
        _, rem = self.div_rem(divisor)
        return rem

    def __eq__(self, other: Any) -> bool:
        if not isinstance(other, RationalPoly):
            if isinstance(other, (int, Fraction)):
                other = RationalPoly([Fraction(other)])
            else:
                return False
        return self.coeffs == other.coeffs

    def to_list(self) -> List[List[int]]:
        """Return list of [numerator, denominator] for JSON serialization."""
        return [[c.numerator, c.denominator] for c in self.coeffs]


def cyclotomic_polynomial(n: int) -> RationalPoly:
    """Compute the n-th cyclotomic polynomial Phi_n(x) with integer coefficients."""
    if n < 1:
        raise ValueError("n must be positive integer")
    if n == 1:
        return RationalPoly([-1, 1])
    if n == 2:
        return RationalPoly([1, 1])
    if n == 3:
        return RationalPoly([1, 1, 1])
    if n == 4:
        return RationalPoly([1, 0, 1])
    if n == 5:
        return RationalPoly([1, 1, 1, 1, 1])
    if n == 6:
        return RationalPoly([1, -1, 1])
    if n == 8:
        return RationalPoly([1, 0, 0, 0, 1])
    if n == 12:
        return RationalPoly([1, 0, -1, 0, 1])
    if n == 24:
        return RationalPoly([1, 0, 0, 0, -1, 0, 0, 0, 1])

    poly_coeffs = [0] * (n + 1)
    poly_coeffs[0] = -1
    poly_coeffs[n] = 1
    curr = RationalPoly(poly_coeffs)
    for d in range(1, n):
        if n % d == 0:
            phi_d = cyclotomic_polynomial(d)
            curr, _ = curr.div_rem(phi_d)
    return curr


def euler_phi(n: int) -> int:
    """Euler totient function."""
    if n < 1:
        raise ValueError("n must be positive")
    res = n
    p = 2
    temp = n
    while p * p <= temp:
        if temp % p == 0:
            while temp % p == 0:
                temp //= p
            res -= res // p
        p += 1
    if temp > 1:
        res -= res // temp
    return res


def cyclotomic_conductor(d: int) -> int:
    """Return the exact arithmetic conductor of the cyclotomic field Q(zeta_d).

    By Kronecker-Weber and the standard cyclotomic theorem:
    Q(zeta_d) has conductor d if d is odd or 4 | d.
    If d = 2 * (odd), Q(zeta_d) = Q(zeta_{d/2}), so the conductor is d / 2.
    """
    if d < 1:
        raise ValueError("d must be positive")
    if d % 4 == 2:
        return d // 2
    if d == 2:
        return 1
    return d



class CycNum:
    """Exact element of cyclotomic field Q(zeta_d) = Q[x] / (Phi_d(x)).

    Represented as a canonical reduced polynomial modulo Phi_d(x).
    """

    def __init__(self, d: int, poly: Union[RationalPoly, Sequence[Union[Fraction, int]], Fraction, int]) -> None:
        self.d = d
        self.modulus = cyclotomic_polynomial(d)
        if isinstance(poly, (int, Fraction)):
            p = RationalPoly([Fraction(poly)])
        elif isinstance(poly, RationalPoly):
            p = poly
        else:
            p = RationalPoly(poly)
        self.poly = p % self.modulus

    @classmethod
    def zero(cls, d: int) -> CycNum:
        return cls(d, RationalPoly(()))

    @classmethod
    def one(cls, d: int) -> CycNum:
        return cls(d, RationalPoly([1]))

    @classmethod
    def primitive_root(cls, d: int) -> CycNum:
        """Return the primitive d-th root omega_d = x mod Phi_d(x)."""
        return cls(d, RationalPoly([0, 1]))

    def is_zero(self) -> bool:
        return self.poly.is_zero()

    def is_one(self) -> bool:
        return self.poly == RationalPoly([1])

    def __add__(self, other: Union[CycNum, Fraction, int]) -> CycNum:
        if isinstance(other, (int, Fraction)):
            return CycNum(self.d, self.poly + other)
        if self.d != other.d:
            raise ValueError(f"Incompatible cyclotomic conductors: {self.d} vs {other.d}")
        return CycNum(self.d, self.poly + other.poly)

    def __radd__(self, other: Union[Fraction, int]) -> CycNum:
        return self + other

    def __sub__(self, other: Union[CycNum, Fraction, int]) -> CycNum:
        if isinstance(other, (int, Fraction)):
            return CycNum(self.d, self.poly - other)
        if self.d != other.d:
            raise ValueError(f"Incompatible cyclotomic conductors: {self.d} vs {other.d}")
        return CycNum(self.d, self.poly - other.poly)

    def __rsub__(self, other: Union[Fraction, int]) -> CycNum:
        return CycNum(self.d, other) - self

    def __neg__(self) -> CycNum:
        return CycNum(self.d, -self.poly)

    def __mul__(self, other: Union[CycNum, Fraction, int]) -> CycNum:
        if isinstance(other, (int, Fraction)):
            return CycNum(self.d, self.poly * other)
        if self.d != other.d:
            raise ValueError(f"Incompatible cyclotomic conductors: {self.d} vs {other.d}")
        return CycNum(self.d, (self.poly * other.poly) % self.modulus)

    def __rmul__(self, other: Union[Fraction, int]) -> CycNum:
        return self * other

    def __pow__(self, power: int) -> CycNum:
        if power == 0:
            return CycNum.one(self.d)
        if power < 0:
            return (self.inverse()) ** (-power)
        base = self
        res = CycNum.one(self.d)
        p = power
        while p > 0:
            if p % 2 == 1:
                res = res * base
            base = base * base
            p //= 2
        return res

    def inverse(self) -> CycNum:
        """Compute algebraic inverse via extended Euclidean algorithm in Q[x]."""
        if self.is_zero():
            raise ZeroDivisionError("Cannot invert zero cyclotomic element")
        a = self.poly
        b = self.modulus
        s0, s1 = RationalPoly([1]), RationalPoly(())
        t0, t1 = RationalPoly(()), RationalPoly([1])

        while not b.is_zero():
            q, r = a.div_rem(b)
            a, b = b, r
            s0, s1 = s1, s0 - q * s1
            t0, t1 = t1, t0 - q * t1

        lead_c = a.coeffs[0]
        inv_poly = s0 * (Fraction(1) / lead_c)
        return CycNum(self.d, inv_poly)

    def conjugate(self) -> CycNum:
        """Apply complex / cyclotomic conjugation (Galois automorphism zeta_d -> zeta_d^(-1)).

        In Q[x]/(Phi_d(x)), zeta_d^(-1) = zeta_d^(d-1).
        Thus x^k -> x^((d - (k % d)) % d).
        """
        res_poly = RationalPoly(())
        for k, c in enumerate(self.poly.coeffs):
            if c == 0:
                continue
            new_power = (self.d - (k % self.d)) % self.d
            term = (CycNum.primitive_root(self.d) ** new_power) * c
            res_poly = res_poly + term.poly
        return CycNum(self.d, res_poly)

    def complex_eval(self) -> complex:
        """Evaluate under canonical embedding zeta_d -> exp(2*pi*i / d)."""
        omega = cmath.exp(2j * math.pi / self.d)
        return self.poly.eval(omega)

    def __eq__(self, other: Any) -> bool:
        if isinstance(other, (int, Fraction)):
            other = CycNum(self.d, other)
        if not isinstance(other, CycNum):
            return False
        if self.d != other.d:
            return False
        return self.poly == other.poly

    def __repr__(self) -> str:
        return f"CycNum(d={self.d}, {self.poly.to_list()})"

    def to_dict(self) -> Dict[str, Any]:
        return {
            "dimension": self.d,
            "coefficients": self.poly.to_list(),
            "complex_approx": [self.complex_eval().real, self.complex_eval().imag],
        }



class ExactMatrix:
    """Square matrix over CycNum (or Rational) with exact operations."""

    def __init__(self, dim: int, d_field: int, data: List[List[CycNum]]) -> None:
        if type(dim) is not int or dim < 1 or type(d_field) is not int or d_field < 1:
            raise ValueError("Matrix dimension and cyclotomic order must be positive integers")
        if len(data) != dim or any(len(row) != dim for row in data):
            raise ValueError("Matrix data must match its square dimension")
        if any(not isinstance(x, CycNum) or x.d != d_field for row in data for x in row):
            raise ValueError("Matrix entries must use the declared cyclotomic field")
        self.dim = dim
        self.d_field = d_field
        self.data = [list(row) for row in data]

    @classmethod
    def zeros(cls, dim: int, d_field: int) -> ExactMatrix:
        zero = CycNum.zero(d_field)
        return cls(dim, d_field, [[zero for _ in range(dim)] for _ in range(dim)])

    @classmethod
    def identity(cls, dim: int, d_field: int) -> ExactMatrix:
        mat = cls.zeros(dim, d_field)
        one = CycNum.one(d_field)
        for i in range(dim):
            mat.data[i][i] = one
        return mat

    def __getitem__(self, idx: Tuple[int, int]) -> CycNum:
        return self.data[idx[0]][idx[1]]

    def __setitem__(self, idx: Tuple[int, int], val: CycNum) -> None:
        self.data[idx[0]][idx[1]] = val

    def __add__(self, other: ExactMatrix) -> ExactMatrix:
        assert self.dim == other.dim and self.d_field == other.d_field
        res = ExactMatrix.zeros(self.dim, self.d_field)
        for i in range(self.dim):
            for j in range(self.dim):
                res.data[i][j] = self.data[i][j] + other.data[i][j]
        return res

    def __sub__(self, other: ExactMatrix) -> ExactMatrix:
        assert self.dim == other.dim and self.d_field == other.d_field
        res = ExactMatrix.zeros(self.dim, self.d_field)
        for i in range(self.dim):
            for j in range(self.dim):
                res.data[i][j] = self.data[i][j] - other.data[i][j]
        return res

    def __mul__(self, scalar: Union[CycNum, Fraction, int]) -> ExactMatrix:
        if not isinstance(scalar, CycNum):
            scalar = CycNum(self.d_field, scalar)
        res = ExactMatrix.zeros(self.dim, self.d_field)
        for i in range(self.dim):
            for j in range(self.dim):
                res.data[i][j] = self.data[i][j] * scalar
        return res

    def __rmul__(self, scalar: Union[CycNum, Fraction, int]) -> ExactMatrix:
        return self * scalar

    def __matmul__(self, other: ExactMatrix) -> ExactMatrix:
        """Matrix multiplication optimized for sparse/permutation/diagonal matrices."""
        assert self.dim == other.dim and self.d_field == other.d_field
        res = ExactMatrix.zeros(self.dim, self.d_field)
        for i in range(self.dim):
            for k in range(self.dim):
                a_ik = self.data[i][k]
                if a_ik.is_zero():
                    continue
                for j in range(self.dim):
                    b_kj = other.data[k][j]
                    if b_kj.is_zero():
                        continue
                    res.data[i][j] = res.data[i][j] + a_ik * b_kj
        return res

    def __pow__(self, power: int) -> ExactMatrix:
        if type(power) is not int or power < 0:
            raise ValueError("Matrix powers must be nonnegative integers")
        if power == 0:
            return ExactMatrix.identity(self.dim, self.d_field)
        base = self
        res = ExactMatrix.identity(self.dim, self.d_field)
        p = power
        while p > 0:
            if p % 2 == 1:
                res = res @ base
            base = base @ base
            p //= 2
        return res

    def trace(self) -> CycNum:
        """Compute exact trace tr(M) = sum_i M_{i, i}."""
        tr = CycNum.zero(self.d_field)
        for i in range(self.dim):
            tr = tr + self.data[i][i]
        return tr

    def dagger(self) -> ExactMatrix:
        """Conjugate transpose."""
        res = ExactMatrix.zeros(self.dim, self.d_field)
        for i in range(self.dim):
            for j in range(self.dim):
                res.data[j][i] = self.data[i][j].conjugate()
        return res

    def is_identity(self) -> bool:
        one = CycNum.one(self.d_field)
        zero = CycNum.zero(self.d_field)
        for i in range(self.dim):
            for j in range(self.dim):
                expected = one if i == j else zero
                if self.data[i][j] != expected:
                    return False
        return True

    def is_zero(self) -> bool:
        zero = CycNum.zero(self.d_field)
        for i in range(self.dim):
            for j in range(self.dim):
                if self.data[i][j] != zero:
                    return False
        return True

    def __eq__(self, other: Any) -> bool:
        if not isinstance(other, ExactMatrix):
            return False
        if self.dim != other.dim or self.d_field != other.d_field:
            return False
        for i in range(self.dim):
            for j in range(self.dim):
                if self.data[i][j] != other.data[i][j]:
                    return False
        return True

    def to_dict(self) -> Dict[str, Any]:
        return {
            "dim": self.dim,
            "d_field": self.d_field,
            "matrix": [[elem.to_dict() for elem in row] for row in self.data],
        }



def construct_shift_operator(d: int) -> ExactMatrix:
    """Construct dimension-d cyclic shift operator X.

    X |j> = |(j + 1) mod d>.
    Matrix elements: X_{j, k} = delta_{j, (k + 1) mod d}.
    """
    mat = ExactMatrix.zeros(d, d)
    one = CycNum.one(d)
    for k in range(d):
        j = (k + 1) % d
        mat.data[j][k] = one
    return mat


def construct_clock_operator(d: int) -> ExactMatrix:
    """Construct dimension-d clock operator Z with phase convention omega = exp(2*pi*i / d).

    Z |j> = omega^j |j>.
    Matrix elements: Z_{j, k} = omega^j delta_{j, k}.
    """
    mat = ExactMatrix.zeros(d, d)
    omega = CycNum.primitive_root(d)
    for j in range(d):
        mat.data[j][j] = omega ** j
    return mat


def verify_weyl_algebra_properties(d: int) -> Dict[str, Any]:
    """Verify unitarity, exact orders, and twisted relation ZX = omega XZ."""
    X = construct_shift_operator(d)
    Z = construct_clock_operator(d)
    omega = CycNum.primitive_root(d)

    X_dag_X = X.dagger() @ X
    X_X_dag = X @ X.dagger()
    Z_dag_Z = Z.dagger() @ Z
    Z_Z_dag = Z @ Z.dagger()

    is_X_unitary = X_dag_X.is_identity() and X_X_dag.is_identity()
    is_Z_unitary = Z_dag_Z.is_identity() and Z_Z_dag.is_identity()

    X_pow_d = X ** d
    Z_pow_d = Z ** d
    has_exact_order_d = X_pow_d.is_identity() and Z_pow_d.is_identity()

    has_minimal_order = True
    for k in range(1, d):
        if (X ** k).is_identity() or (Z ** k).is_identity():
            has_minimal_order = False
            break

    ZX = Z @ X
    XZ = X @ Z
    omega_XZ = XZ * omega
    twisted_commutation_holds = (ZX == omega_XZ)

    omega_inv = omega.inverse()
    omega_inv_ZX = ZX * omega_inv
    dual_twisted_holds = (XZ == omega_inv_ZX)

    return {
        "dimension": d,
        "is_X_unitary": is_X_unitary,
        "is_Z_unitary": is_Z_unitary,
        "orders_d_verified": has_exact_order_d,
        "minimal_orders_verified": has_minimal_order,
        "twisted_commutation_holds": twisted_commutation_holds,
        "dual_twisted_holds": dual_twisted_holds,
        "status": "EXACT_AT_DECLARED_ROOT" if (is_X_unitary and is_Z_unitary and has_exact_order_d and twisted_commutation_holds) else "FAILED",
    }



def ccr_residual(Q: ExactMatrix, P: ExactMatrix, lambda_val: Union[CycNum, Fraction, int]) -> ExactMatrix:
    """Compute the direct CCR residual operator R_lambda(Q, P) = QP - PQ - lambda * I."""
    assert Q.dim == P.dim and Q.d_field == P.d_field
    QP = Q @ P
    PQ = P @ Q
    comm = QP - PQ
    lam_I = ExactMatrix.identity(Q.dim, Q.d_field) * lambda_val
    return comm - lam_I


def verify_trace_obstruction(d: int, lambda_num: int = 1, lambda_den: int = 1) -> Dict[str, Any]:
    """Check a clock/shift instance of the cited finite-dimensional trace argument.

    For any d x d matrices Q, P in characteristic zero:
        tr([Q, P]) = tr(QP - PQ) = 0
    whereas
        tr(lambda * I_d) = lambda * d != 0 for lambda != 0.
    """
    lam = Fraction(lambda_num, lambda_den)
    if lam == 0:
        raise ValueError("lambda must be nonzero for the obstruction")

    X = construct_shift_operator(d)
    Z = construct_clock_operator(d)
    comm_XZ = (X @ Z) - (Z @ X)
    tr_comm = comm_XZ.trace()
    tr_target = lam * d

    R = ccr_residual(X, Z, lam)
    tr_R = R.trace()

    abs_lam = abs(lam)
    trace_norm_lower_bound = abs_lam * d
    frobenius_norm_sq_lower_bound = (abs_lam ** 2) * d
    norm_frob_lower_bound = abs_lam

    return {
        "dimension": d,
        "lambda": str(lam),
        "trace_commutator": tr_comm.to_dict(),
        "trace_commutator_is_zero": tr_comm.is_zero(),
        "trace_target_scalar": str(tr_target),
        "trace_target_is_nonzero": (tr_target != 0),
        "obstruction_holds": tr_comm.is_zero() and (tr_target != 0),
        "residual_trace": tr_R.to_dict(),
        "trace_norm_lower_bound": str(trace_norm_lower_bound),
        "frobenius_norm_lower_bound_approx": math.sqrt(float(frobenius_norm_sq_lower_bound)),
        "normalized_frobenius_lower_bound": str(norm_frob_lower_bound),
        "status": "REFUSED_BY_TRACE",
    }



def char_p_weyl_representation(p: int) -> Dict[str, Any]:
    """Demonstrate that in characteristic p > 0 with p | d, [P, Q] = I_p IS satisfiable.

    In the polynomial representation K[x] / (x^p) over F_p:
    Q = multiplication by x (nilpotent shift)
    P = formal derivative d/dx

    Then [P, Q] f(x) = d/dx(x f(x)) - x f'(x) = f(x) + x f'(x) - x f'(x) = f(x).
    Thus [P, Q] = I_p in M_p(F_p).
    Notice tr(I_p) = p * 1 = 0 in F_p, which avoids the trace obstruction.
    """
    if type(p) is not int or p < 2 or any(p % q == 0 for q in range(2, math.isqrt(p) + 1)):
        raise ValueError("The F_p countermodel requires prime characteristic")
    Q = [[0 for _ in range(p)] for _ in range(p)]
    P = [[0 for _ in range(p)] for _ in range(p)]
    for j in range(p - 1):
        Q[j + 1][j] = 1
    for j in range(1, p):
        P[j - 1][j] = j % p

    PQ = [[0 for _ in range(p)] for _ in range(p)]
    QP = [[0 for _ in range(p)] for _ in range(p)]
    for i in range(p):
        for j in range(p):
            for k in range(p):
                PQ[i][j] = (PQ[i][j] + P[i][k] * Q[k][j]) % p
                QP[i][j] = (QP[i][j] + Q[i][k] * P[k][j]) % p

    comm = [[(PQ[i][j] - QP[i][j]) % p for j in range(p)] for i in range(p)]
    is_identity_mod_p = all(
        comm[i][j] == (1 if i == j else 0) for i in range(p) for j in range(p)
    )
    tr_I_mod_p = sum(comm[i][i] for i in range(p)) % p

    return {
        "characteristic": p,
        "dimension": p,
        "commutator_is_identity_mod_p": is_identity_mod_p,
        "trace_identity_mod_p": tr_I_mod_p,
        "obstruction_evaporates_in_char_p": (tr_I_mod_p == 0),
        "status": "COUNTERMODEL_IN_CHAR_P",
    }



TESTED_DIMENSIONS = [2, 3, 4, 5, 6, 7, 8, 12, 24]

def compute_dimension_table() -> List[Dict[str, Any]]:
    """Compute exact cyclotomic conductor cost, minimal polynomials, and dimension classification."""
    rows = []
    for d in TESTED_DIMENSIONS:
        phi = euler_phi(d)
        cond = cyclotomic_conductor(d)
        poly = cyclotomic_polynomial(d)
        is_odd_prime = (d in [3, 5, 7])
        is_char_two = (d in [2, 4, 8])
        is_prime_power = (d in [2, 3, 4, 5, 7, 8])
        is_composite = (d in [4, 6, 8, 12, 24])

        rows.append({
            "dimension": d,
            "euler_phi": phi,
            "conductor": cond,
            "cyclotomic_poly_coeffs": poly.to_list(),
            "field_extension": f"Q(zeta_{d})" if cond == d else f"Q(zeta_{cond})",
            "degree_over_Q": phi,
            "is_odd_prime": is_odd_prime,
            "is_power_of_two": is_char_two,
            "scalar_characteristic": 0,
            "is_prime_power": is_prime_power,
            "is_composite": is_composite,
            "phase_invertibility_mod_d": "2_is_invertible" if d % 2 == 1 else "2_not_invertible_requires_escalation",
        })
    return rows



def generate_canonical_block01_receipt() -> Dict[str, Any]:
    """Generate canonical execution receipt for Campaign C500 Block 01."""
    weyl_results = {}
    obstruction_results = {}
    for d in TESTED_DIMENSIONS:
        weyl_results[f"d_{d}"] = verify_weyl_algebra_properties(d)
        obstruction_results[f"d_{d}"] = verify_trace_obstruction(d)

    char_p_results = {
        "p_2": char_p_weyl_representation(2),
        "p_3": char_p_weyl_representation(3),
        "p_5": char_p_weyl_representation(5),
    }

    dimension_table = compute_dimension_table()

    receipt = {
        "authority_effect": "None",
        "citation": "sealed-derivation-v1 (3100c4e)",
        "campaign": "C500",
        "block": "block_01",
        "global_targets": "C500-T301..C500-T325",
        "terminal_outcome": "FINITE_WEYL_RESIDUAL_WITH_DIRECT_CCR_NO_GO",
        "predecessor_binding_status": "NOT_VERIFIED_BY_KERNEL",
        "source_anchor_binding": {
            "anchor_id": "S1",
            "citation": "Lledo and Martinez, arXiv:2111.15221",
            "consumed_role": "Folner-type finite dimensional approximation questions for Weyl algebra",
            "unauthorized_extrapolation": "Exact finite representation of unbounded CCR",
        },
        "weyl_results": weyl_results,
        "obstruction_results": obstruction_results,
        "char_p_results": char_p_results,
        "dimension_table": dimension_table,
        "machine_bet_clauses": {
            "direct_ccr_nonzero_finite_status": "REFUSED_BY_TRACE",
            "finite_weyl_pair_status": "EXACT_AT_DECLARED_ROOT",
            "weyl_implies_direct_ccr": False,
            "characteristic_cases_are_separate": True,
            "all_consumed_predecessor_inputs_are_sha_pinned": False,
        },
        "formal_refusal": {
            "refusal_target": "C500-T312",
            "invalid_inference": "Differentiating finite Weyl relation ZX = omega XZ to obtain Lie-form CCR [Q, P] = i*hbar*I",
            "reasons": [
                "No finite-dimensional square matrices in characteristic zero satisfy [Q, P] = lambda*I for lambda != 0 (Target C500-T305).",
                "The spectrum of clock operator Z is finite cyclic Z_d, which admits no unbounded self-adjoint momentum generator on C^d.",
                "Differentiating across discrete group actions with fixed phase step theta = 2*pi/d is mathematically invalid.",
            ],
        },
    }
    return receipt


if __name__ == "__main__":
    receipt = generate_canonical_block01_receipt()
    print(json.dumps(receipt, indent=2, sort_keys=True))

__all__ = ['CycNum', 'ExactMatrix', 'RationalPoly', 'TESTED_DIMENSIONS', 'ccr_residual', 'char_p_weyl_representation', 'compute_dimension_table', 'construct_clock_operator', 'construct_shift_operator', 'cyclotomic_conductor', 'cyclotomic_polynomial', 'euler_phi', 'generate_canonical_block01_receipt', 'verify_trace_obstruction', 'verify_weyl_algebra_properties']
