
use num_traits::{One, Signed, Zero};
use omega_number_theory::rational::Rational;

use crate::error::ClassicalShadowError;
use crate::simplex::ProbabilitySimplex;
use crate::stochastic_map::StochasticMap;

pub const MAX_LADDER_LEVELS: usize = 4096;

#[derive(Debug, Clone, PartialEq, Eq, thiserror::Error)]
pub enum MajorizationError {
    #[error("a probability vector needs at least one entry")]
    Empty,
    #[error("entry {index} is negative")]
    NegativeEntry { index: usize },
    #[error("the entries sum to {sum}, not one")]
    NotNormalized { sum: Rational },
    #[error("the ratio of a thermal ladder must be positive")]
    NonPositiveRatio,
    #[error("a thermal ladder needs at least one level")]
    ZeroLevels,
    #[error("{what} {requested} exceeds the limit {limit}")]
    LimitExceeded {
        what: &'static str,
        requested: usize,
        limit: usize,
    },
    #[error("coordinate {index} is outside a vector of length {len}")]
    CoordinateOutOfRange { index: usize, len: usize },
    #[error("a T-transform needs two distinct coordinates and a weight in [0, 1]")]
    InvalidTransform,
    #[error("the first vector does not majorize the second, so no T-transform chain exists")]
    NotMajorized,
    #[error("the T-transform construction could not proceed at step {step}")]
    ConstructionStuck { step: usize },
    #[error("probability refusal: {0}")]
    Probability(#[from] ClassicalShadowError),
}

#[derive(Debug, Clone, PartialEq, Eq)]
pub struct ProbabilityVector {
    decreasing: Vec<Rational>,
}

impl ProbabilityVector {
    pub fn try_new(entries: Vec<Rational>) -> Result<Self, MajorizationError> {
        if entries.is_empty() {
            return Err(MajorizationError::Empty);
        }
        let mut sum = Rational::zero();
        for (index, entry) in entries.iter().enumerate() {
            if entry.is_negative() {
                return Err(MajorizationError::NegativeEntry { index });
            }
            sum += entry;
        }
        if !sum.is_one() {
            return Err(MajorizationError::NotNormalized { sum });
        }
        let mut decreasing = entries;
        decreasing.sort_by(|a, b| b.cmp(a));
        Ok(Self { decreasing })
    }

    pub fn from_simplex(p: &ProbabilitySimplex) -> Self {
        let mut decreasing = p.probs().to_vec();
        decreasing.sort_by(|a, b| b.cmp(a));
        Self { decreasing }
    }

    pub fn n(&self) -> usize {
        self.decreasing.len()
    }

    pub fn decreasing(&self) -> &[Rational] {
        &self.decreasing
    }

    pub fn partial_sums(&self) -> Vec<Rational> {
        let mut total = Rational::zero();
        self.decreasing
            .iter()
            .map(|p| {
                total += p;
                total.clone()
            })
            .collect()
    }

    fn padded_entries(&self, len: usize) -> Vec<Rational> {
        let mut entries = self.decreasing.clone();
        while entries.len() < len {
            entries.push(Rational::zero());
        }
        entries
    }

    pub fn to_simplex(&self) -> Result<ProbabilitySimplex, MajorizationError> {
        Ok(ProbabilitySimplex::try_new(self.decreasing.clone())?)
    }
}

#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub enum Majorization {
    Equal,
    PMajorizesQ,
    QMajorizesP,
    Incomparable,
}

pub fn compare(p: &ProbabilityVector, q: &ProbabilityVector) -> Majorization {
    let n = p.n().max(q.n());
    let (sp, sq) = (partial_sums_padded(p, n), partial_sums_padded(q, n));
    let p_dominates = sp.iter().zip(&sq).all(|(a, b)| a >= b);
    let q_dominates = sp.iter().zip(&sq).all(|(a, b)| b >= a);
    match (p_dominates, q_dominates) {
        (true, true) => Majorization::Equal,
        (true, false) => Majorization::PMajorizesQ,
        (false, true) => Majorization::QMajorizesP,
        (false, false) => Majorization::Incomparable,
    }
}

fn partial_sums_padded(p: &ProbabilityVector, n: usize) -> Vec<Rational> {
    let mut sums = p.partial_sums();
    let last = sums.last().cloned().unwrap_or_else(Rational::zero);
    while sums.len() < n {
        sums.push(last.clone());
    }
    sums
}

