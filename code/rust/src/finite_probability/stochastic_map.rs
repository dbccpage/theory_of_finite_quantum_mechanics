
use linear_algebra::backend::basic_matrix::BasicMatrix;
use num_bigint::BigInt;
use num_traits::{One, Signed, Zero};
use omega_number_theory::rational::Rational;

use crate::error::ClassicalShadowError;
use crate::finite_set::{checked_size_product, FinN};
use crate::simplex::ProbabilitySimplex;

#[derive(Debug, Clone)]
pub struct StochasticMap {
    source_n: usize,
    target_n: usize,
    rows: Vec<Vec<Rational>>,
    label: String,
}

impl PartialEq for StochasticMap {
    fn eq(&self, other: &Self) -> bool {
        self.source_n == other.source_n
            && self.target_n == other.target_n
            && self.rows == other.rows
    }
}

impl Eq for StochasticMap {}

fn half() -> Rational {
    Rational::new(BigInt::one(), BigInt::from(2))
}

impl StochasticMap {
    pub fn try_from_rows(
        source_n: usize,
        target_n: usize,
        rows: Vec<Vec<Rational>>,
        label: impl Into<String>,
    ) -> Result<Self, ClassicalShadowError> {
        if source_n == 0 || target_n == 0 {
            return Err(ClassicalShadowError::ZeroCardinality);
        }
        if rows.len() != source_n {
            return Err(ClassicalShadowError::DimensionMismatch {
                expected: source_n,
                actual: rows.len(),
            });
        }
        for (i, row) in rows.iter().enumerate() {
            if row.len() != target_n {
                return Err(ClassicalShadowError::DimensionMismatch {
                    expected: target_n,
                    actual: row.len(),
                });
            }
            let mut sum = Rational::zero();
            for (j, e) in row.iter().enumerate() {
                if e.is_negative() {
                    return Err(ClassicalShadowError::NegativeEntry {
                        index: i * target_n + j,
                    });
                }
                sum += e;
            }
            if !sum.is_one() {
                return Err(ClassicalShadowError::RowNotNormalized { row: i, sum });
            }
        }
        Ok(Self {
            source_n,
            target_n,
            rows,
            label: label.into(),
        })
    }

    pub fn from_conditionals(
        conditionals: &[ProbabilitySimplex],
        label: impl Into<String>,
    ) -> Result<Self, ClassicalShadowError> {
        let first = conditionals.first().ok_or(ClassicalShadowError::Empty)?;
        let rows = conditionals
            .iter()
            .map(|c| c.probs().to_vec())
            .collect::<Vec<_>>();
        Self::try_from_rows(conditionals.len(), first.n(), rows, label)
    }

    pub fn from_function(
        target_n: usize,
        images: &[usize],
        label: impl Into<String>,
    ) -> Result<Self, ClassicalShadowError> {
        if images.is_empty() || target_n == 0 {
            return Err(ClassicalShadowError::ZeroCardinality);
        }
        let mut rows = Vec::with_capacity(images.len());
        for &image in images {
            if image >= target_n {
                return Err(ClassicalShadowError::IndexOutOfRange {
                    index: image,
                    bound: target_n,
                });
            }
            let mut row = vec![Rational::zero(); target_n];
            row[image] = Rational::one();
            rows.push(row);
        }
        Self::try_from_rows(images.len(), target_n, rows, label)
    }

    pub fn permutation(
        images: &[usize],
        label: impl Into<String>,
    ) -> Result<Self, ClassicalShadowError> {
        let n = images.len();
        let mut seen = vec![false; n];
        for (position, &image) in images.iter().enumerate() {
            if image >= n || seen[image] {
                return Err(ClassicalShadowError::NotAPermutation { position });
            }
            seen[image] = true;
        }
        Self::from_function(n, images, label)
    }

    pub fn constant(
        source_n: usize,
        distribution: &ProbabilitySimplex,
        label: impl Into<String>,
    ) -> Result<Self, ClassicalShadowError> {
        if source_n == 0 {
            return Err(ClassicalShadowError::ZeroCardinality);
        }
        let rows = vec![distribution.probs().to_vec(); source_n];
        Self::try_from_rows(source_n, distribution.n(), rows, label)
    }

    pub fn identity(
        carrier: &FinN,
        label: impl Into<String>,
    ) -> Result<Self, ClassicalShadowError> {
        let n = carrier.cardinality();
        let images: Vec<usize> = (0..n).collect();
        Self::from_function(n, &images, label)
    }

    pub fn copy(n: usize) -> Result<Self, ClassicalShadowError> {
        let size = checked_size_product(n, n)?;
        let images: Vec<usize> = (0..n).map(|i| i * n + i).collect();
        Self::from_function(size, &images, "copy")
    }

    pub fn discard(n: usize) -> Result<Self, ClassicalShadowError> {
        Self::from_function(1, &vec![0; n], "discard")
    }

    pub fn first_projection(n: usize, m: usize) -> Result<Self, ClassicalShadowError> {
        let size = checked_size_product(n, m)?;
        let images: Vec<usize> = (0..size).map(|k| k / m).collect();
        Self::from_function(n, &images, "first projection")
    }

