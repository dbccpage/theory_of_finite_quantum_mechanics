"""Independent checker for PG-SN-CARRIER.

Recomputes every record without importing the producer and with a different representation: presentations are the
wire strings of the source grammar (`<>`, `<a>`, `<ab>`, `<a->b>`, `[a,b]`, `u_N<body>`, `r_N<body>`, `NON_DESCENT`)
and the retraction is a regular-expression parser over those strings, not a match over tuples. Shape counts, the total
and the per-stage shape counts use closed forms in g. AuthorityEffect: None.
"""
import json
import re
import sys
from pathlib import Path

ROOT = next((p for p in Path(__file__).resolve().parents if (p / 'dag/pfp/prepare_stage.py').is_file()),
            Path(r'C:\Users\a343o\source\repos\theory_of_finite_quantum_mechanics\.claude\worktrees\unified-dag\.claude\worktrees\pfp-batch-01'))
sys.path.insert(0, str(ROOT / 'dag/pfp'))
import exact_json as E  # noqa: E402

TASK = 'PG-SN-CARRIER'
KEYS = {'input', 'shapes', 'base_total', 'stage_shape_counts', 'table_prefix', 'table_matches', 'table_equal_total_stages',
        'old_image_checked', 'old_image_failures', 'lift_image_sizes', 'universe_size', 'non_base_presentations',
        'unrestricted_image_size', 'unrestricted_fibre_over_ground', 'unrestricted_injective',
        'refusal_round_trip_accepts_ground', 'refusal_round_trip_returns_token', 'stage_mismatch_refused', 'long_body_refused',
        'cumulative_stage_counts', 'cumulative_matches'}
TABLE = {0: 0, 1: 1, 2: 2, 3: 2, 4: 4, 5: 5, 6: 6}


def require(condition, message):
    if not condition:
        raise ValueError(message)


def is_int(x):
    return type(x) is int


def int_list(x):
    return type(x) is list and all(is_int(v) for v in x)


def bool_list(x):
    return type(x) is list and all(type(v) is bool for v in x)


def card(n):
    return TABLE.get(n, n)


def letters(g):
    return [chr(97 + i) for i in range(g)]


def base_wires(g):
    a = letters(g)
    out = ['<>'] + ['<%s>' % x for x in a]
    out += ['<%s%s>' % (x, y) for x in a for y in a]
    out += ['<%s->%s>' % (x, y) for x in a for y in a]
    out += ['[%s,%s]' % (x, y) for x in a for y in a]
    return out


def body_of(wire):
    """The inner body of a base wire, as the lift writes it."""
    if wire == '<>':
        return ''
    if wire.startswith('['):
        return wire[1:-1]
    return wire[1:-1]


def lift_wire(n, wire):
    return 'u_%d<%s>' % (n, body_of(wire))


def retract_wire(n, text):
    m = re.fullmatch(r'u_(\d+)<(.*)>', text)
    if not m or int(m.group(1)) != n:
        return None
    body = m.group(2)
    if body == '':
        return '<>'
    if re.fullmatch(r'[a-z]', body):
        return '<%s>' % body
    if re.fullmatch(r'[a-z][a-z]', body):
        return '<%s>' % body
    mm = re.fullmatch(r'([a-z])->([a-z])', body)
    if mm:
        return '<%s->%s>' % (mm.group(1), mm.group(2))
    mm = re.fullmatch(r'([a-z]),([a-z])', body)
    if mm:
        return '[%s,%s]' % (mm.group(1), mm.group(2))
    return None


def all_bodies(g, maxlen):
    a = letters(g)
    out = ['%s->%s' % (x, y) for x in a for y in a] + ['%s,%s' % (x, y) for x in a for y in a]
    layer = ['']
    out.append('')
    for _ in range(maxlen):
        layer = [w + x for w in layer for x in a]
        out += layer
    return out


def universe(g, stages, maxlen):
    items = list(base_wires(g))
    for n in range(stages):
        for body in all_bodies(g, maxlen):
            items.append('u_%d<%s>' % (n, body))
            items.append('r_%d<%s>' % (n, body))
    items.append('NON_DESCENT')
    return items


def unrestricted(n, wire, base_set):
    """Lift defined on every wire string: base shapes lift as usual, anything else goes to the empty body."""
    if wire in base_set:
        return lift_wire(n, wire)
    return 'u_%d<>' % n


