#!/usr/bin/env python3
"""Replay of every numbered result in 7_paper_rewritten.md.

Each check recomputes one proposition, identity or number of the rewritten
paper from scratch (symbolically with sympy, or numerically with numpy) and
reports PASS or FAIL.  The script exits with status 1 if any check fails.

    python3 7_paper_rewritten_checks.py

Only numpy and sympy are needed.
"""
from __future__ import annotations

import math
import sys

import numpy as np
import sympy as sp

CHECKS = []


def check(label):
    def deco(fn):
        CHECKS.append((label, fn))
        return fn
    return deco


def close(a, b, rel=1e-9, abs_=0.0):
    return abs(a - b) <= abs_ + rel * max(abs(a), abs(b))


# --------------------------------------------------------------------------
# Section 1
# --------------------------------------------------------------------------

@check("Prop 1.2  kinetic term expands to |grad phi|^2 - 2 e A rho grad beta + e^2 A^2 rho; dL/dA = e rho V")
def c_prop12():
    # values of phi = a + i b and of its derivative at one point: an algebraic identity
    a, b, ap, bp, e, m, A = sp.symbols("a b a' b' e m A", real=True)
    phi, dphi = a + sp.I * b, ap + sp.I * bp
    D = dphi - sp.I * e * A * phi
    lhs = sp.expand(D * sp.conjugate(D))
    rho = a**2 + b**2
    rho_dbeta = sp.im(sp.expand(sp.conjugate(phi) * dphi))          # rho * d(beta)/dx = Im(phi* phi')
    rhs = ap**2 + bp**2 - 2 * e * A * rho_dbeta + e**2 * A**2 * rho
    ok1 = sp.expand(lhs - rhs) == 0
    L = -lhs / (2 * m)
    dLdA = sp.expand(sp.diff(L, A) - (e / m) * (rho_dbeta - e * A * rho))   # e rho V, V = (beta' - e A)/m
    return ok1 and dLdA == 0, "identity and dL/dA_i = e rho V_i verified symbolically"


@check("Thm 1.3   div(lap A - grad div A) = 0 identically in three dimensions")
def c_thm13():
    x, y, z = sp.symbols("x y z", real=True)
    A = [sp.Function(f"A{i}")(x, y, z) for i in range(3)]
    X = (x, y, z)
    divA = sum(sp.diff(A[i], X[i]) for i in range(3))
    vec = [sum(sp.diff(A[i], X[j], 2) for j in range(3)) - sp.diff(divA, X[i]) for i in range(3)]
    d = sp.simplify(sum(sp.diff(vec[i], X[i]) for i in range(3)))
    return d == 0, "div of the transverse operator vanishes"


@check("Prop 1.6  slab bound sup|A0| <= delta L^2/8 and ball integral 2 pi a^2")
def c_prop16():
    rng = np.random.default_rng(1)
    L, delta, n = 2.0, 0.7, 801
    xs = np.linspace(-L / 2, L / 2, n)
    h = xs[1] - xs[0]
    # -f'' = q, f(+-L/2) = 0, second-order finite differences
    main = np.full(n - 2, 2.0 / h**2)
    off = np.full(n - 3, -1.0 / h**2)
    M = np.diag(main) + np.diag(off, 1) + np.diag(off, -1)
    worst = 0.0
    for _ in range(20):
        q = delta * np.tanh(3 * rng.standard_normal(n))   # |q| <= delta, arbitrary sign pattern
        f = np.linalg.solve(M, q[1:-1])
        worst = max(worst, np.abs(f).max())
    f_eq = np.linalg.solve(M, np.full(n - 2, delta))
    bound = delta * L**2 / 8
    ok_a = worst <= bound * (1 + 1e-6) and close(f_eq.max(), bound, rel=1e-4)
    # ball: integral of 1/|x-y| over |y|<=a equals 2 pi (a^2 - |x|^2/3) inside, maximal at the centre
    a = 1.0
    r = np.linspace(0, a, 400)[1:]
    th = np.linspace(0, np.pi, 400)
    R, TH = np.meshgrid(r, th, indexing="ij")
    def ball_integral(x0):
        dist = np.sqrt(R**2 + x0**2 - 2 * R * x0 * np.cos(TH))
        integrand = 2 * np.pi * R**2 * np.sin(TH) / dist
        return np.trapezoid(np.trapezoid(integrand, th, axis=1), r)
    I0, I_half = ball_integral(0.0), ball_integral(0.5 * a)
    ok_b = close(I0, 2 * np.pi * a**2, rel=5e-3) and I_half < I0 and close(I_half, 2 * np.pi * (a**2 - 0.25 / 3), rel=5e-3)
    return ok_a and ok_b, f"slab worst {worst:.4f} <= {bound:.4f}; ball centre {I0:.4f} vs {2*np.pi:.4f}"


