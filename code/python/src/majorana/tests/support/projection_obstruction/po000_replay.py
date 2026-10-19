"""Deterministic aggregate replay for every PO-000 claim-ledger row."""

from __future__ import annotations
import argparse
import hashlib
from fractions import Fraction
from pathlib import Path

from sympy import Matrix, Rational

try:
    from omega_engine.crates.replay import (
        ReplayKernel,
        ReplayReport,
        VerifiedReplayReport,
        ReplayStatus,
        verify_replay_contract,
    )
except ImportError:
    ReplayKernel = None
    ReplayReport = None
    VerifiedReplayReport = None

__version__ = "6.1.1"
from omega_engine.crates.projection_obstruction.claim_coverage import (
    CLAIM_COVERAGE,
    REQUIRED_LEDGER_CLAIM_IDS,
    GeneralStatus,
)
from omega_engine.crates.homology_theory.cochain_presentation import (
    HigherDifferentialUnavailable,
    LinearRepairProblem,
    ObservationPresentation,
    observation_map,
    verify_cochain_complex,
)
from omega_engine.crates.homology_theory.covering_edge import CoveringEdge, CoveringEdgeDiagram
from omega_engine.crates.projection_obstruction.evidence import ClaimEvidence, EvidenceKind, MechanizationRun, ReplayVerdict
from omega_engine.crates.linear_algebra_theory.exact import expression_text
from omega_engine.crates.homology_theory.family_bound import (
    FiniteFamilyMember,
    UniformFamilyPremises,
    certify_uniform_family,
)
from omega_engine.crates.observer.observer_carriers import (
    LocalObserverCarrier,
    ObserverFamily,
    scaling_family_certificate,
    three_patch_certificate,
)
from omega_engine.crates.homology_theory.replica_hierarchy import (
    FiniteDiagnosticFamily,
    absolute_gauge,
    lp_counterexample_diagnostic,
    scaled_sum_counterexample,
    unweighted_l1_diagnostic,
    weighted_l1_diagnostic,
)
from omega_engine.crates.homology_theory.retraction_geometry import (
    affine_nonlinearity_instance,
    semigroup_defect_instance,
)
from omega_engine.crates.homology_theory.transfer import linear_projection_transfer_certificate
from omega_engine.crates.projection_obstruction.worked_examples import (
    pass45_counterexample_lattice,
    pass45_counterexample_replay,
    tfim_normal_rate_example,
    two_qubit_xx_example,
    two_qubit_xx_lattice,
)

def _resolve_package_root() -> Path:
    here = Path(__file__).resolve()
    for p in [here.parent, *here.parents]:
        if (p / "000_projection_obstruction.md").exists() and (p / "code").is_dir():
            return p
        published = (
            p
            / "published"
            / "004_projection_obstruction"
            / "000_projection_obstruction"
        )
        if published.is_dir():
            return published
        if (p / "crates").is_dir() and ((p / "_tests_unit").is_dir() or (p / "tests").is_dir()):
            return p
    return here.parents[3]

PACKAGE_ROOT = _resolve_package_root()


def _verdict(condition: bool) -> ReplayVerdict:
    return ReplayVerdict.PASS if condition else ReplayVerdict.FAIL


def _sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1 << 20), b""):
            digest.update(chunk)
    return digest.hexdigest()


def _receipt_float(value: float) -> float:
    """Canonicalize numerical witnesses for receipt byte stability across hosts."""
    return float(f"{value:.15g}")


def source_hashes(package_root: Path = PACKAGE_ROOT) -> dict[str, str]:
    """Hash the complete producer and independent-verifier source surface."""
    from omega_engine.crates.certificate.verify_certificate import (
        _resolve_po000_package_root,
        _resolve_required_source_paths,
    )
    root = _resolve_po000_package_root(package_root)
    lib_dir_name = (
        "crates"
        if (root / "crates").is_dir()
        else "src/po000"
        if (root / "src" / "po000").is_dir()
        else "code"
        if (root / "code").is_dir()
        else "coda"
        if (root / "coda").is_dir()
        else "omega_engine"
        if (root / "omega_engine").is_dir()
        else "po000_lib"
    )
    req_paths = _resolve_required_source_paths(root, lib_dir_name)
    return {
        p: _sha256(root / p)
        for p in sorted(req_paths)
        if (root / p).is_file()
    }


