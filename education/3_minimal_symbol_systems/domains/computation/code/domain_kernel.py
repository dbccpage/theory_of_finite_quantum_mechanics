"""
Domain Kernel Re-export Shim
AuthorityEffect: None
"""

try:
    from .domain_computation_kernel import (
        DomainEngine,
        DomainState,
        FuelExecutionReceipt,
        FuelStatus,
        HaltingObstruction,
        PrimitiveDifferenceSetting,
        SimplicialBoundaryReceipt,
        TuringConfiguration,
        TuringStepReceipt,
    )
except (ImportError, ValueError):
    from domain_computation_kernel import (
        DomainEngine,
        DomainState,
        FuelExecutionReceipt,
        FuelStatus,
        HaltingObstruction,
        PrimitiveDifferenceSetting,
        SimplicialBoundaryReceipt,
        TuringConfiguration,
        TuringStepReceipt,
    )

__all__ = [
    "FuelExecutionReceipt",
    "FuelStatus",
    "HaltingObstruction",
    "PrimitiveDifferenceSetting",
    "SimplicialBoundaryReceipt",
    "TuringConfiguration",
    "TuringStepReceipt",
    "DomainState",
    "DomainEngine",
]
