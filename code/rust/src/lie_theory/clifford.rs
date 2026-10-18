//! Exact Clifford families, Jordan-Wigner representations and their spin action.
//!
//! Declared matrices are admitted against every anticommutator
//! {gamma_mu,gamma_nu}=2 eta_mu delta_mu_nu I. Canonical constructors use the
//! Pauli owner and minimal complex representations of dimension 2^floor(n/2).
//! The volume element has square (-1)^(n(n-1)/2) product eta; even families
//! yield a normalized chirality involution. Matrix elimination belongs to
//! `linear_algebra::exact_field`; no bit mask is used to form chirality.
//!
//! AuthorityEffect: None.
use crate::pauli_symplectic::{pauli_word, Pauli, PauliError};
use crate::scalar::ComplexField;
use linear_algebra::backend::basic_matrix::BasicMatrix;
use linear_algebra::exact_field::{elimination, matrix as mx, ExactFieldError};
use omega_number_theory::rational::{ri, rq, Rational};

#[derive(Debug, Clone, PartialEq, Eq, thiserror::Error)]
pub enum CliffordError {
    #[error("a Clifford family must be nonempty")]
    Empty,
    #[error("gamma {index} has a different square shape")]
    Shape { index: usize },
    #[error("metric length or sign is invalid")]
    Metric,
    #[error("the Clifford anticommutator fails at ({mu},{nu})")]
    Anticommutator { mu: usize, nu: usize },
    #[error("the dense Clifford construction exceeds its declared size bound")]
    SizeBound,
    #[error("an odd family has no chirality")]
    OddFamily,
    #[error("the field does not contain i")]
    MissingImaginaryUnit,
    #[error("the spin element does not have the declared square shape")]
    SpinShape,
    #[error("the element is not in the Clifford normalizer")]
    NotNormalizer,
    #[error(transparent)]
    Pauli(#[from] PauliError),
    #[error(transparent)]
    Matrix(#[from] ExactFieldError),
}

#[derive(Debug, Clone, PartialEq, Eq)]
pub struct CliffordFamily<F> {
    gammas: Vec<BasicMatrix<F>>,
    metric: Vec<i8>,
}

impl<F: ComplexField> CliffordFamily<F> {
    pub fn admit(gammas: Vec<BasicMatrix<F>>, metric: Vec<i8>) -> Result<Self, CliffordError> {
        let size = gammas.first().ok_or(CliffordError::Empty)?.rows();
        if gammas.len() > 128 || size > 64 {
            return Err(CliffordError::SizeBound);
        }
        if let Some(index) = gammas
            .iter()
            .position(|g| g.shape() != (size, size) || size == 0)
        {
            return Err(CliffordError::Shape { index });
        }
        if metric.len() != gammas.len() || metric.iter().any(|s| *s != 1 && *s != -1) {
            return Err(CliffordError::Metric);
        }
        let identity = mx::identity::<F>(size)?;
        for mu in 0..gammas.len() {
            for nu in mu..gammas.len() {
                let expected = mx::scale(
                    &identity,
                    &F::from_rational(&ri(if mu == nu {
                        2 * i64::from(metric[mu])
                    } else {
                        0
                    })),
                )?;
                if mx::anticommutator(&gammas[mu], &gammas[nu])? != expected {
                    return Err(CliffordError::Anticommutator { mu, nu });
                }
            }
        }
        Ok(Self { gammas, metric })
    }
    pub fn gammas(&self) -> &[BasicMatrix<F>] {
        &self.gammas
    }
    pub fn metric(&self) -> &[i8] {
        &self.metric
    }
    pub fn size(&self) -> usize {
        self.gammas[0].rows()
    }
    pub fn euclidean(n: usize) -> Result<Self, CliffordError> {
        if n == 0 {
            return Err(CliffordError::Empty);
        }
        if n > 12 {
            return Err(CliffordError::SizeBound);
        }
        let m = n / 2;
        let mut gammas = Vec::with_capacity(n);
        for mode in 0..m {
            for axis in [Pauli::X, Pauli::Y] {
                let mut word = vec![Pauli::Identity; m];
                for item in &mut word[..mode] {
                    *item = Pauli::Z;
                }
                word[mode] = axis;
                gammas.push(pauli_word::<F>(&word)?);
            }
        }
        if n % 2 == 1 {
            gammas.push(pauli_word::<F>(&vec![Pauli::Z; m])?);
        }
        Self::admit(gammas, vec![1; n])
    }
    pub fn minkowski(positive: usize, negative: usize) -> Result<Self, CliffordError> {
        let n = positive
            .checked_add(negative)
            .ok_or(CliffordError::SizeBound)?;
        let mut family = Self::euclidean(n)?;
        if negative != 0 {
            let i = F::imaginary_unit().ok_or(CliffordError::MissingImaginaryUnit)?;
            for index in positive..n {
                family.gammas[index] = mx::scale(&family.gammas[index], &i)?;
                family.metric[index] = -1;
            }
        }
        Self::admit(family.gammas, family.metric)
    }
    pub fn volume_square(&self) -> i8 {
        let n = self.gammas.len();
        let permutation = if n % 4 == 2 || n % 4 == 3 { -1 } else { 1 };
        self.metric.iter().fold(permutation, |a, b| a * b)
    }
    pub fn volume_element(&self) -> Result<BasicMatrix<F>, CliffordError> {
        let mut volume = mx::identity(self.size())?;
        for gamma in &self.gammas {
            volume = mx::multiply(&volume, gamma)?;
        }
        Ok(volume)
    }
    pub fn chirality(&self) -> Result<BasicMatrix<F>, CliffordError> {
        if self.gammas.len() % 2 == 1 {
            return Err(CliffordError::OddFamily);
        }
        let volume = self.volume_element()?;
        if self.volume_square() == 1 {
            Ok(volume)
        } else {
            Ok(mx::scale(
                &volume,
                &F::imaginary_unit().ok_or(CliffordError::MissingImaginaryUnit)?,
            )?)
        }
    }
    pub fn product_span_rank(&self) -> Result<usize, CliffordError> {
        let n = self.gammas.len();
        let d = self.size();
        if n > 8 {
            return Err(CliffordError::SizeBound);
        }
        let mut entries = Vec::with_capacity((1 << n) * d * d);
        for mask in 0..1usize << n {
            let mut product = mx::identity(d)?;
            for mu in 0..n {
                if mask & (1 << mu) != 0 {
                    product = mx::multiply(&product, &self.gammas[mu])?;
                }
            }
            entries.extend_from_slice(product.as_slice());
        }
        let stacked =
            BasicMatrix::from_row_major(1 << n, d * d, entries).map_err(ExactFieldError::from)?;
        Ok(elimination::rank(&stacked)?)
    }
    pub fn plane_spin_element(
        &self,
        mu: usize,
        nu: usize,
        a: &Rational,
        b: &Rational,
    ) -> Result<BasicMatrix<F>, CliffordError> {
        if mu == nu || mu >= self.gammas.len() || nu >= self.gammas.len() {
            return Err(CliffordError::Metric);
        }
        let scalar = mx::scale(&mx::identity(self.size())?, &F::from_rational(a))?;
        let bivector = mx::scale(
            &mx::multiply(&self.gammas[mu], &self.gammas[nu])?,
            &F::from_rational(b),
        )?;
        Ok(mx::add(&scalar, &bivector)?)
    }
    /// `S^-1 gamma_mu S=sum_nu L_mu_nu gamma_nu`, verified by reconstruction.
    pub fn vector_action(&self, s: &BasicMatrix<F>) -> Result<BasicMatrix<F>, CliffordError> {
        if s.shape() != (self.size(), self.size()) {
            return Err(CliffordError::SpinShape);
        }
        let inverse = elimination::inverse(s)?;
        let n = self.gammas.len();
        let mut action = mx::zeros(n, n)?;
        for mu in 0..n {
            let image = mx::multiply(&mx::multiply(&inverse, &self.gammas[mu])?, s)?;
            let mut reconstruction = mx::zeros(self.size(), self.size())?;
            for nu in 0..n {
                let t = mx::trace(&mx::multiply(&image, &self.gammas[nu])?)?.mul(
                    &F::from_rational(&rq(i64::from(self.metric[nu]), self.size() as i64)),
                );
                action
                    .set(mu, nu, t.clone())
                    .map_err(ExactFieldError::from)?;
                reconstruction = mx::add(&reconstruction, &mx::scale(&self.gammas[nu], &t)?)?;
            }
            if reconstruction != image {
                return Err(CliffordError::NotNormalizer);
            }
        }
        Ok(action)
    }
}

pub fn jordan_wigner_family<F: ComplexField>(
    modes: usize,
) -> Result<CliffordFamily<F>, CliffordError> {
    if modes > 6 {
        return Err(CliffordError::SizeBound);
    }
    CliffordFamily::euclidean(2 * modes)
}

pub fn jordan_wigner_operator<F: ComplexField>(
    modes: usize,
    index: usize,
) -> Result<BasicMatrix<F>, CliffordError> {
    if modes == 0 || modes > 6 || index >= 2 * modes {
        return Err(CliffordError::SizeBound);
    }
    let mut word = vec![Pauli::Identity; modes];
    for item in &mut word[..index / 2] {
        *item = Pauli::Z;
    }
    word[index / 2] = if index % 2 == 0 { Pauli::X } else { Pauli::Y };
    Ok(pauli_word::<F>(&word)?)
}
