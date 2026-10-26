"""
Comprehensive Unit Test Suite for PO-000 Projection Obstruction.
Provides Lev Landau style invariants, exact boundary checks, and full coverage
across code/ modules without synthetic positivity hacks or float swallow.
"""

from __future__ import annotations

import sys
import tempfile
from pathlib import Path
from fractions import Fraction
import pytest

_code_dir = Path(__file__).resolve().parents[1]
if str(_code_dir) not in sys.path:
    sys.path.insert(0, str(_code_dir))

from exactsym import Matrix, Rational, simplify

# Imports from package modules inside code/
from exact import (
    as_rational,
    exact_matrix,
    exact_matrix_from_matrix,
    exact_column,
    l1_norm,
    exact_equal,
    expression_text,
)
from cochain_presentation import (
    ObservationMap,
    InducedCochain,
    LinearRepairProblem,
    ObservationPresentation,
    AdmittedComplexV1,
)
from covering_edge import (
    CoveringEdge,
    CoveringEdgeDiagram,
    l1_operator_norm,
)
from evidence import (
    EvidenceKind,
    ReplayVerdict,
    ClaimEvidence,
)
import replica_hierarchy
import retraction_geometry
import transfer
import worked_examples
import falsification_sandbox
import artifact_bundle
import inline_code_companion
import replay
import verify_certificate


# --- Section 1: Exact Module Invariants ---

def test_exact_matrix_validation():
    """Verify exact_matrix handles empty input, ragged rows, and rational conversions."""
    m_empty = exact_matrix([])
    assert m_empty.shape == (0, 0)

    m_valid = exact_matrix([[1, "1/2"], [Fraction(1, 3), Rational(2, 5)]])
    assert m_valid.shape == (2, 2)
    assert m_valid[0, 1] == Rational(1, 2)
    assert m_valid[1, 0] == Rational(1, 3)

    with pytest.raises(ValueError, match="equal length"):
        exact_matrix([[1, 2], [3]])


def test_exact_as_rational_types():
    """Verify as_rational accepts exact types and rejects float/invalid."""
    assert as_rational(True) == Rational(1)
    assert as_rational(False) == Rational(0)
    assert as_rational(5) == Rational(5)
    assert as_rational(Fraction(1, 3)) == Rational(1, 3)
    assert as_rational("3/4") == Rational(3, 4)
    assert as_rational(Rational(2, 5)) == Rational(2, 5)

    with pytest.raises(TypeError):
        as_rational(3.14)
    with pytest.raises(TypeError):
        as_rational([1, 2])  # type: ignore


def test_exact_matrix_from_matrix_and_column():
    """Verify matrix conversion and column vector creation."""
    sym_m = Matrix([[1, 2], [3, 4]])
    ex_m = exact_matrix_from_matrix(sym_m)
    assert ex_m == sym_m

    col = exact_column([1, "2/3", Fraction(3, 4)])
    assert col.shape == (3, 1)
    assert col[1, 0] == Rational(2, 3)


def test_l1_norm_and_exact_equal():
    """Verify symbolic l1_norm and exact_equal comparison."""
    vec = Matrix([[Rational(1, 2)], [Rational(-3, 4)]])
    norm = l1_norm(vec)
    assert norm == Rational(5, 4)

    with pytest.raises(ValueError, match="column vector"):
        l1_norm(Matrix([[1, 2], [3, 4]]))

    assert exact_equal(vec, Matrix([[Rational(1, 2)], [Rational(-3, 4)]]))
    assert not exact_equal(vec, Matrix([[1], [0]]))
    assert not exact_equal(vec, Rational(5, 4))
    assert exact_equal(Rational(1, 2) + Rational(1, 2), 1)


def test_expression_text():
    """Verify deterministic string representations."""
    mat = Matrix([[1, 2], [3, 4]])
    txt = expression_text(mat)
    assert "1" in txt and "4" in txt

    sym_val = simplify(Rational(1, 3) + Rational(2, 3))
    assert expression_text(sym_val) == "1"
    assert expression_text("custom_string") == "custom_string"


# --- Section 2: Cochain Presentation ---

def test_observation_map_exactness():
    """Verify ObservationMap creation and projection."""
    obs = ObservationMap("e1", Matrix([[1, 0], [0, 1]]))
    res = Matrix([[2], [3]])
    out = obs.observe(res)
    assert out == res

    with pytest.raises(ValueError, match="shape"):
        obs.observe(Matrix([[1], [2], [3]]))


def test_induced_cochain():
    """Verify InducedCochain vector assembly."""
    c = InducedCochain(
        edge_order=("e1", "e2"),
        blocks=(Matrix([[1], [2]]), Matrix([[3], [4]])),
    )
    vec = c.as_vector()
    assert vec.shape == (4, 1)

    c_empty = InducedCochain(edge_order=(), blocks=())
    assert c_empty.as_vector().shape == (0, 1)


