"""Finite strict-operad presentation of the prompt civilization workflow.

This module declares typed one-operations loaded from the companion
operad_operations.yaml manifest.  It does not assert that detectors, repairs,
or reviews are equivalent paths, and it admits no Path2.
"""

from __future__ import annotations

import hashlib
from pathlib import Path
from typing import Any, cast, Tuple

import yaml

from omega_engine.kernel.higher_operad.canonical import canonical_id
from omega_engine.kernel.higher_operad.model import (
    AuthorityEffect,
    ColourSpec,
    InvocationGrade,
    OperationSpec,
    PortSpec,
)


def _file_digest(path: Path) -> str:
    return "sha256:" + hashlib.sha256(path.read_bytes()).hexdigest()


def _colour(
    colour_id: str,
    family: str,
    schema_ref: str,
    validator_ref: str,
    validator_digest: str,
) -> ColourSpec:
    schema_digest = canonical_id(
        "omega.prompt-civilization.schema-declaration.v1",
        {
            "family": family,
            "schema_ref": schema_ref,
            "validator_ref": validator_ref,
            "validator_digest": validator_digest,
        },
    )
    return ColourSpec(
        colour_id=colour_id,
        family=family,
        schema_ref=schema_ref,
        schema_digest=schema_digest,
        validator_ref=validator_ref,
        validator_digest=validator_digest,
    )


def prompt_civilization_presentation() -> tuple[
    Tuple[ColourSpec, ...], Tuple[OperationSpec, ...]
]:
    root = Path(__file__).resolve().parent
    repo_root = root
    for p in [root] + list(root.parents):
        if (p / "omega_engine_pfp").exists():
            repo_root = p
            break

    packet_path = (
        repo_root / "omega_engine_pfp" / "domain" / "entities" / "packet_envelope.py"
    )

    # Map digest sources to actual files
    digest_map = {
        "models": _file_digest(root / "models.py"),
        "review": _file_digest(root / "review.py"),
        "dialogue": _file_digest(root / "dialogue.py"),
        "packet": _file_digest(packet_path),
    }

    yaml_path = root / "operad_operations.yaml"
    with yaml_path.open("r", encoding="utf-8") as f:
        manifest: dict[str, Any] = yaml.safe_load(f)

    colours_list: list[ColourSpec] = []
    for c in manifest["colours"]:
        digest = digest_map[c["digest_source"]]
        colours_list.append(
            _colour(
                colour_id=c["colour_id"],
                family=c["family"],
                schema_ref=c["schema_ref"],
                validator_ref=c["validator_ref"],
                validator_digest=digest,
            )
        )
    colours = tuple(colours_list)
    by_id = {colour.colour_id: colour for colour in colours}

    def port(port_id: str, colour_id: str) -> PortSpec:
        colour = by_id[colour_id]
        return PortSpec(port_id, colour.colour_id, colour.schema_ref)

    operations_list: list[OperationSpec] = []
    for op in manifest["operations"]:
        executor_digest = digest_map[op["digest_source"]]
        inputs = tuple(op["inputs"])
        operations_list.append(
            OperationSpec(
                operation_id=op["operation_id"],
                version="v1",
                input_ports=tuple(
                    port(f"input-{index}", colour_id)
                    for index, colour_id in enumerate(inputs)
                ),
                output_port=port("output", op["output"]),
                executor_ref=op["executor_ref"],
                executor_digest=executor_digest,
                invocation_grade=InvocationGrade.DISCIPLINE,
                authority_effect=AuthorityEffect.NONE,
                authority_ceiling=AuthorityEffect.NONE,
            )
        )
    operations = tuple(operations_list)
    return colours, operations


def presentation_id() -> str:
    colours, operations = prompt_civilization_presentation()
    return cast(
        str,
        canonical_id(
            "omega.prompt-civilization.operad-presentation.v1",
            {
                "colours": [colour.to_canonical() for colour in colours],
                "operations": [operation.to_canonical() for operation in operations],
                "path2_claims": [],
                "authority_effect": "None",
            },
        ),
    )


__all__ = ["presentation_id", "prompt_civilization_presentation"]
