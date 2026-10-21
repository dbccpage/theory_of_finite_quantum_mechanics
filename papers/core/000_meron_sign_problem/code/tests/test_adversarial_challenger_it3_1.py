"""test_adversarial_challenger_it3_1.py: Empirical Stress Suite for Iteration 3 Remediations.
AuthorityEffect: None.

Adversarial stress harness challenging:
1. 3D loops: extreme winding numbers, complex interlocking links, unlinked multi-loop systems.
2. 4D half-instantons: high-charge sectors, large symmetric clusters, mixed ensembles.
3. Proper pairing & cancellation: (1 + (-1)) w(C) = 0 with exact Fraction(0, 1) duality gap.
4. Neutral vacuum sectors: Q=0 strictly positive and never falsely rejected.
5. Mixed ensembles: dense mixtures of 3D loops and 4D instantons with large coprime rational weights.
6. Zero float conversions: strict Fraction and int arithmetic.
"""

from __future__ import annotations

import ast
import os
from fractions import Fraction

import pytest

from topological_cluster_4d_solver import (
    TopologicalCluster4DSolver,
    execute_involution_cancellation,
)
from topological_half_instanton_4d import (
    HalfInstantonCluster4D,
    fermion_determinant_sign,
    orientation_flip,
    second_chern_number,
)
from topological_meron_3d import (
    ClosedStringLoop3D,
    build_hopf_link_pair,
    build_unlinked_pair,
    discrete_gauss_linking_number,
    exact_linking_matrix,
    facet_intersection_linking_number,
    linking_number,
    loop_involution_tau,
    winding_parity,
)


def _build_winding_loop_3d(
    wx: int,
    wy: int,
    wz: int,
    lattice_dim: tuple[int, int, int] = (4, 4, 4),
    loop_id: str = "loop_winding",
) -> ClosedStringLoop3D:
    """Adversarial generator for 3D closed loop with exact winding (wx, wy, wz)."""
    lx, ly, lz = lattice_dim
    x, y, z = 0, 0, 0
    pts = [(x % lx, y % ly, z % lz)]

    if wx != 0:
        step_x = 1 if wx > 0 else -1
        for _ in range(abs(wx) * lx):
            x += step_x
            pts.append((x % lx, y % ly, z % lz))

    if wy != 0:
        step_y = 1 if wy > 0 else -1
        for _ in range(abs(wy) * ly):
            y += step_y
            pts.append((x % lx, y % ly, z % lz))

    if wz != 0:
        step_z = 1 if wz > 0 else -1
        for _ in range(abs(wz) * lz):
            z += step_z
            pts.append((x % lx, y % ly, z % lz))

    return ClosedStringLoop3D(id=loop_id, coordinates=pts, lattice_dim=lattice_dim)


# ===========================================================================
# 1. 3D Meron String Loops: Extreme Winding & Linking
# ===========================================================================


class TestExtremeWinding3D:
    """Stress tests 3D string loops with extreme winding numbers and topology."""

    def test_extreme_winding_vector_5_neg7_11(self) -> None:
        """Tests loop with W = (5, -7, 11). Parity = (5 - 7 + 11) % 2 = 1."""
        loop = _build_winding_loop_3d(5, -7, 11, lattice_dim=(4, 4, 4), loop_id="extreme_odd")
        assert loop.winding_vector == (5, -7, 11)
        assert loop.winding_parity == 1
        assert winding_parity(loop) == 1
        assert not loop.is_contractible

        tau_loop = loop_involution_tau(loop)
        assert tau_loop.winding_vector == (-5, 7, -11)
        assert tau_loop.winding_parity == 1

        # Cancellation in solver
        canc = execute_involution_cancellation([loop, tau_loop])
        assert canc.odd_sectors_cancelled == 2
        assert canc.duality_gap == Fraction(0, 1)
        assert canc.odd_sum == Fraction(0, 1)
        assert canc.status == "EXACT_REPAIR"

    def test_extreme_winding_vector_100_101_102(self) -> None:
        """Tests large winding loop W = (100, 101, 102). Parity = 303 % 2 = 1."""
        loop = _build_winding_loop_3d(100, 101, 102, lattice_dim=(4, 4, 4), loop_id="huge_loop")
        assert loop.winding_vector == (100, 101, 102)
        assert loop.winding_parity == 1

        tau_loop = loop_involution_tau(loop)
        assert tau_loop.winding_vector == (-100, -101, -102)

        weight = Fraction(3141592653589793, 2718281828459045)
        canc = execute_involution_cancellation([loop, tau_loop], [weight, weight])
        assert canc.odd_sectors_cancelled == 2
        assert canc.duality_gap == Fraction(0, 1)
        assert canc.status == "EXACT_REPAIR"

    def test_even_extreme_winding_remains_in_even_sector(self) -> None:
        """Tests even winding loops: W = (50, -50, 0) and W = (12, 14, 16)."""
        loop_even = _build_winding_loop_3d(50, -50, 0, lattice_dim=(4, 4, 4), loop_id="even_wind")
        assert loop_even.winding_vector == (50, -50, 0)
        assert loop_even.winding_parity == 0

        # Even loop does not require cancellation, contributes +w to even sum
        w = Fraction(42, 1)
        canc = execute_involution_cancellation([loop_even], [w])
        assert canc.odd_sectors_cancelled == 0
        assert canc.zero_sectors_positive is True
        assert canc.total_partition_sum == w
        assert canc.duality_gap == Fraction(0, 1)
        assert canc.status == "EXACT_REPAIR"


