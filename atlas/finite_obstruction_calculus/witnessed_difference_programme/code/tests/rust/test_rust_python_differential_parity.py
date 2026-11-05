"""Cross-language differential parity tests between Python witnessed_difference and native Rust engine.

Obstruction comparisons call the same canonical functional owner; they check adapter
agreement, not independent solvers. Genesis comparisons retain their separate algorithms.

# Executable finite evidence; AuthorityEffect: None.
"""

from __future__ import annotations

from fractions import Fraction
import json

import pytest

from witnessed_difference.cochains import FiniteComplex
from witnessed_difference.obstruction import exact_quotient_l1
from witnessed_difference.outcomes import Accepted
from original_genesis_observer import HistoryMemory, WordTransducer
from native_wdp import solve_native_genesis_descent, solve_native_obstruction


def test_differential_parity_cycle_graphs():
    """Verify exact parity on 3-cycle, 4-cycle, and 5-cycle graphs."""
    cycles = [
        # Triangle
        (["v0", "v1", "v2"], [("v0", "v1"), ("v1", "v2"), ("v0", "v2")]),
        # Square
        (["a", "b", "c", "d"], [("a", "b"), ("b", "c"), ("c", "d"), ("a", "d")]),
        # Pentagon
        (["p0", "p1", "p2", "p3", "p4"], [("p0", "p1"), ("p1", "p2"), ("p2", "p3"), ("p3", "p4"), ("p0", "p4")]),
    ]

    for vertices, edges in cycles:
        complex_obj = FiniteComplex(tuple(vertices), tuple(edges))

        # Test case 1: Exact cochain (sum around cycle matches boundary)
        exact_cochain = {}
        for idx, (u, v) in enumerate(edges[:-1]):
            exact_cochain[(u, v)] = Fraction(idx + 1, 2)
        # Final edge closes the cycle
        exact_cochain[edges[-1]] = sum(exact_cochain[e] for e in edges[:-1])

        py_res = exact_quotient_l1(complex_obj, exact_cochain)
        assert isinstance(py_res, Accepted)
        rust_res = solve_native_obstruction(vertices, edges, exact_cochain, require_native=True)

        assert py_res.value.value == rust_res.value["phi1"] == Fraction(0)
        assert rust_res.value["is_exact"] is True

        # Test case 2: Obstructed cochain (cycle sum has residual holonomy)
        obstructed_cochain = dict(exact_cochain)
        obstructed_cochain[edges[-1]] = exact_cochain[edges[-1]] + Fraction(1)

        py_obs = exact_quotient_l1(complex_obj, obstructed_cochain)
        assert isinstance(py_obs, Accepted)
        rust_obs = solve_native_obstruction(vertices, edges, obstructed_cochain, require_native=True)

        assert py_obs.value.value == rust_obs.value["phi1"]
        assert rust_obs.value["phi1"] > Fraction(0)
        assert rust_obs.value["is_exact"] is False


def test_differential_parity_tree_topologies():
    """Verify that tree graphs always yield phi1 = 0 in both Python adapters and Rust."""
    # Star graph K_{1,4}
    vertices = ["center", "leaf1", "leaf2", "leaf3", "leaf4"]
    edges = [("center", f"leaf{i}") for i in range(1, 5)]
    complex_obj = FiniteComplex(tuple(vertices), tuple(edges))

    cochain = {
        ("center", "leaf1"): Fraction(3, 7),
        ("center", "leaf2"): Fraction(-5, 11),
        ("center", "leaf3"): Fraction(17, 2),
        ("center", "leaf4"): Fraction(0),
    }

    py_res = exact_quotient_l1(complex_obj, cochain)
    assert isinstance(py_res, Accepted)
    rust_res = solve_native_obstruction(vertices, edges, cochain, require_native=True)

    assert py_res.value.value == Fraction(0)
    assert rust_res.value["phi1"] == Fraction(0)
    assert rust_res.value["is_exact"] is True

    # Check that potential differences match edge values
    for (u, v), val in cochain.items():
        assert rust_res.value["potential"][v] - rust_res.value["potential"][u] == val


def test_differential_parity_genesis_quotient_map():
    """Verify Genesis Moore machine descent parity when configuration is a quotient map."""
    memory_transitions = ((0, 1), (1, 0))
    memory_initial = 0
    transducer_transitions = ((0, 0),)
    transducer_emit = (((0,), (1,)),)
    transducer_initial = 0
    prefix_words = (1,)
    final_words = ((),)

    # Python computation
    py_memory = HistoryMemory(memory_transitions, memory_initial)
    py_transducer = WordTransducer(
        transducer_transitions,
        transducer_emit,
        transducer_initial,
        prefix_words,
        final_words,
    )
    py_cert = py_transducer.descent(py_memory)

    # Rust computation
    rust_cert = solve_native_genesis_descent(
        [list(row) for row in memory_transitions],
        memory_initial,
        [list(row) for row in transducer_transitions],
        [[list(word) for word in row] for row in transducer_emit],
        transducer_initial,
        list(prefix_words),
        [list(word) for word in final_words],
        require_native=True,
    )

    assert py_cert[0] == "map"
    assert rust_cert.value["kind"] == "map"
    assert rust_cert.value["prefix"] == list(prefix_words)
    assert json.loads(rust_cert.value["certificate"]) == list(py_cert[1])


def test_differential_parity_genesis_collision_witness():
    """Verify Genesis Moore machine collision witness discovery parity."""
    # Defective memory transitions causing collision
    memory_transitions = ((0, 1), (0, 1))
    memory_initial = 0
    transducer_transitions = ((0, 0),)
    transducer_emit = (((0,), (1,)),)
    transducer_initial = 0
    prefix_words = (1,)
    final_words = ((),)

    py_memory = HistoryMemory(memory_transitions, memory_initial)
    py_transducer = WordTransducer(
        transducer_transitions,
        transducer_emit,
        transducer_initial,
        prefix_words,
        final_words,
    )
    py_cert = py_transducer.descent(py_memory)

    rust_cert = solve_native_genesis_descent(
        [list(row) for row in memory_transitions],
        memory_initial,
        [list(row) for row in transducer_transitions],
        [[list(word) for word in row] for row in transducer_emit],
        transducer_initial,
        list(prefix_words),
        [list(word) for word in final_words],
        require_native=True,
    )

    assert py_cert[0] == "collision"
    assert rust_cert.value["kind"] == "collision"
    assert rust_cert.value["collision_first"] is not None
    assert rust_cert.value["collision_second"] is not None
