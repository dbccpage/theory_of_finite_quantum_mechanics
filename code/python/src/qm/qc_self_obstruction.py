"""Exact rational replay of the self-obstruction analysis of reliable quantum computation.

Replays in exact arithmetic (fractions, no floating point) the finite statements that the Lean modules
QcConcatenation, QcRepairQueue, QcEntropySink and QcSelfObstruction (lean4/) prove in general, on
declared families and instances; the Rust twin is code/rust/src/qm/campaigns/qc_self_obstruction.rs.

* Q2: the concatenation recurrence p_{k+1} = c p_k^2, its closed form c p_k = (c p_0)^(2^k), the
  three regimes (below, at, above the threshold 1/c) and explicit crossing levels.
* Q3: the level-dependent overhead c_k, the amplification amp (amp_0 = 1, amp_{k+1} = c_k amp_k^2),
  p_k = p_0^(2^k) amp_k, the bound witness amp_k <= M^(2^k), the at-most-exponential family
  c_k <= A 2^(k+1), the polynomial family (k+1)^2 and the double exponential family a b^(2^k) whose
  amplification escapes every bound.
* Q1: the repair backlog q_{t+1} = max(0, q_t + lam + g mu - mu) and the fresh-supply threshold.
* Q4: depolarizing noise on rational Bloch vectors and 2x2 Gaussian-rational density matrices; the
  squared Bloch distance contracts by (1 - p)^2 per noisy rotation, and (Pauli part)^2 = |v|^2 1.
* Q6 support: a finite fresh-mark budget bounds the number of rounds.

Every function checks a declared finite instance. A passing check is not a proof of the general
statement; the general statements are the kernel-checked Lean theorems. No claim about any physical
device is made. AuthorityEffect: None.
"""
from fractions import Fraction as Q

AUTHORITY_EFFECT = "AuthorityEffect: None"
FENCE = ("Finite exact replay on declared instances; not a proof of the general statements; "
         "no claim about physical hardware; the threshold theorem and the Aharonov-Ben-Or-"
         "Impagliazzo-Nisan 1996 theorem are cited literature, not imported as proof.")


def _q(x):
    """Admit an exact rational (int or Fraction); refuse floats and bools."""
    if type(x) is bool or type(x) is float:
        raise ValueError("exact rational required (no bool or float)")
    if type(x) is int or isinstance(x, Q):
        return Q(x)
    raise ValueError("exact rational required")


def _levels(n):
    if type(n) is not int or n < 0:
        raise ValueError("a nonnegative integer level count is required")
    return n


# ----------------------------------------------------------------------------- Q2: constant overhead
def conc(c, p, k):
    """Level-k error of p_{k+1} = c p_k^2 started at p_0 = p."""
    c, p, k = _q(c), _q(p), _levels(k)
    x = p
    for _ in range(k):
        x = c * x * x
    return x


def conc_closed_holds(c, p, k):
    """c * p_k == (c p_0)^(2^k), the exact closed form (Lean: conc_closed)."""
    c, p, k = _q(c), _q(p), _levels(k)
    return c * conc(c, p, k) == (c * p) ** (2 ** k)


def classify(c, p):
    """'below' | 'fixed' | 'above' according to c p_0 versus 1 (requires c > 0, p >= 0)."""
    c, p = _q(c), _q(p)
    if c <= 0 or p < 0:
        raise ValueError("c > 0 and p >= 0 are required")
    r = c * p
    return "below" if r < 1 else ("fixed" if r == 1 else "above")


def threshold(c):
    """The certified threshold 1 / c for the recurrence p_{k+1} = c p_k^2."""
    c = _q(c)
    if c <= 0:
        raise ValueError("c > 0 is required")
    return 1 / c


def first_level_below(c, p, eps, max_levels=16):
    """Smallest k <= max_levels with p_k < eps, else None (exact)."""
    c, p, eps = _q(c), _q(p), _q(eps)
    if eps <= 0:
        raise ValueError("eps > 0 is required")
    x = p
    for k in range(max_levels + 1):
        if x < eps:
            return k
        x = c * x * x
    return None


