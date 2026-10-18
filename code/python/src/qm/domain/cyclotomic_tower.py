"""Cyclotomic Carrier Tower, Directed Inclusion, and Born Weight Characterization.

Step 1-8 of the 50-step formal derivation from cyclotomic carriers to finite QM.
AuthorityEffect: None.
Citation: sealed-derivation-v1 (3100c4e)
"""

from __future__ import annotations

import math
from fractions import Fraction
from typing import Any, Dict, List, Optional, Tuple, Union


def cyclotomic_polynomial_coeffs(n: int) -> List[int]:
    """Compute coefficients of the n-th cyclotomic polynomial Phi_n(x) [lowest to highest degree]."""
    if type(n) is not int or n < 1:
        raise ValueError("conductor must be a positive integer")
    if n == 1:
        return [-1, 1]
    elif n == 2:
        return [1, 1]
    elif n == 3:
        return [1, 1, 1]
    elif n == 4:
        return [1, 0, 1]
    elif n == 5:
        return [1, 1, 1, 1, 1]
    elif n == 6:
        return [1, -1, 1]
    elif n == 8:
        return [1, 0, 0, 0, 1]
    elif n == 12:
        return [1, 0, -1, 0, 1]
    elif n == 24:
        return [1, 0, 0, 0, -1, 0, 0, 0, 1]
    else:
        poly = [0] * (n + 1)
        poly[0] = -1
        poly[n] = 1
        divisors = [d for d in range(1, n) if n % d == 0]
        curr = poly
        for d in divisors:
            sub = cyclotomic_polynomial_coeffs(d)
            curr = _poly_div(curr, sub)
        return curr


def _poly_div(p1: List[int], p2: List[int]) -> List[int]:
    """Exact polynomial division p1 / p2 with integer coefficients."""
    n1 = len(p1) - 1
    n2 = len(p2) - 1
    if not p1 or not p2 or p2[-1] == 0:
        raise ValueError("nonempty polynomials and a nonzero leading divisor are required")
    quot = [0] * (n1 - n2 + 1)
    rem = [Fraction(c) for c in p1]
    for i in range(n1 - n2, -1, -1):
        coeff = rem[i + n2] / p2[-1]
        if coeff.denominator != 1:
            raise ValueError("polynomial quotient is not integral")
        quot[i] = coeff.numerator
        for j in range(n2 + 1):
            rem[i + j] -= coeff * p2[j]
    if any(rem):
        raise ValueError("polynomial division has a nonzero remainder")
    return quot or [0]