# --------------------------------------------------------------------------
# Section 2: the reduced model (2.1), with and without loss (2.5)
# --------------------------------------------------------------------------

def rk4(f, y0, t0, t1, dt):
    t, y = t0, np.array(y0, dtype=complex)
    ts, ys = [t], [y.copy()]
    while t < t1 - 1e-15:
        h = min(dt, t1 - t)
        k1 = f(t, y)
        k2 = f(t + h / 2, y + h / 2 * k1)
        k3 = f(t + h / 2, y + h / 2 * k2)
        k4 = f(t + h, y + h * k3)
        y = y + h / 6 * (k1 + 2 * k2 + 2 * k3 + k4)
        t += h
        ts.append(t)
        ys.append(y.copy())
    return np.array(ts), np.array(ys)


def reduced(g, kappa, loss=0.0):
    def f(t, y):
        c0, c1, A = y[0], y[1], y[2].real
        R = 2 * (np.conj(c0) * c1).real
        return np.array([g * A * c1, -g * A * c0, kappa * R - loss * A], dtype=complex)
    return f


def ellipk(k):
    """Complete elliptic integral K(k) by the arithmetic-geometric mean."""
    a, b = 1.0, math.sqrt(1 - k * k)
    while abs(a - b) > 1e-15:
        a, b = (a + b) / 2, math.sqrt(a * b)
    return math.pi / (2 * a)


@check("Prop 2.3  N, Im(chi0* chi1) and (1/2)A^2 + Omega Z/(8 pi L3) are invariant; Z^2+R^2 = N^2-4I^2")
def c_prop23():
    g, Omega, L3 = 0.7, 1.3, 0.4
    kappa = g * Omega / (4 * np.pi * L3)
    rng = np.random.default_rng(2)
    y0 = [complex(*rng.standard_normal(2)), complex(*rng.standard_normal(2)), 0.3]
    ts, ys = rk4(reduced(g, kappa), y0, 0, 40, 1e-3)
    c0, c1, A = ys[:, 0], ys[:, 1], ys[:, 2].real
    N = abs(c0)**2 + abs(c1)**2
    I = (np.conj(c0) * c1).imag
    Z = abs(c1)**2 - abs(c0)**2
    R = 2 * (np.conj(c0) * c1).real
    E = 0.5 * A**2 + Omega / (8 * np.pi * L3) * Z
    drift = max(np.ptp(N) / N[0], np.ptp(I) / max(abs(I[0]), 1e-12), np.ptp(E) / max(abs(E[0]), 1e-12))
    ok = drift < 1e-7 and np.allclose(Z**2 + R**2, N**2 - 4 * I**2, rtol=1e-9)
    return ok, f"max relative drift of the three invariants {drift:.1e}"


