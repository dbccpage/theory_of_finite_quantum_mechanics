"""Unit tests for the 11 WDP foundational bridges and derivations."""

from __future__ import annotations

import unittest
from fractions import Fraction

from witnessed_difference.exact_linear import ExactField
from witnessed_difference.foundational_bridges import (
    EvaluationStatus,
    FiniteTransducer,
    Inscription,
    MathematicalReceipt,
    MultiplicityDistribution,
    admit_mark,
    apartness_witness,
    bool_d0,
    bool_d1,
    bool_xor,
    check_no_authority_effect,
    compute_triangle_mark_differences,
    empty_inscription,
    evaluate_report_claim,
    find_rational_l1_minimizer,
    product_transducer,
    rational_l1_norm,
    solve_frustrated_spin_cycle,
    verify_deterministic_retention,
    verify_flat_locus_curvature,
    verify_triangle_coboundary_zero,
)
from witnessed_difference.outcomes import Accepted, AuthorityEffect, RefusalCode, Refused


class TestFoundationalBridges(unittest.TestCase):
    def test_bridge_1_inscription_and_marks(self) -> None:
        e = empty_inscription()
        self.assertEqual(e.depth, 0)
        self.assertEqual(admit_mark(e), "mark_0")

        n1 = e.nest()
        self.assertEqual(n1.depth, 1)
        self.assertEqual(admit_mark(n1), "mark_1")

        n2 = n1.nest()
        self.assertEqual(n2.depth, 2)
        self.assertEqual(admit_mark(n2), "mark_2")

        diff = apartness_witness(e, n1)
        self.assertIsInstance(diff, Accepted)
        self.assertEqual(diff.value, True)

        same = apartness_witness(n1, Inscription(depth=1))
        self.assertIsInstance(same, Refused)
        self.assertEqual(same.code, RefusalCode.NOT_DISJOINT)

    def test_bridge_2_marks_to_cochains(self) -> None:
        self.assertFalse(bool_xor(True, True))
        self.assertTrue(bool_xor(True, False))
        self.assertTrue(bool_xor(False, True))
        self.assertFalse(bool_xor(False, False))

        f_vals = {"u": True, "v": False, "w": True}
        f = lambda x: f_vals[x]

        self.assertTrue(bool_d0(f, "u", "v"))
        self.assertFalse(bool_d0(f, "u", "w"))

        res = verify_triangle_coboundary_zero(f, "u", "v", "w")
        self.assertIsInstance(res, Accepted)
        self.assertEqual(res.value, True)

        # Refusal branch when 1-cochain is not closed (e.g. non-differential boundary)
        bad_e = lambda u, v: True
        res_bad = verify_triangle_coboundary_zero(f, "u", "v", "w", e_override=bad_e)
        self.assertIsInstance(res_bad, Refused)
        self.assertEqual(res_bad.code, RefusalCode.NOT_A_DIFFERENTIAL)

        # Test all 8 binary combinations on 3 points
        for b_u in (False, True):
            for b_v in (False, True):
                for b_w in (False, True):
                    mapping = {"u": b_u, "v": b_v, "w": b_w}
                    fn = lambda x: mapping[x]
                    r = verify_triangle_coboundary_zero(fn, "u", "v", "w")
                    self.assertIsInstance(r, Accepted)

    def test_bridge_2_non_boolean_cochains_are_refused(self) -> None:
        for invalid in (0, 1, None, "False", 0.0, 1.0):
            with self.subTest(value=invalid):
                with self.assertRaises(TypeError):
                    bool_xor(invalid, False)
                result = verify_triangle_coboundary_zero(lambda _: invalid, "a", "b", "c")
                self.assertIsInstance(result, Refused)
                self.assertEqual(result.code, RefusalCode.INVALID_INPUT)
                edge_result = verify_triangle_coboundary_zero(
                    lambda _: False, "a", "b", "c", e_override=lambda _u, _v: invalid
                )
                self.assertIsInstance(edge_result, Refused)
                self.assertEqual(edge_result.code, RefusalCode.INVALID_INPUT)

    def test_bridge_3_genesis_to_contextual_observers(self) -> None:
        t1 = FiniteTransducer(
            num_states=2,
            num_inputs=2,
            step_table=((1, 0), (0, 1)),
        )
        self.assertEqual(t1.step(0, 0), 1)
        self.assertEqual(t1.step(0, 1), 0)
        self.assertEqual(t1.step(1, 0), 0)
        self.assertEqual(t1.step(1, 1), 1)

        with self.assertRaises(IndexError):
            t1.step(2, 0)
        with self.assertRaises(IndexError):
            t1.step(0, 2)

        t2 = FiniteTransducer(
            num_states=3,
            num_inputs=1,
            step_table=((1,), (2,), (0,)),
        )
        prod = product_transducer(t1, t2)
        self.assertEqual(prod.num_states, 6)
        self.assertEqual(prod.num_inputs, 2)
        # Check transition from composite state (0, 0) -> state 0
        # t1(0, 0) = 1, t2(0, 0) = 1 -> (1, 1) = 1*3 + 1 = 4
        self.assertEqual(prod.step(0, 0), 4)

    def test_bridge_4_multiplicity_to_probability(self) -> None:
        ref_neg = MultiplicityDistribution.from_counts({"a": -1, "b": 2})
        self.assertIsInstance(ref_neg, Refused)
        self.assertEqual(ref_neg.code, RefusalCode.INVALID_INPUT)

        ref_empty = MultiplicityDistribution.from_counts({"a": 0, "b": 0})
        self.assertIsInstance(ref_empty, Refused)
        self.assertEqual(ref_empty.code, RefusalCode.EMPTY_SPACE)

        dist_acc = MultiplicityDistribution.from_counts({"a": 3, "b": 7})
        self.assertIsInstance(dist_acc, Accepted)
        dist = dist_acc.value

        self.assertEqual(dist.probability("a"), Fraction(3, 10))
        self.assertEqual(dist.probability("b"), Fraction(7, 10))
        self.assertEqual(dist.probability("c"), Fraction(0, 10))

        union_acc = dist.disjoint_union_probability(["a", "b"])
        self.assertIsInstance(union_acc, Accepted)
        self.assertEqual(union_acc.value, Fraction(1, 1))

        union_dup = dist.disjoint_union_probability(["a", "a"])
        self.assertIsInstance(union_dup, Refused)
        self.assertEqual(union_dup.code, RefusalCode.NOT_DISJOINT)

    def test_bridge_4_invalid_counts_are_refused(self) -> None:
        for invalid in (True, False, Fraction(1), 1.0, "1", None):
            with self.subTest(value=invalid):
                result = MultiplicityDistribution.from_counts({"a": invalid, "b": 2})
                self.assertIsInstance(result, Refused)
                self.assertEqual(result.code, RefusalCode.INVALID_INPUT)

    def test_bridge_4_freezes_counts_and_validates_direct_construction(self) -> None:
        original = {"a": 3, "b": 7}
        result = MultiplicityDistribution.from_counts(original)
        self.assertIsInstance(result, Accepted)
        original["a"] = 30
        self.assertEqual(result.value.probability("a"), Fraction(3, 10))
        with self.assertRaises(TypeError):
            result.value.counts["a"] = 30
        self.assertEqual(result.value.probability("a"), Fraction(3, 10))
        for counts, total in (({"a": True}, 1), ({"a": -1, "b": 2}, 1), ({"a": 1}, 2), ({"a": 1}, True)):
            with self.subTest(counts=counts, total=total):
                with self.assertRaises(ValueError):
                    MultiplicityDistribution(counts, total)

    def test_bridge_5_reports_to_evaluation(self) -> None:
        self.assertEqual(
            evaluate_report_claim(in_profile=False, evidence_valid=True),
            EvaluationStatus.OUTSIDE_PROFILE,
        )
        self.assertEqual(
            evaluate_report_claim(in_profile=False, evidence_valid=False),
            EvaluationStatus.OUTSIDE_PROFILE,
        )
        self.assertEqual(
            evaluate_report_claim(in_profile=True, evidence_valid=True),
            EvaluationStatus.ACCEPT,
        )
        self.assertEqual(
            evaluate_report_claim(in_profile=True, evidence_valid=False),
            EvaluationStatus.REJECT,
        )

    def test_bridge_5_non_boolean_guards_are_refused(self) -> None:
        for invalid in (0, 1, None, "False", 0.0, 1.0):
            with self.subTest(value=invalid):
                self.assertEqual(evaluate_report_claim(invalid, True), EvaluationStatus.REFUSE)
                self.assertEqual(evaluate_report_claim(True, invalid), EvaluationStatus.REFUSE)
                self.assertEqual(evaluate_report_claim(False, invalid), EvaluationStatus.REFUSE)

    def test_bridge_6_proposals_to_authorization(self) -> None:
        receipt = MathematicalReceipt(
            receipt_id="rec_001",
            claim_id="claim_001",
            verified=True,
        )
        self.assertEqual(receipt.authority_effect, AuthorityEffect.NONE)
        check = check_no_authority_effect(receipt)
        self.assertIsInstance(check, Accepted)
        self.assertEqual(check.value, True)

        receipt_bad = MathematicalReceipt(
            receipt_id="rec_bad",
            claim_id="claim_bad",
            verified=True,
            authority_effect="ExternalAuthorizationToken",
        )
        check_bad = check_no_authority_effect(receipt_bad)
        self.assertIsInstance(check_bad, Refused)
        self.assertEqual(check_bad.code, RefusalCode.CLAIM_STATUS_FIREWALL)

    def test_bridge_7_triangle_parity_cochain(self) -> None:
        # All equal
        d_ab, d_bc, d_ac, parity = compute_triangle_mark_differences(("A", "A", "A"))
        self.assertEqual((d_ab, d_bc, d_ac, parity), (False, False, False, False))

        # Two equal: A = B != C
        d_ab, d_bc, d_ac, parity = compute_triangle_mark_differences(("A", "A", "B"))
        self.assertEqual((d_ab, d_bc, d_ac, parity), (False, True, True, False))

        # Two equal: B = C != A
        d_ab, d_bc, d_ac, parity = compute_triangle_mark_differences(("A", "B", "B"))
        self.assertEqual((d_ab, d_bc, d_ac, parity), (True, False, True, False))

        # Two equal: A = C != B
        d_ab, d_bc, d_ac, parity = compute_triangle_mark_differences(("A", "B", "A"))
        self.assertEqual((d_ab, d_bc, d_ac, parity), (True, True, False, False))

        # Pairwise distinct: parity is 1 (boundary is not 0 for >= 3 marks)
        d_ab, d_bc, d_ac, parity = compute_triangle_mark_differences(("A", "B", "C"))
        self.assertEqual((d_ab, d_bc, d_ac, parity), (True, True, True, True))

    def test_bridge_8_arbitrary_norm_rational_attainment(self) -> None:
        empty_res = find_rational_l1_minimizer([])
        self.assertIsInstance(empty_res, Refused)
        self.assertEqual(empty_res.code, RefusalCode.EMPTY_SPACE)

        pt1 = (Fraction(1, 2), Fraction(-3, 4))
        pt2 = (Fraction(0), Fraction(1, 4))
        pt3 = (Fraction(1), Fraction(1))

        self.assertEqual(rational_l1_norm(pt1), Fraction(5, 4))
        self.assertEqual(rational_l1_norm(pt2), Fraction(1, 4))
        self.assertEqual(rational_l1_norm(pt3), Fraction(2, 1))

        res = find_rational_l1_minimizer([pt1, pt2, pt3])
        self.assertIsInstance(res, Accepted)
        min_pt, min_val = res.value
        self.assertEqual(min_pt, pt2)
        self.assertEqual(min_val, Fraction(1, 4))

    def test_bridge_8_refuses_approximate_or_untyped_candidates(self) -> None:
        for invalid in (0.0, 1.0, True, False, "1", None):
            with self.subTest(value=invalid):
                with self.assertRaises(TypeError):
                    rational_l1_norm((invalid,))
                result = find_rational_l1_minimizer(((Fraction(0),), (invalid,)))
                self.assertIsInstance(result, Refused)
                self.assertEqual(result.code, RefusalCode.INVALID_INPUT)
        self.assertEqual(rational_l1_norm((3, -4)), Fraction(7))
        self.assertIs(type(rational_l1_norm((3, -4))), Fraction)
        result = find_rational_l1_minimizer(((2, 3), (1, 1)))
        self.assertIsInstance(result, Accepted)
        self.assertEqual(result.value[1], Fraction(2))

    def test_bridge_9_flat_locus_curvature(self) -> None:
        # Nilpotent matrix: d = [[0, 1], [0, 0]] -> d^2 = [[0, 0], [0, 0]]
        nilpotent = (
            (Fraction(0), Fraction(1)),
            (Fraction(0), Fraction(0)),
        )
        res = verify_flat_locus_curvature(nilpotent, ExactField.RATIONAL)
        self.assertIsInstance(res, Accepted)
        self.assertEqual(res.value, True)

        # Non-nilpotent: identity matrix -> d^2 = identity != 0
        non_nilpotent = (
            (Fraction(1), Fraction(0)),
            (Fraction(0), Fraction(1)),
        )
        bad_res = verify_flat_locus_curvature(non_nilpotent, ExactField.RATIONAL)
        self.assertIsInstance(bad_res, Refused)
        self.assertEqual(bad_res.code, RefusalCode.NOT_A_DIFFERENTIAL)

    def test_bridge_10_cover_marginals_frustrated_cycle(self) -> None:
        # Odd cycle (triangle, pentagon) cannot be 2-colored
        res3 = solve_frustrated_spin_cycle(3)
        self.assertIsInstance(res3, Refused)
        self.assertEqual(res3.code, RefusalCode.INFEASIBLE)

        res5 = solve_frustrated_spin_cycle(5)
        self.assertIsInstance(res5, Refused)
        self.assertEqual(res5.code, RefusalCode.INFEASIBLE)

        # Even cycle (square) can be 2-colored
        res4 = solve_frustrated_spin_cycle(4)
        self.assertIsInstance(res4, Accepted)
        self.assertEqual(
            res4.value,
            {"s_0": False, "s_1": True, "s_2": False, "s_3": True},
        )

    def test_bridge_10_refuses_empty_or_invalid_cycle_lengths(self) -> None:
        for invalid in (0, -1, -2, True, False, 1.0, "4", None):
            with self.subTest(value=invalid):
                result = solve_frustrated_spin_cycle(invalid)
                self.assertIsInstance(result, Refused)
                self.assertEqual(result.code, RefusalCode.INVALID_INPUT)
        self.assertIsInstance(solve_frustrated_spin_cycle(1), Refused)
        two_cycle = solve_frustrated_spin_cycle(2)
        self.assertIsInstance(two_cycle, Accepted)
        self.assertEqual(two_cycle.value, {"s_0": False, "s_1": True})

    def test_bridge_11_deterministic_retention(self) -> None:
        det_transitions = [
            ("s0", "a", "s1"),
            ("s0", "b", "s0"),
            ("s1", "a", "s0"),
            ("s1", "b", "s1"),
        ]
        res = verify_deterministic_retention(det_transitions)
        self.assertIsInstance(res, Accepted)
        self.assertEqual(res.value, True)

        branching_transitions = [
            ("s0", "a", "s1"),
            ("s0", "a", "s2"),  # conflicting destination
        ]
        res_branch = verify_deterministic_retention(branching_transitions)
        self.assertIsInstance(res_branch, Refused)
        self.assertEqual(res_branch.code, RefusalCode.NOT_CLOSED)


if __name__ == "__main__":
    unittest.main()
