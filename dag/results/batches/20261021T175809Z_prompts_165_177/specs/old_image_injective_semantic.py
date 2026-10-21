"""Semantic near misses for the PG-OLD-IMAGE-INJECTIVE certificate.

Each mutant is a well-formed record a reviewer could believe, and each breaks one premise of the node.
"""


def _rec(data, a, b, o):
    return next(r for r in data['records'] if r['input'] == [a, b, o])


def semantic_mutants(data, profile):
    def law_forces_off_image_refusal(d):
        r = _rec(d, 2, 3, 2)
        r['law_nonrefusing'] = 0
        r['law_refusing'] = r['law']

    def law_without_injectivity(d):
        r = _rec(d, 2, 2, 2)
        r['law_noninjective'] = 1

    def law_forces_observation_preservation(d):
        r = _rec(d, 2, 2, 2)
        r['obs_preserved'] = r['obs_total']

    def law_repairs_obstructions(d):
        r = _rec(d, 2, 2, 2)
        r['persists'] = 0

    def recovery_exists_for_larger_source(d):
        r = _rec(d, 3, 2, 2)
        r['law'] = 1
        r['law_refusing'] = 1

    def recovery_unique_per_lift(d):
        r = _rec(d, 2, 3, 2)
        r['law'] = r['injective_u']
        r['law_nonrefusing'] = 0

    def old_image_law_counts_all_functions(d):
        r = _rec(d, 1, 2, 2)
        r['law'] = r['pairs_total']

    def law_count_ignores_refusal_summand(d):
        r = _rec(d, 2, 3, 2)
        r['law'] = 12
        r['law_nonrefusing'] = 6

    def law_forces_surjective_lift(d):
        r = _rec(d, 2, 3, 2)
        r['law'] = 0
        r['law_refusing'] = 0
        r['law_nonrefusing'] = 0

    def empty_source_observation_failure(d):
        r = _rec(d, 0, 3, 2)
        r['obs_preserved'] = r['obs_total'] - 1

    def surjective_lift_has_nonrefusing_recovery(d):
        r = _rec(d, 3, 3, 2)
        r['law_nonrefusing'] = 1
        r['law_refusing'] -= 1

    return [
        {'id': 'law_forces_off_image_refusal', 'rationale': 'Claim every law-satisfying recovery of the (2,3) census refuses the off-image point; 12 of the 18 do not, which is off_image_not_implied.', 'mutate': law_forces_off_image_refusal},
        {'id': 'law_without_injectivity', 'rationale': 'Report a law pair with a non-injective lift in the (2,2) census; the injectivity theorem excludes it.', 'mutate': law_without_injectivity},
        {'id': 'law_forces_observation_preservation', 'rationale': 'Claim every observation pair is preserved by a law lift; only q = q-prime-after-u pairs are (8 of 32 at (2,2,2)).', 'mutate': law_forces_observation_preservation},
        {'id': 'law_repairs_obstructions', 'rationale': 'Claim an old obstruction never persists through a law lift; it persists in 7 of the 16 obstruction pairs per law pair at (2,2,2).', 'mutate': law_repairs_obstructions},
        {'id': 'recovery_exists_for_larger_source', 'rationale': 'Claim a typed recovery exists from three old terms into two lifted points; injectivity (pigeonhole) forbids it.', 'mutate': recovery_exists_for_larger_source},
        {'id': 'recovery_unique_per_lift', 'rationale': 'Claim the recovery is determined by the lift (one law pair per injective lift); the off-image values are free so there are 18 law pairs over 6 lifts at (2,3).', 'mutate': recovery_unique_per_lift},
        {'id': 'law_counts_all_functions', 'rationale': 'Claim every pair satisfies the law in the (1,2) census; only the pairs recovering the lifted point do.', 'mutate': old_image_law_counts_all_functions},
        {'id': 'law_count_ignores_refusal_summand', 'rationale': 'Count the recoveries as a^(b-a) per lift (12 at (2,3)) forgetting that the refusal summand is also a value off the image; there are 18.', 'mutate': law_count_ignores_refusal_summand},
        {'id': 'law_forces_surjective_lift', 'rationale': 'Claim no recovery exists for a non-onto lift (law = 0 at (2,3)); every injective lift has one, and the 6 lifts give 18 recoveries.', 'mutate': law_forces_surjective_lift},
        {'id': 'empty_source_observation_failure', 'rationale': 'Claim observation preservation can fail for an empty source (8 of 8 are preserved at (0,3,2)); this is why observation_not_implied_general needs a nonempty A.', 'mutate': empty_source_observation_failure},
        {'id': 'surjective_lift_has_nonrefusing_recovery', 'rationale': 'Claim a law-satisfying recovery of a bijective lift accepts an off-image point; a bijection has no off-image point and its recovery is unique (6 pairs at (3,3)).', 'mutate': surjective_lift_has_nonrefusing_recovery},
    ]


def semantic_controls(data, profile):
    def reverse_record_order(d):
        d['records'].reverse()

    return [{'id': 'reverse_record_order', 'rationale': 'The cases are a set; any order of the same records is the same certificate.', 'mutate': reverse_record_order}]
