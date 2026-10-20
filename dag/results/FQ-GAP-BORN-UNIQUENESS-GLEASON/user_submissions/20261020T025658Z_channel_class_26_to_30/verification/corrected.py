"""Reviewed bounded CC-26..30 replay: exact rational/Gaussian rational matrices. General proofs are separate; failure exits nonzero."""
from sympy import *
from sympy.matrices.matrixbase import MatrixBase
from math import isqrt
import json, sys
sys.dont_write_bytecode = True

def in_K(M):
    return all(simplify(re(x)).is_Rational is True and simplify(im(x)).is_Rational is True for x in M)

def admit_stochastic(S):
    if not isinstance(S, MatrixBase) or S.rows < 1 or S.cols < 1:
        raise ValueError("positive stochastic dimensions required")
    if not all(x.is_Rational is True and x >= 0 for x in S):
        raise ValueError("nonnegative exact rational entries required")
    if any(sum(S[:,j]) != 1 for j in range(S.cols)):
        raise ValueError("column normalization required")


def E(d, j, k):
    return Matrix(d, d, lambda a, b: 1 if (a == j and b == k) else 0)

def Delta(X):
    return diag(*[X[j, j] for j in range(X.rows)])

def Ad(U):
    return lambda X: U * X * U.H

def Smat(Phi, d, e):
    """Classical kernel S[k,j] = Phi(E_jj)[k,k]."""
    return Matrix(e, d, lambda k, j: Phi(E(d, j, j))[k, k])

def kraus(L, d=None, e=None):
    if L:
        ee, dd = L[0].shape
        if any(K.shape != (ee, dd) or not in_K(K) for K in L):
            raise ValueError("Kraus shapes and Gaussian rational entries required")
        if (d is not None and d != dd) or (e is not None and e != ee):
            raise ValueError("declared Kraus dimensions mismatch")
        d, e = dd, ee
    if type(d) is not int or type(e) is not int or d < 1 or e < 1:
        raise ValueError("empty Kraus families require positive declared dimensions")
    def apply(X):
        if X.shape != (d, d): raise ValueError("input matrix shape mismatch")
        return sum((K * X * K.H for K in L), zeros(e, e))
    return apply

def choi(Phi, d):
    e = Phi(E(d, 0, 0)).rows
    J = zeros(d * e, d * e)
    for j in range(d):
        for k in range(d):
            blk = Phi(E(d, j, k))
            J[j * e:(j + 1) * e, k * e:(k + 1) * e] = blk
    return J

ok = True
checks = []
def check(name, cond):
    global ok
    if cond is None:
        passed = False
    else:
        try: passed = bool(cond)
        except TypeError: passed = False
    ok = ok and passed
    checks.append({"name": name, "passed": passed})
    print(("PASS " if passed else "FAIL ") + name)
    return passed

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

def lift(S):
    admit_stochastic(S)
    return lambda X: diag(*list(S * Matrix([X[j,j] for j in range(X.rows)])))


X = Matrix(3, 3, lambda a, b: Rational(a + 2 * b + 1, 7)) ; X = X + X.H

check("CC-28 functoriality E(TS) = E(T) o E(S)", lift(T * S)(X) == lift(T)(lift(S)(X)))
check("CC-28 E(I) = Delta", lift(eye(3))(X) == Delta(X))
def four_squares(n):
    """Exact finite search. Lagrange existence is imported; no practical runtime bound."""
    from itertools import product
    if isinstance(n, bool) or not isinstance(n, (int, Integer)) or n < 0:
        raise ValueError("nonnegative exact integer required")
    n = int(n)
    r = isqrt(n)
    for a,b,c,d in product(range(r+1), repeat=4):
        if a*a+b*b+c*c+d*d == n:
            return [x for x in (a,b,c,d) if x]
    raise RuntimeError("no four-square witness found")
