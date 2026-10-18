"""Contracted cycle-aware traversal engine.

The candidate construction and correction actions live under ``operator``;
this engine only coordinates one traversal step and carries no authority.
"""

from __future__ import annotations

from typing import Any, Final

from omega_engine.crates.operator.generator.gen_cycle_aware import CycleAwareGenerator
from omega_engine.crates.engine.base.eng_base import Engine

CONTRACT_ID: Final[str] = "urn:omega:engine:cycle_aware_engine:file:v1.0.0"


class CycleAwareEngine(Engine):
    authority_effect: Final[str] = "None"
    implements: Final[tuple[str, ...]] = (CONTRACT_ID,)

    def __init__(self, generator: CycleAwareGenerator):
        super().__init__(engine_id="cycle_aware_engine", engine_version="v1.0.0")
        self.generator = generator

    def traverse(self, state: Any) -> list[Any]:
        return self.generator.generate(state)


__all__ = ["CONTRACT_ID", "CycleAwareEngine"]
