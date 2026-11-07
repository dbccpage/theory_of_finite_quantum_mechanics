"""Independent check for DFM-Z1-Z2-COUNTERTERM-FENCE.

Recomputes the Dirac matrices, one inverse-propagator difference, and one
lowered vertex contraction with fractions.Fraction. This file imports no
repository code. It does not evaluate a counterterm ratio.
"""

from fractions import Fraction


def exact(value):
    if isinstance(value, Fraction):
        return value
    if type(value) is int:
        return Fraction(value)
    raise TypeError("expected an int or Fraction (not bool, float, or text)")


def g(re, im=0):
    return (exact(re), exact(im))


def add(a, b):
    return (a[0] + b[0], a[1] + b[1])


def sub(a, b):
    return (a[0] - b[0], a[1] - b[1])


def mul(a, b):
    return (a[0] * b[0] - a[1] * b[1], a[0] * b[1] + a[1] * b[0])


def scale(s, a):
    s = exact(s)
    return (s * a[0], s * a[1])


def madd(a, b):
    return [[add(a[i][j], b[i][j]) for j in range(4)] for i in range(4)]


def msub(a, b):
    return [[sub(a[i][j], b[i][j]) for j in range(4)] for i in range(4)]


def mscale(s, a):
    return [[scale(s, a[i][j]) for j in range(4)] for i in range(4)]


def mmul(a, b):
    zero = g(0)
    out = [[zero for _ in range(4)] for _ in range(4)]
    for i in range(4):
        for j in range(4):
            acc = zero
            for k in range(4):
                acc = add(acc, mul(a[i][k], b[k][j]))
            out[i][j] = acc
    return out


def zero_matrix():
    return [[g(0) for _ in range(4)] for _ in range(4)]


def eye():
    out = zero_matrix()
    for i in range(4):
        out[i][i] = g(1)
    return out


def g0():
    out = zero_matrix()
    out[0][0] = g(1)
    out[1][1] = g(1)
    out[2][2] = g(-1)
    out[3][3] = g(-1)
    return out


def g1():
    out = zero_matrix()
    out[0][3] = g(1)
    out[1][2] = g(1)
    out[2][1] = g(-1)
    out[3][0] = g(-1)
    return out


def g2():
    out = zero_matrix()
    out[0][3] = g(0, -1)
    out[1][2] = g(0, 1)
    out[2][1] = g(0, 1)
    out[3][0] = g(0, -1)
    return out


def g3():
    out = zero_matrix()
    out[0][2] = g(1)
    out[1][3] = g(-1)
    out[2][0] = g(-1)
    out[3][1] = g(1)
    return out


GAMMAS = (g0(), g1(), g2(), g3())
ETA = (Fraction(1), Fraction(-1), Fraction(-1), Fraction(-1))


def slash(v):
    out = mscale(v[0], GAMMAS[0])
    for j in range(1, 4):
        out = msub(out, mscale(v[j], GAMMAS[j]))
    return out


def prop_inv(v, mass):
    return msub(slash(v), mscale(mass, eye()))


def prop(v, mass):
    denom = v[0] * v[0] - v[1] * v[1] - v[2] * v[2] - v[3] * v[3] - mass * mass
    if denom == 0:
        raise SystemExit("singular propagator")
    return mscale(1 / denom, madd(slash(v), mscale(mass, eye())))


def dirac(matrix):
    acc = None
    for nu in range(4):
        term = mmul(GAMMAS[nu], mmul(matrix, mscale(ETA[nu], GAMMAS[nu])))
        acc = term if acc is None else madd(acc, term)
    return acc


def vertex(mu, left, right):
    acc = None
    for nu in range(4):
        term = mmul(
            GAMMAS[nu],
            mmul(left, mmul(GAMMAS[mu], mmul(right, mscale(ETA[nu], GAMMAS[nu])))),
        )
        acc = term if acc is None else madd(acc, term)
    return acc


def require(condition, message):
    if not condition:
        raise SystemExit(message)


def main():
    p = (exact(2), exact(0), exact(0), exact(0))
    q = (exact(1), exact(0), exact(0), exact(1))
    mass = exact(1)
    pq = tuple(p[i] + q[i] for i in range(4))
    require(msub(prop_inv(pq, mass), prop_inv(p, mass)) == slash(q), "inverse difference")
    sample_p = (exact(4), exact(-1), exact(2), exact(3))
    sample_q = (exact(-2), exact(5), exact(0), exact(1))
    sample_m = exact(6)
    sample_pq = tuple(sample_p[i] + sample_q[i] for i in range(4))
    require(
        msub(prop_inv(sample_pq, sample_m), prop_inv(sample_p, sample_m)) == slash(sample_q),
        "sample inverse difference",
    )
    sp = prop(p, mass)
    spq = prop(pq, mass)
    qslash = slash(q)
    require(mmul(spq, mmul(qslash, sp)) == msub(sp, spq), "sandwich")
    q_cov = (q[0], -q[1], -q[2], -q[3])
    contracted = None
    for mu in range(4):
        term = mscale(q_cov[mu], vertex(mu, spq, sp))
        contracted = term if contracted is None else madd(contracted, term)
    sigma = msub(dirac(sp), dirac(spq))
    require(contracted == sigma, "contraction")
    expected = zero_matrix()
    expected[0][0] = g(Fraction(2, 7))
    expected[0][2] = g(Fraction(-2, 7))
    expected[1][1] = g(Fraction(2, 7))
    expected[1][3] = g(Fraction(2, 7))
    expected[2][0] = g(Fraction(2, 7))
    expected[2][2] = g(Fraction(26, 21))
    expected[3][1] = g(Fraction(-2, 7))
    expected[3][3] = g(Fraction(26, 21))
    require(contracted == expected, "entries")
    print("inverse difference: slash(p+q)-mI minus slash(p)-mI equals slash(q)")
    print("at p=(2,0,0,0), q=(1,0,0,1), k=0, m=1 the contraction equals the witness")
    print("diagonal 2/7, 2/7, 26/21, 26/21")
    print("off-diagonal (0,2)=-2/7, (1,3)=2/7, (2,0)=2/7, (3,1)=-2/7")
    print("checked: sandwich, lowered contraction, witness entries; Z1/Z2 not computed")


if __name__ == "__main__":
    main()
