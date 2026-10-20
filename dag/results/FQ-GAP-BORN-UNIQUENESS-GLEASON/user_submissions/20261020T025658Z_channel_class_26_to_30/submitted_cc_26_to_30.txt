"""Exact checks for CC-26 .. CC-30 (sympy, rationals / Gaussian rationals only)."""
from sympy import *

def E(d, j, k):
    return Matrix(d, d, lambda a, b: 1 if (a == j and b == k) else 0)

def Delta(X):
    return diag(*[X[j, j] for j in range(X.rows)])

def Ad(U):
    return lambda X: U * X * U.H

def Smat(Phi, d, e):
    """Classical kernel S[k,j] = Phi(E_jj)[k,k]."""
    return Matrix(e, d, lambda k, j: Phi(E(d, j, j))[k, k])

def kraus(L):
    return lambda X: sum((l * X * l.H for l in L), zeros(L[0].rows, L[0].rows))

def choi(Phi, d):
    e = Phi(E(d, 0, 0)).rows
    J = zeros(d * e, d * e)
    for j in range(d):
        for k in range(d):
            blk = Phi(E(d, j, k))
            J[j * e:(j + 1) * e, k * e:(k + 1) * e] = blk
    return J

ok = True
def check(name, cond):
    global ok
    cond = bool(cond)
    ok = ok and cond
    print(("PASS " if cond else "FAIL ") + name)

# ---------- CC-26 : spanning set and inversion formula ----------
for d in [2, 3, 4]:
    e = lambda j: E(d, j, j)[:, j]
    states = [e(j) * e(j).H for j in range(d)]
    for j in range(d):
        for k in range(j + 1, d):
            v = e(j) + e(k);     states.append(v * v.H / 2)
            v = e(j) - I * e(k); states.append(v * v.H / 2)
    M = Matrix([list(s) for s in states])
    check(f"CC-26 d={d}: {len(states)} states, rank {M.rank()} == d^2={d*d}", len(states) == d * d and M.rank() == d * d)
    check(f"CC-26 d={d}: all traces 1", all(s.trace() == 1 for s in states))
d = 3; e = lambda j: E(d, j, j)[:, j]
j, k = 0, 1
rp = (e(j) + e(k)) * (e(j) + e(k)).H / 2
rm = (e(j) - I * e(k)) * (e(j) - I * e(k)).H / 2
check("CC-26 inversion E_jk = rp - i rm - (1-i)/2 (E_jj+E_kk)",
      simplify(rp - I * rm - (1 - I) / 2 * (E(d, j, j) + E(d, k, k)) - E(d, j, k)) == zeros(d, d))
check("CC-26 inversion E_kj = rp + i rm - (1+i)/2 (E_jj+E_kk)",
      simplify(rp + I * rm - (1 + I) / 2 * (E(d, j, j) + E(d, k, k)) - E(d, k, j)) == zeros(d, d))
# CP-but-not-TP example: X -> A X A* with A = diag(1, 1/2)
A = diag(1, Rational(1, 2)); Phi = Ad(A)
J = choi(Phi, 2)
check("CC-26 CP-not-TP: Choi PSD", J.is_positive_semidefinite)
check("CC-26 CP-not-TP: tr Phi(E_11) = 1/4 != 1", Phi(E(2, 1, 1)).trace() == Rational(1, 4))

# ---------- CC-27 : kernel composition ----------
U = Matrix([[3, 4], [-4, 3]]) / 5
check("CC-27 U rational unitary", U.H * U == eye(2))
SU = Smat(Ad(U), 2, 2); SUU = Smat(Ad(U * U), 2, 2)
check("CC-27 S_{Ad_U}[k,j] = |U_kj|^2", SU == Matrix(2, 2, lambda k, j: abs(U[k, j]) ** 2))
print("   S_U =", SU.tolist(), " S_U^2 =", (SU * SU).tolist(), " S_{U^2} =", SUU.tolist())
check("CC-27 failure: S_{U^2} != S_U^2", SUU != SU * SU)
check("CC-27 failure: S_{U^2} - S_U^2 = [[-288,288],[288,-288]]/625",
      SUU - SU * SU == Matrix([[-288, 288], [288, -288]]) / 625)
