"""Targeted fixed witnesses for reconstruction classification."""
from fractions import Fraction

from witnessed_difference.reconstruction_classification import (
    composition_discriminator_witness,
    signed_readout_countermodel,
)


def test_signed_full_effect_no_go_and_coarse_effect_escape() -> None:
    witness = signed_readout_countermodel()
    assert witness["total"] == 1
    assert witness["negative_indicator"] == -1
    assert witness["all_reports_classical"] is False
    assert witness["coarse_report_probability"] == 1
    assert witness["negative_jordan_mass"] == 1


def test_imported_quantum_pr_discriminator_is_exact_and_nonclassical() -> None:
    witness = composition_discriminator_witness()
    assert witness["direction_norm_squared"] == 1
    assert witness["quantum_chsh"] == Fraction(14, 5)
    assert witness["quantum_squared"] == Fraction(196, 25)
    assert witness["quantum_bound_slack"] == Fraction(4, 25)
    assert witness["classical_bound_violated"] is True
    assert witness["pr_squared"] == 16
    assert witness["pr_excluded"] is True