class TestComplexInterlockingLinks3D:
    """Stress tests complex interlocking links and unlinked systems."""

    def test_hopf_link_exact_invariants(self) -> None:
        """Verifies Hopf link pair linking number Lk in {-1, 1}."""
        l1, l2 = build_hopf_link_pair(origin=(1, 1, 1), lattice_dim=(6, 6, 6))
        lk_gauss = discrete_gauss_linking_number(l1, l2)
        lk_facet = facet_intersection_linking_number(l1, l2)
        assert abs(lk_gauss) == 1
        assert lk_gauss == lk_facet
        assert linking_number(l1, l2) == lk_gauss

    def test_unlinked_pair_zero_linking(self) -> None:
        """Verifies unlinked disjoint loops have Lk = 0."""
        u1, u2 = build_unlinked_pair(lattice_dim=(8, 8, 8))
        assert linking_number(u1, u2) == 0
        assert discrete_gauss_linking_number(u1, u2) == 0
        assert facet_intersection_linking_number(u1, u2) == 0

    def test_three_component_link_chain(self) -> None:
        """Verifies a 3-component link chain: L1 links L2, L2 links L3, L1 unlinked from L3."""
        lattice = (16, 16, 16)
        l1_pts = [
            (1, 1, 2), (2, 1, 2), (3, 1, 2), (4, 1, 2), (5, 1, 2),
            (5, 2, 2), (5, 3, 2), (5, 4, 2), (5, 5, 2),
            (4, 5, 2), (3, 5, 2), (2, 5, 2), (1, 5, 2),
            (1, 4, 2), (1, 3, 2), (1, 2, 2),
        ]
        l1 = ClosedStringLoop3D("L1", l1_pts, lattice_dim=lattice)

        l2_pts = [
            (3, 3, 1), (3, 3, 2), (3, 3, 3), (3, 3, 4), (3, 3, 5), (3, 3, 6), (3, 3, 7),
            (3, 4, 7), (3, 5, 7), (3, 6, 7), (3, 7, 7),
            (3, 7, 6), (3, 7, 5), (3, 7, 4), (3, 7, 3), (3, 7, 2), (3, 7, 1),
            (3, 6, 1), (3, 5, 1), (3, 4, 1),
        ]
        l2 = ClosedStringLoop3D("L2", l2_pts, lattice_dim=lattice)

        l3_pts = [
            (1, 5, 6), (2, 5, 6), (3, 5, 6), (4, 5, 6), (5, 5, 6),
            (5, 6, 6), (5, 7, 6), (5, 8, 6), (5, 9, 6),
            (4, 9, 6), (3, 9, 6), (2, 9, 6), (1, 9, 6),
            (1, 8, 6), (1, 7, 6), (1, 6, 6),
        ]
        l3 = ClosedStringLoop3D("L3", l3_pts, lattice_dim=lattice)

        mat = exact_linking_matrix([l1, l2, l3])
        # Check symmetric integer matrix with 0 diagonal
        assert mat[0][0] == 0 and mat[1][1] == 0 and mat[2][2] == 0
        assert mat[0][1] == mat[1][0]
        assert mat[1][2] == mat[2][1]
        assert mat[0][2] == mat[2][0]

        # Topological chain structure
        assert abs(mat[0][1]) == 1
        assert abs(mat[1][2]) == 1
        assert mat[0][2] == 0

    def test_multi_hopf_disjoint_systems(self) -> None:
        """Verifies 4-loop system with two disjoint Hopf pairs."""
        lattice = (12, 12, 12)
        h1a, h1b = build_hopf_link_pair(origin=(1, 1, 1), lattice_dim=lattice)
        h2a, h2b = build_hopf_link_pair(origin=(7, 7, 7), lattice_dim=lattice)

        mat = exact_linking_matrix([h1a, h1b, h2a, h2b])
        assert abs(mat[0][1]) == 1 and abs(mat[1][0]) == 1
        assert abs(mat[2][3]) == 1 and abs(mat[3][2]) == 1
        assert mat[0][2] == 0 and mat[0][3] == 0
        assert mat[1][2] == 0 and mat[1][3] == 0


