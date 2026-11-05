"""T25-T30: Policy validation, input rejection, and probe counterexample search tests for GS-001.

Verifies rejection of negative tolerances, rejection of complex inputs in real vector space APIs,
typed CounterexampleResult objects, and release manifest integrity.
"""

import sys
from pathlib import Path
import numpy as np
import pytest

_pkg = Path(__file__).resolve().parents[1]
if str(_pkg / "code") not in sys.path:
    sys.path.insert(0, str(_pkg / "code"))

from norms import l1, l2, anisotropic_gauge
from probes import probe_counterexample_search
from gs001_gauges import (
    is_faithful,
    is_absolutely_homogeneous,
    is_subadditive,
    is_m_compatible,
    EdgeDiagram,
    evaluate_max_edgewise,
    evaluate_zero_diagnostic,
    evaluate_anisotropic_edgewise_sum,
    check_p1_additivity,
    check_p2_faithfulness,
    check_p3_maximal_symmetry,
    check_p4_edge_uniformity,
    verify_s9b_two_sided_necessity_table,
)


def test_t25_invalid_negative_tolerance_rejection():
    """T25: Negative tolerances must raise ValueError across all predicate probes."""
    samples = [np.array([1.0, 2.0])]
    with pytest.raises(ValueError, match="non-negative"):
        is_faithful(l1, samples, atol=-1.0)

    with pytest.raises(ValueError, match="non-negative"):
        is_absolutely_homogeneous(l1, samples[0], [2.0], atol=-0.5)

    with pytest.raises(ValueError, match="non-negative"):
        is_subadditive(l1, [(samples[0], samples[0])], atol=-0.1)

    with pytest.raises(ValueError, match="non-negative"):
        is_m_compatible(l1, [np.eye(2)], l2, samples, atol=-0.01)


def test_t26_complex_input_rejection():
    """T26: Real vector space norm APIs must reject complex inputs with TypeError."""
    z = np.array([1.0 + 2.0j, 3.0])
    with pytest.raises(TypeError, match="Real vector space"):
        l1(z)

    with pytest.raises(TypeError, match="Real vector space"):
        l2(z)

    with pytest.raises(TypeError, match="Real vector space"):
        anisotropic_gauge(z, (1.0, 2.0))

    with pytest.raises(TypeError, match="Real vector"):
        is_faithful(l1, [z])

    with pytest.raises(TypeError, match="Real vector"):
        is_absolutely_homogeneous(l1, z, [2.0])


def test_t27_typed_counterexample_result_probe():
    """T27: Sample-based searches must return typed CounterexampleResult objects."""
    samples_in = [np.array([1.0, 0.0]), np.array([0.0, 1.0])]
    # l1 is symmetric on samples_in
    res_no = probe_counterexample_search(
        lambda v: abs(l1(v) - l1(v[::-1])) < 1e-9, samples_in
    )
    assert not res_no.found_counterexample
    assert not bool(res_no)
    assert res_no.witness is None

    # Anisotropic l1 is NOT symmetric
    res_yes = probe_counterexample_search(
        lambda v: abs(
            anisotropic_gauge(v, (1.0, 2.0)) - anisotropic_gauge(v[::-1], (1.0, 2.0))
        )
        < 1e-9,
        [np.array([1.0, 0.0])],
    )
    assert res_yes.found_counterexample
    assert bool(res_yes)
    assert np.allclose(res_yes.witness, np.array([1.0, 0.0]))


def test_t28_edge_and_error_branch_coverage():
    """T28: Verify error handling and edge cases across gs001 modules."""
    from convex import minkowski_functional
    from diagrams import EdgeDiagram
    from norms import anisotropic_gauge, exact_induced_operator_norm

    # Zero vector minkowski
    assert minkowski_functional(np.array([0.0, 0.0]), lambda v: True) == 0.0

    # Horizon scaling error in minkowski
    with pytest.raises(ValueError, match="outside scaling horizon"):
        minkowski_functional(np.array([10.0, 10.0]), lambda v: False)

    # EdgeDiagram invalid weight
    with pytest.raises(ValueError, match="strictly positive"):
        EdgeDiagram(((0, 1),), (-1.0,), (l1,))

    # Anisotropic weight <= 0
    with pytest.raises(ValueError, match="strictly positive"):
        anisotropic_gauge(np.array([1.0, 2.0]), (1.0, -1.0))

    # Anisotropic dim mismatch
    with pytest.raises(ValueError, match="Dimension mismatch"):
        anisotropic_gauge(np.array([1.0, 2.0, 3.0]), (1.0, 2.0))

    # Matrix dim mismatch in exact_induced_operator_norm
    with pytest.raises(ValueError, match="square real matrix"):
        exact_induced_operator_norm(np.ones((2, 3)))

    # linf -> l1 limit > 12
    with pytest.raises(ValueError, match="limited to dimension"):
        exact_induced_operator_norm(np.ones((13, 13)), "linf", "l1")

    # Operator dim mismatch in is_m_compatible
    with pytest.raises(ValueError, match="square real matrices"):
        is_m_compatible(l1, [np.ones((2, 3))])


