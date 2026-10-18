"""majorana_multiqubit_noise.py — Multi-Qubit Braided Clifford Operations with Local Noise.

AuthorityEffect: None.
Reference: sealed-derivation-v1 (3100c4e), Claim MAJ-C7/MAJ-C8, gemini_000.md.

Implements:
1. Multi-Qubit Majorana Carrier Encoding:
   - Encodes N logical qubits into 4N Majorana zero modes (2 pairs = 4 modes per qubit).
   - Qubit q occupies modes gamma_{4q-3}, gamma_{4q-2}, gamma_{4q-1}, gamma_{4q}.
2. Braided Clifford Gate Synthesis:
   - Phase gate S_q: Elementary braid R_{4q-3}.
   - Hadamard gate H_q: Composite braid sequence R_{4q-2} R_{4q-3} R_{4q-2}.
   - Entangling CNOT / Inter-Qubit Braid: Braids bridging adjacent qubit clusters.
3. Local Hamiltonian Noise Perturbations:
   - Models stray quasiparticle or local defect Hamiltonian H_noise = sum_{a < b} eps_{ab} (i gamma_a gamma_b).
   - Evaluates commutator defect [H_noise, gamma_k] and circuit transformation defect ||U K U^T - K||.
   - All calculations performed in exact rational arithmetic (fractions.Fraction) under Zero-Float Law.
4. Proposal Fidelity Protocol (PFP) Referee Noise Gate:
   - Evaluates multi-qubit braided circuits under noise.
   - Classifies proposals into ACCEPTED_STABLE or REFUSAL_NOISE_LEAKAGE based on rational threshold.
"""

from __future__ import annotations

import hashlib
import json
from dataclasses import dataclass
from fractions import Fraction
from typing import Any, List, Sequence, Tuple

from majorana_braid_exact import ExactSignedPermutationMatrix, MajoranaBraidCircuit

from omega_engine_operating_system.adapters.rust_host.majorana_math import (
    NativeMathRefusal,
    call_native,
    decode_rational,
)


def _exact_wire(value: Fraction | int, label: str) -> str:
    if isinstance(value, (float, bool)) or not isinstance(value, (int, Fraction)):
        raise TypeError(f"{label} must be Fraction or int")
    return str(Fraction(value))


def _inverse_flag(value: object) -> bool:
    if type(value) is bool:
        return value
    if type(value) is int and value in (0, 1):
        return value == 1
    raise TypeError("inverse must be bool or integer 0/1")


def _matrix_wire(matrix: Any) -> dict[str, Any]:
    return {
        "dim": matrix.dim,
        "data": [[str(Fraction(value)) for value in row] for row in matrix.data],
    }


