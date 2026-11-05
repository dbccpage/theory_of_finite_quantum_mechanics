import random
from dataclasses import replace
from fractions import Fraction
from itertools import product

from witnessed_difference.cochains import FiniteComplex
from witnessed_difference.complex_growth import (
    GrowthReceipt,
    WeightedWindow,
    attach_face,
    claim_growth_repair,
    growth_receipt,
    make_window,
    restrict_complex,
    subdivide_edge,
)
from witnessed_difference.obstruction import DiagnosticClass, verify_quotient_certificate
from witnessed_difference.outcomes import Accepted, AuthorityEffect, RefusalCode, Refused

TRIANGLE_EDGES = ((0, 1), (1, 2), (0, 2))
CYCLE_EDGES = ((0, 1), (1, 2), (2, 3), (0, 3))


def accepted(outcome):
    assert isinstance(outcome, Accepted), outcome
    assert outcome.authority_effect is AuthorityEffect.NONE
    return outcome.value


def refused(outcome, code: RefusalCode, fragment: str = "") -> Refused:
    assert isinstance(outcome, Refused), outcome
    assert outcome.code is code, outcome
    assert fragment in outcome.detail, outcome.detail
    return outcome


def window(vertices, edges, values, weights=None, faces=()) -> WeightedWindow:
    complex_ = FiniteComplex(vertices, edges, faces)
    declared = None if weights is None else dict(zip(edges, weights))
    return accepted(make_window(complex_, dict(zip(edges, values)), declared))


def phi(before: WeightedWindow, after: WeightedWindow) -> GrowthReceipt:
    receipt = accepted(growth_receipt(before, after))
    assert accepted(verify_quotient_certificate(receipt.before_certificate)) is receipt.before_certificate
    assert accepted(verify_quotient_certificate(receipt.after_certificate)) is receipt.after_certificate
    return receipt


def test_manuscript_triangle_example_attach_and_split() -> None:
    hollow = window((0, 1, 2), TRIANGLE_EDGES, (1, 1, -1))
    filled = accepted(attach_face(hollow, (0, 1, 2)))
    receipt = phi(hollow, filled)
    assert (receipt.before_phi1, receipt.before_gamma2) == (3, 0)
    assert (receipt.after_phi1, receipt.after_gamma2) == (3, 3)
    assert receipt.phi1_change == 0 and receipt.gamma2_change == 3
    assert receipt.before_class is DiagnosticClass.CLOSED_RESIDUAL
    assert receipt.after_class is DiagnosticClass.ACTIVE_CLOSURE_FAILURE
    for split in (Fraction(1, 2), 5):
        subdivided = accepted(subdivide_edge(hollow, (0, 1), "m", split))
        assert subdivided.complex_.edges == ((0, "m"), ("m", 1), (1, 2), (0, 2))
        assert subdivided.cochain[:2] == (Fraction(split), 1 - Fraction(split))
        assert subdivided.weights == (1, 1, 1, 1)
        assert phi(hollow, subdivided).after_phi1 == 3


def test_face_attachment_never_changes_phi_and_can_raise_gamma_exhaustively() -> None:
    raised = 0
    for values in product(range(-2, 3), repeat=3):
        for weights in ((1, 1, 1), (1, 2, 3)):
            hollow = window((0, 1, 2), TRIANGLE_EDGES, values, weights)
            receipt = phi(hollow, accepted(attach_face(hollow, (0, 1, 2))))
            assert receipt.phi1_change == 0
            assert receipt.before_gamma2 == 0 and receipt.after_gamma2 >= 0
            raised += receipt.gamma2_change > 0
    assert raised > 0


def test_equal_weight_subdivision_never_changes_phi_exhaustively() -> None:
    for values in product(range(-2, 3), repeat=3):
        hollow = window((0, 1, 2), TRIANGLE_EDGES, values, (2, 1, 3))
        for edge, split in product(TRIANGLE_EDGES, (0, Fraction(1, 3), -2)):
            subdivided = accepted(subdivide_edge(hollow, edge, "m", split))
            assert phi(hollow, subdivided).phi1_change == 0


def test_restriction_never_raises_phi_on_the_triangle_and_the_four_cycle() -> None:
    cases = [((0, 1, 2), TRIANGLE_EDGES, 3), ((0, 1, 2, 3), CYCLE_EDGES, 4)]
    for vertices, edges, size in cases:
        for values in product(range(-1, 2) if size == 4 else range(-2, 3), repeat=size):
            big = window(vertices, edges, values, tuple(range(1, size + 1)))
            for dropped in edges:
                kept = tuple(edge for edge in edges if edge != dropped)
                small = accepted(restrict_complex(big, vertices, kept))
                assert small.weights == tuple(big.weight_map()[edge] for edge in kept)
                assert phi(small, big).phi1_change >= 0


def test_restriction_on_random_subgraph_pairs() -> None:
    rng = random.Random(20260929)
    for _ in range(40):
        count = rng.randint(3, 5)
        pairs = [(a, b) for a in range(count) for b in range(a + 1, count)]
        edges = tuple(rng.sample(pairs, rng.randint(count - 1, len(pairs))))
        values = tuple(rng.randint(-3, 3) for _ in edges)
        weights = tuple(Fraction(rng.randint(1, 4), rng.randint(1, 3)) for _ in edges)
        big = window(tuple(range(count)), edges, values, weights)
        kept = tuple(rng.sample(edges, rng.randint(1, len(edges) - 1)))
        vertices = tuple(sorted({vertex for edge in kept for vertex in edge}))
        small = accepted(restrict_complex(big, vertices, kept))
        assert phi(small, big).phi1_change >= 0


