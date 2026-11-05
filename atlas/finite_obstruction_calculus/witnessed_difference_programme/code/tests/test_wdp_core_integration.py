"""End-to-end integration tests for WDP core package, Rust solver, and tests suite.

Obstruction comparisons call the same canonical functional owner; they check adapter
agreement, not independent solvers. Genesis comparisons retain their separate algorithms.

# Executable finite evidence; AuthorityEffect: None.
"""

from fractions import Fraction
import pytest

from witnessed_difference.cochains import FiniteComplex
from witnessed_difference.obstruction import exact_quotient_l1
from witnessed_difference.outcomes import Accepted
from native_wdp import solve_native_obstruction


def test_core_package_and_rust_solver_parity():
    """Verify exact agreement between Python witnessed_difference and native Rust solver."""
    vertices = ("v0", "v1", "v2")
    edges = (("v0", "v1"), ("v1", "v2"), ("v0", "v2"))
    complex_obj = FiniteComplex(vertices, edges)

    # Cochain with holonomy defect
    cochain_map = {
        ("v0", "v1"): Fraction(1),
        ("v1", "v2"): Fraction(1),
        ("v0", "v2"): Fraction(0),
    }

    # Python package calculation
    py_outcome = exact_quotient_l1(complex_obj, cochain_map)
    assert isinstance(py_outcome, Accepted)
    py_cert = py_outcome.value

    # Native Rust calculation
    rust_cert = solve_native_obstruction(vertices, edges, cochain_map)

    # Assert exact parity
    assert py_cert.value == rust_cert.value["phi1"]
    assert (py_cert.value == 0) == rust_cert.value["is_exact"]
    assert rust_cert.value["authority_effect"] == "None"


def test_zero_holonomy_exact_unwinding():
    """Verify exact unwinding when cycle sum vanishes."""
    vertices = ("v0", "v1", "v2")
    edges = (("v0", "v1"), ("v1", "v2"), ("v0", "v2"))
    complex_obj = FiniteComplex(vertices, edges)

    cochain_map = {
        ("v0", "v1"): Fraction(3, 4),
        ("v1", "v2"): Fraction(1, 4),
        ("v0", "v2"): Fraction(1),
    }

    py_outcome = exact_quotient_l1(complex_obj, cochain_map)
    assert isinstance(py_outcome, Accepted)
    py_cert = py_outcome.value

    rust_cert = solve_native_obstruction(vertices, edges, cochain_map)

    assert py_cert.value == Fraction(0)
    assert rust_cert.value["phi1"] == Fraction(0)
    assert rust_cert.value["is_exact"] is True
