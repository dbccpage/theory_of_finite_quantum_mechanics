"""SoS exact dual pricing adapter (FW-8 rail → Gate-11 cascade receipts).

AuthorityEffect: None.

Wraps ``solve_degree_k_phi_exact`` / ``DegreeKPricingDeclaration`` so the
solver-of-solvers cascade can emit independently replayable rational dual
zero-gap receipts. Float multi-cycle L1 remains diagnostic only.

Does not implement continuum duals, Pontryagin duals, or pi from residual
periods. Those are OPEN research programmes outside this adapter.
"""

from __future__ import annotations

from dataclasses import dataclass
from decimal import Decimal
from fractions import Fraction
from typing import Any, Dict, Mapping, Optional, Sequence, Tuple, Union

from sympy import Matrix, Rational, simplify
from sympy.matrices.matrixbase import MatrixBase

from omega_engine.crates.functional.degree_k_phi import (
    DegreeKPricingDeclaration,
    DegreeKPricingRefused,
    ExactDegreeKPhiReceipt,
    solve_degree_k_phi_exact,
)
from omega_engine.crates.residuals.network_residual import Network

ExactScalar = Union[int, str, Decimal, Fraction, Rational]


class ExactDualPricingError(Exception):
    """Fail-closed refusal for exact dual pricing."""

    def __init__(self, code: str, detail: str) -> None:
        self.code = code
        self.detail = detail
        super().__init__(f"{code}: {detail}")


@dataclass(frozen=True)
class ExactDualPricingReceipt:
    """SoS-facing exact dual zero-gap receipt. AuthorityEffect: None."""

    degree: int
    phi_k: Rational
    dual_value: Rational
    exact_gap: Rational
    is_certified: bool
    arithmetic_mode: str
    dual_witness_status: str
    declaration_degree: int
    authority_effect: str = "None"
    refuse_code: Optional[str] = None
    estate_wide_phi_k_theorem: str = "REFUSED"
    normhood_from_attainment_alone: str = "REFUSED"
    alpha_star: Tuple[str, ...] = ()
    y_star: Tuple[str, ...] = ()
    residual: Tuple[str, ...] = ()

    @property
    def duality_gap(self) -> Rational:
        return self.exact_gap

    def as_cascade_fields(self) -> Dict[str, Any]:
        """Fields mergeable into SolverCascadeReceipt."""
        gap_f: Optional[float]
        try:
            gap_f = float(self.exact_gap)
        except Exception:
            gap_f = None
        return {
            "is_certified": self.is_certified,
            "duality_gap": gap_f if self.is_certified else gap_f,
            "dual_witness_status": self.dual_witness_status,
            "exact_phi_k": str(self.phi_k),
            "exact_dual_value": str(self.dual_value),
            "exact_gap": str(self.exact_gap),
            "exact_degree": self.degree,
            "arithmetic_mode": self.arithmetic_mode,
            "authority_effect": self.authority_effect,
            "estate_wide_phi_k_theorem": self.estate_wide_phi_k_theorem or "REFUSED",
            "normhood_from_attainment_alone": self.normhood_from_attainment_alone
            or "REFUSED",
        }


def _matrix_to_str_tuple(mat: MatrixBase) -> Tuple[str, ...]:
    col = mat if mat.cols == 1 else mat
    if col.cols != 1:
        flat = []
        for i in range(col.rows):
            for j in range(col.cols):
                flat.append(str(col[i, j]))
        return tuple(flat)
    return tuple(str(col[i, 0]) for i in range(col.rows))


def _from_exact_receipt(receipt: ExactDegreeKPhiReceipt) -> ExactDualPricingReceipt:
    ok = bool(receipt.verify()) and simplify(receipt.exact_gap) == 0
    return ExactDualPricingReceipt(
        degree=receipt.degree,
        phi_k=receipt.primal_value,
        dual_value=receipt.dual_value,
        exact_gap=receipt.exact_gap,
        is_certified=ok,
        arithmetic_mode="Q",
        dual_witness_status="certified_exact" if ok else "uncertified_exact",
        declaration_degree=receipt.declaration.degree,
        authority_effect="None",
        refuse_code=None if ok else "EXACT_REPLAY_FAILED",
        estate_wide_phi_k_theorem="REFUSED",
        normhood_from_attainment_alone="REFUSED",
        alpha_star=_matrix_to_str_tuple(receipt.alpha),
        y_star=_matrix_to_str_tuple(receipt.y_star),
        residual=_matrix_to_str_tuple(receipt.residual),
    )


