"""
Lev Landau Hardline Soviet Test Suite for PO-000 Projection Obstruction.
Authored under /techne-code-soviet-builder rules:
- Derives boundary failures before assertion
- Covers all edge cases, exceptions, countermodels, and invalid input paths
- Pushes total coverage on code/ modules past 95%.
"""

from __future__ import annotations

import sys
import tempfile
from pathlib import Path
import pytest
import numpy as np

_code_dir = Path(__file__).resolve().parents[1]
if str(_code_dir) not in sys.path:
    sys.path.insert(0, str(_code_dir))

from exactsym import Matrix, Rational, pi

import cochain_presentation
import observer_carriers
import quantum_lattice
import family_bound
import replica_hierarchy
import retraction_geometry
import transfer
import falsification_sandbox
import inline_code_companion
import verify_certificate


# --- 1. Replica Hierarchy Soviet Inspection & Countermodels ---

def test_replica_hierarchy_exceptions_and_audits():
    """Derive and verify every exception and audit branch in replica_hierarchy.py."""
    # Exception: empty edges
    with pytest.raises(ValueError, match="at least one edge"):
        replica_hierarchy.FiniteDiagnosticFamily(edges=[], gauges={}, diagnostic=lambda e, p: 0)

    # Exception: duplicate edges
    with pytest.raises(ValueError, match="unique"):
        replica_hierarchy.FiniteDiagnosticFamily(
            edges=["e1", "e1"], gauges={"e1": replica_hierarchy.absolute_gauge}, diagnostic=lambda e, p: 0
        )

    # Exception: missing local gauge
    with pytest.raises(ValueError, match="exactly one local gauge"):
        replica_hierarchy.FiniteDiagnosticFamily(
            edges=["e1", "e2"], gauges={"e1": replica_hierarchy.absolute_gauge}, diagnostic=lambda e, p: 0
        )

    # Exception: edge_types mismatch
    with pytest.raises(ValueError, match="edge_types must cover"):
        replica_hierarchy.FiniteDiagnosticFamily(
            edges=["e1"],
            gauges={"e1": replica_hierarchy.absolute_gauge},
            diagnostic=lambda e, p: 0,
            edge_types={"other": "t1"},
        )

    family = replica_hierarchy.FiniteDiagnosticFamily(
        edges=["e1", "e2"],
        gauges={"e1": replica_hierarchy.absolute_gauge, "e2": replica_hierarchy.absolute_gauge},
        diagnostic=replica_hierarchy.unweighted_l1_diagnostic,
    )

    # Evaluate exceptions
    with pytest.raises(ValueError, match="unknown edge"):
        family.evaluate(["e1", "unknown"], {"e1": (Rational(1),), "unknown": (Rational(1),)})

    with pytest.raises(ValueError, match="domain must equal"):
        family.evaluate(["e1"], {"e1": (Rational(1),), "e2": (Rational(1),)})

    # Audit exceptions
    with pytest.raises(ValueError, match="sample grids must be nonempty"):
        family.audit(samples={"e1": [(Rational(1),)]})

    with pytest.raises(ValueError, match="nonnegative"):
        family.audit(samples={"e1": [(Rational(1),)], "e2": [(Rational(1),)]}, scalars=(-1,))

    # Audit clean PASS
    audit_pass = family.audit(samples={"e1": [(Rational(0),), (Rational(1),)], "e2": [(Rational(0),), (Rational(1),)]})
    assert audit_pass.checked_points > 0
    assert audit_pass.re1_global_gauge is True
    assert audit_pass.re3_disjoint_replica_additivity is True
    assert audit_pass.re5_singleton_calibration is True

    # Audit countermodels for RE1 violations:
    # 1. Non-zero value at zero
    f_nonzero_zero = replica_hierarchy.FiniteDiagnosticFamily(
        edges=["e1"], gauges={"e1": replica_hierarchy.absolute_gauge}, diagnostic=lambda e, p: Rational(5)
    )
    a1 = f_nonzero_zero.audit(samples={"e1": [(Rational(0),), (Rational(1),)]})
    assert a1.re1_global_gauge is False

    # 2. Faithfulness violation (zero at non-zero point)
    f_unfaithful = replica_hierarchy.FiniteDiagnosticFamily(
        edges=["e1"], gauges={"e1": replica_hierarchy.absolute_gauge}, diagnostic=lambda e, p: Rational(0)
    )
    a2 = f_unfaithful.audit(samples={"e1": [(Rational(0),), (Rational(1),)]})
    assert a2.re1_global_gauge is False

    # 3. Positive homogeneity violation J(c*x) != c*J(x)
    f_homog = replica_hierarchy.FiniteDiagnosticFamily(
        edges=["e1"], gauges={"e1": replica_hierarchy.absolute_gauge}, diagnostic=lambda e, p: p["e1"][0]**2
    )
    a3 = f_homog.audit(samples={"e1": [(Rational(0),), (Rational(1),)]}, scalars=(Rational(2),))
    assert a3.re1_global_gauge is False

    # 4. Subadditivity violation J(x+y) > J(x) + J(y)
    f_subadd = replica_hierarchy.FiniteDiagnosticFamily(
        edges=["e1"], gauges={"e1": replica_hierarchy.absolute_gauge}, diagnostic=lambda e, p: p["e1"][0]**2
    )
    a4 = f_subadd.audit(samples={"e1": [(Rational(0),), (Rational(1),), (Rational(2),)]}, scalars=(Rational(1),))
    assert a4.re1_global_gauge is False

    # 5. RE2 violation (equal magnitudes give different diagnostic values)
    f_re2 = replica_hierarchy.FiniteDiagnosticFamily(
        edges=["e1"], gauges={"e1": lambda p: abs(p[0])}, diagnostic=lambda e, p: p["e1"][0]
    )
    a5 = f_re2.audit(samples={"e1": [(Rational(-1),), (Rational(1),)]}, scalars=(Rational(1),))
    assert a5.re2_local_magnitude_sufficiency is False

    # Audit countermodel for lp (p=2)
    lp_family = replica_hierarchy.FiniteDiagnosticFamily(
        edges=["e1", "e2"],
        gauges={"e1": replica_hierarchy.absolute_gauge, "e2": replica_hierarchy.absolute_gauge},
        diagnostic=replica_hierarchy.lp_counterexample_diagnostic,
    )
    lp_audit = lp_family.audit(samples={"e1": [(Rational(1),)], "e2": [(Rational(1),)]})
    assert lp_audit.re3_disjoint_replica_additivity is False

    # Conclusion certificate check
    cert_res = family.conclusion_certificate({"e1": (Rational(1),), "e2": (Rational(1),)})
    assert cert_res.singleton_decomposition_holds is True

    # Helper exception checks
    with pytest.raises(ValueError, match="expects one coordinate"):
        replica_hierarchy.absolute_gauge((Rational(1), Rational(2)))

    weighted_diag = replica_hierarchy.weighted_l1_diagnostic({"e1": Rational(1), "e2": Rational(2)})
    with pytest.raises(ValueError, match="missing weights"):
        weighted_diag(("e1", "unknown"), {"e1": (Rational(1),), "unknown": (Rational(1),)})

    with pytest.raises(ValueError, match="strictly positive"):
        replica_hierarchy.weighted_l1_diagnostic({"e1": Rational(0)})

    with pytest.raises(ValueError, match="needs c>0 and c!=1"):
        replica_hierarchy.scaled_sum_counterexample(Rational(1))


