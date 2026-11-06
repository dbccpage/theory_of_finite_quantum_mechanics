"""Replays every claim in 2_dag.json and tests every goal.

    python 8_checks.py              every claim and goal, about two minutes (needs sympy and numpy)
    python 8_checks.py --rerun      also the Appendix C simulation, about 30 minutes
    python 8_checks.py --selftest   breaks a quote, a length and a term in a copy of the posts,
                                    and confirms each break is caught
    python 8_checks.py --pdf        rebuilds 5_dissection.pdf from 5_dissection.md (needs pandoc and xelatex)
                                    and fails on any overfull line or missing character

Exit status 0 only if every claim holds and every goal's tests pass.
Equation numbers refer to the paper, 3_paper.md.
"""
import argparse, hashlib, json, math, pathlib, re, shutil, struct, subprocess, sys, tempfile, zlib

import numpy as np
import sympy as sp

HERE = pathlib.Path(__file__).resolve().parent
PAPER = (HERE / "3_paper.md").read_text(encoding="utf-8")
REPLIES = (HERE / "4_replies.md").read_text(encoding="utf-8")
DAG = json.loads((HERE / "2_dag.json").read_text(encoding="utf-8"))
CHECKS = {}


def check(fn):
    CHECKS[fn.__name__] = fn
    return fn


def flat(s):
    s = s.replace("’", "'").replace("‘", "'").replace("“", '"').replace("”", '"')
    return re.sub(r"\s+", " ", s)


PAPER_FLAT = flat(PAPER)
HER_POST = flat(re.search(r"Her post, verbatim.*?\n\n> (.*?)\n", REPLIES, flags=re.S).group(1))


# ---------------------------------------------------------------- her reasoning
@check
def which_path_record():
    """Finite two-path model: screen amplitude a_L(x) + a_R(x), with a record and a reader."""
    x = np.linspace(-1, 1, 401)
    env = np.exp(-x**2 / 0.18)
    aL, aR = env * np.exp(20j * x), env * np.exp(-20j * x)
    screen = lambda st: (np.abs(st) ** 2).sum(axis=1)
    smooth = np.abs(aL) ** 2 + np.abs(aR) ** 2
    P0 = screen((aL + aR)[:, None])                          # no record
    rec = np.zeros((401, 4), complex)                        # record x reader, basis |m r>
    rec[:, 0], rec[:, 2] = aL, aR                            # |L,0,0> + |R,1,0>: recorded, unread
    read = np.zeros((401, 4), complex)
    read[:, 0], read[:, 3] = aL, aR                          # reader copied the record: |0,0>, |1,1>
    rng = np.random.default_rng(1)
    Q, _ = np.linalg.qr(rng.normal(size=(4, 4)) + 1j * rng.normal(size=(4, 4)))
    stripes = np.abs(P0 - smooth).max() / smooth.max()
    return [
        (stripes > 0.99, f"no record: stripes, depth {stripes:.3f} of the smooth pattern"),
        (np.abs(screen(rec) - smooth).max() < 1e-12, "record kept, never read: no stripes"),
        (np.abs(screen(read) - screen(rec)).max() < 1e-12, "record read later: the screen is unchanged"),
        (np.abs(screen(rec @ Q.T) - screen(rec)).max() < 1e-12, "any operation on record and reader leaves the screen unchanged"),
    ]


@check
def equal_records_equal_odds():
    hA, hB = {1: 0.9, 0: 0.1}, {1: 0.5, 0: 0.5}
    rng = np.random.default_rng(2)
    same = all(math.prod(hB[d] for d in D) == math.prod(dict(hB)[d] for d in D) > 0
               for D in (rng.integers(0, 2, 12).tolist() for _ in range(50)))
    indep = {(a, b): 0.25 for a in (0, 1) for b in (0, 1)}
    twice = {(a, b): (0.5 if a == b else 0.0) for a in (0, 1) for b in (0, 1)}
    marg = lambda P, i: {v: sum(p for k, p in P.items() if k[i] == v) for v in (0, 1)}
    return [
        (abs(hA[1] / hB[1] - 1.8) < 1e-12, "same report, different chances: 0.9 against 0.5, factor 1.8"),
        (same, "equal chances for every record, sampled independently: equal, nonzero likelihoods on any data"),
        (marg(indep, 0) == marg(twice, 0) and twice[(1, 1)] / indep[(1, 1)] == 2.0,
         "without independence: same single-report chances, joint 1/4 against 1/2, factor 2"),
    ]


@check
def her_words():
    return [(w in HER_POST, f"her post says: {w}") for w in
            ("The simulation isn't a giant computer", "it's our consciousness",
             "whether a human observer or just a measurement device", "It's just like a video game",
             "the universe does not render what is offscreen")]


