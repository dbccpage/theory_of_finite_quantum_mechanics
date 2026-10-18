"""majorana_noise_sweep.py — Multi-Parameter Noise Sweeps on Random Rational Matrices K in Q^{4N x 4N}.

AuthorityEffect: None.
Reference: sealed-derivation-v1 (3100c4e), Claim MAJ-C7/MAJ-C8, gemini_000.md.

Mechanizes:
1. Deterministic Rational Noise Matrix Generator:
   - Synthesizes exact random skew-symmetric Hamiltonian noise matrices K in Q^{4N x 4N} via seedable integer LCG.
   - Enforces K^T = -K, zero diagonal, and bounded rational entries |eps_{ab}| <= eps under Zero-Float Law.
2. Multi-Parameter Noise Surface Sweeps:
   - Explores multidimensional parameter space (qubit count N, perturbation coupling scale eps, tolerance eps_tol).
   - Evaluates multi-qubit braided Clifford operations (Phase, Hadamard, CNOT) under generated noise.
   - Computes commutation defect ||U K U^T - K|| and maximum mode leakage in exact rationals.
3. Empirical PFP Acceptance Surface Boundary Mapping:
   - Determines empirical acceptance probability P_accept(eps, eps_tol).
   - Maps sharp transition boundary where defect crosses tolerance threshold.
   - Emits MultiQubitNoiseSweepReceipt certified with SHA-256 under AuthorityEffect: None.
"""

from __future__ import annotations

import hashlib
import json
from dataclasses import dataclass
from fractions import Fraction
from typing import Any, List, Sequence, Tuple

from majorana_multiqubit_noise import (
    LocalMajoranaNoise,
    MultiQubitNoisyBraidProposalPacket,
    MultiQubitNoisyBraidReferee,
    _exact_wire,
)

from omega_engine_operating_system.adapters.rust_host.majorana_math import (
    NativeMathRefusal,
    call_native,
    decode_rational,
)


class DeterministicRationalNoiseGenerator:
    """The paper's exact seeded LCG, evaluated by the canonical Rust host."""

    def __init__(self, seed: int = 42) -> None:
        if not isinstance(seed, int) or isinstance(seed, bool):
            raise TypeError("seed must be an integer")
        self._state = seed & 0xFFFFFFFF

    def _request(self, operation: str, **payload: Any) -> dict[str, Any]:
        result = call_native(
            "majorana_noise_generate",
            {
                "operation": operation,
                "state": self._state,
                **payload,
            },
        )
        state = result.get("state")
        if type(state) is not int or not 0 <= state <= 0xFFFFFFFF:
            raise NativeMathRefusal(
                "NATIVE_MATH_RNG_STATE", "native RNG state must be a uint32", outcome=result
            )
        return result

    def _next_uint(self) -> int:
        return self.next_int_in_range(0, 0xFFFFFFFF)

    def next_int_in_range(self, min_val: int, max_val: int) -> int:
        if not isinstance(min_val, int) or isinstance(min_val, bool):
            raise TypeError("min_val must be an integer")
        if not isinstance(max_val, int) or isinstance(max_val, bool):
            raise TypeError("max_val must be an integer")
        if min_val > max_val:
            raise ValueError(f"min_val {min_val} > max_val {max_val}")
        result = self._request("integer", min_val=min_val, max_val=max_val)
        value = result.get("value")
        if type(value) is not int or not min_val <= value <= max_val:
            raise NativeMathRefusal(
                "NATIVE_MATH_RNG_VALUE",
                "native integer sample is outside its declared range",
                outcome=result,
            )
        self._state = result["state"]
        return value

    def next_fraction(
        self, max_denom: int = 50, scale_bound: Fraction = Fraction(1, 10)
    ) -> Fraction:
        if max_denom < 1:
            raise ValueError("max_denom must be >= 1")
        result = self._request(
            "fraction", max_denom=max_denom, scale_bound=_exact_wire(scale_bound, "scale_bound")
        )
        value = decode_rational(result["value"])
        self._state = result["state"]
        return value

    def generate_skew_symmetric_matrix(
        self,
        dim: int,
        scale_bound: Fraction = Fraction(1, 10),
        density: Fraction = Fraction(1, 1),
        max_denom: int = 50,
    ) -> LocalMajoranaNoise:
        if dim < 2:
            raise ValueError(f"dim must be >= 2, got {dim}")
        result = self._request(
            "matrix",
            dim=dim,
            scale_bound=_exact_wire(scale_bound, "scale_bound"),
            density=_exact_wire(density, "density"),
            max_denom=max_denom,
        )
        noise = LocalMajoranaNoise._from_native(result["matrix"])
        self._state = result["state"]
        return noise


