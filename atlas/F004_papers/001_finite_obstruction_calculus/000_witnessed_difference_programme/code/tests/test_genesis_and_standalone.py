"""Tests for standalone WDP scripts and Genesis observer models.

# Executable finite evidence; AuthorityEffect: None.
"""

from fractions import Fraction
import pytest

from original_genesis_observer import (
    HistoryMemory,
    WordTransducer,
    original_classification,
)
from finite_profile_evaluator import (
    Evidence,
    Profile,
    evaluate,
    status_guards,
    verify_evidence,
)
from functional_classification import (
    RetentionSignature,
    realize_retention,
)
from self_reference_bridges import (
    BridgeSignature,
    realize_bridge,
)
from semiring_coarse_graining import (
    membership,
    product,
    quotient,
)


def test_genesis_observer_properties():
    """Verify Genesis Moore machine run and descent."""
    memory = HistoryMemory(((0, 1), (1, 0)), 0)
    rho = WordTransducer(((0, 0),), (((0,), (1,)),), 0, (1,), ((),))

    certificate = rho.descent(memory)
    assert certificate[:2] == ("map", (1, 0))
    assert rho.verify(memory, certificate)
    assert memory.run(rho.apply((1,) * 10001)) == 0


def test_profile_evaluator_properties():
    """Verify CH20 profile evaluation and guard invariants."""
    profile = Profile(
        table=(("q", True), ("p", False)),
        admitted=frozenset({"q", "p"}),
        refused=frozenset({"p"}),
        budget=2,
    )
    candidates = (Evidence("q", True),)
    status = evaluate(profile, "q", candidates)
    assert status.value == "Proved"
    assert verify_evidence(profile, candidates[0]) is True

    # Refused query
    status_refused = evaluate(profile, "p", candidates)
    assert status_refused.value == "Refused"


def test_functional_classification_properties():
    """Verify retention signature realization and original classification."""
    rho = WordTransducer(((0, 0),), (((0,), (1,)),), 0, (1,), ((),))
    parity = HistoryMemory(((0, 1), (1, 0)), 0)
    status, _ = original_classification(parity, ("a", "b"), {"prefix": rho})
    assert status == "O1Only"

    # Test RetentionSignature
    sig = RetentionSignature(
        nontrivial=True,
        reversible=True,
        observable=True,
        tolerance=False,
        minimal=True,
        active=True,
    )
    assert sig.realizable() is True
    witness = realize_retention(sig)
    assert witness.signature() == sig


def test_self_reference_bridge():
    """Verify self-referential bridge signature realization."""
    sig = BridgeSignature(
        report_total=True,
        linkage_provided=True,
        linkage_verified=True,
        report_stable=True,
        comparison_available=True,
        comparison_success=True,
    )
    assert sig.realizable() is True
    witness = realize_bridge(sig)
    assert witness.signature() == sig


def test_semiring_coarse_graining():
    """Verify exact rational semiring coarse graining and intertwining."""
    matrix = ((2, -1, 3), (0, 1, 3), (4, -2, 1))
    blocks = ((0, 1), (2,))
    reduced = quotient(matrix, blocks)
    assert reduced == ((Fraction(1), Fraction(3)), (Fraction(2), Fraction(1)))
    h = membership(3, blocks)
    assert product(matrix, h) == product(h, reduced)