def test_restriction_keeps_declared_faces() -> None:
    filled = window((0, 1, 2), TRIANGLE_EDGES, (1, 1, 0), faces=((0, 1, 2),))
    same = accepted(restrict_complex(filled, (0, 1, 2), TRIANGLE_EDGES, ((0, 1, 2),)))
    assert same == filled
    hollow = accepted(restrict_complex(filled, (0, 1, 2), TRIANGLE_EDGES))
    receipt = phi(hollow, filled)
    assert receipt.phi1_change == 0 and receipt.after_gamma2 == 2


def test_growth_is_never_a_repair_claim() -> None:
    big = window((0, 1, 2), TRIANGLE_EDGES, (1, 1, -1))
    small = accepted(restrict_complex(big, (0, 1, 2), TRIANGLE_EDGES[:2]))
    shrink = phi(big, small)
    assert shrink.phi1_change == -3
    grow = phi(small, big)
    for receipt in (shrink, grow):
        refused(claim_growth_repair(receipt), RefusalCode.SCOPE_VIOLATION, "fixed window")
    refused(claim_growth_repair("receipt"), RefusalCode.INVALID_INPUT)


def test_window_admission_refusals() -> None:
    triangle = FiniteComplex((0, 1, 2), TRIANGLE_EDGES)
    refused(make_window("complex", {}), RefusalCode.INVALID_INPUT, "finite complex")
    refused(make_window(triangle, {(0, 1): 1}), RefusalCode.INVALID_INPUT, "cochain")
    refused(make_window(triangle, dict.fromkeys(TRIANGLE_EDGES, 0.5)), RefusalCode.INVALID_INPUT)
    refused(make_window(triangle, dict.fromkeys(TRIANGLE_EDGES, 1), dict.fromkeys(TRIANGLE_EDGES, 0)), RefusalCode.INVALID_INPUT)
    reversed_values = accepted(make_window(triangle, {(1, 0): 2, (1, 2): 0, (0, 2): 0}))
    assert reversed_values.cochain == (-2, 0, 0)


def test_growth_step_refusals() -> None:
    hollow = window((0, 1, 2), TRIANGLE_EDGES, (1, 1, -1))
    filled = accepted(attach_face(hollow, (0, 1, 2)))
    refused(restrict_complex(hollow, (0, 1, 2, 3), TRIANGLE_EDGES), RefusalCode.OUTSIDE_CARRIER)
    refused(restrict_complex(hollow, (0, 1, 2), ((1, 0),)), RefusalCode.OUTSIDE_CARRIER)
    refused(restrict_complex(hollow, ([0],), ()), RefusalCode.OUTSIDE_CARRIER)
    refused(restrict_complex(filled, (0, 1, 2), TRIANGLE_EDGES, ((0, 2, 1),)), RefusalCode.OUTSIDE_CARRIER)
    refused(restrict_complex(hollow, (0, 1), TRIANGLE_EDGES), RefusalCode.INVALID_INPUT, "not a finite complex")
    refused(restrict_complex(filled, (0, 1, 2), TRIANGLE_EDGES[:2], ((0, 1, 2),)), RefusalCode.INVALID_INPUT)
    refused(attach_face(filled, (2, 1, 0)), RefusalCode.INVALID_INPUT, "not a new face")
    refused(attach_face(hollow, [0, 1, 2]), RefusalCode.INVALID_INPUT, "not a new face")
    refused(attach_face(filled, ([0], 1, 2)), RefusalCode.INVALID_INPUT, "not a new face")
    path = window((0, 1, 2), TRIANGLE_EDGES[:2], (1, 1))
    refused(attach_face(path, (0, 1, 2)), RefusalCode.INVALID_INPUT, "not a finite complex")
    refused(subdivide_edge(hollow, (1, 0), "m", 0), RefusalCode.OUTSIDE_CARRIER)
    refused(subdivide_edge(filled, (0, 1), "m", 0), RefusalCode.INVALID_INPUT, "bounds a declared face")
    refused(subdivide_edge(hollow, (0, 1), 2, 0), RefusalCode.INVALID_INPUT, "must be new")
    refused(subdivide_edge(hollow, (0, 1), "m", 0.5), RefusalCode.INVALID_INPUT, "exact")
    refused(subdivide_edge(hollow, (0, 1), ["m"], 0), RefusalCode.INVALID_INPUT, "not a finite complex")
    for step in (
        lambda w: restrict_complex(w, (0, 1, 2), TRIANGLE_EDGES),
        lambda w: attach_face(w, (0, 1, 2)),
        lambda w: subdivide_edge(w, (0, 1), "m", 0),
        lambda w: growth_receipt(w, hollow),
        lambda w: growth_receipt(hollow, w),
    ):
        refused(step("window"), RefusalCode.INVALID_INPUT, "weighted window")
        refused(step(replace(hollow, cochain=(Fraction(1),))), RefusalCode.INVALID_INPUT, "aligned")
        refused(step(replace(hollow, weights=(Fraction(1), Fraction(1), Fraction(0)))), RefusalCode.INVALID_INPUT)


# Executable finite evidence; AuthorityEffect: None.
