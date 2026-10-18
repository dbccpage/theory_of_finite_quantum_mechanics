r"""
Degree-k L1 solvers.

The historical NumPy/SciPy functions in this module are numerical replay APIs.
The ``*_exact`` functions are a separate rational rail: they require an
explicit modelling declaration and return a replayable primal/dual receipt.

AuthorityEffect: None.

Canonical Implementation: omega_engine.crates.functional.degree_k_phi
"""

from __future__ import annotations

from collections.abc import Mapping, Sequence
from dataclasses import dataclass
from typing import Any, ClassVar, Dict, Tuple

import numpy as np
from scipy.optimize import linprog
from sympy import Matrix, Rational, simplify
from sympy.matrices.matrixbase import MatrixBase

from omega_engine.crates.functional.higher_simplex_assembly import (
    SimplexComplex,
    assemble_from_network,
    boundary_matrix,
    rational_boundary_matrix,
)
from omega_engine.crates.homology_theory.cochain_presentation import (
    LinearRepairProblem,
    QuotientDistanceCertificate,
)
from omega_engine.crates.linear_algebra_theory.exact import (
    ExactInput,
    exact_column,
    exact_equal,
    exact_matrix,
    exact_matrix_from_matrix,
)


class DegreeKPhiUncertified(Exception):
    """Raised when phi_k fails dual certification."""

    pass


@dataclass
class DegreeKPhiReceipt:
    """Legacy floating-point result for numerical degree-k LP replay."""

    min_l1: float
    dual_val: float
    duality_gap: float
    alpha_opt: np.ndarray
    dual_phi: np.ndarray
    residual: np.ndarray
    primal_solved: bool
    dual_solved: bool
    is_certified: bool
    used_fallback: bool
    weak_duality_violated: bool
    degree: int
    authority_effect: str = "None"


def solve_degree_k_phi(
    d_lower: np.ndarray,
    omega: np.ndarray,
    tol: float = 1e-6,
    degree: int = 1,
) -> DegreeKPhiReceipt:
    """Numerical primal-dual L1 replay on an explicit float matrix."""
    w_vec = np.asarray(omega, dtype=float)
    n_rows = len(w_vec)
    if n_rows == 0:
        return DegreeKPhiReceipt(
            min_l1=0.0,
            dual_val=0.0,
            duality_gap=0.0,
            alpha_opt=np.array([]),
            dual_phi=np.array([]),
            residual=np.array([]),
            primal_solved=True,
            dual_solved=True,
            is_certified=True,
            used_fallback=False,
            weak_duality_violated=False,
            degree=degree,
            authority_effect="None",
        )

    B = np.asarray(d_lower, dtype=float)
    n_cols = B.shape[1] if B.ndim == 2 else 0

    if n_cols > 0:
        c_primal = np.zeros(n_cols + n_rows)
        c_primal[n_cols:] = 1.0

        I_m = np.eye(n_rows)
        A_ub = np.block([[B, -I_m], [-B, -I_m]])
        b_ub = np.concatenate([w_vec, -w_vec])
        bounds_primal = [(None, None)] * n_cols + [(0.0, None)] * n_rows

        res_primal = linprog(c_primal, A_ub=A_ub, b_ub=b_ub, bounds=bounds_primal, method="highs")
        if res_primal.success:
            alpha_opt = res_primal.x[:n_cols]
            primal_solved = True
        else:
            alpha_opt = np.zeros(n_cols)
            primal_solved = False
    else:
        alpha_opt = np.array([])
        primal_solved = True

    residual = w_vec - (B @ alpha_opt if n_cols > 0 else np.zeros_like(w_vec))
    min_l1 = float(np.sum(np.abs(residual)))

    c_dual = -w_vec
    bounds_dual = [(-1.0, 1.0)] * n_rows

    if n_cols > 0:
        A_eq_dual = B.T
        b_eq_dual = np.zeros(n_cols)
        res_dual = linprog(c_dual, A_eq=A_eq_dual, b_eq=b_eq_dual, bounds=bounds_dual, method="highs")
    else:
        phi_sub = np.sign(w_vec)
        phi_sub[phi_sub == 0] = 1.0
        dual_val = float(np.dot(phi_sub, w_vec))
        res_dual = type("DualRes", (), {"success": True, "x": phi_sub, "fun": -dual_val})()

    if res_dual.success:
        dual_phi = np.asarray(res_dual.x, dtype=float)
        dual_val = float(np.dot(dual_phi, w_vec))
        dual_solved = True
    else:
        dual_phi = np.zeros(n_rows)
        dual_val = 0.0
        dual_solved = False

    duality_gap = abs(min_l1 - dual_val)
    weak_duality_violated = dual_val > min_l1 + tol
    used_fallback = not (primal_solved and dual_solved)
    is_certified = (
        primal_solved
        and dual_solved
        and (duality_gap <= tol)
        and (not weak_duality_violated)
        and (not used_fallback)
    )

    return DegreeKPhiReceipt(
        min_l1=min_l1,
        dual_val=dual_val,
        duality_gap=duality_gap,
        alpha_opt=alpha_opt,
        dual_phi=dual_phi,
        residual=residual,
        primal_solved=primal_solved,
        dual_solved=dual_solved,
        is_certified=is_certified,
        used_fallback=used_fallback,
        weak_duality_violated=weak_duality_violated,
        degree=degree,
        authority_effect="None",
    )


