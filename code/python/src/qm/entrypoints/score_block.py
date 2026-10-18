#!/usr/bin/env python3
"""Block result validator and scoring tool for Campaign C250.

AuthorityEffect: None. Citation: sealed-derivation-v1 (3100c4e).
"""
from __future__ import annotations

import argparse
import hashlib
import json
import math
import re
import sys
from pathlib import Path
from typing import Any

REQUIRED_FIELDS = [
    "authority_effect",
    "block_id",
    "global_steps",
    "status",
    "timestamp",
    "kernel_results",
    "rust_parity",
    "lean4_formalization",
    "evidence_receipts",
    "claim_ledger_additions",
    "gap_register_disposition",
    "adversarial_audit",
    "verification_gates",
]

HEX64_REGEX = re.compile(r"^[0-9a-f]{64}$")


class BlockValidationError(Exception):
    """Raised when a block result artifact fails schema or verification checks."""


def _check_required_fields_and_authority(data: dict[str, Any]) -> None:
    if not isinstance(data, dict):
        raise BlockValidationError(f"Root object must be a dict, got {type(data).__name__}")
    missing = [f for f in REQUIRED_FIELDS if f not in data]
    if missing:
        raise BlockValidationError(f"Missing required fields: {missing}")
    if data["authority_effect"] != "None":
        raise BlockValidationError(
            f"authority_effect must be exactly 'None', got '{data['authority_effect']}'"
        )


def _check_block_id_and_steps(data: dict[str, Any], expected_block: int) -> None:
    expected_block_id = f"block_{expected_block:02d}"
    if data["block_id"] != expected_block_id:
        raise BlockValidationError(
            f"block_id '{data['block_id']}' does not match expected '{expected_block_id}'"
        )
    gs = data["global_steps"]
    if not isinstance(gs, dict):
        raise BlockValidationError(f"global_steps must be a dict, got {type(gs).__name__}")
    for k in ("start", "end", "count"):
        if k not in gs or type(gs[k]) is not int:
            raise BlockValidationError(f"global_steps.{k} must be an int")
    expected_start = 51 + (expected_block - 1) * 25
    expected_end = expected_start + 24
    if gs["start"] != expected_start or gs["end"] != expected_end or gs["count"] != 25:
        raise BlockValidationError(
            f"global_steps ({gs['start']}-{gs['end']}, count={gs['count']}) "
            f"does not match expected block range ({expected_start}-{expected_end}, count=25)"
        )
    if gs["end"] - gs["start"] + 1 != gs["count"]:
        raise BlockValidationError("global_steps count does not equal (end - start + 1)")


def _check_status_timestamp_and_subobjects(data: dict[str, Any]) -> None:
    if not isinstance(data["status"], str) or not data["status"]:
        raise BlockValidationError("status must be a non-empty string")
    if not isinstance(data["timestamp"], str) or len(data["timestamp"]) < 10:
        raise BlockValidationError("timestamp must be a valid ISO string")
    for field in ("kernel_results", "rust_parity", "lean4_formalization", "adversarial_audit", "verification_gates"):
        if not isinstance(data[field], dict):
            raise BlockValidationError(f"Field '{field}' must be a dict, got {type(data[field]).__name__}")
    for field in ("evidence_receipts", "claim_ledger_additions", "gap_register_disposition"):
        if not isinstance(data[field], list):
            raise BlockValidationError(f"Field '{field}' must be a list, got {type(data[field]).__name__}")


def _verify_receipt_disk_file(idx: int, item: dict[str, Any], digest: str, base_dir: Path, notes: list[str]) -> None:
    relative = Path(item["path"])
    if relative.is_absolute():
        raise BlockValidationError("Evidence paths must be relative to the declared root")
    file_path = (base_dir / relative).resolve()
    if not file_path.is_relative_to(base_dir.resolve()):
        raise BlockValidationError("Evidence path escapes the declared root")
    if not file_path.is_file():
        raise BlockValidationError(f"Missing evidence file: {item['path']}")
    actual_digest = hashlib.sha256(file_path.read_bytes()).hexdigest()
    if actual_digest != digest:
        raise BlockValidationError(
            f"evidence_receipts[{idx}] digest mismatch for {item['path']}: "
            f"declared {digest} != actual {actual_digest}"
        )
    notes.append(f"Receipt verified: {item['path']} ({digest[:8]}...)")


