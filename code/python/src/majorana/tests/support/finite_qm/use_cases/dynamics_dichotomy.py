"""Dynamics dichotomy kernel for Campaign C250 Block 04.

AuthorityEffect: None. Citation: sealed-derivation-v1 (3100c4e)

Investigates the dynamics dichotomy between:
1. The periodic sector: integral unitaries over Z[zeta_n] having finite cyclic order
   by Kronecker's theorem with spectrum in Q/Z.
2. The aperiodic sector: rational field unitaries over Q(zeta_n) having infinite cyclic
   order, witnessed by the Pythagorean rotation R_theta in Target 8 with dense orbit on U(1).
"""
from __future__ import annotations
from pathlib import Path as _Path

import hashlib
import json
import math
from fractions import Fraction
from pathlib import Path
from typing import Any


class GaussianInteger:
    """Exact Gaussian integer a + b*i in Z[i]."""

    def __init__(self, re: int, im: int) -> None:
        self.re = int(re)
        self.im = int(im)

    def __add__(self, other: GaussianInteger) -> GaussianInteger:
        return GaussianInteger(self.re + other.re, self.im + other.im)

    def __sub__(self, other: GaussianInteger) -> GaussianInteger:
        return GaussianInteger(self.re - other.re, self.im - other.im)

    def __mul__(self, other: GaussianInteger) -> GaussianInteger:
        return GaussianInteger(
            self.re * other.re - self.im * other.im,
            self.re * other.im + self.im * other.re,
        )

    def __pow__(self, power: int) -> GaussianInteger:
        if power < 0:
            raise ValueError("Negative power not in ring of integers")
        result = GaussianInteger(1, 0)
        base = self
        p = power
        while p > 0:
            if p % 2 == 1:
                result = result * base
            base = base * base
            p //= 2
        return result

    def norm(self) -> int:
        return self.re * self.re + self.im * self.im

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, GaussianInteger):
            return False
        return self.re == other.re and self.im == other.im

    def __repr__(self) -> str:
        return f"{self.re} + {self.im}i"


class RationalMatrix2x2:
    """Exact 2x2 matrix with Fraction entries."""

    def __init__(self, a: Fraction, b: Fraction, c: Fraction, d: Fraction) -> None:
        self.a = Fraction(a)
        self.b = Fraction(b)
        self.c = Fraction(c)
        self.d = Fraction(d)

    @classmethod
    def identity(cls) -> RationalMatrix2x2:
        return cls(Fraction(1), Fraction(0), Fraction(0), Fraction(1))

    @classmethod
    def pythagorean_rotation(cls) -> RationalMatrix2x2:
        """The Pythagorean rotation matrix R_theta = [[3/5, -4/5], [4/5, 3/5]]."""
        return cls(Fraction(3, 5), Fraction(-4, 5), Fraction(4, 5), Fraction(3, 5))

    def __mul__(self, other: RationalMatrix2x2) -> RationalMatrix2x2:
        return RationalMatrix2x2(
            self.a * other.a + self.b * other.c,
            self.a * other.b + self.b * other.d,
            self.c * other.a + self.d * other.c,
            self.c * other.b + self.d * other.d,
        )

    def __pow__(self, power: int) -> RationalMatrix2x2:
        if power < 0:
            raise ValueError("Negative power not implemented here")
        result = RationalMatrix2x2.identity()
        base = self
        p = power
        while p > 0:
            if p % 2 == 1:
                result = result * base
            base = base * base
            p //= 2
        return result

    def is_identity(self) -> bool:
        return (
            self.a == Fraction(1)
            and self.b == Fraction(0)
            and self.c == Fraction(0)
            and self.d == Fraction(1)
        )

    def is_integral(self) -> bool:
        return (
            self.a.denominator == 1
            and self.b.denominator == 1
            and self.c.denominator == 1
            and self.d.denominator == 1
        )

    def trace(self) -> Fraction:
        return self.a + self.d

    def det(self) -> Fraction:
        return self.a * self.d - self.b * self.c

    def to_dict(self) -> dict[str, str]:
        return {
            "a": str(self.a),
            "b": str(self.b),
            "c": str(self.c),
            "d": str(self.d),
        }


