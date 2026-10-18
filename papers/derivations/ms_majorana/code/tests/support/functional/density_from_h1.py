"""
Pure bridge from L1 Hodge residuals to density matrices.

This module only computes algebraic carriers derived from h1:
sector weights, normalized probabilities, optional witnessed phases,
and the corresponding density matrix. It does not rank, select, accept,
tune, or compare candidates.

Undefined-case convention (consistent across the module):
    - Zero residual / zero mass within MASS_EPS  -> None  ("no density").
    - Empty residual                              -> None.
    - Non-finite residual (NaN/Inf)               -> ValueError (caller bug).
    - Carrier / endpoint / phase-length mismatch  -> ValueError (structural).
None means "carrier does not support a density"; ValueError means the inputs
are malformed. These are never silently mixed.

Density validity (canonical path ``density_from_h1`` /
``rank_one_density_from_residual``): the returned matrix is a rank-one
projector |psi><psi| with unit trace, Hermitian, and PSD. Non-canonical
diagonal / phase constructions are normalized but not guaranteed rank-one.
"""

from dataclasses import dataclass
from typing import List, Optional, Tuple
import numpy as np

MASS_EPS = 1e-12


@dataclass
class H1Sector:
    index: int
    edge_indices: List[int]
    weight: float
    probability: float


@dataclass
class SectorMassCertificate:
    phi1: float
    sector_weight_sum: float
    mass_error: float


@dataclass
class H1SectorDecomposition:
    sectors: List[H1Sector]
    certificate: SectorMassCertificate


class PhaseWitnessKind:
    OrientedCycleTransport = "OrientedCycleTransport"
    PathGroupoidRepresentation = "PathGroupoidRepresentation"
    UnitaryRepresentation = "UnitaryRepresentation"


@dataclass
class PhaseWitness:
    kind: str
    phases: List[float]


@dataclass
class H1Density:
    density: np.ndarray  
    sectors: H1SectorDecomposition
    phase_witness: Optional[PhaseWitness]


def edge_sector_decomposition(h1: List[float]) -> Optional[H1SectorDecomposition]:
    if not h1:
        return None
    if any(not np.isfinite(v) for v in h1):
        raise ValueError("h1 contains non-finite residual")

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
    n_nodes: int, edges: List[Tuple[int, int]], h1: List[float]
) -> Optional[H1SectorDecomposition]:
    if n_nodes == 0 or not h1:
        return None
    if len(edges) != len(h1):
        raise ValueError(f"h1 length {len(h1)} does not match edge count {len(edges)}")
    if any(not np.isfinite(v) for v in h1):
        raise ValueError("h1 contains non-finite residual")

    phi1 = sum(abs(v) for v in h1)
    if phi1 <= MASS_EPS:
        return None

    weights = [0.0] * n_nodes
    edge_indices: List[List[int]] = [[] for _ in range(n_nodes)]

    for edge_index, (u, v) in enumerate(edges):
        if u < 0 or v < 0 or u >= n_nodes or v >= n_nodes:
            raise ValueError(f"edge {edge_index} has endpoint outside node carrier")
        half_weight = 0.5 * abs(h1[edge_index])
        weights[u] += half_weight
        weights[v] += half_weight
        edge_indices[u].append(edge_index)
        edge_indices[v].append(edge_index)

    sectors = []
    for index, weight in enumerate(weights):
        sectors.append(
            H1Sector(
                index=index,
                edge_indices=list(edge_indices[index]),
                weight=weight,
                probability=weight / phi1,
            )
        )

    return _with_certificate(sectors, phi1)


def _with_certificate(sectors: List[H1Sector], phi1: float) -> H1SectorDecomposition:
    sector_weight_sum = sum(s.weight for s in sectors)
    cert = SectorMassCertificate(
        phi1=phi1,
        sector_weight_sum=sector_weight_sum,
        mass_error=abs(sector_weight_sum - phi1),
    )
    return H1SectorDecomposition(sectors=sectors, certificate=cert)


