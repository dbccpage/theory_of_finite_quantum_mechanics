"""Independent checker for PG-INERT-DIAMOND.

Does not import the producer and does not enumerate traces one by one. It counts all event traces of length <= L by
dynamic programming over a joint state: the model run, the model run on the supply-deleted trace, the model run
started after the literal supply, the rival run (supply admits) and its prefixed twin, plus the flags
(inscribed, supply-only, root-only, first event). States are strings (data as a digit string, forms as a digit
string), a different representation from the producer's tuples. AuthorityEffect: None.
"""
import sys
from collections import Counter
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = next((p for p in HERE.parents if (p / 'dag/pfp/prepare_stage.py').is_file()),
            Path(r'C:\Users\a343o\source\repos\theory_of_finite_quantum_mechanics\.claude\worktrees\unified-dag\.claude\worktrees\pfp-batch-01'))
sys.path.insert(0, str(ROOT / 'dag/pfp'))
import exact_json as E  # noqa: E402

TASK = 'PG-INERT-DIAMOND'
COUNT_KEYS = ['traces', 'refused', 'rooted_ok', 'supply_deletion_changes', 'supply_only_traces', 'supply_only_moved', 'moved',
              'reachable_states', 'with_coproduct', 'inscribed_no_coproduct', 'inscribed_with_coproduct', 'uninscribed_with_coproduct',
              'rooted_with_coproduct', 'rooted_without_coproduct', 'root_traces', 'root_traces_with_coproduct',
              'mention_prefix_diff', 'rival_mention_prefix_diff', 'rival_supply_only_moved',
              'rooted_later_supply_changes', 'root_omission_visible', 'rooted_refuses_unrooted_accepted']
KEYS = {'input'} | set(COUNT_KEYS)
EVENTS = [(k, x) for k in 'sa' for x in range(3)] + [('f', 0), ('f', 1)]
EMPTY = ('', '')


def require(condition, message):
    if not condition:
        raise ValueError(message)


def is_int(x):
    return type(x) is int


def model(state, ev, rival=False):
    """One event on a state ('data digits', 'form digits'); None means refused. rival: supply admits."""
    if state is None:
        return None
    data, forms = state
    kind, x = ev
    if kind == 'f':
        return None if x == 0 else (data, forms + str(x))
    if kind == 's' and not rival:
        return state
    return state if str(x) in data else (data + str(x), forms)


def coproduct(state):
    return ('1' in state[0]) and ('2' in state[0])


def expected(max_len):
    out = {k: 0 for k in COUNT_KEYS}
    start = (EMPTY, EMPTY, model(EMPTY, ('s', 0)), EMPTY, model(EMPTY, ('s', 0), True), False, True, 0, True, 0)
    level = Counter({start: 1})
    finals = set()
    for n in range(max_len + 1):
        for key, count in level.items():
            run, filt, prefixed, rrun, rprefixed, inscribed, supply_only, first, root_only, second = key
            out['traces'] += count
            out['supply_deletion_changes'] += count * (run != filt)
            if supply_only:
                out['supply_only_traces'] += count
                out['supply_only_moved'] += count * (run != EMPTY)
                if n >= 1:
                    out['rival_supply_only_moved'] += count * (rrun != EMPTY)
            rooted = first == 1 and run is not None
            if first == 1:
                # kept = first event + non-supply events: the supply-deleted run `filt` is its outcome, since the first event is an identity
                out['rooted_later_supply_changes'] += count * (run != filt)
                # omitting the first event leaves a history that is accepted only if it again begins with the literal supply
                if run is not None and not second == 1:
                    out['root_omission_visible'] += count
            if run is not None and first != 1:
                out['rooted_refuses_unrooted_accepted'] += count
            out['rooted_ok'] += count * rooted
            if root_only:
                out['root_traces'] += count
            out['mention_prefix_diff'] += count * (run != prefixed)
            out['rival_mention_prefix_diff'] += count * (rrun != rprefixed)
            if run is None:
                out['refused'] += count
                continue
            finals.add(run)
            out['moved'] += count * (run != EMPTY)
            cop = coproduct(run)
            out['with_coproduct'] += count * cop
            if root_only and cop:
                out['root_traces_with_coproduct'] += count
            if inscribed:
                out['inscribed_with_coproduct' if cop else 'inscribed_no_coproduct'] += count
            elif cop:
                out['uninscribed_with_coproduct'] += count
            if rooted:
                out['rooted_with_coproduct' if cop else 'rooted_without_coproduct'] += count
        if n == max_len:
            break
        nxt = Counter()
        for key, count in level.items():
            run, filt, prefixed, rrun, rprefixed, inscribed, supply_only, first, root_only, second = key
            for ev in EVENTS:
                is_supply = ev[0] == 's'
                new = (model(run, ev), filt if is_supply else model(filt, ev), model(prefixed, ev), model(rrun, ev, True),
                       model(rprefixed, ev, True), inscribed or ev == ('s', 0), supply_only and is_supply,
                       first if first else (1 if ev == ('s', 0) else 2), root_only and ev in (('s', 0), ('a', 0)),
                       second if second else (0 if not first else (1 if ev == ('s', 0) else 2)))
                nxt[new] += count
        level = nxt
    out['reachable_states'] = len(finals)
    out['input'] = [max_len]
    return out


