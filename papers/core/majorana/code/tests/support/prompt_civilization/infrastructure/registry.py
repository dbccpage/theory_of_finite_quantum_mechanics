"""Deterministic anti-skill registry syntax and composition checks.

AuthorityEffect: None.
"""

from __future__ import annotations

from dataclasses import dataclass
import json
from pathlib import Path
from typing import Any, Iterable, Mapping, Tuple

from omega_engine.kernel.higher_operad.canonical import canonical_id
from omega_engine_operations.domain.rop.result import Err, Ok, Refusal, Result

from ..domain.constants import AUTHORITY_EFFECT_NONE, SCHEMA_ANTISKILL_REGISTRY
from ..domain.models import AntiSkillSpecV1
from .json_wire import loads_strict_json


@dataclass(frozen=True)
class DiagnosticV1:
    code: str
    message: str
    spec_ids: Tuple[str, ...] = ()

    def to_dict(self) -> dict[str, Any]:
        return {
            "code": self.code,
            "message": self.message,
            "spec_ids": list(self.spec_ids),
        }


@dataclass(frozen=True)
class Diagnostics:
    items: Tuple[DiagnosticV1, ...]

    @property
    def ok(self) -> bool:
        return not self.items

    def to_dict(self) -> dict[str, Any]:
        return {
            "schema_version": "omega.antiskill.diagnostics.v1",
            "items": [item.to_dict() for item in self.items],
            "authority_effect": AUTHORITY_EFFECT_NONE,
        }


from ..domain.models import AntiSkillRegistryV1


def _overlap_diagnostics(specs: tuple[AntiSkillSpecV1, ...]) -> list[DiagnosticV1]:
    diagnostics: list[DiagnosticV1] = []
    for index, first in enumerate(specs):
        for second in specs[index + 1 :]:
            overlap = set(first.activation_fields) & set(second.activation_fields)
            if not overlap:
                continue
            findings_only = first.repair_kind == second.repair_kind == "finding_only"
            declared_commuting = (
                second.spec_id in first.commutes_with
                and first.spec_id in second.commutes_with
            )
            ordered = (
                first.composition_order is not None
                and second.composition_order is not None
                and first.composition_order != second.composition_order
            )
            if not (findings_only or declared_commuting or ordered):
                diagnostics.append(
                    DiagnosticV1(
                        code="OVERLAPPING_REPAIRS_UNORDERED",
                        message=(
                            "overlapping repair fields require a strict composition order "
                            "or mutual tested commutation: " + ", ".join(sorted(overlap))
                        ),
                        spec_ids=(first.spec_id, second.spec_id),
                    )
                )
    return diagnostics


def compile_registry_syntax_only(
    specs: Iterable[AntiSkillSpecV1 | Mapping[str, Any]],
) -> Result[AntiSkillRegistryV1, Diagnostics]:
    """Check exact spec syntax and composition; grant no admission status."""

    parsed: list[AntiSkillSpecV1] = []
    diagnostics: list[DiagnosticV1] = []
    for index, item in enumerate(specs):
        if index >= 256:
            diagnostics.append(
                DiagnosticV1(
                    code="REGISTRY_RESOURCE_LIMIT",
                    message="registry exceeds the 256-spec limit",
                )
            )
            break
        try:
            if isinstance(item, AntiSkillSpecV1):
                parsed.append(AntiSkillSpecV1.from_dict(item.to_dict()))
            elif type(item) is dict:
                parsed.append(AntiSkillSpecV1.from_dict(item))
            else:
                raise ValueError("only AntiSkillSpecV1 mappings are accepted")
        except (TypeError, ValueError) as exc:
            diagnostics.append(
                DiagnosticV1(
                    code="INVALID_SPEC_SHAPE",
                    message=f"spec[{index}]: {exc}",
                )
            )
    parsed.sort(key=lambda item: item.spec_id)
    ids = [item.spec_id for item in parsed]
    duplicates = sorted({item for item in ids if ids.count(item) > 1})
    if duplicates:
        diagnostics.append(
            DiagnosticV1(
                code="DUPLICATE_SPEC_ID",
                message="duplicate admitted spec ids",
                spec_ids=tuple(duplicates),
            )
        )
    diagnostics.extend(_overlap_diagnostics(tuple(parsed)))
    if diagnostics:
        return Err(Diagnostics(tuple(diagnostics)))
    return Ok(AntiSkillRegistryV1(tuple(parsed)))


def load_admitted_registry(path: Path) -> Result[AntiSkillRegistryV1, Refusal]:
    """Load the v0 runtime registry, which must remain exactly empty."""

    try:
        payload = path.read_bytes()
        if len(payload) > 2 * 1024 * 1024:
            raise ValueError("registry exceeds the 2 MiB limit")
        raw = loads_strict_json(payload.decode("utf-8", errors="strict"))
        parsed = AntiSkillRegistryV1.from_dict(raw)
        compiled = compile_registry_syntax_only(
            spec.to_dict() for spec in parsed.specs
        )
        if isinstance(compiled, Err):
            return Err(
                Refusal(
                    code="REGISTRY_COMPILE_REFUSED",
                    message=json.dumps(compiled.error.to_dict(), sort_keys=True),
                    locus=str(path),
                )
            )
        if compiled.value.registry_id != parsed.registry_id:
            return Err(
                Refusal(
                    code="REGISTRY_REPLAY_MISMATCH",
                    message="stored registry id differs from independent compilation",
                    locus=str(path),
                )
            )
        if compiled.value.specs:
            return Err(
                Refusal(
                    code="ADMISSION_VALIDATOR_UNAVAILABLE",
                    message=(
                        "v0 cannot load a nonempty anti-skill registry until an "
                        "external validator replays COMPUTED_PASS evidence and "
                        "binds an explicit human admission decision"
                    ),
                    locus=str(path),
                )
            )
        return Ok(compiled.value)
    except (OSError, UnicodeDecodeError, json.JSONDecodeError, TypeError, ValueError) as exc:
        return Err(
            Refusal(
                code="REGISTRY_LOAD_REFUSED",
                message=str(exc),
                locus=str(path),
            )
        )


__all__ = [
    "AntiSkillRegistryV1",
    "DiagnosticV1",
    "Diagnostics",
    "compile_registry_syntax_only",
    "load_admitted_registry",
]
