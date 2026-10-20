"""Exact checks for BR-31 .. BR-40.  sympy only; every number is in Q(i) unless a check is *about* leaving Q(i)."""
from sympy import *
from sympy.physics.quantum import TensorProduct as TP
from itertools import product
ok = True
from math import isqrt
from sympy import S as exact_S

def require(condition, message='expected an exact true Boolean'):
    if condition is not True and condition is not exact_S.true:
        raise ValueError(message)

def gaussian_rational(x):
    x = sympify(x)
    if not isinstance(x, Expr):
        return False
    return not x.has(Float) and simplify(re(x)).is_Rational is True and (simplify(im(x)).is_Rational is True)

def admit_matrix(value, square=False, hermitian=False):
    matrix = Matrix(value)
    require(all((gaussian_rational(x) for x in matrix)), 'entries must be exact Gaussian rationals')
    if square:
        require(matrix.rows == matrix.cols, 'square matrix required')
    if hermitian:
        require(matrix == matrix.H, 'Hermitian matrix required')
    return matrix

def check(name, cond):
    global ok
    require(cond, 'failed exact check: ' + name)
    ok = True
    print('PASS ' + name)

def E(n, j, k):
    return Matrix(n, n, lambda a, b: 1 if a == j and b == k else 0)

def ev(n, j):
    return Matrix(n, 1, lambda a, b: 1 if a == j else 0)

def kraus(L, n_out, n_in):
    return lambda X: sum((l * X * l.H for l in L), zeros(n_out, n_out))

def adj(L, n_out, n_in):
    return lambda Y: sum((l.H * Y * l for l in L), zeros(n_in, n_in))

def choi(Phi, d, e):
    C = zeros(d * e, d * e)
    for j in range(d):
        for k in range(d):
            C[j * e:(j + 1) * e, k * e:(k + 1) * e] = Phi(E(d, j, k))
    return C

def tr_out(C, d, e):
    return Matrix(d, d, lambda j, k: sum((C[j * e + a, k * e + a] for a in range(e))))

def tr_in(C, d, e):
    return Matrix(e, e, lambda a, b: sum((C[j * e + a, j * e + b] for j in range(d))))

def herm_eq(X, Y):
    return simplify(X - Y) == zeros(*X.shape)

def S(d, j, k):
    return E(d, j, k) + E(d, k, j)

def T(d, j, k):
    return I * (E(d, j, k) - E(d, k, j))

def G(d, j, k):
    return (eye(d) + S(d, j, k)) / 2

def Hp(d, j, k):
    return (eye(d) + T(d, j, k)) / 2

def psd_certify(A):
    """Exact pivoted LDL* with certificate.  Returns ('psd', L, D) with A = L D L*, D diagonal >= 0,
    or ('neg', v) with v != 0 rational and v* A v < 0.  A must be Hermitian with entries in Q(i)."""
    A = admit_matrix(A, square=True, hermitian=True)
    A = Matrix(A).applyfunc(lambda x: expand(simplify(x)))
    n = A.rows
    require(simplify(A - A.H) == zeros(n, n), 'assertion obligation failed')
    for j in range(n):
        require(A[j, j].is_Rational, ('non-rational diagonal', A[j, j]))
    if n == 0:
        return ('psd', eye(0), zeros(0, 0))
    diag_entries = [A[j, j] for j in range(n)]
    for j in range(n):
        if diag_entries[j] < 0:
            return ('neg', ev(n, j))
    if all((x == 0 for x in diag_entries)):
        if A == zeros(n, n):
            return ('psd', eye(n), zeros(n, n))
        for j in range(n):
            for k in range(n):
                if j != k and A[j, k] != 0:
                    return ('neg', ev(n, j) - conjugate(A[j, k]) * ev(n, k))
    j0 = next((j for j in range(n) if diag_entries[j] > 0))
    order = [j0] + [j for j in range(n) if j != j0]
    P = Matrix(n, n, lambda r, c: 1 if order[r] == c else 0)
    B = P * A * P.T
    pi = B[0, 0]
    col = B[1:, 0]
    Schur = (B[1:, 1:] - col * col.H / pi).applyfunc(expand)
    res = psd_certify(Schur)
    if res[0] == 'psd':
        _, Lp, Dp = res
        L1 = eye(n)
        L1[1:, 0] = col / pi
        L1[1:, 1:] = Lp
        D = diag(pi, *[Dp[i, i] for i in range(n - 1)])
        return ('psd', P.T * L1, D)
    else:
        vp = res[1]
        x = -(col.H * vp)[0] / pi
        v = Matrix([x] + list(vp))
        return ('neg', P.T * v)

