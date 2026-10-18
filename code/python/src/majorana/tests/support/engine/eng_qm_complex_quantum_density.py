"""Complex quantum density engine supporting complex unitary transformations.

Faithful port of ``crates/omega_engine.crates.engine/src/quantum/complex_quantum_density_engine.rs``.
"""

from __future__ import annotations
import math
from typing import Callable, Optional

import numpy as np

CONTRACT_ID = "urn:omega:qm:complex_quantum_density_engine:file:v1.0.0"
AUTHORITY_EFFECT = "None"

from omega_engine.crates.linear_algebra_theory.density import (
    DensityMatrixConfig,
    DimensionMismatch,
    NonHermitian,
    NonPhysical,
    NonUnitary,
    NotPositiveSemidefinite,
    NumericalDensityMatrix,
    TraceNotOne,
)

EPSILON_QUANTUM_EIGEN = 1e-9


def complex_to_real_block(matrix: np.ndarray) -> np.ndarray:
    n = matrix.shape[0]
    block = np.zeros((2 * n, 2 * n), dtype=float)
    for i in range(n):
        for j in range(n):
            z = matrix[i, j]
            block[i, j] = z.real
            block[i, j + n] = -z.imag
            block[i + n, j] = z.imag
            block[i + n, j + n] = z.real
    return block


from omega_engine.crates.engine.base.eng_base import Engine


