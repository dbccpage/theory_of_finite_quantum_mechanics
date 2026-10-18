"""Conversation segmentation and candidate-only anti-skill mining use cases.

AuthorityEffect: None.
"""

from __future__ import annotations

import json
from pathlib import Path
import re
from typing import cast, Iterable

from omega_engine.kernel.higher_operad.canonical import canonical_id
from omega_engine_operations.domain.rop.result import Err, Ok, Refusal, Result

from ..domain.models import AntiSkillCandidateV1, ConversationEpisodeV1, sha256_ref
from ..domain.json_wire import loads_strict_json


CLAUDE_FORMAT = "claude-terminal-export-v1"
JSONL_FORMAT = "omega-conversation-episode-jsonl-v1"

_TOOL_PREFIXES = (
    "Agent(",
    "Bash(",
    "Edit(",
    "Glob(",
    "Grep(",
    "Read(",
    "Skill(",
    "Task(",
    "Update(",
    "Write(",
)


def _read_source(source: Path | bytes) -> tuple[bytes, str]:
    if isinstance(source, Path):
        raw = source.read_bytes().replace(b"\r\n", b"\n").replace(b"\r", b"\n")
        locus = str(source)
    elif type(source) is bytes:
        raw = source.replace(b"\r\n", b"\n").replace(b"\r", b"\n")
        locus = "<bytes>"
    else:
        raise TypeError("source must be pathlib.Path or exact bytes")
    if len(raw) > 32 * 1024 * 1024:
        raise ValueError("dialogue source exceeds the 32 MiB limit")
    return raw, locus


def _normalize_terminal_body(lines: list[str]) -> str:
    paragraphs: list[str] = []
    current: list[str] = []
    for raw in lines:
        stripped = raw.strip()
        if not stripped:
            if current:
                paragraphs.append(" ".join(current))
                current = []
            continue
        current.append(stripped)
    if current:
        paragraphs.append(" ".join(current))
    return "\n\n".join(
        paragraph
        for paragraph in paragraphs
        if not paragraph.startswith(("✻", "※ recap:"))
    ).strip()


def _is_tool_turn(body: str) -> bool:
    first = body.splitlines()[0].strip() if body else ""
    return first.startswith(_TOOL_PREFIXES)


def _segment_claude(
    raw: bytes,
    *,
    start_line: int | None,
    end_line: int | None,
    session_id: str,
    task_id: str,
    model_id: str,
) -> list[ConversationEpisodeV1]:
    text = raw.decode("utf-8", errors="strict")
    lines = text.splitlines()
    start = 1 if start_line is None else start_line
    end = len(lines) if end_line is None else end_line
    if start < 1 or end < start or end > len(lines):
        raise ValueError("line bounds are outside the source")

    turns: list[tuple[str, list[str]]] = []
    for raw_line in lines[start - 1 : end]:
        if raw_line.startswith("❯ "):
            turns.append(("user", [raw_line[2:]]))
        elif raw_line.startswith("● "):
            turns.append(("assistant", [raw_line[2:]]))
        elif turns:
            turns[-1][1].append(raw_line)

    normalized: list[tuple[str, str]] = []
    for role, body_lines in turns:
        body = _normalize_terminal_body(body_lines)
        if body:
            normalized.append((role, body))
    episodes: list[ConversationEpisodeV1] = []
    pending_user: str | None = None
    source_digest = sha256_ref(raw)
    for role, body in normalized:
        if role == "user":
            pending_user = body
            continue
        if _is_tool_turn(body):
            continue
        if pending_user is None:
            continue
        episodes.append(
            ConversationEpisodeV1(
                source_digest=source_digest,
                source_format=CLAUDE_FORMAT,
                ordinal=len(episodes) + 1,
                user_label="Jeremy",
                user_text=pending_user,
                assistant_label="Fable",
                assistant_text=body,
                session_id=session_id,
                task_id=task_id,
                model_id=model_id,
            )
        )
        pending_user = None
    return episodes


def _segment_jsonl(raw: bytes) -> list[ConversationEpisodeV1]:
    text = raw.decode("utf-8", errors="strict")
    episodes: list[ConversationEpisodeV1] = []
    for line_number, line in enumerate(text.splitlines(), start=1):
        if not line.strip():
            continue
        try:
            wire = loads_strict_json(line)
            episodes.append(ConversationEpisodeV1.from_dict(wire))
        except (json.JSONDecodeError, TypeError, ValueError) as exc:
            raise ValueError(f"invalid episode JSONL at line {line_number}: {exc}") from exc
    return episodes


