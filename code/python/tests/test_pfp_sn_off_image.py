"""Exact controls for the S(n) off-image refusal certificate (PFP batch 01, PG-SN-OFF-IMAGE-REFUSAL)."""
import importlib.util
import unittest
from pathlib import Path

_SOURCE = Path(__file__).resolve().parents[1] / 'src/qm/pfp_sn_off_image.py'
_SPEC = importlib.util.spec_from_file_location('pfp_sn_off_image', _SOURCE)
m = importlib.util.module_from_spec(_SPEC)
_SPEC.loader.exec_module(m)


class SnOffImage(unittest.TestCase):
    def test_refusal_is_exactly_off_image_on_a_range_of_universes(self):
        for g in range(0, 4):
            for stages in (1, 2, 3):
                uni = m.universe(g, stages, 3)
                for n in range(stages):
                    image = {m.section_lift(n, b) for b in m.bases(g)}
                    for p in uni:
                        self.assertEqual(m.retr(n, p)[0] == 'nonDescent', p not in image, (g, stages, n, p))

    def test_accepted_payload_is_the_base_presentation(self):
        for g in range(0, 4):
            for n in range(3):
                for b in m.bases(g):
                    self.assertEqual(m.retr(n, m.section_lift(n, b)), ('accepted', m.to_pres(b)))

    def test_section_roundtrip_holds_on_image_and_fails_on_refused(self):
        r = m.record(2, 3, 3, 1)
        self.assertEqual(r['roundtrip_holds'], r['image_size'])
        self.assertEqual(r['roundtrip_fails'], r['refused'])
        self.assertEqual(r['roundtrip_holds'] + r['roundtrip_fails'], r['universe'])

    def test_other_stage_lifts_are_refused(self):
        for g in range(0, 4):
            for stages in (2, 3, 4):
                for n in range(stages):
                    for k in range(stages):
                        if k != n:
                            for b in m.bases(g):
                                self.assertEqual(m.retr(n, m.section_lift(k, b)), ('nonDescent',))

    def test_law_alone_does_not_refuse_lax_retraction(self):
        for g in range(0, 4):
            for b in m.bases(g):
                self.assertEqual(m.lax_retr(0, m.section_lift(0, b)), ('accepted', m.to_pres(b)))
        r = m.record(2, 4, 3, 0)
        self.assertEqual(r['lax_law_failures'], 0)
        self.assertEqual(r['lax_iff_violations'], r['refused'])
        self.assertGreater(r['refused'], 0)

    def test_toy_witness_matches_the_source_numbers(self):
        # source Rust witness: s(x) = 2x on {0,1,2}, 6 points, 3 on-image, 3 refused
        r = m.toy_record(3, 2)
        self.assertEqual((r['points'], r['on_image'], r['refused']), (6, 3, 3))
        self.assertEqual((r['law_failures'], r['sound_failures']), (0, 0))

    def test_toy_refusal_is_divisibility_on_a_range(self):
        for k in range(0, 7):
            for c in range(1, 6):
                r = m.toy_record(k, c)
                self.assertEqual(r['on_image'], k)
                self.assertEqual(r['refused'], (c - 1) * k)
                self.assertEqual((r['law_failures'], r['sound_failures']), (0, 0))

    def test_wire_format(self):
        lines = m.wire_lines(m.certificate())
        self.assertEqual(len(lines), len(m.CASES))
        self.assertEqual(lines[0], 'offimage\t0\t2\t2\t0\t6\t1\t5\t1\t0\t0\t1\t5\t1\t0\t0\t5')
        self.assertEqual(lines[8], 'toy\t3\t2\t6\t3\t3\t0\t0')
        self.assertEqual(m.public_tsv().count('\n'), len(m.CASES))


if __name__ == '__main__':
    unittest.main()
