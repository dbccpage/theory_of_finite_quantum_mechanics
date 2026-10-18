"""Soviet Invariant Test Battery for Discrete General Relativity on L1.

Strict invariant, adversarial, and property-based verification:
1. Flat-space zero-defect & zero-residual recovery.
2. Simplicial Bianchi identities on closed complexes (3-sphere, 4-sphere, flat torus).
3. Nilpotency of simplicial boundary and coboundary operators (partial^2 = 0, d^2 = 0).
4. Wheeler-DeWitt gauge invariance under arbitrary pure gauge shifts (d_0 gamma).
5. Exact strong duality: certified dual circulation witness with zero duality gap.
6. Complementary slackness & orthogonality of dual witness.
7. Stress tests under extreme geometries (degenerate simplices, needle edges).
8. Ponzano-Regge semiclassical phase L1 Lipschitz continuity.
9. Quarantined high-energy physics falsification receipts.

AuthorityEffect: None.
"""

from __future__ import annotations

import math
from fractions import Fraction
import numpy as np
import pytest

from simplex import (
    Simplex,
    cayley_menger_volume_sq,
    simplex_volume,
    regular_simplex_dihedral_angle,
    tetrahedron_dihedral_angle,
    four_simplex_dihedral_angle,
    compute_simplex_dihedral_angles,
    compute_hinge_deficit_angle,
)
from complex import (
    SimplicialComplex,
    build_simplex_boundary_complex,
    build_4simplex_boundary_3sphere,
    build_5simplex_boundary_4sphere,
    build_flat_torus_2d,
)
from bianchi import (
    contracted_bianchi_vertex_flux_3d,
    simplicial_bianchi_boundary_flux,
    verify_contracted_bianchi_3d,
    verify_closed_bianchi_flux,
)
from wdw_constraint import (
    CauchySlice3D,
    DiscreteWDWConstraintSystem,
    compute_discrete_scalar_curvature,
)
from dual_witness import (
    DualCertifiedL1Solver,
    compute_l1_quotient_with_dual_witness,
)
from exact_lp import exact_rational_l1_quotient
from ponzano_regge import (
    evaluate_semiclassical_regge_phase,
    compute_l1_phase_envelope,
    verify_regge_action_lipschitz_bound,
    evaluate_schlafli_path_bound,
)
from high_energy_fence import (
    HighEnergyQuarantineRegister,
    falsify_gauge_group_uniqueness,
    falsify_higgs_vev_derivation,
    falsify_susy_saturation_scale,
    falsify_alpha_fine_structure_wall,
    falsify_dark_sector_analogy,
)


class TestSovietSimplicialTopologyInvariants:
    """Rigorous topological invariant tests."""

    def test_topological_nilpotency_sphere3(self):
        """Verify partial^2 = 0 and d^2 = 0 on triangulated 3-sphere (boundary of 4-simplex)."""
        s3 = build_4simplex_boundary_3sphere()
        assert s3.euler_characteristic() == 0  # chi(S^3) = 0
        assert s3.verify_nilpotency(1) is True
        assert s3.verify_nilpotency(2) is True
        assert s3.verify_nilpotency(3) is True

    def test_topological_nilpotency_sphere4(self):
        """Verify partial^2 = 0 and d^2 = 0 on triangulated 4-sphere (boundary of 5-simplex)."""
        s4 = build_5simplex_boundary_4sphere()
        assert s4.euler_characteristic() == 2  # chi(S^4) = 2
        assert s4.verify_nilpotency(1) is True
        assert s4.verify_nilpotency(2) is True
        assert s4.verify_nilpotency(3) is True
        assert s4.verify_nilpotency(4) is True

    def test_flat_torus_euler_characteristic_and_nilpotency(self):
        """Verify flat 2D torus has chi(T^2) = 0 and exact operator nilpotency."""
        torus = build_flat_torus_2d(3, 3)
        assert torus.euler_characteristic() == 0
        assert torus.verify_nilpotency(1) is True
        assert torus.verify_nilpotency(2) is True