def first_level_above(c, p, big, max_levels=16):
    """Smallest k <= max_levels with p_k > big, else None (exact)."""
    c, p, big = _q(c), _q(p), _q(big)
    x = p
    for k in range(max_levels + 1):
        if x > big:
            return k
        x = c * x * x
    return None


def half_bound_holds(c, p, k):
    """If c p_0 <= 1/2 then p_k <= (1/2)^(2^k) / c (Lean: sub_half_bound)."""
    c, p, k = _q(c), _q(p), _levels(k)
    if c <= 0 or p < 0 or c * p > Q(1, 2):
        raise ValueError("requires c > 0, p >= 0, c p <= 1/2")
    return conc(c, p, k) <= Q(1, 2) ** (2 ** k) / c


def linear_level(a, p, k):
    """Level-k error of the unrepaired union bound p_{k+1} = a p_k (Lean: lin_closed, a^k p)."""
    a, p, k = _q(a), _q(p), _levels(k)
    x = p
    for _ in range(k):
        x = a * x
    return x


def pair_count(a):
    """Unordered pairs among a fault locations: the constant c of a distance-three level."""
    if type(a) is not int or a < 0:
        raise ValueError("a nonnegative integer location count is required")
    return Q(a * (a - 1), 2)


# ----------------------------------------------------------------------------- Q3: level-dependent
def amp(cs, k):
    """amp_0 = 1, amp_{k+1} = c_k amp_k^2 for the overhead list cs = [c_0, c_1, ...]."""
    cs = [_q(c) for c in cs]
    k = _levels(k)
    if k > len(cs):
        raise ValueError("not enough overheads supplied")
    x = Q(1)
    for j in range(k):
        x = cs[j] * x * x
    return x


def concv(cs, p, k):
    """Level-k error of p_{k+1} = c_k p_k^2."""
    cs = [_q(c) for c in cs]
    p, k = _q(p), _levels(k)
    if k > len(cs):
        raise ValueError("not enough overheads supplied")
    x = p
    for j in range(k):
        x = cs[j] * x * x
    return x


def concv_amp_holds(cs, p, k):
    """p_k == p^(2^k) amp_k (Lean: concv_eq_amp)."""
    return concv(cs, p, k) == _q(p) ** (2 ** k) * amp(cs, k)


def amp_bound_holds(cs, M):
    """amp_k <= M^(2^k) for every k up to len(cs): a finite witness for AmpBounded."""
    M = _q(M)
    if M <= 0:
        raise ValueError("M > 0 is required")
    return all(amp(cs, k) <= M ** (2 ** k) for k in range(len(cs) + 1))


def amp_escape_level(cs, M):
    """Smallest k <= len(cs) with amp_k > M^(2^k) (a finite refutation of that M), else None."""
    M = _q(M)
    if M <= 0:
        raise ValueError("M > 0 is required")
    for k in range(len(cs) + 1):
        if amp(cs, k) > M ** (2 ** k):
            return k
    return None


def const_family(c, n):
    return [_q(c)] * _levels(n)


def geom_family(A, B, n):
    """c_k = A B^(k+1) (geometric growth of the overhead)."""
    A, B = _q(A), _q(B)
    return [A * B ** (k + 1) for k in range(_levels(n))]


def exp_family(A, n):
    """c_k = A 2^(k+1): the geometric family with B = 2."""
    return geom_family(A, 2, n)


def poly_family(n):
    """c_k = (k+1)^2."""
    return [Q((k + 1) ** 2) for k in range(_levels(n))]


def dexp_family(a, b, n):
    """c_k = a b^(2^k)."""
    a, b = _q(a), _q(b)
    return [a * b ** (2 ** k) for k in range(_levels(n))]


