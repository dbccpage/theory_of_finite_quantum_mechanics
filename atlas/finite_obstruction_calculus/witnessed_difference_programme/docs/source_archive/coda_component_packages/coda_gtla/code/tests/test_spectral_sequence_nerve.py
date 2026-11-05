# -*- coding: utf-8 -*-
"""Finite two-row bicomplex cycle and quotient regressions.

E2^{2,0}=ker(dv_20)/dh_10(ker(dv_10)). The canonical triangle example
has zero E2 target quotient. Face counts are combinatorial counts, not
complexity bounds or evidence that truncation preserves cohomology.
"""

from __future__ import annotations

import pytest
from cochain_presentation import _as_exact_rational
from coda_gtla_core import (
    Bicomplex2Nerve,
    ProblemInstance,
    TerminalKind,
    execute_master_normal_form,
)
from sympy import Matrix, Rational

# ==============================================================================
# 1. Bicomplex Anticommutation & Differentials Composition
# ==============================================================================


def test_bicomplex_2nerve_anticommutation_axioms():
    """Verify that the 2-nerve bicomplex satisfies horizontal square zero and anticommutation."""
    bicomplex = Bicomplex2Nerve.build_canonical_2nerve()
    assert bicomplex.validate() is True

    # Horizontal squares zero
    assert bicomplex.dh_10 * bicomplex.dh_00 == Matrix.zeros(2, 6)
    assert bicomplex.dh_11 * bicomplex.dh_01 == Matrix.zeros(1, 3)

    # Anticommutation identities: dh * dv + dv * dh == 0
    anticomm_0 = bicomplex.dh_01 * bicomplex.dv_00 + bicomplex.dv_10 * bicomplex.dh_00
    assert anticomm_0 == Matrix.zeros(3, 6)

    anticomm_1 = bicomplex.dh_11 * bicomplex.dv_10 + bicomplex.dv_20 * bicomplex.dh_10
    assert anticomm_1 == Matrix.zeros(1, 6)


def test_total_complex_differentials_composition():
    """Verify that total complex differentials D0 and D1 satisfy D1 * D0 == 0."""
    bicomplex = Bicomplex2Nerve.build_canonical_2nerve()
    d0 = bicomplex.total_complex_d0()
    d1 = bicomplex.total_complex_d1()

    # Tot^0 = C^{0,0} (6)
    # Tot^1 = C^{1,0} (6) + C^{0,1} (3) = 9
    # Tot^2 = C^{2,0} (2) + C^{1,1} (3) = 5
    assert d0.shape == (9, 6)
    assert d1.shape == (5, 9)

    assert d1 * d0 == Matrix.zeros(5, 6)
    assert d1.rank() == 4
    # Dual kernel ker(D1^T) has dimension 5 - 4 = 1
    assert len(d1.T.nullspace()) == 1


# ==============================================================================
# 2. Higher Differential d2 Zig-Zag Obstruction Extraction
# ==============================================================================


def test_higher_differential_d2_zigzag_obstruction_extraction():
    """
    Evaluates extraction of secondary differential d_2: E_2^{0,1} -> E_2^{2,0}.
    Maps local 1-cocycle omega in C^{0,1} with holonomy flux phi in ker(dv_10) to d_2 omega in C^{2,0}.
    """
    bicomplex = Bicomplex2Nerve.build_canonical_2nerve()

    # Local 1-cocycle on 3 vertices
    omega_01 = Matrix([Rational(1), Rational(0), Rational(-1)])

    # Holonomy flux in ker(dv_10): non-trivial 0-cocycle on edge 0: [1, 1, 0, 0, 0, 0]^T
    flux = Matrix([Rational(1), Rational(1), Rational(0), Rational(0), Rational(0), Rational(0)])

    eta, d2_omega, omega_tot = bicomplex.compute_d2_zigzag_obstruction(omega_01, holonomy_flux=flux)

    assert eta.shape == (6, 1)
    assert d2_omega.shape == (2, 1)
    assert omega_tot.shape == (5, 1)

    # This representative is nonzero, although its E2 class is zero.
    assert d2_omega != Matrix.zeros(2, 1)
    # Omega_tot is embedded purely in C^{2,0} top component
    assert omega_tot[0:2, 0] == d2_omega
    assert omega_tot[2:5, 0] == Matrix.zeros(3, 1)


# ==============================================================================
# 3. Exact Rational LP Dual Witness Certification
# ==============================================================================


