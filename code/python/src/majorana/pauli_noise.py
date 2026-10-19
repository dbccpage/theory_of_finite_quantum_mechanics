"""Exact local Majorana Hamiltonian noise and deterministic rational sampling.

AuthorityEffect: None.
"""

from __future__ import annotations

from dataclasses import dataclass
from fractions import Fraction
import json
from typing import Any, Dict, List, Sequence, Tuple

from .braid_action import MajoranaBraidAction
from .multiqubit_braid import MultiQubitOperation, compile_multi_qubit_braid

MAX_NOISE_MODES: int = 1_024
_U32_MASK: int = 0xFFFF_FFFF


class NoiseError(Exception):
    pass


def _fraction_to_str(val: Fraction) -> str:
    return f"{val.numerator}" if val.denominator == 1 else f"{val.numerator}/{val.denominator}"


def _str_to_fraction(text: str) -> Fraction:
    return Fraction(text)


@dataclass
class SkewNoiseMatrix:
    dim: int
    data: List[List[Fraction]]

    def __post_init__(self) -> None:
        if self.dim < 2 or self.dim > MAX_NOISE_MODES:
            raise NoiseError(f"dim {self.dim} outside 2..={MAX_NOISE_MODES}")
        if len(self.data) != self.dim or any(len(r) != self.dim for r in self.data):
            raise NoiseError("Invalid shape for noise matrix")
        for i in range(self.dim):
            if self.data[i][i] != 0:
                raise NoiseError(f"Nonzero diagonal at mode {i + 1}")
            for j in range(self.dim):
                if self.data[i][j] != -self.data[j][i]:
                    raise NoiseError(f"Matrix not skew-symmetric at ({i + 1}, {j + 1})")

    @classmethod
    def zeros(cls, dim: int) -> "SkewNoiseMatrix":
        return cls(dim, [[Fraction(0) for _ in range(dim)] for _ in range(dim)])

    def conjugate_by_braid(self, action: MajoranaBraidAction) -> "SkewNoiseMatrix":
        """K'_{ij} = s_i s_j K_{pi(i), pi(j)}."""
        if action.mode_count() != self.dim:
            raise NoiseError(f"braid has {action.mode_count()} modes, noise has {self.dim}")
        out = [[Fraction(0) for _ in range(self.dim)] for _ in range(self.dim)]
        for i in range(self.dim):
            img_i = action.image(i + 1)
            pi_i = img_i.mode - 1
            s_i = img_i.sign
            for j in range(self.dim):
                img_j = action.image(j + 1)
                pi_j = img_j.mode - 1
                s_j = img_j.sign
                out[i][j] = self.data[pi_i][pi_j] * s_i * s_j
        return SkewNoiseMatrix(self.dim, out)

    def frobenius_norm_sq(self) -> Fraction:
        return sum((x * x for row in self.data for x in row), Fraction(0))

    def max_abs_entry(self) -> Fraction:
        return max((abs(x) for row in self.data for x in row), default=Fraction(0))


