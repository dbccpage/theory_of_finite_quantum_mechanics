"""Protocols and interfaces for prompt civilization ports.

AuthorityEffect: None.
"""

from __future__ import annotations

from typing import Protocol, Sequence, runtime_checkable

from .models import AntiSkillSpecV1, PromptReviewReceiptV1, TypedPromptV1


@runtime_checkable
class AntiSkillRegistryProtocol(Protocol):
    """Port for anti-skill registry storage and lookup."""

    @property
    def registry_id(self) -> str:
        ...

    def get(self, rule_id: str) -> AntiSkillSpecV1 | None:
        ...

    def list_rules(self) -> Sequence[AntiSkillSpecV1]:
        ...


@runtime_checkable
class PromptReviewerProtocol(Protocol):
    """Port for deterministic prompt review execution."""

    def review_prompt(
        self,
        prompt: TypedPromptV1,
        registry: AntiSkillRegistryProtocol,
    ) -> PromptReviewReceiptV1:
        ...
