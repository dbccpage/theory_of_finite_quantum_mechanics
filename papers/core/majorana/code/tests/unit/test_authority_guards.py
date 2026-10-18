from __future__ import annotations
"""M5 + M6 — IsAuth seven-guard conjunction and the T39 non-parenting mirror.

THEORETICAL MINIMUM (M6)
  INVARIANT  is_auth is the conjunction of seven descent guards over a typed
             AuthorityTerminal + AuthorityDescentState; ONE false guard kills
             it; malformed inputs never pass (fail-closed).
  BREAK      Any single guard dropped from the conjunction admits its row.
  WITNESS    The 7-row single-false-guard matrix, each row flipping exactly
             one guard of an otherwise all-true state.
  MUTATION   Delete `descent_state.human_promoted` from the all() tuple in
             omega_types.terminal.is_auth -> that row goes red.

THEORETICAL MINIMUM (M5)
  INVARIANT  T39 mirror: a certificate-shaped structure terminal never
             parents authority — authority_from_outcome returns None for
             every non-AuthorityTerminal outcome, and CertifiedAuthority
             .certify refuses non-authority terminals in type.
  BREAK      A StructureDerived carrying a Lean certificate is laundered
             into a CertifiedAuthority.
  WITNESS    authority_from_outcome(...) is None; ValueError from certify.
  MUTATION   In omega_types.outcome.authority_from_outcome, return a forged
             CertifiedAuthority.__new__ sentinel on the non-authority branch
             -> the None assertions go red.

AuthorityEffect: None throughout.
"""


import dataclasses

import pytest

from omega_engine.crates.replay import DescentWitness, ReplayTracePacket
from omega_engine.crates.type.outcome import CertifiedAuthority, authority_from_outcome
from omega_engine.crates.type.refusal import Refusal
from omega_engine.crates.type.terminal import (
    AuthorityDescentState,
    AuthorityTerminal,
    RefusedFormalism,
    ScopedNegative,
    StructureDerived,
    is_auth,
)


def _packet() -> ReplayTracePacket:
    return ReplayTracePacket(
        paper_sha256="a" * 64,
        proposal_sha256="b" * 64,
        gate_receipt_sha256="c" * 64,
        loop_pass=1,
        step_index=1,
        status="CheckPassed",
    )


def _witness() -> DescentWitness:
    packet = _packet()
    return DescentWitness.from_verified_replay(packet, packet.replay_hash)


def _all_true_state(replay_hash: str | None = None) -> AuthorityDescentState:
    return AuthorityDescentState(
        replay_hash=replay_hash if replay_hash is not None else _packet().replay_hash,
        deterministic=True,
        phi1=0,
        exhaustive=True,
        skeleton_aligned=True,
        lift_required=False,
        has_refusal=False,
        human_promoted=True,
    )


def _terminal() -> AuthorityTerminal:
    return AuthorityTerminal("exact_rule_derived", evidence_level=3)


class TestIsAuthSevenGuardMatrix:
    """M6: seven rows, each flipping exactly one guard (Landau class 2)."""

    def test_all_seven_guards_true_passes(self) -> None:
        assert is_auth(_terminal(), _all_true_state()) is True

    @pytest.mark.parametrize(
        "single_false_override",
        [
            {"deterministic": False},
            {"phi1": 1},
            {"exhaustive": False},
            {"skeleton_aligned": False},
            {"lift_required": True},
            {"has_refusal": True},
            {"human_promoted": False},
        ],
        ids=lambda ov: next(iter(ov.items()))[0],
    )
    def test_each_single_false_guard_kills_the_conjunction(
        self, single_false_override: dict
    ) -> None:
        state = dataclasses.replace(_all_true_state(), **single_false_override)
        assert is_auth(_terminal(), state) is False

    @pytest.mark.parametrize(
        "bad_terminal",
        [
            None,
            "AuthorityTerminal",
            StructureDerived("lean4", certificate={"theorem": "T39"}),
            RefusedFormalism("lean4", "no descent"),
        ],
    )
    def test_non_authority_terminal_never_passes(self, bad_terminal) -> None:
        assert is_auth(bad_terminal, _all_true_state()) is False

    @pytest.mark.parametrize("bad_state", [None, "state", {"deterministic": True}, 42])
    def test_missing_or_untyped_state_never_passes(self, bad_state) -> None:
        assert is_auth(_terminal(), bad_state) is False

    @pytest.mark.parametrize(
        "bad_hash",
        ["", "xyz", "A" * 64, "a" * 63, "a" * 65, "g" * 64],
    )
    def test_malformed_replay_hash_never_passes(self, bad_hash: str) -> None:
        state = dataclasses.replace(_all_true_state(), replay_hash=bad_hash)
        assert is_auth(_terminal(), state) is False

    def test_empty_token_or_missing_evidence_level_never_passes(self) -> None:
        assert is_auth(AuthorityTerminal("", 3), _all_true_state()) is False
        assert is_auth(AuthorityTerminal("tok", None), _all_true_state()) is False


