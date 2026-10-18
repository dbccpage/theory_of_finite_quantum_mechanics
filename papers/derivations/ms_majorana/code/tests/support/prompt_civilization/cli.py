"""CLI for deterministic prompt review and candidate-only dialogue mining.

There is intentionally no command that sends a prompt or admits an anti-skill.
"""

from __future__ import annotations

import argparse
import json
import os
from pathlib import Path
import sys
import tempfile
from typing import Any

from omega_engine_operations.domain.rop.result import Err

from .dialogue import mine_candidates, segment_dialogue
from .evals import evaluate_fixtures
from .json_wire import loads_strict_json
from .models import (
    ApprovedPromptV1,
    ConversationEpisodeV1,
    PromptReviewBundleV1,
)
from .registry import AntiSkillRegistryV1, load_admitted_registry
from .review import approve_prompt, packetize_prompt, review_prompt


DEFAULT_REGISTRY = Path(".agents/anti_skills/admitted/registry.json")


def _read_json(path: Path) -> Any:
    raw = path.read_bytes()
    if len(raw) > 2 * 1024 * 1024:
        raise ValueError("JSON input exceeds the 2 MiB limit")
    return loads_strict_json(raw.decode("utf-8", errors="strict"))


def _write_json(path: Path | None, value: Any) -> None:
    text = json.dumps(value, ensure_ascii=False, indent=2, sort_keys=True) + "\n"
    if path is None:
        sys.stdout.write(text)
    else:
        path.parent.mkdir(parents=True, exist_ok=True)
        temporary: Path | None = None
        try:
            with tempfile.NamedTemporaryFile(
                mode="w",
                encoding="utf-8",
                newline="\n",
                dir=path.parent,
                prefix=f".{path.name}.",
                suffix=".tmp",
                delete=False,
            ) as stream:
                temporary = Path(stream.name)
                stream.write(text)
                stream.flush()
                os.fsync(stream.fileno())
            os.replace(temporary, path)
        finally:
            if temporary is not None and temporary.exists():
                temporary.unlink()


def _emit_refusal(error: Any) -> int:
    payload = error.to_dict() if hasattr(error, "to_dict") else {"message": str(error)}
    sys.stderr.write(json.dumps({"ok": False, "refusal": payload}, indent=2) + "\n")
    return 2


def cmd_segment(args: argparse.Namespace) -> int:
    result = segment_dialogue(
        args.source,
        source_format=args.source_format,
        start_line=args.start_line,
        end_line=args.end_line,
        session_id=args.session_id,
        task_id=args.task_id,
        model_id=args.model_id,
    )
    if isinstance(result, Err):
        return _emit_refusal(result.error)
    _write_json(
        args.output,
        {
            "schema_version": "omega.antiskill.segmented-dialogue.v1",
            "episodes": [episode.to_dict() for episode in result.value],
            "authority_effect": "None",
        },
    )
    return 0


def cmd_mine(args: argparse.Namespace) -> int:
    wire = _read_json(args.episodes)
    if type(wire) is not dict or set(wire) != {
        "schema_version",
        "episodes",
        "authority_effect",
    }:
        return _emit_refusal("segmented dialogue fields are not exact")
    if type(wire["episodes"]) is not list:
        return _emit_refusal("episodes must be an array")
    try:
        episodes = [ConversationEpisodeV1.from_dict(item) for item in wire["episodes"]]
        candidates = mine_candidates(episodes)
    except (TypeError, ValueError) as exc:
        return _emit_refusal(exc)
    _write_json(
        args.output,
        {
            "schema_version": "omega.antiskill.candidate-set.v1",
            "candidates": [candidate.to_dict() for candidate in candidates],
            "auto_admit": False,
            "authority_effect": "None",
        },
    )
    return 0


def _load_registry(path: Path) -> tuple[AntiSkillRegistryV1 | None, int]:
    result = load_admitted_registry(path)
    if isinstance(result, Err):
        return None, _emit_refusal(result.error)
    return result.value, 0


def cmd_validate_registry(args: argparse.Namespace) -> int:
    registry, code = _load_registry(args.registry)
    if registry is None:
        return code
    _write_json(args.output, registry.to_dict())
    return 0