# ===========================================================================
# 2. 4D Half-Instantons: High-Charge & Symmetric Sectors
# ===========================================================================


class TestHalfInstantons4D:
    """Stress tests high-charge, symmetric, and odd half-instanton sectors."""

    def test_high_charge_integer_sector(self) -> None:
        """Tests high-charge sector N_+ = 50, N_- = 0: c_2 = 25 in Z."""
        c = HalfInstantonCluster4D(50, 0, weight=Fraction(999, 1))
        assert second_chern_number(c) == Fraction(25, 1)
        assert c.is_integer_charge is True
        assert c.is_half_integer_charge is False
        assert fermion_determinant_sign(c) == 1

        # Integer charge sector behaves as even/positive sector
        canc = execute_involution_cancellation([c])
        assert canc.odd_sectors_cancelled == 0
        assert canc.zero_sectors_positive is True
        assert canc.total_partition_sum == Fraction(999, 1)
        assert canc.duality_gap == Fraction(0, 1)
        assert canc.status == "EXACT_REPAIR"

    def test_high_charge_half_integer_sector(self) -> None:
        """Tests high-charge odd sector N_+ = 51, N_- = 0: c_2 = 51/2 in (1/2)Z \\ Z."""
        c = HalfInstantonCluster4D(51, 0, weight=Fraction(17, 3))
        assert second_chern_number(c) == Fraction(51, 2)
        assert c.is_half_integer_charge is True
        assert fermion_determinant_sign(c) == -1

        tau_c = orientation_flip(c)
        assert second_chern_number(tau_c) == Fraction(-51, 2)
        assert fermion_determinant_sign(tau_c) == 1
        assert tau_c.weight == c.weight

        canc = execute_involution_cancellation([c, tau_c])
        assert canc.odd_sectors_cancelled == 2
        assert canc.duality_gap == Fraction(0, 1)
        assert canc.odd_sum == Fraction(0, 1)
        assert canc.status == "EXACT_REPAIR"

    def test_large_symmetric_cluster_q_zero(self) -> None:
        """Tests large symmetric cluster N_+ = 25, N_- = 25: Q = 0."""
        c = HalfInstantonCluster4D(25, 25, weight=Fraction(100, 1))
        assert second_chern_number(c) == Fraction(0, 1)
        assert c.is_zero_charge is True
        assert fermion_determinant_sign(c) == 1

        canc = execute_involution_cancellation([c])
        assert canc.zero_sectors_positive is True
        assert canc.duality_gap == Fraction(0, 1)
        assert canc.total_partition_sum == Fraction(100, 1)
        assert canc.status == "EXACT_REPAIR"

    def test_very_large_symmetric_cluster_100_100(self) -> None:
        """Tests massive symmetric cluster N_+ = 100, N_- = 100."""
        c = HalfInstantonCluster4D(100, 100, weight=Fraction(1234567, 89))
        assert second_chern_number(c) == Fraction(0, 1)
        assert c.is_zero_charge is True
        assert fermion_determinant_sign(c) == 1

        canc = execute_involution_cancellation([c])
        assert canc.zero_sectors_positive is True
        assert canc.duality_gap == Fraction(0, 1)
        assert canc.total_partition_sum == Fraction(1234567, 89)
        assert canc.status == "EXACT_REPAIR"

    def test_involution_involution_identity(self) -> None:
        """Verifies tau(tau(C)) == C across diverse clusters."""
        clusters = [
            HalfInstantonCluster4D(1, 0, weight=Fraction(1, 3)),
            HalfInstantonCluster4D(0, 1, weight=Fraction(2, 5)),
            HalfInstantonCluster4D(7, 4, weight=Fraction(11, 7)),
            HalfInstantonCluster4D(50, 0, weight=Fraction(9, 2)),
            HalfInstantonCluster4D(25, 25, weight=Fraction(13, 1)),
        ]
        for c in clusters:
            tau_c = orientation_flip(c)
            tau_tau_c = orientation_flip(tau_c)
            assert tau_tau_c.n_plus == c.n_plus
            assert tau_tau_c.n_minus == c.n_minus
            assert tau_tau_c.sign_factor == c.sign_factor
            assert tau_tau_c.weight == c.weight
            assert fermion_determinant_sign(tau_tau_c) == fermion_determinant_sign(c)