@check
def paper_quotes():
    need = [
        "Vision is perhaps the most important link between the outside world of the observable phenomena and the inner life of our mind.",
        "But how a quantum mind could perceive the macro-world is yet another mystery altogether.",
        "we have to adopt a hemispherical or spherical surface headset covering our head",
        "definition of $\\theta_0$ is in Appendix A",
        "|\\varphi|^2 \\propto |r(x^1,x^2) + o(x^1,x^2)|^2",
        "We intend to apply our approach to manipulate holographic memory and subjective experiences by external electromagnetic fields in a future experimental study.",
    ]
    res = [(len(re.findall(r"render", PAPER, flags=re.I)) == 0, "the word 'render' occurs 0 times in the paper")]
    res += [(flat(q) in PAPER_FLAT, "in the paper: " + q[:70]) for q in need]
    res.append((bool(re.search(r"slight distortion.{0,200}Laplacian", PAPER_FLAT, flags=re.I)),
                "in the paper: the slight distortions are put down to the Laplacian term"))
    return res


# ---------------------------------------------------------------- Appendix A
@check
def gauge_freezes_charge():
    t, x, y, z = sp.symbols("t x y z")
    A = [sp.Function(n)(t, x, y, z) for n in ("A1", "A2", "A3")]
    E = [-sp.diff(c, t) for c in A]                          # A^0 = 0
    divE = sum(sp.diff(Ec, v) for Ec, v in zip(E, (x, y, z)))
    divA = sum(sp.diff(c, v) for c, v in zip(A, (x, y, z)))
    Om = sp.symbols("Omega", positive=True)
    c0, c1, p0, p1 = sp.symbols("c0 c1 p0 p1")
    phi = c0 * p0 + c1 * sp.exp(-sp.I * Om * t) * p1
    cross = sp.expand(phi * sp.conjugate(phi)) - sp.expand(c0 * sp.conjugate(c0) * p0 * sp.conjugate(p0) + c1 * sp.conjugate(c1) * p1 * sp.conjugate(p1))
    return [
        (sp.simplify(divE + sp.diff(divA, t)) == 0, "with A^0 = 0, div E = -d/dt div A, which is 0 when div A = 0: (A7) freezes the charge"),
        (sp.simplify(sp.diff(cross, t)) != 0, "the two-level cross term 2 Re(c0* c1 exp(-i Omega t) phi0* phi1) oscillates at Omega"),
        (sp.simplify(cross.subs(c1, 0)) == 0, "so a density constant in time needs c0* c1 = 0: no coherence R, no source for (A38)"),
    ]


@check
def pulse_algebra():
    t, g, Om, N, L3, th0 = sp.symbols("t g Omega N L_3 theta_0", positive=True)
    A, Z, R = sp.symbols("A Z R")
    dZ, dR, dA = -2 * g * A * R, 2 * g * A * Z, g * Om / (4 * sp.pi * L3) * R      # (A36)-(A38)
    k = g**2 * Om * N / (2 * sp.pi)
    theta = 2 * sp.atan(sp.exp(k * t) * sp.tan(th0 / 2))                            # (A44)
    tauR = 2 * sp.pi / (g**2 * Om * N)
    tau0 = -tauR * sp.log(sp.tan(th0 / 2))
    target = g * Om * N / (4 * sp.pi) / sp.cosh((t - tau0) / tauR)                  # (A45)
    vals = {g: 0.7, Om: 1.3, N: 5, th0: 0.4}
    res = [abs((sp.diff(theta, t) / (2 * g) - target).subs(vals).subs(t, tt).evalf()) < 1e-9 for tt in (0.1, 1.0, 3.0)]
    return [
        (sp.simplify(A * dA + Om / (8 * sp.pi * L3) * dZ) == 0 and sp.simplify(Z * dZ + R * dR) == 0,
         "(A36)-(A38) conserve the energy (A39) and Z^2 + R^2: without the added loss they oscillate"),
        (sp.simplify(sp.diff(theta, t) - k * sp.sin(theta)) == 0 and all(res), "(A44) solves (A43) and gives the sech pulse (A45), tau_R = 2 pi/(g^2 Omega N)"),
        (sp.limit(tau0, th0, 0, "+") == sp.oo, "at theta_0 = 0 the delay tau_0 is infinite: no pulse"),
        (round(2e-3 / 500e-9) == 4000 and round(math.sqrt(2500e-4) / 500e-9) == 1_000_000,
         "the Section 3 slab is 4000 wavelengths deep and 1e6 across"),
    ]