    pub fn second_projection(n: usize, m: usize) -> Result<Self, ClassicalShadowError> {
        let size = checked_size_product(n, m)?;
        let images: Vec<usize> = (0..size).map(|k| k % m).collect();
        Self::from_function(m, &images, "second projection")
    }

    pub fn swap(n: usize, m: usize) -> Result<Self, ClassicalShadowError> {
        let size = checked_size_product(n, m)?;
        let images: Vec<usize> = (0..size).map(|k| (k % m) * n + k / m).collect();
        Self::from_function(size, &images, "swap")
    }

    pub fn source_n(&self) -> usize {
        self.source_n
    }

    pub fn target_n(&self) -> usize {
        self.target_n
    }

    pub fn rows(&self) -> &[Vec<Rational>] {
        &self.rows
    }

    pub fn label(&self) -> &str {
        &self.label
    }

    pub fn get(&self, i: usize, j: usize) -> Option<Rational> {
        self.rows.get(i).and_then(|r| r.get(j).cloned())
    }

    pub fn conditional(&self, i: usize) -> Result<ProbabilitySimplex, ClassicalShadowError> {
        let row = self
            .rows
            .get(i)
            .ok_or(ClassicalShadowError::IndexOutOfRange {
                index: i,
                bound: self.source_n,
            })?;
        ProbabilitySimplex::try_new(row.clone())
    }

    pub fn is_endomorphism(&self) -> bool {
        self.source_n == self.target_n
    }

    pub fn apply(
        &self,
        p: &ProbabilitySimplex,
    ) -> Result<ProbabilitySimplex, ClassicalShadowError> {
        if p.n() != self.source_n {
            return Err(ClassicalShadowError::ShapeMismatch {
                left: p.n(),
                right: self.source_n,
            });
        }
        let mut out = vec![Rational::zero(); self.target_n];
        for (pi, row) in p.probs().iter().zip(&self.rows) {
            for (acc, e) in out.iter_mut().zip(row) {
                *acc += pi * e;
            }
        }
        let target = FinN::try_new(self.target_n)?;
        ProbabilitySimplex::try_from_probs(&target, out, format!("{}o{}", self.label, p.label()))
    }

    pub fn pullback(&self, values: &[Rational]) -> Result<Vec<Rational>, ClassicalShadowError> {
        if values.len() != self.target_n {
            return Err(ClassicalShadowError::DimensionMismatch {
                expected: self.target_n,
                actual: values.len(),
            });
        }
        Ok(self
            .rows
            .iter()
            .map(|row| row.iter().zip(values).map(|(m, f)| m * f).sum())
            .collect())
    }

    pub fn compose(&self, next: &StochasticMap) -> Result<StochasticMap, ClassicalShadowError> {
        if self.target_n != next.source_n {
            return Err(ClassicalShadowError::ShapeMismatch {
                left: self.target_n,
                right: next.source_n,
            });
        }
        let mut rows = Vec::with_capacity(self.source_n);
        for self_row in &self.rows {
            let mut row = vec![Rational::zero(); next.target_n];
            for (sik, next_row) in self_row.iter().zip(&next.rows) {
                if sik.is_zero() {
                    continue;
                }
                for (acc, e) in row.iter_mut().zip(next_row) {
                    *acc += sik * e;
                }
            }
            rows.push(row);
        }
        Self::try_from_rows(
            self.source_n,
            next.target_n,
            rows,
            format!("({} ; {})", self.label, next.label),
        )
    }

    pub fn power(
        &self,
        exponent: u32,
        max_exponent: u32,
    ) -> Result<StochasticMap, ClassicalShadowError> {
        if !self.is_endomorphism() {
            return Err(ClassicalShadowError::ShapeMismatch {
                left: self.source_n,
                right: self.target_n,
            });
        }
        if exponent > max_exponent {
            return Err(ClassicalShadowError::LimitExceeded {
                what: "matrix power",
                requested: exponent as usize,
                limit: max_exponent as usize,
            });
        }
        let mut result = Self::identity(&FinN::try_new(self.source_n)?, "id")?;
        let mut square = self.clone();
        let mut remaining = exponent;
        while remaining > 0 {
            if remaining & 1 == 1 {
                result = result.compose(&square)?;
            }
            remaining >>= 1;
            if remaining > 0 {
                square = square.compose(&square)?;
            }
        }
        result.label = format!("{}^{}", self.label, exponent);
        Ok(result)
    }

    pub fn tensor(&self, other: &StochasticMap) -> Result<StochasticMap, ClassicalShadowError> {
        let source_n = checked_size_product(self.source_n, other.source_n)?;
        let target_n = checked_size_product(self.target_n, other.target_n)?;
        let mut rows = Vec::with_capacity(source_n);
        for row1 in &self.rows {
            for row2 in &other.rows {
                let mut row = Vec::with_capacity(target_n);
                for a in row1 {
                    for b in row2 {
                        row.push(a * b);
                    }
                }
                rows.push(row);
            }
        }
        Self::try_from_rows(
            source_n,
            target_n,
            rows,
            format!("({} x {})", self.label, other.label),
        )
    }

