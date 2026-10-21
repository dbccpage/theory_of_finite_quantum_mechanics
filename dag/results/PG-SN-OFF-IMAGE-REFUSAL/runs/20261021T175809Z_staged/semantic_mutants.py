"""Semantic near misses for the PG-SN-OFF-IMAGE-REFUSAL certificate.

Each mutant is a well-formed record a reviewer could believe, and each breaks one premise of the node.
"""


def _rec(data, g, stages, n):
    return next(r for r in data['records'] if r['kind'] == 'offimage' and r['input'][0] == g and r['input'][1] == stages and r['input'][3] == n)


def _toy(data, k, c):
    return next(r for r in data['records'] if r['kind'] == 'toy' and r['input'] == [k, c])


def semantic_mutants(data, profile):
    def old_image_law_implies_refusal(d):
        r = _rec(d, 2, 4, 0)
        r['lax_refused'] = r['refused']

    def refusal_misses_a_off_image_point(d):
        _rec(d, 2, 4, 0)['iff_violations'] = 1

    def wrong_stage_lift_accepted(d):
        r = _rec(d, 2, 4, 3)
        r['stage_mismatch_refused'] -= 1

    def long_body_accepted(d):
        r = _rec(d, 3, 3, 2)
        r['long_body_refused'] -= 1

    def roundtrip_holds_everywhere(d):
        r = _rec(d, 1, 3, 1)
        r['roundtrip_holds'] = r['universe']
        r['roundtrip_fails'] = 0

    def single_stage_universe_hides_stage_test(d):
        r = _rec(d, 2, 1, 0)
        r['stage_mismatch_refused'] = 3 * 15

    def lax_retraction_breaks_the_law(d):
        _rec(d, 3, 4, 1)['lax_law_holds'] -= 1

    def payload_confuses_shapes(d):
        _rec(d, 2, 4, 0)['payload_failures'] = 1

    def accepted_beyond_the_image(d):
        r = _rec(d, 2, 4, 0)
        r['accepted'] = r['image_size'] + 1
        r['refused'] -= 1

    def section_lift_not_injective(d):
        r = _rec(d, 2, 4, 0)
        r['image_size'] -= 1
        r['lift_collisions'] = 1

    def toy_with_zero_multiplier(d):
        r = _toy(d, 3, 2)
        r['input'] = [3, 0]
        r['points'] = r['on_image'] = r['refused'] = 0

    def total_retraction_refuses_without_the_roundtrip_test(d):
        r = _toy(d, 3, 2)
        r['refused'] = 0
        r['on_image'] = r['points']

    def identity_section_has_off_image_points(d):
        r = _toy(d, 4, 1)
        r['refused'] = 1
        r['on_image'] = 3

    return [
        {'id': 'old_image_law_implies_refusal', 'rationale': 'Claim that a retraction obeying the old-image law already refuses every off-image point (lax violations 0); the lax retraction obeys the law and refuses none of the 185 off-image points.', 'mutate': old_image_law_implies_refusal},
        {'id': 'refusal_misses_a_off_image_point', 'rationale': 'Report one disagreement between refusal and off-image-ness for the pinned retraction; the characterisation has no exception on the universe.', 'mutate': refusal_misses_a_off_image_point},
        {'id': 'wrong_stage_lift_accepted', 'rationale': 'Claim one section image at another stage is accepted by r_n; the stage test is exact (15 of 15 per other stage are refused at g = 2).', 'mutate': wrong_stage_lift_accepted},
        {'id': 'long_body_accepted', 'rationale': 'Claim a three-or-more-glyph body at the right stage is accepted; only bodies of the five shapes are accepted.', 'mutate': long_body_accepted},
        {'id': 'roundtrip_holds_everywhere', 'rationale': 'Claim s(r(p)) = p for every presentation of the one-glyph universe; it fails on every refused point (37 of 42).', 'mutate': roundtrip_holds_everywhere},
        {'id': 'single_stage_universe_hides_stage_test', 'rationale': 'Report stage-mismatch refusals in a universe that has a single stage; there is no other stage to mismatch.', 'mutate': single_stage_universe_hides_stage_test},
        {'id': 'lax_retraction_breaks_the_law', 'rationale': 'Claim the lax retraction that accepts everything fails the old-image law; it obeys the law exactly, which is why the law cannot be the refusal.', 'mutate': lax_retraction_breaks_the_law},
        {'id': 'payload_confuses_shapes', 'rationale': 'Report one wrong payload (for example a retained pair read back as a simplex cut); accepted_only_from_section fixes the payload as the base presentation, and the universe has none wrong.', 'mutate': payload_confuses_shapes},
        {'id': 'accepted_beyond_the_image', 'rationale': 'Claim a retraction term r_n<..> or the refusal token is accepted by r_n, so more outcomes are accepted than there are section images (16 instead of 15 at g = 2).', 'mutate': accepted_beyond_the_image},
        {'id': 'section_lift_not_injective', 'rationale': 'Claim two base presentations lift to the same term (image smaller than Base, 14 of 15); the lift is injective.', 'mutate': section_lift_not_injective},
        {'id': 'toy_with_zero_multiplier', 'rationale': 'A toy section with multiplier 0 has no total left inverse y // 0 and is not one of the public cases.', 'mutate': toy_with_zero_multiplier},
        {'id': 'total_retraction_accepts_everything', 'rationale': 'Claim the toy witness (section 2x, retraction y // 2) leaves nothing to refuse; the round trip s(r(y)) = y refuses the 3 odd points of 6.', 'mutate': total_retraction_refuses_without_the_roundtrip_test},
        {'id': 'identity_section_has_off_image_points', 'rationale': 'Claim the identity section (multiplier 1) has an off-image point to refuse; a surjective section has none.', 'mutate': identity_section_has_off_image_points},
    ]


def semantic_controls(data, profile):
    def reverse_record_order(d):
        d['records'].reverse()

    return [{'id': 'reverse_record_order', 'rationale': 'The cases are a set; any order of the same records is the same certificate.', 'mutate': reverse_record_order}]
