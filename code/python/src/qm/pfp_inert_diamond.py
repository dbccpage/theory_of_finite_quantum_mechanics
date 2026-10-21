"""The inert inscription <>: exhaustive event traces of a finite admission model.

Producer for PFP batch 01, node PG-INERT-DIAMOND (a DEFINITION node: the honest result is consistency and
independence of the definition, not a proof of it). Exact integers only.
Tokens 0 = "<>" (the literal), 1 = a Difference datum, 2 = a Structure datum. Events: supply t (mention),
admit t (datum admission, re-admission designates), form n (admit a form of arity n; arity 0 is refused).
Supply never changes the state (rule L1, a stipulation: the zero counts of supply-deletion and prefix columns follow from it by definition and corroborate the implementation, not the hypothesis); the rival rule makes supply admit. The rooted replay (first event must be supply of <>) is a separate gate. Every
trace of length <= L over the 8 events is replayed. Finite instances; the general statements are the Lean
module InertDiamond. AuthorityEffect: None.
"""
from itertools import product

TOKENS = (0, 1, 2)
CLS = {0: None, 1: 'diff', 2: 'struct'}
EVENTS = [('s', 0), ('s', 1), ('s', 2), ('a', 0), ('a', 1), ('a', 2), ('f', 0), ('f', 1)]
INIT = ((), ())
SUPPLY0 = ('s', 0)
CASES = [(0,), (1,), (2,), (3,), (4,), (5,)]
FIELDS = ['traces', 'refused', 'rooted_ok', 'supply_deletion_changes', 'supply_only_traces', 'supply_only_moved', 'moved',
          'reachable_states', 'with_coproduct', 'inscribed_no_coproduct', 'inscribed_with_coproduct', 'uninscribed_with_coproduct',
          'rooted_with_coproduct', 'rooted_without_coproduct', 'root_traces', 'root_traces_with_coproduct',
          'mention_prefix_diff', 'rival_mention_prefix_diff', 'rival_supply_only_moved',
          'rooted_later_supply_changes', 'root_omission_visible', 'rooted_refuses_unrooted_accepted']


def admit(state, t):
    data, forms = state
    return state if t in data else (data + (t,), forms)


def step(state, ev):
    """The model: supply is the identity; admit designates; form 0 is refused (None)."""
    kind, x = ev
    if kind == 's':
        return state
    if kind == 'a':
        return admit(state, x)
    return None if x < 1 else (state[0], state[1] + (x,))


def rival_step(state, ev):
    """Rival rule: supply of a token admits it. Everything else as in the model."""
    return admit(state, ev[1]) if ev[0] == 's' else step(state, ev)


def replay(trace, state=INIT, stepper=step):
    for ev in trace:
        state = stepper(state, ev)
        if state is None:
            return None
    return state


def rooted_replay(trace):
    """Rooted replay (the Rust gate): the first event must be the supply of <>; the rest is replayed from the empty state."""
    return replay(trace[1:]) if trace and trace[0] == SUPPLY0 else None


def has_coproduct(state):
    classes = {CLS[t] for t in state[0]}
    return 'diff' in classes and 'struct' in classes


def record(max_len):
    r = {k: 0 for k in FIELDS}
    finals = set()
    for n in range(max_len + 1):
        for trace in product(EVENTS, repeat=n):
            r['traces'] += 1
            final = replay(trace)
            filtered = replay([e for e in trace if e[0] != 's'])
            r['supply_deletion_changes'] += final != filtered
            inscribed = ('s', 0) in trace
            supply_only = all(e[0] == 's' for e in trace)
            if supply_only:
                r['supply_only_traces'] += 1
                r['supply_only_moved'] += final != INIT
                if n >= 1:
                    r['rival_supply_only_moved'] += replay(trace, INIT, rival_step) != INIT
            rooted_out = rooted_replay(trace)
            rooted = n >= 1 and trace[0] == SUPPLY0 and final is not None
            assert (rooted_out is not None) == rooted
            if n >= 1 and trace[0] == SUPPLY0:
                kept_first = [trace[0]] + [e for e in trace[1:] if e[0] != 's']
                r['rooted_later_supply_changes'] += rooted_out != rooted_replay(kept_first)
                r['root_omission_visible'] += rooted_out is not None and rooted_replay(trace[1:]) is None
            r['rooted_refuses_unrooted_accepted'] += rooted_out is None and final is not None
            r['rooted_ok'] += rooted
            root_only = all(e in (('s', 0), ('a', 0)) for e in trace)
            if root_only:
                r['root_traces'] += 1
            after_prefix = replay(trace, step(INIT, ('s', 0)))
            r['mention_prefix_diff'] += final != after_prefix
            rival_after = replay(trace, rival_step(INIT, ('s', 0)), rival_step)
            r['rival_mention_prefix_diff'] += replay(trace, INIT, rival_step) != rival_after
            if final is None:
                r['refused'] += 1
                continue
            finals.add(final)
            r['moved'] += final != INIT
            cop = has_coproduct(final)
            r['with_coproduct'] += cop
            if root_only and cop:
                r['root_traces_with_coproduct'] += 1
            if inscribed:
                r['inscribed_with_coproduct' if cop else 'inscribed_no_coproduct'] += 1
            elif cop:
                r['uninscribed_with_coproduct'] += 1
            if rooted:
                r['rooted_with_coproduct' if cop else 'rooted_without_coproduct'] += 1
    r['reachable_states'] = len(finals)
    return dict({'input': [max_len]}, **r)


def certificate(cases=CASES):
    return {'records': [record(*c) for c in cases]}


def wire_lines(data):
    return ['\t'.join(['inert'] + [str(x) for x in r['input']] + [str(r[f]) for f in FIELDS]) for r in data['records']]


def public_tsv(cases=CASES):
    return ''.join('inert\t%d\n' % c for c in cases)
