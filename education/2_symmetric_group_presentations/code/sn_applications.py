"""Downstream Domain Applications of S(n) Tower Architecture.

Source models and algorithms for Track 020 curriculum notebooks.
AuthorityEffect: None.
"""

from __future__ import annotations

import math
from dataclasses import dataclass
from typing import Sequence, Set, Tuple


def topological_relational_join(
    table_a: Set[Tuple[str, str]],
    table_b: Set[Tuple[str, str]],
) -> Set[Tuple[str, str, str]]:
    """Compute relational join as simplicial edge incidence pullback.

    Joins table_a (entity, department) and table_b (department, building)
    along the shared department attribute.
    """
    return {(name, dept, bldg) for (name, dept) in table_a for (d2, bldg) in table_b if dept == d2}


class SessionChannel:
    """Dual-channel linear session protocol with strict linear exhaustion."""

    def __init__(self) -> None:
        self.state: str = "INIT"

    def send(self, msg: str) -> None:
        """Send message along channel, transitioning INIT -> SENT."""
        if self.state != "INIT":
            raise ValueError(f"Linear violation: cannot send in state {self.state}")
        self.state = "SENT"

    def recv(self) -> str:
        """Receive message along channel, transitioning SENT -> CLOSED."""
        if self.state != "SENT":
            raise ValueError(f"Linear violation: cannot recv in state {self.state}")
        self.state = "CLOSED"
        return "ACK"

    @property
    def is_closed(self) -> bool:
        """Check if channel has completed its linear lifecycle."""
        return self.state == "CLOSED"


@dataclass
class DownstreamApplication:
    """Downstream application model enforcing Third Layer Law boundaries."""

    name: str
    domain: str
    layer: int = 3
    authority_effect: str = "None"
    genesis_effect: str = "None"

    def verify_fences(self) -> bool:
        """Verify layer boundary fences: zero generative authority over Genesis."""
        return self.authority_effect == "None" and self.genesis_effect == "None" and self.layer == 3


class ReggeMetric:
    """Floating-point equilateral triangle Gram example, not interval certification."""

    @staticmethod
    def equilateral_gram_determinant(edge_squared_scale: float = 1.0) -> float:
        """Compute Gram matrix determinant for an equilateral 2-simplex.

        Gram matrix is:
            [ [s,   s/2],
              [s/2, s  ] ]
        where s is edge_squared_scale.
        """
        s = edge_squared_scale
        return (s * s) - ((s * 0.5) * (s * 0.5))

    @staticmethod
    def equilateral_gram_trace(edge_squared_scale: float = 1.0) -> float:
        """Compute Gram matrix trace for an equilateral 2-simplex."""
        return 2.0 * edge_squared_scale

    @classmethod
    def verify_positivity(cls, edge_squared_scale: float = 1.0) -> bool:
        """Check Gram matrix determinant and trace are strictly positive."""
        det = cls.equilateral_gram_determinant(edge_squared_scale)
        trace = cls.equilateral_gram_trace(edge_squared_scale)
        return det > 0.0 and trace > 0.0


class ReggeCurvature:
    """Discrete Regge curvature and hinge deficit angle calculator."""

    @staticmethod
    def deficit_angle(dihedrals: Sequence[float]) -> float:
        """Calculate hinge deficit angle epsilon_h = 2*pi - sum(theta_i)."""
        return 2.0 * math.pi - sum(dihedrals)

    @classmethod
    def is_flat_hinge(cls, dihedrals: Sequence[float], tol: float = 1e-9) -> bool:
        """Check if sum of dihedral angles equals 2*pi within numeric tolerance."""
        deficit = cls.deficit_angle(dihedrals)
        return math.isclose(deficit, 0.0, abs_tol=tol)

    @classmethod
    def is_positive_curvature(cls, dihedrals: Sequence[float]) -> bool:
        """Check if deficit angle is strictly positive."""
        return cls.deficit_angle(dihedrals) > 0.0
