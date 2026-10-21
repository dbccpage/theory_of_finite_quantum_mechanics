"""Exact controls for the S(n) carrier certificate (PFP batch 01, PG-SN-CARRIER)."""
import importlib.util
import unittest
from pathlib import Path

_SOURCE = Path(__file__).resolve().parents[1] / 'src/qm/pfp_sn_carrier.py'
_SPEC = importlib.util.spec_from_file_location('pfp_sn_carrier', _SOURCE)
m = importlib.util.module_from_spec(_SPEC)
_SPEC.loader.exec_module(m)


class SnCarrier(unittest.TestCase):
    def test_old_image_law_on_every_base_presentation_and_stage(self):
        for g in range(0, 6):
            for n in range(0, 7):
                for b in m.bases(g):
                    self.assertEqual(m.retr(n, m.section_lift(n, b)), ('accepted', m.to_pres(b)))

    def test_lift_is_injective_with_the_closed_form_cardinality(self):
        for g in range(0, 8):
            base = m.bases(g)
            self.assertEqual(len(base), 1 + g + 3 * g * g)
            for n in (0, 3):
                self.assertEqual(len({m.section_lift(n, b) for b in base}), len(base))

    def test_lift_image_is_exactly_the_accepted_set_of_the_same_stage(self):
        for g in range(0, 4):
            uni = m.universe(g, 3, 3)
            for n in range(3):
                accepted = {p for p in uni if m.retr(n, p)[0] == 'accepted'}
                self.assertEqual(accepted, {m.section_lift(n, b) for b in m.bases(g)})

    def test_declared_table_is_no_stage_count_for_any_alphabet(self):
        for g in range(0, 60):
            total = 1 + g + 3 * g * g
            self.assertNotEqual(m.carrier_card(0), total)
            self.assertNotEqual(m.carrier_card(2), total)
            self.assertNotEqual(m.carrier_card(3), total)
            self.assertEqual(m.carrier_card(1) == total, g == 0)
            self.assertFalse(g == m.carrier_card(1) and g * g == m.carrier_card(2))

    def test_unrestricted_lift_collapses_non_base_presentations(self):
        for g in range(0, 5):
            uni = m.universe(g, 3, 3)
            fibre = [p for p in uni if m.unrestricted_lift(1, p) == ('lift', 1, ('glyphs', ()))]
            nonbase = len(uni) - len(m.bases(g))
            self.assertEqual(len(fibre), nonbase + 1)
            self.assertIn(('nonDescent',), fibre)
            self.assertIn(('ground',), fibre)

    def test_refusal_token_round_trip_changes_input(self):
        out = m.retr(0, m.unrestricted_lift(0, ('nonDescent',)))
        self.assertEqual(out, ('accepted', ('ground',)))
        self.assertNotEqual(out, ('accepted', ('nonDescent',)))

    def test_one_glyph_coincidences_are_only_coincidences(self):
        r = m.record(1, 3, 3)
        self.assertEqual(r['table_matches'], [False, True, False, True])
        self.assertEqual(r['table_equal_total_stages'], [5])

    def test_ground_carrier_is_declared_empty_while_ground_presentation_is_a_point(self):
        for g in range(0, 4):
            self.assertEqual(m.carrier_card(0), 0)
            self.assertEqual(m.bases(g)[0], ('ground',))

    def test_stage_guard_and_long_glyph_bodies(self):
        for g in range(0, 4):
            for n in range(4):
                for k in range(4):
                    if k != n:
                        for b in m.bases(g):
                            self.assertEqual(m.retr(n, m.section_lift(k, b)), ('nonDescent',))
        self.assertEqual(m.retr(1, ('lift', 1, ('glyphs', (0, 1, 0)))), ('nonDescent',))
        r = m.record(2, 4, 3)
        self.assertEqual((r['stage_mismatch_refused'], r['long_body_refused']), (4 * 3 * 15, 4 * 8))

    def test_table_versus_cumulative_counts_and_empty_alphabet(self):
        for g in range(1, 30):
            cum = [1, 1 + g, 1 + g + g * g, 1 + g + 3 * g * g]
            self.assertEqual([m.carrier_card(i) == cum[i] for i in range(4)], [False] * 4)
        self.assertEqual(m.record(0, 2, 2)['table_equal_total_stages'], [1])

    def test_wire_format(self):
        lines = m.wire_lines(m.certificate())
        self.assertEqual(len(lines), len(m.CASES))
        self.assertEqual(lines[2], 'carrier\t2\t4\t3\t1,2,4,4,4\t15\t1,2,4,8\t0,1,2,2\t0,0,0,0\t-\t60\t0\t15,15,15,15\t200\t185\t15\t186\t0\t1\t0\t180\t32\t1,3,7,15\t0,0,0,0')
        self.assertEqual(m.public_tsv().count('\n'), len(m.CASES))


if __name__ == '__main__':
    unittest.main()