class ComplexQuantumDensityEngine(Engine):
    @staticmethod
    def complex_state_from_embedding(
        embedding: list[float],
        phase_fn: Optional[Callable[[int, float], float]] = None,
    ) -> np.ndarray:
        if not embedding or any(not math.isfinite(x) for x in embedding):
            raise NonPhysical("Embedding contains invalid entries")

        max_val = max(embedding)
        exps = [math.exp(x - max_val) for x in embedding]
        sum_exp = sum(exps)
        if sum_exp < EPSILON_QUANTUM_EIGEN or not math.isfinite(sum_exp):
            raise NonPhysical("Softmax sum is too small or non-finite")

        psi = np.zeros(len(embedding), dtype=complex)
        for i, x in enumerate(embedding):
            p = exps[i] / sum_exp
            phase = phase_fn(i, x) if phase_fn is not None else 0.0
            if not math.isfinite(phase):
                raise NonPhysical("Phase is non-finite")
            psi[i] = math.sqrt(p) * (math.cos(phase) + 1j * math.sin(phase))

        cfg = DensityMatrixConfig.default()
        norm2 = sum(c.real * c.real + c.imag * c.imag for c in psi)
        if abs(norm2 - 1.0) > cfg.trace_tol():
            raise TraceNotOne(f"norm2={norm2}, tol={cfg.trace_tol()}")

        return psi

    @staticmethod
    def apply_complex_unitary(
        dm: NumericalDensityMatrix,
        u: np.ndarray,
    ) -> NumericalDensityMatrix:
        dim = dm.dim()
        if u.shape != (dim, dim):
            raise DimensionMismatch(
                f"u shape {u.shape} does not match density matrix dimension {dim}"
            )

        cfg = DensityMatrixConfig.default()
        check = u.conj().T @ u
        identity = np.eye(dim)

        max_diff = float(np.max(np.abs(check - identity)))
        frob_diff = float(np.linalg.norm(check - identity))

        if max_diff > cfg.unitary_tol() or frob_diff > cfg.unitary_tol():
            raise NonUnitary(f"non-unitary operator; defect={frob_diff}")

        new_rho = u @ dm.rho() @ u.conj().T
        result = NumericalDensityMatrix.from_validated(
            new_rho.shape[0], new_rho.flatten().tolist(), cfg
        )

        trace = complex(np.trace(result.rho()))
        eigs = np.linalg.eigvalsh(complex_to_real_block(result.rho()))
        min_ev = float(np.min(eigs))

        if not np.all(np.isfinite(result.rho())):
            raise NonPhysical("non-physical density matrix")

        adjoint = result.rho().conj().T
        diff = result.rho() - adjoint
        max_hermitian_defect = max(abs(trace.imag), float(np.max(np.abs(diff))))
        if max_hermitian_defect > cfg.hermitian_tol():
            raise NonHermitian(f"non-hermitian matrix; defect={max_hermitian_defect}")

        if abs(trace.real - 1.0) > cfg.trace_tol():
            raise TraceNotOne(f"trace={trace.real}, tol={cfg.trace_tol()}")

        if min_ev < -cfg.psd_tol():
            raise NotPositiveSemidefinite(
                f"min_eigenvalue={min_ev}, tol={cfg.psd_tol()}"
            )

        return result

    @staticmethod
    def validate_complex_density_matrix(
        dm: NumericalDensityMatrix,
    ) -> NumericalDensityMatrix:
        cfg = DensityMatrixConfig.default()
        trace = complex(np.trace(dm.rho()))
        eigs = np.linalg.eigvalsh(complex_to_real_block(dm.rho()))
        min_ev = float(np.min(eigs))

        if not np.all(np.isfinite(dm.rho())):
            raise NonPhysical("non-physical density matrix")

        adjoint = dm.rho().conj().T
        diff = dm.rho() - adjoint
        max_hermitian_defect = max(abs(trace.imag), float(np.max(np.abs(diff))))
        if max_hermitian_defect > cfg.hermitian_tol():
            raise NonHermitian(f"non-hermitian matrix; defect={max_hermitian_defect}")

        if abs(trace.real - 1.0) > cfg.trace_tol():
            raise TraceNotOne(f"trace={trace.real}, tol={cfg.trace_tol()}")

        if min_ev < -cfg.psd_tol():
            raise NotPositiveSemidefinite(
                f"min_eigenvalue={min_ev}, tol={cfg.psd_tol()}"
            )

        return dm

    @staticmethod
    def purity_complex(dm: NumericalDensityMatrix) -> float:
        cfg = DensityMatrixConfig.default()
        prod = dm.rho() @ dm.rho()
        tr = complex(np.trace(prod))
        if abs(tr.imag) > cfg.hermitian_tol():
            raise NonHermitian(f"non-hermitian product; defect={abs(tr.imag)}")
        return tr.real

    @staticmethod
    def von_neumann_entropy_complex(
        dm: NumericalDensityMatrix,
    ) -> float:
        cfg = DensityMatrixConfig.default()
        eigs = np.linalg.eigvalsh(dm.rho())
        entropy = 0.0

        for lam in eigs:
            if lam < -cfg.psd_tol():
                raise NotPositiveSemidefinite(
                    f"min_eigenvalue={lam}, tol={cfg.psd_tol()}"
                )
            elif lam > 0.0:
                entropy += -float(lam) * math.log(float(lam))
        return float(entropy)

    @staticmethod
    def diagonal_overlap_fidelity(
        a: NumericalDensityMatrix,
        b: NumericalDensityMatrix,
    ) -> float:
        if a.dim() != b.dim():
            raise DimensionMismatch(
                f"Dimension mismatch: expected {a.dim()}, actual {b.dim()}"
            )
        cfg = DensityMatrixConfig.default()
        sum_sqrt = 0.0

        for i in range(a.dim()):
            ai = a.rho()[i, i].real
            bi = b.rho()[i, i].real

            if ai < -cfg.psd_tol() or bi < -cfg.psd_tol():
                raise NotPositiveSemidefinite(f"min_eigenvalue={min(ai, bi)}")

            if ai > 0.0 and bi > 0.0:
                sum_sqrt += math.sqrt(ai * bi)

        overlap = sum_sqrt * sum_sqrt
        if overlap < -cfg.trace_tol() or overlap > 1.0 + cfg.trace_tol():
            raise NonPhysical("invalid overlap fidelity value")

        return overlap

    @staticmethod
    def full_fidelity_complex_unimplemented(
        a: NumericalDensityMatrix,
        b: NumericalDensityMatrix,
    ) -> float:
        if a.dim() != b.dim():
            raise DimensionMismatch(
                f"Dimension mismatch: expected {a.dim()}, actual {b.dim()}"
            )
        raise NonPhysical("full complex fidelity is unimplemented")