pub fn majorizes(p: &ProbabilityVector, q: &ProbabilityVector) -> bool {
    matches!(
        compare(p, q),
        Majorization::Equal | Majorization::PMajorizesQ
    )
}

pub fn locc_convertible(source: &ProbabilityVector, target: &ProbabilityVector) -> bool {
    majorizes(target, source)
}

pub fn thermal_ladder(
    ratio: &Rational,
    levels: usize,
) -> Result<ProbabilityVector, MajorizationError> {
    if !ratio.is_positive() {
        return Err(MajorizationError::NonPositiveRatio);
    }
    if levels == 0 {
        return Err(MajorizationError::ZeroLevels);
    }
    if levels > MAX_LADDER_LEVELS {
        return Err(MajorizationError::LimitExceeded {
            what: "ladder levels",
            requested: levels,
            limit: MAX_LADDER_LEVELS,
        });
    }
    let mut weights = Vec::with_capacity(levels);
    let mut power = Rational::one();
    for _ in 0..levels {
        weights.push(power.clone());
        power = &power * ratio;
    }
    let total: Rational = weights.iter().sum();
    ProbabilityVector::try_new(weights.into_iter().map(|w| w / &total).collect())
}

#[derive(Debug, Clone, PartialEq, Eq)]
pub struct TTransform {
    i: usize,
    j: usize,
    lambda: Rational,
}

impl TTransform {
    pub fn try_new(i: usize, j: usize, lambda: Rational) -> Result<Self, MajorizationError> {
        if i == j || lambda.is_negative() || lambda > Rational::one() {
            return Err(MajorizationError::InvalidTransform);
        }
        Ok(Self { i, j, lambda })
    }

    pub fn i(&self) -> usize {
        self.i
    }

    pub fn j(&self) -> usize {
        self.j
    }

    pub fn lambda(&self) -> &Rational {
        &self.lambda
    }

    pub fn apply(&self, x: &[Rational]) -> Result<Vec<Rational>, MajorizationError> {
        for &index in &[self.i, self.j] {
            if index >= x.len() {
                return Err(MajorizationError::CoordinateOutOfRange {
                    index,
                    len: x.len(),
                });
            }
        }
        let other = Rational::one() - &self.lambda;
        let mut out = x.to_vec();
        out[self.i] = &self.lambda * &x[self.i] + &other * &x[self.j];
        out[self.j] = &other * &x[self.i] + &self.lambda * &x[self.j];
        Ok(out)
    }

    pub fn as_map(&self, n: usize) -> Result<StochasticMap, MajorizationError> {
        for &index in &[self.i, self.j] {
            if index >= n {
                return Err(MajorizationError::CoordinateOutOfRange { index, len: n });
            }
        }
        let other = Rational::one() - &self.lambda;
        let mut rows = vec![vec![Rational::zero(); n]; n];
        for (k, row) in rows.iter_mut().enumerate() {
            row[k] = Rational::one();
        }
        rows[self.i][self.i] = self.lambda.clone();
        rows[self.i][self.j] = other.clone();
        rows[self.j][self.i] = other;
        rows[self.j][self.j] = self.lambda.clone();
        Ok(StochasticMap::try_from_rows(n, n, rows, "T-transform")?)
    }
}

pub fn t_transform_chain(
    p: &ProbabilityVector,
    q: &ProbabilityVector,
) -> Result<Vec<TTransform>, MajorizationError> {
    if !majorizes(p, q) {
        return Err(MajorizationError::NotMajorized);
    }
    let n = p.n().max(q.n());
    let mut current = p.padded_entries(n);
    let target = q.padded_entries(n);
    let mut chain = Vec::new();
    while current != target {
        let step = chain.len();
        let j = (0..n)
            .rev()
            .find(|&i| current[i] > target[i])
            .ok_or(MajorizationError::ConstructionStuck { step })?;
        let k = (j + 1..n)
            .find(|&i| current[i] < target[i])
            .ok_or(MajorizationError::ConstructionStuck { step })?;
        let available = &current[j] - &target[j];
        let needed = &target[k] - &current[k];
        let moved = if available < needed {
            available
        } else {
            needed
        };
        let gap = &current[j] - &current[k];
        let lambda = Rational::one() - &moved / &gap;
        current[j] -= &moved;
        current[k] += &moved;
        chain.push(TTransform::try_new(j, k, lambda)?);
    }
    Ok(chain)
}

