"""Pure bridge from L1 Hodge residuals (h1) to density matrices.

Faithful port of ``crates/omega_engine.crates.engine/src/quantum/density_from_h1.rs``.

Computes algebraic carriers derived from h1: sector weights, normalized
probabilities, optional witnessed phases, and the corresponding density matrix
(built via :class:`omega_linear_algebra.density.NumericalDensityMatrix`).

Error convention mirrors Rust:
  * ``Option<T>`` -> ``None``
  * ``Result<_, String>`` -> ``ValueError`` with the same message
  * ``Result<_, DensityMatrixError>`` -> the typed exception from ``density.py``
"""

from __future__ import annotations
import math
from typing import List, Optional


from omega_engine.crates.linear_algebra_theory.density import (
    DensityMatrixConfig,
    NumericalDensityMatrix,
    ZeroDimension,
    NonFiniteEntry,
    ZeroVector,
    H1NormalizationError,
)
from omega_engine.crates.type.qm_density import (
    H1Density,
    H1Sector,
    H1SectorDecomposition,
    PhaseWitness,
    PhaseWitnessKind,
    SectorMassCertificate,
)

MASS_EPS = 1e-12


class DensityRefusal(Exception):
    def __init__(self, refusal_route: str, message: str = ""):
        super().__init__(message or refusal_route)
        self.refusal_route = refusal_route


class NoValidDensity(DensityRefusal):
    def __init__(self, msg: str = "NO_VALID_DENSITY"):
        super().__init__("NO_VALID_DENSITY", msg)


class ZeroResidualVector(DensityRefusal):
    def __init__(self, msg: str = "ZERO_RESIDUAL_VECTOR"):
        super().__init__("ZERO_RESIDUAL_VECTOR", msg)


class H1NormalizationRefused(DensityRefusal):
    def __init__(self, msg: str = "H1_NORMALIZATION_REFUSED"):
        super().__init__("H1_NORMALIZATION_REFUSED", msg)


class DensityConstructionRefused(DensityRefusal):
    def __init__(self, msg: str = "DENSITY_CONSTRUCTION_REFUSED"):
        super().__init__("DENSITY_CONSTRUCTION_REFUSED", msg)


def _with_certificate(sectors: List[H1Sector], phi1: float) -> H1SectorDecomposition:
    sector_weight_sum = sum(s.weight for s in sectors)
    prob_sum = sum(s.probability for s in sectors)
    return H1SectorDecomposition(
        sectors=sectors,
        certificate=SectorMassCertificate(
            phi1=phi1,
            sector_weight_sum=sector_weight_sum,
            mass_error=abs(sector_weight_sum - phi1),
            prob_error=abs(prob_sum - 1.0),
        ),
    )


def edge_sector_decomposition(h1) -> Optional[H1SectorDecomposition]:
    if not len(h1) or any(not math.isfinite(v) for v in h1):
        return None
    phi1 = sum(abs(v) for v in h1)
    if phi1 <= MASS_EPS:
        return None
    sectors = []
    for index, value in enumerate(h1):
        weight = abs(value)
        sectors.append(
            H1Sector(
                index=index,
                edge_indices=[index],
                weight=weight,
                probability=weight / phi1,
            )
        )
    return _with_certificate(sectors, phi1)


