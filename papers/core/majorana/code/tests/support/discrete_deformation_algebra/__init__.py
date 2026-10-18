"""Discrete Deformation Calculus (DDC) and Algorithm Prime package.

AuthorityEffect: None throughout.
Path: ``008_engine_runtime/_demos/omega_discreate_deformation_algebra/``
"""

from omega_engine.crates.homology_theory.finite_cochain_complex import (
    COEFFICIENT_DOMAIN,
    FiniteCochainComplex,
    Matrix,
    Scalar,
    Vector,
    coerce_vector,
)
from omega_engine.crates.type.runtime_axes import (
    DiagnosticClass,
    RoutingTerminal,
    ExtensionStatus,
    AuthorityStatus,
    DdaLetter,
    DdaStepReceipt,
    CohomologicalStatus,
)

from .axis_adapter import (
    AliasAdapterRefusal,
    SUPPORTED_AXES,
    alias_table,
    known_axes_for,
    resolve_alias,
)
from .dda import DdaTraceEngine
from .dda_engine import (
    DDAEngine,
    TerminationStatus,
    FoundationCert,
    DDAStepCert,
    WindowLiftCert,
    TerminationCert,
)
from .dda_cascade_router import DdaCascadeRouter
from .dda_trace_recorder import DDATraceRecorder, get_global_trace_recorder, DDAOperationRecord




from .cochain import CoboundaryComplex, square_zero_check, residual_verdict

try:
    from omega_engine_governance.contracts import (
        ProposalEnvelope,
        FidelityPacket,
        ObstructionDescentPacket,
        CochainComplexData,
        assert_packet_type_separation,
    )
except Exception:
    ProposalEnvelope = None
    FidelityPacket = None
    ObstructionDescentPacket = None
    CochainComplexData = None
    assert_packet_type_separation = None


from .pfp import PfpFrontendEngine, false_green_blocked
from .lce import LceEngine, ContextExtensionRequest, LicensedContextExtension
from .round9 import (
    DiagnosticFamily,
    SourceLocus,
    DiagnosticResidualPacket,
    validate_diagnostic_packet,
    LossLedger,
    LossEntry,
    LossMonotonicityViolationError,
    GlobalRunEnvelope,
    ReentryReceipt,
    execute_coda_reentry,
    ReentryLaunderingError,
)
from .receipt_emission import (
    GtlaReceiptEmission,
    ReceiptEmissionRefusal,
    adapter_declaration,
    derive_step_axes,
    emit_gtla_receipt,
)
from .tower_boundary import (
    GtocCut,
    ImportLedger,
    ImportLedgerEntry,
    GtfocTerminalClass,
    GtfdaDescentPacket,
    validate_gtfda_authority,
    validate_prime000_declaration_order,
    validate_gtfoc_exact_repair_isolation,
    classify_gtfoc_trichotomy,
    validate_gtla_summary_compression,
    validate_gtla_summary_compression_multiset,
    validate_gtmur_target_authority,
    validate_gtta_terminal_disjointness,
)


__version__ = "0.2.0"
__all__ = [
    "COEFFICIENT_DOMAIN",
    "FiniteCochainComplex",
    "Matrix",
    "Scalar",
    "Vector",
    "coerce_vector",
    "DiagnosticClass",
    "RoutingTerminal",
    "ExtensionStatus",
    "AuthorityStatus",
    "DdaLetter",
    "DdaStepReceipt",
    "CohomologicalStatus",
    "AliasAdapterRefusal",
    "SUPPORTED_AXES",
    "alias_table",
    "known_axes_for",
    "resolve_alias",
    "DdaTraceEngine",
    "DDAEngine",
    "DdaCascadeRouter",
    "CascadeSolver",
    "SolverCascadeReceipt",
    "DDATraceRecorder",
    "get_global_trace_recorder",
    "DDAOperationRecord",
    "CoboundaryComplex",




    "square_zero_check",
    "residual_verdict",
    "ProposalEnvelope",
    "FidelityPacket",
    "ObstructionDescentPacket",
    "CochainComplexData",
    "PfpFrontendEngine",
    "false_green_blocked",
    "LceEngine",
    "ContextExtensionRequest",
    "LicensedContextExtension",
    "DiagnosticFamily",
    "SourceLocus",
    "DiagnosticResidualPacket",
    "validate_diagnostic_packet",
    "LossLedger",
    "LossEntry",
    "LossMonotonicityViolationError",
    "GlobalRunEnvelope",
    "ReentryReceipt",
    "execute_coda_reentry",
    "ReentryLaunderingError",
    "GtlaReceiptEmission",
    "ReceiptEmissionRefusal",
    "adapter_declaration",
    "derive_step_axes",
    "emit_gtla_receipt",
    "GtocCut",
    "ImportLedger",
    "ImportLedgerEntry",
    "GtfocTerminalClass",
    "GtfdaDescentPacket",
    "validate_gtfda_authority",
    "validate_prime000_declaration_order",
    "validate_gtfoc_exact_repair_isolation",
    "classify_gtfoc_trichotomy",
    "validate_gtla_summary_compression",
    "validate_gtla_summary_compression_multiset",
    "validate_gtmur_target_authority",
    "validate_gtta_terminal_disjointness",
]


def __getattr__(name: str):
    if name in ("CascadeSolver", "SolverCascadeReceipt"):
        from omega_engine.crates.solver.solv_omega_engine_solver_of_solvers.solv_oesos import (
            CascadeSolver,
            SolverCascadeReceipt,
        )
        if name == "CascadeSolver":
            return CascadeSolver
        return SolverCascadeReceipt
    raise AttributeError(f"module {__name__!r} has no attribute {name!r}")