# --- 2. Cochain Presentation & Linear Repair Soviet Inspection ---

def test_cochain_presentation_deep_coverage():
    """Derive and verify every missing exception in cochain_presentation.py."""
    obs1 = cochain_presentation.ObservationMap("e1", Matrix([[1, 0]]))
    
    # Missing observation map error
    with pytest.raises(ValueError, match="observation-map domain mismatch"):
        cochain_presentation.ObservationPresentation(["e1", "e2"], {"e1": obs1})

    pres = cochain_presentation.ObservationPresentation(["e1"], {"e1": obs1})
    with pytest.raises(cochain_presentation.MissingObservationMapError, match="normal residuals missing declared edges"):
        pres.induce_field({})

    # Non-exact cochain exactness check
    problem = cochain_presentation.LinearRepairProblem(Matrix([[1, 0], [0, 0]]))
    non_exact_cert = problem.exactness_certificate(Matrix([[0], [1]]))
    assert not non_exact_cert.is_exact_coboundary
    assert non_exact_cert.verify()

    # Non-zero quotient distance
    problem_proj = cochain_presentation.LinearRepairProblem(Matrix([[1, 0], [0, 0]]))
    dist_cert = problem_proj.quotient_l1_distance(Matrix([[0], [1]]))
    assert dist_cert.verify()
    assert dist_cert.distance == 1

    # Primal and dual rank 0 vertices
    witness_p, res_p, opt_p = cochain_presentation._exact_l1_primal_vertex(Matrix.zeros(2, 2), Matrix([[1], [2]]))
    assert opt_p == 3
    witness_d, opt_d = cochain_presentation._exact_l1_dual_vertex(Matrix.zeros(2, 2), Matrix([[1], [2]]))
    assert opt_d == 3

    # Admitted complex coboundary problem
    cap = cochain_presentation.AdmittedComplexV1(d0=Matrix([[1], [0]]), d1=Matrix([[0, 1]]))
    ac_prob = cochain_presentation.AdmittedComplexCoboundaryProblem(cap)
    assert ac_prob.d0 == cap.d0

    with pytest.raises(cochain_presentation.HigherDifferentialUnavailable, match="missing AdmittedComplexV1"):
        cochain_presentation.AdmittedComplexCoboundaryProblem("not_a_capability")

    # Complex verification error checks
    with pytest.raises(cochain_presentation.HigherDifferentialUnavailable, match="supplies no C2 or d1"):
        cochain_presentation.verify_cochain_complex(Matrix([[1], [0]]), None)

    with pytest.raises(ValueError, match="dimensions do not compose"):
        cochain_presentation.verify_cochain_complex(Matrix([[1], [0]]), Matrix([[1, 0, 0]]))

    with pytest.raises(ArithmeticError, match="d1\\*d0=0 complex condition failed"):
        cochain_presentation.verify_cochain_complex(Matrix([[1], [0]]), Matrix([[1, 1]]))

    assert cochain_presentation.observation_map("e1", [[1, 0]]).edge_id == "e1"
    assert cochain_presentation.exact_cochain([1, 2]).shape == (2, 1)


