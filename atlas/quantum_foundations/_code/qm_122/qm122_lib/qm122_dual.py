"""Dual of named QM_122 Lean theorems. Not M_n(C). Not Gleason.

AuthorityEffect: None.
"""

from __future__ import annotations

from itertools import permutations
from typing import Callable

Report = bool
Pair = tuple[bool, bool]


def collapse(q: Report) -> Report:
    return False


def toggle(q: Report) -> Report:
    return not q


def has_two_sided_inverse(tau: Callable[[Report], Report]) -> bool:
    tau_table = {q: tau(q) for q in (False, True)}
    if any(type(image) is not bool for image in tau_table.values()):
        return False

    for inv_false in (False, True):
        for inv_true in (False, True):
            inv = {False: inv_false, True: inv_true}

            def inv_fn(q: Report, table: dict[bool, bool] = inv) -> Report:
                return table[q]

            if all(
                inv_fn(tau_table[q]) == q and tau_table[inv_fn(q)] == q
                for q in (False, True)
            ):
                return True
    return False


def bool_reversibles() -> list[Callable[[Report], Report]]:
    maps: list[Callable[[Report], Report]] = []
    for f_false in (False, True):
        for f_true in (False, True):
            table = {False: f_false, True: f_true}

            def tau(q: Report, t: dict[bool, bool] = table) -> Report:
                return t[q]

            if has_two_sided_inverse(tau):
                maps.append(tau)
    return maps


PAIR_DOMAIN: tuple[Pair, ...] = tuple(
    (a, b) for a in (False, True) for b in (False, True)
)


def _reversible_pair_maps() -> list[Callable[[Pair], Pair]]:
    maps: list[Callable[[Pair], Pair]] = []
    for outputs in permutations(PAIR_DOMAIN):
        table = dict(zip(PAIR_DOMAIN, outputs, strict=True))

        def pair_map(x: Pair, values: dict[Pair, Pair] = table) -> Pair:
            return values[x]

        maps.append(pair_map)
    return maps


def identity_dilations() -> list[Callable[[Pair], Pair]]:
    """Enumerate every reversible map that fixes the report coordinate."""
    return [
        dil
        for dil in _reversible_pair_maps()
        if all(dil(x)[0] == x[0] for x in PAIR_DOMAIN)
    ]


def collapse_dilations() -> list[Callable[[Pair], Pair]]:
    """Enumerate every reversible dilation with ancilla prepared at false."""
    return [
        dil
        for dil in _reversible_pair_maps()
        if all(dil((q, False))[0] == collapse(q) for q in (False, True))
    ]


def gmul(z: tuple[int, int], w: tuple[int, int]) -> tuple[int, int]:
    ar, ai = z
    br, bi = w
    return (ar * br - ai * bi, ar * bi + ai * br)


def one_plus_i_not_unit() -> bool:
    """Exhaust the exact mod-two obstruction to ``(1+i)w = 1``.

    Every Gaussian-integer candidate reduces to one of these four
    residue pairs. Multiplication by ``1+i`` gives equal real and
    imaginary residues, so it cannot equal the residue ``(1, 0)``.
    """
    for x_mod_two in (0, 1):
        for y_mod_two in (0, 1):
            real, imag = gmul((1, 1), (x_mod_two, y_mod_two))
            if (real % 2, imag % 2) == (1, 0):
                return False
    return True


def dump_right(u: dict[bool, int], v: dict[bool, int], p: Pair) -> int:
    a, b = p
    if not b:
        return u[a] * (v[False] + v[True])
    return 0


def tensor(u: dict[bool, int], v: dict[bool, int], p: Pair) -> int:
    return u[p[0]] * v[p[1]]


def delta(i: bool) -> dict[bool, int]:
    return {False: 1 if not i else 0, True: 1 if i else 0}


def no_report_half_step() -> bool:
    for s_false in (False, True):
        for s_true in (False, True):
            sigma = {False: s_false, True: s_true}
            if all(sigma[sigma[q]] == toggle(q) for q in (False, True)):
                return False
    return True


def mix(v: dict[bool, tuple[int, int]]) -> dict[bool, tuple[int, int]]:
    vf, vt = v[False], v[True]
    return {
        False: (vf[0] + vt[0], vf[1] + vt[1]),
        True: (vf[0] - vt[0], vf[1] - vt[1]),
    }


def nsq(z: tuple[int, int]) -> int:
    return z[0] * z[0] + z[1] * z[1]


def total_weight(v: dict[bool, tuple[int, int]]) -> int:
    return nsq(v[False]) + nsq(v[True])
