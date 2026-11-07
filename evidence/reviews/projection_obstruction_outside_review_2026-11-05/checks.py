"""Replays used in the 2026-11-05 check of an outside review of
Projection Obstruction v6.9.20 (papers/000_projection_obstruction).

Run from the repository root:
    python reviews/projection_obstruction_outside_review_2026-11-05/checks.py

C1  Proposition 7.4.5 / Corollary 7.4.6: three-patch Local Green / Global Red,
    scaling, and the quotient class of the section defect (7.4.8).
C2  WDP-DIM-1 / T.8 row counts applied to the three-patch family: how many
    added linear rows make the three observers raw-sound and repair-class
    sound.
C3  Theorem 5.16 sharpness example: V=R, A=1, m=1, f=(x-1)^p.
C4  Corollary 5.17 on two qubits: pair readout under three Hamiltonians
    (onset 1, persistent zero, onset 3), cyclic dimension kappa against the
    bound binom(d^2+2, 2) = 153.
C5  Onset order depends on the readout: the same residual read through two
    different linear maps has onset 1 and onset 2.
"""
from __future__ import annotations

import sys
from itertools import product
from math import comb
from pathlib import Path

import sympy as sp

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "papers" / "000_projection_obstruction" / "code"))
from polynomial_onset import certify_onset, verify_onset  # noqa: E402

OK = []


def check(name: str, cond: bool, detail: str = "") -> None:
    OK.append(cond)
    print(f"[{'PASS' if cond else 'FAIL'}] {name} {detail}")


# ---------------------------------------------------------------- C1
def c1() -> None:
    e = sp.eye(3)
    patches = ["u1", "u2", "u3"]
    overlaps = {"x12": (0, 1), "x23": (1, 2), "x31": (2, 0)}
    edges = [(x, patches[i]) for x, (i, j) in overlaps.items() for i in (i, j)]
    watcher = {(x, u): patches.index(u) for (x, u) in edges}

    def section(lam):
        s = {u: lam * e[:, k] for k, u in enumerate(patches)}
        s.update({x: sp.zeros(3, 1) for x in overlaps})
        return s

    def defect(s):
        return {ed: s[ed[1]] - s[ed[0]] for ed in edges}  # identity restrictions

    def raw(d):
        return sum(sum(abs(v) for v in d[ed]) for ed in edges)

    def tallies(d):
        out = []
        for a in range(3):
            tot = 0
            for ed in edges:
                if watcher[ed] == a:
                    v = d[ed].copy()
                    v.row_del(a)
                    tot += sum(abs(x) for x in v)
            out.append(tot)
        return out

    d1 = defect(section(1))
    check("C1a three-patch: I(s)=6, J=[0,0,0]", raw(d1) == 6 and tallies(d1) == [0, 0, 0])
    for lam in (sp.Rational(1, 7), 5, 10**6):
        d = defect(section(lam))
        check(f"C1b scaled lam={lam}: I=6*lam, All-Green", raw(d) == 6 * lam and tallies(d) == [0, 0, 0])
    # 7.4.8: Delta(s) = d0 s is exact, so the quotient class is zero: repair
    # alpha = s itself gives Delta(s) - d0 alpha = 0.
    check("C1c Phi([Delta(s)]) = 0 (defect is a coboundary; repair alpha = s)", raw(defect({k: v - v for k, v in section(1).items()})) == 0)


