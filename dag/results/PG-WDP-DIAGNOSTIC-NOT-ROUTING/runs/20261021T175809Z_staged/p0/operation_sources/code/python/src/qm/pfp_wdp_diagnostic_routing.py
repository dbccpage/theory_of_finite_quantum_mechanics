"""Diagnostic class, routing terminal, residual and authority tag: exhaustive tables of the real source maps.

Producer for PFP batch 01, node PG-WDP-DIAGNOSTIC-NOT-ROUTING. Exact integers and names only.
Transcribed from the_symbol_game (sha256 pinned in the operad collection and rechecked by the node author):
  omega_types/src/routing.rs      RoutingTerminal, From<TerminalStatus>, PfpTerminal, From<PfpTerminal>
  omega_types/src/terminal_status.rs  TerminalStatus (21), residual_class, authority_level tag, authority_terminal, terminal_from_fiber
  omega_policy/src/trichotomy.rs  ObstructionDiagnosticClass (Rust names the exact class `ExactRepair`; the ledger says `ExactClass`)
  omega_id_run/src/run.rs 626-633 diagnostic class -> status tag (the tag "ExactRepair" is not a PfpTerminal and has no route)
  omega_certifiers/src/checked_packet.rs 248  only the exact class is certificate-eligible
  external WitnessedDifference/Routing.lean  RelativeStatus and route (a four-valued axis with Bool inputs)
The source defines NO map from the diagnostic class to a routing terminal except the partial composite run.rs + terminal_routing.json.
The identification of ResidualClass with the diagnostic class is NOT made. AuthorityEffect: None.
"""
from itertools import product

ROUTES = ['CheckPassed', 'RequiresLift', 'Repair', 'Refusal', 'NoRule', 'BudgetUnknown', 'Refused']
STATUS_ROUTE = [
    ('ExactRuleDerived', 'CheckPassed'), ('UniqueOutputDerived', 'CheckPassed'), ('NoRuleInSearchClass', 'NoRule'),
    ('NonUniqueOutput', 'Repair'), ('EnumeratorFailure', 'Repair'), ('Refused', 'Refused'),
    ('LabelConflictsWithDerivation', 'Refused'), ('BudgetUnknown', 'BudgetUnknown'), ('InvalidProposal', 'Refused'),
    ('OperatorConflict', 'Refused'), ('UnknownSector', 'Repair'), ('NoDescentYet', 'Repair'),
    ('LabelOnlyUncertified', 'Repair'), ('LiftRequired', 'RequiresLift'), ('ParseRefused', 'Refusal'),
    ('ReplayMismatch', 'Repair'), ('PolicyAmbiguous', 'Repair'), ('NoPacket', 'Refusal'),
    ('VerifierDisabled', 'Repair'), ('SearchIncomplete', 'Repair'), ('PolicyUnderspecified', 'Repair')]
RESIDUAL = {'ExactRuleDerived': 'Exact', 'UniqueOutputDerived': 'Exact', 'NoRuleInSearchClass': 'ClosedSurvivor',
            'Refused': 'Refused', 'LabelConflictsWithDerivation': 'Refused', 'InvalidProposal': 'Refused',
            'OperatorConflict': 'Refused', 'ParseRefused': 'Refused'}  # every other status: Open
AUTH_CERTIFIABLE = {'ExactRuleDerived', 'UniqueOutputDerived'}
AUTH_REFUSED = {'Refused', 'LabelConflictsWithDerivation', 'InvalidProposal', 'OperatorConflict'}  # others: Uncertified
PFP_ROUTE = [
    ('Exact', 'CheckPassed'), ('Verified', 'CheckPassed'), ('VerifiedWithResiduals', 'CheckPassed'),
    ('StabilizedSurvivor', 'RequiresLift'), ('NeedsExternalOracle', 'RequiresLift'), ('OpenObstruction', 'Refusal'),
    ('BlockedByEvidence', 'Refusal'), ('InfrastructureFailure', 'Refusal'), ('Refused', 'Refused'),
    ('BudgetExhausted', 'BudgetUnknown')]