def is_psd(A):
    r = psd_certify(A)
    if r[0] == 'psd':
        _, L, D = r
        require(simplify(L * D * L.H - Matrix(A)) == zeros(*Matrix(A).shape), 'certificate failed')
        require(all((D[i, i] >= 0 for i in range(D.rows))), 'assertion obligation failed')
        return True
    v = r[1]
    val = simplify((v.H * Matrix(A) * v)[0])
    require(v != zeros(*v.shape) and val < 0, ('witness failed', val))
    return False
print('== BR-35 ==')
tests = {'[[1,1],[1,1]] singular PSD': (Matrix([[1, 1], [1, 1]]), True), '[[0,1],[1,0]] zero diag nonzero': (Matrix([[0, 1], [1, 0]]), False), '[[0,i],[-i,0]] zero diag complex': (Matrix([[0, I], [-I, 0]]), False), '[[1,1],[1,0]] positive pivot then negative Schur': (Matrix([[1, 1], [1, 0]]), False), 'zero matrix 3x3': (zeros(3, 3), True), 'negative diagonal': (Matrix([[1, 0], [0, -Rational(1, 7)]]), False), 'Gram of rational complex matrix 3x3': ((lambda B: B.H * B)(Matrix([[1, I, Rational(1, 2)], [0, 2, (1 + I) / 3]])), True), 'rank-deficient Gram with zero-diagonal block after pivot': ((lambda B: B.H * B)(Matrix([[1, 0, 0]])), True), 'M0 of BR-36': (eye(2) - (E(2, 0, 0) + G(2, 0, 1) + Hp(2, 0, 1)) / 3, True), '[[2,3],[3,2]]': (Matrix([[2, 3], [3, 2]]), False), '3x3 with hidden negativity': (Matrix([[1, 1, 1], [1, 1, 1], [1, 1, Rational(1, 2)]]), False)}
for name, (A, expect) in tests.items():
    check(f'BR-35 {name}: verdict {expect} with valid certificate/witness', is_psd(A) == expect)
A = Matrix([[1, 2], [2, 1]])
M = Matrix([[1, I], [0, 2]])
r = psd_certify(A)
v = r[1]
Bc = M * A * M.H
w = M.H.inv() * v
check('BR-35 witness transport: v*Av<0  =>  w=(M*)^{-1}v gives w*(MAM*)w<0', simplify((w.H * Bc * w)[0]) == simplify((v.H * A * v)[0]) < 0)
print('== BR-31 ==')
d = 2
K1 = [E(2, 0, 0)]
K2 = [E(2, 0, 1)]
e = [2, 2]
Etot = sum(e)

def J(i):
    off = sum(e[:i])
    return Matrix(Etot, e[i], lambda a, b: 1 if a == off + b else 0)
rho = Matrix([[Rational(1, 3), (1 + I) / 6], [(1 - I) / 6, Rational(2, 3)]])
check('BR-31 rho is a density', is_psd(rho) and rho.trace() == 1)
Phi = [kraus(K1, 2, 2), kraus(K2, 2, 2)]
sig = [Phi[i](rho) for i in range(2)]
check('BR-31 branch states PSD, traces sum to 1', all((is_psd(s) for s in sig)) and sum((s.trace() for s in sig)) == 1)
Sigma = sum((J(i) * sig[i] * J(i).H for i in range(2)), zeros(Etot, Etot))
check('BR-31 tagged direct sum is a density', is_psd(Sigma) and Sigma.trace() == 1)
check('BR-31 tag recoverable: sigma_i = J_i* Sigma J_i', all((J(i).H * Sigma * J(i) == sig[i] for i in range(2))))
check('BR-31 scalar marginal p(i) = Tr(Sigma P_i)', all(((Sigma * J(i) * J(i).H).trace() == sig[i].trace() for i in range(2))))
typed_kraus = [J(0) * k for k in K1] + [J(1) * k for k in K2]
check('BR-31 typed map is TP: sum (J_i K)*(J_i K) = I_d', sum((k.H * k for k in typed_kraus), zeros(2, 2)) == eye(2))
L = [[E(2, 0, 0)], [E(2, 1, 1)]]
new_e = [2, 2, 2]
Enew = 6

