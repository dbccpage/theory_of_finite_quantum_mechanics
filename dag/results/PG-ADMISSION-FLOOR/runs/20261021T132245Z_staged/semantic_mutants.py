"""Semantic near misses for the admission floor certificate.

Each mutant is a well-formed record a reviewer could believe; each reads a fixed instance as a general statement,
drops a hypothesis, or derives the law from distinctness.
"""


def _rec(data, kind, n):
    return next(r for r in data['records'] if r['kind'] == kind and r['n'] == n)


def semantic_mutants(data, profile):
    def relatedness_implies_distinctness(d):
        r = _rec(d, 'classify', 1)
        r['unrelated_equal'] += r['related_equal']
        r['related_equal'] = 0

    def distinctness_implies_relatedness(d):
        r = _rec(d, 'classify', 2)
        r['related_distinct'] += r['unrelated_distinct']
        r['unrelated_distinct'] = 0

    def cut_on_a_subsingleton(d):
        r = _rec(d, 'classify', 1)
        r['cut_relations'] = 1
        r['cut_triples'] = 1

    def law_requires_an_instance(d):
        r = _rec(d, 'classify', 3)
        r['law_without_instance'] = 0

    def instance_forces_the_law(d):
        r = _rec(d, 'classify', 3)
        r['law_bearing'] += r['instance_without_law']
        r['instance_without_law'] = 0

    def identification_preserves_the_law(d):
        r = _rec(d, 'identify', 2)
        r['rq_overlap'] = 2
        r['cut_q_identified_with_target'] = 2

    def separation_does_not_suffice(d):
        r = _rec(d, 'identify', 3)
        r['rq_with_target'] -= 1
        r['rq_identifying'] += 1

    return [
        {'id': 'relatedness_implies_distinctness', 'rationale': 'Read the third pointed-relation clause without its irreflexivity hypothesis: no self-loop on the one-point carrier.', 'mutate': relatedness_implies_distinctness},
        {'id': 'distinctness_implies_relatedness', 'rationale': 'Claim two distinct marked points are always related; the empty relation on two points is the counterexample.', 'mutate': distinctness_implies_relatedness},
        {'id': 'cut_on_a_subsingleton', 'rationale': 'Allow an exhibited cut on a one-point carrier; the law and the instance cannot both hold there.', 'mutate': cut_on_a_subsingleton},
        {'id': 'law_requires_an_instance', 'rationale': 'Claim the empty relation is not law-bearing because it exhibits nothing; the law alone holds on any carrier.', 'mutate': law_requires_an_instance},
        {'id': 'instance_forces_the_law', 'rationale': 'Claim every relation with an exhibited pair is irreflexive; the total relation on one point is the counterexample.', 'mutate': instance_forces_the_law},
        {'id': 'identification_preserves_the_law', 'rationale': 'Claim some map identifying two related points still carries the relation into an irreflexive target.', 'mutate': identification_preserves_the_law},
        {'id': 'separation_does_not_suffice', 'rationale': 'Claim a map separating all related pairs can still fail to have a law-bearing target; the inequality relation is such a target.', 'mutate': separation_does_not_suffice},
    ]


def semantic_controls(data, profile):
    def reverse_record_order(d):
        d['records'].reverse()

    return [{'id': 'reverse_record_order', 'rationale': 'The cases are a set; any order of the same records is the same certificate.', 'mutate': reverse_record_order}]
