"""Tests of retained finite calculations and declared fixtures.
Physical recovery and removed certificate wrappers are outside this test scope.
"""

import math
import subprocess
import sys
from pathlib import Path

import pytest

current_dir = Path(__file__).resolve().parent
if str(current_dir) not in sys.path:
    sys.path.insert(0, str(current_dir))

from regge_wdw_evaluator import ReggeWdwEvaluator



def test_lean4_regge_wdw_core_compilation():
    """Validates that lean4/regge_wdw_core.lean elaborates cleanly with zero errors."""
    lean_file = current_dir.parent / "lean4" / "regge_wdw_core.lean"
    assert lean_file.exists(), f"Missing Lean 4 core file: {lean_file}"
    res = subprocess.run(["lean", str(lean_file)], capture_output=True, text=True)
    assert res.returncode == 0, f"Lean compilation error:\n{res.stderr}"




def test_cayley_menger_regular_tetrahedron():
    """Validates Cayley-Menger metric determinant and RCNF satisfaction on a regular tetrahedron."""
    evaluator = ReggeWdwEvaluator(in_memory=True)
    receipt = evaluator.evaluate_regular_tetrahedron(edge_length=1.0)
    assert receipt.satisfies_rcnf is True
    assert receipt.num_vertices == 4
    assert receipt.num_edges == 6
    assert receipt.num_tetrahedra == 1
    # Analytical volume: 1 / (6 * sqrt(2)) ~ 0.117851
    expected_vol = 1.0 / (6.0 * math.sqrt(2.0))
    assert abs(receipt.total_volume - expected_vol) < 1e-9
    # Dihedral angle for regular tetrahedron is arccos(1/3) ~ 1.230959 rad
    for d in receipt.deficits:
        assert abs(d.dihedral_angles[0] - math.acos(1.0 / 3.0)) < 1e-9
    evaluator.close()


def test_triangulated_3sphere_regge_deficits():
    """Validates Regge deficit angles on a closed 3-sphere (boundary of a 4-simplex)."""
    evaluator = ReggeWdwEvaluator(in_memory=True)
    receipt = evaluator.evaluate_triangulated_3sphere_boundary_4simplex(edge_length=2.0)
    assert receipt.satisfies_rcnf is True
    assert receipt.num_vertices == 5
    assert receipt.num_edges == 10
    assert receipt.num_tetrahedra == 5
    # Deficit angle at each edge: 2pi - 3*arccos(1/3) ~ 2.5937 rad
    expected_deficit = 2.0 * math.pi - 3.0 * math.acos(1.0 / 3.0)
    for d in receipt.deficits:
        assert abs(d.deficit_angle - expected_deficit) < 1e-9
        assert d.regge_action_contribution > 0.0
    assert receipt.total_regge_action > 0.0
    evaluator.close()


def test_schlafli_identity_vanishing():
    """Validates the discrete Schläfli variation identity sum(l_h * d_epsilon_h) = 0."""
    evaluator = ReggeWdwEvaluator(in_memory=True)
    evaluator.evaluate_triangulated_3sphere_boundary_4simplex(edge_length=1.0)
    residual = evaluator.verify_schlafli_identity(base_length=1.0, perturbation=1e-4)
    assert residual < 1e-9, f"Schlafli identity violated with residual {residual}"
    evaluator.close()


def test_bqnf_pachner_local_gauge_repair():
    """Validates BQNF incremental repair routing under local diffeomorphism / gauge deformation."""
    evaluator = ReggeWdwEvaluator(in_memory=True)
    receipt = evaluator.route_pachner_event(
        pachner_type="metric_deformation",
        affected_hinge=3,
        prior_deficit=2.5937,
        new_deficit=2.5950,
        is_gauge_invariant=True,
    )
    assert receipt.disposition == "Repair"
    assert receipt.is_exact_repaired is True
    assert receipt.repair_potential is not None
    assert abs(receipt.repair_potential - (-0.0013)) < 1e-6
    evaluator.close()


def test_bqnf_global_curvature_recompute():
    """Validates BQNF routing to bounded recompute when topological class changes."""
    evaluator = ReggeWdwEvaluator(in_memory=True)
    receipt = evaluator.route_pachner_event(
        pachner_type="2_to_3",
        affected_hinge=0,
        prior_deficit=2.5937,
        new_deficit=1.8210,
        is_gauge_invariant=False,
    )
    assert receipt.disposition == "Recompute"
    assert receipt.is_exact_repaired is False
    assert receipt.repair_potential is None
    evaluator.close()