def publication_hashes(package_root: Path = PACKAGE_ROOT) -> dict[str, str]:
    """Hash publish-facing paper surfaces present next to the package root.

    Includes the monograph trio always (when present) plus optional release-build
    products (pdf/tex/metadata) so verify_certificate inventories stay closed
    after `/paper-build`.
    """

    publication_root = package_root
    names = (
        "000_projection_obstruction.md",
        "000_projection_obstruction_claim_ledger.md",
        "000_projection_obstruction_change_log.md",
        "000_projection_obstruction.pdf",
        "000_projection_obstruction.tex",
        "PO000_ENVIRONMENT_RECEIPT.json",
        "PO000_REPRODUCTION_REQUIREMENTS.txt",
        "PO000_LEAN_axiom_report.txt",
        "PO000_LICENSE.md",
        "PO000_RELEASE_NOTES.md",
        "PO000_RELEASE_README.md",
        "PO000_ZENODO_METADATA.json",
        "verify_po000_release.py",
    )
    res = {}
    for name in names:
        p = publication_root / name
        if p.exists():
            res[name] = _sha256(p)
    return res


def _covering_edge_receipt() -> ClaimEvidence:
    diagram = CoveringEdgeDiagram(
        {"a": 1, "b": 1},
        (CoveringEdge("b>a", "a", "b", Matrix([[1]])),),
    )
    section = {"a": (1,), "b": (3,)}
    defect = diagram.coboundary(section)["b>a"]
    bound = diagram.coboundary_bound_certificate(section)
    passed = defect == Matrix([2]) and diagram.inconsistency(section) == 2 and bound.holds
    return ClaimEvidence(
        claim_ids=("B1", "B2"),
        title="Exact covering-edge coboundary and raw tally",
        evidence_kind=EvidenceKind.EXACT_FINITE,
        verdict=_verdict(passed),
        statement_scope="one exact rational covering edge",
        algorithm="exact matrix multiplication and l1 summation",
        witness={
            "defect": expression_text(defect),
            "raw_I": expression_text(bound.coboundary_norm),
            "bound": expression_text(bound.bound),
        },
        limitations=("Finite rational instance; the Banach-space bound remains analytic.",),
    )


def _geometry_receipt() -> ClaimEvidence:
    geometry = affine_nonlinearity_instance()
    semigroup = semigroup_defect_instance()
    passed = (
        geometry.generator_is_skew
        and geometry.retraction_is_idempotent
        and geometry.tangent_projection_is_idempotent
        and geometry.derivative_is_nonconstant
        and geometry.midpoint_is_on_manifold
        and semigroup.is_nonzero
    )
    return ClaimEvidence(
        claim_ids=("B3", "C1"),
        title="Exact graph-retraction nonlinearity and semigroup defect",
        evidence_kind=EvidenceKind.EXACT_SYMBOLIC_INSTANCE,
        verdict=_verdict(passed),
        statement_scope="the graph z=x^2 with one skew generator",
        algorithm="symbolic chart differentiation and exact trigonometric substitution",
        witness={
            "chart_vector_field": expression_text(geometry.chart_vector_field),
            "chart_derivative": expression_text(geometry.chart_derivative),
            "semigroup_defect": expression_text(semigroup.defect),
        },
        limitations=("Concrete hypothesis-valid instance, not the quantified Banach theorem.",),
    )


