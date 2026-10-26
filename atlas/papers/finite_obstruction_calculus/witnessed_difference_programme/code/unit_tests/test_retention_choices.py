from itertools import product

import pytest
from witnessed_difference.retention_choices import (
    RetentionSignature,
    TypedRetention,
    greatest_forward_relation,
    initial_recognition_is_forward_compatible,
    is_forward_compatible,
    raw_report_descends,
    relation_is_equivalence,
)


def test_complete_typed_cartesian_extension_space_and_greatest_relation():
    signature = RetentionSignature(2, 1, 2)
    counts = signature.counts()
    packets = {signature.from_codes(u, r, c) for u, r, c in product(range(4), range(4), range(16))}
    assert len(packets) == counts["packets"] == 256
    assert len({p.updates for p in packets}) == counts["updates"] == 4
    assert len({p.readouts for p in packets}) == counts["readouts"] == 4
    assert len({p.comparison for p in packets}) == counts["comparisons"] == 16
    for packet in packets:
        receipt = greatest_forward_relation(packet)
        assert is_forward_compatible(packet, receipt.relation)
        assert len(receipt.relations) <= 5
        union = frozenset()
        for bits in range(16):
            candidate = frozenset(
                (x, y) for x in range(2) for y in range(2) if bits & (1 << (2 * x + y))
            )
            if is_forward_compatible(packet, candidate):
                assert candidate <= receipt.relation
                union |= candidate
        assert union == receipt.relation


def test_named_regularities_have_exact_counts():
    signature = RetentionSignature(2, 1, 3)
    packets = [signature.from_codes(0, r, c) for r in range(9) for c in range(512)]
    counts = signature.counts()
    assert len({p.comparison for p in packets if p.is_tolerance()}) == counts["tolerances"] == 8
    assert len({p.comparison for p in packets if relation_is_equivalence(3, p.comparison)}) == 5
    assert (
        len({p.readouts for p in packets if len(set(p.readouts)) == 2})
        == counts["injective_readouts"]
        == 6
    )
    assert counts["surjective_readouts"] == 0
    assert RetentionSignature(3, 2, 2).counts()["surjective_readouts"] == 6
    assert RetentionSignature(3, 2, 2).counts()["bijective_updates"] == 36


def test_nontransitive_tolerance_and_accidentally_equivalent_state_relation():
    comparison = frozenset({(0, 0), (1, 1), (2, 2), (0, 1), (1, 0), (1, 2), (2, 1)})
    keep = TypedRetention(RetentionSignature(3, 1, 3), ((0,), (1,), (2,)), (0, 1, 2), comparison)
    assert keep.is_tolerance()
    relation = greatest_forward_relation(keep).relation
    assert relation == comparison
    assert not relation_is_equivalence(3, relation)
    refined = TypedRetention(keep.signature, ((0,), (2,), (2,)), keep.readouts, comparison)
    refined_relation = greatest_forward_relation(refined).relation
    assert relation_is_equivalence(3, refined_relation)
    assert not raw_report_descends(refined, refined_relation)


def test_equivalence_is_not_literal_readout_descent():
    packet = TypedRetention(
        RetentionSignature(2, 1, 2), ((0,), (1,)), (0, 1), frozenset(product(range(2), repeat=2))
    )
    relation = greatest_forward_relation(packet).relation
    assert relation_is_equivalence(2, relation)
    assert not raw_report_descends(packet, relation)


def test_coupling_comes_from_named_regularity_not_typing():
    equality = frozenset({(0, 0), (1, 1)})
    keep = TypedRetention(RetentionSignature(3, 1, 2), ((0,), (1,), (2,)), (0, 0, 1), equality)
    breaking = TypedRetention(keep.signature, ((0,), (2,), (2,)), keep.readouts, equality)
    assert initial_recognition_is_forward_compatible(keep)
    assert not initial_recognition_is_forward_compatible(breaking)


def test_natural_components_exist_but_output_symmetry_forbids_selected_readout():
    signature = RetentionSignature(2, 1, 2)
    identity_update = ((0,), (1,))
    equality = frozenset({(0, 0), (1, 1)})
    for readout in product(range(2), repeat=2):
        packet = TypedRetention(signature, identity_update, readout, equality)
        assert packet.updates == identity_update
        assert tuple(1 - output for output in packet.readouts) != packet.readouts


def test_exact_arbitrary_precision_counts_and_zero_report_alphabet():
    assert RetentionSignature(2, 0, 0).counts()["packets"] == 0
    assert RetentionSignature(2, 0, 1).counts()["updates"] == 1
    assert RetentionSignature(2, 0, 12).counts()["comparisons"] == 2**144
    with pytest.raises(ValueError):
        RetentionSignature(2, 0, 0).from_codes(0, 0, 0)


@pytest.mark.parametrize("signature", [(0, 1, 1), (-1, 1, 1), (1, -1, 1), (1, 1, -1)])
def test_invalid_cardinalities(signature):
    with pytest.raises(ValueError):
        RetentionSignature(*signature)


def test_boolean_cardinality_and_false_choice_codes_fail_closed():
    with pytest.raises(TypeError):
        RetentionSignature(True, 1, 1)
    with pytest.raises(ValueError):
        RetentionSignature(2, 1, 2).from_codes(4, 0, 0)
    with pytest.raises(ValueError):
        RetentionSignature(2, 1, 2).from_codes(0, False, 0)