# ===========================================================================
# 3. Proper Pairing and Zero Duality Gap
# ===========================================================================


class TestProperPairingCancellation:
    """Stress tests pairwise cancellation: (1 + (-1)) w(C) = 0 and fail-closed defects."""

    @pytest.mark.parametrize(
        "n_plus,n_minus,weight",
        [
            (1, 0, Fraction(1, 1)),
            (0, 1, Fraction(7, 3)),
            (3, 0, Fraction(11, 13)),
            (2, 1, Fraction(101, 97)),
            (7, 4, Fraction(355, 113)),
            (17, 8, Fraction(1000000007, 998244353)),
            (51, 0, Fraction(123456789, 987654321)),
        ],
    )
    def test_exact_zero_sum_doublet_fraction_zero(
        self, n_plus: int, n_minus: int, weight: Fraction
    ) -> None:
        """Verifies (1 + (-1)) w(C) = 0 identically with exact zero duality gap."""
        solver = TopologicalCluster4DSolver()
        c = HalfInstantonCluster4D(n_plus, n_minus, weight=weight)
        tau_c = orientation_flip(c)

        s1 = fermion_determinant_sign(c)
        s2 = fermion_determinant_sign(tau_c)
        assert s1 == -1
        assert s2 == 1
        assert (s1 + s2) * weight == Fraction(0, 1)

        # verify_zero_sum_doublet method on solver
        d_info = solver.verify_zero_sum_doublet((c, tau_c))
        assert d_info["exact_zero_sum_doublet"] is True
        assert d_info["duality_gap"] == "0"
        assert d_info["weight_preserved"] is True
        assert d_info["involution_intact"] is True

        # Standalone verify_zero_sum_doublet from topological_half_instanton_4d
        from topological_half_instanton_4d import (
            verify_zero_sum_doublet as verify_instanton_doublet,
        )
        inst_info = verify_instanton_doublet(c)
        assert inst_info["exact_zero_sum_doublet"] is True
        assert inst_info["duality_gap"] == "0"
        assert inst_info["pair_weighted_sum"] == "0"

        # verify_doublet_rop ROP method
        rop_res = solver.verify_doublet_rop((c, tau_c))
        assert rop_res.is_ok

        # execute_involution_cancellation
        canc = execute_involution_cancellation([c, tau_c])
        assert canc.odd_sectors_cancelled == 2
        assert canc.duality_gap == Fraction(0, 1)
        assert canc.odd_sum == Fraction(0, 1)
        assert canc.status == "EXACT_REPAIR"

    def test_forged_partner_perturbed_sign_fails_closed(self) -> None:
        """Verifies that partner with identical sign is rejected with typed refusal."""
        solver = TopologicalCluster4DSolver()
        c = HalfInstantonCluster4D(1, 0, weight=Fraction(5, 3))
        # Forged partner: swapped centers but sign_factor=1 (both signs = -1)
        c_forged = HalfInstantonCluster4D(0, 1, weight=Fraction(5, 3), sign_factor=1)

        rop_res = solver.verify_doublet_rop((c, c_forged))
        assert rop_res.is_err
        refusal = rop_res.unwrap_err()
        assert refusal.code == "REFUSAL_SIGN_PERTURBED"

        canc = execute_involution_cancellation([c, c_forged])
        assert canc.duality_gap == 2 * Fraction(5, 3)
        assert canc.status == "UNREPAIRED_OBSTRUCTION"
        assert canc.odd_sectors_cancelled == 0

    def test_asymmetric_weight_fails_closed(self) -> None:
        """Verifies that partner with unequal weight produces non-zero duality gap."""
        solver = TopologicalCluster4DSolver()
        w1 = Fraction(10, 1)
        w2 = Fraction(11, 1)
        c = HalfInstantonCluster4D(1, 0, weight=w1)
        tau_c = HalfInstantonCluster4D(0, 1, weight=w2, sign_factor=-1)

        rop_res = solver.verify_doublet_rop((c, tau_c))
        assert rop_res.is_err
        assert rop_res.unwrap_err().code == "REFUSAL_WEIGHT_ASYMMETRY"

        canc = execute_involution_cancellation([c, tau_c])
        assert canc.status == "UNREPAIRED_OBSTRUCTION"
        assert canc.duality_gap == abs(w2 - w1)


