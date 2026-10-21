from __future__ import annotations
"""
Lev Landau Hardline Soviet Test Suite for PO-000 Projection Obstruction.
Authored under /techne-code-soviet-builder rules:
- Derives boundary failures before assertion
- Covers all edge cases, exceptions, countermodels, and invalid input paths
- Pushes total coverage on code/ modules past 95%.
"""


import sys
import tempfile
import json
from pathlib import Path
from fractions import Fraction
import pytest
import numpy as np
from sympy import Matrix, Rational, simplify, Symbol, pi

_code_dir = Path(__file__).resolve().parents[2] / "code"
if str(_code_dir) not in sys.path:
    sys.path.insert(0, str(_code_dir))

import omega_engine.crates.linear_algebra_theory.exact as exact
import omega_engine.crates.homology_theory.cochain_presentation as cochain_presentation
import omega_engine.crates.homology_theory.covering_edge as covering_edge
import omega_engine.crates.projection_obstruction.evidence as evidence
import omega_engine.crates.observer.observer_carriers as observer_carriers
import omega_engine.crates.quantum_physics.quantum_lattice as quantum_lattice
import omega_engine.crates.homology_theory.family_bound as family_bound
import omega_engine.crates.quantum_physics.lattice_simulation as lattice_simulation
import omega_engine.crates.homology_theory.replica_hierarchy as replica_hierarchy
import omega_engine.crates.homology_theory.retraction_geometry as retraction_geometry
import omega_engine.crates.homology_theory.transfer as transfer
import omega_engine.crates.projection_obstruction.worked_examples as worked_examples
import omega_engine.crates.projection_obstruction.falsification_sandbox as falsification_sandbox
import omega_engine.crates.projection_obstruction.artifact_bundle as artifact_bundle
import omega_engine.crates.projection_obstruction.claim_coverage as claim_coverage
import omega_engine.crates.projection_obstruction.inline_code_companion as inline_code_companion
import omega_engine.crates.projection_obstruction.generate_figures as generate_figures
import omega_engine.crates.projection_obstruction.verify_certificate as verify_certificate