# obstruction term Omega = Delta Phi (Id - Delta) Psi Delta evaluated on E_00
Omega = lambda Phi, Psi: (lambda X: Delta(Phi((lambda Y: Y - Delta(Y))(Psi(Delta(X))))))
Om = Omega(Ad(U), Ad(U))
check("CC-27 failure: Omega(E_00) = diag(-288,288)/625", Om(E(2, 0, 0)) == diag(-288, 288) / 625)

# success 1: Psi measure-and-prepare in the X/Y bases -> Psi(E_jj) diagonal
e0, e1 = Matrix([1, 0]), Matrix([0, 1])
vs = [e0 + e1, e0 - e1, e0 + I * e1, e0 - I * e1]; outs = [e0, e1, e0, e1]
L = [o * v.H / 2 for v, o in zip(vs, outs)]
check("CC-27 Psi normalized (sum L*L = I)", sum((l.H * l for l in L), zeros(2, 2)) == eye(2))
Psi = kraus(L)
check("CC-27 Psi(E_00) = Psi(E_11) = I/2 (diagonal)", Psi(E(2, 0, 0)) == eye(2) / 2 and Psi(E(2, 1, 1)) == eye(2) / 2)
SPsi = Smat(Psi, 2, 2)
check("CC-27 success-1: S_{Ad_U o Psi} = S_U S_Psi", Smat(lambda X: U * Psi(X) * U.H, 2, 2) == SU * SPsi)
check("CC-27 success-1: Omega = 0 on E_00,E_11", all(Omega(Ad(U), Psi)(E(2, j, j)) == zeros(2, 2) for j in range(2)))
# success 2: Phi = Ad_U o Delta kills off-diagonals before acting
PhiD = lambda X: U * Delta(X) * U.H
check("CC-27 success-2: S_{Phi o Ad_U} = S_Phi S_U", Smat(lambda X: PhiD(U * X * U.H), 2, 2) == Smat(PhiD, 2, 2) * SU)
check("CC-27 success-2: Omega = 0", all(Omega(PhiD, Ad(U))(E(2, j, j)) == zeros(2, 2) for j in range(2)))
# success 3: disjoint coherence supports, d=3
Ablk = diag(U, 1); Bblk = diag(1, U)
SA, SB, SBA = Smat(Ad(Ablk), 3, 3), Smat(Ad(Bblk), 3, 3), Smat(Ad(Bblk * Ablk), 3, 3)
check("CC-27 success-3: S_{BA} = S_B S_A (disjoint supports)", SBA == SB * SA)
check("CC-27 success-3: Delta(B E_01 B*) = 0 and Delta(B E_10 B*) = 0",
      Delta(Bblk * E(3, 0, 1) * Bblk.H) == zeros(3, 3) and Delta(Bblk * E(3, 1, 0) * Bblk.H) == zeros(3, 3))
check("CC-27 success-3: Omega = 0", all(Omega(Ad(Bblk), Ad(Ablk))(E(3, j, j)) == zeros(3, 3) for j in range(3)))
# but Ad_B is not dephasing-covariant
check("CC-27 success-3: (a) fails for Psi=Ad_A: Ad_A(E_00) has off-diagonal", (Ablk * E(3, 0, 0) * Ablk.H)[0, 1] != 0)
check("CC-27 success-3: (b) fails for Phi=Ad_B: Delta(B E_12 B*) != 0", Delta(Bblk * E(3, 1, 2) * Bblk.H) != zeros(3, 3))
# duality: Delta_g Phi (Id - Delta_e) = 0  <=>  Phi^dagger(E_mm) diagonal for all m
Udag = lambda Phi, e, g: (lambda Y: Matrix(e, e, lambda a, b: Phi(E(e, b, a)).multiply(Y).trace()) )  # Phi^dagger via <Phi(E_ba),Y>
def dual(Phi, e, g):
    # Phi^dagger(Y)[a,b] = Tr(Phi(E_ab)^* Y) ... use definition Tr(Phi(X)^* Y) = Tr(X^* Phi^dag(Y))
    return lambda Y: Matrix(e, e, lambda a, b: (Phi(E(e, a, b)).H * Y).trace())
