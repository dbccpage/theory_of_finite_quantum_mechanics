"""Process / Choi matrices, generalized Born rule, causal mixtures, quantum switch.

Faithful port of ``crates/omega_engine.crates.engine/src/quantum/process_matrix_engine.rs``.

This is the structural / higher-order-process layer that the square reusable
``omega_linear_algebra.channel.QuantumChannel`` does not cover. Density-matrix
checks (Hermitian / PSD) are done here via the same complex->real-block trick
the Rust crate uses.
"""

from __future__ import annotations
import math
from typing import List

CONTRACT_ID = "urn:omega:qm:process_matrix_engine:file:v1.1.0"
AUTHORITY_EFFECT = "None"

import numpy as np

from omega_engine.crates.type.qm_engine import CausalMixture, CausalOrder, LabIoDim

DEFAULT_TOLERANCE = 1e-9
EPSILON_QUANTUM_EIGEN = 1e-9


class ProcessMatrixError(Exception):
    pass


class EmptyLabs(ProcessMatrixError):
    pass


class EmptyKrausSet(ProcessMatrixError):
    pass


class NonSquareMatrix(ProcessMatrixError):
    pass


class DimensionMismatch(ProcessMatrixError):
    pass


class NonHermitian(ProcessMatrixError):
    pass


class NotPositive(ProcessMatrixError):
    pass


class NonTracePreserving(ProcessMatrixError):
    pass


class InvalidProbability(ProcessMatrixError):
    pass


class InvalidMixtureWeights(ProcessMatrixError):
    pass


class InvalidState(ProcessMatrixError):
    pass


class InvalidUnitary(ProcessMatrixError):
    pass




def _ensure_square(m: np.ndarray) -> None:
    if m.ndim != 2 or m.shape[0] != m.shape[1]:
        raise NonSquareMatrix(f"matrix must be square, got {m.shape}")


def _identity(dim: int) -> np.ndarray:
    return np.eye(dim, dtype=complex)


def _max_entry_norm(m: np.ndarray) -> float:
    if m.size == 0:
        return 0.0
    return float(np.max(np.abs(m)))


def _complex_to_real_block(m: np.ndarray) -> np.ndarray:
    n = m.shape[0]
    block = np.zeros((2 * n, 2 * n), dtype=float)
    block[0:n, 0:n] = m.real
    block[0:n, n : 2 * n] = -m.imag
    block[n : 2 * n, 0:n] = m.imag
    block[n : 2 * n, n : 2 * n] = m.real
    return block


def _min_hermitian_eigenvalue(m: np.ndarray) -> float:
    block = _complex_to_real_block(m)
    block = 0.5 * (block + block.T)
    eigs = np.linalg.eigvalsh(block)
    return float(np.min(eigs))


def _ensure_hermitian_positive(m: np.ndarray, tolerance: float) -> None:
    hermitian_error = _max_entry_norm(m - m.conj().T)
    if hermitian_error > tolerance:
        raise NonHermitian(f"operator is not Hermitian, max error {hermitian_error}")
    min_ev = _min_hermitian_eigenvalue(m)
    if min_ev < -tolerance:
        raise NotPositive(
            f"operator is not positive semidefinite, min eigenvalue {min_ev}"
        )


def _ensure_unitary(m: np.ndarray) -> None:
    _ensure_square(m)
    defect = float(np.linalg.norm(m.conj().T @ m - _identity(m.shape[0])))
    if defect > DEFAULT_TOLERANCE:
        raise InvalidUnitary(f"unitary check failed, max error {defect}")


def _vectorize_kraus(k: np.ndarray, dim_in: int, dim_out: int) -> np.ndarray:
    """Column-stacking vec: v[input*dim_out + output] = k[output, input]."""
    v = np.zeros(dim_in * dim_out, dtype=complex)
    for inp in range(dim_in):
        for out in range(dim_out):
            v[inp * dim_out + out] = k[out, inp]
    return v