def test_wdw_normal_form_certification_2state():
    """Validates WDWNF certification on a symmetric 2-state quantum geometric transfer matrix."""
    evaluator = ReggeWdwEvaluator(in_memory=True)
    T = [
        [0.8, 0.2],
        [0.2, 0.8],
    ]
    contract = evaluator.evaluate_finite_history(
        contract_id="WDWNF-2STATE-MINISUPERSPACE",
        system_transfer_matrix=T,
        num_clock_states=4,
    )
    assert contract.is_recurrence_satisfied is True
    assert contract.recurrence_residual_norm < 1e-9
    assert contract.is_relational_conditioned_exact is True
    assert contract.max_sql_residual < 1e-9
    assert contract.clock_marginal_entropy > 0.0
    assert contract.has_valid_history is True
    evaluator.close()


def test_wdw_normal_form_certification_4state():
    """Validates WDWNF certification on a 4-state simplicial volume transfer operator."""
    evaluator = ReggeWdwEvaluator(in_memory=True)
    T = [
        [0.7, 0.1, 0.1, 0.1],
        [0.1, 0.7, 0.1, 0.1],
        [0.1, 0.1, 0.7, 0.1],
        [0.1, 0.1, 0.1, 0.7],
    ]
    contract = evaluator.evaluate_finite_history(
        contract_id="WDWNF-4STATE-FLRW-VOLUME",
        system_transfer_matrix=T,
        num_clock_states=6,
    )
    assert contract.clock_dimension == 6
    assert contract.system_dimension == 4
    assert contract.is_recurrence_satisfied is True
    assert contract.has_valid_history is True
    evaluator.close()


def test_clock_marginal_entropy():
    """Validates that Page-Wootters relational time requires strictly positive entanglement entropy."""
    evaluator = ReggeWdwEvaluator(in_memory=True)
    T = [[0.6, 0.4], [0.4, 0.6]]
    contract = evaluator.evaluate_finite_history(
        contract_id="PWNF-ENTANGLEMENT-TEST",
        system_transfer_matrix=T,
        num_clock_states=5,
    )
    assert contract.clock_marginal_entropy > 0.5
    evaluator.close()


def test_negative_control_degenerate_triangle_rcnf():
    """Negative control: degenerate triangle violating triangle inequality yields zero area."""
    area = ReggeWdwEvaluator.triangle_area(1.0, 2.0, 10.0)
    assert area == 0.0


def test_empty_history_is_rejected():
    evaluator = ReggeWdwEvaluator(in_memory=True)
    try:
        with pytest.raises(ValueError):
            evaluator.evaluate_finite_history("EMPTY", [], 0)
    finally:
        evaluator.close()


def test_arxiv_1904_01966_riemann_ricci_recovery():
    """Recovers arXiv:1904.01966 Eq. 17-19: Discrete Riemann tensor contracts to R = 2 * rho * eps."""
    evaluator = ReggeWdwEvaluator(in_memory=True)
    rho = 2.5
    eps = 0.8
    u_vec = (0.6, 0.8, 0.0)

    receipt = evaluator.evaluate_discrete_riemann_and_bianchi(
        joint_p=1,
        rho_p=rho,
        epsilon_p=eps,
        u_vector=u_vec,
        hinge_length=1.2,
    )

    # Analytical Ricci scalar is 2 * rho * eps = 2 * 2.5 * 0.8 = 4.0
    assert math.isclose(receipt.analytical_scalar, 4.0, rel_tol=1e-9)
    assert math.isclose(receipt.ricci_scalar, 4.0, rel_tol=1e-9)
    assert receipt.scalar_residual <= 1e-12
    # Antisymmetry in pairs: R_{abmn} == -R_{bamn}
    assert receipt.antisymmetry_residual <= 1e-12
    evaluator.close()


def test_arxiv_1904_01966_first_bianchi_identity():
    """Recovers arXiv:1904.01966 Eq. 21-22: First Bianchi identity R_{[abm]n} = 0."""
    evaluator = ReggeWdwEvaluator(in_memory=True)
    for u_vec in [(1.0, 0.0, 0.0), (0.0, 1.0, 0.0), (0.57735, 0.57735, 0.57735)]:
        receipt = evaluator.evaluate_discrete_riemann_and_bianchi(
            joint_p=2,
            rho_p=1.8,
            epsilon_p=0.45,
            u_vector=u_vec,
        )
        assert receipt.first_bianchi_residual <= 1e-12
        assert receipt.satisfies_bianchi is True
    evaluator.close()