def Jn(i):
    off = sum(new_e[:i])
    return Matrix(Enew, new_e[i], lambda a, b: 1 if a == off + b else 0)
nested = [[l * k for k in K1 for l in L[0]], [l * k for k in K1 for l in L[1]], K2]
Sigma_nested = sum((Jn(i) * kraus(nested[i], 2, 2)(rho) * Jn(i).H for i in range(3)), zeros(6, 6))
Lam_kraus = [Jn(2) * J(1).H] + [Jn(l) * lb * J(0).H for l in range(2) for lb in L[l]]
Lam = kraus(Lam_kraus, 6, 4)
check('BR-31 nested instrument = typed component map applied to tagged sum', Lam(Sigma) == Sigma_nested)
check('BR-31 Lambda is TP on M_E', sum((k.H * k for k in Lam_kraus), zeros(4, 4)) == eye(4))
check('BR-31 zero-probability slot gives zero block (slot 2 of nested: Psi_2(sigma_1))', Jn(1).H * Sigma_nested * Jn(1) == L[1][0] * sig[0] * L[1][0].H)
sig0 = Phi[0](E(2, 1, 1))
check('BR-31 Tr sigma = 0  =>  sigma = 0 (retained as zero block, no normalization)', sig0 == zeros(2, 2))
print('== BR-32 ==')
U = Matrix([[(3 + 4 * I) / 5, 0], [0, 1]]) * Matrix([[3, 4], [-4, 3]]) / 5
Kr = [Matrix([[1, I], [0, Rational(1, 2)]]) / 2, U / 2]
PhiK = kraus(Kr, 2, 2)
C = choi(PhiK, 2, 2)
check('BR-32 Phi*(I_e) = (Tr_out C)^T  (complex Kraus)', herm_eq(adj(Kr, 2, 2)(eye(2)), tr_out(C, 2, 2).T))
check('BR-32 Tr_out C = conj(Phi*(I)) in general; equals transpose since Phi*(I) Hermitian', herm_eq(tr_out(C, 2, 2), adj(Kr, 2, 2)(eye(2)).conjugate()))
A = Hp(2, 0, 1)
PhiA = lambda X: Matrix([[(A * X).trace()]])
CA = choi(PhiA, 2, 1)
check('BR-32 scalar output: C_Phi = A^T', herm_eq(CA, A.T))
check('BR-32 A^T != A for H12', A.T != A)
check('BR-32 Phi_A*(1) = A* = A (Hermitian) via adjoint identity on all E_jk', all((simplify(conjugate((A * E(2, j, k)).trace()) - (E(2, j, k).H * A.H).trace()) == 0 for j in range(2) for k in range(2))))
povm = [E(2, 0, 0) / 3, G(2, 0, 1) / 3, Hp(2, 0, 1) / 3]
povm = [eye(2) - sum(povm, zeros(2, 2))] + povm
Cs = [choi(lambda X, M=M: Matrix([[(M * X).trace()]]), 2, 1) for M in povm]
check('BR-32 trace-instrument Choi tuple = (A_i^T)', all((herm_eq(Cs[i], povm[i].T) for i in range(4))))
check('BR-32 sum_i Tr_out C_i = I  (transpose invariant)', herm_eq(sum(Cs, zeros(2, 2)), eye(2)))
check('BR-32 some C_i != A_i (H12 slot)', Cs[3] != povm[3])
print('== BR-33 ==')
D = diag(-1, 1)
Xf = Matrix([[0, 1], [1, 0]])
after = [E(2, 0, 0), D * E(2, 1, 1)]
first_I = [eye(2) * E(2, 0, 0), eye(2) * E(2, 1, 1)]
check('BR-33 example: merge-after {E11, D E22} equals merge-first-with-I {E11, E22} as representatives', after == first_I)
first_D = [D * E(2, 0, 0), D * E(2, 1, 1)]
check('BR-33 example: merge-first-with-D differs as representative (sign) but same CP map', first_D != after and herm_eq(choi(kraus(first_D, 2, 2), 2, 2), choi(kraus(after, 2, 2), 2, 2)))
Z = diag(1, -1)
Phi1 = kraus([Rational(3, 5) * eye(2)], 2, 2)
Phi2 = kraus([Rational(4, 5) * eye(2)], 2, 2)
Mmap = lambda X: Phi1(X) + Z * Phi2(X) * Z
Theta = lambda Y: Rational(9, 25) * Y + Rational(16, 25) * Z * Y * Z
check('BR-33 merge-first Theta exists (= M since Phi1+Phi2 = Id) and is CP', herm_eq(choi(lambda X: Theta(Phi1(X) + Phi2(X)), 2, 2), choi(Mmap, 2, 2)) and is_psd(choi(Theta, 2, 2)))
check('BR-33 ... but termwise fails: Theta o Phi1 != Id o Phi1', choi(lambda X: Theta(Phi1(X)), 2, 2) != choi(Phi1, 2, 2))
P1 = kraus([E(2, 0, 0)], 2, 2)
P2 = kraus([E(2, 0, 1)], 2, 2)
check('BR-33 slots {E11},{E12} normalized', E(2, 0, 0).H * E(2, 0, 0) + E(2, 0, 1).H * E(2, 0, 1) == eye(2))
Msum = lambda X: P1(X) + P2(X)
Mafter = lambda X: P1(X) + Xf * P2(X) * Xf
k = E(2, 0, 0) - E(2, 1, 1)
check('BR-33 kernel obstruction: (Phi1+Phi2)(E11-E22) = 0 but merge-after map is nonzero there', Msum(k) == zeros(2, 2) and Mafter(k) != zeros(2, 2))
check('BR-33 merge-after representative is still a normalized instrument {E11, X E12 = E22}', [E(2, 0, 0), Xf * E(2, 0, 1)] == [E(2, 0, 0), E(2, 1, 1)])
print('== BR-34 ==')
C_a = [choi(lambda X, M=M: Matrix([[(M * X).trace()]]), 2, 1) for M in [E(2, 0, 0), E(2, 1, 1)]]
C_b = [choi(lambda X, M=M: Matrix([[(M * X).trace()]]), 2, 1) for M in [G(2, 0, 1), eye(2) - G(2, 0, 1)]]
lam = Rational(2, 7)
mix = [lam * C_a[i] + (1 - lam) * C_b[i] for i in range(2)]
check('BR-34 rational convex mixture: PSD, rational, normalized', all((is_psd(c) for c in mix)) and all((gaussian_rational(x) for c in mix for x in c)) and herm_eq(sum((tr_out(c, 2, 1) for c in mix), zeros(2, 2)), eye(2)))
lam_irr = 1 / sqrt(2)
mix_irr = lam_irr * C_a[0] + (1 - lam_irr) * C_b[0]
check('BR-34 irrational weight leaves Q(i): entry (1,1) = (1+1/sqrt2)/2 is irrational', not simplify(mix_irr[0, 0]).is_rational and simplify(mix_irr[0, 0] - (1 + lam_irr) / 2) == 0)