def incidence_sector_decomposition(
    n_nodes: int, edges, h1
) -> Optional[H1SectorDecomposition]:
    if n_nodes == 0 or not len(h1):
        return None
    if len(edges) != len(h1):
        raise ValueError(f"h1 length {len(h1)} does not match edge count {len(edges)}")
    if any(not math.isfinite(v) for v in h1):
        raise ValueError("h1 contains non-finite residual")

    phi1 = sum(abs(v) for v in h1)
    if phi1 <= MASS_EPS:
        return None

    weights = [0.0] * n_nodes
    edge_indices: List[List[int]] = [[] for _ in range(n_nodes)]
    for edge_index, (u, v) in enumerate(edges):
        if u < 0 or v < 0 or u >= n_nodes or v >= n_nodes:
            raise ValueError(
                f"edge {edge_index} has endpoint outside node carrier of dimension {n_nodes}"
            )

        half_weight = 0.5 * abs(h1[edge_index])
        weights[u] += half_weight
        weights[v] += half_weight
        edge_indices[u].append(edge_index)
        edge_indices[v].append(edge_index)

    sectors = []
    for index in range(n_nodes):
        sectors.append(
            H1Sector(
                index=index,
                edge_indices=edge_indices[index],
                weight=weights[index],
                probability=weights[index] / phi1,
            )
        )
    return _with_certificate(sectors, phi1)


def rank_one_density_from_residual_checked(
    h1, config: DensityMatrixConfig
) -> NumericalDensityMatrix:
    if not len(h1):
        raise ZeroDimension("density matrix dimension must be positive")
    if any(not math.isfinite(v) for v in h1):
        raise NonFiniteEntry("density matrix contains non-finite entry at index 0")

    norm2 = sum(v * v for v in h1)
    if norm2 <= config.zero_norm_tol():
        raise ZeroVector("residual vector has zero norm")

    delta = abs(norm2 - 1.0)
    if delta > config.trace_tol():
        raise H1NormalizationError(
            f"h1 normalization error: delta={delta}, tol={config.trace_tol()}"
        )

    psi = [complex(v, 0.0) for v in h1]
    return NumericalDensityMatrix.from_amplitudes(psi, config)


def rank_one_density_from_residual(h1) -> Optional[NumericalDensityMatrix]:
    try:
        return rank_one_density_from_residual_checked(h1, DensityMatrixConfig.default())
    except Exception:
        return None


def density_from_h1(h1) -> Optional[H1Density]:
    cfg = DensityMatrixConfig.default()
    try:
        density = rank_one_density_from_residual_checked(h1, cfg)
    except Exception:
        return None
    sectors = edge_sector_decomposition(h1)
    if sectors is None:
        return None
    return H1Density(density=density, sectors=sectors, phase_witness=None)


def diagonal_density_from_h1(h1) -> Optional[H1Density]:
    sectors = edge_sector_decomposition(h1)
    if sectors is None:
        return None
    try:
        return density_from_sectors_diagonal(sectors)
    except Exception:
        return None


def density_from_h1_typed(h1) -> H1Density:
    cfg = DensityMatrixConfig.default()
    if not len(h1):
        raise NoValidDensity("empty h1 residual")
    norm2 = sum(v * v for v in h1)
    if norm2 <= cfg.zero_norm_tol():
        raise ZeroResidualVector()
    try:
        density = rank_one_density_from_residual_checked(h1, cfg)
    except H1NormalizationError as e:
        raise H1NormalizationRefused(str(e))
    except Exception as e:
        raise DensityConstructionRefused(str(e))

    sectors = edge_sector_decomposition(h1)
    if sectors is None:
        raise NoValidDensity("failed to construct sector decomposition from h1")
    return H1Density(density=density, sectors=sectors, phase_witness=None)


def diagonal_density_from_h1_typed(h1) -> H1Density:
    sectors = edge_sector_decomposition(h1)
    if sectors is None:
        raise NoValidDensity("failed to construct sector decomposition from h1")
    try:
        return density_from_sectors_diagonal(sectors)
    except Exception as e:
        raise DensityConstructionRefused(str(e))