    pub fn deterministic_function(&self) -> Option<Vec<usize>> {
        self.rows
            .iter()
            .map(|row| {
                let mut one_at = None;
                for (j, e) in row.iter().enumerate() {
                    if e.is_one() {
                        one_at = Some(j);
                    } else if !e.is_zero() {
                        return None;
                    }
                }
                one_at
            })
            .collect()
    }

    pub fn is_deterministic(&self) -> bool {
        self.deterministic_function().is_some()
    }

    pub fn is_identity(&self) -> bool {
        self.is_endomorphism()
            && self
                .deterministic_function()
                .is_some_and(|images| images.iter().enumerate().all(|(i, &image)| i == image))
    }

    pub fn is_permutation(&self) -> bool {
        if !self.is_endomorphism() {
            return false;
        }
        match self.deterministic_function() {
            Some(images) => {
                let mut seen = vec![false; self.target_n];
                images.iter().all(|&image| {
                    let fresh = !seen[image];
                    seen[image] = true;
                    fresh
                })
            }
            None => false,
        }
    }

    pub fn column_sums(&self) -> Vec<Rational> {
        let mut sums = vec![Rational::zero(); self.target_n];
        for row in &self.rows {
            for (acc, e) in sums.iter_mut().zip(row) {
                *acc += e;
            }
        }
        sums
    }

    pub fn is_doubly_stochastic(&self) -> bool {
        self.is_endomorphism() && self.column_sums().iter().all(Rational::is_one)
    }

    pub fn transpose(&self) -> Result<StochasticMap, ClassicalShadowError> {
        let rows: Vec<Vec<Rational>> = (0..self.target_n)
            .map(|j| self.rows.iter().map(|row| row[j].clone()).collect())
            .collect();
        Self::try_from_rows(
            self.target_n,
            self.source_n,
            rows,
            format!("{}^T", self.label),
        )
    }

    pub fn dobrushin_coefficient(&self) -> Rational {
        let mut best = Rational::zero();
        for (i, row) in self.rows.iter().enumerate() {
            for other in &self.rows[i + 1..] {
                let l1: Rational = row.iter().zip(other).map(|(a, b)| (a - b).abs()).sum();
                if l1 > best {
                    best = l1;
                }
            }
        }
        best * half()
    }

    pub fn bayesian_inverse(
        &self,
        prior: &ProbabilitySimplex,
    ) -> Result<(ProbabilitySimplex, StochasticMap), ClassicalShadowError> {
        let marginal = self.apply(prior)?;
        let mut rows = Vec::with_capacity(self.target_n);
        for (j, q) in marginal.probs().iter().enumerate() {
            if q.is_zero() {
                return Err(ClassicalShadowError::ZeroMass { index: j });
            }
            rows.push(
                prior
                    .probs()
                    .iter()
                    .zip(&self.rows)
                    .map(|(p, row)| p * &row[j] / q)
                    .collect(),
            );
        }
        let posterior = Self::try_from_rows(
            self.target_n,
            self.source_n,
            rows,
            format!("bayes({})", self.label),
        )?;
        Ok((marginal, posterior))
    }

    pub fn to_basic_matrix(&self) -> Result<BasicMatrix<Rational>, ClassicalShadowError> {
        let data: Vec<Rational> = self.rows.iter().flatten().cloned().collect();
        Ok(BasicMatrix::from_row_major(
            self.source_n,
            self.target_n,
            data,
        )?)
    }

    pub fn try_from_basic_matrix(
        matrix: &BasicMatrix<Rational>,
        label: impl Into<String>,
    ) -> Result<Self, ClassicalShadowError> {
        let mut rows = Vec::with_capacity(matrix.rows());
        for i in 0..matrix.rows() {
            let mut row = Vec::with_capacity(matrix.cols());
            for j in 0..matrix.cols() {
                row.push(matrix.get(i, j)?);
            }
            rows.push(row);
        }
        Self::try_from_rows(matrix.rows(), matrix.cols(), rows, label)
    }
}

#[cfg(test)]
mod tests {
    use super::*;
    use crate::test_support::{grid_simplices, simplex, stochastic as map};
    use omega_number_theory::rational::{ri, rq};

    fn q(n: i64, d: i64) -> Rational {
        rq(n, d)
    }

    fn fin(n: usize) -> FinN {
        FinN::try_new(n).unwrap()
    }

    fn chain_a() -> StochasticMap {
        map(&[
            &[(1, 2), (1, 3), (1, 6)],
            &[(1, 4), (1, 4), (1, 2)],
            &[(2, 5), (1, 5), (2, 5)],
        ])
    }

    fn chain_b() -> StochasticMap {
        map(&[
            &[(0, 1), (1, 1), (0, 1)],
            &[(1, 3), (1, 3), (1, 3)],
            &[(1, 7), (2, 7), (4, 7)],
        ])
    }


    #[test]
    fn the_identity_is_row_stochastic_with_ones_on_the_diagonal() {
        let id = StochasticMap::identity(&fin(3), "id").unwrap();
        assert!(id.is_endomorphism());
        assert!(id.is_identity());
        for i in 0..3 {
            for j in 0..3 {
                assert_eq!(id.get(i, j).unwrap(), if i == j { ri(1) } else { ri(0) });
            }
        }
    }