# --- 3. Family Bound & Uniform Scale Soviet Inspection ---

def test_family_bound_deep_coverage():
    """Verify uniform family member validation and edge load bounds."""
    m1 = family_bound.FiniteFamilyMember(
        system_id="m1",
        site_count=2,
        edge_count=1,
        local_interaction_norm=Rational(1),
        active_edge_rates=(Rational(1),),
    )
    assert m1.system_id == "m1"

    # Invalid members
    with pytest.raises(ValueError, match="system_id must be nonempty"):
        family_bound.FiniteFamilyMember("  ", 2, 1, Rational(1), (Rational(1),))

    with pytest.raises(ValueError, match="site_count must be a positive integer"):
        family_bound.FiniteFamilyMember("m_bad", 0, 1, Rational(1), (Rational(1),))

    with pytest.raises(ValueError, match="edge_count must be a positive integer"):
        family_bound.FiniteFamilyMember("m_bad1", 2, 0, Rational(1), (Rational(1),))

    with pytest.raises(ValueError, match="nonnegative"):
        family_bound.FiniteFamilyMember("m_bad2", 2, 1, Rational(-1), (Rational(1),))

    with pytest.raises(ValueError, match="active-edge count cannot exceed"):
        family_bound.FiniteFamilyMember("m_bad3", 2, 1, Rational(1), (Rational(1), Rational(2)))

    with pytest.raises(ValueError, match="nonnegative"):
        family_bound.FiniteFamilyMember("m_bad4", 2, 1, Rational(1), (Rational(-1),))

    # Uniform family premises with valid short-time window
    family_prem = family_bound.UniformFamilyPremises(
        g_star=Rational(2),
        eta_star=Rational(1, 4),
        nu_star=Rational(1, 2),
        a_star=Rational(1, 2),
    )
    cert = family_bound.certify_uniform_family(members=(m1,), premises=family_prem, time=Rational(1, 1000))
    assert cert.accepted is True

    # Failing family refusal reasons
    for bad_prem in (
        family_bound.UniformFamilyPremises(g_star=Rational(0), eta_star=Rational(1, 4), nu_star=Rational(1, 2), a_star=Rational(1, 2)),
        family_bound.UniformFamilyPremises(g_star=Rational(2), eta_star=Rational(0), nu_star=Rational(1, 2), a_star=Rational(1, 2)),
        family_bound.UniformFamilyPremises(g_star=Rational(2), eta_star=Rational(2), nu_star=Rational(1, 2), a_star=Rational(1, 2)),
        family_bound.UniformFamilyPremises(g_star=Rational(2), eta_star=Rational(1, 4), nu_star=Rational(0), a_star=Rational(1, 2)),
        family_bound.UniformFamilyPremises(g_star=Rational(2), eta_star=Rational(1, 4), nu_star=Rational(1, 2), a_star=Rational(0)),
    ):
        cert_ref = family_bound.certify_uniform_family(members=(m1,), premises=bad_prem, time=Rational(1, 1000))
        assert cert_ref.accepted is False

    # Member-based refusals
    m_high_g = family_bound.FiniteFamilyMember("m_high", 2, 1, Rational(10), (Rational(1),))
    cert_high = family_bound.certify_uniform_family(members=(m_high_g,), premises=family_prem, time=Rational(1, 1000))
    assert cert_high.accepted is False

    m_low_rate = family_bound.FiniteFamilyMember("m_low", 2, 1, Rational(1), (Rational(1, 100),))
    cert_low = family_bound.certify_uniform_family(members=(m_low_rate,), premises=family_prem, time=Rational(1, 1000))
    assert cert_low.accepted is False

    # Duplicate system ID refusal
    cert_dup = family_bound.certify_uniform_family(members=(m1, m1), premises=family_prem, time=Rational(1, 1000))
    assert cert_dup.accepted is False

    # Time outside uniform window refusal
    cert_time = family_bound.certify_uniform_family(members=(m1,), premises=family_prem, time=Rational(1, 10))
    assert cert_time.accepted is False

    # Failing family certification (empty family)
    cert_fail = family_bound.certify_uniform_family(members=(), premises=family_prem, time=Rational(1, 1000))
    assert cert_fail.accepted is False