pub fn apply_chain(
    chain: &[TTransform],
    start: &[Rational],
) -> Result<Vec<Rational>, MajorizationError> {
    let mut x = start.to_vec();
    for transform in chain {
        x = transform.apply(&x)?;
    }
    Ok(x)
}

pub fn doubly_stochastic_transform(
    p: &ProbabilityVector,
    q: &ProbabilityVector,
) -> Result<StochasticMap, MajorizationError> {
    let chain = t_transform_chain(p, q)?;
    let n = p.n().max(q.n());
    let mut map = StochasticMap::try_from_rows(
        n,
        n,
        (0..n)
            .map(|i| {
                (0..n)
                    .map(|j| {
                        if i == j {
                            Rational::one()
                        } else {
                            Rational::zero()
                        }
                    })
                    .collect()
            })
            .collect(),
        "id",
    )?;
    for transform in &chain {
        map = map.compose(&transform.as_map(n)?)?;
    }
    Ok(map)
}

#[cfg(test)]
mod tests {
    use super::*;
    use crate::test_support::compositions;
    use omega_number_theory::rational::{ri, rq};

    fn pv(entries: &[(i64, i64)]) -> ProbabilityVector {
        ProbabilityVector::try_new(entries.iter().map(|&(n, d)| rq(n, d)).collect()).unwrap()
    }

    fn grid_vectors(grid: i64, n: usize) -> Vec<ProbabilityVector> {
        let mut seen = std::collections::BTreeSet::new();
        let mut out = Vec::new();
        for c in compositions(grid, n) {
            let v =
                ProbabilityVector::try_new(c.into_iter().map(|k| rq(k, grid)).collect()).unwrap();
            if seen.insert(v.decreasing().to_vec()) {
                out.push(v);
            }
        }
        out
    }

    #[test]
    fn construction_sorts_and_refuses_empty_negative_and_unnormalised_input() {
        let v = pv(&[(1, 6), (1, 2), (1, 3)]);
        assert_eq!(v.decreasing(), &[rq(1, 2), rq(1, 3), rq(1, 6)]);
        assert_eq!(v.partial_sums(), vec![rq(1, 2), rq(5, 6), ri(1)]);
        assert_eq!(
            ProbabilityVector::try_new(vec![]),
            Err(MajorizationError::Empty)
        );
        assert_eq!(
            ProbabilityVector::try_new(vec![rq(3, 2), rq(-1, 2)]),
            Err(MajorizationError::NegativeEntry { index: 1 })
        );
        assert_eq!(
            ProbabilityVector::try_new(vec![rq(1, 2), rq(1, 3)]),
            Err(MajorizationError::NotNormalized { sum: rq(5, 6) })
        );
    }

    #[test]
    fn the_four_outcomes_each_occur_and_the_documented_example_is_incomparable() {
        let p = pv(&[(7, 10), (3, 20), (3, 20)]);
        let q = pv(&[(3, 5), (7, 20), (1, 20)]);
        assert_eq!(compare(&p, &q), Majorization::Incomparable);
        assert_eq!(compare(&q, &p), Majorization::Incomparable);
        let sharp = pv(&[(1, 2), (1, 2), (0, 1)]);
        let flat = pv(&[(1, 3), (1, 3), (1, 3)]);
        assert_eq!(compare(&sharp, &flat), Majorization::PMajorizesQ);
        assert_eq!(compare(&flat, &sharp), Majorization::QMajorizesP);
        assert_eq!(
            compare(&sharp, &pv(&[(0, 1), (1, 2), (1, 2)])),
            Majorization::Equal
        );
    }

    #[test]
    fn a_point_mass_majorizes_everything_and_the_uniform_vector_is_majorized_by_everything() {
        for n in 1..=4usize {
            let mut dirac = vec![ri(0); n];
            dirac[0] = ri(1);
            let dirac = ProbabilityVector::try_new(dirac).unwrap();
            let uniform = ProbabilityVector::try_new(vec![rq(1, n as i64); n]).unwrap();
            for v in grid_vectors(6, n) {
                assert!(majorizes(&dirac, &v));
                assert!(majorizes(&v, &uniform));
            }
            let expected = if n == 1 {
                Majorization::Equal
            } else {
                Majorization::PMajorizesQ
            };
            assert_eq!(compare(&dirac, &uniform), expected);
        }
    }