class TestT39CertificateNeverParentsAuthority:
    """M5: the certificate-shaped outcome is structurally barred (Landau class 2)."""

    def test_structure_derived_with_certificate_yields_none(self) -> None:
        witness = _witness()
        state = _all_true_state(replay_hash=witness.replay_hash)
        outcome = StructureDerived(
            "lean4", certificate={"theorem": "T39", "axioms": ["propext"]}
        )
        assert authority_from_outcome(outcome, witness, state) is None

    @pytest.mark.parametrize(
        "non_authority_outcome",
        [
            ScopedNegative("lean4", "no applicable rule"),
            RefusedFormalism("lean4", "parse refused"),
            Refusal("typed refusal"),
        ],
        ids=["scoped_negative", "refused_formalism", "refusal"],
    )
    def test_every_non_authority_outcome_yields_none(
        self, non_authority_outcome
    ) -> None:
        witness = _witness()
        state = _all_true_state(replay_hash=witness.replay_hash)
        assert authority_from_outcome(non_authority_outcome, witness, state) is None

    def test_certify_refuses_non_authority_terminal_in_type(self) -> None:
        witness = _witness()
        state = _all_true_state(replay_hash=witness.replay_hash)
        structure = StructureDerived("lean4", certificate={"theorem": "T39"})
        with pytest.raises(ValueError, match="does not satisfy the authority guards"):
            CertifiedAuthority.certify(structure, witness, state)

    def test_certify_refuses_witness_that_is_not_a_descent_witness(self) -> None:
        state = _all_true_state()
        with pytest.raises(TypeError, match="requires a DescentWitness"):
            CertifiedAuthority.certify(_terminal(), "not a witness", state)

    def test_certify_refuses_state_not_bound_to_the_witness(self) -> None:
        witness = _witness()
        state = dataclasses.replace(
            _all_true_state(replay_hash=witness.replay_hash), replay_hash="d" * 64
        )
        with pytest.raises(ValueError, match="not bound to the replay witness"):
            CertifiedAuthority.certify(_terminal(), witness, state)

    def test_all_guards_true_still_ends_at_the_host_permission_wall(self) -> None:
        # Even the fully-guarded authority terminal cannot certify locally;
        # authority_from_outcome absorbs the PermissionError into None.
        witness = _witness()
        state = _all_true_state(replay_hash=witness.replay_hash)
        assert is_auth(_terminal(), state) is True
        assert authority_from_outcome(_terminal(), witness, state) is None


class TestCertifiedAuthoritySealedConstruction:
    """P1 SECURITY repair: the live-forgeable ``_secret_key`` class attribute
    is now name-mangled. Before this repair, a reviewer live-forged
    ``CertifiedAuthority(CertifiedAuthority._secret_key, "FAKE_TERMINAL",
    "FAKE_WITNESS")`` and it constructed, completely bypassing
    ``certify()``'s always-refuse host law.
    """

    def test_old_unmangled_secret_key_attribute_no_longer_exists(self) -> None:
        # The forgery path the reviewer used: reading the plain class
        # attribute to smuggle in the sentinel. It must not resolve.
        with pytest.raises(AttributeError):
            CertifiedAuthority._secret_key  # type: ignore[attr-defined]

    def test_direct_construction_with_forged_sentinel_is_refused(self) -> None:
        with pytest.raises(TypeError, match="sealed"):
            CertifiedAuthority(object(), "FAKE_TERMINAL", "FAKE_WITNESS")

    def test_direct_construction_with_none_key_is_refused(self) -> None:
        with pytest.raises(TypeError, match="sealed"):
            CertifiedAuthority(None, "FAKE_TERMINAL", "FAKE_WITNESS")

    def test_mangled_key_path_is_the_documented_best_effort_boundary(self) -> None:
        # The technically-still-reachable path (Python has no private
        # fields): a determined caller can dig out the name-mangled
        # attribute directly. This is the SAME honesty level as GtlaNf and
        # DescentWitness (Inspector M18) — best-effort, not cryptographic.
        # It is exercised here only to document the boundary, not to
        # endorse it as a legitimate construction route.
        mangled_key = CertifiedAuthority._CertifiedAuthority__sealed_key
        forged = CertifiedAuthority(mangled_key, "FAKE_TERMINAL", "FAKE_WITNESS")
        assert forged.terminal == "FAKE_TERMINAL"
        assert forged.witness == "FAKE_WITNESS"