def test_linear_repair_problem_exact_and_quotient():
    """Verify LinearRepairProblem exactness and quotient certificates."""
    repair_map = Matrix([[1, 0], [0, 1]])
    cochain = Matrix([[2], [3]])
    problem = LinearRepairProblem(repair_map)

    cert_exact = problem.exactness_certificate(cochain)
    assert cert_exact.is_exact_coboundary
    assert cert_exact.verify()

    cert_dist = problem.quotient_l1_distance(cochain)
    assert cert_dist.verify()
    assert cert_dist.distance == 0


def test_observation_presentation_and_complex():
    """Verify ObservationPresentation and AdmittedComplexV1."""
    obs1 = ObservationMap("e1", Matrix([[1, 0]]))
    presentation = ObservationPresentation(["e1"], {"e1": obs1})

    cochain = presentation.induce_field({"e1": Matrix([[2], [3]])})
    assert cochain.as_vector() == Matrix([[2]])

    d0 = Matrix([[1], [0]])
    d1 = Matrix([[0, 1]])
    comp = AdmittedComplexV1(d0, d1)
    assert comp.d0 == d0
    assert comp.d1 == d1

    with pytest.raises(ValueError, match="dimensions do not compose"):
        AdmittedComplexV1(Matrix([[1], [0]]), Matrix([[1, 0, 0]]))


# --- Section 3: Covering Edge Diagrams ---

def test_covering_edge_diagram_validation():
    """Verify CoveringEdgeDiagram fiber and edge invariants."""
    e1 = CoveringEdge("e1", "n1", "n2", Matrix([[1, 0], [0, 1]]))
    diagram = CoveringEdgeDiagram({"n1": 2, "n2": 2}, [e1])
    assert diagram.fiber_dimensions["n1"] == 2
    assert len(diagram.edges) == 1

    with pytest.raises(ValueError, match="at least one fiber"):
        CoveringEdgeDiagram({}, [])

    with pytest.raises(ValueError, match="positive"):
        CoveringEdgeDiagram({"n1": -1}, [])

    with pytest.raises(ValueError, match="unique"):
        CoveringEdgeDiagram({"n1": 2, "n2": 2}, [e1, e1])

    with pytest.raises(ValueError, match="unknown node"):
        CoveringEdgeDiagram({"n1": 2}, [CoveringEdge("e1", "n1", "missing", Matrix([[1, 0]]))])

    with pytest.raises(ValueError, match="shape"):
        CoveringEdgeDiagram({"n1": 2, "n2": 3}, [CoveringEdge("e1", "n1", "n2", Matrix([[1, 0]]))])


def test_l1_operator_norm():
    """Verify exact l1 operator norm calculation."""
    m = Matrix([[1, -3], [2, 1]])
    assert l1_operator_norm(m) == 4
    assert l1_operator_norm(Matrix.zeros(0, 0)) == 0


# --- Section 4: Evidence & Mechanization Records ---

def test_evidence_models():
    """Verify ClaimEvidence and MechanizationRun record validation."""
    ev = ClaimEvidence(
        claim_ids=("A2",),
        title="Test Claim A2",
        evidence_kind=EvidenceKind.EXACT_FINITE,
        verdict=ReplayVerdict.PASS,
        statement_scope="Scope A2",
        algorithm="Exact Math",
    )
    assert ev.claim_ids == ("A2",)
    assert ev.authority_effect == "None"

    # Use complete mechanization run to satisfy model validator
    run = replay.build_mechanization_run()
    assert run.paper_id == "PO-000"
    assert len(run.results) > 0
    assert run.execution_completed


# --- Section 5: Falsification Sandbox & Worked Examples ---

def test_falsification_sandbox_run():
    """Verify falsification sandbox functions and break panel."""
    results = falsification_sandbox.run_all_breaks()
    assert len(results) == 4
    falsification_sandbox.assert_all_breaks_trip(results)

    pos, neg = falsification_sandbox.control_signed_bell_both_signs()
    assert pos > 0 and neg > 0


def test_worked_examples_execution():
    """Verify worked examples suite runs cleanly."""
    xx = worked_examples.two_qubit_xx_example()
    assert xx.observed_defect > 0

    tfim = worked_examples.tfim_normal_rate_example()
    assert tfim.expected_rate == 2.0

    p45_lat = worked_examples.pass45_counterexample_lattice()
    assert len(p45_lat.site_order) == 3

    p45_rep = worked_examples.pass45_counterexample_replay()
    assert p45_rep.isolated_bound_violated


def test_inline_code_companion():
    """Verify inline code companion execution."""
    eig_sum, formula_val = inline_code_companion.run_example_61_bell_state_leakage()
    assert abs(eig_sum - formula_val) < 1e-10

    norm_sum, nu_e = inline_code_companion.run_example_62_tfim_normal_rate()
    assert abs(norm_sum - 2.0) < 1e-10
    assert abs(nu_e - 2.0) < 1e-10


# --- Section 6: Artifact Bundle & Replay Run ---