def test_arxiv_1904_01966_second_bianchi_identity():
    """Recovers arXiv:1904.01966 Eq. 28, 35: Discrete second Bianchi via bone boundary closure sum eps_p * U^p = 0."""
    evaluator = ReggeWdwEvaluator(in_memory=True)
    # Closed configuration of 6 bones summing to zero orientation flux
    bones = [
        (1, 1.0, 0.5, (1.0, 0.0, 0.0), 1.0),
        (2, 1.0, 0.5, (-1.0, 0.0, 0.0), 1.0),
        (3, 1.0, 0.3, (0.0, 1.0, 0.0), 1.0),
        (4, 1.0, 0.3, (0.0, -1.0, 0.0), 1.0),
        (5, 1.0, 0.4, (0.0, 0.0, 1.0), 1.0),
        (6, 1.0, 0.4, (0.0, 0.0, -1.0), 1.0),
    ]
    norm, satisfies = evaluator.evaluate_discrete_second_bianchi(bones)
    assert satisfies is True
    assert norm <= 1e-12
    evaluator.close()


def test_arxiv_1904_01966_discrete_einstein_equations():
    """Recovers arXiv:1904.01966 Eq. 69: Discrete vacuum Einstein equations sum eps * dL/dl = 0."""
    evaluator = ReggeWdwEvaluator(in_memory=True)
    # 4 interior edges satisfying vacuum minimal action condition
    variations = [
        (1, 0.0, 0.0, 0.0),
        (2, 0.0, 0.0, 0.0),
        (3, 0.0, 0.0, 0.0),
        (4, 0.0, 0.0, 0.0),
    ]
    max_res, satisfies = evaluator.evaluate_discrete_einstein_equations(variations)
    assert satisfies is True
    assert max_res <= 1e-12
    evaluator.close()


def test_lorentzian_cdt_causal_pachner_bqnf_repair():
    """Evaluates 4D Lorentzian CDT causal Pachner moves preserving spatial slice foliation."""
    evaluator = ReggeWdwEvaluator(in_memory=True)
    # Causal (2,3) move preserving spatial Euler characteristic chi(Sigma_t) = 2
    receipt1 = evaluator.evaluate_lorentzian_cdt_pachner_move(
        slice_t=1,
        move_type="causal_2_to_3",
        prior_euler_char=2,
        post_euler_char=2,
        creates_ctc=False,
        local_gauge_shift=0.5,
    )
    assert receipt1.disposition == "ExactRepair"
    assert receipt1.is_exact_repaired is True

    # Causal (2,6) move preserving spatial foliation
    receipt2 = evaluator.evaluate_lorentzian_cdt_pachner_move(
        slice_t=1,
        move_type="causal_2_to_6",
        prior_euler_char=2,
        post_euler_char=2,
        creates_ctc=False,
        local_gauge_shift=0.8,
    )
    assert receipt2.disposition == "ExactRepair"
    assert receipt2.is_exact_repaired is True
    evaluator.close()


def test_lorentzian_cdt_acausal_topology_change_refusal():
    """Negative control: Acausal Pachner move modifying spatial slice Euler characteristic is refused."""
    evaluator = ReggeWdwEvaluator(in_memory=True)
    # Acausal branching: Euler char changes from 2 to 4 (spurious wormhole / baby universe formation)
    receipt = evaluator.evaluate_lorentzian_cdt_pachner_move(
        slice_t=2,
        move_type="acausal_branching",
        prior_euler_char=2,
        post_euler_char=4,
        creates_ctc=False,
    )
    assert receipt.disposition == "ClosureFailure"
    assert receipt.is_exact_repaired is False
    evaluator.close()


def test_lorentzian_cdt_ctc_refusal():
    """Negative control: Lorentzian move introducing a Closed Timelike Curve is strictly refused."""
    evaluator = ReggeWdwEvaluator(in_memory=True)
    receipt = evaluator.evaluate_lorentzian_cdt_pachner_move(
        slice_t=3,
        move_type="causal_2_to_3",
        prior_euler_char=2,
        post_euler_char=2,
        creates_ctc=True,
    )
    assert receipt.disposition == "ClosureFailure"
    assert receipt.is_exact_repaired is False
    evaluator.close()
