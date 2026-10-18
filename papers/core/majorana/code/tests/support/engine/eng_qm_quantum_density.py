"""Density construction engine.

Faithful port of ``crates/omega_engine.crates.engine/src/quantum/quantum_density_engine.rs``.

Reuses :class:`omega_linear_algebra.density.NumericalDensityMatrix` for all
density-matrix math (purity / entropy / coherence). This module only adds the
construction-report layer and the from-states mixture builder.
"""

from __future__ import annotations
import math
from typing import List, Optional, Tuple, TYPE_CHECKING

CONTRACT_ID = "urn:omega:qm:quantum_density_engine:file:v1.0.0"
AUTHORITY_EFFECT = "None"

if TYPE_CHECKING:
    from omega_engine.crates.type.qm_density import BranchResidualCandidate, GomcDiagnosticConfig, ResidualDensityReport
    from omega_engine.crates.type.qm_engine import ReasoningDensityConfig

import numpy as np

from omega_engine.crates.linear_algebra_theory.density import (
    DensityMatrixConfig,
    NumericalDensityMatrix,
    NoValidStates,
)
from omega_engine.crates.type.qm_engine import DensityConstruction, DensityConstructionReport


from omega_engine.crates.engine.base.eng_base import Engine


class QuantumDensityEngine(Engine):
    @staticmethod
    def generate_report(
        dm: NumericalDensityMatrix,
        construction: DensityConstruction,
        source_count: int,
        top_k: Optional[int],
    ) -> DensityConstructionReport:
        try:
            entropy = dm.von_neumann_entropy()
        except Exception:
            entropy = 0.0
        return DensityConstructionReport(
            construction=construction,
            rank=dm.dim(),
            entropy=entropy,
            purity=dm.purity(),
            source_count=source_count,
            top_k=top_k,
        )

    @staticmethod
    def from_states(states: List[List[float]]) -> Optional[NumericalDensityMatrix]:
        try:
            dm, _ = QuantumDensityEngine.from_states_checked(
                states, DensityMatrixConfig.default()
            )
            return dm
        except Exception:
            return None

    @staticmethod
    def from_states_typed(
        states: List[List[float]], config: Optional[DensityMatrixConfig] = None
    ) -> Tuple[NumericalDensityMatrix, DensityConstructionReport]:
        cfg = config or DensityMatrixConfig.default()
        try:
            return QuantumDensityEngine.from_states_checked(states, cfg)
        except Exception as e:
            from omega_engine.crates.operator.boundaries.ctor_qm_density_from_h1 import DensityConstructionRefused

            raise DensityConstructionRefused(f"DENSITY_CONSTRUCTION_REFUSED: {e}")

    @staticmethod
    def from_states_checked(states: List[List[float]], config: DensityMatrixConfig):
        if not states:
            raise NoValidStates("no valid states")

        components = []
        valid_count = 0.0
        for s in states:
            norm_sq = sum(x * x for x in s)
            if norm_sq >= config.zero_norm_tol():
                psi = [complex(x / math.sqrt(norm_sq), 0.0) for x in s]
                rho = NumericalDensityMatrix.from_amplitudes(psi, config)
                components.append([rho, 1.0])
                valid_count += 1.0

        if valid_count < 1.0:
            raise NoValidStates("no valid states")

        for c in components:
            c[1] /= valid_count

        dm = NumericalDensityMatrix.try_mixture(
            [(c[0], c[1]) for c in components], config
        )
        report = QuantumDensityEngine.generate_report(
            dm, DensityConstruction.PureOuterProduct, len(states), None
        )
        return dm, report

    @staticmethod
    def purity(dm: NumericalDensityMatrix) -> float:
        return dm.purity()

    @staticmethod
    def von_neumann_entropy(dm: NumericalDensityMatrix) -> float:
        try:
            return dm.von_neumann_entropy()
        except Exception:
            return 0.0

    @staticmethod
    def l1_coherence(dm: NumericalDensityMatrix) -> float:
        return dm.l1_coherence()

    @staticmethod
    def hs_fidelity(a: NumericalDensityMatrix, b: NumericalDensityMatrix) -> float:
        if a.dim() != b.dim():
            return 0.0
        prod = a.rho() @ b.rho()
        val = np.trace(prod).real
        return float(min(max(val, 0.0), 1.0))

    @staticmethod
    def maximally_mixed(dim: int) -> NumericalDensityMatrix:
        return NumericalDensityMatrix.try_maximally_mixed(dim)

    @staticmethod
    def sequence_ensemble_density(
        rows: List[List[float]],
        weights: Optional[List[float]],
        config: "ReasoningDensityConfig",
        density_config: DensityMatrixConfig,
    ):
        from omega_engine.crates.engine.eng_qm_reasoning_density import sequence_ensemble_density

        return sequence_ensemble_density(rows, weights, config, density_config)

    @staticmethod
    def window_density_trajectory(
        rows: List[List[float]],
        window_size: int,
        stride: int,
        config: "ReasoningDensityConfig",
        density_config: DensityMatrixConfig,
    ):
        from omega_engine.crates.engine.eng_qm_reasoning_density import window_density_trajectory

        return window_density_trajectory(
            rows, window_size, stride, config, density_config
        )

    @staticmethod
    def edge_residual_density_report(h1: List[float]):
        from omega_engine.crates.operator.transforms.trans_qm_residual_density import edge_residual_density_report

        return edge_residual_density_report(h1)

    @staticmethod
    def incidence_residual_density_report(
        n_nodes: int,
        edges: List[Tuple[int, int]],
        h1: List[float],
    ):
        from omega_engine.crates.operator.transforms.trans_qm_residual_density import incidence_residual_density_report

        return incidence_residual_density_report(n_nodes, edges, h1)

    @staticmethod
    def coarse_grain_residual_density_report(
        report: "ResidualDensityReport",
        labels: List[int],
    ):
        from omega_engine.crates.operator.transforms.trans_qm_residual_density import coarse_grain_residual_density_report

        return coarse_grain_residual_density_report(report, labels)

    @staticmethod
    def branch_residual_search_report(candidates: List["BranchResidualCandidate"]):
        from omega_engine.crates.operator.transforms.trans_qm_residual_density import branch_residual_search_report

        return branch_residual_search_report(candidates)

    @staticmethod
    def residual_channel_pushforward_report(
        report: "ResidualDensityReport",
        transition: List[List[float]],
    ):
        from omega_engine.crates.operator.transforms.trans_qm_residual_density import residual_channel_pushforward_report

        return residual_channel_pushforward_report(report, transition)

    @staticmethod
    def edge_gomc_diagnostic_report(h1: List[float], config: "GomcDiagnosticConfig"):
        from omega_engine.crates.diagnostic.diag_qm_gomc import edge_gomc_diagnostic_report

        return edge_gomc_diagnostic_report(h1, config)

    @staticmethod
    def incidence_gomc_diagnostic_report(
        n_nodes: int,
        edges: List[Tuple[int, int]],
        h1: List[float],
        config: "GomcDiagnosticConfig",
    ):
        from omega_engine.crates.diagnostic.diag_qm_gomc import incidence_gomc_diagnostic_report

        return incidence_gomc_diagnostic_report(n_nodes, edges, h1, config)