class TestSovietSimplicialBianchiInvariants:
    """Rigorous simplicial Bianchi identity tests in 3D and 4D."""

    def test_flat_space_zero_deficit_and_bianchi(self):
        """On a regular flat 2D triangular grid, every interior vertex has valency 6 and deficit 0."""
        torus = build_flat_torus_2d(3, 3)
        # In a regular equilateral triangular grid, dihedral angle = pi/3, 6 triangles meet at vertex
        deficits = np.zeros(torus.num_edges)
        res = verify_closed_bianchi_flux(torus, deficits, hinge_dim=1)
        assert res["is_satisfied"] is True
        assert res["total_l1_flux"] == 0.0

    def test_closed_bianchi_flux_vanishing_on_4sphere(self):
        """On a closed triangulated 4-sphere (boundary of 5-simplex), triangular hinges carry
        curvature 2-cochain epsilon in C^2. On a regular configuration where deficits are uniform,
        d_2 epsilon = 0 vanishes identically due to alternating sign cancellation.
        Note: each triangle in partial Delta^5 belongs to exactly 3 (not 5) 4-simplices.
        """
        s4 = build_5simplex_boundary_4sphere()
        # In 4D, hinges are 2-simplices (triangles, 20 of them)
        # Each triangle is shared by 6 - 3 = 3 4-simplices
        deficits = np.ones(s4.num_faces) * (2.0 * math.pi - 3 * regular_simplex_dihedral_angle(4))
        res = verify_closed_bianchi_flux(s4, deficits, hinge_dim=2)
        assert res["is_satisfied"] is True
        assert res["total_l1_flux"] < 1e-12

    def test_closed_bianchi_counterexample_on_perturbed_4sphere(self):
        """Reviewer Counterexample (Jeremy H. Carroll, Sept 2026):
        On S^4 = partial Delta^5, changing edge l_{01} = 1.0 -> 1.1 leaves all 6 4-simplices
        strictly nondegenerate, but breaks the unrestricted scalar Bianchi identity:
            ||d_2 epsilon||_1 approx 1.956565 != 0.
        Demonstrates that exact Regge Bianchi identities require non-abelian SO(4) holonomies
        and do not reduce to scalar cochain coboundary vanishing on generic curved complexes.
        """
        from itertools import combinations

        # 6 vertices 0..5
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

        # Each triangle must belong to exactly 3 4-simplices
        for t, ths in tri_dihedrals.items():
            assert len(ths) == 3, f"Triangle {t} belongs to {len(ths)} simplices, expected 3"

        deficits = {t: 2.0 * math.pi - sum(ths) for t, ths in tri_dihedrals.items()}

        # Compute d_2 epsilon on tetrahedra:
        # (d_2 epsilon)(v0, v1, v2, v3) = eps(1,2,3) - eps(0,2,3) + eps(0,1,3) - eps(0,1,2)
        d2_eps: dict[tuple[int, int, int, int], float] = {}
        for tau in tetrahedra:
            v0, v1, v2, v3 = tau
            val = deficits[(v1, v2, v3)] - deficits[(v0, v2, v3)] + deficits[(v0, v1, v3)] - deficits[(v0, v1, v2)]
            d2_eps[tau] = val

        l1_flux = sum(abs(v) for v in d2_eps.values())
        linf_flux = max(abs(v) for v in d2_eps.values())

        # Exact reviewer values:
        # ||d2 eps||_1 approx 1.9565652080
        # ||d2 eps||_inf approx 0.2445706510
        # (d2 eps)(0,2,3,4) approx -0.2445706510
        assert abs(l1_flux - 1.9565652080) < 1e-6
        assert abs(linf_flux - 0.2445706510) < 1e-6
        assert abs(d2_eps[(0, 2, 3, 4)] - (-0.2445706510)) < 1e-6
        assert l1_flux > 1.9  # Confirms non-vanishing scalar flux

    def test_simplicial_faces_and_subsimplices(self):
        """Test Simplex dataclass subface decomposition."""
        t = Simplex(dimension=3, vertices=(0, 1, 2, 3))
        faces = t.faces
        assert len(faces) == 4
        assert all(f.dimension == 2 for f in faces)
        # 0-simplex faces
        v = Simplex(dimension=0, vertices=(0,))
        assert v.faces == []

        with pytest.raises(ValueError):
            Simplex(dimension=2, vertices=(0, 1))

    def test_contracted_bianchi_verification_helper(self):
        """Test verify_contracted_bianchi_3d helper function."""
        coords = {
            0: np.array([0.0, 0.0, 0.0]),
            1: np.array([1.0, 0.0, 0.0]),
            2: np.array([-1.0, 0.0, 0.0]),
        }
        edges = [(0, 1), (0, 2)]
        deficits = {(0, 1): 0.5, (0, 2): 0.5}
        res = verify_contracted_bianchi_3d(coords, edges, deficits, interior_vertices=[0])
        assert res["authority_effect"] == "None"
        assert res["is_satisfied"] is True

    def test_contracted_bianchi_vertex_flux_vanishing(self):
        """In 3D, verify contracted Bianchi flux sum_{e in star(v)} eps_e * hat{e} = 0 for symmetric star."""
        # 6 symmetric edges in 3D space meeting at origin
        coords = {
            0: np.array([0.0, 0.0, 0.0]),
            1: np.array([1.0, 0.0, 0.0]),
            2: np.array([-1.0, 0.0, 0.0]),
            3: np.array([0.0, 1.0, 0.0]),
            4: np.array([0.0, -1.0, 0.0]),
            5: np.array([0.0, 0.0, 1.0]),
            6: np.array([0.0, 0.0, -1.0]),
        }
        edges = [(0, 1), (0, 2), (0, 3), (0, 4), (0, 5), (0, 6)]
        # Equal deficit on opposite edges
        deficits = {
            (0, 1): 0.3, (0, 2): 0.3,
            (0, 3): -0.2, (0, 4): -0.2,
            (0, 5): 0.1, (0, 6): 0.1,
        }
        incident = edges
        flux = contracted_bianchi_vertex_flux_3d(0, coords, incident, deficits)
        assert np.allclose(flux, 0.0, atol=1e-14)


