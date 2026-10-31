"""
Integration Tests for Higher-Form 2-Gauge Defect Networks and Continuous Foliated Fracton Order.

Paper: 002_projection_obstruction/023_fermion_sign_and_computational_hardness
Test File: test_foliated_fracton_2gauge_defects.py
AuthorityEffect: None
"""

from pathlib import Path
import sys
import math
import pytest
import numpy as np

code_dir = Path(__file__).resolve().parent.parent.parent
if str(code_dir) not in sys.path:
    sys.path.insert(0, str(code_dir))

from fractions import Fraction
import random

from src.fsp.foliated_fracton_2gauge_defects import (
    FoliatedFractonConfig,
    FoliatedFractonEngine,
    FoliationDirection,
    ExcitationMobility,
    FractonDefect,
    SubsystemChargeRegistry,
    TerminalRoute,
    HingeLineonSignCertifier,
    Lineon1DState,
)


class TestFoliatedFracton2GaugeDefects:
    """Integration test suite for foliated fracton order and 2-gauge defect networks."""

    def setup_method(self) -> None:
        self.config = FoliatedFractonConfig(
            lx=4,
            ly=4,
            lz=4,
            kappa_subsystem_penalty=2.0,
            k_level=2,
            temperature=1.0,
        )
        self.engine = FoliatedFractonEngine(self.config)

    def test_subsystem_charge_registry_neutrality(self) -> None:
        """Verifies that an empty or balanced dipole configuration is subsystem neutral."""
        registry = SubsystemChargeRegistry(lx=4, ly=4, lz=4)
        assert registry.is_subsystem_neutral()
        assert registry.count_active_leaves() == 0

        d1 = FractonDefect(
            defect_id=1,
            mobility=ExcitationMobility.PLANON,
            position=(1, 1, 1),
            charge=+1,
            leaf_direction=FoliationDirection.XY,
        )
        d2 = FractonDefect(
            defect_id=2,
            mobility=ExcitationMobility.PLANON,
            position=(2, 2, 1),
            charge=-1,
            leaf_direction=FoliationDirection.XY,
        )
        registry.add_defect(d1)
        registry.add_defect(d2)

        assert registry.charges_xy[1] == 0

    def test_planon_dipole_exact_repair(self) -> None:
        """Verifies that neutral planon dipoles inside a single leaf route to EXACT_REPAIR."""
        res = self.engine.evaluate_neutral_planon_dipoles(z_leaf=0)
        assert res.terminal_route == TerminalRoute.EXACT_REPAIR
        assert res.defect_mass_phi1 == 0.0
        assert res.curvature_gamma2 == 0.0
        assert res.subsystem_action_gap == 0.0
        assert res.average_sign == 1.0
        assert res.is_foliated_projection_successful is True

    def test_isolated_fracton_extensive_action_gap(self) -> None:
        """Verifies that hopping an isolated fracton across leaves induces an action gap."""
        res = self.engine.evaluate_isolated_fracton_separation(separation_z=3)
        assert res.terminal_route == TerminalRoute.SPLIT_BRAIN_REFUSAL
        assert res.subsystem_action_gap > 0.0
        assert res.defect_mass_phi1 > 0.0
        assert res.curvature_gamma2 == 0.0
        assert res.average_sign == 0.0
        assert res.is_foliated_projection_successful is False

    def test_action_gap_scaling_with_separation(self) -> None:
        """Verifies that the subsystem action gap scales with separation distance."""
        res_sep1 = self.engine.evaluate_isolated_fracton_separation(separation_z=1)
        res_sep3 = self.engine.evaluate_isolated_fracton_separation(separation_z=3)
        assert res_sep3.subsystem_action_gap >= res_sep1.subsystem_action_gap

    def test_abelian_intersecting_2gauge_sheets(self) -> None:
        """Verifies that abelian 2-gauge defect sheets commute and route to EXACT_REPAIR."""
        res = self.engine.evaluate_intersecting_2gauge_defects(is_nonabelian=False)
        assert res.terminal_route == TerminalRoute.EXACT_REPAIR
        assert res.defect_mass_phi1 == 0.0
        assert res.curvature_gamma2 == 0.0
        assert res.average_sign == 1.0
        assert res.details["trace"] == 2.0

    def test_nonabelian_intersecting_2gauge_sheets(self) -> None:
        """Verifies that non-abelian 2-gauge sheets produce negative trace and OPEN_SIGN_OBSTRUCTION."""
        res = self.engine.evaluate_intersecting_2gauge_defects(is_nonabelian=True)
        assert res.terminal_route == TerminalRoute.OPEN_SIGN_OBSTRUCTION
        assert res.defect_mass_phi1 == 2.0
        assert res.curvature_gamma2 == pytest.approx(math.pi)
        assert res.average_sign == -1.0
        assert res.details["trace"] == -2.0

    def test_foliated_projection_decoupled_sheets(self) -> None:
        """Verifies that foliated quantum double projection repairs decoupled 2-gauge sheets."""
        res = self.engine.evaluate_foliated_categorical_projection(has_corner_lineon_turn=False)
        assert res.terminal_route == TerminalRoute.EXACT_REPAIR
        assert res.defect_mass_phi1 == 0.0
        assert res.curvature_gamma2 == 0.0
        assert res.average_sign == 1.0
        assert res.is_foliated_projection_successful is True
        assert res.details["projected_trace"] >= 0.0

    def test_foliated_projection_corner_lineon_obstruction(self) -> None:
        """Verifies that corner lineon turns obstruct foliated factorization."""
        res = self.engine.evaluate_foliated_categorical_projection(has_corner_lineon_turn=True)
        assert res.terminal_route == TerminalRoute.OPEN_SIGN_OBSTRUCTION
        assert res.defect_mass_phi1 == 2.0
        assert res.curvature_gamma2 == pytest.approx(math.pi)
        assert res.average_sign == -1.0
        assert res.is_foliated_projection_successful is False
        assert res.details["projected_trace"] < 0.0

    def test_lineon_1d_state_ordering(self) -> None:
        """Verifies that Lineon1DState enforces strict coordinate ordering."""
        valid_state = Lineon1DState(pos1=1, pos2=3)
        assert valid_state.pos1 == 1 and valid_state.pos2 == 3

        with pytest.raises(ValueError):
            Lineon1DState(pos1=3, pos2=3)

        with pytest.raises(ValueError):
            Lineon1DState(pos1=4, pos2=2)

    def test_hinge_sign_elimination(self) -> None:
        """
        Comprehensive test for TFQ-1219 (FSP-HINGE-LINEON-SIGN-CLAIM):
        1. 1D collision avoidance invariant across 100 randomized valid hop sequences.
        2. Discrete IVT exchange refusal: confirms that any permutation requires a collision site.
        3. Exact trace values Tr(M) in {+2, -2} over Q(i).
        4. 5-fold BQNF terminal routing consistency.
        5. Trivial worldline permutation parity (+1).
        """
        # 1. 100 randomized valid hop sequences
        rng = random.Random(42)
        for _ in range(100):
            p1 = rng.randint(-20, 0)
            p2 = rng.randint(1, 20)
            hops = []
            curr1, curr2 = p1, p2
            for _ in range(15):
                # Choose hop delta that maintains curr1 + d1 < curr2 + d2
                valid_hops = [
                    (d1, d2)
                    for d1 in [-1, 0, 1]
                    for d2 in [-1, 0, 1]
                    if curr1 + d1 < curr2 + d2
                ]
                d1, d2 = rng.choice(valid_hops)
                hops.append((d1, d2))
                curr1 += d1
                curr2 += d2
            assert HingeLineonSignCertifier.verify_1d_lineon_collision_avoidance(p1, p2, hops)

        # Refusal check: hop that causes collision is rejected
        assert not HingeLineonSignCertifier.verify_1d_lineon_collision_avoidance(0, 1, [(1, 0)])

        # 2. Discrete IVT exchange refusal
        p1, p2 = 0, 4
        # Single-step sequential hops exchanging 0 and 4:
        # Particle 1: 0 -> 1 -> 2 -> 3 -> 4
        # Particle 2: 4 -> 3 -> 2 -> 1 -> 0
        traj1 = [0, 1, 2, 2, 3, 4]
        traj2 = [4, 4, 3, 2, 1, 0]
        # At index t=3, traj1[3] == 2 == traj2[3] (collision site!)
        assert HingeLineonSignCertifier.verify_discrete_ivt_collision_obstruction(p1, p2, traj1, traj2)

        # 3. Exact trace values Tr(M) in {+2, -2} over Q(i)
        # Abelian 2-gauge sheets (identity)
        b_xy_ab = np.eye(2, dtype=complex)
        b_yz_ab = np.eye(2, dtype=complex)
        tr_ab = HingeLineonSignCertifier.compute_hinge_holonomy_trace(b_xy_ab, b_yz_ab)
        assert tr_ab == Fraction(2, 1)

        # Non-abelian 2-gauge sheets (Pauli matrices sigma_z, sigma_x where [z, x] anti-commute)
        sigma_z = np.array([[1, 0], [0, -1]], dtype=complex)
        sigma_x = np.array([[0, 1], [1, 0]], dtype=complex)
        tr_nonab = HingeLineonSignCertifier.compute_hinge_holonomy_trace(sigma_z, sigma_x)
        assert tr_nonab == Fraction(-2, 1)

        # 4. BQNF terminal routing consistency
        assert HingeLineonSignCertifier.evaluate_terminal_routing(
            is_corner_lineon=False, is_nonabelian=False
        ) == TerminalRoute.EXACT_REPAIR
        assert HingeLineonSignCertifier.evaluate_terminal_routing(
            is_corner_lineon=True, is_nonabelian=False
        ) == TerminalRoute.OPEN_SIGN_OBSTRUCTION
        assert HingeLineonSignCertifier.evaluate_terminal_routing(
            is_corner_lineon=False, is_nonabelian=True
        ) == TerminalRoute.OPEN_SIGN_OBSTRUCTION

        # 5. Trivial worldline permutation parity (+1)
        assert HingeLineonSignCertifier.permutation_sign_trivial(is_collision_free=True) == 1
        with pytest.raises(ValueError):
            HingeLineonSignCertifier.permutation_sign_trivial(is_collision_free=False)

        # 6. Multi-hinge Y-junction collision-free exchange vs axis conservation (Theorems 6-8)
        yj = HingeLineonSignCertifier.verify_y_junction_collision_free_exchange()
        assert yj["trajectory_steps"] == 6
        assert yj["collision_free"] is True
        assert yj["valid_y_junction_hops"] is True
        assert yj["exchanged"] is True
        assert yj["exchange_sign"] == -1
        assert yj["abelian_holonomy_exchange_weight"] == -2
        assert yj["nonabelian_holonomy_exchange_weight"] == 2
        assert yj["axis_conserved_branch_exchange_possible"] is False

    def test_noncommuting_su2_positive_commutator_trace_counterexample(self) -> None:
        """
        Regression test for the SU(2) non-commuting holonomy counterexample (Theorem 10):
        A = diag(i, -i) and B = [[4/5, -3/5], [3/5, 4/5]] are both in SU(2) and do not
        commute (AB != BA), yet Tr(A B A^-1 B^-1) = 14/25 > 0 (not -2, and not rounded to 1).
        """
        a_complex = np.array([[1j, 0.0], [0.0, -1j]], dtype=complex)
        b_complex = np.array([[4.0 / 5.0, -3.0 / 5.0], [3.0 / 5.0, 4.0 / 5.0]], dtype=complex)
        assert not np.allclose(a_complex @ b_complex, b_complex @ a_complex)
        b_binary = np.array([[Fraction(float(x.real)) for x in row] for row in b_complex], dtype=object)
        assert HingeLineonSignCertifier.compute_hinge_holonomy_trace(a_complex, b_complex) == HingeLineonSignCertifier.compute_hinge_holonomy_trace(a_complex, b_binary)
        assert HingeLineonSignCertifier.compute_hinge_holonomy_trace(a_complex, b_complex) > Fraction(0, 1)

        a_exact = np.array([[(Fraction(0, 1), Fraction(1, 1)), (Fraction(0, 1), Fraction(0, 1))],
                            [(Fraction(0, 1), Fraction(0, 1)), (Fraction(0, 1), Fraction(-1, 1))]], dtype=object)
        b_exact = np.array([[Fraction(4, 5), Fraction(-3, 5)],
                            [Fraction(3, 5), Fraction(4, 5)]], dtype=object)
        assert HingeLineonSignCertifier.compute_hinge_holonomy_trace(a_exact, b_exact) == Fraction(14, 25)





