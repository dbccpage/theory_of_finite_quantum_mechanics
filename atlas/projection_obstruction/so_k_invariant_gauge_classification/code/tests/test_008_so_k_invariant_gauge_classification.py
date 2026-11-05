"""
End-to-end integration and certification tests for so_k_invariant_gauge_classification.
Paper: GS-002 (so_k_invariant_gauge_classification)
"""

import pytest

from mod_008_so_k_invariant_gauge_classification_core import PaperEvaluator


def test_package_evaluator_passes_comprehensively() -> None:
    evaluator = PaperEvaluator()
    res = evaluator.evaluate()

    assert res["paper_id"] == "so_k_invariant_gauge_classification"
    assert res["status"] == "EVALUATED_PASS"

    # Verify SO(k) invariance
    assert res["sok_invariance"] is True

    # Verify quotient obstruction values on triangle
    assert res["phi_21_mixed"] == pytest.approx(1.41421356, abs=1e-4)
    assert res["phi_11_coordinate"] == pytest.approx(2.0, abs=1e-4)

    # Verify strong duality gap
    assert res["duality_gap"] == pytest.approx(0.0, abs=1e-4)

    # Verify triangle separation ratio
    assert res["triangle_ratio"] == pytest.approx(1.41421356, abs=1e-4)

    # Verify closure bound and adversarial resilience
    assert res["closure_bound_satisfied"] is True
    assert res["adversarial_resilience"] is True