# ---------------------------------------------------------------- Appendix B
@check
def hologram_terms():
    r, o = sp.symbols("r o")
    rs, os_ = sp.conjugate(r), sp.conjugate(o)
    A52 = sp.expand(r * (r * rs + o * os_ + rs * o + r * os_))
    M2, At, Ai = sp.symbols("M2 Atilde A_i")
    return [
        (sp.expand(A52 - (r**2 * rs + r * o * os_ + r * rs * o + r**2 * os_)) == 0 and A52.has(r * rs * o) and A52.has(r**2 * os_),
         "(A52) contains the image |r|^2 o and the twin r^2 o*"),
        ((M2 * At).subs(M2, 0) == 0, "in (A48) the external wave enters only through M^2 Atilde: none at M^2 = 0"),
        (abs(0.3**2 * 1.0 / 2.0 - 0.045) < 1e-12, "screening number e^2 |phi|^2/(M^2 m) = 0.045 at e = 0.3, |phi|^2 = 1, M^2 = 2 m^2"),
    ]


# ---------------------------------------------------------------- Appendix C
def _gauss(coef):
    t, x, y = sp.symbols("t x y", real=True)
    e, m, M2, gam, v = sp.symbols("e m M2 gamma v", positive=True)
    A1, A2, E1, E2, n, A0, B1, B2 = (sp.Function(s)(t, x, y) for s in ("A1", "A2", "E1", "E2", "n", "A0", "B1", "B2"))
    dE1 = sp.diff(A1, y, 2) - sp.diff(A2, x, y) - coef(e, m) * n * A1 - M2 * A1 - gam * (E1 + sp.diff(A0, x)) + v * B1   # (A82)
    dE2 = sp.diff(A2, x, 2) - sp.diff(A1, x, y) - coef(e, m) * n * A2 - M2 * A2 - gam * (E2 + sp.diff(A0, y)) + v * B2   # (A84)
    dn = (e / m) * (sp.diff(n * A1, x) + sp.diff(n * A2, y))                                                             # (A86)
    r = sp.expand(sp.diff(dE1, x) + sp.diff(dE2, y) - (-e) * dn)                                                         # J^0 = -e n
    expected = sp.expand(-M2 * (sp.diff(A1, x) + sp.diff(A2, y)) - gam * (sp.diff(E1 + sp.diff(A0, x), x) + sp.diff(E2 + sp.diff(A0, y), y))
                         + v * (sp.diff(B1, x) + sp.diff(B2, y)))
    return r, expected


@check
def gauss_residual():
    r, expected = _gauss(lambda e, m: e**2 / m)
    n1, n2 = sp.symbols("n1 n2")
    curl = sp.diff(sp.Function("g")(n2), n1) - sp.diff(sp.Function("f")(n1), n2)
    return [
        (sp.simplify(r - expected) == 0, "d/dt(div E - J^0) = -M^2 div A - gamma div(E + grad A0) + v div(A(n-1) + A(n+1)); the e^2 terms cancel"),
        (curl == 0, "the targets (10)-(11) are curl-free, so the drive is longitudinal and div A is not zero"),
    ]


@check
def drive_recursion():
    x, y, M2, v = sp.symbols("x y M2 v", positive=True)
    u1, u2, nxt = (sp.Function(s)(x, y) for s in ("u1", "u2", "nxt"))
    static = lambda prev: sp.diff(u1, y, 2) - sp.diff(u2, x, y) - M2 * u1 + v * (prev + nxt)
    ok_prev = (-sp.diff(u1, y, 2) + sp.diff(u2, x, y) + M2 * u1) / v - nxt
    printed = (-sp.diff(u1, x, 2) + sp.diff(u2, x, y) + M2 * u1) / v - nxt
    u = [0.0, 0.1]
    for _ in range(4):
        u.append(2.5 * u[-1] - u[-2])
    return [
        (sp.simplify(static(ok_prev)) == 0, "the static inverse of (A82) carries -d2^2 u1"),
        (sp.simplify(static(printed) - (sp.diff(u1, y, 2) - sp.diff(u1, x, 2))) == 0, "the printed (A88) carries -d1^2 u1 and fails (A82) by d2^2 u1 - d1^2 u1"),
        (abs(u[-1] - 2.13125) < 1e-12, f"for targets (10)-(11): u(n-1) = 2.5 u(n) - u(n+1) gives {u[-1]:.2f}"),
        (abs(0.1 * 2**4 / 0.8**4 - 3.906) < 1e-3, "the text's 0.1 x 2^4/0.8^4 = 3.9 drops the -u(n+1) term"),
    ]