def test_holonomy_preserves_small_binary_inputs():
    tiny = float(2**-40)
    a = np.array([[tiny, 0], [0, 1]], dtype=float)
    assert HingeLineonSignCertifier._to_gaussian_rat(tiny) == (Fraction(tiny), Fraction(0))
    assert HingeLineonSignCertifier.compute_hinge_holonomy_trace(a, np.eye(2)) == 2


def test_holonomy_preserves_large_denominator_rationals():
    q = Fraction(1, 10**12 + 39)
    assert HingeLineonSignCertifier._to_gaussian_rat(q) == (q, Fraction(0))


@pytest.mark.parametrize("shape", [(3, 3), (2, 3), (1, 1)])
def test_holonomy_rejects_wrong_matrix_shape(shape):
    with pytest.raises(ValueError, match="2x2"):
        HingeLineonSignCertifier.compute_hinge_holonomy_trace(np.eye(*shape), np.eye(2))


def test_holonomy_rejects_singular_matrix():
    with pytest.raises(ValueError, match="Singular"):
        HingeLineonSignCertifier.compute_hinge_holonomy_trace(np.zeros((2, 2)), np.eye(2))


def test_holonomy_preserves_numpy_extended_precision():
    value = np.longdouble("1.0000000000000000001")
    assert HingeLineonSignCertifier._to_gaussian_rat(value) == (Fraction(*value.as_integer_ratio()), Fraction(0))
