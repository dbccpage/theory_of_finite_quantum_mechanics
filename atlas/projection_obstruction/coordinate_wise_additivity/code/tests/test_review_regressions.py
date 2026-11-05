"""Regression witnesses for invalid-input acceptance and quotient confusion."""

import json
import subprocess
import sys
from fractions import Fraction
from pathlib import Path

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
from coord_additivity import (
    EdgeOrbitDiagnostic,
    anisotropic_l1,
    ce3_cross_edge_fails_locality,
    ce5_lp_power_fails_homogeneity,
    coord_l1,
    coord_l1_exact,
    coord_l2,
    coord_linf,
    decompose_additive_basis,
    decompose_additive_basis_exact,
    is_absolutely_homogeneous,
    is_coord_permutation_symmetric,
    is_disjoint_coord_additive,
    theorem1_holds,
    theorem1_weight,
    uniform_collapse,
)
from quantum_schatten import (
    cptp_depolarizing_channel,
    is_orthogonal_operator_additive,
    is_unitarily_invariant,
    quantum_state_trace_distance,
    schatten_norm,
    trace_norm,
)


@pytest.mark.parametrize("bad", [np.array([np.nan]), np.array([np.inf]),
                                np.array([[1.0]]), np.array([1j])])
@pytest.mark.parametrize("norm", [coord_l1, coord_l2, coord_linf])
def test_norms_reject_a_different_or_nonfinite_carrier(norm, bad):
    with pytest.raises(ValueError):
        norm(bad)


@pytest.mark.parametrize("weight", [-1.0, np.nan, np.inf])
def test_weights_cannot_make_an_invalid_seminorm(weight):
    with pytest.raises(ValueError):
        coord_l1([1.0], weight)
    with pytest.raises(ValueError):
        anisotropic_l1([1.0], (weight,))
    with pytest.raises(ValueError):
        EdgeOrbitDiagnostic((0,), (weight,))
    with pytest.raises(ValueError):
        uniform_collapse([weight], [1.0])


@pytest.mark.parametrize("orbit", [-1, 1, 0.5, True])
def test_orbit_ids_do_not_use_negative_or_coerced_indexing(orbit):
    with pytest.raises(ValueError, match="orbit id"):
        EdgeOrbitDiagnostic((orbit,), (1.0,))


@pytest.mark.parametrize("value", [np.nan, np.inf, -1.0])
def test_nonfinite_or_negative_callable_values_cannot_pass_probes(value):
    def bad_nu(x):
        return value
    for probe in (
        lambda: is_absolutely_homogeneous(bad_nu, np.ones(2), [2.0]),
        lambda: is_coord_permutation_symmetric(bad_nu, np.ones(2)),
        lambda: is_disjoint_coord_additive(bad_nu, 2),
        lambda: decompose_additive_basis(bad_nu, 2),
        lambda: theorem1_holds(bad_nu, [np.ones(2)]),
    ):
        with pytest.raises(ValueError, match="diagnostic output"):
            probe()


def test_a_finite_success_does_not_prove_theorem1():
    # L2 agrees with L1 on the sampled basis but fails at (1,1).
    assert theorem1_holds(coord_l2, [np.array([1.0, 0.0])])[0]
    assert not theorem1_holds(coord_l2, [np.ones(2)])[0]


def test_euclidean_norm_avoids_squaring_overflow_on_representable_results():
    assert coord_l2([1e308]) == 1e308
    assert coord_l2([]) == 0


@pytest.mark.parametrize("dimension", [-1, 1.5, True])
def test_invalid_dimensions_are_rejected(dimension):
    for extract in (decompose_additive_basis, decompose_additive_basis_exact):
        with pytest.raises(ValueError, match="dimension"):
            extract(coord_l1, dimension)
    with pytest.raises(ValueError, match="dimension"):
        theorem1_weight(coord_l1, dimension)


def test_empty_and_mismatched_probes_have_no_positive_receipt():
    with pytest.raises(ValueError, match="positive integer"):
        theorem1_weight(coord_l1, 0)
    with pytest.raises(ValueError, match="probe dimension"):
        theorem1_holds(coord_l1, [np.ones(1), np.ones(2)])
    with pytest.raises(ValueError, match="scalar probe"):
        is_absolutely_homogeneous(coord_l1, np.ones(1), [])
    with pytest.raises(ValueError, match="tolerance"):
        is_coord_permutation_symmetric(coord_l1, np.ones(1), atol=np.nan)
    assert decompose_additive_basis(coord_l1, 0) == []


def test_uniformity_requires_matching_counts_and_exactly_equal_weights():
    with pytest.raises(ValueError, match="count mismatch"):
        uniform_collapse([1.0, 2.0], [3.0])
    with pytest.raises(ValueError, match="edge norm"):
        uniform_collapse([1.0], [-1.0])
    # Approximate agreement is not the uniformity hypothesis of Theorem 3.
    assert uniform_collapse([1.0, np.nextafter(1.0, 2.0)], [3.0, 4.0])[1] is None
    with pytest.raises(ValueError, match="weight must be nonnegative"):
        coord_l1_exact([1], -1)


def test_edges_share_the_declared_coordinate_dimension():
    diagnostic = EdgeOrbitDiagnostic((0, 0), (Fraction(3, 2),))
    with pytest.raises(ValueError, match="coordinate dimension"):
        diagnostic.total([np.ones(1), np.ones(2)])
    with pytest.raises(ValueError, match="coordinate dimension"):
        diagnostic.total_exact([[Fraction(1)], [Fraction(1), Fraction(2)]])
    assert diagnostic.total_exact([[Fraction(1, 3)], [Fraction(-1, 3)]]) == 1