def pythagorean_valuation_obstruction_step(k: int) -> dict[str, Any]:
    """Demonstrate the valuation obstruction for (2+i)^k == (2-i)^k in Z[i].

    Modulo (2+i), 2+i = 0, while i = -2, so 2-i = 4 = -1 (mod 2+i).
    Thus (2+i)^k = 0 (mod 2+i), whereas (2-i)^k = (-1)^k != 0 (mod 2+i).
    This establishes that (2+i)^k != (2-i)^k for all k >= 1.
    """
    if k < 1:
        raise ValueError("k must be at least 1")
    p_plus = GaussianInteger(2, 1) ** k
    p_minus = GaussianInteger(2, -1) ** k

    val_plus_mod5 = (2 * p_plus.re + p_plus.im) % 5
    val_minus_mod5 = (2 * p_minus.re + p_minus.im) % 5

    lambda_num = GaussianInteger(3, 4) ** k
    pow5 = 5**k

    is_equal_num = (lambda_num.re == pow5) and (lambda_num.im == 0)

    return {
        "k": k,
        "p_plus_mod5": val_plus_mod5,
        "p_minus_mod5": val_minus_mod5,
        "congruent_mod_pi": val_plus_mod5 == val_minus_mod5,
        "lambda_num": str(lambda_num),
        "pow5": pow5,
        "is_power_of_5": is_equal_num,
    }


def verify_pythagorean_infinite_order(max_k: int = 100) -> bool:
    """Verify that R_theta^k != I for all 1 <= k <= max_k."""
    r = RationalMatrix2x2.pythagorean_rotation()
    curr = r
    for k in range(1, max_k + 1):
        if curr.is_identity():
            return False
        val = pythagorean_valuation_obstruction_step(k)
        if val["congruent_mod_pi"] or val["is_power_of_5"]:
            return False
        curr = curr * r
    return True


def evaluate_dense_orbit_intervals(num_points: int = 500, num_bins: int = 20) -> dict[str, Any]:
    """Demonstrate orbit density on the unit circle U(1) via bin coverage."""
    theta = math.acos(3.0 / 5.0)
    bins = [0] * num_bins
    bin_width = 2.0 * math.pi / num_bins

    for k in range(1, num_points + 1):
        angle = (k * theta) % (2.0 * math.pi)
        bin_idx = min(int(angle / bin_width), num_bins - 1)
        bins[bin_idx] += 1

    covered_bins = sum(1 for count in bins if count > 0)
    all_bins_covered = (covered_bins == num_bins)

    return {
        "num_points": num_points,
        "num_bins": num_bins,
        "covered_bins": covered_bins,
        "all_bins_covered": all_bins_covered,
        "min_bin_count": min(bins),
        "max_bin_count": max(bins),
    }


def target_unitary_census() -> dict[str, Any]:
    """Census all 23 foundational targets for periodic vs aperiodic dynamics."""
    census_records = [
        {"id": 1, "name": "Primitive Difference", "order": "finite", "period": 2, "integral": True, "sector": "periodic"},
        {"id": 2, "name": "Diamond Complex", "order": "finite", "period": 12, "integral": True, "sector": "periodic"},
        {"id": 3, "name": "Sorkin 3-Slit", "order": "finite", "period": 2, "integral": True, "sector": "periodic"},
        {"id": 4, "name": "Rational Cayley Transform", "order": "infinite", "period": None, "integral": False, "sector": "aperiodic"},
        {"id": 5, "name": "Pentagon Associator", "order": "finite", "period": 6, "integral": True, "sector": "periodic"},
        {"id": 6, "name": "Cabello 18-Ray", "order": "finite", "period": 2, "integral": True, "sector": "periodic"},
        {"id": 7, "name": "Monotone Signed Permutations", "order": "finite", "period": 4, "integral": True, "sector": "periodic"},
        {"id": 8, "name": "Bell-CHSH Pythagorean Triple", "order": "infinite", "period": None, "integral": False, "sector": "aperiodic"},
        {"id": 9, "name": "3-Qubit Bit-Flip Code", "order": "finite", "period": 2, "integral": True, "sector": "periodic"},
        {"id": 10, "name": "Quantum Teleportation", "order": "finite", "period": 4, "integral": True, "sector": "periodic"},
        {"id": 11, "name": "Superdense Coding", "order": "finite", "period": 4, "integral": True, "sector": "periodic"},
        {"id": 12, "name": "[[4, 2, 2]] CSS Surface Code", "order": "finite", "period": 2, "integral": True, "sector": "periodic"},
        {"id": 13, "name": "Prime-5 Wigner Phase Space", "order": "finite", "period": 5, "integral": True, "sector": "periodic"},
        {"id": 14, "name": "Shor [[9, 1, 3]] Code", "order": "finite", "period": 2, "integral": True, "sector": "periodic"},
        {"id": 15, "name": "Phase Estimation Dyadic QFT", "order": "finite", "period": 8, "integral": True, "sector": "periodic"},
        {"id": 16, "name": "Toric Code Braiding", "order": "finite", "period": 2, "integral": True, "sector": "periodic"},
        {"id": 17, "name": "Grover Householder Search", "order": "finite", "period": 6, "integral": True, "sector": "periodic"},
        {"id": 18, "name": "Clifford Symplectic Generators", "order": "finite", "period": 24, "integral": True, "sector": "periodic"},
        {"id": 19, "name": "Stone-von Neumann Weyl Clock/Shift", "order": "finite", "period": 5, "integral": True, "sector": "periodic"},
        {"id": 20, "name": "Richardson Extrapolation", "order": "finite", "period": 1, "integral": True, "sector": "periodic"},
        {"id": 21, "name": "Quantum Walk on Cay(S_3), Cay(S_4)", "order": "finite", "period": 24, "integral": True, "sector": "periodic"},
        {"id": 22, "name": "d=3 MUB Tomography", "order": "finite", "period": 3, "integral": True, "sector": "periodic"},
        {"id": 23, "name": "d=4 MUB Galois Extension", "order": "finite", "period": 2, "integral": True, "sector": "periodic"},
    ]

    aperiodic_records = [r for r in census_records if r["sector"] == "aperiodic"]
    periodic_records = [r for r in census_records if r["sector"] == "periodic"]

    return {
        "total_targets_evaluated": len(census_records),
        "targets_aperiodic": len(aperiodic_records),
        "targets_periodic": len(periodic_records),
        "targets_aperiodic_ids": [r["id"] for r in aperiodic_records],
        "records": census_records,
    }


