"""Lambda Operators crate (all modules use lamb_ prefix)."""

from omega_engine.crates.operator.lambda_op.lamb_bitwise import BitwiseOperations
from omega_engine.crates.operator.lambda_op.lamb_cycle_correction import apply_correction
from omega_engine.crates.operator.lambda_op.lamb_affine_feasibility import project_onto_affine
from omega_engine.crates.operator.lambda_op.lamb_chain_obstruction import compute_po_015_projection_obstruction
from omega_engine.crates.operator.lambda_op.lamb_qm_cycle_space import compute_harmonic_basis
from omega_engine.crates.operator.lambda_op.lamb_fixpoint import FixpointConverge, fixpoint_bounded_recursion
from omega_engine.crates.operator.lambda_op.lamb_network_simplex_basis import Basis

try:
    from omega_engine.crates.operator.lambda_op.lamb_obstruction_candidates import (
        BestScoreSelector,
        CandidateSelector,
        select_best_accepted,
    )
except Exception:
    BestScoreSelector = None
    CandidateSelector = None
    select_best_accepted = None

__all__ = [
    "BitwiseOperations",
    "apply_correction",
    "project_onto_affine",
    "compute_po_015_projection_obstruction",
    "compute_harmonic_basis",
    "FixpointConverge",
    "fixpoint_bounded_recursion",
    "Basis",
    "BestScoreSelector",
    "CandidateSelector",
    "select_best_accepted",
]