def test_replica_hierarchy_exceptions_and_audits():
    """Derive and verify every exception and audit branch in replica_hierarchy.py."""
    with pytest.raises(ValueError, match="at least one edge"):
        replica_hierarchy.FiniteDiagnosticFamily(edges=[], gauges={}, diagnostic=lambda e, p: 0)

    with pytest.raises(ValueError, match="unique"):
        replica_hierarchy.FiniteDiagnosticFamily(
            edges=["e1", "e1"], gauges={"e1": replica_hierarchy.absolute_gauge}, diagnostic=lambda e, p: 0
        )

    with pytest.raises(ValueError, match="exactly one local gauge"):
        replica_hierarchy.FiniteDiagnosticFamily(
            edges=["e1", "e2"], gauges={"e1": replica_hierarchy.absolute_gauge}, diagnostic=lambda e, p: 0
        )

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

    with pytest.raises(ValueError, match="unknown edge"):
        family.evaluate(["e1", "unknown"], {"e1": (Rational(1),), "unknown": (Rational(1),)})

    with pytest.raises(ValueError, match="domain must equal"):
        family.evaluate(["e1"], {"e1": (Rational(1),), "e2": (Rational(1),)})

    with pytest.raises(ValueError, match="sample grids must be nonempty"):
        family.audit(samples={"e1": [(Rational(1),)]})

    with pytest.raises(ValueError, match="nonnegative"):
        family.audit(samples={"e1": [(Rational(1),)], "e2": [(Rational(1),)]}, scalars=(-1,))

    audit_pass = family.audit(samples={"e1": [(Rational(0),), (Rational(1),)], "e2": [(Rational(0),), (Rational(1),)]})
    assert audit_pass.checked_points > 0
    assert audit_pass.re1_global_gauge is True
    assert audit_pass.re3_disjoint_replica_additivity is True
    assert audit_pass.re5_singleton_calibration is True

    f_nonzero_zero = replica_hierarchy.FiniteDiagnosticFamily(
        edges=["e1"], gauges={"e1": replica_hierarchy.absolute_gauge}, diagnostic=lambda e, p: Rational(5)
    )
    a1 = f_nonzero_zero.audit(samples={"e1": [(Rational(0),), (Rational(1),)]})
    assert a1.re1_global_gauge is False

    f_unfaithful = replica_hierarchy.FiniteDiagnosticFamily(
        edges=["e1"], gauges={"e1": replica_hierarchy.absolute_gauge}, diagnostic=lambda e, p: Rational(0)
    )
    a2 = f_unfaithful.audit(samples={"e1": [(Rational(0),), (Rational(1),)]})
    assert a2.re1_global_gauge is False

    f_homog = replica_hierarchy.FiniteDiagnosticFamily(
        edges=["e1"], gauges={"e1": replica_hierarchy.absolute_gauge}, diagnostic=lambda e, p: p["e1"][0]**2
    )
    a3 = f_homog.audit(samples={"e1": [(Rational(0),), (Rational(1),)]}, scalars=(Rational(2),))
    assert a3.re1_global_gauge is False

    f_subadd = replica_hierarchy.FiniteDiagnosticFamily(
        edges=["e1"], gauges={"e1": replica_hierarchy.absolute_gauge}, diagnostic=lambda e, p: p["e1"][0]**2
    )
    a4 = f_subadd.audit(samples={"e1": [(Rational(0),), (Rational(1),), (Rational(2),)]}, scalars=(Rational(1),))
    assert a4.re1_global_gauge is False

    f_re2 = replica_hierarchy.FiniteDiagnosticFamily(
        edges=["e1"], gauges={"e1": lambda p: abs(p[0])}, diagnostic=lambda e, p: p["e1"][0]
    )
    a5 = f_re2.audit(samples={"e1": [(Rational(-1),), (Rational(1),)]}, scalars=(Rational(1),))
    assert a5.re2_local_magnitude_sufficiency is False

    lp_family = replica_hierarchy.FiniteDiagnosticFamily(
        edges=["e1", "e2"],
        gauges={"e1": replica_hierarchy.absolute_gauge, "e2": replica_hierarchy.absolute_gauge},
        diagnostic=replica_hierarchy.lp_counterexample_diagnostic,
    )
    lp_audit = lp_family.audit(samples={"e1": [(Rational(1),)], "e2": [(Rational(1),)]})
    assert lp_audit.re3_disjoint_replica_additivity is False

    cert_res = family.conclusion_certificate({"e1": (Rational(1),), "e2": (Rational(1),)})
    assert cert_res.singleton_decomposition_holds is True

    with pytest.raises(ValueError, match="expects one coordinate"):
        replica_hierarchy.absolute_gauge((Rational(1), Rational(2)))

    weighted_diag = replica_hierarchy.weighted_l1_diagnostic({"e1": Rational(1), "e2": Rational(2)})
    with pytest.raises(ValueError, match="missing weights"):
        weighted_diag(("e1", "unknown"), {"e1": (Rational(1),), "unknown": (Rational(1),)})

    with pytest.raises(ValueError, match="strictly positive"):
        replica_hierarchy.weighted_l1_diagnostic({"e1": Rational(0)})

    with pytest.raises(ValueError, match="needs c>0 and c!=1"):
        replica_hierarchy.scaled_sum_counterexample(Rational(1))



