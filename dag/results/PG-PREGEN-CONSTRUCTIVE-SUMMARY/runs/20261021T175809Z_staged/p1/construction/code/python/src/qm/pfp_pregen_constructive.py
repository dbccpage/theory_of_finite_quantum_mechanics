"""Pre-Genesis summary over listed histories: first-match reconstruction versus fiber constancy, exhaustively.

Producer for PFP batch 01, node PG-PREGEN-CONSTRUCTIVE-SUMMARY. Exact integers only.
Population H = {0..p-1}; a listing is ANY list over H of length <= ell (repeats allowed, so every listed
population is covered); reports V = {0..v-1}; answers S = {0..s-1}. For every (listing, report, answer) the
producer computes the first-match reconstruction recon(x) = answer of the first listed history reporting x
(or none) and compares "recon returns every listed answer" with "answer constant on report fibers among the
listed histories". It also records what happens off the listing. These are finite instances; the general
choice-free statement is the Lean module PregenConstructive. AuthorityEffect: None.
"""
from itertools import product

CASES = [(0, 2, 0, 0), (0, 2, 2, 2), (1, 2, 2, 2), (2, 2, 2, 0), (2, 2, 0, 2), (2, 3, 2, 2), (2, 3, 3, 2),
         (3, 1, 2, 2), (3, 2, 3, 2), (3, 3, 2, 2), (3, 3, 3, 2), (3, 3, 2, 3), (3, 4, 2, 2), (4, 3, 3, 2), (4, 4, 2, 2)]


def recon(listing, report, answer, x):
    for h in listing:
        if report[h] == x:
            return answer[h]
    return None


def record(p, ell, v, s):
    lists = [()]
    for k in range(1, ell + 1):
        lists += list(product(range(p), repeat=k))
    reports = list(product(range(v), repeat=p))
    answers = list(product(range(s), repeat=p))
    r = dict(zip(['listed_fc', 'recon_correct', 'mismatch', 'complete_triples', 'complete_mismatch', 'partial_false_positive',
                  'unlisted_refused', 'unlisted_correct', 'unlisted_wrong'], [0] * 9))
    triples = 0
    for listing in lists:
        listed = set(listing)
        complete = len(listed) == p
        for report in reports:
            for answer in answers:
                triples += 1
                fc = all(answer[a] == answer[b] for a in listing for b in listing if report[a] == report[b])
                rc = all(recon(listing, report, answer, report[a]) == answer[a] for a in listing)
                global_fc = all(answer[a] == answer[b] for a in range(p) for b in range(p) if report[a] == report[b])
                r['listed_fc'] += fc
                r['recon_correct'] += rc
                r['mismatch'] += fc != rc
                if complete:
                    r['complete_triples'] += 1
                    r['complete_mismatch'] += fc != global_fc
                elif fc and not global_fc:
                    r['partial_false_positive'] += 1
                if fc:
                    for h in range(p):
                        if h in listed:
                            continue
                        got = recon(listing, report, answer, report[h])
                        if got is None:
                            r['unlisted_refused'] += 1
                        elif got == answer[h]:
                            r['unlisted_correct'] += 1
                        else:
                            r['unlisted_wrong'] += 1
    return dict({'input': [p, ell, v, s], 'lists': len(lists), 'triples': triples}, **r)


FIELDS = ['lists', 'triples', 'listed_fc', 'recon_correct', 'mismatch', 'complete_triples', 'complete_mismatch',
          'partial_false_positive', 'unlisted_refused', 'unlisted_correct', 'unlisted_wrong']


def certificate(cases=CASES):
    return {'records': [record(*c) for c in cases]}


def wire_lines(data):
    return ['\t'.join(['listed'] + [str(x) for x in r['input']] + [str(r[f]) for f in FIELDS]) for r in data['records']]


def public_tsv(cases=CASES):
    return ''.join('listed\t%d\t%d\t%d\t%d\n' % c for c in cases)