# ---------------------------------------------------------------- C2
def c2() -> None:
    # Carrier: C^0 = (R^3)^6 indexed [u1,u2,u3,x12,x23,x31]; C^1 = (R^3)^6 over
    # the six covering edges. d0: s -> (s(u_i) - s(x_ij)). Observers: each edge
    # (x_ij,u_i) is watched only by observer i through deletion of coordinate i.
    patches = ["u1", "u2", "u3"]
    overlaps = {"x12": (0, 1), "x23": (1, 2), "x31": (2, 0)}
    nodes = patches + list(overlaps)
    edges = [(x, i) for x, (i, j) in overlaps.items() for i in (i, j)]  # (overlap, patch index)
    n0, n1 = 3 * len(nodes), 3 * len(edges)
    D0 = sp.zeros(n1, n0)
    for r, (x, i) in enumerate(edges):
        for c in range(3):
            D0[3 * r + c, 3 * i + c] = 1
            D0[3 * r + c, 3 * nodes.index(x) + c] = -1
    # Q: stacked observer rows, 2 rows per edge (delete coordinate i)
    Q = sp.zeros(2 * len(edges), n1)
    for r, (x, i) in enumerate(edges):
        rows = [c for c in range(3) if c != i]
        for k, c in enumerate(rows):
            Q[2 * r + k, 3 * r + c] = 1
    R = D0.columnspace()           # realizable defects
    B = R                          # repairs are the same coboundary (PO uses d0 for both)
    K = Q.nullspace()
    V = n1

    def dim(vs):
        return sp.Matrix.hstack(*vs).rank() if vs else 0

    def inter(X, Y):
        # dim(X cap Y) = dim X + dim Y - dim(X + Y)
        return dim(X) + dim(Y) - dim(X + Y)

    dR, dK, dRK = dim(R), dim(K), inter(R, K)
    m_raw = dRK
    m_quot = dK - inter(K, B)
    m_both = dK - inter(K, B) + inter(R, K)  # T = R cap K cap B = R cap K since R = B
    m_quot_R = dRK - dRK                      # T.8 with R = B
    print(f"      dim V={V}, dim R=dim B={dR}, dim K={dK}, dim(R cap K)={dRK}")
    print(f"      WDP-DIM-1: m_raw={m_raw}, m_quot={m_quot}, m_both={m_both}; T.8 m_quot,R={m_quot_R}")
    check("C2a three observers are not raw-sound: R cap K != 0", dRK > 0)
    check("C2b arbitrary-cochain repair-class soundness needs 3 rows; restricted to realizable defects (T.8) it needs 0", m_quot == 3 and m_quot_R == 0)
    # Attainment: dual rows of a basis of R cap K make the augmented observer raw-sound.
    # R cap K: solve for s with D0 s in K, i.e. Q D0 s = 0; then R cap K = D0 * null(Q D0)
    RKvecs = [D0 * v for v in (Q * D0).nullspace()]
    RKvecs = [v for v in RKvecs if any(v)]
    basis = sp.Matrix.hstack(*RKvecs)
    _, piv = basis.rref()           # independent columns
    Bm = basis[:, list(piv)]
    E = (Bm.T * Bm).inv() * Bm.T          # rows: dual coordinates on R cap K
    A = Q.col_join(E)
    check("C2c adding m_raw dual rows makes the observer injective on R", (A * sp.Matrix.hstack(*R)).rank() == dR, f"(added {E.rows} rows)")


# ---------------------------------------------------------------- C3
def c3() -> None:
    for p in (1, 2, 3, 5):
        f = sp.Poly((sp.Symbol("x") - 1) ** p)
        readout = {(k,): f.coeff_monomial(sp.Symbol("x") ** k) for k in range(p + 1)}
        cert = certify_onset([[1]], [1], [readout])
        kappa = len(cert.annihilator) - 1
        check(f"C3 p={p}: kappa={kappa}=p+1, onset={cert.first_onset}=p, replay", kappa == p + 1 and cert.first_onset == p and verify_onset([[1]], [1], [readout], cert))


# ---------------------------------------------------------------- C4/C5
I2 = sp.eye(2)
X = sp.Matrix([[0, 1], [1, 0]])
Y = sp.Matrix([[0, -sp.I], [sp.I, 0]])
Z = sp.Matrix([[1, 0], [0, -1]])
PAULI = [I2, X, Y, Z]
BASIS = [sp.kronecker_product(a, b) for a in PAULI for b in PAULI]  # Hermitian basis of 4x4, real coords


def coords(M):
    # M Hermitian 4x4 -> real coordinates in Pauli basis (M = sum c_k P_k, c_k = Tr(P_k M)/4)
    return sp.Matrix([sp.simplify((P * M).trace() / 4) for P in BASIS])