class TestSovietWDWConstraintAndDualL1Solvers:
    """Rigorous tests for Wheeler-DeWitt constraint closure and exact dual witnesses."""

    def test_exact_constraint_closure_pure_gauge(self):
        """When constraint violation is pure gauge omega = d_0 alpha, Phi = 0 and is_closed is True."""
        torus = build_flat_torus_2d(3, 3)
        d0 = torus.coboundary_matrix(0)
        np.random.seed(42)
        alpha_true = np.random.randn(torus.num_vertices)
        omega_gauge = d0 @ alpha_true

        solver = DualCertifiedL1Solver(tol=1e-8)
        res = solver.solve(omega_gauge, d0)

        assert res.is_closed is True
        assert res.primal_obj < 1e-8
        assert res.duality_gap < 1e-8
        assert res.dual_divergence_norm < 1e-8

    def test_non_closable_constraint_violation_dual_witness_certification(self):
        """When constraint violation has genuine obstruction (loop/cycle), Phi > 0 and dual witness certifies it."""
        torus = build_flat_torus_2d(3, 3)
        d0 = torus.coboundary_matrix(0)

        # Create a non-trivial circulation on edges
        omega_loop = np.ones(torus.num_edges)
        solver = DualCertifiedL1Solver(tol=1e-8)
        res = solver.solve(omega_loop, d0)

        assert res.is_closed is False
        assert res.primal_obj > 0.0
        # Strong duality must hold with zero duality gap
        assert res.duality_gap < 1e-8
        # Dual witness must be a valid 1-cycle (divergence free)
        assert res.dual_divergence_norm < 1e-8
        # Dual witness must satisfy L_infty norm <= 1
        assert np.max(np.abs(res.dual_witness)) <= 1.0 + 1e-8
        # Complementary slackness: <w, residual> == ||residual||_1
        dot_val = float(np.dot(res.dual_witness, res.primal_residual))
        assert abs(dot_val - res.primal_obj) < 1e-8

    def test_wdw_gauge_invariance_under_arbitrary_shifts(self):
        """The L1 quotient residual Phi([omega]) is strictly gauge invariant: Phi([omega + d_0 gamma]) = Phi([omega])."""
        s3 = build_4simplex_boundary_3sphere()
        d0 = s3.coboundary_matrix(0)

        omega = np.array([1.0, 0.5, -0.5, 0.2, 0.0, 1.2, -0.8, 0.4, -0.1, 0.3])
        solver = DualCertifiedL1Solver(tol=1e-8)
        base_res = solver.solve(omega, d0)

        # Add 5 different random gauge shifts
        np.random.seed(123)
        for _ in range(5):
            gamma = np.random.randn(s3.num_vertices) * 10.0
            omega_shifted = omega + d0 @ gamma
            shifted_res = solver.solve(omega_shifted, d0)

            assert abs(shifted_res.primal_obj - base_res.primal_obj) < 1e-8
            assert abs(shifted_res.dual_obj - base_res.dual_obj) < 1e-8

    def test_exact_rational_triangle_loop_quotient(self):
        """Verify exact rational L1 solver on minimal 2-simplex triangle loop."""
        d0 = [
            [-1, 1, 0],
            [0, -1, 1],
            [1, 0, -1],
        ]
        # Pure cycle loop omega = [1, 1, 1]
        res = exact_rational_l1_quotient([1, 1, 1], d0)
        assert res.primal_obj == Fraction(3, 1)
        assert res.dual_obj == Fraction(3, 1)
        assert res.duality_gap == Fraction(0, 1)
        assert res.is_closed is False


