"""History-report criterion: exhaustive finite certificate over all (report, question) function pairs.

Producer for PFP batch 01, node PG-HISTORY-REPORT-CRITERION. Exact integers only.
Histories H = {0..h-1}, reports V = {0..v-1}, answers S = {0..s-1}. For every report H -> V and every
question H -> S the producer decides, by brute force, whether the question factors through the report image
(some g on the image with g o report = question), whether it is constant on report fibers, how many factors
g exist, and how many extensions f : V -> S off the image exist. These are finite instances; the general
statement (arbitrary types, with the axiom bill of each direction) is the Lean module HistoryReport.
AuthorityEffect: None.
"""
from itertools import product

CASES = [(0, 0, 0), (0, 0, 2), (0, 2, 2), (1, 0, 2), (1, 1, 0), (1, 2, 2), (2, 2, 1), (2, 2, 2), (2, 3, 2),
         (3, 1, 2), (3, 2, 2), (3, 3, 2), (3, 3, 3), (4, 3, 2), (4, 4, 2), (0, 2, 0)]


def record(h, v, s):
    all_f = list(product(range(s), repeat=v))
    answers = list(product(range(s), repeat=h))
    pairs = fiber_constant = factoring = mismatch = 0
    hist = {}
    max_mult = 0
    ext_total = nonunique = surj = surj_nonunique = 0
    for rep in product(range(v), repeat=h):
        image = sorted(set(rep))
        k = len(image)
        hist[k] = hist.get(k, 0) + 1
        is_surj = k == v
        if is_surj:
            surj += 1
        index = {x: i for i, x in enumerate(image)}
        factor_count = {}
        for g in product(range(s), repeat=k):
            key = tuple(g[index[rep[i]]] for i in range(h))
            factor_count[key] = factor_count.get(key, 0) + 1
        ext_count = {}
        for f in all_f:
            key = tuple(f[rep[i]] for i in range(h))
            ext_count[key] = ext_count.get(key, 0) + 1
        for ans in answers:
            pairs += 1
            fc = all(ans[i] == ans[j] for i in range(h) for j in range(h) if rep[i] == rep[j])
            ng = factor_count.get(ans, 0)
            fact = ng > 0
            fiber_constant += fc
            factoring += fact
            mismatch += fc != fact
            if ng > max_mult:
                max_mult = ng
            ne = ext_count.get(ans, 0)
            ext_total += ne
            if fact and ne >= 2:
                nonunique += 1
                if is_surj:
                    surj_nonunique += 1
    return {'input': [h, v, s], 'pairs': pairs, 'fiber_constant': fiber_constant, 'factoring': factoring,
            'mismatch': mismatch, 'image_hist': [[k, hist[k]] for k in sorted(hist)], 'max_factor_multiplicity': max_mult,
            'extensions_total': ext_total, 'nonunique_off_image': nonunique, 'surjective_reports': surj,
            'surjective_nonunique': surj_nonunique}


def certificate(cases=CASES):
    return {'records': [record(*c) for c in cases]}


def wire_lines(data):
    out = []
    for r in data['records']:
        hist = ';'.join('%d:%d' % (k, c) for k, c in r['image_hist']) or '-'
        out.append('\t'.join(['report'] + [str(x) for x in r['input']] + [
            str(r['pairs']), str(r['fiber_constant']), str(r['factoring']), str(r['mismatch']), hist,
            str(r['max_factor_multiplicity']), str(r['extensions_total']), str(r['nonunique_off_image']),
            str(r['surjective_reports']), str(r['surjective_nonunique'])]))
    return out


def public_tsv(cases=CASES):
    return ''.join('report\t%d\t%d\t%d\n' % c for c in cases)
