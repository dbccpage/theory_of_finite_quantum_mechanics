# -*- coding: utf-8 -*-
"""
test_review_regressions.py: Regression test suite for FDA peer review findings.

Verifies:
1. ExactnessCertificate.verify() float firewall and shape validation (P1).
2. evaluate_authority() compatibility entry certificate validation and strict boolean typing (P1).
3. Guard g5 candidate identity binding and count consistency (P2).
4. Circular re-export and import-order independence (P2).

AuthorityEffect: None.
"""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path

import pytest
from cochain_presentation import (
    ExactnessCertificate,
    LinearRepairProblem,
    QuotientDistanceCertificate,
)
from coda_fda_core import (
    DescentPacket,
    GuardEvidence,
    HaltGuards,
    RefusalCode,
    all_guards_true,
    derive_guards,
    evaluate_authority,
    evaluate_authorization,
)
from sympy import Float, ImmutableMatrix, Matrix, Rational


def _valid_packet() -> DescentPacket:
    return DescentPacket(
        carrier_k="carrier_test",
        evaluator_class_e=["c1", "c2"],
        verifier_v="verifier_v1",
        terminalizer_tau="tau_t",
        discipline_lambda="L_disc",
    )


# -----------------------------------------------------------------------------
# Finding 1: Membership certificates verify exactness without float leak (P1)
# -----------------------------------------------------------------------------
def test_exactness_certificate_rejects_float_and_sympy_float():
    """Reproduce Finding 1: N=2^60, repair_map=(1,1)^T, cochain=(N, N+1)^T, witness=Float(N, 15)."""
    n = 2**60
    repair_map = Matrix([[1], [1]])
    cochain = Matrix([[n], [n + 1]])

    # Float witness that would round to zero difference in float arithmetic
    float_witness = Matrix([Float(n, 15)])
    cert_float = ExactnessCertificate(
        is_exact_coboundary=True,
        cochain=cochain,
        repair_map=repair_map,
        witness=float_witness,
        separating_left_kernel_vector=None,
        separating_pairing=None,
    )
    assert cert_float.verify() is False, "ExactnessCertificate must reject SymPy Float witness"

    # Python float witness
    py_float_witness = Matrix([float(n)])
    cert_py_float = ExactnessCertificate(
        is_exact_coboundary=True,
        cochain=cochain,
        repair_map=repair_map,
        witness=py_float_witness,
        separating_left_kernel_vector=None,
        separating_pairing=None,
    )
    assert cert_py_float.verify() is False, "ExactnessCertificate must reject Python float witness"

    # Exact rational witness (which does not equal cochain, distance is 1)
    exact_witness = Matrix([n])
    cert_exact_wrong = ExactnessCertificate(
        is_exact_coboundary=True,
        cochain=cochain,
        repair_map=repair_map,
        witness=exact_witness,
        separating_left_kernel_vector=None,
        separating_pairing=None,
    )
    assert cert_exact_wrong.verify() is False, "ExactnessCertificate must reject false exactness claim"


def test_exactness_certificate_shape_and_immutability():
    """Test shape validation and immutability for ExactnessCertificate."""
    repair_map = Matrix([[1], [-1]])
    cochain = Matrix([[2], [-2]])
    exact_witness = Matrix([2])

    cert = ExactnessCertificate(
        is_exact_coboundary=True,
        cochain=cochain,
        repair_map=repair_map,
        witness=exact_witness,
        separating_left_kernel_vector=None,
        separating_pairing=None,
    )
    assert cert.verify() is True
    assert isinstance(cert.repair_map, ImmutableMatrix)
    assert isinstance(cert.cochain, ImmutableMatrix)
    assert isinstance(cert.witness, ImmutableMatrix)

    # Malformed shape
    bad_shape_cert = ExactnessCertificate(
        is_exact_coboundary=True,
        cochain=Matrix([[2, 2]]),  # 1x2 instead of 2x1
        repair_map=repair_map,
        witness=exact_witness,
        separating_left_kernel_vector=None,
        separating_pairing=None,
    )
    assert bad_shape_cert.verify() is False


# -----------------------------------------------------------------------------
# Finding 2: Compatibility evaluate_authority() validates certificates (P1)
# -----------------------------------------------------------------------------
def test_evaluate_authority_validates_certificate_and_distance():
    """Reproduce Finding 2: evaluate_authority must reject corrupted certs and distance mismatches."""
    packet = _valid_packet()
    guards = all_guards_true()

    # 1. Valid certificate whose residual distance is 2, with all-green guards (guards claim zero residual mass)
    d0 = Matrix([[1], [-1]])
    omega_dist2 = Matrix([[1], [1]])
    problem = LinearRepairProblem(d0)
    cert_dist2 = problem.quotient_l1_distance(omega_dist2)
    assert cert_dist2.distance == Rational(2, 1)
    assert cert_dist2.verify() is True

    res_dist_mismatch = evaluate_authority(
        "p_mismatch", packet, guards, residual_certificate=cert_dist2
    )
    assert res_dist_mismatch.inhabited is False
    assert res_dist_mismatch.refusal_code == RefusalCode.R_contradictory_evidence.value
    assert res_dist_mismatch.terminal_state == "term_failed_distance_mismatch"

    # 2. Corrupted certificate whose own verify() returns False
    corrupt_cert = QuotientDistanceCertificate(
        distance=Rational(0, 1),
        repair_witness=Matrix([0]),
        residual=Matrix([[0], [0]]),
        cochain=Matrix([[0], [0]]),
        dual_witness=Matrix([[99], [99]]),  # corrupted dual witness violating box bound
        dual_pairing=Rational(0, 1),
        repair_map=d0,
    )
    assert corrupt_cert.verify() is False

    res_corrupt = evaluate_authority(
        "p_corrupt", packet, guards, residual_certificate=corrupt_cert
    )
    assert res_corrupt.inhabited is False
    assert res_corrupt.refusal_code == RefusalCode.R_contradictory_evidence.value
    assert res_corrupt.terminal_state == "term_failed_invalid_certificate"

    # 3. String "False" in deterministic guard raises TypeError in HaltGuards constructor
    with pytest.raises(TypeError, match="must be strictly a bool"):
        HaltGuards(
            accepted=True,
            deterministic="False",  # string should not be truthy-coerced
            zero_residual_mass=True,
            skeleton_preserving=True,
            exhaustive=True,
            no_pending_lift=True,
            no_refusal=True,
        )

    # 4. Non-HaltGuards passed to evaluate_authority raises TypeError
    with pytest.raises(TypeError, match="must be a HaltGuards instance"):
        evaluate_authority("p_bad", packet, guards="all_true")