def test_s9b_two_sided_necessity_table():
    """Verify S9b two-sided necessity table: each counterexample drops exactly one property."""
    table = verify_s9b_two_sided_necessity_table()

    # Verify all 5 diagnostics are present
    assert set(table.keys()) == {
        "nu_max",
        "nu_zero",
        "nu_aniso",
        "nu_weighted",
        "nu_uniform",
    }

    # Row 1: nu_max drops P1
    r_max = table["nu_max"]
    assert r_max.dropped_property == "P1"
    assert not r_max.p1_additive
    assert r_max.p2_faithful
    assert r_max.p3_maximal_symmetry
    assert r_max.p4_uniform
    assert r_max.is_two_sided_witness

    # Row 2: nu_zero drops P2
    r_zero = table["nu_zero"]
    assert r_zero.dropped_property == "P2"
    assert r_zero.p1_additive
    assert not r_zero.p2_faithful
    assert r_zero.p3_maximal_symmetry
    assert r_zero.p4_uniform
    assert r_zero.is_two_sided_witness

    # Row 3: nu_aniso drops P3
    r_aniso = table["nu_aniso"]
    assert r_aniso.dropped_property == "P3"
    assert r_aniso.p1_additive
    assert r_aniso.p2_faithful
    assert not r_aniso.p3_maximal_symmetry
    assert r_aniso.p4_uniform
    assert r_aniso.is_two_sided_witness

    # Row 4: nu_weighted drops P4
    r_weighted = table["nu_weighted"]
    assert r_weighted.dropped_property == "P4"
    assert r_weighted.p1_additive
    assert r_weighted.p2_faithful
    assert r_weighted.p3_maximal_symmetry
    assert not r_weighted.p4_uniform
    assert r_weighted.is_two_sided_witness

    # Row 5: nu_uniform satisfies ALL properties
    r_u = table["nu_uniform"]
    assert r_u.dropped_property == "None"
    assert r_u.p1_additive
    assert r_u.p2_faithful
    assert r_u.p3_maximal_symmetry
    assert r_u.p4_uniform
    assert r_u.is_two_sided_witness


def test_s9b_individual_property_checks_and_error_branches():
    """Verify S9b property checkers, failure modes, and edge cases."""
    # P1 additivity failure on l2 cross-edge aggregation: sqrt(||c1||^2 + ||c2||^2)
    def l2_cross_edge_diag(cochains):
        return float(np.sqrt(sum(l2(c) ** 2 for c in cochains)))

    c1 = [np.array([1.0, 0.0]), np.array([0.0, 0.0])]
    c2 = [np.array([0.0, 0.0]), np.array([0.0, 1.0])]
    assert not check_p1_additivity(l2_cross_edge_diag, c1, c2)

    # P2 faithfulness failure when D(0) != 0
    assert not check_p2_faithfulness(lambda c: 1.0, [c1])

    # P2 faithfulness failure when D(x) = 0 for non-zero x
    assert not check_p2_faithfulness(lambda c: 0.0, [c1])

    # P3 maximal symmetry failure on anisotropic gauge
    aniso_diag = EdgeDiagram(
        ((0, 1),), (1.0,), (lambda v: anisotropic_gauge(v, (1.0, 3.0)),)
    )
    assert not check_p3_maximal_symmetry(aniso_diag)

    # P4 edge uniformity on empty diagram
    assert check_p4_edge_uniformity(EdgeDiagram((), (), ()))

    # P4 edge uniformity failure on non-uniform weights
    non_unif = EdgeDiagram(((0, 1), (1, 2)), (1.0, 2.0), (l2, l2))
    assert not check_p4_edge_uniformity(non_unif)

    # Edge evaluations count mismatches
    diag2 = EdgeDiagram(((0, 1), (1, 2)), (1.0, 1.0), (l2, l2))
    with pytest.raises(ValueError, match="Cochain components count mismatch"):
        evaluate_max_edgewise(diag2, [np.array([1.0, 0.0])])

    with pytest.raises(ValueError, match="Cochain components count mismatch"):
        evaluate_zero_diagnostic(diag2, [np.array([1.0, 0.0])])

    with pytest.raises(ValueError, match="Cochain components count mismatch"):
        evaluate_anisotropic_edgewise_sum(diag2, [np.array([1.0, 0.0])])

    # Anisotropic dimension mismatch
    with pytest.raises(ValueError, match="Dimension mismatch"):
        evaluate_anisotropic_edgewise_sum(
            diag2,
            [np.array([1.0, 0.0, 0.0]), np.array([0.0, 1.0, 0.0])],
            weights_per_dim=(1.0, 2.0),
        )

    # Empty cochains in evaluate_max_edgewise
    empty_diag = EdgeDiagram((), (), ())
    assert evaluate_max_edgewise(empty_diag, []) == 0.0

    # Explicit probe operators and vectors in check_p3_maximal_symmetry
    explicit_ops = [np.eye(2)]
    explicit_vecs = [np.array([1.0, 0.0])]
    assert check_p3_maximal_symmetry(
        EdgeDiagram(((0, 1),), (1.0,), (l2,)),
        probe_operators=explicit_ops,
        probe_vectors=explicit_vecs,
    )