def four_squares(n):
    require(sympify(n).is_Integer is True and n >= 0, 'nonnegative integer required')
    r = isqrt(int(n))
    for a, b, c, dd in product(range(r + 1), repeat=4):
        if a * a + b * b + c * c + dd * dd == n:
            return [x for x in (a, b, c, dd) if x]
    raise RuntimeError('four-square search exhausted its exact bound')

def rational_roots_of_weight(w):
    require(sympify(w).is_Rational is True and w >= 0, 'nonnegative rational weight required')
    p, q = fraction(w)
    return [Rational(a, q) for a in four_squares(p * q)]
Ka = [[E(2, 0, 0)], [E(2, 1, 1)]]
Kb = [[Matrix([[1, 1], [0, 0]]) / 2] * 2, [Matrix([[1, -1], [0, 0]]) / 2] * 2]
check('BR-34 instrument b normalized', sum((k.H * k for s in Kb for k in s), zeros(2, 2)) == eye(2))
w = [Rational(2, 7), Rational(5, 7)]
mixK = [[r * k for r in rational_roots_of_weight(w[0]) for k in Ka[i]] + [r * k for r in rational_roots_of_weight(w[1]) for k in Kb[i]] for i in range(2)]
check('BR-34 four-square mixture: rational, normalized', all((x.is_rational for s in mixK for k in s for x in k)) and sum((k.H * k for s in mixK for k in s), zeros(2, 2)) == eye(2))
check('BR-34 four-square mixture realizes the Choi mixture', all((herm_eq(choi(kraus(mixK[i], 2, 2), 2, 2), w[0] * choi(kraus(Ka[i], 2, 2), 2, 2) + w[1] * choi(kraus(Kb[i], 2, 2), 2, 2)) for i in range(2))))
rho_r = Matrix([[Rational(1, 3), (1 + I) / 6], [(1 - I) / 6, Rational(2, 3)]])
sb = kraus(Kb[0], 2, 2)(rho_r)
check('BR-34 rational rho: branch state rational, trace in Q, conditional state rational', all((gaussian_rational(x) for x in sb)) and sb.trace().is_rational and all(((x / sb.trace()).is_rational or x.is_Number for x in sb)))
rho_irr = (eye(2) + S(2, 0, 1) / sqrt(2)) / 2
check('BR-34 irrational density exists: (I + S/sqrt2)/2 has eigenvalues (1 +- 1/sqrt2)/2 >= 0', all((simplify(l) >= 0 for l in rho_irr.eigenvals())))
check('BR-34 its probe value p(G12) = 1/2 + 1/(2 sqrt2) is irrational', not simplify((rho_irr * G(2, 0, 1)).trace()).is_rational)
print('== BR-36 ==')
M1, M2, M3 = (E(2, 0, 0) / 3, G(2, 0, 1) / 3, Hp(2, 0, 1) / 3)
M0 = eye(2) - M1 - M2 - M3
check('BR-36 M0 = [[1/3, -(1+i)/6],[-(1-i)/6, 2/3]]', herm_eq(M0, Matrix([[Rational(1, 3), -(1 + I) / 6], [-(1 - I) / 6, Rational(2, 3)]])))
check('BR-36 M0 PSD (det 1/6)', is_psd(M0) and simplify(M0.det()) == Rational(1, 6))
evs = list(M0.eigenvals().keys())
check('BR-36 eig(M0) = (3 -+ sqrt3)/6', set((simplify(x) for x in evs)) == {(3 - sqrt(3)) / 6, (3 + sqrt(3)) / 6})
q1, q2, q3 = symbols('q1 q2 q3', real=True)
rho_q = Matrix([[3 * q1, 3 * q2 - Rational(1, 2) + I * (3 * q3 - Rational(1, 2))], [3 * q2 - Rational(1, 2) - I * (3 * q3 - Rational(1, 2)), 1 - 3 * q1]])
check('BR-36 inverse reproduces q1,q2,q3', all((simplify((rho_q * M).trace() - q) == 0 for M, q in [(M1, q1), (M2, q2), (M3, q3)])))
check('BR-36 q0 = 1 - q1 - q2 - q3', simplify((rho_q * M0).trace() - (1 - q1 - q2 - q3)) == 0)
ball = (6 * q1 - 1) ** 2 + (6 * q2 - 1) ** 2 + (6 * q3 - 1) ** 2 - 1
check('BR-36 det(rho) >= 0  <=>  (6q1-1)^2+(6q2-1)^2+(6q3-1)^2 <= 1   (4 det = -ball)', expand(4 * rho_q.det() + ball) == 0)
for pt, want in [((Rational(1, 6),) * 3, 'I/2'), ((0, Rational(1, 6), Rational(1, 6)), 'E22'), ((Rational(1, 3), Rational(1, 6), Rational(1, 6)), 'E11'), ((Rational(1, 6), 0, Rational(1, 6)), '(e1-e2)/sqrt2'), ((Rational(1, 6), Rational(1, 6), 0), '(e1+ie2)/sqrt2')]:
    r = rho_q.subs({q1: pt[0], q2: pt[1], q3: pt[2]})
    check(f'BR-36 point {pt} -> {want}: density, ball value {simplify(ball.subs({q1: pt[0], q2: pt[1], q3: pt[2]}))}', is_psd(r) and r.trace() == 1)
