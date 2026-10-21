"""Off-image refusal of the pinned S(n) retraction on explicit universes of presentations.

Producer for PFP batch 01, node PG-SN-OFF-IMAGE-REFUSAL. Exact integers only. The model is the pinned SnCarrier of
000_pre_genesis_to_mssn/lean4/SnCarrier.lean with the glyph alphabet abstracted to g glyphs. For each case
(g, S, L, n) the universe is every presentation of the grammar whose lifts and retractions have stage below S and
glyph-list bodies of length at most L (L >= 2 so that every section image lies in the universe). The retraction
r_n and the section u_n are executed on the whole universe and the claims of the node are counted: accepted
outcomes are exactly the section image, refusal holds exactly off the image (violations counted), the payload of an
accepted outcome is the base presentation, the round trip s(r(p)) = p holds on the image and fails on every refused
point, lifts at another stage are refused, over-long bodies are refused, and a lax retraction that accepts the
refused points as the ground presentation obeys the old-image law but breaks the refusal characterisation.
Scope: the declared local model only; no cardinality theorem; no nested lift/retraction as a base member.
AuthorityEffect: None.
"""
from itertools import product

CASES = [['offimage', 0, 2, 2, 0], ['offimage', 1, 3, 3, 1], ['offimage', 2, 4, 3, 0], ['offimage', 2, 4, 3, 3], ['offimage', 3, 3, 4, 2],
         ['offimage', 2, 1, 2, 0], ['offimage', 3, 4, 3, 1], ['offimage', 2, 2, 2, 1],
         ['toy', 3, 2], ['toy', 0, 2], ['toy', 4, 1], ['toy', 2, 3], ['toy', 5, 3]]

FIELDS = ['universe', 'accepted', 'refused', 'image_size', 'iff_violations', 'payload_failures', 'roundtrip_holds',
          'roundtrip_fails', 'stage_mismatch_refused', 'long_body_refused', 'lax_law_failures', 'lax_iff_violations']


def bases(g):
    out = [('ground',)] + [('supplied', m) for m in range(g)]
    for kind in ('pair', 'cut', 'simplex'):
        out += [('relation', kind, a, b) for a in range(g) for b in range(g)]
    return out


def to_pres(b):
    if b[0] == 'ground':
        return ('ground',)
    if b[0] == 'supplied':
        return b
    return ('rel',) + b[1:]


def section_lift(n, b):
    if b[0] == 'ground':
        return ('lift', n, ('glyphs', ()))
    if b[0] == 'supplied':
        return ('lift', n, ('glyphs', (b[1],)))
    kind, a, c = b[1], b[2], b[3]
    if kind == 'pair':
        return ('lift', n, ('glyphs', (a, c)))
    if kind == 'cut':
        return ('lift', n, ('arrow', a, c))
    return ('lift', n, ('pair', a, c))


def retr(n, p):
    if p[0] != 'lift' or p[1] != n:
        return ('nonDescent',)
    body = p[2]
    if body[0] == 'glyphs':
        gs = body[1]
        if len(gs) == 0:
            return ('accepted', ('ground',))
        if len(gs) == 1:
            return ('accepted', ('supplied', gs[0]))
        if len(gs) == 2:
            return ('accepted', ('rel', 'pair', gs[0], gs[1]))
        return ('nonDescent',)
    if body[0] == 'arrow':
        return ('accepted', ('rel', 'cut', body[1], body[2]))
    return ('accepted', ('rel', 'simplex', body[1], body[2]))


def lax_retr(n, p):
    out = retr(n, p)
    return out if out[0] == 'accepted' else ('accepted', ('ground',))


def bodies(g, maxlen):
    out = [('arrow', a, b) for a in range(g) for b in range(g)] + [('pair', a, b) for a in range(g) for b in range(g)]
    for k in range(maxlen + 1):
        out += [('glyphs', t) for t in product(range(g), repeat=k)]
    return out


def universe(g, stages, maxlen):
    items = [('ground',)] + [('supplied', m) for m in range(g)]
    for kind in ('pair', 'cut', 'simplex'):
        items += [('rel', kind, a, b) for a in range(g) for b in range(g)]
    for n in range(stages):
        for body in bodies(g, maxlen):
            items.append(('lift', n, body))
            items.append(('retraction', n, body))
    items.append(('nonDescent',))
    return items


def record(g, stages, maxlen, n):
    base = bases(g)
    uni = universe(g, stages, maxlen)
    image = {section_lift(n, b): b for b in base}
    accepted = refused = iff_viol = payload_fail = rt_holds = rt_fails = long_refused = lax_viol = 0
    for p in uni:
        out = retr(n, p)
        off = p not in image
        if (out[0] == 'nonDescent') != off:
            iff_viol += 1
        if (lax_retr(n, p)[0] == 'nonDescent') != off:
            lax_viol += 1
        if out[0] == 'accepted':
            accepted += 1
            b = image.get(p)
            if b is None or out[1] != to_pres(b):
                payload_fail += 1
            if b is not None and section_lift(n, b) == p:
                rt_holds += 1
            else:
                rt_fails += 1
        else:
            refused += 1
            rt_fails += 1
            if p[0] == 'lift' and p[1] == n and p[2][0] == 'glyphs' and len(p[2][1]) >= 3:
                long_refused += 1
    mismatch = sum(1 for m in range(stages) if m != n for b in base if retr(n, section_lift(m, b))[0] == 'nonDescent')
    lax_law_fail = sum(1 for b in base if lax_retr(n, section_lift(n, b)) != ('accepted', to_pres(b)))
    rec = {'kind': 'offimage', 'input': [g, stages, maxlen, n]}
    rec.update(dict(zip(FIELDS, [len(uni), accepted, refused, len(image), iff_viol, payload_fail, rt_holds, rt_fails,
                                 mismatch, long_refused, lax_law_fail, lax_viol])))
    return rec


TOY_FIELDS = ['points', 'on_image', 'refused', 'law_failures', 'sound_failures']


def toy_record(k, c):
    """Abstract construction: s(x) = c*x on 0..k-1 into 0..c*k-1, total r0(y) = y // c, and the refusing retraction
    r(y) = inl(r0 y) if s(r0 y) == y else refusal. For c = 2, k = 3 this is the toy witness of the source Rust file."""
    def s(x):
        return c * x

    def r(y):
        x = y // c
        return ('inl', x) if s(x) == y else ('inr',)

    points = c * k
    on_image = sum(1 for y in range(points) if r(y)[0] == 'inl')
    refused = sum(1 for y in range(points) if r(y)[0] == 'inr')
    law_fail = sum(1 for x in range(k) if r(s(x)) != ('inl', x))
    sound_fail = sum(1 for y in range(points) if r(y)[0] == 'inl' and s(r(y)[1]) != y)
    rec = {'kind': 'toy', 'input': [k, c]}
    rec.update(dict(zip(TOY_FIELDS, [points, on_image, refused, law_fail, sound_fail])))
    return rec


def certificate(cases=CASES):
    return {'records': [record(*c[1:]) if c[0] == 'offimage' else toy_record(*c[1:]) for c in cases]}


def wire_lines(data):
    out = []
    for r in data['records']:
        fields = FIELDS if r['kind'] == 'offimage' else TOY_FIELDS
        out.append('\t'.join([r['kind']] + [str(x) for x in r['input']] + [str(r[f]) for f in fields]))
    return out


def public_tsv(cases=CASES):
    return ''.join('\t'.join([c[0]] + [str(x) for x in c[1:]]) + '\n' for c in cases)