    #[test]
    fn the_identity_is_a_two_sided_unit_for_composition_on_square_and_rectangular_maps() {
        let id2 = StochasticMap::identity(&fin(2), "id2").unwrap();
        let id3 = StochasticMap::identity(&fin(3), "id3").unwrap();
        let flip = map(&[&[(0, 1), (1, 1)], &[(1, 1), (0, 1)]]);
        assert_eq!(id2.compose(&flip).unwrap(), flip);
        assert_eq!(flip.compose(&id2).unwrap(), flip);
        let emb = map(&[&[(1, 2), (1, 2), (0, 1)], &[(0, 1), (1, 3), (2, 3)]]);
        assert_eq!(id2.compose(&emb).unwrap(), emb);
        assert_eq!(emb.compose(&id3).unwrap(), emb);
        let p = simplex(&[(1, 4), (3, 4)]);
        assert_eq!(id2.apply(&p).unwrap(), p);
    }

    #[test]
    fn composition_is_associative_and_the_action_agrees_with_it() {
        let a = map(&[&[(1, 2), (1, 2)], &[(1, 3), (2, 3)]]);
        let b = map(&[&[(1, 1), (0, 1), (0, 1)], &[(0, 1), (1, 2), (1, 2)]]);
        let c = map(&[&[(1, 4), (3, 4)], &[(1, 2), (1, 2)], &[(2, 5), (3, 5)]]);
        let left = a.compose(&b).unwrap().compose(&c).unwrap();
        let right = a.compose(&b.compose(&c).unwrap()).unwrap();
        assert_eq!(left, right);
        assert_eq!((left.source_n(), left.target_n()), (2, 2));
        let p = simplex(&[(2, 5), (3, 5)]);
        let step = c.apply(&b.apply(&a.apply(&p).unwrap()).unwrap()).unwrap();
        assert_eq!(step, left.apply(&p).unwrap());
    }

    #[test]
    fn a_map_sends_a_distribution_to_a_distribution_with_the_hand_computed_masses() {
        let m = map(&[&[(1, 1), (0, 1)], &[(1, 2), (1, 2)], &[(0, 1), (1, 1)]]);
        let u = ProbabilitySimplex::uniform(&fin(3), "u").unwrap();
        assert_eq!(m.apply(&u).unwrap().probs(), &[q(1, 2), q(1, 2)]);
    }

    #[test]
    fn a_non_row_stochastic_matrix_is_refused_at_its_row() {
        let err = StochasticMap::try_from_rows(
            2,
            2,
            vec![vec![q(1, 2), q(1, 3)], vec![q(1, 1), q(0, 1)]],
            "bad",
        );
        assert_eq!(
            err,
            Err(ClassicalShadowError::RowNotNormalized {
                row: 0,
                sum: q(5, 6)
            })
        );
    }

    #[test]
    fn malformed_shapes_and_negative_entries_are_refused_with_their_positions() {
        let try_rows = |target_n: usize, rows: Vec<Vec<Rational>>| {
            StochasticMap::try_from_rows(2, target_n, rows, "hand")
        };
        assert_eq!(
            try_rows(0, vec![vec![], vec![]]),
            Err(ClassicalShadowError::ZeroCardinality)
        );
        assert_eq!(
            StochasticMap::try_from_rows(0, 2, vec![], "hand"),
            Err(ClassicalShadowError::ZeroCardinality)
        );
        assert_eq!(
            try_rows(2, vec![vec![ri(1), ri(0)]]),
            Err(ClassicalShadowError::DimensionMismatch {
                expected: 2,
                actual: 1
            })
        );
        assert_eq!(
            try_rows(2, vec![vec![ri(1), ri(0)], vec![ri(1)]]),
            Err(ClassicalShadowError::DimensionMismatch {
                expected: 2,
                actual: 1
            })
        );
        assert_eq!(
            try_rows(2, vec![vec![q(3, 2), q(-1, 2)], vec![ri(1), ri(0)]]),
            Err(ClassicalShadowError::NegativeEntry { index: 1 })
        );
    }

    #[test]
    fn composition_passes_the_i64_ceiling_exactly() {
        let a0 = Rational::new(BigInt::one(), BigInt::from(2u8).pow(40));
        let b0 = Rational::new(BigInt::one(), BigInt::from(3u8).pow(25));
        let a = StochasticMap::try_from_rows(
            2,
            2,
            vec![vec![a0.clone(), q(1, 1) - &a0], vec![q(1, 2), q(1, 2)]],
            "A",
        )
        .unwrap();
        let b = StochasticMap::try_from_rows(
            2,
            2,
            vec![vec![b0.clone(), q(1, 1) - &b0], vec![q(1, 5), q(4, 5)]],
            "B",
        )
        .unwrap();
        let ab = a.compose(&b).unwrap();
        let expected = &a0 * &b0 + (q(1, 1) - &a0) * q(1, 5);
        assert!(*expected.denom() > BigInt::from(i64::MAX));
        assert_eq!(ab.get(0, 0), Some(expected));
        for row in ab.rows() {
            assert_eq!(row.iter().sum::<Rational>(), q(1, 1));
        }
    }


