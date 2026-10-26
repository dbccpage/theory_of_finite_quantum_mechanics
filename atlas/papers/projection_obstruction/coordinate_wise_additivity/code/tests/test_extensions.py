"""Unit & Integration Tests for GS-000 Extensions: Cohomology Quotients, Gauge Holonomies, and Quantum Schatten Norms."""

import numpy as np
import pytest
from cohomology_quotients import (
    DirectedGraph,
    coboundary_d0,
    global_orbit_zero_difference_equiv,
    is_coboundary,
    lggr_obstruction_witness,
    local_zero_difference_equiv,
)
from coord_additivity import EdgeOrbitDiagnostic
from gauge_holonomy import (
    CellComplex2D,
    Plaquette,
    SU2GaugeField,
    U1GaugeField,
    check_disjoint_plaquette_additivity,
    evaluate_u1_flux_l1,
)
from quantum_schatten import (
    are_mutually_orthogonal_support,
    cptp_depolarizing_channel,
    is_orthogonal_operator_additive,
    is_unitarily_invariant,
    quantum_state_trace_distance,
    schatten_norm,
    singular_values,
    trace_norm,
)


class TestCohomologyQuotients:
    """Tests for graph cochains, coboundary operator d_0, and LGGR/EPK quotient relations."""

    def test_directed_graph_and_incidence_matrix(self):
        # Triangle graph: vertices 0, 1, 2; edges (0,1), (1,2), (2,0)
        edges = ((0, 1), (1, 2), (2, 0))
        g = DirectedGraph(num_vertices=3, edges=edges)
        assert g.num_vertices == 3
        assert g.num_edges == 3

        b = g.incidence_matrix()
        # Row 0: -1 at 0, +1 at 1
        assert b[0, 0] == -1.0 and b[0, 1] == 1.0 and b[0, 2] == 0.0
        # Row 1: -1 at 1, +1 at 2
        assert b[1, 1] == -1.0 and b[1, 2] == 1.0
        # Row 2: -1 at 2, +1 at 0
        assert b[2, 2] == -1.0 and b[2, 0] == 1.0

    def test_coboundary_d0_exactness(self):
        edges = ((0, 1), (1, 2), (2, 0))
        g = DirectedGraph(num_vertices=3, edges=edges)

        # 1D potential
        v = np.array([10.0, 25.0, 15.0])
        delta = coboundary_d0(g, v)
        # edge 0: v1 - v0 = 15.0
        # edge 1: v2 - v1 = -10.0
        # edge 2: v0 - v2 = -5.0
        assert np.allclose(delta, [15.0, -10.0, -5.0])
        assert np.isclose(np.sum(delta), 0.0)  # Cycle sum must vanish

        # Exact coboundary detection
        is_exact, v_rec = is_coboundary(g, delta)
        assert is_exact
        assert v_rec is not None

        # Obstructed cochain with non-zero cycle flux
        obstructed_delta = np.array([15.0, -10.0, 0.0])  # Cycle sum = 5.0
        is_exact_bad, _ = is_coboundary(g, obstructed_delta)
        assert not is_exact_bad

    def test_coboundary_d0_2d_multichannel(self):
        edges = ((0, 1), (1, 2))
        g = DirectedGraph(num_vertices=3, edges=edges)
        v = np.array([[1.0, 2.0], [3.0, 5.0], [7.0, 11.0]])
        delta = coboundary_d0(g, v)
        assert delta.shape == (2, 2)
        assert np.allclose(delta[0], [2.0, 3.0])
        assert np.allclose(delta[1], [4.0, 6.0])

        is_exact, v_rec = is_coboundary(g, delta)
        assert is_exact
        assert v_rec is not None

        with pytest.raises(ValueError, match="must be 1D or 2D"):
            coboundary_d0(g, np.zeros((3, 2, 2)))

        with pytest.raises(ValueError, match="must be 1D or 2D"):
            is_coboundary(g, np.zeros((2, 2, 2)))

    def test_local_vs_global_zero_difference_and_lggr(self):
        d1 = [np.array([1.0, 2.0]), np.array([3.0, 4.0])]
        d2 = [np.array([-3.0, 0.0]), np.array([0.0, 7.0])]
        weights = [1.0, 1.0]

        # d1 l1 = 3, 7; d2 l1 = 3, 7 -> local green
        assert local_zero_difference_equiv(d1, d2, weights)

        with pytest.raises(ValueError, match="Edge count mismatch"):
            local_zero_difference_equiv(d1, [d2[0]], weights)

        diag = EdgeOrbitDiagnostic(orbit_of_edge=(0, 1), orbit_weights=(1.0, 2.0))
        assert global_orbit_zero_difference_equiv(d1, d2, diag)

        # LGGR witness test
        witness = lggr_obstruction_witness()
        assert witness["local_green"]
        assert witness["unweighted_equal"]
        assert witness["global_red"]


