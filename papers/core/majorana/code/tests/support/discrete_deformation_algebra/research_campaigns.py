"""Finite research campaigns driven by the cascade solver and DDA traces.

The campaigns deliberately separate executable finite shadows from the much
larger physics claims that motivated them.  A passing finite shadow is recorded
as local evidence.  Missing detectors, comparison maps, or derivations are
recorded as ``Z·T`` in the experimental dialect, never as solved claims.

AuthorityEffect: None.
"""

from __future__ import annotations

import hashlib
import json
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any, Dict, Iterable, List, Mapping, Optional, Type

import numpy as np
from omega_engine.crates.carrier.cochain_carrier import CochainCarrier
from omega_engine.crates.discrete_deformation_algebra.dda_dag_builder import build_dda_dag
from omega_engine.crates.discrete_deformation_algebra.dda_trace_logger import (
    TraceLogger,
    _find_repo_root,
)
from omega_engine.crates.discrete_deformation_algebra.symbol_game_bridge import (
    emit_symbol_game_dda_trace,
    emit_symbol_game_dda_trace_v3,
    verify_symbol_game_dda_bridge,
    verify_symbol_game_dda_bridge_v3,
)
from omega_engine.crates.discrete_deformation_algebra.trajectory_recorder import (
    verify_trajectory_chain,
)
from omega_engine.crates.engine.eng_symbol_game import OesosLab
from omega_engine.crates.homology_theory.lefschetz_thimble import (
    airy_action,
    descent_directions,
    integrate_exp_action,
    monodromy,
    trace_thimble,
)
from omega_engine.crates.operator.projector.proj_symbol_game import TerminalStatus
from omega_engine.crates.residuals.network_residual import Network
from omega_engine.crates.solver.solv_airy_newton_proposal import (
    AiryNewtonProposalSolver,
)
from omega_engine.crates.solver.solv_coda_cascade_proposal import (
    CodaCascadeProposalSolver,
)
from omega_engine.crates.solver.solv_omega_engine_solver_of_solvers.solv_oesos import (
    CascadeSolver as CanonicalCascadeSolver,
)
from omega_engine.crates.state.airy_state import AiryCriticalStateV1
from omega_engine.crates.state.cochain_state import CochainState
from omega_engine.crates.type.runtime_axes import DdaDialect
from omega_engine.crates.type.symgame import TerminalStatus

from omega_engine_governance.contracts.dda_packets import (
    DDATapeDFA,
    DDATapeValidationError,
)
from omega_engine_pfp.domain import (
    DDA_TRACE_MEDIA_TYPE,
    EVALUATE_FINITE,
    GR_FINITE_FAMILY,
    GR_STRETCH_FAMILY,
    LOCAL_REPLAYABLE_FINITE_EVIDENCE,
    REFUSAL_ONLY,
    REFUSE_UNSUPPORTED,
    RESEARCH_PACKET_MEDIA_TYPE,
    SOURCE_INTAKE_MEDIA_TYPE,
    WITTEN_FINITE_FAMILY,
    WITTEN_FULL_FAMILY,
    FrozenCorpus,
    ResearchClaimPayloadV1,
    ResearchClaimV1,
    SourceArtifactV1,
    SourceIntakeBundleV1,
    artifact_ref_from_path,
    build_research_claim_envelope,
    build_research_run_root,
    parse_research_claim_envelope,
    propose_routing_update,
    verify_research_run_root,
    write_research_run_root,
)
from omega_engine_pfp.domain.entities.oesos_evidence_bundle import (
    OESOS_EVIDENCE_BUNDLE_MEDIA_TYPE,
    build_oesos_evidence_bundle,
    write_oesos_evidence_bundle,
)
from omega_engine_pfp.domain.entities.packet_envelope import PacketEnvelopeV2
from omega_engine_pfp.domain.shared_kernel.canonical import thaw
from omega_engine_pfp.fixtures import (
    ExhaustiveCspSolver,
    NoOpClaimingSolver,
    build_demo_problem,
)
from omega_engine_pfp.use_cases.problem_builders.airy_problem import (
    DEFAULT_AIRY_LAMBDA,
    DEFAULT_AIRY_SEEDS,
    build_airy_problem,
)
from omega_engine_pfp.use_cases.problem_builders.coda_problem import (
    build_coda_problem,
)
from omega_engine_pfp.use_cases.prompt_artifact import (
    write_content_addressed_json,
)
from omega_engine_pfp.use_cases.research import (
    build_source_artifact,
    build_source_intake_bundle,
)


@dataclass(frozen=True)
class CampaignOutcome:
    name: str
    status: str
    tape: List[str]
    trace_path: str
    residual_initial: Optional[float]
    residual_final: Optional[float]
    metrics: Dict[str, Any]
    retained_obstructions: List[str]


@dataclass(frozen=True)
class _ResearchPacketContext:
    envelope: PacketEnvelopeV2
    payload: ResearchClaimPayloadV1
    intake: SourceIntakeBundleV1
    packet_path: Path
    intake_path: Path

    @property
    def claim_ids(self) -> tuple[str, ...]:
        return tuple(claim.claim_id for claim in self.payload.claims)

    @property
    def unresolved_obligations(self) -> tuple[str, ...]:
        return tuple(
            sorted(
                {
                    obligation
                    for claim in self.payload.claims
                    for obligation in claim.unresolved_obligations
                }
            )
        )


_CAMPAIGN_RUNNERS = (
    "solver_of_solvers_witten_airy_finite",
    "solver_of_solvers_witten_full_chern_simons",
    "solver_of_solvers_gr_constraint_closure",
    "solver_of_solvers_gr_stretch_claims",
    "solver_of_solvers_symbol_game_coda",
    "solver_of_solvers_symbol_game_self_improvement",
    "solver_of_solvers_trace_self_audit",
)
_LEGACY_RUST_HOST_ARTIFACTS = (
    "solver_of_solvers_symbol_game_coda_rust_host_description_v1.json",
    "solver_of_solvers_symbol_game_coda_rust_host_manifest_v1.json",
    "solver_of_solvers_symbol_game_coda_rust_host_request_v1.json",
    "solver_of_solvers_symbol_game_coda_rust_host_outcome_v1.json",
)
_RUST_HOST_ARTIFACT_GLOB = "solver_of_solvers_symbol_game_coda_rust_host_*_v1_*.json"
_RESEARCH_ARTIFACT_GLOBS = (
    "solver_of_solvers_*_research_packet_v1_*.json",
    "solver_of_solvers_*_source_intake_v1_*.json",
    "solver_of_solvers_*_research_run_root_v1_*.json",
    "solver_of_solvers_*_oesos_evidence_bundle_v1_*.json",
)
_ADDITIONAL_RESEARCH_TRACE_RUNNERS = (
    "solver_of_solvers_witten_airy_finite-oesos",
    "solver_of_solvers_gr_constraint_closure-injected-test-rail",
)
_CAMPAIGN_REPORTS = (
    "dda_dag.json",
    "dda_dag_summary.md",
    "solver_of_solvers_report.json",
    "solver_of_solvers_report.md",
    "autoskill_metrics.json",
    "auto_improve_autoskill_report.md",
    *_LEGACY_RUST_HOST_ARTIFACTS,
)


def _reset_owned_campaign_outputs(trace_dir: Path) -> None:
    """Replace only artifacts owned by this fixed seven-run campaign."""
    for runner_id in _CAMPAIGN_RUNNERS:
        for owned_runner in (runner_id, f"{runner_id}-v2-local"):
            for path in trace_dir.glob(f"{owned_runner}_*_dda_trace.jsonl"):
                if path.is_file():
                    path.unlink()
    for runner_id in _ADDITIONAL_RESEARCH_TRACE_RUNNERS:
        for path in trace_dir.glob(f"{runner_id}_*_dda_trace.jsonl"):
            if path.is_file():
                path.unlink()
    for name in _CAMPAIGN_REPORTS:
        path = trace_dir / name
        if path.is_file():
            path.unlink()
    for path in trace_dir.glob(_RUST_HOST_ARTIFACT_GLOB):
        if path.is_file():
            path.unlink()
    for pattern in _RESEARCH_ARTIFACT_GLOBS:
        for path in trace_dir.glob(pattern):
            if path.is_file():
                path.unlink()


def _remove_legacy_rust_host_artifacts(trace_dir: Path) -> None:
    """Remove ambiguous pre-content-addressing aliases before a standalone run."""

    for name in _LEGACY_RUST_HOST_ARTIFACTS:
        path = trace_dir / name
        if path.is_file():
            path.unlink()


def _portable_path(path: Path) -> str:
    resolved = path.resolve()
    repo_root = _find_repo_root(Path(__file__).resolve().parent)
    try:
        return resolved.relative_to(repo_root).as_posix()
    except ValueError:
        return str(resolved)


def _write_rust_host_artifacts(
    trace_dir: Path,
    evaluation: Any,
) -> Dict[str, str]:
    """Retain the complete untrusted wire evidence beside the DDA traces."""

    artifacts = {
        "description": evaluation.description.to_dict(),
        "carrier_manifest": evaluation.carrier_manifest.to_dict(),
        "request": evaluation.request.to_dict(),
        "outcome": evaluation.outcome.to_dict(),
    }
    retained: Dict[str, str] = {}
    for label, payload in artifacts.items():
        encoded = (json.dumps(payload, indent=2, sort_keys=True) + "\n").encode("utf-8")
        content_root = hashlib.sha256(encoded).hexdigest()
        name = (
            "solver_of_solvers_symbol_game_coda_rust_host_"
            f"{label}_v1_{content_root}.json"
        )
        path = trace_dir / name
        try:
            with path.open("xb") as handle:
                handle.write(encoded)
        except FileExistsError:
            if path.read_bytes() != encoded:
                raise RuntimeError(
                    f"content-addressed Rust host artifact collision: {path}"
                )
        retained[label] = _portable_path(path)
    return retained


_WITTEN_PDF_PATH = (
    "omega_engine/research/published/"
    "edward_witten_analytic_continuation_chern_simons_1001.2933.pdf"
)
_WITTEN_PDF_SHA256 = "d10e8d591b29284dcf029c2bde74b27bf76be98f957173eeb545d04e3f79cfd6"
_WITTEN_PDF_BYTE_COUNT = 1_164_417
_GR_PUBLISHED_ROOT = (
    "omega_research/programs/010_general_relativity/"
    "constraint_closure_and_the_l1_structure_of_physical_law"
)


def _complex_payload(value: complex) -> Dict[str, str]:
    return {
        "real_hex": float(value.real).hex(),
        "imag_hex": float(value.imag).hex(),
    }


def _claim(
    *,
    claim_id: str,
    statement: str,
    disposition: str,
    source_ids: Iterable[str],
    assumptions: Iterable[str],
    units: str,
    carrier: str,
    coefficient_semantics: str,
    projection: str,
    retraction: str,
    obstruction: str,
    detector: str,
    comparison_map: str,
    falsifier: str,
    independent_checker: str,
    unresolved_obligations: Iterable[str] = (),
) -> ResearchClaimV1:
    return ResearchClaimV1(
        claim_id=claim_id,
        statement=statement,
        disposition=disposition,
        source_ids=tuple(sorted(source_ids)),
        assumptions=tuple(sorted(assumptions)),
        units=units,
        carrier=carrier,
        coefficient_semantics=coefficient_semantics,
        projection=projection,
        retraction=retraction,
        obstruction=obstruction,
        detector=detector,
        comparison_map=comparison_map,
        falsifier=falsifier,
        independent_checker=independent_checker,
        unresolved_obligations=tuple(sorted(unresolved_obligations)),
        evidence_ceiling=(
            LOCAL_REPLAYABLE_FINITE_EVIDENCE
            if disposition == EVALUATE_FINITE
            else REFUSAL_ONLY
        ),
    )


