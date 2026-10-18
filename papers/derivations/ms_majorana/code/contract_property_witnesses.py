"""Integer contract witnesses named by MajoranaCore. No hardware claim is discharged.

Origin: papers/derivations/ms_majorana/lean4/MajoranaCore.lean theorems parity_eigenvalues, pfaffian_topological_sign, ising_quantum_dim_squared, toric_distance_3x4, and transfer_gap_strictly_positive
Claim: urn:omega:fqm:ms-majorana:contract:integer-witnesses:v1
AuthorityEffect: None
Mutation-Kills: 6 non-equivalent source mutants, executed by papers/derivations/ms_majorana/code/tests/unit/test_l5a_exact_slice.py.
Scope Fence: These identities do not establish a Majorana zero mode in a device, a transfer rate, or a continuum limit.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Mapping


class ContractError(ValueError):
    """One violated contract invariant, with the measured parameters."""

    def __init__(self, invariant: str, parameters: Mapping[str, object] | None = None) -> None:
        self.invariant = invariant
        self.parameters = {} if parameters is None else dict(parameters)
        rendered = ", ".join(f"{key}={value}" for key, value in self.parameters.items())
        message = invariant if rendered == "" else f"{invariant} ({rendered})"
        super().__init__(message)


def _fail(invariant: str, **parameters: object) -> ContractError:
    return ContractError(invariant, parameters)


def _sign(value: object, role: str) -> int:
    if isinstance(value, float):
        raise _fail("float refused at the public boundary", role=role, received="float")
    if isinstance(value, bool) or type(value) is not int:
        raise _fail("boolean or non-integer sign refused", role=role, received=type(value).__name__)
    if value != 1 and value != -1:
        raise _fail("sign is not 1 or -1", role=role, received=value)
    return value


def _positive(value: object, role: str) -> int:
    if isinstance(value, float):
        raise _fail("float refused at the public boundary", role=role, received="float")
    if isinstance(value, bool) or type(value) is not int:
        raise _fail("boolean or non-integer refused", role=role, received=type(value).__name__)
    if value <= 0:
        raise _fail("positive integer required", role=role, received=value)
    return value


@dataclass(frozen=True)
class SignSquareCertificate:
    """Witness that a declared sign squares to 1."""

    sign: int
    square: int


def certify_parity_square(eigenvalue: object) -> SignSquareCertificate:
    """Discharge parity_eigenvalues for one declared eigenvalue."""
    sign = _sign(eigenvalue, "eigenvalue")
    square = sign * sign
    if square != 1:
        raise _fail("parity eigenvalue did not square to 1", eigenvalue=sign, square=square)
    return SignSquareCertificate(sign, square)


def certify_pfaffian_sign(sign: object) -> SignSquareCertificate:
    """Discharge pfaffian_topological_sign for one declared sign."""
    parsed = _sign(sign, "pfaffian")
    square = parsed * parsed
    if square != 1:
        raise _fail("pfaffian sign did not square to 1", sign=parsed, square=square)
    return SignSquareCertificate(parsed, square)


@dataclass(frozen=True)
class IsingDimensionCertificate:
    """Witness that the squared Ising quantum dimensions satisfy sigma^2 = 1 + 1."""

    one_sq: int
    psi_sq: int
    sigma_sq: int


def certify_ising_dimensions() -> IsingDimensionCertificate:
    """Discharge ising_quantum_dim_squared on the three declared anyon labels."""
    one_sq = 1
    psi_sq = 1
    sigma_sq = 2
    if sigma_sq != one_sq + psi_sq:
        raise _fail("Ising dimension squares disagreed", sigma_sq=sigma_sq, sum=one_sq + psi_sq)
    return IsingDimensionCertificate(one_sq, psi_sq, sigma_sq)


@dataclass(frozen=True)
class ToricDistanceCertificate:
    """Witness that toric distance is the minimum of the two positive side lengths."""

    rows: int
    cols: int
    distance: int


def certify_toric_distance(rows: object, cols: object) -> ToricDistanceCertificate:
    """Discharge toric_distance, including the 3 by 4 case whose distance is 3."""
    parsed_rows = _positive(rows, "rows")
    parsed_cols = _positive(cols, "cols")
    distance = parsed_rows if parsed_rows < parsed_cols else parsed_cols
    if parsed_rows == 3 and parsed_cols == 4 and distance != 3:
        raise _fail("toric distance of the 3 by 4 torus is not 3", distance=distance)
    return ToricDistanceCertificate(parsed_rows, parsed_cols, distance)


@dataclass(frozen=True)
class TransferGapCertificate:
    """Witness that the product of two positive integers is positive."""

    gamma_qp: int
    braid_time: int
    product: int


def certify_transfer_gap(gamma_qp: object, braid_time: object) -> TransferGapCertificate:
    """Discharge transfer_gap_strictly_positive as an integer product, not a physical rate."""
    gamma = _positive(gamma_qp, "gamma_qp")
    time = _positive(braid_time, "braid_time")
    product = gamma * time
    if product <= 0:
        raise _fail("transfer gap product is not positive", gamma_qp=gamma, braid_time=time, product=product)
    return TransferGapCertificate(gamma, time, product)


__all__ = [
    "ContractError",
    "IsingDimensionCertificate",
    "SignSquareCertificate",
    "ToricDistanceCertificate",
    "TransferGapCertificate",
    "certify_ising_dimensions",
    "certify_parity_square",
    "certify_pfaffian_sign",
    "certify_toric_distance",
    "certify_transfer_gap",
]