def solve_degree_k_joint_primal(
    d_lower: np.ndarray,
    d_k_upper: np.ndarray,
    omega: np.ndarray,
    degree: int = 1,
) -> DegreeKPhiReceipt:
    """Primal-only joint gauge + coexact repair solver."""
    w_vec = np.asarray(omega, dtype=float)
    n_rows = len(w_vec)

    B = np.asarray(d_lower, dtype=float)
    n_pot = B.shape[1] if B.ndim == 2 else 0

    C = np.asarray(d_k_upper, dtype=float)
    n_coex = C.shape[1] if C.ndim == 2 else 0

    n_cols = n_pot + n_coex
    if n_cols == 0 or n_rows == 0:
        return DegreeKPhiReceipt(
            min_l1=float(np.sum(np.abs(w_vec))),
            dual_val=0.0,
            duality_gap=float(np.sum(np.abs(w_vec))),
            alpha_opt=np.array([]),
            dual_phi=np.zeros(n_rows),
            residual=w_vec.copy(),
            primal_solved=True,
            dual_solved=False,
            is_certified=False,
            used_fallback=False,
            weak_duality_violated=False,
            degree=degree,
            authority_effect="None",
        )

    A_joint = np.block([B, C])
    c = np.zeros(n_cols + n_rows)
    c[n_cols:] = 1.0

    I_m = np.eye(n_rows)
    A_ub = np.block([[A_joint, -I_m], [-A_joint, -I_m]])
    b_ub = np.concatenate([w_vec, -w_vec])
    bounds = [(None, None)] * n_cols + [(0.0, None)] * n_rows

    res = linprog(c, A_ub=A_ub, b_ub=b_ub, bounds=bounds, method="highs")
    if res.success:
        alpha_opt = res.x[:n_pot]
        residual = w_vec - A_joint @ res.x[:n_cols]
        min_l1 = float(np.sum(np.abs(residual)))
        primal_solved = True
    else:
        alpha_opt = np.zeros(n_pot)
        residual = w_vec.copy()
        min_l1 = float(np.sum(np.abs(w_vec)))
        primal_solved = False

    return DegreeKPhiReceipt(
        min_l1=min_l1,
        dual_val=0.0,
        duality_gap=min_l1,
        alpha_opt=alpha_opt,
        dual_phi=np.zeros(n_rows),
        residual=residual,
        primal_solved=primal_solved,
        dual_solved=False,
        is_certified=False,
        used_fallback=not primal_solved,
        weak_duality_violated=False,
        degree=degree,
        authority_effect="None",
    )


