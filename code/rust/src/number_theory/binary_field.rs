//! `GF(2^k)` with elements packed as bit masks: bit `i` of an element is its
//! coefficient of `x^i`, and arithmetic is carry-less modulo an irreducible
//! polynomial. The symplectic trace form on `GF(2^k)^2` is included for the
//! Weyl-board spread checks.
//!
//! AuthorityEffect: None.

use crate::finite_field::checked_pow;

#[derive(Debug, Clone)]
pub struct BinaryField {
    degree: usize,
    modulus: usize,
    mask: usize,
    elements: Vec<usize>,
}

impl BinaryField {
    /// `GF(2^degree)` modulo `modulus`, a bit mask whose bit `i` is the
    /// coefficient of `x^i`.
    ///
    /// Panics unless `modulus` is an irreducible polynomial of exactly
    /// `degree`: any other modulus gives a ring with zero divisors, not a
    /// field. [`find_irreducible_binary_polynomial`] returns a valid one.
    pub fn new(degree: usize, modulus: usize) -> Self {
        assert!(
            poly_degree(modulus) == Some(degree) && is_irreducible_binary(modulus),
            "binary field modulus {modulus:#b} is not an irreducible polynomial of degree {degree}"
        );
        let order = checked_pow(2, degree).expect("binary field sample dimensions fit in usize");
        Self {
            degree,
            modulus,
            mask: order - 1,
            elements: (0..order).collect(),
        }
    }

    pub fn degree(&self) -> usize {
        self.degree
    }

    /// The irreducible modulus as a bit mask: bit `i` is the coefficient of `x^i`.
    pub fn modulus(&self) -> usize {
        self.modulus
    }

    pub fn order(&self) -> usize {
        self.elements.len()
    }

    pub fn elements(&self) -> &[usize] {
        &self.elements
    }

    pub fn add(&self, left: usize, right: usize) -> usize {
        (left ^ right) & self.mask
    }

    pub fn mul(&self, mut left: usize, mut right: usize) -> usize {
        let mut product = 0usize;
        while right != 0 {
            if right & 1 == 1 {
                product ^= left;
            }
            right >>= 1;
            left <<= 1;
            if left & (1usize << self.degree) != 0 {
                left ^= self.modulus;
            }
        }
        product & self.mask
    }

    pub fn square(&self, value: usize) -> usize {
        self.mul(value, value)
    }

    pub fn trace(&self, value: usize) -> usize {
        let mut sum = 0usize;
        let mut conjugate = value;
        for _ in 0..self.degree {
            sum = self.add(sum, conjugate);
            conjugate = self.square(conjugate);
        }
        sum & 1
    }

    pub fn symplectic_trace(&self, left: (usize, usize), right: (usize, usize)) -> usize {
        let xy = self.mul(left.0, right.1);
        let yx = self.mul(left.1, right.0);
        self.trace(self.add(xy, yx))
    }
}

pub fn find_irreducible_binary_polynomial(degree: usize) -> Option<usize> {
    let start = (1usize << degree) | 1;
    let end = 1usize << (degree + 1);
    (start..end)
        .step_by(2)
        .find(|poly| poly_degree(*poly) == Some(degree) && is_irreducible_binary(*poly))
}

fn is_irreducible_binary(poly: usize) -> bool {
    let degree = poly_degree(poly).expect("nonzero polynomial");
    for divisor_degree in 1..=degree / 2 {
        let start = (1usize << divisor_degree) | 1;
        let end = 1usize << (divisor_degree + 1);
        for divisor in (start..end).step_by(2) {
            if poly_degree(divisor) == Some(divisor_degree) && poly_mod_binary(poly, divisor) == 0 {
                return false;
            }
        }
    }
    true
}

fn poly_mod_binary(mut dividend: usize, divisor: usize) -> usize {
    let divisor_degree = poly_degree(divisor).expect("nonzero divisor");
    while let Some(dividend_degree) = poly_degree(dividend) {
        if dividend_degree < divisor_degree {
            break;
        }
        dividend ^= divisor << (dividend_degree - divisor_degree);
    }
    dividend
}

fn poly_degree(poly: usize) -> Option<usize> {
    if poly == 0 {
        None
    } else {
        Some(usize::BITS as usize - 1 - poly.leading_zeros() as usize)
    }
}

pub fn binary_polynomial_coefficients(poly: usize, degree: usize) -> Vec<usize> {
    (0..=degree).map(|i| (poly >> i) & 1).collect()
}

/// A Weyl operator `i^phase X^x Z^z` on `C^{2^k}`, labelled over `GF(2^k)`.
#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub struct BinaryPauli {
    /// Phase exponent for `i^phase`.
    pub phase: u8,
    pub x: usize,
    pub z: usize,
}

