"""Finite quantum-to-classical descent fixtures. Python 3, standard library only.

All arithmetic is in Q(i). No repository imports, solvers, floats, or network.
Analytic proofs and physical assumptions are stated in the accompanying answer;
this checker verifies the explicit finite algebra, not those assumptions.
"""

from dataclasses import dataclass
from fractions import Fraction as F
from itertools import combinations, product

if not __debug__:
    raise RuntimeError("Run without -O: certificate assertions must remain enabled.")


@dataclass(frozen=True)
class C:
    re: F = F(0)
    im: F = F(0)

    def __post_init__(self):
        object.__setattr__(self, "re", F(self.re))
        object.__setattr__(self, "im", F(self.im))

    def __add__(self, other):
        other = c(other)
        return C(self.re + other.re, self.im + other.im)

    __radd__ = __add__

    def __neg__(self):
        return C(-self.re, -self.im)

    def __sub__(self, other):
        return self + -c(other)

    def __rsub__(self, other):
        return c(other) + -self

    def __mul__(self, other):
        other = c(other)
        return C(self.re * other.re - self.im * other.im, self.re * other.im + self.im * other.re)

    __rmul__ = __mul__

    def conj(self):
        return C(self.re, -self.im)

    def __truediv__(self, other):
        other = c(other)
        denom = other.re * other.re + other.im * other.im
        z = self * other.conj()
        return C(z.re / denom, z.im / denom)


def c(x):
    return x if isinstance(x, C) else C(x)


ZERO, ONE, II = C(), C(1), C(0, 1)


def mat(rows):
    return [[c(x) for x in row] for row in rows]


def eye(n):
    return mat([[int(i == j) for j in range(n)] for i in range(n)])


def zeros(m, n):
    return mat([[0] * n for _ in range(m)])


def add(A, B):
    return [[a + b for a, b in zip(x, y)] for x, y in zip(A, B)]


def scale(k, A):
    return [[c(k) * x for x in row] for row in A]


def mm(A, B):
    return [
        [sum((A[i][k] * B[k][j] for k in range(len(B))), ZERO) for j in range(len(B[0]))]
        for i in range(len(A))
    ]


def dag(A):
    return [[x.conj() for x in col] for col in zip(*A)]


def kron(A, B):
    return [[a * b for a in ar for b in br] for ar in A for br in B]


def trace(A):
    return sum((A[i][i] for i in range(len(A))), ZERO)


def real(x):
    assert x.im == 0
    return x.re


def ket(n, i):
    return mat([[int(j == i)] for j in range(n)])


def outer(v):
    return mm(v, dag(v))


def basis(A):
    """Nonzero RREF rows; exact field elimination."""
    A = [row[:] for row in A]
    r = 0
    for j in range(len(A[0])):
        pivot = next((i for i in range(r, len(A)) if A[i][j] != ZERO), None)
        if pivot is None:
            continue
        A[r], A[pivot] = A[pivot], A[r]
        d = A[r][j]
        A[r] = [x / d for x in A[r]]
        for i in range(len(A)):
            if i != r:
                d = A[i][j]
                A[i] = [x - d * y for x, y in zip(A[i], A[r])]
        r += 1
    return A[:r]


def rank(A):
    return len(basis(A))


def closure(Q, L):
    A = basis(Q)
    dimensions = [len(A)]
    while True:
        B = basis(A + mm(A, L))
        dimensions.append(len(B))
        if len(B) == len(A):
            return B, dimensions
        A = B


def psd(A):
    """Exact Hermitian Schur-complement test, including zero pivots."""
    assert A == dag(A)
    A = [row[:] for row in A]
    for i in range(len(A)):
        p = real(A[i][i])
        assert p >= 0
        if p == 0:
            assert all(A[j][i] == ZERO for j in range(i + 1, len(A)))
        else:
            for j in range(i + 1, len(A)):
                for k in range(i + 1, len(A)):
                    A[j][k] = A[j][k] - A[j][i] * A[i][k] / p


def density(A):
    psd(A)
    assert trace(A) == ONE


def ptrace(A, keep, n):
    bits = list(product((0, 1), repeat=n))
    result = zeros(2 ** len(keep), 2 ** len(keep))

    def index(b):
        return sum(b[k] << len(keep) - j - 1 for j, k in enumerate(keep))

    for i, bi in enumerate(bits):
        for j, bj in enumerate(bits):
            if all(bi[k] == bj[k] for k in range(n) if k not in keep):
                u, v = index(bi), index(bj)
                result[u][v] = result[u][v] + A[i][j]
    return result


