"""Semantic near misses for the free-monoid non-isomorphism certificate (PG-FREE-MONOID-NONISO).

Each mutant is a well-formed record a reviewer could believe; each breaks one premise of the node or is a
counterexample to the unpaid bridge named in does_not_support.
"""


def _record(data, n, m, d):
    return next(r for r in data['records'] if r['input'] == [n, m, d])


def semantic_mutants(data, profile):
    def set_bijection_read_as_isomorphism(d):
        _record(d, 2, 3, 2)['homomorphism_violations'] = 0

    def different_alphabets_different_sets(d):
        _record(d, 1, 2, 2)['set_bijection'] = 0

    def collapsing_surjection_read_as_bijection(d):
        r = _record(d, 3, 2, 2)
        r['bijective_candidates'] = 2
        r['bijective_not_permutation'] = 2

    def longer_words_are_atoms(d):
        _record(d, 2, 3, 2)['atoms_n'] = 6

    def discrete_equivalence_between_unequal_sizes(d):
        _record(d, 2, 3, 2)['discrete_equivalences'] = 6

    def trivial_monoid_isomorphic_to_one_generator(d):
        _record(d, 0, 1, 2)['bijective_candidates'] = 1

    def unique_isomorphism_for_equal_sizes(d):
        r = _record(d, 3, 3, 2)
        r['permutation_homs'] = 1
        r['bijective_candidates'] = 1

    def words_by_length_ignore_alphabet(d):
        _record(d, 3, 2, 2)['words_n'] = [1, 2, 4, 8, 16]

    return [
        {'id': 'set_bijection_read_as_isomorphism', 'rationale': 'Read the explicit shortlex bijection of the underlying sets of Fin 2 and Fin 3 words as multiplicative; it fails on 841 of 900 pairs.', 'mutate': set_bijection_read_as_isomorphism},
        {'id': 'different_alphabets_different_sets', 'rationale': 'Claim the underlying sets differ in cardinality, so non-isomorphism is a cardinality fact; both are countably infinite and the shortlex map is a bijection.', 'mutate': different_alphabets_different_sets},
        {'id': 'collapsing_surjection_read_as_bijection', 'rationale': 'Count homomorphisms from three generators onto two letters as bijective; they identify two generators and are not injective.', 'mutate': collapsing_surjection_read_as_bijection},
        {'id': 'longer_words_are_atoms', 'rationale': 'Claim some words of length two are indecomposable; the atoms are exactly the one-letter words.', 'mutate': longer_words_are_atoms},
        {'id': 'discrete_equivalence_between_unequal_sizes', 'rationale': 'Claim discrete categories on 2 and 3 objects are equivalent; an equivalence of discrete categories is a bijection of objects.', 'mutate': discrete_equivalence_between_unequal_sizes},
        {'id': 'trivial_monoid_isomorphic_to_one_generator', 'rationale': 'Claim the free monoid on the empty alphabet (one element) is isomorphic to the free monoid on one letter (countably infinite).', 'mutate': trivial_monoid_isomorphic_to_one_generator},
        {'id': 'unique_isomorphism_for_equal_sizes', 'rationale': 'Claim equal alphabets give a unique isomorphism; every permutation of the 3 letters gives one (6 of them).', 'mutate': unique_isomorphism_for_equal_sizes},
        {'id': 'words_by_length_ignore_alphabet', 'rationale': 'Report the word counts by length of the 2-letter alphabet for a 3-letter one, hiding that the counts differ.', 'mutate': words_by_length_ignore_alphabet},
    ]


def semantic_controls(data, profile):
    def reverse_record_order(d):
        d['records'].reverse()

    return [{'id': 'reverse_record_order', 'rationale': 'The cases are a set; any order of the same records is the same certificate.', 'mutate': reverse_record_order}]
