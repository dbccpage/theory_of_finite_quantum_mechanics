//! Exact Stinespring realizations with a declared weighted environment metric.
//!
//! A weighted Kraus channel has V†(I tensor G)V=I with G=diag(w_k).
//! The channel is the corresponding weighted partial trace; rational four-square
//! splitting also gives an ordinary isometry over Q(i), at the cost of a larger
//! environment. Choi rank is the minimal environment dimension over C.
//! AuthorityEffect: None.

use crate::exact_channel::{ExactChannelError, ExactKrausChannel};
use crate::exact_hermitian::exact_limits;
use linear_algebra::backend::basic_matrix::BasicMatrix;
use linear_algebra::exact_field::{involution as star, matrix as mx};
use omega_number_theory::cyclotomic::GaussianRat;
use omega_number_theory::rational::Rational;

#[derive(Debug, Clone, PartialEq, Eq)]
pub struct WeightedStinespring {
    channel: ExactKrausChannel,
    isometry: BasicMatrix<GaussianRat>,
    metric: Vec<Rational>,
}

impl WeightedStinespring {
    /// Minimal weighted realization from a canonical Choi factorization.
    pub fn from_channel(channel: &ExactKrausChannel) -> Result<Self, ExactChannelError> {
        let channel = channel.minimal()?;
        let r = channel.operators().len();
        let rows = omega_kernel::resource_limits::OperationLimits::default()
            .checked_product(channel.dim_out(), r)?;
        omega_kernel::resource_limits::OperationLimits::default().check_hilbert_dim(rows)?;
        omega_kernel::resource_limits::OperationLimits::default().check_dense_matrix(
            rows,
            channel.dim_in(),
            std::mem::size_of::<GaussianRat>(),
        )?;
        let mut v = mx::zeros_with_limits(rows, channel.dim_in(), exact_limits())?;
        for (k, op) in channel.operators().iter().enumerate() {
            for b in 0..channel.dim_out() {
                for a in 0..channel.dim_in() {
                    v.set(b * r + k, a, op.get_ref(b, a)?.clone())?;
                }
            }
        }
        let result = Self {
            metric: channel.weights().to_vec(),
            channel,
            isometry: v,
        };
        if !result.verify()? {
            return Err(ExactChannelError::FactorizationReplay);
        }
        Ok(result)
    }
    pub fn environment_dim(&self) -> usize {
        self.metric.len()
    }
    pub fn isometry(&self) -> &BasicMatrix<GaussianRat> {
        &self.isometry
    }
    pub fn environment_metric(&self) -> &[Rational] {
        &self.metric
    }
    /// Independent contraction of the declared metric and V, with exact replay.
    pub fn verify(&self) -> Result<bool, ExactChannelError> {
        let r = self.environment_dim();
        let weighted = mx::from_fn_with_limits(
            self.isometry.rows(),
            self.isometry.cols(),
            exact_limits(),
            |row, col| {
                self.isometry.as_slice()[row * self.isometry.cols() + col]
                    .mul(&GaussianRat::from_rational(self.metric[row % r].clone()))
            },
        )?;
        let gram =
            mx::multiply_with_limits(&star::adjoint(&self.isometry)?, &weighted, exact_limits())?;
        Ok(gram == mx::identity_with_limits(self.channel.dim_in(), exact_limits())?)
    }

    /// Weighted partial trace, evaluated directly from V and G rather than
    /// reconstructing a Kraus family.
    pub fn apply(
        &self,
        rho: &BasicMatrix<GaussianRat>,
    ) -> Result<BasicMatrix<GaussianRat>, ExactChannelError> {
        crate::exact_hermitian::check_well_formed(rho).map_err(ExactChannelError::Malformed)?;
        if rho.rows() != self.channel.dim_in() || rho.cols() != self.channel.dim_in() {
            return Err(ExactChannelError::StateShape {
                expected: self.channel.dim_in(),
                actual: (rho.rows(), rho.cols()),
            });
        }
        let r = self.environment_dim();
        // Matrix products carry the shared scalar-operation budget; the naive
        // four-index contraction would perform O(d_in² d_out² r) field work.
        omega_kernel::resource_limits::OperationLimits::default().check_dense_matrix(
            self.isometry.rows(),
            self.isometry.rows(),
            std::mem::size_of::<GaussianRat>(),
        )?;
        let state = mx::multiply_with_limits(
            &mx::multiply_with_limits(&self.isometry, rho, exact_limits())?,
            &star::adjoint(&self.isometry)?,
            exact_limits(),
        )?;
        Ok(mx::from_fn_with_limits(
            self.channel.dim_out(),
            self.channel.dim_out(),
            exact_limits(),
            |b, c| {
                (0..r).fold(GaussianRat::zero(), |sum, k| {
                    sum.add(
                        &state.as_slice()[(b * r + k) * state.cols() + c * r + k]
                            .mul(&GaussianRat::from_rational(self.metric[k].clone())),
                    )
                })
            },
        )?)
    }

    /// Ordinary isometry over the original field after bounded four-square splitting.
    pub fn ordinary_isometry(
        &self,
        budget: u64,
    ) -> Result<BasicMatrix<GaussianRat>, ExactChannelError> {
        self.channel.to_unit_weight(budget)?.stinespring_isometry()
    }
}