@check("Thm 2.4/2.5  lossless: pendulum, period 4K(cos(theta0/2))/omega_c, max A = omega_c cos(theta0/2)/g, A returns to 0")
def c_thm25():
    g, Omega, L3, Np = 1.0, 2.0, 0.5, 3.0
    kappa = g * Omega / (4 * np.pi * L3)
    wc = math.sqrt(2 * g * kappa * Np)
    theta0 = 0.6
    y0 = [math.sqrt(Np) * math.sin(theta0 / 2), math.sqrt(Np) * math.cos(theta0 / 2), 0.0]
    T_pred = 4 / wc * ellipk(math.cos(theta0 / 2))
    ts, ys = rk4(reduced(g, kappa), y0, 0, 2.2 * T_pred, 2e-4)
    A = ys[:, 2].real
    Z = abs(ys[:, 1])**2 - abs(ys[:, 0])**2
    R = 2 * (np.conj(ys[:, 0]) * ys[:, 1]).real
    theta = np.unwrap(np.arctan2(R, Z))
    # pendulum equation along the orbit
    thdd = np.gradient(np.gradient(theta, ts), ts)
    ok_pend = np.abs(thdd[50:-50] - wc**2 * np.sin(theta[50:-50])).max() < 1e-3 * wc**2
    # zeros of A are the turning points, spaced by half a period
    sgn = np.sign(A)
    zeros = ts[1:][(sgn[1:] * sgn[:-1]) < 0]
    half_periods = np.diff(zeros)
    ok_T = len(half_periods) >= 3 and np.allclose(half_periods, T_pred / 2, rtol=2e-3)
    ok_max = close(np.abs(A).max(), wc / g * math.cos(theta0 / 2), rel=1e-4)
    ok_range = close(theta.min(), theta0, rel=1e-3) and close(theta.max(), 2 * math.pi - theta0, rel=1e-3)
    return ok_pend and ok_T and ok_max and ok_range, f"period {half_periods[0]*2:.5f} vs {T_pred:.5f}; max A {np.abs(A).max():.5f} vs {wc/g*math.cos(theta0/2):.5f}"


@check("Thm 2.5(iii)  small seed: each pulse tends to (omega_c/g) sech(omega_c (t - t1)); T ~ (4/omega_c) ln(8/theta0)")
def c_thm25iii():
    g, Omega, L3, Np = 1.0, 2.0, 0.5, 3.0
    kappa = g * Omega / (4 * np.pi * L3)
    wc = math.sqrt(2 * g * kappa * Np)
    theta0 = 1e-3
    y0 = [math.sqrt(Np) * math.sin(theta0 / 2), math.sqrt(Np) * math.cos(theta0 / 2), 0.0]
    T_pred = 4 / wc * ellipk(math.cos(theta0 / 2))
    ts, ys = rk4(reduced(g, kappa), y0, 0, 0.75 * T_pred, 5e-4)
    A = ys[:, 2].real
    i1 = np.argmax(A)
    t1 = ts[i1]
    win = (ts > t1 - 6 / wc) & (ts < t1 + 6 / wc)
    model = wc / g / np.cosh(wc * (ts[win] - t1))
    err = np.abs(A[win] - model).max() / (wc / g)
    T_asym = 4 / wc * math.log(8 / theta0)
    return err < 2e-3 and close(T_pred, T_asym, rel=1e-5), f"sech error {err:.1e}; T {T_pred:.4f} vs asymptotic {T_asym:.4f}"


