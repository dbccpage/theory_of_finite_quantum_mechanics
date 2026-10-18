"""Quantum channels (CPTP maps) as reusable, composable operators.

Pure-Python port of the Kraus/CPTP and Choi machinery from the Rust
``omega_engine.crates.engine::quantum`` modules. A :class:`QuantumChannel` is a completely
positive, trace-preserving map represented by Kraus operators
``{K_i}`` with ``sum_i K_i^dag K_i = I``. Channels apply to a
:class:`NumericalDensityMatrix` and compose (``self . other``), so a sequence
of QM reviews is itself an operator that composes.

References
----------
Rust: ``crates/omega_engine.crates.engine/src/quantum/{quantum_channel,process_matrix_engine}.rs``
"""

from __future__ import annotations
from dataclasses import dataclass
from typing import List

import numpy as np

from .density import DensityMatrixConfig, DensityMatrixCandidate, NumericalDensityMatrix


@dataclass
class QuantumChannel:
    """A CPTP map defined by square Kraus operators of a fixed dimension."""

    dim: int
    kraus: List[np.ndarray]
    label: str = "channel"

    def __post_init__(self) -> None:
        if self.dim <= 0:
            raise ValueError("channel dimension must be positive")
        if not self.kraus:
            raise ValueError("channel needs at least one Kraus operator")
        self.kraus = [np.asarray(k, dtype=complex) for k in self.kraus]
        for k in self.kraus:
            if k.shape != (self.dim, self.dim):
                raise ValueError(f"Kraus op shape {k.shape} != ({self.dim},{self.dim})")

    def completeness_defect(self) -> float:
        """||sum_i K_i^dag K_i - I||_F. Zero for a trace-preserving channel."""
        acc = np.zeros((self.dim, self.dim), dtype=complex)
        for k in self.kraus:
            acc += k.conj().T @ k
        return float(np.linalg.norm(acc - np.eye(self.dim)))

    def is_cptp(self, tol: float = 1e-9) -> bool:
        return self.completeness_defect() <= tol

    def apply(
        self, rho: NumericalDensityMatrix, config: DensityMatrixConfig | None = None
    ) -> NumericalDensityMatrix:
        """Apply the channel: rho -> sum_i K_i rho K_i^dag (validated)."""
        cfg = config or DensityMatrixConfig.default()
        return rho.apply_kraus(self.kraus, cfg)

    def apply_raw(self, rho: np.ndarray) -> np.ndarray:
        out = np.zeros((self.dim, self.dim), dtype=complex)
        for k in self.kraus:
            out += k @ rho @ k.conj().T
        return out

    def compose(self, other: "QuantumChannel") -> "QuantumChannel":
        """Return the channel ``self . other`` (apply ``other`` first)."""
        if self.dim != other.dim:
            raise ValueError("cannot compose channels of different dimension")
        composed = [k2 @ k1 for k2 in self.kraus for k1 in other.kraus]
        return QuantumChannel(
            self.dim, composed, label=f"({self.label} o {other.label})"
        )

    def choi(self) -> np.ndarray:
        """Choi matrix J = sum_i vec(K_i) vec(K_i)^dag, shape (dim^2, dim^2).

        Hermitian and positive semidefinite by construction (CP witness).
        """
        d = self.dim
        j = np.zeros((d * d, d * d), dtype=complex)
        for k in self.kraus:
            v = k.reshape(-1, order="F")  
            j += np.outer(v, v.conj())
        return j

    @classmethod
    def identity(cls, dim: int) -> "QuantumChannel":
        return cls(dim, [np.eye(dim, dtype=complex)], label="identity")

    @classmethod
    def dephasing(cls, dim: int, p: float) -> "QuantumChannel":
        """Diagonal (phase-damping) channel with dephasing probability ``p``.

        Keeps populations, attenuates coherences by ``1 - p``. Models loss of
        off-diagonal structure when reviewing a noisy prompt/response.
        """
        if not 0.0 <= p <= 1.0:
            raise ValueError("dephasing probability must be in [0, 1]")
        return DephasingChannel(dim, p)

    @classmethod
    def depolarizing(cls, dim: int, p: float) -> "QuantumChannel":
        """Depolarizing channel: rho -> (1-p) rho + p I/dim."""
        if not 0.0 <= p <= 1.0:
            raise ValueError("depolarizing probability must be in [0, 1]")
        return DepolarizingChannel(dim, p)

    @classmethod
    def from_unitary(cls, u: np.ndarray) -> "QuantumChannel":
        u = np.asarray(u, dtype=complex)
        return cls(u.shape[0], [u], label="unitary")


class DephasingChannel(QuantumChannel):
    """Optimized dephasing channel avoiding expensive matrix multiplication for large dimensions."""

    def __init__(self, dim: int, p: float):
        self.p = p
        k0 = np.sqrt(1.0 - p) * np.eye(dim, dtype=complex)
        kraus = [k0]
        for i in range(dim):
            proj = np.zeros((dim, dim), dtype=complex)
            proj[i, i] = np.sqrt(p)
            kraus.append(proj)
        super().__init__(dim, kraus, label=f"dephasing(p={p})")

    def apply(
        self, rho: NumericalDensityMatrix, config: DensityMatrixConfig | None = None
    ) -> NumericalDensityMatrix:
        cfg = config or DensityMatrixConfig.default()
        cfg.validate()
        rho_arr = rho.rho()
        new_rho = (1.0 - self.p) * rho_arr + self.p * np.diag(np.diag(rho_arr))
        return DensityMatrixCandidate.from_rho(new_rho).validate(cfg)


class DepolarizingChannel(QuantumChannel):
    """Optimized depolarizing channel avoiding O(dim^2) Kraus operators and matrix multiplication."""

    def __init__(self, dim: int, p: float):
        self.p = p
        kraus = []
        if dim <= 8:
            kraus.append(np.sqrt(1.0 - p) * np.eye(dim, dtype=complex))
            scale = np.sqrt(p / (dim * dim))
            for i in range(dim):
                for j in range(dim):
                    e = np.zeros((dim, dim), dtype=complex)
                    e[i, j] = 1.0
                    kraus.append(scale * np.sqrt(float(dim)) * e)
        else:
            kraus = [np.eye(dim, dtype=complex)]
        super().__init__(dim, kraus, label=f"depolarizing(p={p})")

    def apply(
        self, rho: NumericalDensityMatrix, config: DensityMatrixConfig | None = None
    ) -> NumericalDensityMatrix:
        cfg = config or DensityMatrixConfig.default()
        cfg.validate()
        rho_arr = rho.rho()
        new_rho = (1.0 - self.p) * rho_arr + (self.p / self.dim) * np.eye(
            self.dim, dtype=complex
        )
        return DensityMatrixCandidate.from_rho(new_rho).validate(cfg)


def density_from_rho(
    rho: np.ndarray, config: DensityMatrixConfig | None = None
) -> NumericalDensityMatrix:
    """Validate an arbitrary rho into a :class:`NumericalDensityMatrix`."""
    cfg = config or DensityMatrixConfig.default()
    return DensityMatrixCandidate.from_rho(np.asarray(rho, dtype=complex)).validate(cfg)




