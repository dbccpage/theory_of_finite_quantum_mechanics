"""Deterministic fixture evaluation for prompt-review policies.

The receipt records a replayable computation.  It is not an attestation, an
admission decision, or evidence that a detector generalizes beyond the named
fixtures.
"""

from __future__ import annotations

from dataclasses import dataclass
import hashlib
import json
from pathlib import Path
import re
from typing import Any, Tuple

from omega_engine.kernel.higher_operad.canonical import canonical_id
from omega_engine_operations.domain.rop.result import Err, Ok, Refusal, Result

from .models import AUTHORITY_EFFECT_NONE, sha256_ref
from .json_wire import loads_strict_json
from .registry import AntiSkillRegistryV1
from .review import POLICY_DIGEST, review_implementation_digest, review_prompt


_DIGEST = re.compile(r"^sha256:[0-9a-f]{64}$")
_IDENTIFIER = re.compile(r"^[A-Za-z0-9][A-Za-z0-9._:/@-]*$")


def _digest_files() -> str:
    digest = hashlib.sha256()
    root = Path(__file__).resolve().parent
    for name in ("evals.py", "json_wire.py", "models.py", "registry.py"):
        raw = (root / name).read_bytes().replace(b"\r\n", b"\n").replace(b"\r", b"\n")
        digest.update(name.encode("utf-8"))
        digest.update(b"\0")
        digest.update(hashlib.sha256(raw).digest())
    digest.update(b"review-implementation\0")
    digest.update(review_implementation_digest().encode("ascii"))
    return "sha256:" + digest.hexdigest()


def _exact_object(value: Any, fields: set[str], label: str) -> dict[str, Any]:
    if type(value) is not dict or any(type(key) is not str for key in value):
        raise ValueError(f"{label} must be an exact string-keyed object")
    missing = fields - set(value)
    unknown = set(value) - fields
    if missing:
        raise ValueError(f"{label} missing fields: {', '.join(sorted(missing))}")
    if unknown:
        raise ValueError(f"{label} unknown fields: {', '.join(sorted(unknown))}")
    return value


def _strings(value: Any, label: str) -> tuple[str, ...]:
    if type(value) is not list or any(type(item) is not str for item in value):
        raise ValueError(f"{label} must be an array of exact strings")
    if len(value) > 256 or any(not item or item.strip() != item for item in value):
        raise ValueError(f"{label} contains invalid strings")
    if len(value) != len(set(value)):
        raise ValueError(f"{label} must not contain duplicates")
    return tuple(value)


@dataclass(frozen=True)
class EvaluationCaseResultV1:
    case_id: str
    case_digest: str
    expected_codes: Tuple[str, ...]
    forbidden_codes: Tuple[str, ...]
    observed_codes: Tuple[str, ...]
    negative_control: bool
    passed: bool
    authority_effect: str = AUTHORITY_EFFECT_NONE
    schema_version: str = "omega.antiskill.evaluation-case-result.v1"
    result_id: str = ""

    def __post_init__(self) -> None:
        if type(self.case_id) is not str or _IDENTIFIER.fullmatch(self.case_id) is None:
            raise ValueError("case_id must be a canonical identifier")
        if type(self.case_digest) is not str or _DIGEST.fullmatch(self.case_digest) is None:
            raise ValueError("case_digest must be a sha256 reference")
        for field in ("expected_codes", "forbidden_codes", "observed_codes"):
            values = getattr(self, field)
            if type(values) is not tuple or any(type(item) is not str for item in values):
                raise ValueError(f"{field} must be an exact string tuple")
            if len(values) != len(set(values)):
                raise ValueError(f"{field} must not contain duplicates")
        if type(self.negative_control) is not bool or type(self.passed) is not bool:
            raise ValueError("evaluation booleans must be exact booleans")
        if self.authority_effect != AUTHORITY_EFFECT_NONE:
            raise ValueError("evaluation result authority_effect must be None")
        if self.schema_version != "omega.antiskill.evaluation-case-result.v1":
            raise ValueError("unsupported evaluation case-result schema")
        expected = canonical_id(
            "omega.antiskill.evaluation-case-result.v1", self._payload()
        )
        if self.result_id and self.result_id != expected:
            raise ValueError("result_id does not match canonical content")
        object.__setattr__(self, "result_id", expected)

    def _payload(self) -> dict[str, Any]:
        return {
            "case_id": self.case_id,
            "case_digest": self.case_digest,
            "expected_codes": list(self.expected_codes),
            "forbidden_codes": list(self.forbidden_codes),
            "observed_codes": list(self.observed_codes),
            "negative_control": self.negative_control,
            "passed": self.passed,
            "authority_effect": self.authority_effect,
            "schema_version": self.schema_version,
        }

    def to_dict(self) -> dict[str, Any]:
        return {**self._payload(), "result_id": self.result_id}

    @classmethod
    def from_dict(cls, value: Any) -> "EvaluationCaseResultV1":
        wire = _exact_object(
            value,
            {
                "case_id",
                "case_digest",
                "expected_codes",
                "forbidden_codes",
                "observed_codes",
                "negative_control",
                "passed",
                "authority_effect",
                "schema_version",
                "result_id",
            },
            "evaluation case result",
        )
        return cls(
            case_id=wire["case_id"],
            case_digest=wire["case_digest"],
            expected_codes=_strings(wire["expected_codes"], "expected_codes"),
            forbidden_codes=_strings(wire["forbidden_codes"], "forbidden_codes"),
            observed_codes=_strings(wire["observed_codes"], "observed_codes"),
            negative_control=wire["negative_control"],
            passed=wire["passed"],
            authority_effect=wire["authority_effect"],
            schema_version=wire["schema_version"],
            result_id=wire["result_id"],
        )


