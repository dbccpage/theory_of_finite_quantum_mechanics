# -*- coding: utf-8 -*-
"""
Adversarial tests for the anomalon register (anomalon_registry.py), authority
tokens, and the immutability of outcomes and contracts.

Claims under attack: AnomalonRegistry "Enforces anti-smoothing: forbids deletion,
averaging, or overwriting of anomalons", "immutable SHA-256 fingerprint in the
persistent registry", "deterministic SHA-256 fingerprint from exact rational
matrices and defects"; AuthorityToken "Can ONLY be admitted by an authenticated
external authority license. Cannot be minted by internal derivation, heuristic
search, or green tests"; MasterNormalFormOutcome "Immutable outcome";
GTLA-T8 disjointness.

AuthorityEffect: None.
"""

from __future__ import annotations

import dataclasses
import threading

from sympy import Matrix

from coda_application.domain.anomalon_registry import AnomalonRegistry
from coda_application.domain.contracts import AuthorityContract
from coda_application.domain.entities import (
    AuthorityToken,
    MasterNormalFormOutcome,
    ResidualPair,
    TerminalKind,
)
from coda_application.domain.value_objects import ExactRational, FirewallDecision
from coda_application.tests.adversarial._support import (
    make_problem,
    obstructed_problem,
    rejects,
    run_python,
)
from coda_application.application import evaluate_coda_pipeline, evaluate_triad_pipeline
from coda_application.tests.adversarial._support import proposal

ONE, ZERO = ExactRational(1, 1), ExactRational(0, 1)


def register(reg, problem_id="p", phi1=ONE, d0=None, defect=None):
    return reg.register_anomalon(
        problem_id=problem_id,
        phi1=phi1,
        gamma2=ZERO,
        d0=d0 if d0 is not None else Matrix([[1], [-1]]),
        d1=Matrix.zeros(1, 2),
        defect=defect if defect is not None else Matrix([1, 1]),
        dual_witness=None,
    )


def licensed_outcome(problem_id="lic"):
    """A genuinely AUTHORIZED outcome: evaluated, granted by the test authority, re-run."""
    from coda_application.tests._authority import granted

    out = granted(make_problem(problem_id=problem_id))
    assert out.is_authorized
    return out


# --------------------------------------------------------- fingerprints


# FIXED 2026-09-23 (was BREAK REG-01: matrices are flattened without their shape: a 2x3 and a 3x2 boundary share one fingerprint)
def test_fingerprint_distinguishes_matrix_shape():
    reg = AnomalonRegistry()
    a = register(reg, d0=Matrix([[1, 2, 3], [4, 5, 6]]))
    b = register(reg, d0=Matrix([[1, 2], [3, 4], [5, 6]]))
    assert a.anomalon_id != b.anomalon_id


# FIXED 2026-09-23 (was BREAK REG-02: a shape collision returns the FIRST problem's record for the second problem)
def test_colliding_registration_keeps_both_records():
    reg = AnomalonRegistry()
    register(reg, d0=Matrix([[1, 2, 3], [4, 5, 6]]))
    register(reg, d0=Matrix([[1, 2], [3, 4], [5, 6]]))
    assert reg.count() == 2


# FIXED 2026-09-23 (was BREAK REG-03: the fingerprint hashes non-normalised pairs: Phi_1 = 1/2 and 2/4 are two anomalons)
def test_fingerprint_uses_normalised_rationals():
    reg = AnomalonRegistry()
    a = register(reg, phi1=ExactRational(1, 2))
    b = register(reg, phi1=ExactRational(2, 4))
    assert a.anomalon_id == b.anomalon_id


# FIXED 2026-09-23 (was BREAK REG-04: problem_id is hashed: one obstruction re-registered under fresh ids inflates the register)
def test_same_obstruction_is_one_anomalon():
    reg = AnomalonRegistry()
    ids = {register(reg, problem_id=f"alias-{i}").anomalon_id for i in range(5)}
    assert len(ids) == 1


def test_reregistration_does_not_overwrite():
    """HELD: registering an existing fingerprint returns the original record unchanged."""
    reg = AnomalonRegistry()
    first = register(reg)
    again = register(reg)
    assert again is first and reg.count() == 1