def refuse_float_as_exact(is_float_certified: bool, arithmetic_mode: str) -> None:
    """Kill: a float-derived result must never be sold as exact certification."""
    if is_float_certified:
        raise ExactDualPricingError(
            "FLOAT_AS_EXACT",
            "float-derived certification is refused regardless of its claimed "
            f"arithmetic_mode={arithmetic_mode!r}",
        )


def refuse_ls_as_canonical(status: str) -> None:
    """Kill: least-squares surrogate must never claim canonical/exact status."""
    if status in ("CANONICAL", "PROVEN", "EXACT_COMPUTATIONAL_RECEIPT", "certified_exact"):
        raise ExactDualPricingError(
            "LS_AS_CANONICAL",
            f"least-squares surrogate cannot claim status {status!r}",
        )


def refuse_phi1_sold_as_phi2(declared_degree: int, computed_degree: int) -> None:
    if declared_degree != computed_degree:
        raise ExactDualPricingError(
            "DEGREE_MISMATCH",
            f"declared degree {declared_degree} != computed degree {computed_degree}",
        )


def refuse_attainment_as_estate_quotient_norm(
    *,
    claim_estate_wide_quotient_norm: bool,
    claim_normhood_from_attainment_alone: bool = False,
) -> None:
    """Kill: finite dual zero-gap attainment ≠ estate-wide quotient-norm theorem.

    Exact Φ_k receipts prove certificate attainment (primal/dual gap 0) on a
    declared finite carrier. Quotient-normhood requires genuine J_k (+ closed
    im d). Estate-wide / arbitrary-carrier theorem remains OPEN (FW-8 FC11).
    """
    if claim_estate_wide_quotient_norm or claim_normhood_from_attainment_alone:
        raise ExactDualPricingError(
            "ATTAINMENT_AS_ESTATE_QUOTIENT_NORM",
            "dual zero-gap attainment is certificate-only; estate-wide "
            "quotient-norm / normhood-from-attainment alone is REFUSED (OPEN theorem)",
        )


def network_incidence_d0(network: Network) -> Matrix:
    """Exact d0 : C0 → C1 incidence matrix (rows=edges, cols=nodes)."""
    nodes = list(network.nodes)
    edges = list(network.edges)
    n0, n1 = len(nodes), len(edges)
    if n0 == 0 or n1 == 0:
        raise ExactDualPricingError("EMPTY_NETWORK", "network has no nodes or edges")
    node_idx = {n: i for i, n in enumerate(nodes)}
    rows = []
    for u, v in edges:
        row = [Rational(0)] * n0
        row[node_idx[u]] = Rational(-1)
        row[node_idx[v]] = Rational(1)
        rows.append(row)
    return Matrix(rows)


def residual_column(
    network: Network,
    residual: Mapping[Tuple[Any, Any], Any],
) -> Matrix:
    """Ordered exact omega column aligned with ``network.edges``.

    Python binary floats are refused at this public exact boundary. Callers may
    use integers, ``Fraction``, ``Decimal``, strings, or SymPy rationals.
    ``Decimal`` is converted through its exact base-10 representation.
    """
    vals = []
    for e in network.edges:
        raw = residual.get(e, 0)
        if isinstance(raw, bool):
            raise ExactDualPricingError("BOOL_SCALAR", "boolean residual entries refused")
        if isinstance(raw, float):
            raise ExactDualPricingError(
                "FLOAT_SCALAR",
                f"binary float residual at edge {e!r} refused by exact pricing",
            )
        if isinstance(raw, Decimal):
            vals.append(Rational(str(raw)))
        else:
            vals.append(Rational(raw))
    return Matrix(vals)