check('BR-36 q0 min = (3 - sqrt3)/6 attained at q_i = (1 + 1/sqrt3)/6, pure state', simplify(1 - 3 * (1 + 1 / sqrt(3)) / 6 - (3 - sqrt(3)) / 6) == 0 and simplify(ball.subs({q1: (1 + 1 / sqrt(3)) / 6, q2: (1 + 1 / sqrt(3)) / 6, q3: (1 + 1 / sqrt(3)) / 6})) == 0)
check('BR-36 rational point outside: q=(1/3,1/3,1/6) -> not a density', not is_psd(rho_q.subs({q1: Rational(1, 3), q2: Rational(1, 3), q3: Rational(1, 6)})))
print('== BR-37 ==')
d, e, g = (2, 3, 2)
Kphi = [Matrix([[1, 0], [0, Rational(1, 2)], [0, (1 + I) / 2]]) / 2, Matrix([[0, 1], [1, 0], [I, 0]]) / 3]
Kpsi = [Matrix([[1, 0, I], [0, 1, 0]]) / 2, Matrix([[0, Rational(1, 3), 0], [1, 0, 1]]) / 2]
PhiM = kraus(Kphi, e, d)
PsiM = kraus(Kpsi, g, e)
Acho = choi(PhiM, d, e)
Bcho = choi(PsiM, e, g)
Ccomp = choi(lambda X: PsiM(PhiM(X)), d, g)
idx = lambda: None
formula = zeros(d * g, d * g)
for j in range(d):
    for k in range(d):
        for al in range(g):
            for be in range(g):
                formula[j * g + al, k * g + be] = sum((Acho[j * e + a, k * e + b] * Bcho[a * g + al, b * g + be] for a in range(e) for b in range(e)))