def cmd_evaluate_fixtures(args: argparse.Namespace) -> int:
    registry, code = _load_registry(args.registry)
    if registry is None:
        return code
    result = evaluate_fixtures(args.cases, args.proposal, registry)
    if isinstance(result, Err):
        return _emit_refusal(result.error)
    _write_json(args.output, result.value.to_dict())
    return 0


def cmd_review(args: argparse.Namespace) -> int:
    registry, code = _load_registry(args.registry)
    if registry is None:
        return code
    proposal = _read_json(args.proposal)
    result = review_prompt(args.original.read_bytes(), proposal, registry)
    if isinstance(result, Err):
        return _emit_refusal(result.error)
    _write_json(args.output, result.value.to_dict())
    return 0


def cmd_approve(args: argparse.Namespace) -> int:
    try:
        bundle = PromptReviewBundleV1.from_dict(_read_json(args.bundle))
    except (TypeError, ValueError) as exc:
        return _emit_refusal(exc)
    result = approve_prompt(
        bundle,
        {
            "approved": True,
            "operator_id": args.operator,
            "review_receipt_id": bundle.receipt.receipt_id,
        },
    )
    if isinstance(result, Err):
        return _emit_refusal(result.error)
    _write_json(args.output, result.value.to_dict())
    return 0


def cmd_packetize(args: argparse.Namespace) -> int:
    try:
        approved = ApprovedPromptV1.from_dict(_read_json(args.approved))
        packet = packetize_prompt(approved)
    except (TypeError, ValueError) as exc:
        return _emit_refusal(exc)
    _write_json(args.output, packet.to_dict())
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="omega-prompt")
    sub = parser.add_subparsers(dest="command", required=True)

    segment = sub.add_parser("segment-dialogue")
    segment.add_argument("--source", type=Path, required=True)
    segment.add_argument("--source-format", default="auto")
    segment.add_argument("--start-line", type=int, default=None)
    segment.add_argument("--end-line", type=int, default=None)
    segment.add_argument("--session-id", default="")
    segment.add_argument("--task-id", default="")
    segment.add_argument("--model-id", default="")
    segment.add_argument("--output", type=Path, default=None)
    segment.set_defaults(func=cmd_segment)

    mine = sub.add_parser("mine-candidates")
    mine.add_argument("--episodes", type=Path, required=True)
    mine.add_argument("--output", type=Path, default=None)
    mine.set_defaults(func=cmd_mine)

    validate = sub.add_parser("validate-registry")
    validate.add_argument("--registry", type=Path, default=DEFAULT_REGISTRY)
    validate.add_argument("--output", type=Path, default=None)
    validate.set_defaults(func=cmd_validate_registry)

    evaluate = sub.add_parser("evaluate-fixtures")
    evaluate.add_argument("--cases", type=Path, required=True)
    evaluate.add_argument("--proposal", type=Path, required=True)
    evaluate.add_argument("--registry", type=Path, default=DEFAULT_REGISTRY)
    evaluate.add_argument("--output", type=Path, default=None)
    evaluate.set_defaults(func=cmd_evaluate_fixtures)

    review = sub.add_parser("review")
    review.add_argument("--original", type=Path, required=True)
    review.add_argument("--proposal", type=Path, required=True)
    review.add_argument("--registry", type=Path, default=DEFAULT_REGISTRY)
    review.add_argument("--output", type=Path, default=None)
    review.set_defaults(func=cmd_review)

    approve = sub.add_parser("approve")
    approve.add_argument("--bundle", type=Path, required=True)
    approve.add_argument("--operator", required=True)
    approve.add_argument("--output", type=Path, default=None)
    approve.set_defaults(func=cmd_approve)

    packetize = sub.add_parser("packetize")
    packetize.add_argument("--approved", type=Path, required=True)
    packetize.add_argument("--output", type=Path, default=None)
    packetize.set_defaults(func=cmd_packetize)
    return parser


def main() -> int:
    args = build_parser().parse_args()
    try:
        return int(args.func(args))
    except (OSError, UnicodeDecodeError, ValueError) as exc:
        return _emit_refusal(exc)


if __name__ == "__main__":
    raise SystemExit(main())
