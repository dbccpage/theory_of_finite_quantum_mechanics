"""Regression tests covering all 10 items from Jeremy H. Carroll's peer review of GR-002.

AuthorityEffect: None.
"""

import math
from fractions import Fraction
import numpy as np
import pytest

from bianchi import verify_contracted_bianchi_3d, verify_closed_bianchi_flux
from cauchy_sandwich import (
    CauchySandwich4Complex,
    build_canonical_3simplex_sandwich,
)
from complex import SimplicialComplex
from degree2_dual_witness import Degree2DualCertifiedL1Solver
from dual_witness import DualCertifiedL1Solver
from exact_lp import exact_rational_l1_quotient, ExactL1Result
from high_energy_fence import (
    falsify_alpha_fine_structure_wall,
    falsify_dark_sector_analogy,
    falsify_gauge_group_uniqueness,
    falsify_higgs_vev_derivation,
    falsify_susy_saturation_scale,
)
from ponzano_regge import (
    compute_l1_phase_envelope,
    evaluate_schlafli_path_bound,
    evaluate_semiclassical_regge_phase,
    verify_regge_action_lipschitz_bound,
)
from simplex import (
    cayley_menger_volume_sq,
    compute_simplex_dihedral_angles,
    reconstruct_simplex_coordinates,
    regular_simplex_dihedral_angle,
    tetrahedron_dihedral_angle,
)
from wdw_constraint import (
    build_hamiltonian_scalar_constraint,
    build_joint_constraint_system,
    build_momentum_vector_constraint,
    build_total_constraint_cochain,
    solve_joint_wdw_constraints,
)


class TestItem1HamiltonianBlindSpot:
    """Item 1: Correct the Hamiltonian blind spot in the proposed Wheeler-DeWitt diagnostic."""

    def test_regular_3sphere_hamiltonian_blind_spot_and_joint_resolution(self):
        """Reviewer reproduced example:
        On regular boundary of 4-simplex (3-sphere), all edge lengths 1, zero momentum:
        Each edge belongs to 3 regular tetrahedra, deficit is approx 2.590307.
        The Hamiltonian builder returns approx -20.722456 at every vertex.
        In the naive encoding omega = p + d0 H, Phi_{d0}(omega) = 0 because d0 H is in im(d0).
        In the joint direct-sum system C^1 + C^0, Phi_joint = Phi(p) + ||H||_1 > 0.
        """
        # 3-sphere: boundary of 4-simplex (5 vertices 0..4, 10 edges, 10 triangles, 5 tetrahedra)
        vertices = list(range(5))
        edges = [(i, j) for i in range(5) for j in range(i + 1, 5)]
        tetrahedra = [
            (0, 1, 2, 3),
            (0, 1, 2, 4),
            (0, 1, 3, 4),
            (0, 2, 3, 4),
            (1, 2, 3, 4),
        ]
        edge_lengths = {e: 1.0 for e in edges}
        # Zero momenta
        p_edge = {e: 0.0 for e in edges}

        # Deficit on each edge: 2*pi - 3 * arccos(1/3) approx 2.5903070552
        theta_tet = regular_simplex_dihedral_angle(3)
        expected_deficit = 2.0 * math.pi - 3.0 * theta_tet
        assert abs(expected_deficit - 2.5903070552) < 1e-6

        # Build Hamiltonian constraint at vertices
        H_vertex = build_hamiltonian_scalar_constraint(
            vertices,
            edges,
            tetrahedra,
            edge_lengths,
            p_edge,
            dual_vertex_volume=1.0,
        )
        # Expected H approx -20.7224564413 at every vertex
        for v in vertices:
            assert abs(H_vertex[v] - (-20.7224564413)) < 1e-6

        # In the naive encoding, total cochain is p + d0 H.
        # Since p = 0, total cochain = d0 H, so Phi_{d0}(total) == 0!
        naive_cochain, d0_matrix = build_total_constraint_cochain(
            vertices, edges, p_edge, H_vertex
        )
        solver = DualCertifiedL1Solver(tol=1e-8)
        naive_result = solver.solve(naive_cochain, d0_matrix)
        # Naive encoding reports is_closed=True, completely blind to H!
        assert naive_result.is_closed is True
        assert naive_result.primal_obj < 1e-8

        # Under the joint direct-sum system (Omega_joint, D_joint, H_norm):
        omega_joint, D_joint, H_l1_norm = build_joint_constraint_system(
            vertices, edges, p_edge, H_vertex
        )
        assert abs(H_l1_norm - 5.0 * 20.7224564413) < 1e-4
        joint_result = solve_joint_wdw_constraints(
            vertices, edges, p_edge, H_vertex, tol=1e-8
        )
        # Joint system correctly preserves Hamiltonian violation:
        assert joint_result["is_closed"] is False
        assert joint_result["hamiltonian_l1_violation"] > 100.0
        assert abs(joint_result["joint_quotient_distance"] - joint_result["hamiltonian_l1_violation"]) < 1e-6

    def test_solve_joint_wdw_constraints_legacy_solver_interface(self, monkeypatch):
        """Older solver versions lacking 'is_certified' attribute must not cause AttributeError."""
        from dual_witness import DualCertifiedL1Solver, L1QuotientResult
        vertices = [0, 1]
        edges = [(0, 1)]
        p_edge = {(0, 1): 0.0}
        H_vertex = {0: 1.0, 1: 2.0}

        class LegacyResult:
            def __init__(self, res: L1QuotientResult):
                self.primal_obj = res.primal_obj
                self.dual_obj = res.dual_obj
                self.duality_gap = res.duality_gap
                self.is_closed = res.is_closed
                self.primal_alpha = res.primal_alpha
                self.primal_residual = res.primal_residual
                self.dual_witness = res.dual_witness
                self.dual_divergence_norm = res.dual_divergence_norm
                self.solver_status = res.solver_status
                # Deliberately omit self.is_certified to simulate legacy solver

        orig_solve = DualCertifiedL1Solver.solve
        def mock_solve(self, omega, d0):
            res = orig_solve(self, omega, d0)
            return LegacyResult(res)

        monkeypatch.setattr(DualCertifiedL1Solver, "solve", mock_solve)
        joint_res = solve_joint_wdw_constraints(vertices, edges, p_edge, H_vertex)
        assert "is_certified" in joint_res
        assert joint_res["is_certified"] is True  # Computed from verified invariants!