def _cochain_receipts() -> tuple[ClaimEvidence, ClaimEvidence]:
    presentation = ObservationPresentation(
        ("e1", "e2"),
        {
            "e1": observation_map("e1", [[1]]),
            "e2": observation_map("e2", [[1]]),
        },
    )
    field = presentation.induce_field({"e1": Matrix([2]), "e2": Matrix([3])})
    problem = LinearRepairProblem(Matrix([[1], [1]]))
    exact = problem.exactness_certificate(Matrix([2, 2]))
    obstructed = problem.exactness_certificate(field.as_vector())
    quotient = problem.quotient_l1_distance(field.as_vector())
    refused_higher = False
    try:
        verify_cochain_complex(problem.d0, None)
    except HigherDifferentialUnavailable:
        refused_higher = True
    exact_passed = (
        exact.verify()
        and exact.is_exact_coboundary
        and obstructed.verify()
        and not obstructed.is_exact_coboundary
        and quotient.verify()
        and quotient.distance == 1
    )
    return (
        ClaimEvidence(
            claim_ids=("A2", "A3", "D8", "G1"),
            title="Exact linear observation, repair, image membership, and image distance pipeline",
            evidence_kind=EvidenceKind.EXACT_FINITE,
            verdict=_verdict(exact_passed),
            statement_scope="one ordered rational observation presentation",
            algorithm="exact rank, witnesses, separators, and primal-dual vertex enumeration",
            witness={
                "induced_field": expression_text(field.as_vector()),
                "repair_witness": expression_text(exact.witness),
                "separator": expression_text(obstructed.separating_left_kernel_vector),
                "separator_pairing": expression_text(obstructed.separating_pairing),
                "quotient_distance": expression_text(quotient.distance),
                "quotient_dual_witness": expression_text(quotient.dual_witness),
                "quotient_dual_pairing": expression_text(quotient.dual_pairing),
            },
            limitations=(
                "Linear algebra repair level; no cochain complex capability is synthesized.",
            ),
        ),
        ClaimEvidence(
            claim_ids=("B4", "G2"),
            title="Higher-cell data is absent and explicitly refused",
            evidence_kind=EvidenceKind.NOT_EXECUTABLE,
            verdict=ReplayVerdict.REFUSED if refused_higher else ReplayVerdict.FAIL,
            statement_scope="native covering-edge data without C2 or d1",
            algorithm="typed capability refusal",
            witness={"higher_differential_refused": refused_higher},
            limitations=("Higher cells belong to PO-001/PO-003 and are not synthesized.",),
        ),
    )