# -----------------------------------------------------------------------------
# Finding 3: Guard g5 binds evidence to candidate identities (P2)
# -----------------------------------------------------------------------------
def test_g5_requires_matching_candidate_ids_for_declared_packet():
    """Reproduce Finding 3: omitting candidate IDs cannot satisfy exhaustiveness for declared packet."""
    packet = _valid_packet()  # evaluator_class_e=["c1", "c2"]

    # 1. Omitting checked_candidate_ids falls back to non-exhaustive when packet is declared
    evidence_no_ids = GuardEvidence(
        pipeline_accepted=True,
        replay_deterministic=True,
        residual_mass=Rational(0, 1),
        skeleton_preserved=True,
        candidates_checked=2,
        candidates_declared=2,
        checked_candidate_ids=None,
    )
    guards = derive_guards(evidence_no_ids, packet)
    assert guards.exhaustive is False, "omitting candidate IDs must not authorize declared packet"
    res = evaluate_authorization("p1", packet, evidence_no_ids)
    assert res.inhabited is False
    assert res.refusal_code == RefusalCode.R_candidate.value

    # 2. Reusing evidence with candidate IDs ["other1", "other2"] against packet ["c1", "c2"]
    evidence_diff_ids = GuardEvidence(
        pipeline_accepted=True,
        replay_deterministic=True,
        residual_mass=Rational(0, 1),
        skeleton_preserved=True,
        candidates_checked=2,
        candidates_declared=2,
        checked_candidate_ids=["other1", "other2"],
    )
    guards_diff = derive_guards(evidence_diff_ids, packet)
    assert guards_diff.exhaustive is False, "evidence for different candidates must not authorize"

    # 3. Supplying matching IDs but inconsistent counts (e.g. candidates_checked=0)
    with pytest.raises(ValueError, match="does not match length of checked_candidate_ids"):
        GuardEvidence(
            pipeline_accepted=True,
            replay_deterministic=True,
            residual_mass=Rational(0, 1),
            skeleton_preserved=True,
            candidates_checked=0,
            candidates_declared=0,
            checked_candidate_ids=["c1", "c2"],
        )

    # 4. Zero declared and checked with empty candidate IDs does not authorize
    evidence_zero = GuardEvidence(
        pipeline_accepted=True,
        replay_deterministic=True,
        residual_mass=Rational(0, 1),
        skeleton_preserved=True,
        candidates_checked=0,
        candidates_declared=0,
        checked_candidate_ids=(),
    )
    guards_zero = derive_guards(evidence_zero, packet)
    assert guards_zero.exhaustive is False

    # 5. Matching IDs and consistent counts authorize successfully
    evidence_matching = GuardEvidence(
        pipeline_accepted=True,
        replay_deterministic=True,
        residual_mass=Rational(0, 1),
        skeleton_preserved=True,
        candidates_checked=2,
        candidates_declared=2,
        checked_candidate_ids=["c1", "c2"],
    )
    guards_matching = derive_guards(evidence_matching, packet)
    assert guards_matching.exhaustive is True
    res_ok = evaluate_authorization("p_ok", packet, evidence_matching)
    assert res_ok.inhabited is True


# -----------------------------------------------------------------------------
# Finding 4: Circular re-exports and import-order independence (P2)
# -----------------------------------------------------------------------------
def test_import_order_independence():
    """Reproduce Finding 4: importing pipeline first, then SealedPipeline from core, must succeed."""
    pkg_code_dir = str(Path(__file__).resolve().parent.parent)

    cmd_pipeline_first = [
        sys.executable,
        "-c",
        (
            f"import sys; sys.path.insert(0, r'{pkg_code_dir}'); "
            "import coda_fda_pipeline; "
            "from coda_fda_core import SealedPipeline; "
            "assert SealedPipeline is not None; print('OK')"
        ),
    ]
    proc1 = subprocess.run(cmd_pipeline_first, capture_output=True, text=True)
    assert proc1.returncode == 0, f"pipeline-first import failed:\nSTDOUT:\n{proc1.stdout}\nSTDERR:\n{proc1.stderr}"
    assert "OK" in proc1.stdout

    cmd_core_first = [
        sys.executable,
        "-c",
        (
            f"import sys; sys.path.insert(0, r'{pkg_code_dir}'); "
            "from coda_fda_core import SealedPipeline; "
            "import coda_fda_pipeline; "
            "assert SealedPipeline is not None; print('OK')"
        ),
    ]
    proc2 = subprocess.run(cmd_core_first, capture_output=True, text=True)
    assert proc2.returncode == 0, f"core-first import failed:\nSTDOUT:\n{proc2.stdout}\nSTDERR:\n{proc2.stderr}"
    assert "OK" in proc2.stdout