# Paper 000 carrier and newly chosen observers.
D0 = mat([[-1, 0, 0], [-1, 0, 0]])
qp, qm = mat([[1, 1]]), mat([[1, -1]])
A = qp + qm
b, w = mat([[1], [1]]), mat([[1], [-1]])
assert rank(D0) == 1 and rank(A) == 2
assert mm(D0, mat([[-1], [0], [0]])) == b
assert mm(D0, mat([[0, 0], [1, 0], [0, 1]])) == zeros(2, 2)
assert mm(qp, w) == mat([[0]]) and mm(qm, b) == mat([[0]])
assert mm(qp, b) == mat([[2]]) and mm(qm, w) == mat([[2]])
assert rank(dag(b) + dag(w)) == 2
assert mm(dag(D0), w) == zeros(3, 1)  # dual annihilation
assert mm(dag(w), w) == mat([[2]])  # matching l1 lower bound
assert max(abs(real(x[0])) for x in w) == 1
assert sum(abs(real(x[0])) for x in w) == 2
assert mm(A, b) == mat([[2], [0]]) and mm(A, w) == mat([[0], [2]])
assert mm(scale(F(1, 2), A), A) == eye(2)
print("cochain: rank D0=1; Phi(b)=0; Phi(w)=2; completed constants=1,1")

# Hidden coherence and exact row closure.
L = mat([[0, 0, 0], [0, 0, -1], [0, 1, 0]])
Q = mat([[0, 0, 1]])
Ad = Q + mat([[0, 1, 0]])
M = mat([[0, 1], [-1, 0]])
v = mat([[0], [1], [0]])
assert mm(Q, v) == mat([[0]]) and mm(mm(Q, L), v) == mat([[1]])
assert mm(Ad, L) == mm(M, Ad)
closure_rows, dims = closure(Q, L)
assert dims == [1, 2, 2] and closure_rows == basis(Ad)
assert basis(Q + mm(Q, L) + mm(mm(Q, L), L)) == closure_rows
assert mm(mm(Q, L), L) == scale(-1, Q)
P = mat([[1, 0], [0, 0]])
lower = mat([[0, 0], [1, 0]])
upper = dag(lower)
assert mm(mm(P, lower), add(eye(2), scale(-1, P))) == zeros(2, 2)
assert mm(add(eye(2), scale(-1, P)), mm(lower, ket(2, 0))) == ket(2, 1)
assert mm(mm(P, upper), add(eye(2), scale(-1, P))) != zeros(2, 2)
assert mm(mm(P, upper), P) == zeros(2, 2)
badL = mat([[1, 0], [0, 2]])
assert mm(qm, mm(badL, b)) == mat([[-1]])  # repair space not invariant

I2 = eye(2)
X = mat([[0, 1], [1, 0]])
Y = mat([[0, -II], [II, 0]])
Z = mat([[1, 0], [0, -1]])
P0, P1 = outer(ket(2, 0)), outer(ket(2, 1))
H = scale(F(1, 2), X)


def comm(A, B):
    return add(mm(A, B), scale(-1, mm(B, A)))


def generator(R):
    return scale(-II, comm(H, R))


paulis = [X, Y, Z]
Lb = [[trace(mm(a, generator(scale(F(1, 2), b)))) for b in paulis] for a in paulis]
assert Lb == L
for sign in (1, -1):
    R = scale(F(1, 2), add(I2, scale(sign * F(3, 5), Y)))
    density(R)
    assert trace(mm(Z, R)) == ZERO
    assert trace(mm(Z, generator(R))) == c(sign * F(3, 5))
    # At t=pi/2, (I2-iX)/sqrt(2); the channel needs only Q(i).
    V = add(I2, scale(-II, X))
    Rt = scale(F(1, 2), mm(mm(V, R), dag(V)))
    assert trace(mm(Z, Rt)) == c(sign * F(3, 5))
assert comm(Y, Z) == scale(2 * II, X)


def flatten(A):
    return [x for row in A for x in row]


assert rank([flatten(I2), flatten(Z), flatten(Y)]) == 3
Khalf = mat([[F(1, 2), F(1, 2)], [F(1, 2), F(1, 2)]])
Kpi = X
assert mm(Khalf, Khalf) == Khalf and Khalf != Kpi
print("unitary fixture: derivatives +/-3/5; closure ranks=1,2,2; one new row")

# Open-system control: population generator and decaying coherences.
Jdown, Jup = mat([[0, 1], [0, 0]]), mat([[0, 0], [1, 0]])


