"""Six operations and the admitted state: exact enumeration of traces over a two-item universe.

Producer for PFP batch 01, node PG-SIX-OPERATIONS. Exact integers only; no random numbers.
State: (mentioned, supplied, designated, admitted, retained, outputs). Operations Mention, Supply, Designate,
Admit, Retain, Operate on one item; Retain and Operate act only on admitted items. Definitional model only:
it does not derive the Reading L / Reading F split. AuthorityEffect: None.
"""
from itertools import product

KINDS = ['mention', 'supply', 'designate', 'admit', 'retain', 'operate']
FIELDS = ['mentioned', 'supplied', 'designated', 'admitted', 'retained', 'outputs']
ITEMS = (0, 1)
OPS = [(k, x) for k in KINDS for x in ITEMS]
CONFLATIONS = {
    'mention_includes_admit': ('mention', 'admit'),
    'supply_includes_admit': ('supply', 'admit'),
    'designate_includes_admit': ('designate', 'admit'),
    'retain_includes_admit': ('retain', 'admit'),
    'operate_includes_admit': ('operate', 'admit'),
    'designate_includes_retain': ('designate', 'retain'),
    'mention_includes_supply': ('mention', 'supply'),
}
CASES = ([['trace', 2, 4, mask] for mask in range(4)]
         + [['footprint', k] for k in KINDS]
         + [['pair', KINDS[i], KINDS[j]] for i in range(6) for j in range(i + 1, 6)]
         + [['conflation', name] for name in CONFLATIONS]
         + [['reading', 0, 'supply_includes_admit'], ['reading', 0, 'admit_includes_supply']])


def empty(admitted=()):
    return (frozenset(), frozenset(), (), frozenset(admitted), frozenset(), frozenset())


def step(s, op):
    k, x = op
    m, u, d, a, r, o = s
    if k == 'mention':
        return (m | {x}, u, d, a, r, o)
    if k == 'supply':
        return (m, u | {x}, d, a, r, o)
    if k == 'designate':
        return (m, u, (x,), a, r, o)
    if k == 'admit':
        return (m, u, d, a | {x}, r, o)
    if k == 'retain':
        return (m, u, d, a, r | {x}, o) if x in a else s
    if k == 'operate':
        return (m, u, d, a, r, o | {x}) if x in a else s
    raise ValueError(k)


def run(s, trace, stepper=step):
    for op in trace:
        s = stepper(s, op)
    return s


def conflated(a_kind, b_kind):
    """Model in which operation a_kind first performs b_kind on the same item."""
    def stepper(s, op):
        if op[0] == a_kind:
            s = step(s, (b_kind, op[1]))
        return step(s, op)
    return stepper


def fields_changed(before, after):
    return ''.join('1' if before[i] != after[i] else '0' for i in range(6))


def listed(s):
    return [sorted(s[0]), sorted(s[1]), list(s[2]), sorted(s[3]), sorted(s[4]), sorted(s[5])]


def trace_text(trace):
    return ','.join('%s:%d' % op for op in trace) or '-'


def trace_record(items, max_len, mask):
    ops = [(k, x) for k in KINDS for x in range(items)]
    init = empty([x for x in range(items) if mask >> x & 1])
    total = changed = with_admit = with_new = mismatches = 0
    finals = set()
    for length in range(max_len + 1):
        for trace in product(ops, repeat=length):
            final = run(init, trace)
            total += 1
            moved = final[3] != init[3]
            has_admit = any(k == 'admit' for k, _ in trace)
            has_new = any(k == 'admit' and x not in init[3] for k, x in trace)
            changed += moved
            with_admit += has_admit
            with_new += has_new
            mismatches += moved != has_new
            finals.add(final)
    return {'kind': 'trace', 'items': items, 'max_len': max_len, 'init_mask': mask, 'traces': total, 'changed': changed,
            'with_admit': with_admit, 'with_new_admit': with_new, 'mismatches': mismatches, 'distinct_final_states': len(finals)}


def footprint_record(kind):
    probe = empty([0])
    return {'kind': 'footprint', 'op': kind, 'new_item_fields': fields_changed(probe, step(probe, (kind, 1))),
            'old_item_fields': fields_changed(probe, step(probe, (kind, 0)))}