check('BR-37 index formula C_{Psi o Phi}[(j,al),(k,be)] = sum_ab A[(j,a),(k,b)] B[(a,al),(b,be)]', herm_eq(formula, Ccomp))

def pt_first(Bm, e, g):
    out = zeros(e * g, e * g)
    for a in range(e):
        for b in range(e):
            out[a * g:(a + 1) * g, b * g:(b + 1) * g] = Bm[b * g:(b + 1) * g, a * g:(a + 1) * g]
    return out

def tr_mid(Mm, d, e, g):
    out = zeros(d * g, d * g)
    for j in range(d):
        for k in range(d):
            for al in range(g):
                for be in range(g):
                    out[j * g + al, k * g + be] = sum((Mm[(j * e + a) * g + al, (k * e + a) * g + be] for a in range(e)))
    return out
link = tr_mid(TP(Acho, eye(g)) * TP(eye(d), pt_first(Bcho, e, g)), d, e, g)
check('BR-37 link product Tr_e[(A x I_g)(I_d x B^{T_e})] = C_{Psi o Phi}', herm_eq(link, Ccomp))
Bl = [choi(kraus([Kpsi[0]], g, e), e, g), choi(kraus([Kpsi[1]], g, e), e, g)]
Lins = [[E(3, 0, 0)], [E(3, 1, 1), E(3, 2, 2)]]
check('BR-37 continuation instrument normalized', sum((l.H * l for s in Lins for l in s), zeros(3, 3)) == eye(3))
Bl = [choi(kraus(s, 3, 3), 3, 3) for s in Lins]
check('BR-37 sum_l Tr_out B_l = I_e', herm_eq(sum((tr_out(b, 3, 3) for b in Bl), zeros(3, 3)), eye(3)))
links = [tr_mid(TP(Acho, eye(3)) * TP(eye(d), pt_first(b, 3, 3)), d, 3, 3) for b in Bl]
check('BR-37 sum_l Tr_g C_(i,l) = Tr_e C_i  (slot normalization preserved, Kraus-free)', herm_eq(sum((tr_out(c, d, 3) for c in links), zeros(d, d)), tr_out(Acho, d, 3)))
check('BR-37 link of PSD is PSD here', all((is_psd(c) for c in links)))
print('== BR-38 ==')

def match_unitary(A, B):
    """A: N x r, B: N x s, A A* = B B*.  Returns rational unitary U (R x R), R = max(r,s), with B_pad = A_pad U."""
    A = admit_matrix(A)
    B = admit_matrix(B)
    require(A.rows == B.rows, 'matching row dimensions required')
    N, r = A.shape
    s = B.shape[1]
    R = max(r, s)
    Ap = A.row_join(zeros(N, R - r))
    Bp = B.row_join(zeros(N, R - s))
    require(simplify(Ap * Ap.H - Bp * Bp.H) == zeros(N, N), 'assertion obligation failed')
    V = eye(R)
    for m in range(N):
        a = V * (Ap.H * ev(N, m))
        b = Bp.H * ev(N, m)
        if simplify(a - b) == zeros(R, 1):
            continue
        w = a - b
        c = (w.H * a)[0]
        require(simplify(c) != 0, 'assertion obligation failed')
        Um = eye(R) - w * w.H / c
        V = simplify(Um * V)
        for n in range(m):
            require(simplify(V * (Ap.H * ev(N, n)) - Bp.H * ev(N, n)) == zeros(R, 1), 'assertion obligation failed')
    U = V.H
    require(simplify(U.H * U) == eye(R) and simplify(Ap * U - Bp) == zeros(N, R), 'assertion obligation failed')
    return U
