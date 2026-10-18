from __future__ import annotations

import math
from dataclasses import dataclass
from typing import Any

from omega_engine_pfp.domain.shared_kernel.canonical import domain_digest, freeze
from omega_engine.crates.operator.projector.proj_symbol_game import Obstruction, ProjectionReceipt
from omega_engine_pfp.domain.entities.packet_envelope import PacketEnvelopeV2
from omega_engine.crates.carrier.cochain_carrier import CochainCarrier
from omega_engine.crates.state.cochain_state import CochainState
from omega_engine.crates.adapter.cochain_network_adapter import carrier_to_network as _network
from omega_engine.crates.functional.cochain_functional import evaluate_cochain_residuals


@dataclass(frozen=True, slots=True)
class CochainProjector:
    carrier: CochainCarrier
    tolerance: float = 1.0e-8
    projector_id: str = "coda-face-aware-phi1-gamma2-projector-v1"
    research_parent_event_id: str | None = None

    @property
    def config_digest(self) -> str:
        config = {
            "projector_id": self.projector_id,
            "carrier": self.carrier,
            "tolerance": self.tolerance,
        }
        if self.research_parent_event_id is not None:
            config["research_parent_event_id"] = self.research_parent_event_id
        return domain_digest(
            "omega.oesos.projector-config.v1",
            config,
        )

    def meaning(self, state: Any) -> Any:
        if not isinstance(state, CochainState):
            raise TypeError("cochain projector requires CochainState")
        if set(state.as_mapping()) != set(self.carrier.edges):
            raise ValueError("cochain support must equal the declared carrier edges")
        return state

    def skeleton(self, state: Any) -> Any:
        self.meaning(state)
        return self.carrier

    def validate_packet(
        self,
        envelope: PacketEnvelopeV2,
        native_initial_state: Any,
    ) -> bool:
        if not isinstance(native_initial_state, CochainState):
            return False
        self.meaning(native_initial_state)
        expected_payload = {
            "carrier": self.carrier,
            "omega": native_initial_state.values,
            "canonical_rust_owner": "omega_solvers::solver_of_solvers",
        }
        if self.research_parent_event_id is not None:
            expected_payload["research_parent_event_id"] = self.research_parent_event_id
        expected_constraints = (
            "d1*d0=0",
            "finite exact carrier",
            "separate phi1 from gamma2",
        )
        return (
            envelope.carrier_id == "finite-cochain-2-v1"
            and envelope.parent_event_id == self.research_parent_event_id
            and envelope.constraints == expected_constraints
            and envelope.payload == freeze(expected_payload)
            and envelope.source_digest
            == domain_digest("omega.oesos.coda-fixture.v1", expected_payload)
        )

    def project(self, state: Any) -> ProjectionReceipt:
        self.meaning(state)
        phi1, gamma2, phi_result = evaluate_cochain_residuals(self.carrier, state)
        obstructions: list[Obstruction] = []
        if phi1 > self.tolerance:
            obstructions.append(
                Obstruction(
                    obstruction_id="cochain:phi1",
                    magnitude=phi1,
                    witness="l1 quotient residual after exact gauge replay",
                    closure_failure=False,
                )
            )
        if gamma2 > self.tolerance:
            obstructions.append(
                Obstruction(
                    obstruction_id="cochain:gamma2",
                    magnitude=gamma2,
                    witness="l1 face coboundary after exact boundary replay",
                    closure_failure=True,
                )
            )
        return ProjectionReceipt(
            projector_id=self.projector_id,
            state_hash=domain_digest("omega.oesos.state.v1", state),
            obstructions=tuple(obstructions),
            witness="coda-face-aware-phi1-gamma2-independent-replay-v1",
            representative_l1_mass=state.raw_l1_mass,
            authority_effect="None",
        )

    def verify_retraction(
        self,
        solver_id: str,
        before_state: Any,
        after_state: Any,
    ) -> bool:
        if solver_id not in {
            "coda-face-aware-phi1-gamma2-cascade-solver-v1",
            "existing-coda-cascade-proposal",
        }:
            return False
        before = self.meaning(before_state)
        after = self.meaning(after_state)
        if before == after:
            return False
        before_skeleton = self.skeleton(before)
        after_skeleton = self.skeleton(after)
        after_projection = self.project(after)
        return (
            before_skeleton == after_skeleton
            and after_projection.is_exact
        )