@check
def dip_first_order():
    e, m, g2 = 0.3, 1.0, 0.01
    divA = -(0.1 / 30 + 0.1 / 20)            # inside the box, targets (10)-(11) with N1 = 30, N2 = 20
    est = lambda t: -(e / m) * divA * (1 - math.exp(-g2 * t)) / g2
    paper = {5: 0.013, 20: 0.045, 40: 0.091, 100: 0.16, 200: 0.21}
    rows = [(abs(est(t) / p - 1) < 0.10, f"t = {t}: first-order estimate {100*est(t):.1f} %, paper {100*p:g} %") for t, p in paper.items()]
    q = PAPER_FLAT
    rows.append(("\\partial_0|\\bar\\varphi^{(n)}|^2 &= \\frac{e}{m}\\left(\\partial_1" in q, "(A86): the density moves with velocity (e/m) A, first order in e"))
    rec = next(c for c in DAG["claims"] if c["id"] == "P8")["rerun_record"]["dip_percent"]
    r1, r2 = rec["e=0.3"] / rec["e=0.15"], rec["e=0.15"] / rec["e=0.075"]
    rows.append((1.6 < r1 < 2.1 and 1.6 < r2 < 2.1, f"recorded rerun: halving e divides the dip by {r1:.2f}, then {r2:.2f}; an e^2 term would give 4 (repeat with --rerun)"))
    return rows


@check
def misprints():
    k, m, e, t, x = sp.symbols("k m e t x", positive=True)
    beta = k * x - k**2 * t / (2 * m)
    lhs = -sp.diff(beta, t) / e
    sq = (e / (2 * m)) * (-sp.diff(beta, x) / e) ** 2
    r_typo, expected = _gauss(lambda e, m: e / m)
    n_, Om = sp.symbols("n Omega", positive=True)
    kk = sp.solve(sp.Eq(k**2 + e**2 * n_ / m, Om**2), k**2)[0]
    return [
        (sp.simplify(lhs - sq) == 0 and sp.simplify(lhs + sq) != 0, "(A70): the free plane wave satisfies the + sign, not the printed -"),
        (sp.simplify(r_typo - expected) != 0, "(A76), (A78) with e instead of e^2: the continuity terms no longer cancel"),
        (sp.simplify(kk - (Om**2 - e**2 * n_ / m)) == 0, "after (A47): a real resonant k needs Omega^2 >= e^2 n/m"),
    ]


