"""Status ledger of the five open Genesis-to-WDP bridge obligations O01..O05: all 3^5 status vectors.

Producer for PFP batch 01, node PG-WDP-GENESIS-BRIDGE-OBLIGATIONS. Exact integers only.
Statuses: 0 = open, 1 = control-only (a scoped control passes, the obligation is not discharged), 2 = discharged.
The end-to-end predicate is DEFINED as 'all five discharged' (a modelling choice: the register gives no independent
semantics for end-to-end beyond saying the end-to-end claims are not done). The programme order O01<O02<O03<O04<O05
is our mapping of the derivation order in genesis_to_wdp_derivation_programme.md section 6; it is not a stated logical
prerequisite relation. The source-reported state (register + completion audit) is control-only for all five, i.e. 11111.
Nothing here discharges any obligation. AuthorityEffect: None.
"""
from itertools import product

N = 5
CASES = [''.join(str(d) for d in v) for v in product(range(3), repeat=N)]
SOURCE_REPORTED = '11111'


def record(code):
    v = [int(c) for c in code]
    n_open, n_control, n_disch = v.count(0), v.count(1), v.count(2)
    # discharged obligations form a prefix of the programme order <=> no discharged position follows an undischarged one
    seen_undischarged = False
    prefix = True
    for s in v:
        if s != 2:
            seen_undischarged = True
        elif seen_undischarged:
            prefix = False
    return {
        'v': v,
        'n_open': n_open,
        'n_control': n_control,
        'n_discharged': n_disch,
        'end_to_end': n_disch == N,
        'controls_run': n_open == 0,
        'prefix_order': prefix,
        'upgrades': sum(2 - s for s in v),
        'completing_upgrades': 1 if n_disch == N - 1 else 0,
        'source_reported': code == SOURCE_REPORTED,
    }


def certificate(cases=CASES):
    return {'records': [record(c) for c in cases]}


def wire_lines(data):
    out = []
    for r in data['records']:
        out.append('\t'.join(['led', ''.join(str(s) for s in r['v']), str(r['n_open']), str(r['n_control']), str(r['n_discharged']),
                              str(int(r['end_to_end'])), str(int(r['controls_run'])), str(int(r['prefix_order'])),
                              str(r['upgrades']), str(r['completing_upgrades']), str(int(r['source_reported']))]))
    return out


def public_tsv(cases=CASES):
    return ''.join('led\t%s\n' % c for c in cases)