def const_invariant_holds(cs, C):
    """amp_k * max(C,1) <= max(C,1)^(2^k) when every c_k <= C (Lean: amp_le_of_bounded)."""
    C = _q(C)
    D = max(C, Q(1))
    cs = [_q(c) for c in cs]
    if any(c < 0 or c > C for c in cs):
        raise ValueError("requires 0 <= c_k <= C")
    return all(amp(cs, k) * D <= D ** (2 ** k) for k in range(len(cs) + 1))


def geom_invariant_holds(A, B, n):
    """amp_k * (A B^(k+2)) <= (A B^2)^(2^k) for c_k = A B^(k+1) (Lean: amp_le_of_geom)."""
    A, B = _q(A), _q(B)
    cs = geom_family(A, B, n)
    return all(amp(cs, k) * (A * B ** (k + 2)) <= (A * B * B) ** (2 ** k) for k in range(len(cs) + 1))


def exp_invariant_holds(A, n):
    """The geometric invariant with B = 2: amp_k * (A 2^(k+2)) <= (4A)^(2^k)."""
    return geom_invariant_holds(A, 2, n)


def size_family(a, b, sizes):
    """c_k = a b^(N_k) for block sizes N_k (the overhead exponential in the level-k block size)."""
    a, b = _q(a), _q(b)
    if any(type(x) is not int or x < 0 for x in sizes):
        raise ValueError("nonnegative integer block sizes are required")
    return [a * b ** x for x in sizes]


def block_exp(sizes):
    """E_0 = 0, E_{k+1} = 2 E_k + N_k, the exponent of b in amp (Lean: blockExp)."""
    out = [0]
    for x in sizes:
        out.append(2 * out[-1] + x)
    return out


def block_exp_bound_holds(sizes, s):
    """E_k + N_k/(2-s) <= 2^k N_0/(2-s) when N_{k+1} <= s N_k with s < 2 (Lean: blockExp_le)."""
    s = _q(s)
    if s >= 2:
        raise ValueError("s < 2 is required")
    if any(sizes[k + 1] > s * sizes[k] for k in range(len(sizes) - 1)):
        raise ValueError("block sizes must satisfy N_{k+1} <= s N_k")
    E = block_exp(sizes)
    return all(E[k] + Q(sizes[k]) / (2 - s) <= 2 ** k * Q(sizes[0]) / (2 - s)
               for k in range(len(sizes)))


def dexp_square_identity_holds(a, b, n):
    """(amp_k a)^2 == (a^2 b^k)^(2^k) for c_k = a b^(2^k) (Lean: amp_dexp_sq)."""
    a, b = _q(a), _q(b)
    cs = dexp_family(a, b, n)
    return all((amp(cs, k) * a) ** 2 == (a * a * b ** k) ** (2 ** k) for k in range(len(cs) + 1))


# ----------------------------------------------------------------------------- Q1: repair backlog
def backlog(lam, g, mu, q0, steps):
    """Backlog trajectory [q_0, ..., q_steps] of q_{t+1} = max(0, q_t + lam + g mu - mu)."""
    lam, g, mu, q0 = _q(lam), _q(g), _q(mu), _q(q0)
    steps = _levels(steps)
    if q0 < 0:
        raise ValueError("q0 >= 0 is required")
    out = [q0]
    for _ in range(steps):
        out.append(max(Q(0), out[-1] + lam + g * mu - mu))
    return out


def drift(lam, g, mu):
    return _q(lam) + _q(g) * _q(mu) - _q(mu)


def backlog_bounded_decision(lam, g, mu):
    """The Lean criterion: bounded iff lam <= (1 - g) mu (exact)."""
    lam, g, mu = _q(lam), _q(g), _q(mu)
    return lam <= (1 - g) * mu


def supply_threshold(lam, g, kappa):
    """Least fresh supply r with lam <= (1 - g) kappa r; requires g < 1 and kappa > 0."""
    lam, g, kappa = _q(lam), _q(g), _q(kappa)
    if g >= 1 or kappa <= 0:
        raise ValueError("requires g < 1 and kappa > 0 (otherwise no supply suffices)")
    return lam / ((1 - g) * kappa)


