"""`RepairHintCandidateV1` -- the one type `EPIC-OE-IMMUNE-001` was missing.

Seven of the epic's eight declared types already existed in
`anti_skill_v2.py`. This was the eighth, and it is the one the epic's whole
argument turns on: the pharmacy's autoimmune failure was that a harvested defect
bundled a detector pattern *together with a repair action* and self-authorised
the pair. Splitting detection from repair is the fix, and the split needs a type
on the repair side that provably cannot cross back.

The epic states the requirement in one sentence: "an optional, separate
corrective proposal bound to an `AntiSkillHitV1`; it cannot alter the finding,
approve itself, or write."

Each clause is tested as a structural property rather than a convention:

- **bound** -- `hit_id` is the hit's content digest, and `from_hit` copies
  `protected_fields` off the hit rather than taking them from the caller.
- **cannot alter the finding** -- a target naming a protected field is refused
  at construction. The hit decides what is protected; the hint cannot narrow it.
- **cannot approve itself or write** -- there is no field to set, and
  `from_mapping` *refuses* a payload carrying one. `SPEC-OE-IMMUNE-001` requires
  rejection "at deserialization"; a filtered-out key is a silent downgrade,
  because the sender believed it granted approval and is never told otherwise.
"""

from __future__ import annotations

import pytest

from omega_engine.crates.prompt_civilization.domain.anti_skill_v2 import (
    AntiSkillHitV1,
)
from omega_engine.crates.prompt_civilization.domain.constants import (
    AUTHORITY_EFFECT_NONE,
)
from omega_engine.crates.prompt_civilization.domain.repair_hint_v1 import (
    REPAIR_HINT_FORBIDDEN_KEYS,
    REPAIR_HINT_SCHEMA_V1,
    RepairHintCandidateV1,
)

DIGEST = "sha256:" + "a" * 64


def make_hit(**overrides) -> AntiSkillHitV1:
    fields = {
        "spec_id": "spec_alpha",
        "failure_code": "code_beta",
        "disposition": "FINDING",
        "subject_id": DIGEST,
        "protected_fields": ("subject_id", "disposition"),
    }
    fields.update(overrides)
    return AntiSkillHitV1(**fields)




def test_a_candidate_carries_the_hit_digest_it_is_bound_to():
    hit = make_hit()
    candidate = RepairHintCandidateV1.from_hit(hit, "narrow the predicate")
    assert candidate.hit_id == hit.hit_id
    assert candidate.spec_id == hit.spec_id


def test_from_hit_copies_the_protection_set_off_the_hit():
    """The caller does not get to say what is protected.

    If `protected_fields` were a parameter, a hint could declare a smaller
    protection set than the finding it claims to serve and then target the
    difference.
    """
    hit = make_hit(protected_fields=("subject_id", "disposition", "spec_id"))
    candidate = RepairHintCandidateV1.from_hit(hit, "narrow it")
    assert candidate.protected_fields == hit.protected_fields


def test_binding_to_something_that_is_not_a_hit_is_refused():
    class LookalikeHit:
        hit_id = DIGEST
        spec_id = "spec_alpha"
        protected_fields = ()

    with pytest.raises(ValueError, match="exact AntiSkillHitV1"):
        RepairHintCandidateV1.from_hit(LookalikeHit(), "narrow it")


def test_a_hit_id_that_is_not_a_digest_is_refused():
    with pytest.raises(ValueError, match="hit_id"):
        RepairHintCandidateV1(
            hit_id="not-a-digest",
            spec_id="spec_alpha",
            suggestion="narrow it",
            protected_fields=(),
        )




def test_targeting_a_protected_field_is_refused():
    """The clause the epic states most plainly: "it cannot alter the finding"."""
    hit = make_hit()
    with pytest.raises(ValueError, match="protected field"):
        RepairHintCandidateV1.from_hit(hit, "overwrite it", ("disposition",))


def test_the_refusal_names_the_offending_field():
    hit = make_hit()
    with pytest.raises(ValueError, match="disposition"):
        RepairHintCandidateV1.from_hit(hit, "overwrite it", ("disposition",))


def test_every_protected_field_is_refused_not_only_the_first():
    """A loop that stopped at the first hit would pass a one-field test."""
    hit = make_hit(protected_fields=("alpha", "beta", "gamma"))
    for field in ("alpha", "beta", "gamma"):
        with pytest.raises(ValueError, match=field):
            RepairHintCandidateV1.from_hit(hit, "overwrite", (field,))


def test_an_unprotected_target_is_allowed():
    """The guard must be able to permit, or refusing proves nothing."""
    hit = make_hit()
    candidate = RepairHintCandidateV1.from_hit(hit, "raise it", ("threshold",))
    assert candidate.targets == ("threshold",)


def test_targets_default_to_empty():
    """A hint that names no field is prose, and prose is admissible."""
    candidate = RepairHintCandidateV1.from_hit(make_hit(), "consider rewording")
    assert candidate.targets == ()




@pytest.mark.parametrize(
    "key", ["approved", "approval", "admitted", "activation", "status", "patch"]
)
def test_an_approval_or_write_field_is_refused_at_deserialization(key):
    hit = make_hit()
    payload = {
        "hit_id": hit.hit_id,
        "spec_id": hit.spec_id,
        "suggestion": "narrow it",
        "protected_fields": (),
        key: True,
    }
    with pytest.raises(ValueError, match="may not carry"):
        RepairHintCandidateV1.from_mapping(payload)