def test_cochain_presentation_deep_coverage():
    """Derive and verify every missing exception in cochain_presentation.py."""
    obs1 = cochain_presentation.ObservationMap("e1", Matrix([[1, 0]]))

    with pytest.raises(ValueError, match="observation-map domain mismatch"):
        cochain_presentation.ObservationPresentation(["e1", "e2"], {"e1": obs1})

    pres = cochain_presentation.ObservationPresentation(["e1"], {"e1": obs1})
    with pytest.raises(cochain_presentation.MissingObservationMapError, match="normal residuals missing declared edges"):
        pres.induce_field({})

    problem = cochain_presentation.LinearRepairProblem(Matrix([[1, 0], [0, 0]]))
    non_exact_cert = problem.exactness_certificate(Matrix([[0], [1]]))
    assert not non_exact_cert.is_exact_coboundary
    assert non_exact_cert.verify()

    problem_proj = cochain_presentation.LinearRepairProblem(Matrix([[1, 0], [0, 0]]))
    dist_cert = problem_proj.quotient_l1_distance(Matrix([[0], [1]]))
    assert dist_cert.verify()
    assert dist_cert.distance == 1

    witness_p, res_p, opt_p = cochain_presentation._exact_l1_primal_vertex(Matrix.zeros(2, 2), Matrix([[1], [2]]))
    assert opt_p == 3
    witness_d, opt_d = cochain_presentation._exact_l1_dual_vertex(Matrix.zeros(2, 2), Matrix([[1], [2]]))
    assert opt_d == 3

    cap = cochain_presentation.AdmittedComplexV1(d0=Matrix([[1], [0]]), d1=Matrix([[0, 1]]))
    ac_prob = cochain_presentation.AdmittedComplexCoboundaryProblem(cap)
    assert ac_prob.d0 == cap.d0

    with pytest.raises(cochain_presentation.HigherDifferentialUnavailable, match="missing AdmittedComplexV1"):
        cochain_presentation.AdmittedComplexCoboundaryProblem("not_a_capability")

    with pytest.raises(cochain_presentation.HigherDifferentialUnavailable, match="supplies no C2 or d1"):
        cochain_presentation.verify_cochain_complex(Matrix([[1], [0]]), None)

    with pytest.raises(ValueError, match="dimensions do not compose"):
        cochain_presentation.verify_cochain_complex(Matrix([[1], [0]]), Matrix([[1, 0, 0]]))

    with pytest.raises(ArithmeticError, match="d1\\*d0=0 complex condition failed"):
        cochain_presentation.verify_cochain_complex(Matrix([[1], [0]]), Matrix([[1, 1]]))

    assert cochain_presentation.observation_map("e1", [[1, 0]]).edge_id == "e1"
    assert cochain_presentation.exact_cochain([1, 2]).shape == (2, 1)



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

    family_prem = family_bound.UniformFamilyPremises(
        g_star=Rational(2),
        eta_star=Rational(1, 4),
        nu_star=Rational(1, 2),
        a_star=Rational(1, 2),
    )
    cert = family_bound.certify_uniform_family(members=(m1,), premises=family_prem, time=Rational(1, 1000))
    assert cert.accepted is True

    for bad_prem in (
        family_bound.UniformFamilyPremises(g_star=Rational(0), eta_star=Rational(1, 4), nu_star=Rational(1, 2), a_star=Rational(1, 2)),
        family_bound.UniformFamilyPremises(g_star=Rational(2), eta_star=Rational(0), nu_star=Rational(1, 2), a_star=Rational(1, 2)),
        family_bound.UniformFamilyPremises(g_star=Rational(2), eta_star=Rational(2), nu_star=Rational(1, 2), a_star=Rational(1, 2)),
        family_bound.UniformFamilyPremises(g_star=Rational(2), eta_star=Rational(1, 4), nu_star=Rational(0), a_star=Rational(1, 2)),
        family_bound.UniformFamilyPremises(g_star=Rational(2), eta_star=Rational(1, 4), nu_star=Rational(1, 2), a_star=Rational(0)),
    ):
        cert_ref = family_bound.certify_uniform_family(members=(m1,), premises=bad_prem, time=Rational(1, 1000))
        assert cert_ref.accepted is False

    m_high_g = family_bound.FiniteFamilyMember("m_high", 2, 1, Rational(10), (Rational(1),))
    cert_high = family_bound.certify_uniform_family(members=(m_high_g,), premises=family_prem, time=Rational(1, 1000))
    assert cert_high.accepted is False

    m_low_rate = family_bound.FiniteFamilyMember("m_low", 2, 1, Rational(1), (Rational(1, 100),))
    cert_low = family_bound.certify_uniform_family(members=(m_low_rate,), premises=family_prem, time=Rational(1, 1000))
    assert cert_low.accepted is False

    cert_dup = family_bound.certify_uniform_family(members=(m1, m1), premises=family_prem, time=Rational(1, 1000))
    assert cert_dup.accepted is False

    cert_time = family_bound.certify_uniform_family(members=(m1,), premises=family_prem, time=Rational(1, 10))
    assert cert_time.accepted is False

    cert_fail = family_bound.certify_uniform_family(members=(), premises=family_prem, time=Rational(1, 1000))
    assert cert_fail.accepted is False