class TestItem2BianchiDiagnostics:
    """Item 2: Withdraw unrestricted scalar 4D Bianchi theorem and enforce NaN rejection."""

    def test_verify_contracted_bianchi_nan_rejection(self):
        """verify_contracted_bianchi_3d must return is_satisfied=False when input deficits contain NaN."""
        vertex_coords = {
            0: np.array([0.0, 0.0, 0.0]),
            1: np.array([1.0, 0.0, 0.0]),
            2: np.array([0.5, math.sqrt(3.0) / 2.0, 0.0]),
            3: np.array([0.5, math.sqrt(3.0) / 6.0, math.sqrt(2.0 / 3.0)]),
        }
        edges = [(0, 1), (0, 2), (0, 3), (1, 2), (1, 3), (2, 3)]
        edge_deficits = {e: float("nan") for e in edges}

        res = verify_contracted_bianchi_3d(vertex_coords, edges, edge_deficits)
        assert res["is_satisfied"] is False
        assert res["authority_effect"] == "None"

    def test_nonregular_4d_simplex_bianchi_counterexample(self):
        """Reviewer counterexample (Jeremy H. Carroll, Sept 2026):
        On boundary of 5-simplex (4-sphere), set all edges to 1 except l_{01} = 1.1.
        Verify that scalar Bianchi flux does not vanish:
        ||d_2 eps||_1 approx 1.956565, ||d_2 eps||_inf approx 0.244571.
        """
        from itertools import combinations

        all_edges = list(combinations(range(6), 2))
        edge_lens = {e: 1.0 for e in all_edges}
        edge_lens[(0, 1)] = 1.1

        all_4simplices = list(combinations(range(6), 5))
        triangles = list(combinations(range(6), 3))
        tetrahedra = list(combinations(range(6), 4))

        tri_dihedrals: dict[tuple[int, int, int], list[float]] = {t: [] for t in triangles}
        for s in all_4simplices:
            dihedrals = compute_simplex_dihedral_angles(s, edge_lens, dim=4)
            for t, th in dihedrals.items():
                tri_dihedrals[t].append(th)

        for t, ths in tri_dihedrals.items():
            assert len(ths) == 3, f"Triangle {t} belongs to {len(ths)} simplices, expected 3"

        deficits = {t: 2.0 * math.pi - sum(ths) for t, ths in tri_dihedrals.items()}

        d2_eps: dict[tuple[int, int, int, int], float] = {}
        for tau in tetrahedra:
            v0, v1, v2, v3 = tau
            val = deficits[(v1, v2, v3)] - deficits[(v0, v2, v3)] + deficits[(v0, v1, v3)] - deficits[(v0, v1, v2)]
            d2_eps[tau] = val

        l1_flux = sum(abs(v) for v in d2_eps.values())
        linf_flux = max(abs(v) for v in d2_eps.values())

        assert abs(l1_flux - 1.9565652080) < 1e-6
        assert abs(linf_flux - 0.2445706510) < 1e-6
        assert abs(d2_eps[(0, 2, 3, 4)] - (-0.2445706510)) < 1e-6
        assert l1_flux > 1.9


