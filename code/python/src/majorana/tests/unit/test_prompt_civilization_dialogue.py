from __future__ import annotations

from dataclasses import replace
import json
from pathlib import Path

from omega_engine.crates.prompt_civilization import (
    CandidateAnnotationV1,
    ConversationEpisodeV1,
    Err,
    mine_candidates,
    segment_dialogue,
)


ROOT = Path(__file__).resolve().parents[2]
SOURCE = ROOT / "_ooutwire" / "2026-08-13-132939-local-command-caveatcaveat-the-messages-below.txt"
SOURCE_DIGEST = "sha256:0ed2e983d596827e5d8e985eb8dfe8e40fad7abe5c43185ceed179d659c5820d"


def test_extracts_exactly_five_substantive_dialogue_pairs() -> None:
    result = segment_dialogue(
        SOURCE,
        start_line=12693,
        end_line=13354,
        session_id="fable-2026-08-13",
        task_id="primitive-difference-audit",
        model_id="claude-opus-5",
    )
    episodes = result.unwrap()
    assert len(episodes) == 5
    assert all(episode.source_digest == SOURCE_DIGEST for episode in episodes)
    assert [episode.ordinal for episode in episodes] == [1, 2, 3, 4, 5]
    combined = "\n".join(
        episode.user_text + "\n" + episode.assistant_text for episode in episodes
    )
    assert "Write(" not in combined
    assert "Bash(" not in combined
    assert "※ recap:" not in combined
    assert "✻ " not in combined


def test_episode_jsonl_round_trip_preserves_ids() -> None:
    episodes = segment_dialogue(SOURCE, start_line=12693, end_line=13354).unwrap()
    raw = "\n".join(
        json.dumps(episode.to_dict(), ensure_ascii=False, sort_keys=True)
        for episode in episodes
    ).encode("utf-8")
    replayed = segment_dialogue(
        raw, source_format="omega-conversation-episode-jsonl-v1"
    ).unwrap()
    assert [episode.episode_id for episode in replayed] == [
        episode.episode_id for episode in episodes
    ]


def test_unsupported_dialogue_format_refuses() -> None:
    result = segment_dialogue(b"speaker one: hello\nspeaker two: hello")
    assert isinstance(result, Err)
    assert result.error.code == "UNSUPPORTED_DIALOGUE_FORMAT"


def _annotated_episode(
    *,
    ordinal: int,
    source_byte: bytes,
    context: str,
) -> ConversationEpisodeV1:
    from omega_engine.crates.prompt_civilization.models import sha256_ref

    return ConversationEpisodeV1(
        source_digest=sha256_ref(source_byte),
        source_format="claude-terminal-export-v1",
        ordinal=ordinal,
        user_label="Jeremy",
        user_text=f"Correction {ordinal}",
        assistant_label="Fable",
        assistant_text=f"Acknowledged {ordinal}",
        session_id=context,
        annotation=CandidateAnnotationV1(
            failure_code="DECLARATION_AS_DERIVATION",
            proposed_invariant="Separate declarations from derived consequences.",
            counterexamples=("An explicitly scoped conditional theorem is legitimate.",),
            protected_fields=("evidence_requirements", "nonclaims"),
            evidence_refs=(f"receipt:{context}",),
        ),
    )


def test_miner_deduplicates_episode_ids_and_keeps_context_independence_visible() -> None:
    first = _annotated_episode(ordinal=1, source_byte=b"a", context="session-a")
    duplicate = ConversationEpisodeV1.from_dict(first.to_dict())
    copied_export = _annotated_episode(
        ordinal=1, source_byte=b"copy", context="session-copy"
    )
    second = _annotated_episode(ordinal=2, source_byte=b"b", context="session-b")
    candidates = mine_candidates([first, duplicate, copied_export, second])
    assert len(candidates) == 1
    assert len(candidates[0].episode_ids) == 2
    assert candidates[0].context_keys == ("session-a", "session-b")
    assert candidates[0].status == "PROPOSED"
    assert candidates[0].authority_effect == "None"


def test_incomplete_annotation_emits_no_candidate() -> None:
    episode = _annotated_episode(ordinal=1, source_byte=b"a", context="session-a")
    incomplete = replace(
        episode,
        annotation=CandidateAnnotationV1(),
        episode_id="",
    )
    assert mine_candidates([incomplete]) == []