@dataclass(frozen=True)
class LocalMajoranaNoise:
    """Validated rational skew Hamiltonian; numerical operations execute in Rust."""

    dim: int
    data: Tuple[Tuple[Fraction, ...], ...]

    def __post_init__(self) -> None:
        if not isinstance(self.dim, int) or isinstance(self.dim, bool) or self.dim < 2:
            raise ValueError(f"dim must be integer >= 2, got {self.dim}")
        if len(self.data) != self.dim or any(len(row) != self.dim for row in self.data):
            raise ValueError(f"Data shape must be {self.dim}x{self.dim}")
        rows = [[_exact_wire(value, "Matrix entries") for value in row] for row in self.data]
        call_native("majorana_noise", {"operation": "from_rows", "dim": self.dim, "data": rows})
        object.__setattr__(
            self, "data", tuple(tuple(Fraction(value) for value in row) for row in rows)
        )

    @classmethod
    def _from_native(cls, value: dict[str, Any]) -> LocalMajoranaNoise:
        dim = value.get("dim", value.get("rows"))
        data = value.get("data")
        if (
            type(dim) is not int
            or dim < 2
            or not isinstance(data, (list, tuple))
            or len(data) != dim
            or any(not isinstance(row, (list, tuple)) or len(row) != dim for row in data)
        ):
            raise NativeMathRefusal(
                "NATIVE_MATH_NOISE_SHAPE", "native noise matrix must be square", outcome=value
            )
        rows = tuple(tuple(decode_rational(entry) for entry in row) for row in data)
        noise = object.__new__(cls)
        object.__setattr__(noise, "dim", dim)
        object.__setattr__(noise, "data", rows)
        return noise

    @classmethod
    def zero(cls, dim: int) -> LocalMajoranaNoise:
        return cls._from_native(call_native("majorana_noise", {"operation": "zero", "dim": dim}))

    @classmethod
    def single_pair(cls, dim: int, a: int, b: int, epsilon: Fraction) -> LocalMajoranaNoise:
        if a == b:
            raise ValueError("Modes a and b must be distinct")
        return cls.stray_couplings(dim, [(a, b, Fraction(_exact_wire(epsilon, "epsilon")))])

    @classmethod
    def stray_couplings(
        cls, dim: int, couplings: Sequence[Tuple[int, int, Fraction]]
    ) -> LocalMajoranaNoise:
        wire = [[a, b, _exact_wire(epsilon, "Coupling epsilon")] for a, b, epsilon in couplings]
        return cls._from_native(
            call_native(
                "majorana_noise", {"operation": "stray_couplings", "dim": dim, "couplings": wire}
            )
        )

    @classmethod
    def correlated_cluster_couplings(
        cls, num_qubits: int, lattice_l: int, budget: Fraction, seed: int = 1
    ) -> Tuple[Tuple[int, int, Fraction], ...]:
        result = call_native(
            "majorana_noise",
            {
                "operation": "correlated",
                "num_qubits": num_qubits,
                "lattice_l": lattice_l,
                "budget": _exact_wire(budget, "budget"),
                "seed": seed,
            },
        )
        return tuple((a, b, decode_rational(value)) for a, b, value in result["couplings"])

    def leakage_on_mode(self, mode: int) -> Fraction:
        result = call_native(
            "majorana_noise", {"operation": "leakage", "noise": _matrix_wire(self), "mode": mode}
        )
        return decode_rational(result["leakage_on_mode"])

    def max_leakage(self) -> Fraction:
        result = call_native(
            "majorana_noise", {"operation": "leakage", "noise": _matrix_wire(self)}
        )
        return decode_rational(result["max_leakage"])

    def transform(self, u: ExactSignedPermutationMatrix) -> LocalMajoranaNoise:
        if u.dim != self.dim:
            raise ValueError(f"Dimension mismatch: U.dim={u.dim} != noise.dim={self.dim}")
        result = call_native(
            "majorana_noise",
            {"operation": "transform", "noise": _matrix_wire(self), "matrix": _matrix_wire(u)},
        )
        return self._from_native(result)

    def commutation_defect(self, u: ExactSignedPermutationMatrix) -> Fraction:
        result = call_native(
            "majorana_noise",
            {
                "operation": "evaluate",
                "noise": _matrix_wire(self),
                "matrix": _matrix_wire(u),
                "tolerance_epsilon": "0",
            },
        )
        return decode_rational(result["circuit_noise_defect"])