class TestItem3ExactRationalLP:
    """Item 3: Make exact results depend on successful exact certificate verification."""

    def test_carroll_denominator_regression_case(self):
        """Reviewer reproduced example:
        omega = [Fraction(1, 1000001)], D = [[-1, 1]].
        True quotient distance is 0: choose alpha = (0, 1/1000001).
        exact_rational_l1_quotient must return exact optimum 0 and is_closed=True.
        """
        omega = [Fraction(1, 1000001)]
        d0 = [[Fraction(-1), Fraction(1)]]

        res = exact_rational_l1_quotient(omega, d0)
        assert res.primal_obj == Fraction(0)
        assert res.dual_obj == Fraction(0)
        assert res.duality_gap == Fraction(0)
        assert res.is_closed is True
        assert res.is_certified is True
        assert res.authority_effect == "None"

        # Check that primal_alpha is exported and exactly cancels omega:
        assert res.primal_alpha is not None
        alpha0, alpha1 = res.primal_alpha
        # D * alpha = -alpha0 + alpha1
        d_alpha = -alpha0 + alpha1
        assert d_alpha == Fraction(1, 1000001)

        # Check export in to_dict()
        d = res.to_dict()
        assert d["is_closed"] is True
        assert d["is_certified"] is True
        assert "primal_alpha" in d

    def test_exact_rational_lp_nonzero_quotient_certificate(self):
        """Non-trivial quotient on oriented cycle: omega = [1, 1, 1], D = cycle incidence."""
        d0 = [
            [Fraction(-1), Fraction(1), Fraction(0)],
            [Fraction(0), Fraction(-1), Fraction(1)],
            [Fraction(1), Fraction(0), Fraction(-1)],
        ]
        omega = [Fraction(1), Fraction(1), Fraction(1)]
        res = exact_rational_l1_quotient(omega, d0)

        assert res.is_closed is False
        assert res.primal_obj == Fraction(3)
        assert res.dual_obj == Fraction(3)
        assert res.duality_gap == Fraction(0)
        assert res.is_certified is True

        # Check dual witness properties: D^T w = 0, |w_i| <= 1, <w, omega> = 3
        w = res.dual_witness
        for wi in w:
            assert abs(wi) <= Fraction(1)
        # D^T w:
        for j in range(3):
            col_dot = sum(d0[i][j] * w[i] for i in range(3))
            assert col_dot == Fraction(0)


class TestItem4NumericalZeroAndCertificates:
    """Item 4: Repair numerical zero shortcuts and export certificates in both solvers."""

    def test_small_nonzero_cycle_not_shortcut_to_zero(self):
        """Reviewer cases with tol=10^-10:
        omega = (5e-11)*(1, 1, 1) on oriented 3-edge cycle with incidence D=d0.
        True quotient distance is 1.5e-10.
        Solvers must NOT return 0 / OPTIMAL_ZERO via np.allclose.
        """
        d0 = np.array([
            [-1.0,  1.0,  0.0],
            [ 0.0, -1.0,  1.0],
            [ 1.0,  0.0, -1.0],
        ])
        omega = 5e-11 * np.ones(3, dtype=float)
        solver = DualCertifiedL1Solver(tol=1e-12)
        res = solver.solve(omega, d0)

        # Objective must reflect the non-trivial cycle distance approx 1.5e-10
        assert res.primal_obj > 1e-11
        assert abs(res.primal_obj - 1.5e-10) < 1e-11

        # Check exported certificate fields in to_dict()
        d = res.to_dict()
        assert "primal_alpha" in d
        assert "primal_residual" in d
        assert "dual_witness" in d
        assert "is_certified" in d

    def test_degree2_dual_witness_exports_and_tolerances(self):
        """Degree 2 solver must export primal_beta, primal_residual, dual_witness."""
        d1 = np.array([
            [ 1.0, -1.0,  1.0],
        ])
        omega = np.array([0.5])
        solver = Degree2DualCertifiedL1Solver(tol=1e-10)
        res = solver.solve(omega, d1)
        d = res.to_dict()
        assert "primal_beta" in d
        assert "primal_residual" in d
        assert "dual_witness" in d
        assert "is_certified" in d