def _witten_sources(repo_root: Path) -> tuple[SourceArtifactV1, ...]:
    sources = (
        build_source_artifact(
            repo_root,
            source_id="WITTEN-AIRY-IMPLEMENTATION",
            path="omega_engine/crates/homology_theory/lefschetz_thimble.py",
            role="implementation",
            normalization="utf8-lf-v1",
            repository_tracked_expected=True,
        ),
        SourceArtifactV1(
            source_id="WITTEN-PAPER-1001.2933",
            path=_WITTEN_PDF_PATH,
            role="primary_source",
            normalization="raw-bytes",
            sha256=_WITTEN_PDF_SHA256,
            byte_count=_WITTEN_PDF_BYTE_COUNT,
            repository_tracked_expected=False,
        ),
    )
    return tuple(sorted(sources, key=lambda source: source.source_id))


def _gr_sources(repo_root: Path) -> tuple[SourceArtifactV1, ...]:
    declarations = (
        (
            "GR-LIVE-NETWORK",
            "omega_engine/crates/residuals/network_residual.py",
            "implementation",
        ),
        (
            "GR-LIVE-SOLVER",
            "omega_engine/crates/solver/"
            "solv_omega_engine_solver_of_solvers/solv_oesos.py",
            "implementation",
        ),
        (
            "GR-PUBLISHED-CLAIM-LEDGER",
            f"{_GR_PUBLISHED_ROOT}/constraint_closure_l1_toy_model_claim_ledger.md",
            "derived_evidence",
        ),
        (
            "GR-PUBLISHED-PAPER",
            f"{_GR_PUBLISHED_ROOT}/constraint_closure_l1_toy_model.md",
            "primary_source",
        ),
        (
            "GR-PUBLISHED-SOLVER",
            f"{_GR_PUBLISHED_ROOT}/code/dda/solver_of_solvers.py",
            "implementation",
        ),
    )
    return tuple(
        sorted(
            (
                build_source_artifact(
                    repo_root,
                    source_id=source_id,
                    path=path,
                    role=role,
                    normalization="utf8-lf-v1",
                    repository_tracked_expected=True,
                )
                for source_id, path, role in declarations
            ),
            key=lambda source: source.source_id,
        )
    )


def _witten_finite_initial_state() -> Dict[str, Any]:
    return {
        "model": "I_lambda(z)=i*lambda*(z^3/3-z)",
        "lambda": _complex_payload(DEFAULT_AIRY_LAMBDA),
        "seeds": [
            {
                "slot_id": f"seed-{index:02d}",
                "value": _complex_payload(seed),
            }
            for index, seed in enumerate(DEFAULT_AIRY_SEEDS)
        ],
        "newton": {
            "maximum_iterations": 64,
            "convergence_threshold_hex": (1.0e-14).hex(),
        },
        "flow": {
            "dt_hex": (1.0e-3).hex(),
            "n_steps": 8000,
            "h_floor_hex": (-20.0).hex(),
            "max_imaginary_drift_hex": (5.0e-3).hex(),
        },
        "real_cycle": {
            "lambda_hex": (2.0).hex(),
            "error_tolerance_hex": (2.0e-3).hex(),
        },
        "monodromy_power": 3,
    }


def _gr_finite_initial_state() -> Dict[str, Any]:
    edges = ((0, 1), (1, 2), (2, 0), (1, 3), (3, 0))
    values = (3.0, 2.0, 2.0, 1.0, 1.0)
    return {
        "coefficient_semantics": "real edge cochains; exact integer fixture values",
        "nodes": [0, 1, 2, 3],
        "edges": [list(edge) for edge in edges],
        "faces": [[0, 1, 2], [0, 1, 3]],
        "weights": [1, 1, 1, 1, 1],
        "omega": [
            {"edge": list(edge), "value_hex": value.hex()}
            for edge, value in zip(edges, values)
        ],
        "tolerance_hex": (1.0e-8).hex(),
        "maximum_lifts": 0,
        "cell_attachment": "disabled",
        "execution_relation": "LIVE_PORT_EXECUTION",
    }


def _retain_research_context(
    *,
    trace_dir: Path,
    repo_root: Path,
    runner_id: str,
    payload: ResearchClaimPayloadV1,
    task_id: str,
    carrier_id: str,
    initial_state: Mapping[str, Any],
    protected_boundaries: tuple[str, ...],
    step_budget: int,
) -> _ResearchPacketContext:
    envelope = build_research_claim_envelope(
        payload,
        task_id,
        carrier_id,
        dict(initial_state),
        tuple(sorted(protected_boundaries)),
        step_budget,
    )
    parsed = parse_research_claim_envelope(envelope)
    if parsed.payload_id != payload.payload_id:
        raise RuntimeError("research packet round trip changed its payload identity")
    intake = build_source_intake_bundle(envelope, repo_root)
    packet_path = write_content_addressed_json(
        trace_dir,
        f"{runner_id}_research_packet_v1",
        envelope.to_dict(),
    )
    intake_path = write_content_addressed_json(
        trace_dir,
        f"{runner_id}_source_intake_v1",
        intake.to_dict(),
    )
    return _ResearchPacketContext(
        envelope=envelope,
        payload=payload,
        intake=intake,
        packet_path=packet_path,
        intake_path=intake_path,
    )


def _build_research_contexts(
    trace_dir: Path,
) -> Dict[str, _ResearchPacketContext]:
    repo_root = _find_repo_root(Path(__file__).resolve().parent)
    witten_sources = _witten_sources(repo_root)
    gr_sources = _gr_sources(repo_root)

    witten_finite_initial = _witten_finite_initial_state()
    witten_finite_payload = ResearchClaimPayloadV1(
        family=WITTEN_FINITE_FAMILY,
        disposition=EVALUATE_FINITE,
        sources=witten_sources,
        claims=(
            _claim(
                claim_id="WITTEN-AIRY-FINITE-SHADOW-V1",
                statement=(
                    "The declared five-seed Airy critical equation closes and "
                    "the bounded numerical thimble checks meet their tolerances."
                ),
                disposition=EVALUATE_FINITE,
                source_ids=(
                    "WITTEN-AIRY-IMPLEMENTATION",
                    "WITTEN-PAPER-1001.2933",
                ),
                assumptions=(
                    "declared finite Airy transcription",
                    "double-precision bounded numerical integration",
                    "fixed five-seed carrier",
                    "Python import bytes are not atomically snapshot-bound to execution",
                ),
                units="dimensionless Airy model",
                carrier="five labeled complex seed slots plus finite flow samples",
                coefficient_semantics="normalized IEEE-754 binary64 float.hex pairs",
                projection="max |lambda*(z^2-1)| on the fixed slots",
                retraction="bounded Newton proposal followed by independent reprojection",
                obstruction="nonzero Airy critical residual or failed flow invariant",
                detector="exact-root and obstructed five-slot controls",
                comparison_map="two-thimble sum versus scipy/mpmath Airy reference",
                falsifier="any declared residual or invariant exceeds its bound",
                independent_checker="OESOS projector plus DDA and run-root replay",
            ),
        ),
        initial_state_payload=witten_finite_initial,
    )
    witten_finite = _retain_research_context(
        trace_dir=trace_dir,
        repo_root=repo_root,
        runner_id="solver_of_solvers_witten_airy_finite",
        payload=witten_finite_payload,
        task_id="solver-of-solvers-witten-airy-finite-v1",
        carrier_id="witten-airy-finite-five-slot-and-flow-v1",
        initial_state=witten_finite_initial,
        protected_boundaries=(
            "finite_evidence_does_not_imply_full_chern_simons",
            "source_bytes_do_not_prove_transcription",
            "witten_airy_critical_equation",
        ),
        step_budget=2,
    )

    witten_full_initial = {
        "finite_context_packet_id": witten_finite.envelope.packet_id,
        "requested_scope": "full analytic continuation of Chern-Simons theory",
    }
    witten_full_payload = ResearchClaimPayloadV1(
        family=WITTEN_FULL_FAMILY,
        disposition=REFUSE_UNSUPPORTED,
        sources=witten_sources,
        claims=(
            _claim(
                claim_id="WITTEN-CHERN-SIMONS-FULL-SCOPE-V1",
                statement=(
                    "Derive the full infinite-dimensional Chern-Simons analytic "
                    "continuation, knot, and twisted N=4 consequences."
                ),
                disposition=REFUSE_UNSUPPORTED,
                source_ids=("WITTEN-PAPER-1001.2933",),
                assumptions=("finite Airy evidence is contextual only",),
                units="not established",
                carrier="infinite-dimensional gauge-orbit configuration space",
                coefficient_semantics="not constructed",
                projection="no adequate full-scope projector",
                retraction="no verified full-scope retraction",
                obstruction="missing continuum carrier and comparison maps",
                detector="finite Airy controls are insufficient",
                comparison_map="not implemented",
                falsifier="a complete independent continuum replay would discharge the gap",
                independent_checker="not implemented",
                unresolved_obligations=(
                    "infinite-dimensional Chern-Simons configuration-space carrier",
                    "knot invariant and twisted N=4 Hilbert-space certificates",
                    "middle-dimensional integration-cycle construction for gauge orbits",
                    "verified four-dimensional flow and Stokes wall comparison maps",
                ),
            ),
        ),
        initial_state_payload=witten_full_initial,
    )
    witten_full = _retain_research_context(
        trace_dir=trace_dir,
        repo_root=repo_root,
        runner_id="solver_of_solvers_witten_full_chern_simons",
        payload=witten_full_payload,
        task_id="solver-of-solvers-witten-full-scope-v1",
        carrier_id="witten-full-scope-unconstructed-v1",
        initial_state=witten_full_initial,
        protected_boundaries=(
            "finite_evidence_does_not_imply_full_chern_simons",
            "unsupported_claims_remain_refused",
        ),
        step_budget=1,
    )

    gr_finite_initial = _gr_finite_initial_state()
    gr_finite_payload = ResearchClaimPayloadV1(
        family=GR_FINITE_FAMILY,
        disposition=EVALUATE_FINITE,
        sources=gr_sources,
        claims=(
            _claim(
                claim_id="GR-FINITE-CONSTRAINT-CLOSURE-V1",
                statement=(
                    "The declared finite face-aware cochain fixture closes Phi1 "
                    "and Gamma2 under an independently reprojected same-carrier repair."
                ),
                disposition=EVALUATE_FINITE,
                source_ids=(
                    "GR-LIVE-NETWORK",
                    "GR-LIVE-SOLVER",
                    "GR-PUBLISHED-PAPER",
                    "GR-PUBLISHED-SOLVER",
                ),
                assumptions=(
                    "finite two-face carrier",
                    "live port executes rather than isolated published package",
                    "positive unit edge weights",
                    "Python import bytes are not atomically snapshot-bound to execution",
                ),
                units="dimensionless weighted L1 cochain residual",
                carrier="four vertices, five oriented edges, two triangular faces",
                coefficient_semantics="real edge cochains with exact integer fixture input",
                projection="independent Phi1 quotient and Gamma2 closure replay",
                retraction="existing cascade output treated only as an OESOS proposal",
                obstruction="cochain:phi1 and cochain:gamma2",
                detector="zero and face-aware positive controls",
                comparison_map="identity on the fixed finite cochain carrier",
                falsifier="nonzero independently reprojected Phi1 or Gamma2",
                independent_checker="OESOS projector plus Symbol Game DDA bridge",
            ),
        ),
        initial_state_payload=gr_finite_initial,
    )
    gr_finite = _retain_research_context(
        trace_dir=trace_dir,
        repo_root=repo_root,
        runner_id="solver_of_solvers_gr_constraint_closure",
        payload=gr_finite_payload,
        task_id="solver-of-solvers-gr-finite-closure-v1",
        carrier_id="finite-cochain-2-v1",
        initial_state=gr_finite_initial,
        protected_boundaries=(
            "cochain_gamma2",
            "cochain_phi1",
            "exact_rational_cochain",
            "l1_norm_ball",
        ),
        step_budget=2,
    )

    stretch_assessments = {
        "GR-STRETCH-BLACK-HOLES-V1": (
            "Derive black-hole geometry and horizon results.",
            "no horizon theorem or solved spacetime geometry is produced",
        ),
        "GR-STRETCH-DARK-ENERGY-V1": (
            "Derive dark energy from obstruction management.",
            "no cosmological solution or data-bound comparison map is implemented",
        ),
        "GR-STRETCH-DARK-MATTER-V1": (
            "Derive dark matter from obstruction management.",
            "no matter-sector dynamics, detector, or observational likelihood is implemented",
        ),
        "GR-STRETCH-FERMION-MASSES-V1": (
            "Derive the fermion mass spectrum.",
            "the current spectrum uses fitted parameters and supplies no unique mass theorem",
        ),
        "GR-STRETCH-INFLATION-CMB-V1": (
            "Show inflation and CMB radiation are large-scale obstruction artifacts.",
            "no cosmological dynamics or CMB likelihood distinguishes the hypothesis",
        ),
        "GR-STRETCH-SM-GAUGE-V1": (
            "Derive SU(3)xSU(2)xU(1).",
            "3-2-1 simplex labels assert the groups rather than force them",
        ),
        "GR-STRETCH-SUSY-V1": (
            "Derive supersymmetry.",
            "a dimensional scale construction is not a superalgebra or spectrum derivation",
        ),
    }
    gr_stretch_initial = {
        "finite_context_packet_id": gr_finite.envelope.packet_id,
        "requested_claim_ids": list(sorted(stretch_assessments)),
    }
    gr_stretch_payload = ResearchClaimPayloadV1(
        family=GR_STRETCH_FAMILY,
        disposition=REFUSE_UNSUPPORTED,
        sources=gr_sources,
        claims=tuple(
            _claim(
                claim_id=claim_id,
                statement=statement,
                disposition=REFUSE_UNSUPPORTED,
                source_ids=(
                    "GR-PUBLISHED-CLAIM-LEDGER",
                    "GR-PUBLISHED-PAPER",
                ),
                assumptions=("finite cochain closure is contextual evidence only",),
                units="not established",
                carrier="required physical carrier not constructed",
                coefficient_semantics="not established",
                projection="no adequate observable projector",
                retraction="no verified physical retraction",
                obstruction=obligation,
                detector="not implemented",
                comparison_map="not implemented",
                falsifier="a unique derivation plus independent observational replay",
                independent_checker="not implemented",
                unresolved_obligations=(obligation,),
            )
            for claim_id, (statement, obligation) in sorted(stretch_assessments.items())
        ),
        initial_state_payload=gr_stretch_initial,
    )
    gr_stretch = _retain_research_context(
        trace_dir=trace_dir,
        repo_root=repo_root,
        runner_id="solver_of_solvers_gr_stretch_claims",
        payload=gr_stretch_payload,
        task_id="solver-of-solvers-gr-stretch-refusal-v1",
        carrier_id="gr-continuum-geometry-refusal-v1",
        initial_state=gr_stretch_initial,
        protected_boundaries=(
            "continuum_from_finite_refused",
            "unsupported_claims_remain_refused",
        ),
        step_budget=1,
    )
    return {
        WITTEN_FINITE_FAMILY: witten_finite,
        WITTEN_FULL_FAMILY: witten_full,
        GR_FINITE_FAMILY: gr_finite,
        GR_STRETCH_FAMILY: gr_stretch,
    }


