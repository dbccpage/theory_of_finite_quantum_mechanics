"""Finite demand accounting s_next = s - d + b: exhaustive classification of (W, D, B) over small universes.

Producer for PFP batch 01, node PG-DEMAND-ACCOUNTING. Exact integers only. Sets are bitmasks over a universe of u
elements; the next register is (W minus D) union B. Every triple (W, D, B) of subsets is classified by which of the two
source hypotheses it satisfies (D subset of W; births disjoint from W minus D) and, per class, the number of triples
for which the identity |next| = |W| - |D| + |B| holds (as an integer identity, and as the truncated natural-number
identity max(0, |W| - |D|) + |B|). A second kind of record shows that a displayed count sequence (the source's
chosen survivor sequence among them) does not determine the (d, b) split of any step.
Scope: finite sets; not a statement about which demands an engine carries. AuthorityEffect: None.
"""

from itertools import product

CASES = [['demand', 0], ['demand', 1], ['demand', 2], ['demand', 3], ['demand', 4], ['demand', 5],
         ['sequence', [0, 1, 1, 1, 0, 1, 1]], ['sequence', [3, 3, 3]], ['sequence', [0, 5, 0, 2]], ['sequence', [4, 1, 4]],
         ['listreg', 2, 2], ['listreg', 3, 3]]

LISTREG_FIELDS = ['total', 'identity_holds', 'nodup_inputs', 'disjoint_inputs', 'nodup_when_disjoint', 'nodup_when_overlap']
CLASS_NAMES = ['hypotheses_hold', 'subset_violated_only', 'overlap_violated_only', 'both_violated']


def popcount(x):
    return bin(x).count('1')


def demand_record(u):
    full = (1 << u) - 1
    tally = [[0, 0, 0] for _ in range(4)]
    for w in range(full + 1):
        for d in range(full + 1):
            for b in range(full + 1):
                survivors = w & ~d & full
                nxt = survivors | b
                s, dd, bb = popcount(w), popcount(d), popcount(b)
                sub_bad = (d & ~w & full) != 0
                ov_bad = (survivors & b) != 0
                k = (1 if sub_bad else 0) + (2 if ov_bad else 0)
                tally[k][0] += 1
                if popcount(nxt) == s - dd + bb:
                    tally[k][1] += 1
                if popcount(nxt) == max(0, s - dd) + bb:
                    tally[k][2] += 1
    return {'kind': 'demand', 'u': u, 'total': 8 ** u, 'classes': tally}


def decomposition_count(s, t):
    """Number of (d, b) with 0 <= d <= s, b >= 0, s - d + b == t (b is then determined by d)."""
    count = 0
    for d in range(s + 1):
        b = t - s + d
        if b >= 0:
            count += 1
    return count


def sequence_record(seq):
    steps = list(zip(seq[:-1], seq[1:]))
    counts = [decomposition_count(s, t) for s, t in steps]
    return {'kind': 'sequence', 'seq': list(seq), 'decompositions': counts, 'underdetermined': any(c >= 2 for c in counts)}


def listreg_record(a, maxlen):
    """List registers over an alphabet of a letters: every active list and births list of length <= maxlen and every
    discharge predicate (a subset of the alphabet). The register is (active filtered by not-discharged) ++ births.
    The length identity needs no disjointness; for duplicate-free inputs the register is duplicate-free exactly when
    the births avoid the survivors."""
    lists = [t for k in range(maxlen + 1) for t in product(range(a), repeat=k)]
    total = identity = nodup_inputs = disjoint = nodup_when_disjoint = nodup_when_overlap = 0
    for active in lists:
        for mask in range(1 << a):
            surv = [x for x in active if not (mask >> x) & 1]
            for births in lists:
                total += 1
                reg = surv + list(births)
                discharged = len(active) - len(surv)
                if len(reg) == len(active) - discharged + len(births):
                    identity += 1
                if len(set(active)) == len(active) and len(set(births)) == len(births):
                    nodup_inputs += 1
                    is_nodup = len(set(reg)) == len(reg)
                    if not (set(surv) & set(births)):
                        disjoint += 1
                        nodup_when_disjoint += 1 if is_nodup else 0
                    elif is_nodup:
                        nodup_when_overlap += 1
    return {'kind': 'listreg', 'input': [a, maxlen], 'total': total, 'identity_holds': identity, 'nodup_inputs': nodup_inputs,
            'disjoint_inputs': disjoint, 'nodup_when_disjoint': nodup_when_disjoint, 'nodup_when_overlap': nodup_when_overlap}

def certificate(cases=CASES):
    out = []
    for case in cases:
        kind, arg = case[0], case[1]
        if kind == 'demand':
            out.append(demand_record(arg))
        elif kind == 'sequence':
            out.append(sequence_record(arg))
        else:
            out.append(listreg_record(case[1], case[2]))
    return {'records': out}


def wire_lines(data):
    out = []
    for r in data['records']:
        if r['kind'] == 'demand':
            cls = ['%d:%d:%d' % tuple(c) for c in r['classes']]
            out.append('\t'.join(['demand', str(r['u']), str(r['total'])] + cls))
        elif r['kind'] == 'sequence':
            out.append('\t'.join(['sequence', ','.join(str(x) for x in r['seq']), ','.join(str(x) for x in r['decompositions']),
                                  str(int(r['underdetermined']))]))
        else:
            out.append('\t'.join(['listreg'] + [str(x) for x in r['input']] + [str(r[k]) for k in LISTREG_FIELDS]))
    return out


def public_tsv(cases=CASES):
    out = []
    for case in cases:
        if case[0] == 'demand':
            out.append('demand\t%d\n' % case[1])
        elif case[0] == 'sequence':
            out.append('sequence\t%s\n' % ','.join(str(x) for x in case[1]))
        else:
            out.append('listreg\t%d\t%d\n' % (case[1], case[2]))
    return ''.join(out)
