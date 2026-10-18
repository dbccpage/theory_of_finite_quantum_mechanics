//! Functor-shaped witness from primitive orbit data to finite Euler products.

#[derive(Debug, Clone, PartialEq)]
pub struct ZetaFunctorWitness {
    pub primitive_orbits: Vec<String>,
    pub finite_euler_product: f64,
}

impl ZetaFunctorWitness {
    pub fn new(primitive_orbits: Vec<String>, finite_euler_product: f64) -> Self {
        Self {
            primitive_orbits,
            finite_euler_product,
        }
    }
}
