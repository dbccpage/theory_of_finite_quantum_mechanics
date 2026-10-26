"""
Selected floating-point fusion-matrix diagnostic regressions.

AuthorityEffect: None.

Check selected level-2/3/4 scalar and matrix formulas, the trivial-flag branch,
route conventions, orientation-weight inputs and the doubled-trace diagnostic.
These are numerical fixtures, not BF-theory, Wang-Levin, modular-category or
physical sign-problem certificates. Historical function and route labels remain
API identifiers. The zero-trace case specifically fences the conventional
average_sign_gin=1 output from an inferred physical ensemble average.
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

from src.fsp.bqnf_sign_evaluator import TerminalRoute
from src.fsp.bf_nonabelian_3loop_braiding import (
    SU2LevelKCategory,
    WangLevin3LoopBraidingModel,
    NonAbelianBfEngine,
    WangLevin3LoopAuditReceipt,
)


def test_holonomy_is_the_declared_commutator():
    """Anticommuting Pauli squares give -I, unlike the old docstring product."""
    class FixedCategory:
        def f_matrix_fundamental(self):
            return np.array([[1, 1], [1, -1]], dtype=complex) / math.sqrt(2)

        def r_matrix_fundamental(self):
            return np.diag([1, 1j])

    model = WangLevin3LoopBraidingModel(k_level=2)
    model.category = FixedCategory()
    assert np.allclose(model.compute_3loop_holonomy_matrix(), -np.eye(2), atol=1e-12)


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
    """Check the all-zero flag's identity matrix and conventional route."""
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
    """Check the supplied level-2 numerical fixture's diagnostic route."""
    model = WangLevin3LoopBraidingModel(k_level=2, loop_fluxes=(0.5, 0.5, 0.5))
    receipt = NonAbelianBfEngine.audit_nonabelian_3loop_braiding(model, use_quantum_double=False)

    assert receipt.is_non_abelian is True
    assert receipt.fusion_space_dim == 2
    assert receipt.involution_pairing_phi1 > 0.0
    assert receipt.cochain_curvature_gamma2 > 0.0
    assert receipt.terminal_route == TerminalRoute.OPEN_SIGN_OBSTRUCTION


def test_nonabelian_3loop_braiding_obstruction_k3():
    """Check the supplied level-3 numerical fixture's diagnostic route."""
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
    """Validates that the quantum double projector P_QD restores real nonnegative trace and ExactRepair."""
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

        assert receipt_proj.trace_holonomy.real >= 0.0
        matrix = model.compute_3loop_holonomy_matrix()
        direct = np.trace(model.compute_quantum_double_projection(matrix))
        assert receipt_proj.trace_holonomy == pytest.approx(direct, abs=1e-12)
        assert abs(receipt_proj.trace_holonomy.imag) < 1e-12


def test_doubled_trace_can_vanish(monkeypatch):
    model = WangLevin3LoopBraidingModel()
    matrix = np.diag([1.0, -1.0]).astype(complex)
    monkeypatch.setattr(model, "compute_3loop_holonomy_matrix", lambda: matrix)
    receipt = NonAbelianBfEngine.audit_nonabelian_3loop_braiding(model, use_quantum_double=True)
    assert np.trace(model.compute_quantum_double_projection(matrix)) == 0
    assert receipt.trace_holonomy == 0
