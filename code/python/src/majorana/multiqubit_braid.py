"""Multi-qubit mode-block braid words from historical gate labels.

AuthorityEffect: None.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Sequence

from .braid_action import (
    BraidActionError,
    MajoranaBraidAction,
    MAX_BRAID_MODES,
)

DEFAULT_MAX_COMPILED_STEPS: int = 65_536


class MultiQubitBraidError(Exception):
    pass


@dataclass(frozen=True)
class MultiQubitOperation:
    kind: str  # "Elementary", "Phase", "Hadamard", "Cnot", "Swap"
    index: int = 0
    qubit: int = 0
    control: int = 0
    target: int = 0
    first: int = 0
    second: int = 0
    inverse: bool = False

    @classmethod
    def Elementary(cls, index: int, inverse: bool = False) -> MultiQubitOperation:
        return cls(kind="Elementary", index=index, inverse=inverse)

    @classmethod
    def Phase(cls, qubit: int, inverse: bool = False) -> MultiQubitOperation:
        return cls(kind="Phase", qubit=qubit, inverse=inverse)

    @classmethod
    def Hadamard(cls, qubit: int, inverse: bool = False) -> MultiQubitOperation:
        return cls(kind="Hadamard", qubit=qubit, inverse=inverse)

    @classmethod
    def Cnot(cls, control: int, target: int) -> MultiQubitOperation:
        return cls(kind="Cnot", control=control, target=target)

    @classmethod
    def Swap(cls, first: int, second: int) -> MultiQubitOperation:
        return cls(kind="Swap", first=first, second=second)


@dataclass
class CompiledMultiQubitBraid:
    num_qubits: int
    gate_count: int
    steps: list[tuple[int, bool]]
    action: MajoranaBraidAction


def compile_multi_qubit_braid(
    num_qubits: int,
    operations: Sequence[MultiQubitOperation],
    max_steps: int = DEFAULT_MAX_COMPILED_STEPS,
) -> CompiledMultiQubitBraid:
    if num_qubits < 1 or num_qubits * 4 > MAX_BRAID_MODES:
        raise MultiQubitBraidError("num_qubits must be >= 1 within braid mode bound")

    num_modes = num_qubits * 4
    steps: list[tuple[int, bool]] = []

    def push(idx: int, inv: bool) -> None:
        if len(steps) >= max_steps:
            raise MultiQubitBraidError(f"compiled braid word exceeds limit {max_steps}")
        steps.append((idx, inv))

    for op in operations:
        if op.kind == "Elementary":
            if op.index < 1 or op.index >= num_modes:
                raise MultiQubitBraidError(f"index {op.index} out of range 1..{num_modes}")
            push(op.index, op.inverse)
        elif op.kind == "Phase":
            if op.qubit < 1 or op.qubit > num_qubits:
                raise MultiQubitBraidError(f"qubit={op.qubit} out of range [1, {num_qubits}]")
            # Phase gate: elementary braid on middle modes of qubit block
            mid = 4 * (op.qubit - 1) + 2
            push(mid, op.inverse)
        elif op.kind == "Hadamard":
            if op.qubit < 1 or op.qubit > num_qubits:
                raise MultiQubitBraidError(f"qubit={op.qubit} out of range [1, {num_qubits}]")
            base = 4 * (op.qubit - 1) + 1
            if not op.inverse:
                push(base + 1, False)
                push(base, False)
                push(base + 1, False)
            else:
                push(base + 1, True)
                push(base, True)
                push(base + 1, True)
        elif op.kind == "Swap":
            q1, q2 = op.first, op.second
            if q1 < 1 or q1 > num_qubits or q2 < 1 or q2 > num_qubits:
                raise MultiQubitBraidError("qubit out of range")
            if abs(q1 - q2) != 1:
                raise MultiQubitBraidError("Adjacent swap requires |q1 - q2| == 1")
            lo = min(q1, q2)
            base = 4 * (lo - 1) + 1
            # 4-mode block swap
            for i in range(4):
                for j in range(3, -1, -1):
                    push(base + i + j, False)
        elif op.kind == "Cnot":
            c, t = op.control, op.target
            if c < 1 or c > num_qubits or t < 1 or t > num_qubits:
                raise MultiQubitBraidError("qubit out of range")
            if c == t:
                raise MultiQubitBraidError("Control and target qubits must be distinct")
            # Synthesize non-local CNOT bridge
            b_c = 4 * (c - 1) + 2
            b_t = 4 * (t - 1) + 2
            lo, hi = min(b_c, b_t), max(b_c, b_t)
            for k in range(lo, hi):
                push(k, False)
            push(hi, False)
            for k in range(hi - 1, lo - 1, -1):
                push(k, True)

    action = MajoranaBraidAction.from_word(num_modes, steps)
    return CompiledMultiQubitBraid(
        num_qubits=num_qubits,
        gate_count=len(operations),
        steps=steps,
        action=action,
    )