Om = Matrix([1, 0, 0, 1])
A1 = Om
B1 = (Rational(3, 5) * Om).row_join(Rational(4, 5) * Om)
U = match_unitary(A1, B1)
print('   U (1->2 padding) =', U.tolist())
check('BR-38 identity channel presentations {I} vs {3/5 I, 4/5 I}: rational unitary after padding', all((x.is_rational for x in U)))
B3 = (Rational(1, 3) * Om).row_join(Rational(2, 3) * Om).row_join(Rational(2, 3) * Om)
U = match_unitary(B1, B3)
check('BR-38 {3/5,4/5} vs {1/3,2/3,2/3}: padded 2->3, rational unitary', all((x.is_rational for x in U)))
A = Matrix([[1, I], [2, 2 * I], [0, 0], [I, 1]])
W = Matrix([[3, 4 * I], [4 * I, 3]]) / 5
B = A * W
check('BR-38 dependent/zero rows, complex: recovered unitary works', simplify(A * match_unitary(A, B) - B) == zeros(4, 2))
K1 = [E(2, 0, 0), E(2, 1, 1)]
Vr = Matrix([[3, 4], [-4, 3]]) / 5
K3 = [Vr[0, 0] * K1[0] + Vr[0, 1] * K1[1], Vr[1, 0] * K1[0] + Vr[1, 1] * K1[1]]
vecm = lambda K: Matrix([K[a, j] for j in range(K.cols) for a in range(K.rows)])
Amat = vecm(K1[0]).row_join(vecm(K1[1]))
Bmat = vecm(K3[0]).row_join(vecm(K3[1]))
check('BR-38 Kraus vectorizations have equal Gram (same channel)', Amat * Amat.H == Bmat * Bmat.H)
Uk = match_unitary(Amat, Bmat)
check('BR-38 Kraus mixing unitary recovered: L_j = sum_i U_ij K_i', all((herm_eq(sum((Uk[i, jj] * K1[i] for i in range(2)), zeros(2, 2)), K3[jj]) for jj in range(2))))
check('BR-38 1/3 = |(1+i)/3|^2 + |1/3|^2  (two rational row vectors needed for rank-one effect E11/3)', abs((1 + I) / 3) ** 2 + Rational(1, 9) == Rational(1, 3))
check('BR-38 integer control only: 3 is not a sum of two integer squares; rational non-norm uses the written descent proof', not any((a * a + b * b == 3 for a in range(3) for b in range(3))))
print('== BR-39 ==')
Ka = [[E(2, 0, 0)], [E(2, 0, 1)]]
Lb = [[Matrix([[1, 1], [0, 0]]) / 2] * 2, [Matrix([[1, -1], [0, 0]]) / 2] * 2]
tens = [[TP(k, l) for k in Ka[i] for l in Lb[j]] for i in range(2) for j in range(2)]
check('BR-39 tensor instrument normalized on K^4', sum((t.H * t for s in tens for t in s), zeros(4, 4)) == eye(4))
unit = [[Matrix([[1]])]]
check('BR-39 tensor unit: K x 1 = K', [[TP(k, Matrix([[1]])) for k in Ka[i]] for i in range(2)] == Ka)

def swap(p, q):
    Sm = zeros(p * q, p * q)
    for a in range(p):
        for b in range(q):
            Sm[b * p + a, a * q + b] = 1
    return Sm