DIAG = [('ExactClass', 'ExactRepair'), ('ClosedResidual', 'StabilizedSurvivor'), ('ActiveClosureFailure', 'OpenObstruction')]
AGREEMENTS = ['-', '00', '01', '10', '11']

_status_route = dict(STATUS_ROUTE)
_pfp_route = dict(PFP_ROUTE)


def residual_of(name):
    return RESIDUAL.get(name, 'Open')


def auth_of(name):
    return 'Certifiable' if name in AUTH_CERTIFIABLE else 'Refused' if name in AUTH_REFUSED else 'Uncertified'


def rel_status(in_profile, contradicted, supported):
    if not in_profile:
        return 'outsideProfile'
    if contradicted:
        return 'refuted'
    return 'supported' if supported else 'undetermined'


def fiber_status(selected, cand, out, exhaustive, agreement, verifier):
    """terminal_from_fiber; 'ERR' stands for an Err."""
    if not selected:
        return 'ERR' if (cand != 0 or out != 0 or exhaustive) else 'NoPacket'
    if not verifier:
        return 'VerifierDisabled'
    if cand > 0 and out == 0:
        return 'ERR'
    if out > cand:
        return 'ERR'
    if cand == 0:
        return 'NoRuleInSearchClass' if exhaustive else 'SearchIncomplete'
    if cand == 1:
        return 'ExactRuleDerived'
    if out == 1:
        coherent, replay = (True, True) if agreement == '-' else (agreement[0] == '1', agreement[1] == '1')
        if not coherent:
            return 'PolicyAmbiguous'
        if not replay:
            return 'ReplayMismatch'
        return 'UniqueOutputDerived'
    return 'NonUniqueOutput'


def _fib_inputs():
    for sel, cand, out, exh, agr, ver in product((0, 1), range(4), range(4), (0, 1), AGREEMENTS, (0, 1)):
        yield sel, cand, out, exh, agr, ver


def _cases():
    cases = ['stat\t%d' % i for i in range(21)] + ['pfp\t%d' % i for i in range(10)] + ['diag\t%d' % i for i in range(3)]
    cases += ['rel\t%d\t%d\t%d' % t for t in product((0, 1), repeat=3)]
    cases += ['fib\t%d\t%d\t%d\t%d\t%s\t%d' % t for t in _fib_inputs()]
    cases += ['sum\t' + n for n in ['residual_routing', 'determination', 'policies', 'diag_cells', 'fiber_routes', 'fiber_statuses', 'image_sizes', 'authority']]
    return cases


CASES = _cases()


def _fib_results():
    return [(t, fiber_status(bool(t[0]), t[1], t[2], bool(t[3]), t[4], bool(t[5]))) for t in _fib_inputs()]


def _summary(name):
    stat = [(n, r, residual_of(n), auth_of(n)) for n, r in STATUS_ROUTE]
    if name == 'residual_routing':
        pairs = sorted({'%s:%s' % (res, r) for _, r, res, _ in stat})
        return [28, len(pairs)], pairs
    if name == 'determination':
        cols = {'residual': 2, 'route': 1, 'auth': 3}
        items = []
        for a, b in [('residual', 'route'), ('route', 'residual'), ('residual', 'auth'), ('auth', 'residual'), ('route', 'auth'), ('auth', 'route')]:
            seen = {}
            ok = True
            for row in stat:
                if seen.setdefault(row[cols[a]], row[cols[b]]) != row[cols[b]]:
                    ok = False
            items.append('%s->%s:%d' % (a, b, int(ok)))
        return [], items
    if name == 'policies':
        return [3, 7, 7 ** 3, 7 * 6 * 5, 0, 7 * 7, 3 * 7], []
    if name == 'diag_cells':
        routed = sorted('%s:%s' % (d, _pfp_route[t]) for d, t in DIAG if t in _pfp_route)
        return [21, len(routed), 3 - len(routed), 21 - len(routed)], routed
    fib = _fib_results()
    if name == 'fiber_routes':
        errs = sum(1 for _, s in fib if s == 'ERR')
        reached = sorted({_status_route[s] for _, s in fib if s != 'ERR'})
        return [len(fib), errs, len(fib) - errs, len(reached)], reached
    if name == 'fiber_statuses':
        counts = {}
        for _, s in fib:
            if s != 'ERR':
                counts[s] = counts.get(s, 0) + 1
        return [len(counts)], sorted('%s:%d' % kv for kv in counts.items())
    if name == 'image_sizes':
        pfp_image = {r for _, r in PFP_ROUTE}
        fib_image = {_status_route[s] for _, s in fib if s != 'ERR'}
        missing = sorted(['pfp-missing:' + r for r in ROUTES if r not in pfp_image] + ['fiber-missing:' + r for r in ROUTES if r not in fib_image])
        return [len({r for _, r in STATUS_ROUTE}), len(pfp_image), len(fib_image), len({rel_status(*t) for t in product((False, True), repeat=3)})], missing
    if name == 'authority':
        tags = [auth_of(n) for n, _ in STATUS_ROUTE]
        return [21, tags.count('Certifiable'), tags.count('Refused'), tags.count('Uncertified'),
                sum(1 for n, _ in STATUS_ROUTE if n in AUTH_CERTIFIABLE), 0, sum(1 for n, _ in STATUS_ROUTE if n in AUTH_CERTIFIABLE)], []
    raise ValueError(name)


