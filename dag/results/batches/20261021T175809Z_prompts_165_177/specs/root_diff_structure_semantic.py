"""Semantic near misses for PG-ROOT-DIFF-STRUCTURE. Each is a well-formed record a reviewer might believe."""


def _rec(data, kind, **match):
    return next(r for r in data['records'] if r['kind'] == kind and all(r.get(k) == v for k, v in match.items()))


def semantic_mutants(data, profile):
    def ranges_overlap(d):
        _rec(d, 'maps', a=2, b=2, c=2)['disjoint'] = False

    def reduction_always_exists(d):
        r = _rec(d, 'reduction', a=0, b=2)
        r['exists_to_pd'] = True
        r['retractions_to_pd'] = 1

    def reduction_is_canonical(d):
        _rec(d, 'reduction', a=2, b=2)['retractions_to_pd'] = 1

    def maps_out_count_is_a_sum(d):
        r = _rec(d, 'maps', a=2, b=1, c=2)
        r['total_maps'] = r['left_maps'] + r['right_maps']
        r['product_matches'] = False

    def coproduct_nonempty_without_posits(d):
        _rec(d, 'posit', a=0, b=0)['nonempty_real0'] = True

    def structure_posit_entails_difference(d):
        _rec(d, 'posit', a=0, b=1)['nonempty_pd'] = True

    def some_pair_has_no_copair(d):
        _rec(d, 'maps', a=1, b=1, c=2)['unique_copairs'] = 3

    def swapped_direction(d):
        r = _rec(d, 'reduction', a=0, b=1)
        r['exists_to_pd'], r['exists_to_s'] = True, False

    def coproduct_size_is_max(d):
        _rec(d, 'posit', a=1, b=1)['coproduct_size'] = 1

    def empty_channels_have_no_retraction(d):
        r = _rec(d, 'reduction', a=0, b=0)
        r['exists_to_pd'] = False
        r['retractions_to_pd'] = 0

    def retractions_swapped_exponent(d):
        _rec(d, 'reduction', a=2, b=3)['retractions_to_pd'] = 9

    def retraction_exists_whenever_other_nonempty(d):
        _rec(d, 'reduction', a=3, b=0)['exists_to_s'] = True

    def zero_codomain_unique_copair(d):
        _rec(d, 'maps', a=1, b=1, c=0)['unique_copairs'] = 1

    def inhabited_channels_irreducible(d):
        _rec(d, 'reduction', a=2, b=2)['exists_to_pd'] = False

    return [
        {'id': 'empty_channels_have_no_retraction', 'rationale': 'Claim no retraction exists when both channels are empty; the empty map is one, although the coproduct itself is empty.', 'mutate': empty_channels_have_no_retraction},
        {'id': 'retractions_swapped_exponent', 'rationale': 'Count retractions onto the difference channel as |S|^|PD| instead of |PD|^|S| (9 for sizes 2, 3 instead of 8).', 'mutate': retractions_swapped_exponent},
        {'id': 'retraction_exists_whenever_other_nonempty', 'rationale': 'Claim a retraction onto the structure channel exists because the difference channel is nonempty; with an empty structure channel no map from a nonempty difference channel into it exists.', 'mutate': retraction_exists_whenever_other_nonempty},
        {'id': 'zero_codomain_unique_copair', 'rationale': 'Claim a pair of maps into the empty set has a unique extension when both channels are nonempty; there are no such maps at all.', 'mutate': zero_codomain_unique_copair},
        {'id': 'inhabited_channels_irreducible', 'rationale': 'Read the DAG sentence "no reduction of either channel to the other" as nonexistence of a retraction for two inhabited channels; retractions exist whenever the target channel is inhabited.', 'mutate': inhabited_channels_irreducible},
        {'id': 'ranges_overlap', 'rationale': 'Claim a structure item can coincide with a difference item inside the coproduct; the injections have disjoint ranges.', 'mutate': ranges_overlap},
        {'id': 'reduction_always_exists', 'rationale': 'Claim the structure channel always reads as a difference even when the difference channel is empty; then no map from structure items to difference items exists.', 'mutate': reduction_always_exists},
        {'id': 'reduction_is_canonical', 'rationale': 'Treat the reduction as unique; when it exists there are |A|^|B| choices and the coproduct selects none.', 'mutate': reduction_is_canonical},
        {'id': 'maps_out_count_is_a_sum', 'rationale': 'Count maps out of a coproduct by adding the counts for the two channels instead of multiplying.', 'mutate': maps_out_count_is_a_sum},
        {'id': 'coproduct_nonempty_without_posits', 'rationale': 'Claim Real_0 has an element when neither channel is posited; the construction alone yields none.', 'mutate': coproduct_nonempty_without_posits},
        {'id': 'structure_posit_entails_difference', 'rationale': 'Claim positing a structure channel posits a difference channel; the two posits are independent.', 'mutate': structure_posit_entails_difference},
        {'id': 'some_pair_has_no_copair', 'rationale': 'Claim that not every pair of maps out of the channels extends to the coproduct; the universal property gives exactly one extension for every pair.', 'mutate': some_pair_has_no_copair},
        {'id': 'swapped_direction', 'rationale': 'Swap which channel a retraction lands in: with an empty difference channel the retraction onto structure exists, not onto difference.', 'mutate': swapped_direction},
        {'id': 'coproduct_size_is_max', 'rationale': 'Take the coproduct of two one-element channels to have one element (a join) instead of two.', 'mutate': coproduct_size_is_max},
    ]


def semantic_controls(data, profile):
    def reverse_record_order(d):
        d['records'].reverse()

    return [{'id': 'reverse_record_order', 'rationale': 'The cases are a set; any order of the same records is the same certificate.', 'mutate': reverse_record_order}]