for name, Phi_, flag in [("Ad_B", Ad(Bblk), False), ("Ad_U o Delta", PhiD, True)]:
    ee = 3 if name == "Ad_B" else 2
    dg = dual(Phi_, ee, ee)
    diag_dual = all(dg(E(ee, m, m)).is_diagonal() for m in range(ee))
    cond_b = all(Delta(Phi_(E(ee, a, b))) == zeros(ee, ee) for a in range(ee) for b in range(ee) if a != b)
    check(f"CC-27 duality for {name}: [(b) holds] == [Phi^dag(E_mm) all diagonal] == {flag}", diag_dual == cond_b == flag)
check("CC-27 success-3: Ad_B o Delta != Delta o Ad_B (not covariant)",
      Bblk * Delta(E(3, 1, 2) + E(3, 2, 1) + E(3, 1, 1)) * Bblk.H != Delta(Bblk * (E(3, 1, 2) + E(3, 2, 1) + E(3, 1, 1)) * Bblk.H))

# ---------- CC-28 : classical lift ----------
S = Matrix([[Rational(1, 2), 1, 0], [Rational(1, 2), 0, 1]])   # 2x3 column-stochastic
T = Matrix([[Rational(1, 3), Rational(3, 4)], [Rational(2, 3), Rational(1, 4)]])
check("CC-28 S column sums 1", all(sum(S[:, j]) == 1 for j in range(3)))
check("CC-28 T column sums 1", all(sum(T[:, j]) == 1 for j in range(2)))
def lift_kraus(S):
    e, d = S.shape
    return [sqrt(S[k, j]) * E(e, k, k)[:, k] * E(d, j, j)[:, j].H for k in range(e) for j in range(d) if S[k, j] != 0]
def lift(S):
    return lambda X: diag(*list(S * Matrix([X[j, j] for j in range(X.rows)])))
KS = lift_kraus(S)
check("CC-28 Kraus normalization sum K*K = I_d", sum((K.H * K for K in KS), zeros(3, 3)) == eye(3))
X = Matrix(3, 3, lambda a, b: Rational(a + 2 * b + 1, 7)) ; X = X + X.H
check("CC-28 Kraus form equals diag(S diag X)", kraus(KS)(X) == lift(S)(X))
check("CC-28 functoriality E(TS) = E(T) o E(S)", lift(T * S)(X) == lift(T)(lift(S)(X)))
check("CC-28 E(I) = Delta", lift(eye(3))(X) == Delta(X))
def four_squares(n):
    """n = a^2+b^2+c^2+d^2 with integers (Lagrange); brute force, n small."""
    from itertools import product
    r = int(n ** 0.5) + 1
    for a, b, c, dd in product(range(r + 1), repeat=4):
        if a * a + b * b + c * c + dd * dd == n:
            return [x for x in (a, b, c, dd) if x]
    raise ValueError
def rational_lift_kraus(S):
    """Exact rational Kraus family for E(S): for s = p/q write pq = sum a_m^2, K = (a_m/q)|k><j|."""
    e, d = S.shape; Ks = []
    for k in range(e):
        for j in range(d):
            s = S[k, j]
            if s == 0: continue
            p, q = fraction(s)
            for a in four_squares(p * q):
                Ks.append(Rational(a, q) * E(e, k, k)[:, k] * E(d, j, j)[:, j].H)
    return Ks
KR = rational_lift_kraus(S)
check("CC-28 four-square rational Kraus: all entries rational", all(x.is_rational for K in KR for x in K))
check("CC-28 four-square rational Kraus: sum K*K = I_d", sum((K.H * K for K in KR), zeros(3, 3)) == eye(3))
check("CC-28 four-square rational Kraus: equals E(S)", kraus(KR)(X) == lift(S)(X))
S7 = Matrix([[Rational(1, 7), Rational(3, 4)], [Rational(6, 7), Rational(1, 4)]])
KR7 = rational_lift_kraus(S7)
check("CC-28 four-square on S7 = [[1/7,3/4],[6/7,1/4]]: normalized rational, equals E(S7)",
      sum((K.H * K for K in KR7), zeros(2, 2)) == eye(2) and all(x.is_rational for K in KR7 for x in K)
      and kraus(KR7)(X[:2, :2]) == lift(S7)(X[:2, :2]))
