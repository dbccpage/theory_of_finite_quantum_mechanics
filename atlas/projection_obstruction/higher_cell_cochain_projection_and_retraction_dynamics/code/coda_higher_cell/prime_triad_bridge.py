"""Declared carrier metadata, aligned adapter losses, and local stop policies.

These helpers do not execute external Prime algorithms or grant authority.
AuthorityEffect: None.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Sequence

import numpy as np

from ._validation import integer, matrix, nonnegative
from .defect_bounds import schatten_1_norm


@dataclass(frozen=True)
class PrimeTriadCarrier:
    """Carrier metadata: dimension_k is degree p = len(simplex)-1."""

    carrier_id: str
    dimension_k: int
    simplex: tuple[int, ...]
    residual_norm: float
    adapter_loss: float
    witness_verified: bool
    budget_remaining: int
    boundary_map_id: str | None = None
    observation_map_id: str | None = None
    witness_receipt_id: str | None = None
    state_fingerprint: str | None = None

    def __post_init__(self) -> None:
        if not isinstance(self.carrier_id, str) or not self.carrier_id.strip():
            raise ValueError("carrier_id must be nonempty")
        degree = integer(self.dimension_k, "dimension_k")
        if not isinstance(self.simplex, tuple) or len(self.simplex) != degree + 1:
            raise ValueError("dimension_k must equal len(simplex)-1")
        vertices = tuple(integer(v, "vertex") for v in self.simplex)
        if tuple(sorted(set(vertices))) != vertices:
            raise ValueError("simplex vertices must be distinct and increasing")
        nonnegative(self.residual_norm, "residual_norm")
        nonnegative(self.adapter_loss, "adapter_loss")
        integer(self.budget_remaining, "budget_remaining")
        if type(self.witness_verified) is not bool:
            raise ValueError("witness_verified must be a bool")
        for identifier in (
            self.boundary_map_id,
            self.observation_map_id,
            self.witness_receipt_id,
            self.state_fingerprint,
        ):
            if identifier is not None and (
                not isinstance(identifier, str) or not identifier.strip()
            ):
                raise ValueError("optional evidence identifiers must be nonempty strings")


def prime_triad_carrier_declaration(carrier: PrimeTriadCarrier) -> dict[str, Any]:
    """Report metadata completeness; identifiers do not verify map contents."""
    valid = bool(
        carrier.boundary_map_id
        and carrier.observation_map_id
        and carrier.witness_receipt_id
        and carrier.witness_verified
    )
    steps = [
        {
            "step": 1,
            "name": "CarrierDefinition",
            "simplex": carrier.simplex,
            "degree": carrier.dimension_k,
        },
        {"step": 2, "name": "BoundaryMap", "identifier": carrier.boundary_map_id},
        {"step": 3, "name": "ObservationMap", "identifier": carrier.observation_map_id},
        {"step": 4, "name": "ProductNormalProjector", "status": "REQUIRES_IMPLEMENTATION"},
        {
            "step": 5,
            "name": "Witness",
            "identifier": carrier.witness_receipt_id,
            "reported_verified": carrier.witness_verified,
        },
        {"step": 6, "name": "Route", "authority_effect": "None"},
        {"step": 7, "name": "Completion", "status": "METADATA_ONLY"},
    ]
    return {
        "carrier_id": carrier.carrier_id,
        "dimension_k": carrier.dimension_k,
        "declaration_valid": valid,
        "declaration_steps": steps,
        "validation_scope": "metadata completeness; evidence contents not replayed",
        "authority_effect": "None",
    }


def adapter_loss_ledger(
    k_defect: np.ndarray, lifted_boundary_defects: Sequence[np.ndarray]
) -> float:
    """||Z - sum_f E_f Z_f||_1 with supplied common-space lifts.

    A difference of scalar norms is only a lower bound and is not accepted
    as an adapter-loss certificate.
    """
    z = matrix(k_defect, "ambient defect")
    total = np.zeros_like(z)
    for lifted in lifted_boundary_defects:
        total += matrix(lifted, "lifted boundary defect", z.shape)
    return schatten_1_norm(z - total)


def can_continue_predicate(
    carrier: PrimeTriadCarrier,
    max_complex_dim: int,
    stagnation_tol: float = 1e-6,
    history_residuals: list[float] | None = None,
    history_states: Sequence[str] | None = None,
) -> tuple[bool, str]:
    """Apply local stop policies; passing does not establish a higher theorem.

    Equal scalar residuals do not establish repeated carrier states.
    history_states must contain fingerprints of complete declared states
    preceding the current one; carrier.state_fingerprint identifies the current state. The caller supplies that identity evidence.
    """
    cap = integer(max_complex_dim, "max_complex_dim")
    tol = nonnegative(stagnation_tol, "stagnation_tol")
    if history_residuals is not None:
        for value in history_residuals:
            nonnegative(value, "history residual")
    if history_states is not None and any(
        not isinstance(s, str) or not s.strip() for s in history_states
    ):
        raise ValueError("state fingerprints must be nonempty strings")
    if carrier.residual_norm == 0:
        return (
            False,
            "HALT_ZERO_RESIDUAL: first-order speed is zero; future exactness is not established",
        )
    if carrier.dimension_k >= cap:
        return False, "HALT_DIMENSION_CAP: no higher simplicial degree in the declared carrier"
    if carrier.adapter_loss < tol:
        return False, "HALT_STAGNATION: declared adapter loss is below the policy threshold"
    if carrier.budget_remaining == 0:
        return False, "HALT_BUDGET_DEPLETION: declared budget exhausted"
    if (
        history_states is not None
        and carrier.state_fingerprint is not None
        and carrier.state_fingerprint in history_states
    ):
        return False, "HALT_OSCILLATION: supplied full-state fingerprint repeats"
    if not carrier.witness_verified:
        return False, "HALT_UNVERIFIED_PROMOTION: no reported witness verification"
    if not prime_triad_carrier_declaration(carrier)["declaration_valid"]:
        return False, "HALT_MISSING_DECLARATION: evidence identifiers are incomplete"
    return True, "CONTINUE_ASCENT: local policy permits a next check; no authority is granted"