def _unvectorize_kraus(v: np.ndarray, dim_in: int, dim_out: int) -> np.ndarray:
    m = np.zeros((dim_out, dim_in), dtype=complex)
    idx = 0
    for j in range(dim_in):
        for i in range(dim_out):
            m[i, j] = v[idx]
            idx += 1
    return m


def _partial_trace_output(choi: np.ndarray, dim_in: int, dim_out: int) -> np.ndarray:
    out = np.zeros((dim_in, dim_in), dtype=complex)
    for i in range(dim_in):
        for j in range(dim_in):
            s = 0.0 + 0.0j
            for o in range(dim_out):
                s += choi[i * dim_out + o, j * dim_out + o]
            out[i, j] = s
    return out


def _partial_trace_input(m: np.ndarray, dim_in: int, dim_out: int) -> np.ndarray:
    out = np.zeros((dim_out, dim_out), dtype=complex)
    for i in range(dim_out):
        for j in range(dim_out):
            for k in range(dim_in):
                out[i, j] += m[i * dim_in + k, j * dim_in + k]
    return out


def _tensor_all(mats: List[np.ndarray]) -> np.ndarray:
    acc = mats[0]
    for m in mats[1:]:
        acc = np.kron(acc, m)
    return acc


def _norm_sqr(psi: np.ndarray) -> float:
    return float(np.sum(np.abs(psi) ** 2))


def _normalize_state(psi: np.ndarray) -> np.ndarray:
    norm = math.sqrt(_norm_sqr(psi))
    if norm <= EPSILON_QUANTUM_EIGEN or not math.isfinite(norm):
        raise InvalidState("state norm is zero or non-finite")
    return psi / norm




from omega_engine.crates.engine.base.eng_base import Engine


class ChoiMatrix(Engine):
    def __init__(self, choi: np.ndarray, dim_in: int, dim_out: int, tolerance: float):
        self.choi = choi
        self.dim_in = dim_in
        self.dim_out = dim_out
        self.tolerance = tolerance

    @classmethod
    def from_kraus(
        cls,
        dim_in: int,
        dim_out: int,
        kraus_ops: List[np.ndarray],
        tolerance: float = DEFAULT_TOLERANCE,
    ) -> "ChoiMatrix":
        if not kraus_ops:
            raise EmptyKrausSet("Choi operator requires at least one Kraus operator")
        d = dim_in * dim_out
        choi = np.zeros((d, d), dtype=complex)
        for k in kraus_ops:
            k = np.asarray(k, dtype=complex)
            if k.shape[0] != dim_out or k.shape[1] != dim_in:
                raise DimensionMismatch(
                    f"dimension mismatch: expected {dim_in * dim_out}, "
                    f"got {k.shape[0] * k.shape[1]}"
                )
            v = _vectorize_kraus(k, dim_in, dim_out)
            choi += np.outer(v, v.conj())
        return cls.from_matrix(dim_in, dim_out, choi, tolerance)

    @classmethod
    def from_matrix(
        cls,
        dim_in: int,
        dim_out: int,
        choi: np.ndarray,
        tolerance: float = DEFAULT_TOLERANCE,
    ) -> "ChoiMatrix":
        choi = np.asarray(choi, dtype=complex)
        _ensure_square(choi)
        expected = dim_in * dim_out
        if choi.shape[0] != expected:
            raise DimensionMismatch(
                f"dimension mismatch: expected {expected}, got {choi.shape[0]}"
            )
        tolerance = max(tolerance, EPSILON_QUANTUM_EIGEN)
        _ensure_hermitian_positive(choi, tolerance)
        return cls(choi, dim_in, dim_out, tolerance)

    @classmethod
    def unitary(cls, unitary: np.ndarray) -> "ChoiMatrix":
        unitary = np.asarray(unitary, dtype=complex)
        _ensure_square(unitary)
        dim = unitary.shape[0]
        defect = _max_entry_norm(unitary.conj().T @ unitary - _identity(dim))
        if defect > DEFAULT_TOLERANCE:
            raise InvalidUnitary(f"unitary check failed, max error {defect}")
        return cls.from_kraus(dim, dim, [unitary])

    def lab_dim(self) -> LabIoDim:
        return LabIoDim(self.dim_in, self.dim_out)

    def trace_preserving_defect(self) -> float:
        traced = _partial_trace_output(self.choi, self.dim_in, self.dim_out)
        return _max_entry_norm(traced - _identity(self.dim_in))

    def is_trace_preserving(self) -> bool:
        return self.trace_preserving_defect() <= self.tolerance




