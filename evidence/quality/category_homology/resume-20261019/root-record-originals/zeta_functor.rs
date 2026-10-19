//! Declared finite orbit/product data. AuthorityEffect: None.
//! The supplied product is metadata; this record does not verify orbit primitivity,
//! compute Euler factors, certify a functor, or define an infinite zeta function.

#[derive(Debug, Clone, PartialEq)]
pub struct ZetaFunctorWitness {
    pub primitive_orbits: Vec<String>,
    pub finite_euler_product: num_rational::BigRational,
}

impl ZetaFunctorWitness {
    pub fn new(
        primitive_orbits: Vec<String>,
        finite_euler_product: num_rational::BigRational,
    ) -> Self {
        Self {
            primitive_orbits,
            finite_euler_product,
        }
    }
}