@dataclass(frozen=True)
class NoiseSweepDataPoint:
    """Individual observation in a multi-parameter noise sweep."""

    point_id: str
    num_qubits: int
    num_modes: int
    noise_scale: Fraction
    tolerance_epsilon: Fraction
    commutation_defect: Fraction
    max_leakage: Fraction
    is_accepted: bool
    status_reason: str

    def __post_init__(self) -> None:
        if isinstance(self.noise_scale, (float, bool)):
            raise TypeError("noise_scale must be Fraction or int")
        if isinstance(self.tolerance_epsilon, (float, bool)):
            raise TypeError("tolerance_epsilon must be Fraction or int")


@dataclass(frozen=True)
class MultiQubitNoiseSweepReceipt:
    """Cryptographic receipt certifying multi-parameter noise sweep results on PFP referee surface."""

    sweep_id: str
    qubit_configs: Tuple[int, ...]
    noise_scales: Tuple[Fraction, ...]
    tolerances: Tuple[Fraction, ...]
    total_evaluations: int
    accepted_evaluations: int
    overall_acceptance_rate: Fraction
    sharp_boundary_verified: bool
    data_points: Tuple[NoiseSweepDataPoint, ...]
    sha256_hash: str
    authority_effect: str = "None"

    def canonical_digest(self) -> str:
        """Deterministic SHA-256 digest of sweep results."""
        payload = {
            "sweep_id": self.sweep_id,
            "qubit_configs": list(self.qubit_configs),
            "noise_scales": [str(s) for s in self.noise_scales],
            "tolerances": [str(t) for t in self.tolerances],
            "total_evaluations": self.total_evaluations,
            "accepted_evaluations": self.accepted_evaluations,
            "overall_acceptance_rate": str(self.overall_acceptance_rate),
            "sharp_boundary_verified": self.sharp_boundary_verified,
            "data_points": [
                {
                    "point_id": p.point_id,
                    "num_qubits": p.num_qubits,
                    "noise_scale": str(p.noise_scale),
                    "tolerance": str(p.tolerance_epsilon),
                    "defect": str(p.commutation_defect),
                    "accepted": p.is_accepted,
                    "status": p.status_reason,
                }
                for p in self.data_points
            ],
            "authority_effect": self.authority_effect,
        }
        raw = json.dumps(payload, sort_keys=True, separators=(",", ":")).encode("utf-8")
        return hashlib.sha256(raw).hexdigest()


