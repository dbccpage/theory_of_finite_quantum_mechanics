//! Strict finite A-infinity algebras from checked differential graded algebras.
//! AuthorityEffect: None. Coefficients lie in an admitted prime field F_p.
//! m_1 has degree +1, m_2 degree 0, and m_n=0 for n=0 and n>=3.
//! The Stasheff identities reduce exactly to d^2=0, graded Leibniz and
//! associativity. This is not a checker for arbitrary higher operations.
#![forbid(unsafe_code)]

#[derive(Debug, Clone, Copy, PartialEq, Eq)]
/// Coefficient-cell and conservative whole-phase field-operation admission.
/// Zero/sparse terms do not refund the bound. Arity applies to queries.
/// Limits do not bound parsing, allocator internals or total process memory/time.
pub struct AlgebraLimits {
    pub max_cells: usize,
    pub max_field_operations: usize,
    pub max_arity: usize,
}
impl Default for AlgebraLimits {
    fn default() -> Self {
        Self {
            max_cells: 4096,
            max_field_operations: 1_000_000,
            max_arity: 64,
        }
    }
}
#[derive(Debug, Clone, PartialEq, Eq)]
pub enum AlgebraError {
    NonPrimeModulus {
        modulus: u16,
    },
    CountOverflow,
    Limit {
        resource: &'static str,
        requested: usize,
        limit: usize,
    },
    Shape {
        table: &'static str,
        expected: usize,
        actual: usize,
    },
    Coefficient {
        table: &'static str,
        index: usize,
        value: u16,
        modulus: u16,
    },
    DegreeOverflow,
    DifferentialDegree {
        input: usize,
        output: usize,
    },
    ProductDegree {
        left: usize,
        right: usize,
        output: usize,
    },
    DifferentialSquared {
        input: usize,
        output: usize,
        residue: u16,
    },
    Leibniz {
        left: usize,
        right: usize,
        output: usize,
        residue: u16,
    },
    Associativity {
        first: usize,
        second: usize,
        third: usize,
        output: usize,
        residue: u16,
    },
    BasisOutOfBounds {
        index: usize,
        dimension: usize,
    },
    AllocationFailed {
        cells: usize,
    },
}
impl std::fmt::Display for AlgebraError {
    fn fmt(&self, f: &mut std::fmt::Formatter<'_>) -> std::fmt::Result {
        write!(f, "{self:?}")
    }
}
impl std::error::Error for AlgebraError {}
type Result<T> = std::result::Result<T, AlgebraError>;
fn add(a: usize, b: usize) -> Result<usize> {
    a.checked_add(b).ok_or(AlgebraError::CountOverflow)
}
fn mul(a: usize, b: usize) -> Result<usize> {
    a.checked_mul(b).ok_or(AlgebraError::CountOverflow)
}
fn admit(resource: &'static str, requested: usize, limit: usize) -> Result<()> {
    if requested > limit {
        return Err(AlgebraError::Limit {
            resource,
            requested,
            limit,
        });
    }
    Ok(())
}
fn shape(table: &'static str, expected: usize, actual: usize) -> Result<()> {
    if expected != actual {
        return Err(AlgebraError::Shape {
            table,
            expected,
            actual,
        });
    }
    Ok(())
}

/// A prime modulus representable by u16. Private storage excludes p=0,1 and
/// composite moduli before any remainder operation in field arithmetic.
/// ```compile_fail
/// use tfqm_homotopy_type_theory::a_infinity::PrimeField;
/// let _ = PrimeField { modulus: 0 };
/// ```
#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub struct PrimeField {
    modulus: u16,
}
impl PrimeField {
    pub fn try_new(modulus: u16) -> Result<Self> {
        let p = u32::from(modulus);
        if p < 2 {
            return Err(AlgebraError::NonPrimeModulus { modulus });
        }
        let mut divisor = 2u32;
        while divisor * divisor <= p {
            if p % divisor == 0 {
                return Err(AlgebraError::NonPrimeModulus { modulus });
            }
            divisor += 1;
        }
        Ok(Self { modulus })
    }
    pub fn modulus(self) -> u16 {
        self.modulus
    }
    fn sum(self, a: u16, b: u16) -> u16 {
        ((u32::from(a) + u32::from(b)) % u32::from(self.modulus)) as u16
    }
    fn product(self, a: u16, b: u16) -> u16 {
        ((u64::from(a) * u64::from(b)) % u64::from(self.modulus)) as u16
    }
    fn negative(self, a: u16) -> u16 {
        if a == 0 {
            0
        } else {
            self.modulus - a
        }
    }
    fn difference(self, a: u16, b: u16) -> u16 {
        // Canonical a,b<p imply 0<=a+p-b<2p; u32 is sufficient for u16 p.
        ((u32::from(a) + u32::from(self.modulus) - u32::from(b)) % u32::from(self.modulus)) as u16
    }
}