def lindblad(R):
    result = zeros(2, 2)
    for rate, J in ((1, Jdown), (2, Jup)):
        E = mm(dag(J), J)
        term = add(mm(mm(J, R), dag(J)), scale(F(-1, 2), add(mm(E, R), mm(R, E))))
        result = add(result, scale(rate, term))
    return result


G = mat([[-2, 1], [2, -1]])
for i, j in product(range(2), repeat=2):
    Eij = mm(ket(2, i), dag(ket(2, j)))
    out = lindblad(Eij)
    assert mat([[out[0][0]], [out[1][1]]]) == mm(G, mat([[Eij[0][0]], [Eij[1][1]]]))
    if i != j:
        assert out == scale(F(-3, 2), Eij)
stationary = mat([[F(1, 3)], [F(2, 3)]])
assert mm(G, stationary) == zeros(2, 1)
assert mm(mat([[1, 1]]), G) == zeros(1, 2)
Pi = mat([[F(1, 3), F(1, 3)], [F(2, 3), F(2, 3)]])
assert mm(Pi, Pi) == Pi and G == scale(-3, add(I2, scale(-1, Pi)))
print("open fixture: G=[[-2,1],[2,-1]]; stationary=(1/3,2/3)")


# Three-qubit measurement unitary, instrument, and all proper reductions.
def cnot(control, target):
    U = zeros(8, 8)
    for j in range(8):
        out = j ^ ((1 << (2 - target)) if j & (1 << (2 - control)) else 0)
        U[out][j] = ONE
    return U


U = mm(cnot(1, 2), cnot(0, 1))
permutation = [0, 1, 3, 2, 7, 6, 4, 5]
assert all(mm(U, ket(8, j)) == ket(8, k) for j, k in enumerate(permutation))
assert mm(dag(U), U) == eye(8)
initial = add(scale(F(3, 5), ket(8, 0)), scale(F(4, 5), ket(8, 4)))
psi = add(scale(F(3, 5), ket(8, 0)), scale(F(4, 5), ket(8, 7)))
assert mm(U, initial) == psi
rho = outer(psi)
sigma = add(scale(F(9, 25), outer(ket(8, 0))), scale(F(16, 25), outer(ket(8, 7))))
pointer = [kron(kron(I2, p), I2) for p in (P0, P1)]
assert add(*pointer) == eye(8)
W = [list(row) for row in zip([r[0] for r in ket(8, 0)], [r[0] for r in ket(8, 7)])]
Ks = [mm(p, W) for p in pointer]
assert add(*(mm(dag(k), k) for k in Ks)) == I2
for i, j in product(range(2), repeat=2):
    assert mm(pointer[i], pointer[j]) == (pointer[i] if i == j else zeros(8, 8))
assert [real(trace(mm(p, rho))) for p in pointer] == [F(9, 25), F(16, 25)]
assert add(*(mm(mm(p, rho), p) for p in pointer)) == sigma
for size in range(3):
    for keep in combinations(range(3), size):
        assert ptrace(rho, keep, 3) == ptrace(sigma, keep, 3)
        density(ptrace(rho, keep, 3))
for R in (rho, sigma):
    density(R)
XXX = kron(kron(X, X), X)
assert trace(mm(rho, XXX)) == c(F(24, 25))
assert trace(mm(sigma, XXX)) == ZERO
diff = add(rho, scale(-1, sigma))
for sign in (1, -1):
    vector = add(ket(8, 0), scale(sign, ket(8, 7)))
    assert mm(diff, vector) == scale(sign * F(12, 25), vector)
assert all(mm(diff, ket(8, j)) == zeros(8, 1) for j in range(1, 7))
SA = ptrace(rho, (0, 1), 3)
prodSA = kron(ptrace(rho, (0,), 3), ptrace(rho, (1,), 3))
residual = add(SA, scale(-1, prodSA))
assert [real(residual[j][j]) for j in range(4)] == [F(144, 625) * s for s in (1, -1, -1, 1)]
assert all(residual[i][j] == ZERO for i in range(4) for j in range(4) if i != j)
assert sum(abs(real(residual[j][j])) for j in range(4)) == F(576, 625)
assert rank([flatten(pointer[0]), flatten(pointer[1])]) == 2
print("measurement: p=(9/25,16/25); D(rho,sigma)=12/25; SA defect=576/625")