# --- 4. Quantum Lattice & Input Validation Soviet Inspection ---

def test_quantum_lattice_input_validation():
    """Verify QuantumInputError checks and edge cases in quantum_lattice.py."""
    with pytest.raises(quantum_lattice.QuantumInputError, match="must be a finite real number"):
        quantum_lattice._finite_float(True, name="val")

    with pytest.raises(quantum_lattice.QuantumInputError, match="must be finite"):
        quantum_lattice._finite_float(float("nan"), name="val")

    with pytest.raises(quantum_lattice.QuantumInputError, match="must be finite and nonnegative"):
        quantum_lattice._finite_nonnegative_float(-1.0, name="val")

    # Readonly matrix validation
    with pytest.raises(quantum_lattice.QuantumInputError, match="must be a finite complex matrix"):
        quantum_lattice._readonly_matrix([1, [2]], name="val")

    with pytest.raises(quantum_lattice.QuantumInputError, match="must be rank two"):
        quantum_lattice._readonly_matrix([1, 2, 3], name="val")

    # Partial trace error checks
    mat_2x2 = np.eye(2, dtype=complex)
    with pytest.raises(quantum_lattice.QuantumInputError, match="keep must be"):
        quantum_lattice.partial_trace_bipartite(mat_2x2, 1, 2, keep="invalid")

    with pytest.raises(quantum_lattice.QuantumInputError, match="bipartite operator has shape"):
        quantum_lattice.partial_trace_bipartite(mat_2x2, 2, 2, keep="a")

    # Quantum lattice model validation checks
    term1 = quantum_lattice.LocalHamiltonianTerm("h1", ("u", "v"), np.eye(4, dtype=complex))
    state_u = np.eye(2, dtype=complex) / 2.0
    state_v = np.eye(2, dtype=complex) / 2.0

    with pytest.raises(quantum_lattice.QuantumInputError, match="must be strictly positive"):
        quantum_lattice.FiniteQuantumLattice(["u", "v"], {"u": 2, "v": 2}, (term1,), {"u": state_u, "v": state_v}, validation_atol=0.0)

    with pytest.raises(quantum_lattice.QuantumInputError, match="exceeds maximum host-enforced cap"):
        quantum_lattice.FiniteQuantumLattice(["u", "v"], {"u": 2, "v": 2}, (term1,), {"u": state_u, "v": state_v}, validation_atol=1.0e-3)

    with pytest.raises(quantum_lattice.QuantumInputError, match="site_order must contain nonempty site identifiers"):
        quantum_lattice.FiniteQuantumLattice([], {"u": 2}, (), {})

    with pytest.raises(quantum_lattice.QuantumInputError, match="site_order contains duplicates"):
        quantum_lattice.FiniteQuantumLattice(["u", "u"], {"u": 2}, (), {})

    with pytest.raises(quantum_lattice.QuantumInputError, match="dimensions must cover exactly site_order"):
        quantum_lattice.FiniteQuantumLattice(["u", "v"], {"u": 2}, (), {})

    with pytest.raises(quantum_lattice.QuantumInputError, match="dimension for 'u' must be a positive integer"):
        quantum_lattice.FiniteQuantumLattice(["u"], {"u": 0}, (), {})

    with pytest.raises(quantum_lattice.QuantumInputError, match="Hamiltonian term labels must be unique"):
        quantum_lattice.FiniteQuantumLattice(["u", "v"], {"u": 2, "v": 2}, (term1, term1), {"u": state_u, "v": state_v})

    term_bad_site = quantum_lattice.LocalHamiltonianTerm("h2", ("u", "unknown"), np.eye(4, dtype=complex))
    with pytest.raises(quantum_lattice.QuantumInputError, match="references unknown sites"):
        quantum_lattice.FiniteQuantumLattice(["u", "v"], {"u": 2, "v": 2}, (term_bad_site,), {"u": state_u, "v": state_v})

    # Method-level exception checks
    lattice = quantum_lattice.FiniteQuantumLattice(["u", "v"], {"u": 2, "v": 2}, (term1,), {"u": state_u, "v": state_v})
    with pytest.raises(quantum_lattice.QuantumInputError, match="an edge must contain two distinct sites"):
        lattice._canonical_edge(["u", "u"])

    with pytest.raises(quantum_lattice.QuantumInputError, match="edge references unknown sites"):
        lattice._canonical_edge(["u", "unknown"])

    with pytest.raises(quantum_lattice.QuantumInputError, match="operator support must be nonempty"):
        lattice.embed_operator(np.eye(2), [])

    with pytest.raises(quantum_lattice.QuantumInputError, match="operator support has unknown sites"):
        lattice.embed_operator(np.eye(2), ["unknown"])

    with pytest.raises(quantum_lattice.QuantumInputError, match="local operator has shape"):
        lattice.embed_operator(np.eye(2), ["u", "v"])

    with pytest.raises(quantum_lattice.QuantumInputError, match="term_labels contains duplicates"):
        lattice.hamiltonian(["h1", "h1"])

    with pytest.raises(quantum_lattice.QuantumInputError, match="unknown Hamiltonian term labels"):
        lattice.hamiltonian(["unknown"])

    with pytest.raises(quantum_lattice.QuantumInputError, match="keep_sites contains duplicates"):
        lattice.partial_trace(np.eye(4), ["u", "u"])

    with pytest.raises(quantum_lattice.QuantumInputError, match="keep_sites has unknown sites"):
        lattice.partial_trace(np.eye(4), ["unknown"])

    with pytest.raises(quantum_lattice.QuantumInputError, match="global operator has shape"):
        lattice.partial_trace(np.eye(2), ["u"])

    assert lattice.partial_trace(np.eye(4), []).shape == (1, 1)
    assert lattice.partial_trace(np.eye(4), ["v", "u"]).shape == (4, 4)


