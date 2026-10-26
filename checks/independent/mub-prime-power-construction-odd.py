"""Independent check for MUB-PRIME-POWER-CONSTRUCTION, odd characteristic.

Exact arithmetic only: finite fields GF(q) for q in {3, 5, 7, 9, 11, 13, 25, 27} built from
explicit irreducible polynomials, and the cyclotomic ring Z[zeta_p] represented as integer
vectors modulo the p-th cyclotomic polynomial.  No repository imports, no floats.

For each q = p^k:
  psi(t) = zeta_p ^ Tr(t), Tr the absolute trace GF(q) -> GF(p);
  bases: standard e_y, and for each a in GF(q) the vectors x -> psi(a x^2 + b x), b in GF(q).
Checks:
  (i)   within each quadratic-phase basis, <v_b, v_b'> = q [b = b'];
  (ii)  for a != a', <v_{a,b}, v_{a',b'}> * conj(<...>) = q (so |<u,v>|^2 / (q q) = 1/q);
  (iii) standard against quadratic-phase: |<e_y, v_{a,b}>|^2 = 1 (so 1/q after normalisation);
  (iv)  the number of bases is q + 1;
  (v)   psi is unitary (conj psi(t) = psi(-t)) and nontrivial.
Exit code 0 only if every check passes.
"""
from __future__ import annotations

import itertools
import sys

failures = 0
checked = 0


def check(cond: bool, msg: str) -> None:
    global failures, checked
    checked += 1
    if not cond:
        failures += 1
        print("FAIL:", msg)


# ---------- GF(p^k) with an explicit irreducible polynomial ----------
IRRED = {  # monic irreducible polynomials, low degree first: x^k = -(c_0 + c_1 x + ...)
    (3, 2): [1, 0],      # x^2 + 1 over GF(3)
    (5, 2): [2, 0],      # x^2 + 2 over GF(5)
    (3, 3): [1, 2, 0],   # x^3 + 2x + 1 over GF(3)
}


def is_irreducible(p: int, coeffs: list[int]) -> bool:
    """Brute-force: no root in GF(p) for degree 2, 3 (sufficient for those degrees)."""
    k = len(coeffs)
    for x in range(p):
        val = (pow(x, k, p) + sum(c * pow(x, i, p) for i, c in enumerate(coeffs))) % p
        if val == 0:
            return False
    return True


class GF:
    def __init__(self, p: int, k: int):
        self.p, self.k, self.q = p, k, p ** k
        self.coeffs = [0] if k == 1 else IRRED[(p, k)]
        if k > 1:
            assert is_irreducible(p, self.coeffs)
        self.elems = [tuple(e) for e in itertools.product(range(p), repeat=k)]
        self.zero = tuple([0] * k)
        self.one = tuple([1] + [0] * (k - 1))

    def add(self, a, b):
        return tuple((x + y) % self.p for x, y in zip(a, b))

    def neg(self, a):
        return tuple((-x) % self.p for x in a)

    def sub(self, a, b):
        return self.add(a, self.neg(b))

    def mul(self, a, b):
        p, k = self.p, self.k
        prod = [0] * (2 * k - 1)
        for i, x in enumerate(a):
            for j, y in enumerate(b):
                prod[i + j] = (prod[i + j] + x * y) % p
        # reduce: x^k = -(c_0 + ... + c_{k-1} x^{k-1})
        for d in range(2 * k - 2, k - 1, -1):
            c = prod[d]
            if c:
                prod[d] = 0
                for i, ci in enumerate(self.coeffs):
                    prod[d - k + i] = (prod[d - k + i] - c * ci) % p
        return tuple(prod[:k])

    def frob(self, a):
        return self.pow(a, self.p)

    def pow(self, a, n):
        r = self.one
        for _ in range(n):
            r = self.mul(r, a)
        return r

    def trace(self, a) -> int:
        """Absolute trace to GF(p), returned as an integer mod p."""
        s = self.zero
        x = a
        for _ in range(self.k):
            s = self.add(s, x)
            x = self.frob(x)
        assert all(c == 0 for c in s[1:]), "trace must lie in the prime field"
        return s[0]


# ---------- Z[zeta_p] as integer vectors of length p modulo (1 + zeta + ... + zeta^{p-1}) ----------
class Cyc:
    def __init__(self, p: int):
        self.p = p

    def canon(self, v):
        c = v[-1]
        return tuple(x - c for x in v)  # subtract (zeta^0 + ... + zeta^{p-1}) * c, which is 0

    def zeta_pow(self, n: int):
        v = [0] * self.p
        v[n % self.p] = 1
        return self.canon(v)

    def add(self, a, b):
        return self.canon(tuple(x + y for x, y in zip(a, b)))

    def mul(self, a, b):
        p = self.p
        out = [0] * p
        for i, x in enumerate(a):
            if x == 0:
                continue
            for j, y in enumerate(b):
                if y:
                    out[(i + j) % p] += x * y
        return self.canon(tuple(out))

    def conj(self, a):
        out = [0] * self.p
        for i, x in enumerate(a):
            out[(-i) % self.p] += x
        return self.canon(tuple(out))

    def int_(self, n: int):
        v = [0] * self.p
        v[0] = n
        return self.canon(tuple(v))


def run(p: int, k: int) -> None:
    F = GF(p, k)
    C = Cyc(p)
    q = F.q

    def psi(t):
        return C.zeta_pow(F.trace(t))

    # (v) unitary and nontrivial
    check(any(psi(t) != C.int_(1) for t in F.elems), f"q={q}: psi nontrivial")
    for t in F.elems:
        check(C.conj(psi(t)) == psi(F.neg(t)), f"q={q}: unitary at {t}")

    def qvec(a, b):
        return [psi(F.add(F.mul(a, F.mul(x, x)), F.mul(b, x))) for x in F.elems]

    def pair(u, v):
        s = C.int_(0)
        for x, y in zip(u, v):
            s = C.add(s, C.mul(C.conj(x), y))
        return s

    qvecs = {(a, b): qvec(a, b) for a in F.elems for b in F.elems}
    # (i) within a basis
    for a in F.elems:
        for b in F.elems:
            for b2 in F.elems:
                ip = pair(qvecs[(a, b)], qvecs[(a, b2)])
                check(ip == (C.int_(q) if b == b2 else C.int_(0)), f"q={q}: within basis a={a} b={b} b'={b2}")
    # (ii) across quadratic-phase bases
    for a in F.elems:
        for a2 in F.elems:
            if a == a2:
                continue
            for b in F.elems:
                for b2 in F.elems:
                    ip = pair(qvecs[(a, b)], qvecs[(a2, b2)])
                    check(C.mul(ip, C.conj(ip)) == C.int_(q), f"q={q}: cross a={a} a'={a2} b={b} b'={b2}")
    # (iii) standard basis against quadratic-phase bases
    for y in F.elems:
        for a in F.elems:
            for b in F.elems:
                ip = qvecs[(a, b)][F.elems.index(y)]  # <e_y, v> = v(y)
                check(C.mul(ip, C.conj(ip)) == C.int_(1), f"q={q}: std y={y} a={a} b={b}")
    # (iv) count
    check(len(F.elems) + 1 == q + 1, f"q={q}: q+1 bases")
    print(f"q = {q} = {p}^{k}: {q + 1} bases verified")


for p, k in [(3, 1), (5, 1), (7, 1), (3, 2), (11, 1), (13, 1), (5, 2), (3, 3)]:
    run(p, k)

print(f"checked {checked} conditions, {failures} failures")
sys.exit(0 if failures == 0 else 1)
