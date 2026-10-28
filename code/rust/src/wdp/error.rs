
use linear_algebra::linear_algebra::image_kernel::ExactLinearAlgebraError;
use tfqm_finite_probability::error::ClassicalShadowError;
use tfqm_functional::gamma2::ExactGamma2Error;
use tfqm_functional::l1_seminorm::L1SeminormError;
use tfqm_holonomy::HolonomyError;
use omega_homology::errors::HomologicalError;
use omega_homology::finite_directed_graph::NamedEdgeResolutionError;
use omega_policy::trichotomy::TrichotomyRefusal;
use omega_quantum_physics::exact_channel::ExactChannelError;
use omega_quantum_physics::exact_hermitian::ExactHermitianError;
use omega_quantum_physics::finite_chsh_correlations::CorrelationError;
use omega_solvers::solver_lp_phi1_quotient::Phi1SolveError;
use thiserror::Error;

use crate::empirical_adapter::AdapterRefusal;

impl From<tfqm_local_green_global_red_lggr::matrix_path_kernel::MatrixPathError> for WdpError {
    fn from(error: tfqm_local_green_global_red_lggr::matrix_path_kernel::MatrixPathError) -> Self {
        use tfqm_local_green_global_red_lggr::matrix_path_kernel::MatrixPathError;
        match error {
            MatrixPathError::InvalidInput { detail } => Self::InvalidInput { detail },
            MatrixPathError::GraphCarrier(error) => Self::GraphCarrier(error),
            MatrixPathError::Holonomy(error) => Self::Holonomy(error),
        }
    }
}

#[derive(Debug, Clone, PartialEq, Eq, Error)]
pub enum WdpError {
    #[error("Invalid input: {detail}")]
    InvalidInput { detail: String },

    #[error("Missing adapter: {detail}")]
    MissingAdapter { detail: String },

    #[error("Adapter mismatch: expected {expected}, found {found}")]
    AdapterMismatch { expected: String, found: String },

    #[error("Carrier element not found: {element}")]
    ElementNotFound { element: String },

    #[error("Sieve does not cover carrier: missing {missing:?}")]
    IncompleteCoverage { missing: Vec<String> },

    #[error(
        "Section domain mismatch for context {context}: expected {expected:?}, found {found:?}"
    )]
    SectionDomainMismatch {
        context: String,
        expected: Vec<String>,
        found: Vec<String>,
    },

    #[error("Graph carrier refusal: {0}")]
    GraphCarrier(#[from] NamedEdgeResolutionError),

    #[error("Finite relation refusal: {0:?}")]
    FiniteRelation(#[from] tfqm_category_theory::finite_relational::RelationalError),

    #[error("Homology refusal: {0}")]
    Homology(#[from] HomologicalError),

    #[error("Holonomy refusal: {0}")]
    Holonomy(#[from] HolonomyError),

    #[error("Linear algebra refusal: {0}")]
    LinearAlgebra(#[from] ExactLinearAlgebraError),

    #[error("L1 presentation refusal: {0}")]
    L1Presentation(#[from] L1SeminormError),

    #[error("Phi1 refusal: {0}")]
    Phi1(#[from] Phi1SolveError),

    #[error("Gamma2 refusal: {0}")]
    Gamma2(#[from] ExactGamma2Error),

    #[error("Trichotomy refusal: {0:?}")]
    Trichotomy(TrichotomyRefusal),

    #[error("Empirical adapter refusal: {0}")]
    Adapter(#[source] Box<AdapterRefusal>),

    #[error("Exact matrix algebra refusal: {0}")]
    ExactField(#[from] linear_algebra::exact_field::ExactFieldError),

    #[error("Matrix storage refusal: {0}")]
    MatrixStorage(#[from] linear_algebra::backend::basic_matrix::MatrixError),

    #[error("Exact channel refusal: {0}")]
    ExactChannel(#[from] ExactChannelError),

    #[error("Exact Hermitian refusal: {0}")]
    ExactHermitian(#[from] ExactHermitianError),

    #[error("CHSH correlation refusal: {0}")]
    Correlation(#[from] CorrelationError),

    #[error("Classical shadow refusal: {0:?}")]
    ClassicalShadow(ClassicalShadowError),

    #[error("Claim status firewall violation: {detail}")]
    ClaimStatusFirewall { detail: String },

    #[error("Awareness firewall violation: attempting to assert phenomenal consciousness")]
    AwarenessFirewallViolation,

    #[error("Authority effect firewall violation: authority effect must be None")]
    AuthorityEffectViolation,
}

impl From<ClassicalShadowError> for WdpError {
    fn from(refusal: ClassicalShadowError) -> Self {
        WdpError::ClassicalShadow(refusal)
    }
}

impl From<AdapterRefusal> for WdpError {
    fn from(refusal: AdapterRefusal) -> Self {
        match refusal {
            AdapterRefusal::InvalidInput { detail } => WdpError::InvalidInput { detail },
            AdapterRefusal::Wdp(error) => *error,
            other => WdpError::Adapter(Box::new(other)),
        }
    }
}
