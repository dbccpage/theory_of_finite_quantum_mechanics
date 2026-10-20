
use crate::finite_field::checked_pow;

#[derive(Debug, Clone, PartialEq, Eq, thiserror::Error)]
pub enum BinaryFieldError {
    #[error("binary field degree {degree} must be in 1..={max_degree}")]
    DegreeOutOfRange { degree: usize, max_degree: usize },
    #[error("binary field modulus {modulus:#b} has degree {actual_degree:?}, expected {expected_degree}")]
    DegreeMismatch {
        modulus: usize,
        expected_degree: usize,
        actual_degree: Option<usize>,
    },
    #[error("binary field modulus {modulus:#b} is reducible over GF(2)")]
    ReducibleModulus { modulus: usize },
    #[error("binary field order 2^{degree} overflows usize")]
    OrderOverflow { degree: usize },
}

#[derive(Debug, Clone, PartialEq, Eq)]
pub struct BinaryField {
    degree: usize,
    modulus: usize,
    mask: usize,
    elements: Vec<usize>,
}

impl BinaryField {
    pub fn try_new(degree: usize, modulus: usize) -> Result<Self, BinaryFieldError> {
        let max_degree = usize::BITS as usize - 2;
        if degree == 0 || degree > max_degree {
            return Err(BinaryFieldError::DegreeOutOfRange { degree, max_degree });
        }
        let actual_degree = poly_degree(modulus);
        if actual_degree != Some(degree) {
            return Err(BinaryFieldError::DegreeMismatch {
                modulus,
                expected_degree: degree,
                actual_degree,
            });
        }
        if !is_irreducible_binary(modulus) {
            return Err(BinaryFieldError::ReducibleModulus { modulus });
        }
        let order = checked_pow(2, degree).ok_or(BinaryFieldError::OrderOverflow { degree })?;
        Ok(Self {
            degree,
            modulus,
            mask: order - 1,
            elements: (0..order).collect(),
        })
    }

    pub fn new(degree: usize, modulus: usize) -> Self {
        Self::try_new(degree, modulus).unwrap_or_else(|err| {
            panic!(
                "binary field modulus {modulus:#b} is not an irreducible polynomial of degree {degree}: {err}"
            )
        })
    }

    pub fn degree(&self) -> usize {
        self.degree
    }

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
    if degree == 0 || degree >= usize::BITS as usize - 1 {
        return None;
    }
    let start = (1usize << degree) | 1;
    let end = 1usize << (degree + 1);
    (start..end)
        .step_by(2)
        .find(|poly| poly_degree(*poly) == Some(degree) && is_irreducible_binary(*poly))
}

fn is_irreducible_binary(poly: usize) -> bool {
    let Some(degree) = poly_degree(poly) else {
        return false;
    };
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
    let Some(divisor_degree) = poly_degree(divisor) else {
        return dividend;
    };
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

#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub struct BinaryPauli {
    pub phase: u8,
    pub x: usize,
    pub z: usize,
}

impl BinaryPauli {
    pub fn identity() -> Self {
        Self {
            phase: 0,
            x: 0,
            z: 0,
        }
    }

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
        let field = BinaryField::new(2, 0b111);
        assert_eq!(field.order(), 4);
        assert_eq!(field.mul(0b10, 0b10), 0b11);
        assert_eq!(field.mul(0b10, 0b11), 0b01);
        assert_eq!(field.add(0b10, 0b11), 0b01);
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
    fn try_new_refuses_invalid_degrees_and_reducible_moduli() {
        assert!(matches!(
            BinaryField::try_new(0, 0b1),
            Err(BinaryFieldError::DegreeOutOfRange { degree: 0, .. })
        ));
        assert!(matches!(
            BinaryField::try_new(usize::BITS as usize, 0b111),
            Err(BinaryFieldError::DegreeOutOfRange { .. })
        ));
        assert_eq!(
            BinaryField::try_new(3, 0b111),
            Err(BinaryFieldError::DegreeMismatch {
                modulus: 0b111,
                expected_degree: 3,
                actual_degree: Some(2),
            })
        );
        assert_eq!(
            BinaryField::try_new(2, 0b101),
            Err(BinaryFieldError::ReducibleModulus { modulus: 0b101 })
        );
        assert!(BinaryField::try_new(2, 0b111).is_ok());
        assert_eq!(find_irreducible_binary_polynomial(0), None);
    }

    #[test]
    #[should_panic(expected = "not an irreducible polynomial")]
    fn a_reducible_modulus_is_refused() {
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