def segment_dialogue(
    source: Path | bytes,
    *,
    source_format: str = "auto",
    start_line: int | None = None,
    end_line: int | None = None,
    session_id: str = "",
    task_id: str = "",
    model_id: str = "",
) -> Result[list[ConversationEpisodeV1], Refusal]:
    """Segment a supported transcript without treating it as evidence of truth."""

    try:
        raw, locus = _read_source(source)
        selected = source_format
        if selected == "auto":
            sample = raw[:64 * 1024].decode("utf-8", errors="strict")
            if "❯ " in sample and "● " in sample:
                selected = CLAUDE_FORMAT
            elif sample.lstrip().startswith("{"):
                selected = JSONL_FORMAT
            else:
                return Err(
                    Refusal(
                        code="UNSUPPORTED_DIALOGUE_FORMAT",
                        message="source is neither a Claude terminal export nor episode JSONL",
                        locus=locus,
                    )
                )
        if selected == CLAUDE_FORMAT:
            episodes = _segment_claude(
                raw,
                start_line=start_line,
                end_line=end_line,
                session_id=session_id,
                task_id=task_id,
                model_id=model_id,
            )
        elif selected == JSONL_FORMAT:
            if start_line is not None or end_line is not None:
                raise ValueError("line bounds are not supported for canonical JSONL")
            episodes = _segment_jsonl(raw)
        else:
            return Err(
                Refusal(
                    code="UNSUPPORTED_DIALOGUE_FORMAT",
                    message=f"unsupported source_format: {selected}",
                    locus=locus,
                )
            )
        if not episodes:
            return Err(
                Refusal(
                    code="NO_DIALOGUE_EPISODES",
                    message="no complete user/assistant episode was found",
                    locus=locus,
                )
            )
        return Ok(episodes)
    except (OSError, UnicodeDecodeError, TypeError, ValueError) as exc:
        return Err(
            Refusal(
                code="DIALOGUE_SEGMENTATION_REFUSED",
                message=str(exc),
                locus=str(source) if isinstance(source, Path) else "<bytes>",
            )
        )


def _slug_failure_code(value: str) -> str:
    slug = re.sub(r"[^a-z0-9]+", "-", value.casefold()).strip("-")
    return (slug or "unclassified-correction") + "-candidate"


def _context_key(episode: ConversationEpisodeV1) -> str:
    explicit = "|".join(
        value
        for value in (episode.session_id, episode.task_id, episode.model_id)
        if value
    )
    return explicit or episode.source_digest


def _episode_content_key(episode: ConversationEpisodeV1) -> str:
    """Deduplicate copied dialogue independently of export and annotation data."""

    return cast(
        str,
        canonical_id(
            "omega.antiskill.dialogue-content.v1",
            {
                "user_label": episode.user_label,
                "user_text": episode.user_text,
                "assistant_label": episode.assistant_label,
                "assistant_text": episode.assistant_text,
            },
        ),
    )


def mine_candidates(
    episodes: Iterable[ConversationEpisodeV1],
) -> list[AntiSkillCandidateV1]:
    """Compile human/model annotations into candidates, never admitted specs.

    Unannotated or incomplete episodes are intentionally ignored.  The model may
    propose an annotation, but the exact counterexample and evidence fields must
    survive validation before a candidate is emitted.
    """

    unique: dict[str, ConversationEpisodeV1] = {}
    for episode in episodes:
        reparsed = ConversationEpisodeV1.from_dict(episode.to_dict())
        unique.setdefault(_episode_content_key(reparsed), reparsed)

    grouped: dict[tuple[str, str], list[ConversationEpisodeV1]] = {}
    for episode in unique.values():
        annotation = episode.annotation
        if not annotation.is_complete:
            continue
        grouped.setdefault(
            (annotation.failure_code, annotation.proposed_invariant), []
        ).append(episode)

    candidates: list[AntiSkillCandidateV1] = []
    for (failure_code, invariant), group in sorted(grouped.items()):
        group.sort(key=lambda item: item.episode_id)
        candidates.append(
            AntiSkillCandidateV1(
                name=_slug_failure_code(failure_code),
                failure_code=failure_code,
                proposed_invariant=invariant,
                episode_ids=tuple(item.episode_id for item in group),
                context_keys=tuple(sorted({_context_key(item) for item in group})),
                evidence_refs=tuple(
                    sorted(
                        {
                            evidence
                            for item in group
                            for evidence in item.annotation.evidence_refs
                        }
                    )
                ),
                counterexamples=tuple(
                    sorted(
                        {
                            example
                            for item in group
                            for example in item.annotation.counterexamples
                        }
                    )
                ),
                protected_fields=tuple(
                    sorted(
                        {
                            field
                            for item in group
                            for field in item.annotation.protected_fields
                        }
                    )
                ),
            )
        )
    return candidates


__all__ = [
    "CLAUDE_FORMAT",
    "JSONL_FORMAT",
    "mine_candidates",
    "segment_dialogue",
]
