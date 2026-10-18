"""The R7 diagnostic must refuse a Stengle certificate it did not compute."""

import importlib.util
from pathlib import Path

_PATH = Path(__file__).with_name("solve_r7_55gen_positivstellensatz.py")
_SPEC = importlib.util.spec_from_file_location("solve_r7_55gen_positivstellensatz", _PATH)
assert _SPEC is not None and _SPEC.loader is not None
_MODULE = importlib.util.module_from_spec(_SPEC)
_SPEC.loader.exec_module(_MODULE)
diagnose_r7_karlsson_boundary = _MODULE.diagnose_r7_karlsson_boundary


def test_r7_refuses_uncomputed_identity() -> None:
    receipt = diagnose_r7_karlsson_boundary()
    assert receipt["status"] == "NOT_A_CERTIFICATE"
    assert receipt["exact_identity_verified"] is False
    assert receipt["identity_evaluated"] is False
    assert receipt["variety_empty_on_exterior"] is False
    assert receipt["sample"]["on_ideal_i55"] is False
    assert receipt["sample"]["nonzero_residuals"]["unimodular"] == 4
    assert receipt["sample"]["g_sep"] == "-1/100"
    assert receipt["perturbed_sample"]["separation_positive"] is True