def pair_record(a, b):
    contexts = 0
    min_len = -1
    for length in range(4):
        for tau in product(OPS, repeat=length):
            s = run(empty(), tau)
            hits = sum(1 for x in ITEMS if step(s, (a, x)) != step(s, (b, x)))
            if hits and min_len < 0:
                min_len = length
            if length <= 2:
                contexts += hits
    return {'kind': 'pair', 'a': a, 'b': b, 'min_len': min_len, 'contexts': contexts}


def conflation_record(name):
    a_kind, b_kind = CONFLATIONS[name]
    stepper = conflated(a_kind, b_kind)
    for length in range(1, 5):
        witness = None
        count = 0
        for trace in product(OPS, repeat=length):
            if run(empty(), trace) != run(empty(), trace, stepper):
                count += 1
                if witness is None:
                    witness = trace
        if witness is not None:
            six, conf = run(empty(), witness), run(empty(), witness, stepper)
            return {'kind': 'conflation', 'name': name, 'min_len': length, 'witness_count': count,
                    'witness': ['%s:%d' % op for op in witness], 'six_state': listed(six), 'conflated_state': listed(conf),
                    'differing_fields': fields_changed(six, conf), 'admitted_differs': six[3] != conf[3]}
    raise ValueError('no witness for ' + name)


READING_MODELS = {'supply_includes_admit': ('supply', 'admit'), 'admit_includes_supply': ('admit', 'supply')}


def reading_record(token, name):
    stepper = conflated(*READING_MODELS[name])
    tl, tf = [('supply', token)], [('supply', token), ('admit', token)]
    six_l, six_f = run(empty(), tl)[3], run(empty(), tf)[3]
    conf_l, conf_f = run(empty(), tl, stepper)[3], run(empty(), tf, stepper)[3]
    return {'kind': 'reading', 'token': token, 'conflation': name, 'six_L_admitted': sorted(six_l), 'six_F_admitted': sorted(six_f),
            'conflated_L_admitted': sorted(conf_l), 'conflated_F_admitted': sorted(conf_f),
            'six_separated': six_l != six_f, 'conflated_separated': conf_l != conf_f}


def record(case):
    kind = case[0]
    if kind == 'trace':
        return trace_record(case[1], case[2], case[3])
    if kind == 'footprint':
        return footprint_record(case[1])
    if kind == 'pair':
        return pair_record(case[1], case[2])
    if kind == 'conflation':
        return conflation_record(case[1])
    if kind == 'reading':
        return reading_record(case[1], case[2])
    raise ValueError('unknown case kind ' + str(kind))


def certificate(cases=CASES):
    return {'records': [record(c) for c in cases]}


def _items(xs):
    return '+'.join(str(x) for x in xs) or '-'


def _state(st):
    return '|'.join('%s:%s' % (name, _items(v)) for name, v in zip('mSdarO', st))


def _line(r):
    k = r['kind']
    if k == 'trace':
        return '\t'.join(['trace', str(r['items']), str(r['max_len']), str(r['init_mask']), str(r['traces']), str(r['changed']),
                          str(r['with_admit']), str(r['with_new_admit']), str(r['mismatches']), str(r['distinct_final_states'])])
    if k == 'footprint':
        return '\t'.join(['footprint', r['op'], r['new_item_fields'], r['old_item_fields']])
    if k == 'pair':
        return '\t'.join(['pair', r['a'], r['b'], str(r['min_len']), str(r['contexts'])])
    if k == 'conflation':
        return '\t'.join(['conflation', r['name'], str(r['min_len']), str(r['witness_count']), ','.join(r['witness']), r['differing_fields'],
                          str(int(r['admitted_differs'])), _state(r['six_state']), _state(r['conflated_state'])])
    return '\t'.join(['reading', str(r['token']), r['conflation'], _items(r['six_L_admitted']), _items(r['six_F_admitted']),
                      _items(r['conflated_L_admitted']), _items(r['conflated_F_admitted']),
                      str(int(r['six_separated'])), str(int(r['conflated_separated']))])


def wire_lines(data):
    return [_line(r) for r in data['records']]


def public_tsv(cases=CASES):
    return ''.join('\t'.join(str(x) for x in c) + '\n' for c in cases)