class MultiQubitBraidCircuit:
    """Paper gate labels compiled to elementary braid words by omega_majorana."""

    def __init__(self, num_qubits: int) -> None:
        if not isinstance(num_qubits, int) or isinstance(num_qubits, bool) or num_qubits < 1:
            raise ValueError(f"num_qubits must be integer >= 1, got {num_qubits}")
        self.num_qubits = num_qubits
        self.num_modes = 4 * num_qubits
        self.underlying_circuit = MajoranaBraidCircuit(self.num_modes)
        self.operations: List[Tuple[str, Tuple[int, ...]]] = []

    def _append_operation(self, name: str, arguments: Tuple[int, ...]) -> MultiQubitBraidCircuit:
        operations = [*self.operations, (name, arguments)]
        result = call_native(
            "majorana_multiqubit_braid",
            {
                "num_qubits": self.num_qubits,
                "operations": [
                    [operation, [args[0], _inverse_flag(args[1])]]
                    if operation in {"elementary", "phase", "hadamard"}
                    else [operation, list(args)]
                    for operation, args in operations
                ],
            },
        )
        raw_steps = result.get("steps")
        if not isinstance(raw_steps, (list, tuple)):
            raise NativeMathRefusal(
                "NATIVE_MATH_BRAID_STEPS", "native braid steps must be pairs", outcome=result
            )
        steps = []
        for step in raw_steps:
            if (
                not isinstance(step, (list, tuple))
                or len(step) != 2
                or type(step[0]) is not int
                or not 1 <= step[0] < self.num_modes
                or type(step[1]) is not bool
            ):
                raise NativeMathRefusal(
                    "NATIVE_MATH_BRAID_STEPS",
                    "native braid steps require an index and boolean flag",
                    outcome=result,
                )
            steps.append((step[0], step[1]))
        self.operations = operations
        self.underlying_circuit.steps = steps
        return self

    def append_elementary(self, j: int, inverse: bool = False) -> MultiQubitBraidCircuit:
        return self._append_operation("elementary", (j, int(_inverse_flag(inverse))))

    def append_phase(self, qubit: int, inverse: bool = False) -> MultiQubitBraidCircuit:
        return self._append_operation("phase", (qubit, int(_inverse_flag(inverse))))

    def append_hadamard(self, qubit: int, inverse: bool = False) -> MultiQubitBraidCircuit:
        return self._append_operation("hadamard", (qubit, int(_inverse_flag(inverse))))

    def append_swap(self, q1: int, q2: int) -> MultiQubitBraidCircuit:
        return self._append_operation("swap", (q1, q2))

    def append_cnot(self, ctrl_qubit: int, tgt_qubit: int) -> MultiQubitBraidCircuit:
        if not (1 <= ctrl_qubit <= self.num_qubits and 1 <= tgt_qubit <= self.num_qubits):
            raise ValueError(f"Qubit index out of range [1, {self.num_qubits}]")
        return self._append_operation("cnot", (ctrl_qubit, tgt_qubit))

    def evaluate_matrix(self) -> ExactSignedPermutationMatrix:
        return self.underlying_circuit.evaluate_matrix()


@dataclass(frozen=True)
class MultiQubitNoisyBraidProposalPacket:
    """Proposal packet submitted to PFP referee containing a multi-qubit braided circuit and noise."""

    round_id: str
    proposer_id: str
    num_qubits: int
    operations: Tuple[Tuple[str, Tuple[int, ...]], ...]
    noise_couplings: Tuple[Tuple[int, int, Fraction], ...]
    tolerance_epsilon: Fraction

    def __post_init__(self) -> None:
        if isinstance(self.tolerance_epsilon, (float, bool)):
            raise TypeError("tolerance_epsilon must be Fraction or int")

    def canonical_digest(self) -> str:
        """Deterministic SHA-256 hash of proposal packet."""
        payload = {
            "round_id": self.round_id,
            "proposer_id": self.proposer_id,
            "num_qubits": self.num_qubits,
            "operations": [[op, list(args)] for op, args in self.operations],
            "noise_couplings": [[a, b, str(Fraction(eps))] for a, b, eps in self.noise_couplings],
            "tolerance_epsilon": str(Fraction(self.tolerance_epsilon)),
        }
        raw = json.dumps(payload, sort_keys=True, separators=(",", ":")).encode("utf-8")
        return hashlib.sha256(raw).hexdigest()


