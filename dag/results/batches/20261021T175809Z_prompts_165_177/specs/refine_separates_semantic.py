"""Semantic near misses for PG-REFINE-SEPARATES. Each is a well-formed record a reviewer might believe."""


def _rec(data, kind, **match):
    return next(r for r in data['records'] if r['kind'] == kind and all(r.get(k) == v for k, v in match.items()))


def semantic_mutants(data, profile):
    def triangle_one_bit(d):
        r = _rec(d, 'graph', name='triangle')
        r.update(bipartite=True, one_bit_tags=2, chi=2, min_bits=1, odd_girth=0)

    def odd_cycle_one_bit(d):
        r = _rec(d, 'graph', name='cycle5')
        r.update(bipartite=True, one_bit_tags=2, chi=2, min_bits=1, odd_girth=0)

    def fibre_of_three_one_bit(d):
        r = _rec(d, 'fiber', m=3)
        r.update(min_bits=1, injective_tags_by_bits=[0, 6, 24, 336])

    def tag_is_unique(d):
        _rec(d, 'graph', name='edge')['one_bit_tags'] = 1

    def components_ignored(d):
        _rec(d, 'graph', name='two_disjoint_edges')['one_bit_tags'] = 2

    def refinement_merges_old(d):
        _rec(d, 'refine', n=3, o=2, t=2)['old_separation_kept'] = 0

    def bits_equal_colours(d):
        _rec(d, 'graph', name='k5')['min_bits'] = 5

    def isomorphism_classes_for_labelled(d):
        r = _rec(d, 'enum', n=4)
        r.update(graphs=11, bipartite=7)

    def degree_bound_as_colouring(d):
        r = _rec(d, 'graph', name='k4')
        r.update(chi=2, min_bits=1, bipartite=True, one_bit_tags=2, odd_girth=0)

    def refinement_iff_fails(d):
        _rec(d, 'refine', n=3, o=2, t=2)['iff_failures'] = 1

    def tag_difference_separates_everything(d):
        _rec(d, 'refine', n=3, o=2, t=2)['separated_by_tag'] = 192

    def petersen_is_four_chromatic(d):
        r = _rec(d, 'graph', name='petersen')
        r.update(chi=4, odd_girth=3)

    def edgeless_needs_a_bit(d):
        _rec(d, 'graph', name='edgeless3')['min_bits'] = 1

    def dense_bipartite_is_not_bipartite(d):
        r = _rec(d, 'graph', name='k33')
        r.update(bipartite=False, one_bit_tags=0, chi=3, min_bits=2, odd_girth=3)

    return [
        {'id': 'refinement_iff_fails', 'rationale': 'Claim a refinement can leave a collapsed pair with different tags unseparated (or merge a pair): the equality of refined reports is exactly equality of both components.', 'mutate': refinement_iff_fails},
        {'id': 'tag_difference_separates_everything', 'rationale': 'Count every pair with different tags as separated by the tag, ignoring that pairs the old report already separates are not collapsed pairs.', 'mutate': tag_difference_separates_everything},
        {'id': 'petersen_is_four_chromatic', 'rationale': 'Confuse the odd girth with the chromatic number: the Petersen graph has odd girth 5 and chromatic number 3.', 'mutate': petersen_is_four_chromatic},
        {'id': 'edgeless_needs_a_bit', 'rationale': 'Claim a tag bit is needed when there is no conflict at all; zero bits suffice.', 'mutate': edgeless_needs_a_bit},
        {'id': 'dense_bipartite_is_not_bipartite', 'rationale': 'Read the dense complete bipartite graph K33 as non-2-colourable because it has many edges; density is not an odd cycle.', 'mutate': dense_bipartite_is_not_bipartite},
        {'id': 'triangle_one_bit', 'rationale': 'The source shows a Bool triangle cannot be 2-coloured only as a fixed instance; claiming one bit separates a 3-clique reads the supplied-tag theorem as if one tag always settles many conflicts.', 'mutate': triangle_one_bit},
        {'id': 'odd_cycle_one_bit', 'rationale': 'A 5-cycle has no triangle yet is not 2-colourable: forgetting the odd-cycle obstruction beyond cliques.', 'mutate': odd_cycle_one_bit},
        {'id': 'fibre_of_three_one_bit', 'rationale': 'A collapsed fibre of size 3 cannot be separated by one binary tag; the single-pair theorem does not give it.', 'mutate': fibre_of_three_one_bit},
        {'id': 'tag_is_unique', 'rationale': 'Treat the supplied tag as determined by the conflict: a proper tag and its complement are two distinct tags, so the choice is not forced.', 'mutate': tag_is_unique},
        {'id': 'components_ignored', 'rationale': 'Count proper tags as if the graph were connected: each connected component can be flipped independently.', 'mutate': components_ignored},
        {'id': 'refinement_merges_old', 'rationale': 'Claim a refinement can merge reports the old report distinguished; the old report is retained as a projection so it cannot.', 'mutate': refinement_merges_old},
        {'id': 'bits_equal_colours', 'rationale': 'Confuse the number of tag values (chi) with the number of bits (ceil log2 chi).', 'mutate': bits_equal_colours},
        {'id': 'isomorphism_classes_for_labelled', 'rationale': 'Report unlabelled graph counts for the labelled enumeration of all graphs on four vertices.', 'mutate': isomorphism_classes_for_labelled},
        {'id': 'degree_bound_as_colouring', 'rationale': 'Treat K4 as 2-colourable from a degree argument; a complete graph on 4 vertices needs 4 tag values, i.e. 2 bits.', 'mutate': degree_bound_as_colouring},
    ]


def semantic_controls(data, profile):
    def reverse_record_order(d):
        d['records'].reverse()

    return [{'id': 'reverse_record_order', 'rationale': 'The cases are a set; any order of the same records is the same certificate.', 'mutate': reverse_record_order}]
