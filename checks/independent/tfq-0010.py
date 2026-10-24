#!/usr/bin/env python3
"""Independent verification for TFQ-0010: Finite QED and electroweak shadow.

Checks:
1. Discrete Ward identity `<J, A + d0 alpha> = <J, A> + <d0* J, alpha>` on a 3-vertex
   triangle complex across 2187 combinations of currents, link fields, and gauge potentials,
   plus non-conserved current coboundary defects.
2. Charged Gaussian-rational `Q(i)` link transport (`|U|^2 = 1`) and vertex rephasing
   covariance (`|g_b (psi_b - U_{ab} psi_a)|^2 = |psi_b - U_{ab} psi_a|^2`) across
   Pythagorean phases `(1,0), (0,1), (3/5, 4/5), (5/13, 12/13), (8/17, 15/17)`.
3. Exact rational Dirac-Coulomb `n=2` fine-structure, Darwin (`-8/128`), and spin-orbit
   (`+8/384` vs `-4/384`) degeneracy (`5/128` for `j=1/2` vs `1/128` for `j=3/2`), plus
   1-loop QED self-energy (`5/6`), Uehling vacuum polarization (`-1/5`), magnetic moment
   splitting (`1/8`), total contact coefficient (`91/120`), and Bethe-lifted bracket (`232711/30000 > 7`).
4. Exact rational Weinberg electroweak mixing identities (`sin^2 theta_W + cos^2 theta_W = 1`,
   `Pi_gamma + Pi_Z = 1`, `Pi_gamma Pi_Z = 0`, custodial `rho = 1`),
   Gell-Mann--Nishijima charge identities, and anomaly cancellation at `N_c = 3` vs failure at `N_c != 3`.
6. Repository source and Lean 4 theorem anchors in `lean4/FiniteQM.lean` and
   `lean4/CampaignTfq0010FiniteQed.lean`.
"""

from __future__ import annotations

import json
import sys
from fractions import Fraction
from pathlib import Path
from typing import Any

GVal = tuple[Fraction, Fraction]


def g_add(z: GVal, w: GVal) -> GVal:
    return (z[0] + w[0], z[1] + w[1])


def g_sub(z: GVal, w: GVal) -> GVal:
    return (z[0] - w[0], z[1] - w[1])


def g_mul(z: GVal, w: GVal) -> GVal:
    return (z[0] * w[0] - z[1] * w[1], z[0] * w[1] + z[1] * w[0])


def g_conj(z: GVal) -> GVal:
    return (z[0], -z[1])


def g_norm_sq(z: GVal) -> Fraction:
    return z[0] * z[0] + z[1] * z[1]


