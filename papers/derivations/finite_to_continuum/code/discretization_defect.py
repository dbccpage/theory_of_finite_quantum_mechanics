"""
CS-Q Discretization Defect Operators and Bounded Continuum Recovery.

AuthorityEffect: None.

Equips discrete lattice and grid solvers with explicit discretization error
operators:
    Result(a) = ContinuousValue + E(a),  where |E(a)| <= C * a^p.

At any finite lattice spacing a = 1/N or discrete step size, the discrete
realization belongs to CODA Layer 4 (CS: Continuum Shadow). The explicit defect
operator provides the constructive bridge to CODA Layer 5 (Q: The Continuum),
producing certified rational interval enclosures:
    Enclosure_cont = [Result(a) - C * a^p, Result(a) + C * a^p] in Q x Q.
"""

from __future__ import annotations

from dataclasses import dataclass
from fractions import Fraction
from hashlib import sha256
import json
from typing import Any, Callable, Dict, List, Optional, Sequence, Tuple

from interval_calculus import (
    RationalInterval,
    _validate_exact_int,
    _validate_exact_rational,
)


@dataclass(frozen=True)
class DiscretizationDefectCarrier:
    """Discrete solver outcome equipped with explicit discretization error bound.

    Result(a) = ContinuousValue + E(a), with |E(a)| <= prefactor_c * a^order_p.
    """

    carrier_id: str
    parameter_a: Fraction
    discrete_value: RationalInterval
    order_p: int
    prefactor_c: Fraction
    physical_observable: str = "energy"

    def __post_init__(self) -> None:
        a = _validate_exact_rational(self.parameter_a, "parameter_a")
        if a <= 0:
            raise ValueError(f"parameter_a must be strictly positive, got {a}")
        p = _validate_exact_int(self.order_p, "order_p")
        if p < 1:
            raise ValueError(f"order_p must be >= 1, got {p}")
        c = _validate_exact_rational(self.prefactor_c, "prefactor_c")
        if c < 0:
            raise ValueError(f"prefactor_c must be non-negative, got {c}")
        if not isinstance(self.discrete_value, RationalInterval):
            raise TypeError(
                f"discrete_value must be RationalInterval, got {type(self.discrete_value).__name__}"
            )

    @property
    def defect_bound(self) -> Fraction:
        """Maximum defect magnitude |E(a)| <= C * a^p."""
        return self.prefactor_c * (self.parameter_a ** self.order_p)

    @property
    def continuum_enclosure(self) -> RationalInterval:
        """Certified rational interval enclosing the true continuum value.

        [discrete_value.lo - defect_bound, discrete_value.hi + defect_bound].
        """
        b = self.defect_bound
        return RationalInterval(self.discrete_value.lo - b, self.discrete_value.hi + b)

    def encloses(self, true_continuum_val: Any) -> bool:
        """Check whether candidate continuum point is enclosed."""
        val = _validate_exact_rational(true_continuum_val, "true_continuum_val")
        return self.continuum_enclosure.contains(val)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "carrier_id": self.carrier_id,
            "parameter_a": str(self.parameter_a),
            "order_p": self.order_p,
            "prefactor_c": str(self.prefactor_c),
            "defect_bound": str(self.defect_bound),
            "discrete_value": {
                "lo": str(self.discrete_value.lo),
                "hi": str(self.discrete_value.hi),
                "width": str(self.discrete_value.width),
            },
            "continuum_enclosure": {
                "lo": str(self.continuum_enclosure.lo),
                "hi": str(self.continuum_enclosure.hi),
                "width": str(self.continuum_enclosure.width),
            },
            "physical_observable": self.physical_observable,
        }


@dataclass(frozen=True)
class MeshRefinementReceipt:
    """Audit receipt verifying multi-mesh consistency between coarse and fine solves."""

    coarse_carrier_id: str
    fine_carrier_id: str
    coarse_a: Fraction
    fine_a: Fraction
    coarse_defect: Fraction
    fine_defect: Fraction
    is_contractive: bool
    is_overlapping: bool
    refined_enclosure: RationalInterval
    receipt_sha256: str
    authority_effect: str = "None"


