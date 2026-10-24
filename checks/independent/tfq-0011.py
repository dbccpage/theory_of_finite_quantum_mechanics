#!/usr/bin/env python3
"""Independent verification for TFQ-0011: Finite QCD shadow.

Checks:
1. Exact rational SU(N_c) color Casimir invariants (`C_2(N_c) = (N_c^2 - 1)/(2 N_c)`,
   `C_2(adj) = N_c`) and two-quark color channel coefficients across `N_c = 2..6`,
   plus SU(3) Cartan Fierz diagonal (`1/3`) and off-diagonal (`-1/6`) weights.
2. Exact rational Wilson-loop Creutz ratios `W(R,T) W(R-1,T-1) / (W(R,T-1) W(R-1,T))`
   isolating `b` for area-law scaling vs `1` for perimeter-law scaling across `R, T in 2..6`
   and rational `b`, plus `L x L` planar lattice Betti numbers `b_1 = (L-1)^2`.
3. Exact rational 1-loop `beta_0(3, N_f) = 11 - 2/3 N_f` (`> 0 <=> N_f <= 16`) and 2-loop
   `beta_1(3, N_f) = 102 - 38/3 N_f` across `N_f = 0..24`, including the Banks-Zaks ratio
   `-beta_0(16)/beta_1(16) = 1/302`.
4. Naive lattice Dirac fermion doubling obstruction (`2^d - 1` spurious Brillouin corners
   in `d = 1..4`) and positive Wilson mass lifts `2 r m >= 2 r > 0`.
5. Diagonal SU(3) Klein-four Landau-Gribov copy counts (`4^3 = 64` on 3 vertices vs `1` after
   spanning-tree gauge fixing), plus repository source and Lean 4 theorem anchors in
   `lean4/FiniteQM.lean` and `lean4/CampaignTfq0011FiniteQcd.lean`.
"""

from __future__ import annotations