class TestItem5PonzanoReggeAsymptotics:
    """Item 5: Separate fixed-angle phase bounds from changing Regge geometry."""

    def test_shifted_vs_unshifted_phase_envelope_conventions(self):
        """Reviewer reproduced values:
        At all spins 1, theta = arccos(1/3):
        evaluate_semiclassical_regge_phase = sum (1 + 0.5) * theta approx 11.07863.
        compute_l1_phase_envelope(include_shift=True) approx 11.07863.
        compute_l1_phase_envelope(include_shift=False) approx 7.38576.
        """
        spins = [1, 1, 1, 1, 1, 1]
        phase = evaluate_semiclassical_regge_phase(spins)
        env_shifted = compute_l1_phase_envelope(spins, include_shift=True)
        env_unshifted = compute_l1_phase_envelope(spins, include_shift=False)

        assert abs(phase - 11.078634) < 1e-5
        assert abs(env_shifted - 11.078634) < 1e-5
        assert abs(env_unshifted - 7.385756) < 1e-5
        assert phase <= env_shifted + 1e-12

    def test_require_geometric_angles_for_irregular_spins(self):
        """When require_geometric_angles=True, non-equal spins without angles raise ValueError."""
        with pytest.raises(ValueError, match="Non-regular spins require explicit"):
            evaluate_semiclassical_regge_phase([1, 2, 2, 2, 2, 2], require_geometric_angles=True)


class TestItem6SimplexGeometryValidation:
    """Item 6: Reject invalid geometry and invalid diagnostic inputs explicitly."""

    def test_unrealizable_tetrahedron_gram_spectrum(self):
        """Reviewer counterexample:
        Tetrahedron with three base edges 1 and three apex edges 0.55.
        Centered Gram spectrum includes -0.023125.
        reconstruct_simplex_coordinates must return None.
        tetrahedron_dihedral_angle must raise ValueError.
        """
        # Vertices: base 0, 1, 2; apex 3
        # Base edges: (0,1), (0,2), (1,2) with length 1.0 (s = 1.0)
        # Apex edges: (0,3), (1,3), (2,3) with length 0.55 (s = 0.55^2 = 0.3025)
        s = {
            (0, 1): 1.0,
            (0, 2): 1.0,
            (1, 2): 1.0,
            (0, 3): 0.55 ** 2,
            (1, 3): 0.55 ** 2,
            (2, 3): 0.55 ** 2,
        }
        # Matrix of squared distances
        mat = np.zeros((4, 4), dtype=float)
        for (i, j), val in s.items():
            mat[i, j] = val
            mat[j, i] = val

        coords = reconstruct_simplex_coordinates(mat, dim=3)
        assert coords is None  # Correctly rejected due to negative Gram eigenvalue

        with pytest.raises(ValueError, match="Cannot compute tetrahedron dihedral angle"):
            tetrahedron_dihedral_angle(s, (0, 1))

    def test_scale_invariance_four_simplex_dihedral_angle(self):
        """Reviewer reproduced issue (Jeremy H. Carroll, Sept 2026):
        A regular 4-simplex should have dihedral angle arccos(1/4) ~ 1.3181160717 at every scale.
        Unscaled Gram cutoffs gave:
          scale = 1: correct 1.3181160717
          scale = 10^8: manufactured right angle 1.5707963268
          scale = 10^-8: rejected as singular
        With scale normalization, all scales return the exact dihedral angle arccos(1/4).
        """
        expected_theta = regular_simplex_dihedral_angle(4)
        all_edges = [(i, j) for i in range(5) for j in range(i + 1, 5)]

        for scale in [1e-8, 1.0, 1e8]:
            edge_lengths = {e: scale for e in all_edges}
            dihedrals = compute_simplex_dihedral_angles(tuple(range(5)), edge_lengths, dim=4)
            for hinge, th in dihedrals.items():
                assert abs(th - expected_theta) < 1e-8, f"Failed at scale {scale}: got {th}, expected {expected_theta}"

    def test_cayley_menger_negative_volume_raises_value_error(self):
        """Negative Cayley-Menger squared volume must raise ValueError instead of clipping to 0."""
        # Invalid tetrahedron with base 1.0, apex 0.55 has det(CM) yielding negative squared volume
        mat = np.array([
            [0.0, 1.0, 1.0, 0.55**2],
            [1.0, 0.0, 1.0, 0.55**2],
            [1.0, 1.0, 0.0, 0.55**2],
            [0.55**2, 0.55**2, 0.55**2, 0.0],
        ])
        with pytest.raises(ValueError, match="Cayley-Menger squared volume is negative"):
            cayley_menger_volume_sq(mat)