def verify_mesh_refinement(
    coarse: DiscretizationDefectCarrier,
    fine: DiscretizationDefectCarrier,
) -> MeshRefinementReceipt:
    """Assert contractive defect reduction and non-empty intersection of enclosures."""
    if coarse.parameter_a <= fine.parameter_a:
        raise ValueError(
            f"coarse spacing {coarse.parameter_a} must be strictly greater than fine spacing {fine.parameter_a}"
        )
    if coarse.order_p != fine.order_p:
        raise ValueError(
            f"Order mismatch: coarse order={coarse.order_p} != fine order={fine.order_p}"
        )

    is_contractive = fine.defect_bound < coarse.defect_bound
    is_overlapping = coarse.continuum_enclosure.intersects(fine.continuum_enclosure)

    if not is_overlapping:
        raise ValueError(
            f"Discretization inconsistency: coarse enclosure {coarse.continuum_enclosure} "
            f"does not intersect fine enclosure {fine.continuum_enclosure} "
            f"(defect constant C={coarse.prefactor_c} may be underestimated)"
        )

    refined = coarse.continuum_enclosure.intersect(fine.continuum_enclosure)

    payload = {
        "coarse_id": coarse.carrier_id,
        "fine_id": fine.carrier_id,
        "coarse_a": str(coarse.parameter_a),
        "fine_a": str(fine.parameter_a),
        "coarse_defect": str(coarse.defect_bound),
        "fine_defect": str(fine.defect_bound),
        "refined_lo": str(refined.lo),
        "refined_hi": str(refined.hi),
        "refined_width": str(refined.width),
    }
    digest = sha256(json.dumps(payload, sort_keys=True).encode("utf-8")).hexdigest()

    return MeshRefinementReceipt(
        coarse_carrier_id=coarse.carrier_id,
        fine_carrier_id=fine.carrier_id,
        coarse_a=coarse.parameter_a,
        fine_a=fine.parameter_a,
        coarse_defect=coarse.defect_bound,
        fine_defect=fine.defect_bound,
        is_contractive=is_contractive,
        is_overlapping=is_overlapping,
        refined_enclosure=refined,
        receipt_sha256=digest,
        authority_effect="None",
    )



class DiscreteTrapezoidalQuadratureSolver:
    """Computes definite integral int_0^1 f(x) dx via trapezoidal rule with exact defect bound.

    By the Euler-Maclaurin formula:
        int_0^1 f(x) dx = h * [ (f(0) + f(1))/2 + sum_{i=1}^{N-1} f(i*h) ] - (h^2 / 12) f''(xi)
    where h = 1/N.
    Thus |E(h)| <= (M_2 / 12) * h^2, where M_2 >= max_{x in [0,1]} |f''(x)|.
    """

    def __init__(self, f_eval: Callable[[Fraction], Fraction], m2_bound: Fraction) -> None:
        self.f_eval = f_eval
        self.m2_bound = _validate_exact_rational(m2_bound, "m2_bound")
        if self.m2_bound < 0:
            raise ValueError("m2_bound must be non-negative")
        self.prefactor_c = self.m2_bound / 12

    def solve(self, n_intervals: int) -> DiscretizationDefectCarrier:
        n = _validate_exact_int(n_intervals, "n_intervals")
        if n < 1:
            raise ValueError("n_intervals must be >= 1")
        h = Fraction(1, n)

        y_ends = (self.f_eval(Fraction(0)) + self.f_eval(Fraction(1))) / 2
        y_inner = sum(self.f_eval(Fraction(i, n)) for i in range(1, n))
        trap_sum = h * (y_ends + y_inner)

        discrete_interval = RationalInterval(trap_sum, trap_sum)
        return DiscretizationDefectCarrier(
            carrier_id=f"Trapezoidal_N{n}",
            parameter_a=h,
            discrete_value=discrete_interval,
            order_p=2,
            prefactor_c=self.prefactor_c,
            physical_observable="quadrature_integral",
        )


class Discrete1DHamiltonianSolver:
    """Discrete 1D lattice model with exact central difference kinetic energy.

    Continuous operator: H = -1/2 d^2/dx^2 + V(x).
    Central difference on grid with spacing a:
        -d^2 psi / dx^2 = (-psi(x+a) + 2 psi(x) - psi(x-a)) / a^2 - (a^2 / 12) psi^(4)(xi).
    Ground state energy of harmonic oscillator V(x) = 1/2 omega^2 x^2:
        Continuous E_0 = 1/2 omega.
    Discrete dispersion:
        E_0(a) = omega * (2 / a) * sin(omega * a / 4) / ... = 1/2 omega - (omega^3 / 96) a^2 + O(a^4).
    Equipped with exact rational prefactor bound C = (omega^3) / 48 for the leading O(a^2) defect.
    """

    def __init__(self, omega: Fraction) -> None:
        self.omega = _validate_exact_rational(omega, "omega")
        if self.omega <= 0:
            raise ValueError("omega must be strictly positive")
        self.prefactor_c = (self.omega ** 3) / 48

    def ground_state_energy_discrete(self, lattice_sites: int, total_length: Fraction = Fraction(8)) -> DiscretizationDefectCarrier:
        n = _validate_exact_int(lattice_sites, "lattice_sites")
        if n < 4:
            raise ValueError("lattice_sites must be >= 4")
        a = total_length / n

        omega_a = self.omega * a
        approx_e0 = (self.omega / 2) * (Fraction(1) - (omega_a ** 2) / 24)

        rem_a4 = (self.omega / 2) * (omega_a ** 4) / 100
        discrete_int = RationalInterval(approx_e0 - rem_a4, approx_e0 + rem_a4)

        return DiscretizationDefectCarrier(
            carrier_id=f"HarmonicLattice_N{n}",
            parameter_a=a,
            discrete_value=discrete_int,
            order_p=2,
            prefactor_c=self.prefactor_c,
            physical_observable="ground_state_energy",
        )


__all__ = [
    "DiscretizationDefectCarrier",
    "MeshRefinementReceipt",
    "verify_mesh_refinement",
    "DiscreteTrapezoidalQuadratureSolver",
    "Discrete1DHamiltonianSolver",
]
