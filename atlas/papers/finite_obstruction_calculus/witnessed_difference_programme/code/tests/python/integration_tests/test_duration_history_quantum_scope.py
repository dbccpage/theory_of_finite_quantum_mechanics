from fractions import Fraction

from witnessed_difference.cochains import FiniteComplex
from witnessed_difference.duration import DurationClass, classify_duration
from witnessed_difference.histories import FiniteHistoryGraph, WeightedEdge, finite_history_sum
from witnessed_difference.outcomes import Accepted, RefusalCode, Refused
from witnessed_difference.probability import FiniteWitnessSpace, event_probability
from witnessed_difference.quantum import (
    QuantumEvidence,
    holonomy,
    make_connection,
    supports_quantum_reconstruction,
)
from witnessed_difference.relative_status import (
    Claim,
    ClaimStatus,
    EvaluationProfile,
    attach_finite_witness,
    route_claim,
)


def test_finite_history_can_feed_declared_gauge_calculation_without_scope_promotion() -> None:
    complex_ = FiniteComplex(("a", "b", "c"), (("a", "b"), ("b", "c"), ("a", "c")))
    duration = classify_duration(
        complex_, {("a", "b"): 1, ("b", "c"): 1, ("a", "c"): 3}
    )
    assert duration.kind is DurationClass.CLOSED_NON_EXACT

    graph = FiniteHistoryGraph(
        ("a", "b", "c"),
        (WeightedEdge("a", "b", Fraction(1, 2)), WeightedEdge("b", "c", Fraction(1, 2))),
    )
    history = finite_history_sum(graph, "a", "c", 2)
    assert isinstance(history, Accepted) and history.value == Fraction(1, 4)
    probability = event_probability(FiniteWitnessSpace(("path", "no-path", "path", "path")), frozenset({"path"}))
    assert isinstance(probability, Accepted) and probability.value == Fraction(3, 4)

    connection = make_connection(
        ("a", "b", "c"),
        (("a", "b", 1j), ("b", "c", 1 + 0j), ("a", "c", 1 + 0j)),
    )
    assert isinstance(connection, Accepted)
    loop = holonomy(connection.value, ("a", "b", "c", "a"))
    assert isinstance(loop, Accepted) and loop.value.norm_squared() == 1

    firewall = supports_quantum_reconstruction(QuantumEvidence.DECLARED_U1_CALCULATION)
    assert isinstance(firewall, Refused) and firewall.code is RefusalCode.SCOPE_VIOLATION
    routed = route_claim(
        Claim("WD6-RECONSTRUCTION", ClaimStatus.OPEN),
        EvaluationProfile("finite-python", frozenset({"WD6-RECONSTRUCTION"})),
    )
    assert attach_finite_witness(routed, "u1-loop").relative_status is ClaimStatus.OPEN
# Executable finite evidence; AuthorityEffect: None.