def rational_lift_kraus(S):
    """Exact rational Kraus family for E(S): for s = p/q write pq = sum a_m^2, K = (a_m/q)|k><j|."""
    admit_stochastic(S)
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
print("   S7 Kraus weights:", [(str(K[0,0] or K[0,1] or K[1,0] or K[1,1])) for K in KR7], "count", len(KR7))  
# Input-first Choi order is |j><j| tensor |k><k| with coefficient S[k,j].
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
    if not isinstance(v, MatrixBase) or v.cols != 1 or v.rows < 1 or not in_K(v):
        raise ValueError("positive Gaussian rational column required")
    if simplify((v.H*v)[0] - 1) != 0:
        raise ValueError("unit norm required")
    n = v.rows
    e1 = Matrix(n,1,lambda a,b: 1 if a == 0 else 0)
    if v == e1: return eye(n)
    w = e1-v; c = 1-conjugate(v[0])
    if c == 0: raise ValueError("nontrivial unit-vector denominator cannot vanish")
    return simplify(eye(n)-w*w.H/c)
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
    if not isinstance(W, MatrixBase) or W.rows < W.cols or not in_K(W):
        raise ValueError("Gaussian rational isometry shape required")
    n,m = W.shape
    if simplify(W.H*W-eye(m)) != zeros(m,m):
        raise ValueError("orthonormal columns required")
    if m == 0: return eye(n)
    if n < 1: raise ValueError("positive row dimension required")
    U1 = house(W[:,0]); R = simplify(U1.H*W)
    check("CC-30 recursion first column, shape="+str(W.shape), simplify(R[:,0]-E(n,0,0)[:,0]) == zeros(n,1))
    check("CC-30 recursion remaining top row, shape="+str(W.shape), simplify(R[0,1:]) == zeros(1,m-1))
    Up = complete(R[1:,1:])
    return simplify(U1*diag(1,Up))
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


# ---------- independent boundary and complex/rectangular challenges ----------
def exact_hermitian_psd(M):
    """Finite Gaussian-rational PSD test via ALL principal minors, with Hermiticity."""
    from itertools import combinations
    if not isinstance(M, MatrixBase) or M.rows != M.cols or not in_K(M):
        raise ValueError("square Gaussian-rational matrix required")
    if simplify(M-M.H) != zeros(M.rows,M.cols): return False
    for k in range(1,M.rows+1):
        for ix in combinations(range(M.rows),k):
            val=simplify(M.extract(ix,ix).det())
            if val.is_Rational is not True or val < 0: return False
    return True
NH=Matrix([[1,1],[-1,1]])
check("CC-26 SymPy positivity may allow non-Hermitian input",NH.is_positive_semidefinite is True and NH.H != NH)
check("CC-26 exact Choi admission rejects non-Hermitian matrix",not exact_hermitian_psd(NH))
check("CC-26 exact Choi admission accepts singular Gram Choi",exact_hermitian_psd(choi(Ad(diag(1,Rational(1,2))),2)))
check("CC-26 exact PSD accepts zero and boundary",exact_hermitian_psd(zeros(2,2)) and exact_hermitian_psd(Matrix([[1,I],[-I,1]])))
check("CC-26 exact PSD rejects negative direction",not exact_hermitian_psd(diag(-1,1)))

for d in [1,2,3,4]:
    for j in range(d):
        for k in range(j+1,d):
            ej=E(d,j,j)[:,j];ek=E(d,k,k)[:,k]
            rp=(ej+ek)*(ej+ek).H/2;rm=(ej-I*ek)*(ej-I*ek).H/2
            check(f"CC-26 all-pair inversion d={d},j={j},k={k}", simplify(rp-I*rm-(1-I)*(E(d,j,j)+E(d,k,k))/2-E(d,j,k))==zeros(d,d))
check("CC-26 d=1 identity normalization", Ad(eye(1))(eye(1)).trace()==1)
Sinv=Smat(Ad(U.H),2,2)
check("CC-27 requested inverse failure", Smat(Ad(U.H*U),2,2)==eye(2) and Sinv*SU!=eye(2))
check("CC-28 Choi diagonal order is input then output", choi(lift(S),3)==diag(*[S[k,j] for j in range(3) for k in range(2)]))
check("CC-28 identity lift is not ambient identity", lift(eye(2))(E(2,0,1))==zeros(2,2) and E(2,0,1)!=zeros(2,2))
check("CC-28 identity lift is identity on diagonal algebra", lift(eye(2))(diag(2,3))==diag(2,3))
Nbig=10**400+10**200+7
Rbig=isqrt(Nbig)
check("integer sqrt bound for 401-digit input", Rbig*Rbig<=Nbig<(Rbig+1)*(Rbig+1))
for n in [0,1,2,3,7,42]:
    aa=four_squares(Integer(n))
    check("four-square exact witness n="+str(n),sum(a*a for a in aa)==n and len(aa)<=4)
# Positive dimensions, zero CP map and the identity/zero-column completion branches.
Zmap=kraus([],d=2,e=3)
check("typed empty Kraus family is 2-to-3 zero CP map", Zmap(eye(2))==zeros(3,3))
check("CC-30 e1 branch", house(Matrix([1,0,0]))==eye(3))
check("CC-30 n=d=1 phase completion", complete(Matrix([[I]]))==Matrix([[I]]))
check("CC-30 empty-column completion", complete(zeros(3,0))==eye(3))
for Wtest in [eye(1),eye(2),Matrix([[1],[0],[0]])]:
    UU=complete(Wtest)
    check("CC-30 identity/square/rectangular branches "+str(Wtest.shape),UU.H*UU==eye(Wtest.rows) and UU[:,:Wtest.cols]==Wtest)
