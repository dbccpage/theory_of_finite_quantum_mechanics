"""Retest checks for 04_self_audit/retest_log.md (threads_simulation_and_consciousness).

Provenance: written 2026-11-05 for the retest round after the first reviewer's reply to
adversarial_review.md. Equation numbers refer to 02_paper/ijms-25-02399.md.

Run: python code/retest_checks.py [t_end]     (needs numpy and sympy; default t_end=40)

R1  Rerun the Section 4 / Appendix C simulation, (A82)-(A87) with (A88)-(A90),
    at the paper's parameters. Check the density dips against the paper
    (1.3% at m x0 = 5, 4.5% at 20, 9.1% at 40), then measure the Gauss-law
    residual  G = div E - J^0 - e  (J^0 = -e|phi|^2, background +e).
    Floating point, numerical: a reproduction, not an exact check.
R2  The super-radiance transition current in Appendix A: is it divergence-free?
    (symbolic, harmonic-oscillator eigenstates as the example).
R3  Equal reports do not give equal likelihoods for hypotheses that are
    distributions over states (exact counterexample).
R4  The resolution limit keeps its condition: a finite observer with |P| >= |X|
    can separate every state (exact).
"""

import sys
from fractions import Fraction

import numpy as np
import sympy as sp

# ---------------------------------------------------------------- R1
def rerun(t_end=40.0, input_max=None):
    L, Ns = 128, 64
    e, m, v, gam, M2, gam2 = 0.3, 1.0, 0.8, 0.2, 2.0, 0.01
    dt, N = 0.001, 4
    n = np.arange(-Ns, Ns)                       # 128 sites, periodic
    n1, n2 = np.meshgrid(n, n, indexing="ij")    # axis 0 = x^1, axis 1 = x^2
    N1, N2 = 30, 20

    def tri(k, Nk):                              # targets (10)-(11)
        k = k.astype(float)
        return np.where(k <= -Nk, 0.1 * (k + Ns) / (Ns - Nk),
               np.where(k >= Nk, 0.1 * (k - Ns) / (Ns - Nk), -0.1 * k / Nk))

    d1 = lambda f: (np.roll(f, -1, -2) - np.roll(f, 1, -2)) / 2
    d2 = lambda f: (np.roll(f, -1, -1) - np.roll(f, 1, -1)) / 2
    d11 = lambda f: np.roll(f, -1, -2) - 2 * f + np.roll(f, 1, -2)
    d22 = lambda f: np.roll(f, -1, -1) - 2 * f + np.roll(f, 1, -1)

    # Inputs by the static inverse (A88)-(A89), written consistently with (A82):
    # u^(n-1) = (-d22 u1 + d1 d2 u2 + M^2 u1)/v - u^(n+1).  For these targets the
    # derivative terms vanish (the paper says so), so this is a scalar recursion.
    u1 = {N: tri(n1, N1), N + 1: 0 * n1.astype(float)}
    u2 = {N: tri(n2, N2), N + 1: 0 * n2.astype(float)}
    for J in range(1, N + 1):
        k = N - J
        u1[k] = (-d22(u1[k + 1]) + d1(d2(u2[k + 1])) + M2 * u1[k + 1]) / v - u1[k + 2]
        u2[k] = (-d11(u2[k + 1]) + d1(d2(u1[k + 1])) + M2 * u2[k + 1]) / v - u2[k + 2]
    U1, U2 = u1[0], u2[0]
    if input_max is not None:                    # bracket: rescale to the paper's stated amplitude
        s = input_max / np.abs(U1).max()
        U1, U2 = U1 * s, U2 * s

    shape = (N, L, L)                            # layers 1..N
    A1, A2, E1, E2 = (np.zeros(shape) for _ in range(4))
    rho = np.ones(shape)

    def A0_of(A1, A2, rho):                      # (A87)
        s = np.sqrt(rho)
        return -(d11(s) + d22(s)) / (2 * m * e * s) + e * (A1**2 + A2**2) / (2 * m)

    def neighbours(A, U, t):                     # A^(n-1) + A^(n+1)
        inp = U * np.exp(-gam2 * t)
        below = np.concatenate([inp[None], A[:-1]], 0)
        above = np.concatenate([A[1:], np.zeros_like(A[:1])], 0)
        return below + above

    def rhs(t, A1, A2, E1, E2, rho):
        A0 = A0_of(A1, A2, rho)
        dE1 = d22(A1) - d1(d2(A2)) - e**2 * rho / m * A1 - M2 * A1 - gam * (E1 + d1(A0)) + v * neighbours(A1, U1, t)
        dE2 = d11(A2) - d1(d2(A1)) - e**2 * rho / m * A2 - M2 * A2 - gam * (E2 + d2(A0)) + v * neighbours(A2, U2, t)
        dA1 = E1 + d1(A0)
        dA2 = E2 + d2(A0)
        drho = (e / m) * (d1(rho * A1) + d2(rho * A2))
        return dA1, dA2, dE1, dE2, drho

    box = (np.abs(n1) < N1) & (np.abs(n2) < N2)
    marks = {5.0: None, 20.0: None, 40.0: None, t_end: None}
    t, steps = 0.0, int(round(t_end / dt))
    y = [A1, A2, E1, E2, rho]
    out = []
    for i in range(1, steps + 1):
        k1 = rhs(t, *y)
        k2 = rhs(t + dt / 2, *[a + dt / 2 * b for a, b in zip(y, k1)])
        k3 = rhs(t + dt / 2, *[a + dt / 2 * b for a, b in zip(y, k2)])
        k4 = rhs(t + dt, *[a + dt * b for a, b in zip(y, k3)])
        y = [a + dt / 6 * (b + 2 * c + 2 * d + f) for a, b, c, d, f in zip(y, k1, k2, k3, k4)]
        t = i * dt
        tt = round(t, 6)
        if tt in marks:
            A1, A2, E1, E2, rho = y
            top = rho[-1]
            dip = 1 - top[box].mean()
            # Gauss residual on the output layer, with the paper's own E from (A83)
            gauss = d1(E1[-1]) + d2(E2[-1]) + e * top - e
            charge = e * (top - 1)
            # Budget: instantaneous contributions to d/dt(div E - J^0) on the output layer.
            # In the continuum only the M^2, gamma and v terms survive; the discrete
            # curl-curl and current terms measure the stencil's own error.
            a1, a2, f1, f2, r = A1[-1], A2[-1], E1[-1], E2[-1], top
            A0 = A0_of(A1, A2, rho)[-1]
            B1 = neighbours(A1, U1, t)[-1]; B2 = neighbours(A2, U2, t)[-1]
            rms = lambda f: float(np.sqrt((f**2).mean()))
            curl = d1(d22(a1) - d1(d2(a2))) + d2(d11(a2) - d1(d2(a1)))
            current = -d1(e**2 * r / m * a1) - d2(e**2 * r / m * a2) - (-e) * (e / m) * (d1(r * a1) + d2(r * a2))
            budget = {"stencil curl": rms(curl), "stencil current": rms(current),
                      "M^2": rms(-M2 * (d1(a1) + d2(a2))),
                      "gamma": rms(-gam * (d1(f1 + d1(A0)) + d2(f2 + d2(A0)))),
                      "v": rms(v * (d1(B1) + d2(B2)))}
            out.append((tt, dip, np.abs(gauss).max(), np.abs(charge).max(),
                        np.sqrt((gauss**2).mean()) / max(np.sqrt((charge**2).mean()), 1e-300),
                        abs(top.mean() - 1), budget))
    return out, U1.max()


