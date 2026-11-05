"""Replay of every number and symbolic claim in ../critique_wdp_po.md.

Provenance: written 2026-11-05 for the Witnessed Difference Programme (WDP) and
Projection Obstruction (PO) audit of Nishiyama, Tanaka, Tuszynski, Tsenkova,
"Holographic Brain Theory: Super-Radiance, Memory Capacity and Control Theory",
IJMS 25(4):2399 (2024). Equation numbers refer to ../ijms-25-02399.md.

Run:  python -I critique_checks.py        (needs numpy and sympy; no scipy)

Every check prints one tag:
  DERIVED   follows from the paper's own equations, or from standard physics,
            by the steps shown here;
  SUPPLIED  a value put in by me, named as such;
  CITED     a standard result used but not re-derived here;
  OPEN      needs information the paper does not give.

Gauss's law in Appendix C and the Landauer retention barrier are replayed in
adversarial_review_checks.py (PR #513) and are not repeated here.
"""

from __future__ import annotations

import math

import numpy as np
import sympy as sp

LINE = "-" * 78


def banner(n: int, title: str) -> None:
    print(f"\n{LINE}\nCheck {n}: {title}\n{LINE}")


# ---------------------------------------------------------------------------
# Check 1. The gauge pair of Appendix A is a constraint on the matter, not a
# gauge choice.  With A^0 = 0 the paper's own (A7) reads
#     +/- d_t (div A) = J_0 + c(x) = -e |phi|^2 + c(x).
# Imposing div A = 0 for all t therefore forces d_t |phi|^2 = 0 pointwise.
# For the two-level state of (A8), (A12) that kills the coherence R = 2 chi0* chi1,
# and with it the right-hand side of (A38): no super-radiant pulse.
# ---------------------------------------------------------------------------
def check_1_gauge_pair() -> None:
    banner(1, "A^0 = 0 together with div A = 0 freezes the charge density (A7)")
    t, x = sp.symbols("t x", real=True)
    Omega = sp.symbols("Omega", positive=True)
    chi0, chi1 = sp.symbols("chi0 chi1")            # slowly varying envelopes
    phi0 = sp.Function("phi0")(x)                     # real eigenfunctions
    phi1 = sp.Function("phi1")(x)
    # (A8), (A12): phi = sum_n e^{-i E_n t} chi_n phi_n  ->  density up to a
    # common phase; keep only the t-dependence through Omega = E_1 - E_0.
    phi = chi0 * phi0 + sp.exp(-sp.I * Omega * t) * chi1 * phi1
    rho = sp.simplify(sp.expand(phi * sp.conjugate(phi)))
    drho = sp.simplify(sp.diff(rho, t))
    # div A = 0 for all t  =>  d_t rho = 0 (from (A7) with A^0 = 0, any c(x)).
    # Solve d_t rho = 0 for the coherence:
    R = sp.symbols("R")  # R = 2 chi0* chi1 (paper's definition after (A35))
    drho_in_R = sp.simplify(drho.subs(sp.conjugate(chi0) * chi1, R / 2)
                            .subs(chi0 * sp.conjugate(chi1), sp.conjugate(R) / 2))
    print("  density of the two-level state:  rho =", rho)
    print("  d rho / dt =", drho_in_R)
    print("  d rho/dt = 0 for all x with phi0*phi1 != 0  =>  R = 0")
    print("  (A38): d A/dt = (g Omega / 4 pi L3) R  =>  A = const: no pulse.")
    print("  Keeping the integration constant c(x) of (A7) does not help:")
    print("  it is time independent, the dipole term oscillates at Omega.")
    print("  TAG: DERIVED (A6, A7, A8, A12, A38).  The 'Coulomb gauge' of")
    print("  Appendix A is the radiation gauge; it is a gauge only when J_0 = 0.")

    # Proca variant used in Appendix B: with M^2 != 0 and conserved current,
    # d_mu A^mu = 0 is forced (take the divergence of the Proca equation).
    # With A^0 = 0 that is div A = 0, and Gauss's law then forces |phi|^2 = 0.
    print("  Appendix B (A48) adds M^2 A_i.  Divergence of the Proca equation")
    print("  with a conserved current gives M^2 d_mu A^mu = 0, so A^0 = 0")
    print("  forces div A = 0 at all times, and then (A7) forces |phi|^2 = 0.")
    print("  TAG: DERIVED (standard Proca identity, CITED).")