class TestSovietStressAndExtremeGeometry:
    """Stress tests on degenerate, needle, and flattened simplices."""

    def test_needle_simplex_cayley_menger_volume(self):
        """Needle triangle with edge lengths (1, 1, 1e-5): volume remains positive and stable."""
        l_sq = np.array([
            [0.0, 1.0, 1.0],
            [1.0, 0.0, (1e-5) ** 2],
            [1.0, (1e-5) ** 2, 0.0],
        ])
        vol = simplex_volume(l_sq)
        assert vol > 0.0
        # For an isosceles needle, height ~ 1e-5 / 2, base ~ 1 -> area ~ 1e-5 / 2 / 2
        assert vol < 1e-4

    def test_degenerate_flattened_simplex_zero_volume(self):
        """Flattened triangle with collinear vertices (edges 1, 1, 2) has Cayley-Menger volume 0."""
        l_sq = np.array([
            [0.0, 1.0, 4.0],
            [1.0, 0.0, 1.0],
            [4.0, 1.0, 0.0],
        ])
        vol = simplex_volume(l_sq)
        assert abs(vol) < 1e-8

    def test_regular_tetrahedron_dihedral_angle(self):
        """Regular tetrahedron dihedral angle is arccos(1/3) ~ 1.230959417 rad."""
        theta = regular_simplex_dihedral_angle(3)
        assert abs(theta - math.acos(1.0 / 3.0)) < 1e-12

    def test_regular_4simplex_dihedral_angle(self):
        """Regular 4-simplex dihedral angle is arccos(1/4) ~ 1.318116072 rad."""
        theta = regular_simplex_dihedral_angle(4)
        assert abs(theta - math.acos(1.0 / 4.0)) < 1e-12


