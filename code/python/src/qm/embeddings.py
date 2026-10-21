"""Block 03 compatibility entrypoint for central embedding calculations."""

from fractions import Fraction

from .busch_effects import sign_variations
from .embedding_relativity import (
    CONDUCTOR_MINIMAL_POLYNOMIALS,
    CyclotomicElement,
    ExactHermitianMatrix,
    FieldElementFPlus,
    IsolatingInterval,
    RationalPoly,
    RealEmbedding,
    TargetEmbeddingAudit,
    compute_real_embeddings,
    construct_conductor_5_witness,
    construct_conductor_8_witness,
    count_roots_in_interval,
    isolate_all_real_roots,
    run_target_census,
    sturm_sequence,
    verify_all_block_03_invariants,
)

__all__ = [
    "CONDUCTOR_MINIMAL_POLYNOMIALS", "CyclotomicElement", "ExactHermitianMatrix",
    "FieldElementFPlus", "IsolatingInterval", "RationalPoly", "RealEmbedding",
    "TargetEmbeddingAudit", "compute_real_embeddings", "construct_conductor_5_witness",
    "construct_conductor_8_witness", "count_roots_in_interval", "isolate_all_real_roots",
    "run_target_census", "sign_variations", "sturm_sequence", "verify_all_block_03_invariants",
]

def conductor_quadratic_value() -> Fraction:
    """Horner value of the conductor-5 polynomial x^2 + x - 1 at the rational point 1."""
    polynomial = CONDUCTOR_MINIMAL_POLYNOMIALS[5]
    value = polynomial.eval(1)
    if value != Fraction(1):
        raise ValueError(f"conductor-5 polynomial at 1 is {value}, not 1")
    return value


if __name__ == "__main__":
    verify_all_block_03_invariants()
    print("c250_b03_embeddings execution verified successfully.")