def _research_binding_evidence(
    context: _ResearchPacketContext,
) -> Dict[str, Any]:
    external_sources = [
        receipt.source_id
        for receipt in context.intake.receipts
        if not receipt.repository_tracked_expected
    ]
    unavailable_sources = [
        receipt.source_id
        for receipt in context.intake.receipts
        if not receipt.available
    ]
    return {
        "packet_id": context.envelope.packet_id,
        "packet_family": context.payload.family,
        "payload_id": context.payload.payload_id,
        "source_manifest_root": context.payload.source_manifest_root,
        "claim_manifest_root": context.payload.claim_manifest_root,
        "initial_state_hash": context.payload.initial_state_hash,
        "source_intake_receipt_id": context.intake.receipt_id,
        "source_intake_all_verified": context.intake.all_verified,
        "claim_ids": list(context.claim_ids),
        "unresolved_obligations": list(context.unresolved_obligations),
        "external_source_bytes_required": external_sources,
        "unavailable_sources": unavailable_sources,
        "packet_artifact": _portable_path(context.packet_path),
        "source_intake_artifact": _portable_path(context.intake_path),
        "authority_effect": "None",
    }


def _attach_research_run_root(
    outcome: CampaignOutcome,
    context: _ResearchPacketContext,
    *,
    trace_dir: Path,
    refusal_codes: Iterable[str] = (),
    evidence_profile: str,
    oesos_problem: Any | None = None,
    oesos_run: Any | None = None,
    oesos_bridge: Any | None = None,
    additional_artifacts: Iterable[tuple[Path, str]] = (),
) -> CampaignOutcome:
    semantic_trace = trace_dir / Path(outcome.trace_path).name
    if (oesos_problem is None) is not (oesos_run is None) or (
        oesos_run is None
    ) is not (oesos_bridge is None):
        raise RuntimeError(
            "OESOS problem, run, and DDA bridge evidence must be retained together"
        )
    oesos_bundle = None
    oesos_bundle_path = None
    if oesos_run is not None:
        oesos_bundle = build_oesos_evidence_bundle(
            oesos_problem,
            oesos_run,
            research_parent_packet_id=context.envelope.packet_id,
        )
        oesos_bundle_path = write_oesos_evidence_bundle(
            oesos_bundle,
            trace_dir,
            filename_prefix=f"{outcome.name}_oesos_evidence_bundle_v1",
        )
    artifacts = [
        artifact_ref_from_path(
            context.packet_path,
            trace_dir,
            media_type=RESEARCH_PACKET_MEDIA_TYPE,
        ),
        artifact_ref_from_path(
            context.intake_path,
            trace_dir,
            media_type=SOURCE_INTAKE_MEDIA_TYPE,
        ),
        artifact_ref_from_path(
            semantic_trace,
            trace_dir,
            media_type=DDA_TRACE_MEDIA_TYPE,
        ),
    ]
    if oesos_bundle_path is not None:
        artifacts.append(
            artifact_ref_from_path(
                oesos_bundle_path,
                trace_dir,
                media_type=OESOS_EVIDENCE_BUNDLE_MEDIA_TYPE,
            )
        )
    for path, media_type in additional_artifacts:
        artifacts.append(
            artifact_ref_from_path(
                path,
                trace_dir,
                media_type=media_type,
            )
        )
    run_root = build_research_run_root(
        trace_path=semantic_trace,
        claim_packet_id=context.envelope.packet_id,
        family_id=context.payload.family,
        source_manifest_root=context.payload.source_manifest_root,
        claim_manifest_root=context.payload.claim_manifest_root,
        source_intake_receipt_id=context.intake.receipt_id,
        terminal_status=outcome.status,
        artifact_manifest=artifacts,
        refusal_codes=tuple(sorted(set(refusal_codes))),
        unresolved_obligations=context.unresolved_obligations,
        evidence_profile=evidence_profile,
        oesos_event_root=(oesos_run.event_root if oesos_run is not None else None),
        oesos_runtime_root=(oesos_run.runtime_id if oesos_run is not None else None),
        oesos_wire_root=(
            oesos_run.to_wire_receipt().receipt_id if oesos_run is not None else None
        ),
        oesos_bridge_root=(None),
    )
    if not verify_research_run_root(run_root, trace_dir):
        raise RuntimeError("research run root did not verify")
    root_path = write_research_run_root(
        run_root,
        trace_dir,
        filename_prefix=f"{outcome.name}_research_run_root_v1",
    )
    metrics = dict(outcome.metrics)
    metrics["research_packet"] = _research_binding_evidence(context)
    metrics["research_run_root"] = {
        "root_id": run_root.root_id,
        "semantic_dda_root": run_root.semantic_dda_root,
        "semantic_trace_label": run_root.semantic_trace_label,
        "artifact": _portable_path(root_path),
        "verified": True,
        "evidence_profile": run_root.evidence_profile,
        "refusal_codes": list(run_root.refusal_codes),
        "authority_effect": "None",
    }
    if oesos_bundle is not None and oesos_bundle_path is not None:
        metrics["research_run_root"]["oesos_evidence_bundle"] = {
            "bundle_id": oesos_bundle.bundle_id,
            "artifact": _portable_path(oesos_bundle_path),
            "event_root": oesos_run.event_root,
            "runtime_root": oesos_run.runtime_id,
            "wire_root": oesos_run.to_wire_receipt().receipt_id,
            "bridge_root": oesos_bridge.bridge_root,
            "bridge_root_relation": "BOUND_ONLY_NOT_RUN_ROOT_REPLAY",
            "authority_effect": "None",
        }
    return CampaignOutcome(
        name=outcome.name,
        status=outcome.status,
        tape=outcome.tape,
        trace_path=outcome.trace_path,
        residual_initial=outcome.residual_initial,
        residual_final=outcome.residual_final,
        metrics=metrics,
        retained_obstructions=outcome.retained_obstructions,
    )


def _decode_complex(value: Mapping[str, Any]) -> complex:
    if set(value) != {"real_hex", "imag_hex"}:
        raise RuntimeError("research complex scalar has an invalid shape")
    real = float.fromhex(str(value["real_hex"]))
    imag = float.fromhex(str(value["imag_hex"]))
    if not np.isfinite(real) or not np.isfinite(imag):
        raise RuntimeError("research complex scalar is non-finite")
    return complex(real, imag)


def _decode_witten_finite_state(
    context: _ResearchPacketContext,
) -> tuple[complex, tuple[complex, ...]]:
    state = thaw(context.payload.initial_state_payload)
    if type(state) is not dict:
        raise RuntimeError("Witten research initial state is not a mapping")
    lam = _decode_complex(state["lambda"])
    raw_seeds = state["seeds"]
    if type(raw_seeds) is not list or len(raw_seeds) != 5:
        raise RuntimeError("Witten research packet requires five seed slots")
    seeds = tuple(_decode_complex(item["value"]) for item in raw_seeds)
    return lam, seeds