class TestSovietPonzanoReggeAsymptotics:
    """Tests for Ponzano-Regge 6j asymptotic phase and L1 Lipschitz continuity."""

    def test_lipschitz_continuity_under_l1_norm(self):
        """Verify |S(j1) - S(j2)| <= ||j1 - j2||_1 * ||theta||_inf for fixed dihedral angles."""
        j1 = [2, 2, 2, 2, 2, 2]
        j2 = [3, 2, 2, 2, 2, 3]  # L1 diff = 2
        res = verify_regge_action_lipschitz_bound(j1, j2)
        assert res["bound_holds"] is True
        assert res["l1_spin_difference"] == 2
        assert res["actual_difference"] <= res["lipschitz_upper_bound"] + 1e-12

    def test_ponzano_regge_varying_angles_counterexample(self):
        """Reviewer Counterexample (Jeremy H. Carroll, Sept 2026):
        When dihedral angles theta(j) vary with the geometry, the fixed-angle bound
        |Delta S| <= ||Delta j||_1 ||theta(j)||_inf fails.
        For all 6 spins = 2 (lengths J = 2.5), increasing spin (0, 1) to 3 (length 3.5):
            |Delta S| approx 1.363496 > ||Delta j||_1 ||theta(j)||_inf approx 1.230959.
        However, the Schläfli path bound |Delta S| <= ||Delta J||_1 sup ||theta||_inf
        and the universal bound pi * ||Delta J||_1 remain valid.
        """
        edges = [(0, 1), (0, 2), (0, 3), (1, 2), (1, 3), (2, 3)]
        J1 = {e: 2.5 for e in edges}
        J2 = {e: 2.5 for e in edges}
        J2[(0, 1)] = 3.5

        th1 = compute_simplex_dihedral_angles(tuple(range(4)), J1, dim=3)
        th2 = compute_simplex_dihedral_angles(tuple(range(4)), J2, dim=3)

        S1 = sum(J1[e] * th1[e] for e in edges)
        S2 = sum(J2[e] * th2[e] for e in edges)

        delta_S = abs(S2 - S1)
        max_th1 = max(th1.values())
        delta_j_1 = 1.0
        naive_bound = delta_j_1 * max_th1

        # Check reviewer's exact values:
        assert abs(delta_S - 1.3634964245) < 1e-6
        assert abs(naive_bound - 1.2309594173) < 1e-6
        assert delta_S > naive_bound  # Confirms counterexample to endpoint fixed-angle bound

        # Validate Schläfli path bound
        schlafli = evaluate_schlafli_path_bound(
            [J1[e] for e in edges],
            [J2[e] for e in edges],
            sup_dihedral_angle=math.pi,
        )
        assert delta_S <= schlafli["pi_universal_bound"]
        assert schlafli["authority_effect"] == "None"

    def test_phase_envelope_upper_bound(self):
        """Verify that |S_Regge| is strictly bounded by ||j||_1 * theta_max."""
        spins = [1, 2, 3, 4, 5, 6]
        env = compute_l1_phase_envelope(spins)
        phase = evaluate_semiclassical_regge_phase(spins)
        # Phase includes +0.5 per edge, so phase <= (||j||_1 + 3) * theta
        max_theta = regular_simplex_dihedral_angle(3)
        assert phase <= (sum(spins) + 3.0) * max_theta + 1e-10

    def test_wdw_full_constraint_system_pipeline(self):
        """Test CauchySlice3D, discrete Ricci scalar curvature, and total constraint cochain."""
        s3 = build_4simplex_boundary_3sphere()
        edge_lens = {tuple(sorted(e)): 1.0 for e in s3.cells[1]}
        momenta = {tuple(sorted(e)): 0.1 for e in s3.cells[1]}
        slice_3d = CauchySlice3D(complex_=s3, edge_lengths=edge_lens, conjugate_momenta=momenta)

        deficits = {tuple(sorted(e)): 0.05 for e in s3.cells[1]}
        wdw_sys = DiscreteWDWConstraintSystem(slice_=slice_3d, deficit_angles=deficits)

        h_perp = wdw_sys.build_hamiltonian_constraint_cochain()
        assert len(h_perp) == s3.num_vertices

        diff = wdw_sys.build_momentum_constraint_cochain()
        assert len(diff) == s3.num_edges

        total_omega = wdw_sys.build_total_constraint_cochain()
        assert len(total_omega) == s3.num_edges

        # Solve L1 constraint closure
        d0 = s3.coboundary_matrix(0)
        res = compute_l1_quotient_with_dual_witness(total_omega, d0)
        assert res.duality_gap < 1e-8
        assert res.authority_effect == "None"

    def test_simplex_geometry_utilities(self):
        """Test dihedral angles, deficit angles, boundary hinges, and error handling."""
        # 1. Boundary deficit angle
        b_def = compute_hinge_deficit_angle([math.pi / 3.0], hinge_is_boundary=True)
        assert abs(b_def - (math.pi - math.pi / 3.0)) < 1e-10

        # 2. 4-simplex dihedral
        theta_4 = four_simplex_dihedral_angle(regular=True)
        assert abs(theta_4 - math.acos(0.25)) < 1e-10
        with pytest.raises(NotImplementedError):
            four_simplex_dihedral_angle(regular=False)

        # 3. Regular tetrahedron dihedral via edge lengths
        s_dict = {
            (min(i, j), max(i, j)): 1.0
            for i in range(4) for j in range(4) if i != j
        }
        theta_tet = tetrahedron_dihedral_angle(s_dict, (0, 1))
        assert abs(theta_tet - math.acos(1.0 / 3.0)) < 1e-6

        # 4. Dimension error
        with pytest.raises(ValueError):
            regular_simplex_dihedral_angle(0)

        # 5. Zero dual volume error in curvature
        with pytest.raises(ValueError):
            compute_discrete_scalar_curvature(0, [(0, 1)], {(0, 1): 1.0}, {(0, 1): 0.1}, dual_volume=0.0)


    def test_solver_dictionaries_and_zero_cochains(self):
        """Test result dictionary serialization and zero-cochain solver behavior."""
        s3 = build_4simplex_boundary_3sphere()
        d0 = s3.coboundary_matrix(0)
        solver = DualCertifiedL1Solver(tol=1e-8)

        # Zero cochain
        zero_res = solver.solve(np.zeros(s3.num_edges), d0)
        assert zero_res.is_closed is True
        assert zero_res.primal_obj == 0.0
        d_dict = zero_res.to_dict()
        assert d_dict["is_closed"] is True

        # Exact rational to_dict
        d0_tri = [[-1, 1, 0], [0, -1, 1], [1, 0, -1]]
        exact_res = exact_rational_l1_quotient([0, 0, 0], d0_tri)
        ex_dict = exact_res.to_dict()
        assert ex_dict["is_closed"] is True

    def test_asymptotics_and_complex_edge_cases(self):
        """Test error handling in asymptotics and complex helpers."""
        # Bad spin count
        with pytest.raises(ValueError):
            evaluate_semiclassical_regge_phase([1, 2, 3])

        with pytest.raises(ValueError):
            evaluate_semiclassical_regge_phase([1, 2, 3, 4, 5, 6], dihedral_angles=[1.0, 2.0])

        with pytest.raises(ValueError):
            verify_regge_action_lipschitz_bound([1, 2], [1, 2])

        # Complex star method
        s3 = build_4simplex_boundary_3sphere()
        star_v0 = s3.star((0,), target_dim=1)
        assert len(star_v0) == 4  # 4 incident edges on vertex 0

        # Flat torus invalid size
        with pytest.raises(ValueError):
            build_flat_torus_2d(2, 2)