# --- 5. Lattice Simulation & Extended Trajectories Soviet Inspection ---

# 2026-09-03: test_lattice_simulation_deep_coverage removed with code/lattice_simulation.py.  The module mislabelled norms of nested global commutators as Taylor coefficients of the edgewise defect and never tested its own inequality inside t <= t0; it carried no claim.

# --- 6. Observer Carriers Deep Coverage ---

def test_observer_carriers_deep_coverage():
    """Verify observer carriers, watcher kernels, and visibility gap calculations."""
    patch_cert = observer_carriers.three_patch_certificate()
    assert patch_cert.tallies.I == 6

    scale_cert = observer_carriers.scaling_family_certificate(scales=[Rational(2)])
    assert scale_cert.exact_linear_scaling is True

    # Observer family exception checks
    with pytest.raises(ValueError, match="needs at least one edge"):
        observer_carriers.ObserverFamily({}, [])

    with pytest.raises(ValueError, match="edge dimensions must be positive integers"):
        observer_carriers.ObserverFamily({"e1": 0}, [])

    with pytest.raises(ValueError, match="must be nonempty"):
        observer_carriers.ObserverFamily({"e1": 2}, [])

    obs1 = observer_carriers.LocalObserverCarrier("w1", {"e1": Matrix([[1, 0]])})
    with pytest.raises(ValueError, match="observer identifiers must be unique"):
        observer_carriers.ObserverFamily({"e1": 2}, [obs1, obs1])

    obs_unknown = observer_carriers.LocalObserverCarrier("w2", {"unknown": Matrix([[1, 0]])})
    with pytest.raises(ValueError, match="references unknown edges"):
        observer_carriers.ObserverFamily({"e1": 2}, [obs_unknown])

    obs_bad_shape = observer_carriers.LocalObserverCarrier("w3", {"e1": Matrix([[1, 0, 0]])})
    with pytest.raises(ValueError, match="has shape"):
        observer_carriers.ObserverFamily({"e1": 2}, [obs_bad_shape])

    obs_non_contractive = observer_carriers.LocalObserverCarrier("w4", {"e1": Matrix([[2, 0]])})
    with pytest.raises(ValueError, match="is not l1-contractive"):
        observer_carriers.ObserverFamily({"e1": 2}, [obs_non_contractive])

    fam = observer_carriers.ObserverFamily({"e1": 2}, [obs1])
    with pytest.raises(ValueError, match="defect domain mismatch"):
        fam.normalize_defects({})

    with pytest.raises(ValueError, match="defect on 'e1' has shape"):
        fam.normalize_defects({"e1": [1, 2, 3]})