class TestLatticeGaugeHolonomies:
    """Tests for discrete U(1) and SU(2) gauge fields, plaquettes, and Wilson loops."""

    def test_u1_gauge_holonomy_and_flux(self):
        # 4 vertices, 4 edges making a single square plaquette
        edges = ((0, 1), (1, 2), (2, 3), (3, 0))
        p0 = Plaquette(plaquette_id=0, boundary=((0, 1), (1, 1), (2, 1), (3, 1)))
        complex2d = CellComplex2D(num_vertices=4, edges=edges, plaquettes=(p0,))

        phases = [0.1, 0.2, 0.3, 0.4]
        field = U1GaugeField(4, phases)

        w = field.link_variable(0)
        assert np.isclose(abs(w), 1.0)

        hol = field.plaquette_holonomy(p0)
        assert np.isclose(abs(hol), 1.0)

        expected_flux = sum(phases)  # 1.0 radian
        assert np.isclose(field.plaquette_flux(p0), expected_flux)
        assert np.isclose(field.wilson_curvature_defect(p0), 1.0 - np.cos(expected_flux))

        val = evaluate_u1_flux_l1(field, complex2d, [2.5])
        assert np.isclose(val, 2.5 * 1.0)

        with pytest.raises(ValueError, match="count mismatch"):
            U1GaugeField(4, [0.1, 0.2])

        with pytest.raises(ValueError, match="count mismatch"):
            evaluate_u1_flux_l1(field, complex2d, [1.0, 2.0])

    def test_disjoint_plaquette_additivity(self):
        # Two disjoint squares: edges 0..3 and 4..7
        edges = (
            (0, 1), (1, 2), (2, 3), (3, 0),
            (4, 5), (5, 6), (6, 7), (7, 4),
        )
        p0 = Plaquette(0, ((0, 1), (1, 1), (2, 1), (3, 1)))
        p1 = Plaquette(1, ((4, 1), (5, 1), (6, 1), (7, 1)))
        complex2d = CellComplex2D(num_vertices=8, edges=edges, plaquettes=(p0, p1))

        phases_a = [0.2, 0.1, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
        phases_b = [0.0, 0.0, 0.0, 0.0, 0.3, 0.2, 0.1, 0.0]

        fa = U1GaugeField(8, phases_a)
        fb = U1GaugeField(8, phases_b)

        weights = [1.0, 2.0]
        ok = check_disjoint_plaquette_additivity(
            complex2d, fa, fb, weights,
            active_plaquettes_a={0}, active_plaquettes_b={1},
        )
        assert ok

        with pytest.raises(ValueError, match="must be disjoint"):
            check_disjoint_plaquette_additivity(
                complex2d, fa, fb, weights,
                active_plaquettes_a={0}, active_plaquettes_b={0},
            )

    def test_su2_gauge_field(self):
        p0 = Plaquette(0, ((0, 1), (1, 1), (2, -1)))
        u_id = np.eye(2, dtype=complex)
        su2_field = SU2GaugeField(3, [u_id, u_id, u_id])
        hol = su2_field.plaquette_holonomy(p0)
        assert np.allclose(hol, u_id)
        assert np.isclose(su2_field.wilson_curvature_defect(p0), 0.0)

        # Default initialization
        su2_default = SU2GaugeField(3)
        assert len(su2_default.matrices) == 3

        with pytest.raises(ValueError, match="count mismatch"):
            SU2GaugeField(3, [u_id])


class TestQuantumSchattenNorms:
    """Tests for non-commutative Schatten norms, orthogonal operator additivity, and unitary invariance."""

    def test_singular_values_and_schatten_norms(self):
        a = np.array([[3.0, 0.0], [0.0, -4.0]])
        s = singular_values(a)
        assert np.allclose(s, [4.0, 3.0])

        assert schatten_norm(a, p=1) == 7.0
        assert trace_norm(a) == 7.0
        assert schatten_norm(a, p=2) == 5.0
        assert schatten_norm(a, p="inf") == 4.0
        assert schatten_norm(a, p=np.inf) == 4.0

        # General p
        val_p3 = schatten_norm(a, p=3)
        assert np.isclose(val_p3, (4.0**3 + 3.0**3) ** (1.0 / 3.0))

        # Empty matrix
        assert schatten_norm(np.empty((0, 0)), p=1) == 0.0

        with pytest.raises(ValueError, match="p must be > 0"):
            schatten_norm(a, p=-1)

    def test_orthogonal_operator_support(self):
        # A supported on (row 0, col 0), B supported on (row 1, col 1)
        a = np.array([[1.0, 0.0], [0.0, 0.0]])
        b = np.array([[0.0, 0.0], [0.0, 3.0]])
        assert are_mutually_orthogonal_support(a, b)

        # Non-orthogonal: overlapping columns
        c = np.array([[1.0, 2.0], [0.0, 0.0]])
        d = np.array([[0.0, 0.0], [3.0, 4.0]])
        assert not are_mutually_orthogonal_support(c, d)

        with pytest.raises(ValueError, match="dimensions must match"):
            are_mutually_orthogonal_support(a, np.ones((3, 2)))

    def test_unitary_invariance(self):
        a = np.array([[1.0, 2.0], [3.0, 4.0]])
        assert is_unitarily_invariant(trace_norm, a, num_trials=5)
        assert is_unitarily_invariant(lambda m: schatten_norm(m, p=2), a, num_trials=5)

    def test_orthogonal_operator_additivity_forces_schatten1(self):
        dim = 2
        # Trace norm (Schatten 1) IS additive on orthogonal supports
        assert is_orthogonal_operator_additive(trace_norm, dim=dim, num_trials=5)

        # Schatten 2 (Frobenius) is NOT additive (it adds quadratically)
        assert not is_orthogonal_operator_additive(lambda m: schatten_norm(m, p=2), dim=dim, num_trials=5)

        # Operator norm (Schatten inf) is NOT additive (it takes max)
        assert not is_orthogonal_operator_additive(lambda m: schatten_norm(m, p="inf"), dim=dim, num_trials=5)

    def test_quantum_state_trace_distance_and_cptp(self):
        rho = np.array([[1.0, 0.0], [0.0, 0.0]])
        sigma = np.array([[0.0, 0.0], [0.0, 1.0]])
        d_orig = quantum_state_trace_distance(rho, sigma)
        assert np.isclose(d_orig, 1.0)  # Orthogonal pure states have trace distance 1.0

        # Apply depolarizing channel
        rho_dep = cptp_depolarizing_channel(rho, p=0.4)
        sigma_dep = cptp_depolarizing_channel(sigma, p=0.4)
        d_dep = quantum_state_trace_distance(rho_dep, sigma_dep)

        # Trace distance must strictly contract under depolarizing channel
        assert d_dep < d_orig
        assert np.isclose(d_dep, 0.6)  # Exactly (1-p) * 1.0


def test_edge_branch_coverage():
    """Exercise remaining edge branches across modules to achieve maximal coverage."""
    from coord_additivity import coord_linf
    from gauge_holonomy import U1GaugeField
    from perturbations import (
        audit_coordinate_symmetry,
        audit_disjoint_additivity,
        audit_edge_locality,
        audit_orbit_uniformity,
    )

    # coord_linf empty array
    assert coord_linf([]) == 0.0

    # audit_coordinate_symmetry single element
    assert audit_coordinate_symmetry([5.0])[0]

    # audit_disjoint_additivity dim < 2
    assert audit_disjoint_additivity(lambda x: 0.0, dim=1)[0]

    # audit_edge_locality num_edges < 2
    assert audit_edge_locality(lambda x: 0.0, num_edges=1, k=2)[0]

    # audit_orbit_uniformity single element
    assert audit_orbit_uniformity([2.0])[0]

    # U1GaugeField default phases
    u_def = U1GaugeField(3)
    assert len(u_def.phases) == 3