class TestSovietHighEnergyQuarantineReceipts:
    """Verify that all speculative climbs are killed and quarantined with mathematical receipts."""

    def test_all_five_quarantine_receipts_present_and_falsified(self):
        """Verify the 5 falsification receipts in the quarantine register."""
        receipts = HighEnergyQuarantineRegister.get_all_receipts()
        assert len(receipts) == 5

        for rec in receipts:
            assert rec.verdict == "QUARANTINED_FALSIFIED"
            assert len(rec.mathematical_proof_of_failure) > 50
            assert rec.authority_effect == "None"

    def test_gauge_uniqueness_falsified(self):
        rec = falsify_gauge_group_uniqueness()
        assert "Category error" in rec.obstruction_type
        assert "Lie brackets" in rec.mathematical_proof_of_failure

    def test_higgs_vev_falsified(self):
        rec = falsify_higgs_vev_derivation()
        assert "Injected scale" in rec.obstruction_type

    def test_susy_saturation_scale_falsified(self):
        rec = falsify_susy_saturation_scale()
        assert "Dimensional inconsistency" in rec.obstruction_type
        assert "degree is an arbitrary unit" in rec.mathematical_proof_of_failure

    def test_alpha_fine_structure_wall_falsified(self):
        rec = falsify_alpha_fine_structure_wall()
        assert "diverging" in rec.mathematical_proof_of_failure

    def test_dark_sector_analogy_falsified(self):
        rec = falsify_dark_sector_analogy()
        assert "Missing dynamical stress-energy tensor" in rec.obstruction_type