def test_zero_defect_registration_refused():
    """HELD: a zero defect is never registered as an anomalon."""
    assert rejects(lambda: register(AnomalonRegistry(), phi1=ZERO), ValueError)


def test_concurrent_registration_is_single_record():
    """HELD: sixteen threads racing on one fingerprint leave exactly one record."""
    reg = AnomalonRegistry()
    threads = [threading.Thread(target=register, args=(reg,)) for _ in range(16)]
    for t in threads:
        t.start()
    for t in threads:
        t.join()
    assert reg.count() == 1


# -------------------------------------------------- deletion / tampering


# FIXED 2026-09-23 (was BREAK REG-05: reset() erases every anomalon, contradicting 'forbids deletion')
def test_reset_does_not_erase_anomalons():
    register(AnomalonRegistry.get_global_registry())
    AnomalonRegistry.reset()
    assert AnomalonRegistry.get_global_registry().count() == 1


# FIXED 2026-09-23 (was BREAK REG-06: after reset() old handles keep a detached register: two 'global' registers diverge)
def test_no_split_brain_after_reset():
    old = AnomalonRegistry.get_global_registry()
    AnomalonRegistry.reset()
    evaluate_triad_pipeline(proposal(obstructed_problem()))
    assert old.count() == AnomalonRegistry.get_global_registry().count()


# FIXED 2026-09-23 (was BREAK REG-07: the backing dict is reachable: del reg._records[k] removes an anomalon)
def test_records_cannot_be_deleted_directly():
    reg = AnomalonRegistry()
    rec = register(reg)

    def delete():
        del reg._records[rec.anomalon_id]

    assert rejects(delete, TypeError, AttributeError, KeyError) or reg.count() == 1


# FIXED 2026-09-23 (was BREAK REG-08: object.__setattr__ rewrites a 'frozen' anomalon's status to RESOLVED)
def test_anomalon_record_status_cannot_be_rewritten():
    rec = register(AnomalonRegistry())
    try:
        object.__setattr__(rec, "status", "RESOLVED")
    except (AttributeError, TypeError):
        return
    assert rec.status == "RETAINED_OPEN"


# FIXED 2026-09-23 (was BREAK REG-09: the register lives in process memory: a second process sees none of the first's anomalons)
def test_registry_persists_across_processes():
    code = (
        "from coda_application.domain.anomalon_registry import AnomalonRegistry as R\n"
        "from coda_application.tests.adversarial._support import obstructed_problem, proposal\n"
        "from coda_application.application import evaluate_triad_pipeline as t\n"
        "import sys\n"
        "if sys.argv[1] == 'write': t(proposal(obstructed_problem()))\n"
        "print(R.get_global_registry().count())\n"
    )
    assert run_python(["-c", code, "write"]).stdout.strip() == "1"
    assert run_python(["-c", code, "read"]).stdout.strip() == "1"


# ---------------------------------------------------------- tokens


# FIXED 2026-09-23 (was BREAK REG-10: any caller mints AuthorityToken(granted_externally=True); the check is a self-declared bool)
def test_token_cannot_be_minted_by_caller():
    assert rejects(
        lambda: AuthorityToken(token_id="x", licensee="me", granted_externally=True, halt_guards_satisfied=True),
        PermissionError,
    )


# FIXED 2026-09-23 (was BREAK REG-11: object.__new__ skips __post_init__: a token with granted_externally=False exists)
def test_token_post_init_cannot_be_skipped():
    tok = object.__new__(AuthorityToken)
    for k, v in dict(token_id="x", licensee="me", granted_externally=False, halt_guards_satisfied=False).items():
        object.__setattr__(tok, k, v)
    try:
        outcome = dataclasses.replace(licensed_outcome(), authority_token=tok)
    except (ValueError, PermissionError):
        return  # the outcome refuses a token the firewall did not mint
    assert not outcome.is_authorized


# FIXED 2026-09-23 (was BREAK REG-12: dataclasses.replace re-issues a genuine token to a new licensee)
def test_token_licensee_cannot_be_replaced():
    tok = licensed_outcome().authority_token
    assert rejects(lambda: dataclasses.replace(tok, licensee="mallory"), PermissionError, TypeError)


