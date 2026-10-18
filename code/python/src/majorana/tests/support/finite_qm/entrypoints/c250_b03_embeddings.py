"""Block 03 compatibility entrypoint for central embedding calculations."""

from omega_engine_projects.ms_majorana.code.tests.support.finite_qm.use_cases.embedding_relativity import CONDUCTOR_MINIMAL_POLYNOMIALS, CyclotomicElement, ExactHermitianMatrix, FieldElementFPlus, IsolatingInterval, RationalPoly, RealEmbedding, TargetEmbeddingAudit, compute_real_embeddings, construct_conductor_5_witness, construct_conductor_8_witness, count_roots_in_interval, isolate_all_real_roots, run_target_census, sign_variations, sturm_sequence, verify_all_block_03_invariants

__all__ = [
    "CONDUCTOR_MINIMAL_POLYNOMIALS", "CyclotomicElement", "ExactHermitianMatrix",
    "FieldElementFPlus", "IsolatingInterval", "RationalPoly", "RealEmbedding",
    "TargetEmbeddingAudit", "compute_real_embeddings", "construct_conductor_5_witness",
    "construct_conductor_8_witness", "count_roots_in_interval", "isolate_all_real_roots",
    "run_target_census", "sign_variations", "sturm_sequence", "verify_all_block_03_invariants",
]

if __name__ == "__main__":
    verify_all_block_03_invariants()
    print("c250_b03_embeddings execution verified successfully.")