def density_from_sectors_diagonal(sectors: H1SectorDecomposition) -> H1Density:
    if not sectors.sectors:
        raise ValueError("sector decomposition is empty")
    config = DensityMatrixConfig.default()
    if (
        sectors.certificate.mass_error > config.trace_tol()
        or sectors.certificate.prob_error > config.trace_tol()
    ):
        raise ValueError("sector mass or probability error exceeded tolerance")
    if any(
        not math.isfinite(s.weight)
        or not math.isfinite(s.probability)
        or s.probability < 0.0
        for s in sectors.sectors
    ):
        raise ValueError("sector decomposition contains non-finite or negative mass")

    probabilities = [s.probability for s in sectors.sectors]
    try:
        density = NumericalDensityMatrix.from_diagonal_probs(probabilities, config)
    except Exception as e:
        raise ValueError(f"Failed to create diagonal density: {e!r}")
    return H1Density(density=density, sectors=sectors, phase_witness=None)


def density_from_sectors_with_phase(
    sectors: H1SectorDecomposition, witness: PhaseWitness
) -> H1Density:
    if not sectors.sectors:
        raise ValueError("sector decomposition is empty")
    config = DensityMatrixConfig.default()
    if (
        sectors.certificate.mass_error > config.trace_tol()
        or sectors.certificate.prob_error > config.trace_tol()
    ):
        raise ValueError("sector mass or probability error exceeded tolerance")
    if any(
        not math.isfinite(s.weight)
        or not math.isfinite(s.probability)
        or s.probability < 0.0
        for s in sectors.sectors
    ):
        raise ValueError("sector decomposition contains non-finite or negative mass")

    if len(witness.phases) != len(sectors.sectors):
        raise ValueError(
            f"phase witness length {len(witness.phases)} does not match sector count {len(sectors.sectors)}"
        )
    if any(not math.isfinite(p) for p in witness.phases):
        raise ValueError("phase witness contains non-finite phase")

    amplitudes = []
    for sector, phase in zip(sectors.sectors, witness.phases):
        r = math.sqrt(sector.probability)
        amplitudes.append(complex(r * math.cos(phase), r * math.sin(phase)))

    norm2 = sum(c.real * c.real + c.imag * c.imag for c in amplitudes)
    if abs(norm2 - 1.0) > config.trace_tol():
        raise ValueError(f"amplitude normalization drift: delta={abs(norm2 - 1.0)}")

    try:
        density = NumericalDensityMatrix.from_amplitudes(amplitudes, config)
    except Exception as e:
        raise ValueError(f"Failed to create pure density: {e!r}")
    return H1Density(density=density, sectors=sectors, phase_witness=witness)


def density_from_h1_with_phase_witness(
    h1, witness: PhaseWitness
) -> Optional[H1Density]:
    sectors = edge_sector_decomposition(h1)
    if sectors is None:
        return None
    return density_from_sectors_with_phase(sectors, witness)


def incidence_density_from_h1(n_nodes: int, edges, h1) -> Optional[H1Density]:
    sectors = incidence_sector_decomposition(n_nodes, edges, h1)
    if sectors is None:
        return None
    return density_from_sectors_diagonal(sectors)


def density_for_carrier_dim(
    carrier_dim: int, n_nodes: int, edges, h1
) -> Optional[H1Density]:
    if carrier_dim == n_nodes:
        return incidence_density_from_h1(n_nodes, edges, h1)
    if carrier_dim == len(h1):
        return l2_raw_amplitude_diagnostic(h1)
    raise ValueError(
        f"density carrier dimension {carrier_dim} matches neither node count {n_nodes} "
        f"nor h1 length {len(h1)}"
    )


l1_sector_decomposition = edge_sector_decomposition


def diagonal_residual_density_diagnostic(h1) -> Optional[H1Density]:
    sectors = l1_sector_decomposition(h1)
    if sectors is None:
        return None
    try:
        return density_from_sectors_diagonal(sectors)
    except Exception:
        return None


def l2_raw_amplitude_diagnostic(h1) -> Optional[H1Density]:
    return density_from_h1(h1)


def conditional_phase_witness_lift(h1, witness: PhaseWitness) -> Optional[H1Density]:
    sectors = l1_sector_decomposition(h1)
    if sectors is None:
        return None
    return density_from_sectors_with_phase(sectors, witness)