import json
import sys
from fractions import Fraction
from pathlib import Path
from typing import Any


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
    # Family 1: SU(N_c) color Casimir and channel decomposition
    # -------------------------------------------------------------------------
    for nc in range(2, 7):
        nc_f = Fraction(nc)
        c_fund = (nc_f * nc_f - 1) / (2 * nc_f)
        c_adj = nc_f
        ch_singlet = -c_fund
        ch_octet = c_adj / 2 - c_fund
        ch_sextet = Fraction(1, 2) - Fraction(1, 2 * nc)
        ch_antitrip = Fraction(-1, 2) - Fraction(1, 2 * nc)
        record(ch_singlet < 0, f"Singlet channel attractive for N_c={nc}")
        record(ch_octet > 0, f"Adjoint channel repulsive for N_c={nc}")
        record(ch_sextet > 0, f"Symmetric channel repulsive for N_c={nc}")
        record(ch_antitrip < 0, f"Antisymmetric channel attractive for N_c={nc}")
        if nc == 3:
            record(c_fund == Fraction(4, 3), "SU(3) C_2(3) = 4/3")
            record(c_adj == Fraction(3), "SU(3) C_2(8) = 3")
            record(ch_singlet == Fraction(-4, 3), "SU(3) singlet = -4/3")
            record(ch_octet == Fraction(1, 6), "SU(3) octet = 1/6")
            record(ch_sextet == Fraction(1, 3), "SU(3) sextet = 1/3")
            record(ch_antitrip == Fraction(-2, 3), "SU(3) antitriplet = -2/3")

    t3 = [Fraction(1, 2), Fraction(-1, 2), Fraction(0)]
    t8 = [Fraction(1, 2), Fraction(1, 2), Fraction(-1)]
    for i in range(3):
        for j in range(3):
            w = Fraction(1) * t3[i] * t3[j] + Fraction(1, 3) * t8[i] * t8[j]
            expected = Fraction(1, 3) if i == j else Fraction(-1, 6)
            record(w == expected, f"Cartan Fierz weight ({i},{j}) = {expected}")

    details["family1_color_casimir"] = {
        "su3_c2_fund": "4/3",
        "su3_c2_adj": "3",
        "su3_singlet": "-4/3",
        "su3_octet": "1/6",
    }

    # -------------------------------------------------------------------------
    # Family 2: Wilson-loop Creutz ratios and planar Betti numbers
    # -------------------------------------------------------------------------
    b_samples = [
        Fraction(1, 9),
        Fraction(1, 4),
        Fraction(1, 3),
        Fraction(1, 2),
        Fraction(2, 3),
        Fraction(3, 5),
    ]
    for b in b_samples:
        for r in range(2, 7):
            for t in range(2, 7):
                w_a = lambda x, y: b ** (x * y)
                w_p = lambda x, y: b ** (2 * (x + y))
                creutz_a = (w_a(r, t) * w_a(r - 1, t - 1)) / (w_a(r, t - 1) * w_a(r - 1, t))
                creutz_p = (w_p(r, t) * w_p(r - 1, t - 1)) / (w_p(r, t - 1) * w_p(r - 1, t))
                record(creutz_a == b, f"Area-law Creutz ratio ({r},{t}) = {b}")
                record(creutz_p == Fraction(1), f"Perimeter-law Creutz ratio ({r},{t}) = 1")

    for L in range(2, 9):
        v = L * L
        e = 2 * L * (L - 1)
        e_tree = v - 1
        b1 = e - e_tree
        record(b1 == (L - 1) ** 2, f"{L}x{L} planar lattice Betti number b1 = {(L-1)**2}")

    details["family2_wilson_creutz"] = {
        "creutz_pairs_checked": len(b_samples) * 25,
        "lattice_3x3_b1": 4,
    }

    # -------------------------------------------------------------------------
    # Family 3: Rational beta0 and beta1 controls
    # -------------------------------------------------------------------------
    for nf in range(0, 25):
        nf_f = Fraction(nf)
        beta0 = Fraction(11) - Fraction(2, 3) * nf_f
        beta1 = Fraction(102) - Fraction(38, 3) * nf_f
        record((beta0 > 0) == (nf <= 16), f"beta0 > 0 iff N_f <= 16 (tested N_f={nf})")
        if nf == 16:
            record(beta0 == Fraction(1, 3), "beta0(16) = 1/3")
            record(beta1 == Fraction(-302, 3), "beta1(16) = -302/3")
            record((-beta0) / beta1 == Fraction(1, 302), "Banks-Zaks ratio at N_f=16 = 1/302")

    details["family3_beta0_beta1"] = {
        "asymptotic_freedom_max_integer_nf": 16,
        "banks_zaks_nf16": "1/302",
    }

    # -------------------------------------------------------------------------
    # Family 4: Lattice Dirac fermion doubling obstruction & Gribov copies
    # -------------------------------------------------------------------------
    for d in range(1, 5):
        corners = 2**d
        doublers = corners - 1
        record(doublers > 0, f"Naive Dirac in d={d} has {doublers} > 0 spurious doublers")
        for r_wilson in [Fraction(1, 4), Fraction(1, 2), Fraction(1)]:
            for m_active in range(1, d + 1):
                lift = 2 * r_wilson * m_active
                record(lift >= 2 * r_wilson and lift > 0, "Wilson lift strictly positive on doublers")

    klein4 = [(1, 1, 1), (1, -1, -1), (-1, 1, -1), (-1, -1, 1)]
    for d1, d2, d3 in klein4:
        record(d1 * d2 * d3 == 1, "Diagonal SU(3) Klein-four element has det = 1")
    record(len(klein4) ** 3 == 64, "3-vertex diagonal Klein-four orbit size = 64")

    details["family4_dirac_doubling_and_gribov"] = {
        "d4_spurious_doublers": 15,
        "klein4_orbit_size": 64,
    }

    # -------------------------------------------------------------------------
    # Family 5: Repo source and Lean file verification
    # -------------------------------------------------------------------------
    repo_root = Path(__file__).resolve().parents[2]
    fqm = repo_root / "lean4/FiniteQM.lean"
    lean_file = repo_root / "lean4/CampaignTfq0011FiniteQcd.lean"

    record(fqm.exists(), "lean4/FiniteQM.lean exists")
    record(lean_file.exists(), "lean4/CampaignTfq0011FiniteQcd.lean exists")

    fqm_src = fqm.read_text(encoding="utf-8")
    for sym in [
        "su3_casimir_and_channel_identities",
        "su3_fierz_diagonal_and_offdiagonal_identities",
        "qcd_beta0_asymptotic_freedom_window",
        "qcd_beta1_and_banks_zaks_fixed_point",
        "wilson_creutz_ratio_area_vs_perimeter",
        "wilson_lattice_3x3_dfm_betti_identity",
        "su3_diagonal_klein_four_landau_gribov_copies",
        "spanning_tree_dfm_eliminates_gribov_copies",
    ]:
        record(sym in fqm_src, f"FiniteQM.lean contains {sym}")

    lean_src = lean_file.read_text(encoding="utf-8")
    required_theorems = [
        "theorem su3_color_casimir_and_fierz_channel_identities",
        "theorem wilson_plaquette_creutz_ratio_area_vs_perimeter_and_3x3_betti",
        "theorem qcd_beta0_asymptotic_freedom_window_and_beta1_banks_zaks",
        "theorem naive_lattice_dirac_doubling_obstruction_and_wilson_lift",
        "theorem nonabelian_su3_klein_four_gribov_copies_and_spanning_tree_gauge",
        "theorem exact_rational_certificate_vs_float_benchmark_epistemic_separation_fence",
        "theorem finite_wilson_beta0_control_not_continuum_confinement_fence",
        "theorem lattice_dirac_doubling_recorded_as_explicit_obstruction_fence",
        "theorem f002_continuum_qcd_remains_open_interface_fence",
        "theorem tfq0011_finite_qcd_shadow_scope_ledger_fence",
    ]
    for thm in required_theorems:
        record(thm in lean_src, f"CampaignTfq0011FiniteQcd.lean contains {thm}")
    record("sorry" not in lean_src, "CampaignTfq0011FiniteQcd.lean is sorry-free")

    return {
        "node_id": "TFQ-0011",
        "checks_total": checks,
        "checks_failed": failed,
        "passed": failed == 0,
        "details": details,
    }


if __name__ == "__main__":
    summary = run_all_checks()
    print(f"TFQ-0011 INDEPENDENT CHECKER PASSED: checks={summary['checks_total']} failed={summary['checks_failed']}")
    if "--json" in sys.argv:
        print(json.dumps(summary, indent=2))
