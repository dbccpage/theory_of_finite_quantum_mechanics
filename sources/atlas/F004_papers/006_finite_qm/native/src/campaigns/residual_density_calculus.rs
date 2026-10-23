//! Programme residual ledgers and coherence admission records.
//! AuthorityEffect: None. Not PROVED. Not GlobalGreen.
use linear_algebra::backend::basic_matrix::BasicMatrix;
use linear_algebra::exact_field::matrix;
use num_traits::Signed;
use omega_functional::born_probabilities::{BornProbabilities, BornProbabilityError};
use omega_number_theory::{cyclotomic::GaussianRat, rational::Rational};
use omega_quantum_physics::exact_hermitian::{self};
use omega_quantum_physics::residual_density_calculus::{sector_measurement, ResidualDensityError};

/// Nonnegative sector masses with positive total.
#[derive(Debug, Clone, PartialEq, Eq)]
pub struct ResidualLedger {
    masses: Vec<Rational>,
}

impl ResidualLedger {
    pub fn new(masses: Vec<Rational>) -> Result<Self, ResidualDensityError> {
        if masses.len() > 128 {
            return Err(ResidualDensityError::Shape);
        }
        BornProbabilities::from_weights(&masses).map_err(|error| match error {
            BornProbabilityError::EmptyInput => ResidualDensityError::Empty,
            BornProbabilityError::NegativeWeight { index } => {
                ResidualDensityError::NegativeMass { index }
            }
            _ => ResidualDensityError::ZeroTotalMass,
        })?;
        Ok(Self { masses })
    }

    /// The orientation-blind ledger `|x|` of a signed residual.
    pub fn from_signed_residual(x: &[Rational]) -> Result<Self, ResidualDensityError> {
        Self::new(x.iter().map(Signed::abs).collect())
    }

    pub fn masses(&self) -> &[Rational] {
        &self.masses
    }

    pub fn total(&self) -> Rational {
        self.masses.iter().sum()
    }

    /// `p(s) = mu(s) / M`.
    pub fn weights(&self) -> Vec<Rational> {
        BornProbabilities::from_weights(&self.masses)
            .expect("constructor admits positive finite masses")
            .probabilities()
            .to_vec()
    }

    /// `rho = diag(p)`.
    pub fn diagonal_density(&self) -> BasicMatrix<GaussianRat> {
        let entries: Vec<GaussianRat> = self
            .weights()
            .into_iter()
            .map(GaussianRat::from_rational)
            .collect();
        matrix::diagonal(&entries).expect("constructor bounds the diagonal carrier")
    }

    /// `Tr(rho^2) = sum p(s)^2`.
    pub fn purity(&self) -> Rational {
        self.weights().iter().map(|p| p * p).sum()
    }
}

/// Read a trace-one PSD diagonal density back as a ledger of its diagonal.
pub fn ledger_from_diagonal_density(
    rho: &BasicMatrix<GaussianRat>,
) -> Result<ResidualLedger, ResidualDensityError> {
    if rho.rows() != rho.cols() || rho.rows() == 0 || rho.rows() > 128 {
        return Err(ResidualDensityError::Shape);
    }
    for row in 0..rho.rows() {
        for col in 0..rho.cols() {
            if row != col && *rho.get_ref(row, col)? != GaussianRat::zero() {
                return Err(ResidualDensityError::OffDiagonal { row, col });
            }
        }
    }
    if !exact_hermitian::is_positive_semidefinite(rho) || matrix::trace(rho)? != GaussianRat::one()
    {
        return Err(ResidualDensityError::NotADensity);
    }
    ResidualLedger::new(sector_measurement(rho)?)
}

/// A coherence license as evaluated for one candidate. The fields are private,
/// so a license exists only as [`evaluate_coherence`] computed it. The source's
/// fifth field, "authority ceiling unchanged", is not stored: no diagnostic
/// here can represent authority, so it would be a constant.
#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub struct CoherenceLicense {
    sector_identity_preserved: bool,
    phase_relation_declared: bool,
    psd_condition_satisfied: bool,
    observer_basis_declared: bool,
}

impl CoherenceLicense {
    /// Computed: the coherent matrix keeps the ledger's weights on its diagonal.
    pub fn sector_identity_preserved(&self) -> bool {
        self.sector_identity_preserved
    }

    /// Computed: at least one off-diagonal phase was actually supplied.
    pub fn phase_relation_declared(&self) -> bool {
        self.phase_relation_declared
    }

    /// Computed: the coherent matrix is exactly PSD.
    pub fn psd_condition_satisfied(&self) -> bool {
        self.psd_condition_satisfied
    }

    /// Declared by the caller.
    pub fn observer_basis_declared(&self) -> bool {
        self.observer_basis_declared
    }

    pub fn is_licensed(&self) -> bool {
        self.sector_identity_preserved
            && self.phase_relation_declared
            && self.psd_condition_satisfied
            && self.observer_basis_declared
    }
}

/// Evaluate a proposed coherent density `rho` for a ledger.
pub fn evaluate_coherence(
    ledger: &ResidualLedger,
    rho: &BasicMatrix<GaussianRat>,
    observer_basis_declared: bool,
) -> CoherenceLicense {
    let n = ledger.masses.len();
    let shaped = rho.rows() == n && rho.cols() == n;
    let weights = ledger.weights();
    let sector_identity_preserved = shaped
        && (0..n).all(|s| {
            rho.get_ref(s, s).expect("matching matrix dimensions")
                == &GaussianRat::from_rational(weights[s].clone())
        });
    let phase_relation_declared = shaped
        && (0..n).any(|r| {
            (0..n).any(|c| {
                r != c
                    && *rho.get_ref(r, c).expect("matching matrix dimensions")
                        != GaussianRat::zero()
            })
        });
    CoherenceLicense {
        sector_identity_preserved,
        phase_relation_declared,
        psd_condition_satisfied: shaped && exact_hermitian::is_positive_semidefinite(rho),
        observer_basis_declared,
    }
}

/// Admit a coherent density only when its license is complete.
pub fn licensed_coherent_density(
    ledger: &ResidualLedger,
    rho: BasicMatrix<GaussianRat>,
    observer_basis_declared: bool,
) -> Result<BasicMatrix<GaussianRat>, CoherenceLicense> {
    let license = evaluate_coherence(ledger, &rho, observer_basis_declared);
    if license.is_licensed() {
        Ok(rho)
    } else {
        Err(license)
    }
}
