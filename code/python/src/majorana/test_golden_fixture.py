"""
test_golden_fixture.py
Shared PY ↔ RS Density Matrix Golden Receipt Test.
AuthorityEffect: None.
"""

import json
from omega_engine.crates.operator.constructor.ctor_qm_density import (
    build_state_feature_matrix,
    build_density_matrix_from_matrix,
)
from omega_engine.crates.observable.obsv_qm_density import emit_observables_receipt


def test_golden_density_matrix_receipt():
    samples = [
        [0.12, 0.45, 0.88, 0.34],
        [0.25, 0.60, 0.70, 0.15],
        [0.80, 0.10, 0.40, 0.95],
    ]
    matrix_f = build_state_feature_matrix(samples, num_bins=4)
    rho = build_density_matrix_from_matrix(matrix_f)
    receipt = emit_observables_receipt(rho)

    assert receipt["dimension"] == 4
    assert abs(receipt["trace"] - 1.0) <= 1e-6
    assert receipt["purity"] >= 0.25
    assert receipt["authority_effect"] == "None"

    receipt_str = json.dumps(receipt)
    assert '"dimension": 4' in receipt_str


