"""Tier 1 exact coverage: Born purity, dephasing, and stabilizer syndromes."""
from fractions import Fraction

from src.qm.campaigns.born_normalization import exact_born_purity
from src.qm.campaigns.cptp_channel import exact_dephasing_defect
from src.qm.campaigns.mermin_peres import verify_mermin_peres_parity
from src.qm.campaigns.stabilizer_codes import (
    build_steane_seven_qubit_code,
    build_three_qubit_bitflip_code,
)


def test_tier1_exact_born_purity():
    purity = exact_born_purity((Fraction(1, 4), Fraction(3, 4)))
    assert purity == Fraction(5, 8)


def test_tier1_exact_dephasing_defect():
    assert exact_dephasing_defect() == Fraction(0)
    assert exact_dephasing_defect(Fraction(1, 2), Fraction(1, 2)) == Fraction(1)


def test_tier1_bitflip_syndromes_are_exact():
    report = build_three_qubit_bitflip_code()
    assert report["syndromes"]["X0"] == (-1, 1)
    assert report["syndromes"]["X2"] == (1, -1)
    assert report["all_syndromes_distinct"] is True


def test_tier1_steane_syndrome_count():
    report = build_steane_seven_qubit_code()
    assert report["unique_error_syndromes_count"] == 21
    assert report["all_single_qubit_errors_correctable"] is True


def test_tier1_mermin_peres_exact_parity():
    assert verify_mermin_peres_parity() is True