def check(request, candidate):
    try:
        _, cand, public = E.bound(request, candidate, TASK)
        data = cand['data']
        require(type(data) is dict and set(data) == {'records'} and type(data['records']) is list, 'G1_SCHEMA:data')
        cases = [tuple(c) for c in public['cases']]
        records = data['records']
        require(len(records) == len(cases), 'G2_COVERAGE:record_count')
        seen = []
        for r in records:
            require(type(r) is dict and set(r) == KEYS, 'G1_SCHEMA:record_keys')
            require(type(r['input']) is list and len(r['input']) == 1 and all(is_int(x) and x >= 0 for x in r['input']), 'G1_SCHEMA:input')
            for key in COUNT_KEYS:
                require(is_int(r[key]), 'G1_SCHEMA:int_' + key)
            seen.append(tuple(r['input']))
            want = expected(*r['input'])
            for key in COUNT_KEYS:
                require(r[key] == want[key], 'G3_WITNESS:' + key)
            # Consistency of the record with the definition: inertness and independence.
            require(r['supply_deletion_changes'] == 0 and r['supply_only_moved'] == 0, 'G3_WITNESS:supply_is_inert')
            require(r['mention_prefix_diff'] == 0, 'G3_WITNESS:mention_count_irrelevant')
            require(r['root_traces_with_coproduct'] == 0, 'G3_WITNESS:root_only_histories_have_no_coproduct')
            require(r['rooted_later_supply_changes'] == 0, 'G3_WITNESS:later_supplies_inert_in_rooted_replay')
            require(r['rooted_refuses_unrooted_accepted'] > 0, 'G3_WITNESS:rooted_gate_is_not_vacuous')
            if r['input'][0] >= 1:
                require(r['root_omission_visible'] > 0, 'G3_WITNESS:root_supply_is_a_precondition_of_the_rooted_replay')
            if r['input'][0] >= 2:
                require(r['uninscribed_with_coproduct'] > 0, 'G3_WITNESS:coproduct_without_inscription_exists')
            if r['input'][0] >= 3:
                require(r['rooted_with_coproduct'] > 0 and r['inscribed_no_coproduct'] > 0, 'G3_WITNESS:inscription_does_not_determine_coproduct')
                require(r['rival_mention_prefix_diff'] > 0, 'G3_WITNESS:inertness_is_a_rule_not_spelling')
        require(sorted(seen) == sorted(cases), 'G2_COVERAGE:inputs_are_the_public_cases')
        return {'records_checked': len(records)}
    except (KeyError, TypeError, IndexError, AttributeError) as error:
        raise ValueError('G1_SCHEMA:malformed ' + repr(error))


if __name__ == '__main__':
    import json
    print(json.dumps(check(sys.argv[1], sys.argv[2])))