def test_exact_rational_lp_dual_witness_bounds_d2_obstruction():
    """
    Verifies that the secondary obstruction d_2 omega is bounded and certified
    by an exact rational LP dual witness y* in ker(B2^T) with ||y*||_infty <= 1.
    This canonical example has zero quotient distance.
    """
    bicomplex = Bicomplex2Nerve.build_canonical_2nerve()
    omega_01 = Matrix([Rational(1), Rational(0), Rational(-1)])
    flux = Matrix([Rational(1), Rational(1), Rational(0), Rational(0), Rational(0), Rational(0)])

    cert = bicomplex.certify_d2_quotient_bounds(omega_01, holonomy_flux=flux)

    assert cert.verify() is True
    assert cert.distance == Rational(0)
    assert cert.dual_pairing == Rational(0)

    # Dual witness annihilates the E2 boundary matrix B2.
    b2 = bicomplex.e2_page_boundary_d2()
    assert b2.T * cert.dual_witness == Matrix.zeros(b2.cols, 1)

    # Dual witness l_infty norm bound <= 1
    assert all(abs(val) <= Rational(1) for val in cert.dual_witness)

    # Mechanical pairing witness
    assert cert.dual_witness.T * cert.cochain == Matrix([[Rational(0)]])


def test_trivial_higher_differential_exact_total_coboundary():
    """
    Confirms that when the secondary differential d_2 omega vanishes in cohomology,
    the quotient distance is exactly zero with verified vanishing residual.
    """
    bicomplex = Bicomplex2Nerve.build_canonical_2nerve()
    omega_01 = Matrix([Rational(1), Rational(0), Rational(-1)])

    # The class vanishes; the chosen representative need not be zero.
    cert = bicomplex.certify_d2_quotient_bounds(omega_01, holonomy_flux=None)

    assert cert.verify() is True
    assert cert.distance == Rational(0)
    assert cert.residual == Matrix.zeros(2, 1)


def test_e2_page_higher_coboundary_rational_lp_bounds():
    """
    Rejects a noncycle and certifies a cycle modulo B_2 = dh_10 * ker(dv_10).
    The canonical target quotient is zero.
    """
    bicomplex = Bicomplex2Nerve.build_canonical_2nerve()
    b2 = bicomplex.e2_page_boundary_d2()

    assert b2.shape == (2, 3)
    assert b2.rank() == 1

    # (1,0) is not a cycle: dv_20*(1,0)=1, so it cannot represent E2.
    with pytest.raises(ValueError, match=r"ker\(dv_20\)"):
        bicomplex.certify_e2_coboundary_bounds(Matrix([1, 0]))

    # Trivial coboundary in im(B_2): [1, 1]^T = B_2 * [1, 0, 0]^T
    psi_trivial = Matrix([Rational(1), Rational(1)])
    cert_trivial = bicomplex.certify_e2_coboundary_bounds(psi_trivial)

    assert cert_trivial.verify() is True
    assert cert_trivial.distance == Rational(0)
    assert cert_trivial.residual == Matrix.zeros(2, 1)


# ==============================================================================
# 4. Combinatorial Face Counts
# ==============================================================================


def test_no_dimension_explosion_2nerve_vs_full_simplex():
    """
    Checks exact face counts through degree two against all simplex faces.
    These counts do not prove LP complexity or preservation of cohomology.
    """
    # 20 vertices
    scaling_20 = Bicomplex2Nerve.compare_dimension_scaling(20, local_fiber_dim=2)
    assert scaling_20["full_simplex_faces"] == 1048575  # 2^20 - 1
    assert scaling_20["2nerve_total_faces"] == 1350  # 20 + 190 + 1140
    assert scaling_20["compression_ratio"] > 776
    assert scaling_20["truncated_face_count_smaller"] is True

    # 30 vertices
    scaling_30 = Bicomplex2Nerve.compare_dimension_scaling(30, local_fiber_dim=2)
    assert scaling_30["full_simplex_faces"] == 1073741823  # > 10^9
    assert scaling_30["2nerve_total_faces"] == 4525  # 30 + 435 + 4060
    assert scaling_30["compression_ratio"] > 237000
    assert scaling_30["truncated_face_count_smaller"] is True


# ==============================================================================
# 5. Master Normal Form Pipeline Integration & Firewall
# ==============================================================================


