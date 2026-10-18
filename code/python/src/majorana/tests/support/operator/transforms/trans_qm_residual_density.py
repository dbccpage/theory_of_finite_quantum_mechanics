"""Diagnostics-only bridge from H1 residual mass to density reports.

Faithful port of ``crates/omega_engine.crates.engine/src/quantum/residual_density_bridge.rs``.
"""

from __future__ import annotations
import math
from typing import List, Optional, Tuple

from omega_engine_governance.contracts import AuthorityEffect
from omega_engine.crates.operator.constructor.ctor_qm_density_from_h1 import (
    density_from_sectors_diagonal,
    incidence_sector_decomposition,
    l1_sector_decomposition,
)
from omega_engine.crates.type.qm_density import (
    BranchResidualCandidate,
    BranchResidualCandidateDiagnostic,
    BranchResidualSearchReport,
    H1Density,
    H1Sector,
    H1SectorDecomposition,
    ResidualDensityConstruction,
    ResidualDensityDiagnostics,
    ResidualDensityReport,
    SectorMassCertificate,
)


def edge_residual_density_report(h1: List[float]) -> Optional[ResidualDensityReport]:
    validate_residual_slice(h1)
    sectors = l1_sector_decomposition(h1)
    if sectors is None:
        return None

    return residual_density_report_from_sectors(
        ResidualDensityConstruction.EdgeDiagonal,
        len(h1),
        sectors,
    )


def incidence_residual_density_report(
    n_nodes: int,
    edges: List[Tuple[int, int]],
    h1: List[float],
) -> Optional[ResidualDensityReport]:
    validate_residual_slice(h1)
    sectors = incidence_sector_decomposition(n_nodes, edges, h1)
    if sectors is None:
        return None

    return residual_density_report_from_sectors(
        ResidualDensityConstruction.IncidenceDiagonal,
        len(edges),
        sectors,
    )


def residual_density_report_from_sectors(
    construction: ResidualDensityConstruction,
    source_count: int,
    sectors: H1SectorDecomposition,
) -> ResidualDensityReport:
    density = density_from_sectors_diagonal(sectors)
    diagnostics = diagnostics_for(construction, source_count, density)
    return ResidualDensityReport(density=density, diagnostics=diagnostics)


def coarse_grain_residual_density_report(
    report: ResidualDensityReport,
    labels: List[int],
) -> ResidualDensityReport:
    source_sectors = report.density.sectors.sectors
    if len(labels) != len(source_sectors):
        raise ValueError(
            f"coarse label count {len(labels)} does not match sector count {len(source_sectors)}"
        )
    if not labels:
        raise ValueError("coarse labels are empty")

    target_dim = max(labels) + 1

    weights = [0.0] * target_dim
    edge_indices: List[List[int]] = [[] for _ in range(target_dim)]
    for sector, label in zip(source_sectors, labels):
        weights[label] += sector.weight
        edge_indices[label].extend(sector.edge_indices)

    raw_l1_mass = report.density.sectors.certificate.phi1
    if raw_l1_mass <= 0.0 or not math.isfinite(raw_l1_mass):
        raise ValueError("coarse-grain source has non-positive or non-finite Phi1")

    sectors_list = []
    for index, weight in enumerate(weights):
        sectors_list.append(
            H1Sector(
                index=index,
                edge_indices=edge_indices[index],
                weight=weight,
                probability=weight / raw_l1_mass,
            )
        )

    sector_weight_sum = sum(s.weight for s in sectors_list)
    prob_sum = sum(s.probability for s in sectors_list)

    coarse = H1SectorDecomposition(
        sectors=sectors_list,
        certificate=SectorMassCertificate(
            phi1=raw_l1_mass,
            sector_weight_sum=sector_weight_sum,
            mass_error=abs(sector_weight_sum - raw_l1_mass),
            prob_error=abs(prob_sum - 1.0),
        ),
    )

    return residual_density_report_from_sectors(
        ResidualDensityConstruction.CoarseGrainedDiagonal,
        report.diagnostics.source_count,
        coarse,
    )