# --- 7. Projection Transfer & Reverse-Triangle Deep Coverage ---

def test_transfer_deep_coverage():
    """Verify reverse-triangle transfer certificate exception and refusal branches."""
    with pytest.raises(ValueError, match="must be a column vector"):
        transfer._exact_vector(Matrix([[1, 2]]), label="bad")

    with pytest.raises(ValueError, match="lipschitz_constant must be nonnegative"):
        transfer.reverse_triangle_certificate([1, 0], [0, 1], [1, 0], [0, 1], lipschitz_constant=-1)

    with pytest.raises(ValueError, match="all four vectors must have the same shape"):
        transfer.reverse_triangle_certificate([1, 0], [0, 1], [1, 0], [0, 1, 0], 1)

    ref_cert = transfer.reverse_triangle_certificate([1, 0], [0, 1], [2, 0], [0, 0], 0)
    assert ref_cert.accepted is False
    assert ref_cert.refusal == "pairwise_lipschitz_premise_failed"

    lin_cert = transfer.linear_projection_transfer_certificate([1, 0], [0, 1], Matrix([[1, 0], [0, 0]]), lipschitz_constant=1)
    assert lin_cert.accepted is True

    with pytest.raises(ValueError, match="projection has shape"):
        transfer.linear_projection_transfer_certificate([1, 0], [0, 1], Matrix([[1, 0]]), 1)

    with pytest.raises(ValueError, match="rho and sigma must have the same shape"):
        transfer.linear_projection_transfer_certificate([1, 0], [0, 1, 0], Matrix([[1, 0], [0, 1]]), 1)

    with pytest.raises(ValueError, match="projection matrix P is not idempotent"):
        transfer.linear_projection_transfer_certificate([1, 0], [0, 1], Matrix([[1, 1], [0, 2]]), 1)


# --- 8. Retraction Geometry Deep Coverage ---

def test_retraction_geometry_deep_coverage():
    """Verify retraction geometry exceptions and lifted affine charts."""
    with pytest.raises(ValueError, match="chart is defined only on M"):
        retraction_geometry.GraphRetraction.chart(Matrix([1, 0, 2]))

    with pytest.raises(ValueError, match="expected a 3x1 ambient point"):
        retraction_geometry.GraphRetraction.require_ambient_point(Matrix([1, 0]))

    with pytest.raises(ValueError, match="projected generator is evaluated only on M"):
        retraction_geometry.projected_generator_ambient(Matrix([1, 0, 2]))

    with pytest.raises(ValueError, match="generator must be 3x3"):
        retraction_geometry.projected_generator_ambient(Matrix([1, 0, 1]), generator=Matrix([[1, 0]]))

    with pytest.raises(ValueError, match="S_t is defined here on M"):
        retraction_geometry.projected_family(Matrix([1, 0, 2]), pi)


# --- 9. Falsification Sandbox Deep Coverage ---

