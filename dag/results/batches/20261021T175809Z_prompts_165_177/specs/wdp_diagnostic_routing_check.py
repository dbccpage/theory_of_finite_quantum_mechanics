"""Independent checker for PG-WDP-DIAGNOSTIC-NOT-ROUTING.

Recomputes every record from the public input lines without importing the producer, from a SEPARATE transcription of the
source tables (grouped by target instead of keyed by status) and by different algorithms: the fiber classifier is rebuilt as
'valid-count test then case split' instead of nested early returns; the policy summary enumerates all 343 functions
{0,1,2} -> 7 routes; the determination matrix is decided on the fibres of the source map; the cell counts are taken over the
full 3x7 and 4x7 products. Every leaf of every record is compared with strict type equality. The source defines no map from
the diagnostic class to a routing terminal except the partial composite run.rs tag + terminal_routing.json. AuthorityEffect: None.
"""
import sys
from itertools import product
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = next((p for p in HERE.parents if (p / 'dag/pfp/prepare_stage.py').is_file()),
            Path(r'C:\Users\a343o\source\repos\theory_of_finite_quantum_mechanics\.claude\worktrees\unified-dag\.claude\worktrees\pfp-batch-01'))
sys.path.insert(0, str(ROOT / 'dag/pfp'))
import exact_json as E  # noqa: E402

TASK = 'PG-WDP-DIAGNOSTIC-NOT-ROUTING'

# --- separate transcription: status order (ALL_TERMINAL_STATUSES) and route groups -------------------------------------
STATUS_ORDER = ('ExactRuleDerived UniqueOutputDerived NoRuleInSearchClass NonUniqueOutput EnumeratorFailure Refused '
                'LabelConflictsWithDerivation BudgetUnknown InvalidProposal OperatorConflict UnknownSector NoDescentYet '
                'LabelOnlyUncertified LiftRequired ParseRefused ReplayMismatch PolicyAmbiguous NoPacket VerifierDisabled '
                'SearchIncomplete PolicyUnderspecified').split()
ROUTE_ORDER = 'CheckPassed RequiresLift Repair Refusal NoRule BudgetUnknown Refused'.split()
ROUTE_GROUPS = {
    'CheckPassed': 'ExactRuleDerived UniqueOutputDerived'.split(),
    'RequiresLift': ['LiftRequired'],
    'Repair': ('NonUniqueOutput EnumeratorFailure UnknownSector NoDescentYet LabelOnlyUncertified ReplayMismatch PolicyAmbiguous '
               'VerifierDisabled SearchIncomplete PolicyUnderspecified').split(),
    'Refusal': ['ParseRefused', 'NoPacket'],
    'NoRule': ['NoRuleInSearchClass'],
    'BudgetUnknown': ['BudgetUnknown'],
    'Refused': 'Refused LabelConflictsWithDerivation InvalidProposal OperatorConflict'.split(),
}
RESIDUAL_GROUPS = {
    'Exact': ['ExactRuleDerived', 'UniqueOutputDerived'],
    'ClosedSurvivor': ['NoRuleInSearchClass'],
    'Refused': 'Refused LabelConflictsWithDerivation InvalidProposal OperatorConflict ParseRefused'.split(),
}  # 'Open' is every status in none of the listed groups
AUTH_GROUPS = {
    'Certifiable': ['ExactRuleDerived', 'UniqueOutputDerived'],
    'Refused': 'Refused LabelConflictsWithDerivation InvalidProposal OperatorConflict'.split(),
}  # 'Uncertified' is the rest
PFP_ORDER = ('Exact Verified VerifiedWithResiduals StabilizedSurvivor NeedsExternalOracle OpenObstruction BlockedByEvidence '
             'InfrastructureFailure Refused BudgetExhausted').split()
PFP_GROUPS = {'CheckPassed': PFP_ORDER[0:3], 'RequiresLift': PFP_ORDER[3:5], 'Refusal': PFP_ORDER[5:8], 'Refused': ['Refused'],
              'BudgetUnknown': ['BudgetExhausted']}
