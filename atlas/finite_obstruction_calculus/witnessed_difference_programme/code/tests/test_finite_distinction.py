"""Finite witnesses for the WD2 manuscript distinction carriers.

# Executable finite evidence; AuthorityEffect: None.
"""

from witnessed_difference.finite_distinction import (
    FiniteAutomaton,
    MooreMachine,
    distinction_relation,
    factored_report_profile,
    minimal_quotient_profile,
    no_escape_profile,
    sharp_chain,
    sharp_profile,
    word_kernel_agrees,
)


def test_sharp_chain_class_counts() -> None:
    empty = sharp_profile(0)
    assert empty["N"] == 0
    assert empty["b0"] == 0
    assert empty["stable_classes"] == 0
    assert empty["class_counts"] == []
    assert empty["word_kernel"] is True

    one = sharp_profile(1)
    assert one["N"] == 0
    assert one["b0"] == 1
    assert one["class_counts"] == [1]

    pair = sharp_profile(2)
    assert pair["b0"] == 2
    assert pair["N"] == 0
    assert pair["class_counts"] == [2, 2]
    assert pair["bound"] == 0

    five = sharp_profile(5)
    assert five["b0"] == 2
    assert five["N"] == 3
    assert five["bound"] == 3
    assert five["stable_classes"] == 5
    assert five["class_counts"] == [2, 3, 4, 5, 5]
    assert five["word_kernel"] is True


def test_update_stable_pair_has_no_separating_word() -> None:
    profile = no_escape_profile()
    assert profile["N"] == 0
    assert profile["b0"] == 1
    assert profile["stable_classes"] == 1
    assert profile["separating"] is None
    assert profile["word_kernel"] is True


def test_factored_reports_preserve_the_horizon_and_the_escape_length_is_two() -> None:
    profile = factored_report_profile()
    assert profile["reports_preserved"] is True
    assert profile["escape_length"] == 2


def test_minimal_deterministic_quotient_factorization() -> None:
    profile = minimal_quotient_profile()
    assert profile["N"] == 0
    assert profile["r_inf_classes"] == 2
    assert profile["intermediate_classes"] == 3
    assert profile["comparison_well_defined"] is True
    assert profile["comparison_surjective"] is True
    assert profile["cardinality_lower_bound"] is True


def test_interface_aliases_and_properties() -> None:
    assert FiniteAutomaton is MooreMachine
    m = sharp_chain(3)
    sigs = distinction_relation(m, 2)
    assert len(sigs) == 3
    assert word_kernel_agrees(m, 2) is True


def test_batch6_meron_toric_and_3cube_witnesses() -> None:
    # 1. Meron 3-rung plaquette syndrome-to-repair adapter
    adapter = {
        (0, 0): (0, 0, 0),
        (1, 0): (1, 0, 0),
        (0, 1): (0, 0, 1),
        (1, 1): (0, 1, 0),
    }
    for b0 in (0, 1):
        for b1 in (0, 1):
            for b2 in (0, 1):
                syn = (b0 ^ b1, b1 ^ b2)
                rep = adapter[syn]
                assert sum(rep) <= 1
                cleared = (b0 ^ rep[0], b1 ^ rep[1], b2 ^ rep[2])
                assert (cleared[0] ^ cleared[1], cleared[1] ^ cleared[2]) == (0, 0)
                if b0 + b1 + b2 <= 1:
                    assert rep == (b0, b1, b2)

    # 2. Toric 4-cycle star syndrome: tree-supported errors are injective, full cycle is in kernel
    def star_syndrome(e: tuple[int, int, int, int]) -> tuple[int, int, int, int]:
        return (e[0] ^ e[3], e[0] ^ e[1], e[1] ^ e[2], e[2] ^ e[3])

    tree_syndromes = {
        star_syndrome((e0, e1, e2, 0))
        for e0 in (0, 1)
        for e1 in (0, 1)
        for e2 in (0, 1)
    }
    assert len(tree_syndromes) == 8
    assert star_syndrome((1, 1, 1, 1)) == (0, 0, 0, 0)