@check("Thm 2.6   overdamped (L3 << tau_R): single sech pulse, peak g Omega N'/(4 pi), width tau_R, delay tau0, theta -> pi")
def c_thm26():
    g, Omega, Np = 1.0, 1.0, 1.0
    tau_R = 2 * math.pi / (g**2 * Omega * Np)
    L3 = 0.005 * tau_R
    kappa = g * Omega / (4 * math.pi * L3)
    theta0 = 0.2
    tau0 = -tau_R * math.log(math.tan(theta0 / 2))
    y0 = [math.sqrt(Np) * math.sin(theta0 / 2), math.sqrt(Np) * math.cos(theta0 / 2), 0.0]
    ts, ys = rk4(reduced(g, kappa, loss=1 / L3), y0, 0, tau0 + 8 * tau_R, L3 / 20)
    A = ys[:, 2].real
    Z = abs(ys[:, 1])**2 - abs(ys[:, 0])**2
    R = 2 * (np.conj(ys[:, 0]) * ys[:, 1]).real
    theta = np.unwrap(np.arctan2(R, Z))
    peak = A.max(); t_peak = ts[np.argmax(A)]
    half = ts[A >= peak / 2]
    fwhm = half[-1] - half[0]
    fwhm_pred = 2 * math.acosh(2) * tau_R
    ok = (close(peak, g * Omega * Np / (4 * math.pi), rel=2e-2) and close(t_peak, tau0, rel=2e-2)
          and close(fwhm, fwhm_pred, rel=2e-2) and np.all(np.diff(theta)[ts[1:] > 5 * L3] > -1e-9)
          and close(theta[-1], math.pi, rel=1e-3))
    return ok, f"peak {peak:.5f} vs {g*Omega*Np/(4*math.pi):.5f}; delay {t_peak:.3f} vs {tau0:.3f}; FWHM {fwhm:.3f} vs {fwhm_pred:.3f}"


@check("Cor 2.7   theta0 = 0 is a fixed point: nothing is emitted without a seed")
def c_cor27():
    g, kappa = 1.0, 3.0
    y0 = [0.0, 2.0, 0.0]            # all quanta in the upper level, no field
    ts, ys = rk4(reduced(g, kappa, loss=0.3), y0, 0, 50, 1e-2)
    return np.abs(ys[:, 2]).max() == 0.0 and np.abs(ys[:, 0]).max() == 0.0, "A and chi0 stay exactly 0"


@check("Prop 2.8  rho = |chi0|^2 phi0^2 + |chi1|^2 phi1^2 + 2 phi0 phi1 Re(chi0* chi1 e^{-i Omega t})")
def c_prop28():
    t, E0, E1, p0, p1 = sp.symbols("t E0 E1 phi0 phi1", real=True)
    c0, c1 = sp.symbols("chi0 chi1")
    phi = sp.exp(-sp.I * E0 * t) * c0 * p0 + sp.exp(-sp.I * E1 * t) * c1 * p1
    rho = sp.expand(phi * sp.conjugate(phi))
    target = (c0 * sp.conjugate(c0)) * p0**2 + (c1 * sp.conjugate(c1)) * p1**2 \
        + 2 * p0 * p1 * sp.re(sp.conjugate(c0) * c1 * sp.exp(-sp.I * (E1 - E0) * t))
    d = sp.simplify(sp.expand_complex(rho - target))
    return d == 0, "density expansion verified; a frozen density fixes the three coefficients"


# --------------------------------------------------------------------------
# Section 3
# --------------------------------------------------------------------------

@check("Thm 3.2   A = T Atilde solves the screened wave equation up to R = (2i k.grad T - lap T) Atilde")
def c_thm32():
    t, x, y, kx, ky, M2, b = sp.symbols("t x y k_x k_y M2 b", real=True)
    T = sp.Function("T")(x, y)
    k0 = sp.sqrt(kx**2 + ky**2)
    At = b * sp.exp(sp.I * (k0 * t - kx * x - ky * y))
    wp2 = M2 / T - M2                      # omega_p^2 = M^2 (1 - T)/T
    A = T * At
    lhs = sp.diff(A, t, 2) - sp.diff(A, x, 2) - sp.diff(A, y, 2) + (wp2 + M2) * A
    Rres = (2 * sp.I * (kx * sp.diff(T, x) + ky * sp.diff(T, y)) - sp.diff(T, x, 2) - sp.diff(T, y, 2)) * At
    d = sp.simplify(sp.expand(lhs - M2 * At - Rres))
    return d == 0, "residual identity (3.3) verified"


