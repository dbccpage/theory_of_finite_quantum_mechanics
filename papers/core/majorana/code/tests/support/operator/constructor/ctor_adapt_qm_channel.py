"""CPTP quantum channels (Kraus form).

Faithful port of ``crates/omega_engine.crates.engine/src/quantum/quantum_channel.rs``.

The Rust ``QuantumChannel`` admits rectangular Kraus operators
``K_i : H_source -> H_target`` (so source/target dims may differ). The reusable
square-only :class:`omega_linear_algebra.channel.QuantumChannel` is re-exported
here under its own name for callers that want the standard-channel constructors
(dephasing/depolarizing/from_unitary/choi).
"""

from __future__ import annotations
from typing import List

import numpy as np

from omega_engine.crates.linear_algebra_theory.density import (
    DensityMatrixConfig,
    DensityMatrixCandidate,
    NumericalDensityMatrix,
    NoValidStates,
    InvalidKrausShape,
    NonTracePreservingChannel,
)
from omega_engine.crates.type.qm_density import StateSpace


class OmegaQuantumChannel:
    """Rectangular Kraus channel: K_i maps source space -> target space."""

    def __init__(self, source: StateSpace, target: StateSpace, kraus: List[np.ndarray]):
        self.source = source
        self.target = target
        self.kraus = [np.asarray(k, dtype=complex) for k in kraus]

    def validate(self) -> None:
        if not self.kraus:
            raise NoValidStates("channel needs at least one Kraus operator")

        dim = self.source.dim
        acc = np.zeros((dim, dim), dtype=complex)
        for k in self.kraus:
            if k.shape[0] != self.target.dim or k.shape[1] != dim:
                raise InvalidKrausShape(
                    f"invalid kraus shape: expected {dim}, actual {k.shape[0]}"
                )
            acc += k.conj().T @ k

        defect = float(np.linalg.norm(acc - np.eye(dim)))
        if defect > 1e-6:
            raise NonTracePreservingChannel(
                f"channel is not trace preserving; defect={defect}"
            )


class CPTPChannel:
    def __init__(self, inner: OmegaQuantumChannel):
        inner.validate()
        self.inner = inner

    @classmethod
    def new(cls, ch: OmegaQuantumChannel) -> "CPTPChannel":
        return cls(ch)

    def apply(self, rho: NumericalDensityMatrix) -> NumericalDensityMatrix:
        dim_out = self.inner.target.dim
        out = np.zeros((dim_out, dim_out), dtype=complex)
        for k in self.inner.kraus:
            out += k @ rho.rho() @ k.conj().T
        cfg = DensityMatrixConfig.default()
        return DensityMatrixCandidate.from_rho(out).validate(cfg)

    def compose(self, other: "CPTPChannel") -> "CPTPChannel":
        assert self.inner.source == other.inner.target
        composed = []
        for k2 in self.inner.kraus:
            for k1 in other.inner.kraus:
                composed.append(k2 @ k1)
        return CPTPChannel(
            OmegaQuantumChannel(
                source=other.inner.source,
                target=self.inner.target,
                kraus=composed,
            )
        )