    #[test]
    fn composition_agrees_with_the_dense_matrix_product_of_linear_algebra() {
        let (a, b) = (chain_a(), chain_b());
        let via_kernel = a.compose(&b).unwrap().to_basic_matrix().unwrap();
        let via_matrix = a
            .to_basic_matrix()
            .unwrap()
            .mul(&b.to_basic_matrix().unwrap())
            .unwrap();
        assert_eq!(via_kernel, via_matrix);
    }

    #[test]
    fn the_dense_matrix_round_trip_is_the_identity_and_refuses_a_non_stochastic_matrix() {
        let a = chain_a();
        let m = a.to_basic_matrix().unwrap();
        assert_eq!(StochasticMap::try_from_basic_matrix(&m, "a").unwrap(), a);
        let bad = BasicMatrix::from_row_major(1, 2, vec![q(1, 2), q(1, 3)]).unwrap();
        assert_eq!(
            StochasticMap::try_from_basic_matrix(&bad, "bad"),
            Err(ClassicalShadowError::RowNotNormalized {
                row: 0,
                sum: q(5, 6)
            })
        );
    }

    #[test]
    fn pushforward_of_p_is_composition_of_the_point_preparation_with_the_map() {
        let a = chain_a();
        let p = simplex(&[(1, 2), (1, 3), (1, 6)]);
        let prepare = StochasticMap::constant(1, &p, "prepare").unwrap();
        let composite = prepare.compose(&a).unwrap();
        assert_eq!(composite.conditional(0).unwrap(), a.apply(&p).unwrap());
    }

    #[test]
    fn pullback_is_adjoint_to_pushforward_on_enumerated_functions() {
        let a = chain_a();
        let p = simplex(&[(1, 2), (1, 3), (1, 6)]);
        let pushed = a.apply(&p).unwrap();
        for f in [
            vec![ri(1), ri(0), ri(0)],
            vec![ri(2), ri(-3), ri(7)],
            vec![q(1, 2), q(5, 3), q(-4, 9)],
        ] {
            let pulled = a.pullback(&f).unwrap();
            assert_eq!(
                p.expectation(&pulled).unwrap(),
                pushed.expectation(&f).unwrap(),
                "sum_i p_i (M f)_i = sum_j (p M)_j f_j for f = {f:?}"
            );
        }
        assert_eq!(
            a.pullback(&[ri(1), ri(2)]),
            Err(ClassicalShadowError::DimensionMismatch {
                expected: 3,
                actual: 2
            })
        );
    }


    #[test]
    fn a_function_becomes_a_deterministic_map_and_composition_composes_functions() {
        let f = StochasticMap::from_function(3, &[2, 0], "f").unwrap();
        let g = StochasticMap::from_function(2, &[1, 1, 0], "g").unwrap();
        assert!(f.is_deterministic());
        assert_eq!(f.deterministic_function(), Some(vec![2, 0]));
        let fg = f.compose(&g).unwrap();
        assert_eq!(fg.deterministic_function(), Some(vec![0, 1]));
        assert_eq!(
            StochasticMap::from_function(3, &[0, 3], "bad"),
            Err(ClassicalShadowError::IndexOutOfRange { index: 3, bound: 3 })
        );
        assert_eq!(
            StochasticMap::from_function(3, &[], "bad"),
            Err(ClassicalShadowError::ZeroCardinality)
        );
        assert!(!chain_a().is_deterministic());
        assert_eq!(chain_a().deterministic_function(), None);
    }

    #[test]
    fn a_permutation_is_validated_and_its_inverse_composes_to_the_identity() {
        let images = [2usize, 0, 3, 1];
        let p = StochasticMap::permutation(&images, "p").unwrap();
        assert!(p.is_permutation());
        let mut inverse = [0usize; 4];
        for (i, &image) in images.iter().enumerate() {
            inverse[image] = i;
        }
        let inv = StochasticMap::permutation(&inverse, "inv").unwrap();
        assert!(p.compose(&inv).unwrap().is_identity());
        assert!(inv.compose(&p).unwrap().is_identity());
        assert_eq!(
            StochasticMap::permutation(&[0, 1, 1], "bad"),
            Err(ClassicalShadowError::NotAPermutation { position: 2 })
        );
        assert_eq!(
            StochasticMap::permutation(&[1, 3], "bad"),
            Err(ClassicalShadowError::NotAPermutation { position: 1 })
        );
        let constant = StochasticMap::from_function(2, &[0, 0], "c").unwrap();
        assert!(constant.is_deterministic());
        assert!(!constant.is_permutation());
    }

