"""Everett DAG value types."""

from dataclasses import dataclass, field
from typing import Optional


@dataclass(frozen=True)
class EverettNodeId:
    val: str

    def __str__(self) -> str:
        return self.val


@dataclass
class EverettNode:
    id: EverettNodeId
    amplitude: float
    configuration_sign_field: list[int]
    child_indices: list[int] = field(default_factory=list)

    def __init__(self, id_val, amplitude: float, configuration_sign_field: list, child_indices: Optional[list] = None):
        self.id = id_val if isinstance(id_val, EverettNodeId) else EverettNodeId(str(id_val))
        self.amplitude = float(amplitude)
        self.configuration_sign_field = [int(value) for value in configuration_sign_field]
        self.child_indices = list(child_indices) if child_indices is not None else []


@dataclass
class EverettArena:
    nodes: list[EverettNode] = field(default_factory=list)


__all__ = ["EverettArena", "EverettNode", "EverettNodeId"]
