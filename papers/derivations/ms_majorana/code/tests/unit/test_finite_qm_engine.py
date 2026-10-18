from __future__ import annotations

import numpy as np
import pytest

from omega_engine.crates.quantum_physics.finite_qm_engine import (
    FiniteQMEngine,
    evaluate_6rung_ladder,
)
from omega_engine.crates.pipeline.import_ledger import (
    QM_121_TO_QM_211,
    RecoveryImportSlot,
    generate_b8_countermodels,
    verify_drop_one_necessity,
)
from omega_engine.crates.pipeline.paper_registry import PAPERS, run as run_paper


def test_rung_1_born_redundancy():
    weights = np.array([2.0, 6.0])
    amplitudes = np.array([np.sqrt(2.0), np.sqrt(6.0)])
    r1 = FiniteQMEngine.rung_1_born_redundancy(weights, amplitudes)

    assert np.allclose(r1.probabilities, [0.25, 0.75])
    assert r1.redundancy_verified is True
    assert np.allclose(r1.amplitude_probabilities, [0.25, 0.75])


def test_rung_2_density_purity():
    weights = np.array([1.0, 3.0])
    r2 = FiniteQMEngine.rung_2_density_purity(weights)

    assert r2.trace == pytest.approx(1.0)
    assert r2.is_psd is True
    assert r2.purity == pytest.approx(0.0625 + 0.5625)
    assert r2.off_diagonal_mass == 0.0


def test_rung_3_cptp_shadow():
    p = 0.1
    K0 = np.sqrt(1 - p) * np.eye(2)
    K1 = np.sqrt(p) * np.array([[0, 1], [1, 0]])
    r3 = FiniteQMEngine.rung_3_cptp_shadow([K0, K1])

    assert r3.trace_preserving is True
    assert r3.is_column_stochastic is True
    assert np.allclose(r3.stochastic_kernel, [[1 - p, p], [p, 1 - p]])


def test_rung_4_path_sum():
    M = np.array([[0.8, 0.2], [0.1, 0.9]])
    r4 = FiniteQMEngine.rung_4_path_sum(M, steps=4)

    assert r4.chapman_kolmogorov_holds is True
    assert np.allclose(r4.power_matrix, np.linalg.matrix_power(M, 4))


def test_rung_5_superposition_fiber():
    amps = np.array([1.0 + 0j, 0.0 + 1j, 1.0 + 1j])
    r5 = FiniteQMEngine.rung_5_superposition_fiber(amps)

    assert r5.nonzero_support_size == 3
    assert r5.fiber_dimension == 2
    assert r5.relative_phase_visible is True


def test_rung_6_interference_cross_term():
    amps_const = np.array([1.0, 1.0])
    r6 = FiniteQMEngine.rung_6_interference_cross_term(amps_const)

    assert r6.l1_sum == 2.0
    assert r6.l2_interfered_mass == 4.0
    assert r6.cross_term == 2.0
    assert r6.is_non_l1_computable is True


def test_evaluate_6rung_ladder_integration():
    weights = np.array([1.0, 1.0])
    amplitudes = np.array([1.0 + 0j, 1.0 + 0j])
    K0 = np.eye(2)
    step_matrix = np.array([[0.5, 0.5], [0.5, 0.5]])

    ladder_res = evaluate_6rung_ladder(weights, amplitudes, [K0], step_matrix, steps=2)

    assert ladder_res["authority_effect"] == "None"
    assert "nonclaim_box" in ladder_res
    assert ladder_res["rung_1_born"]["redundancy_verified"] is True
    assert ladder_res["rung_2_density"]["is_psd"] is True
    assert ladder_res["rung_6_interference"]["cross_term"] == pytest.approx(2.0)


def test_b8_countermodels_and_crosswalk():
    cms = generate_b8_countermodels()
    assert len(cms) == 8

    res = verify_drop_one_necessity()
    assert res["all_drop_one_break_recovery"] is True
    assert res["status"] == "DROP_ONE_NECESSITY_VERIFIED"
    assert res["qm_121_to_qm_211_crosswalk"]["all_8_slots_mapped"] is True

    mapped_slots = set()
    for slots in QM_121_TO_QM_211.values():
        mapped_slots.update(slots)
    assert mapped_slots == set(RecoveryImportSlot)


def test_paper_registry_qm_000_to_qm_010():
    qm_papers = [
        "qm_000_primitive_difference_for_quantum_carriers",
        "qm_001_tower_walk_registry_relative_interface_lift",
        "qm_002_cofiber_to_banach_quotient_bridge",
        "qm_003_residual_density_calculus_l1_l2_boundary",
        "qm_004_general_obstruction_management_calculus",
        "qm_005_finite_quantum_packet_theorem_m2",
        "qm_006_quantum_realization_requires_finite_descent",
        "qm_007_quantum_realization_spine",
        "qm_008_finite_descent_to_coda_foc_projection",
        "qm_009_continuum_shadow_non_promotion",
        "qm_009_interpretations_as_authority_shadows",
        "qm_010_hilbert_space_cochains_qm_cohomology",
    ]

    for p_id in qm_papers:
        p_entry = next((p for p in PAPERS if p["paper_id"] == p_id), None)
        assert p_entry is not None, f"Paper {p_id} missing from registry"

        eval_res = run_paper(p_entry["module"])
        assert "math_objects" in eval_res or "residual_metrics" in eval_res or "skeleton" in eval_res