print("   S7 Kraus weights:", [(str(K[0,0] or K[0,1] or K[1,0] or K[1,1])) for K in KR7], "count", len(KR7))  # documented below; normalization handled by splitting 1/2 = (1/2)*1 with non-square Kraus in CC-28 text
# rational Kraus via K_kj = s_kj |k><j| ⊗ nothing  -> K*K = s^2, not s.  So instead use K_kj = |k><j| with weight: see text.
# Alternative exact rational presentation: K_{kj,m} = |k><j| for m = 1..p_kj over a common denominator D with s_kj = p_kj / D, each scaled by 1/sqrt(D)?  still irrational.
# Rational presentation that works: row-split. Documented in CC-28 text as the (a,b)-factorization with explicit check:
# Choi(E(S)) = sum_{j,k} S[k,j] |k><k| ⊗ |j><j|, which is diagonal with rational entries; Kraus from eigen-decomposition of a diagonal PSD matrix uses sqrt(S[k,j]).
J = choi(lift(S), 3)
check("CC-28 Choi diagonal rational", J.is_diagonal() and all(x.is_rational for x in J))

# ---------- CC-29 : Choi equality ----------
Omv = Matrix([1, 0, 0, 1])  # unnormalized max-entangled vector
JI = Omv * Omv.H
for cs in [[1], [Rational(3, 5), Rational(4, 5)], [Rational(5, 13), Rational(12, 13)],
           [Rational(1, 3), Rational(2, 3), Rational(2, 3)], [Rational(1, 2)] * 4, [(1 + I) / 2, (1 - I) / 2]]:
    K = [c * eye(2) for c in cs]
    check(f"CC-29 identity presentation {cs}: Choi = |Omega><Omega|", expand(choi(kraus(K), 2)) == JI)
    check(f"CC-29 identity presentation {cs}: normalized", expand(sum((k.H * k for k in K), zeros(2, 2))) == eye(2))
# different Kraus families, same channel: dephasing via {P0,P1} vs {I/√2? no} -> {I,Z}/... use rational: {(I+Z)/2,(I-Z)/2}={P0,P1}; and {I/2 * 2 copies?}
Z = diag(1, -1)
K1 = [E(2, 0, 0), E(2, 1, 1)]
K2 = [(eye(2) + Z) / 2 * 1, (eye(2) - Z) / 2]
# a genuinely different presentation: rotate within the Kraus index by rational unitary V on index space
V = Matrix([[3, 4], [-4, 3]]) / 5
K3 = [V[0, 0] * K1[0] + V[0, 1] * K1[1], V[1, 0] * K1[0] + V[1, 1] * K1[1]]
check("CC-29 dephasing: K1 vs rotated K3 same Choi", choi(kraus(K1), 2) == choi(kraus(K3), 2))
check("CC-29 dephasing: K3 is not a permutation of K1", set(map(ImmutableMatrix, K3)) != set(map(ImmutableMatrix, K1)))
# composition descends: Choi of composition depends only on Choi
Phi_a = kraus(K1); Phi_b = kraus(K3)
check("CC-29 composition descends", choi(lambda X: Ad(U)(Phi_a(X)), 2) == choi(lambda X: Ad(U)(Phi_b(X)), 2))

# ---------- CC-30 : rational unitary completion ----------
def house(v):
    n = v.rows; e1 = Matrix(n, 1, lambda a, b: 1 if a == 0 else 0)
    if v == e1:
        return eye(n)
    w = e1 - v; c = 1 - conjugate(v[0])
    return eye(n) - w * w.H / c
tests = [Matrix([Rational(1, 3), Rational(2, 3), Rational(2, 3)]),
         Matrix([Rational(3, 5), 4 * I / 5]),
         Matrix([-1, 0]), Matrix([I, 0]), Matrix([(3 + 4 * I) / 5, 0]),
         Matrix([0, Rational(3, 5), Rational(4, 5)]),
         Matrix([Rational(1, 2), Rational(1, 2), Rational(1, 2), Rational(1, 2)])]
