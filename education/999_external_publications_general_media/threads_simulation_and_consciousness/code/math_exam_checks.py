"""Re-derivations behind 03_critique/math_exam_review.md (the outside mathematical examination).

Run from the folder above:  python -I code/math_exam_checks.py
Exit 0 only if every expectation holds.
"""
import sys
import numpy as np
import sympy as sp

FAIL = []


def expect(cond, msg):
    print(("PASS " if cond else "FAIL ") + msg)
    if not cond:
        FAIL.append(msg)


# 1. (A70) sign: free plane wave, R constant, A = A0 = 0.
k, m, e, t, x = sp.symbols("k m e t x", positive=True)
beta = k * x - k**2 * t / (2 * m)
lhs = -sp.diff(beta, t) / e                       # A0 - (1/e) d_t beta
sq = (e / (2 * m)) * (-sp.diff(beta, x) / e) ** 2  # (e/2m) |A - grad beta / e|^2
expect(sp.simplify(lhs - sq) == 0, "(A70) with the plus sign is solved by the free plane wave")
expect(sp.simplify(lhs + sq) != 0, "(A70) as printed (minus sign) is not: residual k^2/(e m)")

# 2. Im(chi0* chi1) is conserved by (A33)-(A34) when the field is real.
g, A = sp.symbols("g A", real=True)
c0, c1 = sp.symbols("c0 c1")
d = sp.conjugate(g * A * c1) * c1 + sp.conjugate(c0) * (-g * A * c0)
expect(sp.simplify(sp.im(sp.expand(d))) == 0, "d/dt (chi0* chi1) is real under (A33)-(A34) with real A")

# 3. Capacity at a 4 meV mode (the examination's sensitivity illustration).
lam_nm = 1239.84 / 0.004
cap_MB = 2.6e15 * (500 / lam_nm) ** 3 / 1e6
expect(abs(lam_nm / 1e3 - 310) < 1, f"4 meV gives lambda = {lam_nm/1e3:.0f} um")
expect(abs(cap_MB - 11) < 0.5, f"and the capacity formula gives {cap_MB:.1f} MB")

# 4. Corner second differences of the target (10) on the paper's grid.
n = np.arange(-64, 65)
f = np.interp(n, [-64, -30, 30, 64], [0, 0.1, -0.1, 0])
d2 = f[2:] - 2 * f[1:-1] + f[:-2]
idx = np.nonzero(np.abs(d2) > 1e-12)[0]
expect(sorted(n[1:-1][idx].tolist()) == [-30, 30], "second differences are nonzero exactly at n = +-30")
expect(abs(abs(d2[idx][0]) - 0.1 * (1 / 30 + 1 / 34)) < 1e-9, f"with magnitude 0.1(1/30+1/34) = {abs(d2[idx][0]):.6f}")
expect(abs(abs(d2[idx][0]) / 0.2 - 0.031) < 0.002, "which is 3.1 % of the M^2 u1 term at those cells")

if FAIL:
    print("\nFAILED:", *FAIL, sep="\n  ")
    sys.exit(1)
print("ALL PASS")
