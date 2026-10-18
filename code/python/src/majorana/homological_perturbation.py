"""Homological Perturbation Lemma (HPL) adapter for native exact-Q math.

AuthorityEffect: None / EvidenceOnly.

Implements the transfer of a differential perturbation δ through a normalized
contraction (i, r, h) : C^• ⇄ D^• under the convention

    id_C − i ∘ r = d_C ∘ h + h ∘ d_C

(the one verify_normalized checks). For that convention the lemma reads

    δ_D = r ∘ (1 + δ h)^{−1} ∘ δ ∘ i

when (1 + δ h) is invertible over Q. The form r (1 − δ h)^{−1} δ i printed in
the retired PO-015 paper belongs to the opposite convention i ∘ r − id_C =
d h + h d; under this module's convention it breaks the chain-map property of
the perturbed inclusion whenever r δ h δ i ≠ 0.

This module is intentionally free of authority effects, host state mutation,
or solver cascade side-effects. It only emits a DeformationReceipt that a
higher stage (CascadeSolver evaluation path) may consume as evidence.

Degree window is fixed to 0–1–2 to match FiniteCochainComplex substrate.
Public carriers use fractions.Fraction; matrix arithmetic and HPL verification
execute in the canonical Rust math crates. Native refusals propagate.

References
----------
- Witnessed Difference Programme, WDP-CH16-C01 (sign-corrected statement for
  this convention)
- Homological Perturbation Lemma (classical / nLab)
"""

from __future__ import annotations

import hashlib
import json
from collections.abc import Mapping
from dataclasses import asdict, dataclass, field
from fractions import Fraction
from typing import Any, Dict, Optional, Sequence, Tuple

from omega_engine_operating_system.adapters.rust_host.majorana_math import (
    NativeMathRefusal,
    call_native,
    decode_rational,
)


Scalar = Fraction
COEFFICIENT_DOMAIN = "Q"
SCHEMA_VERSION = "homology.homological_perturbation.v0.1"


def _scalar(value: int | str | Fraction) -> Scalar:
    if isinstance(value, bool) or isinstance(value, float):
        raise TypeError("floating point / bool forbidden; use int, str, or Fraction")
    return Fraction(value)