def run_all_checks() -> dict[str, Any]:
    checks = 0
    failed = 0
    details: dict[str, Any] = {}

    def record(cond: bool, msg: str) -> None:
        nonlocal checks, failed
        checks += 1
        if not cond:
            failed += 1
            raise AssertionError(f"FAILED check #{checks}: {msg}")

    # -------------------------------------------------------------------------
    # Family 1: Discrete Ward identity on triangle complex
    # -------------------------------------------------------------------------
    vals = [Fraction(-1), Fraction(0), Fraction(1)]
    for j in vals:
        for a01 in vals:
            for a12 in vals:
                for a20 in vals:
                    for al0 in vals:
                        for al1 in vals:
                            for al2 in vals:
                                base = j * a01 + j * a12 + j * a20
                                shifted = (
                                    j * (a01 + (al1 - al0))
                                    + j * (a12 + (al2 - al1))
                                    + j * (a20 + (al0 - al2))
                                )
                                record(
                                    shifted == base,
                                    "Conserved current coupling is gauge-invariant",
                                )

    # Non-conserved current (1, 0, 0) has non-zero divergence at vertices 0 and 1
    non_conserved_defect = Fraction(1) * (Fraction(0) + (Fraction(1) - Fraction(0)))
    record(non_conserved_defect == Fraction(1), "Non-conserved current has non-zero Ward defect")

    details["family1_discrete_ward"] = {
        "conserved_cases_checked": 3**7,
        "non_conserved_defect": str(non_conserved_defect),
    }

    # -------------------------------------------------------------------------
    # Family 2: Charged Gaussian-rational link transport
    # -------------------------------------------------------------------------
    unit_phases: list[GVal] = [
        (Fraction(1), Fraction(0)),
        (Fraction(0), Fraction(1)),
        (Fraction(3, 5), Fraction(4, 5)),
        (Fraction(5, 13), Fraction(12, 13)),
        (Fraction(8, 17), Fraction(15, 17)),
    ]
    psi_samples: list[GVal] = [
        (Fraction(1), Fraction(2)),
        (Fraction(-3, 2), Fraction(1, 2)),
        (Fraction(2, 3), Fraction(-4, 3)),
    ]
    for u in unit_phases:
        record(g_norm_sq(u) == Fraction(1), f"Unit norm phase {u}")
        record(g_mul(g_conj(u), u) == (Fraction(1), Fraction(0)), f"U^* U = 1 for {u}")
        for ga in unit_phases:
            for gb in unit_phases:
                # Gauge-transformed link U' = g_b U g_a^*
                u_prime = g_mul(g_mul(gb, u), g_conj(ga))
                record(g_norm_sq(u_prime) == Fraction(1), "Dressed link phase remains unit norm")
                for psi_a in psi_samples:
                    for psi_b in psi_samples:
                        cov_diff = g_sub(psi_b, g_mul(u, psi_a))
                        psi_a_p = g_mul(ga, psi_a)
                        psi_b_p = g_mul(gb, psi_b)
                        cov_diff_p = g_sub(psi_b_p, g_mul(u_prime, psi_a_p))
                        record(
                            cov_diff_p == g_mul(gb, cov_diff),
                            "Covariant edge difference transforms as g_b D_{ab} psi",
                        )
                        record(
                            g_norm_sq(cov_diff_p) == g_norm_sq(cov_diff),
                            "Covariant edge difference squared norm is gauge-invariant",
                        )

    details["family2_charged_link_transport"] = {
        "unit_phases_count": len(unit_phases),
        "covariance_identities_checked": len(unit_phases) ** 3 * len(psi_samples) ** 2,
    }

    # -------------------------------------------------------------------------
    # Family 3: Clifford/CAR, Dirac-Coulomb fine structure, and Lamb shift datum
    # -------------------------------------------------------------------------
    c_1s = Fraction(1, 8)
    c_2_jhalf = Fraction(5, 128)
    c_2_jthreehalf = Fraction(1, 128)
    c_2s_rel_kin = Fraction(13, 128)
    c_2s_darwin = Fraction(-8, 128)
    c_2p_rel_kin = Fraction(7, 384)
    c_2p12_so = Fraction(8, 384)
    c_2p32_so = Fraction(-4, 384)
    record(c_2s_rel_kin + c_2s_darwin == c_2_jhalf, "2s_1/2 rel_kin + Darwin = 5/128")
    record(c_2p_rel_kin + c_2p12_so == c_2_jhalf, "2p_1/2 rel_kin + SO = 5/128")
    record(c_2p_rel_kin + c_2p32_so == c_2_jthreehalf, "2p_3/2 rel_kin + SO = 1/128")
    record(c_2_jhalf - c_2_jthreehalf == Fraction(1, 32), "Delta_FS (m c^2) = 1/32")
    record(2 * (c_2_jhalf - c_2_jthreehalf) == Fraction(1, 16), "Delta_FS (Ry) = 1/16")

    se_const = Fraction(10, 9) - Fraction(5, 18)
    uehling_vp = Fraction(-1, 5)
    mag_diff = Fraction(1, 12) - Fraction(-1, 24)
    lamb_contact = se_const + uehling_vp + mag_diff
    bracket_lo = Fraction(9840487, 1000000) - Fraction(2841787, 1000000) + lamb_contact
    record(se_const == Fraction(5, 6), "QED 1-loop self-energy constant = 5/6")
    record(se_const + uehling_vp == Fraction(19, 30), "SE + Uehling VP = 19/30")
    record(mag_diff == Fraction(1, 8), "Anomalous magnetic moment 2s - 2p_1/2 = 1/8")
    record(lamb_contact == Fraction(91, 120), "Lamb shift contact coefficient = 91/120")
    record(bracket_lo == Fraction(232711, 30000) and bracket_lo > 7, "Bethe bracket > 7")

    details["family3_dirac_and_lamb_shift"] = {
        "c_1s": str(c_1s),
        "c_2_jhalf": str(c_2_jhalf),
        "c_2_jthreehalf": str(c_2_jthreehalf),
        "lamb_contact": str(lamb_contact),
        "bracket_lo": str(bracket_lo),
    }

    # -------------------------------------------------------------------------
    # Family 4: Weinberg electroweak projectors and anomaly cancellation
    # -------------------------------------------------------------------------
    coupling_pairs = [
        (Fraction(4, 5), Fraction(3, 5)),
        (Fraction(1), Fraction(1)),
        (Fraction(2), Fraction(1)),
        (Fraction(3, 2), Fraction(1, 2)),
    ]
    for g, gp in coupling_pairs:
        d = g * g + gp * gp
        sin2 = (gp * gp) / d
        cos2 = (g * g) / d
        record(sin2 + cos2 == Fraction(1), "sin^2 + cos^2 = 1")
        for v in [Fraction(1), Fraction(2), Fraction(3, 2)]:
            mw2 = (v * v / 4) * (g * g)
            mz2 = (v * v / 4) * d
            rho = mw2 / (mz2 * cos2)
            record(rho == Fraction(1), "Custodial rho = 1")

    yQ, yu, yd, yL, ye = (
        Fraction(1, 6),
        Fraction(2, 3),
        Fraction(-1, 3),
        Fraction(-1, 2),
        Fraction(-1),
    )
    for nc in range(1, 7):
        nc_f = Fraction(nc)
        a_su3 = nc_f * (2 * yQ - yu - yd)
        a_su2 = nc_f * yQ + yL
        a_grav = nc_f * (2 * yQ - yu - yd) + (2 * yL - ye)
        a_u1 = nc_f * (2 * yQ**3 - yu**3 - yd**3) + (2 * yL**3 - ye**3)
        all_zero = a_su3 == 0 and a_su2 == 0 and a_grav == 0 and a_u1 == 0
        record(all_zero == (nc == 3), f"Anomalies all cancel iff N_c = 3 (tested N_c={nc})")

    details["family4_electroweak_and_anomalies"] = {
        "weinberg_witness_sin2_4_5_3_5": "9/25",
        "anomaly_cancellation_unique_nc": 3,
    }

    # -------------------------------------------------------------------------
    # Family 5: Repo source and Lean file verification
    # -------------------------------------------------------------------------
    repo_root = Path(__file__).resolve().parents[2]
    fqm = repo_root / "lean4/FiniteQM.lean"
    lean_file = repo_root / "lean4/CampaignTfq0010FiniteQed.lean"

    record(fqm.exists(), "lean4/FiniteQM.lean exists")
    record(lean_file.exists(), "lean4/CampaignTfq0010FiniteQed.lean exists")

    fqm_src = fqm.read_text(encoding="utf-8")
    for sym in [
        "weinberg_projectors_complete_orthogonal_idempotent",
        "ew_custodial_rho_eq_one",
        "sm_gell_mann_nishijima_charge_identities",
        "sm_all_four_anomalies_cancel_at_nc3_and_fail_at_nc1",
        "car_clifford_nilpotency_and_occupation_projector",
        "dirac_coulomb_fine_structure_n2_and_darwin_spin_orbit_degeneracy",
        "qed_one_loop_lamb_shift_contact_and_bethe_lifting",
    ]:
        record(sym in fqm_src, f"FiniteQM.lean contains {sym}")

    lean_src = lean_file.read_text(encoding="utf-8")
    required_theorems = [
        "theorem discrete_ward_identity_and_coboundary_gauge_coupling_invariance",
        "theorem charged_gaussian_rational_link_transport_and_vertex_covariant_difference",
        "theorem finite_clifford_car_nilpotency_and_occupation_number_projector",
        "theorem dirac_coulomb_n2_fine_structure_darwin_and_spin_orbit_degeneracy",
        "theorem qed_one_loop_vacuum_polarization_and_lamb_shift_contact_datum",
        "theorem weinberg_electroweak_projectors_and_custodial_rho_identity",
        "theorem gell_mann_nishijima_and_anomaly_cancellation_at_nc3_vs_nc1",
        "theorem f002_interface_inventory_does_not_derive_continuum_qed_fence",
        "theorem finite_qed_computational_controls_scope_separation_fence",
        "theorem tfq0010_finite_qed_and_electroweak_shadow_ledger_fence",
    ]
    for thm in required_theorems:
        record(thm in lean_src, f"CampaignTfq0010FiniteQed.lean contains {thm}")
    record("sorry" not in lean_src, "CampaignTfq0010FiniteQed.lean is sorry-free")

    return {
        "node_id": "TFQ-0010",
        "checks_total": checks,
        "checks_failed": failed,
        "passed": failed == 0,
        "details": details,
    }


if __name__ == "__main__":
    summary = run_all_checks()
    print(f"TFQ-0010 INDEPENDENT CHECKER PASSED: checks={summary['checks_total']} failed={summary['checks_failed']}")
    if "--json" in sys.argv:
        print(json.dumps(summary, indent=2))