def phi_k_on_complex(
    complex_obj: SimplexComplex,
    degree: int,
    cochain_values: Dict[Tuple[Any, ...], float],
    tol: float = 1e-6,
) -> DegreeKPhiReceipt:
    """Build a float coboundary matrix and run the numerical LP replay."""
    cells_k = complex_obj.cells.get(degree, [])
    cells_km1 = complex_obj.cells.get(degree - 1, [])
    n_k = len(cells_k)

    if n_k == 0:
        return DegreeKPhiReceipt(
            min_l1=0.0,
            dual_val=0.0,
            duality_gap=0.0,
            alpha_opt=np.array([]),
            dual_phi=np.array([]),
            residual=np.array([]),
            primal_solved=True,
            dual_solved=True,
            is_certified=True,
            used_fallback=False,
            weak_duality_violated=False,
            degree=degree,
            authority_effect="None",
        )

    cell_index_k = {cell: idx for idx, cell in enumerate(cells_k)}
    w_vec = np.zeros(n_k, dtype=float)
    for cell, val in cochain_values.items():
        sorted_cell = tuple(sorted(cell))
        if sorted_cell in cell_index_k:
            w_vec[cell_index_k[sorted_cell]] += val

    if cells_km1:
        d_k_lower = boundary_matrix(cells_k, cells_km1)
        d_lower = d_k_lower.T
    else:
        d_lower = np.zeros((n_k, 0), dtype=float)

    return solve_degree_k_phi(d_lower, w_vec, tol=tol, degree=degree)


def phi_k_on_network(
    network: Any,
    degree: int,
    cochain_values: Dict[Tuple[Any, ...], float],
    tol: float = 1e-6,
) -> DegreeKPhiReceipt:
    """Assemble SimplexComplex from Network and solve primal-dual phi_k."""
    complex_obj = assemble_from_network(network, max_dim=degree + 1)
    return phi_k_on_complex(complex_obj, degree, cochain_values, tol=tol)


def phi_k_estimate(
    network: Any,
    degree: int,
    cochain_values: Dict[Tuple[Any, ...], float],
    tol: float = 1e-6,
) -> DegreeKPhiReceipt:
    """Full receipt estimate — never raises exceptions."""
    return phi_k_on_network(network, degree, cochain_values, tol=tol)


def phi_k(
    network: Any,
    degree: int,
    cochain_values: Dict[Tuple[Any, ...], float],
    tol: float = 1e-6,
) -> float:
    """Fail-closed certified scalar API."""
    receipt = phi_k_on_network(network, degree, cochain_values, tol=tol)
    if not receipt.is_certified:
        raise DegreeKPhiUncertified(
            f"phi_{degree} evaluation failed dual certification: duality_gap={receipt.duality_gap:.6f}, "
            f"primal_solved={receipt.primal_solved}, dual_solved={receipt.dual_solved}"
        )
    return receipt.min_l1


class DegreeKPricingRefused(ValueError):
    """The exact rail refused an absent or invalid modelling capability."""


@dataclass(frozen=True)
class DegreeKPricingDeclaration:
    """Declared scope needed before an exact degree-k computation is meaningful.

    This object does not prove that a supplied carrier has the declared
    semantics.  It makes the modelling assumptions explicit and machine
    checkable at the computational boundary.
    """

    degree: int
    genuine_l1_norm: bool
    index_agnostic_reachability: bool
    reachability_declaration: str
    authority_effect: str = "None"
    norm: str = "l1"

    @classmethod
    def exact_l1(
        cls,
        degree: int,
        reachability_declaration: str = "GS-001_INDEX_AGNOSTIC_REACHABILITY",
    ) -> "DegreeKPricingDeclaration":
        """Construct the standard explicit capability used by FW-8 fixtures."""

        return cls(
            degree=degree,
            genuine_l1_norm=True,
            index_agnostic_reachability=True,
            reachability_declaration=reachability_declaration,
            authority_effect="None",
            norm="l1",
        )

    def validate(self) -> None:
        if not isinstance(self.degree, int) or isinstance(self.degree, bool) or self.degree < 1:
            raise DegreeKPricingRefused("exact degree-k pricing requires degree >= 1")
        if self.genuine_l1_norm is not True or self.norm != "l1":
            raise DegreeKPricingRefused("exact degree-k pricing requires a genuine l1 norm")
        if self.index_agnostic_reachability is not True:
            raise DegreeKPricingRefused(
                "exact degree-k pricing requires declared index-agnostic reachability"
            )
        if (
            not isinstance(self.reachability_declaration, str)
            or not self.reachability_declaration.strip()
        ):
            raise DegreeKPricingRefused("the reachability declaration must be non-empty")
        if self.authority_effect != "None":
            raise DegreeKPricingRefused("AuthorityEffect must be None")