@dataclass
class LocalMajoranaNoise:
    data: List[List[Fraction]]

    @classmethod
    def from_rows(cls, data: Sequence[Sequence[Fraction]]) -> "LocalMajoranaNoise":
        dim = len(data)
        if dim < 2 or dim > MAX_NOISE_MODES:
            raise NoiseError(f"dim must be integer >= 2 and <= {MAX_NOISE_MODES}")
        if any(len(row) != dim for row in data):
            raise NoiseError(f"noise matrix must have shape {dim} by {dim}")
        rows = [[Fraction(val) for val in row] for row in data]
        for r in range(dim):
            if rows[r][r] != 0:
                raise NoiseError(f"Diagonal entry at mode {r + 1} must be 0 for skew-symmetric matrix")
            for c in range(r + 1, dim):
                if rows[r][c] != -rows[c][r]:
                    raise NoiseError(f"Matrix must be skew-symmetric at ({r + 1}, {c + 1})")
        return cls(rows)

    @classmethod
    def zero(cls, dim: int) -> "LocalMajoranaNoise":
        if dim < 2 or dim > MAX_NOISE_MODES:
            raise NoiseError(f"dim must be integer >= 2 and <= {MAX_NOISE_MODES}")
        return cls([[Fraction(0) for _ in range(dim)] for _ in range(dim)])

    @classmethod
    def single_pair(
        cls, dim: int, a: int, b: int, epsilon: Fraction
    ) -> "LocalMajoranaNoise":
        return cls.stray_couplings(dim, [(a, b, epsilon)])

    @classmethod
    def stray_couplings(
        cls, dim: int, couplings: Sequence[Tuple[int, int, Fraction]]
    ) -> "LocalMajoranaNoise":
        noise = cls.zero(dim)
        for a, b, eps in couplings:
            noise._check_mode(a)
            noise._check_mode(b)
            if a == b:
                raise NoiseError(f"Self-coupling at mode {a} is invalid")
            val = Fraction(eps)
            noise.data[a - 1][b - 1] += val
            noise.data[b - 1][a - 1] -= val
        return noise

    def dim(self) -> int:
        return len(self.data)

    def rows(self) -> List[List[Fraction]]:
        return self.data

    def _check_mode(self, mode: int) -> None:
        if mode < 1 or mode > self.dim():
            raise NoiseError(f"mode={mode} out of range [1, {self.dim()}]")

    def leakage_on_mode(self, mode: int) -> Fraction:
        self._check_mode(mode)
        return sum((Fraction(2) * abs(val) for val in self.data[mode - 1]), Fraction(0))

    def max_leakage(self) -> Fraction:
        return max(
            (
                sum((Fraction(2) * abs(val) for val in row), Fraction(0))
                for row in self.data
            ),
            default=Fraction(0),
        )

    def _check_action(self, action: MajoranaBraidAction) -> None:
        if action.mode_count() != self.dim():
            raise NoiseError(f"braid has {action.mode_count()} modes, noise has {self.dim()}")

    def transform(self, action: MajoranaBraidAction) -> "LocalMajoranaNoise":
        self._check_action(action)
        d = self.dim()
        transformed = LocalMajoranaNoise.zero(d)
        images = action.images()
        for r, img_r in enumerate(images):
            for c, img_c in enumerate(images):
                val = self.data[img_r.mode - 1][img_c.mode - 1]
                transformed.data[r][c] = val if img_r.sign == img_c.sign else -val
        return transformed

    def commutation_defect(self, action: MajoranaBraidAction) -> Fraction:
        self._check_action(action)
        defect = Fraction(0)
        images = action.images()
        for r, img_r in enumerate(images):
            for c in range(r + 1, len(images)):
                img_c = images[c]
                source = self.data[img_r.mode - 1][img_c.mode - 1]
                diff = (
                    abs(source - self.data[r][c])
                    if img_r.sign == img_c.sign
                    else abs(-source - self.data[r][c])
                )
                if diff > defect:
                    defect = diff
        return defect