@dataclass(frozen=True)
class MultiQubitNoisyBraidReceipt:
    """Receipt emitted by the PFP Referee certifying multi-qubit stability under local noise."""

    receipt_id: str
    round_id: str
    proposer_id: str
    is_accepted: bool
    status_reason: str
    num_qubits: int
    num_modes: int
    gate_count: int
    is_so_dim: bool
    determinant: Fraction
    max_noise_leakage: Fraction
    circuit_noise_defect: Fraction
    tolerance_epsilon: Fraction
    sha256_hash: str
    authority_effect: str = "None"

    def canonical_digest(self) -> str:
        """Calculates deterministic SHA-256 hash of receipt contents."""
        payload = {
            "receipt_id": self.receipt_id,
            "round_id": self.round_id,
            "proposer_id": self.proposer_id,
            "is_accepted": self.is_accepted,
            "status_reason": self.status_reason,
            "num_qubits": self.num_qubits,
            "num_modes": self.num_modes,
            "gate_count": self.gate_count,
            "is_so_dim": self.is_so_dim,
            "determinant": str(self.determinant),
            "max_noise_leakage": str(self.max_noise_leakage),
            "circuit_noise_defect": str(self.circuit_noise_defect),
            "tolerance_epsilon": str(self.tolerance_epsilon),
            "authority_effect": self.authority_effect,
        }
        raw = json.dumps(payload, sort_keys=True, separators=(",", ":")).encode("utf-8")
        return hashlib.sha256(raw).hexdigest()