@dataclass(frozen=True)
class ExactDegreeKPhiReceipt:
    """Exact finite rational primal/dual receipt for one declared degree."""

    degree: int
    declaration: DegreeKPricingDeclaration
    primal_value: Rational
    dual_value: Rational
    exact_gap: Rational
    alpha: Matrix
    residual: Matrix
    y_star: Matrix
    W_LP: Matrix
    certificate: QuotientDistanceCertificate
    status: ClassVar[str] = "EXACT_COMPUTATIONAL_RECEIPT"
    authority_effect: str = "None"

    @property
    def min_l1(self) -> Rational:
        """Compatibility spelling for the exact primal value."""

        return self.primal_value

    @property
    def alpha_star(self) -> Matrix:
        return self.alpha

    @property
    def duality_gap(self) -> Rational:
        return self.exact_gap

    @property
    def is_certified(self) -> bool:
        """Whether the finite rational primal/dual receipt replays exactly."""

        return self.verify()

    def verify(self) -> bool:
        try:
            self.declaration.validate()
        except DegreeKPricingRefused:
            return False
        return (
            self.degree == self.declaration.degree
            and self.authority_effect == "None"
            and self.certificate.verify()
            and exact_equal(self.alpha, self.certificate.repair_witness)
            and exact_equal(self.residual, self.certificate.residual)
            and exact_equal(self.y_star, self.certificate.dual_witness)
            and exact_equal(self.W_LP, self.y_star)
            and simplify(self.primal_value - self.certificate.distance) == 0
            and simplify(self.dual_value - self.certificate.dual_pairing) == 0
            and simplify(self.primal_value - self.dual_value) == 0
            and simplify(self.exact_gap) == 0
        )


def _require_degree_k_declaration(
    declaration: DegreeKPricingDeclaration | None,
    degree: int | None = None,
) -> DegreeKPricingDeclaration:
    if declaration is None:
        raise DegreeKPricingRefused("the exact rail requires a DegreeKPricingDeclaration")
    if not isinstance(declaration, DegreeKPricingDeclaration):
        raise DegreeKPricingRefused("invalid degree-k pricing declaration type")
    declaration.validate()
    if degree is not None and declaration.degree != degree:
        raise DegreeKPricingRefused(
            f"declaration degree {declaration.degree} does not match requested degree {degree}"
        )
    return declaration


def _exact_repair_map(
    d_lower: MatrixBase | Sequence[Sequence[ExactInput]],
) -> Matrix:
    if isinstance(d_lower, MatrixBase):
        return exact_matrix_from_matrix(d_lower)
    return exact_matrix(d_lower)


def _exact_cochain_column(
    omega: MatrixBase | Sequence[ExactInput],
) -> Matrix:
    if isinstance(omega, MatrixBase):
        vector = exact_matrix_from_matrix(omega)
        if vector.cols != 1:
            raise DegreeKPricingRefused("omega must be an exact column vector")
        return vector
    return exact_column(omega)


def solve_degree_k_phi_exact(
    d_lower: MatrixBase | Sequence[Sequence[ExactInput]],
    omega: MatrixBase | Sequence[ExactInput],
    declaration: DegreeKPricingDeclaration | None,
) -> ExactDegreeKPhiReceipt:
    """Solve a declared finite rational degree-k quotient problem exactly.

    Binary floats are rejected by the shared exact scalar gate.  The returned
    ``y_star`` (also exposed as ``W_LP``) is the LP dual witness; it is not an
    estate-level semantic object and carries no authority.
    """

    capability = _require_degree_k_declaration(declaration)
    repair_map = _exact_repair_map(d_lower)
    cochain = _exact_cochain_column(omega)
    if repair_map.rows == 0 or cochain.rows == 0:
        raise DegreeKPricingRefused("empty/degenerate degree-k carriers are refused")
    if repair_map.rows != cochain.rows:
        raise DegreeKPricingRefused(
            f"repair map has {repair_map.rows} rows but omega has {cochain.rows} entries"
        )

    certificate = LinearRepairProblem(repair_map).quotient_l1_distance(cochain)
    primal_value = simplify(certificate.distance)
    dual_value = simplify(certificate.dual_pairing)
    receipt = ExactDegreeKPhiReceipt(
        degree=capability.degree,
        declaration=capability,
        primal_value=primal_value,
        dual_value=dual_value,
        exact_gap=simplify(primal_value - dual_value),
        alpha=certificate.repair_witness,
        residual=certificate.residual,
        y_star=certificate.dual_witness,
        W_LP=certificate.dual_witness,
        certificate=certificate,
        authority_effect="None",
    )
    if not receipt.verify():
        raise ArithmeticError("internal exact degree-k receipt failed replay")
    return receipt