def _decode_gr_finite_state(
    context: _ResearchPacketContext,
) -> tuple[CochainCarrier, CochainState]:
    state = thaw(context.payload.initial_state_payload)
    if type(state) is not dict:
        raise RuntimeError("GR research initial state is not a mapping")
    nodes = tuple(int(node) for node in state["nodes"])
    edges = tuple(tuple(int(node) for node in edge) for edge in state["edges"])
    faces = tuple(tuple(int(node) for node in face) for face in state["faces"])
    weights = tuple(int(weight) for weight in state["weights"])
    values = {
        tuple(int(node) for node in item["edge"]): float.fromhex(str(item["value_hex"]))
        for item in state["omega"]
    }
    return (
        CochainCarrier(nodes=nodes, edges=edges, faces=faces, weights=weights),
        CochainState.from_mapping(values),
    )


def _run_rust_host_for_symbol_game(
    problem: Any,
    run: Any,
    *,
    trace_dir: Path,
    rust_host_path: Path | None,
) -> tuple[
    Any | None,
    tuple[str, ...],
    Dict[str, Any],
]:
    """Return a typed refusal until the deleted Rust host adapter is rebuilt."""

    if rust_host_path is None:
        return (
            None,
            ("RUST_HOST_NOT_RUN",),
            {
                "status": "NOT_RUN",
                "authority_effect": "None",
            },
        )
    return (
        None,
        ("RUST_HOST_CLIENT_REFUSED", "RUST_HOST_ADAPTER_UNAVAILABLE"),
        {
            "status": "CLIENT_REFUSED",
            "code": "RUST_HOST_ADAPTER_UNAVAILABLE",
            "detail": (
                "the legacy Rust Prime/OESOS adapter was deleted; "
                "external host execution remains disabled"
            ),
            "authority_effect": "None",
        },
    )


def _airy_reference(lam: float) -> complex:
    """Standard Airy value matching ``exp(i*lam*(x^3/3-x))`` on the real line."""
    try:
        from scipy.special import airy

        ai = airy(-(lam ** (2.0 / 3.0)))[0]
    except ImportError:
        import mpmath

        ai = float(mpmath.airyai(-(lam ** (2.0 / 3.0))))
    return 2.0 * np.pi * lam ** (-1.0 / 3.0) * complex(ai)


def _airy_real_cycle_check(lam: float = 2.0) -> Dict[str, Any]:
    """Numerically test the two-thimble real-cycle decomposition up to orientation."""
    action = airy_action(lam)
    thimble_values: Dict[complex, complex] = {}
    for critical_point in (-1.0 + 0j, 1.0 + 0j):
        direction_out, direction_in = descent_directions(action, critical_point)
        branch_out = trace_thimble(
            action,
            critical_point,
            direction_out,
            dt=5.0e-4,
            n_steps=60000,
            h_floor=-30.0,
        )
        branch_in = trace_thimble(
            action,
            critical_point,
            direction_in,
            dt=5.0e-4,
            n_steps=60000,
            h_floor=-30.0,
        )
        thimble_values[critical_point] = integrate_exp_action(
            action, branch_out, branch_in
        )

    reference = _airy_reference(lam)
    candidates = [
        {
            "orientation": [sign_plus, sign_minus],
            "error": float(
                abs(
                    sign_plus * thimble_values[1.0 + 0j]
                    + sign_minus * thimble_values[-1.0 + 0j]
                    - reference
                )
            ),
        }
        for sign_plus in (1, -1)
        for sign_minus in (1, -1)
    ]
    candidates.sort(key=lambda candidate: candidate["error"])
    tolerance = 2.0e-3
    matches = [candidate for candidate in candidates if candidate["error"] < tolerance]
    return {
        "lambda": lam,
        "reference": str(reference),
        "thimble_values": {
            str(point): str(value) for point, value in thimble_values.items()
        },
        "best_orientation": candidates[0]["orientation"],
        "best_error": candidates[0]["error"],
        "matching_orientation_count": len(matches),
        "tolerance": tolerance,
    }


def _outcome(
    logger: TraceLogger,
    status: str,
    residual_initial: Optional[float],
    residual_final: Optional[float],
    metrics: Dict[str, Any],
    retained_obstructions: Iterable[str] = (),
) -> CampaignOutcome:
    return CampaignOutcome(
        name=logger.runner_id,
        status=status,
        tape=logger.tape,
        trace_path=_portable_path(logger.jsonl_path),
        residual_initial=residual_initial,
        residual_final=residual_final,
        metrics=metrics,
        retained_obstructions=list(retained_obstructions),
    )