# ---------------------------------------------------------------------------
# Check 2. (A36)-(A38) with the loss term of (A42) reproduce the sech pulse
# (A45)-(A47) in the limit L3 -> 0 (adiabatic elimination of the field).
# Units: g = Omega = N = 1, so tau_R = 2 pi.  theta_0 is SUPPLIED by the paper
# (the quantum initiation theta_0 ~ 2/sqrt(N), Gross & Haroche 1982, is not
# derived there).
# ---------------------------------------------------------------------------
def check_2_maxwell_bloch_sech() -> None:
    banner(2, "Maxwell-Bloch (A36)-(A38) + loss (A42) -> sech pulse (A45)")
    g, Om, N = 1.0, 1.0, 1.0
    tau_R = 2 * math.pi / (g * g * Om * N)             # (A46)
    theta0 = 0.01                                       # SUPPLIED tipping angle
    tau0 = -tau_R * math.log(math.tan(theta0 / 2))     # after (A46)

    def rhs(y, L3):
        Z, R, A = y
        return np.array([-2 * g * A * R,                         # (A36)
                         2 * g * A * Z,                          # (A37)
                         g * Om / (4 * math.pi * L3) * R - A / L3])  # (A38)+(A42)

    def rk4(y0, L3, T, h):
        y = np.array(y0, float)
        ts = np.arange(0.0, T, h)
        out = np.empty((len(ts), 3))
        for i, _ in enumerate(ts):
            out[i] = y
            k1 = rhs(y, L3)
            k2 = rhs(y + 0.5 * h * k1, L3)
            k3 = rhs(y + 0.5 * h * k2, L3)
            k4 = rhs(y + h * k3, L3)
            y = y + h / 6 * (k1 + 2 * k2 + 2 * k3 + k4)
        return ts, out

    for L3 in (0.5, 0.05, 0.005):                       # SUPPLIED, in units 1/Omega
        y0 = [N * math.cos(theta0), N * math.sin(theta0), 0.0]
        ts, out = rk4(y0, L3, 2.2 * tau0, min(1e-3, L3 / 20))
        A_num = out[:, 2]
        A_sech = g * Om * N / (4 * math.pi) / np.cosh((ts - tau0) / tau_R)   # (A45)
        err = np.max(np.abs(A_num - A_sech)) / np.max(A_sech)
        i_pk = int(np.argmax(A_num))
        cons = np.max(np.abs(out[:, 0] ** 2 + out[:, 1] ** 2 - N * N))
        print(f"  L3 = {L3:6.3f}: peak A num = {A_num[i_pk]:.5f} at t = {ts[i_pk]:7.2f};"
              f"  sech peak = {g*Om*N/(4*math.pi):.5f} at tau0 = {tau0:7.2f};"
              f"  max rel. error = {err:.3e};  max |Z^2+R^2-N^2| = {cons:.1e}")
    print("  TAG: DERIVED. The sech solution is the bad-cavity (L3 -> 0) limit of")
    print("  the semiclassical Maxwell-Bloch equations; it needs theta_0, g, Omega,")
    print("  N, L3, none of which the paper gives a value for -> tau_R is OPEN.")