@dataclass(frozen=True)
class ExactMatrix:
    """Dense matrix over Q with explicit (rows, cols) so 0-row matrices keep shape."""

    rows: int
    cols: int
    data: Tuple[Tuple[Fraction, ...], ...]

    def __post_init__(self) -> None:
        if any(
            isinstance(d, bool) or not isinstance(d, int) or d < 0 for d in (self.rows, self.cols)
        ):
            raise ValueError("dimensions must be nonnegative integers")
        object.__setattr__(self, "data", tuple(tuple(_scalar(x) for x in row) for row in self.data))
        if self.rows == 0:
            if self.data != ():
                raise ValueError("0-row matrix must have data=()")
            return
        if len(self.data) != self.rows:
            raise ValueError(f"data has {len(self.data)} rows; expected {self.rows}")
        for i, row in enumerate(self.data):
            if len(row) != self.cols:
                raise ValueError(f"row {i} has length {len(row)}; expected {self.cols}")

    @classmethod
    def zero(cls, rows: int, cols: int) -> "ExactMatrix":
        z = Fraction(0)
        data = tuple(tuple(z for _ in range(cols)) for _ in range(rows))
        return cls(rows, cols, data)

    @classmethod
    def identity(cls, n: int) -> "ExactMatrix":
        data = tuple(tuple(Fraction(1 if i == j else 0) for j in range(n)) for i in range(n))
        return cls(n, n, data)

    @classmethod
    def from_rows(
        cls,
        rows_data: Sequence[Sequence[int | str | Fraction]],
        *,
        expected_rows: Optional[int] = None,
        expected_cols: Optional[int] = None,
        label: str = "matrix",
    ) -> "ExactMatrix":
        for dimension in (expected_rows, expected_cols):
            if dimension is not None and (
                isinstance(dimension, bool) or not isinstance(dimension, int) or dimension < 0
            ):
                raise ValueError("expected dimensions must be nonnegative integers")
        if expected_rows is not None and len(rows_data) != expected_rows:
            raise ValueError(f"{label} has {len(rows_data)} rows; expected {expected_rows}")
        rows = len(rows_data)
        if rows == 0:
            cols = expected_cols if expected_cols is not None else 0
            return cls(0, cols, ())
        cols = len(rows_data[0])
        if expected_cols is not None and cols != expected_cols:
            raise ValueError(f"{label} has {cols} cols; expected {expected_cols}")
        data = tuple(tuple(_scalar(v) for v in row) for row in rows_data)
        for i, row in enumerate(data):
            if len(row) != cols:
                raise ValueError(f"{label}[{i}] has length {len(row)}; expected {cols}")
        return cls(rows, cols, data)

    @property
    def shape(self) -> Tuple[int, int]:
        return (self.rows, self.cols)

    def is_zero(self) -> bool:
        return all(all(x == 0 for x in row) for row in self.data)

    def _wire(self) -> dict[str, Any]:
        return {
            "rows": self.rows,
            "cols": self.cols,
            "data": [[str(_scalar(x)) for x in row] for row in self.data],
        }

    @classmethod
    def _from_wire(cls, wire: dict[str, Any]) -> "ExactMatrix":
        return cls.from_rows(
            [[decode_rational(value) for value in row] for row in wire["data"]],
            expected_rows=wire["rows"],
            expected_cols=wire["cols"],
        )

    def _native(self, operation: str, **kwargs: Any) -> "ExactMatrix":
        result = call_native(
            "math_rational_matrix", {"operation": operation, "matrix": self._wire(), **kwargs}
        )
        return self._from_wire(result["matrix"])

    def matmul(self, other: "ExactMatrix") -> "ExactMatrix":
        if self.cols != other.rows:
            raise ValueError(f"matmul shape mismatch: {self.shape} @ {other.shape}")
        return self._native("multiply", other=other._wire())

    def __add__(self, other: "ExactMatrix") -> "ExactMatrix":
        if self.shape != other.shape:
            raise ValueError(f"add shape mismatch: {self.shape} vs {other.shape}")
        return self._native("add", other=other._wire())

    def __sub__(self, other: "ExactMatrix") -> "ExactMatrix":
        if self.shape != other.shape:
            raise ValueError(f"sub shape mismatch: {self.shape} vs {other.shape}")
        return self._native("subtract", other=other._wire())

    def __neg__(self) -> "ExactMatrix":
        return self._native("scale", scalar="-1")

    def try_invert(self) -> Optional["ExactMatrix"]:
        """Return the native exact inverse, or None if singular."""
        if self.rows != self.cols:
            raise ValueError("try_invert requires square matrix")
        result = call_native(
            "math_rational_matrix", {"operation": "inverse", "matrix": self._wire()}
        )["matrix"]
        return None if result is None else self._from_wire(result)

    def digest(self) -> str:
        payload = {
            "rows": self.rows,
            "cols": self.cols,
            "data": [[str(x) for x in row] for row in self.data],
        }
        raw = json.dumps(payload, sort_keys=True).encode("utf-8")
        return hashlib.sha256(raw).hexdigest()


def zero_matrix(rows: int, cols: int) -> ExactMatrix:
    return ExactMatrix.zero(rows, cols)


def identity_matrix(n: int) -> ExactMatrix:
    return ExactMatrix.identity(n)


def try_invert(m: ExactMatrix) -> Optional[ExactMatrix]:
    return m.try_invert()


def is_zero_matrix(m: ExactMatrix) -> bool:
    return m.is_zero()




@dataclass(frozen=True)
class DegreeDimensions:
    """Dimensions of a cochain complex in degrees 0, 1, 2."""

    dim0: int
    dim1: int
    dim2: int

    def __post_init__(self) -> None:
        if any(
            isinstance(d, bool) or not isinstance(d, int) or d < 0
            for d in (self.dim0, self.dim1, self.dim2)
        ):
            raise ValueError("dimensions must be nonnegative integers")