def test_artifact_bundle_and_replay():
    """Verify write_artifact_bundle, build_mechanization_run, and CLI main functions."""
    run = replay.build_mechanization_run()
    assert run.execution_completed
    assert run.executable_checks_passed

    with tempfile.TemporaryDirectory() as tmpdir:
        tmp_path = Path(tmpdir)
        cert, man = artifact_bundle.write_artifact_bundle(
            tmp_path / "cert.json",
            tmp_path / "SHA256SUMS",
        )
        assert cert.exists()
        assert man.exists()

        res_main = artifact_bundle.main(["--certificate", str(cert), "--manifest", str(man)])
        assert res_main == 0

        res_replay = replay.main(["--output", str(tmp_path / "out.json")])
        assert res_replay == 0


# 2026-09-03: test_generate_figures removed with public_export/ and code/generate_figures.py.

# --- Section 7: Lattice Simulation & Extended Dynamics ---

# 2026-09-03: test_lattice_simulation_trajectories removed with code/lattice_simulation.py.  The module mislabelled norms of nested global commutators as Taylor coefficients of the edgewise defect and never tested its own inequality inside t <= t0; it carried no claim.

# --- Section 8: Independent Verifier Module ---

def test_independent_verifier_module():
    """Verify verify_certificate module logic."""
    run = replay.build_mechanization_run()
    pkg_root = Path(_code_dir).parent
    errors = verify_certificate.verify_document(run.model_dump(mode="json"), pkg_root)
    assert errors == []

    with tempfile.TemporaryDirectory() as tmpdir:
        tmp_cert = Path(tmpdir) / "cert.json"
        tmp_cert.write_text(run.model_dump_json(indent=2), encoding="utf-8")
        ret = verify_certificate.main([str(tmp_cert)])
        assert ret == 0


# --- Section 9: Auxiliary Math & Quantum Lattice Modules ---

def test_replica_and_retraction_geometry():
    """Verify replica_hierarchy, retraction_geometry, and transfer modules."""
    edges = ("e1", "e2")
    pt = {"e1": (Rational(1),), "e2": (Rational(2),)}
    lp_val = replica_hierarchy.lp_counterexample_diagnostic(edges, pt)
    assert lp_val > 0

    scaled_eval = replica_hierarchy.scaled_sum_counterexample(Rational(2))
    assert scaled_eval(edges, pt) > 0

    aff_inst = retraction_geometry.affine_nonlinearity_instance()
    assert aff_inst.derivative_is_nonconstant is True

    chart_transfer = retraction_geometry.chart_transfer_witness()
    assert chart_transfer.positive_db_nonconstant is True
    assert chart_transfer.positive_derivative_matches_tangent_restriction is True
    assert chart_transfer.positive_curvature_nonzero is True
    assert chart_transfer.negative_chart_derivative_constant is True
    assert chart_transfer.negative_b_is_affine is True
    assert chart_transfer.negative_ambient_derivative_nonconstant is True
    assert chart_transfer.negative_curvature_nonzero is True
    assert chart_transfer.tangent_restriction_necessary is True
    assert chart_transfer.retractions_are_idempotent is True

    vertical_graph = retraction_geometry.vertical_graph_chart_witness()
    assert vertical_graph.cancellation_db_constant is True
    assert vertical_graph.cancellation_identity_matches is True
    assert vertical_graph.noncancellation_db_matches_formula is True
    assert vertical_graph.noncancellation_values_distinct is True
    assert vertical_graph.noncancellation_difference_matches is True
    assert vertical_graph.dissipative_identity is True
    assert vertical_graph.retraction_is_idempotent is True

    shear = retraction_geometry.sheared_graph_chart_witness()
    assert shear.chart_field_matches_shear_formula is True
    assert shear.db_matches_derivative_formula is True
    assert shear.db_values_distinct is True
    assert shear.vertical_db_constant is True
    assert shear.retraction_moves_chart_coordinate is True
    assert exact_equal(shear.off_graph_chart, Matrix([[Rational(3)]]))
    assert exact_equal(shear.off_graph_image, Matrix([[Rational(-1)]]))
    assert not exact_equal(shear.off_graph_chart, shear.off_graph_image)
    assert shear.dissipative_identity is True
    assert shear.retraction_is_idempotent is True

    semi_inst = retraction_geometry.semigroup_defect_instance()
    assert semi_inst.is_nonzero is True

    trans_cert = transfer.linear_projection_transfer_certificate(
        rho=(1, 2),
        sigma=(1, 0),
        projection=Matrix([[1, 0], [0, 0]]),
        lipschitz_constant=Rational(1, 2),
    )
    assert trans_cert.verify()


def test_quantum_lattice_operators_and_states():
    """Verify quantum lattice construction, normal rates, and edge evolution."""
    lat = worked_examples.two_qubit_xx_lattice()
    assert lat.site_order == ("a", "b")
    assert lat.full_incident_norm_g > 0

    replay_norm = lat.normal_rate_replay(("a", "b"))
    assert replay_norm.nu_e >= 0.0