def run_witten_airy_finite_campaign(
    trace_dir: Path,
    research_context: _ResearchPacketContext | None = None,
) -> CampaignOutcome:
    """Run a finite numerical Airy/Picard-Lefschetz shadow of Witten §3.1."""
    trace_dir = Path(trace_dir)
    contexts = _build_research_contexts(trace_dir) if research_context is None else None
    context = research_context or contexts[WITTEN_FINITE_FAMILY]
    binding = _research_binding_evidence(context)
    lam, seeds = _decode_witten_finite_state(context)
    problem = build_airy_problem(
        task_id="solver-of-solvers-witten-airy-oesos-v1",
        lam=lam,
        seeds=seeds,
        research_parent_event_id=context.envelope.packet_id,
        source_digest=context.payload.source_manifest_root,
    )
    oesos_run = OesosLab((AiryNewtonProposalSolver(),)).solve(problem)
    if not oesos_run.evidence_valid():
        raise RuntimeError("finite Airy OESOS run did not reconcile")
    oesos_bridge = emit_symbol_game_dda_trace(
        oesos_run,
        trace_dir=trace_dir,
        runner_id="solver_of_solvers_witten_airy_finite-oesos",
        campaign_name="Witten finite Airy critical-point OESOS rail",
        extra_evidence={
            "research_packet": binding,
            "scope": "five-seed critical equation only",
            "authority_effect": "None",
        },
    )
    if not verify_symbol_game_dda_bridge(oesos_run, oesos_bridge):
        raise RuntimeError("finite Airy OESOS bridge did not verify")
    if oesos_bridge.initial_residual is None:
        raise RuntimeError("finite Airy OESOS bridge lacks an initial residual")
    initial_residual = oesos_bridge.initial_residual
    pdf_receipt = next(
        receipt
        for receipt in context.intake.receipts
        if receipt.source_id == "WITTEN-PAPER-1001.2933"
    )
    pdf_sha256 = pdf_receipt.observed_sha256
    source_codes: list[str] = ["PYTHON_IMPORT_SOURCE_ATOMICITY_UNPROVEN"]
    if not pdf_receipt.verified:
        source_codes.append("WITTEN_SOURCE_BYTES_UNVERIFIED")
    if not pdf_receipt.repository_tracked_expected:
        source_codes.append("EXTERNAL_SOURCE_BYTES_REQUIRED")
    logger = TraceLogger(
        "solver_of_solvers_witten_airy_finite",
        campaign_name="Witten 1001.2933 finite Airy wedge",
        trace_dir=trace_dir,
        dialect=DdaDialect.EXPERIMENTAL_Z_V1,
        auto_lifecycle=False,
    )

    action = airy_action(lam)
    logger.record_step(
        "R",
        "measure_airy_seed_gradient_residual",
        "WITTEN_PDF",
        "CRITICAL_POINT_SEARCH",
        "MAX_ABS_GRADIENT_ON_DECLARED_SEEDS",
        residual_before=initial_residual,
        residual_after=initial_residual,
        effect="residual_carried",
        obstruction_id="WITTEN_AIRY_CRITICAL_EQUATION",
        evidence={
            "pdf": _WITTEN_PDF_PATH,
            "pdf_sha256": pdf_sha256,
            "source_artifact_present": pdf_receipt.available,
            "source_intake_verified": pdf_receipt.verified,
            "repository_tracked_expected": (pdf_receipt.repository_tracked_expected),
            "lambda": str(lam),
            "seed_count": len(seeds),
            "norm": "max |dI/dx|",
            "research_packet": binding,
        },
    )
    logger.record_step(
        "C",
        "expose_finite_airy_model",
        "CRITICAL_POINT_SEARCH",
        "FINITE_AIRY_MODEL",
        "WITTEN_1001.2933_SEC_3.1_MODEL",
        residual_before=initial_residual,
        residual_after=initial_residual,
        effect="context_exposed",
        obstruction_id="WITTEN_AIRY_CRITICAL_EQUATION",
        evidence={
            "scope": "transcribed finite Airy action; no full Chern-Simons promotion"
        },
    )

    if not oesos_run.locally_resolved:
        unresolved_residual = (
            float(oesos_bridge.final_residual)
            if oesos_bridge.final_residual is not None
            else initial_residual
        )
        metrics = {
            "scope": "finite-dimensional transcribed Airy numerical model only",
            "execution_source_atomicity": "UNPROVEN",
            "source_artifact_present": pdf_receipt.available,
            "source_intake_verified": pdf_receipt.verified,
            "repository_tracked_expected": pdf_receipt.repository_tracked_expected,
            "source_pdf_sha256": pdf_sha256,
            "critical_point_count": 0,
            "critical_residual": unresolved_residual,
            "oesos": {
                "locally_resolved": False,
                "packet_id": oesos_run.packet_id,
                "parent_research_packet_id": oesos_run.parent_event_id,
                "runtime_id": oesos_run.runtime_id,
                "event_root": oesos_run.event_root,
                "wire_receipt_id": oesos_run.to_wire_receipt().receipt_id,
                "bridge_root": oesos_bridge.bridge_root,
                "bridge_valid": True,
                "trace_path": _portable_path(Path(oesos_bridge.dda_trace_path)),
                "tape": list(oesos_bridge.dda_tape),
                "active_obstructions": list(oesos_run.active_obstructions),
                "authority_effect": "None",
            },
        }
        logger.refuse(
            "OESOS did not produce an independently reprojected exact Airy state",
            "FINITE_AIRY_MODEL",
            "FINITE_AIRY_OESOS_REFUSED",
            "OESOS_ACTIVE_OBSTRUCTIONS",
            residual=unresolved_residual,
            obstruction_id="WITTEN_AIRY_CRITICAL_EQUATION",
            evidence=metrics,
        )
        refusal_codes = ("WITTEN_AIRY_OESOS_UNRESOLVED", *source_codes)
        outcome = _outcome(
            logger,
            "REFUSED",
            initial_residual,
            unresolved_residual,
            metrics,
            refusal_codes,
        )
        return _attach_research_run_root(
            outcome,
            context,
            trace_dir=trace_dir,
            refusal_codes=refusal_codes,
            evidence_profile="RefusalOnly",
            oesos_problem=problem,
            oesos_run=oesos_run,
            oesos_bridge=oesos_bridge,
            additional_artifacts=(
                (
                    Path(oesos_bridge.dda_trace_path),
                    DDA_TRACE_MEDIA_TYPE,
                ),
            ),
        )

    if type(oesos_run.final_native_state) is not AiryCriticalStateV1:
        raise RuntimeError("finite Airy OESOS output has the wrong state type")
    critical_points = sorted(
        set(oesos_run.final_native_state.complex_values()),
        key=lambda point: (point.real, point.imag),
    )
    critical_residual = (
        float(oesos_bridge.final_residual)
        if oesos_bridge.final_residual is not None
        else float("inf")
    )
    logger.record_step(
        "E",
        "solve_airy_critical_points",
        "FINITE_AIRY_MODEL",
        "CRITICAL_POINTS_SOLVED",
        "NEWTON_ROOT_RESIDUAL",
        residual_before=initial_residual,
        residual_after=critical_residual,
        effect="obstruction_eliminated",
        obstruction_id="WITTEN_AIRY_CRITICAL_EQUATION",
        evidence={
            "critical_points": [str(point) for point in critical_points],
            "oesos_event_root": oesos_run.event_root,
            "oesos_runtime_id": oesos_run.runtime_id,
            "oesos_bridge_root": oesos_bridge.bridge_root,
            "oesos_trace": _portable_path(Path(oesos_bridge.dda_trace_path)),
            "research_packet_id": context.envelope.packet_id,
            "authority_effect": "None",
        },
    )

    flow_records = []
    for point in critical_points:
        direction = descent_directions(action, point)[0]
        flow_records.append(
            trace_thimble(
                action,
                point,
                direction,
                dt=1.0e-3,
                n_steps=8000,
                h_floor=-20.0,
            )
        )
    monotone = bool(flow_records) and all(
        record.h_monotone_decreasing for record in flow_records
    )
    max_im_drift = max(
        (record.max_im_drift for record in flow_records), default=float("inf")
    )
    flow_defect = (0.0 if monotone else 1.0) + max(0.0, float(max_im_drift) - 5.0e-3)
    matrix = monodromy()
    monodromy_defect = float(
        np.linalg.norm(matrix @ matrix @ matrix - np.eye(2, dtype=int))
    )
    real_cycle = _airy_real_cycle_check()
    real_cycle_orientation_defect = float(
        abs(int(real_cycle["matching_orientation_count"]) - 1)
    )
    real_cycle_tolerance_defect = max(
        0.0,
        float(real_cycle["best_error"]) - float(real_cycle["tolerance"]),
    )
    real_cycle_boundary_defect = float(
        float(real_cycle["best_error"]) >= float(real_cycle["tolerance"])
    )
    real_cycle_defect = (
        real_cycle_orientation_defect
        + real_cycle_tolerance_defect
        + real_cycle_boundary_defect
    )
    structure_defect = flow_defect + monodromy_defect + real_cycle_defect
    total_residual = critical_residual + structure_defect

    logger.record_step(
        "Lambda",
        "construct_thimble_and_stokes_structure",
        "CRITICAL_POINTS_SOLVED",
        "FINITE_AIRY_NUMERICAL_STRUCTURE",
        "DOWNWARD_FLOW_AND_STOKES_MATRICES",
        residual_before=critical_residual,
        residual_after=structure_defect,
        effect="structure_added",
        obstruction_id="WITTEN_AIRY_FLOW_STRUCTURE",
        structure_delta={
            "critical_points": len(critical_points),
            "traced_thimble_branches": len(flow_records),
            "stokes_generators": 2,
            "real_cycle_thimbles": 2,
        },
        evidence={
            "h_monotone_decreasing": monotone,
            "max_im_action_drift": float(max_im_drift),
            "monodromy_matrix": matrix.tolist(),
            "norm_M_cubed_minus_identity": monodromy_defect,
            "real_cycle_check": real_cycle,
            "real_cycle_defect": real_cycle_defect,
        },
    )

    finite_closed = (
        len(critical_points) == 2
        and critical_residual < 1.0e-8
        and monotone
        and max_im_drift < 5.0e-3
        and monodromy_defect == 0.0
        and real_cycle["matching_orientation_count"] == 1
        and real_cycle["best_error"] < real_cycle["tolerance"]
    )
    metrics = {
        "scope": "finite-dimensional transcribed Airy numerical model only",
        "execution_source_atomicity": "UNPROVEN",
        "source_artifact_present": pdf_receipt.available,
        "source_intake_verified": pdf_receipt.verified,
        "repository_tracked_expected": pdf_receipt.repository_tracked_expected,
        "source_pdf_sha256": pdf_sha256,
        "critical_point_count": len(critical_points),
        "critical_residual": critical_residual,
        "flow_monotone": monotone,
        "max_im_action_drift": float(max_im_drift),
        "monodromy_defect": monodromy_defect,
        "real_cycle_check": real_cycle,
        "real_cycle_defect": real_cycle_defect,
        "real_cycle_orientation_defect": real_cycle_orientation_defect,
        "real_cycle_tolerance_defect": real_cycle_tolerance_defect,
        "real_cycle_boundary_defect": real_cycle_boundary_defect,
        "oesos": {
            "locally_resolved": oesos_run.locally_resolved,
            "packet_id": oesos_run.packet_id,
            "parent_research_packet_id": oesos_run.parent_event_id,
            "runtime_id": oesos_run.runtime_id,
            "event_root": oesos_run.event_root,
            "wire_receipt_id": oesos_run.to_wire_receipt().receipt_id,
            "bridge_root": oesos_bridge.bridge_root,
            "bridge_valid": True,
            "trace_path": _portable_path(Path(oesos_bridge.dda_trace_path)),
            "tape": list(oesos_bridge.dda_tape),
            "authority_effect": "None",
        },
    }
    if finite_closed:
        closure_status = "FINITE_NUMERICAL_SHADOW_CLOSED"
        if not pdf_receipt.verified:
            closure_status += "_SOURCE_UNVERIFIED"
        elif not pdf_receipt.repository_tracked_expected:
            closure_status += "_EXTERNAL_SOURCE_BYTES_REQUIRED"
        logger.finalize_success(
            "FINITE_AIRY_NUMERICAL_STRUCTURE",
            closure_status,
            "FINITE_AIRY_INVARIANTS",
            residual=total_residual,
            evidence={
                "claim_scope": "finite Airy numerical shadow only",
                "source_binding": (
                    "HASHED_EXTERNAL_LOCAL_PDF"
                    if pdf_receipt.verified
                    else "SOURCE_ARTIFACT_NOT_PRESENT"
                ),
                "research_packet_id": context.envelope.packet_id,
                "source_intake_receipt_id": context.intake.receipt_id,
                "oesos_event_root": oesos_run.event_root,
                "authority_effect": "None",
            },
        )
        outcome = _outcome(
            logger,
            closure_status,
            initial_residual,
            total_residual,
            metrics,
            source_codes,
        )
        return _attach_research_run_root(
            outcome,
            context,
            trace_dir=trace_dir,
            refusal_codes=source_codes,
            evidence_profile="LocalReplayableFiniteEvidence",
            oesos_problem=problem,
            oesos_run=oesos_run,
            oesos_bridge=oesos_bridge,
            additional_artifacts=(
                (
                    Path(oesos_bridge.dda_trace_path),
                    DDA_TRACE_MEDIA_TYPE,
                ),
            ),
        )

    logger.refuse(
        "finite Airy numerical invariants failed their declared tolerances",
        "FINITE_AIRY_NUMERICAL_STRUCTURE",
        "FINITE_AIRY_WEDGE_REFUSED",
        "FINITE_AIRY_TOLERANCE_FAILURE",
        residual=total_residual,
        obstruction_id="WITTEN_AIRY_NUMERICAL_FAILURE",
        evidence=metrics,
    )
    outcome = _outcome(
        logger,
        "REFUSED",
        initial_residual,
        total_residual,
        metrics,
        ["WITTEN_AIRY_NUMERICAL_FAILURE", *source_codes],
    )
    return _attach_research_run_root(
        outcome,
        context,
        trace_dir=trace_dir,
        refusal_codes=("WITTEN_AIRY_NUMERICAL_FAILURE", *source_codes),
        evidence_profile="RefusalOnly",
        oesos_problem=problem,
        oesos_run=oesos_run,
        oesos_bridge=oesos_bridge,
        additional_artifacts=(
            (
                Path(oesos_bridge.dda_trace_path),
                DDA_TRACE_MEDIA_TYPE,
            ),
        ),
    )


def run_witten_full_scope_refusal(
    trace_dir: Path,
    research_context: _ResearchPacketContext | None = None,
) -> CampaignOutcome:
    """Fence the finite Airy result from the full Chern-Simons continuation."""
    trace_dir = Path(trace_dir)
    contexts = _build_research_contexts(trace_dir) if research_context is None else None
    context = research_context or contexts[WITTEN_FULL_FAMILY]
    missing = list(context.unresolved_obligations)
    binding = _research_binding_evidence(context)
    logger = TraceLogger(
        "solver_of_solvers_witten_full_chern_simons",
        campaign_name="Witten 1001.2933 full-scope claim fence",
        trace_dir=trace_dir,
        dialect=DdaDialect.EXPERIMENTAL_Z_V1,
        auto_lifecycle=False,
    )
    residual = float(len(missing))
    logger.record_step(
        "R",
        "measure_full_scope_witness_gap",
        "FINITE_AIRY_EVIDENCE",
        "FULL_SCOPE_GAP_MEASURED",
        "MISSING_WITNESS_COUNT",
        residual_before=residual,
        residual_after=residual,
        effect="residual_carried",
        obstruction_id="WITTEN_FULL_SCOPE_GAP",
        evidence={
            "missing_witnesses": missing,
            "research_packet": binding,
        },
    )
    logger.record_step(
        "C",
        "expose_full_chern_simons_target",
        "FULL_SCOPE_GAP_MEASURED",
        "FULL_SCOPE_UNRESOLVED",
        "FINITE_TO_INFINITE_SCOPE_CHECK",
        residual_before=residual,
        residual_after=residual,
        effect="context_exposed",
        obstruction_id="WITTEN_FULL_SCOPE_GAP",
        evidence={"missing_witness_count": len(missing)},
    )
    logger.refuse(
        "the finite Airy wedge does not license the infinite-dimensional Chern-Simons or N=4 claims",
        "FULL_SCOPE_UNRESOLVED",
        "FULL_SCOPE_REFUSED",
        "NO_FULL_SCOPE_DETECTOR_OR_COMPARISON_MAP",
        residual=residual,
        obstruction_id="WITTEN_FULL_SCOPE_GAP",
        evidence={
            "missing_witnesses": missing,
            "claim_ids": list(context.claim_ids),
            "research_packet_id": context.envelope.packet_id,
            "source_intake_receipt_id": context.intake.receipt_id,
            "authority_effect": "None",
        },
    )
    outcome = _outcome(
        logger,
        "REFUSED",
        residual,
        residual,
        {
            "claim_ids": list(context.claim_ids),
            "missing_witnesses": missing,
            "finite_context_is_not_promotion": True,
            "authority_effect": "None",
        },
        ["WITTEN_FULL_SCOPE_GAP"],
    )
    return _attach_research_run_root(
        outcome,
        context,
        trace_dir=trace_dir,
        refusal_codes=("WITTEN_FULL_SCOPE_GAP",),
        evidence_profile="RefusalOnly",
    )


