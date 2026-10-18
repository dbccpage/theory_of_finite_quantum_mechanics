"""OESOS: Omega Engine Solver of Solvers — object set (not Engine).

AuthorityEffect: None. Solver outputs EvidenceOnly.
Math residual geometry is delegated to homology/functional/residuals.
Public exact obstruction kernel: evaluate_obstruction (Gate 11).
"""

from .cascade import OesosCascade
from .problem import ObstructionProblem
try:
    from .solv_queue import ResidualQueue
except ImportError:
    from .queue import ResidualQueue

from .receipt import CascadeReceipt, StageRecord
from .registry import SolverRegistry
from .stage import CascadeStage, StageKind
from .obstruction_evaluator import (
    ObstructionClass,
    ObstructionReceipt,
    evaluate_obstruction,
    solve_obstruction,
)
from .network_to_obstruction import (
    classify_network_residual,
    network_to_finite_complex,
    obstruction_class_to_terminal_status,
    residual_to_omega,
)
try:
    from .solv_exact_dual_pricing import (
        ExactDualPricingError,
        ExactDualPricingReceipt,
        price_exact_degree_k,
        price_network_phi1_exact,
        price_degree_k_with_optional_nilpotency,
        refuse_float_as_exact,
        refuse_ls_as_canonical,
    )
except ImportError:
    from omega_engine.crates.solver.solv_omega_engine_solver_of_solvers.solv_exact_dual_pricing import (
        ExactDualPricingError,
        ExactDualPricingReceipt,
        price_exact_degree_k,
        price_network_phi1_exact,
        price_degree_k_with_optional_nilpotency,
        refuse_float_as_exact,
        refuse_ls_as_canonical,
    )

__all__ = [
    "OesosCascade",
    "ObstructionProblem",
    "ResidualQueue",
    "CascadeReceipt",
    "StageRecord",
    "SolverRegistry",
    "CascadeStage",
    "StageKind",
    "ObstructionClass",
    "ObstructionReceipt",
    "evaluate_obstruction",
    "solve_obstruction",
    "classify_network_residual",
    "network_to_finite_complex",
    "obstruction_class_to_terminal_status",
    "residual_to_omega",
    "ExactDualPricingError",
    "ExactDualPricingReceipt",
    "price_exact_degree_k",
    "price_network_phi1_exact",
    "price_degree_k_with_optional_nilpotency",
    "refuse_float_as_exact",
    "refuse_ls_as_canonical",
]
