from __future__ import annotations

import json
from pathlib import Path

from jsonschema import Draft202012Validator

from omega_engine.crates.prompt_civilization import (
    approve_prompt,
    compile_registry_syntax_only,
    review_prompt,
    segment_dialogue,
)


ROOT = Path(__file__).resolve().parents[2]
SOURCE = (
    ROOT
    / "_ooutwire"
    / "2026-08-13-132939-local-command-caveatcaveat-the-messages-below.txt"
)


def _validate(name: str, instance: object) -> None:
    schema = json.loads(
        (ROOT / ".agents" / "anti_skills" / "schema.json").read_text(
            encoding="utf-8"
        )
    )
    Draft202012Validator.check_schema(schema)
    selected = {
        "$schema": schema["$schema"],
        "$defs": schema["$defs"],
        "$ref": f"#/$defs/{name}",
    }
    Draft202012Validator(selected).validate(instance)


def _proposal() -> dict[str, object]:
    return json.loads(
        (
            ROOT
            / ".agents"
            / "anti_skills"
            / "fixtures"
            / "valid_prompt_proposal.json"
        ).read_text(encoding="utf-8")
    )


def test_public_schema_validates_committed_and_computed_artifacts() -> None:
    registry = compile_registry_syntax_only([]).unwrap()
    original = b"Repair and independently verify the scoped defect."
    bundle = review_prompt(original, _proposal(), registry).unwrap()
    approved = approve_prompt(
        bundle,
        {
            "approved": True,
            "operator_id": "jeremy",
            "review_receipt_id": bundle.receipt.receipt_id,
        },
    ).unwrap()
    episode = segment_dialogue(SOURCE, start_line=12693, end_line=13354).unwrap()[0]
    candidates = json.loads(
        (
            ROOT
            / ".agents"
            / "anti_skills"
            / "ooutwire"
            / "seed_candidates.json"
        ).read_text(encoding="utf-8")
    )["candidates"]
    evaluation = json.loads(
        (
            ROOT
            / ".agents"
            / "anti_skills"
            / "fixtures"
            / "eval_receipt.json"
        ).read_text(encoding="utf-8")
    )

    _validate("registry", registry.to_dict())
    _validate("conversationEpisode", episode.to_dict())
    _validate("candidate", candidates[0])
    _validate("typedPrompt", bundle.prompt.to_dict())
    _validate("promptFinding", bundle.findings[0].to_dict())
    _validate("promptReviewReceipt", bundle.receipt.to_dict())
    _validate("promptReviewBundle", bundle.to_dict())
    _validate("approvedPrompt", approved.to_dict())
    _validate("evaluationReceipt", evaluation)