# ---------------------------------------------------------------- R2
def transition_current_divergence():
    x, mw = sp.symbols("x m_omega", positive=True)
    psi0 = sp.exp(-mw * x**2 / 2)
    psi1 = x * sp.exp(-mw * x**2 / 2)
    j = psi0 * sp.diff(psi1, x) - psi1 * sp.diff(psi0, x)   # the (A11)/(A27) transition current, up to constants
    return sp.simplify(sp.diff(j, x)), sp.simplify(sp.diff(j, x) / (psi0 * psi1))


# ---------------------------------------------------------------- R3
def bayes_counterexample():
    q = {"a": 0, "b": 0, "c": 1}                  # a and b give the same report
    H1 = {"a": Fraction(1, 2), "b": Fraction(1, 2)}
    H2 = {"a": Fraction(1, 2), "c": Fraction(1, 2)}
    lik = lambda H, D: sum(p for s, p in H.items() if q[s] == D)
    D = 0
    return q["a"] == q["b"], lik(H1, D), lik(H2, D), lik(H1, D) / lik(H2, D)


# ---------------------------------------------------------------- R4
def small_domain():
    X = ["s1", "s2", "s3"]
    q = {"s1": 0, "s2": 1, "s3": 2}               # |P| = |X| = 3
    return all(q[x] != q[y] for x in X for y in X if x != y)


if __name__ == "__main__":
    t_end = float(sys.argv[1]) if len(sys.argv) > 1 else 40.0
    input_max = float(sys.argv[2]) if len(sys.argv) > 2 else None
    print("R2: d/dx of transition current =", transition_current_divergence()[0])
    print("    ratio to psi0*psi1 =", transition_current_divergence()[1], "(nonzero constant -> density must oscillate)")
    same, l1, l2, bf = bayes_counterexample()
    print(f"R3: q(a)=q(b): {same};  P(D=0|H1)={l1}, P(D=0|H2)={l2}, Bayes factor={bf}")
    print("R4: |P|=|X|=3 observer separates every state:", small_domain())
    print(f"R1: rerunning Appendix C to m x0 = {t_end} ...")
    rows, umax = rerun(t_end, input_max)
    print(f"    input max u^(0) = {umax:.3f} from (A88)-(A89); used: {input_max or umax:.3f} (paper: 'approximately 3')")
    print("    m x0 | density dip in box | paper | max|Gauss residual| | max|e*drho| | rms ratio | total-charge drift")
    paper = {5.0: "1.3%", 20.0: "4.5%", 40.0: "9.1%"}
    for tt, dip, g, c, ratio, drift, budget in rows:
        print(f"    {tt:5.1f} | {100*dip:6.2f}% | {paper.get(tt,'-'):>5} | {g:.3e} | {c:.3e} | {ratio:.3g} | {drift:.1e}")
        print("           rate budget (rms): " + ", ".join(f"{k} {v:.2e}" for k, v in budget.items()))
