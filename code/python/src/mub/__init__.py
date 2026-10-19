"""Python dual-implementation for Mutually Unbiased Bases (MUB).

AuthorityEffect: None.
Dual-home with code/rust/src/mub (crate tfqm_mub).
"""

from __future__ import annotations

from fractions import Fraction
from typing import Any, Dict

# Re-exports from mub_verify
from .mub_verify import (
    Cyc24,
    SqrtBox,
    cyc24_interval_enclosure,
    sqrt_rational_interval,
    BasisBox,
    RationalInterval,
    VectorBox,
    box_volume,
    boxes_overlap_interior,
    EnclosedTriple,
    EnclosedVector,
    D,
    standard_basis_b1,
    verify_triple_pairwise_mu,
    CertifiedBox,
    CoverReport,
    box_touches_torus,
    cover_region,
    verify_full_coverage,
    FullCoverageSummary,
    IndependentMubVerifier,
    SampledBoxResult,
    StratifiedVerificationSummary,
)

AUTHORITY_EFFECT: str = "None"


def authority_effect() -> str:
    """Always 'None' — this surface mints no authority."""
    return AUTHORITY_EFFECT


def package_info() -> Dict[str, str]:
    """Crate identity matching Rust python.rs."""
    return {
        "name": "omega_mub",
        "math_ssot": "rust",
        "authority_effect": "None",
        "note": "Dual-face Python/Rust MUB verification suite.",
    }


def verify_mub_crate_invariants() -> bool:
    """Top-level MUB invariant verification executing genuine algebraic checks."""
    from .mub_verify.mub_triples import dita_seed_triple_columns, verify_triple_pairwise_mu
    cols = dita_seed_triple_columns(0, 8)
    if not verify_triple_pairwise_mu(cols):
        raise ValueError("MUB triple pairwise mutual unbiasedness failed")
    return True