def rounds_upper_bound(budget, rmin):
    """Rounds completed with a total of budget fresh marks, at least rmin per round."""
    budget, rmin = _q(budget), _q(rmin)
    if rmin <= 0:
        raise ValueError("rmin > 0 is required")
    return budget / rmin


# ----------------------------------------------------------------------------- Q4: depolarizing decay
def bloch_dot(u, v):
    return sum((a * b for a, b in zip(u, v)), Q(0))


def bloch_sq_dist(r, s):
    d = [_q(a) - _q(b) for a, b in zip(r, s)]
    return bloch_dot(d, d)


def mat_vec(R, v):
    return [sum((R[i][j] * v[j] for j in range(3)), Q(0)) for i in range(3)]


def is_rational_rotation(R):
    """R^T R == 1 exactly (a rational orthogonal matrix)."""
    return all(sum((R[k][i] * R[k][j] for k in range(3)), Q(0)) == (1 if i == j else 0)
               for i in range(3) for j in range(3))


def rot_z(c, s):
    """Rotation about z by an angle with rational cos c and sin s (c^2 + s^2 = 1 required)."""
    c, s = _q(c), _q(s)
    if c * c + s * s != 1:
        raise ValueError("c^2 + s^2 = 1 is required")
    return [[c, -s, Q(0)], [s, c, Q(0)], [Q(0), Q(0), Q(1)]]


def rot_x(c, s):
    c, s = _q(c), _q(s)
    if c * c + s * s != 1:
        raise ValueError("c^2 + s^2 = 1 is required")
    return [[Q(1), Q(0), Q(0)], [Q(0), c, -s], [Q(0), s, c]]


def bloch_step(p, R, r):
    """Rotate then depolarize: r -> (1 - p) R r."""
    p = _q(p)
    if not is_rational_rotation(R):
        raise ValueError("a rational rotation is required")
    return [(1 - p) * x for x in mat_vec(R, [_q(a) for a in r])]


def bloch_run(history, r):
    """history = [(p_i, R_i), ...]."""
    for p, R in history:
        r = bloch_step(p, R, r)
    return r


def contraction_factor_sq(history):
    """prod (1 - p_i)^2."""
    out = Q(1)
    for p, _ in history:
        out *= (1 - _q(p)) ** 2
    return out


def decay_identity_holds(history, r, s):
    """sqDist(run r, run s) == prod (1 - p_i)^2 sqDist(r, s) (Lean: sqDist_runB)."""
    return bloch_sq_dist(bloch_run(history, r), bloch_run(history, s)) == \
        contraction_factor_sq(history) * bloch_sq_dist(r, s)


def decay_le_inv_holds(p, t):
    """(1 - p)^t <= 1 / (1 + p t) for 0 <= p <= 1 (Lean: decay_le_inv)."""
    p, t = _q(p), _levels(t)
    if not (0 <= p <= 1):
        raise ValueError("0 <= p <= 1 is required")
    return (1 - p) ** t <= 1 / (1 + p * t)


def depth_until_below(p, delta, max_depth=100000):
    """Smallest t with (1 - p)^t <= delta (exact); None past max_depth. Requires 0 < p < 1."""
    p, delta = _q(p), _q(delta)
    if not (0 < p < 1) or delta <= 0:
        raise ValueError("0 < p < 1 and delta > 0 are required")
    x, t = Q(1), 0
    while x > delta:
        t += 1
        if t > max_depth:
            return None
        x *= 1 - p
    return t


# 2x2 Gaussian-rational density matrices: entries are (re, im) pairs of Fractions.
def _cmul(a, b):
    return (a[0] * b[0] - a[1] * b[1], a[0] * b[1] + a[1] * b[0])


def _cadd(a, b):
    return (a[0] + b[0], a[1] + b[1])


def _cconj(a):
    return (a[0], -a[1])


def mat2_mul(A, B):
    return [[_cadd(_cmul(A[i][0], B[0][j]), _cmul(A[i][1], B[1][j])) for j in range(2)]
            for i in range(2)]


def mat2_dagger(A):
    return [[_cconj(A[j][i]) for j in range(2)] for i in range(2)]


