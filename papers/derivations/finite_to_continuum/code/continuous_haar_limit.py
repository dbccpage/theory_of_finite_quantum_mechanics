"""
Inductive direct limit of finite cyclic character sums to continuous Haar measure.

AuthorityEffect: None.

Demonstrates in this discrete setting the recovery of continuous character orthogonality
and Haar measure on S^1 from inductive colimits of finite cyclic presentations:
  1. Finite cyclic groups G_n = < x | x^{2^n} = 1 > with dyadic inclusions
     i_n: G_n -> G_{n+1} mapping m |-> 2m.
  2. For fixed continuous character frequencies k, j in Z, the normalized finite sum
     S_n(k, j) = (1 / 2^n) sum_{m=0}^{2^n-1} chi_{k-j}^{(n)}(m) stabilizes in finite
     levels to the Kronecker delta delta_{k, j} as soon as 2^n > |k - j|.
  3. Trigonometric polynomials P(x) = sum_k c_k exp(2 pi i k x) with exact rational
     coefficients recover their continuous Haar integral c_0 exactly on finite dyadic grids.
  4. Lipschitz continuous observables admit certified rational interval Cauchy sequences
     (I_n)_{n=0}^infty with width(I_n) <= 2L / 2^n contracting to a ContinuumEnclosure.

All calculations strictly adhere to the Zero-Float Law and Claim Hygiene Rule.
"""

from __future__ import annotations

import json
import sys
from dataclasses import dataclass
from fractions import Fraction
from hashlib import sha256
from types import MappingProxyType
from typing import Any, Dict, List, Mapping, Sequence, Tuple

if hasattr(sys, "set_int_max_str_digits"):
    sys.set_int_max_str_digits(100000)

from coda_inductive_presentation import (
    ContinuumEnclosure,
    constructive_cauchy_completion,
)
from interval_calculus import (
    RationalInterval,
    _validate_exact_int,
    _validate_exact_rational,
)


@dataclass(frozen=True)
class HaarLimitCharacterPair:
    """Pair of continuous character frequencies (k, j) in Z x Z on S^1."""

    k: int
    j: int
    delta_freq: int
    stabilization_level: int

    def __init__(self, k: int, j: int) -> None:
        k_val = _validate_exact_int(k, "frequency k")
        j_val = _validate_exact_int(j, "frequency j")
        delta = k_val - j_val
        if delta == 0:
            stab = 0
        else:
            stab = abs(delta).bit_length()
        object.__setattr__(self, "k", k_val)
        object.__setattr__(self, "j", j_val)
        object.__setattr__(self, "delta_freq", delta)
        object.__setattr__(self, "stabilization_level", stab)

    @property
    def exact_haar_integral(self) -> Fraction:
        """Exact continuous Haar integral \\int_{S^1} \\chi_k(x) \\chi_j^*(x) d\\mu(x) = \\delta_{k, j}."""
        return Fraction(1) if self.delta_freq == 0 else Fraction(0)

    def discrete_sum_at_level(self, level: int) -> Fraction:
        """Evaluate normalized discrete character sum S_n(k, j) in exact rational arithmetic.

        S_n(k, j) = (1 / 2^n) sum_{m=0}^{2^n-1} exp(2 pi i (k - j) m / 2^n).
        By finite group character orthogonality, this is 1 if (k - j) = 0 mod 2^n, else 0.
        """
        lvl = _validate_exact_int(level, "presentation level")
        if lvl < 0:
            raise ValueError(f"Level must be non-negative, got {lvl}")
        ord_val = 1 << lvl
        if self.delta_freq % ord_val == 0:
            return Fraction(1)
        return Fraction(0)

    def evaluate_limit_sequence(self, max_level: int) -> List[Fraction]:
        """Compute the sequence of normalized sums S_0, S_1, ..., S_{max_level}."""
        max_lvl = _validate_exact_int(max_level, "max_level")
        if max_lvl < 0:
            raise ValueError("max_level must be nonnegative")
        return [self.discrete_sum_at_level(lvl) for lvl in range(max_lvl + 1)]

    def is_stabilized_at(self, level: int) -> bool:
        """Check whether the discrete sum at this level has reached the continuous limit."""
        return self.discrete_sum_at_level(level) == self.exact_haar_integral