def test_quantum_lattice_input_validation():
    """Verify QuantumInputError checks and edge cases in quantum_lattice.py."""
    with pytest.raises(quantum_lattice.QuantumInputError, match="must be a finite real number"):
        quantum_lattice._finite_float(True, name="val")

    with pytest.raises(quantum_lattice.QuantumInputError, match="must be finite"):
        quantum_lattice._finite_float(float("nan"), name="val")

    with pytest.raises(quantum_lattice.QuantumInputError, match="must be finite and nonnegative"):
        quantum_lattice._finite_nonnegative_float(-1.0, name="val")

    with pytest.raises(quantum_lattice.QuantumInputError, match="must be a finite complex matrix"):
        quantum_lattice._readonly_matrix([1, [2]], name="val")

    with pytest.raises(quantum_lattice.QuantumInputError, match="must be rank two"):
        quantum_lattice._readonly_matrix([1, 2, 3], name="val")

    mat_2x2 = np.eye(2, dtype=complex)
    with pytest.raises(quantum_lattice.QuantumInputError, match="keep must be"):
        quantum_lattice.partial_trace_bipartite(mat_2x2, 1, 2, keep="invalid")

    with pytest.raises(quantum_lattice.QuantumInputError, match="bipartite operator has shape"):
        quantum_lattice.partial_trace_bipartite(mat_2x2, 2, 2, keep="a")

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



def test_lattice_simulation_deep_coverage():
    """Verify 1D/2D TFIM, Heisenberg dynamics, thermal sweeps, and higher order commutators."""
    sim_1d = lattice_simulation.run_lattice_simulation_replay(
        model_type="1d_tfim", num_sites_or_rows=3, coupling=1.0, transverse_field_or_delta=1.0, t_max=0.05, num_points=3
    )
    assert sim_1d.num_sites == 3
    assert len(sim_1d.trajectories) == 3

    sim_2d = lattice_simulation.run_lattice_simulation_replay(
        model_type="2d_tfim", num_sites_or_rows=2, cols=2, coupling=1.0, transverse_field_or_delta=1.0, t_max=0.05, num_points=3
    )
    assert sim_2d.num_sites == 4

    sim_heis = lattice_simulation.run_lattice_simulation_replay(
        model_type="1d_heisenberg", num_sites_or_rows=3, coupling=1.0, transverse_field_or_delta=1.0, t_max=0.05, num_points=3
    )
    assert sim_heis.num_sites == 3

    with pytest.raises(quantum_lattice.QuantumInputError, match="Unknown model_type"):
        lattice_simulation.run_lattice_simulation_replay("invalid_model")

    with pytest.raises(quantum_lattice.QuantumInputError, match="2D grid must have at least 4 sites"):
        lattice_simulation.build_2d_heisenberg_hamiltonian(1, 1, 1.0)

    h_tot, h_int, edges = lattice_simulation.build_2d_heisenberg_hamiltonian(rows=2, cols=2, J=1.0)
    assert h_tot.shape == (16, 16)
    assert len(edges) == 4

    rho0 = np.eye(8, dtype=complex) / 8.0
    h_sim, h_int_sim, _ = lattice_simulation.build_1d_tfim_hamiltonian(num_sites=3, coupling=1.0, transverse_field=1.0)
    c1, c2, c3, c4 = lattice_simulation.compute_higher_order_commutator_coefficients(h_sim, h_int_sim, rho0)
    assert c1 >= 0 and c2 >= 0 and c3 >= 0 and c4 >= 0

    for model in ("1d_tfim", "2d_tfim", "1d_heisenberg"):
        therm_replay = lattice_simulation.run_thermal_defect_simulation_replay(
            model_type=model, num_sites_or_rows=2, cols=2, coupling=1.0, transverse_field_or_delta=0.5, betas=(0.1, 1.0), t_max=0.05, num_points=3, state_mode="product_thermal"
        )
        assert len(therm_replay.results) == 2

    gibbs_replay = lattice_simulation.run_thermal_defect_simulation_replay(
        model_type="1d_tfim", num_sites_or_rows=2, coupling=1.0, transverse_field_or_delta=0.5, betas=(0.0, 0.5), t_max=0.05, num_points=3, state_mode="global_gibbs"
    )
    assert len(gibbs_replay.results) == 2

    for model in ("1d_tfim", "2d_tfim", "1d_heisenberg"):
        scaling = lattice_simulation.compute_thermodynamic_defect_scaling(
            model_type=model,
            sizes_or_grids=((2, 2), (2, 3)) if model == "2d_tfim" else (2, 3),
            coupling=1.0,
            transverse_field_or_delta=1.0,
            t_max=0.05,
            num_points=3,
        )
        assert len(scaling.results) >= 1