for v in tests:
    Uh = simplify(house(v))
    check(f"CC-30 v={v.T.tolist()}: U*U=I, Ue1=v, c!=0", simplify(Uh.H * Uh) == eye(v.rows) and simplify(Uh[:, 0] - v) == zeros(v.rows, 1) and (v == E(v.rows, 0, 0)[:, 0] or (1 - conjugate(v[0])) != 0))
    print("   U =", Uh.tolist(), " det =", simplify(Uh.det()))
# inductive completion of a rational isometry W (n x m)
def complete(W):
    n, m = W.shape
    if m == 0:
        return eye(n)
    U1 = house(W[:, 0])
    R = U1.H * W                      # first column -> e1, so R = [[1, *],[0, W']]
    assert simplify(R[:, 0] - E(n, 0, 0)[:, 0]) == zeros(n, 1)
    assert simplify(R[0, 1:]) == zeros(1, m - 1)   # isometry columns orthogonal to e1
    Wp = R[1:, 1:]
    Up = complete(Wp)
    return U1 * diag(1, Up)
W = Matrix([[Rational(1, 3), Rational(2, 3)], [Rational(2, 3), Rational(1, 3)], [Rational(2, 3), -Rational(2, 3)]])
check("CC-30 W is an isometry", W.H * W == eye(2))
Uc = simplify(complete(W))
check("CC-30 completion: unitary, rational, first m columns = W", simplify(Uc.H * Uc) == eye(3) and Uc[:, :2] == W and all(x.is_rational for x in Uc))
print("   completed U =", Uc.tolist())

# ---------- CC-29 : explicit Choi-level composition (link product) and tensor ----------
def ptrace_middle(M, d, e, g):
    """Tr over the middle factor of M in M_d (x) M_e (x) M_g."""
    out = zeros(d * g, d * g)
    for a in range(d):
        for b in range(d):
            for c in range(g):
                for f in range(g):
                    out[a * g + c, b * g + f] = sum(M[(a * e + m) * g + c, (b * e + m) * g + f] for m in range(e))
    return out
def partial_T_first(J, e, g):
    """Transpose on the first (e-dim) factor of J in M_e (x) M_g."""
    out = zeros(e * g, e * g)
    for a in range(e):
        for b in range(e):
            out[a * g:(a + 1) * g, b * g:(b + 1) * g] = J[b * g:(b + 1) * g, a * g:(a + 1) * g]
    return out
from sympy.physics.quantum import TensorProduct as TP
Psi1 = Ad(U); Phi1 = kraus(K1)       # both qubit maps: d=e=g=2
JPsi, JPhi = choi(Psi1, 2), choi(Phi1, 2)
link = ptrace_middle(TP(JPsi, eye(2)) * TP(eye(2), partial_T_first(JPhi, 2, 2)), 2, 2, 2)
check("CC-29 link product: J(Phi o Psi) = Tr_e[(J(Psi) x I)(I x J(Phi)^{T_e})]", link == choi(lambda X: Phi1(Psi1(X)), 2))
# tensor product: J(Phi x Psi) = P (J(Phi) x J(Psi)) P^T with P the leg permutation (d,e,d',e') -> (d,d',e,e')
def perm_legs(d, e, dp, ep):
    n = d * e * dp * ep; P = zeros(n, n)
    for a in range(d):
        for b in range(e):
            for c in range(dp):
                for f in range(ep):
                    src = ((a * e + b) * dp + c) * ep + f        # order (d,e,d',e')
                    dst = ((a * dp + c) * e + b) * ep + f        # order (d,d',e,e')
                    P[dst, src] = 1
    return P
P = perm_legs(2, 2, 2, 2)
Jt = P * TP(JPhi, JPsi) * P.T
PhiPsi = lambda X: sum(((TP(Kk, U)) * X * (TP(Kk, U)).H for Kk in K1), zeros(4, 4))
check("CC-29 tensor: J(Phi x Psi) = P (J(Phi) x J(Psi)) P^T", Jt == choi(PhiPsi, 4))
print("\nALL PASS" if ok else "\nSOME FAILED")