from __future__ import annotations
r"""
Finite transport: path sums, Chapman--Kolmogorov, and the unitary / stochastic shadows.

AuthorityEffect: None.

Canonical Implementation: omega_engine.crates.homology_theory.finite_transport
"""


from typing import Any, Dict, List, Optional, Sequence

import numpy as np

from omega_engine.crates.quantum_physics.primitives import dagger


def is_column_stochastic(m: np.ndarray, atol: float = 1e-9) -> bool:
    r"""Nonnegative entries and every column summing to 1."""
    a = np.asarray(m, dtype=float)
    return bool(np.all(a >= -atol) and np.allclose(a.sum(axis=0), 1.0, atol=atol))


def is_unitary(u: np.ndarray, atol: float = 1e-9) -> bool:
    r""":math:`U^\dagger U = I`."""
    return bool(np.allclose(dagger(u) @ u, np.eye(u.shape[0]), atol=atol))


def is_hermitian(h: np.ndarray, atol: float = 1e-9) -> bool:
    r""":math:`H = H^\dagger`."""
    return bool(np.allclose(h, dagger(h), atol=atol))


def path_sum(m: np.ndarray, steps: int) -> np.ndarray:
    r""":math:`M^{n}` --- the length-``steps`` path sum on the carrier."""
    if steps < 0:
        raise ValueError("path_sum: steps must be nonnegative")
    return np.linalg.matrix_power(np.asarray(m), steps)


def chapman_kolmogorov(m: np.ndarray, p: int, q: int) -> Dict[str, Any]:
    r"""Check :math:`M^{p+q} = M^p M^q` on a concrete carrier."""
    lhs = path_sum(m, p + q)
    rhs = path_sum(m, p) @ path_sum(m, q)
    return {
        "p": p,
        "q": q,
        "max_abs_deviation": float(np.max(np.abs(lhs - rhs))),
        "holds": bool(np.allclose(lhs, rhs, atol=1e-9)),
        "authority_effect": "None",
    }


def unitary_from_hamiltonian(h: np.ndarray, t: float) -> np.ndarray:
    r""":math:`U(t) = e^{-iHt}`."""
    from scipy.linalg import expm

    return expm(-1j * np.asarray(h, dtype=complex) * t)


def heisenberg_evolve(a_op: np.ndarray, h: np.ndarray, t: float) -> np.ndarray:
    r""":math:`A(t) = U^\dagger A U` --- the Heisenberg picture (qm_041)."""
    u = unitary_from_hamiltonian(h, t)
    return dagger(u) @ np.asarray(a_op, dtype=complex) @ u


def pictures_agree(
    rho: np.ndarray, a_op: np.ndarray, h: np.ndarray, t: float
) -> Dict[str, Any]:
    r"""Schrödinger and Heisenberg give the same expectation (qm_040/qm_041)."""
    u = unitary_from_hamiltonian(h, t)
    schroedinger = complex(np.trace(a_op @ (u @ rho @ dagger(u))))
    heisenberg = complex(np.trace(heisenberg_evolve(a_op, h, t) @ rho))
    return {
        "schroedinger_expectation": float(np.real(schroedinger)),
        "heisenberg_expectation": float(np.real(heisenberg)),
        "agree": bool(np.isclose(schroedinger, heisenberg, atol=1e-10)),
        "authority_effect": "None",
    }


def norm_preservation_separation(dim: int = 3, t: float = 0.7) -> Dict[str, Any]:
    r"""Unitary transport preserves :math:`\ell^2`; stochastic transport preserves :math:`\ell^1`."""
    rng_h = np.zeros((dim, dim), dtype=complex)
    for i in range(dim):
        for j in range(dim):
            rng_h[i, j] = np.cos(1.0 + i * 0.7 + j * 1.3) + 1j * np.sin(0.3 + i * 1.1 - j * 0.5)
    h = (rng_h + dagger(rng_h)) / 2.0
    u = unitary_from_hamiltonian(h, t)

    s = np.abs(u) ** 2
    s = s / s.sum(axis=0, keepdims=True)

    v = np.zeros(dim, dtype=complex)
    v[0] = 1.0
    p = np.zeros(dim, dtype=float)
    p[0] = 1.0

    uv = u @ v
    sp = s @ p

    return {
        "unitary_check": is_unitary(u),
        "stochastic_check": is_column_stochastic(s),
        "unitary_preserves_l2": bool(
            np.isclose(np.linalg.norm(uv, 2), np.linalg.norm(v, 2), atol=1e-10)
        ),
        "unitary_preserves_l1": bool(
            np.isclose(np.sum(np.abs(uv)), np.sum(np.abs(v)), atol=1e-10)
        ),
        "stochastic_preserves_l1": bool(np.isclose(np.sum(sp), np.sum(p), atol=1e-10)),
        "stochastic_preserves_l2": bool(
            np.isclose(np.linalg.norm(sp, 2), np.linalg.norm(p, 2), atol=1e-10)
        ),
        "verdict": "the two transports have different invariants; neither implies the other",
        "import_slot": "OB-UNITARY (declared, not derived)",
        "authority_effect": "None",
    }


def decoherence_functional(
    histories: Sequence[Sequence[int]], m: np.ndarray, rho0: np.ndarray
) -> Dict[str, Any]:
    r"""A finite Gell-Mann--Hartle style decoherence functional (qm_043)."""
    ops = []
    for hist in histories:
        c = np.eye(m.shape[0], dtype=complex)
        for idx in hist:
            proj = np.zeros_like(c)
            proj[idx, idx] = 1.0
            c = proj @ np.asarray(m, dtype=complex) @ c
        ops.append(c)

    d = np.zeros((len(ops), len(ops)), dtype=complex)
    for i, ci in enumerate(ops):
        for j, cj in enumerate(ops):
            d[i, j] = np.trace(ci @ rho0 @ dagger(cj))

    off = float(np.max(np.abs(d - np.diag(np.diag(d))))) if len(ops) > 1 else 0.0
    return {
        "decoherence_matrix": d,
        "max_offdiagonal": off,
        "is_consistent_set": bool(off < 1e-9),
        "diagonal_probabilities": np.real(np.diag(d)),
        "authority_effect": "None",
    }


__all__ = [
    "is_column_stochastic",
    "is_unitary",
    "is_hermitian",
    "path_sum",
    "chapman_kolmogorov",
    "unitary_from_hamiltonian",
    "heisenberg_evolve",
    "pictures_agree",
    "norm_preservation_separation",
    "decoherence_functional",
]



