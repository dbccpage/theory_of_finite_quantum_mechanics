"""
Unit tests for DDC Operation M (Typed Refusal).
AuthorityEffect: None.
"""

from fractions import Fraction

from typed_refusal import OperationRequest, TypedRefusalGate


def test_refusal_ungrounded_locus():
    """Verify refusal when locus is not grounded in source text."""
    gate = TypedRefusalGate(grounded_loci={"locus_1"}, valid_witnesses={"wit_1"})
    req = OperationRequest(
        op_letter="E",
        locus="ungrounded_hallucinated_locus",
        witness="wit_1",
        cost=Fraction(1),
        payload={},
    )
    receipt = gate.evaluate(req, remaining_budget=Fraction(10))

    assert receipt is not None
    assert receipt.refusal_code == "REFUSED_UNGROUNDED_LOCUS"
    assert receipt.state_preserved is True


def test_refusal_invalid_witness():
    """Verify refusal when witness digest is missing or invalid."""
    gate = TypedRefusalGate(grounded_loci={"locus_1"}, valid_witnesses={"wit_1"})
    req = OperationRequest(
        op_letter="E",
        locus="locus_1",
        witness="bad_fake_witness",
        cost=Fraction(1),
        payload={},
    )
    receipt = gate.evaluate(req, remaining_budget=Fraction(10))

    assert receipt is not None
    assert receipt.refusal_code == "REFUSED_INVALID_WITNESS"
    assert receipt.state_preserved is True


def test_refusal_budget_exhausted():
    """Verify refusal when operation cost exceeds remaining budget."""
    gate = TypedRefusalGate(grounded_loci={"locus_1"}, valid_witnesses={"wit_1"})
    req = OperationRequest(
        op_letter="E",
        locus="locus_1",
        witness="wit_1",
        cost=Fraction(15),
        payload={},
    )
    receipt = gate.evaluate(req, remaining_budget=Fraction(10))

    assert receipt is not None
    assert receipt.refusal_code == "REFUSED_BUDGET_EXHAUSTED"
    assert receipt.state_preserved is True


def test_valid_request_passes_gate():
    """Verify that a valid, grounded, witnessed, budgeted request passes cleanly."""
    gate = TypedRefusalGate(grounded_loci={"locus_1"}, valid_witnesses={"wit_1"})
    req = OperationRequest(
        op_letter="E",
        locus="locus_1",
        witness="wit_1",
        cost=Fraction(2),
        payload={},
    )
    receipt = gate.evaluate(req, remaining_budget=Fraction(10))

    assert receipt is None
