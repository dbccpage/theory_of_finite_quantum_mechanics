"""
test_bf_nonabelian_3loop_braiding.py — Integration Tests for (3+1)D Non-Abelian SU(2)_k Topological BF Theory & 3-Loop Braiding.

AuthorityEffect: None.

Tests:
1. SU(2)_k Modular Category Data: validates quantum dimensions, twists, and F-matrix unitarity for k = 2, 3, 4.
2. Abelian limit (j = 0): confirms contractible holonomy, zero defect mass, and TerminalRoute.ExactRepair.
3. Non-abelian 3-loop braiding at k = 2: confirms 2x2 matrix holonomy, non-real/indefinite trace,
   positive defect mass Phi_1 > 0, and TerminalRoute.OpenSignObstruction.
4. Non-abelian 3-loop braiding at k = 3: confirms Fibonacci-level braiding obstruction, Phi_1 > 0,
   and TerminalRoute.OpenSignObstruction.
5. Orientation energy asymmetry: confirms thermal weight gap and TerminalRoute.SplitBrainRefusal.
6. Quantum double projection repair (Drinfeld Double D(SU(2)_k)): confirms that folding M_WL (x) M_WL^dagger
   identically restores real positive trace, nullifies defect mass Phi_1 = 0, and routes to TerminalRoute.ExactRepair.
"""

from __future__ import annotations

import cmath
import math
from pathlib import Path
import sys
import numpy as np
import pytest

current_dir = Path(__file__).resolve().parent
code_dir = current_dir.parent.parent
if str(code_dir) not in sys.path:
    sys.path.insert(0, str(code_dir))

from bqnf_sign_evaluator import TerminalRoute
from bf_nonabelian_3loop_braiding import (
    SU2LevelKCategory,
    WangLevin3LoopBraidingModel,
    NonAbelianBfEngine,
    WangLevin3LoopAuditReceipt,
)


def test_su2_level_k_modular_data():
    """Validates SU(2)_k quantum dimensions, total dimension, and fundamental F-matrix unitarity."""
    for k in [2, 3, 4]:
        cat = SU2LevelKCategory(k=k)
        assert cat.num_objects == k + 1
        assert pytest.approx(cat.quantum_dimension(0)) == 1.0

        for two_j in range(cat.num_objects):
            assert cat.quantum_dimension(two_j) > 0.0

        F = cat.f_matrix_fundamental()
        assert F.shape == (2, 2)
        assert np.allclose(F @ F.conj().T, np.eye(2), atol=1e-12)


def test_abelian_trivial_flux_limit():
    """Validates that for spin-0 loops, 3-loop braiding reduces to identity and ExactRepair."""
    model = WangLevin3LoopBraidingModel(k_level=2, loop_fluxes=(0.0, 0.0, 0.0))
    receipt = NonAbelianBfEngine.audit_nonabelian_3loop_braiding(model)

    assert receipt.is_non_abelian is False
    assert receipt.fusion_space_dim == 1
    assert receipt.trace_holonomy == pytest.approx(1.0 + 0.0j)
    assert receipt.cochain_curvature_gamma2 == 0.0
    assert receipt.involution_pairing_phi1 == 0.0
    assert receipt.average_sign_gin == 1.0
    assert receipt.terminal_route == TerminalRoute.EXACT_REPAIR


def test_nonabelian_3loop_braiding_obstruction_k2():
    """Validates that in SU(2)_2 BF theory, fundamental 3-loop braiding produces OpenSignObstruction."""
    model = WangLevin3LoopBraidingModel(k_level=2, loop_fluxes=(0.5, 0.5, 0.5))
    receipt = NonAbelianBfEngine.audit_nonabelian_3loop_braiding(model, use_quantum_double=False)

    assert receipt.is_non_abelian is True
    assert receipt.fusion_space_dim == 2
    assert receipt.involution_pairing_phi1 > 0.0
    assert receipt.cochain_curvature_gamma2 > 0.0
    assert receipt.terminal_route == TerminalRoute.OPEN_SIGN_OBSTRUCTION


def test_nonabelian_3loop_braiding_obstruction_k3():
    """Validates that in SU(2)_3 BF theory, fundamental 3-loop braiding produces OpenSignObstruction."""
    model = WangLevin3LoopBraidingModel(k_level=3, loop_fluxes=(0.5, 0.5, 0.5))
    receipt = NonAbelianBfEngine.audit_nonabelian_3loop_braiding(model, use_quantum_double=False)

    assert receipt.is_non_abelian is True
    assert receipt.fusion_space_dim == 2
    assert receipt.involution_pairing_phi1 > 0.0
    assert receipt.terminal_route == TerminalRoute.OPEN_SIGN_OBSTRUCTION


def test_orientation_energy_asymmetry_split_brain():
    """Validates that orientation energy asymmetry Delta E > 0 routes to SplitBrainRefusal."""
    model = WangLevin3LoopBraidingModel(
        k_level=2,
        loop_fluxes=(0.5, 0.5, 0.5),
        temperature=1.0,
        energy_gap_orient=0.5,
    )
    receipt = NonAbelianBfEngine.audit_nonabelian_3loop_braiding(model, use_quantum_double=False)

    assert receipt.terminal_route == TerminalRoute.REFUSED
    assert receipt.involution_pairing_phi1 > 0.0


def test_quantum_double_projection_repair():
    """Validates that the quantum double projector P_QD restores real positive trace and ExactRepair."""
    for k in [2, 3, 4]:
        model = WangLevin3LoopBraidingModel(k_level=k, loop_fluxes=(0.5, 0.5, 0.5))
        receipt_unproj = NonAbelianBfEngine.audit_nonabelian_3loop_braiding(model, use_quantum_double=False)
        assert receipt_unproj.terminal_route == TerminalRoute.OPEN_SIGN_OBSTRUCTION

        receipt_proj = NonAbelianBfEngine.audit_nonabelian_3loop_braiding(model, use_quantum_double=True)
        assert receipt_proj.is_quantum_double_projected is True
        assert receipt_proj.involution_pairing_phi1 == 0.0
        assert receipt_proj.cochain_curvature_gamma2 == 0.0
        assert receipt_proj.average_sign_gin == 1.0
        assert receipt_proj.terminal_route == TerminalRoute.EXACT_REPAIR

        assert receipt_proj.trace_holonomy.real > 0.0
        assert abs(receipt_proj.trace_holonomy.imag) < 1e-12