def record(line):
    f = line.split('\t')
    kind = f[0]
    if kind == 'stat':
        n, r = STATUS_ROUTE[int(f[1])]
        return {'kind': 'stat', 'i': int(f[1]), 'name': n, 'route': r, 'residual': residual_of(n), 'auth': auth_of(n),
                'authterm': n in AUTH_CERTIFIABLE}
    if kind == 'pfp':
        n, r = PFP_ROUTE[int(f[1])]
        return {'kind': 'pfp', 'i': int(f[1]), 'name': n, 'route': r}
    if kind == 'diag':
        n, tag = DIAG[int(f[1])]
        return {'kind': 'diag', 'i': int(f[1]), 'name': n, 'run_tag': tag, 'route': _pfp_route.get(tag, '-'), 'cert_eligible': int(f[1]) == 0}
    if kind == 'rel':
        i, c, s = (bool(int(x)) for x in f[1:4])
        return {'kind': 'rel', 'in_profile': i, 'contradicted': c, 'supported': s, 'status': rel_status(i, c, s)}
    if kind == 'fib':
        sel, cand, out, exh, agr, ver = bool(int(f[1])), int(f[2]), int(f[3]), bool(int(f[4])), f[5], bool(int(f[6]))
        s = fiber_status(sel, cand, out, exh, agr, ver)
        return {'kind': 'fib', 'selected': sel, 'cand': cand, 'out': out, 'exhaustive': exh, 'agreement': agr, 'verifier': ver,
                'status': s, 'route': '-' if s == 'ERR' else _status_route[s]}
    if kind == 'sum':
        ints, items = _summary(f[1])
        return {'kind': 'sum', 'name': f[1], 'ints': ints, 'items': items}
    raise ValueError(line)


def certificate(cases=CASES):
    return {'records': [record(c) for c in cases]}


def _join(xs):
    return ';'.join(str(x) for x in xs) or '-'


def wire_lines(data):
    out = []
    for r in data['records']:
        k = r['kind']
        if k == 'stat':
            out.append('\t'.join(['stat', str(r['i']), r['name'], r['route'], r['residual'], r['auth'], str(int(r['authterm']))]))
        elif k == 'pfp':
            out.append('\t'.join(['pfp', str(r['i']), r['name'], r['route']]))
        elif k == 'diag':
            out.append('\t'.join(['diag', str(r['i']), r['name'], r['run_tag'], r['route'], str(int(r['cert_eligible']))]))
        elif k == 'rel':
            out.append('\t'.join(['rel', str(int(r['in_profile'])), str(int(r['contradicted'])), str(int(r['supported'])), r['status']]))
        elif k == 'fib':
            out.append('\t'.join(['fib', str(int(r['selected'])), str(r['cand']), str(r['out']), str(int(r['exhaustive'])), r['agreement'],
                                  str(int(r['verifier'])), r['status'], r['route']]))
        else:
            out.append('\t'.join(['sum', r['name'], _join(r['ints']), _join(r['items'])]))
    return out


def public_tsv(cases=CASES):
    return ''.join(c + '\n' for c in cases)
