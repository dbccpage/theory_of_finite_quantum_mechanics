"""Exact paper fixtures for the paid phase/readout bridge."""
from fractions import Fraction

from witnessed_difference.rational_phase_witness import rational_phase_and_readout_witness


def test_rational_gauge_telescopes_without_selecting_normalized_power_readout() -> None:
    witness = rational_phase_and_readout_witness()
    assert witness["loop"] == Fraction(5, 12)
    assert witness["transformed_loop"] == witness["loop"]
    assert witness["path_shift"] == witness["endpoint_shift"]
    assert 5 * witness["chosen_fifth_root_of_third_turn"] == Fraction(1, 3)
    assert sum(witness["quadratic_probabilities"]) == 1
    assert sum(witness["quartic_probabilities"]) == 1
    assert witness["quadratic_probabilities"] != witness["quartic_probabilities"]