@dataclass(frozen=True)
class AntiSkillEvaluationReceiptV1:
    fixture_digest: str
    proposal_fixture_digest: str
    registry_id: str
    policy_digest: str
    implementation_digest: str
    case_results: Tuple[EvaluationCaseResultV1, ...]
    outcome: str
    authority_effect: str = AUTHORITY_EFFECT_NONE
    schema_version: str = "omega.antiskill.evaluation-receipt.v1"
    receipt_id: str = ""

    def __post_init__(self) -> None:
        for field in (
            "fixture_digest",
            "proposal_fixture_digest",
            "registry_id",
            "policy_digest",
            "implementation_digest",
        ):
            value = getattr(self, field)
            if type(value) is not str or _DIGEST.fullmatch(value) is None:
                raise ValueError(f"{field} must be a sha256 reference")
        if type(self.case_results) is not tuple or not self.case_results:
            raise ValueError("evaluation receipt requires case results")
        if any(not isinstance(item, EvaluationCaseResultV1) for item in self.case_results):
            raise TypeError("case_results must contain EvaluationCaseResultV1")
        if len({item.case_id for item in self.case_results}) != len(self.case_results):
            raise ValueError("evaluation case ids must be unique")
        if self.outcome not in {"COMPUTED_PASS", "COMPUTED_FAIL"}:
            raise ValueError("unsupported computed evaluation outcome")
        if (self.outcome == "COMPUTED_PASS") != all(
            item.passed for item in self.case_results
        ):
            raise ValueError("evaluation outcome does not match case results")
        if self.authority_effect != AUTHORITY_EFFECT_NONE:
            raise ValueError("evaluation receipt authority_effect must be None")
        if self.schema_version != "omega.antiskill.evaluation-receipt.v1":
            raise ValueError("unsupported anti-skill evaluation-receipt schema")
        expected = canonical_id("omega.antiskill.evaluation-receipt.v1", self._payload())
        if self.receipt_id and self.receipt_id != expected:
            raise ValueError("evaluation receipt_id does not match canonical content")
        object.__setattr__(self, "receipt_id", expected)

    def _payload(self) -> dict[str, Any]:
        return {
            "fixture_digest": self.fixture_digest,
            "proposal_fixture_digest": self.proposal_fixture_digest,
            "registry_id": self.registry_id,
            "policy_digest": self.policy_digest,
            "implementation_digest": self.implementation_digest,
            "case_results": [item.to_dict() for item in self.case_results],
            "outcome": self.outcome,
            "authority_effect": self.authority_effect,
            "schema_version": self.schema_version,
        }

    def to_dict(self) -> dict[str, Any]:
        return {**self._payload(), "receipt_id": self.receipt_id}

    @classmethod
    def from_dict(cls, value: Any) -> "AntiSkillEvaluationReceiptV1":
        wire = _exact_object(
            value,
            {
                "fixture_digest",
                "proposal_fixture_digest",
                "registry_id",
                "policy_digest",
                "implementation_digest",
                "case_results",
                "outcome",
                "authority_effect",
                "schema_version",
                "receipt_id",
            },
            "anti-skill evaluation receipt",
        )
        if type(wire["case_results"]) is not list:
            raise ValueError("case_results must be an array")
        return cls(
            fixture_digest=wire["fixture_digest"],
            proposal_fixture_digest=wire["proposal_fixture_digest"],
            registry_id=wire["registry_id"],
            policy_digest=wire["policy_digest"],
            implementation_digest=wire["implementation_digest"],
            case_results=tuple(
                EvaluationCaseResultV1.from_dict(item) for item in wire["case_results"]
            ),
            outcome=wire["outcome"],
            authority_effect=wire["authority_effect"],
            schema_version=wire["schema_version"],
            receipt_id=wire["receipt_id"],
        )


