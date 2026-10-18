"""Focused production checks for the narrow SolverKernel v1.2 substrate."""

from dataclasses import FrozenInstanceError

import pytest

from omega_engine.crates.type.solver_kernel import (
    ManagedSolverOutput,
    ProofArtifactCandidate,
    SolverResult,
)


def test_managed_output_accepts_only_lifecycle_completion_states() -> None:
    result = SolverResult(payload={"candidate": 1})
    ManagedSolverOutput("inv", "request", "completed_with_output", result)

    for forbidden_judgment in ("Solved", "Accepted", "Refused"):
        with pytest.raises(ValueError):
            ManagedSolverOutput("inv", "request", forbidden_judgment, result)


def test_proof_artifact_candidate_cannot_self_verify() -> None:
    candidate = ProofArtifactCandidate(
        artifact_kind="eigenpair_candidate",
        claim_predicate_ref="urn:omega:claim:eigenpair",
        payload_hash="sha256:abc",
        generation_algorithm_ref="urn:omega:algorithm:spectral",
    )
    result = SolverResult(payload=1, proof_artifact_candidates=(candidate,))

    assert candidate.verification_status == "Unverified"
    assert candidate.evidence_class == "EvidenceOnly"
    assert candidate.authority_effect == "None"
    assert result.proof_artifact_candidates == (candidate,)
    with pytest.raises(TypeError):
        ProofArtifactCandidate(
            "kind", "claim", "hash", "algorithm", verification_status="Verified"
        )


def test_diagnostics_are_defensively_snapshotted() -> None:
    diagnostics = {"iterations": 3}
    result = SolverResult(payload=1, diagnostics=diagnostics)
    diagnostics["iterations"] = 99

    assert result.diagnostics == {"iterations": 3}
    with pytest.raises(TypeError):
        result.diagnostics["iterations"] = 4
    with pytest.raises(FrozenInstanceError):
        result.diagnostics = {}
