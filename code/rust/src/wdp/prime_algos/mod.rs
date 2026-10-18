//! Omega Engine Algorithm Prime Triad and Descent Engine.
//!
//! Owns:
//! - Prime -1: Candidate proposal and untrusted intake ([`prime_candidate`]).
//! - Prime 000: Binding twelve-step obstruction packet fill order, admission, and conformance ([`prime_algorithm_0`], [`prime_algorithm_0_admission`], [`prime_algorithm_0_conformance`]).
//! - Prime 001: Inter-carrier transport soundness and sealed loss ledgers ([`prime_algorithm_1`]).
//! - Prime 002: Continuation predicate `CanContinue_n`, six anti-cheat halting laws, and terminalizer ([`prime_algorithm_2`]).
//! - Scope commitments & sealed evidence ([`prime_scope`]).
//! - Nine Up-Lift Gate ([`licensed_lift_gate`]).
//! - Domain Adapters & Rosetta cross-domain stats ([`domain_adapters`], [`rosetta`]).
//! - Descent Engine: Sovereign coordinator wiring Prime Triad to [`crate::coda`] and [`crate::solver_of_solvers`] ([`descent_engine`]).
//!
//! AuthorityEffect: strictly None throughout. All mathematical decisions are exact rational (`BigRational`).

/// Finite mathematical lift/guard/terminal profile, not the full Prime 002 gate.
pub mod finite_routing;
pub mod descent_engine;
pub mod domain_adapters;
pub mod licensed_lift_gate;
pub mod prime_algorithm_0;
pub mod prime_algorithm_0_admission;
pub mod prime_algorithm_0_conformance;
pub mod prime_algorithm_1;
pub mod prime_algorithm_2;
pub mod prime_candidate;
pub mod prime_scope;
pub mod rosetta;

// Backward-compatibility aliases
pub use prime_algorithm_0 as oeprmalg0;
pub use prime_algorithm_0_admission as oeprmalg0_admission;
pub use prime_algorithm_0_conformance as oeprmalg0_conformance;
pub use prime_algorithm_1 as oeprmalg1;
pub use prime_algorithm_2 as oeprmalg2;

// Convenient re-exports
pub use descent_engine::{DescentExecutionReceipt, DescentRefusal, PrimeDescentCoordinator};
pub use licensed_lift_gate::{LicensedLiftAdmission, NineUpLiftBits, PaperEr003LiftCertificate};
pub use prime_algorithm_0::{
    run_admitted, run_oeprmalg0, run_prime_algorithm_0, DomainAdapter, Oeprmalg0Receipt,
    PrimeAlgorithm0Receipt, PrimeDomain,
};
pub use prime_algorithm_1::{
    transport, LossLedger, TransportRefusal, TransportStatus, TransportedPacket,
};
pub use prime_algorithm_2::{
    can_continue_n, terminalize, write_step, AntiCheatLaw, Budget, ContinuationEvidence,
    ControlState, Gamma2Zero, LawRefusal, OpenControlState, StepClaim, StepOp, StepPermit,
    TerminalControlState, TerminalPermit, TerminalRefusal,
};
pub use prime_candidate::{CandidateProposalV1, PrimeStage, PrimeStageRecordV1, PrimeTraceLogger};
pub use prime_scope::{BoundCarrierManifest, CallerAttested, ScopeBinding};