# ---------------------------------------------------------------------------
# Check 3. Madelung form of (A63) with Gamma_2 and D^{11} dropped gives (A69)
# and (A70) exactly.  Two spatial dimensions, as in Appendix C.
# ---------------------------------------------------------------------------
def check_3_madelung() -> None:
    banner(3, "(A63) with Gamma_2 = D^11 = 0  <=>  continuity (A69) + Bohm constraint (A70)")
    t, x, y = sp.symbols("t x y", real=True)
    e, m = sp.symbols("e m", positive=True)
    J = sp.symbols("J")                                  # stands for the imaginary unit
    Rf = sp.Function("R")(t, x, y)                       # |phi-bar|, real
    beta = sp.Function("beta")(t, x, y)                  # phase, real
    A0 = sp.Function("A0")(t, x, y)
    A1 = sp.Function("A1")(t, x, y)
    A2 = sp.Function("A2")(t, x, y)

    # Work on prefactors: phi = F e^{i beta}.  Then d_v(F e^{i beta}) = (F_v + J beta_v F) e^{i beta},
    # so the covariant derivative acts on prefactors as D_v F = F_v + J beta_v F - J e A_v F.
    def D(F, var, A):
        return sp.diff(F, var) + J * sp.diff(beta, var) * F - J * e * A * F

    F = Rf
    pref = (J * (sp.diff(F, t) + J * sp.diff(beta, t) * F) + e * A0 * F
            + (D(D(F, x, A1), x, A1) + D(D(F, y, A2), y, A2)) / (2 * m))   # (A63) / e^{i beta}
    poly = sp.Poly(sp.expand(pref), J)
    coeffs = {k[0]: c for k, c in zip(poly.monoms(), poly.coeffs())}
    # J^2 = -1, J^3 = -J, J^4 = 1 ...
    re_part = sum(c * (-1) ** (k // 2) for k, c in coeffs.items() if k % 2 == 0)
    im_part = sum(c * (-1) ** ((k - 1) // 2) for k, c in coeffs.items() if k % 2 == 1)

    V1 = A1 - sp.diff(beta, x) / e                       # gauge-invariant combination of (A69)
    V2 = A2 - sp.diff(beta, y) / e
    # (A69): d_t R^2 = (e/m) [ d_x(R^2 V1) + d_y(R^2 V2) ]
    a69 = sp.diff(Rf ** 2, t) - (e / m) * (sp.diff(Rf ** 2 * V1, x) + sp.diff(Rf ** 2 * V2, y))
    test69 = sp.simplify(sp.expand(2 * Rf * im_part - a69))
    test69b = sp.simplify(sp.expand(2 * Rf * im_part + a69))
    # (A70) as printed: A0 - d_t beta / e = -lap R/(2 m e R) - (e/2m)(V1^2 + V2^2)
    # (A81), (A87) as printed:   A0 = -lap R/(2 m e R) + e(A1^2 + A2^2)/(2m)   (plus sign)
    lap_term = (sp.diff(Rf, x, 2) + sp.diff(Rf, y, 2)) / (2 * m * e * Rf)
    a70_printed = A0 - sp.diff(beta, t) / e + lap_term + (e / (2 * m)) * (V1 ** 2 + V2 ** 2)
    a70_plus = A0 - sp.diff(beta, t) / e + lap_term - (e / (2 * m)) * (V1 ** 2 + V2 ** 2)
    test70_printed = sp.simplify(sp.expand(re_part / (e * Rf) - a70_printed))
    test70_plus = sp.simplify(sp.expand(re_part / (e * Rf) - a70_plus))
    print("  2R * Im[(A63)/phi] - (A69) =", test69, "   (other sign:", test69b, ")")
    print("  Re[(A63)/phi]/(eR) - (A70 as printed, minus sign) =", sp.factor(test70_printed))
    print("  Re[(A63)/phi]/(eR) - (A70 with the (A81)/(A87) plus sign) =", test70_plus)
    ok = (test69 == 0 or test69b == 0) and test70_plus == 0
    print("  TAG: DERIVED" if ok else "  TAG: MISMATCH, inspect",
          "- (A69)/(A70) are the Madelung (charged-superfluid) form of (A63).")
    print("  Printed-sign finding: (A70) carries -(e/2m)(A - grad beta/e)^2; the derivation")
    print("  and (A81), (A87) carry +. The simulation equations (A87) have the derived sign.")
    print("  The only term carrying hbar after restoring units is the Bohm term")
    print("  -hbar^2 lap R / (2 m e R) in (A70)/(A81)/(A87).  Drop it (hbar -> 0) and")
    print("  (A76)-(A87) are classical charged-fluid + Maxwell + Proca + Ohmic damping.")


# ---------------------------------------------------------------------------
# Check 4. Size of the Bohm term at the step edge of Figure 6 with the paper's
# own parameters: e = 0.3, |phi|^2 = 1 -> 0.79 (21 % dip), A ~ 0.1 (targets),
# lattice m a_s = 1.  The edge width w (in cells) is not reported: OPEN.
# ---------------------------------------------------------------------------
def check_4_bohm_term_size() -> None:
    banner(4, "Bohm term vs the A^2 term in A_0 (A87) at the Figure 6 step edge")
    e, A = 0.3, 0.1                                  # paper's values (Section 4)
    R_in, R_out = math.sqrt(0.79), 1.0               # |phi-bar| inside / outside the dip
    dR = R_out - R_in
    a2 = e * (A * A) / 2.0                           # e(A1^2+A2^2)/2m, in units of m
    print(f"  e A^2 / 2m term        = {a2:.4f} m     (A ~ 0.1 target amplitude)")
    for w in (1, 2, 5, 10, 30):
        bohm = dR / (w * w) / (2 * e * R_in)         # lap R ~ dR / w^2 (cells), / (2 m e R)
        print(f"  edge width w = {w:2d} cells: |Bohm term| ~ {bohm:.4f} m   ratio to A^2 term = {bohm/a2:7.1f}")
    print("  TAG: DERIVED (orders of magnitude from the paper's parameters);")
    print("  the simulated edge width, and so the actual ratio, is OPEN.")


# ---------------------------------------------------------------------------
# Check 5. Appendix B reconstruction amplitude with the Section 4 parameters:
# the hologram modulates the field by e^2 |phi|^2 / (M^2 m) (A49).
# Units: m a_s = 1, |phi|^2 = 1 means |phi|^2 = m^3.
# ---------------------------------------------------------------------------
def check_5_hologram_modulation() -> None:
    banner(5, "Hologram modulation depth e^2 |phi|^2 / (M^2 m)  (A49), Section 4 numbers")
    e, phi2, M2 = 0.3, 1.0, 2.0                      # e, |phi|^2 (m^3), M^2 (m^2)
    depth = e * e * phi2 / M2                        # dimensionless, m's cancel
    print(f"  e^2 |phi|^2 / (M^2 m) = {depth:.4f}  -> reconstruction term |r|^2 o carries")
    print(f"  {100*depth:.1f} % of the reference amplitude, diffraction efficiency ~ {depth**2:.1e}")
    print("  (A49) expansion is valid only when this number is small, so a strong")
    print("  reconstruction and a valid expansion exclude each other. TAG: DERIVED.")
    print("  The object wave o has no source in (A48)-(A52): SUPPLIED by the paper.")
    print("  |phi|^2 ∝ |r+o|^2 (A51) is put in, not produced by (A80): SUPPLIED.")


# ---------------------------------------------------------------------------
# Check 6. "Single-mode waveguides with a cutoff wavelength 21 nm" (Section 5).
# Perfectly conducting circular pipe: dominant TE11 cutoff lambda_c = 1.7063 d.
# Dielectric rod/tube (what a protein cylinder in water is): no cutoff, but the
# V-number decides confinement.  CITED: Jackson; Snyder & Love.
# ---------------------------------------------------------------------------
def check_6_waveguide() -> None:
    banner(6, "Microtubule as a waveguide: the 21 nm cutoff read both ways")
    p11 = 1.8412                                     # first zero of J1'  (TE11)
    lam_c_over_d = 2 * math.pi / (2 * p11)           # lambda_c = pi d / p11' = 1.7063 d
    d = 21.0 / lam_c_over_d
    print(f"  conducting pipe: lambda_c = {lam_c_over_d:.4f} d; 21 nm cutoff <-> d = {d:.1f} nm")
    print("  propagation needs lambda < lambda_c: 500 nm, 1500 nm and all of UV-NIR are")
    print("  BELOW cutoff (evanescent).  The sentence 'guide light from strong UV to NIR'")
    print("  has the inequality backwards under the model that gave the 21 nm.")
    n_core, n_clad = 1.50, 1.33                      # SUPPLIED: protein, water
    for d_nm, lam in ((25.0, 500.0), (25.0, 1500.0), (15.0, 500.0)):
        V = math.pi * d_nm / lam * math.sqrt(n_core ** 2 - n_clad ** 2)
        print(f"  dielectric cylinder d = {d_nm:4.0f} nm, lambda = {lam:5.0f} nm: V = {V:.3f}"
              f"  (single-mode below 2.405; V << 1 means the mode is essentially unconfined)")
    print("  TAG: DERIVED from CITED textbook formulas; indices SUPPLIED.")


# ---------------------------------------------------------------------------
# Check 7. Emission direction in Appendix A.  (A10)-(A13): A_1 = A_2 = 0, the
# wave vector is k = (k1, k2, 0).  So the field is polarized along the
# microtubule axis x^3 and propagates perpendicular to it.  A dipole along x^3
# radiates with pattern sin^2(theta) (theta from the axis): nothing along the axis.
# ---------------------------------------------------------------------------
def check_7_emission_direction() -> None:
    banner(7, "Where the super-radiant light goes (A10)-(A13), (A27)")
    for deg in (0, 30, 60, 90):
        th = math.radians(deg)
        print(f"  theta = {deg:2d} deg from the x^3 axis: dipole pattern sin^2 = {math.sin(th)**2:.3f}")
    print("  k = (k1, k2, 0) (A13): propagation in the plane perpendicular to the axis.")
    print("  Figure 1 draws rings of light leaving the ENDS of the microtubule, and")
    print("  Section 5 needs axial guiding.  Both are SUPPLIED against (A13). TAG: DERIVED.")


# ---------------------------------------------------------------------------
# Check 8. Energy budget.  Section 5: 10^-13 W per mitochondrion (CITED by the
# paper).  Photon at 500 nm: 2.48 eV.  Capacity (5): 2.5 PB = 2e16 bit.
# ---------------------------------------------------------------------------
def check_8_energy_budget() -> None:
    banner(8, "Energy budget: photons per second from 1e-13 W, bits to write")
    eV = 1.602176634e-19
    E_ph = 1239.84198 / 500.0                        # eV
    rate = 1e-13 / (E_ph * eV)
    bits = 2.5e15 * 8
    years = bits / rate / 3.15576e7
    print(f"  photon energy at 500 nm = {E_ph:.3f} eV;  1e-13 W = {rate:.2e} photons/s")
    print(f"  2.5 PB = {bits:.1e} bit; at >= 1 photon per bit one such source needs {years:.0f} years")
    print("  The paper does not say how many sources, nor a write time: the budget is OPEN.")
    print("  TAG: DERIVED arithmetic on the paper's own numbers.")


# ---------------------------------------------------------------------------
# Check 9. The mass m fixes every scale of Appendix C (m a_s = 1).  Two readings.
# ---------------------------------------------------------------------------
def check_9_scale_m() -> None:
    banner(9, "No scale: the lattice unit a_s = hbar c / m c^2 ties fringes to M^2 and gamma")
    hbar_c = 197.3269804                             # eV nm
    hbar = 6.582119569e-16                           # eV s
    for m_eV, label in ((4e-3, "paper's water rotational scale, 4 meV (Section 5)"),
                        (hbar_c / 100.0, "m chosen so that a_s = 100 nm resolves 500 nm fringes")):
        a_s = hbar_c / m_eV                          # nm
        box = 128 * a_s
        cell = 30 * a_s
        t_unit = hbar / m_eV
        M = math.sqrt(2.0) * m_eV
        gamma = 0.2 * m_eV
        print(f"  m = {m_eV:.4g} eV ({label}):")
        print(f"     a_s = {a_s:.4g} nm, 128-cell box = {box/1e6:.4g} mm, N1 = 30 cells = {cell/1e6:.4g} mm,"
              f" m x^0 = 200 -> {200*t_unit:.3g} s")
        print(f"     M = sqrt(2) m = {M:.3g} eV, gamma = 0.2 m = {gamma:.3g} eV = {gamma/hbar:.3g} s^-1")
    print("  Either the hologram cell is millimetres (not an optical hologram at 500 nm),")
    print("  or the Meissner mass and the damping are electron-volt quantities in water.")
    print("  TAG: DERIVED; the paper never chooses m, so Section 4 has no units: OPEN.")


# ---------------------------------------------------------------------------
# Check 10. PO Theorem 5.1 on a toy with the paper's coupling structure.
# Two bosonic modes a (field) and b (matter density), coherent product start.
#   H = w a†a + W b†b + g (b†b) (a + a†)        (density times field quadrature)
# Pure-state normal rate (PO §5.3.1): nu = 2 ||chi||, chi = centred h applied to
# the product state.  For this H: nu = 2 g * Delta(b†b) * Delta(a+a†) = 2 g |beta| * 1.
# The paper's Appendix C runs the product (mean-field) trajectory and never
# computes nu, g or the window.  This check computes them for the toy.
# ---------------------------------------------------------------------------
def check_10_po_theorem_5_1_toy() -> None:
    banner(10, "PO Theorem 5.1: entanglement budget of a mean-field (product) run, toy")
    nmax = 28                                        # SUPPLIED truncation
    g, w, W = 0.05, 1.0, 1.0                         # SUPPLIED
    alpha, beta = 1.0, 1.5                           # SUPPLIED coherent amplitudes
    a = np.diag(np.sqrt(np.arange(1, nmax)), 1).astype(complex)
    n = a.conj().T @ a
    I = np.eye(nmax)
    x = a + a.conj().T
    H = w * np.kron(n, I) + W * np.kron(I, n) + g * np.kron(x, n)   # a ⊗ b ordering
    h_e = g * np.kron(x, n)

    def coh(z):
        v = np.array([z ** k / math.sqrt(math.factorial(k)) for k in range(nmax)], complex)
        return v / np.linalg.norm(v)

    va, vb = coh(alpha), coh(beta)
    u = np.kron(va, vb)
    # centred interaction applied to u: chi = (1-|a><a|) ⊗ (1-|b><b|) h u
    Pa = I - np.outer(va, va.conj())
    Pb = I - np.outer(vb, vb.conj())
    chi = np.kron(Pa, Pb) @ (h_e @ u)
    nu = 2 * np.linalg.norm(chi)
    nu_formula = 2 * g * abs(beta) * 1.0             # Delta n_b = |beta|, Delta x_a = 1
    g_inc = np.linalg.norm(h_e, 2)                   # incident interaction norm (2-local part)
    print(f"  nu (numeric, 2||chi||) = {nu:.6f};  nu (formula 2 g |beta| Delta x) = {nu_formula:.6f}")
    print(f"  incident norm g_inc = ||h_e||_inf = {g_inc:.3f} (truncation {nmax} levels)")
    E, V = np.linalg.eigh(H)
    rho0 = np.outer(u, u.conj())

    def defect(t):
        U = (V * np.exp(-1j * E * t)) @ V.conj().T
        rho = U @ rho0 @ U.conj().T
        r4 = rho.reshape(nmax, nmax, nmax, nmax)
        rho_a = np.einsum("ijkj->ik", r4)
        rho_b = np.einsum("ijil->jl", r4)
        Dm = rho - np.kron(rho_a, rho_b)
        return np.sum(np.abs(np.linalg.eigvalsh((Dm + Dm.conj().T) / 2)))

    t_half = nu / (48 * g_inc ** 2)                  # half-slope window of Theorem 5.1
    print(f"  half-slope window t <= nu/(48 g_inc^2) = {t_half:.3e}")
    for t in (0.25 * t_half, t_half, 0.05, 0.2, 0.5, 1.0):
        D = defect(t)
        lb = nu * t - 24 * g_inc ** 2 * t * t
        print(f"  t = {t:9.3e}: D(t) = {D:.6e}   nu t = {nu*t:.6e}   lower bound = {max(lb,0):.6e}"
              f"   {'ok' if D >= lb - 1e-12 else 'VIOLATED'}")
    print("  TAG: DERIVED on a SUPPLIED toy. The quantity the paper owes for Appendix C is")
    print("  this nu (and Lambda_* for the damped case), with its e, m, N: OPEN.")


# ---------------------------------------------------------------------------
# Check 11. Small arithmetic the text relies on.
# ---------------------------------------------------------------------------
def check_11_small_arithmetic() -> None:
    banner(11, "Small arithmetic")
    gain = 0.1 * 2 ** 4 / 0.8 ** 4
    print(f"  static-inversion gain 0.1 (M^2/m^2)^4 / v^4 = {gain:.3f}  (paper: 'approximately 3')")
    n_water = 3.34e22                                # molecules per cm^3 (CITED)
    per_lam3 = n_water * (500e-7) ** 3
    print(f"  water molecules per (500 nm)^3 = {per_lam3:.2e}")
    kT = 8.617333262e-5 * 310
    print(f"  k_B T at 310 K = {1e3*kT:.2f} meV; 4 meV / k_B T = {4e-3/kT:.3f} (the water scale is thermal)")
    print("  TAG: DERIVED.")


if __name__ == "__main__":
    check_1_gauge_pair()
    check_2_maxwell_bloch_sech()
    check_3_madelung()
    check_4_bohm_term_size()
    check_5_hologram_modulation()
    check_6_waveguide()
    check_7_emission_direction()
    check_8_energy_budget()
    check_9_scale_m()
    check_10_po_theorem_5_1_toy()
    check_11_small_arithmetic()
    print(f"\n{LINE}\nDone.\n")