    #[test]
    fn doubly_stochastic_means_the_uniform_distribution_is_preserved() {
        let half_half = map(&[&[(1, 2), (1, 2)], &[(1, 2), (1, 2)]]);
        assert!(half_half.is_doubly_stochastic());
        let u = ProbabilitySimplex::uniform(&fin(3), "u").unwrap();
        let mix = map(&[
            &[(1, 2), (1, 4), (1, 4)],
            &[(1, 4), (1, 2), (1, 4)],
            &[(1, 4), (1, 4), (1, 2)],
        ]);
        assert!(mix.is_doubly_stochastic());
        assert_eq!(mix.apply(&u).unwrap(), u);
        let skew = map(&[&[(1, 1), (0, 1)], &[(1, 2), (1, 2)]]);
        assert!(!skew.is_doubly_stochastic());
        assert_ne!(
            skew.apply(&ProbabilitySimplex::uniform(&fin(2), "u").unwrap())
                .unwrap(),
            ProbabilitySimplex::uniform(&fin(2), "u").unwrap()
        );
        assert!(
            !map(&[&[(1, 2), (1, 2), (0, 1)], &[(0, 1), (1, 2), (1, 2)]]).is_doubly_stochastic()
        );
        assert_eq!(skew.column_sums(), vec![q(3, 2), q(1, 2)]);
    }

    #[test]
    fn convex_mixtures_of_permutations_are_doubly_stochastic_and_the_transpose_is_too() {
        let id = StochasticMap::identity(&fin(3), "id").unwrap();
        let rot = StochasticMap::permutation(&[1, 2, 0], "rot").unwrap();
        let swap = StochasticMap::permutation(&[1, 0, 2], "swap").unwrap();
        let weights = [q(1, 2), q(1, 3), q(1, 6)];
        let mut rows = vec![vec![ri(0); 3]; 3];
        for (w, perm) in weights.iter().zip([&id, &rot, &swap]) {
            for (i, row) in perm.rows().iter().enumerate() {
                for (j, e) in row.iter().enumerate() {
                    rows[i][j] += w * e;
                }
            }
        }
        let mixture = StochasticMap::try_from_rows(3, 3, rows, "mix").unwrap();
        assert!(mixture.is_doubly_stochastic());
        let transposed = mixture.transpose().unwrap();
        assert!(transposed.is_doubly_stochastic());
        assert_eq!(transposed.transpose().unwrap(), mixture);
    }

    #[test]
    fn the_transpose_of_a_map_that_is_not_doubly_stochastic_is_refused() {
        let skew = map(&[&[(1, 1), (0, 1)], &[(1, 2), (1, 2)]]);
        assert_eq!(
            skew.transpose(),
            Err(ClassicalShadowError::RowNotNormalized {
                row: 0,
                sum: q(3, 2)
            })
        );
    }


    #[test]
    fn the_tensor_product_has_product_shape_and_entries() {
        let a = map(&[&[(1, 2), (1, 2)], &[(1, 3), (2, 3)]]);
        let b = map(&[&[(1, 4), (3, 4), (0, 1)]]);
        let t = a.tensor(&b).unwrap();
        assert_eq!((t.source_n(), t.target_n()), (2, 6));
        for i1 in 0..2 {
            for j1 in 0..2 {
                for j2 in 0..3 {
                    assert_eq!(
                        t.get(i1, j1 * 3 + j2).unwrap(),
                        a.get(i1, j1).unwrap() * b.get(0, j2).unwrap()
                    );
                }
            }
        }
    }

    #[test]
    fn the_interchange_law_and_the_action_on_products_hold() {
        let a = map(&[&[(1, 2), (1, 2)], &[(1, 3), (2, 3)]]);
        let b = map(&[&[(1, 4), (1, 4), (1, 2)], &[(1, 1), (0, 1), (0, 1)]]);
        let c = map(&[&[(1, 5), (4, 5)], &[(2, 3), (1, 3)]]);
        let d = map(&[&[(1, 2), (1, 2)], &[(1, 3), (2, 3)], &[(3, 4), (1, 4)]]);
        let left = a
            .tensor(&b)
            .unwrap()
            .compose(&c.tensor(&d).unwrap())
            .unwrap();
        let right = a
            .compose(&c)
            .unwrap()
            .tensor(&b.compose(&d).unwrap())
            .unwrap();
        assert_eq!(left, right);
        let p = simplex(&[(1, 4), (3, 4)]);
        let r = simplex(&[(1, 2), (1, 2)]);
        let on_product = a
            .tensor(&b)
            .unwrap()
            .apply(&p.product(&r).unwrap())
            .unwrap();
        assert_eq!(
            on_product,
            a.apply(&p).unwrap().product(&b.apply(&r).unwrap()).unwrap()
        );
    }

    #[test]
    fn tensoring_with_the_one_point_identity_changes_nothing() {
        let a = chain_a();
        let unit = StochasticMap::identity(&fin(1), "unit").unwrap();
        assert_eq!(unit.tensor(&a).unwrap(), a);
        assert_eq!(a.tensor(&unit).unwrap(), a);
    }

