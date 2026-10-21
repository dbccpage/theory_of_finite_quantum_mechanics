"""Adapter contracts; numerical correctness is exercised by native Rust tests.

These mocked replies only establish delegation, input refusal, outcome custody,
and tamper-sensitive replay. They are not mathematical parity evidence.
"""

from __future__ import annotations

import importlib.util
import sys
import unittest
from pathlib import Path
from unittest.mock import patch

from sympy import Float, Matrix, Rational, sqrt

CODE = Path(__file__).resolve().parents[2]
for directory in (CODE.parents[4], CODE):
    if str(directory) not in sys.path:
        sys.path.insert(0, str(directory))

from omega_engine_operating_system.adapters.rust_host.majorana_math import (
    NativeMathRefusal,
    NativeMathReply,
)


def load(name: str, filename: str):
    spec = importlib.util.spec_from_file_location(name, CODE / filename)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load {filename}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


transfer = load("paper_native_transfer_contract", "transfer.py")
family = load("paper_native_family_contract", "family_bound.py")


def reply(result: dict) -> NativeMathReply:
    return NativeMathReply({"success": True, "result": result, "evidence": "test-boundary-only"})


TRANSFER = {
    "accepted": True,
    "lipschitz_constant": "1/2",
    "source_distance": "2",
    "projection_distance": "0",
    "rho_defect": "2",
    "sigma_defect": "0",
    "defect_difference": "2",
    "transfer_lower_bound": "-3",
    "pairwise_lipschitz_premise": True,
    "reverse_triangle_holds": True,
    "defect_difference_bound_holds": True,
    "transfer_holds": True,
    "refusal": None,
}
MEMBER = {
    "active_edge_count": 2,
    "active_edge_density": "1/2",
    "edge_site_density": "1",
}
FAMILY = {
    "accepted": True,
    "time": "1/64",
    "uniform_window_upper": "1/64",
    "local_edge_polynomial": "3/128",
    "edge_density_floor": "3/256",
    "site_density_floor": "3/256",
    "half_slope_site_floor": "3/256",
    "member_bounds": [
        {
            "system_id": "N4",
            "active_edge_density": "1/2",
            "edge_site_density": "1",
            "edge_density_lower_bound": "3/256",
            "site_density_lower_bound": "3/256",
        }
    ],
    "refusals": [],
}


class NativeFunctionalDelegation(unittest.TestCase):
    def test_transfer_replays_original_request_and_retains_outcome(self) -> None:
        native = reply(TRANSFER)
        with patch.object(transfer, "call_native", return_value=native) as called:
            certificate = transfer.reverse_triangle_certificate(
                [1, 2], [1, 0], [1, 0], [1, 0], "1/2"
            )
            self.assertEqual(certificate.rho_defect, Rational(2))
            self.assertIs(certificate.native_outcome, native.outcome)
            self.assertTrue(certificate.verify())
            self.assertEqual(called.call_args.args[0], "functional_projection_transfer")
            self.assertEqual(called.call_args.args[1]["rho"], ["1", "2"])
            certificate.transfer_lower_bound = Rational(9)
            self.assertFalse(certificate.verify())
            certificate.transfer_lower_bound = Rational(-3)
            certificate.accepted = 1
            self.assertFalse(certificate.verify())

    def test_projection_checks_and_products_cross_the_native_seam(self) -> None:
        def invoke(action: str, payload: dict) -> NativeMathReply:
            if action == "functional_projection_transfer":
                return reply(TRANSFER)
            if payload["operation"] == "is_idempotent":
                return reply({"is_idempotent": True})
            return reply({"vector": ["1", "0"]})

        with patch.object(transfer, "call_native", side_effect=invoke) as called:
            certificate = transfer.linear_projection_transfer_certificate(
                [1, 2], [1, 0], Matrix.diag(1, 0), "1/2"
            )
            self.assertTrue(certificate.accepted)
            self.assertEqual(
                [call.args[0] for call in called.call_args_list],
                [
                    "math_rational_matrix",
                    "math_rational_matrix",
                    "math_rational_matrix",
                    "functional_projection_transfer",
                ],
            )

    def test_exact_input_contract_refuses_before_native_call(self) -> None:
        with patch.object(transfer, "call_native") as called:
            for bad in (True, 0.5, Float("0.5"), sqrt(2)):
                with self.assertRaises(TypeError):
                    transfer.reverse_triangle_certificate([bad], [0], [0], [0], 1)
            for rows in (2, 3, 8):
                with self.assertRaises(ValueError):
                    transfer.reverse_triangle_certificate(Matrix.zeros(rows, 0), [], [], [], 1)
            called.assert_not_called()

    def test_all_three_canonical_empty_vectors_cross_as_empty_arrays(self) -> None:
        with patch.object(transfer, "call_native", return_value=reply(TRANSFER)) as called:
            for shape in ((0, 0), (0, 1), (1, 0)):
                transfer.reverse_triangle_certificate(Matrix.zeros(*shape), [], [], [], 1)
                self.assertEqual(called.call_args.args[1]["rho"], [])

    def test_native_failure_propagates_with_no_python_calculation(self) -> None:
        error = NativeMathRefusal("TEST_NATIVE_REFUSAL", "unavailable", outcome={"failure": "test"})
        with patch.object(transfer, "call_native", side_effect=error):
            with self.assertRaises(NativeMathRefusal) as caught:
                transfer.reverse_triangle_certificate([1], [0], [0], [0], 1)
            self.assertIs(caught.exception, error)

    def test_family_objects_and_certificate_delegate_and_replay(self) -> None:
        def invoke(action: str, payload: dict) -> NativeMathReply:
            return reply(MEMBER if action == "functional_family_member" else FAMILY)

        with patch.object(family, "call_native", side_effect=invoke) as called:
            member = family.FiniteFamilyMember("N4", 4, 4, 2, [3, 4])
            self.assertEqual(member.active_edge_density, Rational(1, 2))
            self.assertEqual(member.edge_site_density, Rational(1))
            certificate = family.certify_uniform_family(
                (member,), family.UniformFamilyPremises(2, "1/2", 3, 1), "1/64"
            )
            self.assertTrue(certificate.verify())
            self.assertEqual(
                called.call_args.args[1]["members"][0]["active_edge_rates"], ["3", "4"]
            )
            self.assertEqual(certificate.native_outcome["evidence"], "test-boundary-only")
            certificate.member_bounds = ()
            self.assertFalse(certificate.verify())

    def test_family_count_and_scalar_guards_are_typed(self) -> None:
        with patch.object(family, "call_native") as called:
            for count in (True, 0.5, 0, -1):
                with self.assertRaises(ValueError):
                    family.FiniteFamilyMember("x", count, 4, 1, [])
            with self.assertRaises(TypeError):
                family.UniformFamilyPremises(0.5, 1, 1, 1)
            called.assert_not_called()


if __name__ == "__main__":
    unittest.main()