def _check_evidence_receipts(data: dict[str, Any], base_dir: Path | None, notes: list[str]) -> None:
    if not data["evidence_receipts"]:
        raise BlockValidationError("At least one evidence receipt is required")
    for idx, item in enumerate(data["evidence_receipts"]):
        if not isinstance(item, dict):
            raise BlockValidationError(f"evidence_receipts[{idx}] must be a dict")
        if "path" not in item or not isinstance(item["path"], str):
            raise BlockValidationError(f"evidence_receipts[{idx}] missing valid 'path'")
        if "sha256" not in item or not isinstance(item["sha256"], str):
            raise BlockValidationError(f"evidence_receipts[{idx}] missing valid 'sha256'")
        digest = item["sha256"].lower()
        if not HEX64_REGEX.match(digest):
            raise BlockValidationError(f"evidence_receipts[{idx}] sha256 is not 64 hex characters: {item['sha256']}")
        if base_dir is not None:
            _verify_receipt_disk_file(idx, item, digest, base_dir, notes)


def _check_verification_gates(data: dict[str, Any], base_dir: Path | None, notes: list[str]) -> None:
    vg = data["verification_gates"]
    if not vg or any(type(value) is not bool or not value for value in vg.values()):
        raise BlockValidationError("Every declared verification gate must be exactly true")
    if base_dir is None:
        notes.append("Schema-only check: receipt bytes were not replayed")


def validate_block_result(data: dict[str, Any], expected_block: int = 1, base_dir: Path | None = None) -> list[str]:
    """Validate a block result dictionary against the declared C250 schema.

    Returns a list of validation notes on success.
    Raises BlockValidationError on any schema violation or check failure.
    """
    _check_required_fields_and_authority(data)
    _check_block_id_and_steps(data, expected_block)
    _check_status_timestamp_and_subobjects(data)
    notes: list[str] = []
    _check_evidence_receipts(data, base_dir, notes)
    _check_verification_gates(data, base_dir, notes)
    notes.append(f"Block block_{expected_block:02d} structure and schema successfully validated.")
    return notes


def parse_clause_expr(expr: str) -> tuple[str, str, Any]:
    """Parse a machine clause expression into (op_type, field_name, operand)."""
    if " == " in expr:
        field, right = expr.split(" == ", 1)
        return "eq", field.strip(), json.loads(right.strip())
    elif " in " in expr:
        left, field = expr.split(" in ", 1)
        return "in", field.strip(), json.loads(left.strip())
    elif " between " in expr:
        field, rest = expr.split(" between ", 1)
        a_str, b_str = rest.split(" and ", 1)
        return "between", field.strip(), (json.loads(a_str.strip()), json.loads(b_str.strip()))
    for token, op_type in ((" != ", "ne"), (" >= ", "ge"), (" <= ", "le"),
                           (" > ", "gt"), (" < ", "lt")):
        if token in expr:
            field, right = expr.split(token, 1)
            return op_type, field.strip(), json.loads(right.strip())
    raise ValueError(f"Unknown clause expression syntax: {expr}")


def _eval_ordered_op(op_type: str, val: Any, operand: Any) -> tuple[str, str]:
    if isinstance(val, bool) or not isinstance(val, (int, float)) or isinstance(operand, bool) or not isinstance(operand, (int, float)):
        return "INVALID", f"cannot order-compare {val!r} with {operand!r}"
    if not math.isfinite(val):
        return "INVALID", f"field is not finite: {val!r}"
    ok = {"ge": val >= operand, "le": val <= operand, "gt": val > operand, "lt": val < operand}[op_type]
    return ("HIT" if ok else "MISS", f"field={val}, operand={operand}")


