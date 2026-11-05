"""Exact integer CAR models of the Meron chain.

The basis bit x of a state s is the occupation n_x. Two builders are given and
cross-checked: ``jw_model`` multiplies Jordan-Wigner matrices c_x, and
``bit_model`` writes the hopping signs directly from the bit strings. All
matrices are integer: K4 = 4K and the insertions are 2a_x, so no rounding occurs.

Options exist only to build the mutations that the tests require to fail:
``erase_wrap_sign`` replaces the physical periodic hopping across the wrap bond
by unsigned spin hopping, ``p_scale`` multiplies every P_x, and
``staggered=False`` drops the factor (-1)^x from a_x.
"""

from __future__ import annotations

import numpy as np


def _popcount(v: int) -> int:
    return bin(v).count("1")


def _stagger(lab: int) -> int:
    """(-1)^lab as an exact integer. ``(-1) ** lab`` is a float when ``lab`` is negative."""
    return -1 if lab % 2 else 1


def _product(a: np.ndarray, b: np.ndarray) -> np.ndarray:
    """a @ b exactly, column by column from the nonzero entries of ``b``.

    The Jordan-Wigner matrices and number operators are signed partial permutations,
    so this is linear in the dimension where a dense int64 product is cubic: the
    ten-mode ring builds in seconds instead of minutes. Entries stay tiny, so no
    overflow guard is needed here.
    """
    out = np.zeros((a.shape[0], b.shape[1]), dtype=np.int64)
    rows, cols = np.nonzero(b)
    for r, c in zip(rows, cols):
        out[:, c] += b[r, c] * a[:, r]
    return out


def annihilators(modes: int) -> list[np.ndarray]:
    """Jordan-Wigner c_x = Z...Z sigma^-_x on ``modes`` modes, as int64 matrices."""
    dim = 1 << modes
    out = []
    for x in range(modes):
        c = np.zeros((dim, dim), dtype=np.int64)
        for s in range(dim):
            if (s >> x) & 1:
                c[s ^ (1 << x), s] = (-1) ** _popcount(s & ((1 << x) - 1))
        out.append(c)
    return out


def _spin_hop(dim: int, x: int, y: int) -> np.ndarray:
    hop = np.zeros((dim, dim), dtype=np.int64)
    for s in range(dim):
        if (s >> y) & 1 and not (s >> x) & 1:
            hop[s ^ (1 << y) ^ (1 << x), s] = 1
    return hop + hop.T


def jw_model(sites, bonds, *, erase_wrap_sign=None, p_scale=1, staggered=True):
    """Return (K4, {site: 2a_site}, {bond: 4P_bond}) from Jordan-Wigner matrices.

    ``sites`` are labels in mode order; ``bonds`` are pairs of labels.
    4P = 2(n_x + n_y - 2 n_x n_y + c_x* c_y + c_y* c_x).
    """
    modes = len(sites)
    index = {lab: j for j, lab in enumerate(sites)}
    cs = annihilators(modes)
    dim = 1 << modes
    eye = np.eye(dim, dtype=np.int64)
    num = [_product(c.T, c) for c in cs]
    k4 = len(bonds) * eye
    fourp = {}
    for bond in bonds:
        i, j = index[bond[0]], index[bond[1]]
        hop = _product(cs[i].T, cs[j]) + _product(cs[j].T, cs[i])
        if erase_wrap_sign is not None and tuple(bond) == tuple(erase_wrap_sign):
            hop = _spin_hop(dim, i, j)
        p4 = p_scale * 2 * (num[i] + num[j] - 2 * _product(num[i], num[j]) + hop)
        fourp[tuple(bond)] = p4
        k4 = k4 - p4
    sign = _stagger if staggered else (lambda lab: 1)
    a2 = {lab: sign(lab) * (2 * num[index[lab]] - eye) for lab in sites}
    return k4, a2, fourp


def bit_model(sites, bonds):
    """Same K4 and 2a_x as ``jw_model``, written directly from bit strings.

    Returns (K4, {site: diagonal of 2a_site as a vector}).
    """
    modes = len(sites)
    index = {lab: j for j, lab in enumerate(sites)}
    dim = 1 << modes
    s = np.arange(dim)
    occ = [(s >> j) & 1 for j in range(modes)]
    k4 = np.zeros((dim, dim), dtype=np.int64)
    for bond in bonds:
        i, j = index[bond[0]], index[bond[1]]
        k4[s, s] += 1 - 2 * (occ[i] + occ[j] - 2 * occ[i] * occ[j])
        lo, hi = min(i, j), max(i, j)
        mask = ((s >> lo) & 1) != ((s >> hi) & 1)
        src = s[mask]
        tgt = src ^ (1 << lo) ^ (1 << hi)
        between = ((1 << hi) - 1) ^ ((1 << (lo + 1)) - 1)
        sgn = np.array([(-1) ** _popcount(int(v) & between) for v in src], dtype=np.int64)
        k4[tgt, src] -= 2 * sgn
    a2 = {lab: _stagger(lab) * (2 * occ[index[lab]] - 1) for lab in sites}
    return k4, a2


def ring(length, **kw):
    """Periodic ring of even ``length``: bonds (x, x+1 mod L), physical CAR signs."""
    if length < 4 or length % 2:
        raise ValueError("ring length must be even and at least 4")
    return jw_model(list(range(length)), [(x, (x + 1) % length) for x in range(length)], **kw)


def chain(lo, hi, **kw):
    """Open chain on sites lo..hi with bonds (x, x+1)."""
    sites = list(range(lo, hi + 1))
    return jw_model(sites, [(x, x + 1) for x in range(lo, hi)], **kw)
