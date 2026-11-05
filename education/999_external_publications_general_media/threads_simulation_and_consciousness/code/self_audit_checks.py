"""Checks behind self_audit.md: every number and equation Claude wrote in this folder.

Run from the folder above:  python code/self_audit_checks.py [--replies PATH]   (needs sympy)
Each check prints PASS or FAIL with the value it recomputed. The exit status is 0 only
if every check passes. A missing replies file, or a file with the wrong number of reply
blocks, is a failure, not a skip. Regression tests: code/test_self_audit_checks.py.
"""
import argparse, math, pathlib, re, sys
import sympy as sp

ap = argparse.ArgumentParser()
ROOT = pathlib.Path(__file__).resolve().parent.parent
ap.add_argument("--replies", default=str(ROOT / "01_thread" / "replies.md"))
ap.add_argument("--board", default=str(ROOT / "05_boards" / "markup_board.html"))
ap.add_argument("--expect-blocks", type=int, default=5)
args = ap.parse_args()

ok = True
def check(name, cond, detail=""):
    global ok
    ok &= bool(cond)
    print(("PASS " if cond else "FAIL ") + name + (f"   [{detail}]" if detail else ""))

# --- S1. Appendix A: Maxwell-Bloch algebra and the sech pulse (board card "paper inputs") ---
t, g, Om, N, L3, th0 = sp.symbols("t g Omega N L_3 theta_0", positive=True)
A, Z, R = sp.symbols("A Z R")
dZ, dR, dA = -2*g*A*R, 2*g*A*Z, g*Om/(4*sp.pi*L3)*R          # (A36)-(A38)
check("S1a energy law (A39) conserved", sp.simplify(A*dA + Om/(8*sp.pi*L3)*dZ) == 0)
check("S1b Z^2+R^2 conserved", sp.simplify(2*Z*dZ + 2*R*dR) == 0)
k = g**2*Om*N/(2*sp.pi)
theta = 2*sp.atan(sp.exp(k*t)*sp.tan(th0/2))                  # (A44)
check("S1c (A44) solves (A43)", sp.simplify(sp.diff(theta, t) - k*sp.sin(theta)) == 0)
tauR = 2*sp.pi/(g**2*Om*N); tau0 = -tauR*sp.log(sp.tan(th0/2))
Acal = sp.diff(theta, t)/(2*g)                                  # (A45), first form
target = g*Om*N/(4*sp.pi)/sp.cosh((t - tau0)/tauR)
num = [ (Acal - target).subs({g:0.7, Om:1.3, N:5, th0:0.4, t:tt}).evalf() for tt in (0.1, 1.0, 3.0) ]
check("S1d (A45) sech form, tau_R=2pi/(g^2 Omega N)", all(abs(x) < 1e-9 for x in num), f"residuals {num}")

# --- S2. Appendix A gauge: A^0=0 gives  d/dt(div A) = e|phi|^2, so div A = 0 cannot hold if |phi|^2 > 0 ---
x, y, z, e = sp.symbols("x y z e")
Ax, Ay, Az = [sp.Function(n)(t, x, y, z) for n in ("A1", "A2", "A3")]
E = [-sp.diff(c, t) for c in (Ax, Ay, Az)]                      # A^0 = 0
divE = sum(sp.diff(Ec, v) for Ec, v in zip(E, (x, y, z)))
divA = sum(sp.diff(c, v) for c, v in zip((Ax, Ay, Az), (x, y, z)))
check("S2a div E = -d/dt(div A) when A^0 = 0", sp.simplify(divE + sp.diff(divA, t)) == 0)
print("     with (A7) div E = J_0 = -e|phi|^2:  d/dt(div A) = e|phi|^2;  div A = 0 forces |phi|^2 = 0")

