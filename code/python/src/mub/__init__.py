"""Python dual-implementation for Mutually Unbiased Bases (MUB).

AuthorityEffect: None.
Dual-home with code/rust/src/mub (crate tfqm_mub).
"""

from __future__ import annotations

import sys
from fractions import Fraction
from typing import Any, Dict

# Re-exports from flattened modules
from .cyclotomic import (
    Cyc24,
    SqrtBox,
    cyc24_interval_enclosure,
    sqrt_rational_interval,
)
from .interval import (
    BasisBox,
    RationalInterval,
    VectorBox,
    box_volume,
    boxes_overlap_interior,
)
from .masses import (
    EnclosedTriple,
    EnclosedVector,
)
from .mub_triples import (
    D,
    standard_basis_b1,
    verify_triple_pairwise_mu,
)
from .cover import (
    CertifiedBox,
    CoverReport,
    box_touches_torus,
    cover_region,
    verify_full_coverage,
)
from .verifier import (
    FullCoverageSummary,
    IndependentMubVerifier,
    SampledBoxResult,
    StratifiedVerificationSummary,
)

from . import mub_verify
from . import conj2_symbolic_verification

_self = sys.modules[__name__]
sys.modules.setdefault("mub_verify", mub_verify)
sys.modules.setdefault("src.mub.mub_verify", mub_verify)
sys.modules.setdefault("conj2_symbolic_verification", conj2_symbolic_verification)
sys.modules.setdefault("src.mub.conj2_symbolic_verification", conj2_symbolic_verification)

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
    from .mub_triples import dita_seed_triple_columns, verify_triple_pairwise_mu
    cols = dita_seed_triple_columns(0, 8)
    if not verify_triple_pairwise_mu(cols):
        raise ValueError("MUB triple pairwise mutual unbiasedness failed")
    return True
