"""End-to-end functional fixtures through the built native host.

Run directly with unittest after building omega_symbol_game. A missing or failing
host is a test failure; this suite has no fallback or skip path.
"""

from __future__ import annotations

import importlib.util
import sys
import unittest
from pathlib import Path

from sympy import Matrix, Rational

CODE = Path(__file__).resolve().parents[2]
for directory in (CODE.parents[4], CODE):
    if str(directory) not in sys.path:
        sys.path.insert(0, str(directory))

from omega_engine_operating_system.adapters.rust_host.majorana_math import (  # noqa: E402
    NativeMathRefusal,
    call_native,
)


def load(name: str, filename: str):
    spec = importlib.util.spec_from_file_location(name, CODE / filename)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load {filename}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


transfer = load("paper_native_transfer_fixture", "transfer.py")
family = load("paper_native_family_fixture", "family_bound.py")


class NativeFunctionalFixtures(unittest.TestCase):
    def test_exact_projected_pair_replays_and_retains_native_evidence(self) -> None:
        report = transfer.linear_projection_transfer_certificate(
            [1, 2], [1, 0], Matrix.diag(1, 0), "1/2"
        )
        self.assertTrue(report.accepted)
        self.assertTrue(report.verify())
        self.assertEqual(report.source_distance, Rational(2))
        self.assertEqual(report.projection_distance, Rational(0))
        self.assertEqual(report.rho_defect, Rational(2))
        self.assertEqual(report.transfer_lower_bound, Rational(-3))
        self.assertIs(report.native_outcome["success"], True)
        self.assertEqual(report.native_outcome["result"]["rho_defect"], "2")

    def test_failed_pairwise_premise_retains_no_transfer_claim(self) -> None:
        report = transfer.linear_projection_transfer_certificate(
            [1, 2], [1, 0], Matrix.eye(2), "1/2"
        )
        self.assertFalse(report.accepted)
        self.assertTrue(report.verify())
        self.assertEqual(report.refusal, "pairwise_lipschitz_premise_failed")
        self.assertIsNone(report.transfer_holds)
        self.assertIsNone(report.defect_difference_bound_holds)

    def test_empty_vectors_preserve_zero_dimension_without_fabricated_coordinates(self) -> None:
        for shape in ((0, 0), (0, 1), (1, 0)):
            report = transfer.reverse_triangle_certificate(Matrix.zeros(*shape), [], [], [], 0)
            self.assertTrue(report.accepted and report.verify())
            self.assertEqual(report.rho_defect, Rational(0))
            self.assertEqual(report.native_outcome["result"]["states"], [[], [], [], []])
        for rows in (2, 3):
            with self.assertRaises(ValueError):
                transfer.reverse_triangle_certificate(Matrix.zeros(rows, 0), [], [], [], 0)

    def test_projection_must_be_idempotent(self) -> None:
        with self.assertRaisesRegex(ValueError, "not idempotent"):
            transfer.linear_projection_transfer_certificate(
                [1, 2], [1, 0], Matrix([[1, 1], [0, 1]]), 1
            )

    def test_supplied_family_reproduces_exact_floors(self) -> None:
        members = (
            family.FiniteFamilyMember("N4", 4, 4, 2, [3, 4]),
            family.FiniteFamilyMember("N6", 6, 9, "3/2", [3, 3, 4, 4, 5, 5]),
        )
        self.assertEqual(members[1].active_edge_density, Rational(2, 3))
        self.assertEqual(members[1].edge_site_density, Rational(3, 2))
        self.assertEqual(members[1].active_edge_count, 6)
        report = family.certify_uniform_family(
            members, family.UniformFamilyPremises(2, "1/2", 3, 1), "1/64"
        )
        self.assertTrue(report.accepted and report.verify())
        self.assertEqual(report.uniform_window_upper, Rational(1, 64))
        self.assertEqual(report.local_edge_polynomial, Rational(3, 128))
        self.assertEqual(report.edge_density_floor, Rational(3, 256))
        self.assertEqual(report.site_density_floor, Rational(3, 256))
        self.assertEqual(report.member_bounds[1].site_density_lower_bound, Rational(3, 128))
        self.assertIs(report.native_outcome["success"], True)

    def test_family_refusal_retains_replayable_premises_without_bounds(self) -> None:
        member = family.FiniteFamilyMember("N4", 4, 4, 2, [1, 4])
        report = family.certify_uniform_family(
            (member,), family.UniformFamilyPremises(2, "1/2", 3, 1), "1/64"
        )
        self.assertFalse(report.accepted)
        self.assertTrue(report.verify())
        self.assertIsNone(report.local_edge_polynomial)
        self.assertEqual(report.member_bounds, ())
        self.assertIn("active_rate_failed", {reason.code for reason in report.refusals})

    def test_report_mutations_fail_native_replay(self) -> None:
        report = transfer.reverse_triangle_certificate([1], [0], [0], [0], 1)
        report.rho_defect = Rational(4)
        self.assertFalse(report.verify())
        member = family.FiniteFamilyMember("N4", 4, 4, 2, [3, 4])
        bound = family.certify_uniform_family(
            (member,), family.UniformFamilyPremises(2, "1/2", 3, 1), "1/64"
        )
        bound.member_bounds = ()
        self.assertFalse(bound.verify())

    def test_wire_refuses_noncanonical_scalars_and_unknown_fields(self) -> None:
        for scalar in (True, 1, 0.5, "2/4", "1/1", "1/0"):
            with self.assertRaises(NativeMathRefusal):
                call_native(
                    "functional_projection_transfer",
                    {
                        "rho": [scalar],
                        "sigma": ["0"],
                        "projected_rho": ["0"],
                        "projected_sigma": ["0"],
                        "lipschitz_constant": "1",
                    },
                )
        with self.assertRaises(NativeMathRefusal):
            call_native(
                "functional_family_member",
                {
                    "system_id": "N4",
                    "site_count": 4,
                    "edge_count": 4,
                    "local_interaction_norm": "2",
                    "active_edge_rates": ["3", "4"],
                    "unexpected": 1,
                },
            )


if __name__ == "__main__":
    unittest.main()
