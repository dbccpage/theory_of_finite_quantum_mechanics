"""Inert prompt-intake records shared by intake components."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Optional


@dataclass
class PromptGeometry:
    prompt_class: str = ""
    morphism_type: str = ""
    entropy: float = 0.0
    coherence: float = 0.0
    decidability: float = 0.0
    hostility: float = 0.0
    fingerprint: str = ""

    def status(self) -> str:
        return "stubbed"


@dataclass
class PromptRecord:
    id: str
    raw_prompt: str
    expected_answer: Optional[str] = None
    geometry: PromptGeometry = field(default_factory=PromptGeometry)


@dataclass
class CotRecord:
    id: str
    obstructed_prompt: str
    cot_steps: list
    final_answer: str
    geometry: PromptGeometry = field(default_factory=PromptGeometry)


__all__ = ["PromptGeometry", "PromptRecord", "CotRecord"]