class CyclotomicElement:
    """Exact element of cyclotomic field Q(zeta_n) represented in power basis mod Phi_n(x)."""

    def __init__(self, conductor: int, coeffs: Union[List[Fraction], List[int], Dict[int, Fraction]]):
        if type(conductor) is not int or conductor < 1:
            raise ValueError("Conductor must be a positive integer")
        self.conductor = conductor
        phi = cyclotomic_polynomial_coeffs(conductor)
        deg = len(phi) - 1

        c_list = [Fraction(0)] * deg
        if isinstance(coeffs, dict):
            for k, v in coeffs.items():
                if type(k) is not int or k < 0:
                    raise ValueError("Basis degree must be a nonnegative integer")
                if k < deg:
                    c_list[k] = Fraction(v)
                else:
                    raise ValueError(f"Degree {k} exceeds basis dimension {deg}")
        else:
            for i, c in enumerate(coeffs):
                if i < deg:
                    c_list[i] = c if isinstance(c, Fraction) else Fraction(c)
                elif c != 0:
                    raise ValueError(f"Nonzero coefficient at degree {i} >= {deg}")
        self.coeffs = tuple(c_list)
        self.deg = deg
        self._canonical_cache: Optional[CyclotomicElement] = None

    @classmethod
    def rational(cls, q: Union[int, Fraction], conductor: int = 1) -> CyclotomicElement:
        phi = cyclotomic_polynomial_coeffs(conductor)
        deg = len(phi) - 1
        c = [Fraction(0)] * deg
        c[0] = Fraction(q)
        return cls(conductor, c)

    @classmethod
    def zeta(cls, conductor: int) -> CyclotomicElement:
        phi = cyclotomic_polynomial_coeffs(conductor)
        deg = len(phi) - 1
        c = [Fraction(0)] * deg
        if deg > 1:
            c[1] = Fraction(1)
        else:
            if conductor == 1:
                c[0] = Fraction(1)
            elif conductor == 2:
                c[0] = Fraction(-1)
        return cls(conductor, c)

    def is_zero(self) -> bool:
        return all(c == 0 for c in self.coeffs)

    def is_one(self) -> bool:
        """Check if element is identity 1 in Q(zeta_n)."""
        return self.is_rational() and (self.coeffs[0] == 1 if self.coeffs else False)

    def __eq__(self, other: Any) -> bool:
        if isinstance(other, (int, Fraction)):
            other = CyclotomicElement.rational(other, self.conductor)
        if not isinstance(other, CyclotomicElement):
            return False
        if self.conductor == other.conductor:
            return self.coeffs == other.coeffs
        lcm_cond = (self.conductor * other.conductor) // math.gcd(self.conductor, other.conductor)
        s_lift = self.lift_to(lcm_cond)
        o_lift = other.lift_to(lcm_cond)
        return s_lift.coeffs == o_lift.coeffs

    def lift_to(self, target_conductor: int) -> CyclotomicElement:
        """Lift element from Q(zeta_m) to Q(zeta_n) where m | n."""
        m = self.conductor
        n = target_conductor
        if m == n:
            return self
        assert n % m == 0, f"Cannot lift from conductor {m} to non-multiple {n}"
        step = n // m

        target_phi = cyclotomic_polynomial_coeffs(n)
        target_deg = len(target_phi) - 1

        res = [Fraction(0)] * target_deg
        for k, c in enumerate(self.coeffs):
            if c == 0:
                continue
            power = (k * step) % n
            term = _reduce_power(power, n, target_phi)
            for i in range(target_deg):
                res[i] += c * term[i]
        return CyclotomicElement(n, res)

    def conjugate(self) -> CyclotomicElement:
        """Complex conjugation automorphism sigma_{-1}: zeta_n -> zeta_n^(-1)."""
        n = self.conductor
        phi = cyclotomic_polynomial_coeffs(n)
        deg = len(phi) - 1
        res = [Fraction(0)] * deg
        for k, c in enumerate(self.coeffs):
            if c == 0:
                continue
            inv_power = (n - (k % n)) % n
            term = _reduce_power(inv_power, n, phi)
            for i in range(deg):
                res[i] += c * term[i]
        return CyclotomicElement(n, res)

    def is_real(self) -> bool:
        """Check if element is invariant under complex conjugation (lands in Q(zeta_n)^+)."""
        return self == self.conjugate()

    def born_weight(self) -> CyclotomicElement:
        """Compute Born weight w = psi * conjugate(psi). Ensured under the declared assumptions to land in Q(zeta_n)^+."""
        w = self * self.conjugate()
        assert w.is_real(), "Born weight must be invariant under complex conjugation"
        return w

    def __add__(self, other: Union[CyclotomicElement, int, Fraction]) -> CyclotomicElement:
        if isinstance(other, (int, Fraction)):
            other = CyclotomicElement.rational(other, self.conductor)
        if self.conductor != other.conductor:
            lcm_cond = (self.conductor * other.conductor) // math.gcd(self.conductor, other.conductor)
            return self.lift_to(lcm_cond) + other.lift_to(lcm_cond)
        new_c = [self.coeffs[i] + other.coeffs[i] for i in range(self.deg)]
        return CyclotomicElement(self.conductor, new_c)

    def __sub__(self, other: Union[CyclotomicElement, int, Fraction]) -> CyclotomicElement:
        if isinstance(other, (int, Fraction)):
            other = CyclotomicElement.rational(other, self.conductor)
        if self.conductor != other.conductor:
            lcm_cond = (self.conductor * other.conductor) // math.gcd(self.conductor, other.conductor)
            return self.lift_to(lcm_cond) - other.lift_to(lcm_cond)
        new_c = [self.coeffs[i] - other.coeffs[i] for i in range(self.deg)]
        return CyclotomicElement(self.conductor, new_c)

    def __mul__(self, other: Union[CyclotomicElement, int, Fraction]) -> CyclotomicElement:
        if isinstance(other, (int, Fraction)):
            return CyclotomicElement(self.conductor, [c * Fraction(other) for c in self.coeffs])
        if self.conductor != other.conductor:
            lcm_cond = (self.conductor * other.conductor) // math.gcd(self.conductor, other.conductor)
            return self.lift_to(lcm_cond) * other.lift_to(lcm_cond)

        n = self.conductor
        phi = cyclotomic_polynomial_coeffs(n)
        deg = len(phi) - 1

        raw = [Fraction(0)] * (2 * deg)
        for i in range(deg):
            if self.coeffs[i] == 0:
                continue
            for j in range(deg):
                if other.coeffs[j] == 0:
                    continue
                raw[i + j] += self.coeffs[i] * other.coeffs[j]

        res = [Fraction(0)] * deg
        for k in range(len(raw)):
            if raw[k] == 0:
                continue
            term = _reduce_power(k, n, phi)
            for i in range(deg):
                res[i] += raw[k] * term[i]
        return CyclotomicElement(n, res)

    def inverse(self) -> CyclotomicElement:
        """Exact multiplicative inverse in Q(zeta_n) via regular representation linear system."""
        if self.is_zero():
            raise ZeroDivisionError("Cannot invert zero CyclotomicElement")
        if all(c == 0 for c in self.coeffs[1:]):
            return CyclotomicElement.rational(Fraction(1) / self.coeffs[0], self.conductor)
        deg = self.deg
        matrix = [[Fraction(0)] * deg for _ in range(deg)]
        for j in range(deg):
            basis_c = [Fraction(0)] * deg
            basis_c[j] = Fraction(1)
            col_elem = self * CyclotomicElement(self.conductor, basis_c)
            for i in range(deg):
                matrix[i][j] = col_elem.coeffs[i]

        aug = [row[:] + [Fraction(1 if i == 0 else 0)] for i, row in enumerate(matrix)]
        for col in range(deg):
            pivot_row = -1
            for r in range(col, deg):
                if aug[r][col] != 0:
                    pivot_row = r
                    break
            if pivot_row == -1:
                raise ZeroDivisionError("Element is non-invertible")
            if pivot_row != col:
                aug[col], aug[pivot_row] = aug[pivot_row], aug[col]

            pivot = aug[col][col]
            for c in range(col, deg + 1):
                aug[col][c] /= pivot

            for r in range(deg):
                if r != col and aug[r][col] != 0:
                    factor = aug[r][col]
                    for c in range(col, deg + 1):
                        aug[r][c] -= factor * aug[col][c]

        inv_c = [aug[r][deg] for r in range(deg)]
        return CyclotomicElement(self.conductor, inv_c)

    def __truediv__(self, other: Union[CyclotomicElement, int, Fraction]) -> CyclotomicElement:
        if isinstance(other, (int, Fraction)):
            if other == 0:
                raise ZeroDivisionError("Division by zero")
            return self * (Fraction(1) / Fraction(other))
        return self * other.inverse()

    def __rtruediv__(self, other: Union[int, Fraction]) -> CyclotomicElement:
        return CyclotomicElement.rational(other, self.conductor) / self

    def __radd__(self, other: Union[int, Fraction]) -> CyclotomicElement:
        return self + other

    def __rsub__(self, other: Union[int, Fraction]) -> CyclotomicElement:
        return CyclotomicElement.rational(other, self.conductor) - self

    def __rmul__(self, other: Union[int, Fraction]) -> CyclotomicElement:
        return self * other


    def __pow__(self, exp: int) -> CyclotomicElement:
        if not isinstance(exp, int):
            return NotImplemented
        if exp == 0:
            return CyclotomicElement.rational(1, self.conductor)
        if exp < 0:
            return (self.inverse()) ** (-exp)
        res = CyclotomicElement.rational(1, self.conductor)
        base = self
        e = exp
        while e > 0:
            if e % 2 == 1:
                res = res * base
            base = base * base
            e //= 2
        return res


    def is_rational(self) -> bool:
        """Check if element lies in prime field Q (all higher degree coefficients zero)."""
        return all(c == 0 for c in self.coeffs[1:])

    def as_rational(self) -> Optional[Fraction]:
        """Return exact rational value in Q if element lies in Q, else None."""
        if self.is_rational():
            return self.coeffs[0] if self.coeffs else Fraction(0)
        return None

    def canonical(self) -> CyclotomicElement:
        """Reduce to the least divisor label accepted by the implemented linear solve."""
        if hasattr(self, "_canonical_cache") and self._canonical_cache is not None:
            return self._canonical_cache

        if self.is_rational():
            res = CyclotomicElement.rational(self.coeffs[0] if self.coeffs else Fraction(0), 1)
            self._canonical_cache = res
            return res

        n = self.conductor
        if n == 1:
            self._canonical_cache = self
            return self

        divisors = [d for d in range(1, n) if n % d == 0]
        phi_n = cyclotomic_polynomial_coeffs(n)
        deg_n = len(phi_n) - 1

        for d in divisors:
            if d == 1:
                continue
            phi_d = cyclotomic_polynomial_coeffs(d)
            deg_d = len(phi_d) - 1
            step = n // d

            cols = []
            for j in range(deg_d):
                p = (j * step) % n
                cols.append(_reduce_power(p, n, phi_n))

            aug = [[cols[j][i] for j in range(deg_d)] + [self.coeffs[i]] for i in range(deg_n)]
            row = 0
            for col in range(deg_d):
                pivot_row = -1
                for r in range(row, deg_n):
                    if aug[r][col] != 0:
                        pivot_row = r
                        break
                if pivot_row == -1:
                    continue
                aug[row], aug[pivot_row] = aug[pivot_row], aug[row]
                pivot = aug[row][col]
                for c in range(col, deg_d + 1):
                    aug[row][c] /= pivot
                for r in range(deg_n):
                    if r != row and aug[r][col] != 0:
                        factor = aug[r][col]
                        for c in range(col, deg_d + 1):
                            aug[r][c] -= factor * aug[row][c]
                row += 1

            consistent = True
            for r in range(row, deg_n):
                if aug[r][deg_d] != 0:
                    consistent = False
                    break

            if consistent:
                sol = [aug[r][deg_d] for r in range(deg_d)]
                candidate = CyclotomicElement(d, sol)
                if candidate.lift_to(n).coeffs == self.coeffs:
                    res = candidate.canonical()
                    self._canonical_cache = res
                    return res

        self._canonical_cache = self
        return self

    def __hash__(self) -> int:
        canon = self.canonical()
        if canon.is_rational():
            q = canon.coeffs[0] if canon.coeffs else Fraction(0)
            return hash(q)
        return hash((canon.conductor, canon.coeffs))

    def __repr__(self) -> str:
        parts = []
        for i, c in enumerate(self.coeffs):
            if c != 0:
                if i == 0:
                    parts.append(f"{c}")
                elif i == 1:
                    parts.append(f"{c}*z{self.conductor}" if c != 1 else f"z{self.conductor}")
                else:
                    parts.append(f"{c}*z{self.conductor}^{i}" if c != 1 else f"z{self.conductor}^{i}")
        if not parts:
            return "0"
        return " + ".join(parts).replace("+ -", "- ")