    #[test]
    fn structural_maps_refuse_a_size_that_overflows_before_allocating() {
        assert_eq!(
            StochasticMap::copy(usize::MAX),
            Err(ClassicalShadowError::SizeOverflow {
                left: usize::MAX,
                right: usize::MAX
            })
        );
        assert_eq!(
            StochasticMap::swap(usize::MAX, 2),
            Err(ClassicalShadowError::SizeOverflow {
                left: usize::MAX,
                right: 2
            })
        );
        assert_eq!(
            StochasticMap::first_projection(2, usize::MAX),
            Err(ClassicalShadowError::SizeOverflow {
                left: 2,
                right: usize::MAX
            })
        );
        assert_eq!(
            StochasticMap::second_projection(usize::MAX, 3),
            Err(ClassicalShadowError::SizeOverflow {
                left: usize::MAX,
                right: 3
            })
        );
    }

    #[test]
    fn copy_and_discard_are_a_comonoid() {
        for n in 1..=4usize {
            let id = StochasticMap::identity(&fin(n), "id").unwrap();
            let copy = StochasticMap::copy(n).unwrap();
            let discard = StochasticMap::discard(n).unwrap();
            assert_eq!(copy.compose(&discard.tensor(&id).unwrap()).unwrap(), id);
            assert_eq!(copy.compose(&id.tensor(&discard).unwrap()).unwrap(), id);
            let left = copy.compose(&copy.tensor(&id).unwrap()).unwrap();
            let right = copy.compose(&id.tensor(&copy).unwrap()).unwrap();
            assert_eq!(left, right);
            assert_eq!(
                copy.compose(&StochasticMap::swap(n, n).unwrap()).unwrap(),
                copy
            );
        }
    }

    #[test]
    fn a_map_commutes_with_copy_exactly_when_it_is_deterministic() {
        let natural = |f: &StochasticMap| {
            let lhs = f
                .compose(&StochasticMap::copy(f.target_n()).unwrap())
                .unwrap();
            let rhs = StochasticMap::copy(f.source_n())
                .unwrap()
                .compose(&f.tensor(f).unwrap())
                .unwrap();
            lhs == rhs
        };
        for a in 0..2usize {
            for b in 0..2usize {
                for c in 0..2usize {
                    let f = StochasticMap::from_function(2, &[a, b, c], "f").unwrap();
                    assert!(natural(&f), "deterministic f = [{a}, {b}, {c}]");
                }
            }
        }
        let noisy = map(&[&[(1, 2), (1, 2)], &[(1, 1), (0, 1)]]);
        assert!(!noisy.is_deterministic());
        assert!(!natural(&noisy));
        assert!(!natural(&chain_a()));
    }

    #[test]
    fn projections_recover_the_factors_of_a_product_and_swap_is_natural() {
        let p = simplex(&[(1, 4), (3, 4)]);
        let r = simplex(&[(1, 2), (1, 3), (1, 6)]);
        let pr = p.product(&r).unwrap();
        assert_eq!(
            StochasticMap::first_projection(2, 3)
                .unwrap()
                .apply(&pr)
                .unwrap(),
            p
        );
        assert_eq!(
            StochasticMap::second_projection(2, 3)
                .unwrap()
                .apply(&pr)
                .unwrap(),
            r
        );
        let f = map(&[&[(1, 2), (1, 2), (0, 1)], &[(0, 1), (1, 3), (2, 3)]]);
        let g = map(&[&[(1, 4), (3, 4)], &[(1, 2), (1, 2)], &[(2, 5), (3, 5)]]);
        let lhs = StochasticMap::swap(2, 3)
            .unwrap()
            .compose(&g.tensor(&f).unwrap())
            .unwrap();
        let rhs = f
            .tensor(&g)
            .unwrap()
            .compose(&StochasticMap::swap(3, 2).unwrap())
            .unwrap();
        assert_eq!(lhs, rhs);
        let s = StochasticMap::swap(2, 3).unwrap();
        assert!(s.is_permutation());
        assert!(s
            .compose(&StochasticMap::swap(3, 2).unwrap())
            .unwrap()
            .is_identity());
    }


    #[test]
    fn the_bayesian_inverse_reproduces_the_joint_distribution_and_inverts_back() {
        let a = chain_a();
        let prior = simplex(&[(1, 2), (1, 3), (1, 6)]);
        let (marginal, posterior) = a.bayesian_inverse(&prior).unwrap();
        assert_eq!(marginal, a.apply(&prior).unwrap());
        for i in 0..3 {
            for j in 0..3 {
                assert_eq!(
                    prior.get(i).unwrap() * a.get(i, j).unwrap(),
                    marginal.get(j).unwrap() * posterior.get(j, i).unwrap()
                );
            }
        }
        let (prior_back, kernel_back) = posterior.bayesian_inverse(&marginal).unwrap();
        assert_eq!(prior_back, prior);
        assert_eq!(kernel_back, a);
    }

    #[test]
    fn a_target_with_zero_mass_has_no_posterior_and_is_refused() {
        let m = map(&[&[(1, 1), (0, 1)], &[(1, 1), (0, 1)]]);
        let prior = simplex(&[(1, 2), (1, 2)]);
        assert_eq!(
            m.bayesian_inverse(&prior),
            Err(ClassicalShadowError::ZeroMass { index: 1 })
        );
    }