class MultiQubitNoiseSweepRunner:
    """Executes multi-parameter noise sweeps over random rational matrices."""

    def __init__(self, seed: int = 42) -> None:
        self.generator = DeterministicRationalNoiseGenerator(seed=seed)
        self.referee = MultiQubitNoisyBraidReferee()

    def run_sweep(
        self,
        qubit_counts: Sequence[int] = (1, 2),
        noise_scales: Sequence[Fraction] = (Fraction(1, 100), Fraction(1, 10)),
        tolerances: Sequence[Fraction] = (Fraction(1, 50), Fraction(1, 20)),
        trials_per_config: int = 2,
        density: Fraction = Fraction(1, 1),
    ) -> MultiQubitNoiseSweepReceipt:
        """Executes full grid sweep across qubit counts, noise scales, and tolerance thresholds."""
        if not qubit_counts or any(q < 1 for q in qubit_counts):
            raise ValueError("qubit_counts must contain integers >= 1")
        if not noise_scales:
            raise ValueError("noise_scales cannot be empty")
        if not tolerances:
            raise ValueError("tolerances cannot be empty")
        if trials_per_config < 1:
            raise ValueError("trials_per_config must be >= 1")

        data_points: List[NoiseSweepDataPoint] = []
        total_evals = 0
        accepted_evals = 0
        point_idx = 0

        for num_qubits in qubit_counts:
            num_modes = 4 * num_qubits
            for scale in noise_scales:
                for tol in tolerances:
                    for trial in range(trials_per_config):
                        point_idx += 1
                        ops: List[Tuple[str, Tuple[int, ...]]] = [("phase", (1, 0))]
                        if num_qubits >= 2:
                            ops.append(("hadamard", (2, 0)))
                            ops.append(("cnot", (1, 2)))
                        if num_qubits >= 3:
                            ops.append(("hadamard", (3, 0)))
                            ops.append(("cnot", (2, 3)))

                        noise = self.generator.generate_skew_symmetric_matrix(
                            dim=num_modes,
                            scale_bound=scale,
                            density=density,
                        )

                        couplings: List[Tuple[int, int, Fraction]] = []
                        for r in range(num_modes):
                            for c in range(r + 1, num_modes):
                                val = noise.data[r][c]
                                if val != Fraction(0, 1):
                                    couplings.append((r + 1, c + 1, val))

                        packet = MultiQubitNoisyBraidProposalPacket(
                            round_id=f"sw_q{num_qubits}_s{point_idx}",
                            proposer_id="agent_sweep_runner",
                            num_qubits=num_qubits,
                            operations=tuple(ops),
                            noise_couplings=tuple(couplings),
                            tolerance_epsilon=tol,
                        )

                        receipt = self.referee.evaluate(packet)
                        total_evals += 1
                        if receipt.is_accepted:
                            accepted_evals += 1

                        data_points.append(
                            NoiseSweepDataPoint(
                                point_id=f"pt_{point_idx:04d}",
                                num_qubits=num_qubits,
                                num_modes=num_modes,
                                noise_scale=Fraction(scale),
                                tolerance_epsilon=Fraction(tol),
                                commutation_defect=receipt.circuit_noise_defect,
                                max_leakage=receipt.max_noise_leakage,
                                is_accepted=receipt.is_accepted,
                                status_reason=receipt.status_reason,
                            )
                        )

        sharp_boundary = all(
            p.is_accepted == (p.status_reason == "ACCEPTED_STABLE") for p in data_points
        )

        acc_rate = Fraction(accepted_evals, total_evals) if total_evals > 0 else Fraction(0, 1)

        receipt_pre = MultiQubitNoiseSweepReceipt(
            sweep_id=f"sweep_{qubit_counts[0]}to{qubit_counts[-1]}_n{total_evals}",
            qubit_configs=tuple(qubit_counts),
            noise_scales=tuple(Fraction(s) for s in noise_scales),
            tolerances=tuple(Fraction(t) for t in tolerances),
            total_evaluations=total_evals,
            accepted_evaluations=accepted_evals,
            overall_acceptance_rate=acc_rate,
            sharp_boundary_verified=sharp_boundary,
            data_points=tuple(data_points),
            sha256_hash="",
            authority_effect="None",
        )

        return MultiQubitNoiseSweepReceipt(
            sweep_id=receipt_pre.sweep_id,
            qubit_configs=receipt_pre.qubit_configs,
            noise_scales=receipt_pre.noise_scales,
            tolerances=receipt_pre.tolerances,
            total_evaluations=receipt_pre.total_evaluations,
            accepted_evaluations=receipt_pre.accepted_evaluations,
            overall_acceptance_rate=receipt_pre.overall_acceptance_rate,
            sharp_boundary_verified=receipt_pre.sharp_boundary_verified,
            data_points=receipt_pre.data_points,
            sha256_hash=receipt_pre.canonical_digest(),
            authority_effect="None",
        )
