"""Thin DDA emitter for OE v0.3 God Code runs. AuthorityEffect: None."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
from typing import Any, Iterable, Sequence

from omega_engine_governance.contracts.dda_packets import DDATapeDFA
from omega_engine.crates.ontology_pd.dda_record import (
    DDA_RECORD_KEYS,
    DDA_RECORD_SCHEMA,
    DdaRecord,
)


DDA_RUN_SCHEMA = "omega.oe_v03.dda_run.v1"
DDA_ENGINE_VERSION = "0.3"
DDA_RUN_RECORD_KEYS = frozenset(
    {
        "schema_version",
        "engine_version",
        "profile",
        "run_id",
        "sequence",
        "total_event_count",
        "event_kind",
        "symbol",
        "payload",
        "authority_effect",
        "previous_record_hash",
        "record_hash",
    }
)
CANONICAL_DDA_ALPHABET = frozenset({"E", "R", "C", "I", "L", "Λ", "D", "M", "T"})
_SOLVED_STATUSES = frozenset({"SOLVED", "MODEL_CHANGED_SOLVED", "Exact", "ExactCellAttached"})
_REFUSAL_STATUSES = frozenset({"TYPED_OBSTRUCTION", "AUTHORIZATION_EXHAUSTED", "REFUSED"})


class DdaJsonlValidationError(ValueError):
    """Raised when a production OE v0.3 JSONL tape fails closed."""


def _canonical_json(value: Any) -> str:
    try:
        return json.dumps(
            value,
            allow_nan=False,
            ensure_ascii=False,
            separators=(",", ":"),
            sort_keys=True,
        )
    except (TypeError, ValueError) as exc:
        raise DdaJsonlValidationError(f"non-canonical JSON value: {exc}") from exc


def _hash_record(record: dict[str, Any]) -> str:
    payload = {key: value for key, value in record.items() if key != "record_hash"}
    return hashlib.sha256(_canonical_json(payload).encode("utf-8")).hexdigest()


def replay_dda_run_record_hash(record: dict[str, Any]) -> str:
    """Recompute one line hash, including schema and engine identity fields."""

    if type(record) is not dict:
        raise TypeError("record must be an exact dict")
    return _hash_record(record)


def _exact_keys(wire: Any, expected: frozenset[str], where: str) -> None:
    if type(wire) is not dict:
        raise DdaJsonlValidationError(f"{where} must be a JSON object")
    actual = set(wire)
    if actual != expected:
        missing = sorted(expected - actual)
        extra = sorted(actual - expected)
        raise DdaJsonlValidationError(
            f"{where} schema keys mismatch: missing={missing}, extra={extra}"
        )


def _validate_source_record(wire: Any, *, profile: str) -> None:
    _exact_keys(wire, DDA_RECORD_KEYS, "source record")
    if wire["schema_version"] != DDA_RECORD_SCHEMA:
        raise DdaJsonlValidationError("unexpected source record schema_version")
    if wire["engine_version"] != DDA_ENGINE_VERSION:
        raise DdaJsonlValidationError("unexpected source record engine_version")
    if wire["profile"] != profile:
        raise DdaJsonlValidationError("source record profile disagrees with run profile")
    if type(wire["t"]) is not int or wire["t"] < 0:
        raise DdaJsonlValidationError("source record t must be a non-negative integer")
    for key in ("step_kind", "rule", "degree", "locus_hash", "hash", "symbol"):
        if type(wire[key]) is not str or not wire[key]:
            raise DdaJsonlValidationError(f"source record {key} must be nonempty str")
    if wire["symbol"] not in CANONICAL_DDA_ALPHABET | {"Z", "Lambda"}:
        raise DdaJsonlValidationError(f"unsupported source symbol {wire['symbol']!r}")
    if wire["residual_zero"] is not None and type(wire["residual_zero"]) is not bool:
        raise DdaJsonlValidationError("source residual_zero must be bool or null")
    for key in ("score_before", "score_after"):
        score = wire[key]
        if score is not None and (
            type(score) is not list
            or len(score) != 4
            or any(type(item) is not int for item in score)
        ):
            raise DdaJsonlValidationError(f"source {key} must be four integers or null")
    if type(wire["payload"]) is not dict:
        raise DdaJsonlValidationError("source record payload must be an object")
    if wire["authority_effect"] != "None":
        raise DdaJsonlValidationError("source record authority_effect must be None")
    _canonical_json(wire)


def _canonical_symbol(source_symbol: str) -> str:
    if source_symbol == "Z":
        return "M"
    if source_symbol == "Lambda":
        return "Λ"
    return source_symbol


def _event_payload_keys(event_kind: str) -> frozenset[str]:
    return {
        "RUN_START": frozenset({"mode", "source_record_count"}),
        "ALGORITHM_STEP": frozenset({"source_record"}),
        "RUN_TERMINAL": frozenset({"terminal_status", "source_terminal_record"}),
    }[event_kind]


def verify_dda_run_records(records: Sequence[dict[str, Any]]) -> bool:
    """Strictly verify schema, source custody, DFA grammar, and parent hashes."""

    if type(records) not in (list, tuple) or not records:
        raise DdaJsonlValidationError("DDA run must contain a nonempty record sequence")
    parent: str | None = None
    profile: str | None = None
    run_id: str | None = None
    source_records: list[dict[str, Any]] = []
    symbols: list[str] = []
    for sequence, record in enumerate(records):
        _exact_keys(record, DDA_RUN_RECORD_KEYS, f"run record {sequence}")
        if record["schema_version"] != DDA_RUN_SCHEMA:
            raise DdaJsonlValidationError("unexpected run schema_version")
        if record["engine_version"] != DDA_ENGINE_VERSION:
            raise DdaJsonlValidationError("unexpected engine_version")
        if type(record["profile"]) is not str or not record["profile"]:
            raise DdaJsonlValidationError("profile must be a nonempty string")
        if type(record["run_id"]) is not str or len(record["run_id"]) != 16:
            raise DdaJsonlValidationError("run_id must be a 16-character digest")
        profile = record["profile"] if profile is None else profile
        run_id = record["run_id"] if run_id is None else run_id
        if record["profile"] != profile or record["run_id"] != run_id:
            raise DdaJsonlValidationError("profile and run_id must be constant across tape")
        if type(record["sequence"]) is not int or record["sequence"] != sequence:
            raise DdaJsonlValidationError("run sequence must be contiguous from zero")
        if (
            type(record["total_event_count"]) is not int
            or record["total_event_count"] != len(records)
        ):
            raise DdaJsonlValidationError("total_event_count does not bind full tape")
        event_kind = record["event_kind"]
        if event_kind not in {"RUN_START", "ALGORITHM_STEP", "RUN_TERMINAL"}:
            raise DdaJsonlValidationError(f"invalid event_kind {event_kind!r}")
        symbol = record["symbol"]
        if type(symbol) is not str or symbol not in CANONICAL_DDA_ALPHABET:
            raise DdaJsonlValidationError(f"invalid canonical DDA symbol {symbol!r}")
        symbols.append(symbol)
        _exact_keys(record["payload"], _event_payload_keys(event_kind), f"{event_kind} payload")
        if record["authority_effect"] != "None":
            raise DdaJsonlValidationError("authority_effect must be None")
        if record["previous_record_hash"] != parent:
            raise DdaJsonlValidationError("previous_record_hash chain mismatch")
        if type(record["record_hash"]) is not str or len(record["record_hash"]) != 64:
            raise DdaJsonlValidationError("record_hash must be a SHA-256 hex digest")
        if record["record_hash"] != _hash_record(record):
            raise DdaJsonlValidationError("record_hash replay mismatch")
        parent = record["record_hash"]

        if event_kind == "RUN_START":
            if sequence != 0 or symbol not in {"E", "R"}:
                raise DdaJsonlValidationError("run tape must start with E or R")
            if type(record["payload"]["mode"]) is not str or not record["payload"]["mode"]:
                raise DdaJsonlValidationError("run mode must be a nonempty string")
            if (
                type(record["payload"]["source_record_count"]) is not int
                or record["payload"]["source_record_count"] < 0
            ):
                raise DdaJsonlValidationError("source_record_count must be non-negative int")
        elif event_kind == "ALGORITHM_STEP":
            source = record["payload"]["source_record"]
            _validate_source_record(source, profile=profile)
            if _canonical_symbol(source["symbol"]) != symbol or symbol == "T":
                raise DdaJsonlValidationError("algorithm symbol/source custody mismatch")
            source_records.append(source)
        else:
            if sequence != len(records) - 1 or symbol != "T":
                raise DdaJsonlValidationError("terminal event must be the final T")
            if (
                type(record["payload"]["terminal_status"]) is not str
                or not record["payload"]["terminal_status"].strip()
            ):
                raise DdaJsonlValidationError("terminal_status must be a nonempty string")
            terminal_source = record["payload"]["source_terminal_record"]
            if terminal_source is not None:
                _validate_source_record(terminal_source, profile=profile)
                if _canonical_symbol(terminal_source["symbol"]) != "T":
                    raise DdaJsonlValidationError("terminal source must carry T")
                source_records.append(terminal_source)

    if records[0]["event_kind"] != "RUN_START":
        raise DdaJsonlValidationError("first event must be RUN_START")
    if records[-1]["event_kind"] != "RUN_TERMINAL":
        raise DdaJsonlValidationError("last event must be RUN_TERMINAL")
    if any(record["event_kind"] != "ALGORITHM_STEP" for record in records[1:-1]):
        raise DdaJsonlValidationError("only algorithm steps may occur inside the tape")
    if records[0]["payload"]["source_record_count"] != len(source_records):
        raise DdaJsonlValidationError("source_record_count custody mismatch")
    source_times = [source["t"] for source in source_records]
    if any(current <= previous for previous, current in zip(source_times, source_times[1:])):
        raise DdaJsonlValidationError("source record t values must strictly increase")
    if symbols[0] not in {"E", "R"} or symbols[-1] != "T":
        raise DdaJsonlValidationError("DDA tape must start E/R and end T")
    if "T" in symbols[:-1]:
        raise DdaJsonlValidationError("T absorption violated")
    terminal_status = records[-1]["payload"]["terminal_status"]
    source_symbols = tuple(_canonical_symbol(source["symbol"]) for source in source_records)
    if "M" in source_symbols and terminal_status not in _REFUSAL_STATUSES:
        raise DdaJsonlValidationError(
            "refusal source requires an obstruction/refusal terminal_status"
        )
    if terminal_status in _SOLVED_STATUSES and not any(
        source["residual_zero"] is True for source in source_records
    ):
        raise DdaJsonlValidationError(
            "solved terminal_status requires source evidence with residual_zero=true"
        )
    terminal_source = records[-1]["payload"]["source_terminal_record"]
    if (
        terminal_source is not None
        and terminal_source["step_kind"] == "CASCADE_RECEIPT_TERMINAL"
        and terminal_source["payload"].get("terminal_status") != terminal_status
    ):
        raise DdaJsonlValidationError(
            "terminal_status disagrees with cascade terminal source"
        )
    try:
        DDATapeDFA.validate(".".join(symbols), dialect=DDATapeDFA.LEGACY_V1)
    except ValueError as exc:
        raise DdaJsonlValidationError(f"DDA tape grammar rejected: {exc}") from exc
    return True


def _reject_duplicate_keys(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    result: dict[str, Any] = {}
    for key, value in pairs:
        if key in result:
            raise DdaJsonlValidationError(f"duplicate key {key!r}")
        result[key] = value
    return result


def _reject_json_constant(value: str) -> None:
    raise DdaJsonlValidationError(f"non-finite JSON constant {value!r}")


def load_dda_run_jsonl(path: Path | str) -> list[dict[str, Any]]:
    """Load a production tape with duplicate-key and exact-schema rejection."""

    source = Path(path)
    if not source.is_file():
        raise DdaJsonlValidationError(f"DDA JSONL path is not a file: {source}")
    records: list[dict[str, Any]] = []
    for line_number, line in enumerate(source.read_text(encoding="utf-8").splitlines(), 1):
        if not line.strip():
            raise DdaJsonlValidationError(f"blank JSONL line at {line_number}")
        try:
            record = json.loads(
                line,
                object_pairs_hook=_reject_duplicate_keys,
                parse_constant=_reject_json_constant,
            )
        except (json.JSONDecodeError, DdaJsonlValidationError) as exc:
            raise DdaJsonlValidationError(f"invalid JSONL line {line_number}: {exc}") from exc
        records.append(record)
    verify_dda_run_records(records)
    return records


def write_dda_run_jsonl(
    path: Path | str,
    records: Sequence[DdaRecord],
    *,
    profile: str,
    mode: str,
    terminal_status: str,
    engine_version: str = DDA_ENGINE_VERSION,
) -> Path:
    """Write and strict-reload a complete hash-chained algorithm-run tape."""

    if not isinstance(path, (Path, str)) or not str(path).strip():
        raise TypeError("path must be an explicit Path or nonempty string")
    out = Path(path)
    if out.suffix.lower() != ".jsonl":
        raise ValueError("production DDA output path must end in .jsonl")
    if out.exists() and not out.is_file():
        raise ValueError("production DDA output path cannot be a directory")
    if type(profile) is not str or not profile or type(mode) is not str or not mode:
        raise TypeError("profile and mode must be nonempty strings")
    if engine_version != DDA_ENGINE_VERSION:
        raise ValueError(f"engine_version must be {DDA_ENGINE_VERSION}")
    source_records = tuple(records)
    if any(type(record) is not DdaRecord for record in source_records):
        raise TypeError("records must contain exact DdaRecord instances")
    source_wires = tuple(record.to_wire() for record in source_records)
    for wire in source_wires:
        _validate_source_record(wire, profile=profile)

    terminal_source: dict[str, Any] | None = None
    algorithm_events: list[tuple[str, dict[str, Any]]] = []
    for index, wire in enumerate(source_wires):
        symbol = _canonical_symbol(wire["symbol"])
        if symbol == "T":
            if index != len(source_wires) - 1:
                raise DdaJsonlValidationError("source T must be the final source record")
            terminal_source = wire
        else:
            algorithm_events.append((symbol, {"source_record": wire}))

    run_material = {
        "schema_version": DDA_RUN_SCHEMA,
        "engine_version": engine_version,
        "profile": profile,
        "mode": mode,
        "terminal_status": terminal_status,
        "source_records": source_wires,
    }
    run_id = hashlib.sha256(_canonical_json(run_material).encode("utf-8")).hexdigest()[:16]
    event_specs: list[tuple[str, str, dict[str, Any]]] = [
        ("RUN_START", "R", {"mode": mode, "source_record_count": len(source_wires)})
    ]
    event_specs.extend(
        ("ALGORITHM_STEP", symbol, payload) for symbol, payload in algorithm_events
    )
    event_specs.append(
        (
            "RUN_TERMINAL",
            "T",
            {
                "terminal_status": terminal_status,
                "source_terminal_record": terminal_source,
            },
        )
    )

    tape: list[dict[str, Any]] = []
    parent: str | None = None
    total_event_count = len(event_specs)
    for sequence, (event_kind, symbol, payload) in enumerate(event_specs):
        wire = {
            "schema_version": DDA_RUN_SCHEMA,
            "engine_version": engine_version,
            "profile": profile,
            "run_id": run_id,
            "sequence": sequence,
            "total_event_count": total_event_count,
            "event_kind": event_kind,
            "symbol": symbol,
            "payload": payload,
            "authority_effect": "None",
            "previous_record_hash": parent,
        }
        wire["record_hash"] = _hash_record(wire)
        parent = wire["record_hash"]
        tape.append(wire)
    verify_dda_run_records(tape)

    out.parent.mkdir(parents=True, exist_ok=True)
    with out.open("w", encoding="utf-8", newline="\n") as handle:
        for record in tape:
            handle.write(_canonical_json(record))
            handle.write("\n")
    loaded = load_dda_run_jsonl(out)
    if loaded[-1]["record_hash"] != tape[-1]["record_hash"]:
        raise DdaJsonlValidationError("strict reload changed the trace root")
    return out


def write_dda_jsonl(path: Path | str, records: Sequence[DdaRecord]) -> Path:
    """Write legacy raw records; production callers use ``write_dda_run_jsonl``."""
    out = Path(path)
    out.parent.mkdir(parents=True, exist_ok=True)
    with out.open("w", encoding="utf-8", newline="\n") as f:
        for rec in records:
            f.write(rec.to_json_line())
            f.write("\n")
    return out


def tape_letters(records: Iterable[DdaRecord]) -> tuple[str, ...]:
    """Project symbol field to a letter tape."""
    return tuple(r.symbol for r in records)


def verify_records_authority_none(records: Sequence[DdaRecord]) -> bool:
    return all(r.authority_effect == "None" for r in records)