# ===========================================================================
# 4. Neutral Vacuum Sectors: Strict Positivity
# ===========================================================================


class TestNeutralVacuumSectors:
    """Stress tests neutral vacuum sectors Q = 0 (N_+ = N_-)."""

    def test_multiple_vacuum_sectors_positivity(self) -> None:
        """Verifies dense ensemble of Q=0 sectors is strictly positive and never rejected."""
        vacuum_sectors = [
            HalfInstantonCluster4D(0, 0, weight=Fraction(1, 2)),
            HalfInstantonCluster4D(1, 1, weight=Fraction(3, 4)),
            HalfInstantonCluster4D(2, 2, weight=Fraction(5, 6)),
            HalfInstantonCluster4D(10, 10, weight=Fraction(11, 12)),
            HalfInstantonCluster4D(50, 50, weight=Fraction(100, 1)),
        ]
        for vac in vacuum_sectors:
            assert vac.is_zero_charge is True
            assert fermion_determinant_sign(vac) == 1

        expected_total = sum(v.weight for v in vacuum_sectors)
        canc = execute_involution_cancellation(vacuum_sectors)
        assert canc.zero_sectors_positive is True
        assert canc.odd_sectors_cancelled == 0
        assert canc.duality_gap == Fraction(0, 1)
        assert canc.total_partition_sum == expected_total
        assert canc.status == "EXACT_REPAIR"

    def test_isolated_vacuum_sector(self) -> None:
        """Verifies single vacuum sector has zero duality gap and positive partition sum."""
        v = HalfInstantonCluster4D(0, 0, weight=Fraction(7, 11))
        canc = execute_involution_cancellation([v])
        assert canc.zero_sectors_positive is True
        assert canc.duality_gap == Fraction(0, 1)
        assert canc.total_partition_sum == Fraction(7, 11)
        assert canc.status == "EXACT_REPAIR"


# ===========================================================================
# 5. Mixed Ensembles: Dense Mixtures with Coprime Weights
# ===========================================================================


