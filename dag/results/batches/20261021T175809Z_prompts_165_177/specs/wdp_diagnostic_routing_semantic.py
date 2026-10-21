"""Semantic near misses for the diagnostic / routing / residual / authority tables.

Each mutant is a well-formed record a reviewer could believe; each breaks one premise or states the unpaid bridge
(a diagnostic class read as a routing terminal, as authority, or as another axis).
"""


def _find(data, kind, **keys):
    return next(r for r in data['records'] if r['kind'] == kind and all(r[k] == v for k, v in keys.items()))


def _sum(data, name):
    return _find(data, 'sum', name=name)


def semantic_mutants(data, profile):
    def exact_class_routes_to_check_passed(d):
        # the exact class has no declared route (its tag "ExactRepair" is not a PfpTerminal); read it as CheckPassed
        _find(d, 'diag', name='ExactClass')['route'] = 'CheckPassed'

    def closed_residual_routes_as_no_rule(d):
        # identify the closed class with ResidualClass.ClosedSurvivor and borrow its route
        _find(d, 'diag', name='ClosedResidual')['route'] = 'NoRule'

    def exact_class_certifies_without_witness(d):
        # diagnostic value read as authority: ExactClass tags certified with no descent witness
        _sum(d, 'authority')['ints'][5] = 2

    def unique_policy_forced(d):
        # claim the diagnostic determines the terminal: one policy, so no choice of policy
        _sum(d, 'policies')['ints'] = [3, 7, 1, 1, 0, 1, 21]

    def pfp_terminals_reach_all_seven(d):
        s = _sum(d, 'image_sizes')
        s['ints'][1] = 7
        s['items'] = [x for x in s['items'] if not x.startswith('pfp-missing')]

    def fiber_reaches_requires_lift(d):
        s = _sum(d, 'fiber_routes')
        s['ints'][3] = 5
        s['items'] = sorted(s['items'] + ['RequiresLift'])

    def route_determines_residual(d):
        s = _sum(d, 'determination')
        s['items'][1] = 'route->residual:1'

    def outside_profile_is_refuted(d):
        # collapse lack of applicability into refutation, exactly what outside_profile_ne_refuted separates
        _find(d, 'rel', in_profile=False, contradicted=True, supported=False)['status'] = 'refuted'

    def surjective_policy_exists(d):
        _sum(d, 'policies')['ints'][4] = 6

    def exact_tag_is_pfp_exact(d):
        # identify the run.rs tag "ExactRepair" with PfpTerminal::Exact and route it (changes two fields of the diag row)
        r = _find(d, 'diag', name='ExactClass')
        r['run_tag'] = 'Exact'
        r['route'] = 'CheckPassed'

    def closed_residual_cert_eligible(d):
        _find(d, 'diag', name='ClosedResidual')['cert_eligible'] = True

    def residual_determines_route(d):
        _sum(d, 'determination')['items'][0] = 'residual->route:1'

    def exact_class_counted_as_routed(d):
        _sum(d, 'diag_cells')['ints'] = [21, 3, 0, 18]

    def parse_refused_routes_to_refused(d):
        # a wrong source-table entry (ParseRefused routed to Refused instead of Refusal) kept consistent in the row only
        _find(d, 'stat', name='ParseRefused')['route'] = 'Refused'

    def no_rule_is_certifiable(d):
        _find(d, 'stat', name='NoRuleInSearchClass')['auth'] = 'Certifiable'

    return [
        {'id': 'exact_class_routes_to_check_passed', 'rationale': 'Gives the exact diagnostic class a declared routing terminal although run.rs emits the tag ExactRepair, which is not a PfpTerminal and has no route.', 'mutate': exact_class_routes_to_check_passed},
        {'id': 'closed_residual_routes_as_no_rule', 'rationale': 'Identifies the diagnostic class ClosedResidual with ResidualClass.ClosedSurvivor and borrows its NoRule route, ignoring that run.rs routes ClosedResidual to RequiresLift.', 'mutate': closed_residual_routes_as_no_rule},
        {'id': 'exact_class_certifies_without_witness', 'rationale': 'Counts certified statuses without a descent witness, i.e. reads a diagnostic value or tag as authority.', 'mutate': exact_class_certifies_without_witness},
        {'id': 'unique_policy_forced', 'rationale': 'Claims the diagnostic class forces its terminal (one policy), contradicting the 343 independent policies and the declared-policy reading of WDP-CH04-O01.', 'mutate': unique_policy_forced},
        {'id': 'pfp_terminals_reach_all_seven', 'rationale': 'Claims every routing terminal is reachable from PfpTerminal; Repair and NoRule are not in its image.', 'mutate': pfp_terminals_reach_all_seven},
        {'id': 'fiber_reaches_requires_lift', 'rationale': 'Claims terminal_from_fiber can produce RequiresLift; it never produces LiftRequired, BudgetUnknown or Refused.', 'mutate': fiber_reaches_requires_lift},
        {'id': 'route_determines_residual', 'rationale': 'Claims the routing terminal determines the residual class; Refusal comes from both a Refused and an Open status.', 'mutate': route_determines_residual},
        {'id': 'outside_profile_is_refuted', 'rationale': 'Reads an out-of-profile item as refuted, the exact distinction the external Routing.lean theorem outside_profile_ne_refuted protects.', 'mutate': outside_profile_is_refuted},
        {'id': 'surjective_policy_exists', 'rationale': 'Claims some policy from the three diagnostic classes covers all seven terminals, impossible by cardinality.', 'mutate': surjective_policy_exists},
        {'id': 'exact_tag_is_pfp_exact', 'rationale': 'Identifies the tag ExactRepair with PfpTerminal::Exact and gives the exact class the route CheckPassed (two fields of one row); the source has no such identification.', 'mutate': exact_tag_is_pfp_exact},
        {'id': 'closed_residual_cert_eligible', 'rationale': 'Makes ClosedResidual certificate-eligible; checked_packet.rs accepts only the exact class.', 'mutate': closed_residual_cert_eligible},
        {'id': 'residual_determines_route', 'rationale': 'Claims the residual class determines the routing terminal in the status tables; Open maps to four terminals.', 'mutate': residual_determines_route},
        {'id': 'exact_class_counted_as_routed', 'rationale': 'Counts three declared diagnostic-to-terminal cells and no unrouted class, hiding that the exact class has no route.', 'mutate': exact_class_counted_as_routed},
        {'id': 'parse_refused_routes_to_refused', 'rationale': 'A mistranscribed source-table entry: ParseRefused routed to Refused instead of Refusal (tests the shared transcription, which the unit test also compares with the Rust source text).', 'mutate': parse_refused_routes_to_refused},
        {'id': 'no_rule_is_certifiable', 'rationale': 'Marks the no-rule terminal authority-bearing; only ExactRuleDerived and UniqueOutputDerived are certifiable at tag level.', 'mutate': no_rule_is_certifiable},
    ]


def semantic_controls(data, profile):
    def reverse_record_order(d):
        d['records'].reverse()

    return [{'id': 'reverse_record_order', 'rationale': 'The public input lines are a set; any order of the same records is the same certificate.', 'mutate': reverse_record_order}]
