from __future__ import annotations

from omega_engine.crates.prompt_civilization import (
    presentation_id,
    prompt_civilization_presentation,
)
from omega_engine.kernel.higher_operad.model import AuthorityEffect
from omega_engine.kernel.higher_operad.terms import Primitive, substitute


def test_prompt_operations_have_exact_declared_boundaries_and_no_authority() -> None:
    colours, operations = prompt_civilization_presentation()
    assert len(colours) == 10
    assert len({colour.schema_digest for colour in colours}) == 10
    packet_colour = next(
        colour for colour in colours if colour.colour_id == "PacketEnvelope"
    )
    assert packet_colour.validator_ref == "omega.symbol-game.packets.v2"
    by_id = {operation.operation_id: operation for operation in operations}
    expected = {
        "omega-prompt-detect": (("PromptArtifact",), "FindingSet"),
        "omega-prompt-repair-proposal": (
            ("PromptArtifact", "FindingSet"),
            "PromptCandidate",
        ),
        "omega-prompt-verify": (
            ("PromptArtifact", "PromptCandidate"),
            "ReviewReceipt",
        ),
        "omega-prompt-approve": (
            ("PromptCandidate", "ReviewReceipt", "OperatorDecision"),
            "ApprovedPrompt",
        ),
        "omega-prompt-packetize": (("ApprovedPrompt",), "PacketEnvelope"),
        "auto-antiskill-segment": (("RawDialogue",), "EpisodeSet"),
        "auto-antiskill-mine-candidate": (
            ("EpisodeSet",),
            "AntiSkillCandidateSet",
        ),
    }
    assert set(by_id) == set(expected)
    for operation_id, (inputs, output) in expected.items():
        operation = by_id[operation_id]
        assert tuple(port.colour_id for port in operation.input_ports) == inputs
        assert operation.output_port.colour_id == output
        assert operation.authority_effect is AuthorityEffect.NONE
        assert operation.authority_ceiling is AuthorityEffect.NONE


def test_detection_substitutes_into_repair_without_claiming_copy_or_equivalence() -> None:
    _, operations = prompt_civilization_presentation()
    by_id = {operation.operation_id: operation for operation in operations}
    composed = substitute(
        Primitive(by_id["omega-prompt-repair-proposal"]),
        1,
        Primitive(by_id["omega-prompt-detect"]),
    ).unwrap()
    assert tuple(port.colour_id for port in composed.boundary.inputs) == (
        "PromptArtifact",
        "PromptArtifact",
    )
    assert composed.boundary.output.colour_id == "PromptCandidate"


def test_operad_presentation_has_deterministic_id_and_no_path_claims() -> None:
    assert presentation_id() == presentation_id()
    assert presentation_id().startswith("sha256:")