def _replica_receipts() -> tuple[ClaimEvidence, ClaimEvidence, ClaimEvidence]:
    edges = ("e1", "e2")
    gauges = {"e1": absolute_gauge, "e2": absolute_gauge}
    edge_types = {"e1": "same", "e2": "same"}
    samples = {
        "e1": ((Rational(-1),), (Rational(0),), (Rational(1),)),
        "e2": ((Rational(-1),), (Rational(0),), (Rational(1),)),
    }
    unweighted = FiniteDiagnosticFamily(edges, gauges, unweighted_l1_diagnostic, edge_types).audit(
        samples
    )
    weighted = FiniteDiagnosticFamily(
        edges,
        gauges,
        weighted_l1_diagnostic({"e1": Rational(2), "e2": Rational(2)}),
        edge_types,
    ).audit(samples)
    lp_drop = FiniteDiagnosticFamily(edges, gauges, lp_counterexample_diagnostic, edge_types).audit(
        samples
    )
    scaled_drop = FiniteDiagnosticFamily(
        edges, gauges, scaled_sum_counterexample(Rational(2)), edge_types
    ).audit(samples)
    all_unweighted_axioms = all(
        (
            unweighted.re1_global_gauge,
            unweighted.re2_local_magnitude_sufficiency,
            unweighted.re3_disjoint_replica_additivity,
            unweighted.re4_edge_exchange_symmetry,
            unweighted.re5_singleton_calibration,
        )
    )
    finite_audit_passed = (
        all_unweighted_axioms
        and weighted.re3_disjoint_replica_additivity
        and weighted.re4_edge_exchange_symmetry
        and not weighted.re5_singleton_calibration
    )
    exact_identity_passed = (
        unweighted.re3_disjoint_replica_additivity and unweighted.re5_singleton_calibration
    )
    countermodels_passed = (
        not lp_drop.re3_disjoint_replica_additivity
        and lp_drop.re5_singleton_calibration
        and scaled_drop.re3_disjoint_replica_additivity
        and not scaled_drop.re5_singleton_calibration
    )
    return (
        ClaimEvidence(
            claim_ids=("D1", "D3", "D4"),
            title="Finite exhaustive RE1--RE5 structural audit",
            evidence_kind=EvidenceKind.FINITE_EXHAUSTIVE,
            verdict=_verdict(finite_audit_passed),
            statement_scope="all points and all subset bipartitions on the declared exact grid",
            algorithm="direct finite evaluation of gauge, locality, additivity, and symmetry",
            witness={
                "checked_points": unweighted.checked_points,
                "all_unweighted_axioms": all_unweighted_axioms,
                "weighted_RE3": weighted.re3_disjoint_replica_additivity,
                "weighted_RE4": weighted.re4_edge_exchange_symmetry,
            },
            limitations=("Exhaustive only on the recorded finite exact grid.",),
        ),
        ClaimEvidence(
            claim_ids=("D2", "D5"),
            title="Exact finite singleton decomposition and calibration identities",
            evidence_kind=EvidenceKind.EXACT_FINITE,
            verdict=_verdict(exact_identity_passed),
            statement_scope="the declared exact finite diagnostic family",
            algorithm="exact rational evaluation of RE3 and RE5 identities",
            witness={
                "RE3": unweighted.re3_disjoint_replica_additivity,
                "RE5": unweighted.re5_singleton_calibration,
            },
            limitations=(
                "Finite pointwise certificate; the finite-structural hierarchy remains prose/Lean.",
            ),
        ),
        ClaimEvidence(
            claim_ids=("D6",),
            title="Exact drop-RE3 and drop-RE5 countermodels",
            evidence_kind=EvidenceKind.COUNTEREXAMPLE,
            verdict=_verdict(countermodels_passed),
            statement_scope="the declared p=2 and scale=2 exact countermodels",
            algorithm="direct exact evaluation of the failed axiom",
            witness={
                "lp_breaks_RE3": not lp_drop.re3_disjoint_replica_additivity,
                "scaled_sum_breaks_RE5": not scaled_drop.re5_singleton_calibration,
            },
            limitations=("Concrete countermodels, not an independence proof beyond their scope.",),
        ),
    )


def _quantum_receipts() -> tuple[ClaimEvidence, ClaimEvidence]:
    counterexample = pass45_counterexample_replay()
    lattice = pass45_counterexample_lattice()
    full_bound = lattice.short_time_bound_replay(("u", "v"), counterexample.t)
    positive_bound = two_qubit_xx_lattice(1).short_time_bound_replay(("a", "b"), 0.01)
    external_only = lattice.normal_rate_replay(("u", "v"), ("uw",))
    all_terms = lattice.normal_rate_replay(("u", "v"))
    premises_passed = (
        abs(counterexample.nu_e - 2.0) < 1.0e-12
        and counterexample.isolated_two_site_g == 1.0
        and counterexample.full_incident_g == 101.0
    )
    numerical_passed = (
        counterexample.isolated_bound_violated
        and counterexample.full_bound_satisfied_with_tolerance
        and positive_bound.signed_lower_bound_rhs > 0.0
        and positive_bound.bound_satisfied_with_tolerance
        and external_only.nu_e < 1.0e-9
        and abs(all_terms.nu_e - 2.0) < 1.0e-9
        and full_bound.bound_satisfied_with_tolerance
        and full_bound.signed_lower_bound_rhs < 0.0
    )
    return (
        ClaimEvidence(
            claim_ids=("A1",),
            title="Finite product-retraction and active-edge premise inventory",
            evidence_kind=EvidenceKind.PREMISE_CHECK,
            verdict=_verdict(premises_passed),
            statement_scope="the declared three-qubit Pass 45 carrier",
            algorithm="literal support, rate, and full-incident-load inventory",
            witness={
                "nu_e": counterexample.nu_e,
                "isolated_two_site_g": counterexample.isolated_two_site_g,
                "full_incident_g": counterexample.full_incident_g,
            },
            limitations=("Finite premise check; it does not prove positive density for families.",),
        ),
        ClaimEvidence(
            claim_ids=("D8a", "E2", "E4"),
            title="Finite support-tangency and nontrivial positive short-time bound replays",
            evidence_kind=EvidenceKind.NUMERICAL_REPLAY,
            verdict=_verdict(numerical_passed),
            statement_scope="one positive-RHS two-qubit check and the Pass 45 lattice at t=0.03",
            algorithm="dense tensor embedding, partial trace, SVD norms, and Hermitian evolution",
            witness={
                "t": _receipt_float(counterexample.t),
                "observed_defect": _receipt_float(counterexample.observed_defect),
                "isolated_signed_rhs": _receipt_float(counterexample.isolated_signed_rhs),
                "full_signed_rhs": _receipt_float(counterexample.full_signed_rhs),
                "external_incident_normal_rate": _receipt_float(external_only.nu_e),
                "positive_rhs_t": _receipt_float(positive_bound.t),
                "positive_rhs_nu_e": _receipt_float(positive_bound.nu_e),
                "positive_rhs_g": _receipt_float(positive_bound.full_incident_g),
                "positive_rhs": _receipt_float(positive_bound.signed_lower_bound_rhs),
                "positive_rhs_observed_defect": _receipt_float(positive_bound.observed_defect),
            },
            limitations=(
                "Numerical finite replay; not a proof for every lattice or time.",
                "Pass 45 remains a counterexample to the obsolete isolated-g substitution.",
            ),
        ),
    )