def expected(g, stages, maxlen):
    base = base_wires(g)
    base_set = set(base)
    old_failures = 0
    sizes = []
    for n in range(stages):
        for b in base:
            if retract_wire(n, lift_wire(n, b)) != b:
                old_failures += 1
        sizes.append(len({lift_wire(n, b) for b in base}))
    uni = universe(g, stages, maxlen)
    image0 = {unrestricted(0, p, base_set) for p in uni}
    fibre = sum(1 for p in uni if unrestricted(0, p, base_set) == 'u_0<>')
    total = 1 + g + 3 * g * g
    require(len(base) == total, 'G3_WITNESS:internal_base_count')
    stage_shapes = [1, g, g * g, 2 * g * g]
    rt = retract_wire(0, unrestricted(0, 'NON_DESCENT', base_set))
    mismatch = sum(1 for n in range(stages) for m in range(stages) if m != n for b in base if retract_wire(n, lift_wire(m, b)) is None)
    long_refused = sum(1 for p in uni for n in range(stages) if re.fullmatch(r'u_%d<[a-z]{3,}>' % n, p) and retract_wire(n, p) is None)
    cumulative = [1, 1 + g, 1 + g + g * g, total]
    return {
        'input': [g, stages, maxlen], 'shapes': [1, g, g * g, g * g, g * g], 'base_total': total,
        'stage_shape_counts': stage_shapes, 'table_prefix': [card(i) for i in range(4)],
        'table_matches': [card(i) == stage_shapes[i] for i in range(4)],
        'table_equal_total_stages': [n for n in range(7) if card(n) == total],
        'old_image_checked': stages * total, 'old_image_failures': old_failures, 'lift_image_sizes': sizes,
        'universe_size': len(uni), 'non_base_presentations': len(uni) - total, 'unrestricted_image_size': len(image0),
        'unrestricted_fibre_over_ground': fibre, 'unrestricted_injective': fibre <= 1,
        'refusal_round_trip_accepts_ground': rt == '<>', 'refusal_round_trip_returns_token': rt == 'NON_DESCENT',
        'stage_mismatch_refused': mismatch, 'long_body_refused': long_refused, 'cumulative_stage_counts': cumulative,
        'cumulative_matches': [card(i) == cumulative[i] for i in range(4)]}


def check(request, candidate):
    try:
        _, cand, public = E.bound(request, candidate, TASK)
        data = cand['data']
        require(type(data) is dict and set(data) == {'records'} and type(data['records']) is list, 'G1_SCHEMA:data')
        cases = [list(c) for c in public['cases']]
        records = data['records']
        require(len(records) == len(cases), 'G2_COVERAGE:record_count')
        seen = []
        for r in records:
            require(type(r) is dict and set(r) == KEYS, 'G1_SCHEMA:record_keys')
            require(int_list(r['input']) and len(r['input']) == 3, 'G1_SCHEMA:input')
            g, stages, maxlen = r['input']
            require(0 <= g <= 8 and 1 <= stages <= 5 and 2 <= maxlen <= 4, 'G1_SCHEMA:input_range')
            for k in ('shapes', 'stage_shape_counts', 'table_prefix', 'table_equal_total_stages', 'lift_image_sizes', 'cumulative_stage_counts'):
                require(int_list(r[k]), 'G1_SCHEMA:' + k)
            require(bool_list(r['table_matches']) and bool_list(r['cumulative_matches']), 'G1_SCHEMA:table_matches')
            for k in ('base_total', 'old_image_checked', 'old_image_failures', 'universe_size', 'non_base_presentations',
                      'unrestricted_image_size', 'unrestricted_fibre_over_ground', 'stage_mismatch_refused', 'long_body_refused'):
                require(is_int(r[k]), 'G1_SCHEMA:' + k)
            for k in ('unrestricted_injective', 'refusal_round_trip_accepts_ground', 'refusal_round_trip_returns_token'):
                require(type(r[k]) is bool, 'G1_SCHEMA:' + k)
            seen.append(list(r['input']))
            want = expected(g, stages, maxlen)
            for k in KEYS:
                require(r[k] == want[k], 'G3_WITNESS:' + k)
            # theorem-level consistency of the candidate itself
            require(r['old_image_failures'] == 0, 'G3_WITNESS:old_image_law_holds_on_base')
            require(all(s == r['base_total'] for s in r['lift_image_sizes']), 'G3_WITNESS:lift_image_has_base_cardinality')
            require(r['unrestricted_injective'] is False, 'G3_WITNESS:unrestricted_lift_collides')
            require(r['refusal_round_trip_accepts_ground'] and not r['refusal_round_trip_returns_token'], 'G3_WITNESS:refusal_token_changed')
            require(r['stage_mismatch_refused'] == r['input'][1] * (r['input'][1] - 1) * r['base_total'], 'G3_WITNESS:stage_guard_is_exact')
            require(r['table_matches'][0] is False, 'G3_WITNESS:ground_carrier_is_declared_empty_not_counted')
        require(sorted(seen) == sorted(cases), 'G2_COVERAGE:inputs_are_the_public_cases')
        return {'records_checked': len(records)}
    except (KeyError, TypeError, IndexError, AttributeError) as error:
        raise ValueError('G1_SCHEMA:malformed ' + repr(error))


if __name__ == '__main__':
    print(json.dumps(check(sys.argv[1], sys.argv[2])))
