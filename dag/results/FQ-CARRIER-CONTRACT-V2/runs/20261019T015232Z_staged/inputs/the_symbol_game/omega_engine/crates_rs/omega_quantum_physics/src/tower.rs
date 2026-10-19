//! Directed exact cyclotomic carriers for finite quantum amplitudes.
//! Inclusions use the canonical field criterion, including Q(zeta_6)=Q(zeta_3).
//! AuthorityEffect: None.
use omega_number_theory::cyclotomic_field::{
    compositum_conductor, contains_cyclotomic_field, embed_cyclotomic, normalized_conductor,
    CyclotomicError, CyclotomicNumber,
};
#[derive(Debug, Clone, PartialEq, Eq)]
pub struct CyclotomicTower {
    conductors: Vec<usize>,
}
impl CyclotomicTower {
    pub fn new(conductors: Vec<usize>) -> Result<Self, CyclotomicError> {
        if conductors.is_empty() || conductors.len() > 1024 {
            return Err(CyclotomicError::ConductorTooLarge {
                conductor: conductors.len(),
                max: 1024,
            });
        }
        for &n in &conductors {
            normalized_conductor(n)?;
        }
        for pair in conductors.windows(2) {
            if !contains_cyclotomic_field(pair[0], pair[1])? {
                return Err(CyclotomicError::ConductorMismatch {
                    left: pair[0],
                    right: pair[1],
                });
            }
        }
        Ok(Self { conductors })
    }
    pub fn conductors(&self) -> &[usize] {
        &self.conductors
    }
    pub fn join(conductors: &[usize]) -> Result<usize, CyclotomicError> {
        conductors
            .iter()
            .try_fold(1, |join, &n| compositum_conductor(join, n))
    }
    pub fn embed(
        &self,
        x: &CyclotomicNumber,
        stage: usize,
    ) -> Result<CyclotomicNumber, CyclotomicError> {
        let conductor = *self
            .conductors
            .get(stage)
            .ok_or(CyclotomicError::ConductorTooLarge {
                conductor: stage,
                max: 1024,
            })?;
        embed_cyclotomic(x, conductor)
    }
}
/// Exact Born norm in the real subfield, computed with complex conjugation.
/// Positivity follows from the chosen complex embedding, not from a rational
/// sign comparison when the answer is algebraic.
pub fn born_norm(amplitude: &CyclotomicNumber) -> Result<CyclotomicNumber, CyclotomicError> {
    amplitude.mul(&amplitude.conjugate())
}
