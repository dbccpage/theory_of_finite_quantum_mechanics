"""Exact separator construction for compatible binary 2x2 pair data.

Pair order 00,01,10,11; cell order --,-+,+-,++. Joint mask bits are
A0,A1,B0,B1, with set bit meaning +. AuthorityEffect: None.
Native witnesses require independent projection checking; this is not a Lean
proof of the complete rational Fine converse.
"""
from __future__ import annotations
from dataclasses import dataclass
from fractions import Fraction as Q

FACET_MASKS = tuple(mask for mask in range(16) if bin(mask).count('1') % 2)


def _exact(values, size):
    if len(values) != size:
        raise ValueError('wrong carrier size')
    if any(type(x) not in (int, Q) for x in values):
        raise TypeError('exact integers or Fractions required')
    return tuple(Q(x) for x in values)


def _law(values, size):
    values = _exact(values, size)
    if any(x < 0 for x in values) or sum(values) != 1:
        raise ValueError('nonnegative normalized law required')
    return values


def validate_pairs(pairs):
    if len(pairs) != 4:
        raise ValueError('four observed pair tables required')
    p = tuple(_law(row, 4) for row in pairs)
    for x in range(2):
        if p[2*x][2]+p[2*x][3] != p[2*x+1][2]+p[2*x+1][3]:
            raise ValueError('incompatible A marginal')
    for y in range(2):
        if p[y][1]+p[y][3] != p[2+y][1]+p[2+y][3]:
            raise ValueError('incompatible B marginal')
    return p


def project_joint(weights):
    weights = _law(weights, 16)
    result = [[Q(0) for _ in range(4)] for _ in range(4)]
    for mask, probability in enumerate(weights):
        for x in range(2):
            for y in range(2):
                cell = 2*((mask >> x) & 1)+((mask >> (2+y)) & 1)
                result[2*x+y][cell] += probability
    return tuple(tuple(row) for row in result)


def verify_extension(pairs, weights):
    p = validate_pairs(pairs)
    if project_joint(weights) != p:
        raise ValueError('joint witness does not project to the observed pair data')


def chsh_facets(pairs):
    p = validate_pairs(pairs)
    e = [row[0]-row[1]-row[2]+row[3] for row in p]
    return tuple(sum((-1 if mask & (1 << j) else 1)*e[j] for j in range(4)) for mask in FACET_MASKS)


def _slice_caps(p, y, b):
    u, v = p[y][2+b], p[2+y][2+b]
    w = p[y][b]+u
    return max(Q(0), u+v-w), min(u, v)


@dataclass(frozen=True)
class SeparatorAnalysis:
    lower: tuple[Q, Q]
    upper: tuple[Q, Q]
    common_lower: Q
    common_upper: Q
    facets: tuple[Q, ...]


def separator_intervals(pairs):
    p = validate_pairs(pairs)
    lower = tuple(sum(_slice_caps(p,y,b)[0] for b in range(2)) for y in range(2))
    upper = tuple(sum(_slice_caps(p,y,b)[1] for b in range(2)) for y in range(2))
    return SeparatorAnalysis(lower, upper, max(lower), min(upper), chsh_facets(p))


def split_triple(pairs, setting, separator):
    p = validate_pairs(pairs)
    if type(setting) is not int or setting not in (0,1):
        raise ValueError('binary setting required')
    r, = _exact([separator],1)
    caps = [_slice_caps(p,setting,b) for b in range(2)]
    if not sum(c[0] for c in caps) <= r <= sum(c[1] for c in caps):
        raise ValueError('separator outside this setting interval')
    t0 = max(caps[0][0],r-caps[1][1])
    triple = [Q(0)]*8
    for b,t in enumerate((t0,r-t0)):
        u,v = p[setting][2+b],p[2+setting][2+b]
        w = p[setting][b]+u
        triple[4*b:4*b+4] = [w-u-v+t,u-t,v-t,t]
    return _law(triple,8)


def conditional_glue(left, right):
    left,right = _law(left,8),_law(right,8)
    q = tuple(left[s]+left[s+4] for s in range(4))
    if q != tuple(right[s]+right[s+4] for s in range(4)):
        raise ValueError('separator marginals differ')
    # Nonnegativity and zero total slice mass force both slice cells to zero.
    return tuple(Q(0) if q[m & 3] == 0 else left[(m & 3)+4*((m >> 2)&1)] *
                 right[(m & 3)+4*((m >> 3)&1)] / q[m & 3] for m in range(16))


@dataclass(frozen=True)
class ExtensionDecision:
    analysis: SeparatorAnalysis
    separator: Q | None
    triples: tuple[tuple[Q, ...], tuple[Q, ...]] | None
    weights: tuple[Q, ...] | None
    violating_mask: int | None


def construct_extension(pairs):
    p = validate_pairs(pairs)
    analysis = separator_intervals(p)
    if analysis.common_lower > analysis.common_upper:
        for mask,value in zip(FACET_MASKS,analysis.facets):
            if value > 2:
                return ExtensionDecision(analysis,None,None,None,mask)
        raise ArithmeticError('empty interval without a CHSH obstruction')
    r = analysis.common_lower
    triples = (split_triple(p,0,r),split_triple(p,1,r))
    weights = conditional_glue(*triples)
    verify_extension(p,weights)
    return ExtensionDecision(analysis,r,triples,weights,None)
