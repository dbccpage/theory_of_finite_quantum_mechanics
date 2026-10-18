
extern crate self as omega_operad_theory;
pub mod kernel;
pub mod foundation;
pub mod realization;
pub mod deformation;
pub mod geometric;
pub mod applications;

#[cfg(feature = "python")]
pub mod python;

pub use foundation::{
    MonoidalOperad, OpenLeaf, OperadColour, OperadSignature, OperadVariant,
    Operation, OperationId, OperationKind, OperationKindType,
    PlanarColoredOperad, PlanarTree, SpanOperand, SymmetricColoredOperad, TreeChild,
    ADMITTED_FINITE_COLOURS,
};

pub use realization::{
    AlgebraModule, ComputationStatus, EvaluationOutcome, EvaluationReceipt,
    EvidenceKind, LawResult, OperadAlgebra, OperadicModule, PolicyDecisionRef,
    StructuralAssociativityWitness,
};

pub use deformation::{
    BarCobarResolution, ColouredCooperad, KoszulDualBuilder, ProposedQuadraticDual,
    QuadraticOperad, QuadraticRelation,
};

pub use geometric::{
    LittleDisksConfiguration, RectilinearDisk,
    build_associative_homology_operad, build_commutative_homology_operad, build_gerstenhaber_homology_operad,
};

pub use applications::{AgentCapabilitySlice, OEASWorkflowOperad, OEAS_ADMITTED_PORT_COLOURS};

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

pub fn authority_effect() -> &'static str {
    "None"
}