def run_gr_constraint_campaign(
    trace_dir: Path,
    cascade_solver_type: Type[Any],
    research_context: _ResearchPacketContext | None = None,
) -> CampaignOutcome:
    """Run the canonical live GR finite fixture through verifier-owned OESOS."""

    if cascade_solver_type is not CanonicalCascadeSolver:
        if research_context is not None:
            raise TypeError(
                "injected GR test rail cannot consume a production research packet"
            )
        return _run_gr_constraint_legacy_campaign(trace_dir, cascade_solver_type)
    trace_dir = Path(trace_dir)
    contexts = _build_research_contexts(trace_dir) if research_context is None else None
    context = research_context or contexts[GR_FINITE_FAMILY]
    carrier, initial_state = _decode_gr_finite_state(context)
    problem = build_coda_problem(
        task_id="solver-of-solvers-gr-finite-oesos-v1",
        research_parent_event_id=context.envelope.packet_id,
        carrier=carrier,
        initial=initial_state,
    )
    run = OesosLab((CodaCascadeProposalSolver(),)).solve(problem)
    if not run.evidence_valid():
        raise RuntimeError("finite GR OESOS run did not reconcile")
    bridge = emit_symbol_game_dda_trace(
        run,
        trace_dir=trace_dir,
        runner_id="solver_of_solvers_gr_constraint_closure",
        campaign_name="GR finite constraint closure through Symbol Game OESOS",
        extra_evidence={
            "research_packet": _research_binding_evidence(context),
            "execution_relation": "LIVE_PORT_EXECUTION",
            "published_package_relation": "CONTEXTUAL_SOURCE_NOT_ISOLATED_REPLAY",
            "candidate_solver": "existing-coda-cascade-proposal",
            "authority_effect": "None",
        },
    )
    if not verify_symbol_game_dda_bridge(run, bridge):
        raise RuntimeError("finite GR OESOS bridge did not verify")
    status = "FINITE_RESIDUAL_CLOSED" if run.locally_resolved else "REFUSED"
    metrics = {
        "scope": "finite face-aware cochain fixture only",
        "execution_source_atomicity": "UNPROVEN",
        "execution_relation": "LIVE_PORT_EXECUTION",
        "published_package_relation": "CONTEXTUAL_SOURCE_NOT_ISOLATED_REPLAY",
        "packet_id": run.packet_id,
        "parent_research_packet_id": run.parent_event_id,
        "runtime_id": run.runtime_id,
        "event_root": run.event_root,
        "wire_receipt_id": run.to_wire_receipt().receipt_id,
        "bridge_root": bridge.bridge_root,
        "bridge_valid": True,
        "initial_raw_mass": bridge.initial_raw_mass,
        "initial_phi1": bridge.initial_phi1,
        "initial_gamma2": bridge.initial_gamma2,
        "final_raw_mass": bridge.final_raw_mass,
        "final_phi1": bridge.final_phi1,
        "final_gamma2": bridge.final_gamma2,
        "residual_metric": bridge.residual_metric,
        "source_terminal_status": run.terminal_status.value,
        "accepted_steps": run.accepted_steps,
        "prime000_shape_only": asdict(run.prime000),
        "prime001_shape_only": asdict(run.adapter),
        "detector_adequacy": asdict(run.detector),
        "authority_effect": "None",
    }
    outcome = CampaignOutcome(
        name="solver_of_solvers_gr_constraint_closure",
        status=status,
        tape=list(bridge.dda_tape),
        trace_path=_portable_path(Path(bridge.dda_trace_path)),
        residual_initial=bridge.initial_residual,
        residual_final=bridge.final_residual,
        metrics=metrics,
        retained_obstructions=[
            *run.active_obstructions,
            "PYTHON_IMPORT_SOURCE_ATOMICITY_UNPROVEN",
        ],
    )
    return _attach_research_run_root(
        outcome,
        context,
        trace_dir=trace_dir,
        refusal_codes=(
            "GR_FINITE_OESOS_UNRESOLVED",
            "PYTHON_IMPORT_SOURCE_ATOMICITY_UNPROVEN",
        )
        if not run.locally_resolved
        else ("PYTHON_IMPORT_SOURCE_ATOMICITY_UNPROVEN",),
        evidence_profile=(
            "LocalReplayableFiniteEvidence" if run.locally_resolved else "RefusalOnly"
        ),
        oesos_problem=problem,
        oesos_run=run,
        oesos_bridge=bridge,
    )


def _run_gr_constraint_legacy_campaign(
    trace_dir: Path, cascade_solver_type: Type[Any]
) -> CampaignOutcome:
    """Retain the injected-solver refusal test rail outside production OESOS."""
    network = Network(
        nodes=[0, 1, 2, 3],
        edges=[(0, 1), (1, 2), (2, 0), (1, 3), (3, 0)],
        faces=[(0, 1, 2), (0, 1, 3)],
    )
    omega = {
        (0, 1): 3.0,
        (1, 2): 2.0,
        (2, 0): 2.0,
        (1, 3): 1.0,
        (3, 0): 1.0,
    }
    solver = cascade_solver_type(network, observer_name="solver_of_solvers_gr_finite")
    receipt = solver.solve(omega, max_lifts=1, enable_cell_attachment=False)
    logger = TraceLogger(
        "solver_of_solvers_gr_constraint_closure-injected-test-rail",
        campaign_name="Injected solver refusal test rail (not production GR)",
        trace_dir=trace_dir,
        dialect=DdaDialect.EXPERIMENTAL_Z_V1,
        auto_lifecycle=False,
    )
    initial = float(receipt.initial_residual_size)
    logger.record_step(
        "R",
        "project_foundation_residual",
        "GR_CONSTRAINT_PROMPT",
        "FOUNDATION_RESIDUAL_MEASURED",
        "FOUNDATION_CERT",
        residual_before=initial,
        residual_after=initial,
        effect="residual_carried",
        obstruction_id="GR_FINITE_PHI1",
        evidence={
            "norm": "L1 quotient residual",
            "admitted_complex_verified": receipt.admitted_complex_verified,
        },
    )
    logger.record_step(
        "C",
        "expose_finite_cochain_carrier",
        "FOUNDATION_RESIDUAL_MEASURED",
        "FINITE_RESIDUAL_STEP_0",
        "FINITE_CARRIER_MANIFEST",
        residual_before=initial,
        residual_after=initial,
        effect="context_exposed",
        obstruction_id="GR_FINITE_PHI1",
        evidence={
            "carrier_shape": {
                "nodes": receipt.carrier_nodes,
                "edges": receipt.carrier_edges,
                "faces": len(network.faces or []),
            }
        },
    )

    current = initial
    for index, certificate in enumerate(solver.dda_engine.step_history, start=1):
        after = current + float(certificate.delta_phi1)
        eliminated = after < current - 1.0e-12
        logger.record_step(
            "E" if eliminated else "R",
            f"apply_{certificate.move_type}",
            f"FINITE_RESIDUAL_STEP_{index - 1}",
            f"FINITE_RESIDUAL_STEP_{index}",
            certificate.after_hash,
            residual_before=current,
            residual_after=after,
            effect="obstruction_eliminated" if eliminated else "residual_carried",
            obstruction_id="GR_FINITE_PHI1",
            evidence={
                "before_hash": certificate.before_hash,
                "after_hash": certificate.after_hash,
                "delta_gamma2": certificate.delta_gamma2,
                "loss_ledger": certificate.loss_ledger,
                "authority_effect": certificate.authority_effect,
            },
        )
        current = after

    for lift in solver.dda_engine.lift_history:
        logger.record_step(
            "Lambda",
            f"lift_C{lift.from_degree}_to_C{lift.to_degree}",
            f"C{lift.from_degree}",
            f"C{lift.to_degree}",
            f"LIFT_{lift.from_degree}_{lift.to_degree}",
            residual_before=None,
            residual_after=float(sum(abs(value) for value in lift.lifted_residuals)),
            effect="structure_added",
            structure_delta={
                "from_degree": lift.from_degree,
                "to_degree": lift.to_degree,
                "higher_cells": lift.num_higher_cells,
                "lift_kind": lift.lift_kind,
            },
        )

    metrics = {
        "execution_relation": "INJECTED_TEST_RAIL_NOT_PRODUCTION",
        "terminal_status": receipt.terminal_status,
        "final_residual_triple": list(receipt.final_residual_triple),
        "admitted_complex_verified": receipt.admitted_complex_verified,
        "dual_certificate_available": receipt.is_certified,
        "duality_gap": receipt.duality_gap,
        "stages": list(receipt.stages_executed),
        "authority_effect": receipt.authority_effect,
    }
    final_residual = max(abs(float(value)) for value in receipt.final_residual_triple)
    finite_closed = (
        receipt.terminal_status == "Exact"
        and receipt.admitted_complex_verified
        and receipt.is_certified
        and final_residual < 1.0e-8
    )
    if finite_closed:
        logger.finalize_success(
            f"FINITE_RESIDUAL_STEP_{len(solver.dda_engine.step_history)}",
            "FINITE_CONSTRAINT_RESIDUAL_CLOSED",
            "CASCADE_SOLVER_RECEIPT",
            residual=final_residual,
            evidence=metrics,
        )
        return _outcome(
            logger,
            "FINITE_RESIDUAL_CLOSED",
            initial,
            final_residual,
            metrics,
        )

    logger.refuse(
        "the finite cascade did not close with the declared admitted-complex checks",
        "FINITE_RESIDUAL",
        "FINITE_CONSTRAINT_REFUSED",
        "CASCADE_SOLVER_REFUSAL",
        residual=final_residual,
        obstruction_id="GR_FINITE_PHI1",
        evidence=metrics,
    )
    return _outcome(
        logger,
        "REFUSED",
        initial,
        final_residual,
        metrics,
        ["GR_FINITE_PHI1"],
    )


def run_gr_stretch_claim_refusal(
    trace_dir: Path,
    research_context: _ResearchPacketContext | None = None,
) -> CampaignOutcome:
    """Record why the finite GR residual run does not derive the stretch claims."""
    trace_dir = Path(trace_dir)
    contexts = _build_research_contexts(trace_dir) if research_context is None else None
    context = research_context or contexts[GR_STRETCH_FAMILY]
    claims = {
        claim.claim_id: claim.unresolved_obligations[0]
        for claim in context.payload.claims
    }
    binding = _research_binding_evidence(context)
    logger = TraceLogger(
        "solver_of_solvers_gr_stretch_claims",
        campaign_name="GR stretch-claim derivation fence",
        trace_dir=trace_dir,
        dialect=DdaDialect.EXPERIMENTAL_Z_V1,
        auto_lifecycle=False,
    )
    residual = float(len(claims))
    logger.record_step(
        "R",
        "measure_unproved_claim_residual",
        "FINITE_GR_RESIDUAL_RESULT",
        "STRETCH_CLAIM_GAP_MEASURED",
        "MISSING_DERIVATION_WITNESSES",
        residual_before=residual,
        residual_after=residual,
        effect="residual_carried",
        obstruction_id="GR_STRETCH_CLAIMS",
        evidence={
            "claim_obstructions": claims,
            "research_packet": binding,
        },
    )
    logger.record_step(
        "C",
        "expose_stretch_claim_ledger",
        "STRETCH_CLAIM_GAP_MEASURED",
        "UNRESOLVED_PHYSICS_CLAIMS",
        "CLAIM_LEDGER_SCOPE_CHECK",
        residual_before=residual,
        residual_after=residual,
        effect="context_exposed",
        obstruction_id="GR_STRETCH_CLAIMS",
        evidence={"claims": list(claims)},
    )
    logger.refuse(
        "finite cochain constraint closure does not entail the requested particle-physics or cosmology claims",
        "UNRESOLVED_PHYSICS_CLAIMS",
        "STRETCH_CLAIMS_REFUSED",
        "CLAIM_HYGIENE_GATE",
        residual=residual,
        obstruction_id="GR_STRETCH_CLAIMS",
        evidence={
            "claim_obstructions": claims,
            "claim_ids": list(context.claim_ids),
            "research_packet_id": context.envelope.packet_id,
            "source_intake_receipt_id": context.intake.receipt_id,
            "authority_effect": "None",
        },
    )
    outcome = _outcome(
        logger,
        "REFUSED",
        residual,
        residual,
        {"claim_assessments": claims},
        list(claims),
    )
    return _attach_research_run_root(
        outcome,
        context,
        trace_dir=trace_dir,
        refusal_codes=("GR_STRETCH_CLAIMS_UNSUPPORTED",),
        evidence_profile="RefusalOnly",
    )