@check("Thm 3.4   -sigma |r+o|^2 r = -sigma[(|r|^2+|o|^2) r + |r|^2 o + r^2 o*];  s = 0.09/2 = 0.045")
def c_thm34():
    r, o, sig = sp.symbols("r o sigma")
    lhs = -sig * (r + o) * sp.conjugate(r + o) * r
    rhs = -sig * ((r * sp.conjugate(r) + o * sp.conjugate(o)) * r + r * sp.conjugate(r) * o + r**2 * sp.conjugate(o))
    ok1 = sp.expand(lhs - rhs) == 0
    s = 0.3**2 * 1.0 / (1.0 * 2.0)
    return ok1 and close(s, 0.045), f"identity verified; s = {s:.3f}"


@check("Prop 3.8  cells: C2 = 4.0e12, n_r d/lambda = 5200, C3 = 2.08e16 (2.6 PB); 1500 nm -> 0.096 PB; 310 um -> 8.7e7 bits (11 MB)")
def c_prop38():
    S, d, nr, lam = 0.25, 2e-3, 1.3, 500e-9
    C2 = 4 * S / lam**2
    ratio = nr * d / lam
    C3 = 4 * nr * S * d / lam**3
    C3_1500 = 4 * nr * S * d / (1500e-9)**3
    lam4meV = 1239.84e-9 / 0.004
    C3_4meV = 4 * nr * S * d / lam4meV**3
    syn = 250e12
    ok = (close(C2, 4.0e12, rel=1e-6) and close(ratio, 5200, rel=1e-6) and close(C3, 2.08e16, rel=1e-6)
          and close(C3 / 8 / 1e15, 2.6, rel=1e-6) and close(C3_1500 / 8 / 1e15, 0.0963, rel=1e-2)
          and close(lam4meV, 310e-6, rel=1e-3) and close(C3_4meV, 8.7e7, rel=2e-2) and close(C3_4meV / 8 / 1e6, 10.9, rel=2e-2)
          and close(syn / 8 / 1e12, 31.25) and close(syn * 4.7 / 8 / 1e12, 146.9, rel=1e-3))
    return ok, f"C2 {C2:.2e}, ratio {ratio:.0f}, C3 {C3:.3e} = {C3/8/1e15:.2f} PB; 310 um: {C3_4meV:.2e} bits = {C3_4meV/8/1e6:.1f} MB"


@check("Prop 3.10 k_B T = 26.71 meV, k_B T ln2 = 18.52 meV; barriers 0.74/0.96/1.20 eV; hc/(k_B T ln2) = 67 um (62 um at 20 meV)")
def c_prop310():
    kB = 8.617333262e-5
    kT = kB * 310
    land = kT * math.log(2)
    tau_a = 1e-12
    bar = [kT * math.log(tr / tau_a) for tr in (1.0, 3600.0, 365.25 * 86400)]
    lam = 1239.84e-9 / land
    lam20 = 1239.84e-9 / 0.020
    ok = (close(kT * 1e3, 26.71, rel=1e-3) and close(land * 1e3, 18.52, rel=1e-3)
          and close(bar[0], 0.738, rel=2e-3) and close(bar[1], 0.957, rel=2e-3) and close(bar[2], 1.199, rel=2e-3)
          and close(lam, 67e-6, rel=1e-2) and close(lam20, 62e-6, rel=1e-2) and close(1239.84 / 500, 2.48, rel=1e-3))
    return ok, f"kT {kT*1e3:.2f} meV, kT ln2 {land*1e3:.2f} meV, barriers {bar[0]:.3f} {bar[1]:.3f} {bar[2]:.3f} eV, {lam*1e6:.1f} um"


# --------------------------------------------------------------------------
# Section 4
# --------------------------------------------------------------------------

