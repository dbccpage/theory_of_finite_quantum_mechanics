"""Independent live-record ceiling check for AUTHF-CARRIER-ADMISSION-GATE.

AuthorityEffect: None. Reads the recovered record and compares its direct
candidate slice with the closed Lean fixture. Passing admits or selects no
carrier; evidence-path resolution and the other candidates' adequacy are outside
this slice. No production structural validator is imported.
"""
from __future__ import annotations

from dataclasses import dataclass
import hashlib
import json
from pathlib import Path
import sys
from typing import Literal, cast

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from checker_support.boundary import cli, evaluate, Violation
from checker_support.cases import Cases
from checker_support.domains import sequence
from checker_support.outcome import Outcome

AdmissionStatus = Literal["open", "partial", "closed", "admitted"]
JsonStringState = Literal["outside", "inside", "escaped"]
STATUSES = ("open", "partial", "closed", "admitted")
SCHEMA = "ait.computability_carrier_candidates.v1"
CANDIDATE_ID = "AIT-DTM0"
MAX_RECORD_BYTES = 1024*1024
MAX_JSON_DEPTH = 128
SOURCE_RECORD = (Path(__file__).resolve().parents[2] /
                 "papers/foundations/authorization_incompleteness/evidence/original/computability_carrier_candidates.json")


def _mapping(value: object, name: str) -> dict[str, object]:
    if type(value) is not dict or any(type(key) is not str for key in value):
        raise Violation("input", f"{name} must be an object with string keys")
    return cast(dict[str, object], value)


def _required(record: dict[str, object], key: str) -> object:
    if key not in record:
        raise Violation("input", f"required record field is absent: {key}")
    return record[key]


def _status(value: object) -> AdmissionStatus:
    if type(value) is not str or value not in STATUSES:
        raise Violation("input", "admission status is outside the closed vocabulary")
    return cast(AdmissionStatus, value)


def _field_status(fields: dict[str, object], name: str) -> AdmissionStatus:
    return _status(_required(_mapping(_required(fields, name), name), "status"))


@dataclass(frozen=True, slots=True)
class DirectCandidateCeiling:
    """Immutable VO for the independently checked direct-candidate slice.

    Parsing records status, never grants it. verify() enforces the recorded
    open/partial ceiling and false selection without inferring missing evidence.
    """

    record_status: AdmissionStatus
    candidate_status: AdmissionStatus
    syntax_status: AdmissionStatus
    execution_status: AdmissionStatus
    universality_status: AdmissionStatus
    selected: bool

    def __post_init__(self) -> None:
        for status in (self.record_status, self.candidate_status, self.syntax_status,
                       self.execution_status, self.universality_status):
            _status(status)
        if type(self.selected) is not bool:
            raise Violation("input", "candidate selection must be an exact bool")

    @staticmethod
    def from_record(record: object) -> Outcome[DirectCandidateCeiling]:
        return evaluate(_extract_slice, record)

    def verify(self) -> Outcome[DirectCandidateCeiling]:
        return evaluate(self._verified)

    def _verified(self) -> DirectCandidateCeiling:
        actual = (self.record_status, self.candidate_status, self.syntax_status,
                  self.execution_status, self.universality_status, self.selected)
        if actual != ("open", "partial", "partial", "partial", "open", False):
            raise Violation("check", "direct candidate differs from the declared open/partial ceiling")
        return self


def _extract_slice(value: object) -> DirectCandidateCeiling:
    record = _mapping(value, "carrier record")
    if _required(record, "schema_version") != SCHEMA:
        raise Violation("input", "unsupported carrier record schema")
    if _required(record, "authority_effect") != "None":
        raise Violation("check", "carrier record authority effect must be None")
    candidates = sequence(_required(record, "candidates"), "candidates", maximum=64)
    matches: list[dict[str, object]] = []
    for candidate in candidates:
        entry = _mapping(candidate, "candidate")
        identity = _required(entry, "id")
        if type(identity) is not str or not identity.strip():
            raise Violation("input", "candidate identity must be nonempty text")
        if identity == CANDIDATE_ID:
            matches.append(entry)
    if len(matches) != 1:
        raise Violation("input", "exactly one AIT-DTM0 candidate is required")
    direct = matches[0]
    fields = _mapping(_required(direct, "fields"), "direct fields")
    selected = _required(direct, "selected")
    if type(selected) is not bool:
        raise Violation("input", "candidate selection must be an exact bool")
    return DirectCandidateCeiling(
        _status(_required(record, "admission_status")),
        _status(_required(direct, "admission_status")),
        _field_status(fields, "syntax_and_encoding"),
        _field_status(fields, "execution_semantics"),
        _field_status(fields, "universality"), selected)


def _unique_object(pairs: list[tuple[str, object]]) -> dict[str, object]:
    record: dict[str, object] = {}
    for key, value in pairs:
        if key in record:
            raise Violation("duplicate", f"duplicate JSON object member: {key}")
        record[key] = value
    return record


def _reject_constant(value: str) -> object:
    raise Violation("input", f"nonstandard JSON constant is forbidden: {value}")


def _string_state(state: JsonStringState, byte: int) -> JsonStringState:
    if state == "escaped":
        return "inside"
    if byte == 92:
        return "escaped"
    if byte == 34:
        return "inside" if state == "outside" else "outside"
    return state


def _check_json_depth(raw: bytes) -> None:
    """Bound containers before parsing, ignoring brackets inside JSON strings."""
    depth = 0
    state: JsonStringState = "outside"
    for byte in raw:
        if state != "outside" or byte == 34:
            state = _string_state(state, byte)
            continue
        if byte in (91, 123):
            depth += 1
            if depth > MAX_JSON_DEPTH:
                raise Violation("resource", "carrier record exceeds 128 JSON containers")
            continue
        if byte in (93, 125):
            depth -= 1


def _read_record(path: Path) -> tuple[object, str]:
    if not isinstance(path, Path):
        raise Violation("input", "record source must be a filesystem Path")
    # Limit the actual read rather than trusting a size check before opening.
    with path.open("rb") as stream:
        raw = stream.read(MAX_RECORD_BYTES+1)
    if len(raw) > MAX_RECORD_BYTES:
        raise Violation("resource", "carrier record exceeds 1 MiB")
    _check_json_depth(raw)
    try:
        record: object = json.loads(raw.decode("utf-8"), object_pairs_hook=_unique_object,
                                    parse_constant=_reject_constant)
    except RecursionError as error:
        raise Violation("resource", "carrier record exceeds the JSON nesting budget") from error
    return record, hashlib.sha256(raw).hexdigest()


def verify_source(path: Path) -> Outcome[tuple[DirectCandidateCeiling, str]]:
    """Bind the parsed-and-verified slice to the exact bytes read, not a later reread."""
    return evaluate(_read_record, path).bind(
        lambda pair: DirectCandidateCeiling.from_record(pair[0]).bind(
            lambda ceiling: ceiling.verify().map(lambda verified: (verified, pair[1]))))


def main(record_path: Path = SOURCE_RECORD) -> int:
    result = verify_source(record_path)
    if result.error is not None:
        raise Violation(result.error.kind, result.error.message)
    if result.value is None:
        raise Violation("check", "verified source omitted its payload")
    ceiling, digest = result.value
    run = Cases()
    run.require(ceiling.verify().ok, "source slice retains the recorded ceiling")
    print(json.dumps({"checks": run.checks, "failures": 0, "source_sha256": digest,
                      "candidate": CANDIDATE_ID, "selected": ceiling.selected,
                      "scope": "direct_candidate_ceiling_only", "AuthorityEffect": "None"},
                     sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(cli(main))