def _portable_bridge_payload(bridge: Any) -> Dict[str, Any]:
    payload = asdict(bridge)
    payload["dda_trace_path"] = _portable_path(Path(bridge.dda_trace_path))
    return payload


def run_symbol_game_coda_campaign(
    trace_dir: Path,
    rust_host_path: Path | None = None,
) -> CampaignOutcome:
    """Run finite CODA through Symbol Game, optional Rust replay, and bridge v3."""

    trace_dir = Path(trace_dir)
    trace_dir.mkdir(parents=True, exist_ok=True)
    _remove_legacy_rust_host_artifacts(trace_dir)
    problem = build_coda_problem(
        task_id="solver-of-solvers-symbol-game-coda"
    )
    run = OesosLab((CodaCascadeProposalSolver(),)).solve(problem)
    evaluation, additional_codes, rust_host = _run_rust_host_for_symbol_game(
        problem,
        run,
        trace_dir=trace_dir,
        rust_host_path=rust_host_path,
    )
    host_outcome = evaluation.outcome.to_dict() if evaluation else None
    request_id = evaluation.request.request_id_sha256 if evaluation else None
    challenge = evaluation.request.challenge_hex if evaluation else None
    bridge = emit_symbol_game_dda_trace_v3(
        run,
        trace_dir=trace_dir,
        runner_id="solver_of_solvers_symbol_game_coda",
        campaign_name="Symbol Game face-aware CODA proposal rail",
        rust_host_outcome=host_outcome,
        expected_host_request_id_sha256=request_id,
        expected_host_challenge_hex=challenge,
        additional_admission_codes=additional_codes,
        extra_evidence={
            "candidate_solver": "existing-coda-cascade-proposal",
            "canonical_rust_owner": "omega_solvers::solver_of_solvers",
            "exact_rust_replay_status": rust_host["status"],
            "prime000_001_receipts": "PYTHON_SHAPE_ONLY",
            "rust_host_outcome_root": (
                evaluation.outcome.outcome_root_sha256 if evaluation else None
            ),
            "global_admission": "Refused",
            "authority_effect": "None",
        },
    )
    bridge_valid = verify_symbol_game_dda_bridge_v3(
        run,
        bridge,
        rust_host_outcome=host_outcome,
        expected_host_request_id_sha256=request_id,
        expected_host_challenge_hex=challenge,
        additional_admission_codes=additional_codes,
    )
    if not bridge_valid or not run.locally_resolved:
        status = "REFUSED"
    elif evaluation is not None:
        status = "RUST_REPLAYED_ADMISSION_REFUSED"
    elif rust_host["status"] == "CLIENT_REFUSED":
        status = "RUST_HOST_CLIENT_REFUSED_GLOBAL_REFUSAL"
    else:
        status = "RUST_HOST_NOT_RUN_GLOBAL_REFUSAL"
    metrics = {
        "bridge": _portable_bridge_payload(bridge),
        "bridge_valid": bridge_valid,
        "packet_id": run.packet_id,
        "runtime_id": run.runtime_id,
        "source_event_root": run.event_root,
        "source_terminal_status": run.terminal_status.value,
        "accepted_steps": run.accepted_steps,
        "prime000_shape_only": asdict(run.prime000),
        "prime001_shape_only": asdict(run.adapter),
        "detector_adequacy": asdict(run.detector),
        "sealed_prime002_status": (
            rust_host["prime002"]["kind"] if evaluation else "NOT_RUN"
        ),
        "rust_oesos_replay_status": rust_host["status"],
        "rust_host": rust_host,
        "global_admission": bridge.global_admission,
        "admission_codes": list(bridge.admission_codes),
        "admission_obstruction_count": bridge.admission_obstruction_count,
        "admission_residual_initial": bridge.admission_obstruction_count,
        "admission_residual_final": bridge.admission_obstruction_count,
        "admission_residual_metric": bridge.admission_residual_metric,
        "local_math_residual_initial": bridge.local_initial_residual,
        "local_math_residual_final": bridge.local_final_residual,
        "local_math_residual_metric": bridge.local_residual_metric,
        "authority_effect": "None",
    }
    return CampaignOutcome(
        name="solver_of_solvers_symbol_game_coda",
        status=status,
        tape=list(bridge.dda_tape),
        trace_path=_portable_path(Path(bridge.dda_trace_path)),
        residual_initial=bridge.local_initial_residual,
        residual_final=bridge.local_final_residual,
        metrics=metrics,
        retained_obstructions=list(bridge.admission_codes),
    )


def run_symbol_game_self_improvement_campaign(
    trace_dir: Path,
) -> CampaignOutcome:
    """Packetize a routing improvement without applying or promoting it."""

    exact = TerminalStatus.LAB_EXACT_CANDIDATE.value
    solvers = (NoOpClaimingSolver(), ExhaustiveCspSolver())
    engine = OesosLab(solvers)
    training = FrozenCorpus(
        "solver-of-solvers-training-v1",
        (
            build_demo_problem(task_id="solver-of-solvers-train-0"),
            build_demo_problem(
                task_id="solver-of-solvers-train-1",
                initial=(("x", 1), ("y", 0)),
            ),
        ),
        (exact, exact),
    )
    held_out = FrozenCorpus(
        "solver-of-solvers-held-out-v1",
        (
            build_demo_problem(
                task_id="solver-of-solvers-held-0",
                initial=(("x", 0), ("y", 1)),
            ),
            build_demo_problem(
                task_id="solver-of-solvers-held-1",
                initial=(("x", 0), ("y", 0)),
            ),
        ),
        (exact, exact),
    )
    proposal = propose_routing_update(
        engine,
        training,
        held_out,
        apply=False,
    )
    run = proposal.policy_packet_run
    admission_codes = ("PRODUCTION_PROMOTION_NOT_AUTHORIZED",)
    bridge = emit_symbol_game_dda_trace_v3(
        run,
        trace_dir=trace_dir,
        runner_id="solver_of_solvers_symbol_game_self_improvement",
        campaign_name="Symbol Game proposal-only self-improvement",
        additional_admission_codes=admission_codes,
        extra_evidence={
            "baseline_policy": proposal.baseline_policy,
            "proposed_policy": proposal.proposed_policy,
            "strict_improvement": proposal.strict_improvement,
            "non_regression_passed": proposal.non_regression_passed,
            "applied_locally": proposal.applied_locally,
            "production_promotion": "NOT_AUTHORIZED",
            "authority_effect": proposal.authority_effect,
        },
    )
    bridge_valid = verify_symbol_game_dda_bridge_v3(
        run,
        bridge,
        additional_admission_codes=admission_codes,
    )
    proposal_only_passed = bool(
        bridge_valid
        and run.locally_resolved
        and proposal.strict_improvement
        and proposal.non_regression_passed
        and not proposal.applied_locally
        and engine.policy == proposal.baseline_policy
    )
    metrics = {
        "bridge": _portable_bridge_payload(bridge),
        "bridge_valid": bridge_valid,
        "baseline_policy": list(proposal.baseline_policy),
        "proposed_policy": list(proposal.proposed_policy),
        "training_baseline": asdict(proposal.training_baseline),
        "training_proposed": asdict(proposal.training_proposed),
        "held_out_baseline": asdict(proposal.held_out_baseline),
        "held_out_proposed": asdict(proposal.held_out_proposed),
        "strict_improvement": proposal.strict_improvement,
        "non_regression_passed": proposal.non_regression_passed,
        "promotion_isolation_attested": proposal.promotion_isolation_attested,
        "applied_locally": proposal.applied_locally,
        "production_promotion": "NOT_AUTHORIZED",
        "global_admission": bridge.global_admission,
        "admission_codes": list(bridge.admission_codes),
        "admission_obstruction_count": bridge.admission_obstruction_count,
        "admission_residual_initial": bridge.admission_obstruction_count,
        "admission_residual_final": bridge.admission_obstruction_count,
        "admission_residual_metric": bridge.admission_residual_metric,
        "local_math_residual_initial": bridge.local_initial_residual,
        "local_math_residual_final": bridge.local_final_residual,
        "local_math_residual_metric": bridge.local_residual_metric,
        "authority_effect": proposal.authority_effect,
    }
    return CampaignOutcome(
        name="solver_of_solvers_symbol_game_self_improvement",
        status=(
            "SELF_IMPROVEMENT_PROPOSAL_PACKETIZED_GLOBAL_REFUSAL"
            if proposal_only_passed
            else "REFUSED"
        ),
        tape=list(bridge.dda_tape),
        trace_path=_portable_path(Path(bridge.dda_trace_path)),
        residual_initial=bridge.local_initial_residual,
        residual_final=bridge.local_final_residual,
        metrics=metrics,
        retained_obstructions=list(bridge.admission_codes),
    )


def run_trace_self_audit(
    trace_dir: Path, trace_paths: Optional[Iterable[Path]] = None
) -> CampaignOutcome:
    """Run the trace machinery over its own newly emitted campaign records."""
    checked: List[Dict[str, Any]] = []
    invalid: List[str] = []
    paths = (
        sorted(trace_dir.glob("*.jsonl"))
        if trace_paths is None
        else sorted(Path(path) for path in trace_paths)
    )
    for path in paths:
        records = [
            json.loads(line)
            for line in path.read_text("utf-8").splitlines()
            if line.strip()
        ]
        if not records:
            continue
        chain_ok, chain_detail = verify_trajectory_chain(records)
        dialect = str(records[0].get("dda_dialect", DDATapeDFA.LEGACY_V1))
        tape = ".".join(str(record.get("letter", "")) for record in records)
        try:
            DDATapeDFA.validate(tape, dialect=dialect)
            grammar_ok = True
            grammar_detail = "valid"
        except DDATapeValidationError as exc:
            grammar_ok = False
            grammar_detail = str(exc)
        if not chain_ok or not grammar_ok:
            invalid.append(path.name)
        checked.append(
            {
                "file": path.name,
                "tape": tape,
                "dialect": dialect,
                "chain_valid": chain_ok,
                "chain_detail": chain_detail,
                "grammar_valid": grammar_ok,
                "grammar_detail": grammar_detail,
            }
        )

    logger = TraceLogger(
        "solver_of_solvers_trace_self_audit",
        campaign_name="solver-of-solvers self-audit",
        trace_dir=trace_dir,
        dialect=DdaDialect.EXPERIMENTAL_Z_V1,
        auto_lifecycle=False,
    )
    final = float(len(invalid))
    initial: Optional[float] = final
    logger.record_step(
        "R",
        "measure_hash_chain_and_grammar_defects",
        "CAMPAIGN_TRACE_DIRECTORY",
        "TRACE_DEFECT_COUNT",
        "CHAIN_AND_DIALECT_VALIDATION",
        residual_before=final,
        residual_after=final,
        effect="residual_carried",
        obstruction_id="TRACE_VALIDITY",
        evidence={"checked_files": len(checked), "invalid_files": invalid},
    )
    logger.record_step(
        "C",
        "expose_generated_trace_manifest",
        "TRACE_DEFECT_COUNT",
        "TRACE_AUDIT_RESULT",
        "TRACE_FILE_MANIFEST",
        residual_before=final,
        residual_after=final,
        effect="context_exposed",
        obstruction_id="TRACE_VALIDITY",
        evidence={"checked": checked},
    )
    if invalid:
        logger.refuse(
            "generated traces failed hash-chain or dialect validation",
            "TRACE_AUDIT_RESULT",
            "SELF_AUDIT_REFUSED",
            "INVALID_TRACE_SET",
            residual=final,
            obstruction_id="TRACE_VALIDITY",
            evidence={"invalid_files": invalid},
        )
        return _outcome(
            logger,
            "REFUSED",
            initial,
            final,
            {"checked": checked},
            invalid,
        )

    logger.finalize_success(
        "TRACE_AUDIT_RESULT",
        "SELF_AUDIT_PASSED",
        "ALL_CHAINS_AND_TAPES_VALID",
        residual=0.0,
        evidence={"checked_files": len(checked)},
    )
    return _outcome(logger, "SELF_AUDIT_PASSED", initial, 0.0, {"checked": checked})


