use crate::linear_algebra::scalars::{q, Semiring};
use crate::linear_algebra::{ExactFieldError, ExactMatrix, GaussianRational, MatrixError, Q};
use serde::{Deserialize, Serialize};
use thiserror::Error;

#[derive(Debug, Clone, PartialEq, Eq, Error)]
pub enum QmError {
    #[error("Dimension mismatch: {0}")]
    DimensionMismatch(String),
    #[error("scalar arithmetic: {0}")]
    Scalar(#[from] crate::linear_algebra::scalars::ScalarError),
    #[error("Matrix error: {0}")]
    Matrix(#[from] MatrixError),
    #[error("exact field error: {0}")]
    ExactField(#[from] ExactFieldError),
    #[error("State normalization violation: trace is not 1")]
    NormalizationViolation,
    #[error("Hermiticity violation: operator is not self-adjoint")]
    HermiticityViolation,
}

#[derive(Debug, Clone, PartialEq, Eq, Serialize, Deserialize)]
pub struct DensityOperator {
    dim: usize,
    matrix: ExactMatrix<GaussianRational>,
}

impl DensityOperator {
    pub fn new(matrix: ExactMatrix<GaussianRational>) -> Result<Self, QmError> {
        let (rows, cols) = matrix.shape();
        if rows != cols {
            return Err(QmError::DimensionMismatch(format!(
                "Density operator must be square, got {}x{}",
                rows, cols
            )));
        }
        if !matrix.is_hermitian()? {
            return Err(QmError::HermiticityViolation);
        }
        let mut tr_real = q(0);
        let mut tr_imag = q(0);
        for i in 0..rows {
            let elem = matrix.get(i, i)?;
            tr_real = tr_real + elem.real();
            tr_imag = tr_imag + elem.imag();
        }
        if tr_real != q(1) || tr_imag != q(0) {
            return Err(QmError::NormalizationViolation);
        }
        Ok(Self { dim: rows, matrix })
    }

    pub fn dimension(&self) -> usize {
        self.dim
    }

    pub fn matrix(&self) -> &ExactMatrix<GaussianRational> {
        &self.matrix
    }

    pub fn expectation(
        &self,
        observable: &ExactMatrix<GaussianRational>,
    ) -> Result<GaussianRational, QmError> {
        if observable.shape() != (self.dim, self.dim) {
            return Err(QmError::DimensionMismatch(format!(
                "Shape mismatch {:?} vs {}",
                observable.shape(),
                self.dim
            )));
        }
        let prod = self.matrix.mul(observable)?;
        let mut tr = GaussianRational::zero();
        for i in 0..self.dim {
            let elem = prod.get(i, i)?;
            tr = tr.try_add(elem)?;
        }
        Ok(tr)
    }

    pub fn purity(&self) -> Result<Q, QmError> {
        let sq = self.matrix.mul(&self.matrix)?;
        let mut tr = q(0);
        for i in 0..self.dim {
            let elem = sq.get(i, i)?;
            tr = tr + elem.real();
        }
        Ok(tr)
    }
}

pub mod born_effect_valuation;
pub mod born_hermitian_valuation;
pub mod campaigns;
pub mod causal_prices;
pub mod discrete_time_stone;
pub mod domain;
pub mod entropy_bounds;
pub mod entropy_solver;
pub mod entrypoints;
pub mod evidence_routes;
pub mod exact_token;
pub mod finite_spinfoam;
pub mod finite_wigner;
pub mod finite_witness;
pub mod group_param;
pub mod hilbert_lift_completion;
pub mod inner_product_uniqueness;
pub mod legacy_suites;
pub mod observer_functor;
pub mod obstruction_calc;
pub mod packet_protocol;
pub mod quantum_packet;
pub mod report_fiber;
pub mod simplicial_grav;
pub mod suites;
pub mod textbook_problems;
pub mod tower_walk;
pub mod u1_phase_completion;

#[derive(Clone, Debug, PartialEq, Eq, Serialize, Deserialize)]
pub struct FiniteQmSuiteReport {
    pub d3_mub_exhaustive: bool,
    pub d3_tomography_ground_state_verified: bool,
    pub d3_tomography_magic_state_verified: bool,
    pub d3_tomography_mixed_state_verified: bool,
    pub d4_mub_exhaustive: bool,
    pub d4_tomography_bell_state_verified: bool,
    pub clifton_kent_all_1024_non_psd_certified: bool,
    pub d5_wigner_algebra_verified: bool,
    pub d5_magic_state_negativity_witnessed: bool,
    pub d5_magic_point_value: omega_number_theory::rational::Rational,
    pub commutator_trace_obstruction_verified: bool,
}

fn verify_mub_exhaustive<
    C: omega_number_theory::scalar::RationalEmbedding
        + ::linear_algebra::exact_field::involution::Involution,
>(
    mub: &omega_quantum_physics::mub::MubSystem<C>,
) -> bool {
    mub.verify_hermiticity()
        && mub.verify_idempotence()
        && mub.verify_rank_one_trace()
        && mub.verify_same_basis_orthogonality()
        && mub.verify_resolution_of_identity()
        && mub.verify_cross_basis_unbiasedness()
}

fn verify_wigner_d5_suite() -> (bool, bool, omega_number_theory::rational::Rational) {
    use omega_number_theory::rational::rq;
    use omega_quantum_physics::wigner;
    let wsys5 = wigner::DiscreteWignerSystemD5::new();
    let d5_wigner_algebra_verified = wsys5.verify_hermiticity()
        && wsys5.verify_unit_trace()
        && wsys5.verify_orthogonality()
        && wsys5.verify_resolution()
        && wsys5.verify_gross_covariance();
    let rho_m5 = wigner::state_magic_d5();
    let w5_grid = wsys5
        .evaluate_exact(&rho_m5)
        .expect("declared exact Wigner fixture");
    let d5_magic_point_value =
        omega_number_theory::cyclotomic_field::CyclotomicNumber::from(&w5_grid[0][0])
            .as_rational()
            .expect("declared magic Wigner origin is rational");
    let d5_magic_state_negativity_witnessed = d5_magic_point_value == rq(-1, 5);
    (
        d5_wigner_algebra_verified,
        d5_magic_state_negativity_witnessed,
        d5_magic_point_value,
    )
}

fn verify_commutator_d3_suite() -> bool {
    let comm_report = omega_quantum_physics::commutator::audit_commutator_obstruction_d3()
        .expect("the declared dimension-three commutator fixture is admitted");
    comm_report.commutator_trace_is_zero
        && comm_report.hypothetical_ccr_trace_non_zero
        && comm_report.weyl_relation_satisfied
        && comm_report.weyl_commutator_trace_is_zero
}

pub fn run_finite_qm_verification_suite() -> FiniteQmSuiteReport {
    use omega_quantum_physics::{mub, tomography};

    let mub3 = mub::MubSystem::mub_d3();
    let d3_mub_exhaustive = verify_mub_exhaustive(&mub3);

    let tomographer = tomography::ExactStateTomographerSystem::new(mub::MubSystem::mub_d3());
    let d3_tomography_ground_state_verified =
        tomographer.verify_exact_reconstruction(&tomography::state_ground_d3());
    let d3_tomography_magic_state_verified =
        tomographer.verify_exact_reconstruction(&tomography::state_magic_d3());
    let d3_tomography_mixed_state_verified =
        tomographer.verify_exact_reconstruction(&tomography::state_mixed_rational_d3());

    let mub4 = mub::MubSystem::mub_d4();
    let d4_mub_exhaustive = verify_mub_exhaustive(&mub4);

    let tomographer_d4 = tomography::ExactStateTomographerSystem::new(mub::MubSystem::mub_d4());
    let d4_tomography_bell_state_verified =
        tomographer_d4.verify_exact_reconstruction(&tomography::state_bell_d4());

    let ck_receipt =
        crate::qm::campaigns::mub_reports::evaluate_all_1024_clifton_kent_valuations(&mub4)
            .expect("declared d4 MUB receipt fixture");
    let clifton_kent_all_1024_non_psd_certified = ck_receipt.contextuality_persists_unconditionally;

    let (d5_wigner_algebra_verified, d5_magic_state_negativity_witnessed, d5_magic_point_value) =
        verify_wigner_d5_suite();

    let commutator_trace_obstruction_verified = verify_commutator_d3_suite();

    FiniteQmSuiteReport {
        d3_mub_exhaustive,
        d3_tomography_ground_state_verified,
        d3_tomography_magic_state_verified,
        d3_tomography_mixed_state_verified,
        d4_mub_exhaustive,
        d4_tomography_bell_state_verified,
        clifton_kent_all_1024_non_psd_certified,
        d5_wigner_algebra_verified,
        d5_magic_state_negativity_witnessed,
        d5_magic_point_value,
        commutator_trace_obstruction_verified,
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_qubit_pure_state_and_pauli_expectation() {
        let rows = vec![
            vec![GaussianRational::one(), GaussianRational::zero()],
            vec![GaussianRational::zero(), GaussianRational::zero()],
        ];
        let mat = ExactMatrix::from_rows(rows).unwrap();
        let rho = DensityOperator::new(mat).unwrap();
        assert_eq!(rho.purity().unwrap(), q(1));

        let sigma_z = ExactMatrix::from_rows(vec![
            vec![GaussianRational::one(), GaussianRational::zero()],
            vec![
                GaussianRational::zero(),
                GaussianRational::from_integers(-1, 0),
            ],
        ])
        .unwrap();

        let exp_z = rho.expectation(&sigma_z).unwrap();
        assert_eq!(exp_z, GaussianRational::one());
    }
}

mod bridge;