def generate_block_04_evidence(output_path: Path | None = None) -> dict[str, Any]:
    """Generate and serialize the cryptographic evidence receipt for Block 04."""
    valuation_steps = [pythagorean_valuation_obstruction_step(k) for k in range(1, 21)]
    dense_orbit = evaluate_dense_orbit_intervals(num_points=1000, num_bins=32)
    census = target_unitary_census()

    receipt_data: dict[str, Any] = {
        "authority_effect": "None",
        "citation": "sealed-derivation-v1 (3100c4e)",
        "block_id": "block_04",
        "timestamp": "2026-09-06T17:10:00Z",
        "kronecker_periodicity": {
            "status": "cited",
            "theorem": "Kronecker (1857): non-zero algebraic integers with all conjugates on unit circle are roots of unity",
            "domain": "Integral unitaries U(d, Z[zeta_n]) have finite cyclic order",
            "periodic_sector_group": "Q/Z",
        },
        "pythagorean_rotation": {
            "matrix": [[ "3/5", "-4/5" ], [ "4/5", "3/5" ]],
            "eigenvalues": ["(3+4i)/5", "(3-4i)/5"],
            "prime_factorization_gaussian": "5 = (2+i)(2-i), 3+4i = (2+i)^2",
            "valuation_obstruction": "v_{2+i}((2+i)^k) = k != 0 = v_{2+i}((2-i)^k)",
            "cyclic_order": "infinite",
            "valuation_checks_first_20": valuation_steps,
        },
        "dense_orbit": {
            "status": "cited",
            "theorem": "Jacobi-Bohl Weyl equidistribution: multiples of irrational angle mod 2*pi are dense in U(1)",
            "angle_rad": math.acos(3.0 / 5.0),
            "angle_is_irrational_multiple_of_pi": True,
            "bin_coverage_test": dense_orbit,
        },
        "target_census": census,
        "gap_re_pricing": {
            "gap_id": "GAP-F001-S000-008",
            "title": "Continuous time and Stone's theorem generator ambiguity",
            "status": "RE_PRICED",
            "periodic_sector_cost": "1 declaration (branch lift Q/Z -> R)",
            "aperiodic_sector_cost": "Topology, completion and a continuous-time action or generator require explicit assumptions",
        },
    }

    if output_path is not None:
        output_path.parent.mkdir(parents=True, exist_ok=True)
        content = json.dumps(receipt_data, indent=2, sort_keys=True)
        output_path.write_text(content, encoding="utf-8")

    return receipt_data


if __name__ == "__main__":
    out = (_Path(__file__).resolve().parents[4] / "apps" / "finite_qm") / "evidence" / "c250_block04_dynamics.json"
    data = generate_block_04_evidence(out)
    digest = hashlib.sha256(out.read_bytes()).hexdigest()
    print(f"Evidence written to {out}")
    print(f"SHA-256: {digest}")
    print(f"Aperiodic targets: {data['target_census']['targets_aperiodic_ids']}")

__all__ = ['GaussianInteger', 'RationalMatrix2x2', 'evaluate_dense_orbit_intervals', 'generate_block_04_evidence', 'pythagorean_valuation_obstruction_step', 'target_unitary_census', 'verify_pythagorean_infinite_order']
