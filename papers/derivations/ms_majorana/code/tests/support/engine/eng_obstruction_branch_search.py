"""Obstruction-native branch search over candidate residual transitions.

Faithful port of ``crates/omega_engine.crates.engine/src/obstruction_branch_search.rs``.
"""

from __future__ import annotations
import math
from typing import List, Optional

CONTRACT_ID = "urn:omega:engine:obstruction_branch_search_engine:file:v1.0.0"
AUTHORITY_EFFECT = "None"

from omega_engine_governance.contracts import AuthorityEffect
from omega_engine.crates.operator.transforms.trans_qm_residual_density import (
    branch_residual_search_report,
)
from omega_engine.crates.type.obstruction_branch import (
    ObstructionBranchCandidate,
    ObstructionBranchCandidateReport,
    ObstructionBranchSearchConfig,
    ObstructionBranchSearchReport,
    ObstructionBranchVerdict,
    ObstructionImprovementTier,
    ObstructionSearchPoint,
)
from omega_engine.crates.type.qm_density import BranchResidualCandidate


def validate_obstruction_search_point(point: ObstructionSearchPoint, role: str) -> None:
    if not math.isfinite(point.phi1) or point.phi1 < 0.0:
        raise ValueError(f"{role} Phi1 must be finite and nonnegative")
    if not math.isfinite(point.gamma2) or point.gamma2 < 0.0:
        raise ValueError(f"{role} Gamma2 must be finite and nonnegative")
    if point.xi is not None and (not math.isfinite(point.xi) or point.xi < 0.0):
        raise ValueError(f"{role} Xi must be finite and nonnegative")


def validate_obstruction_branch_config(config: ObstructionBranchSearchConfig) -> None:
    for name, value in (
        ("Phi1", config.phi_tol),
        ("Gamma2", config.gamma_tol),
        ("Xi", config.xi_tol),
    ):
        if not math.isfinite(value) or value < 0.0:
            raise ValueError(f"{name} tolerance must be finite and nonnegative")


def obstruction_branch_search_report(
    before: ObstructionSearchPoint,
    candidates: List[ObstructionBranchCandidate],
    config: ObstructionBranchSearchConfig,
) -> ObstructionBranchSearchReport:
    validate_obstruction_branch_config(config)
    validate_obstruction_search_point(before, "before")

    if not candidates:
        return ObstructionBranchSearchReport(
            before=before,
            candidates=[],
            branch_density=None,
            best_descent_candidate=None,
            authority_effect=AuthorityEffect.None_,
        )

    reports = []
    for index, candidate in enumerate(candidates):
        if not candidate.label or not candidate.label.strip():
            raise ValueError(f"branch candidate {index} label must be non-empty")
        validate_obstruction_search_point(candidate.after, "candidate")
        improvement_tier, proposal_mass = improvement_mass_fn(
            before, candidate.after, config
        )
        verdict = (
            ObstructionBranchVerdict.RejectedNoDescent
            if improvement_tier == ObstructionImprovementTier.None_
            else ObstructionBranchVerdict.StrictDescent
        )
        reports.append(
            ObstructionBranchCandidateReport(
                label=candidate.label,
                provenance=candidate.provenance,
                after=candidate.after,
                verdict=verdict,
                improvement_tier=improvement_tier,
                proposal_mass=proposal_mass,
                proposal_probability=0.0,
                rank=0,
                authority_effect=AuthorityEffect.None_,
            )
        )

    proposal_candidates = [
        BranchResidualCandidate(label=r.label, proposal_mass=r.proposal_mass)
        for r in reports
    ]
    branch_density = branch_residual_search_report(proposal_candidates)

    if branch_density is not None:
        for report, branch in zip(reports, branch_density.candidates):
            report.proposal_probability = branch.proposal_probability
            report.rank = branch.rank

    best_idx = None
    best_val = -1.0
    for idx, report in enumerate(reports):
        if report.verdict == ObstructionBranchVerdict.StrictDescent:
            if (
                best_idx is None
                or report.proposal_mass > best_val
                or (abs(report.proposal_mass - best_val) < 1e-15 and idx > best_idx)
            ):
                best_idx = idx
                best_val = report.proposal_mass

    return ObstructionBranchSearchReport(
        before=before,
        candidates=reports,
        branch_density=branch_density,
        best_descent_candidate=best_idx,
        authority_effect=AuthorityEffect.None_,
    )


def improvement_mass_fn(
    before: ObstructionSearchPoint,
    after: ObstructionSearchPoint,
    config: ObstructionBranchSearchConfig,
) -> tuple[ObstructionImprovementTier, float]:
    if after.phi1 + config.phi_tol < before.phi1:
        return (
            ObstructionImprovementTier.Phi1,
            max(before.phi1 - after.phi1, 0.0),
        )

    if abs(after.phi1 - before.phi1) > config.phi_tol:
        return (ObstructionImprovementTier.None_, 0.0)

    if after.gamma2 + config.gamma_tol < before.gamma2:
        return (
            ObstructionImprovementTier.Gamma2,
            max(before.gamma2 - after.gamma2, 0.0),
        )

    if abs(after.gamma2 - before.gamma2) > config.gamma_tol:
        return (ObstructionImprovementTier.None_, 0.0)

    if before.xi is not None and after.xi is not None:
        if after.xi + config.xi_tol < before.xi:
            return (
                ObstructionImprovementTier.Xi,
                max(before.xi - after.xi, 0.0),
            )

from omega_engine.crates.engine.base.eng_base import Engine


class ObstructionBranchSearchEngine(Engine):
    authority_effect = "None"
    implements = (CONTRACT_ID,)