/// Immutable admitted DGA tables. All vector operations use these fixed field,
/// basis and grading data; no unverified higher-operation callback is accepted.
/// ```compile_fail
/// use tfqm_homotopy_type_theory::a_infinity::{PrimeField, StrictAInfinity};
/// let _ = StrictAInfinity { field: PrimeField::try_new(2).unwrap(),
///     degrees: vec![0], differential: vec![], product: vec![] };
/// ```
/// ```
/// use tfqm_homotopy_type_theory::a_infinity::{AlgebraLimits, StrictAInfinity, AlgebraError};
/// let limits = AlgebraLimits::default();
/// let algebra = StrictAInfinity::try_new(3, vec![0], vec![0], vec![1], limits)?;
/// assert_eq!(algebra.basis_operation(&[0, 0], limits)?.coefficient(0)?, 1);
/// # Ok::<(), AlgebraError>(())
/// ```
#[derive(Debug, PartialEq, Eq)]
pub struct StrictAInfinity {
    field: PrimeField,
    degrees: Vec<i32>,
    differential: Vec<u16>,
    product: Vec<u16>,
}
impl StrictAInfinity {
    pub fn try_new(
        modulus: u16,
        degrees: Vec<i32>,
        differential: Vec<u16>,
        product: Vec<u16>,
        limits: AlgebraLimits,
    ) -> Result<Self> {
        let field = PrimeField::try_new(modulus)?;
        admit_tables(degrees.len(), differential.len(), product.len(), limits)?;
        check_coefficients(field, "differential", &differential)?;
        check_coefficients(field, "product", &product)?;
        let algebra = Self {
            field,
            degrees,
            differential,
            product,
        };
        algebra.check_structure()?;
        Ok(algebra)
    }
    fn check_structure(&self) -> Result<()> {
        self.check_grading()?;
        self.check_d_squared()?;
        self.check_leibniz()?;
        self.check_associativity()
    }
    pub fn field(&self) -> PrimeField {
        self.field
    }
    pub fn dimension(&self) -> usize {
        self.degrees.len()
    }
    pub fn degrees(&self) -> &[i32] {
        &self.degrees
    }
    pub fn differential_table(&self) -> &[u16] {
        &self.differential
    }
    pub fn product_table(&self) -> &[u16] {
        &self.product
    }
    fn d(&self, input: usize, output: usize) -> u16 {
        self.differential[input * self.dimension() + output]
    }
    fn m(&self, left: usize, right: usize, output: usize) -> u16 {
        self.product[(left * self.dimension() + right) * self.dimension() + output]
    }
    fn check_grading(&self) -> Result<()> {
        for i in 0..self.dimension() {
            for j in 0..self.dimension() {
                self.check_d_degree(i, j)?;
                self.check_product_degrees(i, j)?;
            }
        }
        Ok(())
    }
    fn check_d_degree(&self, input: usize, output: usize) -> Result<()> {
        if self.d(input, output) != 0 {
            let degree = self.degrees[input]
                .checked_add(1)
                .ok_or(AlgebraError::DegreeOverflow)?;
            if degree != self.degrees[output] {
                return Err(AlgebraError::DifferentialDegree { input, output });
            }
        }
        Ok(())
    }
    fn check_product_degrees(&self, left: usize, right: usize) -> Result<()> {
        for output in 0..self.dimension() {
            if self.m(left, right, output) != 0 {
                self.check_product_degree(left, right, output)?;
            }
        }
        Ok(())
    }
    fn check_product_degree(&self, left: usize, right: usize, output: usize) -> Result<()> {
        let degree = self.degrees[left]
            .checked_add(self.degrees[right])
            .ok_or(AlgebraError::DegreeOverflow)?;
        if degree != self.degrees[output] {
            return Err(AlgebraError::ProductDegree {
                left,
                right,
                output,
            });
        }
        Ok(())
    }
    fn check_d_squared(&self) -> Result<()> {
        for input in 0..self.dimension() {
            for output in 0..self.dimension() {
                let residue = self.d_squared_coefficient(input, output);
                if residue != 0 {
                    return Err(AlgebraError::DifferentialSquared {
                        input,
                        output,
                        residue,
                    });
                }
            }
        }
        Ok(())
    }
    fn d_squared_coefficient(&self, input: usize, output: usize) -> u16 {
        let mut sum = 0;
        for inner in 0..self.dimension() {
            sum = self.field.sum(
                sum,
                self.field
                    .product(self.d(input, inner), self.d(inner, output)),
            );
        }
        sum
    }
    fn check_leibniz(&self) -> Result<()> {
        for left in 0..self.dimension() {
            for right in 0..self.dimension() {
                self.check_leibniz_row(left, right)?;
            }
        }
        Ok(())
    }
    fn check_leibniz_row(&self, left: usize, right: usize) -> Result<()> {
        for output in 0..self.dimension() {
            let residue = self.leibniz_coefficient(left, right, output);
            if residue != 0 {
                return Err(AlgebraError::Leibniz {
                    left,
                    right,
                    output,
                    residue,
                });
            }
        }
        Ok(())
    }
    fn leibniz_coefficient(&self, left: usize, right: usize, output: usize) -> u16 {
        let (mut lhs, mut first, mut second) = (0, 0, 0);
        for inner in 0..self.dimension() {
            lhs = self.field.sum(
                lhs,
                self.field
                    .product(self.m(left, right, inner), self.d(inner, output)),
            );
            first = self.field.sum(
                first,
                self.field
                    .product(self.d(left, inner), self.m(inner, right, output)),
            );
            second = self.field.sum(
                second,
                self.field
                    .product(self.d(right, inner), self.m(left, inner, output)),
            );
        }
        if self.degrees[left].rem_euclid(2) != 0 {
            second = self.field.negative(second);
        }
        self.field.difference(lhs, self.field.sum(first, second))
    }
    fn check_associativity(&self) -> Result<()> {
        for first in 0..self.dimension() {
            for second in 0..self.dimension() {
                for third in 0..self.dimension() {
                    self.check_associative_row(first, second, third)?;
                }
            }
        }
        Ok(())
    }
    fn check_associative_row(&self, first: usize, second: usize, third: usize) -> Result<()> {
        for output in 0..self.dimension() {
            let residue = self.associator_coefficient(first, second, third, output);
            if residue != 0 {
                return Err(AlgebraError::Associativity {
                    first,
                    second,
                    third,
                    output,
                    residue,
                });
            }
        }
        Ok(())
    }
    fn associator_coefficient(
        &self,
        first: usize,
        second: usize,
        third: usize,
        output: usize,
    ) -> u16 {
        let (mut lhs, mut rhs) = (0, 0);
        for inner in 0..self.dimension() {
            lhs = self.field.sum(
                lhs,
                self.field
                    .product(self.m(first, second, inner), self.m(inner, third, output)),
            );
            rhs = self.field.sum(
                rhs,
                self.field
                    .product(self.m(second, third, inner), self.m(first, inner, output)),
            );
        }
        self.field.difference(lhs, rhs)
    }
    fn check_basis(&self, index: usize) -> Result<()> {
        if index >= self.dimension() {
            return Err(AlgebraError::BasisOutOfBounds {
                index,
                dimension: self.dimension(),
            });
        }
        Ok(())
    }
    pub fn basis_operation(
        &self,
        inputs: &[usize],
        limits: AlgebraLimits,
    ) -> Result<Operation<'_>> {
        admit("arity", inputs.len(), limits.max_arity)?;
        for &index in inputs {
            self.check_basis(index)?;
        }
        let coefficients = match inputs {
            [input] => {
                Some(&self.differential[input * self.dimension()..(input + 1) * self.dimension()])
            }
            [left, right] => {
                let row = (left * self.dimension() + right) * self.dimension();
                Some(&self.product[row..row + self.dimension()])
            }
            _ => None,
        };
        Ok(Operation {
            algebra: self,
            coefficients,
        })
    }
    pub fn evaluate(&self, inputs: &[&[u16]], limits: AlgebraLimits) -> Result<Vec<u16>> {
        self.admit_evaluation(inputs, limits)?;
        let mut output = zero_buffer(self.dimension())?;
        match inputs {
            [input] => self.evaluate_d(input, &mut output),
            [left, right] => self.evaluate_product(left, right, &mut output),
            _ => {}
        }
        Ok(output)
    }
    fn admit_evaluation(&self, inputs: &[&[u16]], limits: AlgebraLimits) -> Result<()> {
        admit("arity", inputs.len(), limits.max_arity)?;
        admit("output cells", self.dimension(), limits.max_cells)?;
        admit(
            "evaluation field operations",
            evaluation_work(self.dimension(), inputs.len())?,
            limits.max_field_operations,
        )?;
        for input in inputs {
            shape("input vector", self.dimension(), input.len())?;
            check_coefficients(self.field, "input vector", input)?;
        }
        Ok(())
    }
    fn evaluate_d(&self, input: &[u16], output: &mut [u16]) {
        for (out, value) in output.iter_mut().enumerate() {
            for (i, &coefficient) in input.iter().enumerate() {
                *value = self
                    .field
                    .sum(*value, self.field.product(coefficient, self.d(i, out)));
            }
        }
    }
    fn evaluate_product(&self, left: &[u16], right: &[u16], output: &mut [u16]) {
        for (out, value) in output.iter_mut().enumerate() {
            self.evaluate_product_coefficient(left, right, out, value);
        }
    }
    fn evaluate_product_coefficient(
        &self,
        left: &[u16],
        right: &[u16],
        output: usize,
        value: &mut u16,
    ) {
        for (i, &a) in left.iter().enumerate() {
            for (j, &b) in right.iter().enumerate() {
                let term = self
                    .field
                    .product(self.field.product(a, b), self.m(i, j, output));
                *value = self.field.sum(*value, term);
            }
        }
    }
}
fn admit_tables(
    n: usize,
    differential: usize,
    product: usize,
    limits: AlgebraLimits,
) -> Result<()> {
    let square = mul(n, n)?;
    let cube = mul(square, n)?;
    admit("table cells", add(square, cube)?, limits.max_cells)?;
    admit(
        "identity field operations",
        identity_work(n)?,
        limits.max_field_operations,
    )?;
    shape("differential", square, differential)?;
    shape("product", cube, product)
}
fn check_coefficients(field: PrimeField, table: &'static str, values: &[u16]) -> Result<()> {
    for (index, &value) in values.iter().enumerate() {
        if value >= field.modulus {
            return Err(AlgebraError::Coefficient {
                table,
                index,
                value,
                modulus: field.modulus,
            });
        }
    }
    Ok(())
}
fn identity_work(n: usize) -> Result<usize> {
    let square = mul(n, n)?;
    let cube = mul(square, n)?;
    let fourth = mul(cube, n)?;
    let fifth = mul(fourth, n)?;
    // d^2:2n^3; Leibniz:6n^4+3n^3; associativity:4n^5+n^4.
    // The extra terms include sign, final addition and subtraction operations.
    add(mul(cube, 5)?, add(mul(fourth, 7)?, mul(fifth, 4)?)?)
}
fn evaluation_work(n: usize, arity: usize) -> Result<usize> {
    match arity {
        1 => mul(mul(n, n)?, 2),
        2 => mul(mul(mul(n, n)?, n)?, 3),
        _ => Ok(0),
    }
}
fn zero_buffer(cells: usize) -> Result<Vec<u16>> {
    let mut values = Vec::new();
    values
        .try_reserve_exact(cells)
        .map_err(|_| AlgebraError::AllocationFailed { cells })?;
    values.resize(cells, 0);
    Ok(values)
}
/// A borrowed basis-operation column, or the exact zero operation of an arity
/// other than one/two. Private fields cannot forge an admitted operation view.
/// ```compile_fail
/// use tfqm_homotopy_type_theory::a_infinity::{AlgebraLimits, StrictAInfinity, Operation};
/// let algebra = StrictAInfinity::try_new(3, vec![0], vec![0], vec![1], AlgebraLimits::default()).unwrap();
/// let _ = Operation { algebra: &algebra, coefficients: Some(&[]) };
/// ```
#[derive(Debug)]
pub struct Operation<'a> {
    algebra: &'a StrictAInfinity,
    coefficients: Option<&'a [u16]>,
}
impl Operation<'_> {
    pub fn algebra(&self) -> &StrictAInfinity {
        self.algebra
    }
    pub fn dimension(&self) -> usize {
        self.algebra.dimension()
    }
    pub fn coefficient(&self, index: usize) -> Result<u16> {
        if index >= self.dimension() {
            return Err(AlgebraError::BasisOutOfBounds {
                index,
                dimension: self.dimension(),
            });
        }
        Ok(self.coefficients.map_or(0, |values| values[index]))
    }
    pub fn is_zero(&self) -> bool {
        self.coefficients
            .is_none_or(|values| values.iter().all(|&v| v == 0))
    }
}

