"""
Numerical certificate and kill-test companion for PO-000 second-derivative bound.

AuthorityEffect: None
"""

from typing import Dict, Any
import numpy as np


class SecondDerivativeBoundCertificate:
    """
    Finite-instance numerical kill-test companion for Appendix B second-derivative bound.
    """

    def __init__(self, g: float):
        self.g = float(g)
        self.paper_one_site_first = 2.0 * self.g
        self.paper_one_site_second = 8.0 * (self.g ** 2)
        self.paper_two_site_second = 24.0 * (self.g ** 2)
        self.paper_M = 48.0 * (self.g ** 2)

    def evaluate_assembly(
        self,
        measured_one_site_first_a: float,
        measured_one_site_first_b: float,
        measured_one_site_second_a: float,
        measured_one_site_second_b: float,
        measured_two_site_second: float,
        atol: float = 1e-12,
    ) -> Dict[str, Any]:
        """
        Check five reduced-state derivative bounds and assemble M_used.
        """
        v_1a = measured_one_site_first_a > self.paper_one_site_first + atol
        v_1b = measured_one_site_first_b > self.paper_one_site_first + atol
        v_2a = measured_one_site_second_a > self.paper_one_site_second + atol
        v_2b = measured_one_site_second_b > self.paper_one_site_second + atol
        v_2ab = measured_two_site_second > self.paper_two_site_second + atol

        violated = v_1a or v_1b or v_2a or v_2b or v_2ab

        assembled_M = (
            measured_two_site_second
            + measured_one_site_second_a
            + 2.0 * measured_one_site_first_a * measured_one_site_first_b
            + measured_one_site_second_b
        )

        M_used = max(assembled_M, self.paper_M) if violated else self.paper_M

        return {
            "second_deriv_source": "product_rule_assembly_under_reduced_state_hyps",
            "g": self.g,
            "assumed_bounds": {
                "one_site_first_a": self.paper_one_site_first,
                "one_site_first_b": self.paper_one_site_first,
                "one_site_second_a": self.paper_one_site_second,
                "one_site_second_b": self.paper_one_site_second,
                "two_site_second": self.paper_two_site_second,
            },
            "measured_bounds": {
                "one_site_first_a": float(measured_one_site_first_a),
                "one_site_first_b": float(measured_one_site_first_b),
                "one_site_second_a": float(measured_one_site_second_a),
                "one_site_second_b": float(measured_one_site_second_b),
                "two_site_second": float(measured_two_site_second),
            },
            "second_deriv_bound_violated": violated,
            "assembled_M": float(assembled_M),
            "M_used": float(M_used),
            "taylor_c2_used": float(M_used / 2.0),
            "authority_effect": "None",
        }

