"""Focused replay tests for the conditional GTLA -> GTQ ascent."""

from copy import deepcopy
from dataclasses import replace

import numpy as np
import pytest

from omega_engine.crates.quantum_physics.gtq_ascent import (
    FiniteShadowSystem,
    ResidualAccount,
    ResidualClosurePacket,
    declared_m2_packet,
    replay_gtfoc_origin,
    replay_packet_relative_survival,
    replay_tower_walk_validator,
    run_gtq_ascent_replay,
)
from omega_engine.crates.quantum_physics.gtq_ascent import run_interface_registry_audit


def test_gtfoc_origin_replays_exact_repair_and_positive_quotient_mass() -> None:
    origin = replay_gtfoc_origin()

    assert origin["complex"]["d1_d0_zero"] is True
    assert origin["exact_repair_example"]["d0_alpha"] == ["2", "-2", "0"]
    assert origin["quotient_survivor"]["closure_defect"] == ["0"]
    assert origin["quotient_survivor"]["phi_1"] == "1"
    assert origin["quotient_survivor"]["positive_residual"] is True


def test_o022a_replays_finite_cofiber_to_banach_quotient_bridge() -> None:
    bridge = run_gtq_ascent_replay()["cofiber_banach_bridge"]

    assert bridge["result_id"] == "O022a"
    assert bridge["status"] == "proved_for_declared_finite_repair_specialization"
    assert bridge["finite_repair_specialization"]["ambient_category"] == "Arr(FinBan_R)"
    assert bridge["witness"]["phi_1"] == "1"
    assert bridge["witness"]["quotient_norm"] == "1"
    assert bridge["bridge_identity"]["replayed"] is True


def test_o022a_refuses_scalar_object_and_unrestricted_gtta_identifications() -> None:
    bridge = run_gtq_ascent_replay()["cofiber_banach_bridge"]
    refusals = {row["claim"]: row for row in bridge["refusals"]}

    assert refusals["Phi_1 = R_Lambda"]["status"] == "refused"
    unrestricted = next(
        row
        for row in bridge["refusals"]
        if "unrestricted CODA-A closure units" in row["claim"]
    )
    assert unrestricted["status"] == "refused_without_declared_realization_functor"


def test_gtq_ascent_replays_all_six_quantum_layers_without_authority_promotion() -> (
    None
):
    replay = run_gtq_ascent_replay()
    omega_q = replay["omega_Q"]

    assert replay["tower_path"] == [
        "CODA-FOC",
        "CODA-FDA",
        "CODA-MUR",
        "CODA-OR",
        "CODA-CS",
        "CODA-A",
    ]
    assert replay["pivot"]["claim_status"] == "conditional_realization_interface_lift"
    assert replay["pivot"]["declared_faithful_comparison"]["phi_1"] == "1"
    assert omega_q["CODA-FOC-Q"]["d_Q_1_d_Q_0_zero"] is True
    assert omega_q["CODA-FDA-Q"]["terminal"] == "ExactQuantumReplay"
    assert omega_q["CODA-FDA-Q"]["authority_minted"] is False
    assert omega_q["CODA-MUR-Q"]["passed"] is True
    assert omega_q["CODA-OR-Q"]["passed"] is True
    assert (
        omega_q["CODA-CS-Q"]["continuum_attempt"]["terminal"]
        == "OracleNeeded(Convergence)"
    )
    assert omega_q["CODA-A-Q"]["contextual_residual"]["terminal"] == "ClosedResidual_Q"
    assert replay["epistemic_firewall"]["status"] == "conditional_realization_spine"


def test_o020_emits_machine_checkable_transition_status_ledger() -> None:
    replay = run_gtq_ascent_replay()
    validator = replay["tower_walk_validator"]
    records = {
        record["transition_id"]: record for record in validator["transition_records"]
    }

    assert validator["result_id"] == "O020"
    assert validator["validator"] == "TowerWalkValidator"
    assert validator["ledger_valid"] is True
    assert validator["forced_lift_proved"] is True
    assert validator["minimal_interface_proved"] is True
    assert validator["forced_lift_scope"] == "declared_registry_only"
    assert records["O020-T01"]["status"] == "Derived"
    assert records["O020-T02"]["status"] == "Imported/Declared"
    assert records["O020-T02"]["passed"] is True
    assert records["O020-T03"]["status"] == "Refused"
    assert records["O020-T03"]["reason"] == "obstruction alone does not license lift"
    assert records["O020-T04"]["status"] == "Conditional"
    assert records["O020-T04"]["requirements"]["minimal_interface"] is True
    assert records["O020-T05"]["status"] == "Conditional/Imported"
    assert records["O020-T06"]["status"] == "Refused"


def test_o020_refuses_ledger_when_required_transport_replay_fails() -> None:
    replay = run_gtq_ascent_replay()
    omega_q = deepcopy(replay["omega_Q"])
    omega_q["CODA-MUR-Q"]["passed"] = False

    with pytest.raises(ValueError, match="authority firewall"):
        replay_tower_walk_validator(replay["origin"], replay["pivot"], omega_q)


def test_o020_without_o022_registry_evidence_remains_conditional() -> None:
    replay = run_gtq_ascent_replay()

    validator = replay_tower_walk_validator(
        replay["origin"], replay["pivot"], replay["omega_Q"]
    )
    forced_lift = next(
        record
        for record in validator["transition_records"]
        if record["transition_id"] == "O020-T04"
    )

    assert validator["ledger_valid"] is True
    assert validator["forced_lift_proved"] is False
    assert validator["minimal_interface_proved"] is False
    assert validator["forced_lift_scope"] == "not_yet_proved"
    assert forced_lift["requirements"]["minimal_interface"] is False


