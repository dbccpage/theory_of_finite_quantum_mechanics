"""Independent checker for PG-SN-OFF-IMAGE-REFUSAL.

Recomputes every record without importing the producer and with a different representation: presentations are the
wire strings of the source grammar (`<>`, `<a>`, `<ab>`, `<a->b>`, `[a,b]`, `u_N<body>`, `r_N<body>`, `NON_DESCENT`),
the retraction is a regular-expression parser over those strings, and the round trip s(r(p)) = p is tested literally
by re-lifting the parsed result and comparing strings. AuthorityEffect: None.
"""
import json
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = next((p for p in HERE.parents if (p / 'dag/pfp/prepare_stage.py').is_file()),
            Path(r'C:\Users\a343o\source\repos\theory_of_finite_quantum_mechanics\.claude\worktrees\unified-dag\.claude\worktrees\pfp-batch-01'))
sys.path.insert(0, str(ROOT / 'dag/pfp'))
import exact_json as E  # noqa: E402

TASK = 'PG-SN-OFF-IMAGE-REFUSAL'
FIELDS = ['universe', 'accepted', 'refused', 'image_size', 'lift_collisions', 'iff_violations', 'payload_failures', 'roundtrip_holds',
          'roundtrip_fails', 'stage_mismatch_refused', 'long_body_refused', 'lax_law_holds', 'lax_refused']
KEYS = {'kind', 'input'} | set(FIELDS)
TOY_FIELDS = ['points', 'on_image', 'refused', 'law_failures', 'sound_failures']
TOY_KEYS = {'kind', 'input'} | set(TOY_FIELDS)


def require(condition, message):
    if not condition:
        raise ValueError(message)


def is_int(x):
    return type(x) is int


def letters(g):
    return [chr(97 + i) for i in range(g)]


def base_wires(g):
    a = letters(g)
    out = ['<>'] + ['<%s>' % x for x in a]
    out += ['<%s%s>' % (x, y) for x in a for y in a]
    out += ['<%s->%s>' % (x, y) for x in a for y in a]
    out += ['[%s,%s]' % (x, y) for x in a for y in a]
    return out


def lift_wire(n, wire):
    body = '' if wire == '<>' else wire[1:-1]
    return 'u_%d<%s>' % (n, body)


def retract_wire(n, text):
    m = re.fullmatch(r'u_(\d+)<(.*)>', text)
    if not m or int(m.group(1)) != n:
        return None
    body = m.group(2)
    if body == '':
        return '<>'
    if re.fullmatch(r'[a-z]{1,2}', body):
        return '<%s>' % body
    mm = re.fullmatch(r'([a-z])->([a-z])', body)
    if mm:
        return '<%s->%s>' % (mm.group(1), mm.group(2))
    mm = re.fullmatch(r'([a-z]),([a-z])', body)
    if mm:
        return '[%s,%s]' % (mm.group(1), mm.group(2))
    return None


def lax_retract(n, text):
    out = retract_wire(n, text)
    return '<>' if out is None else out


def all_bodies(g, maxlen):
    a = letters(g)
    out = ['%s->%s' % (x, y) for x in a for y in a] + ['%s,%s' % (x, y) for x in a for y in a] + ['']
    layer = ['']
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


def expected(g, stages, maxlen, n):
    base = base_wires(g)
    uni = universe(g, stages, maxlen)
    image = {lift_wire(n, b): b for b in base}
    accepted = iff_viol = payload_fail = rt_holds = lax_refused = long_refused = 0
    for p in uni:
        res = retract_wire(n, p)
        off = p not in image
        if (res is None) != off:
            iff_viol += 1
        if lax_retract(n, p) is None:
            lax_refused += 1
        if res is not None:
            accepted += 1
            if image.get(p) != res:
                payload_fail += 1
            if lift_wire(n, res) == p:
                rt_holds += 1
        elif re.fullmatch(r'u_%d<[a-z]{3,}>' % n, p):
            long_refused += 1
    mismatch = sum(1 for m in range(stages) if m != n for b in base if retract_wire(n, lift_wire(m, b)) is None)
    lax_law_holds = sum(1 for b in base if lax_retract(n, lift_wire(n, b)) == b)
    return {'kind': 'offimage', 'input': [g, stages, maxlen, n], 'universe': len(uni), 'accepted': accepted, 'refused': len(uni) - accepted,
            'image_size': len(image), 'lift_collisions': len(base) - len(image), 'iff_violations': iff_viol, 'payload_failures': payload_fail,
            'roundtrip_holds': rt_holds, 'roundtrip_fails': len(uni) - rt_holds, 'stage_mismatch_refused': mismatch,
            'long_body_refused': long_refused, 'lax_law_holds': lax_law_holds, 'lax_refused': lax_refused}


