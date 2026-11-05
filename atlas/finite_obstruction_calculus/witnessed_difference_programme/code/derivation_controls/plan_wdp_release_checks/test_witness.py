import importlib.util
from pathlib import Path

import pytest


def _load():
    path = Path(__file__).resolve().parent / "witness.py"
    spec = importlib.util.spec_from_file_location("plan_wdp_release_checks_witness", path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_release_checks_and_disposition() -> None:
    module = _load()
    result = module.witness()
    assert result == {
        "affected_checks_passed": True,
        "silent_baseline_refresh": False,
        "dec_wdp_repin_separate": True,
        "publication_clearance_claimed": False,
        "relative_directory_href_count": 0,
        "pdf_nonempty": True,
        "release_verification_status": "PASS",
    }


def test_silent_baseline_refresh_and_failed_checks_refuse() -> None:
    module = _load()
    with pytest.raises(ValueError, match="silent trusted-baseline refresh"):
        module.evaluate_ci_policy_disposition(
            affected_checks_passed=True,
            silent_baseline_refresh=True,
            repin_owner_approved=False,
            unresolved_policy_items=("DEC-WDP-REPIN",),
        )
    with pytest.raises(ValueError, match="affected local checks"):
        module.evaluate_ci_policy_disposition(
            affected_checks_passed=False,
            silent_baseline_refresh=False,
            repin_owner_approved=False,
            unresolved_policy_items=("DEC-WDP-REPIN",),
        )