@check("Thm 4.1   polar form of (M) gives continuity and (B) with + (m/2) V^2; printed (A70) fails for a free plane wave")
def c_thm41():
    t, x = sp.symbols("t x", real=True)
    e, m = sp.symbols("e m", positive=True)
    rho = sp.Function("rho")(t, x)
    beta = sp.Function("beta")(t, x)
    A = sp.Function("A")(t, x)
    A0 = sp.Function("A0")(t, x)
    U = sp.Function("U")(x)
    phi = sp.sqrt(rho) * sp.exp(sp.I * beta)
    D = lambda f: sp.diff(f, x) - sp.I * e * A * f
    eqM = (sp.I * sp.diff(phi, t) + e * A0 * phi) - (-D(D(phi)) / (2 * m) + U * phi)
    expr = sp.expand(eqM * sp.exp(-sp.I * beta))
    # evaluate at a point: every function value and derivative becomes a real symbol
    rt, rx, rxx, be, bt, bx, bxx, Av, Ax, A0v, Uv = sp.symbols("r_t r_x r_xx be b_t b_x b_xx A A_x A0 U", real=True)
    r = sp.symbols("r", positive=True)
    rep = {sp.Derivative(rho, t): rt, sp.Derivative(rho, x): rx, sp.Derivative(rho, (x, 2)): rxx,
           sp.Derivative(beta, t): bt, sp.Derivative(beta, x): bx, sp.Derivative(beta, (x, 2)): bxx,
           sp.Derivative(A, x): Ax}
    expr = expr.subs(rep).subs({rho: r, beta: be, A: Av, A0: A0v, U: Uv})
    expr = sp.expand(expr)
    re_, im_ = sp.re(expr), sp.im(expr)
    V = (bx - e * Av) / m
    rho_V_x = rx * V + r * (bxx - e * Ax) / m                       # d/dx (rho V)
    cont = sp.simplify(2 * sp.sqrt(r) * im_ - rt - rho_V_x)      # 2 sqrt(rho) Im(...) = d rho/dt + d(rho V)/dx
    lap_sqrt = (rxx / (2 * sp.sqrt(r)) - rx**2 / (4 * r ** sp.Rational(3, 2)))   # (sqrt rho)''
    bern = sp.simplify(re_ / sp.sqrt(r) - ((e * A0v - bt) + lap_sqrt / (2 * m * sp.sqrt(r)) - m * V**2 / 2 - Uv))
    ok1 = cont == 0 and bern == 0
    # free plane wave: rho const, beta = k x - k^2 t/(2m), A = A0 = U = 0
    k = sp.symbols("k", real=True)
    beta_pw = k * x - k**2 * t / (2 * m)
    corrected = sp.simplify((0 - sp.diff(beta_pw, t)) - (m / 2) * (sp.diff(beta_pw, x) / m)**2)
    printed = sp.simplify((0 - sp.diff(beta_pw, t)) + (m / 2) * (sp.diff(beta_pw, x) / m)**2)
    return ok1 and corrected == 0 and printed != 0, "(C) and (B) verified; printed sign gives d beta/dt = +k^2/2m for a free wave"


@check("Thm 4.5   d/dt (div E + e rho) = -(M^2 + gamma d/dt) div A + v div(A_prev + A_next) for the layer system")
def c_thm45():
    t, x, y = sp.symbols("t x y", real=True)
    e, m, M2, gam, v = sp.symbols("e m M2 gamma v", positive=True)
    A1, A2, A0, rho = [sp.Function(n, real=True)(t, x, y) for n in ("A1", "A2", "A0", "rho")]
    P1, P2, Q1, Q2 = [sp.Function(n, real=True)(t, x, y) for n in ("P1", "P2", "Q1", "Q2")]   # neighbouring layers
    E1 = sp.diff(A1, t) - sp.diff(A0, x)
    E2 = sp.diff(A2, t) - sp.diff(A0, y)
    dE1 = sp.diff(A1, y, 2) - sp.diff(sp.diff(A2, x), y) - e**2 * rho / m * A1 - M2 * A1 - gam * sp.diff(A1, t) + v * (P1 + Q1)
    dE2 = sp.diff(A2, x, 2) - sp.diff(sp.diff(A1, x), y) - e**2 * rho / m * A2 - M2 * A2 - gam * sp.diff(A2, t) + v * (P2 + Q2)
    drho = e / m * (sp.diff(rho * A1, x) + sp.diff(rho * A2, y))
    dG = sp.diff(dE1, x) + sp.diff(dE2, y) + e * drho
    divA = sp.diff(A1, x) + sp.diff(A2, y)
    rhs = -M2 * divA - gam * sp.diff(divA, t) + v * (sp.diff(P1 + Q1, x) + sp.diff(P2 + Q2, y))
    return sp.simplify(sp.expand(dG - rhs)) == 0, "Gauss-law drift identity (4.3) verified"