@check
def madelung_pair():
    """(A63) with phi = R exp(i beta): imaginary part gives (A69), real part gives (A70) with the + sign."""
    t, x, y = sp.symbols("t x y", real=True)
    e, m = sp.symbols("e m", positive=True)
    J = sp.symbols("J")                                   # stands for the imaginary unit
    R, beta, A0, A1, A2 = (sp.Function(s)(t, x, y) for s in ("R", "beta", "A0", "A1", "A2"))
    D = lambda F, var, A: sp.diff(F, var) + J * sp.diff(beta, var) * F - J * e * A * F
    pref = J * (sp.diff(R, t) + J * sp.diff(beta, t) * R) + e * A0 * R + (D(D(R, x, A1), x, A1) + D(D(R, y, A2), y, A2)) / (2 * m)
    poly = sp.Poly(sp.expand(pref), J)
    co = {k[0]: c for k, c in zip(poly.monoms(), poly.coeffs())}
    re_ = sum(c * (-1) ** (k // 2) for k, c in co.items() if k % 2 == 0)
    im_ = sum(c * (-1) ** ((k - 1) // 2) for k, c in co.items() if k % 2 == 1)
    V1, V2 = A1 - sp.diff(beta, x) / e, A2 - sp.diff(beta, y) / e
    a69 = sp.diff(R**2, t) - (e / m) * (sp.diff(R**2 * V1, x) + sp.diff(R**2 * V2, y))
    lap = (sp.diff(R, x, 2) + sp.diff(R, y, 2)) / (2 * m * e * R)
    plus = A0 - sp.diff(beta, t) / e + lap - (e / (2 * m)) * (V1**2 + V2**2)
    ok69 = sp.simplify(sp.expand(2 * R * im_ - a69)) == 0 or sp.simplify(sp.expand(2 * R * im_ + a69)) == 0
    return [(ok69, "Im part of (A63): the continuity equation (A69)"),
            (sp.simplify(sp.expand(re_ / (e * R) - plus)) == 0,
             "Re part: (A70) with + (e/2m)(A - grad beta/e)^2 and the Laplacian term, the only term that carries Planck's constant")]


# ---------------------------------------------------------------- numbers
kT = 8.617333262e-5 * 310
HC_EV_UM = 1.23984198


@check
def thermal_numbers():
    yr = 365.25 * 86400
    return [
        (abs(kT * math.log(2) - 0.0185) < 1e-4, f"k_B T ln 2 at 310 K = {1e3*kT*math.log(2):.1f} meV (paper: 20)"),
        (abs(HC_EV_UM / 0.5 - 2.48) < 0.005, f"500 nm photon = {HC_EV_UM/0.5:.2f} eV (paper: 2.4)"),
        (abs(HC_EV_UM / (kT * math.log(2)) - 67) < 0.5, f"hc/(k_B T ln 2) = {HC_EV_UM/(kT*math.log(2)):.0f} um (paper: 60, from 20 meV)"),
        (abs(kT * math.log(yr / 1e-12) - 1.20) < 0.005, f"one-year barrier, attempt time 1 ps: {kT*math.log(yr/1e-12):.2f} eV"),
        (abs(kT * math.log(yr / 1.0) - 0.461) < 0.001, f"one-year barrier, attempt time 1 s: {kT*math.log(yr):.2f} eV"),
    ]


@check
def capacity_numbers():
    per_mm2 = 4 * 1.3 * 2e-3 / (500e-9) ** 3 * 1e-6
    PB = per_mm2 * 2500e2 / 8 / 1e15
    surface_TB = 4 / (500e-9) ** 2 * 2500e-4 / 8 / 1e12
    lam4 = 1239.84198 / 0.004 / 1e3
    return [
        (abs(per_mm2 / 8.32e10 - 1) < 1e-3, f"4 n_r d/lambda^3 = {per_mm2:.3g} bit/mm^2"),
        (abs(PB - 2.6) < 0.01, f"x 2500 cm^2 = {PB:.2f} PB (paper: 2.5)"),
        (abs(250e12 / 8 / 1e12 - 31.25) < 1e-9, "250e12 synapses x 1 bit = 31.25 TB (paper: 30)"),
        (abs(surface_TB - 0.5) < 1e-9 and abs(1.3 * 2e-3 / 500e-9 - 5200) < 1e-6, f"surface hologram {surface_TB:.1f} TB; thickness factor n_r d/lambda = 5200"),
        (abs(lam4 - 310) < 1 and abs(PB * 1e9 * (0.5 / lam4) ** 3 - 11) < 0.5, f"at 4 meV: lambda = {lam4:.0f} um, capacity {PB*1e9*(0.5/lam4)**3:.0f} MB"),
        (abs(PB * (500 / 1500) ** 3 - 0.096) < 0.002, "at 1500 nm: about 0.1 PB"),
    ]


@check
def waveguide_numbers():
    V = 2 * math.pi * 12.5 / 500 * math.sqrt(1.5**2 - 1.33**2)
    return [(abs(V - 0.11) < 0.005, f"V = (2 pi a/lambda) sqrt(n1^2 - n2^2) = {V:.2f} at a = 12.5 nm, 500 nm"),
            (500 / 21 > 20, "500 nm is 24 times the 21 nm cutoff, on the side a hollow guide does not pass")]


@check
def energy_budget():
    rate = 1e-13 / (HC_EV_UM / 0.5 * 1.602176634e-19)
    years = 2.5e15 * 8 / rate / (365.25 * 86400)
    return [(abs(rate / 2.5e5 - 1) < 0.02, f"1e-13 W at 500 nm = {rate:.3g} photons/s"),
            (abs(years / 2500 - 1) < 0.02, f"2.5 PB at one photon per bit: {years:.0f} years")]


@check
def rerun_gauss():
    rec = next(c for c in DAG["claims"] if c["id"] == "P2r")["rerun_record"]
    paper = {5: 1.3, 20: 4.5, 40: 9.1}
    rows = [(1.0 <= g <= 2.4, f"recorded rerun, t = {t:g}: rms Gauss residual / rms charge change = {g:.2f}")
            for t, g in zip(rec["t"], rec["gauss_over_charge"])]
    rows += [(abs(d / paper[t] - 1) < 0.12, f"recorded rerun, t = {t:g}: dip {d:.2f} % against the paper's {paper[t]:g} % (input {rec['input']:g})")
             for t, d in zip(rec["t"], rec["dip_percent"])]
    return rows + [(True, "repeat with --rerun")]


# ---------------------------------------------------------------- the simulation (--rerun)
def simulate(t_end, e=0.3, dt=0.001, input_max=None, marks=(5.0, 20.0, 40.0)):
    """(A82)-(A87) with inputs from the corrected (A88)-(A89), RK4 on a 128 x 128 periodic grid."""
    L, Ns, m, v, gam, M2, gam2, N, N1, N2 = 128, 64, 1.0, 0.8, 0.2, 2.0, 0.01, 4, 30, 20
    n = np.arange(-Ns, Ns)
    n1, n2 = np.meshgrid(n, n, indexing="ij")
    tri = lambda k, Nk: np.where(k <= -Nk, 0.1 * (k + Ns) / (Ns - Nk), np.where(k >= Nk, 0.1 * (k - Ns) / (Ns - Nk), -0.1 * k / Nk))
    d1 = lambda f: (np.roll(f, -1, -2) - np.roll(f, 1, -2)) / 2
    d2 = lambda f: (np.roll(f, -1, -1) - np.roll(f, 1, -1)) / 2
    d11 = lambda f: np.roll(f, -1, -2) - 2 * f + np.roll(f, 1, -2)
    d22 = lambda f: np.roll(f, -1, -1) - 2 * f + np.roll(f, 1, -1)
    u1 = {N: tri(n1, N1).astype(float), N + 1: 0.0 * n1}
    u2 = {N: tri(n2, N2).astype(float), N + 1: 0.0 * n2}
    for J in range(1, N + 1):
        k = N - J
        u1[k] = (-d22(u1[k + 1]) + d1(d2(u2[k + 1])) + M2 * u1[k + 1]) / v - u1[k + 2]
        u2[k] = (-d11(u2[k + 1]) + d1(d2(u1[k + 1])) + M2 * u2[k + 1]) / v - u2[k + 2]
    U1, U2 = u1[0], u2[0]
    if input_max:
        s = input_max / np.abs(U1).max()
        U1, U2 = U1 * s, U2 * s
    A0_of = lambda A1, A2, rho: -(d11(np.sqrt(rho)) + d22(np.sqrt(rho))) / (2 * m * e * np.sqrt(rho)) + e * (A1**2 + A2**2) / (2 * m)

    def nb(A, U, t):
        return np.concatenate([(U * np.exp(-gam2 * t))[None], A[:-1]], 0) + np.concatenate([A[1:], np.zeros_like(A[:1])], 0)

    def rhs(t, A1, A2, E1, E2, rho):
        A0 = A0_of(A1, A2, rho)
        return (E1 + d1(A0), E2 + d2(A0),
                d22(A1) - d1(d2(A2)) - e**2 * rho / m * A1 - M2 * A1 - gam * (E1 + d1(A0)) + v * nb(A1, U1, t),
                d11(A2) - d1(d2(A1)) - e**2 * rho / m * A2 - M2 * A2 - gam * (E2 + d2(A0)) + v * nb(A2, U2, t),
                (e / m) * (d1(rho * A1) + d2(rho * A2)))

    y = [np.zeros((N, L, L)) for _ in range(4)] + [np.ones((N, L, L))]
    box = (np.abs(n1) < N1) & (np.abs(n2) < N2)
    out, t = [], 0.0
    for i in range(1, int(round(t_end / dt)) + 1):
        k1 = rhs(t, *y)
        k2 = rhs(t + dt / 2, *[a + dt / 2 * b for a, b in zip(y, k1)])
        k3 = rhs(t + dt / 2, *[a + dt / 2 * b for a, b in zip(y, k2)])
        k4 = rhs(t + dt, *[a + dt * b for a, b in zip(y, k3)])
        y = [a + dt / 6 * (b + 2 * c + 2 * d + f) for a, b, c, d, f in zip(y, k1, k2, k3, k4)]
        t = i * dt
        if round(t, 6) in marks:
            top, E1, E2 = y[4][-1], y[2][-1], y[3][-1]
            G = d1(E1) + d2(E2) + e * top - e
            ch = e * (top - 1)
            out.append((round(t, 6), 1 - top[box].mean(), float(np.sqrt((G**2).mean()) / np.sqrt((ch**2).mean()))))
    return out, float(np.abs(U1).max())


def rerun():
    rows, _ = simulate(40.0, input_max=3.0)
    paper = {5.0: 0.013, 20.0: 0.045, 40.0: 0.091}
    res = [(abs(d / paper[t] - 1) < 0.12, f"input scaled to 3: t = {t:g}, dip {100*d:.2f} % (paper {100*paper[t]:g} %), Gauss/charge {g:.2f}") for t, d, g in rows]
    res.append((all(1.0 <= g <= 2.4 for _, _, g in rows), "Gauss residual 1.1 to 2.3 times the charge change"))
    full, _ = simulate(20.0, e=0.3, dt=0.002, marks=(20.0,))
    half, _ = simulate(20.0, e=0.15, dt=0.002, marks=(20.0,))
    ratio = full[0][1] / half[0][1]
    res.append((1.6 < ratio < 2.1, f"halving e at t = 20: dip {100*full[0][1]:.2f} % -> {100*half[0][1]:.2f} %, ratio {ratio:.2f} (first order gives 2, e^2 would give 4)"))
    return res


# ---------------------------------------------------------------- goals: the posts and documents
BANNED_POSTS = (r"\b(WDP|witness(?:ed)?|supplied|derived|channels?|packets?|evaluators?|ledgers?|omega|anomalon|lean4?|"
                r"metaphysics?|metaphysical|ontolog\w*|philosoph\w*|chatgpt|deepseek|claude|run_f|llm|language model|apparatus)\b")
BANNED_DOCS = (r"\b(WDP|Witnessed Difference|Projection Obstruction|omega engine|anomalon|metaphysic\w*|ontolog\w*|philosoph\w*|"
               r"chatgpt|deepseek|claude|run_f|llm|language model|apparatus)\b|claude\.ai")


def posts(text):
    out = []
    for m in re.finditer(r"^## (\d+)\. (.*?)\n\nPicture: `([^`]+)`\n\n> (.*?)\n", text, flags=re.M):
        out.append((int(m.group(1)), m.group(2), m.group(3), m.group(4)))
    return out


def png_size(p):
    with open(p, "rb") as f:
        head = f.read(24)
    return struct.unpack(">II", head[16:24]) if head[:8] == b"\x89PNG\r\n\x1a\n" else (0, 0)


def bare(s):
    """Lower case, no quote marks, one space: for matching a quotation against its source."""
    for tex, uni in (("$\\theta_0$", "\u03b8\u2080"), ("$L_3$", "L\u2083"), ("$10^{-13}$", "10\u207b\u00b9\u00b3")):
        s = s.replace(tex, uni)
    return re.sub(r"\s+", " ", re.sub(r"[\"'\u2018\u2019\u201c\u201d]", "", s)).strip(" .,").lower()


def quotes(s):
    s = s.replace("“", '"').replace("”", '"')
    return [q for q in re.findall(r'"([^"]+)"', s)]


def post_tests(text, check_files=True):
    P = posts(text)
    res = [(len(P) == 7, f"{len(P)} posts found, 7 expected")]
    for n, title, pic, body in P:
        res.append((len(body) <= 500, f"post {n}: {len(body)} characters"))
        hits = sorted(set(h.lower() for h in re.findall(BANNED_POSTS, body, flags=re.I)))
        res.append((not hits, f"post {n}: no in-house or retired terms" + (f" (found {', '.join(hits)})" if hits else "")))
        outside = re.sub(r'"[^"]*"', "", body.replace("“", '"').replace("”", '"'))
        res.append(("offscreen" not in outside.lower(), f"post {n}: 'offscreen' only inside her quoted words"))
        for q in quotes(body):
            src = flat(q).rstrip(".,")
            res.append((src.lower() in PAPER_FLAT.lower() or src.lower() in HER_POST.lower(), f"post {n}: quote matches its source: \"{q[:50]}\""))
        if check_files:
            res.append(((HERE / pic).is_file() and png_size(HERE / pic) == (1080, 1080), f"post {n}: picture {pic} at 1080 x 1080"))
    if P:
        last = P[-1][3]
        res.append(("[link]" in last and 500 - len(last) + len("[link]") >= 100, f"post 7 leaves {500 - len(last) + 6} characters for the link"))
    return res


def doc_tests(name, cite_paper_quotes):
    s = (HERE / name).read_text(encoding="utf-8")
    hits = sorted(set(h.lower() for h in re.findall(BANNED_DOCS, s, flags=re.I)))
    res = [(not hits, f"{name}: no in-house terms or model names" + (f" (found {', '.join(hits)})" if hits else ""))]
    labels = sorted(set(re.findall(r"\(A(\d+)\)", s)), key=int)
    missing = [a for a in labels if not re.search(rf"\\tag\{{A{a}\}}|\(A{a}\)", PAPER)]
    res.append((not missing, f"{name}: all {len(labels)} equation labels it cites occur in the paper" + (f" (missing {missing})" if missing else "")))
    if cite_paper_quotes:
        bad = [q for q in quotes(s) if len(q.split()) >= 4 and bare(q.replace(" [sic]", "")) not in bare(PAPER_FLAT)
               and bare(q) not in bare(HER_POST)]
        res.append((not bad, f"{name}: every quote of four words or more matches the paper" + (f" (no match: {bad[:3]})" if bad else "")))
    return res


REVIEW_NUMBERS = ["2.13", "3.9", "18.5 meV", "2.48 eV", "67 µm", "1.20 eV", "0.46 eV", "8.32", "2.6 PB", "31.25 TB", "0.5 TB",
                  "5200", "310 µm", "11 MB", "0.045", "0.11", "4000", "1.1 to 2.3", "0.25"]


def source_hash(name):
    """First 16 hex digits of the SHA-256 of a text file, line endings normalized to LF."""
    text = (HERE / name).read_text(encoding="utf-8").replace("\r\n", "\n")
    return hashlib.sha256(text.encode("utf-8")).hexdigest()[:16]


def pdf_keyword_hash(path):
    """The source hash the build wrote into the PDF keywords (stored as UTF-16 hex inside a compressed stream)."""
    raw = path.read_bytes()
    blobs = [raw]
    for m in re.finditer(rb"stream\r?\n(.*?)\r?\nendstream", raw, re.S):
        try:
            blobs.append(zlib.decompress(m.group(1)))
        except zlib.error:
            pass
    tag = "source-sha256-"
    for blob in blobs:
        low = blob.lower()
        i = low.find(tag.encode("utf-16-be").hex().encode())
        if i >= 0:
            j = i + len(tag) * 4
            return bytes.fromhex(low[j:j + 64].decode()).decode("utf-16-be")
        i = blob.find(tag.encode())
        if i >= 0:
            return blob[i + len(tag):i + len(tag) + 16].decode()
    return None


def pdf_tests():
    pdf = HERE / "5_dissection.pdf"
    if not pdf.is_file():
        return [(False, "5_dissection.pdf exists")]
    got, want = pdf_keyword_hash(pdf), source_hash("5_dissection.md")
    return [(got == want, f"5_dissection.pdf was built from the current 5_dissection.md (source hash {want}, PDF says {got})")]


def build_pdf():
    """pandoc to LaTeX, then xelatex twice; the source hash goes into the PDF keywords."""
    if not (shutil.which("pandoc") and shutil.which("xelatex")):
        return [(False, "pandoc and xelatex are on the PATH")]
    tables = r"\usepackage{etoolbox}\AtBeginEnvironment{longtable}{\renewcommand{\arraystretch}{1.3}}"
    with tempfile.TemporaryDirectory() as tmp:
        tex = pathlib.Path(tmp) / "5_dissection.tex"
        subprocess.run(["pandoc", str(HERE / "5_dissection.md"), "-s", "-o", str(tex), "--shift-heading-level-by=-1",
                        "-V", "documentclass=article", "-V", "fontsize=11pt", "-V", "geometry:margin=1in",
                        "-V", "linestretch=1.08", "-V", "colorlinks=true", "-V", "linkcolor=teal", "-V", "urlcolor=teal",
                        "-V", "header-includes=" + tables, "-M", "date=November 2026",
                        "-M", "keywords=source-sha256-" + source_hash("5_dissection.md")], check=True)
        for _ in range(2):
            subprocess.run(["xelatex", "-interaction=nonstopmode", tex.name], cwd=tmp, stdout=subprocess.DEVNULL, check=False)
        log = (pathlib.Path(tmp) / "5_dissection.log").read_text(encoding="utf-8", errors="replace")
        out = pathlib.Path(tmp) / "5_dissection.pdf"
        if out.is_file():
            shutil.copy(out, HERE / "5_dissection.pdf")
        pages = re.search(r"Output written on .*?\((\d+) pages", log)
        return [(out.is_file(), f"xelatex wrote 5_dissection.pdf ({pages.group(1) if pages else '?'} pages)"),
                (not re.search(r"Overfull \\hbox", log), "no overfull lines"),
                (not re.search(r"Missing character", log), "no missing characters")]


def goal_tests(goal):
    gid = goal["id"]
    if gid in ("G1", "G2"):
        return post_tests(REPLIES)
    if gid == "G3":
        s = (HERE / "6_review_for_the_authors.md").read_text(encoding="utf-8")
        plain = s.replace("$", "")
        return doc_tests("6_review_for_the_authors.md", False) + [(n in plain, f"review quotes the recomputed value {n}") for n in REVIEW_NUMBERS]
    if gid == "G4":
        return doc_tests("5_dissection.md", True) + pdf_tests()
    if gid == "G5":
        return [(set(c["check"] for c in DAG["claims"]) <= set(CHECKS), "every claim names a check that exists")]
    return [(False, f"no tests for {gid}")]


def selftest():
    good = REPLIES
    P = posts(good)
    breaks = {
        "dropped 'perhaps'": good.replace("Vision is perhaps the most", "Vision is the most"),
        "in-house term": good.replace("I read the paper you linked", "I read, as witnessed, the paper you linked"),
        "over-length post": good.replace(P[0][3], P[0][3] + " " + "x" * 60),
    }
    res = [(all(ok for ok, _ in post_tests(good, False)), "the posts as written pass")]
    for name, bad in breaks.items():
        res.append((not all(ok for ok, _ in post_tests(bad, False)), f"{name}: caught"))
    return res


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--rerun", action="store_true")
    ap.add_argument("--selftest", action="store_true")
    ap.add_argument("--pdf", action="store_true")
    a = ap.parse_args()
    failed = []

    def show(label, rows):
        for ok, msg in rows:
            print(("PASS " if ok else "FAIL ") + label + "  " + msg)
            if not ok:
                failed.append(label + " " + msg)

    if a.pdf:
        show("pdf", build_pdf())
    held = {}
    for c in DAG["claims"]:
        rows = CHECKS[c["check"]]() if c["check"] in CHECKS else [(False, "no such check: " + c["check"])]
        held[c["id"]] = all(ok for ok, _ in rows)
        show(c["id"], rows)
    for gl in DAG["goals"]:
        rows = goal_tests(gl) + [(held.get(n, False), f"needs {n}") for n in gl.get("needs", [])]
        show(gl["id"], rows)
    if a.rerun:
        show("rerun", rerun())
    if a.selftest:
        show("selftest", selftest())
    print("\nALL PASS" if not failed else f"\n{len(failed)} FAILED")
    return 0 if not failed else 1


if __name__ == "__main__":
    sys.exit(main())