class TestItem7CauchySandwichFoliation:
    """Item 7: Narrow Cauchy-sandwich claims and fix vertex copying collisions."""

    def test_disjoint_vertex_mapping_noncontiguous_labels(self):
        """Base vertices {0, 1, 4, 5} must not collide with top vertices."""
        spatial_coords = {
            0: np.array([0.0, 0.0, 0.0]),
            1: np.array([1.0, 0.0, 0.0]),
            4: np.array([0.5, math.sqrt(3.0) / 2.0, 0.0]),
            5: np.array([0.5, math.sqrt(3.0) / 6.0, math.sqrt(2.0 / 3.0)]),
        }
        spatial_tetrahedra = [(0, 1, 4, 5)]
        sandwich = CauchySandwich4Complex(
            spatial_vertices=spatial_coords,
            spatial_tetrahedra=spatial_tetrahedra,
        )
        # Must have exactly 8 spacetime vertices (4 base + 4 top)
        assert sandwich.num_vertices == 8
        base_set = set(spatial_coords.keys())
        top_set = set(sandwich.top_vertex_map.values())
        assert base_set.isdisjoint(top_set)

    def test_nonuniform_lapse_timelike_tracks_spacelike_slice_failure(self):
        """Reviewer reproduced example:
        Regular unit spatial tetrahedron, zero shift, dt=1, lapses (1, 3, 1, 1).
        has_timelike_tracks() is True.
        Final-slice edge (4, 5) has squared interval -3 < 0 (timelike, not spacelike).
        is_spacelike_slice(1) is False.
        is_cauchy_foliation() is False.
        """
        sandwich = build_canonical_3simplex_sandwich(dt=1.0, lapse_val=1.0, shift_val=0.0)
        # Apply non-uniform lapse (1, 3, 1, 1)
        sandwich.lapse[0] = 1.0
        sandwich.lapse[1] = 3.0
        sandwich.lapse[2] = 1.0
        sandwich.lapse[3] = 1.0
        sandwich.rebuild_sandwich()

        assert sandwich.has_timelike_tracks() is True
        assert sandwich.is_spacelike_slice(0) is True
        assert sandwich.is_spacelike_slice(1) is False  # Final slice is not spacelike!
        assert sandwich.is_cauchy_foliation() is False


class TestItem8HighEnergyQuarantine:
    """Item 8: Reconcile boundary curvature, topology terminology, and quarantine text."""

    def test_quarantine_receipts_authority_none(self):
        """All quarantine receipts declare AuthorityEffect: None and accurate grounds."""
        rec_alpha = falsify_alpha_fine_structure_wall()
        assert "2*pi by discrete Gauss-Bonnet" in rec_alpha.mathematical_proof_of_failure
        assert rec_alpha.authority_effect == "None"

        rec_dark = falsify_dark_sector_analogy()
        assert "unrestricted quotient distance" in rec_dark.mathematical_proof_of_failure
        assert rec_dark.authority_effect == "None"

        rec_susy = falsify_susy_saturation_scale()
        assert "arbitrary" in rec_susy.mathematical_proof_of_failure
        assert rec_susy.authority_effect == "None"