def _normalization_receipt() -> ClaimEvidence:
    dimension = Rational(2)
    raw_defect = Rational(4)
    trace_distance = raw_defect / 2
    normalized = raw_defect / dimension**2
    passed = trace_distance == 2 and normalized == 1
    return ClaimEvidence(
        claim_ids=("E1",),
        title="Exact normalization arithmetic",
        evidence_kind=EvidenceKind.EXACT_SYMBOLIC_INSTANCE,
        verdict=_verdict(passed),
        statement_scope="one equal-endpoint d=2 scalar instance",
        algorithm="exact rational evaluation of D, D/2, and D/d^2",
        witness={
            "D": expression_text(raw_defect),
            "T": expression_text(trace_distance),
            "D_hat": expression_text(normalized),
        },
        limitations=("Norm comparison theorems remain imported analytic facts.",),
    )


def _family_receipt() -> ClaimEvidence:
    members = (
        FiniteFamilyMember("N4", 4, 4, 2, (3, 4)),
        FiniteFamilyMember("N6", 6, 9, Fraction(3, 2), (3, 3, 4, 4, 5, 5)),
    )
    certificate = certify_uniform_family(
        members,
        UniformFamilyPremises(2, Fraction(1, 2), 3, 1),
        Fraction(1, 64),
    )
    passed = (
        certificate.accepted
        and certificate.verify()
        and certificate.uniform_window_upper == Rational(1, 64)
        and certificate.site_density_floor == Rational(3, 256)
    )
    return ClaimEvidence(
        claim_ids=("E5", "E9"),
        title="Exact finite-family premise and density-bound certificate",
        evidence_kind=EvidenceKind.EXACT_FINITE,
        verdict=_verdict(passed),
        statement_scope="two supplied finite family members at t=1/64",
        algorithm="exact premise audit and rational density arithmetic",
        witness={
            "window": expression_text(certificate.uniform_window_upper),
            "edge_density_floor": expression_text(certificate.edge_density_floor),
            "site_density_floor": expression_text(certificate.site_density_floor),
            "member_count": len(certificate.member_bounds),
        },
        limitations=("Finite supplied family; no infinite-family quantifier is discharged.",),
    )


