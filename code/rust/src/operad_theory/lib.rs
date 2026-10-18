//! Omega Operad Theory: 5-Tier Coloured Operad Architecture in Rust.
//!
//! Five-tier mathematical hierarchy:
//!   1. Foundation: Colours, Signatures, Operations, Planar & Symmetric Coloured Operads, Monoidal Operads, Planar Trees
//!   2. Realization: Multi-Sorted Algebras, Operadic Modules, Associativity Witnesses
//!   3. Deformation: Quadratic Operads, Cooperads, Bar-Cobar Resolutions, Koszul Duality
//!   4. Geometric: Little n-Disks Operad D_n, Homology Operads H_*(D_n)
//!   5. Applications: OEAS Applied Workflow Operad & Agent Interpreters
//!
//! AuthorityEffect: None.

extern crate self as omega_operad_theory;
pub mod kernel;
pub mod foundation;
pub mod realization;
pub mod deformation;
pub mod geometric;
pub mod applications;

#[cfg(feature = "python")]
pub mod python;

// Tier 1 Re-exports
pub use foundation::{
    MonoidalOperad, OpenLeaf, OperadColour, OperadSignature, OperadVariant,
    Operation, OperationId, OperationKind, OperationKindType,
    PlanarColoredOperad, PlanarTree, SpanOperand, SymmetricColoredOperad, TreeChild,
    ADMITTED_FINITE_COLOURS,
};

// Tier 2 Re-exports
pub use realization::{
    AlgebraModule, ComputationStatus, EvaluationOutcome, EvaluationReceipt,
    EvidenceKind, LawResult, OperadAlgebra, OperadicModule, PolicyDecisionRef,
    StructuralAssociativityWitness,
};

// Tier 3 Re-exports
pub use deformation::{
    BarCobarResolution, ColouredCooperad, KoszulDualBuilder, ProposedQuadraticDual,
    QuadraticOperad, QuadraticRelation,
};

// Tier 4 Re-exports
pub use geometric::{
    LittleDisksConfiguration, RectilinearDisk,
    build_associative_homology_operad, build_commutative_homology_operad, build_gerstenhaber_homology_operad,
};

// Tier 5 Re-exports
pub use applications::{AgentCapabilitySlice, OEASWorkflowOperad, OEAS_ADMITTED_PORT_COLOURS};

// Estate kernel re-exports (digest-bearing; see `kernel` module docs).
pub use kernel::{
    canonical_bytes, canonical_id, ActionLicense, AgentLicense, AtomicPath2, Attestation,
    AttestationKind, AuthorityEffect, BoundarySignature, BudgetTransition, CertifiedPair,
    ColourSpec, ComparisonEvidence, ComparisonVerdict, EquivalenceGrade, ExecutionEvent,
    ExecutionEventInput, HorizontalPath2, IdentityPath2, InversePath2, InvocationGrade,
    KernelError, LicensedTerm, NormalizedTerm, ObligationBundle, ObligationKind, ObserverDeclaration,
    OperandRef, OperationSpec, OperationSpecInput, OperationTerm, Path2, PortSpec, ProofObligation,
    AgentFibrationError, AgentPath, AgentPathWitness, AntibodyScreen, Homotopy2Cell, transport,
    Refinement, Refusal, ReplayVerifiedAttestation, VerticalPath2, WhiskerPath2,
};

/// Always `"None"` — this crate mints zero authority.
pub fn authority_effect() -> &'static str {
    "None"
}
