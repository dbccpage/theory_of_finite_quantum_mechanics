"""Exact finite checks for the Meron thermodynamic-limit derivation.

``run_all()`` returns a dict of named checks. Every value is computed in exact
integer or Fraction arithmetic from independently built CAR matrices, except
the entries under ``diagnostics``, which use floating point and prove nothing.

Run ``python -m meron_thermodynamic_limit.checks`` from ``code/`` to print JSON.
"""

from __future__ import annotations

import json
from fractions import Fraction

import numpy as np

from . import car, constants
from . import series as S

ORDER = 4          # theta order used against the open chain [-4, 4]
RINGS = (4, 6, 8)
CHAIN = (-4, 4)

ZERO_MODE = [Fraction(1, 4), Fraction(1, 8), Fraction(1, 48), Fraction(-1, 96)]


def _fmt(x):
    if isinstance(x, Fraction):
        if x.denominator == 1:
            return str(x.numerator)
        return f"{x.numerator}/{x.denominator}"
    if isinstance(x, dict):
        return {str(k): _fmt(v) for k, v in x.items()}
    if isinstance(x, (list, tuple)):
        return [_fmt(v) for v in x]
    return x


def ring_bonds(length):
    return [(x, (x + 1) % length) for x in range(length)]


def builders_agree(lengths=(4, 6)):
    for length in lengths:
        k4, a2, _ = car.ring(length)
        kb, ab = car.bit_model(list(range(length)), ring_bonds(length))
        if not np.array_equal(k4, kb):
            return False
        if not all(np.array_equal(np.diag(a2[x]), ab[x]) for x in range(length)):
            return False
    return True


def projector_checks(length=6):
    """(4P)^2 = 4(4P) for every bond, so I/4 - P has spectrum in {1/4, -3/4}."""
    _, _, fourp = car.ring(length)
    return all(np.array_equal(p @ p, 4 * p) for p in fourp.values())


def _site_paulis(length):
    """Single-site X_z and Z_z on the spin space, as int64 matrices."""
    dim = 1 << length
    s = np.arange(dim)
    out = {}
    for z in range(length):
        x = np.zeros((dim, dim), dtype=np.int64)
        x[s ^ (1 << z), s] = 1
        zz = np.diag(1 - 2 * ((s >> z) & 1)).astype(np.int64)
        out[z] = (x, zz)
    return out


def _nonlocal_mutation(fourp, length):
    """Replace 4P_(0,1) by 4P_(0,1)(I + Z_2...Z_{L-1})/2: a projector that is not local."""
    dim = 1 << length
    s = np.arange(dim)
    par = np.zeros(dim, dtype=np.int64)
    for z in range(2, length):
        par ^= (s >> z) & 1
    q = np.diag(1 - par).astype(np.int64)  # (I + Z_2...Z_{L-1})/2
    out = dict(fourp)
    out[(0, 1)] = fourp[(0, 1)] @ q
    return out


def _parity(length):
    """Total fermion parity prod_z Z_z, as an int64 diagonal matrix."""
    s = np.arange(1 << length)
    par = np.zeros(1 << length, dtype=np.int64)
    for z in range(length):
        par ^= (s >> z) & 1
    return np.diag(1 - 2 * par).astype(np.int64)


def _odd_mutation(fourp, length):
    """Replace 4P_(0,1) by 2(I + (c_0 + c_0^*) Z_2...Z_{L-1}): 4 times a projector,
    commuting with c_z, c_z^* off the bond, but odd (round-5 objection R5-OBJ-02)."""
    dim = 1 << length
    s = np.arange(dim)
    par = np.zeros(dim, dtype=np.int64)
    for z in range(2, length):
        par ^= (s >> z) & 1
    c0 = car.annihilators(length)[0]
    u = (c0 + c0.T) @ np.diag(1 - 2 * par).astype(np.int64)
    out = dict(fourp)
    out[(0, 1)] = 2 * (np.eye(dim, dtype=np.int64) + u)
    return out


def _hamiltonian_from(fourp, eye):
    """4K = (number of bonds) I - sum of the bond terms."""
    built = len(fourp) * eye
    for m in fourp.values():
        built = built - m
    return built