Wrect=Matrix([[Rational(1,3),Rational(2,3)],[Rational(2,3),Rational(1,3)],[Rational(2,3),-Rational(2,3)]])*diag(1,I)
Krect=[Wrect];Lrect=[Matrix([[1,0,0],[0,1,0]]),Matrix([[0,0,1],[0,0,0]])]
G=Matrix([[3,4*I],[4*I,3]])/5
Lrect=[G*L for L in Lrect]
PhiR=kraus(Krect);PsiR=kraus(Lrect)
check("CC-29 rectangular complex channels normalized",sum((K.H*K for K in Krect),zeros(2,2))==eye(2) and sum((L.H*L for L in Lrect),zeros(3,3))==eye(3))
Achoi=choi(PhiR,2);Bchoi=choi(PsiR,3)
linkR=ptrace_middle(TP(Achoi,eye(2))*TP(eye(2),partial_T_first(Bchoi,3,2)),2,3,2)
directR=choi(lambda X:PsiR(PhiR(X)),2)
check("CC-29 complex rectangular link product",simplify(linkR-directR)==zeros(4,4))
wrongR=ptrace_middle(TP(Achoi,eye(2))*TP(eye(2),Bchoi),2,3,2)
check("CC-29 omitted partial transpose is detected",simplify(wrongR-directR)!=zeros(4,4))
# Independent component contraction, not the partial-trace implementation.
byindex=Matrix(4,4,lambda a,b:sum(Achoi[(a//2)*3+j,(b//2)*3+k]*Bchoi[j*2+a%2,k*2+b%2] for j in range(3) for k in range(3)))
check("CC-29 link agrees with explicit four-index contraction",simplify(byindex-directR)==zeros(4,4))
DP=dual(PhiR,2,3);DQ=dual(PsiR,3,2);DC=dual(lambda X:PsiR(PhiR(X)),2,2)
for a in range(2):
    for b in range(2):
        Y=E(2,a,b)
        check(f"CC-29 complex rectangular dual composition {a},{b}",simplify(DC(Y)-DP(DQ(Y)))==zeros(2,2))
X=Matrix([[1,I],[-I,2]]);Y=Matrix([[2,I,0],[-I,1,1],[0,1,3]])
check("CC-29 Hilbert-Schmidt adjoint identity",simplify((PhiR(X).H*Y).trace()-(X.H*DP(Y)).trace())==0)
# Rectangular tensor leg permutation, with genuinely complex entries.
Perm=perm_legs(2,3,2,2)
expected=Perm*TP(Achoi,choi(Ad(G),2))*Perm.T
tensorR=kraus([TP(Wrect,G)])
actual=choi(tensorR,4)
check("CC-29 complex rectangular tensor leg order",simplify(expected-actual)==zeros(24,24))
check("CC-29 omitted tensor permutation detected",TP(Achoi,choi(Ad(G),2))!=actual)
check("CC-30 complex rectangular completion", (lambda UU: simplify(UU.H*UU)==eye(3) and simplify(UU[:,:2]-Wrect)==zeros(3,2) and in_K(UU))(complete(Wrect)))
refusals=[]
def expect_refusal(name,fn):
    try: fn()
    except (ValueError,TypeError): refusals.append(name);check(name,True)
    else: check(name,False)
expect_refusal("reject nonunit vector",lambda:house(Matrix([2,0])))
expect_refusal("reject nonisometry",lambda:complete(Matrix([[1,1],[0,0]])))
expect_refusal("reject irrational vector entry",lambda:house(Matrix([sqrt(2)/2,sqrt(2)/2])))
expect_refusal("reject negative stochastic entry",lambda:rational_lift_kraus(Matrix([[2],[-1]])))
expect_refusal("reject unnormalized stochastic column",lambda:rational_lift_kraus(Matrix([[Rational(1,3)],[Rational(1,3)]])))
expect_refusal("reject float stochastic entry",lambda:rational_lift_kraus(Matrix([[Float('0.5')],[Float('0.5')]])))
expect_refusal("reject noninteger four-square input",lambda:four_squares(Rational(1,2)))
expect_refusal("reject untyped empty Kraus family",lambda:kraus([]))
expect_refusal("reject Kraus shape mismatch",lambda:kraus([eye(2),zeros(3,2)]))
print("\nALL PASS" if ok else "\nSOME FAILED")
print('REPLAY_JSON '+json.dumps({'scope':'Bounded exact rational/Gaussian-rational fixture replay; general mathematical proofs are separate, no Lean certificate.','checks':checks,'checks_passed':sum(x['passed'] for x in checks),'checks_failed':sum(not x['passed'] for x in checks),'invalid_inputs_rejected':refusals},sort_keys=True))
if not ok: raise SystemExit(1)