class MultiQubitNoisyBraidReferee:
    """PFP Referee evaluating multi-qubit braided Clifford operations under local noise perturbations."""

    def __init__(self, referee_id: str = "REF-MS-MAJORANA-PFP-NOISE-V1") -> None:
        self.referee_id = referee_id

    def evaluate(self, proposal: MultiQubitNoisyBraidProposalPacket) -> MultiQubitNoisyBraidReceipt:
        """Evaluates proposal packet against SO(4N) and noise leakage invariants."""
        if proposal.num_qubits < 1:
            return self._emit_rejection(
                proposal, "REFUSAL_INVALID_QUBITS", Fraction(0, 1), Fraction(0, 1)
            )

        num_modes = 4 * proposal.num_qubits

        try:
            circuit = MultiQubitBraidCircuit(proposal.num_qubits)
            for op, args in proposal.operations:
                if op == "elementary":
                    j, inv = args
                    circuit.append_elementary(j, inverse=inv)
                elif op == "phase":
                    q, inv = args
                    circuit.append_phase(q, inverse=inv)
                elif op == "hadamard":
                    q, inv = args
                    circuit.append_hadamard(q, inverse=inv)
                elif op == "cnot":
                    q1, q2 = args
                    circuit.append_cnot(q1, q2)
                elif op == "swap":
                    q1, q2 = args
                    circuit.append_swap(q1, q2)
                else:
                    return self._emit_rejection(
                        proposal, f"REFUSAL_UNKNOWN_OP_{op}", Fraction(0, 1), Fraction(0, 1)
                    )
        except NativeMathRefusal as exc:
            if exc.code != "NATIVE_MATH_REFUSED":
                raise
            return self._emit_rejection(
                proposal, f"REFUSAL_CIRCUIT_BUILD_FAILED: {exc}", Fraction(0, 1), Fraction(0, 1)
            )
        except Exception as exc:
            return self._emit_rejection(
                proposal, f"REFUSAL_CIRCUIT_BUILD_FAILED: {exc}", Fraction(0, 1), Fraction(0, 1)
            )

        mat = circuit.evaluate_matrix()
        is_ortho = mat.is_orthogonal()
        det = mat.determinant()
        is_so = is_ortho and det == Fraction(1, 1)

        if not is_so:
            return self._emit_rejection(
                proposal, "REFUSAL_NON_SO_MATRIX", Fraction(0, 1), Fraction(0, 1)
            )

        try:
            noise = LocalMajoranaNoise.stray_couplings(num_modes, proposal.noise_couplings)
        except NativeMathRefusal as exc:
            if exc.code != "NATIVE_MATH_REFUSED":
                raise
            return self._emit_rejection(
                proposal, f"REFUSAL_INVALID_NOISE: {exc}", Fraction(0, 1), Fraction(0, 1)
            )
        except Exception as exc:
            return self._emit_rejection(
                proposal, f"REFUSAL_INVALID_NOISE: {exc}", Fraction(0, 1), Fraction(0, 1)
            )

        tol = Fraction(proposal.tolerance_epsilon)
        evaluated = call_native(
            "majorana_noise",
            {
                "operation": "evaluate",
                "noise": _matrix_wire(noise),
                "matrix": _matrix_wire(mat),
                "tolerance_epsilon": str(tol),
            },
        )
        max_leakage = decode_rational(evaluated["max_noise_leakage"])
        defect = decode_rational(evaluated["circuit_noise_defect"])
        is_stable = evaluated["is_accepted"]
        status = evaluated["status_reason"]

        receipt_pre = MultiQubitNoisyBraidReceipt(
            receipt_id=f"RECEIPT-{proposal.round_id}-{hashlib.sha256(proposal.round_id.encode('utf-8')).hexdigest()[:8]}",
            round_id=proposal.round_id,
            proposer_id=proposal.proposer_id,
            is_accepted=is_stable,
            status_reason=status,
            num_qubits=proposal.num_qubits,
            num_modes=num_modes,
            gate_count=len(proposal.operations),
            is_so_dim=is_so,
            determinant=det,
            max_noise_leakage=max_leakage,
            circuit_noise_defect=defect,
            tolerance_epsilon=tol,
            sha256_hash="",
            authority_effect="None",
        )

        return MultiQubitNoisyBraidReceipt(
            receipt_id=receipt_pre.receipt_id,
            round_id=receipt_pre.round_id,
            proposer_id=receipt_pre.proposer_id,
            is_accepted=receipt_pre.is_accepted,
            status_reason=receipt_pre.status_reason,
            num_qubits=receipt_pre.num_qubits,
            num_modes=receipt_pre.num_modes,
            gate_count=receipt_pre.gate_count,
            is_so_dim=receipt_pre.is_so_dim,
            determinant=receipt_pre.determinant,
            max_noise_leakage=receipt_pre.max_noise_leakage,
            circuit_noise_defect=receipt_pre.circuit_noise_defect,
            tolerance_epsilon=receipt_pre.tolerance_epsilon,
            sha256_hash=receipt_pre.canonical_digest(),
            authority_effect="None",
        )

    def _emit_rejection(
        self,
        proposal: MultiQubitNoisyBraidProposalPacket,
        reason: str,
        leakage: Fraction,
        defect: Fraction,
    ) -> MultiQubitNoisyBraidReceipt:
        receipt_pre = MultiQubitNoisyBraidReceipt(
            receipt_id=f"RECEIPT-{proposal.round_id}-REJECT",
            round_id=proposal.round_id,
            proposer_id=proposal.proposer_id,
            is_accepted=False,
            status_reason=reason,
            num_qubits=proposal.num_qubits,
            num_modes=4 * proposal.num_qubits if proposal.num_qubits >= 1 else 0,
            gate_count=len(proposal.operations),
            is_so_dim=False,
            determinant=Fraction(0, 1),
            max_noise_leakage=leakage,
            circuit_noise_defect=defect,
            tolerance_epsilon=Fraction(proposal.tolerance_epsilon),
            sha256_hash="",
            authority_effect="None",
        )
        return MultiQubitNoisyBraidReceipt(
            receipt_id=receipt_pre.receipt_id,
            round_id=receipt_pre.round_id,
            proposer_id=receipt_pre.proposer_id,
            is_accepted=receipt_pre.is_accepted,
            status_reason=receipt_pre.status_reason,
            num_qubits=receipt_pre.num_qubits,
            num_modes=receipt_pre.num_modes,
            gate_count=receipt_pre.gate_count,
            is_so_dim=receipt_pre.is_so_dim,
            determinant=receipt_pre.determinant,
            max_noise_leakage=receipt_pre.max_noise_leakage,
            circuit_noise_defect=receipt_pre.circuit_noise_defect,
            tolerance_epsilon=receipt_pre.tolerance_epsilon,
            sha256_hash=receipt_pre.canonical_digest(),
            authority_effect="None",
        )
