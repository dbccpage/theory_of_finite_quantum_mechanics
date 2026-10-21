"""Semantic near misses for the collapsed observation barrier certificate.

Each mutant is a well-formed record that a reviewer could believe and each breaks one premise or states the
unpaid bridge (a tag that is selected, or an unconditional factorisation criterion) without support.
"""
from itertools import product


def _alt_hist(n, my, mz, rule):
    """Histogram of a wrong rule for the least tag alphabet, computed over the same pairs (p, s)."""
    hist = {}
    for p in product(range(my), repeat=n):
        for s in product(range(mz), repeat=n):
            fibres = {}
            for a, b in zip(p, s):
                fibres.setdefault(a, []).append(b)
            k = rule(fibres, s)
            hist[k] = hist.get(k, 0) + 1
    return [[k, hist[k]] for k in sorted(hist)]


def _record(data, n, my, mz):
    return next(r for r in data['records'] if r['input'] == [n, my, mz])


def semantic_mutants(data, profile):
    def empty_task_codomain_factors(d):
        # fixed instance read as the unconditional iff: empty X, one profile value, empty Z "factors"
        r = _record(d, 0, 1, 0)
        r['factoring'] = 1
        r['factorizations'] = 1

    def barrier_has_an_exception(d):
        r = _record(d, 3, 2, 2)
        r['factoring'] += 1
        r['violations'] = 1

    def one_bit_always_suffices(d):
        r = _record(d, 4, 1, 4)
        r['min_tag_hist'] = [[1, 4], [2, 252]]

    def added_tag_never_helps(d):
        r = _record(d, 3, 2, 3)
        r['min_tag_hist'] = [[0, 156], [1, 60]]

    def factorisation_unique(d):
        r = _record(d, 3, 2, 3)
        r['factorizations'] = r['factoring']

    def roles_swapped(d):
        r = _record(d, 3, 2, 3)
        r['factorizations'] = 3 ** 3 * 2 ** 3

    def injective_profile_still_collapses(d):
        r = _record(d, 2, 2, 2)
        r['fibre_constant'] -= 4
        r['collapsed_separated'] += 4
        r['factoring'] -= 4

    def alphabet_is_global_distinct_count(d):
        _record(d, 3, 2, 3)['min_tag_hist'] = _alt_hist(3, 2, 3, lambda f, s: max(1, len(set(s))))

    def alphabet_is_fibre_size(d):
        _record(d, 3, 2, 3)['min_tag_hist'] = _alt_hist(3, 2, 3, lambda f, s: max(1, max((len(v) for v in f.values()), default=0)))

    def alphabet_needs_one_more_value(d):
        r = _record(d, 3, 2, 2)
        r['min_tag_hist'] = [[k + 1, c] for k, c in r['min_tag_hist']]

    def empty_carrier_needs_one_tag_value(d):
        _record(d, 0, 0, 1)['min_tag_hist'] = [[1, 1]]

    return [
        {'id': 'empty_task_codomain_factors', 'rationale': 'Read "fibre-constant iff factors" as unconditional: with empty X and empty Z the fibre condition is vacuous but no g : Y -> Z exists.', 'mutate': empty_task_codomain_factors},
        {'id': 'barrier_has_an_exception', 'rationale': 'Claim one task that separates a collapsed pair nevertheless factors through the profile.', 'mutate': barrier_has_an_exception},
        {'id': 'one_bit_always_suffices', 'rationale': 'Claim an added binary tag always recovers the task; four task values inside one fibre need four tag values.', 'mutate': one_bit_always_suffices},
        {'id': 'added_tag_never_helps', 'rationale': 'Read "no function of the quotient separates" as "nothing separates": claim the separated pairs need no added tag at all (alphabet size 0).', 'mutate': added_tag_never_helps},
        {'id': 'factorisation_unique', 'rationale': 'Count one factor per factoring pair; the factor is unique only on the image of the profile (history_factor_unique), free elsewhere.', 'mutate': factorisation_unique},
        {'id': 'profile_task_roles_swapped', 'rationale': 'Swap the roles of profile and task codomains in the factor count (mz ** n * my ** mz instead of my ** n * mz ** my).', 'mutate': roles_swapped},
        {'id': 'injective_profile_still_collapses', 'rationale': 'Count the injective profiles on a two-point carrier as having collapsed separated pairs.', 'mutate': injective_profile_still_collapses},
        {'id': 'alphabet_is_global_distinct_count', 'rationale': 'Read the least tag alphabet as the number of distinct task values overall; it is the largest number inside one fibre, which is smaller whenever the values are spread over several fibres.', 'mutate': alphabet_is_global_distinct_count},
        {'id': 'alphabet_is_fibre_size', 'rationale': 'Read the least tag alphabet as the size of the largest fibre; points of a fibre with the same task value share one tag value.', 'mutate': alphabet_is_fibre_size},
        {'id': 'alphabet_needs_one_more_value', 'rationale': 'Off by one: claim the tag needs one more value than the largest number of distinct task values in a fibre.', 'mutate': alphabet_needs_one_more_value},
        {'id': 'empty_carrier_needs_one_tag_value', 'rationale': 'Convention error for the empty carrier: the empty alphabet already works there (Y x empty is empty); one value is needed only for nonempty X.', 'mutate': empty_carrier_needs_one_tag_value},
    ]


def semantic_controls(data, profile):
    def reverse_record_order(d):
        d['records'].reverse()

    return [{'id': 'reverse_record_order', 'rationale': 'The cases are a set; any order of the same records is the same certificate.', 'mutate': reverse_record_order}]