def price_exact_degree_k(
    d_lower: MatrixBase | Sequence[Sequence[ExactScalar]],
    omega: MatrixBase | Sequence[ExactScalar],
    declaration: Optional[DegreeKPricingDeclaration] = None,
    *,
    degree: Optional[int] = None,
) -> ExactDualPricingReceipt:
    """Exact dual pricing for a declared finite cochain residual.

    Requires DegreeKPricingDeclaration (default: exact_l1 at ``degree`` or 1).
    Binary floats inside d_lower/omega are rejected by the exact scalar gate.
    """
    if declaration is None:
        k = 1 if degree is None else degree
        declaration = DegreeKPricingDeclaration.exact_l1(k)
    if degree is not None:
        refuse_phi1_sold_as_phi2(declaration.degree, degree)
    try:
        exact = solve_degree_k_phi_exact(d_lower, omega, declaration)
    except (DegreeKPricingRefused, TypeError) as err:
        raise ExactDualPricingError("PRICING_REFUSED", str(err)) from err
    receipt = _from_exact_receipt(exact)
    if not receipt.is_certified:
        raise ExactDualPricingError(
            "ZERO_GAP_FAILED",
            f"exact gap {receipt.exact_gap} failed replay",
        )
    return receipt


def price_network_phi1_exact(
    network: Network,
    residual: Mapping[Tuple[Any, Any], Any],
    declaration: Optional[DegreeKPricingDeclaration] = None,
) -> ExactDualPricingReceipt:
    """Price a network edge residual at degree 1 with exact dual zero-gap."""
    if declaration is None:
        declaration = DegreeKPricingDeclaration.exact_l1(1)
    if declaration.degree != 1:
        raise ExactDualPricingError(
            "NETWORK_PHI1_DEGREE",
            "price_network_phi1_exact requires declaration.degree == 1",
        )
    d0 = network_incidence_d0(network)
    omega = residual_column(network, residual)
    return price_exact_degree_k(d0, omega, declaration, degree=1)


def price_degree_k_with_optional_nilpotency(
    d_lower: MatrixBase | Sequence[Sequence[ExactScalar]],
    omega: MatrixBase | Sequence[ExactScalar],
    declaration: DegreeKPricingDeclaration,
    d_upper: Optional[MatrixBase] = None,
) -> ExactDualPricingReceipt:
    """Exact Phi_k with optional d_k o d_{k-1} = 0 gate for k requiring Gamma descent.

    When ``d_upper`` is supplied, enforces nilpotency of the degree-(k) face:
    d_upper @ d_lower == 0 (exact). For Phi_2 this is d2@d1 or d1@d0 depending
    on carrier convention; caller supplies the pair that prices the residual.
    """
    if d_upper is not None:
        dL = d_lower if isinstance(d_lower, MatrixBase) else Matrix(d_lower)
        dU = d_upper if isinstance(d_upper, MatrixBase) else Matrix(d_upper)
        if dU.cols == dL.rows:
            product = dU * dL
            if product != Matrix.zeros(product.rows, product.cols):
                raise ExactDualPricingError(
                    "NILPOTENCY_FAILED",
                    "d_upper @ d_lower is not zero; refuse Phi_k descent",
                )
        elif dL.cols == dU.rows:
            product = dL * dU
            if product != Matrix.zeros(product.rows, product.cols):
                raise ExactDualPricingError(
                    "NILPOTENCY_FAILED",
                    "d_lower @ d_upper is not zero; refuse Phi_k descent",
                )
        else:
            raise ExactDualPricingError(
                "NILPOTENCY_SHAPE",
                f"cannot check nilpotency: d_lower {dL.shape} vs d_upper {dU.shape}",
            )
    return price_exact_degree_k(d_lower, omega, declaration, degree=declaration.degree)


__all__ = [
    "ExactDualPricingError",
    "ExactDualPricingReceipt",
    "refuse_float_as_exact",
    "refuse_ls_as_canonical",
    "refuse_phi1_sold_as_phi2",
    "refuse_attainment_as_estate_quotient_norm",
    "network_incidence_d0",
    "residual_column",
    "price_exact_degree_k",
    "price_network_phi1_exact",
    "price_degree_k_with_optional_nilpotency",
    "DegreeKPricingDeclaration",
]