    #[test]
    fn majorization_is_a_preorder_antisymmetric_exactly_up_to_permutation() {
        for (grid, n) in [(6, 3), (5, 4)] {
            let vectors = grid_vectors(grid, n);
            for p in &vectors {
                assert!(majorizes(p, p), "reflexive");
                for q in &vectors {
                    let forward = majorizes(p, q);
                    let backward = majorizes(q, p);
                    assert_eq!(forward && backward, p == q);
                    assert_eq!(compare(p, q) == Majorization::Equal, p == q);
                    if forward {
                        for r in &vectors {
                            if majorizes(q, r) {
                                assert!(majorizes(p, r), "transitive");
                            }
                        }
                    }
                }
            }
        }
    }

    fn majorizes_by_subsets(p: &ProbabilityVector, q: &[Rational]) -> bool {
        let n = q.len();
        let sums = p.partial_sums();
        (1u32..(1 << n)).all(|mask| {
            let k = mask.count_ones() as usize;
            let total: Rational = (0..n).filter(|i| mask >> i & 1 == 1).map(|i| &q[i]).sum();
            total <= sums[k - 1]
        })
    }

    fn majorizes_by_hinges(p: &[Rational], q: &[Rational]) -> bool {
        let hinge = |v: &[Rational], c: &Rational| -> Rational {
            v.iter()
                .map(|x| if x > c { x - c } else { Rational::zero() })
                .sum()
        };
        p.iter().chain(q).all(|c| hinge(p, c) >= hinge(q, c))
    }

    #[test]
    fn the_partial_sum_test_agrees_with_the_subset_and_the_hinge_definitions() {
        for n in [3usize, 4] {
            let vectors = grid_vectors(5, n);
            for p in &vectors {
                for q in &vectors {
                    let expected = majorizes(p, q);
                    let mut reversed: Vec<Rational> = q.decreasing().to_vec();
                    reversed.reverse();
                    assert_eq!(
                        majorizes_by_subsets(p, &reversed),
                        expected,
                        "{:?} vs {:?}",
                        p,
                        q
                    );
                    assert_eq!(majorizes_by_hinges(p.decreasing(), &reversed), expected);
                }
            }
        }
    }

    #[test]
    fn a_permutation_of_the_entries_does_not_change_the_vector_or_any_comparison() {
        let base = [rq(1, 2), rq(1, 3), rq(1, 6), rq(0, 1)];
        let reference = ProbabilityVector::try_new(base.to_vec()).unwrap();
        let other = pv(&[(1, 4), (1, 4), (1, 4), (1, 4)]);
        let mut permutations = 0;
        for a in 0..4 {
            for b in 0..4 {
                for c in 0..4 {
                    for d in 0..4 {
                        let mut picked = vec![a, b, c, d];
                        picked.sort_unstable();
                        picked.dedup();
                        if picked.len() < 4 {
                            continue;
                        }
                        let permuted = ProbabilityVector::try_new(
                            [a, b, c, d].iter().map(|&i| base[i].clone()).collect(),
                        )
                        .unwrap();
                        assert_eq!(permuted, reference);
                        assert_eq!(compare(&permuted, &other), compare(&reference, &other));
                        permutations += 1;
                    }
                }
            }
        }
        assert_eq!(permutations, 24);
    }

    #[test]
    fn vectors_of_different_lengths_compare_by_padding_with_zeros() {
        let short = pv(&[(1, 2), (1, 2)]);
        let long = pv(&[(1, 2), (1, 2), (0, 1), (0, 1)]);
        assert_eq!(compare(&short, &long), Majorization::Equal);
        let flat = pv(&[(1, 3), (1, 3), (1, 3)]);
        assert_eq!(compare(&short, &flat), Majorization::PMajorizesQ);
        assert_eq!(compare(&flat, &short), Majorization::QMajorizesP);
    }

