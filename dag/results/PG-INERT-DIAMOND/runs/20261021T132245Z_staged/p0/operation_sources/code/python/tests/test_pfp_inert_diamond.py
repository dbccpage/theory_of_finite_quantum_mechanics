"""Exact controls for the inert-inscription certificate (PFP batch 01, PG-INERT-DIAMOND)."""
import importlib.util
import unittest
from itertools import product
from pathlib import Path

_SOURCE = Path(__file__).resolve().parents[1] / 'src/qm/pfp_inert_diamond.py'
_SPEC = importlib.util.spec_from_file_location('pfp_inert_diamond', _SOURCE)
m = importlib.util.module_from_spec(_SPEC)
_SPEC.loader.exec_module(m)

SUPPLY0 = ('s', 0)


def traces(max_len):
    for n in range(max_len + 1):
        yield from product(m.EVENTS, repeat=n)


class InertDiamond(unittest.TestCase):
    def test_closed_form_trace_counts(self):
        for L in range(0, 5):
            r = m.record(L)
            self.assertEqual(r['traces'], (8 ** (L + 1) - 1) // 7)
            self.assertEqual(r['supply_only_traces'], (3 ** (L + 1) - 1) // 2)
            self.assertEqual(r['root_traces'], 2 ** (L + 1) - 1)

    def test_supply_deletion_and_mention_prefix_never_change_the_outcome(self):
        for trace in traces(4):
            kept = [e for e in trace if e[0] != 's']
            self.assertEqual(m.replay(trace), m.replay(kept))
            self.assertEqual(m.replay((SUPPLY0,) + trace), m.replay(trace))
            self.assertEqual(m.replay(((SUPPLY0,) * 3) + trace), m.replay(trace))

    def test_only_admission_class_events_move_the_state(self):
        states = {m.replay(t) for t in traces(3)} - {None}
        for state in states:
            for ev in m.EVENTS:
                after = m.step(state, ev)
                if after is not None and after != state:
                    self.assertNotEqual(ev[0], 's')

    def test_root_only_histories_never_have_coproduct_for_any_classification(self):
        # one admitted token carries one class: try every assignment of classes to token 0
        for cls0 in (None, 'diff', 'struct'):
            for trace in traces(5):
                if all(e in (SUPPLY0, ('a', 0)) for e in trace):
                    state = m.replay(trace)
                    classes = {cls0 for t in state[0]}
                    self.assertFalse('diff' in classes and 'struct' in classes)

    def test_inscription_and_coproduct_are_independent(self):
        both = m.replay([SUPPLY0, ('a', 1), ('a', 2)])
        only_inscription = m.replay([SUPPLY0])
        without = m.replay([('a', 1), ('a', 2)])
        self.assertTrue(m.has_coproduct(both))
        self.assertFalse(m.has_coproduct(only_inscription))
        self.assertTrue(m.has_coproduct(without))

    def test_rival_rule_breaks_inertness(self):
        self.assertEqual(m.replay([SUPPLY0]), m.INIT)
        self.assertNotEqual(m.replay([SUPPLY0], m.INIT, m.rival_step), m.INIT)
        self.assertGreater(m.record(3)['rival_mention_prefix_diff'], 0)

    def test_arity_zero_is_refused_and_readmission_designates(self):
        self.assertIsNone(m.replay([('f', 0)]))
        self.assertIsNone(m.replay([('a', 1), ('f', 0), ('a', 2)]))
        self.assertEqual(m.replay([('a', 1), ('a', 1)]), (((1,)), ()))

    def test_rooted_replay_makes_the_first_supply_a_precondition_and_later_supplies_inert(self):
        for trace in traces(4):
            if trace and trace[0] == SUPPLY0:
                kept = [trace[0]] + [e for e in trace[1:] if e[0] != 's']
                self.assertEqual(m.rooted_replay(trace), m.rooted_replay(kept))
                if m.rooted_replay(trace) is not None and not (len(trace) > 1 and trace[1] == SUPPLY0):
                    self.assertIsNone(m.rooted_replay(trace[1:]))
            else:
                self.assertIsNone(m.rooted_replay(trace))
        self.assertIsNone(m.rooted_replay([('s', 1)]))
        self.assertIsNone(m.rooted_replay([]))
        self.assertIsNotNone(m.replay([]))

    def test_wire_format(self):
        lines = m.wire_lines(m.certificate())
        self.assertEqual(len(lines), len(m.CASES))
        self.assertTrue(lines[1].startswith('inert\t1\t9\t1\t1\t0\t4\t0\t4\t5\t0\t1\t0\t0\t0\t1\t3\t0\t0\t6\t3\t0\t1\t7'))
        self.assertTrue(all(line == line.strip() and '\t\t' not in line for line in lines))


if __name__ == '__main__':
    unittest.main()
