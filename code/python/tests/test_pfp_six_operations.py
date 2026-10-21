"""Exact controls for the six-operation state machine certificate (PFP batch 01, PG-SIX-OPERATIONS)."""
import importlib.util
import unittest
from itertools import product
from pathlib import Path

_SOURCE = Path(__file__).resolve().parents[1] / 'src/qm/pfp_six_operations.py'
_SPEC = importlib.util.spec_from_file_location('pfp_six_operations', _SOURCE)
m = importlib.util.module_from_spec(_SPEC)
_SPEC.loader.exec_module(m)


def all_ops(items):
    return [(k, x) for k in m.KINDS for x in range(items)]


class SixOperations(unittest.TestCase):
    def test_admitted_changes_iff_a_new_item_is_admitted_three_items_length_three(self):
        ops = all_ops(3)
        for mask in range(8):
            init = m.empty([x for x in range(3) if mask >> x & 1])
            for length in range(4):
                for trace in product(ops, repeat=length):
                    final = m.run(init, trace)
                    new_admit = any(k == 'admit' and x not in init[3] for k, x in trace)
                    self.assertEqual(final[3] != init[3], new_admit, (mask, trace))
                    self.assertEqual(final[3], init[3] | {x for k, x in trace if k == 'admit'})

    def test_the_other_five_operations_never_touch_admitted_in_any_reachable_state(self):
        ops = all_ops(2)
        for length in range(4):
            for trace in product(ops, repeat=length):
                s = m.run(m.empty(), trace)
                for kind in m.KINDS:
                    if kind == 'admit':
                        continue
                    for x in m.ITEMS:
                        self.assertEqual(m.step(s, (kind, x))[3], s[3])

    def test_trace_counts_match_the_closed_forms(self):
        rows = [m.trace_record(2, 4, mask) for mask in range(4)]
        self.assertEqual([r['traces'] for r in rows], [22621] * 4)
        self.assertEqual([r['changed'] for r in rows], [11510, 6516, 6516, 0])
        self.assertEqual([r['with_admit'] for r in rows], [11510] * 4)
        for r in rows:
            self.assertEqual(r['mismatches'], 0)
            self.assertEqual(r['changed'], r['with_new_admit'])

    def test_each_operation_writes_its_own_component_and_only_admit_writes_admitted(self):
        want = {'mention': '100000', 'supply': '010000', 'designate': '001000'}
        for kind, bits in want.items():
            row = m.footprint_record(kind)
            self.assertEqual((row['new_item_fields'], row['old_item_fields']), (bits, bits))
        self.assertEqual(m.footprint_record('admit')['new_item_fields'], '000100')
        self.assertEqual(m.footprint_record('admit')['old_item_fields'], '000000')
        self.assertEqual(m.footprint_record('retain')['new_item_fields'], '000000')
        self.assertEqual(m.footprint_record('retain')['old_item_fields'], '000010')
        self.assertEqual(m.footprint_record('operate')['old_item_fields'], '000001')

    def test_six_operations_have_pairwise_different_results_at_the_probe(self):
        probe = m.empty([0])
        results = [m.step(probe, (k, 0)) for k in m.KINDS]
        self.assertEqual(len(set(results)), 6)

    def test_readings_separated_by_admitted_state_only_without_conflation(self):
        row = m.reading_record(0)
        self.assertEqual((row['six_L_admitted'], row['six_F_admitted']), ([], [0]))
        self.assertEqual((row['conflated_L_admitted'], row['conflated_F_admitted']), ([0], [0]))
        self.assertTrue(row['six_separated'])
        self.assertFalse(row['conflated_separated'])

    def test_every_conflation_has_a_short_witness_and_only_admit_conflations_touch_admitted(self):
        for name, (a, b) in m.CONFLATIONS.items():
            row = m.conflation_record(name)
            self.assertLessEqual(row['min_len'], 2)
            self.assertEqual(row['admitted_differs'], b == 'admit')
            self.assertGreaterEqual(row['witness_count'], 1)
        self.assertEqual(m.conflation_record('designate_includes_retain')['witness'], ['admit:0', 'designate:0'])

    def test_retain_and_operate_are_separated_only_after_an_admission(self):
        row = m.pair_record('retain', 'operate')
        self.assertEqual(row['min_len'], 1)
        self.assertEqual(m.pair_record('mention', 'supply')['min_len'], 0)

    def test_repeated_admit_does_not_change_a_set_although_the_source_counter_would(self):
        s = m.run(m.empty(), [('admit', 0), ('admit', 0)])
        self.assertEqual(len(s[3]), 1)

    def test_wire_and_public_input_cover_every_case(self):
        data = m.certificate()
        self.assertEqual(len(m.wire_lines(data)), len(m.CASES))
        self.assertEqual(len(m.public_tsv().splitlines()), len(m.CASES))
        self.assertTrue(m.wire_lines(data)[0].startswith('trace\t2\t4\t0\t22621\t11510\t'))
        self.assertTrue(all(line == line.strip() and '\t\t' not in line for line in m.wire_lines(data)))


if __name__ == '__main__':
    unittest.main()
