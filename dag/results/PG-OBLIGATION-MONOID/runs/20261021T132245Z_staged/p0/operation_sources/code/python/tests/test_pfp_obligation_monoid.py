"""Exact controls for the obligation monoid certificate (PFP batch 01, PG-OBLIGATION-MONOID)."""
import importlib.util
import unittest
from itertools import product
from pathlib import Path

_SOURCE = Path(__file__).resolve().parents[1] / 'src/qm/pfp_obligation_monoid.py'
_SPEC = importlib.util.spec_from_file_location('pfp_obligation_monoid', _SOURCE)
m = importlib.util.module_from_spec(_SPEC)
_SPEC.loader.exec_module(m)
CERT = m.certificate()


def rec(kind, *args):
    return next(r for r in CERT['records'] if r['kind'] == kind and r['args'] == list(args))


class ObligationMonoid(unittest.TestCase):
    def test_counter_vectors_are_a_cancellative_commutative_monoid_not_a_group(self):
        for r in CERT['records']:
            if r['kind'] == 'laws':
                self.assertEqual((r['assoc_failures'], r['comm_failures'], r['unit_failures'], r['cancel_failures']), (0, 0, 0, 0), r['args'])
                self.assertEqual(r['invertible_nonzero'], 0, r['args'])

    def test_free_commutative_monoid_universal_property_on_a_box(self):
        # lift f x = sum x_i f_i into Z/5; additive, equals f on singles, and any word of singles for x gives it
        mod = 5
        for k in (1, 2, 3):
            for f in product(range(mod), repeat=k):
                def lift(x):
                    return sum(a * b for a, b in zip(x, f)) % mod
                for x in product(range(3), repeat=k):
                    for y in product(range(3), repeat=k):
                        self.assertEqual(lift(m.vadd(x, y)), (lift(x) + lift(y)) % mod)
                    total = 0
                    for i, c in enumerate(x):  # decompose x as a sum of basis vectors in a fixed order
                        total = (total + c * f[i]) % mod
                    self.assertEqual(lift(x), total)

    def test_bounded_combine_is_partially_associative_with_matching_definedness(self):
        for r in CERT['records']:
            if r['kind'] == 'bounded':
                self.assertEqual((r['definedness_mismatch'], r['value_mismatch']), (0, 0), r['args'])
                self.assertGreater(r['overflow_pairs'], 0)
        r = rec('bounded', 1, 6)
        self.assertEqual(r['defined_pairs'], 28)  # pairs (a, b) with a + b <= 6 over 0..6

    def test_saturating_total_is_not_cancellative(self):
        for cap in (3, 6):
            r = rec('saturating', cap)
            self.assertEqual(r['cancel_failures'], cap * (cap + 1) * (cap + 2) // 3)
            self.assertEqual(r['assoc_failures'], 0)

    def test_event_trace_is_a_monoid_homomorphism_and_forgets_order(self):
        for word in ('', 'D', 'DAR', 'DARI', 'IRAD', 'DDAARR'):
            self.assertEqual(m.events(word or '-')['split_failures'], 0)
        self.assertEqual(m.trace('DA'), m.trace('AD'))
        self.assertEqual(m.trace('R'), m.trace('I'))  # the event table is not injective
        self.assertEqual(m.events('DARI')['perm_count'], 24)
        self.assertEqual(m.events('DARI')['perm_trace_failures'], 0)

    def test_cost_is_length_and_valid_fresh_is_order_blind(self):
        for w in ('D', 'DA', 'AD', 'DAR', 'RI'):
            self.assertEqual(m.events(w)['cost'], len(w))
        ad, da = m.events('AD'), m.events('DA')
        self.assertTrue(ad['valid_fresh'] and da['valid_fresh'])
        self.assertFalse(ad['declare_then_assert'])
        self.assertTrue(da['declare_then_assert'])
        self.assertGreaterEqual(da['cost'], 2)

    def test_ledger_refusal_modes_and_precedence(self):
        self.assertEqual(m.ledger('d:A:1')['status'], 'NeverGenerated')
        self.assertEqual(m.ledger('d:A:0')['status'], 'ok')           # zero discharge is a no-op
        self.assertEqual(m.ledger('g:A:0,d:A:1')['status'], 'NeverGenerated')
        self.assertEqual(m.ledger('g:A:2,d:A:3')['status'], 'OverDischarge')
        self.assertEqual(m.ledger('g:C:18446744073709551615,g:C:1')['status'], 'CountOverflow')
        self.assertTrue(m.ledger('g:A:2,d:A:1,d:A:1')['settled'])
        exact = m.ledger('g:A:18446744073709551615,d:A:18446744073709551615')  # lands exactly on the bound: allowed
        self.assertEqual((exact['status'], exact['generated'], exact['settled']), ('ok', [18446744073709551615, 0, 0], True))
        self.assertEqual(m.ledger('g:A:18446744073709551615,g:A:1,d:A:1')['fail_index'], 1)

    def test_ledger_invariant_discharged_never_exceeds_generated_on_all_short_traces(self):
        ops = [('g', i, c) for i in range(3) for c in (0, 1, 2)] + [('d', i, c) for i in range(3) for c in (0, 1, 2)]
        for length in range(0, 4):
            for trace in product(ops, repeat=length):
                arg = ','.join('%s:%s:%d' % (k, 'ABC'[i], c) for k, i, c in trace) or '-'
                r = m.ledger(arg)
                self.assertTrue(all(d <= g for g, d in zip(r['generated'], r['discharged'])), arg)
                self.assertEqual(r['outstanding'], [g - d for g, d in zip(r['generated'], r['discharged'])])

    def test_wire_format_lines(self):
        lines = m.wire_lines(CERT)
        self.assertEqual(len(lines), len(m.CASES))
        self.assertEqual(lines[0], 'laws\t1\t5\t5\t125\t0\t0\t0\t0\t0')
        self.assertIn('ledger\td:A:1\tNeverGenerated\t0\t0,0,0\t0,0,0\t0,0,0\t1', lines)


if __name__ == '__main__':
    unittest.main()
