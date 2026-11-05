"""Finite CAR holonomy on the four-site star and one separate meron orbit.

The hop sign is (-1) to the occupied count strictly below the annihilated
site, plus the occupied count strictly below the created site after removal.
Configuration gauges are vertex bits added in F2. The k=1 orbit is separate.
"""

from __future__ import annotations

from fractions import Fraction

SITES: tuple[int, ...] = (0, 1, 2, 3)
MASKS: tuple[int, ...] = (6, 5, 12, 9, 10, 3, 6)
HOPS: tuple[tuple[int, int], ...] = (
    (1, 0),
    (0, 3),
    (2, 0),
    (0, 1),
    (3, 0),
    (0, 2),
)
SITE_EDGES: tuple[tuple[int, int], ...] = ((0, 1), (0, 2), (0, 3))
FOREIGN_SCALARS: frozenset[int] = frozenset({912, 36864})


def _occupied_before(mask: int, site: int) -> int:
    if site not in SITES:
        raise ValueError("site outside {0,1,2,3}")
    return (mask & ((1 << site) - 1)).bit_count()


def hop_sign(mask: int, src: int, dst: int) -> tuple[int, int]:
    if src not in SITES or dst not in SITES:
        raise ValueError("site outside {0,1,2,3}")
    if ((mask >> src) & 1) == 0 or ((mask >> dst) & 1) == 1:
        raise ValueError("illegal hop")
    before_removal = _occupied_before(mask, src)
    interim = mask ^ (1 << src)
    before_creation = _occupied_before(interim, dst)
    sign = -1 if (before_removal + before_creation) & 1 else 1
    return sign, interim | (1 << dst)


def cycle_signs() -> tuple[int, ...]:
    signs: list[int] = []
    for mask, nxt, (src, dst) in zip(MASKS[:-1], MASKS[1:], HOPS, strict=True):
        if mask.bit_count() != 2 or nxt.bit_count() != 2:
            raise RuntimeError("mask is not a two-particle occupation")
        if src != 0 and dst != 0:
            raise RuntimeError("hop leaves the star center")
        sign, target = hop_sign(mask, src, dst)
        if target != nxt:
            raise RuntimeError("hop missed the declared mask")
        signs.append(sign)
    return tuple(signs)


def _product(signs: tuple[int, ...]) -> int:
    value = 1
    for sign in signs:
        if sign not in (1, -1):
            raise RuntimeError("sign is not a unit")
        value *= sign
    return value


def _parity(signs: tuple[int, ...]) -> tuple[int, int]:
    bit_sum = sum(0 if sign == 1 else 1 for sign in signs)
    return bit_sum, bit_sum & 1


def _gauges(signs: tuple[int, ...]) -> tuple[int, int]:
    vertices = MASKS[:-1]
    if len(vertices) != len(signs):
        raise RuntimeError("one configuration vertex per hop is required")
    if len(set(vertices)) != len(vertices):
        raise RuntimeError("configuration vertices are not distinct")
    heads = tuple(vertices[(index + 1) % len(vertices)] for index in range(len(vertices)))
    if heads != MASKS[1:]:
        raise RuntimeError("hop heads are not the declared successors")
    base = _product(signs)
    count = 1 << len(vertices)
    plus = 0
    for bits in range(count):
        gauged = base
        for index in range(len(vertices)):
            g_tail = (bits >> index) & 1
            g_head = (bits >> ((index + 1) % len(vertices))) & 1
            if (g_tail + g_head) & 1:
                gauged = -gauged
        if gauged == 1:
            plus += 1
        elif gauged != -1:
            raise RuntimeError("gauged product left {+1,-1}")
    return count, plus


def _site_cycle_rank() -> int:
    parent = {site: site for site in SITES}

    def find(site: int) -> int:
        while parent[site] != site:
            parent[site] = parent[parent[site]]
            site = parent[site]
        return site

    redundant = 0
    for left, right in SITE_EDGES:
        if left not in parent or right not in parent:
            raise RuntimeError("edge leaves the four sites")
        a = find(left)
        b = find(right)
        if a == b:
            redundant += 1
        else:
            parent[b] = a
    components = len({find(site) for site in SITES})
    rank = len(SITE_EDGES) - len(SITES) + components
    if rank != redundant:
        raise RuntimeError("cycle rank disagrees with redundant edges")
    return rank


def _orbit() -> tuple[int, Fraction, int]:
    k = 1
    amplitude = 1
    baseline = 1
    mode = 1
    if (k, amplitude, baseline, mode) != (1, 1, 1, 1):
        raise RuntimeError("orbit is not the pinned k=1 character")
    partition = 0
    coefficient = 0
    for orientation in (0, 1):
        character = -1 if (mode & orientation).bit_count() & 1 else 1
        observable = -1 if orientation & 1 else 1
        partition += amplitude * baseline * character
        coefficient += character * observable
    hat = Fraction(coefficient, 1 << k)
    numerator = amplitude * baseline * (1 << k) * hat
    if not isinstance(numerator, Fraction) or numerator.denominator != 1:
        raise RuntimeError("numerator is not an integer")
    return partition, hat, numerator.numerator


def witness() -> dict[str, int | Fraction | tuple[int, ...]]:
    signs = cycle_signs()
    sign_product = _product(signs)
    bit_sum, f2_sum = _parity(signs)
    if sign_product != (1 if f2_sum == 0 else -1):
        raise RuntimeError("product and F2 parity disagree")
    gauges, plus = _gauges(signs)
    rank = _site_cycle_rank()
    partition, hat, numerator = _orbit()
    all_negative = (-1) ** len(signs)
    if all_negative == sign_product:
        raise RuntimeError("all-negative assignment collided with this cycle")
    if (
        sign_product in FOREIGN_SCALARS
        or numerator in FOREIGN_SCALARS
        or partition in FOREIGN_SCALARS
    ):
        raise RuntimeError("a foreign fixture scalar was copied into this carrier")
    holonomy_removed = 1 if sign_product == 1 else 0
    numerator_preserved = 1 if hat == 0 else 0
    conjunction = 1 if holonomy_removed == 1 and numerator_preserved == 1 else 0
    weights = {mask.bit_count() for mask in MASKS}
    if weights != {2}:
        raise RuntimeError("occupations are not uniformly two particles")
    return {
        "sites": len(SITES),
        "center": 0,
        "particles": weights.pop(),
        "hops": len(signs),
        "signs": signs,
        "sign_product": sign_product,
        "parity_bit_sum": bit_sum,
        "f2_cycle_sum": f2_sum,
        "gauges": gauges,
        "gauges_with_product_plus": plus,
        "site_edges": len(SITE_EDGES),
        "site_cycle_rank": rank,
        "all_negative_product": all_negative,
        "k": 1,
        "A": 1,
        "s": 1,
        "m": 1,
        "Z_U": partition,
        "hat_O": hat,
        "N_U": numerator,
        "holonomy_removed": holonomy_removed,
        "numerator_preserved": numerator_preserved,
        "conjunction": conjunction,
    }


def refuse_foreign_scalar(value: int) -> None:
    if value in FOREIGN_SCALARS:
        raise ValueError("912 and 36864 are not the star product or the k=1 numerator")