@dataclass(frozen=True)
class TrigPolynomial:
    """Trigonometric polynomial P(x) = sum_{k} c_k exp(2 pi i k x) with exact rational coefficients.

    Represented as a mapping from integer frequency k to exact Fraction c_k.
    """

    coefficients: Mapping[int, Fraction]

    def __init__(self, coeffs: Dict[int, Any]) -> None:
        clean: Dict[int, Fraction] = {}
        for k, v in coeffs.items():
            k_int = _validate_exact_int(k, "frequency")
            v_frac = _validate_exact_rational(v, f"coefficient c_{k}")
            if v_frac != 0:
                clean[k_int] = v_frac
        object.__setattr__(self, "coefficients", MappingProxyType(clean))

    @property
    def exact_haar_integral(self) -> Fraction:
        """Exact continuous Haar integral \\int_{S^1} P(x) d\\mu(x) = c_0."""
        return self.coefficients.get(0, Fraction(0))

    @property
    def max_frequency(self) -> int:
        """Maximum absolute non-zero frequency in the polynomial."""
        if not self.coefficients:
            return 0
        return max(abs(k) for k in self.coefficients.keys())

    @property
    def stabilization_level(self) -> int:
        """Minimum dyadic level n_0 such that 2^{n_0} > max |k| for all non-zero frequencies."""
        max_f = self.max_frequency
        if max_f == 0:
            return 0
        return max_f.bit_length()

    def discrete_riemann_sum(self, level: int) -> Fraction:
        """Evaluate discrete Riemann sum R_n(P) = (1 / 2^n) sum_{m=0}^{2^n-1} P(m / 2^n).

        Using linearity of finite character sums:
          R_n(P) = sum_k c_k * S_n(k, 0).
        """
        lvl = _validate_exact_int(level, "presentation level")
        if lvl < 0:
            raise ValueError("presentation level must be nonnegative")
        ord_val = 1 << lvl
        total = Fraction(0)
        for k, c_k in self.coefficients.items():
            if k % ord_val == 0:
                total += c_k
        return total

    def verify_haar_recovery(self, max_level: int) -> Dict[str, Any]:
        """Verify that R_n(P) stabilizes to the exact continuous Haar integral."""
        max_level = _validate_exact_int(max_level, "max_level")
        if max_level < 0:
            raise ValueError("max_level must be nonnegative")
        stab = self.stabilization_level
        seq = [self.discrete_riemann_sum(lvl) for lvl in range(max_level + 1)]
        is_exact_from_stab = max_level >= stab and all(
            seq[lvl] == self.exact_haar_integral
            for lvl in range(stab, max_level + 1)
        )
        return {
            "max_frequency": self.max_frequency,
            "stabilization_level": stab,
            "exact_haar_integral": str(self.exact_haar_integral),
            "sequence": [str(val) for val in seq],
            "stabilized_levels_tested": max(0, max_level - stab + 1),
            "recovers_exact_haar": is_exact_from_stab,
        }



@dataclass(frozen=True)
class LipschitzContinuumEnclosure:
    """Enclosure of continuous Haar integral for Lipschitz functions via dyadic Riemann sums.

    For f: S^1 -> R with Lipschitz constant L in Q_{>0}:
      |R_n(f) - \\int f d\\mu| <= L / 2^n.
    At level n, I_n = [R_n - L / 2^n, R_n + L / 2^n] with width 2L / 2^n.
    """

    lipschitz_constant: Fraction
    levels: int
    intervals: Tuple[RationalInterval, ...]

    def __init__(
        self,
        lipschitz_constant: Any,
        riemann_sums: Sequence[Any],
    ) -> None:
        L = _validate_exact_rational(lipschitz_constant, "lipschitz_constant")
        if L <= 0:
            raise ValueError(f"Lipschitz constant must be strictly positive, got {L}")

        intervals_list: List[RationalInterval] = []
        for n, r_val in enumerate(riemann_sums):
            r_frac = _validate_exact_rational(r_val, f"riemann_sum at level {n}")
            radius = L / (1 << n)
            intervals_list.append(RationalInterval(r_frac - radius, r_frac + radius))

        object.__setattr__(self, "lipschitz_constant", L)
        object.__setattr__(self, "levels", len(intervals_list))
        object.__setattr__(self, "intervals", tuple(intervals_list))

    def to_continuum_enclosure(self, name: str) -> ContinuumEnclosure:
        """Construct a validated ContinuumEnclosure in CODA-Q."""
        return constructive_cauchy_completion(
            name=name,
            generator=lambda n: self.intervals[n],
            steps=self.levels,
        )