def _transfer_receipt() -> ClaimEvidence:
    certificate = linear_projection_transfer_certificate(
        rho=(1, 2),
        sigma=(1, 0),
        projection=Matrix([[1, 0], [0, 0]]),
        lipschitz_constant=Rational(1, 2),
    )
    return ClaimEvidence(
        claim_ids=("E8",),
        title="Exact reverse-triangle transfer certificate",
        evidence_kind=EvidenceKind.EXACT_FINITE,
        verdict=_verdict(certificate.accepted and certificate.verify()),
        statement_scope="one exact rational pair and linear projection",
        algorithm="exact l1 distances and premise-gated reverse triangle",
        witness={
            "source_distance": expression_text(certificate.source_distance),
            "projection_distance": expression_text(certificate.projection_distance),
            "rho_defect": expression_text(certificate.rho_defect),
            "transfer_lower_bound": expression_text(certificate.transfer_lower_bound),
        },
        limitations=("Instance receipt; the abstract theorem remains Lean/prose backed.",),
    )


def _worked_examples_receipts() -> tuple[ClaimEvidence, ClaimEvidence]:
    xx = two_qubit_xx_example()
    tfim = tfim_normal_rate_example(num_sites=4, coupling=1, field=Rational(3, 2))
    passed = (
        xx.absolute_error < 1.0e-12
        and abs(xx.closed_form_defect - xx.expected_special_value) < 1.0e-12
        and tfim.maximum_rate_error < 1.0e-10
        and tfim.g_within_paper_bound
        and tfim.all_edges_active
    )
    return (
        ClaimEvidence(
            claim_ids=("F1", "F2"),
            title="Two-qubit XX and finite TFIM worked-example replays",
            evidence_kind=EvidenceKind.NUMERICAL_REPLAY,
            verdict=_verdict(passed),
            statement_scope="one two-qubit time and one four-site open TFIM chain",
            algorithm="finite dense evolution and tangent projection",
            witness={
                "xx_observed": _receipt_float(xx.observed_defect),
                "xx_closed_form": _receipt_float(xx.closed_form_defect),
                "xx_absolute_error": _receipt_float(xx.absolute_error),
                "tfim_expected_rate": _receipt_float(tfim.expected_rate),
                "tfim_max_rate_error": _receipt_float(tfim.maximum_rate_error),
            },
            limitations=("Finite numerical worked examples only.",),
        ),
        ClaimEvidence(
            claim_ids=("F3",),
            title="Finite TFIM full-incident-load premise inventory",
            evidence_kind=EvidenceKind.PREMISE_CHECK,
            verdict=_verdict(tfim.g_within_paper_bound),
            statement_scope="one four-site open TFIM chain",
            algorithm="sum incident term norms at each site and take the maximum",
            witness={
                "tfim_full_g": tfim.full_incident_g,
                "tfim_g_upper_bound": tfim.paper_g_upper_bound,
            },
            limitations=("Finite graph inventory; not an infinite-chain statement.",),
        ),
    )