def test_falsification_sandbox_deep_coverage():
    """Verify falsification sandbox edge cases and helpers."""
    assert falsification_sandbox.bell_closed_form(0.1) > 0
    assert falsification_sandbox.edgewise_l1([]) == 0.0
    assert falsification_sandbox.global_max_aggregator([]) == 0.0


# --- 10. Independent Verifier Deep Coverage ---

def test_verify_certificate_deep_coverage():
    """Verify all verification failure modes in verify_certificate.py."""
    pkg_root = Path(_code_dir).parent

    # Invalid document type
    errors_type = verify_certificate.verify_document("not_a_dict", pkg_root)
    assert len(errors_type) > 0

    # Missing required keys
    errors_keys = verify_certificate.verify_document({}, pkg_root)
    assert len(errors_keys) > 0

    # Source hashes validation errors
    bad_hashes_1 = verify_certificate.verify_hash_inventory(
        {"code/tests/test_po000_core.py": 123}, required_paths={"code/tests/test_po000_core.py"}, root=pkg_root, field_name="source_hashes"
    )
    assert any("must be strings" in err for err in bad_hashes_1)

    bad_hashes_2 = verify_certificate.verify_hash_inventory(
        {}, required_paths={"code/tests/test_po000_core.py"}, root=pkg_root, field_name="source_hashes"
    )
    assert any("must be a nonempty object" in err for err in bad_hashes_2)

    bad_hashes_3 = verify_certificate.verify_hash_inventory(
        {"code/tests/test_po000_core.py": "0" * 64, "extra.py": "0" * 64},
        required_paths={"code/tests/test_po000_core.py"},
        root=pkg_root,
        field_name="source_hashes",
    )
    assert any("unexpected paths" in err for err in bad_hashes_3)

    bad_hashes_4 = verify_certificate.verify_hash_inventory(
        {"code/tests/test_po000_core.py": "short_hash"},
        required_paths={"code/tests/test_po000_core.py"},
        root=pkg_root,
        field_name="source_hashes",
    )
    assert any("invalid SHA-256 digest" in err for err in bad_hashes_4)

    bad_hashes_5 = verify_certificate.verify_hash_inventory(
        {"code/tests/test_po000_core.py": "0" * 64},
        required_paths={"code/tests/test_po000_core.py"},
        root=pkg_root,
        field_name="source_hashes",
    )
    assert any("hash mismatch" in err for err in bad_hashes_5)

    # Document validation errors
    bad_doc_1 = {
        "schema_version": "wrong_version",
        "paper_version": "1.0",
        "python_package_version": "1.0",
        "paper_id": "WRONG",
        "authority_effect": "Full",
        "results": "not_a_list",
        "unresolved_claim_ids": "not_a_list",
    }
    errs1 = verify_certificate.verify_document(bad_doc_1, pkg_root)
    assert len(errs1) > 0

    bad_doc_2 = {
        "schema_version": "po000.mechanization_run.v3",
        "paper_version": "6.0",
        "python_package_version": "6.1.1",
        "paper_id": "PO-000",
        "authority_effect": "None",
        "mechanization_date": "2026-08-01",
        "sha256sums_relative_path": "SHA256SUMS",
        "source_hashes": {},
        "evidence_hashes": {},
        "results": [
            {
                "claim_ids": ["D2"],
                "evidence_kind": "exact_algebraic_recheck",
                "verdict": "fail",
                "title": "",
                "statement_scope": "scope",
                "algorithm": "alg",
                "witness": {},
                "limitations": [],
                "authority_effect": "None",
            }
        ],
        "unresolved_claim_ids": ["D2", "D2", "UNKNOWN_CLAIM"],
    }
    errs2 = verify_certificate.verify_document(bad_doc_2, pkg_root)
    assert any("unresolved_claim_ids contains duplicates" in err for err in errs2)
    assert any("records a failed executable check" in err for err in errs2)

    # CLI failure mode
    with tempfile.TemporaryDirectory() as tmpdir:
        bad_cert = Path(tmpdir) / "bad.json"
        bad_cert.write_text("{}", encoding="utf-8")
        ret = verify_certificate.main([str(bad_cert)])
        assert ret == 1


# --- 13. Inline Code Companion Execution Tests ---