def phi_k_on_complex_exact(
    complex_obj: SimplexComplex,
    degree: int,
    cochain_values: Mapping[Tuple[Any, ...], ExactInput] | Sequence[ExactInput] | MatrixBase,
    declaration: DegreeKPricingDeclaration | None,
) -> ExactDegreeKPhiReceipt:
    """Assemble a simplicial coboundary and evaluate exact ``Phi_k``.

    A mapping is keyed by canonical oriented simplex tuples.  A sequence uses
    the complex's declared ``cells[degree]`` order.  These are the only two
    witness-index conventions accepted on this rail.
    """

    capability = _require_degree_k_declaration(declaration, degree)
    cells_k = list(complex_obj.cells.get(degree, ()))
    cells_km1 = list(complex_obj.cells.get(degree - 1, ()))
    if not cells_k or not cells_km1:
        raise DegreeKPricingRefused("empty/degenerate simplicial degree is refused")
    if len(set(cells_k)) != len(cells_k) or len(set(cells_km1)) != len(cells_km1):
        raise DegreeKPricingRefused("duplicate simplex cells are refused")
    if any(len(cell) != degree + 1 or tuple(sorted(cell)) != cell for cell in cells_k):
        raise DegreeKPricingRefused("degree-k cells must be canonical oriented simplices")
    lower_set = set(cells_km1)
    if any(
        cell[:index] + cell[index + 1 :] not in lower_set
        for cell in cells_k
        for index in range(len(cell))
    ):
        raise DegreeKPricingRefused("degree-k carrier is missing a declared boundary face")

    if isinstance(cochain_values, MatrixBase):
        cochain = _exact_cochain_column(cochain_values)
    elif isinstance(cochain_values, Mapping):
        canonical_values: dict[Tuple[Any, ...], ExactInput] = {}
        for cell, value in cochain_values.items():
            canonical_cell = tuple(sorted(cell))
            if tuple(cell) != canonical_cell:
                raise DegreeKPricingRefused(
                    f"cochain index must use canonical orientation: {cell!r}"
                )
            if canonical_cell not in set(cells_k):
                raise DegreeKPricingRefused(f"cochain names undeclared degree-k cell {cell!r}")
            if canonical_cell in canonical_values:
                raise DegreeKPricingRefused(f"duplicate cochain index {canonical_cell!r}")
            canonical_values[canonical_cell] = value
        cochain = exact_column(canonical_values.get(cell, 0) for cell in cells_k)
    else:
        cochain = exact_column(cochain_values)
    if cochain.shape != (len(cells_k), 1):
        raise DegreeKPricingRefused(
            f"cochain has shape {cochain.shape}; expected {(len(cells_k), 1)}"
        )

    coboundary = rational_boundary_matrix(cells_k, cells_km1).T
    return solve_degree_k_phi_exact(coboundary, cochain, capability)


def phi_k_exact(
    complex_obj: SimplexComplex,
    degree: int,
    cochain_values: Mapping[Tuple[Any, ...], ExactInput] | Sequence[ExactInput] | MatrixBase,
    declaration: DegreeKPricingDeclaration | None,
) -> Rational:
    """Scalar convenience API for the exact declared rail."""

    return phi_k_on_complex_exact(
        complex_obj, degree, cochain_values, declaration
    ).primal_value


__all__ = [
    "DegreeKPhiUncertified",
    "DegreeKPhiReceipt",
    "solve_degree_k_phi",
    "solve_degree_k_joint_primal",
    "phi_k_on_complex",
    "phi_k_on_network",
    "phi_k_estimate",
    "phi_k",
    "DegreeKPricingRefused",
    "DegreeKPricingDeclaration",
    "ExactDegreeKPhiReceipt",
    "solve_degree_k_phi_exact",
    "phi_k_on_complex_exact",
    "phi_k_exact",
]