@dataclass(frozen=True)
class NormalizedContraction:
    """Normalized (special) deformation retract / contraction data.

    Maps (degree 0 chain maps i, r and degree −1 homotopy h) between
    complexes C and D of window degrees 0-1-2.

    Conventions (WDP-CH16-C01):
        i : D → C   (inclusion / section)
        r : C → D   (retraction / projection)
        h : C → C   (homotopy operator, lowers degree by 1)

    Required identities for a *normalized contraction*:
        1. r ∘ i = id_D
        2. id_C − i ∘ r = d_C ∘ h + h ∘ d_C
        3. h ∘ i = 0
        4. r ∘ h = 0
        5. h ∘ h = 0
    """

    C: DegreeDimensions
    D: DegreeDimensions
    dC0: ExactMatrix
    dC1: ExactMatrix
    dD0: ExactMatrix
    dD1: ExactMatrix
    i0: ExactMatrix
    i1: ExactMatrix
    i2: ExactMatrix
    r0: ExactMatrix
    r1: ExactMatrix
    r2: ExactMatrix
    h1: ExactMatrix
    h2: ExactMatrix

    @classmethod
    def from_matrices(
        cls,
        C_dims: tuple[int, int, int],
        D_dims: tuple[int, int, int],
        dC0: Sequence[Sequence[int | str | Fraction]],
        dC1: Sequence[Sequence[int | str | Fraction]],
        dD0: Sequence[Sequence[int | str | Fraction]],
        dD1: Sequence[Sequence[int | str | Fraction]],
        i0: Sequence[Sequence[int | str | Fraction]],
        i1: Sequence[Sequence[int | str | Fraction]],
        i2: Sequence[Sequence[int | str | Fraction]],
        r0: Sequence[Sequence[int | str | Fraction]],
        r1: Sequence[Sequence[int | str | Fraction]],
        r2: Sequence[Sequence[int | str | Fraction]],
        h1: Sequence[Sequence[int | str | Fraction]],
        h2: Sequence[Sequence[int | str | Fraction]],
    ) -> "NormalizedContraction":
        C = DegreeDimensions(*C_dims)
        D = DegreeDimensions(*D_dims)
        return cls(
            C=C,
            D=D,
            dC0=ExactMatrix.from_rows(dC0, expected_rows=C.dim1, expected_cols=C.dim0, label="dC0"),
            dC1=ExactMatrix.from_rows(dC1, expected_rows=C.dim2, expected_cols=C.dim1, label="dC1"),
            dD0=ExactMatrix.from_rows(dD0, expected_rows=D.dim1, expected_cols=D.dim0, label="dD0"),
            dD1=ExactMatrix.from_rows(dD1, expected_rows=D.dim2, expected_cols=D.dim1, label="dD1"),
            i0=ExactMatrix.from_rows(i0, expected_rows=C.dim0, expected_cols=D.dim0, label="i0"),
            i1=ExactMatrix.from_rows(i1, expected_rows=C.dim1, expected_cols=D.dim1, label="i1"),
            i2=ExactMatrix.from_rows(i2, expected_rows=C.dim2, expected_cols=D.dim2, label="i2"),
            r0=ExactMatrix.from_rows(r0, expected_rows=D.dim0, expected_cols=C.dim0, label="r0"),
            r1=ExactMatrix.from_rows(r1, expected_rows=D.dim1, expected_cols=C.dim1, label="r1"),
            r2=ExactMatrix.from_rows(r2, expected_rows=D.dim2, expected_cols=C.dim2, label="r2"),
            h1=ExactMatrix.from_rows(h1, expected_rows=C.dim0, expected_cols=C.dim1, label="h1"),
            h2=ExactMatrix.from_rows(h2, expected_rows=C.dim1, expected_cols=C.dim2, label="h2"),
        )


@dataclass(frozen=True)
class SideConditionReport:
    """Exact results for the five contraction laws and both chain-map laws."""

    ri_equals_id_D: bool
    sdr_equation: bool
    hi_zero: bool
    rh_zero: bool
    hh_zero: bool
    details: Dict[str, str] = field(default_factory=dict)
    inclusion_chain_map: bool = True
    retraction_chain_map: bool = True

    @property
    def is_normalized(self) -> bool:
        return all(
            (
                self.ri_equals_id_D,
                self.sdr_equation,
                self.hi_zero,
                self.rh_zero,
                self.hh_zero,
                self.inclusion_chain_map,
                self.retraction_chain_map,
            )
        )


def _contraction_wire(contraction: NormalizedContraction) -> dict[str, Any]:
    return {
        "c_dimensions": [contraction.C.dim0, contraction.C.dim1, contraction.C.dim2],
        "d_dimensions": [contraction.D.dim0, contraction.D.dim1, contraction.D.dim2],
        "d_c": [contraction.dC0._wire(), contraction.dC1._wire()],
        "d_d": [contraction.dD0._wire(), contraction.dD1._wire()],
        "inclusion": [getattr(contraction, f"i{k}")._wire() for k in range(3)],
        "retraction": [getattr(contraction, f"r{k}")._wire() for k in range(3)],
        "homotopy": [contraction.h1._wire(), contraction.h2._wire()],
    }


