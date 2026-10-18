"""
test_su_nc_adjoint_flux.py — Integration Tests for SU(N_c) Adjoint Color Flux Tubes and Zero N-ality.

AuthorityEffect: None.

Tests:
1. Boundary operator nilpotence d1 . d0 == 0 on the adjoint flux-tube simplicial complex.
2. Zero N-ality of adjoint representation (k=0 mod N_c) eliminates cochain curvature (Gamma_2 = 0.0).
3. Adjoint string breaking enables 100% GIN involution pairing, restoring average sign to 1.0 -> ExactRepair.
4. Non-zero N-ality of fundamental representation (k=1) preserves cochain curvature (Gamma_2 > 0) -> OpenSignObstruction.
5. Multi-flavor scaling across N_c in {2, 3, 4} and N_f in {1, 2, 4} with GIN mode indexing.
"""

from __future__ import annotations

import math
from pathlib import Path
import sys
import pytest

current_dir = Path(__file__).resolve().parent
code_dir = current_dir.parent.parent
if str(code_dir) not in sys.path:
    sys.path.insert(0, str(code_dir))

from src.fsp.su_nc_adjoint_flux import (
    SUNCAdjointSimplicialComplex,
    SUNCAdjointEngine,
    SUNCAdjointAuditReceipt,
)


def test_simplicial_nilpotence():
    """Validates boundary operator nilpotence d1 . d0 == 0 on the 4-vertex, 5-link, 2-face complex."""
    complex_obj = SUNCAdjointSimplicialComplex()
    assert complex_obj.complex.check_nilpotence() is True


def test_adjoint_zero_n_ality_and_cochain_closure():
    """
    Validates that adjoint matter with zero N-ality (k = 0 mod N_c) undergoes string breaking
    into color-singlet loops that eliminate 2-cochain curvature (Gamma_2 = 0.0).
    """
    engine = SUNCAdjointEngine(n_c=3, n_f=2, string_tension_sigma=1.0, adjoint_mass_m=0.4, in_memory=True)
    try:
        receipt = engine.audit_adjoint_flux_tube(tube_length_r=1.5)

        assert receipt.n_c == 3
        assert receipt.n_f == 2
        assert receipt.matter_representation == "Adjoint"
        assert receipt.n_ality == 0
        assert receipt.string_breaking_occurred is True

        assert receipt.cochain_curvature_gamma_2 == pytest.approx(0.0, abs=1e-6)
    finally:
        engine.close()


def test_adjoint_gin_involution_pairing():
    """
    Validates that zero N-ality and exact charge-conjugation/flavor-reflection involution
    pair 100% of negative paths under GIN mode indexing, routing to TerminalRoute.ExactRepair.
    """
    engine = SUNCAdjointEngine(n_c=3, n_f=2, in_memory=True)
    try:
        receipt = engine.audit_adjoint_flux_tube(tube_length_r=1.5)

        assert receipt.involution_pairing_rate == pytest.approx(1.0)
        assert receipt.gin_quotiented_average_sign == pytest.approx(1.0)

        assert receipt.terminal_route == "ExactRepair"
    finally:
        engine.close()


def test_fundamental_n_ality_open_curvature_obstruction():
    """
    Validates that fundamental representation matter (N-ality = 1) cannot break the string
    into singlet loops, maintaining non-zero cochain curvature (Gamma_2 > 0) -> OpenSignObstruction.
    """
    engine = SUNCAdjointEngine(n_c=3, n_f=2, in_memory=True)
    try:
        receipt = engine.audit_fundamental_flux_tube()

        assert receipt.matter_representation == "Fundamental"
        assert receipt.n_ality == 1
        assert receipt.string_breaking_occurred is False

        assert receipt.cochain_curvature_gamma_2 > 0.0
        assert receipt.cochain_curvature_gamma_2 == pytest.approx(2.0, rel=1e-4)

        assert receipt.terminal_route == "OpenSignObstruction"
    finally:
        engine.close()


def test_multi_flavor_scaling_and_modes():
    """Validates multi-flavor scaling across gauge groups SU(2), SU(3), SU(4) and flavors N_f in {1, 2, 4}."""
    for nc in (2, 3, 4):
        for nf in (1, 2, 4):
            engine = SUNCAdjointEngine(n_c=nc, n_f=nf, in_memory=True)
            try:
                receipt = engine.audit_adjoint_flux_tube(tube_length_r=1.2)
                assert receipt.n_c == nc
                assert receipt.n_f == nf
                assert receipt.cochain_curvature_gamma_2 == pytest.approx(0.0, abs=1e-6)
                assert receipt.terminal_route == "ExactRepair"

                expected_modes = 2 * (nc ** 2 - 1) * nf
                c = engine.conn.cursor()
                c.execute("SELECT COUNT(DISTINCT mode_id) FROM GinModePostingList;")
                count = c.fetchone()[0]
                assert count == expected_modes
            finally:
                engine.close()