def test_quotient_examples_use_the_same_pair_for_each_comparison():
    witness = lggr_obstruction_witness()
    assert witness["local_green"] and witness["fixed_profile_global_equal"]
    assert witness["fixed_profile_total_1"] == witness["fixed_profile_total_2"] == 13
    assert witness["unweighted_equal"] and not witness["coarse_pair_per_edge_equal"]
    assert witness["orbit_total_a"] == 13 and witness["orbit_total_b"] == 17
    assert witness["varying_profile_total_1"] == 13
    assert witness["varying_profile_total_2"] == 20
    assert ce3_cross_edge_fails_locality()


@pytest.mark.parametrize("vertices,edges", [(-1, ()), (2, ((-1, 0),)),
                                          (2, ((0, 2),)), (2, ((0,),))])
def test_graph_indices_cannot_escape_the_declared_carrier(vertices, edges):
    with pytest.raises(ValueError):
        DirectedGraph(vertices, edges)


def test_empty_graph_coboundaries_and_multichannel_residuals():
    graph = DirectedGraph(2, ())
    assert coboundary_d0(graph, np.ones(2)).shape == (0,)
    assert is_coboundary(graph, np.empty(0))[0]
    assert is_coboundary(graph, np.empty((0, 2)))[0]
    loop = DirectedGraph(1, ((0, 0),))
    assert not is_coboundary(loop, np.array([[0.0, 1.0]]))[0]


def test_invalid_graph_arrays_and_tolerances_do_not_report_equivalence():
    graph = DirectedGraph(2, ((0, 1),))
    for array in (np.ones(1), np.array([0.0, np.nan]), np.array([1j, 0j])):
        with pytest.raises(ValueError):
            coboundary_d0(graph, array)
    with pytest.raises(ValueError):
        is_coboundary(graph, np.array([np.inf]))
    with pytest.raises(ValueError):
        is_coboundary(graph, np.ones(1), tol=-1)
    with pytest.raises(ValueError):
        local_zero_difference_equiv([np.ones(1)], [np.ones(2)], [1.0])
    with pytest.raises(ValueError):
        global_orbit_zero_difference_equiv([], [], EdgeOrbitDiagnostic((), ()), tol=np.nan)


@pytest.mark.parametrize("p", [0.0, -1.0, np.nan, np.inf])
def test_power_probe_excludes_undefined_and_nonfinite_exponents(p):
    with pytest.raises(ValueError, match="positive"):
        ce5_lp_power_fails_homogeneity(p)


@pytest.mark.parametrize("identifier", [None, ""])
def test_metadata_gate_rejects_the_former_identifierless_relation(tmp_path, identifier):
    root = Path(__file__).resolve().parents[2]
    metadata = json.loads((root / "zenodo_metadata.json").read_text())
    relation = {"relation": "isDerivedFrom", "resource_type": "software", "scheme": "url"}
    if identifier is not None:
        relation["identifier"] = identifier
    metadata["related_identifiers"].append(relation)
    (tmp_path / "zenodo_metadata.json").write_text(json.dumps(metadata))
    result = subprocess.run([
        sys.executable, "-c",
        "import sys; from pathlib import Path; import verify_deposit as v; "
        "v.ROOT=Path(sys.argv[1]); v.verify_metadata()", str(tmp_path),
    ], cwd=root, capture_output=True, text=True)
    assert result.returncode != 0
    assert "requires identifier, relation, and scheme" in result.stderr


def test_quantum_probes_cannot_accept_nan_or_no_trials():
    with pytest.raises(ValueError, match="diagnostic output"):
        is_unitarily_invariant(lambda matrix: np.nan, np.eye(2))
    with pytest.raises(ValueError, match="diagnostic output"):
        is_orthogonal_operator_additive(lambda matrix: np.nan, 2)
    with pytest.raises(ValueError, match="positive integer"):
        is_unitarily_invariant(trace_norm, np.eye(2), num_trials=0)
    with pytest.raises(ValueError, match="at least two"):
        is_orthogonal_operator_additive(trace_norm, 1)
    with pytest.raises(ValueError, match="finite two-dimensional"):
        trace_norm(np.array([1.0]))
    with pytest.raises(ValueError, match="p must be"):
        schatten_norm(np.empty((0, 0)), p=np.nan)


@pytest.mark.parametrize("matrix", [np.empty((0, 0)), np.ones((2, 3)),
                                  np.array([[1, 1], [0, 0]]),
                                  np.eye(2), np.diag([-1.0, 2.0])])
def test_trace_distance_rejects_invalid_density_matrices(matrix):
    with pytest.raises(ValueError, match="density matrix"):
        quantum_state_trace_distance(matrix, np.diag([1.0, 0.0]))


def test_quantum_state_carrier_and_convex_mixture_parameters():
    rho, sigma = np.diag([1.0, 0.0]), np.diag([0.0, 1.0])
    with pytest.raises(ValueError, match="dimensions"):
        quantum_state_trace_distance(rho, np.diag([1.0, 0.0, 0.0]))
    for parameter in (-0.1, 1.1, np.nan):
        with pytest.raises(ValueError, match="mixing weight"):
            cptp_depolarizing_channel(rho, parameter)
    assert quantum_state_trace_distance(cptp_depolarizing_channel(rho, 0), sigma) == 1
    assert quantum_state_trace_distance(cptp_depolarizing_channel(rho, 1),
                                       cptp_depolarizing_channel(sigma, 1)) == 0