class TestDenseMixedEnsembles:
    """Stress tests dense mixtures of 3D loops and 4D instantons with large coprime weights."""

    def test_dense_mixed_ensemble_exact_repair(self) -> None:
        """Constructs dense mixture of odd 3D loops, odd 4D instantons, and neutral vacuum sectors."""
        # Odd 4D instanton pairs
        w_4d_1 = Fraction(1000000007, 998244353)
        c1 = HalfInstantonCluster4D(17, 4, weight=w_4d_1)
        tau_c1 = orientation_flip(c1)

        w_4d_2 = Fraction(123456789, 987654321)
        c2 = HalfInstantonCluster4D(3, 0, weight=w_4d_2)
        tau_c2 = orientation_flip(c2)

        # Odd 3D loop pairs
        w_3d_1 = Fraction(314159265, 271828182)
        l1 = _build_winding_loop_3d(5, -7, 11, loop_id="l1_odd")
        tau_l1 = loop_involution_tau(l1)

        w_3d_2 = Fraction(8675309, 1000003)
        l2 = _build_winding_loop_3d(100, 101, 102, loop_id="l2_odd")
        tau_l2 = loop_involution_tau(l2)

        # Neutral 4D vacuum sectors
        w_vac1 = Fraction(500000000, 1000000001)
        vac1 = HalfInstantonCluster4D(10, 10, weight=w_vac1)

        w_vac2 = Fraction(7777777, 8888889)
        vac2 = HalfInstantonCluster4D(4, 2, weight=w_vac2)  # Even charge 4-2=2

        # Even 3D loop
        w_loop_even = Fraction(9999991, 10000019)
        l_even = _build_winding_loop_3d(2, 4, 6, loop_id="l_even")

        clusters = [c1, tau_c1, c2, tau_c2, l1, tau_l1, l2, tau_l2, vac1, vac2, l_even]
        weights = [w_4d_1, w_4d_1, w_4d_2, w_4d_2, w_3d_1, w_3d_1, w_3d_2, w_3d_2, w_vac1, w_vac2, w_loop_even]

        canc = execute_involution_cancellation(clusters, weights)
        expected_even_sum = w_vac1 + w_vac2 + w_loop_even

        assert canc.odd_sectors_cancelled == 8
        assert canc.zero_sectors_positive is True
        assert canc.duality_gap == Fraction(0, 1)
        assert canc.odd_sum == Fraction(0, 1)
        assert canc.zero_sum == expected_even_sum
        assert canc.total_partition_sum == expected_even_sum
        assert canc.status == "EXACT_REPAIR"

    def test_dense_mixed_ensemble_hostile_weight_tamper(self) -> None:
        """Tampering with a single weight in mixed ensemble triggers fail-closed obstruction."""
        w1 = Fraction(1000000007, 998244353)
        c1 = HalfInstantonCluster4D(17, 4, weight=w1)
        tau_c1 = orientation_flip(c1)

        w2 = Fraction(314159265, 271828182)
        l1 = _build_winding_loop_3d(5, -7, 11, loop_id="l1_odd")
        tau_l1 = loop_involution_tau(l1)

        w_vac = Fraction(500000000, 1000000001)
        vac = HalfInstantonCluster4D(10, 10, weight=w_vac)

        clusters = [c1, tau_c1, l1, tau_l1, vac]
        # Perturb weight of c1
        delta = Fraction(1, 1000000000)
        tampered_weights = [w1 + delta, w1, w2, w2, w_vac]

        canc = execute_involution_cancellation(clusters, tampered_weights)
        assert canc.status == "UNREPAIRED_OBSTRUCTION"
        assert canc.duality_gap == delta

    def test_dense_mixed_ensemble_dropped_partner(self) -> None:
        """Dropping a partner leaves an odd cluster unpaired with non-zero duality gap."""
        w1 = Fraction(1000000007, 998244353)
        c1 = HalfInstantonCluster4D(17, 4, weight=w1)

        w2 = Fraction(314159265, 271828182)
        l1 = _build_winding_loop_3d(5, -7, 11, loop_id="l1_odd")
        tau_l1 = loop_involution_tau(l1)

        w_vac = Fraction(500000000, 1000000001)
        vac = HalfInstantonCluster4D(10, 10, weight=w_vac)

        # c1 is unpaired
        clusters = [c1, l1, tau_l1, vac]
        weights = [w1, w2, w2, w_vac]

        canc = execute_involution_cancellation(clusters, weights)
        assert canc.status == "UNREPAIRED_OBSTRUCTION"
        assert canc.duality_gap == w1


# ===========================================================================
# 6. Zero Floating-Point Conversions AST Audit
# ===========================================================================


class TestZeroFloatPurity:
    """AST audit asserting zero float constants or float() calls across core modules."""

    def test_zero_float_ast_purity_across_core_modules(self) -> None:
        """Inspects AST of all 4 core project files to assert 100% float-free code."""
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        core_files = [
            "topological_meron_3d.py",
            "topological_half_instanton_4d.py",
            "topological_cluster_4d_solver.py",
            "adversarial_topological_audit.py",
        ]
        violations = []
        for fname in core_files:
            fpath = os.path.join(base_dir, fname)
            assert os.path.exists(fpath), f"File {fpath} does not exist"
            with open(fpath, "r", encoding="utf-8") as fh:
                tree = ast.parse(fh.read(), filename=fpath)
            for node in ast.walk(tree):
                if isinstance(node, ast.Constant) and type(node.value) is float:
                    violations.append((fname, node.lineno, f"Float constant: {node.value}"))
                elif isinstance(node, ast.Call) and getattr(node.func, "id", None) == "float":
                    violations.append((fname, node.lineno, "Call to float()"))

        assert len(violations) == 0, f"Found float violations: {violations}"
