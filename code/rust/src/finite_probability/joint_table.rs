
use linear_algebra::backend::basic_matrix::{BasicMatrix, MatrixError};
use linear_algebra::linear_algebra::image_kernel::{ExactLinearAlgebraError, ExactRowReduction};
use num_bigint::BigInt;
use num_traits::{One, Signed, Zero};
use tfqm_number_theory::rational::Rational;

use crate::error::ClassicalShadowError;
use crate::simplex::ProbabilitySimplex;
use crate::stochastic_map::StochasticMap;

#[derive(Debug, Clone, PartialEq, Eq, thiserror::Error)]
pub enum WeightTableError {
    #[error("a table needs at least one row and one column")]
    Empty,
    #[error("row {row} has {actual} entries, expected {expected}")]
    Ragged {
        row: usize,
        expected: usize,
        actual: usize,
    },
    #[error("weight at ({row}, {col}) is negative")]
    NegativeWeight { row: usize, col: usize },
    #[error("the total weight is zero")]
    ZeroTotal,
    #[error("cell ({row}, {col}) is outside a {rows}x{cols} table")]
    CellOutOfRange {
        row: usize,
        col: usize,
        rows: usize,
        cols: usize,
    },
    #[error("tables of shapes {left:?} and {right:?} cannot be combined")]
    ShapeMismatch {
        left: (usize, usize),
        right: (usize, usize),
    },
    #[error("a mixture needs at least one part")]
    EmptyMixture,
    #[error("mixture weight {index} is negative")]
    NegativeMixtureWeight { index: usize },
    #[error("mixture weights sum to {sum}, not one")]
    MixtureNotNormalized { sum: Rational },
    #[error("the map on side {side} has {actual} source states, the table side has {expected}")]
    MapShape {
        side: char,
        expected: usize,
        actual: usize,
    },
    #[error(
        "state {index} of side {side} has zero marginal mass, so its conditional is undetermined"
    )]
    ZeroMarginal { side: char, index: usize },
    #[error("the function on side {side} has {actual} values, the table side has {expected}")]
    FunctionLength {
        side: char,
        expected: usize,
        actual: usize,
    },
    #[error("probability refusal: {0}")]
    Probability(#[from] ClassicalShadowError),
    #[error("matrix storage refusal: {0}")]
    Matrix(#[from] MatrixError),
    #[error("linear algebra refusal: {0}")]
    LinearAlgebra(#[from] ExactLinearAlgebraError),
}

#[derive(Debug, Clone, PartialEq, Eq)]
pub struct JointTable {
    rows: usize,
    cols: usize,
    weights: Vec<Rational>,
}

#[derive(Debug, Clone, PartialEq, Eq)]
pub struct FrechetBounds {
    pub lower: Vec<Vec<Rational>>,
    pub upper: Vec<Vec<Rational>>,
}

fn two() -> Rational {
    Rational::from_integer(BigInt::from(2))
}

impl JointTable {
    pub fn new(rows: Vec<Vec<Rational>>) -> Result<Self, WeightTableError> {
        let n_rows = rows.len();
        let n_cols = rows.first().map_or(0, Vec::len);
        if n_rows == 0 || n_cols == 0 {
            return Err(WeightTableError::Empty);
        }
        let mut weights = Vec::with_capacity(n_rows * n_cols);
        for (row, entries) in rows.into_iter().enumerate() {
            if entries.len() != n_cols {
                return Err(WeightTableError::Ragged {
                    row,
                    expected: n_cols,
                    actual: entries.len(),
                });
            }
            for (col, w) in entries.into_iter().enumerate() {
                if w.is_negative() {
                    return Err(WeightTableError::NegativeWeight { row, col });
                }
                weights.push(w);
            }
        }
        let table = Self {
            rows: n_rows,
            cols: n_cols,
            weights,
        };
        if table.total().is_zero() {
            return Err(WeightTableError::ZeroTotal);
        }
        Ok(table)
    }

    pub fn point(rows: usize, cols: usize, a: usize, b: usize) -> Result<Self, WeightTableError> {
        if rows == 0 || cols == 0 {
            return Err(WeightTableError::Empty);
        }
        if a >= rows || b >= cols {
            return Err(WeightTableError::CellOutOfRange {
                row: a,
                col: b,
                rows,
                cols,
            });
        }
        Ok(Self::point_inside(rows, cols, a, b))
    }

    fn point_inside(rows: usize, cols: usize, a: usize, b: usize) -> Self {
        let mut weights = vec![Rational::zero(); rows * cols];
        weights[a * cols + b] = Rational::one();
        Self {
            rows,
            cols,
            weights,
        }
    }

    pub fn from_prior_and_kernel(
        prior: &ProbabilitySimplex,
        kernel: &StochasticMap,
    ) -> Result<Self, WeightTableError> {
        if kernel.source_n() != prior.n() {
            return Err(WeightTableError::MapShape {
                side: 'A',
                expected: prior.n(),
                actual: kernel.source_n(),
            });
        }
        let mut weights = Vec::with_capacity(prior.n() * kernel.target_n());
        for (p, row) in prior.probs().iter().zip(kernel.rows()) {
            for m in row {
                weights.push(p * m);
            }
        }
        Ok(Self {
            rows: prior.n(),
            cols: kernel.target_n(),
            weights,
        })
    }

    pub fn independent_coupling(pa: &ProbabilitySimplex, pb: &ProbabilitySimplex) -> Self {
        let mut weights = Vec::with_capacity(pa.n() * pb.n());
        for p in pa.probs() {
            for q in pb.probs() {
                weights.push(p * q);
            }
        }
        Self {
            rows: pa.n(),
            cols: pb.n(),
            weights,
        }
    }

    pub fn northwest_corner_coupling(pa: &ProbabilitySimplex, pb: &ProbabilitySimplex) -> Self {
        let (n, m) = (pa.n(), pb.n());
        let mut weights = vec![Rational::zero(); n * m];
        let (mut i, mut j) = (0usize, 0usize);
        let mut remaining_a = pa.probs()[0].clone();
        let mut remaining_b = pb.probs()[0].clone();
        while i < n && j < m {
            let moved = if remaining_a < remaining_b {
                remaining_a.clone()
            } else {
                remaining_b.clone()
            };
            weights[i * m + j] += &moved;
            remaining_a -= &moved;
            remaining_b -= &moved;
            if remaining_a.is_zero() {
                i += 1;
                if i < n {
                    remaining_a = pa.probs()[i].clone();
                }
            }
            if remaining_b.is_zero() {
                j += 1;
                if j < m {
                    remaining_b = pb.probs()[j].clone();
                }
            }
        }
        Self {
            rows: n,
            cols: m,
            weights,
        }
    }

    pub fn from_product_simplex(
        rows: usize,
        cols: usize,
        simplex: &ProbabilitySimplex,
    ) -> Result<Self, WeightTableError> {
        if rows == 0 || cols == 0 {
            return Err(WeightTableError::Empty);
        }
        let expected = crate::finite_set::checked_size_product(rows, cols)?;
        if simplex.n() != expected {
            return Err(ClassicalShadowError::DimensionMismatch {
                expected,
                actual: simplex.n(),
            }
            .into());
        }
        Ok(Self {
            rows,
            cols,
            weights: simplex.probs().to_vec(),
        })
    }

    pub fn shape(&self) -> (usize, usize) {
        (self.rows, self.cols)
    }

    pub fn weight(&self, a: usize, b: usize) -> Option<&Rational> {
        if a < self.rows && b < self.cols {
            Some(&self.weights[a * self.cols + b])
        } else {
            None
        }
    }

    pub fn weights(&self) -> &[Rational] {
        &self.weights
    }

    pub fn total(&self) -> Rational {
        self.weights.iter().sum()
    }

    pub fn marginal_a(&self) -> Vec<Rational> {
        self.weights
            .chunks(self.cols)
            .map(|row| row.iter().sum())
            .collect()
    }

    pub fn marginal_b(&self) -> Vec<Rational> {
        (0..self.cols)
            .map(|b| {
                (0..self.rows)
                    .map(|a| &self.weights[a * self.cols + b])
                    .sum()
            })
            .collect()
    }

    pub fn marginal_distribution_a(&self) -> Result<ProbabilitySimplex, WeightTableError> {
        Ok(ProbabilitySimplex::try_from_weights(self.marginal_a())?)
    }

    pub fn marginal_distribution_b(&self) -> Result<ProbabilitySimplex, WeightTableError> {
        Ok(ProbabilitySimplex::try_from_weights(self.marginal_b())?)
    }

    pub fn to_simplex(&self) -> Result<ProbabilitySimplex, WeightTableError> {
        Ok(ProbabilitySimplex::try_from_weights(self.weights.clone())?)
    }

    pub fn transpose(&self) -> Self {
        let mut weights = Vec::with_capacity(self.weights.len());
        for b in 0..self.cols {
            for a in 0..self.rows {
                weights.push(self.weights[a * self.cols + b].clone());
            }
        }
        Self {
            rows: self.cols,
            cols: self.rows,
            weights,
        }
    }

    pub fn conditional_b_given_a(&self) -> Result<StochasticMap, WeightTableError> {
        let marginal = self.marginal_a();
        let mut rows = Vec::with_capacity(self.rows);
        for (a, (chunk, wa)) in self.weights.chunks(self.cols).zip(&marginal).enumerate() {
            if wa.is_zero() {
                return Err(WeightTableError::ZeroMarginal {
                    side: 'A',
                    index: a,
                });
            }
            rows.push(chunk.iter().map(|w| w / wa).collect());
        }
        Ok(StochasticMap::try_from_rows(
            self.rows, self.cols, rows, "P(B|A)",
        )?)
    }

    pub fn conditional_a_given_b(&self) -> Result<StochasticMap, WeightTableError> {
        self.transpose()
            .conditional_b_given_a()
            .map_err(|error| match error {
                WeightTableError::ZeroMarginal { index, .. } => {
                    WeightTableError::ZeroMarginal { side: 'B', index }
                }
                other => other,
            })
    }

    pub fn product_defect(&self) -> Vec<Vec<Rational>> {
        let total = self.total();
        let (ma, mb) = (self.marginal_a(), self.marginal_b());
        (0..self.rows)
            .map(|a| {
                (0..self.cols)
                    .map(|b| &self.weights[a * self.cols + b] - &ma[a] * &mb[b] / &total)
                    .collect()
            })
            .collect()
    }

    pub fn product_defect_mass(&self) -> Rational {
        self.product_defect()
            .iter()
            .flatten()
            .map(Signed::abs)
            .sum()
    }

    pub fn dependence_total_variation(&self) -> Rational {
        self.product_defect_mass() / (two() * self.total())
    }

    pub fn has_vanishing_minors(&self) -> bool {
        let w = |a: usize, b: usize| &self.weights[a * self.cols + b];
        (0..self.rows).all(|a| {
            ((a + 1)..self.rows).all(|a2| {
                (0..self.cols).all(|b| {
                    ((b + 1)..self.cols).all(|b2| w(a, b) * w(a2, b2) == w(a, b2) * w(a2, b))
                })
            })
        })
    }

    pub fn is_independent(&self) -> bool {
        let pivot = self
            .weights
            .iter()
            .position(|w| w.is_positive())
            .map(|k| (k / self.cols, k % self.cols));
        let Some((r, c)) = pivot else {
            return false;
        };
        let pivot_weight = &self.weights[r * self.cols + c];
        (0..self.rows).all(|a| {
            let ratio = &self.weights[a * self.cols + c] / pivot_weight;
            (0..self.cols).all(|b| {
                self.weights[a * self.cols + b] == &ratio * &self.weights[r * self.cols + b]
            })
        })
    }

    pub fn rank(&self) -> Result<usize, WeightTableError> {
        let matrix = BasicMatrix::from_row_major(self.rows, self.cols, self.weights.clone())?;
        Ok(matrix.rank()?)
    }

    pub fn factor_marginals(
        &self,
    ) -> Result<Option<(ProbabilitySimplex, ProbabilitySimplex)>, WeightTableError> {
        if !self.is_independent() {
            return Ok(None);
        }
        Ok(Some((
            self.marginal_distribution_a()?,
            self.marginal_distribution_b()?,
        )))
    }

    pub fn chi_square_statistic(&self) -> Rational {
        let total = self.total();
        let (ma, mb) = (self.marginal_a(), self.marginal_b());
        let mut statistic = Rational::zero();
        for a in 0..self.rows {
            for b in 0..self.cols {
                if ma[a].is_zero() || mb[b].is_zero() {
                    continue;
                }
                let expected = &ma[a] * &mb[b] / &total;
                let gap = &self.weights[a * self.cols + b] - &expected;
                statistic += &gap * &gap / &expected;
            }
        }
        statistic
    }

    pub fn expectation_of_product(
        &self,
        f: &[Rational],
        g: &[Rational],
    ) -> Result<Rational, WeightTableError> {
        self.check_function_lengths(f, g)?;
        let total = self.total();
        let mut sum = Rational::zero();
        for (a, fa) in f.iter().enumerate() {
            for (b, gb) in g.iter().enumerate() {
                sum += &self.weights[a * self.cols + b] * fa * gb;
            }
        }
        Ok(sum / total)
    }

    pub fn covariance(&self, f: &[Rational], g: &[Rational]) -> Result<Rational, WeightTableError> {
        self.check_function_lengths(f, g)?;
        let total = self.total();
        let mean_f: Rational = self
            .marginal_a()
            .iter()
            .zip(f)
            .map(|(w, v)| w * v)
            .sum::<Rational>()
            / &total;
        let mean_g: Rational = self
            .marginal_b()
            .iter()
            .zip(g)
            .map(|(w, v)| w * v)
            .sum::<Rational>()
            / &total;
        Ok(self.expectation_of_product(f, g)? - mean_f * mean_g)
    }

    fn check_function_lengths(
        &self,
        f: &[Rational],
        g: &[Rational],
    ) -> Result<(), WeightTableError> {
        if f.len() != self.rows {
            return Err(WeightTableError::FunctionLength {
                side: 'A',
                expected: self.rows,
                actual: f.len(),
            });
        }
        if g.len() != self.cols {
            return Err(WeightTableError::FunctionLength {
                side: 'B',
                expected: self.cols,
                actual: g.len(),
            });
        }
        Ok(())
    }

    pub fn normalized(&self) -> Self {
        let total = self.total();
        Self {
            rows: self.rows,
            cols: self.cols,
            weights: self.weights.iter().map(|w| w / &total).collect(),
        }
    }

    pub fn point_product_decomposition(&self) -> Vec<(Rational, JointTable)> {
        let total = self.total();
        let mut parts = Vec::new();
        for a in 0..self.rows {
            for b in 0..self.cols {
                let w = &self.weights[a * self.cols + b];
                if w.is_positive() {
                    parts.push((w / &total, Self::point_inside(self.rows, self.cols, a, b)));
                }
            }
        }
        parts
    }

    pub fn convex_mixture(parts: &[(Rational, JointTable)]) -> Result<Self, WeightTableError> {
        let shape = parts
            .first()
            .ok_or(WeightTableError::EmptyMixture)?
            .1
            .shape();
        let mut sum = Rational::zero();
        let mut weights = vec![Rational::zero(); shape.0 * shape.1];
        for (index, (q, table)) in parts.iter().enumerate() {
            if q.is_negative() {
                return Err(WeightTableError::NegativeMixtureWeight { index });
            }
            if table.shape() != shape {
                return Err(WeightTableError::ShapeMismatch {
                    left: shape,
                    right: table.shape(),
                });
            }
            sum += q;
            for (acc, w) in weights.iter_mut().zip(&table.weights) {
                *acc += q * w;
            }
        }
        if !sum.is_one() {
            return Err(WeightTableError::MixtureNotNormalized { sum });
        }
        Ok(Self {
            rows: shape.0,
            cols: shape.1,
            weights,
        })
    }

    pub fn l1_distance(&self, other: &Self) -> Result<Rational, WeightTableError> {
        if self.shape() != other.shape() {
            return Err(WeightTableError::ShapeMismatch {
                left: self.shape(),
                right: other.shape(),
            });
        }
        Ok(self
            .weights
            .iter()
            .zip(&other.weights)
            .map(|(x, y)| (x - y).abs())
            .sum())
    }

    pub fn apply_local_maps(
        &self,
        g_a: &StochasticMap,
        g_b: &StochasticMap,
    ) -> Result<Self, WeightTableError> {
        if g_a.source_n() != self.rows {
            return Err(WeightTableError::MapShape {
                side: 'A',
                expected: self.rows,
                actual: g_a.source_n(),
            });
        }
        if g_b.source_n() != self.cols {
            return Err(WeightTableError::MapShape {
                side: 'B',
                expected: self.cols,
                actual: g_b.source_n(),
            });
        }
        let (ka, kb) = (g_a.rows(), g_b.rows());
        let (rows, cols) = (g_a.target_n(), g_b.target_n());
        let mut weights = vec![Rational::zero(); rows * cols];
        for (row, ka_row) in self.weights.chunks(self.cols).zip(ka) {
            for (w, kb_row) in row.iter().zip(kb) {
                if w.is_zero() {
                    continue;
                }
                for (a2, pa) in ka_row.iter().enumerate() {
                    let wa = w * pa;
                    for (b2, pb) in kb_row.iter().enumerate() {
                        weights[a2 * cols + b2] += &wa * pb;
                    }
                }
            }
        }
        Ok(Self {
            rows,
            cols,
            weights,
        })
    }
}

pub fn frechet_bounds(pa: &ProbabilitySimplex, pb: &ProbabilitySimplex) -> FrechetBounds {
    let one = Rational::one();
    let mut lower = Vec::with_capacity(pa.n());
    let mut upper = Vec::with_capacity(pa.n());
    for p in pa.probs() {
        let mut lo_row = Vec::with_capacity(pb.n());
        let mut hi_row = Vec::with_capacity(pb.n());
        for q in pb.probs() {
            let floor = p + q - &one;
            lo_row.push(if floor.is_positive() {
                floor
            } else {
                Rational::zero()
            });
            hi_row.push(if p < q { p.clone() } else { q.clone() });
        }
        lower.push(lo_row);
        upper.push(hi_row);
    }
    FrechetBounds { lower, upper }
}

#[cfg(test)]
mod tests {
    use super::*;
    use crate::finite_set::FinN;
    use crate::test_support::{compositions, simplex, stochastic};
    use tfqm_number_theory::rational::{ri, rq};

    fn table(rows: &[&[i64]]) -> JointTable {
        JointTable::new(
            rows.iter()
                .map(|r| r.iter().map(|&v| ri(v)).collect())
                .collect(),
        )
        .unwrap()
    }

    fn all_tables(r: usize, c: usize, max: i64) -> Vec<JointTable> {
        let cells = r * c;
        let mut out = Vec::new();
        let mut digits = vec![0i64; cells];
        loop {
            if digits.iter().any(|&d| d != 0) {
                let rows: Vec<Vec<Rational>> = digits
                    .chunks(c)
                    .map(|chunk| chunk.iter().map(|&d| ri(d)).collect())
                    .collect();
                out.push(JointTable::new(rows).unwrap());
            }
            let mut k = 0;
            while k < cells {
                digits[k] += 1;
                if digits[k] <= max {
                    break;
                }
                digits[k] = 0;
                k += 1;
            }
            if k == cells {
                return out;
            }
        }
    }


    #[test]
    fn a_table_is_refused_when_empty_ragged_negative_or_zero() {
        assert_eq!(JointTable::new(vec![]), Err(WeightTableError::Empty));
        assert_eq!(JointTable::new(vec![vec![]]), Err(WeightTableError::Empty));
        assert_eq!(
            JointTable::new(vec![vec![ri(1), ri(1)], vec![ri(1)]]),
            Err(WeightTableError::Ragged {
                row: 1,
                expected: 2,
                actual: 1
            })
        );
        assert_eq!(
            JointTable::new(vec![vec![ri(1), ri(-1)]]),
            Err(WeightTableError::NegativeWeight { row: 0, col: 1 })
        );
        assert_eq!(
            JointTable::new(vec![vec![ri(0); 2]; 2]),
            Err(WeightTableError::ZeroTotal)
        );
    }

    #[test]
    fn a_point_table_is_refused_outside_its_shape() {
        assert_eq!(
            JointTable::point(2, 2, 2, 0),
            Err(WeightTableError::CellOutOfRange {
                row: 2,
                col: 0,
                rows: 2,
                cols: 2
            })
        );
        assert_eq!(JointTable::point(0, 2, 0, 0), Err(WeightTableError::Empty));
        let e = JointTable::point(2, 3, 1, 2).unwrap();
        assert_eq!(e.total(), ri(1));
        assert_eq!(e.weight(1, 2), Some(&ri(1)));
        assert_eq!(e.weight(0, 0), Some(&ri(0)));
        assert_eq!(e.weight(2, 0), None);
    }


    #[test]
    fn marginals_and_total_have_their_hand_values() {
        let t = table(&[&[1, 2, 3], &[4, 5, 6]]);
        assert_eq!(t.total(), ri(21));
        assert_eq!(t.marginal_a(), vec![ri(6), ri(15)]);
        assert_eq!(t.marginal_b(), vec![ri(5), ri(7), ri(9)]);
        assert_eq!(
            t.marginal_distribution_a().unwrap().probs(),
            &[rq(6, 21), rq(15, 21)]
        );
        assert_eq!(t.transpose().marginal_a(), t.marginal_b());
        assert_eq!(t.transpose().transpose(), t);
    }

    #[test]
    fn the_defect_has_zero_row_and_column_sums() {
        for t in all_tables(2, 3, 2) {
            let delta = t.product_defect();
            for row in &delta {
                assert_eq!(row.iter().sum::<Rational>(), ri(0), "row sums");
            }
            for b in 0..3 {
                assert_eq!(
                    delta.iter().map(|r| &r[b]).sum::<Rational>(),
                    ri(0),
                    "column sums"
                );
            }
        }
    }

    #[test]
    fn conditionals_of_a_joint_built_from_a_prior_and_a_kernel_return_that_kernel() {
        let prior = simplex(&[(1, 2), (1, 3), (1, 6)]);
        let kernel = stochastic(&[
            &[(1, 2), (1, 3), (1, 6)],
            &[(1, 4), (1, 4), (1, 2)],
            &[(2, 5), (1, 5), (2, 5)],
        ]);
        let joint = JointTable::from_prior_and_kernel(&prior, &kernel).unwrap();
        assert_eq!(joint.total(), ri(1));
        assert_eq!(joint.marginal_distribution_a().unwrap(), prior);
        assert_eq!(joint.conditional_b_given_a().unwrap(), kernel);
        let (marginal, posterior) = kernel.bayesian_inverse(&prior).unwrap();
        assert_eq!(joint.marginal_distribution_b().unwrap(), marginal);
        assert_eq!(joint.conditional_a_given_b().unwrap(), posterior);
    }

    #[test]
    fn a_conditional_of_a_zero_mass_state_is_refused_and_a_prior_kernel_mismatch_too() {
        let t = table(&[&[1, 1], &[0, 0], &[2, 2]]);
        assert_eq!(
            t.conditional_b_given_a(),
            Err(WeightTableError::ZeroMarginal {
                side: 'A',
                index: 1
            })
        );
        let u = table(&[&[1, 0, 1], &[1, 0, 1]]);
        assert_eq!(
            u.conditional_a_given_b(),
            Err(WeightTableError::ZeroMarginal {
                side: 'B',
                index: 1
            })
        );
        let prior = simplex(&[(1, 2), (1, 2)]);
        let kernel = stochastic(&[&[(1, 1)], &[(1, 1)], &[(1, 1)]]);
        assert_eq!(
            JointTable::from_prior_and_kernel(&prior, &kernel),
            Err(WeightTableError::MapShape {
                side: 'A',
                expected: 2,
                actual: 3
            })
        );
    }

    #[test]
    fn a_table_round_trips_through_a_simplex_on_the_product_carrier() {
        let t = table(&[&[1, 2, 3], &[4, 5, 6]]).normalized();
        let s = t.to_simplex().unwrap();
        assert_eq!(s.n(), 6);
        assert_eq!(JointTable::from_product_simplex(2, 3, &s).unwrap(), t);
        assert_eq!(
            JointTable::from_product_simplex(2, 2, &s),
            Err(WeightTableError::Probability(
                ClassicalShadowError::DimensionMismatch {
                    expected: 4,
                    actual: 6
                }
            ))
        );
        assert_eq!(
            JointTable::from_product_simplex(0, 2, &s),
            Err(WeightTableError::Empty)
        );
    }


    fn independence_decisions(t: &JointTable) -> [bool; 7] {
        let indicator = |n: usize, k: usize| -> Vec<Rational> {
            (0..n).map(|i| if i == k { ri(1) } else { ri(0) }).collect()
        };
        let (rows, cols) = t.shape();
        let all_indicator_covariances_vanish = (0..rows).all(|a| {
            (0..cols).all(|b| {
                t.covariance(&indicator(rows, a), &indicator(cols, b))
                    .unwrap()
                    .is_zero()
            })
        });
        [
            t.product_defect_mass().is_zero(),
            t.has_vanishing_minors(),
            t.is_independent(),
            t.rank().unwrap() == 1,
            t.chi_square_statistic().is_zero(),
            all_indicator_covariances_vanish,
            t.factor_marginals().unwrap().is_some(),
        ]
    }

    #[test]
    fn seven_independent_decisions_of_independence_agree_on_every_small_table() {
        let mut independent = 0;
        let mut dependent = 0;
        for (r, c) in [(2, 2), (2, 3), (3, 2)] {
            for t in all_tables(r, c, 2) {
                let decisions = independence_decisions(&t);
                assert!(
                    decisions.iter().all(|&d| d == decisions[0]),
                    "decisions {decisions:?} disagree on {:?}",
                    t.weights()
                );
                if decisions[0] {
                    independent += 1;
                } else {
                    dependent += 1;
                }
            }
        }
        assert!(
            independent > 10 && dependent > 10,
            "{independent} / {dependent}"
        );
    }

    #[test]
    fn a_table_that_factors_has_its_marginals_as_factors_and_reassembles_from_them() {
        let t = table(&[&[2, 4, 6], &[1, 2, 3]]);
        assert!(t.is_independent());
        let (pa, pb) = t.factor_marginals().unwrap().unwrap();
        let rebuilt = JointTable::independent_coupling(&pa, &pb);
        assert_eq!(rebuilt, t.normalized());
        assert_eq!(t.product_defect_mass(), ri(0));
        assert_eq!(t.dependence_total_variation(), ri(0));
        assert_eq!(t.rank().unwrap(), 1);
    }

    #[test]
    fn the_pearson_statistic_of_a_two_by_two_table_is_its_closed_form() {
        for t in all_tables(2, 2, 3) {
            let (ma, mb) = (t.marginal_a(), t.marginal_b());
            if ma.iter().chain(&mb).any(Zero::is_zero) {
                continue;
            }
            let w = |a, b| t.weight(a, b).unwrap().clone();
            let det = w(0, 0) * w(1, 1) - w(0, 1) * w(1, 0);
            let closed = t.total() * &det * &det / (&ma[0] * &ma[1] * &mb[0] * &mb[1]);
            assert_eq!(t.chi_square_statistic(), closed, "{:?}", t.weights());
        }
        assert_eq!(table(&[&[2, 1], &[1, 2]]).chi_square_statistic(), rq(2, 3));
    }

    #[test]
    fn a_zero_marginal_cell_does_not_enter_the_pearson_statistic() {
        let t = table(&[&[3, 0, 1], &[1, 0, 3]]);
        let statistic = t.chi_square_statistic();
        let trimmed = table(&[&[3, 1], &[1, 3]]);
        assert_eq!(statistic, trimmed.chi_square_statistic());
        assert!(statistic.is_positive());
    }

    #[test]
    fn dependence_total_variation_is_a_fraction_of_one_and_zero_only_for_products() {
        for t in all_tables(2, 2, 3) {
            let d = t.dependence_total_variation();
            assert!(d >= ri(0) && d < ri(1), "{d}");
            assert_eq!(d.is_zero(), t.is_independent());
        }
        assert_eq!(
            table(&[&[1, 0], &[0, 1]]).dependence_total_variation(),
            rq(1, 2)
        );
    }

    #[test]
    fn covariance_vanishes_on_products_for_every_pair_of_functions_but_not_conversely_for_one_pair()
    {
        let product = table(&[&[2, 4], &[1, 2]]);
        let functions = [
            vec![ri(1), ri(0)],
            vec![ri(3), ri(-2)],
            vec![rq(1, 2), rq(5, 7)],
        ];
        for f in &functions {
            for g in &functions {
                assert_eq!(product.covariance(f, g).unwrap(), ri(0));
            }
        }
        let diagonal = table(&[&[1, 0], &[0, 1]]);
        assert!(!diagonal.is_independent());
        assert_eq!(
            diagonal
                .covariance(&[ri(1), ri(1)], &[ri(1), ri(0)])
                .unwrap(),
            ri(0)
        );
        assert_eq!(
            diagonal
                .covariance(&[ri(1), ri(0)], &[ri(1), ri(0)])
                .unwrap(),
            rq(1, 4)
        );
        assert_eq!(
            diagonal.covariance(&[ri(1)], &[ri(1), ri(0)]),
            Err(WeightTableError::FunctionLength {
                side: 'A',
                expected: 2,
                actual: 1
            })
        );
        assert_eq!(
            diagonal.covariance(&[ri(1), ri(0)], &[ri(1)]),
            Err(WeightTableError::FunctionLength {
                side: 'B',
                expected: 2,
                actual: 1
            })
        );
    }

    #[test]
    fn the_covariance_of_indicators_is_the_normalised_product_defect() {
        for t in all_tables(2, 3, 2) {
            let delta = t.product_defect();
            for a in 0..2 {
                for b in 0..3 {
                    let fa: Vec<Rational> =
                        (0..2).map(|i| if i == a { ri(1) } else { ri(0) }).collect();
                    let gb: Vec<Rational> =
                        (0..3).map(|j| if j == b { ri(1) } else { ri(0) }).collect();
                    assert_eq!(t.covariance(&fa, &gb).unwrap() * t.total(), delta[a][b]);
                }
            }
        }
    }


    #[test]
    fn the_point_product_decomposition_reassembles_the_normalised_table() {
        for t in all_tables(2, 2, 2) {
            let parts = t.point_product_decomposition();
            assert_eq!(parts.iter().map(|(w, _)| w).sum::<Rational>(), ri(1));
            assert_eq!(JointTable::convex_mixture(&parts).unwrap(), t.normalized());
        }
    }

    #[test]
    fn mixtures_are_refused_when_empty_misweighted_or_misshaped() {
        let a = table(&[&[1, 0], &[0, 1]]);
        let b = table(&[&[1, 1], &[1, 1]]);
        assert_eq!(
            JointTable::convex_mixture(&[]),
            Err(WeightTableError::EmptyMixture)
        );
        assert_eq!(
            JointTable::convex_mixture(&[(rq(3, 2), a.clone()), (rq(-1, 2), b.clone())]),
            Err(WeightTableError::NegativeMixtureWeight { index: 1 })
        );
        assert_eq!(
            JointTable::convex_mixture(&[(rq(1, 2), a.clone()), (rq(1, 4), b.clone())]),
            Err(WeightTableError::MixtureNotNormalized { sum: rq(3, 4) })
        );
        let wide = table(&[&[1, 1, 1], &[1, 1, 1]]);
        assert_eq!(
            JointTable::convex_mixture(&[(rq(1, 2), a), (rq(1, 2), wide)]),
            Err(WeightTableError::ShapeMismatch {
                left: (2, 2),
                right: (2, 3)
            })
        );
    }

    #[test]
    fn the_l1_distance_is_a_metric_on_small_tables() {
        let tables = all_tables(2, 2, 1);
        for x in &tables {
            assert_eq!(x.l1_distance(x).unwrap(), ri(0));
            for y in &tables {
                let d = x.l1_distance(y).unwrap();
                assert_eq!(d, y.l1_distance(x).unwrap());
                assert_eq!(d.is_zero(), x == y);
                for z in &tables {
                    assert!(d <= x.l1_distance(z).unwrap() + z.l1_distance(y).unwrap());
                }
            }
        }
        assert_eq!(
            tables[0].l1_distance(&table(&[&[1, 1, 1]])),
            Err(WeightTableError::ShapeMismatch {
                left: (2, 2),
                right: (1, 3)
            })
        );
    }


    #[test]
    fn local_maps_preserve_the_total_and_the_identity_acts_trivially() {
        let t = table(&[&[1, 2], &[3, 4]]);
        let id = StochasticMap::identity(&FinN::try_new(2).unwrap(), "id").unwrap();
        assert_eq!(t.apply_local_maps(&id, &id).unwrap(), t);
        let noisy = stochastic(&[&[(1, 2), (1, 2), (0, 1)], &[(0, 1), (1, 3), (2, 3)]]);
        let out = t.apply_local_maps(&noisy, &id).unwrap();
        assert_eq!(out.shape(), (3, 2));
        assert_eq!(out.total(), t.total());
    }

    #[test]
    fn maps_of_the_wrong_source_size_are_refused_on_either_side() {
        let t = table(&[&[1, 2], &[3, 4]]);
        let id2 = StochasticMap::identity(&FinN::try_new(2).unwrap(), "id").unwrap();
        let id3 = StochasticMap::identity(&FinN::try_new(3).unwrap(), "id").unwrap();
        assert_eq!(
            t.apply_local_maps(&id3, &id2),
            Err(WeightTableError::MapShape {
                side: 'A',
                expected: 2,
                actual: 3
            })
        );
        assert_eq!(
            t.apply_local_maps(&id2, &id3),
            Err(WeightTableError::MapShape {
                side: 'B',
                expected: 2,
                actual: 3
            })
        );
    }

    #[test]
    fn no_local_stochastic_map_can_increase_the_dependence_total_variation() {
        let local_maps = [
            stochastic(&[&[(1, 2), (1, 2)], &[(1, 3), (2, 3)]]),
            stochastic(&[&[(1, 1), (0, 1)], &[(1, 1), (0, 1)]]),
            stochastic(&[&[(0, 1), (1, 1)], &[(1, 1), (0, 1)]]),
            stochastic(&[&[(1, 4), (3, 4)], &[(3, 4), (1, 4)]]),
        ];
        for t in all_tables(2, 2, 2) {
            let before = t.dependence_total_variation();
            for ga in &local_maps {
                for gb in &local_maps {
                    let after = t
                        .apply_local_maps(ga, gb)
                        .unwrap()
                        .dependence_total_variation();
                    assert!(after <= before, "{after} > {before} on {:?}", t.weights());
                }
            }
        }
        let t = table(&[&[1, 0], &[0, 1]]);
        let constant = stochastic(&[&[(1, 2), (1, 2)], &[(1, 2), (1, 2)]]);
        let id = StochasticMap::identity(&FinN::try_new(2).unwrap(), "id").unwrap();
        assert_eq!(
            t.apply_local_maps(&constant, &id)
                .unwrap()
                .dependence_total_variation(),
            ri(0)
        );
    }


    #[test]
    fn the_independent_coupling_has_the_given_marginals_and_zero_defect() {
        let pa = simplex(&[(1, 2), (1, 3), (1, 6)]);
        let pb = simplex(&[(1, 4), (3, 4)]);
        let c = JointTable::independent_coupling(&pa, &pb);
        assert_eq!(c.marginal_distribution_a().unwrap(), pa);
        assert_eq!(c.marginal_distribution_b().unwrap(), pb);
        assert!(c.is_independent());
    }

    #[test]
    fn the_northwest_corner_coupling_has_the_marginals_and_a_small_support() {
        let grid: Vec<ProbabilitySimplex> = (1..=3)
            .flat_map(|n| {
                compositions(4, n)
                    .into_iter()
                    .map(|c| {
                        ProbabilitySimplex::try_new(c.into_iter().map(|k| rq(k, 4)).collect())
                            .unwrap()
                    })
                    .collect::<Vec<_>>()
            })
            .collect();
        for pa in &grid {
            for pb in &grid {
                let c = JointTable::northwest_corner_coupling(pa, pb);
                assert_eq!(c.shape(), (pa.n(), pb.n()));
                assert_eq!(c.marginal_a(), pa.probs().to_vec());
                assert_eq!(c.marginal_b(), pb.probs().to_vec());
                let support = c.weights().iter().filter(|w| w.is_positive()).count();
                assert!(
                    support < pa.n() + pb.n(),
                    "support {support} of a {}x{} table",
                    pa.n(),
                    pb.n()
                );
            }
        }
        let c = JointTable::northwest_corner_coupling(
            &simplex(&[(1, 2), (1, 2)]),
            &simplex(&[(1, 4), (3, 4)]),
        );
        assert_eq!(c.weights(), &[rq(1, 4), rq(1, 4), ri(0), rq(1, 2)]);
    }

    #[test]
    fn every_joint_table_respects_the_frechet_bounds_and_each_bound_is_attained() {
        let grid = compositions(4, 2);
        for x in &grid {
            for y in &grid {
                let pa =
                    ProbabilitySimplex::try_new(x.iter().map(|&k| rq(k, 4)).collect()).unwrap();
                let pb =
                    ProbabilitySimplex::try_new(y.iter().map(|&k| rq(k, 4)).collect()).unwrap();
                let bounds = frechet_bounds(&pa, &pb);
                let mut seen_lower = false;
                let mut seen_upper = false;
                for t in 0..=4i64 {
                    let p00 = rq(t, 4);
                    let p01 = pa.probs()[0].clone() - &p00;
                    let p10 = pb.probs()[0].clone() - &p00;
                    let p11 = pa.probs()[1].clone() - &p10;
                    let cells = [[p00, p01], [p10, p11]];
                    if cells.iter().flatten().any(Signed::is_negative) {
                        continue;
                    }
                    for a in 0..2 {
                        for b in 0..2 {
                            assert!(
                                cells[a][b] >= bounds.lower[a][b],
                                "lower bound at ({a}, {b})"
                            );
                            assert!(
                                cells[a][b] <= bounds.upper[a][b],
                                "upper bound at ({a}, {b})"
                            );
                        }
                    }
                    seen_lower |= cells[0][0] == bounds.lower[0][0];
                    seen_upper |= cells[0][0] == bounds.upper[0][0];
                }
                assert!(
                    seen_lower && seen_upper,
                    "bounds on cell (0,0) are not attained"
                );
            }
        }
    }

    #[test]
    fn frechet_bounds_have_their_hand_values() {
        let pa = simplex(&[(3, 4), (1, 4)]);
        let pb = simplex(&[(2, 3), (1, 3)]);
        let b = frechet_bounds(&pa, &pb);
        assert_eq!(b.lower[0][0], rq(5, 12));
        assert_eq!(b.upper[0][0], rq(2, 3));
        assert_eq!(b.lower[1][1], ri(0));
        assert_eq!(b.upper[1][1], rq(1, 4));
    }
}
