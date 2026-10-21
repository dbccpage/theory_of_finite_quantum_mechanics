"""Semantic near misses for the chain retraction certificate.

Each mutant is a well-formed record that a reviewer could believe: an extension that is said not to kill an old class
although no retraction exists, a hypothesis (subcomplex, section law) dropped, or the converse read in the wrong ring.
"""


def _rec(data, name):
    return next(r for r in data['records'] if r['name'] == name)


def semantic_mutants(data, profile):
    def isolated_points_retract(d):
        r = _rec(d, 'two_isolated_points_in_edge')
        r['rank_hi'] = [2, 0]
        r['killed'] = 0
        r['h_injective'] = True
        r['retraction_exists'] = True

    def triangle_class_survives_the_face(d):
        r = _rec(d, 'triangle_boundary_in_filled_triangle')
        r['rank_hi'] = [1, 1, 0]
        r['killed'] = 0
        r['h_injective'] = True

    def hollow_tetrahedron_class_survives(d):
        r = _rec(d, 'hollow_tetrahedron_in_solid_tetrahedron')
        r['rank_hi'] = [1, 0, 1, 0]
        r['killed'] = 0
        r['h_injective'] = True

    def injective_but_no_retraction(d):
        r = _rec(d, 'triangle_boundary_with_pendant_edge')
        r['retraction_exists'] = False
        r['retraction'] = []
        r['system_rank'] = 2

    def non_subcomplex_gets_homology(d):
        r = _rec(d, 'edge_without_its_endpoint_is_not_a_subcomplex')
        r['is_subcomplex'] = True
        r['dims_C'] = [1, 1, 0]
        r['betti_C'] = [1, 1, 0]

    def retraction_that_is_not_a_section(d):
        r = _rec(d, 'point_in_edge')
        r['retraction'][0][0][0] = '0'

    def skeleton_inclusion_retracts(d):
        r = _rec(d, 'tetrahedron_1_skeleton_in_2_skeleton')
        r['killed'] = 0
        r['rank_hi'] = [1, 3, 0]
        r['h_injective'] = True

    def identity_vertex_retraction_claimed(d):
        r = _rec(d, 'two_isolated_points_in_edge')
        r['retraction_exists'] = True
        r['retraction'] = [[['1', '0'], ['0', '1']], []]
        r['system_rank'] = 0
        r['augmented_rank'] = 0

    def injectivity_read_off_degree_zero(d):
        r = _rec(d, 'hollow_tetrahedron_in_solid_tetrahedron')
        r['killed'] = 0
        r['h_injective'] = True
        r['retraction_exists'] = True
        r['system_rank'] = 5
        r['augmented_rank'] = 5

    return [
        {'id': 'isolated_points_retract', 'rationale': 'Claim two isolated points are a retract of the edge joining them; the class p - q dies in the edge and cannot survive a retraction.', 'mutate': isolated_points_retract},
        {'id': 'triangle_class_survives_the_face', 'rationale': 'Claim the cycle of the triangle boundary survives attaching its face; the face kills it.', 'mutate': triangle_class_survives_the_face},
        {'id': 'hollow_tetrahedron_class_survives', 'rationale': 'Claim the degree-2 class of the hollow tetrahedron survives filling the solid.', 'mutate': hollow_tetrahedron_class_survives},
        {'id': 'injective_but_no_retraction', 'rationale': 'Deny the converse over Q on a case where the homology map is injective (this tests the converse enforcement of the checker); it fails over Z in a one-term instance, but a retraction exists over Q here.', 'mutate': injective_but_no_retraction},
        {'id': 'non_subcomplex_gets_homology', 'rationale': 'Treat an edge without its endpoint as a subcomplex; the inclusion is then not a chain map and the section hypothesis is dropped.', 'mutate': non_subcomplex_gets_homology},
        {'id': 'retraction_that_is_not_a_section', 'rationale': 'Present a chain map from the edge to the point whose restriction to the point is not the identity.', 'mutate': retraction_that_is_not_a_section},
        {'id': 'skeleton_inclusion_retracts', 'rationale': 'Claim the 1-skeleton of the tetrahedron is a retract of its 2-skeleton; the three independent 1-cycles bound faces.', 'mutate': skeleton_inclusion_retracts},
        {'id': 'identity_vertex_retraction_claimed', 'rationale': 'Claim a retraction of the edge onto its two endpoints that is the identity on the vertices (the section law holds) while ignoring that it must commute with the boundary: it would send the edge boundary (-1, 1) to 0.', 'mutate': identity_vertex_retraction_claimed},
        {'id': 'injectivity_read_off_degree_zero', 'rationale': 'Declare the homology map injective because it is in degree 0 while the degree-2 class of the hollow tetrahedron is killed.', 'mutate': injectivity_read_off_degree_zero},
    ]


def semantic_controls(data, profile):
    def reverse_record_order(d):
        d['records'].reverse()

    return [{'id': 'reverse_record_order', 'rationale': 'The cases are a set; any order of the same records is the same certificate.', 'mutate': reverse_record_order}]