    #[test]
    fn nielsen_conversion_goes_from_more_to_less_entangled_spectra_only() {
        let maximally_entangled = pv(&[(1, 2), (1, 2)]);
        let product = pv(&[(1, 1), (0, 1)]);
        let partial = pv(&[(3, 4), (1, 4)]);
        assert!(locc_convertible(&maximally_entangled, &partial));
        assert!(locc_convertible(&partial, &product));
        assert!(locc_convertible(&maximally_entangled, &product));
        assert!(!locc_convertible(&product, &maximally_entangled));
        assert!(!locc_convertible(&partial, &maximally_entangled));
        assert!(locc_convertible(&partial, &partial));
        let a = pv(&[(7, 10), (3, 20), (3, 20)]);
        let b = pv(&[(3, 5), (7, 20), (1, 20)]);
        assert!(!locc_convertible(&a, &b) && !locc_convertible(&b, &a));
    }

    #[test]
    fn the_thermal_ladder_has_the_documented_values_and_the_ratio_order_is_the_majorization_order()
    {
        let ladder = thermal_ladder(&rq(1, 2), 4).unwrap();
        assert_eq!(
            ladder.decreasing(),
            &[rq(8, 15), rq(4, 15), rq(2, 15), rq(1, 15)]
        );
        assert_eq!(
            thermal_ladder(&ri(1), 3).unwrap(),
            pv(&[(1, 3), (1, 3), (1, 3)])
        );
        assert_eq!(
            thermal_ladder(&ri(2), 4).unwrap(),
            thermal_ladder(&rq(1, 2), 4).unwrap()
        );
        let ratios = [
            rq(1, 10),
            rq(1, 5),
            rq(1, 3),
            rq(1, 2),
            rq(2, 3),
            rq(9, 10),
            ri(1),
        ];
        for levels in [2usize, 3, 5] {
            for (a, r1) in ratios.iter().enumerate() {
                for r2 in &ratios[a + 1..] {
                    let (l1, l2) = (
                        thermal_ladder(r1, levels).unwrap(),
                        thermal_ladder(r2, levels).unwrap(),
                    );
                    assert_eq!(
                        compare(&l1, &l2),
                        Majorization::PMajorizesQ,
                        "r1 = {r1}, r2 = {r2}, levels = {levels}"
                    );
                }
            }
        }
    }

    #[test]
    fn a_thermal_ladder_refuses_a_non_positive_ratio_no_levels_and_too_many_levels() {
        assert_eq!(
            thermal_ladder(&ri(0), 3),
            Err(MajorizationError::NonPositiveRatio)
        );
        assert_eq!(
            thermal_ladder(&ri(-1), 3),
            Err(MajorizationError::NonPositiveRatio)
        );
        assert_eq!(
            thermal_ladder(&rq(1, 2), 0),
            Err(MajorizationError::ZeroLevels)
        );
        assert_eq!(
            thermal_ladder(&rq(1, 2), MAX_LADDER_LEVELS + 1),
            Err(MajorizationError::LimitExceeded {
                what: "ladder levels",
                requested: MAX_LADDER_LEVELS + 1,
                limit: MAX_LADDER_LEVELS
            })
        );
        assert_eq!(thermal_ladder(&rq(1, 2), 1).unwrap(), pv(&[(1, 1)]));
    }

    #[test]
    fn a_t_transform_moves_mass_between_two_coordinates_and_refuses_bad_arguments() {
        let t = TTransform::try_new(0, 2, rq(1, 4)).unwrap();
        let x = vec![ri(4), ri(9), ri(0)];
        assert_eq!(t.apply(&x).unwrap(), vec![ri(1), ri(9), ri(3)]);
        assert_eq!(
            t.apply(&[ri(1), ri(1)]),
            Err(MajorizationError::CoordinateOutOfRange { index: 2, len: 2 })
        );
        assert_eq!(
            TTransform::try_new(1, 1, rq(1, 2)),
            Err(MajorizationError::InvalidTransform)
        );
        assert_eq!(
            TTransform::try_new(0, 1, rq(-1, 2)),
            Err(MajorizationError::InvalidTransform)
        );
        assert_eq!(
            TTransform::try_new(0, 1, rq(3, 2)),
            Err(MajorizationError::InvalidTransform)
        );
        assert_eq!(
            TTransform::try_new(0, 1, ri(1))
                .unwrap()
                .apply(&[ri(1), ri(2)])
                .unwrap(),
            vec![ri(1), ri(2)]
        );
        assert_eq!(
            TTransform::try_new(0, 1, ri(0))
                .unwrap()
                .apply(&[ri(1), ri(2)])
                .unwrap(),
            vec![ri(2), ri(1)]
        );
        let m = t.as_map(3).unwrap();
        assert!(m.is_doubly_stochastic());
        let p = ProbabilitySimplex::try_new(vec![rq(1, 2), rq(1, 3), rq(1, 6)]).unwrap();
        assert_eq!(
            m.apply(&p).unwrap().probs().to_vec(),
            t.apply(p.probs()).unwrap()
        );
        assert_eq!(
            t.as_map(2),
            Err(MajorizationError::CoordinateOutOfRange { index: 2, len: 2 })
        );
    }

