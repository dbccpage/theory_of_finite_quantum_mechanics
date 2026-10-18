
pub struct FunctionalLayerBoundary;

pub mod aggregation;
pub mod binary_degree;
pub mod born_probabilities;
pub mod circle_piecewise_linear;
pub mod decoherence;
pub mod distinguishability;
pub mod dual_verification;
pub mod factory;
pub mod finite_family_bound;
pub mod gamma2;
pub mod gamma_reconciliation;
pub mod l1_seminorm;
pub mod loss_curvature;
pub mod mub_feasibility_wall;
pub mod normal_projection;
pub mod norms;
pub mod observer_gauge;
pub mod operator_trace_closure;
pub mod path_error;
pub mod phi1;
pub mod phi2;
pub mod phi3;
pub mod phi4;
pub mod product_distance;
pub mod protected_linear_quotient;
pub mod projection_leakage;
pub mod projection_transfer;
pub mod quantum_gaps;
pub mod residual;
pub mod residual_splitting;
pub mod simplicial_defect;
pub mod trace_diagnostics;
pub mod transport_amplitude;
pub mod weighted_l1_norm;
mod wire;
pub mod xi;

pub use gamma2::{ExactGamma2Result, Gamma2Functional};
pub use mub_feasibility_wall::{
    MubFeasibilityWallDiagnosticIntervalAttempt, MubFeasibilityWallEvidenceKind,
    MubFeasibilityWallFunctional, MubFeasibilityWallScalarIntervalAttempt,
    MubFeasibilityWallTargetComparison, MubFeasibilityWallValue,
};
pub use phi1::{ExactPhi1Certificate, Phi1Functional, VerifiedExactPhi1};
pub use phi2::{ExactPhi2Certificate, Phi2Functional, VerifiedExactPhi2};
pub use phi3::{ExactPhi3Certificate, Phi3Functional, VerifiedExactPhi3};
pub use phi4::{ExactPhi4Certificate, Phi4Functional, VerifiedExactPhi4};
pub use xi::{DensityLift, XiFunctional, XiResult};
