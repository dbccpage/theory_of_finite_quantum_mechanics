"""Semantic near misses for the inert-inscription certificate (PG-INERT-DIAMOND).

Each mutant is a well-formed record a reviewer could believe; each breaks one premise of the definition or is
a counterexample to the unpaid bridge named in does_not_support (the root Real_0 = Difference + Structure is not
derived from the inscription).
"""


def _record(data, max_len):
    return next(r for r in data['records'] if r['input'] == [max_len])


def semantic_mutants(data, profile):
    def supply_moves_state(d):
        r = _record(d, 3)
        r['supply_only_moved'] = r['supply_only_traces'] - 1

    def inscription_implies_coproduct(d):
        r = _record(d, 3)
        r['inscribed_with_coproduct'] += r['inscribed_no_coproduct']
        r['inscribed_no_coproduct'] = 0

    def coproduct_requires_inscription(d):
        r = _record(d, 3)
        r['inscribed_with_coproduct'] += r['uninscribed_with_coproduct']
        r['uninscribed_with_coproduct'] = 0

    def root_admission_gives_coproduct(d):
        _record(d, 4)['root_traces_with_coproduct'] = 3

    def mention_count_matters(d):
        _record(d, 4)['mention_prefix_diff'] = 100

    def inertness_is_spelling(d):
        _record(d, 4)['rival_mention_prefix_diff'] = 0

    def rooted_replay_accepts_everything(d):
        r = _record(d, 3)
        r['rooted_ok'] = r['traces'] - r['refused']

    def readmission_duplicates(d):
        _record(d, 2)['reachable_states'] += 6

    def root_supply_invisible_to_rooted(d):
        _record(d, 3)['root_omission_visible'] = 0

    def rooted_gate_is_vacuous(d):
        _record(d, 3)['rooted_refuses_unrooted_accepted'] = 0

    def later_supply_changes_rooted_outcome(d):
        _record(d, 3)['rooted_later_supply_changes'] = 5

    return [
        {'id': 'supply_moves_state', 'rationale': 'Claim a history of mentions alone leaves the empty state; here all but one nonempty supply-only history is said to move it (inertness is the L1 rule).', 'mutate': supply_moves_state},
        {'id': 'inscription_implies_coproduct', 'rationale': 'Claim every history that inscribes <> reaches coproduct structure, i.e. read the inscription as the root Real_0 = Difference + Structure.', 'mutate': inscription_implies_coproduct},
        {'id': 'coproduct_requires_inscription', 'rationale': 'Claim coproduct structure needs a supply of <>; the unrooted model reaches it by admitting two channel data alone (the Rust replay then refuses such a history for lacking the root event).', 'mutate': coproduct_requires_inscription},
        {'id': 'root_admission_gives_coproduct', 'rationale': 'Claim admitting <> itself already yields both channels; one admitted token carries one class.', 'mutate': root_admission_gives_coproduct},
        {'id': 'mention_count_matters', 'rationale': 'Claim an extra leading mention of <> changes the outcome for many histories; under the model rule it changes none.', 'mutate': mention_count_matters},
        {'id': 'inertness_is_spelling', 'rationale': 'Claim a leading mention of <> is inert under every step rule because of how it is spelled; under the rival rule (supply admits) it changes the outcome.', 'mutate': inertness_is_spelling},
        {'id': 'rooted_replay_accepts_everything', 'rationale': 'Ignore the requirement that the first event be the supply of <>: count every unrefused history as rooted.', 'mutate': rooted_replay_accepts_everything},
        {'id': 'readmission_duplicates', 'rationale': 'Count states as if re-admission of an admitted datum duplicated it (law L6 chooses designation), inflating the reachable states.', 'mutate': readmission_duplicates},
        {'id': 'root_supply_invisible_to_rooted', 'rationale': 'Claim the leading supply of <> is invisible to the rooted outcome; omitting it turns an accepted history into a refusal (MissingLiteralRoot), so it is an admission precondition, not inert.', 'mutate': root_supply_invisible_to_rooted},
        {'id': 'rooted_gate_is_vacuous', 'rationale': 'Claim every history accepted by the unrooted model is accepted by the rooted replay; the rooted gate refuses all histories not beginning with the supply of <>, including the empty one.', 'mutate': rooted_gate_is_vacuous},
        {'id': 'later_supply_changes_rooted_outcome', 'rationale': 'Claim that supplies after the root can change the rooted outcome; only the first supply is a precondition, later ones are inert.', 'mutate': later_supply_changes_rooted_outcome},
    ]


def semantic_controls(data, profile):
    def reverse_record_order(d):
        d['records'].reverse()

    return [{'id': 'reverse_record_order', 'rationale': 'The cases are a set; any order of the same records is the same certificate.', 'mutate': reverse_record_order}]