def _disjoint_unit_sets(units):
    """Every set of at least two units (bonds or single sites) with pairwise disjoint supports.

    The bond-only groups are among them, so this covers item 2 of ``bond_locality`` too.
    """
    out = []

    def grow(chosen, rest):
        if len(chosen) >= 2:
            out.append(tuple(chosen))
        for i, u in enumerate(rest):
            if all(not (set(u[0]) & set(c[0])) for c in chosen):
                grow(chosen + [u], rest[i + 1:])
    grow([], list(units))
    return out


def bond_locality(length=6, *, erase=False, nonlocal_mutation=False,
                  source_mutation=False, odd_mutation=False,
                  hamiltonian_mutation=None):
    """TL-1's premises, exactly, for the physical or the sign-erased ring.

    1. Every bond term is 4 times a projector.
    2. Terms on disjoint bonds commute, and for every set of pairwise disjoint
       bonds the normalized trace of the product is the product of the traces
       (the bond-only groups are among the unit groups of item 6).
    3. Support: a bond term commutes with every local operator off its bond, and
       with the source a_z there. Local operators are c_z and c_z^* (CAR) for the
       physical ring, and the site Paulis X_z, Z_z (spin language) for the erased one.
    4. Vanishing mean coefficients: Tr(K^n a_x) = 0 for n <= L.
       This finite check alone does not establish vanishing to every order.
    5. Evenness: every bond term and every source commutes with the total parity.
    6. Source support: each source a_z commutes with every local operator off z,
       and for every set of pairwise disjoint units (bond terms and sources) the
       normalized trace of the product is the product of the traces.

    7. Binding: the K in use is built from the bond terms in use,
       4K = (number of bonds) I - sum of the bond terms.

    Item 6 checks products of single units; word-level factorization over
    disjoint components follows from items 3, 5 and 6 (TL-1, locality lemma).

    Every mutation is a different model, and all seven premises are checked
    against that model. ``nonlocal_mutation`` swaps in a bond term that passes 1
    and pairwise factorization but is not local (round-4 counterexample
    R4-CX-01); ``source_mutation`` dresses the source a_{L/2} by the total
    parity (round-5 counterexample R5-CX-01); ``odd_mutation`` swaps in an odd
    bond term that passes the support test (round-5 objection R5-OBJ-02). The
    term mutations rebuild K from the swapped term, so they reach the premise
    they are built to fail rather than stopping at the binding.
    ``hamiltonian_mutation`` adds a term to K while leaving the bond terms and
    sources as they are (round-6 counterexample R6-CX-01): ``"zz"`` adds
    4 Z_0 Z_{L/2}, ``"ptot"`` adds 4 times the total parity, ``"z1z4"`` adds
    4 Z_1 Z_4 (needs L >= 5). Each must fail.
    """
    kw = {"erase_wrap_sign": (length - 1, 0)} if erase else {}
    k4, a2, fourp = car.ring(length, **kw)
    dim = 1 << length
    eye = np.eye(dim, dtype=np.int64)
    if nonlocal_mutation:
        fourp = _nonlocal_mutation(fourp, length)
        k4 = _hamiltonian_from(fourp, eye)
    if odd_mutation:
        fourp = _odd_mutation(fourp, length)
        k4 = _hamiltonian_from(fourp, eye)
    if source_mutation:
        a2 = dict(a2)
        a2[length // 2] = a2[length // 2] @ _parity(length)
    if hamiltonian_mutation is not None:
        if hamiltonian_mutation == "z1z4" and length < 5:
            raise ValueError("the z1z4 mutation needs a ring of length at least 5")
        zs = {z: ops[1] for z, ops in _site_paulis(length).items()}
        extra = {"zz": lambda: zs[0] @ zs[length // 2],
                 "ptot": lambda: _parity(length),
                 "z1z4": lambda: zs[1] @ zs[4]}[hamiltonian_mutation]()
        k4 = k4 + 4 * extra
    if not np.array_equal(k4, _hamiltonian_from(fourp, eye)):
        return False
    bonds = list(fourp)
    if erase:
        local = {z: list(ops) for z, ops in _site_paulis(length).items()}
    else:
        cs = car.annihilators(length)
        local = {z: [cs[z], cs[z].T] for z in range(length)}

    def ntr(m):
        return Fraction(int(np.trace(m)), dim)

    for b in bonds:
        p = fourp[b]
        if not np.array_equal(p @ p, 4 * p):
            return False
        for c in bonds:
            if not (set(b) & set(c)) and not np.array_equal(p @ fourp[c], fourp[c] @ p):
                return False
        for z in range(length):
            if z in b:
                continue
            for op in local[z] + [a2[z]]:
                if not np.array_equal(p @ op, op @ p):
                    return False
    power = eye
    for _ in range(length + 1):
        if any(np.trace(power @ a) != 0 for a in a2.values()):
            return False
        power = power @ k4
    par = _parity(length)
    for op in list(fourp.values()) + list(a2.values()):
        if not np.array_equal(op @ par, par @ op):
            return False
    for z, a in a2.items():
        for w in range(length):
            if w == z:
                continue
            for op in local[w]:
                if not np.array_equal(a @ op, op @ a):
                    return False
    units = [(b, fourp[b]) for b in bonds] + [((z,), a2[z]) for z in sorted(a2)]
    for group in _disjoint_unit_sets(units):
        prod, want = eye, Fraction(1)
        for _, m in group:
            prod = prod @ m
            want *= ntr(m)
        if ntr(prod) != want:
            return False
    return True


def row_sum_series(k4, a2, length, order, *, pw=None, normalise=True, ztr=None):
    pw = S.powers(k4, order) if pw is None else pw
    z = S.partition_traces(pw) if ztr is None else ztr
    total = S.zero_series(order)
    for y in range(length):
        table = S.trace_table(pw, a2[0], a2[y], order)
        total = S.add(total, S.series(table, z, order, 4, normalise=normalise))
    return total


def two_point(k4, a2, sites, order, pw=None):
    pw = S.powers(k4, order) if pw is None else pw
    return {y: S.correlation(k4, a2[0], a2[y], order, 4, pw=pw) for y in sites}


def ring_distance(y, length):
    return min(y % length, (-y) % length)


def lift_check(chain_corr, ring_corr, length, order):
    """Compare C^L_{0y} with sum_{n == y mod L} C^chain_{0n}, order by order.

    Returns (orders that agree for every y, orders that disagree for some y).
    """
    agree, differ = [], []
    for n in range(order + 1):
        ok = True
        for y, coeffs in ring_corr.items():
            pred = [sum((chain_corr[m][n][k] for m in chain_corr if (m - y) % length == 0),
                        Fraction(0)) for k in range(order + 1)]
            if pred != coeffs[n]:
                ok = False
        (agree if ok else differ).append(n)
    return agree, differ


def particle_hole_mean(length=6, order=6):
    """Tr(K4^n 2a_x) = 0 for all n <= order: <a_x> vanishes to every computed order."""
    k4, a2, _ = car.ring(length)
    pw = S.powers(k4, order)
    return all(int(np.sum(np.diag(m).astype(object) * np.diag(a2[x]).astype(object))) == 0
               for m in pw for x in range(length))


def commutator_identity(length=6):
    """[A,[K,A]] = 2 sum_x h_x with h_x = c_x* c_y + c_y* c_x."""
    k4, a2, _ = car.ring(length)
    cs = car.annihilators(length)
    a_tot = sum(a2.values())
    lhs = a_tot @ (k4 @ a_tot - a_tot @ k4) - (k4 @ a_tot - a_tot @ k4) @ a_tot
    hsum = sum(cs[x].T @ cs[(x + 1) % length] + cs[(x + 1) % length].T @ cs[x]
               for x in range(length))
    return bool(np.array_equal(lhs, 32 * hsum))


def _local_b0(length):
    """Return (B_0, j_0) with j_0 = c_1* c_0 - c_0* c_1 and B_0 = -[K, j_0]."""
    k4, _, _ = car.ring(length)
    cs = car.annihilators(length)
    j0 = cs[1].T @ cs[0] - cs[0].T @ cs[1]
    b0_4 = -(k4 @ j0 - j0 @ k4)  # = 4 B_0
    return b0_4, k4


def ibp_identity(length, order, modes=(1, 2, 3)):
    """omega^2 khat_L(m) = 2 theta F - theta^2 ghat(m), coefficientwise in theta.

    F = <h_0>, g(u) = (1/L)<[K,[K,A]](u) A>; also checks g = sum_y <B_0(u) a_y>,
    F'(0) = 1/4 and g(theta = 0) = 1/2.
    """
    k4, a2, _ = car.ring(length)
    cs = car.annihilators(length)
    pw = S.powers(k4, order)
    eye = np.eye(1 << length, dtype=np.int64)
    a_tot = sum(a2.values())
    h0 = cs[0].T @ cs[1] + cs[1].T @ cs[0]
    k_ser = row_sum_series(k4, a2, length, order, pw=pw)
    f_ser = S.correlation(k4, h0, eye, order, 1, pw=pw)
    inner = k4 @ a_tot - a_tot @ k4
    x_op = k4 @ inner - inner @ k4  # = 32 [K,[K,A]]
    g_ser = S.scale_series(S.correlation(k4, x_op, a_tot, order, 64, pw=pw), Fraction(1, length))
    b0_4, _ = _local_b0(length)
    g_loc = S.zero_series(order)
    for y in range(length):
        g_loc = S.add(g_loc, S.correlation(k4, b0_4, a2[y], order, 8, pw=pw))
    ok = True
    for m in modes:
        for n in range(order + 1):
            lhs = {p - 2: -v for p, v in S.fourier(k_ser[n], m).items()}
            rhs = {}
            if n >= 1 and f_ser[n - 1][0]:
                rhs[0] = 2 * f_ser[n - 1][0]
            if n >= 2:
                for p, v in S.fourier(g_ser[n - 2], m).items():
                    rhs[p] = rhs.get(p, Fraction(0)) - v
            if lhs != {p: v for p, v in rhs.items() if v}:
                ok = False
    return {
        "identity": ok,
        "g_is_local_sum": g_ser == g_loc,
        "F_coefficients": [f_ser[n][0] for n in range(order + 1)],
        "g_at_theta_0": g_ser[0][0],
        "g_at_theta_0_u_independent": all(c == 0 for c in g_ser[0][1:]),
    }


def b0_support_and_norm(length=8):
    """B_0 is even and commutes with c_z, c_z^* for z outside {-1,0,1,2}.

    By the locality lemma of TL-1 that places it in the CAR algebra of those four
    modes. Commuting with n_z alone would not: a parity-dressed operator passes that.
    ||B_0|| <= 3 is reported as a floating-point eigenvalue diagnostic only.
    """
    b0_4, _ = _local_b0(length)
    cs = car.annihilators(length)
    support = {(-1) % length, 0, 1, 2}
    local = all(np.array_equal(b0_4 @ op, op @ b0_4)
                for z, c in enumerate(cs) if z not in support for op in (c, c.T))
    par = _parity(length)
    even = bool(np.array_equal(b0_4 @ par, par @ b0_4))
    hermitian = bool(np.array_equal(b0_4, b0_4.T))
    norm = float(np.max(np.abs(np.linalg.eigvalsh(b0_4.astype(float))))) / 4
    return {"local": local, "even": even, "hermitian": hermitian, "norm_diagnostic": norm}


def psd_exact(m) -> bool:
    """Exact test that a symmetric rational matrix is positive semidefinite.

    Symmetric Gaussian elimination in Fractions: a negative pivot fails, and a zero
    pivot must have a zero row.
    """
    rows = [list(row) for row in m]
    n = len(rows)
    if any(len(row) != n for row in rows):
        return False
    if any((type(v) not in (int, Fraction) and not isinstance(v, np.integer))
           or isinstance(v, (bool, np.bool_)) for row in rows for v in row):
        return False
    a = [[v if type(v) is Fraction else Fraction(int(v)) for v in row] for row in rows]
    if any(a[i][j] != a[j][i] for i in range(n) for j in range(n)):
        return False
    for k in range(n):
        if a[k][k] < 0:
            return False
        if a[k][k] == 0:
            if any(a[k][j] != 0 for j in range(k + 1, n)):
                return False
            continue
        for i in range(k + 1, n):
            f = a[i][k] / a[k][k]
            if f:
                for j in range(k, n):
                    a[i][j] -= f * a[k][j]
    return True


def b0_norm_certificate():
    """||B_0|| <= 3 exactly: 144 I - (4B_0)^2 >= 0 on the four modes -1, 0, 1, 2.

    Only the bonds (-1,0), (0,1), (1,2) fail to commute with j_0, so B_0 is a CAR
    polynomial in these four modes; its norm does not depend on the representation.
    In fact ||B_0||^2 <= 3 (48 I - (4B_0)^2 >= 0); the proof only uses the weaker 3.
    """
    k4, _, _ = car.chain(-1, 2)
    cs = car.annihilators(4)
    j0 = cs[2].T @ cs[1] - cs[1].T @ cs[2]  # modes ordered -1, 0, 1, 2
    b = -(k4 @ j0 - j0 @ k4)
    eye = np.eye(16, dtype=np.int64)
    return {"norm_le_3": psd_exact(144 * eye - b @ b),
            "norm_sq_le_3": psd_exact(48 * eye - b @ b),
            "norm_sq_le_2_fails": not psd_exact(32 * eye - b @ b)}


def mutations(order=ORDER):
    """Each mutation must change an exact value that the correct model fixes."""
    out = {}
    # erased wrap sign (unsigned spin hop across the wrap bond): an arc of the ring is
    # the same CAR system either way, so the kernel may change only from order L on.
    # It must change exactly there.
    for length in (4, 6):
        k4, a2, _ = car.ring(length)
        k4e, a2e, _ = car.ring(length, erase_wrap_sign=(length - 1, 0))
        good = row_sum_series(k4, a2, length, length + 1)
        bad = row_sum_series(k4e, a2e, length, length + 1)
        out[f"erased_wrap_sign_L{length}_row_sum_differs_at_orders"] = [
            n for n in range(length + 2) if good[n] != bad[n]]
    k4, a2, _ = car.ring(6)
    pw = S.powers(k4, 2)
    good = row_sum_series(k4, a2, 6, 2, pw=pw)
    # unnormalised trace: theta = 0 value is 2^L/4, not 1/4
    raw = row_sum_series(k4, a2, 6, 0, normalise=False)
    out["unnormalised_theta0_value"] = S.fourier(raw[0], 0)[0]
    # normalising by 2^L instead of Z: differs first at theta^2
    by_dim = row_sum_series(k4, a2, 6, 2, pw=pw, ztr=[1 << 6, 0, 0])
    out["normalise_by_2L_first_differing_order"] = next(
        n for n in range(3) if by_dim[n] != good[n])
    # doubled projector: theta^2 nonzero-mode coefficient changes from -t^2/2
    k4d, a2d, _ = car.ring(6, p_scale=2)
    dbl = row_sum_series(k4d, a2d, 6, 2)
    out["doubled_P_c2_mode1"] = S.fourier(dbl[2], 1)
    # unstaggered a: first-order zero-mode coefficient changes from 1/8
    k4u, a2u, _ = car.ring(6, staggered=False)
    uns = row_sum_series(k4u, a2u, 6, 1)
    out["unstaggered_zero_mode_theta1"] = S.fourier(uns[1], 0)[0]
    return out


def erased_sign_site_differences(length):
    """Orders at which the per-site kernels C_{0y} of the physical and sign-erased rings differ.

    Below order ``length`` no cluster reaches around the ring, so both models restrict to the
    same open-arc system and their kernels agree site by site; the lift therefore covers the
    erased (spin-periodic) ring too, and the two first differ at order ``length``.
    """
    k4, a2, _ = car.ring(length)
    k4e, a2e, _ = car.ring(length, erase_wrap_sign=(length - 1, 0))
    good = two_point(k4, a2, range(length), length)
    bad = two_point(k4e, a2e, range(length), length)
    return [n for n in range(length + 1) if any(good[y][n] != bad[y][n] for y in range(length))]


def wrap_sign_zero_modes(length=6, order=6):
    """Exact zero-mode series of k_L with the physical wrap sign and with it erased."""
    out = {}
    for name, kw in (("physical", {}), ("erased", {"erase_wrap_sign": (length - 1, 0)})):
        k4, a2, _ = car.ring(length, **kw)
        ser = row_sum_series(k4, a2, length, order)
        out[name] = [S.fourier(ser[n], 0).get(0, Fraction(0)) for n in range(order + 1)]
    out["first_difference_order"] = next(
        (n for n in range(order + 1) if out["physical"][n] != out["erased"][n]), None)
    return out


def float_row_sum(length, theta, u):
    """Diagnostic only: k_L(theta, u) by floating-point diagonalisation."""
    k4, a2, _ = car.ring(length)
    evals, vecs = np.linalg.eigh(k4.astype(float) / 4)
    a_tot = sum(a2.values()).astype(float) / 2
    a0 = np.diag(a2[0]).astype(float) / 2
    a0e = vecs.T @ np.diag(a0) @ vecs
    ae = vecs.T @ a_tot @ vecs
    w = np.exp(-theta * (evals - evals.min()))
    left = np.exp(-(1 - u) * theta * (evals - evals.min()))
    right = np.exp(-u * theta * (evals - evals.min()))
    num = np.sum(left[:, None] * a0e * right[None, :] * ae.T)
    return float(num / w.sum())


def run_all():
    res = {"builders_agree": builders_agree(), "projector": projector_checks(),
           "particle_hole_mean_zero": particle_hole_mean() and particle_hole_mean(4, 5),
           "commutator_A_K_A": commutator_identity()}
    lo, hi = CHAIN
    kc, ac, _ = car.chain(lo, hi)
    chain_corr = two_point(kc, ac, range(lo, hi + 1), ORDER)
    res["theta0_delta_quarter"] = all(
        chain_corr[y][0][0] == (Fraction(1, 4) if y == 0 else 0)
        and not any(chain_corr[y][0][1:]) for y in chain_corr)
    res["chain_vanishing_order_equals_distance"] = all(
        S.first_order(c) == abs(y) for y, c in chain_corr.items() if abs(y) <= ORDER)
    rings = {}
    for length in RINGS:
        k4, a2, _ = car.ring(length)
        pw = S.powers(k4, ORDER)
        rc = two_point(k4, a2, range(length), ORDER, pw=pw)
        top = min(ORDER, length - 1)
        agree, differ = lift_check(chain_corr, rc, length, ORDER)
        kser = S.zero_series(ORDER)
        for c in rc.values():
            kser = S.add(kser, c)
        trans = row_sum_series(k4, a2, length, ORDER, pw=pw)
        rings[length] = {
            "vanishing_order_equals_ring_distance": all(
                S.first_order(c) == ring_distance(y, length)
                for y, c in rc.items() if ring_distance(y, length) <= ORDER),
            "lift_agrees_through_order": max(
                (n for n in agree if all(m in agree for m in range(n + 1))), default=-1),
            "lift_expected_through_order": top,
            "lift_differs_at_orders": differ,
            "zero_mode": [S.fourier(kser[n], 0)[0] for n in range(ORDER + 1)],
            "mode_1": [S.fourier(kser[n], 1) for n in range(ORDER + 1)],
            "symmetric_u_to_1_minus_u": _symmetric(kser),
            "fixed_origin_assembly_consistency": kser == trans,
        }
    res["rings"] = rings
    res["ibp"] = {length: ibp_identity(length, 5 if length == 4 else 4) for length in (4, 6)}
    res["b0"] = b0_support_and_norm()
    res["b0_norm_certificate"] = b0_norm_certificate()
    res["mutations"] = mutations()
    res["wrap_sign_zero_modes_L6"] = wrap_sign_zero_modes(6, 6)
    res["particle_hole_scope"] = [{"length": 4, "order": 5}, {"length": 6, "order": 6}]
    res["bond_locality"] = {
        "physical_L6": bond_locality(6), "erased_L6": bond_locality(6, erase=True),
        "nonlocal_mutation_L6": bond_locality(6, nonlocal_mutation=True),
        "source_mutation_L6": bond_locality(6, source_mutation=True),
        "odd_mutation_L6": bond_locality(6, odd_mutation=True)}
    res["erased_sign_site_differences"] = {length: erased_sign_site_differences(length) for length in (4, 6)}
    res["constants"] = constants.as_json()
    res["diagnostics"] = {
        f"k_L(1/192, 1/3) L={length}": float_row_sum(length, 1 / 192, 1 / 3)
        for length in (4, 6, 8, 10)}
    return res


def _symmetric(kser):
    """Each theta^n polynomial p(u) satisfies p(u) = p(1-u)."""
    from math import comb
    for p in kser:
        q = [sum(p[k] * comb(k, j) * (-1) ** j for k in range(j, len(p))) for j in range(len(p))]
        if q != p:
            return False
    return True


if __name__ == "__main__":
    print(json.dumps(_fmt(run_all()), indent=1, sort_keys=True))