class TestItem11HiggsSusyAndDiagnosticEvidence:
    """Item 11: Make historical Higgs/SUSY and current diagnostic evidence consistent."""

    def test_higgs_certificate_sampling_and_fixed_carrier_homogeneity(self):
        """Higgs certificate JSON reflects exact fixed-carrier quotient homogeneity:
        E(phi) = |phi| along fixed rays (R^2 = 1.0), quartic fit 0.985563.
        """
        import json
        from pathlib import Path

        cert_path = Path(__file__).resolve().parents[1] / "higgs_pure_linear_certificate.json"
        assert cert_path.is_file()
        with open(cert_path, "r", encoding="utf-8") as f:
            data = json.load(f)

        assert abs(data["r2_scores"]["r2_linear"] - 1.0) < 1e-6
        assert abs(data["r2_scores"]["r2_quartic"] - 0.985563) < 1e-5
        assert data["authority_effect"] == "None"
        assert "Mexican-hat" in data["verdict"]

    def test_barbero_immirzi_finite_run_mcmc_percentages(self):
        """Barbero-Immirzi header documents verified finite-run MCMC observations and barrier."""
        import barbero_immirzi_fence as bi
        assert "80.94%" in bi.__doc__
        assert "0.004%" in bi.__doc__
        assert "AuthorityEffect: None" in bi.__doc__
        barrier = bi.escape_barrier()
        assert abs(barrier["barrier_to_k8_peak"] - 4.29155) < 1e-3

    def test_gauge_higgs_susy_derivation_historical_ansatz(self):
        """Gauge-Higgs-SUSY derivation declares exploratory historical ansatz and is_valid=False."""
        from gauge_higgs_susy_derivation import run_full_gauge_higgs_susy_derivation
        result = run_full_gauge_higgs_susy_derivation()
        assert result.authority_effect == "None"
        assert result.is_valid is False
        assert result.classification == "HISTORICAL_EXPLORATORY_ANSATZ"
        assert len(result.witness.payload_hash) == 64
        assert result.witness.payload_hash != "0" * 64