impl BinaryPauli {
    /// The identity operator.
    pub fn identity() -> Self {
        Self {
            phase: 0,
            x: 0,
            z: 0,
        }
    }

    /// The Hermitian representative of `X^x Z^z`.
    pub fn hermitian(field: &BinaryField, x: usize, z: usize) -> Self {
        Self {
            phase: field.trace(field.mul(x, z)) as u8,
            x,
            z,
        }
    }

    pub fn mul(self, other: Self, field: &BinaryField) -> Self {
        let raw_sign = field.trace(field.mul(self.z, other.x)) as u8;
        Self {
            phase: (self.phase + other.phase + 2 * raw_sign) % 4,
            x: field.add(self.x, other.x),
            z: field.add(self.z, other.z),
        }
    }

    pub fn adjoint(self, field: &BinaryField) -> Self {
        let raw_adjoint_sign = field.trace(field.mul(self.x, self.z)) as u8;
        Self {
            phase: (4 - self.phase + 2 * raw_adjoint_sign) % 4,
            x: self.x,
            z: self.z,
        }
    }

    pub fn is_vector_zero(self) -> bool {
        self.x == 0 && self.z == 0
    }
}

/// Every product of a subset of `generators`, indexed by the subset's bit mask.
pub fn build_line_group(field: &BinaryField, generators: &[BinaryPauli]) -> Vec<BinaryPauli> {
    let mut group = Vec::with_capacity(field.order());
    for mask in 0..field.order() {
        let mut op = BinaryPauli::identity();
        for (bit, generator) in generators.iter().enumerate() {
            if (mask >> bit) & 1 == 1 {
                op = op.mul(*generator, field);
            }
        }
        group.push(op);
    }
    group
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn the_first_irreducible_polynomials_are_the_known_ones() {
        assert_eq!(find_irreducible_binary_polynomial(1), Some(0b11));
        assert_eq!(find_irreducible_binary_polynomial(2), Some(0b111));
        assert_eq!(find_irreducible_binary_polynomial(3), Some(0b1011));
        assert_eq!(find_irreducible_binary_polynomial(4), Some(0b10011));
        assert_eq!(binary_polynomial_coefficients(0b1011, 3), vec![1, 1, 0, 1]);
    }

    #[test]
    fn gf4_multiplication_and_trace_match_hand_computation() {
        // GF(4) = F_2[x] / (x^2 + x + 1): x * x = x + 1, x * (x + 1) = 1.
        let field = BinaryField::new(2, 0b111);
        assert_eq!(field.order(), 4);
        assert_eq!(field.mul(0b10, 0b10), 0b11);
        assert_eq!(field.mul(0b10, 0b11), 0b01);
        assert_eq!(field.add(0b10, 0b11), 0b01);
        // Tr(a) = a + a^2: Tr(0) = Tr(1) = 0, Tr(x) = Tr(x + 1) = 1.
        let traces: Vec<usize> = field.elements().iter().map(|a| field.trace(*a)).collect();
        assert_eq!(traces, vec![0, 0, 1, 1]);
    }

    #[test]
    fn every_nonzero_element_has_an_inverse() {
        for degree in 1..=5 {
            let modulus = find_irreducible_binary_polynomial(degree).unwrap();
            let field = BinaryField::new(degree, modulus);
            for a in field.elements().iter().copied().filter(|a| *a != 0) {
                assert!(
                    field.elements().iter().any(|b| field.mul(a, *b) == 1),
                    "GF(2^{degree}): {a:#b} has no inverse"
                );
            }
        }
    }

    #[test]
    #[should_panic(expected = "not an irreducible polynomial")]
    fn a_reducible_modulus_is_refused() {
        // x^2 + 1 = (x + 1)^2 over F_2.
        BinaryField::new(2, 0b101);
    }

    #[test]
    #[should_panic(expected = "not an irreducible polynomial")]
    fn a_modulus_of_the_wrong_degree_is_refused() {
        BinaryField::new(3, 0b111);
    }

    #[test]
    fn hermitian_paulis_are_self_adjoint_involutions() {
        let field = BinaryField::new(2, 0b111);
        for x in field.elements() {
            for z in field.elements() {
                let p = BinaryPauli::hermitian(&field, *x, *z);
                assert_eq!(p.adjoint(&field), p);
                assert_eq!(p.mul(p, &field), BinaryPauli::identity());
            }
        }
    }

    #[test]
    fn a_line_group_has_one_element_per_subset_of_generators() {
        let field = BinaryField::new(2, 0b111);
        let generators = [
            BinaryPauli::hermitian(&field, 0b01, 0),
            BinaryPauli::hermitian(&field, 0b10, 0),
        ];
        let group = build_line_group(&field, &generators);
        assert_eq!(group.len(), 4);
        assert_eq!(group[0], BinaryPauli::identity());
        assert_eq!(group[3], generators[0].mul(generators[1], &field));
    }
}