def _side_condition_report(report: dict[str, Any]) -> SideConditionReport:
    fields = {
        "ri_equals_id_D": report["ri_equals_id_d"],
        "sdr_equation": report["sdr_equation"],
        "hi_zero": report["hi_zero"],
        "rh_zero": report["rh_zero"],
        "hh_zero": report["hh_zero"],
        "inclusion_chain_map": report["inclusion_chain_map"],
        "retraction_chain_map": report["retraction_chain_map"],
    }
    if any(not isinstance(value, bool) for value in fields.values()):
        raise TypeError("native side-condition report must contain booleans")
    details = {name: "native exact identity failed" for name, value in fields.items() if not value}
    return SideConditionReport(**fields, details=details)


def verify_normalized(contraction: NormalizedContraction) -> SideConditionReport:
    """Check the normalized contraction and chain maps in native exact arithmetic."""
    result = call_native("homology_contraction", {"contraction": _contraction_wire(contraction)})
    report = result.get("report")
    if not isinstance(report, Mapping):
        raise NativeMathRefusal(
            "NATIVE_CONTRACTION_REFUSED",
            str(result.get("obstruction_reason", "native contraction report is absent")),
            outcome=getattr(result, "outcome", result),
        )
    return _side_condition_report(report)




@dataclass(frozen=True)
class DifferentialPerturbation:
    """Degree-+1 endomorphism δ of C (blocks δ0 : C0→C1, δ1 : C1→C2)."""

    delta0: ExactMatrix
    delta1: ExactMatrix

    @classmethod
    def from_matrices(
        cls,
        C_dims: tuple[int, int, int],
        delta0: Sequence[Sequence[int | str | Fraction]],
        delta1: Sequence[Sequence[int | str | Fraction]],
    ) -> "DifferentialPerturbation":
        dims = DegreeDimensions(*C_dims)
        dim0, dim1, dim2 = dims.dim0, dims.dim1, dims.dim2
        return cls(
            delta0=ExactMatrix.from_rows(
                delta0, expected_rows=dim1, expected_cols=dim0, label="delta0"
            ),
            delta1=ExactMatrix.from_rows(
                delta1, expected_rows=dim2, expected_cols=dim1, label="delta1"
            ),
        )


@dataclass(frozen=True)
class DeformationReceipt:
    """Evidence-only receipt of an HPL transfer attempt.

    AuthorityEffect is always "None". Downstream CascadeSolver / OESOS stages
    may read this receipt; they never treat it as an ActionLicense.
    """

    success: bool
    invertibility: bool
    delta_D0: Optional[ExactMatrix] = None
    delta_D1: Optional[ExactMatrix] = None
    obstruction_reason: Optional[str] = None
    side_conditions: Optional[SideConditionReport] = None
    contraction_digest: Optional[str] = None
    perturbation_digest: Optional[str] = None
    evidence_sha256: Optional[str] = None
    reduced_square_zero: Optional[bool] = None
    schema_version: str = SCHEMA_VERSION
    authority_effect: str = "None"
    coefficient_domain: str = COEFFICIENT_DOMAIN
    finite_window: Tuple[int, int, int] = (0, 1, 2)
    extra: Dict[str, Any] = field(default_factory=dict)

    def digest(self) -> str:
        def mat_repr(m: Optional[ExactMatrix]) -> Any:
            if m is None:
                return None
            return {
                "rows": m.rows,
                "cols": m.cols,
                "data": [[str(x) for x in row] for row in m.data],
            }

        payload = {
            "success": self.success,
            "invertibility": self.invertibility,
            "obstruction_reason": self.obstruction_reason,
            "delta_D0": mat_repr(self.delta_D0),
            "delta_D1": mat_repr(self.delta_D1),
            "contraction_digest": self.contraction_digest,
            "perturbation_digest": self.perturbation_digest,
            "reduced_square_zero": self.reduced_square_zero,
            "schema_version": self.schema_version,
            "authority_effect": self.authority_effect,
            "coefficient_domain": self.coefficient_domain,
            "finite_window": self.finite_window,
            "side_conditions": None
            if self.side_conditions is None
            else asdict(self.side_conditions),
            "extra": self.extra,
        }
        raw = json.dumps(payload, sort_keys=True, default=str).encode("utf-8")
        return hashlib.sha256(raw).hexdigest()