def test_the_refusal_names_the_smuggled_key():
    hit = make_hit()
    with pytest.raises(ValueError, match="pharmacy_status"):
        RepairHintCandidateV1.from_mapping(
            {
                "hit_id": hit.hit_id,
                "spec_id": hit.spec_id,
                "suggestion": "x",
                "protected_fields": (),
                "pharmacy_status": "admitted",
            }
        )


def test_a_smuggled_key_is_refused_not_dropped():
    """The distinction the spec insists on.

    Dropping the key would construct a valid candidate and return it, and the
    caller who believed it had granted approval would never learn otherwise.
    """
    hit = make_hit()
    payload = {
        "hit_id": hit.hit_id,
        "spec_id": hit.spec_id,
        "suggestion": "x",
        "protected_fields": (),
        "approved": True,
    }
    with pytest.raises(ValueError):
        RepairHintCandidateV1.from_mapping(payload)


def test_an_unknown_field_is_refused():
    """Unknown-field rejection, as the spec requires of the sibling types."""
    hit = make_hit()
    with pytest.raises(ValueError, match="unknown fields"):
        RepairHintCandidateV1.from_mapping(
            {
                "hit_id": hit.hit_id,
                "spec_id": hit.spec_id,
                "suggestion": "x",
                "protected_fields": (),
                "novel_key": 1,
            }
        )


def test_a_clean_payload_parses():
    """`from_mapping` must be able to succeed, or its refusals prove nothing."""
    hit = make_hit()
    candidate = RepairHintCandidateV1.from_mapping(
        {
            "hit_id": hit.hit_id,
            "spec_id": hit.spec_id,
            "suggestion": "narrow the predicate",
            "protected_fields": ("subject_id",),
            "targets": ("threshold",),
        }
    )
    assert candidate.targets == ("threshold",)
    assert candidate.protected_fields == ("subject_id",)


def test_the_forbidden_key_set_covers_the_families_the_spec_names():
    """approval, activation, admission, status, and write/patch."""
    for key in ("approved", "activation", "admitted", "status", "patch", "write"):
        assert key in REPAIR_HINT_FORBIDDEN_KEYS




def test_authority_effect_is_none_and_anything_else_is_refused():
    hit = make_hit()
    candidate = RepairHintCandidateV1.from_hit(hit, "narrow it")
    assert candidate.authority_effect == AUTHORITY_EFFECT_NONE
    with pytest.raises(ValueError, match="authority_effect"):
        RepairHintCandidateV1(
            hit_id=hit.hit_id,
            spec_id=hit.spec_id,
            suggestion="narrow it",
            protected_fields=(),
            authority_effect="ACTION_LICENSE",
        )


def test_the_candidate_id_is_content_addressed():
    hit = make_hit()
    a = RepairHintCandidateV1.from_hit(hit, "narrow it", ("threshold",))
    b = RepairHintCandidateV1.from_hit(hit, "narrow it", ("threshold",))
    assert a.candidate_id == b.candidate_id
    c = RepairHintCandidateV1.from_hit(hit, "widen it", ("threshold",))
    assert c.candidate_id != a.candidate_id


def test_a_tampered_candidate_id_is_refused():
    hit = make_hit()
    good = RepairHintCandidateV1.from_hit(hit, "narrow it")
    with pytest.raises(ValueError, match="does not match canonical content"):
        RepairHintCandidateV1(
            hit_id=good.hit_id,
            spec_id=good.spec_id,
            suggestion=good.suggestion,
            protected_fields=good.protected_fields,
            candidate_id="sha256:" + "b" * 64,
        )


def test_an_unsupported_schema_version_is_refused():
    hit = make_hit()
    with pytest.raises(ValueError, match="schema"):
        RepairHintCandidateV1(
            hit_id=hit.hit_id,
            spec_id=hit.spec_id,
            suggestion="narrow it",
            protected_fields=(),
            schema_version="omega.antiskill.repair-hint-candidate.v2",
        )


def test_to_dict_round_trips_through_from_mapping():
    hit = make_hit()
    original = RepairHintCandidateV1.from_hit(hit, "narrow it", ("threshold",))
    restored = RepairHintCandidateV1.from_mapping(original.to_dict())
    assert restored == original


def test_the_type_is_exported_from_its_own_module():
    from omega_engine.crates.prompt_civilization.domain import repair_hint_v1

    assert "RepairHintCandidateV1" in repair_hint_v1.__all__
    assert REPAIR_HINT_SCHEMA_V1 == "omega.antiskill.repair-hint-candidate.v1"


def test_the_adjunct_is_not_inside_the_digest_bound_detection_module():
    """The reason this type lives in its own file.

    truth_boundary_canary.py stamps every canary spec with
    anti_skill_v2_implementation_digest(), a hash of that module's bytes.
    Adding this class there changed implementation_digest, cascaded into
    spec_digest, and invalidated committed admission evidence a human signed.
    Regenerating the canary to accommodate an unrelated change is the
    autoimmune failure IMMUNE-001 exists to prevent.
    """
    from omega_engine.crates.prompt_civilization.domain import anti_skill_v2

    assert "RepairHintCandidateV1" not in anti_skill_v2.__all__
    assert not hasattr(anti_skill_v2, "RepairHintCandidateV1")