def expected_toy(k, c):
    """Section x -> c*x into 0..c*k-1. A point y is on the image iff c divides y; the refusing retraction accepts
    exactly those (round trip s(r y) = y), so the counts are k and (c-1)*k with no law or soundness failure."""
    points = c * k
    on_image = sum(1 for y in range(points) if y % c == 0)
    refused = sum(1 for y in range(points) if y % c != 0)

    def retract(y):
        q, rem = divmod(y, c)
        return q if rem == 0 else None

    law_failures = sum(1 for x in range(k) if retract(c * x) != x)
    sound_failures = sum(1 for y in range(points) if retract(y) is not None and c * retract(y) != y)
    return {'kind': 'toy', 'input': [k, c], 'points': points, 'on_image': on_image, 'refused': refused,
            'law_failures': law_failures, 'sound_failures': sound_failures}


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
            require(type(r) is dict and r.get('kind') in ('offimage', 'toy'), 'G1_SCHEMA:kind')
            require(type(r['input']) is list and all(is_int(x) and x >= 0 for x in r['input']), 'G1_SCHEMA:input')
            if r['kind'] == 'toy':
                require(set(r) == TOY_KEYS and len(r['input']) == 2, 'G1_SCHEMA:toy_keys')
                require(all(is_int(r[f]) for f in TOY_FIELDS), 'G1_SCHEMA:toy_fields')
                k, c = r['input']
                require(k <= 8 and 1 <= c <= 6, 'G1_SCHEMA:toy_range')
                seen.append(['toy'] + list(r['input']))
                want = expected_toy(k, c)
                for f in TOY_FIELDS:
                    require(r[f] == want[f], 'G3_WITNESS:toy_' + f)
                require(r['on_image'] + r['refused'] == r['points'], 'G3_WITNESS:toy_partition')
                require(r['law_failures'] == 0 and r['sound_failures'] == 0, 'G3_WITNESS:toy_section_retraction')
                continue
            require(set(r) == KEYS and len(r['input']) == 4, 'G1_SCHEMA:record_keys')
            g, stages, maxlen, n = r['input']
            require(g <= 8 and 1 <= stages <= 5 and 2 <= maxlen <= 4 and n < stages, 'G1_SCHEMA:input_range')
            require(all(is_int(r[f]) for f in FIELDS), 'G1_SCHEMA:fields')
            seen.append(['offimage'] + list(r['input']))
            want = expected(g, stages, maxlen, n)
            for f in FIELDS:
                require(r[f] == want[f], 'G3_WITNESS:' + f)
            # theorem-level consistency of the candidate itself
            require(r['iff_violations'] == 0 and r['payload_failures'] == 0, 'G3_WITNESS:refusal_is_exactly_off_image')
            require(r['accepted'] == r['image_size'] == r['roundtrip_holds'], 'G3_WITNESS:accepted_is_the_image')
            require(r['roundtrip_fails'] == r['refused'], 'G3_WITNESS:roundtrip_fails_exactly_on_refused')
            require(r['lift_collisions'] == 0, 'G3_WITNESS:section_lift_injective')
            require(r['lax_law_holds'] == r['image_size'] and r['lax_refused'] == 0, 'G3_WITNESS:lax_obeys_law_but_refuses_nothing')
        require(sorted(seen) == sorted(cases), 'G2_COVERAGE:inputs_are_the_public_cases')
        return {'records_checked': len(records)}
    except (KeyError, TypeError, IndexError, AttributeError) as error:
        raise ValueError('G1_SCHEMA:malformed ' + repr(error))

if __name__ == '__main__':
    print(json.dumps(check(sys.argv[1], sys.argv[2])))