    #[test]
    fn the_dobrushin_coefficient_has_the_expected_extreme_values() {
        assert_eq!(
            map(&[&[(1, 3), (2, 3)], &[(1, 3), (2, 3)]]).dobrushin_coefficient(),
            ri(0)
        );
        assert_eq!(map(&[&[(1, 3), (2, 3)]]).dobrushin_coefficient(), ri(0));
        assert_eq!(
            StochasticMap::identity(&fin(3), "id")
                .unwrap()
                .dobrushin_coefficient(),
            ri(1)
        );
        assert_eq!(
            map(&[&[(1, 2), (1, 2), (0, 1)], &[(0, 1), (1, 2), (1, 2)]]).dobrushin_coefficient(),
            q(1, 2)
        );
    }

    #[test]
    fn total_variation_contracts_by_at_most_the_dobrushin_coefficient_and_the_bound_is_tight() {
        let maps = [
            chain_a(),
            chain_b(),
            map(&[&[(1, 2), (1, 2), (0, 1)], &[(0, 1), (1, 2), (1, 2)]]),
        ];
        for m in &maps {
            let n = m.source_n();
            let delta = m.dobrushin_coefficient();
            assert!(delta >= ri(0) && delta <= ri(1));
            let grid = grid_simplices(4, n);
            for p in &grid {
                for r in &grid {
                    let before = p.total_variation(r).unwrap();
                    let after = m
                        .apply(p)
                        .unwrap()
                        .total_variation(&m.apply(r).unwrap())
                        .unwrap();
                    assert!(after <= &delta * before);
                }
            }
            let mut attained = false;
            for i in 0..n {
                for k in 0..n {
                    let pi = ProbabilitySimplex::dirac(&fin(n), i, "p").unwrap();
                    let pk = ProbabilitySimplex::dirac(&fin(n), k, "r").unwrap();
                    let after = m
                        .apply(&pi)
                        .unwrap()
                        .total_variation(&m.apply(&pk).unwrap())
                        .unwrap();
                    if i != k && after == delta {
                        attained = true;
                    }
                }
            }
            assert!(attained, "no pair of point masses attains delta = {delta}");
        }
    }


    #[test]
    fn powers_agree_with_repeated_composition_and_are_bounded() {
        let a = chain_a();
        assert!(a.power(0, 10).unwrap().is_identity());
        assert_eq!(a.power(1, 10).unwrap(), a);
        let cubed = a.compose(&a).unwrap().compose(&a).unwrap();
        assert_eq!(a.power(3, 10).unwrap(), cubed);
        let seventh = (0..6).fold(a.clone(), |acc, _| acc.compose(&a).unwrap());
        assert_eq!(a.power(7, 10).unwrap(), seventh);
        assert_eq!(
            a.power(11, 10),
            Err(ClassicalShadowError::LimitExceeded {
                what: "matrix power",
                requested: 11,
                limit: 10
            })
        );
        let rectangular = map(&[&[(1, 2), (1, 2), (0, 1)], &[(0, 1), (1, 2), (1, 2)]]);
        assert_eq!(
            rectangular.power(2, 10),
            Err(ClassicalShadowError::ShapeMismatch { left: 2, right: 3 })
        );
    }

    #[test]
    fn composition_and_application_refuse_mismatched_carriers() {
        let a = chain_a();
        let two = map(&[&[(1, 2), (1, 2)], &[(1, 3), (2, 3)]]);
        assert_eq!(
            a.compose(&two),
            Err(ClassicalShadowError::ShapeMismatch { left: 3, right: 2 })
        );
        assert_eq!(
            two.apply(&simplex(&[(1, 3), (1, 3), (1, 3)])),
            Err(ClassicalShadowError::ShapeMismatch { left: 3, right: 2 })
        );
    }

    #[test]
    fn conditionals_and_constant_maps_round_trip() {
        let a = chain_a();
        let rows: Vec<ProbabilitySimplex> = (0..3).map(|i| a.conditional(i).unwrap()).collect();
        assert_eq!(StochasticMap::from_conditionals(&rows, "a").unwrap(), a);
        assert_eq!(
            a.conditional(3),
            Err(ClassicalShadowError::IndexOutOfRange { index: 3, bound: 3 })
        );
        assert_eq!(
            StochasticMap::from_conditionals(&[], "a"),
            Err(ClassicalShadowError::Empty)
        );
        let p = simplex(&[(1, 4), (3, 4)]);
        let c = StochasticMap::constant(3, &p, "c").unwrap();
        assert_eq!(c.dobrushin_coefficient(), ri(0));
        assert_eq!(c.apply(&simplex(&[(1, 3), (1, 3), (1, 3)])).unwrap(), p);
        assert_eq!(
            StochasticMap::constant(0, &p, "c"),
            Err(ClassicalShadowError::ZeroCardinality)
        );
    }

    #[test]
    fn labels_are_provenance_and_do_not_affect_equality() {
        let x = StochasticMap::try_from_rows(1, 2, vec![vec![q(1, 2), q(1, 2)]], "x").unwrap();
        let y = StochasticMap::try_from_rows(1, 2, vec![vec![q(1, 2), q(1, 2)]], "y").unwrap();
        assert_eq!(x, y);
        assert_eq!(x.label(), "x");
    }
}
