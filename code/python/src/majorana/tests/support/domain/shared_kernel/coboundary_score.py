"""Shared Kernel: Coboundary scoring, candidate proposal, and residual drop Value Objects.

AuthorityEffect: None.
"""

from __future__ import annotations

from dataclasses import dataclass, field

from .authority_effect import AuthorityEffect
from .residual_colour import ResidualColour
from .residual_drop import ResidualDropV1


@dataclass(frozen=True, slots=True)
class CoboundaryScoreResult:
    """Result of evaluating discrete coboundary scoring vector for a candidate proposal."""

    phi1: float
    gamma2: float
    xi: float
    combined_score: float
    is_exact: bool
    refusals: tuple[str, ...] = field(default_factory=tuple)
    residual_colour: str = ResidualColour.OPEN.value

    def to_dict(self) -> dict[str, object]:
        return {
            "phi1": self.phi1,
            "gamma2": self.gamma2,
            "xi": self.xi,
            "combined_score": self.combined_score,
            "is_exact": self.is_exact,
            "refusals": list(self.refusals),
            "residual_colour": self.residual_colour,
            "authority_effect": AuthorityEffect.NONE.value,
        }


@dataclass(frozen=True, slots=True)
class CandidateProposal:
    """Value object representing a candidate proposal with payload, patch, and target demands."""

    proposal_id: str
    target_obstruction_ids: tuple[str, ...]
    eliminated_demand_ids: tuple[str, ...]
    patch_bytes_digest: str | None = None
    dual_witness_digest: str | None = None
    carrier_hash: str | None = None

    def __post_init__(self) -> None:
        object.__setattr__(self, "target_obstruction_ids", tuple(sorted(set(self.target_obstruction_ids))))
        object.__setattr__(self, "eliminated_demand_ids", tuple(sorted(set(self.eliminated_demand_ids))))


__all__ = [
    "CandidateProposal",
    "CoboundaryScoreResult",
    "ResidualDropV1",
]
