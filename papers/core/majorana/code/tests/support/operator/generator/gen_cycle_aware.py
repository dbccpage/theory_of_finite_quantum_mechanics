import math

from omega_engine.crates.operator.generator.gen_obstruction import CandidateGenerator
from omega_engine.crates.type.obstruction_runtime import Candidate
from omega_engine.crates.functional.fn_xi_witness import XiDiagnosticFunctional, validate_xi_diagnostic
from omega_engine.crates.operator.lambda_op.lamb_cycle_correction import apply_correction
from omega_engine.crates.type.cycle_aware import CorrectionStrategy, CycleAwareConfig


class CycleCorrectableState:
    def edge_values(self) -> list:
        raise NotImplementedError

    def edges(self) -> list:
        raise NotImplementedError

    def node_count(self) -> int:
        raise NotImplementedError

    def with_corrected_edges(self, corrected: list):
        raise NotImplementedError

    def validate_cycle_correctable(self) -> bool:
        return (
            len(self.edge_values()) == len(self.edges())
            and all(
                u < self.node_count() and v < self.node_count() for u, v in self.edges()
            )
            and all(math.isfinite(x) for x in self.edge_values())
        )


class CycleAwareGenerator(CandidateGenerator):
    def __init__(self, config: CycleAwareConfig, diagnostic: XiDiagnosticFunctional):
        self.config = config
        self.diagnostic = diagnostic

    def generate(self, state) -> list:
        try:
            if not 0.0 <= self.config.xi_activation_threshold <= 1.0:
                raise ValueError("xi_activation_threshold must be in [0,1]")
            if not CorrectionStrategy.is_valid(self.config.strategy):
                raise ValueError("invalid correction strategy")
        except ValueError:
            return []

        if (
            not hasattr(state, "validate_cycle_correctable")
            or not state.validate_cycle_correctable()
        ):
            return []

        try:
            diag = self.diagnostic.diagnose(state)
        except Exception:
            return []

        if not validate_xi_diagnostic(diag, len(state.edge_values())):
            return []

        if diag.xi_value >= self.config.xi_activation_threshold:
            return []

        witness = diag.witness
        if not witness.worst_edges:
            return []

        worst_edges = witness.worst_edges[: self.config.top_k_edges]
        if not worst_edges:
            return []

        candidates = []

        corrected_all = apply_correction(
            state.edge_values(),
            diag.harmonic_projection,
            worst_edges,
            self.config.strategy,
        )
        candidates.append(
            Candidate.new(
                state.with_corrected_edges(corrected_all),
                "cycle_aware.bulk_correction",
                f"corrects {len(worst_edges)} worst edges (max_distortion={witness.max_distortion():.4f}, xi={diag.xi_value:.4f})",
            )
        )

        for edge_idx in worst_edges:
            corrected_single = apply_correction(
                state.edge_values(),
                diag.harmonic_projection,
                [edge_idx],
                self.config.strategy,
            )
            candidates.append(
                Candidate.new(
                    state.with_corrected_edges(corrected_single),
                    "cycle_aware.single_edge",
                    f"corrects edge {edge_idx} (distortion={witness.edge_distortions[edge_idx]:.4f})",
                )
            )

        return candidates