DIAG_ORDER = ['ExactClass', 'ClosedResidual', 'ActiveClosureFailure']
DIAG_TAG = {'ExactClass': 'ExactRepair', 'ClosedResidual': 'StabilizedSurvivor', 'ActiveClosureFailure': 'OpenObstruction'}
SUMS = ['residual_routing', 'determination', 'policies', 'diag_cells', 'fiber_routes', 'fiber_statuses', 'image_sizes', 'authority']
AGR = ['-', '00', '01', '10', '11']


def require(condition, message):
    if not condition:
        raise ValueError(message)


def strict_eq(a, b):
    if type(a) is not type(b):
        return False
    if isinstance(a, list):
        return len(a) == len(b) and all(strict_eq(x, y) for x, y in zip(a, b))
    if isinstance(a, dict):
        return a.keys() == b.keys() and all(strict_eq(a[k], b[k]) for k in a)
    return a == b


def invert(groups, order, rest=None):
    table = {}
    for target, members in groups.items():
        for m in members:
            require(m not in table, 'transcription clash ' + m)
            table[m] = target
    for m in order:
        if m not in table:
            table[m] = rest
    return table


ROUTE_OF = invert(ROUTE_GROUPS, STATUS_ORDER)
RESID_OF = invert(RESIDUAL_GROUPS, STATUS_ORDER, 'Open')
AUTH_OF = invert(AUTH_GROUPS, STATUS_ORDER, 'Uncertified')
PFP_OF = invert(PFP_GROUPS, PFP_ORDER)
assert all(v is not None for v in ROUTE_OF.values()) and len(ROUTE_OF) == 21 and len(PFP_OF) == 10


def rel_of(i, c, s):
    table = {(False, False, False): 'outsideProfile', (False, False, True): 'outsideProfile',
             (False, True, False): 'outsideProfile', (False, True, True): 'outsideProfile',
             (True, True, False): 'refuted', (True, True, True): 'refuted',
             (True, False, True): 'supported', (True, False, False): 'undetermined'}
    return table[(i, c, s)]


def fiber(sel, cand, out, exh, agr, ver):
    if not sel:
        return 'NoPacket' if (cand, out, exh) == (0, 0, False) else 'ERR'
    if not ver:
        return 'VerifierDisabled'
    valid = (cand == 0 and out == 0) or (cand > 0 and 1 <= out <= cand)
    if not valid:
        return 'ERR'
    if cand == 0:
        return 'NoRuleInSearchClass' if exh else 'SearchIncomplete'
    if cand == 1:
        return 'ExactRuleDerived'
    if out != 1:
        return 'NonUniqueOutput'
    coherent, replay = {'-': (True, True), '00': (False, False), '01': (False, True), '10': (True, False), '11': (True, True)}[agr]
    return 'PolicyAmbiguous' if not coherent else 'ReplayMismatch' if not replay else 'UniqueOutputDerived'


def fib_inputs():
    return [(bool(s), c, o, bool(x), a, bool(v)) for s, c, o, x, a, v in product((0, 1), range(4), range(4), (0, 1), AGR, (0, 1))]


def fib_table():
    return [(t, fiber(*t)) for t in fib_inputs()]


_FIB = fib_table()


def functional(src, dst):
    """src -> dst is a function on the 21 statuses iff each src-fibre has one dst value."""
    for a in set(src.values()):
        if len({dst[s] for s in STATUS_ORDER if src[s] == a}) != 1:
            return 0
    return 1