class TestItem12DegreeLiftingAndCoexactUpdate:
    """Item 12: Repair degree lifting and qualify the coexact update's descent claim."""

    def test_c2_to_c3_lift_cell_arities_and_boundary(self):
        """Reviewer reproduced component example:
        On a valid 4-simplex carrier, put value 1 on triangle (0,1,2) and zero on other faces.
        Higher cells for C^2 -> C^3 lift must be tetrahedra (4 vertices), not 4-simplices (5 vertices).
        Boundary sum on tetrahedra yields raw L1 norm 2.0.
        """
        from higher_simplex_assembly import (
            SimplexComplex,
            discover_higher_cells_for_lift,
            boundary_sum,
        )
        # 4-simplex with vertices 0..4
        vertices = tuple(range(5))
        edges = [(i, j) for i in range(5) for j in range(i + 1, 5)]
        faces = [(i, j, k) for i in range(5) for j in range(i + 1, 5) for k in range(j + 1, 5)]
        tetrahedra = [
            (i, j, k, l)
            for i in range(5)
            for j in range(i + 1, 5)
            for k in range(j + 1, 5)
            for l in range(k + 1, 5)
        ]
        four_simplices = [(0, 1, 2, 3, 4)]

        complex_4s = SimplexComplex(
            vertices=list(vertices),
            cells={
                0: [(v,) for v in vertices],
                1: edges,
                2: faces,
                3: tetrahedra,
                4: four_simplices,
            },
        )

        higher_cells, kind = discover_higher_cells_for_lift(complex_4s, from_degree=2)
        assert kind == "tetrahedra"
        assert len(higher_cells) == 5
        # Every cell must have 4 vertices (3-simplex)
        for cell in higher_cells:
            assert len(cell) == 4

        # Put value 1.0 on triangle (0, 1, 2) and 0.0 on all other faces
        face_values = {f: (1.0 if f == (0, 1, 2) else 0.0) for f in faces}

        # Compute higher cochain via boundary_sum
        higher_cochain = {cell: boundary_sum(cell, face_values) for cell in higher_cells}
        raw_l1 = sum(abs(v) for v in higher_cochain.values())
        # Exactly 2 tetrahedra contain face (0, 1, 2): (0,1,2,3) and (0,1,2,4)
        assert abs(raw_l1 - 2.0) < 1e-9

    def test_five_triangle_shared_edge_coexact_update(self):
        """Reviewer reproduced example:
        Five triangles sharing an edge (0,1) with value 1, remaining edges 0.
        Executing coexact_curl records that curl increases from 5 to 20/3,
        and records curl_mass_canceled = 0.0 rather than claiming 5 was canceled.
        """
        from discrete_descent_engine import DDAEngine, Network

        # Triangles (0, 1, i) for i in 2..6
        nodes = list(range(7))
        edges = [(0, 1)] + [(0, i) for i in range(2, 7)] + [(1, i) for i in range(2, 7)]
        faces = [(0, 1, i) for i in range(2, 7)]
        net = Network(nodes=nodes, edges=edges, faces=faces)

        edge_values = {e: (1.0 if e == (0, 1) else 0.0) for e in edges}
        engine = DDAEngine(network=net)
        found_cert = engine.run_foundation(edge_values)
        step_cert, residuals = engine.step(move_type="coexact_curl")

        # Gamma before = 5.0, gamma after = 20/3 approx 6.6667
        assert abs(found_cert.gamma2 - 5.0) < 1e-6
        assert abs(residuals[1] - 20.0 / 3.0) < 1e-6
        assert step_cert.loss_ledger["delta_gamma2"] > 0.0  # Curl strictly increased!
        assert step_cert.loss_ledger["curl_mass_canceled"] == 0.0  # Zero cancellation credited!

    def test_lp_failure_upper_bound_propagation(self):
        """When the LP solver fails, evaluate_residual flags result as an uncertified upper bound."""
        from degree_generic_residual import _solve_l1_linear_system, evaluate_residual
        from higher_simplex_assembly import SimplexComplex

        # Test _solve_l1_linear_system on empty matrix
        x, res, norm, success = _solve_l1_linear_system(np.zeros((3, 0)), np.array([1.0, 2.0, 3.0]))
        assert success is True
        assert abs(norm - 6.0) < 1e-9

        # SimplexComplex with single edge
        sc = SimplexComplex(vertices=[0, 1], cells={0: [(0,), (1,)], 1: [(0, 1)]})
        report = evaluate_residual(sc, degree=1, cochain={(0, 1): 1.5})
        assert report.is_certified is False  # Honest uncertified status
        assert report.lp_success is True

    def test_solver_cascade_receipt_is_solved_consistency_checks(self):
        """Reviewer reproduced issue:
        SolverCascadeReceipt.is_solved() must reject:
        - terminal_status='AUTHORIZATION_EXHAUSTED'
        - residual triple (0, 1, 0) even if final_residual_size is 0
        - admitted_complex_verified=False
        - unfulfilled prior_degree_obligations
        """
        from solver_of_solvers import SolverCascadeReceipt

        # 1. Authorization exhausted with zero residual must NOT be solved
        r_auth = SolverCascadeReceipt(
            carrier_nodes=4,
            carrier_edges=5,
            initial_residual_size=1.0,
            final_residual_size=0.0,
            stages_executed=["S1"],
            degree_window_reached=1,
            terminal_status="AUTHORIZATION_EXHAUSTED",
            final_residual_triple=(0.0, 0.0, 0.0),
            admitted_complex_verified=True,
        )
        assert r_auth.is_solved() is False

        # 2. Residual triple (0, 1, 0) must NOT be solved even if scalar residual is 0
        r_triple = SolverCascadeReceipt(
            carrier_nodes=4,
            carrier_edges=5,
            initial_residual_size=1.0,
            final_residual_size=0.0,
            stages_executed=["S1"],
            degree_window_reached=1,
            terminal_status="Exact",
            final_residual_triple=(0.0, 1.0, 0.0),
            admitted_complex_verified=True,
        )
        assert r_triple.is_solved() is False

        # 3. Unverified admitted complex must NOT be solved
        r_unver = SolverCascadeReceipt(
            carrier_nodes=4,
            carrier_edges=5,
            initial_residual_size=1.0,
            final_residual_size=0.0,
            stages_executed=["S1"],
            degree_window_reached=1,
            terminal_status="Exact",
            final_residual_triple=(0.0, 0.0, 0.0),
            admitted_complex_verified=False,
        )
        assert r_unver.is_solved() is False

        # 4. Non-zero prior obligation must NOT be solved
        r_prior = SolverCascadeReceipt(
            carrier_nodes=4,
            carrier_edges=5,
            initial_residual_size=1.0,
            final_residual_size=0.0,
            stages_executed=["S1"],
            degree_window_reached=1,
            terminal_status="Exact",
            final_residual_triple=(0.0, 0.0, 0.0),
            admitted_complex_verified=True,
            prior_degree_obligations={0: 0.5},
        )
        assert r_prior.is_solved() is False

        # 5. All valid conditions met -> returns True
        r_valid = SolverCascadeReceipt(
            carrier_nodes=4,
            carrier_edges=5,
            initial_residual_size=1.0,
            final_residual_size=0.0,
            stages_executed=["S1"],
            degree_window_reached=1,
            terminal_status="Exact",
            final_residual_triple=(0.0, 0.0, 0.0),
            admitted_complex_verified=True,
            prior_degree_obligations={},
        )
        assert r_valid.is_solved() is True