def _eval_clause_op(op_type: str, val: Any, operand: Any) -> tuple[str, str]:
    if op_type == "eq":
        ok = val == operand and (isinstance(val, bool) == isinstance(operand, bool))
        return ("HIT", "") if ok else ("MISS", f"field={val}, bet={operand}")
    if op_type == "in":
        ok = isinstance(val, (list, tuple, set)) and operand in val
        return ("HIT", "") if ok else ("MISS", f"field={val}, bet={operand}")
    if op_type == "between":
        a, b = operand
        ok = type(val) in (int, float) and math.isfinite(val) and a <= val <= b
        return ("HIT", "") if ok else ("MISS", f"field={val}, range=[{a}, {b}]")
    if op_type == "ne":
        same = val == operand and (isinstance(val, bool) == isinstance(operand, bool))
        return ("MISS" if same else "HIT", f"field={val!r}, excluded={operand!r}")
    if op_type in ("ge", "le", "gt", "lt"):
        return _eval_ordered_op(op_type, val, operand)
    return "OPEN", "unhandled"


def parse_and_score_clause(cid: str, forced_label: str, expr: str, result_data: dict[str, Any]) -> dict[str, Any]:
    """Score a single machine clause against result_data."""
    forced = (forced_label == "FORCED")
    op_type, field, operand = parse_clause_expr(expr)
    if field not in result_data or result_data[field] is None:
        return {
            "cid": cid,
            "forced": forced,
            "status": "OPEN",
            "detail": "field missing or null",
            "expr": expr,
        }
    val = result_data[field]
    status, detail = _eval_clause_op(op_type, val, operand)
    return {"cid": cid, "forced": forced, "status": status, "detail": detail, "expr": expr}


def _parse_bet_clause_line(s: str, bet_path: Path, result_data: dict[str, Any], clauses: list[dict[str, Any]]) -> None:
    m = re.match(r"^(M\d+)\s+\[(FORCED|NOT FORCED)\]:\s*(.+)$", s)
    if not m:
        raise ValueError(f"Malformed machine clause in {bet_path}: {s}")
    cid, forced_label, expr = m.groups()
    if any(c["cid"] == cid for c in clauses):
        raise ValueError(f"Duplicate machine clause {cid} in {bet_path}")
    clauses.append(parse_and_score_clause(cid, forced_label, expr, result_data))


def score_bet_file(bet_path: Path, result_data: dict[str, Any]) -> dict[str, Any]:
    """Parse and score all machine clauses in a bet plaintext file."""
    lines = bet_path.read_text(encoding="utf-8").splitlines()
    bet_id = lines[0].strip() if lines else bet_path.stem
    in_machine = False
    clauses: list[dict[str, Any]] = []
    for line in lines:
        s = line.strip()
        if s.startswith("MACHINE CLAUSES"):
            in_machine = True
        elif s.startswith("JUDGED CLAUSES") or s.startswith("WHAT WOULD FALSIFY"):
            in_machine = False
        elif in_machine and s.startswith("M"):
            _parse_bet_clause_line(s, bet_path, result_data, clauses)

    if not clauses:
        raise ValueError(f"No machine clauses in {bet_path}")

    hits = sum(1 for c in clauses if not c["forced"] and c["status"] == "HIT")
    misses = sum(1 for c in clauses if not c["forced"] and c["status"] == "MISS")
    open_count = sum(1 for c in clauses if not c["forced"] and c["status"] == "OPEN")
    forced_count = sum(1 for c in clauses if c["forced"])

    return {
        "bet_id": bet_id,
        "clauses": clauses,
        "hits": hits,
        "misses": misses,
        "open": open_count,
        "forced": forced_count,
    }