def _read_exact_json(path: Path) -> Any:
    raw = path.read_bytes()
    if len(raw) > 2 * 1024 * 1024:
        raise ValueError("evaluation JSON exceeds the 2 MiB limit")
    return loads_strict_json(raw.decode("utf-8", errors="strict"))


def evaluate_fixtures(
    cases_path: Path,
    proposal_path: Path,
    registry: AntiSkillRegistryV1,
) -> Result[AntiSkillEvaluationReceiptV1, Refusal]:
    """Replay named cases against the exact registry and review implementation."""

    try:
        case_bytes = cases_path.read_bytes()
        proposal_bytes = proposal_path.read_bytes()
        wire = _exact_object(
            _read_exact_json(cases_path),
            {"schema_version", "cases", "authority_effect"},
            "evaluation fixture",
        )
        if wire["schema_version"] != "omega.antiskill.eval-cases.v1":
            raise ValueError("unsupported evaluation fixture schema")
        if wire["authority_effect"] != AUTHORITY_EFFECT_NONE:
            raise ValueError("evaluation fixture authority_effect must be None")
        if type(wire["cases"]) is not list or not wire["cases"]:
            raise ValueError("evaluation fixture requires cases")
        if len(wire["cases"]) > 256:
            raise ValueError("evaluation fixture exceeds the 256-case limit")
        proposal = _read_exact_json(proposal_path)
        if type(proposal) is not dict:
            raise ValueError("proposal fixture must be an exact object")
        validated_registry = AntiSkillRegistryV1.from_dict(registry.to_dict())
        results: list[EvaluationCaseResultV1] = []
        for index, item in enumerate(wire["cases"]):
            case = _exact_object(
                item,
                {
                    "case_id",
                    "original_prompt",
                    "proposal_overrides",
                    "expected_codes",
                    "forbidden_codes",
                    "negative_control",
                },
                f"evaluation case {index}",
            )
            if (
                type(case["case_id"]) is not str
                or _IDENTIFIER.fullmatch(case["case_id"]) is None
            ):
                raise ValueError("case_id must be a canonical identifier")
            if type(case["original_prompt"]) is not str:
                raise ValueError("original_prompt must be an exact string")
            if type(case["proposal_overrides"]) is not dict:
                raise ValueError("proposal_overrides must be an exact object")
            if type(case["negative_control"]) is not bool:
                raise ValueError("negative_control must be an exact boolean")
            merged = dict(proposal)
            merged.update(case["proposal_overrides"])
            reviewed = review_prompt(
                case["original_prompt"].encode("utf-8"), merged, validated_registry
            )
            if isinstance(reviewed, Err):
                raise ValueError(
                    f"case {case['case_id']} review refused: {reviewed.error.message}"
                )
            observed = tuple(
                sorted(
                    finding.code
                    for finding in reviewed.value.findings
                    if finding.severity in {"ERROR", "WARNING"}
                )
            )
            expected = tuple(sorted(_strings(case["expected_codes"], "expected_codes")))
            forbidden = tuple(
                sorted(_strings(case["forbidden_codes"], "forbidden_codes"))
            )
            passed = expected == observed and set(forbidden).isdisjoint(observed)
            if case["negative_control"]:
                passed = passed and not observed
            results.append(
                EvaluationCaseResultV1(
                    case_id=case["case_id"],
                    case_digest=canonical_id(
                        "omega.antiskill.evaluation-case.v1", case
                    ),
                    expected_codes=expected,
                    forbidden_codes=forbidden,
                    observed_codes=observed,
                    negative_control=case["negative_control"],
                    passed=passed,
                )
            )
        receipt = AntiSkillEvaluationReceiptV1(
            fixture_digest=sha256_ref(case_bytes),
            proposal_fixture_digest=sha256_ref(proposal_bytes),
            registry_id=validated_registry.registry_id,
            policy_digest=POLICY_DIGEST,
            implementation_digest=_digest_files(),
            case_results=tuple(results),
            outcome=(
                "COMPUTED_PASS" if all(item.passed for item in results) else "COMPUTED_FAIL"
            ),
        )
        return Ok(receipt)
    except (OSError, TypeError, ValueError, json.JSONDecodeError) as exc:
        return Err(
            Refusal(
                code="EVALUATION_REFUSED",
                message=str(exc),
                locus="anti-skill-fixtures",
            )
        )


__all__ = [
    "AntiSkillEvaluationReceiptV1",
    "EvaluationCaseResultV1",
    "evaluate_fixtures",
]
