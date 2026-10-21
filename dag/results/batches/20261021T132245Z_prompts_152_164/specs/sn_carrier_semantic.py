"""Semantic near misses for the PG-SN-CARRIER certificate.

Each mutant is a well-formed record a reviewer could believe, and each breaks one premise of the node.
"""


def _rec(data, g):
    return next(r for r in data['records'] if r['input'][0] == g)


def semantic_mutants(data, profile):
    def table_read_as_shape_counts(d):
        _rec(d, 2)['table_matches'] = [True, True, True, True]

    def table_matches_pair_count_at_one_glyph(d):
        _rec(d, 1)['table_matches'][2] = True

    def ground_presentation_counted_as_carrier(d):
        _rec(d, 3)['table_matches'][0] = True

    def unrestricted_lift_has_recovery(d):
        r = _rec(d, 2)
        r['unrestricted_injective'] = True
        r['unrestricted_fibre_over_ground'] = 1

    def refusal_token_recovered(d):
        r = _rec(d, 2)
        r['refusal_round_trip_returns_token'] = True
        r['refusal_round_trip_accepts_ground'] = False

    def lift_image_shrinks_with_stage(d):
        r = _rec(d, 2)
        r['lift_image_sizes'][-1] = 2

    def ledger_defect_read_as_restricted_failure(d):
        _rec(d, 3)['old_image_failures'] = 1

    def mismatched_stage_lift_accepted(d):
        _rec(d, 2)['stage_mismatch_refused'] -= 1

    def long_glyph_body_accepted(d):
        _rec(d, 3)['long_body_refused'] -= 1

    def table_read_as_cumulative_counts(d):
        _rec(d, 2)['cumulative_matches'] = [False, True, True, False]

    def empty_alphabet_coincidence_read_as_general(d):
        _rec(d, 2)['table_equal_total_stages'] = [1]

    return [
        {'id': 'table_read_as_shape_counts', 'rationale': 'Claim the declared table 0,1,2,2 equals the per-stage presentation counts over a two-glyph alphabet (1,2,4,8); no alphabet size makes stages 1 and 2 agree.', 'mutate': table_read_as_shape_counts},
        {'id': 'table_matches_pair_count_at_one_glyph', 'rationale': 'With one glyph the supplied and cut/simplex counts happen to equal the table (1 and 2) but the pair count is 1, not the declared 2.', 'mutate': table_matches_pair_count_at_one_glyph},
        {'id': 'ground_presentation_counted_as_carrier', 'rationale': 'Read the length-one ground token as a one-point carrier; the source declares the index-zero carrier empty while the ground presentation is one point of Base.', 'mutate': ground_presentation_counted_as_carrier},
        {'id': 'unrestricted_lift_has_recovery', 'rationale': 'Claim the unrestricted (pre-repair) lift is injective; the refusal token and every lift/retraction term collide with the ground presentation.', 'mutate': unrestricted_lift_has_recovery},
        {'id': 'refusal_token_recovered', 'rationale': 'Claim the refusal token survives the unrestricted round trip; it returns as the ground presentation.', 'mutate': refusal_token_recovered},
        {'id': 'lift_image_shrinks_with_stage', 'rationale': 'Claim the image of the section lift at the last stage has the declared-table size 2; the lift is injective so every stage has the full Base cardinality.', 'mutate': lift_image_shrinks_with_stage},
        {'id': 'mismatched_stage_lift_accepted', 'rationale': 'Claim one section image at another stage is accepted by r_n; the stage guard is exact (180 of 180 mismatched pairs are refused at g = 2 over four stages).', 'mutate': mismatched_stage_lift_accepted},
        {'id': 'long_glyph_body_accepted', 'rationale': 'Claim a lift whose glyph body has three or more glyphs is accepted at its own stage; only the five base shapes are (108 such refusals at g = 3).', 'mutate': long_glyph_body_accepted},
        {'id': 'table_read_as_cumulative_counts', 'rationale': 'Compare the declared table 0,1,2,2 with the cumulative counts 1,3,7,15 over two glyphs and claim agreement at stages 1 and 2; no stage agrees.', 'mutate': table_read_as_cumulative_counts},
        {'id': 'empty_alphabet_coincidence_read_as_general', 'rationale': 'The table equals the base total at stage 1 only for the empty alphabet (total 1); claiming it for a two-glyph alphabet reads the degenerate case as general.', 'mutate': empty_alphabet_coincidence_read_as_general},
        {'id': 'ledger_defect_read_as_restricted_failure', 'rationale': 'Read WDP-P001-019 as saying the pinned restricted lift fails the old-image law; the law holds on every base presentation, the defect belongs to the unrestricted interface.', 'mutate': ledger_defect_read_as_restricted_failure},
    ]


def semantic_controls(data, profile):
    def reverse_record_order(d):
        d['records'].reverse()

    return [{'id': 'reverse_record_order', 'rationale': 'The cases are a set; any order of the same records is the same certificate.', 'mutate': reverse_record_order}]