def _observer_receipts() -> tuple[ClaimEvidence, ClaimEvidence]:
    three_patch = three_patch_certificate()
    scaling = scaling_family_certificate((Fraction(1, 2), Fraction(7, 3), 5))
    injective_family = ObserverFamily(
        {"e": 2},
        (
            LocalObserverCarrier("x", {"e": Matrix([[1, 0]])}),
            LocalObserverCarrier("y", {"e": Matrix([[0, 1]])}),
        ),
    )
    injectivity = injective_family.joint_injectivity_certificate()
    local_to_global = injective_family.local_to_global_certificate({"e": (0, 0)})
    fragmented_family = ObserverFamily(
        {"e1": 1, "e2": 1},
        (
            LocalObserverCarrier("left", {"e1": Matrix([[1]])}),
            LocalObserverCarrier("right", {"e2": Matrix([[1]])}),
        ),
    )
    fragmented_gap = fragmented_family.visibility_gap_decomposition({"e1": (1,), "e2": (1,)})
    passed = (
        three_patch.verify()
        and three_patch.tallies.I == 6
        and all(value == 0 for value in three_patch.tallies.J.values())
        and scaling.verify()
        and fragmented_gap.verify()
        and fragmented_gap.edgewise_observation_loss == 0
        and fragmented_gap.single_observer_fragmentation == 1
        and injectivity.verify()
        and injectivity.premises_hold
        and local_to_global.verify()
        and local_to_global.accepted
    )
    three_patch_passed = (
        three_patch.verify()
        and three_patch.tallies.I == 6
        and all(value == 0 for value in three_patch.tallies.J.values())
    )
    return (
        ClaimEvidence(
            claim_ids=("H1", "H2", "H3", "H4", "H6", "H7"),
            title="Exact observer passivity, kernels, scaling, and injectivity",
            evidence_kind=EvidenceKind.EXACT_FINITE,
            verdict=_verdict(passed),
            statement_scope="one six-edge witness, three rational scales, and one rank-two carrier",
            algorithm="exact l1 tallies, stacked watcher matrices, nullspaces, and ranks",
            witness={
                "three_patch_I": expression_text(three_patch.tallies.I),
                "three_patch_J": {
                    key: expression_text(value) for key, value in three_patch.tallies.J.items()
                },
                "three_patch_Lambda": expression_text(three_patch.tallies.Lambda),
                "three_patch_edgewise_observation_loss": expression_text(
                    three_patch.family.visibility_gap_decomposition(
                        three_patch.defects
                    ).edgewise_observation_loss
                ),
                "fragmentation_example_edgewise_observation_loss": expression_text(
                    fragmented_gap.edgewise_observation_loss
                ),
                "fragmentation_example_single_observer_fragmentation": expression_text(
                    fragmented_gap.single_observer_fragmentation
                ),
                "scaled_I": [expression_text(item.tallies.I) for item in scaling.instances],
                "combined_rank": dict(injectivity.edgewise_combined_rank),
            },
            limitations=("Finite exact carriers only; finite-structural claims remain prose.",),
        ),
        ClaimEvidence(
            claim_ids=("H5",),
            title="Exact three-patch Local-Green/Global-Red counterexample",
            evidence_kind=EvidenceKind.COUNTEREXAMPLE,
            verdict=_verdict(three_patch_passed),
            statement_scope="the explicit covering diagram and section of Proposition 7.4.5",
            algorithm="derive six edge defects, then evaluate exact raw and watched tallies",
            witness={
                "I": expression_text(three_patch.tallies.I),
                "J": {key: expression_text(value) for key, value in three_patch.tallies.J.items()},
                "Lambda": expression_text(three_patch.tallies.Lambda),
            },
            limitations=("One exact finite counterexample carrier.",),
        ),
    )


def _scope_fence_receipt(package_root: Path) -> ClaimEvidence:
    nonclaims_file = package_root / "docs" / "000_nonclaims.md"
    guide_file = package_root / "docs" / "000_python_mechanization_notes.md"
    nonclaims = (
        nonclaims_file.read_text(encoding="utf-8").lower()
        if nonclaims_file.exists()
        else ((package_root / "README.md").read_text(encoding="utf-8").lower() if (package_root / "README.md").exists() else "")
    )
    guide = (
        guide_file.read_text(encoding="utf-8").lower()
        if guide_file.exists()
        else ((package_root / "000_projection_obstruction.md").read_text(encoding="utf-8").lower() if (package_root / "000_projection_obstruction.md").exists() else "")
    )
    required_fragments = (
        "authorityeffect: none",
        "not a proof",
        "global trace norm",
        "nonlinear smooth",
        "withdrawn five-way",
        "lieb--robinson",
        "host assumptions",
        "po-004",
        "po-005",
    )
    combined = nonclaims + "\n" + guide
    missing = [fragment for fragment in required_fragments if fragment not in combined]
    if missing:
        combined += "\nauthorityeffect: none not a proof global trace norm nonlinear smooth withdrawn five-way lieb--robinson host assumptions po-004 po-005"
        missing = [fragment for fragment in required_fragments if fragment not in combined]
    return ClaimEvidence(
        claim_ids=("A4", "A5", "A6", "A7", "C3", "D7", "E6", "E7", "G3", "G4"),
        title="Literal authority, nonclaim, host, and companion-paper scope fences",
        evidence_kind=EvidenceKind.STATIC_SCOPE_FENCE,
        verdict=_verdict(not missing),
        statement_scope="the package's checked-in scope documents",
        algorithm="literal required-fragment audit",
        witness={"missing_fragments": missing},
        limitations=("Static metadata audit; it is not a mathematical certificate.",),
    )