def cheb_U(J, c):
    u_prev, u = 0.0, 1.0
    for _ in range(J):
        u_prev, u = u, 2 * c * u - u_prev
    return u


@check("Thm 4.6/Cor 4.7  U_4(1.25) = 21.3125 -> input 2.13 (source: 3.9); with omega_p^2 kept, U_4(1.30625) = 27.1 -> 2.71; forward solve recovers the target")
def c_thm46():
    M2, v, N, amp, wp2 = 2.0, 0.8, 4, 0.1, 0.09
    c = M2 / (2 * v)
    U4 = cheb_U(4, c)
    eta = math.acosh(c)
    U4_closed = math.sinh(5 * eta) / math.sinh(eta)
    src = amp * (M2 ** 4) / (v ** 4)
    c2 = (M2 + wp2) / (2 * v)
    U4b = cheb_U(4, c2)
    # forward problem: M^2 u_n - v (u_{n-1} + u_{n+1}) = 0, n = 1..N, u_0 given, u_{N+1} = 0
    u0 = amp * U4
    Mat = np.zeros((N, N)); rhs = np.zeros(N)
    for n in range(N):
        Mat[n, n] = M2
        if n > 0: Mat[n, n - 1] = -v
        if n < N - 1: Mat[n, n + 1] = -v
    rhs[0] = v * u0
    u = np.linalg.solve(Mat, rhs)
    ok = (close(U4, 21.3125) and close(U4_closed, 21.3125, rel=1e-12) and close(amp * U4, 2.13125)
          and close(src, 3.90625) and close(U4b, 27.1075, rel=1e-4) and close(u[-1], amp, rel=1e-12))
    return ok, f"U4 {U4:.4f}, input {amp*U4:.5f}; source {src:.5f}; with omega_p^2 {U4b:.4f} -> {amp*U4b:.3f}; forward u_N = {u[-1]:.6f}"


def lattice_targets(Ns=64, N1=30, N2=20, amp=0.1):
    n = np.arange(-Ns, Ns)
    def tri(n, Nc):
        out = np.empty_like(n, dtype=float)
        left = n <= -Nc; right = n >= Nc; mid = ~(left | right)
        out[left] = (n[left] + Ns) / (Ns - Nc)
        out[mid] = -n[mid] / Nc
        out[right] = (n[right] - Ns) / (Ns - Nc)
        return amp * out
    A1 = np.tile(tri(n, N1)[:, None], (1, 2 * Ns))
    A2 = np.tile(tri(n, N2)[None, :], (2 * Ns, 1))
    return A1, A2


@check("Thm 4.6 (lattice)  for the separable targets the derivative terms of (4.4) vanish on the 128x128 periodic lattice")
def c_thm46_lattice():
    A1, A2 = lattice_targets()
    d2_A1 = np.roll(A1, -1, 1) - 2 * A1 + np.roll(A1, 1, 1)                 # d2^2 A1
    B = np.roll(A2, -1, 1) - np.roll(A2, 1, 1)                               # 2 d2 A2
    d12_A2 = (np.roll(B, -1, 0) - np.roll(B, 1, 0)) / 4                        # d1 d2 A2
    ok = np.abs(d2_A1).max() == 0.0 and np.abs(d12_A2).max() == 0.0
    return ok, "both derivative terms are exactly zero; the recursion is purely algebraic"