def test_inline_code_companion_functions():
    """Verify inline code companion functions match closed forms."""

    eig_sum, formula_val = inline_code_companion.run_example_61_bell_state_leakage(np.pi / 8)
    assert abs(eig_sum - formula_val) < 1e-12

    eig_sum_tfim, nu_e = inline_code_companion.run_example_62_tfim_normal_rate(J=1.0)
    assert abs(eig_sum_tfim - nu_e) < 1e-12

    raw_I, J_vals = inline_code_companion.run_section_745_tripartite_all_green_diagram()
    assert raw_I == 6.0
    assert J_vals == [0.0, 0.0, 0.0]


def test_cochain_and_quantum_lattice_additional_coverage():
    """Exercise additional branches in cochain_presentation and quantum_lattice."""
    import cochain_presentation
    import quantum_lattice
    import pytest
    from exactsym import Matrix

    # quantum_lattice validation
    with pytest.raises(quantum_lattice.QuantumInputError):
        quantum_lattice._finite_nonnegative_float(-1.0, name="t")

    with pytest.raises(quantum_lattice.QuantumInputError):
        quantum_lattice._finite_nonnegative_float("invalid", name="t")

    # cochain_presentation exceptions & methods
    obs_map = cochain_presentation.ObservationMap("e1", Matrix([[1, 0]]))
    with pytest.raises(ValueError):
        obs_map.observe(Matrix([1, 2, 3]))

    # ObservationPresentation validation
    with pytest.raises(ValueError):
        cochain_presentation.ObservationPresentation([], {})

    with pytest.raises(ValueError):
        cochain_presentation.ObservationPresentation(["e1", "e1"], {"e1": obs_map})

    with pytest.raises(ValueError):
        cochain_presentation.ObservationPresentation(["e1"], {"e1": obs_map, "e2": obs_map})

    # AdmittedComplexV1 invalid composition
    d0 = Matrix([[1], [1]])
    d1_bad = Matrix([[1, 1]])
    with pytest.raises(ValueError):
        cochain_presentation.AdmittedComplexV1(d0, d1_bad)


def test_replica_hierarchy_branch_coverage():
    """Exercise failure branches in replica_hierarchy."""
    import replica_hierarchy
    from exactsym import Abs

    # Non-gauge diagnostic (violates RE1)
    bad_diag = replica_hierarchy.FiniteDiagnosticFamily(
        edges=("e1", "e2"),
        edge_types={"e1": "t1", "e2": "t1"},
        gauges={"e1": lambda v: Abs(v[0]), "e2": lambda v: Abs(v[0])},
        diagnostic=lambda edges, pt: -1 if any(v[0] < 0 for v in pt.values()) else sum(Abs(pt[e][0]) for e in edges),
    )
    samples = {"e1": [(1,), (-1,)], "e2": [(1,), (-1,)]}
    audit = bad_diag.audit(samples)
    assert not audit.re1_global_gauge
    assert len(audit.counterexamples) > 0


def test_verify_certificate_coverage(tmp_path):
    """Exercise verify_certificate validation and main execution paths."""
    import verify_certificate

    # Test main with missing/invalid file
    non_existent = tmp_path / "missing.json"
    res = verify_certificate.main([str(non_existent)])
    assert res == 1

    # Test verify_document with invalid top-level object
    errs = verify_certificate.verify_document("not_a_dict", tmp_path)
    assert "top-level JSON value must be an object" in errs[0]

    # Test verify_document missing top-level fields
    errs = verify_certificate.verify_document({}, tmp_path)
    assert len(errs) > 0

    # Test verify_hash_inventory missing/extra fields
    errs_hashes = verify_certificate.verify_hash_inventory(
        {"missing_key": "abc"},
        required_paths={"required_key"},
        root=tmp_path,
        field_name="test_hashes",
    )
    assert len(errs_hashes) > 0

    # Test verify_document with invalid paper version and non-list results
    bad_data = {
        "schema_version": "1.0",
        "paper_version": "1.0",
        "python_package_version": "1.0.0",
        "paper_id": "WRONG-ID",
        "authority_effect": "WRONG",
        "results": ["not_a_dict"],
        "unresolved_claim_ids": ["DUPLICATE", "DUPLICATE", "UNKNOWN_CLAIM"],
        "refusals_present": True,
        "open_obligations_present": False,
        "claim_disposition_complete": False,
        "promotion_eligible": True,
    }
    errs_bad = verify_certificate.verify_document(bad_data, tmp_path)
    assert len(errs_bad) > 5
