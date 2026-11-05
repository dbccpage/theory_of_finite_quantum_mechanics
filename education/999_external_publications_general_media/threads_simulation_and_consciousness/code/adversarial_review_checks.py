"""Checks for adversarial_review.md (threads_simulation_and_consciousness).

Provenance: written 2026-11-05 for the adversarial review of two ChatGPT
arguments about Nishiyama et al., IJMS 25(4):2399 (2024). Equation numbers
refer to ijms-25-02399.md in this folder.

Run: python adversarial_review_checks.py   (needs sympy)

Check 1 (symbolic): for the Appendix C system (A82)-(A87), compute
  d/dt (div E - J^0)
using only the paper's own equations. Maxwell's equations would make this zero.
Check 2 (exact rational arithmetic plus logs evaluated at the end): the
Landauer and retention numbers.
"""

import sympy as sp

t, x, y = sp.symbols("t x y", real=True)
e, m, M2, gam, v = sp.symbols("e m M2 gamma v", positive=True)

A1 = sp.Function("A1")(t, x, y)
A2 = sp.Function("A2")(t, x, y)
E1 = sp.Function("E1")(t, x, y)
E2 = sp.Function("E2")(t, x, y)
rho = sp.Function("n")(t, x, y)          # |phi|^2, the boson density
A0 = sp.Function("A0")(t, x, y)
B1 = sp.Function("B1")(t, x, y)          # A1^(n-1) + A1^(n+1), neighbouring layers
B2 = sp.Function("B2")(t, x, y)


def check_gauss(coef):
    """coef is the coefficient of |phi|^2 A_i in the Ampere equation."""
    dE1 = sp.diff(A1, y, 2) - sp.diff(A2, x, y) - coef * rho * A1 - M2 * A1 \
        - gam * (E1 + sp.diff(A0, x)) + v * B1                     # (A82)
    dE2 = sp.diff(A2, x, 2) - sp.diff(A1, x, y) - coef * rho * A2 - M2 * A2 \
        - gam * (E2 + sp.diff(A0, y)) + v * B2                     # (A84)
    drho = (e / m) * (sp.diff(rho * A1, x) + sp.diff(rho * A2, y))  # (A86)
    J0 = -e * rho                                                  # (A66)
    d_divE = sp.diff(dE1, x) + sp.diff(dE2, y)
    d_J0 = -e * drho
    return sp.simplify(sp.expand(d_divE - d_J0))


print("Check 1a: d/dt(div E - J^0) with e^2/m, as in (A71) and (A82):")
r = check_gauss(e**2 / m)
print("   ", r)
# Separate the pieces by parameter.
for name, sym in (("M^2", M2), ("gamma", gam), ("v", v)):
    print(f"    {name} part:", sp.simplify(r.coeff(sym)))
rest = sp.simplify(r - sum(r.coeff(s) * s for s in (M2, gam, v)))
print("    remainder with no M^2, gamma, v:", rest)

print("\nCheck 1b: same, with e/m as printed in (A76):")
r_typo = check_gauss(e / m)
r_typo_rest = sp.simplify(r_typo - sum(r_typo.coeff(s) * s for s in (M2, gam, v)))
print("    remainder with no M^2, gamma, v:", sp.factor(r_typo_rest))

print("\nCheck 1c: initial data. E = 0, A = 0, |phi| = 1 at t = 0.")
print("    div E = 0, J^0 = -e. (A68) with its integration constant set to zero")
print("    requires div E = J^0, so it fails at t = 0 unless a background +e is kept.")

print("\nCheck 1d: the target fields (10)-(11) are curl-free.")
n1, n2, Ns, N1, N2 = sp.symbols("n1 n2 N_s N_1 N_2")
A1t = sp.Function("f")(n1)   # (10) depends on n1 only
A2t = sp.Function("g")(n2)   # (11) depends on n2 only
curl = sp.diff(A2t, n1) - sp.diff(A1t, n2)
print("    d1 A2_target - d2 A1_target =", curl, "(so the drive is purely longitudinal)")

print("\nCheck 2: thermal numbers (eV, K).")
kB = sp.Rational(8617333262, 10**14)      # eV/K (CODATA, exact SI definition)
hc = sp.Rational(123984198, 10**8)        # eV*um
T = 310
kT = kB * T
kTln2 = kT * sp.log(2)
Eph = hc / sp.Rational(1, 2)             # 500 nm = 0.5 um
print("    k_B T          =", sp.N(kT, 6), "eV")
print("    k_B T ln 2     =", sp.N(kTln2, 6), "eV   (paper: 20 meV)")
print("    photon 500 nm  =", sp.N(Eph, 6), "eV   (paper: 2.4 eV)")
print("    lambda_max = hc/(k_B T ln 2) =", sp.N(hc / kTln2, 5), "um (paper: 60 um)")
print("    thermal photon occupation at 500 nm, 1/(exp(E/kT)-1) ~", sp.N(1 / (sp.exp(Eph / kT) - 1), 3))
tau0 = sp.Rational(1, 10**12)             # s, molecular attempt time (supplied)
year = sp.Rational(31557600)              # s, Julian year
need = sp.log(year / tau0)
print("    ln(1 year / 1 ps) =", sp.N(need, 5), " -> barrier needed =", sp.N(need * kT, 4), "eV")
for label, dE in (("4 meV (paper's water rotational scale)", sp.Rational(4, 1000)),
                  ("0.2 eV (typical hydrogen bond, cited)", sp.Rational(2, 10))):
    print(f"    retention with barrier {label}: tau0*exp(dE/kT) =",
          sp.N(tau0 * sp.exp(dE / kT), 3), "s")
hbar = sp.Rational(6582119569, 10**25)    # eV*s
print("    if m = 4 meV, m x0 = 200 corresponds to", sp.N(200 * hbar / sp.Rational(4, 1000), 3), "s")

print("\nCheck 3: capacity arithmetic in (3)-(5).")
cap_m2 = 4 * sp.Rational(13, 10) * sp.Rational(2, 1000) / sp.Rational(5, 10**7) ** 3
print("    4 n_r d / lambda^3 =", sp.N(cap_m2 / 10**6, 4), "bit/mm^2 (paper: 8e10)")
print("    x 2500 cm^2        =", sp.N(cap_m2 * sp.Rational(1, 4) / 8 / 10**15, 4), "PB (paper: 2.5)")
print("    250e12 synapses x 1 bit =", sp.N(sp.Rational(250 * 10**12, 8 * 10**12), 4), "TB (paper: 30)")
