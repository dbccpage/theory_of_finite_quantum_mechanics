"""Fixed exact phase/readout witnesses; AuthorityEffect: None.

General phase arithmetic belongs to Rust rational_turns; these are finite paper
receipts, not a replacement number-theory implementation.
"""
from fractions import Fraction


def rational_phase_and_readout_witness() -> dict[str, object]:
    edge_phases = (Fraction(1, 3), Fraction(1, 4), Fraction(1, 6))
    potential = (Fraction(1, 5), Fraction(2, 7), Fraction(-1, 8))
    transformed = (
        edge_phases[0] + potential[1] - potential[0],
        edge_phases[1] + potential[2] - potential[1],
        edge_phases[2] + potential[2] - potential[0],
    )
    loop = (edge_phases[0] + edge_phases[1] - edge_phases[2]) % 1
    transformed_loop = (transformed[0] + transformed[1] - transformed[2]) % 1
    return {
        "loop": loop,
        "transformed_loop": transformed_loop,
        "endpoint_shift": potential[2] - potential[0],
        "path_shift": transformed[0] + transformed[1] - edge_phases[0] - edge_phases[1],
        "chosen_fifth_root_of_third_turn": Fraction(1, 15),
        "quadratic_probabilities": (Fraction(1, 5), Fraction(4, 5)),
        "quartic_probabilities": (Fraction(1, 17), Fraction(16, 17)),
    }