_REDUCE_POWER_CACHE: Dict[Tuple[int, int], List[Fraction]] = {}


def _reduce_power(power: int, conductor: int, phi: List[int]) -> List[Fraction]:
    """Reduce x^power modulo monic cyclotomic polynomial phi."""
    key = (power, conductor)
    if key in _REDUCE_POWER_CACHE:
        return _REDUCE_POWER_CACHE[key]
    deg = len(phi) - 1
    if power < deg:
        res = [Fraction(0)] * deg
        res[power] = Fraction(1)
        _REDUCE_POWER_CACHE[key] = res
        return res

    rem = [Fraction(0)] * (power + 1)
    rem[power] = Fraction(1)
    for i in range(power, deg - 1, -1):
        if rem[i] != 0:
            c = rem[i]
            for j in range(deg + 1):
                rem[i - deg + j] -= c * phi[j]
    res = [rem[i] for i in range(deg)]
    _REDUCE_POWER_CACHE[key] = res
    return res


class CyclotomicTower:
    """Manages directed cyclotomic tower Q(zeta_m) <= Q(zeta_n) and maximal abelian carrier Q^ab."""

    @staticmethod
    def is_directed_subfield(m: int, n: int) -> bool:
        """Declared divisibility diagram, a sufficient field inclusion, not an iff."""
        if type(m) is not int or type(n) is not int or min(m, n) < 1:
            raise ValueError("conductors must be positive integers")
        return n % m == 0

    @staticmethod
    def minimal_conductor(conductors: List[int]) -> int:
        """Least multiple of supplied labels, not minimality of their actual fields."""
        curr = 1
        for c in conductors:
            if type(c) is not int or c < 1:
                raise ValueError("conductors must be positive integers")
            curr = (curr * c) // math.gcd(curr, c)
        return curr

    @staticmethod
    def verify_all_targets(targets: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Verify that all target conductors divide the target LCM conductor n*."""
        conductors = [t["conductor"] for t in targets]
        n_star = CyclotomicTower.minimal_conductor(conductors)
        containment = {}
        for t in targets:
            c = t["conductor"]
            is_in = CyclotomicTower.is_directed_subfield(c, n_star)
            containment[t["target_id"]] = {
                "name": t["name"],
                "conductor": c,
                "embeds_in_target_lcm": is_in,
                "target_lcm_conductor": n_star,
                "embeds_in_universal": is_in,
                "universal_conductor": n_star,
            }
        return {
            "n_star": n_star,
            "claim_type": "DECLARED_LABEL_DIVISIBILITY_ONLY",
            "minimality_proved": False,
            "target_lcm_field": f"Q(zeta_{n_star})",
            "universal_field": f"Q(zeta_{n_star})",
            "all_embedded": all(v["embeds_in_target_lcm"] for v in containment.values()),
            "details": containment
        }

    @staticmethod
    def achievable_born_weights(conductor: int, dim: int) -> Dict[str, Any]:
        """Declare a norm-image set; no density, convexity, or existence proof."""
        return {
            "conductor": conductor,
            "dimension": dim,
            "field": f"Q(zeta_{conductor})",
            "real_subfield": f"Q(zeta_{conductor})^+",
            "claim_type": "DECLARED_NORM_IMAGE_NOT_CHARACTERIZATION",
            "achievable_set_type": "Declared norm-image subset of probability simplex",
            "description": (
                f"The set of Born weights B_{dim}(Q(zeta_{conductor})) is {{ (|psi_1|^2, ..., |psi_{dim}|^2) : "
                f"psi in Q(zeta_{conductor})^{dim}, sum |psi_j|^2 = 1 }}. "
                f"The formula is a declaration, not a computation of every achievable weight."
            ),
            "density": None,
            "convexity": None
        }

__all__ = ['CyclotomicElement', 'CyclotomicTower', 'cyclotomic_polynomial_coeffs']