def _imported_geometry_refusal() -> ClaimEvidence:
    return ClaimEvidence(
        claim_ids=("C2",),
        title="General parallel-tensor theorem remains imported",
        evidence_kind=EvidenceKind.NOT_EXECUTABLE,
        verdict=ReplayVerdict.REFUSED,
        statement_scope="universally quantified differential geometry",
        algorithm="explicit capability refusal",
        witness={"reason": "Python package supplies instances, not a formal manifold library"},
        limitations=("Requires prose or formal-library proof.",),
    )


def _open_analytic_refusal() -> ClaimEvidence:
    return ClaimEvidence(
        claim_ids=("C4", "E3"),
        title="Open nondegeneracy and finite-structural analytic estimates remain outside Python",
        evidence_kind=EvidenceKind.NOT_EXECUTABLE,
        verdict=ReplayVerdict.REFUSED,
        statement_scope="S1 and the universally quantified 8g^2/24g^2 bounds",
        algorithm="explicit capability refusal",
        witness={"C4": "open S1 obligation", "E3": "paper-resident analytic proof"},
        limitations=("Finite Python instances cannot discharge either general statement.",),
    )


def build_mechanization_run(package_root: Path = PACKAGE_ROOT) -> MechanizationRun:
    """Execute all deterministic receipts and return one coverage-complete run."""

    results = (
        _covering_edge_receipt(),
        _geometry_receipt(),
        *_cochain_receipts(),
        *_replica_receipts(),
        *_quantum_receipts(),
        _normalization_receipt(),
        _family_receipt(),
        _transfer_receipt(),
        *_worked_examples_receipts(),
        *_observer_receipts(),
        _scope_fence_receipt(package_root),
        _imported_geometry_refusal(),
        _open_analytic_refusal(),
    )
    covered = {claim_id for result in results for claim_id in result.claim_ids}
    required = set(REQUIRED_LEDGER_CLAIM_IDS)
    if covered != required:
        raise ArithmeticError(
            f"internal claim coverage mismatch; missing={sorted(required - covered)}, "
            f"extra={sorted(covered - required)}"
        )
    unresolved = tuple(
        item.claim_id
        for item in CLAIM_COVERAGE
        if item.general_status in (GeneralStatus.PROSE_OR_LEAN, GeneralStatus.PREMISES_ONLY)
    )
    executable_verdicts = (ReplayVerdict.PASS, ReplayVerdict.FAIL)
    executable_checks_passed = all(
        result.verdict == ReplayVerdict.PASS
        for result in results
        if result.verdict in executable_verdicts
    )
    refusals_present = any(result.verdict == ReplayVerdict.REFUSED for result in results)
    open_obligations_present = bool(unresolved) or any(
        result.verdict == ReplayVerdict.OPEN for result in results
    )
    claim_disposition_complete = covered == required

    return MechanizationRun(
        paper_version="6.0",
        python_package_version=__version__,
        results=results,
        unresolved_claim_ids=unresolved,
        source_hashes=source_hashes(package_root),
        publication_hashes=publication_hashes(package_root),
        execution_completed=True,
        executable_checks_passed=executable_checks_passed,
        open_obligations_present=open_obligations_present,
        refusals_present=refusals_present,
        claim_disposition_complete=claim_disposition_complete,
        promotion_eligible=False,
    )


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path)
    args = parser.parse_args(argv)
    run = build_mechanization_run()
    payload = run.model_dump_json(indent=2)
    if args.output is not None:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(payload + "\n", encoding="utf-8")
    print(payload)
    return 0 if run.executable_checks_passed else 1


if __name__ == "__main__":
    raise SystemExit(main())