class ProcessMatrix(Engine):
    def __init__(
        self,
        choi: np.ndarray,
        labs: List[LabIoDim],
        tolerance: float = DEFAULT_TOLERANCE,
    ):
        choi = np.asarray(choi, dtype=complex)
        if not labs:
            raise EmptyLabs("process matrix must include at least one lab")
        _ensure_square(choi)
        expected = 1
        for lab in labs:
            expected *= lab.total_dim()
        if choi.shape[0] != expected:
            raise DimensionMismatch(
                f"dimension mismatch: expected {expected}, got {choi.shape[0]}"
            )
        tolerance = max(tolerance, EPSILON_QUANTUM_EIGEN)
        _ensure_hermitian_positive(choi, tolerance)
        self.choi = choi
        self.labs = labs
        self.tolerance = tolerance

    @classmethod
    def new(cls, choi: np.ndarray, labs: List[LabIoDim]) -> "ProcessMatrix":
        return cls(choi, labs)

    @classmethod
    def normalized_positive(
        cls, choi: np.ndarray, labs: List[LabIoDim]
    ) -> "ProcessMatrix":
        choi = np.asarray(choi, dtype=complex)
        trace = float(np.trace(choi).real)
        if trace <= EPSILON_QUANTUM_EIGEN or not math.isfinite(trace):
            raise InvalidProbability(f"Born rule produced invalid probability {trace}")
        return cls(choi / trace, labs)

    def generalized_born_probability(self, local_ops: List[ChoiMatrix]) -> float:
        if len(local_ops) != len(self.labs):
            raise DimensionMismatch(
                f"dimension mismatch: expected {len(self.labs)}, got {len(local_ops)}"
            )
        for expected, op in zip(self.labs, local_ops):
            if expected != op.lab_dim():
                raise DimensionMismatch(
                    f"dimension mismatch: expected {expected.total_dim()}, got {op.lab_dim().total_dim()}"
                )
        effect = _tensor_all([op.choi for op in local_ops])
        value = np.trace(effect @ self.choi)
        if abs(value.imag) > self.tolerance:
            raise InvalidProbability(
                f"Born rule produced invalid probability {value.real}"
            )
        if value.real < -self.tolerance or value.real > 1.0 + self.tolerance:
            raise InvalidProbability(
                f"Born rule produced invalid probability {value.real}"
            )
        return 0.0 if value.real < 0.0 else float(value.real)

    def witness_value(self, witness: np.ndarray) -> float:
        witness = np.asarray(witness, dtype=complex)
        _ensure_square(witness)
        if witness.shape[0] != self.choi.shape[0]:
            raise DimensionMismatch(
                f"dimension mismatch: expected {self.choi.shape[0]}, got {witness.shape[0]}"
            )
        return float(np.trace(witness @ self.choi).real)

    def violates_witness_constraint(self, witness: np.ndarray) -> bool:
        return self.witness_value(witness) < -self.tolerance