def correlated_cluster_couplings(
    num_qubits: int,
    lattice_side: int,
    budget: Fraction,
    seed: int,
) -> List[Tuple[int, int, Fraction]]:
    dim = num_qubits * 4
    if num_qubits <= 0 or dim > MAX_NOISE_MODES:
        raise NoiseError(
            f"qubit count must be positive and four times it must be <= {MAX_NOISE_MODES}"
        )
    budget_q = Fraction(budget)
    if budget_q < 0:
        raise NoiseError("noise scale and tolerance must be nonnegative")

    side = max(lattice_side, 2)
    side_length = Fraction(side - 1)
    y_denom = Fraction(max((num_qubits - 1) // 2, 1))

    def coordinate(mode: int) -> Tuple[Fraction, Fraction]:
        qubit = (mode - 1) // 4
        offset = (mode - 1) % 4
        x = Fraction(qubit % 2) * side_length + Fraction(offset % 2, 4)
        y = Fraction(qubit // 2) * side_length / y_denom + Fraction(offset // 2, 4)
        return x, y

    couplings: List[Tuple[int, int, Fraction]] = []
    seed_mod = seed % 7
    for a in range(1, dim):
        xa, ya = coordinate(a)
        for b in range(a + 1, dim + 1):
            xb, yb = coordinate(b)
            distance = abs(xa - xb) + abs(ya - yb)
            modulation = (seed_mod * (a % 7) * (b % 7)) % 7 + 1
            value = budget_q * Fraction(modulation, 7) / (Fraction(1) + distance)
            couplings.append((a, b, value))
    return couplings


class DeterministicRationalNoiseGenerator:
    def __init__(self, seed: int) -> None:
        self._state: int = int(seed) & _U32_MASK

    def state(self) -> int:
        return self._state

    def _next_uint(self) -> int:
        self._state = (self._state * 1_664_525 + 1_013_904_223) & _U32_MASK
        return self._state

    def next_int_in_range(self, minimum: int, maximum: int) -> int:
        if minimum > maximum:
            raise NoiseError("integer sampling range is empty")
        span = maximum - minimum + 1
        return minimum + (self._next_uint() % span)

    def next_fraction(self, max_denominator: int, scale_bound: Fraction) -> Fraction:
        if max_denominator <= 0:
            raise NoiseError("maximum denominator must be at least one")
        bound = Fraction(scale_bound)
        if bound < 0:
            raise NoiseError("noise scale and tolerance must be nonnegative")
        if bound == 0:
            return Fraction(0)

        denominator = 1 + (self._next_uint() % max_denominator)
        prod = Fraction(denominator) * bound
        maximum_numerator = prod.numerator // prod.denominator
        if maximum_numerator == 0:
            inv = Fraction(1) / bound
            denominator = (inv.numerator // inv.denominator) + 1
            numerator = 1
        else:
            draw = self._next_uint()
            numerator = (draw % maximum_numerator) + 1
        value = Fraction(numerator, denominator)
        if self._next_uint() % 2 == 0:
            value = -value
        return value

    def generate_skew_symmetric_matrix(
        self,
        dim: int,
        scale_bound: Fraction,
        density: Fraction,
        max_denominator: int,
    ) -> LocalMajoranaNoise:
        bound = Fraction(scale_bound)
        dens = Fraction(density)
        if dens < 0 or dens > 1:
            raise NoiseError("density must be in [0, 1]")
        if bound < 0:
            raise NoiseError("noise scale and tolerance must be nonnegative")
        if max_denominator <= 0:
            raise NoiseError("maximum denominator must be at least one")
        scaled = dens * 1000
        threshold = scaled.numerator // scaled.denominator
        noise = LocalMajoranaNoise.zero(dim)
        for row in range(dim):
            for col in range(row + 1, dim):
                roll = 1 + (self._next_uint() % 1000)
                if roll <= threshold:
                    value = self.next_fraction(max_denominator, bound)
                    noise.data[col][row] = -value
                    noise.data[row][col] = value
        return noise


@dataclass(frozen=True)
class NoiseEvaluation:
    max_noise_leakage: Fraction
    circuit_noise_defect: Fraction
    tolerance_epsilon: Fraction
    is_accepted: bool

    def status_reason(self) -> str:
        return "ACCEPTED_STABLE" if self.is_accepted else "REFUSAL_NOISE_LEAKAGE"

    def to_dict(self) -> Dict[str, Any]:
        return {
            "max_noise_leakage": _fraction_to_str(self.max_noise_leakage),
            "circuit_noise_defect": _fraction_to_str(self.circuit_noise_defect),
            "tolerance_epsilon": _fraction_to_str(self.tolerance_epsilon),
            "is_accepted": self.is_accepted,
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "NoiseEvaluation":
        return cls(
            max_noise_leakage=_str_to_fraction(str(data["max_noise_leakage"])),
            circuit_noise_defect=_str_to_fraction(str(data["circuit_noise_defect"])),
            tolerance_epsilon=_str_to_fraction(str(data["tolerance_epsilon"])),
            is_accepted=bool(data["is_accepted"]),
        )


def evaluate_noise(
    noise: LocalMajoranaNoise,
    action: MajoranaBraidAction,
    tolerance: Fraction,
) -> NoiseEvaluation:
    tol = Fraction(tolerance)
    if tol < 0:
        raise NoiseError("noise scale and tolerance must be nonnegative")
    defect = noise.commutation_defect(action)
    return NoiseEvaluation(
        max_noise_leakage=noise.max_leakage(),
        circuit_noise_defect=defect,
        tolerance_epsilon=tol,
        is_accepted=(defect <= tol),
    )


@dataclass(frozen=True)
class PauliNoiseScalingRow:
    num_qubits: int
    mode_count: int
    lattice_side: int
    seed: int
    coupling_count: int
    budget: Fraction
    first_coupling: Fraction
    last_coupling: Fraction
    mode1_leakage: Fraction
    max_noise_leakage: Fraction
    circuit_noise_defect: Fraction
    tight_tolerance: Fraction
    tight_accepted: bool
    tight_status: str
    boundary_tolerance: Fraction
    boundary_accepted: bool
    boundary_status: str
    leakage_preserved: bool
    inverse_restores_noise: bool
    lcg_final_state: int
    lcg_max_leakage: Fraction
    lcg_commutation_defect: Fraction

    def to_dict(self) -> Dict[str, Any]:
        return {
            "num_qubits": self.num_qubits,
            "mode_count": self.mode_count,
            "lattice_side": self.lattice_side,
            "seed": self.seed,
            "coupling_count": self.coupling_count,
            "budget": _fraction_to_str(self.budget),
            "first_coupling": _fraction_to_str(self.first_coupling),
            "last_coupling": _fraction_to_str(self.last_coupling),
            "mode1_leakage": _fraction_to_str(self.mode1_leakage),
            "max_noise_leakage": _fraction_to_str(self.max_noise_leakage),
            "circuit_noise_defect": _fraction_to_str(self.circuit_noise_defect),
            "tight_tolerance": _fraction_to_str(self.tight_tolerance),
            "tight_accepted": self.tight_accepted,
            "tight_status": self.tight_status,
            "boundary_tolerance": _fraction_to_str(self.boundary_tolerance),
            "boundary_accepted": self.boundary_accepted,
            "boundary_status": self.boundary_status,
            "leakage_preserved": self.leakage_preserved,
            "inverse_restores_noise": self.inverse_restores_noise,
            "lcg_final_state": self.lcg_final_state,
            "lcg_max_leakage": _fraction_to_str(self.lcg_max_leakage),
            "lcg_commutation_defect": _fraction_to_str(self.lcg_commutation_defect),
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "PauliNoiseScalingRow":
        return cls(
            num_qubits=int(data["num_qubits"]),
            mode_count=int(data["mode_count"]),
            lattice_side=int(data["lattice_side"]),
            seed=int(data["seed"]),
            coupling_count=int(data["coupling_count"]),
            budget=_str_to_fraction(str(data["budget"])),
            first_coupling=_str_to_fraction(str(data["first_coupling"])),
            last_coupling=_str_to_fraction(str(data["last_coupling"])),
            mode1_leakage=_str_to_fraction(str(data["mode1_leakage"])),
            max_noise_leakage=_str_to_fraction(str(data["max_noise_leakage"])),
            circuit_noise_defect=_str_to_fraction(str(data["circuit_noise_defect"])),
            tight_tolerance=_str_to_fraction(str(data["tight_tolerance"])),
            tight_accepted=bool(data["tight_accepted"]),
            tight_status=str(data["tight_status"]),
            boundary_tolerance=_str_to_fraction(str(data["boundary_tolerance"])),
            boundary_accepted=bool(data["boundary_accepted"]),
            boundary_status=str(data["boundary_status"]),
            leakage_preserved=bool(data["leakage_preserved"]),
            inverse_restores_noise=bool(data["inverse_restores_noise"]),
            lcg_final_state=int(data["lcg_final_state"]),
            lcg_max_leakage=_str_to_fraction(str(data["lcg_max_leakage"])),
            lcg_commutation_defect=_str_to_fraction(str(data["lcg_commutation_defect"])),
        )


def benchmark_pauli_noise_scaling(
    qubit_counts: Sequence[int],
) -> List[PauliNoiseScalingRow]:
    """Finite scaling benchmark for exact rational correlated Pauli noise and deterministic
    LCG noise evaluation under multi-qubit Majorana braiding across declared qubit_counts.
    Matches Rust tfqm_majorana::benchmark_pauli_noise_scaling bit-for-bit.
    """
    if not qubit_counts:
        raise NoiseError("qubit_counts must be non-empty")
    rows: List[PauliNoiseScalingRow] = []
    for nq in qubit_counts:
        if nq < 2:
            raise NoiseError("benchmark_pauli_noise_scaling requires num_qubits >= 2")
        mode_count = 4 * nq
        lattice_side = max(nq, 2)
        seed = nq + 1
        budget = Fraction(1, 10)
        couplings = correlated_cluster_couplings(nq, lattice_side, budget, seed)
        coupling_count = len(couplings)
        first_coupling = couplings[0][2] if couplings else Fraction(0)
        last_coupling = couplings[-1][2] if couplings else Fraction(0)
        cluster_noise = LocalMajoranaNoise.stray_couplings(mode_count, couplings)

        ops = [
            MultiQubitOperation.Phase(qubit=1),
            MultiQubitOperation.Hadamard(qubit=nq),
            MultiQubitOperation.Swap(first=1, second=2),
            MultiQubitOperation.Cnot(control=1, target=nq),
        ]
        compiled = compile_multi_qubit_braid(nq, ops)

        mode1_leakage = cluster_noise.leakage_on_mode(1)
        tight_tolerance = Fraction(1, 100)
        eval_tight = evaluate_noise(cluster_noise, compiled.action, tight_tolerance)
        boundary_tolerance = eval_tight.circuit_noise_defect
        eval_boundary = evaluate_noise(cluster_noise, compiled.action, boundary_tolerance)

        transformed = cluster_noise.transform(compiled.action)
        leakage_preserved = transformed.max_leakage() == cluster_noise.max_leakage()
        restored = transformed.transform(compiled.action.inverse())
        inverse_restores_noise = restored == cluster_noise

        lcg = DeterministicRationalNoiseGenerator(100 + nq)
        lcg_noise = lcg.generate_skew_symmetric_matrix(
            mode_count, Fraction(1, 20), Fraction(1, 2), 50
        )
        lcg_final_state = lcg.state()
        lcg_max_leakage = lcg_noise.max_leakage()
        lcg_commutation_defect = lcg_noise.commutation_defect(compiled.action)

        rows.append(
            PauliNoiseScalingRow(
                num_qubits=nq,
                mode_count=mode_count,
                lattice_side=lattice_side,
                seed=seed,
                coupling_count=coupling_count,
                budget=budget,
                first_coupling=first_coupling,
                last_coupling=last_coupling,
                mode1_leakage=mode1_leakage,
                max_noise_leakage=eval_tight.max_noise_leakage,
                circuit_noise_defect=eval_tight.circuit_noise_defect,
                tight_tolerance=tight_tolerance,
                tight_accepted=eval_tight.is_accepted,
                tight_status=eval_tight.status_reason(),
                boundary_tolerance=boundary_tolerance,
                boundary_accepted=eval_boundary.is_accepted,
                boundary_status=eval_boundary.status_reason(),
                leakage_preserved=leakage_preserved,
                inverse_restores_noise=inverse_restores_noise,
                lcg_final_state=lcg_final_state,
                lcg_max_leakage=lcg_max_leakage,
                lcg_commutation_defect=lcg_commutation_defect,
            )
        )
    return rows


def pauli_noise_scaling_to_canonical_json(rows: Sequence[PauliNoiseScalingRow]) -> str:
    """Serialize PauliNoiseScalingRow list to canonical 2-space pretty JSON with LF line endings."""
    return json.dumps([row.to_dict() for row in rows], indent=2)


def pauli_noise_scaling_from_canonical_json(json_str: str) -> List[PauliNoiseScalingRow]:
    """Deserialize PauliNoiseScalingRow list from canonical JSON string."""
    raw = json.loads(json_str)
    return [PauliNoiseScalingRow.from_dict(item) for item in raw]