# --- S3. Numbers quoted in replies, board and adversary file ---
NA = 6.02214076e23
per_lambda3 = 55.5 * NA * 1e3 * (500e-9)**3
check("S3a water molecules per (500 nm)^3 ~ 4.2e9", abs(per_lambda3/4.18e9 - 1) < 0.01, f"{per_lambda3:.3e}")
kT = 8.617333e-5 * 310
check("S3b kT at 310 K = 26.7 meV", abs(kT - 0.02671) < 1e-4, f"{kT*1e3:.2f} meV")
check("S3c exp(-2.4 eV/kT) ~ e^-90 (paper's 2.4 eV)", abs(2.4/kT - 89.8) < 0.5, f"2.4/kT = {2.4/kT:.1f}")
E500 = 1239.84198/500
check("S3d photon at 500 nm = 2.48 eV, so with it the exponent is ~ -93", abs(E500/kT - 92.8) < 0.5, f"{E500/kT:.1f}")
yr, ps = 365.25*86400, 1e-12
barrier = math.log(yr/ps) * kT
check("S3e one-year retention, single barrier, supplied attempt time tau0 = 1 ps: 1.20 eV", abs(barrier - 1.20) < 0.01, f"{barrier:.3f} eV, ln = {math.log(yr/ps):.2f}")
barrier_1s = math.log(yr/1.0) * kT
check("S3e2 same year, tau0 = 1 s instead: 0.46 eV (the attempt time is an input)", abs(barrier_1s - 0.461) < 0.001, f"{barrier_1s:.3f} eV")
cap = 4*1.3*2e-3/(500e-9)**3 * 1e-6                             # bit per mm^2
check("S3f capacity 8.32e10 bit/mm^2 (paper rounds to 8e10)", abs(cap/8.32e10 - 1) < 1e-3, f"{cap:.3e}")
total_PB = cap * 2500e2 / 8 / 1e15
check("S3g x 2500 cm^2 = 2.6 PB (paper: 2.5)", abs(total_PB - 2.6) < 0.01, f"{total_PB:.3f} PB")
check("S3h 250e12 x 1 bit = 31.25 TB (paper: 30)", abs(250e12/8/1e12 - 31.25) < 1e-9)
check("S3i 250e12 x 4.7 bit = 147 TB (still < 2.6 PB)", abs(250e12*4.7/8/1e12 - 146.9) < 0.1, f"{250e12*4.7/8/1e12:.1f} TB")
fac = 0.1*2**4/0.8**4
check("S3j paper's input factor 0.1 x 2^4/0.8^4 = 3.9", abs(fac - 3.906) < 1e-3, f"{fac:.3f}")

# --- S4. Bayes: equal reports, unequal likelihoods (normalized), and the equal-weights case ---
hA = {True: 0.9, False: 0.1}; hB = {True: 0.5, False: 0.5}
check("S4a both normalized, both can emit 'true', Bayes factor 1.8 != 1",
      abs(sum(hA.values()) - 1) < 1e-12 and abs(sum(hB.values()) - 1) < 1e-12 and abs(hA[True]/hB[True] - 1.8) < 1e-12)
D = [True, False, True]
hC = dict(hB)  # a second hypothesis with the same weights as B
LA = math.prod(hC[d] for d in D); LB = math.prod(hB[d] for d in D)
check("S4b equal weights, independent reports => equal likelihoods on any data, nonzero here", LA == LB and LB > 0)
# S4c: the product rule needs independence. Same single-report weights, different joint law.
indep = {(a, b): 0.25 for a in (True, False) for b in (True, False)}          # two independent fair bits
repeat = {(a, b): (0.5 if a == b else 0.0) for a in (True, False) for b in (True, False)}  # one fair bit, read twice
marg = lambda P, i: {v: sum(p for k, p in P.items() if k[i] == v) for v in (True, False)}
check("S4c equal marginals, unequal joints: P(TT) 1/4 vs 1/2, Bayes factor 2",
      marg(indep, 0) == marg(repeat, 0) and marg(indep, 1) == marg(repeat, 1)
      and repeat[(True, True)] / indep[(True, True)] == 2.0)

# --- S5. Reply character counts (the replies file is required) ---
rep = pathlib.Path(args.replies)
if not rep.is_file():
    check("S5 replies file present", False, str(rep))
else:
    blocks = re.findall(r"^> (.*(?:\n> .*)*)", rep.read_text(encoding="utf-8"), flags=re.M)
    check("S5 number of reply blocks", len(blocks) == args.expect_blocks, f"{len(blocks)} found, {args.expect_blocks} expected")
    for i, b in enumerate(blocks, 1):
        text = "\n".join(l[2:] if l.startswith("> ") else l for l in b.split("\n"))
        check(f"S5.{i} reply block at most 500 chars", len(text) <= 500, f"{len(text)} chars")

# --- S6. The board's retention note names the supplied attempt time (review finding 4) ---
board = pathlib.Path(args.board)
if not board.is_file():
    check("S6 board file present", False, str(board))
btxt = board.read_text(encoding="utf-8") if board.is_file() else ""
sent = [s for s in re.split(r"(?<=[.])\s", btxt) if "1.2 eV" in s]
check("S6 every board sentence with 1.2 eV also states the attempt time 1 ps",
      bool(sent) and all("1 ps" in s for s in sent), f"{len(sent)} sentence(s)")

print("ALL PASS" if ok else "SOME CHECKS FAILED")
sys.exit(0 if ok else 1)