#[cfg(test)]
mod tests {
    use super::*;
    fn contractible(prime: u16) -> StrictAInfinity {
        // Basis 1,e, |e|=-1, d(e)=1 and e^2=0.
        StrictAInfinity::try_new(
            prime,
            vec![0, -1],
            vec![0, 0, 1, 0],
            vec![1, 0, 0, 1, 0, 1, 0, 0],
            AlgebraLimits::default(),
        )
        .unwrap()
    }
    #[test]
    fn prime_gate_checks_all_u16_values_against_sieve() {
        let mut prime = vec![true; 65536];
        prime[0] = false;
        prime[1] = false;
        for p in 2..256 {
            if prime[p] {
                for multiple in (p * p..65536).step_by(p) {
                    prime[multiple] = false;
                }
            }
        }
        for p in 0..=u16::MAX {
            assert_eq!(PrimeField::try_new(p).is_ok(), prime[p as usize], "{p}");
        }
    }
    #[test]
    fn field_arithmetic_extremes_match_wide_integer_remainders() {
        for p in [2, 3, 5, 251, 65521] {
            let field = PrimeField::try_new(p).unwrap();
            for a in [0, 1, p / 2, p - 1] {
                for b in [0, 1, p / 2, p - 1] {
                    let (a128, b128, p128) = (u128::from(a), u128::from(b), u128::from(p));
                    assert_eq!(field.sum(a, b), ((a128 + b128) % p128) as u16);
                    assert_eq!(field.product(a, b), ((a128 * b128) % p128) as u16);
                    assert_eq!(field.difference(a, b), ((a128 + p128 - b128) % p128) as u16);
                }
            }
        }
    }
    #[test]
    fn constructor_refuses_each_independent_algebra_law() {
        let d = AlgebraLimits::default();
        let mut differential = vec![0; 9];
        differential[1] = 1;
        differential[5] = 1;
        assert!(matches!(
            StrictAInfinity::try_new(3, vec![0, 1, 2], differential, vec![0; 27], d),
            Err(AlgebraError::DifferentialSquared {
                input: 0,
                output: 2,
                residue: 1
            })
        ));
        let mut product = vec![0; 8];
        product[0] = 1;
        assert!(matches!(
            StrictAInfinity::try_new(3, vec![0, -1], vec![0, 0, 1, 0], product, d),
            Err(AlgebraError::Leibniz { .. })
        ));
        let mut product = vec![0; 8];
        product[1] = 1;
        product[4] = 1;
        assert!(matches!(
            StrictAInfinity::try_new(3, vec![0, 0], vec![0; 4], product, d),
            Err(AlgebraError::Associativity { .. })
        ));
    }
    #[test]
    fn contractible_dga_evaluates_with_independent_coordinate_formulas() {
        for prime in [2, 3, 5] {
            let a = contractible(prime);
            let limits = AlgebraLimits::default();
            for u in 0..prime {
                for v in 0..prime {
                    assert_eq!(a.evaluate(&[&[u, v]], limits).unwrap(), vec![v, 0]);
                    for x in 0..prime {
                        for y in 0..prime {
                            let expected = vec![
                                (u32::from(u) * u32::from(x) % u32::from(prime)) as u16,
                                ((u32::from(u) * u32::from(y) + u32::from(v) * u32::from(x))
                                    % u32::from(prime)) as u16,
                            ];
                            assert_eq!(a.evaluate(&[&[u, v], &[x, y]], limits).unwrap(), expected);
                        }
                    }
                }
            }
            assert!(a.basis_operation(&[0, 0, 0], limits).unwrap().is_zero());
            assert!(a.basis_operation(&[usize::MAX, 0, 0], limits).is_err());
            assert!(a
                .evaluate(&[&[prime, 0], &[0, 0], &[0, 0]], limits)
                .is_err());
            assert_eq!(a.evaluate(&[], limits).unwrap(), vec![0, 0]);
        }
    }
    fn reference_product(table: u8, left: u8, right: u8) -> u8 {
        let mut result = 0;
        for i in 0..2 {
            for j in 0..2 {
                if left & (1 << i) != 0 && right & (1 << j) != 0 {
                    for out in 0..2 {
                        if table & (1 << ((2 * i + j) * 2 + out)) != 0 {
                            result ^= 1 << out;
                        }
                    }
                }
            }
        }
        result
    }
    #[test]
    fn all_binary_two_dimensional_products_match_all_vector_associativity() {
        let limits = AlgebraLimits::default();
        let mut accepted = 0;
        for table in 0..=u8::MAX {
            let expected = (0..4).all(|a| {
                (0..4).all(|b| {
                    (0..4).all(|c| {
                        reference_product(table, reference_product(table, a, b), c)
                            == reference_product(table, a, reference_product(table, b, c))
                    })
                })
            });
            let product = (0..8).map(|i| u16::from((table >> i) & 1)).collect();
            let result = StrictAInfinity::try_new(2, vec![0, 0], vec![0; 4], product, limits);
            assert_eq!(result.is_ok(), expected, "{table}");
            accepted += usize::from(result.is_ok());
            if let Ok(algebra) = result {
                for left in 0..4u8 {
                    for right in 0..4u8 {
                        let l = [u16::from(left & 1), u16::from((left >> 1) & 1)];
                        let r = [u16::from(right & 1), u16::from((right >> 1) & 1)];
                        let actual = algebra.evaluate(&[&l, &r], limits).unwrap();
                        let expected = reference_product(table, left, right);
                        assert_eq!(
                            actual,
                            vec![u16::from(expected & 1), u16::from((expected >> 1) & 1)]
                        );
                    }
                }
            }
        }
        assert!(accepted > 0 && accepted < 256);
    }
    #[test]
    fn limits_domains_and_degree_boundaries_are_exact_and_typed() {
        let limits = AlgebraLimits {
            max_cells: 2,
            max_field_operations: 16,
            max_arity: 2,
        };
        assert_eq!(identity_work(1), Ok(16));
        assert!(StrictAInfinity::try_new(3, vec![0], vec![0], vec![1], limits).is_ok());
        assert!(StrictAInfinity::try_new(
            3,
            vec![0],
            vec![0],
            vec![1],
            AlgebraLimits {
                max_field_operations: 15,
                ..limits
            }
        )
        .is_err());
        assert!(StrictAInfinity::try_new(
            3,
            vec![0],
            vec![0],
            vec![1],
            AlgebraLimits {
                max_cells: 1,
                ..limits
            }
        )
        .is_err());
        assert!(StrictAInfinity::try_new(3, vec![0], vec![3], vec![0], limits).is_err());
        assert!(StrictAInfinity::try_new(3, vec![i32::MAX], vec![1], vec![0], limits).is_err());
        assert!(StrictAInfinity::try_new(3, vec![i32::MAX], vec![0], vec![1], limits).is_err());
        assert!(StrictAInfinity::try_new(3, vec![i32::MIN], vec![0], vec![0], limits).is_ok());
        assert_eq!(identity_work(usize::MAX), Err(AlgebraError::CountOverflow));
        let a = contractible(3);
        assert!(a.evaluate(&[&[1]], AlgebraLimits::default()).is_err());
        assert!(a
            .evaluate(
                &[&[0, 0]],
                AlgebraLimits {
                    max_field_operations: 7,
                    ..AlgebraLimits::default()
                }
            )
            .is_err());
        assert!(a
            .evaluate(
                &[&[0, 0]],
                AlgebraLimits {
                    max_cells: 1,
                    ..AlgebraLimits::default()
                }
            )
            .is_err());
        let zero = StrictAInfinity::try_new(
            2,
            vec![],
            vec![],
            vec![],
            AlgebraLimits {
                max_cells: 0,
                max_field_operations: 0,
                max_arity: 0,
            },
        )
        .unwrap();
        assert!(zero
            .evaluate(&[], AlgebraLimits::default())
            .unwrap()
            .is_empty());
    }
    #[test]
    fn shape_domain_and_grade_roles_have_specific_refusals() {
        let d = AlgebraLimits::default();
        assert_eq!(
            StrictAInfinity::try_new(3, vec![], vec![0], vec![], d).err(),
            Some(AlgebraError::Shape {
                table: "differential",
                expected: 0,
                actual: 1
            })
        );
        assert_eq!(
            StrictAInfinity::try_new(3, vec![], vec![], vec![0], d).err(),
            Some(AlgebraError::Shape {
                table: "product",
                expected: 0,
                actual: 1
            })
        );
        assert_eq!(
            StrictAInfinity::try_new(3, vec![0], vec![3], vec![0], d).err(),
            Some(AlgebraError::Coefficient {
                table: "differential",
                index: 0,
                value: 3,
                modulus: 3
            })
        );
        assert_eq!(
            StrictAInfinity::try_new(3, vec![0], vec![0], vec![3], d).err(),
            Some(AlgebraError::Coefficient {
                table: "product",
                index: 0,
                value: 3,
                modulus: 3
            })
        );
        assert_eq!(
            StrictAInfinity::try_new(3, vec![0, 0], vec![0, 1, 0, 0], vec![0; 8], d).err(),
            Some(AlgebraError::DifferentialDegree {
                input: 0,
                output: 1
            })
        );
        assert_eq!(
            StrictAInfinity::try_new(3, vec![1], vec![0], vec![1], d).err(),
            Some(AlgebraError::ProductDegree {
                left: 0,
                right: 0,
                output: 0
            })
        );
        assert_eq!(
            StrictAInfinity::try_new(3, vec![i32::MAX], vec![1], vec![0], d).err(),
            Some(AlgebraError::DegreeOverflow)
        );
        assert_eq!(
            StrictAInfinity::try_new(3, vec![i32::MAX], vec![0], vec![1], d).err(),
            Some(AlgebraError::DegreeOverflow)
        );
    }
    #[test]
    fn query_arity_output_bounds_and_work_admission_are_inclusive() {
        let a = contractible(3);
        let d = AlgebraLimits::default();
        let small = AlgebraLimits { max_arity: 2, ..d };
        assert_eq!(
            a.basis_operation(&[0, 0, 0], small).err(),
            Some(AlgebraError::Limit {
                resource: "arity",
                requested: 3,
                limit: 2
            })
        );
        assert_eq!(
            a.evaluate(&[&[0, 0], &[0, 0], &[0, 0]], small).err(),
            Some(AlgebraError::Limit {
                resource: "arity",
                requested: 3,
                limit: 2
            })
        );
        assert_eq!(
            a.basis_operation(&[2, 0, 0], d).err(),
            Some(AlgebraError::BasisOutOfBounds {
                index: 2,
                dimension: 2
            })
        );
        let zero = a.basis_operation(&[], d).unwrap();
        assert!(std::ptr::eq(zero.algebra(), &a));
        assert_eq!(zero.dimension(), 2);
        assert_eq!(zero.coefficient(0), Ok(0));
        assert_eq!(
            zero.coefficient(2),
            Err(AlgebraError::BasisOutOfBounds {
                index: 2,
                dimension: 2
            })
        );
        assert!(zero.coefficient(usize::MAX).is_err());
        assert_eq!(
            a.evaluate(
                &[&[1, 2]],
                AlgebraLimits {
                    max_field_operations: 8,
                    ..d
                }
            )
            .unwrap(),
            vec![2, 0]
        );
        assert!(a
            .evaluate(
                &[&[1, 2]],
                AlgebraLimits {
                    max_field_operations: 7,
                    ..d
                }
            )
            .is_err());
        assert_eq!(
            a.evaluate(
                &[&[1, 2], &[2, 1]],
                AlgebraLimits {
                    max_field_operations: 24,
                    ..d
                }
            )
            .unwrap(),
            vec![2, 2]
        );
        assert!(a
            .evaluate(
                &[&[1, 2], &[2, 1]],
                AlgebraLimits {
                    max_field_operations: 23,
                    ..d
                }
            )
            .is_err());
        assert_eq!(
            a.evaluate(
                &[],
                AlgebraLimits {
                    max_field_operations: 0,
                    ..d
                }
            )
            .unwrap(),
            vec![0, 0]
        );
    }
}