def _stable_digest_of_contraction(c: NormalizedContraction) -> str:
    parts = {
        "C": (c.C.dim0, c.C.dim1, c.C.dim2),
        "D": (c.D.dim0, c.D.dim1, c.D.dim2),
        "dC0": c.dC0.digest(),
        "dC1": c.dC1.digest(),
        "dD0": c.dD0.digest(),
        "dD1": c.dD1.digest(),
        "i0": c.i0.digest(),
        "i1": c.i1.digest(),
        "i2": c.i2.digest(),
        "r0": c.r0.digest(),
        "r1": c.r1.digest(),
        "r2": c.r2.digest(),
        "h1": c.h1.digest(),
        "h2": c.h2.digest(),
    }
    raw = json.dumps(parts, sort_keys=True).encode("utf-8")
    return hashlib.sha256(raw).hexdigest()


def _stable_digest_of_perturbation(p: DifferentialPerturbation) -> str:
    parts = {
        "delta0": p.delta0.digest(),
        "delta1": p.delta1.digest(),
    }
    raw = json.dumps(parts, sort_keys=True).encode("utf-8")
    return hashlib.sha256(raw).hexdigest()


def transfer_perturbation(
    contraction: NormalizedContraction,
    perturbation: DifferentialPerturbation,
    *,
    require_normalized: bool = True,
    check_perturbed_square_zero: bool = False,
) -> DeformationReceipt:
    """Transfer a perturbation with the canonical native HPL implementation.

    The native transfer verifies contraction chain maps and both original and
    perturbed square-zero identities on every call. The retained flags are sent
    to the host for API compatibility; they cannot disable native invariants.
    Mathematical obstructions return unsuccessful evidence receipts. Transport
    failures raise NativeMathRefusal and never invoke a Python math fallback.
    """
    if not isinstance(require_normalized, bool) or not isinstance(
        check_perturbed_square_zero, bool
    ):
        raise TypeError("HPL verification flags must be booleans")
    result = call_native(
        "homology_perturbation",
        {
            "contraction": _contraction_wire(contraction),
            "delta": [perturbation.delta0._wire(), perturbation.delta1._wire()],
            "require_normalized": require_normalized,
            "check_perturbed_square_zero": check_perturbed_square_zero,
        },
    )
    deltas = result.get("delta_d")
    report = result.get("side_conditions")
    extra: Dict[str, Any] = {}
    if isinstance(getattr(result, "outcome", None), Mapping):
        extra["native_outcome"] = dict(result.outcome)
    if result.get("perturbed_contraction") is not None:
        extra["native_checked_contraction"] = result["perturbed_contraction"]
    receipt = DeformationReceipt(
        success=result["success"],
        invertibility=result["invertibility"],
        delta_D0=None if deltas is None else ExactMatrix._from_wire(deltas[0]),
        delta_D1=None if deltas is None else ExactMatrix._from_wire(deltas[1]),
        obstruction_reason=result.get("obstruction_reason"),
        side_conditions=None if report is None else _side_condition_report(report),
        contraction_digest=_stable_digest_of_contraction(contraction),
        perturbation_digest=_stable_digest_of_perturbation(perturbation),
        reduced_square_zero=result.get("reduced_square_zero"),
        extra=extra,
    )
    object.__setattr__(receipt, "evidence_sha256", receipt.digest())
    return receipt


def identity_contraction(
    dims: tuple[int, int, int],
    d0: Sequence[Sequence[int | str | Fraction]],
    d1: Sequence[Sequence[int | str | Fraction]],
) -> NormalizedContraction:
    """Trivial normalized contraction of a complex onto itself (i=r=id, h=0)."""
    dim0, dim1, dim2 = dims
    id0 = ExactMatrix.identity(dim0)
    id1 = ExactMatrix.identity(dim1)
    id2 = ExactMatrix.identity(dim2)
    z01 = ExactMatrix.zero(dim0, dim1)
    z12 = ExactMatrix.zero(dim1, dim2)
    return NormalizedContraction.from_matrices(
        C_dims=dims,
        D_dims=dims,
        dC0=d0,
        dC1=d1,
        dD0=d0,
        dD1=d1,
        i0=id0.data,
        i1=id1.data,
        i2=id2.data,
        r0=id0.data,
        r1=id1.data,
        r2=id2.data,
        h1=z01.data,
        h2=z12.data,
    )


__all__ = [
    "COEFFICIENT_DOMAIN",
    "SCHEMA_VERSION",
    "ExactMatrix",
    "DegreeDimensions",
    "NormalizedContraction",
    "SideConditionReport",
    "DifferentialPerturbation",
    "DeformationReceipt",
    "verify_normalized",
    "transfer_perturbation",
    "identity_contraction",
    "try_invert",
    "zero_matrix",
    "identity_matrix",
    "is_zero_matrix",
]