class QuantumSwitch(Engine):
    @staticmethod
    def apply(
        target: np.ndarray, control: np.ndarray, u_a: np.ndarray, u_b: np.ndarray
    ) -> np.ndarray:
        target = np.asarray(target, dtype=complex)
        control = np.asarray(control, dtype=complex)
        u_a = np.asarray(u_a, dtype=complex)
        u_b = np.asarray(u_b, dtype=complex)
        _ensure_square(u_a)
        _ensure_square(u_b)
        if u_a.shape[0] != u_b.shape[0]:
            raise DimensionMismatch(
                f"dimension mismatch: expected {u_a.shape[0]}, got {u_b.shape[0]}"
            )
        target_dim = u_a.shape[0]
        if target.shape[0] != target_dim:
            raise DimensionMismatch(
                f"dimension mismatch: expected {target_dim}, got {target.shape[0]}"
            )
        if control.shape[0] != 2:
            raise DimensionMismatch(
                f"dimension mismatch: expected 2, got {control.shape[0]}"
            )
        _ensure_unitary(u_a)
        _ensure_unitary(u_b)

        target = _normalize_state(target)
        control = _normalize_state(control)
        branch_ab = u_b @ (u_a @ target)
        branch_ba = u_a @ (u_b @ target)

        out = np.zeros(2 * target_dim, dtype=complex)
        for i in range(target_dim):
            out[i] = control[0] * branch_ab[i]
            out[target_dim + i] = control[1] * branch_ba[i]
        return _normalize_state(out)

    @staticmethod
    def reduced_control_density(
        switch_state: np.ndarray, target_dim: int
    ) -> np.ndarray:
        switch_state = np.asarray(switch_state, dtype=complex)
        if switch_state.shape[0] != 2 * target_dim:
            raise DimensionMismatch(
                f"dimension mismatch: expected {2 * target_dim}, got {switch_state.shape[0]}"
            )
        rho = np.zeros((2, 2), dtype=complex)
        for c1 in range(2):
            for c2 in range(2):
                s = 0.0 + 0.0j
                for t in range(target_dim):
                    s += (
                        switch_state[c1 * target_dim + t]
                        * switch_state[c2 * target_dim + t].conjugate()
                    )
                rho[c1, c2] = s
        return rho

    @staticmethod
    def order_coherence(switch_state: np.ndarray, target_dim: int) -> float:
        rho_c = QuantumSwitch.reduced_control_density(switch_state, target_dim)
        return float(abs(rho_c[0, 1]))




class CPTPChoi(Engine):
    def __init__(self, raw: ChoiMatrix):
        tol = raw.tolerance
        if raw.trace_preserving_defect() > tol:
            raise NonTracePreserving(
                f"instrument is not trace-preserving, max error {raw.trace_preserving_defect()}"
            )
        min_ev = _min_hermitian_eigenvalue(raw.choi)
        if min_ev < -tol:
            raise NotPositive(
                f"operator is not positive semidefinite, min eigenvalue {min_ev}"
            )
        self.inner = raw

    @classmethod
    def new(cls, raw: ChoiMatrix) -> "CPTPChoi":
        return cls(raw)




def apply_via_choi(
    choi: np.ndarray, rho: np.ndarray, dim_in: int, dim_out: int
) -> np.ndarray:
    choi = np.asarray(choi, dtype=complex)
    rho = np.asarray(rho, dtype=complex)
    rho_t = rho.T
    id_out = _identity(dim_out)
    kron = np.kron(id_out, rho_t)
    tmp = choi @ kron
    return _partial_trace_input(tmp, dim_in, dim_out)


def choi_from_kraus(kraus: List[np.ndarray], dim_in: int, dim_out: int) -> np.ndarray:
    d = dim_in * dim_out
    choi = np.zeros((d, d), dtype=complex)
    for k in kraus:
        v = _vectorize_kraus(np.asarray(k, dtype=complex), dim_in, dim_out)
        choi += np.outer(v, v.conj())
    return choi


def kraus_from_choi(
    choi: np.ndarray, dim_in: int, dim_out: int, tol: float
) -> List[np.ndarray]:
    choi = np.asarray(choi, dtype=complex)
    herm = 0.5 * (choi + choi.conj().T)
    eigvals, eigvecs = np.linalg.eigh(herm)
    kraus_ops = []
    for i, lam in enumerate(eigvals):
        if lam > tol:
            v = eigvecs[:, i]
            k = _unvectorize_kraus(v, dim_in, dim_out)
            k = k * math.sqrt(lam)
            kraus_ops.append(k)
    return kraus_ops