def bloch_matrix(r):
    """rho(r) = (1 + r . sigma) / 2 with exact Gaussian-rational entries."""
    x, y, z = (_q(a) for a in r)
    h = Q(1, 2)
    return [[((1 + z) * h, Q(0)), (x * h, -y * h)],
            [(x * h, y * h), ((1 - z) * h, Q(0))]]


def pauli_part(v):
    """v . sigma as a 2x2 Gaussian-rational matrix (the Lean blochMat)."""
    x, y, z = (_q(a) for a in v)
    return [[(z, Q(0)), (x, -y)], [(x, y), (-z, Q(0))]]


def pauli_part_squares_to_norm(v):
    """(v . sigma)^2 == |v|^2 * 1 exactly (Lean: blochMat_sq)."""
    n = bloch_dot([_q(a) for a in v], [_q(a) for a in v])
    return mat2_mul(pauli_part(v), pauli_part(v)) == [[(n, Q(0)), (Q(0), Q(0))],
                                                       [(Q(0), Q(0)), (n, Q(0))]]


def unitary_about(axis, c, s):
    """U = c 1 - i s sigma_axis (c^2 + s^2 = 1): a Gaussian-rational unitary rotating the Bloch
    vector about the axis by the angle 2 phi with cos phi = c, sin phi = s."""
    c, s = _q(c), _q(s)
    if c * c + s * s != 1 or axis not in ("x", "z"):
        raise ValueError("c^2 + s^2 = 1 and axis x or z are required")
    if axis == "z":
        return [[(c, -s), (Q(0), Q(0))], [(Q(0), Q(0)), (c, s)]]
    return [[(c, Q(0)), (Q(0), -s)], [(Q(0), -s), (c, Q(0))]]


def depolarize_matrix(p, rho):
    """(1 - p) rho + p (tr rho / 2) 1 for a 2x2 matrix."""
    p = _q(p)
    tr = _cadd(rho[0][0], rho[1][1])
    out = [[((1 - p) * rho[i][j][0], (1 - p) * rho[i][j][1]) for j in range(2)] for i in range(2)]
    for i in range(2):
        out[i][i] = _cadd(out[i][i], (p * tr[0] / 2, p * tr[1] / 2))
    return out


def matrix_step(p, U, rho):
    """Unitary conjugation then global depolarizing noise."""
    return depolarize_matrix(p, mat2_mul(mat2_mul(U, rho), mat2_dagger(U)))


def bloch_of_matrix(rho):
    """The Bloch vector (2 Re rho01, -2 Im rho01, rho00 - rho11) of a 2x2 Hermitian trace-one matrix."""
    return [2 * rho[0][1][0], -2 * rho[0][1][1], rho[0][0][0] - rho[1][1][0]]


# ----------------------------------------------------------------------------- Q5: assembled report
def level_for_failure(c, p, circuit_locations, eps, max_levels=16):
    """Smallest level k with L * p_k <= eps below threshold (constant overhead), else None."""
    c, p, L, eps = _q(c), _q(p), _q(circuit_locations), _q(eps)
    if classify(c, p) != "below" or L < 0 or eps <= 0:
        return None
    x = p
    for k in range(max_levels + 1):
        if L * x <= eps:
            return k
        x = c * x * x
    return None


def viability_report(lam, g, kappa, r, c, p, circuit_locations, eps):
    """Conditions of the conditional certificate on a declared instance (constant overhead c)."""
    lam, g, kappa, r = _q(lam), _q(g), _q(kappa), _q(r)
    out = {"authority": AUTHORITY_EFFECT, "supply_ok": False, "below_threshold": False,
           "level": None}
    if g < 1 and kappa > 0:
        out["supply_ok"] = supply_threshold(lam, g, kappa) <= r
    out["below_threshold"] = classify(c, p) == "below"
    if out["supply_ok"] and out["below_threshold"]:
        out["level"] = level_for_failure(c, p, circuit_locations, eps)
    out["certified"] = out["level"] is not None
    return out