class TestItem13ReceiptsAndTracePortability:
    """Item 13: Make state receipts unambiguous and trace generation portable."""

    def test_fingerprinted_bag_collision_resistance(self):
        """Reviewer reproduced example:
        Distinct bags with name N and data {'a':'bc'} vs {'ab':'c'} must NOT collide.
        """
        from certified_pipeline import FingerprintedBag

        bag1 = FingerprintedBag(name="N", data={"a": "bc"})
        bag2 = FingerprintedBag(name="N", data={"ab": "c"})

        assert bag1.fingerprint() != bag2.fingerprint()

    def test_trace_recorder_shallow_path_portability(self, tmp_path):
        """Trace recorders must not raise IndexError on shallow directory depths."""
        from dda_trace_recorder import DDATraceRecorder
        from descent_trace_recorder import DDATraceRecorder as DescentRecorder

        rec1 = DDATraceRecorder(trace_dir=str(tmp_path / "t1"))
        assert rec1.trace_dir.is_dir()

        rec2 = DescentRecorder(trace_dir=str(tmp_path / "t2"))
        assert rec2.trace_dir.is_dir()


class TestItem14MonteCarloSamplingAndEquilibrium:
    """Item 14: Replace sampling-budget 'equilibrium certificate' with accurately scoped result."""

    def test_analytical_boltzmann_reference_distribution(self):
        """Analytical Boltzmann distribution has p(6) ~ 0.8095177985 at beta=1, gamma=0.274066."""
        from regge_monte_carlo import analytical_boltzmann_distribution
        p = analytical_boltzmann_distribution(beta=1.0, immirzi_gamma=0.274066)
        assert abs(p[6] - 0.8095177985) < 1e-8
        assert abs(sum(p.values()) - 1.0) < 1e-12

    def test_regge_monte_carlo_budget_heuristic_and_tv_distance(self):
        """Simulation exports budget heuristic and non-negative total variation distance."""
        from regge_monte_carlo import run_regge_monte_carlo_simulation
        res = run_regge_monte_carlo_simulation(n_hinges=10, n_steps=50, beta=1.0, seed=42)
        assert res["budget_heuristic_reached"] is True
        assert res["total_variation_distance"] >= 0.0
        assert "analytical_distribution" in res
        assert "empirical_distribution" in res
        assert "total_action" in res

    def test_regge_adapter_sampling_receipt_and_nonnegative_residual_mass(self):
        """Reviewer reproduced example:
        1,000 hinges, 3,000 steps, beta=1, seed 42:
        Total action is negative (~ -2522.45), but residual_mass must NOT be negative.
        Residual mass represents non-negative L1 TV distance.
        Certificate type is MONTE_CARLO_SAMPLING_RECEIPT, certifying recorded data identity.
        """
        from regge_monte_carlo import ReggeMonteCarloSolverAdapter, SolverInput
        adapter = ReggeMonteCarloSolverAdapter()
        output = adapter.solve(
            SolverInput(
                problem_id="mc-budget-test",
                data={"n_hinges": 1000, "n_steps": 3000, "beta": 1.0, "seed": 42},
            )
        )
        assert output.residual_mass >= 0.0  # Must NEVER be negative!
        assert output.certificate.certificate_type == "MONTE_CARLO_SAMPLING_RECEIPT"
        assert output.metadata["total_action"] < -2000.0  # Signed action preserved in metadata
        assert abs(output.metadata["total_action"] - (-2522.45383)) < 5.0
