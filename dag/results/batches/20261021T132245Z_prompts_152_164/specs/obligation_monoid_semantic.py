"""Semantic near misses for the obligation monoid certificate.

Each mutant is a well-formed record a reviewer could believe: a wrong algebraic reading of the monoid, a hidden
overflow or error case, or the unpaid bridge (events and S(n) maps are monoid morphisms) asserted from a table.
"""


def _find(data, kind, *args):
    return next(r for r in data['records'] if r['kind'] == kind and r['args'] == list(args))


def semantic_mutants(data, profile):
    def cancellation_fails_for_counters(d):
        _find(d, 'laws', 3, 3)['cancel_failures'] = 54

    def counters_form_a_group(d):
        _find(d, 'laws', 2, 3)['invertible_nonzero'] = 8

    def saturating_sum_is_cancellative(d):
        _find(d, 'saturating', 3)['cancel_failures'] = 0

    def overflow_hidden(d):
        r = _find(d, 'ledger', 'g:C:18446744073709551615,g:C:1')
        r['status'] = 'ok'
        r['fail_index'] = -1
        r['generated'] = [0, 0, 18446744073709551616]
        r['outstanding'] = [0, 0, 18446744073709551616]

    def bound_ignored(d):
        r = _find(d, 'bounded', 2, 5)
        r['defined_pairs'] = r['pairs']
        r['overflow_pairs'] = 0

    def discharge_of_ungenerated_is_ok(d):
        r = _find(d, 'ledger', 'd:A:1')
        r['status'] = 'ok'
        r['fail_index'] = -1

    def zero_discharge_is_an_error(d):
        r = _find(d, 'ledger', 'd:A:0')
        r['status'] = 'NeverGenerated'
        r['fail_index'] = 0

    def over_discharge_reported_as_never_generated(d):
        r = _find(d, 'ledger', 'g:A:2,d:A:3')
        r['status'] = 'NeverGenerated'

    def declare_then_assert_is_order_blind_fixed(d):
        _find(d, 'events', 'AD')['declare_then_assert'] = True

    def removal_counted_as_declaration(d):
        r = _find(d, 'events', 'R')
        r['destructive'] = 0
        r['terms'] = 1

    def trace_is_order_sensitive(d):
        _find(d, 'events', 'DARI')['perm_count'] = 1

    def bounded_combine_not_associative(d):
        _find(d, 'bounded', 1, 6)['definedness_mismatch'] = 1

    def saturating_sum_not_associative(d):
        _find(d, 'saturating', 3)['assoc_failures'] = 1

    def discharge_checked_against_generated(d):
        r = _find(d, 'ledger', 'g:A:2,d:A:2,d:A:1')
        r['status'] = 'ok'
        r['fail_index'] = -1
        r['discharged'] = [3, 0, 0]
        r['outstanding'] = [-1, 0, 0]
        r['settled'] = False

    def generation_at_the_bound_refused(d):
        r = _find(d, 'ledger', 'g:A:18446744073709551615,d:A:18446744073709551615')
        r['status'] = 'CountOverflow'
        r['fail_index'] = 0
        r['generated'] = [0, 0, 0]
        r['discharged'] = [0, 0, 0]
        r['outstanding'] = [0, 0, 0]
        r['settled'] = True

    return [
        {'id': 'cancellation_fails_for_counters', 'rationale': 'Claim x + z = y + z does not imply x = y for counter vectors; it holds, and failure belongs to saturating sums.', 'mutate': cancellation_fails_for_counters},
        {'id': 'counters_form_a_group', 'rationale': 'Claim nonzero counter vectors are invertible; an obligation count cannot be negative, so the monoid is not a group.', 'mutate': counters_form_a_group},
        {'id': 'saturating_sum_is_cancellative', 'rationale': 'Treat the saturating total as cancellative; saturating sums are associative and commutative but cancel only below the cap.', 'mutate': saturating_sum_is_cancellative},
        {'id': 'overflow_hidden', 'rationale': 'Accept a generated count above 2^64-1 instead of reporting CountOverflow.', 'mutate': overflow_hidden},
        {'id': 'bound_ignored', 'rationale': 'Count every pair as defined under the bound; pairs whose coordinate sum exceeds M are refused.', 'mutate': bound_ignored},
        {'id': 'discharge_of_ungenerated_is_ok', 'rationale': 'Let a positive discharge of a never-generated id succeed; the ledger refuses it.', 'mutate': discharge_of_ungenerated_is_ok},
        {'id': 'zero_discharge_is_an_error', 'rationale': 'Treat discharge of count zero as an error; the rule makes it a no-op even for a never-generated id.', 'mutate': zero_discharge_is_an_error},
        {'id': 'over_discharge_reported_as_never_generated', 'rationale': 'Swap the two refusal kinds: over-discharge needs a positive generated count.', 'mutate': over_discharge_reported_as_never_generated},
        {'id': 'declare_then_assert_is_order_blind', 'rationale': 'Claim the trace A D declares before it asserts; the counter condition ValidFresh holds but the order does not.', 'mutate': declare_then_assert_is_order_blind_fixed},
        {'id': 'removal_counted_as_declaration', 'rationale': 'Send the event removeDiff to the declare vector instead of the destructive one: a confusion of the term counter and the destructive counter (the table sends removeDiff and identifyTerms to the same destructive vector).', 'mutate': removal_counted_as_declaration},
        {'id': 'trace_is_order_sensitive', 'rationale': 'Claim the four-letter word has a single arrangement; the trace is invariant under all 24 permutations, which is why order is lost.', 'mutate': trace_is_order_sensitive},
        {'id': 'bounded_combine_not_associative', 'rationale': 'Claim the bounded combine is defined for one bracketing and not the other on some triple; both are defined exactly when every coordinate sum x+y+z is within the bound.', 'mutate': bounded_combine_not_associative},
        {'id': 'saturating_sum_not_associative', 'rationale': 'Claim the saturating sum fails associativity; it is associative and commutative and fails only cancellation.', 'mutate': saturating_sum_not_associative},
        {'id': 'discharge_checked_against_generated', 'rationale': 'Check a discharge against the total generated count instead of the outstanding count: g:A:2, d:A:2, d:A:1 would be accepted with discharged 3 > generated 2.', 'mutate': discharge_checked_against_generated},
        {'id': 'generation_at_the_bound_refused', 'rationale': 'Treat a generation that lands exactly on 2^64-1 as an overflow; only a count above the bound is refused.', 'mutate': generation_at_the_bound_refused},
    ]


def semantic_controls(data, profile):
    def reverse_record_order(d):
        d['records'].reverse()

    return [{'id': 'reverse_record_order', 'rationale': 'The cases are a set; any order of the same records is the same certificate.', 'mutate': reverse_record_order}]