@check("Thm 4.8   div A_tgt at the centre = -0.1(1/30+1/20); delta_centre = -0.25(1-e^{-0.01 t}); table within 1 point of Figure 6")
def c_thm48():
    A1, A2 = lattice_targets()
    div = (np.roll(A1, -1, 0) - np.roll(A1, 1, 0)) / 2 + (np.roll(A2, -1, 1) - np.roll(A2, 1, 1)) / 2   # a_s = 1/m
    centre = div[64, 64]
    e, g2 = 0.3, 0.01
    coeff = e * centre / g2
    times = np.array([5, 20, 40, 100, 200])
    delta = coeff * (1 - np.exp(-g2 * times)) * 100
    source = np.array([-1.3, -4.5, -9.1, -16, -21])
    ok = (close(centre, -0.1 * (1 / 30 + 1 / 20), rel=1e-12) and close(coeff, -0.25, rel=1e-12)
          and np.allclose(delta, [-1.22, -4.53, -8.24, -15.80, -21.62], atol=0.01)
          and np.abs(delta - source).max() <= 1.0)
    return ok, "delta % = " + ", ".join(f"{d:.1f}" for d in delta) + f"; max gap to Figure 6 {np.abs(delta-source).max():.2f} points"


@check("Thm 4.10  sum of div A_tgt over the periodic box is 0; corner rise +0.156(1-e^{-0.01 t}) = +13.5% at t = 200")
def c_thm410():
    A1, A2 = lattice_targets()
    div = (np.roll(A1, -1, 0) - np.roll(A1, 1, 0)) / 2 + (np.roll(A2, -1, 1) - np.roll(A2, 1, 1)) / 2
    corner = div[0, 0]      # n1 = n2 = -64: inside both outer pieces
    e, g2 = 0.3, 0.01
    coeff = e * corner / g2
    rise200 = coeff * (1 - math.exp(-2.0)) * 100
    ok = (abs(div.sum()) < 1e-12 and close(corner, 0.1 * (1 / 34 + 1 / 44), rel=1e-12)
          and close(coeff, 0.15642, rel=1e-3) and close(rise200, 13.5, rel=5e-3))
    return ok, f"sum {div.sum():.1e}; corner coefficient {coeff:.4f}; rise at 200: {rise200:.1f}%"


# --------------------------------------------------------------------------
# Appendices
# --------------------------------------------------------------------------

@check("App. A/C  lattice cell 1/m: 49 um at m = 4 meV, 1.2e-17 m at the water-molecule mass; T(0.1) = 4.38 (4/omega_c)")
def c_appendix():
    hbarc = 197.3269804e-9   # eV m
    a_4meV = hbarc / 0.004
    a_water = hbarc / (18 * 931.494e6)
    T01 = ellipk(math.cos(0.05))
    ok = close(a_4meV, 49.3e-6, rel=2e-3) and close(a_water, 1.18e-17, rel=1e-2) and close(T01, 4.38, rel=3e-3)
    return ok, f"{a_4meV*1e6:.1f} um; {a_water:.2e} m; K(cos 0.05) = {T01:.4f}"


def main():
    width = max(len(l) for l, _ in CHECKS)
    failed = 0
    for label, fn in CHECKS:
        try:
            ok, detail = fn()
        except Exception as exc:        # a crash is a failure, not a skip
            ok, detail = False, f"error: {exc!r}"
        failed += (not ok)
        print(f"{'PASS' if ok else 'FAIL'}  {label}\n      {detail}")
    print(f"\n{len(CHECKS) - failed} of {len(CHECKS)} checks pass")
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