    #[test]
    fn the_chain_carries_p_to_q_exactly_with_at_most_n_minus_one_strict_transforms() {
        for (grid, n) in [(6, 3), (7, 4), (8, 5)] {
            let vectors = grid_vectors(grid, n);
            let mut strict_pairs = 0;
            for p in &vectors {
                for q in &vectors {
                    if !majorizes(p, q) {
                        assert_eq!(
                            t_transform_chain(p, q),
                            Err(MajorizationError::NotMajorized)
                        );
                        continue;
                    }
                    strict_pairs += usize::from(p != q);
                    let chain = t_transform_chain(p, q).unwrap();
                    assert!(chain.len() < n, "{} transforms for n = {n}", chain.len());
                    assert_eq!(chain.is_empty(), p == q);
                    for t in &chain {
                        assert!(t.lambda().is_positive() && *t.lambda() < ri(1));
                        assert!(t.i() < t.j());
                    }
                    assert_eq!(apply_chain(&chain, p.decreasing()).unwrap(), q.decreasing());
                    let m = doubly_stochastic_transform(p, q).unwrap();
                    assert!(m.is_doubly_stochastic());
                    assert_eq!(
                        m.apply(&p.to_simplex().unwrap()).unwrap().probs(),
                        q.decreasing()
                    );
                }
            }
            assert!(
                strict_pairs >= vectors.len(),
                "{strict_pairs} strict majorizing pairs"
            );
        }
    }

    #[test]
    fn a_doubly_stochastic_image_is_always_majorized_by_its_source_but_a_general_map_need_not_be() {
        let f = |rows: &[&[(i64, i64)]]| crate::test_support::stochastic(rows);
        let doubly_stochastic = [
            f(&[
                &[(1, 2), (1, 4), (1, 4)],
                &[(1, 4), (1, 2), (1, 4)],
                &[(1, 4), (1, 4), (1, 2)],
            ]),
            f(&[
                &[(0, 1), (1, 1), (0, 1)],
                &[(0, 1), (0, 1), (1, 1)],
                &[(1, 1), (0, 1), (0, 1)],
            ]),
            f(&[
                &[(1, 3), (1, 3), (1, 3)],
                &[(1, 3), (1, 3), (1, 3)],
                &[(1, 3), (1, 3), (1, 3)],
            ]),
            f(&[
                &[(1, 2), (1, 2), (0, 1)],
                &[(1, 2), (0, 1), (1, 2)],
                &[(0, 1), (1, 2), (1, 2)],
            ]),
        ];
        let vectors = grid_vectors(6, 3);
        for m in &doubly_stochastic {
            assert!(m.is_doubly_stochastic());
            for p in &vectors {
                let image = m.apply(&p.to_simplex().unwrap()).unwrap();
                assert!(
                    majorizes(p, &ProbabilityVector::from_simplex(&image)),
                    "{:?} -> {:?}",
                    p,
                    image
                );
            }
        }
        let collapse = f(&[
            &[(1, 1), (0, 1), (0, 1)],
            &[(1, 1), (0, 1), (0, 1)],
            &[(1, 1), (0, 1), (0, 1)],
        ]);
        assert!(!collapse.is_doubly_stochastic());
        let uniform = pv(&[(1, 3), (1, 3), (1, 3)]);
        let image = ProbabilityVector::from_simplex(
            &collapse.apply(&uniform.to_simplex().unwrap()).unwrap(),
        );
        assert_eq!(compare(&uniform, &image), Majorization::QMajorizesP);
    }
}
