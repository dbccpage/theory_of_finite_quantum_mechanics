"""
ANSI SQL Domain Kernel Re-export Shim
AuthorityEffect: None
"""

try:
    from .domain_ansi_sql_kernel import (
        BareissDeterminantReceipt,
        DomainEngine,
        DomainState,
        FermionGINReceipt,
        PrimitiveDifferenceSetting,
        RedhefferBenchmarkReceipt,
        SimplicialBoundaryReceipt,
        build_redheffer_matrix,
        compute_mertens,
        compute_mobius,
    )
except (ImportError, ValueError):
    from domain_ansi_sql_kernel import (
        BareissDeterminantReceipt,
        DomainEngine,
        DomainState,
        FermionGINReceipt,
        PrimitiveDifferenceSetting,
        RedhefferBenchmarkReceipt,
        SimplicialBoundaryReceipt,
        build_redheffer_matrix,
        compute_mertens,
        compute_mobius,
    )

__all__ = [
    "BareissDeterminantReceipt",
    "DomainEngine",
    "DomainState",
    "FermionGINReceipt",
    "PrimitiveDifferenceSetting",
    "RedhefferBenchmarkReceipt",
    "SimplicialBoundaryReceipt",
    "build_redheffer_matrix",
    "compute_mertens",
    "compute_mobius",
]
