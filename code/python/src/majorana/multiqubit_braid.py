"""Multi-qubit mode-block braid words from historical gate labels.

AuthorityEffect: None.
"""

from __future__ import annotations

from dataclasses import dataclass
import json
from typing import Any, Dict, List, Sequence

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

    def check_qubit(qubit: int) -> None:
        if qubit < 1 or qubit > num_qubits:
            raise MultiQubitBraidError(f"qubit={qubit} out of range [1, {num_qubits}]")

    def append_block_swap(first: int, second: int) -> None:
        start = 4 * min(first, second) - 3
        for offset in range(4):
            for index in range(start + 3 - offset, start + 7 - offset):
                push(index, False)

    for op in operations:
        if op.kind == "Elementary":
            if op.index < 1 or op.index >= num_modes:
                raise MultiQubitBraidError(f"index {op.index} out of range 1..{num_modes}")
            push(op.index, op.inverse)
        elif op.kind == "Phase":
            check_qubit(op.qubit)
            push(4 * op.qubit - 3, op.inverse)
        elif op.kind == "Hadamard":
            check_qubit(op.qubit)
            push(4 * op.qubit - 2, op.inverse)
            push(4 * op.qubit - 3, op.inverse)
            push(4 * op.qubit - 2, op.inverse)
        elif op.kind == "Swap":
            q1, q2 = op.first, op.second
            check_qubit(q1)
            check_qubit(q2)
            if abs(q1 - q2) != 1:
                raise MultiQubitBraidError("Adjacent swap requires |q1 - q2| == 1")
            append_block_swap(q1, q2)
        elif op.kind == "Cnot":
            c, t = op.control, op.target
            check_qubit(c)
            check_qubit(t)
            if c == t:
                raise MultiQubitBraidError("Control and target qubits must be distinct")
            routing_start = len(steps)
            current_target = t
            while abs(current_target - c) > 1:
                next_target = current_target - 1 if t > c else current_target + 1
                append_block_swap(current_target, next_target)
                current_target = next_target
            routing_end = len(steps)
            push(4 * min(c, current_target), False)
            for position in range(routing_end - 1, routing_start - 1, -1):
                index, inverse = steps[position]
                push(index, not inverse)

    action = MajoranaBraidAction.from_word(num_modes, steps)
    return CompiledMultiQubitBraid(
        num_qubits=num_qubits,
        gate_count=len(operations),
        steps=steps,
        action=action,
    )


def compile_multiqubit_braid(
    num_qubits: int,
    operations: Sequence[MultiQubitOperation],
) -> CompiledMultiQubitBraid:
    """Alias matching Rust compile_multiqubit_braid."""
    return compile_multi_qubit_braid(num_qubits, operations, DEFAULT_MAX_COMPILED_STEPS)


def compile_multiqubit_braid_with_limit(
    num_qubits: int,
    operations: Sequence[MultiQubitOperation],
    max_steps: int,
) -> CompiledMultiQubitBraid:
    """Alias matching Rust compile_multiqubit_braid_with_limit."""
    return compile_multi_qubit_braid(num_qubits, operations, max_steps)


@dataclass(frozen=True)
class MultiQubitBraidScalingRow:
    """Multi-qubit braid scaling row matching Rust MultiQubitBraidScalingRow."""
    num_qubits: int
    mode_count: int
    cnot_steps: int
    determinant_sign: int
    inverse_restores_identity: bool

    def to_dict(self) -> Dict[str, Any]:
        return {
            "num_qubits": self.num_qubits,
            "mode_count": self.mode_count,
            "cnot_steps": self.cnot_steps,
            "determinant_sign": self.determinant_sign,
            "inverse_restores_identity": self.inverse_restores_identity,
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "MultiQubitBraidScalingRow":
        return cls(
            num_qubits=int(data["num_qubits"]),
            mode_count=int(data["mode_count"]),
            cnot_steps=int(data["cnot_steps"]),
            determinant_sign=int(data["determinant_sign"]),
            inverse_restores_identity=bool(data["inverse_restores_identity"]),
        )


def benchmark_multiqubit_braid_scaling(
    qubit_counts: Sequence[int],
) -> List[MultiQubitBraidScalingRow]:
    """Finite register scaling benchmark for multi-qubit Majorana braid compilation across
    declared qubit counts N_q (4 * N_q Majorana modes, up to 16 qubits / 64 modes).
    Matches Rust tfqm_majorana::benchmark_multiqubit_braid_scaling bit-for-bit.
    """
    rows: List[MultiQubitBraidScalingRow] = []
    for nq in qubit_counts:
        if nq < 2:
            raise MultiQubitBraidError("num_qubits must be >= 2 for CNOT scaling benchmark")
        ops = [MultiQubitOperation.Cnot(control=1, target=nq)]
        compiled = compile_multiqubit_braid(nq, ops)
        inv = compiled.action.inverse()
        prod = compiled.action.compose(inv)
        ident = MajoranaBraidAction.identity(4 * nq)
        rows.append(
            MultiQubitBraidScalingRow(
                num_qubits=nq,
                mode_count=4 * nq,
                cnot_steps=len(compiled.steps),
                determinant_sign=compiled.action.determinant_sign(),
                inverse_restores_identity=(prod == ident),
            )
        )
    return rows


def multiqubit_braid_scaling_to_canonical_json(rows: Sequence[MultiQubitBraidScalingRow]) -> str:
    """Serialize MultiQubitBraidScalingRow list to canonical 2-space pretty JSON with LF line endings."""
    return json.dumps([row.to_dict() for row in rows], indent=2)


def multiqubit_braid_scaling_from_canonical_json(json_str: str) -> List[MultiQubitBraidScalingRow]:
    """Deserialize MultiQubitBraidScalingRow list from canonical JSON string."""
    raw = json.loads(json_str)
    return [MultiQubitBraidScalingRow.from_dict(item) for item in raw]