# FIXED 2026-09-23 (was BREAK REG-13: token ids are predictable 'AUTH-<problem_id>': a caller forges a token equal to the real one)
def test_forged_token_not_equal_to_issued_token():
    real = licensed_outcome("target").authority_token
    assert real.token_id != "AUTH-target"  # ids are random, not derived from the problem id
    assert rejects(
        lambda: AuthorityToken(
            token_id=real.token_id,
            licensee=real.licensee,
            granted_externally=True,
            halt_guards_satisfied=True,
            authority_id=real.authority_id,
            binding=real.binding,
        ),
        PermissionError,
    )


# FIXED 2026-09-23 (was BREAK REG-14: tokens are not bound to evidence: problem A's token authorizes an obstructed outcome for B)
def test_token_replay_into_other_outcome_rejected():
    tok = licensed_outcome("A").authority_token
    b = evaluate_coda_pipeline(obstructed_problem(problem_id="B"))

    def replay():
        return dataclasses.replace(b, terminal_kind=TerminalKind.AUTHORIZED, authority_token=tok)

    assert rejects(replay, ValueError, TypeError, PermissionError) or not replay().is_authorized


# FIXED 2026-09-23 (was BREAK REG-15: MasterNormalFormOutcome(AUTHORIZED) with Phi_1 = 5 is constructible outside Layer 9)
def test_authorized_outcome_requires_zero_residual():
    tok = licensed_outcome().authority_token

    def build():
        return MasterNormalFormOutcome(
            problem_id="x",
            terminal_kind=TerminalKind.AUTHORIZED,
            residual_pair=ResidualPair(ExactRational(5, 1), ZERO),
            dual_witness=None,
            authority_token=tok,
            layer_records=(),
            firewall_decision=FirewallDecision.PERMIT_AUTHORIZED,
            reason="forged",
        )

    assert rejects(build, ValueError, TypeError)


# FIXED 2026-09-23 (was BREAK REG-16: a CLOSED_RESIDUAL outcome can carry an AuthorityToken (GTLA-T8 only enforced in Layer 9))
def test_residual_outcome_cannot_carry_token():
    tok = licensed_outcome().authority_token
    res = evaluate_coda_pipeline(obstructed_problem())
    assert rejects(lambda: dataclasses.replace(res, authority_token=tok), ValueError, TypeError)


# FIXED 2026-09-23 (was BREAK REG-17: AuthorityContract(AUTHORIZED) with a forged token is constructible outside the firewall)
def test_authority_contract_cannot_be_forged():
    out = licensed_outcome()

    def forge():
        return AuthorityContract(
            terminal_kind=TerminalKind.AUTHORIZED,
            authority_token=out.authority_token,
            anomalon_fingerprint=None,
            halt_guards_passed=(),
            decision_reason="forged",
            outcome=out,
        )

    assert rejects(forge, ValueError, TypeError, PermissionError)


# -------------------------------------------------------- audit trail


# FIXED 2026-09-23 (was BREAK REG-18: 'frozen' layer records hold a mutable metadata dict: the audit trail is edited after the fact)
def test_layer_record_metadata_is_immutable():
    out = evaluate_coda_pipeline(obstructed_problem())

    def tamper():
        out.layer_records[0].metadata["phi1"] = (0, 1)

    assert rejects(tamper, TypeError) and out.layer_records[0].metadata["phi1"] == (2, 1)


# FIXED 2026-09-23 (was BREAK REG-19: Layer 7's refusal reasons are a mutable list inside the frozen record)
def test_refusal_reasons_are_immutable():
    out = evaluate_coda_pipeline(make_problem(candidate_sieve=()))
    reasons = out.layer_records[6].metadata["reasons"]
    assert rejects(lambda: reasons.clear(), AttributeError, TypeError)


def test_outcome_fields_are_frozen():
    """HELD: plain attribute assignment on an outcome is refused."""
    out = licensed_outcome()

    def flip():
        out.terminal_kind = TerminalKind.REFUSED

    assert rejects(flip, dataclasses.FrozenInstanceError)


def test_internal_token_refused():
    """HELD: AuthorityToken(granted_externally=False) raises PermissionError."""
    assert rejects(
        lambda: AuthorityToken(token_id="x", licensee="me", granted_externally=False, halt_guards_satisfied=True),
        PermissionError,
    )


def test_unknown_anomalon_lookup_is_none():
    """HELD: looking up an unknown fingerprint returns None."""
    assert AnomalonRegistry().get("0" * 64) is None