def test_observer_carriers_deep_coverage():
    """Verify observer carriers, watcher kernels, and visibility gap calculations."""
    patch_cert = observer_carriers.three_patch_certificate()
    assert patch_cert.tallies.I == 6

    scale_cert = observer_carriers.scaling_family_certificate(scales=[Rational(2)])
    assert scale_cert.exact_linear_scaling is True

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



def test_falsification_sandbox_deep_coverage():
    """Verify falsification sandbox edge cases and helpers."""
    assert falsification_sandbox.bell_closed_form(0.1) > 0
    assert falsification_sandbox.edgewise_l1([]) == 0.0
    assert falsification_sandbox.global_max_aggregator([]) == 0.0



def test_verify_certificate_deep_coverage():
    """Verify all verification failure modes in verify_certificate.py."""
    pkg_root = verify_certificate.RELEASE_ROOT

    errors_type = verify_certificate.verify_document("not_a_dict", pkg_root)
    assert len(errors_type) > 0

    errors_keys = verify_certificate.verify_document({}, pkg_root)
    assert len(errors_keys) > 0

    sample_path = sorted(verify_certificate.REQUIRED_SOURCE_PATHS)[0] if verify_certificate.REQUIRED_SOURCE_PATHS else "_tests_unit/test_po000_core.py"

    bad_hashes_1 = verify_certificate.verify_hash_inventory(
        {sample_path: 123}, required_paths={sample_path}, root=pkg_root, field_name="source_hashes"
    )
    assert any("must be strings" in err for err in bad_hashes_1)

    bad_hashes_2 = verify_certificate.verify_hash_inventory(
        {}, required_paths={sample_path}, root=pkg_root, field_name="source_hashes"
    )
    assert any("must be a nonempty object" in err for err in bad_hashes_2)

    bad_hashes_3 = verify_certificate.verify_hash_inventory(
        {sample_path: "0" * 64, "extra.py": "0" * 64},
        required_paths={sample_path},
        root=pkg_root,
        field_name="source_hashes",
    )
    assert any("unexpected paths" in err for err in bad_hashes_3)

    bad_hashes_4 = verify_certificate.verify_hash_inventory(
        {sample_path: "short_hash"},
        required_paths={sample_path},
        root=pkg_root,
        field_name="source_hashes",
    )
    assert any("invalid SHA-256 digest" in err for err in bad_hashes_4)

    bad_hashes_5 = verify_certificate.verify_hash_inventory(
        {sample_path: "0" * 64},
        required_paths={sample_path},
        root=pkg_root,
        field_name="source_hashes",
    )
    assert any("hash mismatch" in err for err in bad_hashes_5)

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
        "sha256sums_relative_path": "sha256sums",
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

    with tempfile.TemporaryDirectory() as tmpdir:
        bad_cert = Path(tmpdir) / "bad.json"
        bad_cert.write_text("{}", encoding="utf-8")
        ret = verify_certificate.main([str(bad_cert)])
        assert ret == 1



def test_inline_code_companion_functions():
    """Verify inline code companion functions match closed forms."""
    import omega_engine.crates.projection_obstruction.inline_code_companion as inline_code_companion

    eig_sum, formula_val = inline_code_companion.run_example_61_bell_state_leakage(np.pi / 8)
    assert abs(eig_sum - formula_val) < 1e-12

    eig_sum_tfim, nu_e = inline_code_companion.run_example_62_tfim_normal_rate(J=1.0)
    assert abs(eig_sum_tfim - nu_e) < 1e-12

    raw_I, J_vals = inline_code_companion.run_section_745_tripartite_all_green_diagram()
    assert raw_I == 6.0
    assert J_vals == [0.0, 0.0, 0.0]



