"""
CODA 2D CS-Q Discretization Defect Operators and 2D Multi-Mesh Refinement.

AuthorityEffect: None.

Equips 2D discrete lattice and grid solvers with explicit discretization error
operators across spatial dimensions (x, y):
    Result(a_x, a_y) = ContinuousValue + E(a_x, a_y),
where:
    |E(a_x, a_y)| <= C_x * a_x^{p_x} + C_y * a_y^{p_y}.

Yields certified 2D continuum enclosures:
    Enclosure_cont_2d = [Result - defect_bound, Result + defect_bound] in Q x Q,
and asserts contractive 2D multi-mesh refinement without floating-point approximations.
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
class DiscretizationDefect2DCarrier:
    """2D discrete solver outcome with explicit 2D discretization error operator."""

    carrier_id: str
    parameter_ax: Fraction
    parameter_ay: Fraction
    discrete_value: RationalInterval
    order_px: int
    order_py: int
    prefactor_cx: Fraction
    prefactor_cy: Fraction
    physical_observable: str = "2d_energy"

    def __post_init__(self) -> None:
        ax = _validate_exact_rational(self.parameter_ax, "parameter_ax")
        ay = _validate_exact_rational(self.parameter_ay, "parameter_ay")
        if ax <= 0 or ay <= 0:
            raise ValueError(f"Grid parameters ax, ay must be strictly positive, got ({ax}, {ay})")
        px = _validate_exact_int(self.order_px, "order_px")
        py = _validate_exact_int(self.order_py, "order_py")
        if px < 1 or py < 1:
            raise ValueError(f"Orders px, py must be >= 1, got ({px}, {py})")
        cx = _validate_exact_rational(self.prefactor_cx, "prefactor_cx")
        cy = _validate_exact_rational(self.prefactor_cy, "prefactor_cy")
        if cx < 0 or cy < 0:
            raise ValueError(f"Prefactors cx, cy must be non-negative, got ({cx}, {cy})")
        if not isinstance(self.discrete_value, RationalInterval):
            raise TypeError("discrete_value must be RationalInterval")

    @property
    def defect_bound(self) -> Fraction:
        """Total 2D defect bound |E(ax, ay)| <= Cx * ax^px + Cy * ay^py."""
        dx = self.prefactor_cx * (self.parameter_ax ** self.order_px)
        dy = self.prefactor_cy * (self.parameter_ay ** self.order_py)
        return dx + dy

    @property
    def continuum_enclosure(self) -> RationalInterval:
        """Certified rational interval enclosing the true continuous 2D value."""
        b = self.defect_bound
        return RationalInterval(self.discrete_value.lo - b, self.discrete_value.hi + b)

    def encloses(self, true_continuum_val: Any) -> bool:
        val = _validate_exact_rational(true_continuum_val, "true_continuum_val")
        return self.continuum_enclosure.contains(val)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "carrier_id": self.carrier_id,
            "grid_spacings": (str(self.parameter_ax), str(self.parameter_ay)),
            "orders": (self.order_px, self.order_py),
            "prefactors": (str(self.prefactor_cx), str(self.prefactor_cy)),
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
class Mesh2DRefinementReceipt:
    """Audit receipt verifying 2D multi-mesh consistency between coarse and fine solves."""

    coarse_carrier_id: str
    fine_carrier_id: str
    coarse_grid: Tuple[Fraction, Fraction]
    fine_grid: Tuple[Fraction, Fraction]
    coarse_defect: Fraction
    fine_defect: Fraction
    is_contractive: bool
    is_overlapping: bool
    refined_enclosure: RationalInterval
    receipt_sha256: str
    authority_effect: str = "None"


def verify_2d_mesh_refinement(
    coarse: DiscretizationDefect2DCarrier,
    fine: DiscretizationDefect2DCarrier,
) -> Mesh2DRefinementReceipt:
    """Assert contractive 2D defect reduction and non-empty intersection of 2D enclosures."""
    if coarse.parameter_ax <= fine.parameter_ax or coarse.parameter_ay <= fine.parameter_ay:
        raise ValueError(
            f"coarse spacings ({coarse.parameter_ax}, {coarse.parameter_ay}) must be strictly "
            f"greater than fine spacings ({fine.parameter_ax}, {fine.parameter_ay})"
        )
    if (coarse.order_px, coarse.order_py) != (fine.order_px, fine.order_py):
        raise ValueError("Order mismatch between coarse and fine 2D meshes")

    is_contractive = fine.defect_bound < coarse.defect_bound
    is_overlapping = coarse.continuum_enclosure.intersects(fine.continuum_enclosure)

    if not is_overlapping:
        raise ValueError(
            f"2D discretization inconsistency: coarse enclosure {coarse.continuum_enclosure} "
            f"does not intersect fine enclosure {fine.continuum_enclosure}"
        )

    refined = coarse.continuum_enclosure.intersect(fine.continuum_enclosure)

    payload = {
        "coarse_id": coarse.carrier_id,
        "fine_id": fine.carrier_id,
        "coarse_ax": str(coarse.parameter_ax),
        "coarse_ay": str(coarse.parameter_ay),
        "fine_ax": str(fine.parameter_ax),
        "fine_ay": str(fine.parameter_ay),
        "coarse_defect": str(coarse.defect_bound),
        "fine_defect": str(fine.defect_bound),
        "refined_lo": str(refined.lo),
        "refined_hi": str(refined.hi),
        "refined_width": str(refined.width),
    }
    digest = sha256(json.dumps(payload, sort_keys=True).encode("utf-8")).hexdigest()

    return Mesh2DRefinementReceipt(
        coarse_carrier_id=coarse.carrier_id,
        fine_carrier_id=fine.carrier_id,
        coarse_grid=(coarse.parameter_ax, coarse.parameter_ay),
        fine_grid=(fine.parameter_ax, fine.parameter_ay),
        coarse_defect=coarse.defect_bound,
        fine_defect=fine.defect_bound,
        is_contractive=is_contractive,
        is_overlapping=is_overlapping,
        refined_enclosure=refined,
        receipt_sha256=digest,
        authority_effect="None",
    )


class Discrete2DCubatureSolver:
    """Computes double integral iint_{[0,1]^2} f(x, y) dx dy via 2D trapezoidal product rule.

    By 2D Euler-Maclaurin expansion:
      |E(hx, hy)| <= (M_xx / 12) * hx^2 + (M_yy / 12) * hy^2
    where M_xx >= max |d^2 f / dx^2| and M_yy >= max |d^2 f / dy^2|.
    """

    def __init__(
        self,
        f_eval: Callable[[Fraction, Fraction], Fraction],
        m_xx_bound: Fraction,
        m_yy_bound: Fraction,
    ) -> None:
        self.f_eval = f_eval
        self.m_xx = _validate_exact_rational(m_xx_bound, "m_xx_bound")
        self.m_yy = _validate_exact_rational(m_yy_bound, "m_yy_bound")
        self.prefactor_cx = self.m_xx / 12
        self.prefactor_cy = self.m_yy / 12

    def solve(self, nx: int, ny: int) -> DiscretizationDefect2DCarrier:
        nx_val = _validate_exact_int(nx, "nx")
        ny_val = _validate_exact_int(ny, "ny")
        if nx_val < 1 or ny_val < 1:
            raise ValueError("nx, ny must be >= 1")

        hx = Fraction(1, nx_val)
        hy = Fraction(1, ny_val)

        total = Fraction(0)
        for i in range(nx_val + 1):
            wx = Fraction(1, 2) if (i == 0 or i == nx_val) else Fraction(1)
            xi = Fraction(i, nx_val)
            for j in range(ny_val + 1):
                wy = Fraction(1, 2) if (j == 0 or j == ny_val) else Fraction(1)
                yj = Fraction(j, ny_val)
                total += wx * wy * self.f_eval(xi, yj)

        cub_sum = hx * hy * total
        val_interval = RationalInterval(cub_sum, cub_sum)

        return DiscretizationDefect2DCarrier(
            carrier_id=f"Cubature2D_{nx_val}x{ny_val}",
            parameter_ax=hx,
            parameter_ay=hy,
            discrete_value=val_interval,
            order_px=2,
            order_py=2,
            prefactor_cx=self.prefactor_cx,
            prefactor_cy=self.prefactor_cy,
            physical_observable="2d_cubature_integral",
        )


__all__ = [
    "DiscretizationDefect2DCarrier",
    "Mesh2DRefinementReceipt",
    "verify_2d_mesh_refinement",
    "Discrete2DCubatureSolver",
]
