"""Re-derivations behind 03_critique/revised_review_check.md (the revised outside review package).

Run from the folder above:  python -I code/revised_review_checks.py
Exit 0 only if every expectation holds.
"""
import math
import sys
import sympy as sp

FAIL = []


def expect(cond, msg):
    print(("PASS " if cond else "FAIL ") + msg)
    if not cond:
        FAIL.append(msg)


# 1. (A88) as printed versus the static inverse of (A82).
x, y, M2, v = sp.symbols("x y M2 v", positive=True)
u1, u2, nxt = sp.Function("u1")(x, y), sp.Function("u2")(x, y), sp.Function("nxt")(x, y)
prev_ok = (-sp.diff(u1, y, 2) + sp.diff(u2, x, y) + M2 * u1) / v - nxt     # from (A82)
prev_pr = (-sp.diff(u1, x, 2) + sp.diff(u2, x, y) + M2 * u1) / v - nxt     # (A88) as printed
static_A82 = lambda prev: sp.diff(u1, y, 2) - sp.diff(u2, x, y) - M2 * u1 + v * (prev + nxt)
expect(sp.simplify(static_A82(prev_ok)) == 0, "the inverse built from (A82) satisfies the static (A82)")
res = sp.simplify(static_A82(prev_pr))
expect(res != 0 and sp.simplify(res - (sp.diff(u1, y, 2) - sp.diff(u1, x, 2))) == 0,
       "the printed (A88) leaves the residual d2^2 u1 - d1^2 u1")

# 2. For the paper's targets, u1 = u1(x) and u2 = u2(y): the (A82) inverse has no derivative terms at all.
f, h = sp.Function("f")(x), sp.Function("h")(y)
expect(sp.diff(f, y, 2) == 0 and sp.diff(h, x, y) == 0, "d2^2 u1 = 0 and d1 d2 u2 = 0 exactly for u1(x), u2(y)")
u = [0.0, 0.1]  # u_{N+1}, u_N
for _ in range(4):
    u.append(2.5 * u[-1] - u[-2])
expect(abs(u[-1] - 2.13125) < 1e-12, f"so the recursion u(n-1) = 2.5 u(n) - u(n+1) gives u0 = {u[-1]:.5f}, not 3.90625")

# 3. The resonance threshold: omega_k = sqrt(k^2 + e^2 n/m) >= sqrt(e^2 n/m), so Omega^2 >= e^2 n/m.
e, n, m, k, Om = sp.symbols("e n m k Omega", positive=True)
omega = sp.sqrt(k**2 + e**2 * n / m)
ksq = sp.solve(sp.Eq(omega**2, Om**2), k**2)[0]
expect(sp.simplify(ksq - (Om**2 - e**2 * n / m)) == 0, "a real resonant k needs Omega^2 >= e^2 n/m (the paper prints Omega >= e^2 n/m)")
expect(abs(math.sqrt(0.09) - 0.3) < 1e-12, "at the Section 4 numbers e^2 n/m = 0.09 m^2, so the threshold is Omega >= 0.3 m")

# 4. Two-level density: frozen |phi|^2 forces the coherence to vanish wherever phi0* phi1 != 0.
t, Omg = sp.symbols("t Omega", positive=True)
c0, c1 = sp.symbols("c0 c1")          # slow amplitudes, held fixed over one optical period
p0, p1 = sp.symbols("p0 p1")          # phi0(x), phi1(x) at one point
phi = c0 * sp.exp(-sp.I * 0 * t) * p0 + c1 * sp.exp(-sp.I * Omg * t) * p1
dens = sp.expand(phi * sp.conjugate(phi))
cross = sp.simplify(dens - c0 * sp.conjugate(c0) * p0 * sp.conjugate(p0) - c1 * sp.conjugate(c1) * p1 * sp.conjugate(p1))
expect(sp.simplify(sp.diff(cross, t)) != 0, "the cross term 2 Re(c0* c1 e^{-i Omega t} phi0* phi1) oscillates at Omega")
expect(sp.simplify(cross.subs(c1, 0)) == 0, "and vanishes only when c0* c1 = 0 (or phi0* phi1 = 0 there)")

# 5. The revised review's numbers.
T = lambda nn: 1 / (1 + 0.045 * nn)
expect(abs((T(0.79) - T(1)) - 0.008733) < 1e-6, "transmission difference for a 21 % density dip: 0.00873")
kT = 8.617333262145e-5 * 310
Y = 365.25 * 86400
for t0, mean, rel in ((1e-12, 1.199, 1.322), (1.0, 0.461, 0.584)):
    expect(abs(kT * math.log(Y / t0) - mean) < 2e-3 and abs(kT * math.log(Y / (t0 * -math.log1p(-0.01))) - rel) < 2e-3,
           f"attempt {t0:g} s: one-year mean barrier {mean} eV, 1 % failure barrier {rel} eV")

if FAIL:
    print("\nFAILED:", *FAIL, sep="\n  ")
    sys.exit(1)
print("ALL PASS")
