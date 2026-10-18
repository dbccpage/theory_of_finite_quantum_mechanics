"""Proposal Evaluator conforming to urn:omega:governance:evaluator:v1.0.0.

Doctrine:
- Evaluator applies declared evaluation policy to already-computed facts.
- Evaluator does not measure, discover, mutate, terminalize, or execute.
- Designed for exact equivalence with Rust trait:
    pub trait Evaluator<C> {
        fn evaluate(&self, input: &EvaluationInput<C>, policy: &EvaluationPolicy)
            -> Result<EvaluationResult, EvaluationError>;
    }
"""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Mapping, Sequence


class KillReason(str, Enum):
    NONE = "None"
    NON_CONTRACTIVE = "NonContractive"
    AUTHORITY_LEAK = "AuthorityLeak"
    UNBOUNDED_ENERGY = "UnboundedEnergy"
    DIVERGENCE = "Divergence"
    CYCLE_DETECTED = "CycleDetected"


@dataclass(frozen=True, slots=True)
class EvaluatorConfig:
    """Explicit tolerance specification and evaluation policy thresholds."""

    tolerance: float = 1.0e-8
    efficiency_epsilon: float = 1.0e-6
    max_proposals: int = 100
    require_exactness: bool = False


@dataclass(frozen=True, slots=True)
class ProposalEvaluationResult:
    """Deterministic evaluation verdict decision envelope."""

    proposal_id: str
    is_admissible: bool
    initial_l1_mass: float
    final_l1_mass: float
    mass_drop: float
    efficiency: float
    kill_reason: KillReason = KillReason.NONE
    details: str = "OK"
    authority_effect: str = "None"


@dataclass(frozen=True, slots=True)
class ProposalEvaluator:
    """Read-only governance decision layer applying admissibility policy to proposals."""

    evaluator_id: str = "proposal-evaluator-v1"
    evaluator_version: str = "v1.0.0"
    config: EvaluatorConfig = field(default_factory=EvaluatorConfig)

    def evaluate_proposal(
        self,
        proposal_id: str,
        initial_mass: float,
        final_mass: float,
        effort: float = 1.0,
        metadata: Mapping[str, Any] | None = None,
    ) -> ProposalEvaluationResult:
        """Evaluates a single proposal for contractiveness, residual drop, and authority cleanliness."""
        meta = metadata or {}
        authority = meta.get("authority_effect", "None")
        if authority != "None":
            return ProposalEvaluationResult(
                proposal_id=proposal_id,
                is_admissible=False,
                initial_l1_mass=initial_mass,
                final_l1_mass=final_mass,
                mass_drop=0.0,
                efficiency=0.0,
                kill_reason=KillReason.AUTHORITY_LEAK,
                details=f"Prohibited authority effect: {authority}",
            )

        mass_drop = initial_mass - final_mass
        if mass_drop < -self.config.tolerance:
            return ProposalEvaluationResult(
                proposal_id=proposal_id,
                is_admissible=False,
                initial_l1_mass=initial_mass,
                final_l1_mass=final_mass,
                mass_drop=mass_drop,
                efficiency=0.0,
                kill_reason=KillReason.NON_CONTRACTIVE,
                details=f"Residual mass increased by {-mass_drop:.6e}",
            )

        if effort <= 0.0:
            effort = 1.0
        efficiency = max(0.0, mass_drop) / effort

        return ProposalEvaluationResult(
            proposal_id=proposal_id,
            is_admissible=True,
            initial_l1_mass=initial_mass,
            final_l1_mass=final_mass,
            mass_drop=mass_drop,
            efficiency=efficiency,
            kill_reason=KillReason.NONE,
            details="Strict descent verified",
        )

    def rank_proposals(
        self,
        results: Sequence[ProposalEvaluationResult],
    ) -> tuple[ProposalEvaluationResult, ...]:
        """Deterministically ranks admissible proposals sorted by efficiency descending."""
        admissible = sorted(
            [r for r in results if r.is_admissible],
            key=lambda r: (r.efficiency, -len(r.proposal_id), r.proposal_id),
            reverse=True,
        )
        return tuple(admissible)


    def select_best_proposal(
        self,
        proposals: Sequence[tuple[str, float, float, float, Mapping[str, Any] | None]],
    ) -> ProposalEvaluationResult | None:
        """Deterministically selects the most efficient contractive proposal from evaluated candidates."""
        evaluated = [
            self.evaluate_proposal(p_id, init, fin, eff, meta)
            for p_id, init, fin, eff, meta in proposals
        ]
        ranked = self.rank_proposals(evaluated)
        return ranked[0] if ranked else None