def _contains_float(obj: Any) -> bool:
    """Recursively verify that no floating-point types exist in data structures."""
    if isinstance(obj, float) or (
        getattr(obj, "dtype", None) is not None and "float" in str(obj.dtype).lower()
    ):
        return True
    if isinstance(obj, dict):
        return any(_contains_float(k) or _contains_float(v) for k, v in obj.items())
    if isinstance(obj, (list, tuple, set)):
        return any(_contains_float(item) for item in obj)
    return False


def generate_continuous_haar_limit_receipt() -> Dict[str, Any]:
    """Generate stamped receipt verifying the direct limit of finite character sums.

    AuthorityEffect: None.
    Demonstrates in this toy setting that inductive colimits of finite cyclic presentations
    recover continuous Haar measure orthogonality without float leakage.
    """
    test_pairs = [
        (0, 0),
        (1, 0),
        (2, 0),
        (3, 1),
        (4, 4),
        (5, 1),
        (7, 3),
        (-2, 2),
    ]

    character_ortho_receipts: List[Dict[str, Any]] = []
    for k, j in test_pairs:
        pair = HaarLimitCharacterPair(k, j)
        seq = pair.evaluate_limit_sequence(max_level=5)
        character_ortho_receipts.append({
            "k": pair.k,
            "j": pair.j,
            "delta_frequency": pair.delta_freq,
            "stabilization_level": pair.stabilization_level,
            "exact_haar_integral": str(pair.exact_haar_integral),
            "sequence_levels_0_to_5": [str(val) for val in seq],
            "stabilized_at_final_level": pair.is_stabilized_at(5),
            "authority_effect": "None",
        })

    poly_1 = TrigPolynomial({
        0: Fraction(3),
        1: Fraction(2),
        -1: Fraction(2),
        2: Fraction(1),
    })
    poly_receipt_1 = poly_1.verify_haar_recovery(max_level=5)

    poly_2 = TrigPolynomial({
        0: Fraction(5, 2),
        3: Fraction(-7, 3),
        -5: Fraction(1, 4),
    })
    poly_receipt_2 = poly_2.verify_haar_recovery(max_level=6)

    test_sums = [
        Fraction(1, 2) + Fraction(1, 2 * (1 << n)) if n > 0 else Fraction(1)
        for n in range(6)
    ]
    lipschitz_enc = LipschitzContinuumEnclosure(
        lipschitz_constant=Fraction(1),
        riemann_sums=test_sums,
    )
    continuum_enc = lipschitz_enc.to_continuum_enclosure("haar_test_observable")

    receipt_body: Dict[str, Any] = {
        "schema": "omega.coda.continuous_haar_limit.v1",
        "authority_effect": "None",
        "cyclic_inductive_colimit": {
            "description": "Dyadic direct limit Z[1/2]/Z, dense in S^1; S^1 is its metric completion",
            "completion_constructed_by_this_receipt": False,
            "base_inclusions": "i_n(m) = 2m mod 2^{n+1}",
            "tested_levels": 6,
        },
        "character_orthogonality_direct_limits": character_ortho_receipts,
        "trig_polynomial_haar_recovery": {
            "poly_1": poly_receipt_1,
            "poly_2": poly_receipt_2,
        },
        "lipschitz_cauchy_contraction": {
            "scope": "conditional on caller sums arising from one periodic Lipschitz function",
            "sample_provenance_verified": False,
            "name": continuum_enc.name,
            "steps": continuum_enc.steps,
            "final_width": str(continuum_enc.final_width),
            "is_cauchy_contractive": continuum_enc.is_cauchy_contractive(),
            "final_interval": [
                str(continuum_enc.final_interval.lo),
                str(continuum_enc.final_interval.hi),
            ],
        },
    }

    receipt_body["zero_float_law_verified"] = not _contains_float(receipt_body)

    raw_json = json.dumps(receipt_body, sort_keys=True, indent=2)
    digest = sha256(raw_json.encode("utf-8")).hexdigest()
    receipt_body["evidence_sha256"] = digest

    return receipt_body


__all__ = [
    "HaarLimitCharacterPair",
    "TrigPolynomial",
    "LipschitzContinuumEnclosure",
    "generate_continuous_haar_limit_receipt",
]