def branch_residual_search_report(
    candidates: List[BranchResidualCandidate],
) -> Optional[BranchResidualSearchReport]:
    if not candidates:
        return None

    for candidate in candidates:
        if not candidate.label or not candidate.label.strip():
            raise ValueError("branch candidate labels must be non-empty")
        if not math.isfinite(candidate.proposal_mass) or candidate.proposal_mass < 0.0:
            raise ValueError("branch proposal masses must be finite and nonnegative")

    total_mass = sum(c.proposal_mass for c in candidates)
    if total_mass <= 0.0:
        return None

    sectors_list = []
    for index, candidate in enumerate(candidates):
        sectors_list.append(
            H1Sector(
                index=index,
                edge_indices=[],
                weight=candidate.proposal_mass,
                probability=candidate.proposal_mass / total_mass,
            )
        )

    sector_weight_sum = sum(s.weight for s in sectors_list)
    prob_sum = sum(s.probability for s in sectors_list)

    decomposition = H1SectorDecomposition(
        sectors=sectors_list,
        certificate=SectorMassCertificate(
            phi1=total_mass,
            sector_weight_sum=sector_weight_sum,
            mass_error=abs(sector_weight_sum - total_mass),
            prob_error=abs(prob_sum - 1.0),
        ),
    )

    report = residual_density_report_from_sectors(
        ResidualDensityConstruction.BranchProposalDiagonal,
        len(candidates),
        decomposition,
    )

    ranked = list(enumerate(report.diagnostics.sector_probabilities))
    ranked.sort(key=lambda item: (-item[1], item[0]))

    ranks = [0] * len(candidates)
    for rank, (index, _) in enumerate(ranked):
        ranks[index] = rank + 1

    diagnostic_candidates = []
    for index, (candidate, probability) in enumerate(
        zip(candidates, report.diagnostics.sector_probabilities)
    ):
        diagnostic_candidates.append(
            BranchResidualCandidateDiagnostic(
                label=candidate.label,
                proposal_mass=candidate.proposal_mass,
                proposal_probability=probability,
                rank=ranks[index],
            )
        )

    return BranchResidualSearchReport(
        density=report.density,
        candidates=diagnostic_candidates,
        total_mass=total_mass,
        trace=report.diagnostics.trace,
        entropy=report.diagnostics.entropy,
        purity=report.diagnostics.purity,
        dominant_branch=report.diagnostics.dominant_sector,
        authority_effect=AuthorityEffect.None_,
    )


def residual_channel_pushforward_report(
    report: ResidualDensityReport,
    transition: List[List[float]],
) -> ResidualDensityReport:
    source_sectors = report.density.sectors.sectors
    if len(transition) != len(source_sectors):
        raise ValueError(
            f"channel row count {len(transition)} does not match source sector count {len(source_sectors)}"
        )
    if not transition:
        raise ValueError("channel transition is empty")

    target_dim = len(transition[0])
    if target_dim == 0:
        raise ValueError("channel target dimension is zero")

    weights = [0.0] * target_dim
    for row_index, (sector, row) in enumerate(zip(source_sectors, transition)):
        validate_stochastic_row(row_index, row, target_dim)
        for target, coefficient in enumerate(row):
            weights[target] += sector.weight * coefficient

    raw_l1_mass = report.density.sectors.certificate.phi1
    if raw_l1_mass <= 0.0 or not math.isfinite(raw_l1_mass):
        raise ValueError("channel source has non-positive or non-finite Phi1")

    sectors_list = []
    for index, weight in enumerate(weights):
        sectors_list.append(
            H1Sector(
                index=index,
                edge_indices=[],
                weight=weight,
                probability=weight / raw_l1_mass,
            )
        )

    sector_weight_sum = sum(s.weight for s in sectors_list)
    prob_sum = sum(s.probability for s in sectors_list)

    pushed = H1SectorDecomposition(
        sectors=sectors_list,
        certificate=SectorMassCertificate(
            phi1=raw_l1_mass,
            sector_weight_sum=sector_weight_sum,
            mass_error=abs(sector_weight_sum - raw_l1_mass),
            prob_error=abs(prob_sum - 1.0),
        ),
    )

    return residual_density_report_from_sectors(
        ResidualDensityConstruction.ChannelPushforwardDiagonal,
        report.diagnostics.source_count,
        pushed,
    )


def diagnostics_for(
    construction: ResidualDensityConstruction,
    source_count: int,
    density: H1Density,
) -> ResidualDensityDiagnostics:
    sector_weights = [s.weight for s in density.sectors.sectors]
    sector_probabilities = [s.probability for s in density.sectors.sectors]
    try:
        entropy = density.density.von_neumann_entropy()
    except Exception as err:
        raise ValueError(f"Failed to compute residual-density entropy: {err}") from err
    purity = density.density.purity()

    return ResidualDensityDiagnostics(
        construction=construction,
        source_count=source_count,
        dim=density.density.dim(),
        sector_weights=sector_weights,
        sector_probabilities=sector_probabilities,
        raw_l1_mass=density.sectors.certificate.phi1,
        mass_error=density.sectors.certificate.mass_error,
        prob_error=density.sectors.certificate.prob_error,
        trace=density.density.trace(),
        entropy=entropy,
        purity=purity,
        l1_coherence=density.density.l1_coherence(),
        dominant_sector=dominant_sector(density.sectors),
        residual_concentration=purity,
        authority_effect=AuthorityEffect.None_,
    )


def validate_residual_slice(h1: List[float]) -> None:
    for value in h1:
        if not math.isfinite(value):
            raise ValueError("h1 contains non-finite residual")


def validate_stochastic_row(row_index: int, row: List[float], target_dim: int) -> None:
    if len(row) != target_dim:
        raise ValueError(
            f"channel row {row_index} length {len(row)} does not match target dimension {target_dim}"
        )
    for coefficient in row:
        if not math.isfinite(coefficient) or coefficient < 0.0:
            raise ValueError(
                f"channel row {row_index} contains non-finite or negative coefficient"
            )

    row_sum = sum(row)
    if abs(row_sum - 1.0) > 1e-9:
        raise ValueError(f"channel row {row_index} is not stochastic: sum={row_sum}")


def dominant_sector(sectors: H1SectorDecomposition) -> Optional[int]:
    best = None
    for sector in sectors.sectors:
        if best is None or sector.probability > best[1]:
            best = (sector.index, sector.probability)
    return best[0] if best is not None else None




