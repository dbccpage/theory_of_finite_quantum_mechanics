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

from src.fsp.foliated_fracton_2gauge_defects import (
    FoliatedFractonConfig,
    FoliatedFractonEngine,
    FoliationDirection,
    ExcitationMobility,
    FractonDefect,
    SubsystemChargeRegistry,
    TerminalRoute,
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