def summary(name):
    if name == 'residual_routing':
        hit = [(a, b) for a, b in product(['Exact', 'ClosedSurvivor', 'Open', 'Refused'], ROUTE_ORDER)
               if any(RESID_OF[s] == a and ROUTE_OF[s] == b for s in STATUS_ORDER)]
        return [4 * 7, len(hit)], sorted('%s:%s' % h for h in hit)
    if name == 'determination':
        axes = {'residual': RESID_OF, 'route': ROUTE_OF, 'auth': AUTH_OF}
        order = [('residual', 'route'), ('route', 'residual'), ('residual', 'auth'), ('auth', 'residual'), ('route', 'auth'), ('auth', 'route')]
        return [], ['%s->%s:%d' % (a, b, functional(axes[a], axes[b])) for a, b in order]
    if name == 'policies':
        funcs = list(product(range(7), repeat=3))
        return [3, 7, len(funcs), sum(1 for f in funcs if len(set(f)) == 3), sum(1 for f in funcs if set(f) == set(range(7))),
                len({(f[0], f[1]) for f in funcs}), 3 * 7], []
    if name == 'diag_cells':
        cells = [(d, r) for d in DIAG_ORDER for r in ROUTE_ORDER]
        routed = [(d, r) for d, r in cells if DIAG_TAG[d] in PFP_OF and PFP_OF[DIAG_TAG[d]] == r]
        unrouted = [d for d in DIAG_ORDER if DIAG_TAG[d] not in PFP_OF]
        return [len(cells), len(routed), len(unrouted), len(cells) - len(routed)], sorted('%s:%s' % c for c in routed)
    if name == 'fiber_routes':
        ok = [s for _, s in _FIB if s != 'ERR']
        reached = sorted({ROUTE_OF[s] for s in ok})
        return [len(_FIB), len(_FIB) - len(ok), len(ok), len(reached)], reached
    if name == 'fiber_statuses':
        got = {}
        for _, s in _FIB:
            if s != 'ERR':
                got[s] = got.get(s, 0) + 1
        return [len(got)], sorted('%s:%d' % kv for kv in got.items())
    if name == 'image_sizes':
        fib_img = {ROUTE_OF[s] for _, s in _FIB if s != 'ERR'}
        pfp_img = set(PFP_OF.values())
        miss = ['pfp-missing:' + r for r in ROUTE_ORDER if r not in pfp_img] + ['fiber-missing:' + r for r in ROUTE_ORDER if r not in fib_img]
        rel_img = {rel_of(*t) for t in product((False, True), repeat=3)}
        return [len(set(ROUTE_OF.values())), len(pfp_img), len(fib_img), len(rel_img)], sorted(miss)
    if name == 'authority':
        tags = [AUTH_OF[s] for s in STATUS_ORDER]
        bearing = [s for s in STATUS_ORDER if s in ('ExactRuleDerived', 'UniqueOutputDerived')]
        certified = lambda s, w: w and s in bearing  # noqa: E731
        return [len(STATUS_ORDER), tags.count('Certifiable'), tags.count('Refused'), tags.count('Uncertified'), len(bearing),
                sum(1 for s in STATUS_ORDER if certified(s, False)), sum(1 for s in STATUS_ORDER if certified(s, True))], []
    raise ValueError('unknown summary ' + name)


def flag(x):
    require(type(x) is bool, 'G1_SCHEMA:flag')
    return str(int(x))


def line_of(r):
    """The public input line a record answers (rebuilt from the record's own input fields)."""
    k = r['kind']
    if k in ('stat', 'pfp', 'diag'):
        require(type(r['i']) is int, 'G1_SCHEMA:i')
        return '%s\t%d' % (k, r['i'])
    if k == 'rel':
        return 'rel\t%s\t%s\t%s' % (flag(r['in_profile']), flag(r['contradicted']), flag(r['supported']))
    if k == 'fib':
        require(type(r['cand']) is int and type(r['out']) is int and type(r['agreement']) is str, 'G1_SCHEMA:fib')
        return 'fib\t%s\t%d\t%d\t%s\t%s\t%s' % (flag(r['selected']), r['cand'], r['out'], flag(r['exhaustive']), r['agreement'], flag(r['verifier']))
    if k == 'sum':
        require(type(r['name']) is str, 'G1_SCHEMA:name')
        return 'sum\t' + r['name']
    raise ValueError('G1_SCHEMA:kind')


