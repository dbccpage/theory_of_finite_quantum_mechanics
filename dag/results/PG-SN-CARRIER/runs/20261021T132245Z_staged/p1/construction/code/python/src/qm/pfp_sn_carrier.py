"""The S(n) base presentations, their section lift and retraction, and the declared carrier table.

Producer for PFP batch 01, node PG-SN-CARRIER. Exact integers only. The model is the pinned SnCarrier of
000_pre_genesis_to_mssn/lean4/SnCarrier.lean (sha256 357376de...) with the glyph alphabet abstracted to g glyphs
0..g-1. For each case (g, S, L) the universe of presentations is built explicitly (ground, supplied marks, the three
relation shapes, lifts and retractions at stages 0..S-1 whose glyph-list bodies have length at most L, and the refusal
token) and the pinned functions are executed on it: the old-image law on every base presentation at every stage, the
image sizes of the lift, the unrestricted (pre-repair) lift of ledger row WDP-P001-019 and its collisions, and the
comparison of the declared cardinality table with the counts the model actually has.
Scope: the declared local model only; nothing here repairs the table or proves a cardinality theorem.
AuthorityEffect: None.
"""
from itertools import product

CASES = [[0, 2, 2], [1, 3, 3], [2, 4, 3], [3, 4, 3], [4, 3, 2], [6, 4, 3]]
TABLE = [0, 1, 2, 2, 4, 5, 6]


def carrier_card(n):
    return TABLE[n] if n < len(TABLE) else n


# presentation encoding: ('ground',), ('supplied', m), ('rel', kind, a, b), ('lift', n, body), ('retraction', n, body), ('nonDescent',)
# body encoding: ('arrow', a, b), ('pair', a, b), ('glyphs', (m, ...))
# base encoding: ('ground',), ('supplied', m), ('relation', kind, a, b)

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


def unrestricted_lift(n, p):
    if p[0] == 'ground':
        return ('lift', n, ('glyphs', ()))
    if p[0] == 'supplied':
        return ('lift', n, ('glyphs', (p[1],)))
    if p[0] == 'rel':
        kind, a, c = p[1], p[2], p[3]
        return section_lift(n, ('relation', kind, a, c))
    return ('lift', n, ('glyphs', ()))


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


def record(g, stages, maxlen):
    base = bases(g)
    shapes = [1, g, g * g, g * g, g * g]
    old_checked = old_fail = 0
    image_sizes = []
    for n in range(stages):
        for b in base:
            old_checked += 1
            if retr(n, section_lift(n, b)) != ('accepted', to_pres(b)):
                old_fail += 1
        image_sizes.append(len({section_lift(n, b) for b in base}))
    uni = universe(g, stages, maxlen)
    nonbase = len(uni) - len(base)
    image0 = {unrestricted_lift(0, p) for p in uni}
    fibre = sum(1 for p in uni if unrestricted_lift(0, p) == ('lift', 0, ('glyphs', ())))
    rt = retr(0, unrestricted_lift(0, ('nonDescent',)))
    stage_shapes = [1, g, g * g, 2 * g * g]
    total = len(base)
    mismatch = sum(1 for n in range(stages) for m in range(stages) if m != n for b in base if retr(n, section_lift(m, b)) == ('nonDescent',))
    long_refused = sum(1 for p in uni if p[0] == 'lift' and p[2][0] == 'glyphs' and len(p[2][1]) >= 3 and retr(p[1], p) == ('nonDescent',))
    cumulative = [1, 1 + g, 1 + g + g * g, 1 + g + 3 * g * g]
    return {
        'input': [g, stages, maxlen],
        'shapes': shapes,
        'base_total': total,
        'stage_shape_counts': stage_shapes,
        'table_prefix': [carrier_card(i) for i in range(4)],
        'table_matches': [carrier_card(i) == stage_shapes[i] for i in range(4)],
        'table_equal_total_stages': [n for n in range(7) if carrier_card(n) == total],
        'old_image_checked': old_checked,
        'old_image_failures': old_fail,
        'lift_image_sizes': image_sizes,
        'universe_size': len(uni),
        'non_base_presentations': nonbase,
        'unrestricted_image_size': len(image0),
        'unrestricted_fibre_over_ground': fibre,
        'unrestricted_injective': fibre <= 1,
        'refusal_round_trip_accepts_ground': rt == ('accepted', ('ground',)),
        'refusal_round_trip_returns_token': rt == ('accepted', ('nonDescent',)),
        'stage_mismatch_refused': mismatch,
        'long_body_refused': long_refused,
        'cumulative_stage_counts': cumulative,
        'cumulative_matches': [carrier_card(i) == cumulative[i] for i in range(4)],
    }


def certificate(cases=CASES):
    return {'records': [record(*c) for c in cases]}


def _b(x):
    return str(int(x))


def _list(xs):
    return ','.join(str(x) for x in xs) or '-'


def wire_lines(data):
    out = []
    for r in data['records']:
        out.append('\t'.join(['carrier'] + [str(x) for x in r['input']] + [
            _list(r['shapes']), str(r['base_total']), _list(r['stage_shape_counts']), _list(r['table_prefix']),
            _list(int(x) for x in r['table_matches']), _list(r['table_equal_total_stages']),
            str(r['old_image_checked']), str(r['old_image_failures']), _list(r['lift_image_sizes']),
            str(r['universe_size']), str(r['non_base_presentations']), str(r['unrestricted_image_size']),
            str(r['unrestricted_fibre_over_ground']), _b(r['unrestricted_injective']),
            _b(r['refusal_round_trip_accepts_ground']), _b(r['refusal_round_trip_returns_token']),
            str(r['stage_mismatch_refused']), str(r['long_body_refused']), _list(r['cumulative_stage_counts']),
            _list(int(x) for x in r['cumulative_matches'])]))
    return out


def public_tsv(cases=CASES):
    return ''.join('carrier\t%d\t%d\t%d\n' % tuple(c) for c in cases)
