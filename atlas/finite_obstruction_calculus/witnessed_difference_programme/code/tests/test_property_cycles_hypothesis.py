"""Property-based testing with Hypothesis on randomized cycle topologies.

# Executable finite evidence; AuthorityEffect: None.
"""

from fractions import Fraction
from hypothesis import given, settings, strategies as st

from witnessed_difference.cochains import FiniteComplex
from witnessed_difference.obstruction import exact_quotient_l1
from witnessed_difference.outcomes import Accepted
from native_wdp import solve_native_obstruction


@st.composite
def rational_strategy(draw):
    num = draw(st.integers(min_value=-500, max_value=500))
    den = draw(st.integers(min_value=1, max_value=500))
    return Fraction(num, den)


@settings(max_examples=40, deadline=None)
@given(
    cycle_len=st.integers(min_value=3, max_value=6),
    data=st.data(),
)
def test_hypothesis_gauge_invariance_and_parity(cycle_len: int, data):
    """Stress-test exact quotient norm, gauge invariance, and Rust parity over random rationals."""
    n = cycle_len
    vertices = tuple(f"v{i}" for i in range(n))
    edges = tuple((f"v{i}", f"v{(i + 1) % n}") for i in range(n))
    complex_obj = FiniteComplex(vertices, edges)

    # Generate random rational edge values
    cochain_map = {}
    for e in edges:
        cochain_map[e] = data.draw(rational_strategy())

    # Calculate via Python
    py_outcome = exact_quotient_l1(complex_obj, cochain_map)
    assert isinstance(py_outcome, Accepted)
    py_cert = py_outcome.value

    # Calculate via Rust native solver
    rust_cert = solve_native_obstruction(vertices, edges, cochain_map)

    # Parity assertions
    assert py_cert.value >= 0
    assert rust_cert.value["phi1"] >= 0
    assert py_cert.value == rust_cert.value["phi1"]
    assert (py_cert.value == 0) == rust_cert.value["is_exact"]

    # Gauge perturbation: add d0(g) for random vertex potential g
    vertex_potentials = {v: data.draw(rational_strategy()) for v in vertices}
    gauged_map = {}
    for u, v in edges:
        d0_val = vertex_potentials[v] - vertex_potentials[u]
        gauged_map[(u, v)] = cochain_map[(u, v)] + d0_val

    # Re-evaluate
    py_gauged_outcome = exact_quotient_l1(complex_obj, gauged_map)
    assert isinstance(py_gauged_outcome, Accepted)
    py_gauged_cert = py_gauged_outcome.value

    rust_gauged_cert = solve_native_obstruction(vertices, edges, gauged_map)

    # Gauge invariance
    assert py_gauged_cert.value == py_cert.value
    assert rust_gauged_cert.value["phi1"] == rust_cert.value["phi1"]
