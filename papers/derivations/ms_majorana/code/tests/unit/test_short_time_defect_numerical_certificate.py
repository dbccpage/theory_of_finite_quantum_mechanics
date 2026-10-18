"""
Unit tests for SecondDerivativeBoundCertificate.
"""

import sys
from pathlib import Path
import pytest

_code_dir = Path(__file__).resolve().parents[2] / "code"
if str(_code_dir) not in sys.path:
    sys.path.insert(0, str(_code_dir))

from omega_engine.crates.quantum_physics.short_time_defect_numerical_certificate import SecondDerivativeBoundCertificate


def test_second_derivative_certificate_pass():
    cert = SecondDerivativeBoundCertificate(g=0.5)
    res = cert.evaluate_assembly(
        measured_one_site_first_a=1.0,
        measured_one_site_first_b=1.0,
        measured_one_site_second_a=2.0,
        measured_one_site_second_b=2.0,
        measured_two_site_second=6.0,
    )
    assert not res["second_deriv_bound_violated"]
    assert res["assembled_M"] == 12.0
    assert res["M_used"] == 12.0
    assert res["taylor_c2_used"] == 6.0
    assert res["second_deriv_source"] == "product_rule_assembly_under_reduced_state_hyps"


def test_second_derivative_certificate_kill_hook():
    cert = SecondDerivativeBoundCertificate(g=0.5)
    res = cert.evaluate_assembly(
        measured_one_site_first_a=1.5,
        measured_one_site_first_b=1.0,
        measured_one_site_second_a=2.0,
        measured_one_site_second_b=2.0,
        measured_two_site_second=6.0,
    )
    assert res["second_deriv_bound_violated"]
    assert res["assembled_M"] > 12.0
    assert res["M_used"] == res["assembled_M"]


