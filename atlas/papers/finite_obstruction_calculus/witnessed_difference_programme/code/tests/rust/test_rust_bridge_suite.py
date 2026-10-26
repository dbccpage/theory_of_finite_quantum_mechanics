"""Tests for the native_wdp Python-to-Rust bridge module.

# Executable finite evidence; AuthorityEffect: None.
"""

from __future__ import annotations

import os
from fractions import Fraction
from pathlib import Path
import pytest

from native_wdp import (
    NativeWdpUnavailable,
    solve_native_genesis_descent,
    solve_native_obstruction,
)


def test_solve_native_obstruction_require_native_success():
    """Verify solve_native_obstruction succeeds when require_native=True."""
    vertices = ("v0", "v1", "v2")
    edges = (("v0", "v1"), ("v1", "v2"), ("v0", "v2"))
    cochain = {
        ("v0", "v1"): Fraction(1),
        ("v1", "v2"): Fraction(2),
        ("v0", "v2"): Fraction(3),
    }
    res = solve_native_obstruction(vertices, edges, cochain, require_native=True)
    assert res.value["authority_effect"] == "None"
    assert res.value["is_exact"] is True
    assert res.value["phi1"] == Fraction(0)
    assert res.value["potential"]["v0"] == Fraction(0)
    assert res.value["potential"]["v1"] == Fraction(1)
    assert res.value["potential"]["v2"] == Fraction(3)


def test_solve_native_obstruction_unavailable_error(monkeypatch: pytest.MonkeyPatch):
    """Verify NativeWdpUnavailable is raised when binary is missing and require_native=True."""
    monkeypatch.setenv("WDP_OBSTRUCTION_BIN", "C:\\nonexistent\\solve_wdp_obstruction.exe")
    vertices = ("v0", "v1")
    edges = (("v0", "v1"),)
    cochain = {("v0", "v1"): Fraction(1)}

    with pytest.raises(NativeWdpUnavailable):
        solve_native_obstruction(vertices, edges, cochain, require_native=True)


def test_exact_rational_float_firewall():
    """Verify that floats, bools, and non-rationals are rejected at the bridge firewall."""
    vertices = ("v0", "v1")
    edges = (("v0", "v1"),)

    for invalid_val in [1.5, True, False, float("nan"), float("inf"), "1/2"]:
        with pytest.raises(TypeError, match="Exact rational required"):
            solve_native_obstruction(vertices, edges, {("v0", "v1"): invalid_val})  # type: ignore[arg-type]


def test_solve_native_genesis_descent_require_native_success():
    """Verify solve_native_genesis_descent succeeds with native execution."""
    memory_transitions = [[0, 1], [1, 0]]
    memory_initial = 0
    transducer_transitions = [[0, 0]]
    transducer_emit = [[[0], [1]]]
    transducer_initial = 0
    prefix_words = [1]
    final_words = [[]]

    res = solve_native_genesis_descent(
        memory_transitions,
        memory_initial,
        transducer_transitions,
        transducer_emit,
        transducer_initial,
        prefix_words,
        final_words,
        require_native=True,
    )
    assert res.value["authority_effect"] == "None"
    assert res.value["kind"] == "map"
    assert res.value["prefix"] == [1]


def test_solve_native_genesis_descent_unavailable_error(monkeypatch: pytest.MonkeyPatch):
    """Verify NativeWdpUnavailable is raised when genesis binary is missing and require_native=True."""
    monkeypatch.setenv("WDP_GENESIS_BIN", "C:\\nonexistent\\solve_genesis_observer.exe")
    with pytest.raises(NativeWdpUnavailable):
        solve_native_genesis_descent(
            [[0, 1], [1, 0]], 0, [[0, 0]], [[[0], [1]]], 0, [1], [[]], require_native=True
        )


@pytest.mark.parametrize("require_native", [True, False])
def test_missing_native_never_falls_back(monkeypatch, require_native):
    monkeypatch.setenv("WDP_OBSTRUCTION_BIN", "/nonexistent/solve_wdp_obstruction")
    with pytest.raises(NativeWdpUnavailable):
        solve_native_obstruction(("a", "b"), (("a", "b"),),
                                 {("a", "b"): Fraction(1)}, require_native=require_native)


def test_disconnected_graph_components():
    """Verify native solver operates correctly on disconnected graph components."""
    vertices = ("a0", "a1", "b0", "b1")
    edges = (("a0", "a1"), ("b0", "b1"))
    cochain = {
        ("a0", "a1"): Fraction(5),
        ("b0", "b1"): Fraction(7),
    }

    res = solve_native_obstruction(vertices, edges, cochain, require_native=True)
    assert res.value["is_exact"] is True
    assert res.value["phi1"] == Fraction(0)
    assert res.value["potential"]["a1"] - res.value["potential"]["a0"] == Fraction(5)
    assert res.value["potential"]["b1"] - res.value["potential"]["b0"] == Fraction(7)


def test_large_integer_rational_entries():
    """Verify exact precision with large numerators and denominators (BigRational)."""
    p = 10**18 + 9
    q = 10**18 + 31
    vertices = ("v0", "v1", "v2")
    edges = (("v0", "v1"), ("v1", "v2"), ("v0", "v2"))
    cochain = {
        ("v0", "v1"): Fraction(p, q),
        ("v1", "v2"): Fraction(2 * p, q),
        ("v0", "v2"): Fraction(3 * p, q),
    }

    res = solve_native_obstruction(vertices, edges, cochain, require_native=True)
    assert res.value["is_exact"] is True
    assert res.value["phi1"] == Fraction(0)
    assert res.value["potential"]["v2"] - res.value["potential"]["v0"] == Fraction(3 * p, q)