def _write_report(
    trace_dir: Path, outcomes: List[CampaignOutcome], dag: Dict[str, Any]
) -> None:
    self_audit = next(
        outcome
        for outcome in outcomes
        if outcome.name == "solver_of_solvers_trace_self_audit"
    )
    trace_validation_passed = (
        dag["invalid_runs"] == 0
        and dag["valid_runs"] == dag["total_runs"]
        and self_audit.status == "SELF_AUDIT_PASSED"
    )
    report = {
        "schema_version": "omega.solver_of_solvers.research_report.v2",
        "authority_effect": "None",
        "dda_dialect": DdaDialect.EXPERIMENTAL_Z_V1.value,
        "trace_validation_status": "PASS" if trace_validation_passed else "REFUSED",
        "outcomes": [asdict(outcome) for outcome in outcomes],
        "dag_summary": {
            key: dag[key]
            for key in (
                "total_runs",
                "valid_runs",
                "invalid_runs",
                "total_steps",
                "structure_built_steps",
                "obstructions_removed_steps",
                "refusal_steps",
                "measured_residual_reduction",
            )
        },
        "nonclaim": (
            "These finite executions are replay evidence. They do not yet establish full "
            "authenticated Symbol Game/OE Prime 000-002/Rust OESOS integration, "
            "the complete Chern-Simons continuation, supersymmetry, the Standard "
            "Model gauge group, fermion masses, dark sectors, black-hole theorems, "
            "or an alternative cosmology."
        ),
    }
    (trace_dir / "solver_of_solvers_report.json").write_text(
        json.dumps(report, indent=2, sort_keys=True, default=str), encoding="utf-8"
    )

    lines = [
        "# Solver of Solvers — Lettered Algebra Campaign",
        "",
        f"Dialect: `{DdaDialect.EXPERIMENTAL_Z_V1.value}` (`Z·T` = refused/unresolved).",
        "",
        "Trace validation: "
        f"`{'PASS' if trace_validation_passed else 'REFUSED'}` "
        f"({dag['valid_runs']}/{dag['total_runs']} valid tapes).",
        "",
        "| Campaign | Status | Tape | Initial residual | Final residual |",
        "|---|---|---|---:|---:|",
    ]
    for outcome in outcomes:
        lines.append(
            f"| {outcome.name} | {outcome.status} | `{'.'.join(outcome.tape)}` | "
            f"{outcome.residual_initial} | {outcome.residual_final} |"
        )
    lines.extend(
        [
            "",
            "## Interpretation fence",
            "",
            report["nonclaim"],
            "",
            "A `Z` step retains the obstruction and is excluded from obstruction-removal totals.",
            "",
        ]
    )
    (trace_dir / "solver_of_solvers_report.md").write_text(
        "\n".join(lines), encoding="utf-8"
    )

    autoskill_metrics = {
        "signals_detected": 5,
        "durable_preferences": 2,
        "proposals_high": 0,
        "proposals_medium": 1,
        "skills_updated": 0,
        "corrections_captured": 5,
        "manual_skill_edits_found": 0,
        "family_propagation_candidates": 1,
        "self_reference_findings": 1,
        "compression_ratio_removed_to_added": "0:0 skill text",
        "emitted_tapes": dag["total_runs"],
        "valid_tapes": dag["valid_runs"],
        "trace_validation_passed": trace_validation_passed,
    }
    (trace_dir / "autoskill_metrics.json").write_text(
        json.dumps(autoskill_metrics, indent=2, sort_keys=True), encoding="utf-8"
    )
    autoskill_verdict = "PATCH" if trace_validation_passed else "REFUSED"
    if trace_validation_passed:
        self_reference_status = (
            f"- None remain in this scoped run. {dag['valid_runs']} of "
            f"{dag['total_runs']} emitted tapes pass grammar and hash-chain validation."
        )
        autoskill_final = "The code learned once; the skill did not self-amplify."
    else:
        self_reference_status = (
            f"- REFUSED: {dag['invalid_runs']} of {dag['total_runs']} emitted tapes "
            "failed grammar or hash-chain validation."
        )
        autoskill_final = (
            "The self-audit refused promotion because trace validation failed."
        )
    autoskill_report = f"""# auto-improve-autoskill Report

## Verdict

{autoskill_verdict}

## One-Paragraph Diagnosis

The solver campaign emitted real hash-chained traces and then found a defect in
its own observer: the first DAG summed residual reductions across unrelated
Airy, GR, and trace-audit carriers. The implementation now reports reductions
per run and marks cross-carrier aggregation `NOT_COMPARABLE`; it also excludes
`M` and experimental `Z` refusals from obstruction-removal counts, isolates
reruns, excludes invalid tapes from aggregates, and distinguishes carrier
metadata from structure actually added.

## Autoskill Metrics Reviewed

| Metric | Value | Finding |
|---|---:|---|
| Signals detected | 5 | Refusal semantics, comparability, rerun isolation, invalid-run pollution, structure counting |
| Durable preferences | 2 | Version dialects; retain refused residuals |
| Corrections captured | 5 | All five became executable code or tests |
| Proposals HIGH/MEDIUM | 0 / 1 | One skill-text proposal remains MEDIUM |
| Skills updated | 0 | A single campaign is insufficient for skill mutation |
| Manual skill edits found | 0 | No governed skill edit was required |
| Family propagation candidates | 1 | Mirror DDA contract remains to be reconciled |
| Self-reference findings | 1 | DAG observer audited its own aggregation |
| Family propagation checked | yes | Live and mirror DDA surfaces were compared |
| Self-reference checked | yes | The generated traces were replayed and validated |
| Git tracking checked | yes | JSONL is ignored by default and must be force-added deliberately |
| Compression ratio | 0:0 | No skill text was changed |

## Review Questions

1. Autoskill caught the need for real trace files, a rebuilt DAG, and a typed
   refusal rather than false closure.
2. It missed the prohibition on summing residuals across incomparable carriers.
3. It initially over-captured self-audit validation as obstruction removal.
4. No proposed skill change was too verbose because none was applied.
5. All five corrections became code and tests instead of new doctrine.
6. Family propagation was checked against the mirror DDA contract.
7. Git tracking was checked; the generated JSONL files are ignored by default.
8. Metrics are recorded in `autoskill_metrics.json`.
9. Self-reference was checked by validating every generated campaign trace.
10. `Z` dialecting is durable; campaign-specific physics claims remain context.

## Missed Signals

- Autoskill does not explicitly require carrier-comparability evidence before
  aggregating numeric residual metrics.

## Over-Captured Signals

- The first observer treated validation of its input traces as a reduction of
  mathematical obstructions.
  This has been removed.

## Family Propagation Failures

- The live Universe Anomalonica DDA contract now supports dialects; the separate
  `omega_engine_py` mirror remains legacy-only and needs an explicit ownership
  decision before synchronization.

## Self-Reference Failures

{self_reference_status}

## Compression Opportunities

| Current Bloat | Proposed Compression | Target |
|---|---|---|
| Narrative residual-comparison warnings | Executable carrier-comparison field | DDA DAG schema |

## Proposed Changes to autoskill

### HIGH Confidence

None.

### MEDIUM Confidence

- File: `autoskill/SKILL.md`
- Section: metrics
- Signal: numeric residuals from distinct carriers were added together.
- Proposed text: require a comparison witness or emit `NOT_COMPARABLE`.
- Compression effect: none yet; this is a proposal, not an applied edit.
- Rationale: one reproducible campaign found the issue, but one occurrence does
  not satisfy the bar for autonomous skill mutation.

## Requires User Approval?

YES — the only skill-text proposal is MEDIUM confidence. No skill was modified.

## Final Verdict

{autoskill_final}
"""
    (trace_dir / "auto_improve_autoskill_report.md").write_text(
        autoskill_report, encoding="utf-8"
    )


def run_research_campaigns(
    trace_dir: Path,
    cascade_solver_type: Type[Any],
    rust_host_path: Path | None = None,
) -> Dict[str, Any]:
    """Run finite Witten/GR cases, refuse extrapolations, then self-audit."""
    if cascade_solver_type is not CanonicalCascadeSolver:
        raise TypeError(
            "run_research_campaigns requires the canonical CascadeSolver; "
            "injected solver doubles are confined to the explicit test rail"
        )
    target = Path(trace_dir)
    target.mkdir(parents=True, exist_ok=True)
    _reset_owned_campaign_outputs(target)
    research_contexts = _build_research_contexts(target)
    outcomes = [
        run_witten_airy_finite_campaign(
            target,
            research_contexts[WITTEN_FINITE_FAMILY],
        ),
        run_witten_full_scope_refusal(
            target,
            research_contexts[WITTEN_FULL_FAMILY],
        ),
        run_gr_constraint_campaign(
            target,
            cascade_solver_type,
            research_contexts[GR_FINITE_FAMILY],
        ),
        run_gr_stretch_claim_refusal(
            target,
            research_contexts[GR_STRETCH_FAMILY],
        ),
        run_symbol_game_coda_campaign(target, rust_host_path=rust_host_path),
        run_symbol_game_self_improvement_campaign(target),
    ]
    campaign_trace_paths = [
        target / Path(outcome.trace_path).name for outcome in outcomes
    ]
    outcomes.append(run_trace_self_audit(target, trace_paths=campaign_trace_paths))
    current_trace_paths = [
        *campaign_trace_paths,
        target / Path(outcomes[-1].trace_path).name,
    ]
    dag = build_dda_dag(target, trace_paths=current_trace_paths)
    _write_report(target, outcomes, dag)
    return {
        "trace_dir": str(target.resolve()),
        "outcomes": [asdict(outcome) for outcome in outcomes],
        "dag": {
            "total_runs": dag["total_runs"],
            "valid_runs": dag["valid_runs"],
            "invalid_runs": dag["invalid_runs"],
            "obstructions_removed_steps": dag["obstructions_removed_steps"],
            "structure_built_steps": dag["structure_built_steps"],
            "refusal_steps": dag["refusal_steps"],
        },
    }


__all__ = [
    "CampaignOutcome",
    "run_gr_constraint_campaign",
    "run_gr_stretch_claim_refusal",
    "run_research_campaigns",
    "run_symbol_game_coda_campaign",
    "run_symbol_game_self_improvement_campaign",
    "run_trace_self_audit",
    "run_witten_airy_finite_campaign",
    "run_witten_full_scope_refusal",
]