def test_pipeline_master_normal_form_integration_with_d2_obstruction():
    """
    The embedded total cochain is exact, even when its representative is nonzero.
    With no declared licence, the zero total quotient distance still refuses.
    """
    bicomplex = Bicomplex2Nerve.build_canonical_2nerve()
    omega_01 = Matrix([Rational(1), Rational(0), Rational(-1)])
    flux = Matrix([Rational(1), Rational(1), Rational(0), Rational(0), Rational(0), Rational(0)])

    _eta, _d2_omega, omega_tot = bicomplex.compute_d2_zigzag_obstruction(
        omega_01, holonomy_flux=flux
    )
    d1 = bicomplex.total_complex_d1()

    prob = ProblemInstance(
        problem_id="test_d2_spectral_sequence",
        raw_data="d2_spectral_data",
        candidate_sieve=("cand1",),
        coarse_profile=(0, 1),
        fine_profile=(0, 1),
        projection_map={0: 0, 1: 1},
        local_sections={"U0": (Rational(1, 2),)},
        overlaps={("U0", "U0"): True},
        d0=d1,
        d1=Matrix.zeros(1, d1.rows),
        defect_cochain=omega_tot,
        fda_license_granted=False,  # Unlicensed
    )

    result = execute_master_normal_form(prob)
    assert result.terminal_outcome.kind != TerminalKind.AUTHORIZED, (
        "FIREWALL BREACH: Higher d_2 spectral sequence defect synthesized spurious AuthorityToken"
    )
    assert result.terminal_outcome.kind == TerminalKind.REFUSED
    assert result.terminal_outcome.phi1_distance == 0


# ==============================================================================
# 6. Strict Zero Floats & Fail-Closed Validation
# ==============================================================================


def test_zero_floats_and_fail_closed_validation():
    """Asserts that floating-point inputs strictly raise TypeError in bicomplex operations."""
    with pytest.raises(TypeError, match="exact arithmetic rejects float"):
        _as_exact_rational(1.234)

    with pytest.raises(TypeError, match="exact arithmetic rejects float"):
        _as_exact_rational(float("nan"))

    with pytest.raises(ValueError, match="num_vertices must be at least 3"):
        Bicomplex2Nerve.compare_dimension_scaling(2)


def test_nonzero_d2_uses_cycle_quotient_while_total_class_is_zero():
    # C^{p,q}=Q for all six spots. dv_10=id, dh_01=dh_10=id,
    # other maps zero. All four bicomplex identities hold.
    z, one = Matrix([[0]]), Matrix([[1]])
    b = Bicomplex2Nerve(z, one, one, z, z, one, z)
    omega = Matrix([1])
    eta, d2, total = b.compute_d2_zigzag_obstruction(omega)
    assert eta == Matrix([-1]) and d2 == Matrix([-1])
    assert b.dv_20 * d2 == Matrix([0])
    assert b.total_complex_d1() * Matrix.vstack(eta, omega) == total
    cert = b.certify_d2_quotient_bounds(omega)
    assert cert.verify() and cert.distance == 1
    assert cert.repair_map.shape == (1, 0)


def test_zigzag_rejects_bad_flux_and_valid_flux_does_not_change_class():
    b = Bicomplex2Nerve.build_canonical_2nerve()
    omega = Matrix([1, 0, -1])
    with pytest.raises(ValueError, match=r"ker\(dv_10\)"):
        b.compute_d2_zigzag_obstruction(omega, Matrix([1, 0, 0, 0, 0, 0]))
    for t in (-2, 0, 3):
        flux = Matrix([t, t, 0, 0, 0, 0])
        eta, d2, total = b.compute_d2_zigzag_obstruction(omega, flux)
        assert b.dv_10 * eta + b.dh_01 * omega == Matrix.zeros(3, 1)
        assert b.dv_20 * d2 == Matrix.zeros(1, 1)
        assert b.total_complex_d1() * Matrix.vstack(eta, omega) == total
        assert b.certify_d2_quotient_bounds(omega, flux).distance == 0


def test_e2_representative_changes_preserve_class():
    b = Bicomplex2Nerve.build_canonical_2nerve()
    omega = Matrix([1, 0, -1])
    for alpha in (Matrix.zeros(6, 1), Matrix([1, 2, 3, 4, 5, 6])):
        shifted = omega + b.dv_00 * alpha
        assert (
            b.certify_d2_quotient_bounds(shifted).distance
            == b.certify_d2_quotient_bounds(omega).distance
        )
    for t in (-3, 0, 5):
        assert b.certify_e2_coboundary_bounds(Matrix([t, t])).distance == 0