def test_o022_registry_relative_minimal_interface_audit_closes_declared_registry() -> (
    None
):
    replay = run_gtq_ascent_replay()
    audit = replay["interface_registry_audit"]
    rows = {row["candidate_id"]: row for row in audit["declared_registry"]}

    assert audit["result_id"] == "O022"
    assert audit["audit"] == "RegistryRelativeMinimalInterfaceAudit"
    assert audit["status"] == "proved_relative_to_declared_registry"
    assert audit["minimal_interface_proved"] is True
    assert audit["forced_lift_scope"] == "declared_registry_only"
    assert audit["universal_uniqueness_proved"] is False
    assert audit["origin_derived"] is False
    assert set(rows) == {
        "scalar_l1_packet",
        "rotational_l1_l2_packet",
        "classical_contextual_gluing_packet",
        "gpt_convex_packet",
        "real_hilbert_rebit_packet",
        "quaternionic_guarded_packet",
        "complex_hilbert_cptp_packet",
    }
    assert rows["scalar_l1_packet"]["resolution_status"] == "fails"
    assert rows["rotational_l1_l2_packet"]["resolution_status"] == "fails"
    assert rows["classical_contextual_gluing_packet"]["resolution_status"] == "fails"
    assert rows["gpt_convex_packet"]["resolution_status"] == "refused"
    assert rows["real_hilbert_rebit_packet"]["resolution_status"] == "fails"
    assert rows["quaternionic_guarded_packet"]["resolution_status"] == "refused"
    assert rows["complex_hilbert_cptp_packet"]["resolution_status"] == "resolves"
    assert rows["complex_hilbert_cptp_packet"]["import_status"] == "imported"


def test_o022_refuses_registry_closure_when_complex_transport_replay_fails() -> None:
    replay = run_gtq_ascent_replay()
    omega_q = deepcopy(replay["omega_Q"])
    omega_q["CODA-MUR-Q"]["passed"] = False

    with pytest.raises(ValueError, match="did not close"):
        run_interface_registry_audit(replay["origin"], replay["pivot"], omega_q)


def test_o021_replays_packet_relative_survival_without_deriving_origin() -> None:
    replay = run_gtq_ascent_replay()
    survival = replay["survival_audit"]

    assert survival["result_id"] == "O021"
    assert survival["terminal"] == "PacketRelativeSurvivalReplay"
    assert survival["local_replay_passed"] is True
    assert all(survival["checks"].values())
    assert survival["imports_preserved"] is True
    assert survival["origin_derived"] is False
    assert survival["full_survives_descent_claim"] is False
    assert survival["external_sealed_pi_sharp_supplied"] is False
    assert survival["comparative_survival_ledger_supplied"] is False


def test_o021_refuses_packet_relative_survival_when_transport_replay_fails() -> None:
    replay = run_gtq_ascent_replay()
    omega_q = deepcopy(replay["omega_Q"])
    omega_q["CODA-MUR-Q"]["passed"] = False

    survival = replay_packet_relative_survival(
        replay["origin"], replay["pivot"], omega_q
    )

    assert survival["terminal"] == "RefusedDescentSurvivalReplay"
    assert survival["local_replay_passed"] is False
    assert survival["checks"]["certified_context_transport"] is False


def test_gtfda_q_refuses_an_incomplete_quantum_packet() -> None:
    packet = replace(declared_m2_packet(), povms={})
    terminal = packet.terminalize()

    assert terminal["status"] == "refused"
    assert terminal["terminal"] == "RefusedQuantumPacket"
    assert terminal["checks"]["povms_declared"] is False


def test_gttc_q_continuum_claim_requires_a_convergence_witness() -> None:
    shadows = FiniteShadowSystem(
        shadows=("K1", "K2"),
        refinements=(("K1", "K2"),),
        topology="finite_matrix_norm_topology",
        cofinal_for_query=True,
        error_budget=0.0,
    )

    assert (
        shadows.terminalize(require_continuum=False)["terminal"] == "FiniteShadowReplay"
    )
    assert (
        shadows.terminalize(require_continuum=True)["terminal"]
        == "OracleNeeded(Convergence)"
    )


def test_gtta_q_refuses_duplicate_residual_accounting() -> None:
    packet = ResidualClosurePacket(
        residuals=(
            ResidualAccount("same_component", "ClosedResidual"),
            ResidualAccount("same_component", "RaisedResidual"),
        )
    )

    with pytest.raises(ValueError, match="exactly once"):
        packet.terminalize()


def test_gtfda_q_checks_trace_preservation_of_declared_kraus_channels() -> None:
    packet = declared_m2_packet()
    bad_channel = (2.0 * np.eye(2, dtype=complex),)
    terminal = replace(
        packet, channels={**packet.channels, "bad": bad_channel}
    ).terminalize()

    assert terminal["terminal"] == "RefusedQuantumPacket"
    assert terminal["checks"]["channels_cp_by_kraus_declaration"] is True
    assert terminal["checks"]["channels_trace_preserving"] is False


def test_gtfda_q_refuses_a_malformed_kraus_operator_shape() -> None:
    packet = declared_m2_packet()
    malformed_channel = (np.eye(3, dtype=complex),)
    terminal = replace(
        packet, channels={**packet.channels, "malformed": malformed_channel}
    ).terminalize()

    assert terminal["terminal"] == "RefusedQuantumPacket"
    assert terminal["checks"]["channels_cp_by_kraus_declaration"] is False
    assert terminal["checks"]["channels_trace_preserving"] is False


