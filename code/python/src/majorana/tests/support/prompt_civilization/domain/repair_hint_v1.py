"""The repair-hint adjunct, deliberately outside `anti_skill_v2`.

`EPIC-OE-IMMUNE-001` names this type once and precisely: "Only two possible
adjuncts remain. `RepairHintCandidateV1` is an optional, separate corrective
proposal bound to an `AntiSkillHitV1`; it cannot alter the finding, approve
itself, or write."

**Why it lives in its own module.** It was first written into
`anti_skill_v2.py` beside the type it binds to, and that broke the committed
truth-boundary canary. `truth_boundary_canary.py` stamps every canary spec with
`anti_skill_v2_implementation_digest()`, a hash of that module's bytes, so
adding *any* code to it changes `implementation_digest`, cascades into
`spec_digest`, and invalidates admission evidence a human signed.

The repair was not to regenerate the canary. Re-stamping committed admission
evidence to accommodate an unrelated code change is exactly the autoimmune
failure this epic exists to prevent -- an automated tool re-authorising the
record that authorises it. The estate's own integrity mechanism caught the
mistake, and the epic's own wording already said the answer: *separate*.

So detection's implementation digest stays stable, and the adjunct sits beside
it rather than inside it.

The three prohibitions are structural here, not conventions:

- **bound** -- `hit_id` is the hit's content digest, and `from_hit` copies
  `protected_fields` off the hit rather than accepting them from a caller.
- **cannot alter the finding** -- a target naming a protected field is refused
  at construction. The hit decides what is protected; the hint cannot narrow it.
- **cannot approve itself or write** -- there is no approval, activation, status
  or patch field to set, and `from_mapping` refuses a payload carrying one.
  `SPEC-OE-IMMUNE-001` requires that rejection "at deserialization": a
  filtered-out key is a silent downgrade, because the sender believed it granted
  approval and is never told otherwise.

Enacting a hint is out of scope for this epic and has no code path here.

AuthorityEffect: None.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Mapping

from .anti_skill_v2 import (
    AntiSkillHitV1,
    _digest,
    _identifier,
    _semantic_id,
    _string_tuple,
    _text,
)
from .constants import AUTHORITY_EFFECT_NONE

REPAIR_HINT_SCHEMA_V1 = "omega.antiskill.repair-hint-candidate.v1"

# Field names a repair hint may never carry, refused rather than dropped.
REPAIR_HINT_FORBIDDEN_KEYS = frozenset(
    {
        "action",
        "activation",
        "activation_profile",
        "active",
        "admission",
        "admitted",
        "apply",
        "approval",
        "approved",
        "authority",
        "authorized",
        "diff",
        "enact",
        "license",
        "patch",
        "path",
        "pharmacy_status",
        "replacement",
        "status",
        "write",
    }
)

REPAIR_HINT_KNOWN_KEYS = frozenset(
    {
        "authority_effect",
        "candidate_id",
        "hit_id",
        "protected_fields",
        "schema_version",
        "spec_id",
        "suggestion",
        "targets",
    }
)


@dataclass(frozen=True, slots=True)
class RepairHintCandidateV1:
    """An inert corrective proposal bound to a hit."""

    hit_id: str
    spec_id: str
    suggestion: str
    protected_fields: tuple[str, ...]
    targets: tuple[str, ...] = ()
    authority_effect: str = AUTHORITY_EFFECT_NONE
    schema_version: str = REPAIR_HINT_SCHEMA_V1
    candidate_id: str = ""

    def __post_init__(self) -> None:
        _digest(self.hit_id, "hit_id")
        _identifier(self.spec_id, "spec_id")
        _text(self.suggestion, "suggestion")
        object.__setattr__(
            self,
            "protected_fields",
            _string_tuple(self.protected_fields, "protected_fields", identifiers=True),
        )
        object.__setattr__(
            self,
            "targets",
            _string_tuple(self.targets, "targets", identifiers=True),
        )
        overlap = sorted(set(self.targets) & set(self.protected_fields))
        if overlap:
            raise ValueError(
                "repair hint targets a protected field: " + ", ".join(overlap)
            )
        if self.authority_effect != AUTHORITY_EFFECT_NONE:
            raise ValueError("repair hint candidate authority_effect must be None")
        if self.schema_version != REPAIR_HINT_SCHEMA_V1:
            raise ValueError("unsupported repair hint candidate schema")
        expected = _semantic_id(REPAIR_HINT_SCHEMA_V1, self._payload())
        if self.candidate_id and self.candidate_id != expected:
            raise ValueError("candidate_id does not match canonical content")
        object.__setattr__(self, "candidate_id", expected)

    @classmethod
    def from_hit(
        cls,
        hit: AntiSkillHitV1,
        suggestion: str,
        targets: tuple[str, ...] = (),
    ) -> "RepairHintCandidateV1":
        """Bind a candidate to a hit, taking the hit's protection set verbatim.

        `protected_fields` is copied off the hit rather than passed in, so a
        caller cannot propose a hint that protects less than the finding does
        and then target the difference.
        """
        if type(hit) is not AntiSkillHitV1:
            raise ValueError("repair hint must bind to an exact AntiSkillHitV1")
        return cls(
            hit_id=hit.hit_id,
            spec_id=hit.spec_id,
            suggestion=suggestion,
            protected_fields=hit.protected_fields,
            targets=targets,
        )

    @classmethod
    def from_mapping(cls, data: Mapping[str, Any]) -> "RepairHintCandidateV1":
        """Parse a payload, refusing approval, activation and write fields."""
        if not isinstance(data, Mapping):
            raise ValueError("repair hint payload must be a mapping")
        smuggled = sorted(REPAIR_HINT_FORBIDDEN_KEYS & set(data))
        if smuggled:
            raise ValueError(
                "repair hint candidate may not carry: " + ", ".join(smuggled)
            )
        unknown = sorted(set(data) - REPAIR_HINT_KNOWN_KEYS)
        if unknown:
            raise ValueError(
                "repair hint candidate has unknown fields: " + ", ".join(unknown)
            )
        return cls(
            hit_id=data["hit_id"],
            spec_id=data["spec_id"],
            suggestion=data["suggestion"],
            protected_fields=tuple(data.get("protected_fields", ())),
            targets=tuple(data.get("targets", ())),
            authority_effect=data.get("authority_effect", AUTHORITY_EFFECT_NONE),
            schema_version=data.get("schema_version", REPAIR_HINT_SCHEMA_V1),
            candidate_id=data.get("candidate_id", ""),
        )

    def _payload(self) -> dict[str, Any]:
        return {
            "authority_effect": self.authority_effect,
            "hit_id": self.hit_id,
            "protected_fields": list(self.protected_fields),
            "schema_version": self.schema_version,
            "spec_id": self.spec_id,
            "suggestion": self.suggestion,
            "targets": list(self.targets),
        }

    def to_dict(self) -> dict[str, Any]:
        return {**self._payload(), "candidate_id": self.candidate_id}


__all__ = [
    "REPAIR_HINT_FORBIDDEN_KEYS",
    "REPAIR_HINT_KNOWN_KEYS",
    "REPAIR_HINT_SCHEMA_V1",
    "RepairHintCandidateV1",
]
