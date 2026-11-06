r"""
Unit tests for PO-012 / GR-002 cell growth engine, L1 structure, and pure diagnostics.
Enforces 95%+ production test coverage gate across modular components.
AuthorityEffect: None.
"""

import math
import numpy as np

from poset import Poset, Extension
from growth_iterator import CellGrowthIterator
from pure_diagnostics import main as main_diagnostics, run_fermion_pure_diagnostic, run_higgs_pure_diagnostic, run_ewsb_pure_diagnostic
from higgs_pure_linear_certificate import generate_certificate
from constraint_closure_l1_structure import ConstraintClosureL1Structure
from l1_regge import compute_regge_valency_deficit, compute_3d_regge_action_minimization, compute_4d_barbero_immirzi_regge_action
from l1_topological_defects import evaluate_2simplex_face_inertia_transition, compute_4d_chiral_winding_number, compute_non_resonant_defect_fraction
from l1_functor import evaluate_forgetful_functor_l1_l2



def test_poset_creation_and_coboundary():
    edges = [(0, 1), (1, 2), (2, 0)]
    poset = Poset(num_vertices=3, edges=edges)
    assert poset.num_vertices == 3
    assert len(poset.edges) == 3
    section = np.array([1.0, 0.0, -1.0])
    cob = poset.coboundary(section)
    assert len(cob) == 3
    betti = poset.extract_betti_number()
    assert betti >= 0


def test_poset_admissible_extensions():
    edges = [(0, 1), (1, 2), (2, 0)]
    poset = Poset(num_vertices=3, edges=edges)
    defect = np.array([2.0, -1.0, -1.0])
    exts = poset.get_admissible_extensions(defect)
    assert len(exts) > 0
    new_poset = poset.add_extensions(exts[:1])
    assert new_poset.num_vertices > 3


def test_growth_iterator_execution():
    edges = [(0, 1), (1, 2), (2, 0)]
    poset = Poset(num_vertices=3, edges=edges)
    iterator = CellGrowthIterator(max_steps=5)
    section = np.array([1.0, 0.0, -1.0])
    res = iterator.iterate(poset, section)
    assert res.final_poset is not None
    assert len(res.l1_norm_history) > 0


def test_growth_iterator_zero_defect():
    edges = [(0, 1), (1, 2), (2, 0)]
    poset = Poset(num_vertices=3, edges=edges)
    iterator = CellGrowthIterator()
    section = np.array([0.0, 0.0, 0.0])
    res = iterator.iterate(poset, section)
    assert res.converged is True


def test_regge_valency_deficit_angle():
    res = compute_regge_valency_deficit(valency=5)
    assert res["deficit_angle_exact"] == "pi/3"
    assert abs(res["deficit_angle_radians"] - math.pi / 3.0) < 1e-12
    assert abs(res["fractional_curvature"] - 1.0 / 6.0) < 1e-12


def test_2simplex_face_inertia_transition():
    res = evaluate_2simplex_face_inertia_transition()
    assert res["hollow_h1_rank"] == 1
    assert res["filled_h1_rank"] == 0
    assert res["hollow_massless_inertia"] == 0.0
    assert res["face_curvature_f"] == 3.0
    assert res["mass_inertia_gap"] == 9.0
    assert res["authority"] == "None"


def test_4d_chiral_winding_number():
    res = compute_4d_chiral_winding_number()
    assert res["topological_winding_number"] == 1
    assert res["chiral_winding_L"] == 1
    assert res["chiral_winding_R"] == -1
    assert res["is_topologically_quantized"] is True
    assert res["authority"] == "None"


def test_3d_simplicial_regge_action_minimization():
    res = compute_3d_regge_action_minimization(
        hinge_valencies=[5, 4, 6, 5],
        hinge_areas=[1.0, 1.0, 1.0, 1.0]
    )
    assert res["lp_solver_success"] is True
    assert abs(res["dihedral_angle_rad"] - math.acos(1.0 / 3.0)) < 1e-12
    assert res["flat_hinge_valency"] > 5.0
    assert len(res["deficit_angles_rad"]) == 4
    assert res["authority"] == "None"


def test_4d_barbero_immirzi_regge_action():
    res = compute_4d_barbero_immirzi_regge_action(
        hinge_valencies_4d=[5, 4, 5, 4],
        triangle_areas=[1.0, 1.0, 1.0, 1.0],
        immirzi_gamma=0.274066
    )
    assert abs(res["hyper_dihedral_angle_rad"] - math.acos(1.0 / 4.0)) < 1e-12
    assert res["flat_4d_hinge_valency"] < 5.0
    assert len(res["epsilon_4d_rad"]) == 4
    assert len(res["epsilon_dual"]) == 4
    assert res["authority"] == "None"


def test_non_resonant_defect_fraction():
    res = compute_non_resonant_defect_fraction(n_edges=3, n_states_per_edge=2)
    assert res["total_configurations"] == 8
    assert res["resonant_configurations"] == 4
    assert res["non_resonant_configurations"] == 4
    assert res["non_resonant_fraction"] == 0.5


def test_forgetful_functor_l1_l2_information_loss():
    cochain = np.array([1.0, -1.0, 2.0, 0.5])
    res = evaluate_forgetful_functor_l1_l2(cochain)
    assert res["forgetful_functor_loss_certified"] is True
    assert res["information_loss"] > 0.0
    assert res["authority"] == "None"


def test_class_facade_backward_compatibility():
    facade = ConstraintClosureL1Structure()
    res = facade.compute_regge_valency_deficit(valency=5)
    assert res["deficit_angle_exact"] == "pi/3"


def test_pure_diagnostics_suite():
    run_fermion_pure_diagnostic()
    run_higgs_pure_diagnostic()
    run_ewsb_pure_diagnostic()
    main_diagnostics()


def test_higgs_pure_linear_certificate(tmp_path):
    cert = generate_certificate(tmp_path / "higgs_pure_linear_certificate.json")
    assert cert["r2_scores"]["r2_linear"] == 1.0
    assert cert["claim_status"] == "FAILED"
    assert "sha256_fingerprint" in cert