def rank_one_density_from_residual(h1: List[float]) -> Optional[np.ndarray]:
    """Constructs canonical minimal rank-one density from the residual vector.

    Returns None for empty / zero residual (no density). Raises ValueError on
    non-finite residual, consistent with the module convention.
    """
    if not h1 or all(abs(v) <= 1e-12 for v in h1):
        return None
    if any(not np.isfinite(v) for v in h1):
        raise ValueError("h1 contains non-finite residual")
    psi = np.array(h1, dtype=complex)
    psi /= np.linalg.norm(psi)
    return np.outer(psi, psi.conj())


def density_from_h1(h1: List[float]) -> Optional[H1Density]:
    """CANONICAL density construction. The ONLY density allowed for evaluator / Ξ."""
    density = rank_one_density_from_residual(h1)
    if density is None:
        return None
    sectors = edge_sector_decomposition(h1)
    if sectors is None:
        return None
    return H1Density(density=density, sectors=sectors, phase_witness=None)


def density_from_sectors_diagonal(sectors: H1SectorDecomposition) -> H1Density:
    """NON-CANONICAL."""
    if not sectors.sectors:
        raise ValueError("sector decomposition is empty")

    probs = [s.probability for s in sectors.sectors]
    if any(not np.isfinite(p) or p < 0.0 for p in probs):
        raise ValueError("sector decomposition contains non-finite or negative mass")
    if abs(sum(probs) - 1.0) > 1e-6:
        raise ValueError("sector probabilities do not sum to 1.0")

    density = np.diag(probs)
    return H1Density(density=density, sectors=sectors, phase_witness=None)


def diagonal_density_from_h1(h1: List[float]) -> Optional[H1Density]:
    """NON-CANONICAL."""
    sectors = edge_sector_decomposition(h1)
    if not sectors:
        return None
    return density_from_sectors_diagonal(sectors)


def density_from_sectors_with_phase(
    sectors: H1SectorDecomposition, witness: PhaseWitness
) -> H1Density:
    """Density reconstruction integrating phases."""
    if not sectors.sectors:
        raise ValueError("sector decomposition is empty")
    if len(witness.phases) != len(sectors.sectors):
        raise ValueError(
            f"phase witness length {len(witness.phases)} does not match sector count {len(sectors.sectors)}"
        )
    if any(not np.isfinite(p) for p in witness.phases):
        raise ValueError("phase witness contains non-finite phase")

    amplitudes = []
    for sector, phase in zip(sectors.sectors, witness.phases):
        amp = np.sqrt(sector.probability) * np.exp(1j * phase)
        amplitudes.append(amp)

    psi = np.array(amplitudes, dtype=complex)
    density = np.outer(psi, psi.conj())

    return H1Density(density=density, sectors=sectors, phase_witness=witness)


def density_from_h1_with_phase_witness(
    h1: List[float], witness: PhaseWitness
) -> Optional[H1Density]:
    sectors = edge_sector_decomposition(h1)
    if not sectors:
        return None
    return density_from_sectors_with_phase(sectors, witness)


def incidence_density_from_h1(
    n_nodes: int, edges: List[Tuple[int, int]], h1: List[float]
) -> Optional[H1Density]:
    sectors = incidence_sector_decomposition(n_nodes, edges, h1)
    if not sectors:
        return None
    return density_from_sectors_diagonal(sectors)


def density_for_carrier_dim(
    carrier_dim: int, n_nodes: int, edges: List[Tuple[int, int]], h1: List[float]
) -> Optional[H1Density]:
    if carrier_dim == n_nodes:
        return incidence_density_from_h1(n_nodes, edges, h1)
    if carrier_dim == len(h1):
        return density_from_h1(h1)
    raise ValueError(
        f"density carrier dimension {carrier_dim} matches neither node count {n_nodes} nor h1 length {len(h1)}"
    )