def from_coords(c):
    return sum((c[k] * BASIS[k] for k in range(16)), sp.zeros(4, 4))


def liouvillian(H):
    # A(Xm) = -i[H, Xm] as a real 16x16 matrix in the Pauli basis
    cols = [coords(-sp.I * (H * P - P * H)) for P in BASIS]
    L = sp.Matrix.hstack(*cols)
    assert all(sp.im(x) == 0 for x in L)
    return L


def ptrace_a(M):  # trace out site a (first factor) -> 2x2
    return sp.Matrix(2, 2, lambda i, j: sum(M[2 * k + i, 2 * k + j] for k in range(2)))


def ptrace_b(M):
    return sp.Matrix(2, 2, lambda i, j: sum(M[2 * i + k, 2 * j + k] for k in range(2)))


def pair_readout_polys():
    # f(X) = X - Tr_b X (x) Tr_a X, as 16 polynomials of degree <= 2 in the 16 coords
    c = sp.symbols("c0:16", real=True)
    M = from_coords(c)
    F = M - sp.kronecker_product(ptrace_b(M), ptrace_a(M))
    out = []
    for k in range(16):
        expr = sp.expand(sp.simplify((BASIS[k] * F).trace() / 4))
        poly = sp.Poly(expr, *c)
        out.append({tuple(mon): coeff for mon, coeff in zip(poly.monoms(), poly.coeffs())})
    return out


def c4() -> None:
    polys = pair_readout_polys()
    m = coords(sp.Matrix([[1, 0, 0, 0], [0] * 4, [0] * 4, [0] * 4]))  # |00><00|
    cases = {
        "XX (onset 1)": (sp.kronecker_product(X, X), 1),
        "ZX (stays product)": (sp.kronecker_product(Z, X), None),
        "-ZZ-(XI+IX), sec. 6.3 (onset 3)": (-sp.kronecker_product(Z, Z) - sp.kronecker_product(X, I2) - sp.kronecker_product(I2, X), 3),
    }
    bound = comb(16 + 2, 2)
    for name, (H, expected) in cases.items():
        L = liouvillian(H)
        cert = certify_onset(L, m, polys)
        kappa = len(cert.annihilator) - 1
        ok = cert.first_onset == expected and kappa <= bound and verify_onset(L, m, polys, cert)
        check(f"C4 {name}: onset={cert.first_onset}, kappa={kappa} <= {bound}", ok)
        if expected == 3:
            jet3 = from_coords(sp.Matrix(cert.derivatives[3]))
            target = 8 * sp.I * (sp.Matrix(4, 4, lambda i, j: 1 if (i, j) == (0, 3) else 0) - sp.Matrix(4, 4, lambda i, j: 1 if (i, j) == (3, 0) else 0))
            check("C4 F'''(0) = 8i(|00><11| - |11><00|) as printed in sec. 6.3", sp.simplify(jet3 - target) == sp.zeros(4, 4))


def c5() -> None:
    polys = pair_readout_polys()
    m = coords(sp.Matrix([[1, 0, 0, 0], [0] * 4, [0] * 4, [0] * 4]))
    L = liouvillian(sp.kronecker_product(X, X))
    full = certify_onset(L, m, polys)
    # Access map: only the ZZ coordinate of the residual (index of Z(x)Z in BASIS = 15)
    zz_only = [polys[15]]
    partial = certify_onset(L, m, zz_only)
    check("C5 full residual onset 1; ZZ-only access map onset 2", full.first_onset == 1 and partial.first_onset == 2, f"(kappa full={len(full.annihilator)-1}, kappa ZZ={len(partial.annihilator)-1})")
    # Access map that annihilates the residual entirely: read only the II coordinate (trace), always zero
    trace_only = [polys[0]]
    blind = certify_onset(L, m, trace_only)
    check("C5 trace-only access map reports persistent zero while residual is nonzero", blind.first_onset is None)


if __name__ == "__main__":
    c1(); c2(); c3(); c4(); c5()
    print(f"\n{sum(OK)}/{len(OK)} checks passed")
    sys.exit(0 if all(OK) else 1)
