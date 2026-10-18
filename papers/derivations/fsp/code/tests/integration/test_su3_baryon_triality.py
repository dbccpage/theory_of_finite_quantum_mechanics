"""
test_su3_baryon_triality.py — Integration Tests for SU(3) Color Flux-Tube Junctions and Cochain Curvature.

AuthorityEffect: None.

Tests:
1. SU(3) Cartan root algebra, color singlet closure, and root length equivariance.
2. Simplicial Y-junction cochain complex nilpotence d1 . d0 == 0.
3. Meson 2-body chain (arity k=2) exhibits zero cochain curvature (Gamma_2 = 0.0) -> ExactRepair.
4. 3-quark Baryon Y-junction (arity k=3) induces higher-order cochain curvature (Gamma_2 > 0.0).
5. Baryon with non-zero curvature and sign residual routes to TerminalRoute.OpenSignObstruction.
6. GIN mode posting lists index all 9 color-spatial modes.
"""

from __future__ import annotations

import math
from fractions import Fraction
from pathlib import Path
import sys
import pytest

current_dir = Path(__file__).resolve().parent
code_dir = current_dir.parent.parent
if str(code_dir) not in sys.path:
    sys.path.insert(0, str(code_dir))

from su3_baryon_triality import (
    SU3SimplicialYJunction,
    SU3BaryonGinEngine,
    SU3BaryonAuditReceipt,
)


def test_su3_cartan_root_algebra():
    """Validates SU(3) weight geometry: color singlet closure and root vector lengths."""
    junction = SU3SimplicialYJunction()
    w = junction.weights

    sum_x = w["R"][0] + w["G"][0] + w["B"][0]
    sum_y = w["R"][1] + w["G"][1] + w["B"][1]
    assert sum_x == pytest.approx(0.0, abs=1e-9)
    assert sum_y == pytest.approx(0.0, abs=1e-9)

    r_rg = junction.evaluate_cartan_root_diff("R", "G")
    r_gb = junction.evaluate_cartan_root_diff("G", "B")
    r_br = junction.evaluate_cartan_root_diff("B", "R")
    assert r_rg == pytest.approx(1.0, rel=1e-5)
    assert r_gb == pytest.approx(1.0, rel=1e-5)
    assert r_br == pytest.approx(1.0, rel=1e-5)


def test_simplicial_complex_nilpotence():
    """Validates boundary operator nilpotence d1 . d0 == 0 on the 4-vertex, 6-link, 3-face complex."""
    junction = SU3SimplicialYJunction()
    assert junction.complex.check_nilpotence() is True


def test_meson_zero_cochain_curvature():
    """Validates that 2-body meson (q q_bar) flux configuration forms a closed cochain with Gamma_2 = 0."""
    engine = SU3BaryonGinEngine(in_memory=True)
    try:
        receipt = engine.audit_su3_baryon_triality()
        assert receipt.meson_arity == 2
        assert receipt.meson_gamma_2 == pytest.approx(0.0, abs=1e-6)
        assert receipt.meson_terminal_route == "ExactRepair"
    finally:
        engine.close()


def test_su3_baryon_triality_higher_order_curvature():
    """
    Validates that 3-quark baryonic Y-junction vertices under 3-cochain arity constraints
    induce higher-order cochain curvature (Gamma_2 > 0) and route to OpenSignObstruction.
    """
    engine = SU3BaryonGinEngine(in_memory=True)
    try:
        receipt = engine.audit_su3_baryon_triality()
        assert receipt.baryon_arity == 3
        assert receipt.gauge_group == "SU(3)"
        assert receipt.center_triality == "Z_3"

        assert receipt.has_higher_order_curvature is True
        assert receipt.baryon_gamma_2 > 0.0
        assert receipt.baryon_gamma_2 == pytest.approx(5.0, rel=1e-4)

        assert receipt.baryon_phi_1 > 0.0
        cochain = [Fraction(x) for x in engine.junction.build_baryon_cochain()[0]]
        boundary = engine.junction.complex.d0
        gauge = [Fraction(0), Fraction(1, 2), Fraction(1, 2), Fraction(1, 2)]
        residual = [cochain[i] - sum(row[j] * gauge[j] for j in range(4))
                    for i, row in enumerate(boundary)]
        dual = [Fraction(x) for x in (1, 0, -1, 1, 1, 0)]
        assert residual == [Fraction(1, 2), 0, -2, 0, 0, 0]
        assert all(sum(boundary[i][j] * dual[i] for i in range(6)) == 0
                   for j in range(4))
        assert max(abs(x) for x in dual) == 1
        assert sum(abs(x) for x in residual) == sum(x * y for x, y in zip(cochain, dual)) == Fraction(5, 2)
        assert receipt.baryon_phi_1 == Fraction(5, 2)

        assert receipt.baryon_terminal_route == "OpenSignObstruction"
    finally:
        engine.close()


def test_su3_gin_mode_posting_list():
    """Validates that GIN inverted posting lists track all 9 color-spatial modes."""
    engine = SU3BaryonGinEngine(in_memory=True)
    try:
        engine.audit_su3_baryon_triality()
        c = engine.conn.cursor()
        c.execute("SELECT COUNT(DISTINCT mode_id) FROM GinModePostingList;")
        count = c.fetchone()[0]
        assert count == 9

        occupied = [m for m, cfgs in engine.posting_index.items() if len(cfgs) > 0]
        assert len(occupied) == 3
        assert set(occupied) == {1, 5, 9}
    finally:
        engine.close()
