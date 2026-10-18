
use crate::types::AuthorityEffect;
use omega_number_theory::cyclotomic_field::CyclotomicNumber;
use omega_number_theory::dyadic_presentation::{
    CharacterSumLimits, DyadicError, DyadicLevel, FiniteDualPrefix,
};

#[derive(Debug, Clone, PartialEq, Eq)]
pub struct DeclaredDyadicPairing {
    prefix: FiniteDualPrefix,
    compared_index: usize,
    actual_inner_product: CyclotomicNumber,
}

impl DeclaredDyadicPairing {
    pub fn new(
        indices: &[usize],
        compared_index: usize,
        limits: CharacterSumLimits,
    ) -> Result<Self, DyadicError> {
        let prefix = FiniteDualPrefix::new(indices)?;
        let group = DyadicLevel::new((prefix.indices().len() - 1) as u32)?;
        if compared_index >= group.order() {
            return Err(DyadicError::OutOfCarrier);
        }
        let actual_inner_product = group.normalized_inner_product(
            &(*prefix.indices().last().unwrap()).into(),
            &compared_index.into(),
            limits,
        )?;
        Ok(Self {
            prefix,
            compared_index,
            actual_inner_product,
        })
    }

    pub fn prefix(&self) -> &FiniteDualPrefix {
        &self.prefix
    }

    pub fn compared_index(&self) -> usize {
        self.compared_index
    }

    pub fn actual_inner_product(&self) -> &CyclotomicNumber {
        &self.actual_inner_product
    }

    pub fn authority_effect(&self) -> AuthorityEffect {
        AuthorityEffect::None
    }
}