def run_self_tests() -> int:
    """Run comprehensive self-tests on schema validation and rejection of planted false clauses."""
    print("Running score_block self-tests...")

    valid_instance: dict[str, Any] = {
        "authority_effect": "None",
        "block_id": "block_01",
        "global_steps": {
            "start": 51,
            "end": 75,
            "count": 25,
        },
        "status": "COMPLETED",
        "timestamp": "2026-09-06T15:00:00Z",
        "kernel_results": {
            "dimensions_tested": [2, 3],
            "conductors_tested": [4, 5, 8, 12, 24],
            "effect_frame_linearity_verified": True,
        },
        "rust_parity": {
            "parity_achieved": True,
            "tests_passed": 12,
        },
        "lean4_formalization": {
            "files": ["H058BuschGleasonEffectFrame.lean"],
            "sorry_count": 0,
        },
        "evidence_receipts": [
            {
                "path": "apps/finite_qm/evidence/test_receipt.json",
                "sha256": "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855",
            }
        ],
        "claim_ledger_additions": [],
        "gap_register_disposition": [],
        "adversarial_audit": {
            "non_psd_negative_controls_rejected": True,
            "boundary_checks_passed": True,
        },
        "verification_gates": {
            "pytest_passed": True,
            "all_tests_green": True,
        },
    }

    try:
        notes = validate_block_result(valid_instance, expected_block=1)
        assert len(notes) >= 1
        print("  [PASS] Valid block result accepted by validator.")
    except Exception as exc:
        print(f"  [FAIL] Valid instance raised unexpected exception: {exc}")
        return 1

    cases: list[tuple[str, dict[str, Any]]] = [
        (
            "Missing authority_effect",
            {k: v for k, v in valid_instance.items() if k != "authority_effect"},
        ),
        (
            "AuthorityEffect promotion violation",
            {**valid_instance, "authority_effect": "PROVEN"},
        ),
        (
            "Mismatched block_id",
            {**valid_instance, "block_id": "block_02"},
        ),
        (
            "Mismatched global_steps range",
            {**valid_instance, "global_steps": {"start": 51, "end": 80, "count": 25}},
        ),
        (
            "Mismatched global_steps count",
            {**valid_instance, "global_steps": {"start": 51, "end": 75, "count": 20}},
        ),
        (
            "Invalid SHA-256 format (short digest)",
            {
                **valid_instance,
                "evidence_receipts": [{"path": "dummy.json", "sha256": "badbeef"}],
            },
        ),
        (
            "Invalid SHA-256 format (non-hex characters)",
            {
                **valid_instance,
                "evidence_receipts": [
                    {
                        "path": "dummy.json",
                        "sha256": "g" * 64,
                    }
                ],
            },
        ),
        (
            "Mismatched evidence structure (missing path)",
            {
                **valid_instance,
                "evidence_receipts": [{"sha256": "a" * 64}],
            },
        ),
        (
            "Failed verification gate (pytest_passed is False)",
            {
                **valid_instance,
                "verification_gates": {"pytest_passed": False, "all_tests_green": True},
            },
        ),
        (
            "Failed verification gate (all_tests_green is False)",
            {
                **valid_instance,
                "verification_gates": {"pytest_passed": True, "all_tests_green": False},
            },
        ),
        (
            "Wrong type for kernel_results (list instead of dict)",
            {**valid_instance, "kernel_results": [1, 2, 3]},
        ),
    ]

    for label, bad_dict in cases:
        try:
            validate_block_result(bad_dict, expected_block=1)
            print(f"  [FAIL] Expected rejection for '{label}', but validator passed.")
            return 1
        except BlockValidationError:
            print(f"  [PASS] Planted defect rejected: {label}")
        except Exception as exc:
            print(f"  [FAIL] Unexpected exception type for '{label}': {type(exc).__name__}: {exc}")
            return 1

    import tempfile
    with tempfile.TemporaryDirectory() as tmpdir:
        tmppath = Path(tmpdir)
        test_file = tmppath / "receipt.json"
        test_file.write_bytes(b"actual content on disk")
        bad_receipt_instance = {
            **valid_instance,
            "evidence_receipts": [
                {
                    "path": "receipt.json",
                    "sha256": "0" * 64,
                }
            ],
        }
        try:
            validate_block_result(bad_receipt_instance, expected_block=1, base_dir=tmppath)
            print("  [FAIL] Expected rejection for disk content digest mismatch, but validator passed.")
            return 1
        except BlockValidationError as exc:
            print(f"  [PASS] Planted disk digest mismatch rejected: {exc}")

    sample_result = {
        "busch_ports": True,
        "choice_free": False,
        "lean_dimensions_proved": [2, 3],
        "residual_declaration_count": 2,
    }

    planted_miss = parse_and_score_clause("M1", "NOT FORCED", "busch_ports == false", sample_result)
    if planted_miss["status"] != "MISS":
        print(f"  [FAIL] Expected planted false clause to score MISS, got {planted_miss['status']}")
        return 1
    print("  [PASS] Planted false clause scored MISS.")

    planted_hit = parse_and_score_clause("M2", "NOT FORCED", "busch_ports == true", sample_result)
    if planted_hit["status"] != "HIT":
        print(f"  [FAIL] Expected true clause to score HIT, got {planted_hit['status']}")
        return 1
    print("  [PASS] True clause scored HIT.")

    planted_in = parse_and_score_clause("M3", "NOT FORCED", "2 in lean_dimensions_proved", sample_result)
    if planted_in["status"] != "HIT":
        print(f"  [FAIL] Expected membership clause to score HIT, got {planted_in['status']}")
        return 1
    print("  [PASS] Membership clause scored HIT.")

    planted_between = parse_and_score_clause("M4", "NOT FORCED", "residual_declaration_count between 1 and 3", sample_result)
    if planted_between["status"] != "HIT":
        print(f"  [FAIL] Expected range clause to score HIT, got {planted_between['status']}")
        return 1
    print("  [PASS] Range clause scored HIT.")

    planted_open = parse_and_score_clause("M5", "NOT FORCED", "nonexistent == 42", sample_result)
    if planted_open["status"] != "OPEN":
        print(f"  [FAIL] Expected missing field to score OPEN, got {planted_open['status']}")
        return 1
    print("  [PASS] Missing field scored OPEN.")

    print("All score_block self-tests completed successfully.")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description="Score and validate C250 block results.")
    parser.add_argument("--block", type=int, default=1, help="Block number (default: 1)")
    parser.add_argument("--result", type=str, default=None, help="Path to block result JSON file")
    parser.add_argument("positional_args", nargs="*", help="Positional: result.json [bets...]")
    parser.add_argument("--self-test", action="store_true", help="Execute built-in self-tests")
    args = parser.parse_args()

    if args.self_test:
        return run_self_tests()

    result_str = args.result
    bet_paths: list[Path] = []
    if args.positional_args:
        if not result_str:
            result_str = args.positional_args[0]
            bet_paths = [Path(p) for p in args.positional_args[1:]]
        else:
            bet_paths = [Path(p) for p in args.positional_args]

    result_path = Path(result_str) if result_str else Path(f"block_{args.block:02d}/result.json")
    if not result_path.exists():
        print(f"Error: Result file not found at '{result_path}'", file=sys.stderr)
        return 1

    try:
        content = json.loads(result_path.read_text(encoding="utf-8"))
    except Exception as exc:
        print(f"Error reading JSON from '{result_path}': {exc}", file=sys.stderr)
        return 1

    try:
        notes = validate_block_result(content, expected_block=args.block, base_dir=result_path.parent.parent)
        for note in notes:
            print(f"INFO: {note}")
        print(f"Result '{result_path}' successfully passed Block {args.block:02d} validation.")
    except BlockValidationError as exc:
        print(f"Validation failure for '{result_path}': {exc}", file=sys.stderr)
        return 1

    if bet_paths:
        print("\n## machine clauses")
        totals: list[str] = []
        for bp in bet_paths:
            if not bp.exists():
                print(f"Error: Bet file not found at '{bp}'", file=sys.stderr)
                return 1
            try:
                scored = score_bet_file(bp, content)
            except (OSError, ValueError) as exc:
                print(f"Error: {exc}", file=sys.stderr)
                return 1
            c_strs = []
            for c in scored["clauses"]:
                if c["status"] == "HIT":
                    c_strs.append(f"{c['cid']} HIT")
                elif c["status"] == "MISS":
                    c_strs.append(f"{c['cid']} MISS ({c['detail']})")
                else:
                    c_strs.append(f"{c['cid']} OPEN ({c['detail']})")
            print(f"{scored['bet_id']}: {', '.join(c_strs)}")
            totals.append(f"{scored['bet_id']}: {scored['hits']}/{scored['misses']}/{scored['open']}")

        print("\n## totals (NOT FORCED only)")
        print("    ".join(totals))

    return 0


if __name__ == "__main__":
    sys.exit(main())

__all__ = ['BlockValidationError', 'HEX64_REGEX', 'REQUIRED_FIELDS', 'main', 'parse_and_score_clause', 'parse_clause_expr', 'run_self_tests', 'score_bet_file', 'validate_block_result']
