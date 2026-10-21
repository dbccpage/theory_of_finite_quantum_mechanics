"""Exact controls for the diagnostic / routing / residual / authority-tag tables (PFP batch 01, PG-WDP-DIAGNOSTIC-NOT-ROUTING)."""
import importlib.util
import unittest
from itertools import product
from pathlib import Path

_SOURCE = Path(__file__).resolve().parents[1] / 'src/qm/pfp_wdp_diagnostic_routing.py'
_SPEC = importlib.util.spec_from_file_location('pfp_wdp_diagnostic_routing', _SOURCE)
m = importlib.util.module_from_spec(_SPEC)
_SPEC.loader.exec_module(m)


def summary(name):
    return next(r for r in m.certificate()['records'] if r['kind'] == 'sum' and r['name'] == name)


class DiagnosticRouting(unittest.TestCase):
    def test_axis_sizes_and_case_counts(self):
        self.assertEqual((len(m.STATUS_ROUTE), len(m.PFP_ROUTE), len(m.DIAG), len(m.ROUTES)), (21, 10, 3, 7))
        self.assertEqual(len(m.CASES), 21 + 10 + 3 + 8 + 640 + 8)
        self.assertEqual(len(m.DIAG) * len(m.ROUTES), 21)

    def test_all_seven_routes_are_reachable_from_terminal_statuses_but_not_from_pfp_terminals(self):
        self.assertEqual({r for _, r in m.STATUS_ROUTE}, set(m.ROUTES))
        self.assertEqual({r for _, r in m.PFP_ROUTE}, {'CheckPassed', 'RequiresLift', 'Refusal', 'Refused', 'BudgetUnknown'})

    def test_policies_none_forced_injective_exist_surjective_do_not(self):
        policies = list(product(range(7), repeat=3))
        self.assertEqual(len(policies), 343)
        self.assertEqual(sum(1 for p in policies if len(set(p)) == 3), 210)
        self.assertEqual(sum(1 for p in policies if len(set(p)) == 7), 0)
        for d, r in product(range(3), range(7)):
            self.assertTrue(any(p[d] == r for p in policies) and any(p[d] != r for p in policies))
        for d, e in [(0, 1), (0, 2), (1, 2)]:
            self.assertEqual(len({(p[d], p[e]) for p in policies}), 49)
        self.assertEqual(summary('policies')['ints'], [3, 7, 343, 210, 0, 49, 21])

    def test_exact_class_has_no_declared_route_and_closed_active_route_differently(self):
        recs = {r['name']: r for r in m.certificate()['records'] if r['kind'] == 'diag'}
        self.assertEqual(recs['ExactClass']['run_tag'], 'ExactRepair')
        self.assertEqual(recs['ExactClass']['route'], '-')
        self.assertEqual(recs['ClosedResidual']['route'], 'RequiresLift')
        self.assertEqual(recs['ActiveClosureFailure']['route'], 'Refusal')
        self.assertEqual(summary('diag_cells')['ints'], [21, 2, 1, 19])

    def test_residual_class_does_not_determine_route_and_vice_versa(self):
        det = dict(i.split(':') for i in summary('determination')['items'])
        self.assertEqual(det['residual->route'], '0')
        self.assertEqual(det['route->residual'], '0')
        self.assertEqual(det['route->auth'], '1')
        self.assertEqual(det['auth->route'], '0')
        open_routes = {r for n, r in m.STATUS_ROUTE if m.residual_of(n) == 'Open'}
        self.assertEqual(open_routes, {'Repair', 'BudgetUnknown', 'RequiresLift', 'Refusal'})
        self.assertEqual(summary('residual_routing')['ints'], [28, 8])

    def test_fiber_classifier_reaches_four_routes_over_a_wider_range(self):
        reached = set()
        for sel, cand, out, exh, agr, ver in product((False, True), range(9), range(9), (False, True), m.AGREEMENTS, (False, True)):
            s = m.fiber_status(sel, cand, out, exh, agr, ver)
            if s != 'ERR':
                reached.add(dict(m.STATUS_ROUTE)[s])
        self.assertEqual(reached, {'CheckPassed', 'Repair', 'NoRule', 'Refusal'})
        self.assertEqual(summary('fiber_routes')['ints'], [640, 400, 240, 4])

    def test_relative_status_axis_outside_profile_is_never_refuted(self):
        for c, s in product((False, True), repeat=2):
            self.assertEqual(m.rel_status(False, c, s), 'outsideProfile')
        for t in product((False, True), repeat=3):
            if m.rel_status(*t) == 'refuted':
                self.assertTrue(t[0])
        self.assertEqual(len({m.rel_status(*t) for t in product((False, True), repeat=3)}), 4)

    def test_authority_tag_is_never_certified_from_the_tag_alone(self):
        auth = summary('authority')['ints']
        self.assertEqual(auth, [21, 2, 4, 15, 2, 0, 2])
        self.assertEqual(sum(1 for n, _ in m.STATUS_ROUTE if m.auth_of(n) not in ('Certifiable', 'Refused', 'Uncertified')), 0)

    def test_wire_format(self):
        lines = m.wire_lines(m.certificate())
        self.assertEqual(len(lines), len(m.CASES))
        self.assertEqual(lines[0], 'stat\t0\tExactRuleDerived\tCheckPassed\tExact\tCertifiable\t1')
        self.assertEqual(lines[31], 'diag\t0\tExactClass\tExactRepair\t-\t1')
        self.assertTrue(lines[-1].startswith('sum\tauthority\t21;2;4;15;2;0;2\t-'))


if __name__ == '__main__':
    unittest.main()
