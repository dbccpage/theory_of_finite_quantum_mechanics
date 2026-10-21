"""Semantic near misses for the bridge-obligation status ledger.

Each mutant is a well-formed ledger row a reviewer could believe; each breaks one premise or states the unpaid bridge
(scoped controls read as discharge, four of five read as enough, an undischarged obligation hidden as passing).
"""


def _rec(data, code):
    return next(r for r in data['records'] if ''.join(str(s) for s in r['v']) == code)


def semantic_mutants(data, profile):
    def all_controls_pass_so_end_to_end(d):
        # the node reading (all five control-only) read as the end-to-end claim
        _rec(d, '11111')['end_to_end'] = True

    def four_of_five_is_enough(d):
        r = _rec(d, '22221')
        r['end_to_end'] = True
        r['completing_upgrades'] = 0

    def open_counts_as_control(d):
        # an obligation with no scoped control at all (open) read as having passed its control
        _rec(d, '01111')['controls_run'] = True

    def out_of_order_discharge_respects_programme_order(d):
        _rec(d, '00002')['prefix_order'] = True

    def final_step_not_available(d):
        # with four of five discharged, one monotone update does complete the claim; hide it
        _rec(d, '22221')['completing_upgrades'] = 0

    def discharged_can_still_move(d):
        _rec(d, '22222')['upgrades'] = 1

    def node_reading_is_end_to_end(d):
        # the node-reading vector 11111 replaced by the all-discharged vector
        _rec(d, '11111')['node_reading'] = False
        _rec(d, '22222')['node_reading'] = True

    def register_literal_reading(d):
        # the alternative reading: the register's literal word OPEN for every obligation, i.e. the vector 00000 instead of 11111
        _rec(d, '11111')['node_reading'] = False
        _rec(d, '00000')['node_reading'] = True

    def two_missing_one_update_completes(d):
        _rec(d, '22211')['completing_upgrades'] = 1

    def all_discharged_not_end_to_end(d):
        _rec(d, '22222')['end_to_end'] = False

    def prefix_flag_reversed(d):
        _rec(d, '22200')['prefix_order'] = False

    def no_control_at_all_passes(d):
        _rec(d, '00000')['controls_run'] = True

    return [
        {'id': 'all_controls_pass_so_end_to_end', 'rationale': 'Reads the source state (every scoped control passes, nothing discharged) as the end-to-end claim, the exact step the node says is unpaid.', 'mutate': all_controls_pass_so_end_to_end},
        {'id': 'four_of_five_is_enough', 'rationale': 'Leave-one-out: four discharged obligations and one control-only still mark the end-to-end claim true.', 'mutate': four_of_five_is_enough},
        {'id': 'open_counts_as_control', 'rationale': 'An obligation with no scoped control (open) is counted as having a passing control.', 'mutate': open_counts_as_control},
        {'id': 'out_of_order_discharge_respects_programme_order', 'rationale': 'Discharging only O05 while O01..O04 are open is read as consistent with the programme derivation order.', 'mutate': out_of_order_discharge_respects_programme_order},
        {'id': 'final_step_not_available', 'rationale': 'Denies that a single monotone update completes the ledger from four discharged, hiding the one remaining step.', 'mutate': final_step_not_available},
        {'id': 'discharged_can_still_move', 'rationale': 'Claims a fully discharged ledger can still be upgraded, mixing the progress order with a status above discharged.', 'mutate': discharged_can_still_move},
        {'id': 'node_reading_is_end_to_end', 'rationale': 'Moves the node-reading marker from the all-control-only vector to the all-discharged vector, overstating what the register says.', 'mutate': node_reading_is_end_to_end},
        {'id': 'register_literal_reading', 'rationale': 'Moves the node-reading marker to 00000 (every obligation literally OPEN, no scoped control counted), the alternative reading of the register wording.', 'mutate': register_literal_reading},
        {'id': 'two_missing_one_update_completes', 'rationale': 'With two obligations still undischarged, claims a single monotone update already completes the ledger.', 'mutate': two_missing_one_update_completes},
        {'id': 'all_discharged_not_end_to_end', 'rationale': 'Marks the all-discharged ledger as not end-to-end, breaking the definition in the other direction.', 'mutate': all_discharged_not_end_to_end},
        {'id': 'prefix_flag_reversed', 'rationale': 'Marks a discharged-prefix ledger (O01..O03 discharged) as violating the programme order.', 'mutate': prefix_flag_reversed},
        {'id': 'no_control_at_all_passes', 'rationale': 'Counts the all-open ledger as having a passing control on every obligation.', 'mutate': no_control_at_all_passes},
    ]


def semantic_controls(data, profile):
    def reverse_record_order(d):
        d['records'].reverse()

    return [{'id': 'reverse_record_order', 'rationale': 'The status vectors are a set; any order of the same rows is the same certificate.', 'mutate': reverse_record_order}]