# Bell table and Farkas dual; no numerical feasibility solver.
bellvec = add(ket(4, 0), ket(4, 3))
bell = scale(F(1, 2), outer(bellvec))
density(bell)
alice = [Z, X]
bob = [
    scale(F(1, 5), add(scale(4, Z), scale(3, X))),
    scale(F(1, 5), add(scale(4, Z), scale(-3, X))),
]
for observable in alice + bob:
    assert dag(observable) == observable and mm(observable, observable) == I2
contexts = list(product(range(2), repeat=2))
outcomes = list(product((1, -1), repeat=2))
tables = []
for x, y in contexts:
    table = []
    for a, bval in outcomes:
        effect = kron(
            scale(F(1, 2), add(I2, scale(a, alice[x]))),
            scale(F(1, 2), add(I2, scale(bval, bob[y]))),
        )
        psd(effect)
        table.append(real(trace(mm(bell, effect))))
    assert sum(table) == 1 and min(table) >= 0
    assert table[0] + table[1] == table[2] + table[3] == F(1, 2)
    assert table[0] + table[2] == table[1] + table[3] == F(1, 2)
    tables.append(table)
assert tables == [[F(9, 20), F(1, 20), F(1, 20), F(9, 20)]] * 2 + [
    [F(2, 5), F(1, 10), F(1, 10), F(2, 5)],
    [F(1, 10), F(2, 5), F(2, 5), F(1, 10)],
]
correlations = [sum(a * bval * p for (a, bval), p in zip(outcomes, t)) for t in tables]
assert correlations == [F(4, 5), F(4, 5), F(3, 5), F(-3, 5)]
assert sum(s * e for s, e in zip((1, 1, 1, -1), correlations)) == F(14, 5)
assignments = list(product((1, -1), repeat=4))
Marg = mat(
    [
        [int(lam[x] == a and lam[2 + y] == bval) for lam in assignments]
        for x, y in contexts
        for a, bval in outcomes
    ]
)
tvec = mat([[p] for tab in tables for p in tab])
dual = mat(
    [
        [F(1, 2) - (1 if (x, y) != (1, 1) else -1) * a * bval]
        for x, y in contexts
        for a, bval in outcomes
    ]
)
assert set(real(row[0]) for row in mm(dag(Marg), dual)) == {F(0), F(4)}
assert mm(dag(dual), tvec) == mat([[F(-4, 5)]])
signed = mat(
    [
        [(1 + F(4, 5) * a0 * b0 + F(4, 5) * a0 * b1 + F(3, 5) * a1 * b0 - F(3, 5) * a1 * b1) / 16]
        for a0, a1, b0, b1 in assignments
    ]
)
assert mm(Marg, signed) == tvec
assert min(real(row[0]) for row in signed) == F(-3, 80)
print("Bell: S=14/5; dual transpose entries={0,4}; dual objective=-4/5")

# Triangle, binary correction, and the physical-star configuration loop.
triangle = mat([[-1, 1, 0], [0, -1, 1], [1, 0, -1]])
trial = mm(triangle, mat([[0], [1], [0]]))
assert trial == mat([[1], [-1], [0]])
assert sum(real(row[0]) for row in trial) == 0
assert sum(abs(real(row[0])) for row in trial) == 2
assert rank(triangle) == 2
Bbinary = {(0, 0, 0), (1, 1, 0)}


def syndrome(e):
    return e[0] ^ e[1]


def xor(e, f):
    return tuple(a ^ bval for a, bval in zip(e, f))


Egood = [(0, 0, 0), (1, 0, 0)]
Ebad = [(0, 0, 0), (0, 0, 1)]


def criterion(E):
    return all(syndrome(e) != syndrome(f) or xor(e, f) in Bbinary for e in E for f in E)


assert criterion(Egood) and not criterion(Ebad)
assert all(xor(e, Egood[syndrome(e)]) in Bbinary for e in Egood)
loop = [{1, 2}, {0, 2}, {2, 3}, {0, 3}, {1, 3}, {0, 1}, {1, 2}]
parities = []
for before, after in zip(loop, loop[1:]):
    (src,) = before - after
    (dst,) = after - before
    assert 0 in (src, dst)
    parities.append(sum(min(src, dst) < j < max(src, dst) for j in before) % 2)
assert parities == [0, 1, 0, 0, 1, 1] and sum(parities) % 2 == 1
print("other carriers: triangle raw=2, quotient=0; binary correction controls; odd star loop")
print("PASS: explicit finite certificates, using exact Q(i) arithmetic.")
print(
    "Not checked by this program: analytic all-time proofs, Lieb-Robinson premises, hardware, or Lean."
)