def expected(line):
    f = line.split('\t')
    k = f[0]
    if k == 'stat':
        s = STATUS_ORDER[int(f[1])]
        return {'kind': 'stat', 'i': int(f[1]), 'name': s, 'route': ROUTE_OF[s], 'residual': RESID_OF[s], 'auth': AUTH_OF[s],
                'authterm': s in ('ExactRuleDerived', 'UniqueOutputDerived')}
    if k == 'pfp':
        p = PFP_ORDER[int(f[1])]
        return {'kind': 'pfp', 'i': int(f[1]), 'name': p, 'route': PFP_OF[p]}
    if k == 'diag':
        d = DIAG_ORDER[int(f[1])]
        return {'kind': 'diag', 'i': int(f[1]), 'name': d, 'run_tag': DIAG_TAG[d], 'route': PFP_OF.get(DIAG_TAG[d], '-'),
                'cert_eligible': d == 'ExactClass'}
    if k == 'rel':
        i, c, s = (x == '1' for x in f[1:4])
        return {'kind': 'rel', 'in_profile': i, 'contradicted': c, 'supported': s, 'status': rel_of(i, c, s)}
    if k == 'fib':
        t = (f[1] == '1', int(f[2]), int(f[3]), f[4] == '1', f[5], f[6] == '1')
        s = fiber(*t)
        return {'kind': 'fib', 'selected': t[0], 'cand': t[1], 'out': t[2], 'exhaustive': t[3], 'agreement': t[4], 'verifier': t[5],
                'status': s, 'route': '-' if s == 'ERR' else ROUTE_OF[s]}
    if k == 'sum':
        ints, items = summary(f[1])
        return {'kind': 'sum', 'name': f[1], 'ints': ints, 'items': items}
    raise ValueError('G1_SCHEMA:kind')


def expected_public_lines():
    lines = ['stat\t%d' % i for i in range(21)] + ['pfp\t%d' % i for i in range(10)] + ['diag\t%d' % i for i in range(3)]
    lines += ['rel\t%d\t%d\t%d' % t for t in product((0, 1), repeat=3)]
    lines += ['fib\t%d\t%d\t%d\t%d\t%s\t%d' % (int(t[0]), t[1], t[2], int(t[3]), t[4], int(t[5])) for t in fib_inputs()]
    lines += ['sum\t' + n for n in SUMS]
    return lines


def check(request, candidate):
    try:
        _, cand, public = E.bound(request, candidate, TASK)
        data = cand['data']
        require(type(data) is dict and set(data) == {'records'} and type(data['records']) is list, 'G1_SCHEMA:data')
        cases = public['cases']
        require(type(cases) is list and all(type(c) is str for c in cases), 'G1_SCHEMA:public_cases')
        require(sorted(cases) == sorted(expected_public_lines()), 'G2_COVERAGE:public_input_is_the_complete_21_10_3_8_640_8_family')
        records = data['records']
        require(len(records) == len(cases), 'G2_COVERAGE:record_count')
        case_set = set(cases)
        lines = []
        for r in records:
            require(type(r) is dict and type(r.get('kind')) is str, 'G1_SCHEMA:record')
            line = line_of(r)
            lines.append(line)
            require(line in case_set, 'G2_COVERAGE:unknown_input')
            require(strict_eq(r, expected(line)), 'G3_WITNESS:' + r['kind'])
        require(sorted(lines) == sorted(cases), 'G2_COVERAGE:inputs_are_the_public_cases')
        return {'records_checked': len(records)}
    except (KeyError, TypeError, IndexError, AttributeError, ValueError) as error:
        if isinstance(error, ValueError) and str(error).startswith('G'):
            raise
        raise ValueError('G1_SCHEMA:malformed ' + repr(error))