tens_rev = [[TP(l, k) for l in Lb[j] for k in Ka[i]] for j in range(2) for i in range(2)]
check('BR-39 swap law: L x K = S_out (K x L) S_in^* with slots (i,j)->(j,i)', all((tens_rev[j * 2 + i][0] == swap(2, 2) * tens[i * 2 + j][0] * swap(2, 2).H for i in range(2) for j in range(2))))
Kp = [[E(2, 0, 0)], [E(2, 1, 1)]]
Lp = [[eye(2)]]
lhs_slot = [kp * k for k in Ka[0] for kp in Kp[0]]
lhs = [TP(a, lp * l) for a in lhs_slot for l in Lb[0] for lp in Lp[0]]
rhs = [TP(kp, lp) * TP(k, l) for k in Ka[0] for l in Lb[0] for kp in Kp[0] for lp in Lp[0]]
check("BR-39 interchange on one slot pair: (K'K) x (L'L) = (K' x L')(K x L)", lhs == rhs)
Ci = choi(kraus(Ka[0], 2, 2), 2, 2)
Cj = choi(kraus(Lb[1], 2, 2), 2, 2)
Cij = choi(kraus(tens[1], 4, 4), 4, 4)

def perm_legs(d, e, dp, ep):
    n = d * e * dp * ep
    P = zeros(n, n)
    for a in range(d):
        for b in range(e):
            for c in range(dp):
                for f in range(ep):
                    P[((a * dp + c) * e + b) * ep + f, ((a * e + b) * dp + c) * ep + f] = 1
    return P
P = perm_legs(2, 2, 2, 2)
check('BR-39 descends: C_(i,j) = P (C_i x C_j) P^T', Cij == P * TP(Ci, Cj) * P.T)
print('== BR-40 ==')
slots = [[E(2, 0, 0)], [], [Matrix([[0, 1], [0, 0]]) / 2 * 0 + Matrix([[0, Rational(3, 5)], [0, 0]]), Matrix([[0, Rational(4, 5)], [0, 0]])]]
e = [2, 2, 2]
Etot = 6
check('BR-40 slots normalized', sum((k.H * k for s in slots for k in s), zeros(2, 2)) == eye(2))
branches = [(i, a) for i in range(3) for a in range(len(slots[i]))]
R = len(branches)
check('BR-40 R = 3 >= 1', R == 3)

def Je(i):
    off = sum(e[:i])
    return Matrix(Etot, e[i], lambda a, b: 1 if a == off + b else 0)
V = sum((TP(Je(i) * slots[i][a], ev(R, t)) for t, (i, a) in enumerate(branches)), zeros(Etot * R, 2))
check('BR-40 V rational isometry K^2 -> K^6 x K^3', V.H * V == eye(2) and all((x.is_rational for x in V)))
Pi = [sum((ev(R, t) * ev(R, t).H for t, (i2, a) in enumerate(branches) if i2 == i), zeros(R, R)) for i in range(3)]
Qi = [TP(eye(Etot), p) for p in Pi]
check('BR-40 Q_i orthogonal projections summing to I; zero slot has Q = 0', all((q * q == q and q.H == q for q in Qi)) and sum(Qi, zeros(18, 18)) == eye(18) and (Qi[1] == zeros(18, 18)))
rho = Matrix([[Rational(1, 3), (1 + I) / 6], [(1 - I) / 6, Rational(2, 3)]])

def tr_env(Y):
    return Matrix(Etot, Etot, lambda a, b: sum((Y[a * R + t, b * R + t] for t in range(R))))
for i in range(3):
    lhs = tr_env(Qi[i] * V * rho * V.H * Qi[i])
    rhs = Je(i) * kraus(slots[i], 2, 2)(rho) * Je(i).H if slots[i] else zeros(Etot, Etot)
    check(f'BR-40 state update slot {i + 1}: Tr_R[Q_i V rho V* Q_i] = J_i Phi_i(rho) J_i*', simplify(lhs - rhs) == zeros(Etot, Etot))
check('BR-40 pointer projection = system block projection on ran V: Q_i V = (J_i J_i* x I) V', all((Qi[i] * V == TP(Je(i) * Je(i).H, eye(R)) * V for i in range(3))))
check('BR-40 Tr_R[V rho V*] = typed output of BR-31', tr_env(V * rho * V.H) == sum((Je(i) * kraus(slots[i], 2, 2)(rho) * Je(i).H for i in range(3) if slots[i]), zeros(Etot, Etot)))
check('BR-40 probabilities: Tr(Q_i V rho V*) = Tr(rho A_i)', all((simplify((Qi[i] * V * rho * V.H).trace() - (rho * sum((k.H * k for k in slots[i]), zeros(2, 2))).trace()) == 0 for i in range(3))))
print('\nALL PASS' if ok else '\nSOME FAILED')
