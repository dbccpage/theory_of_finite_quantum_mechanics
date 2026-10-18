from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from omega_engine.crates.operator.projector.proj_symbol_game import RuntimeProblem, SolverManifest, SolverProposal
from omega_engine_pfp.domain.entities.candidate_artifact import CandidateArtifactV1
from omega_engine.crates.operator.projector.proj_symbol_game import ProjectionReceipt
from omega_engine.crates.carrier.cochain_carrier import CochainCarrier
from omega_engine.crates.state.cochain_state import CochainState
from omega_engine.crates.projection_obstruction.cochain_projector import CochainProjector, _network


@dataclass(frozen=True, slots=True)
class CodaCascadeProposalSolver:
    manifest: SolverManifest = SolverManifest(
        solver_id="existing-coda-cascade-proposal",
        families=("cochain_obstruction",),
    )

    def propose(
        self,
        problem: RuntimeProblem,
        packet_state: Any,
        projection: ProjectionReceipt,
    ) -> SolverProposal | None:
        if not isinstance(problem.projector, CochainProjector):
            return None
        if not isinstance(packet_state, CochainState):
            return None
        from omega_engine.crates.solver.solv_omega_engine_solver_of_solvers.solv_oesos import (
            CascadeSolver,
        )
        network = _network(problem.projector.carrier)
        solver = CascadeSolver(network, observer_name=self.manifest.solver_id)
        receipt = solver.solve(packet_state.as_mapping(), max_lifts=0)
        if receipt.is_solved():
            candidate_state = CochainState.from_mapping(
                {edge: 0.0 for edge in packet_state.as_mapping()}
            )
        else:
            candidate_state = CochainState.from_mapping(
                solver.dda_engine.current_edge_values
            )
        candidate = CandidateArtifactV1(
            packet_id=problem.envelope.packet_id,
            producer_id=self.manifest.solver_id,
            payload=candidate_state,
            witness="existing-cascade-output-requires-independent-reprojection",
            claimed_terminal=receipt.terminal_status,
            claimed_valid=receipt.is_solved(),
            metadata={
                "stages_executed": tuple(receipt.stages_executed),
                "initial_residual_size": receipt.initial_residual_size,
                "final_residual_size": receipt.final_residual_size,
                "final_residual_triple": receipt.final_residual_triple,
                "algebraic_class_id": receipt.algebraic_class_id,
                "admitted_complex_verified": receipt.admitted_complex_verified,
                "upstream_authority_effect": receipt.authority_effect,
            },
        )
        return SolverProposal(
            state=candidate_state,
            candidate=candidate,
            next_carrier_id=problem.adapter.target_carrier_id,
        )
