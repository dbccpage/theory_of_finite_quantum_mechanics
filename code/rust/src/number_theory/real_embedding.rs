
use std::cmp::Ordering;

use num_bigint::BigInt;
use num_integer::Integer;
use num_traits::{One, Signed};
use omega_kernel::interval::Interval;

use crate::cyclotomic_field::{min_poly_of_2cos, CyclotomicError, CyclotomicNumber};
use crate::polynomial::{
    isolate_real_roots, refine_simple_root, Polynomial, PolynomialError, RootLocation,
};
use crate::rational::Rational;

pub const MAX_REFINEMENTS: usize = 50_000;

#[derive(Debug, Clone, PartialEq, Eq, thiserror::Error)]
pub enum EmbeddingError {
    #[error("the element is not real: complex conjugation does not fix it")]
    NotReal,
    #[error(
        "{k} does not name a real embedding of Q(zeta_{conductor}): it must be coprime to the \
         conductor"
    )]
    InvalidClass { k: i64, conductor: usize },
    #[error(
        "the element lies in Q(zeta_{element}) but these are the embeddings of \
         Q(zeta_{embeddings})"
    )]
    ConductorMismatch { element: usize, embeddings: usize },
    #[error("tolerance must be positive, got {0}")]
    NonPositiveTolerance(String),
    #[error("the sign is still undecided after {iterations} bisections")]
    PrecisionLimit { iterations: usize },
    #[error("internal inconsistency: {0}")]
    Inconsistent(&'static str),
    #[error(transparent)]
    Cyclotomic(#[from] CyclotomicError),
    #[error(transparent)]
    Polynomial(#[from] PolynomialError),
}

#[derive(Clone, Debug)]
pub struct RealEmbeddings {
    conductor: usize,
    psi: Polynomial<Rational>,
    classes: Vec<usize>,
    locations: Vec<RootLocation>,
}

pub fn real_embeddings(conductor: usize) -> Result<RealEmbeddings, EmbeddingError> {
    RealEmbeddings::new(conductor)
}

impl RealEmbeddings {
    pub fn new(conductor: usize) -> Result<Self, EmbeddingError> {
        let psi = min_poly_of_2cos(conductor)?;
        let roots = isolate_real_roots(&psi)?;
        let classes: Vec<usize> = if conductor <= 2 {
            vec![1]
        } else {
            (1..=conductor / 2)
                .filter(|k| k.gcd(&conductor) == 1)
                .collect()
        };
        if roots.len() != classes.len() || roots.iter().any(|r| r.multiplicity != 1) {
            return Err(EmbeddingError::Inconsistent(
                "Psi_n must have exactly phi(n)/2 simple real roots",
            ));
        }
        let locations = roots.into_iter().rev().map(|r| r.location).collect();
        Ok(Self {
            conductor,
            psi,
            classes,
            locations,
        })
    }

    pub fn conductor(&self) -> usize {
        self.conductor
    }

    pub fn count(&self) -> usize {
        self.classes.len()
    }

    pub fn classes(&self) -> &[usize] {
        &self.classes
    }

    pub fn min_poly(&self) -> &Polynomial<Rational> {
        &self.psi
    }

    fn class_index(&self, k: i64) -> Result<usize, EmbeddingError> {
        let invalid = || EmbeddingError::InvalidClass {
            k,
            conductor: self.conductor,
        };
        let n = self.conductor as i64;
        let residue = usize::try_from(k.rem_euclid(n)).map_err(|_| invalid())?;
        if residue.gcd(&self.conductor) != 1 {
            return Err(invalid());
        }
        let canonical = if self.conductor <= 2 {
            1
        } else {
            residue.min(self.conductor - residue)
        };
        self.classes
            .binary_search(&canonical)
            .map_err(|_| invalid())
    }

    pub fn root_location(&self, k: i64) -> Result<RootLocation, EmbeddingError> {
        let index = self.class_index(k)?;
        self.locations
            .get(index)
            .cloned()
            .ok_or(EmbeddingError::Inconsistent("a class has no root"))
    }

    fn refine(&mut self, index: usize, bits: u32) -> Result<(), EmbeddingError> {
        let location = self
            .locations
            .get(index)
            .ok_or(EmbeddingError::Inconsistent("a class has no root"))?;
        if let RootLocation::Isolated(interval) = location {
            let target = interval.diam() * Rational::new(BigInt::one(), BigInt::one() << bits);
            let refined = refine_simple_root(&self.psi, interval, &target)?;
            if let Some(slot) = self.locations.get_mut(index) {
                *slot = refined;
            }
        }
        Ok(())
    }

    pub fn root_enclosure(
        &mut self,
        k: i64,
        tolerance: &Rational,
    ) -> Result<Interval, EmbeddingError> {
        self.enclose_polynomial(&Polynomial::from_i64s(&[0, 1]), k, tolerance)
    }

    fn certified_location_sign(
        reduced: &Polynomial<Rational>,
        location: &RootLocation,
    ) -> Option<Ordering> {
        match location {
            RootLocation::Exact(root) => Some(reduced.sign_at(root)),
            RootLocation::Isolated(interval) => {
                let enclosure = reduced.eval_interval(interval);
                if enclosure.lo().is_positive() {
                    Some(Ordering::Greater)
                } else if enclosure.hi().is_negative() {
                    Some(Ordering::Less)
                } else {
                    None
                }
            }
        }
    }

    pub fn sign_of_polynomial(
        &mut self,
        g: &Polynomial<Rational>,
        k: i64,
    ) -> Result<Ordering, EmbeddingError> {
        let index = self.class_index(k)?;
        let reduced = g.rem(&self.psi)?;
        if reduced.is_zero() {
            return Ok(Ordering::Equal);
        }
        for _ in 0..MAX_REFINEMENTS {
            let location = self
                .locations
                .get(index)
                .ok_or(EmbeddingError::Inconsistent("a class has no root"))?;
            if let Some(sign) = Self::certified_location_sign(&reduced, location) {
                return Ok(sign);
            }
            self.refine(index, 4)?;
        }
        Err(EmbeddingError::PrecisionLimit {
            iterations: MAX_REFINEMENTS,
        })
    }

    pub fn enclose_polynomial(
        &mut self,
        g: &Polynomial<Rational>,
        k: i64,
        tolerance: &Rational,
    ) -> Result<Interval, EmbeddingError> {
        if !tolerance.is_positive() {
            return Err(EmbeddingError::NonPositiveTolerance(tolerance.to_string()));
        }
        let index = self.class_index(k)?;
        let reduced = g.rem(&self.psi)?;
        for _ in 0..MAX_REFINEMENTS {
            match self
                .locations
                .get(index)
                .ok_or(EmbeddingError::Inconsistent("a class has no root"))?
            {
                RootLocation::Exact(root) => return Ok(Interval::point(reduced.eval(root))),
                RootLocation::Isolated(interval) => {
                    let enclosure = reduced.eval_interval(interval);
                    if enclosure.diam() <= *tolerance {
                        return Ok(enclosure);
                    }
                }
            }
            self.refine(index, 8)?;
        }
        Err(EmbeddingError::PrecisionLimit {
            iterations: MAX_REFINEMENTS,
        })
    }

    fn real_polynomial(
        &self,
        x: &CyclotomicNumber,
    ) -> Result<Polynomial<Rational>, EmbeddingError> {
        if x.conductor() != self.conductor {
            return Err(EmbeddingError::ConductorMismatch {
                element: x.conductor(),
                embeddings: self.conductor,
            });
        }
        if !x.is_real() {
            return Err(EmbeddingError::NotReal);
        }
        Ok(x.real_part_polynomial())
    }

    pub fn sign_under_embedding(
        &mut self,
        x: &CyclotomicNumber,
        k: i64,
    ) -> Result<Ordering, EmbeddingError> {
        let g = self.real_polynomial(x)?;
        self.sign_of_polynomial(&g, k)
    }

    pub fn sign(&mut self, x: &CyclotomicNumber) -> Result<Ordering, EmbeddingError> {
        self.sign_under_embedding(x, 1)
    }

    pub fn signs(
        &mut self,
        x: &CyclotomicNumber,
    ) -> Result<Vec<(usize, Ordering)>, EmbeddingError> {
        let g = self.real_polynomial(x)?;
        let classes = self.classes.clone();
        classes
            .into_iter()
            .map(|k| {
                let k_signed =
                    i64::try_from(k).map_err(|_| EmbeddingError::Inconsistent("class fits i64"))?;
                Ok((k, self.sign_of_polynomial(&g, k_signed)?))
            })
            .collect()
    }

    pub fn is_positive_under_all_embeddings(
        &mut self,
        x: &CyclotomicNumber,
    ) -> Result<bool, EmbeddingError> {
        Ok(self
            .signs(x)?
            .iter()
            .all(|(_, sign)| *sign == Ordering::Greater))
    }

    pub fn compare(
        &mut self,
        x: &CyclotomicNumber,
        y: &CyclotomicNumber,
        k: i64,
    ) -> Result<Ordering, EmbeddingError> {
        let difference = x.sub(y)?;
        self.sign_under_embedding(&difference, k)
    }

    pub fn enclose(
        &mut self,
        x: &CyclotomicNumber,
        k: i64,
        tolerance: &Rational,
    ) -> Result<Interval, EmbeddingError> {
        let g = self.real_polynomial(x)?;
        self.enclose_polynomial(&g, k, tolerance)
    }
}

#[cfg(test)]
mod tests {
    use super::*;
    use crate::cyclotomic_field::sqrt_of_integer;
    use crate::polynomial::{count_real_roots, euler_phi, real_root_bound};
    use crate::rational::{r_zero, ri, rq};
    use crate::test_support::Lcg;

    fn zeta(n: usize, k: i64) -> CyclotomicNumber {
        CyclotomicNumber::zeta(n, k).unwrap()
    }

    fn t_of(n: usize) -> CyclotomicNumber {
        let z = zeta(n, 1);
        z.add(&z.conjugate()).unwrap()
    }

    fn real_grid_element(n: usize, rng: &mut Lcg) -> CyclotomicNumber {
        let degree = euler_phi(n);
        let coefficients = (0..degree)
            .map(|_| rq(rng.next_signed(4), 1 + rng.next_below(3) as i64))
            .collect();
        CyclotomicNumber::from_coefficients(n, coefficients)
            .unwrap()
            .real_part()
    }

    fn tiny() -> Rational {
        rq(1, 1_000_000_000_000)
    }


    #[test]
    fn there_are_phi_over_two_embeddings_indexed_by_classes_coprime_to_the_conductor() {
        for n in [5usize, 7, 8, 9, 12, 15, 20, 24, 30] {
            let e = RealEmbeddings::new(n).unwrap();
            assert_eq!(e.count(), euler_phi(n) / 2, "n = {n}");
            assert_eq!(e.classes().len(), e.count());
            assert!(
                e.classes().windows(2).all(|w| w[0] < w[1]),
                "classes ascend"
            );
            assert!(e
                .classes()
                .iter()
                .all(|k| *k >= 1 && 2 * k <= n && k.gcd(&n) == 1));
            assert_eq!(e.classes()[0], 1, "the canonical class is 1");
        }
        let e120 = real_embeddings(120).unwrap();
        assert_eq!(e120.count(), 16);
        assert_eq!(
            e120.classes(),
            &[1, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 49, 53, 59]
        );
        assert_eq!(RealEmbeddings::new(1).unwrap().count(), 1);
        assert_eq!(RealEmbeddings::new(2).unwrap().count(), 1);
        assert_eq!(RealEmbeddings::new(3).unwrap().count(), 1);
        assert_eq!(RealEmbeddings::new(4).unwrap().count(), 1);
        assert_eq!(RealEmbeddings::new(6).unwrap().count(), 1);
    }

    #[test]
    fn classes_are_taken_modulo_n_and_up_to_sign() {
        let mut e = RealEmbeddings::new(24).unwrap();
        let t = t_of(24);
        let canonical = e.sign_under_embedding(&t, 5).unwrap();
        for k in [5i64, -5, 19, -19, 29, 24 + 5, 24 * 7 - 5] {
            assert_eq!(e.sign_under_embedding(&t, k).unwrap(), canonical, "k = {k}");
        }
        assert_eq!(e.class_index(-1).unwrap(), 0);
        assert_eq!(e.class_index(23).unwrap(), 0);
        assert_eq!(e.class_index(25).unwrap(), 0);
    }

    #[test]
    fn a_class_that_shares_a_factor_with_the_conductor_is_refused() {
        let mut e = RealEmbeddings::new(24).unwrap();
        let t = t_of(24);
        for k in [0i64, 2, 3, 4, 6, 8, 9, 12, 24, 48] {
            assert_eq!(
                e.sign_under_embedding(&t, k),
                Err(EmbeddingError::InvalidClass { k, conductor: 24 }),
                "k = {k}"
            );
        }
        let mut e2 = RealEmbeddings::new(2).unwrap();
        assert!(
            e2.sign_under_embedding(&zeta(2, 1), 0).is_err(),
            "0 shares a factor with 2"
        );
        assert!(e2.sign_under_embedding(&zeta(2, 1), 1).is_ok());
    }

    #[test]
    fn the_largest_root_belongs_to_the_canonical_class_and_roots_decrease_with_k() {
        let mut e = RealEmbeddings::new(120).unwrap();
        let classes = e.classes().to_vec();
        let enclosures: Vec<Interval> = classes
            .iter()
            .map(|k| {
                e.root_enclosure(i64::try_from(*k).unwrap(), &tiny())
                    .unwrap()
            })
            .collect();
        for window in enclosures.windows(2) {
            assert!(
                window[0].lo() > window[1].hi(),
                "2cos(2 pi k/n) decreases with k: {:?} vs {:?}",
                window[0],
                window[1]
            );
        }
        assert!(enclosures[0].lo() > &rq(199, 100));
        assert!(enclosures.last().unwrap().hi() < &rq(-199, 100));
    }

    #[test]
    fn root_enclosures_agree_with_floating_cosines_as_a_test_only_oracle() {
        for n in [5usize, 7, 8, 12, 15, 24] {
            let mut e = RealEmbeddings::new(n).unwrap();
            for k in e.classes().to_vec() {
                let enclosure = e
                    .root_enclosure(i64::try_from(k).unwrap(), &tiny())
                    .unwrap();
                let expected = 2.0 * (2.0 * std::f64::consts::PI * (k as f64) / (n as f64)).cos();
                let mid = enclosure.mid();
                let as_float = mid.numer().to_string().parse::<f64>().unwrap()
                    / mid.denom().to_string().parse::<f64>().unwrap();
                assert!(
                    (as_float - expected).abs() < 1e-9,
                    "n = {n}, k = {k}: {as_float} vs {expected}"
                );
                assert!(enclosure.diam() <= tiny());
            }
        }
    }


    #[test]
    fn the_golden_witness_differs_between_the_two_embeddings_of_q_zeta_5() {
        let t = t_of(5);
        let two = CyclotomicNumber::from_rational(5, ri(2)).unwrap();
        let one = CyclotomicNumber::one(5).unwrap();
        let d1 = t.scale(&ri(2)).sub(&one).unwrap();
        let d2 = two.sub(&t.scale(&ri(2))).unwrap();
        let mut e = RealEmbeddings::new(5).unwrap();
        assert_eq!(e.sign_under_embedding(&d1, 1).unwrap(), Ordering::Greater);
        assert_eq!(e.sign_under_embedding(&d2, 1).unwrap(), Ordering::Greater);
        assert_eq!(e.sign_under_embedding(&d1, 2).unwrap(), Ordering::Less);
        assert_eq!(e.sign_under_embedding(&d2, 2).unwrap(), Ordering::Greater);
        let sqrt5 = t.scale(&ri(2)).add(&one).unwrap();
        assert_eq!(sqrt5, sqrt_of_integer(5, &BigInt::from(5)).unwrap());
        assert_eq!(
            e.signs(&sqrt5).unwrap(),
            vec![(1, Ordering::Greater), (2, Ordering::Less)]
        );
    }

    #[test]
    fn the_conductor_8_witness_differs_between_the_two_embeddings() {
        let t = t_of(8);
        let one = CyclotomicNumber::one(8).unwrap();
        let two = CyclotomicNumber::from_rational(8, ri(2)).unwrap();
        let d1 = t.sub(&one).unwrap();
        let d2 = two.sub(&t).unwrap();
        let mut e = RealEmbeddings::new(8).unwrap();
        assert_eq!(e.sign_under_embedding(&d1, 1).unwrap(), Ordering::Greater);
        assert_eq!(e.sign_under_embedding(&d1, 3).unwrap(), Ordering::Less);
        assert_eq!(e.sign_under_embedding(&d2, 1).unwrap(), Ordering::Greater);
        assert_eq!(e.sign_under_embedding(&d2, 3).unwrap(), Ordering::Greater);
    }

    #[test]
    fn two_minus_t_is_totally_positive_and_t_is_not() {
        for n in [3usize, 5, 7, 8, 9, 12, 15, 24, 30] {
            let mut e = RealEmbeddings::new(n).unwrap();
            let t = t_of(n);
            let two = CyclotomicNumber::from_rational(n, ri(2)).unwrap();
            assert!(
                e.is_positive_under_all_embeddings(&two.sub(&t).unwrap())
                    .unwrap(),
                "2 - t, n = {n}"
            );
            assert!(
                e.is_positive_under_all_embeddings(&two.add(&t).unwrap())
                    .unwrap(),
                "2 + t, n = {n}"
            );
            if e.count() > 1 {
                assert!(
                    !e.is_positive_under_all_embeddings(&t).unwrap(),
                    "t is not totally positive, n = {n}"
                );
            }
        }
    }

    #[test]
    fn conductors_one_and_two_have_the_exact_value_of_their_root() {
        let mut e1 = RealEmbeddings::new(1).unwrap();
        assert_eq!(e1.sign(&zeta(1, 1)).unwrap(), Ordering::Greater);
        assert_eq!(e1.root_location(1).unwrap(), RootLocation::Exact(ri(2)));
        let mut e2 = RealEmbeddings::new(2).unwrap();
        assert_eq!(e2.sign(&zeta(2, 1)).unwrap(), Ordering::Less);
        assert_eq!(e2.root_location(1).unwrap(), RootLocation::Exact(ri(-2)));
        assert_eq!(
            RealEmbeddings::new(3).unwrap().root_location(1).unwrap(),
            RootLocation::Exact(ri(-1))
        );
        assert_eq!(
            RealEmbeddings::new(4).unwrap().root_location(1).unwrap(),
            RootLocation::Exact(ri(0))
        );
        assert_eq!(
            RealEmbeddings::new(6).unwrap().root_location(1).unwrap(),
            RootLocation::Exact(ri(1))
        );
    }

    #[test]
    fn rational_elements_have_the_sign_of_the_rational_under_every_embedding() {
        let mut e = RealEmbeddings::new(12).unwrap();
        for (q, expected) in [
            (rq(3, 7), Ordering::Greater),
            (rq(-2, 9), Ordering::Less),
            (ri(0), Ordering::Equal),
        ] {
            let x = CyclotomicNumber::from_rational(12, q).unwrap();
            for (_, sign) in e.signs(&x).unwrap() {
                assert_eq!(sign, expected);
            }
        }
    }

    #[test]
    fn the_zero_element_is_decided_exactly_and_nonzero_elements_never_are_zero() {
        let mut e = RealEmbeddings::new(24).unwrap();
        let zero = CyclotomicNumber::zero(24).unwrap();
        assert_eq!(e.sign(&zero).unwrap(), Ordering::Equal);
        let psi = e.min_poly().clone();
        for k in e.classes().to_vec() {
            assert_eq!(
                e.sign_of_polynomial(&psi, i64::try_from(k).unwrap())
                    .unwrap(),
                Ordering::Equal,
                "Psi(t_{k}) = 0"
            );
        }
        let h = Polynomial::from_i64s(&[3, -1, 2]);
        let r = Polynomial::from_i64s(&[1, 1]);
        let g = psi.mul(&h).add(&r);
        for k in e.classes().to_vec() {
            let k = i64::try_from(k).unwrap();
            assert_eq!(
                e.sign_of_polynomial(&g, k).unwrap(),
                e.sign_of_polynomial(&r, k).unwrap()
            );
        }
        let x = t_of(24).add(&CyclotomicNumber::one(24).unwrap()).unwrap();
        assert!(e
            .signs(&x)
            .unwrap()
            .iter()
            .all(|(_, s)| *s != Ordering::Equal));
    }


    #[test]
    fn the_sign_under_embedding_k_equals_the_canonical_sign_of_the_galois_conjugate() {
        let mut rng = Lcg::new(2024);
        for n in [5usize, 7, 8, 9, 12, 15, 20, 24, 30] {
            let mut e = RealEmbeddings::new(n).unwrap();
            for _ in 0..3 {
                let x = real_grid_element(n, &mut rng);
                for k in e.classes().to_vec() {
                    let k = i64::try_from(k).unwrap();
                    let conjugate = x.galois(k).unwrap();
                    assert_eq!(
                        e.sign_under_embedding(&x, k).unwrap(),
                        e.sign(&conjugate).unwrap(),
                        "n = {n}, k = {k}, x = {x}"
                    );
                }
            }
        }
    }

    #[test]
    fn the_sign_of_a_constructed_square_root_follows_its_galois_action() {
        let cases: [(usize, i64); 8] = [
            (5, 5),
            (8, 2),
            (12, 3),
            (24, 6),
            (24, 2),
            (28, 7),
            (20, 5),
            (15, 5),
        ];
        for (n, d) in cases {
            let root = sqrt_of_integer(n, &BigInt::from(d)).unwrap();
            let mut e = RealEmbeddings::new(n).unwrap();
            assert_eq!(
                e.sign(&root).unwrap(),
                Ordering::Greater,
                "sqrt({d}) > 0 canonically in Q(zeta_{n})"
            );
            for k in e.classes().to_vec() {
                let k = i64::try_from(k).unwrap();
                let fixed = root.galois(k).unwrap() == root;
                let expected = if fixed {
                    Ordering::Greater
                } else {
                    Ordering::Less
                };
                assert_eq!(
                    e.sign_under_embedding(&root, k).unwrap(),
                    expected,
                    "n = {n}, d = {d}, k = {k}"
                );
            }
        }
    }

    fn characteristic_polynomial(n: usize, x: &CyclotomicNumber) -> Polynomial<Rational> {
        let psi = min_poly_of_2cos(n).unwrap();
        let m = psi.degree().unwrap();
        let g = x.real_part_polynomial();
        let points: Vec<Rational> = (0..=m).map(|i| ri(i64::try_from(i).unwrap())).collect();
        let values: Vec<Rational> = points
            .iter()
            .map(|y| psi.resultant(&Polynomial::constant(y.clone()).sub(&g)))
            .collect();
        let mut result = Polynomial::zero();
        for (i, yi) in values.iter().enumerate() {
            let mut basis = Polynomial::one();
            let mut denominator = Rational::from_integer(BigInt::one());
            for (j, xj) in points.iter().enumerate() {
                if i != j {
                    basis = basis.mul(&Polynomial::from_coefficients(vec![-xj.clone(), ri(1)]));
                    denominator = denominator * (&points[i] - xj);
                }
            }
            result = result.add(&basis.scale(&(yi / &denominator)));
        }
        result
    }

    #[test]
    fn counts_of_positive_and_negative_embeddings_match_sturm_counts_of_the_characteristic_polynomial(
    ) {
        let mut rng = Lcg::new(31337);
        let mut checked = 0;
        for n in [5usize, 7, 8, 9, 12, 15, 20, 24] {
            let mut e = RealEmbeddings::new(n).unwrap();
            for _ in 0..6 {
                let x = real_grid_element(n, &mut rng);
                let chi = characteristic_polynomial(n, &x);
                let Some(bound) = real_root_bound(&chi) else {
                    continue;
                };
                if chi.discriminant().map(|d| d == r_zero()).unwrap_or(true) {
                    continue;
                }
                let signs = e.signs(&x).unwrap();
                let positive = signs
                    .iter()
                    .filter(|(_, s)| *s == Ordering::Greater)
                    .count();
                let negative = signs.iter().filter(|(_, s)| *s == Ordering::Less).count();
                let by_sturm_positive = count_real_roots(&chi, &r_zero(), &bound).unwrap();
                let by_sturm_negative = count_real_roots(&chi, &-bound.clone(), &r_zero()).unwrap();
                assert_eq!(positive, by_sturm_positive, "n = {n}, x = {x}");
                assert_eq!(negative, by_sturm_negative, "n = {n}, x = {x}");
                assert_eq!(positive + negative, e.count());
                checked += 1;
            }
        }
        assert!(
            checked >= 20,
            "the grid must exercise many elements, got {checked}"
        );
    }

    #[test]
    fn signs_agree_with_floating_point_away_from_zero_as_a_test_only_oracle() {
        let mut rng = Lcg::new(4242);
        let mut compared = 0;
        for n in [5usize, 7, 8, 9, 12, 15, 24] {
            let mut e = RealEmbeddings::new(n).unwrap();
            for _ in 0..4 {
                let x = real_grid_element(n, &mut rng);
                let g = x.real_part_polynomial();
                for k in e.classes().to_vec() {
                    let t = 2.0 * (2.0 * std::f64::consts::PI * (k as f64) / (n as f64)).cos();
                    let mut value = 0.0f64;
                    for c in g.coefficients().iter().rev() {
                        let c = c.numer().to_string().parse::<f64>().unwrap()
                            / c.denom().to_string().parse::<f64>().unwrap();
                        value = value * t + c;
                    }
                    if value.abs() < 1e-6 {
                        continue;
                    }
                    let expected = if value > 0.0 {
                        Ordering::Greater
                    } else {
                        Ordering::Less
                    };
                    assert_eq!(
                        e.sign_under_embedding(&x, i64::try_from(k).unwrap())
                            .unwrap(),
                        expected,
                        "n = {n}, k = {k}, value = {value}"
                    );
                    compared += 1;
                }
            }
        }
        assert!(compared > 50);
    }

    #[test]
    fn comparison_of_real_elements_is_antisymmetric_transitive_and_translation_invariant() {
        let mut rng = Lcg::new(909);
        let n = 15;
        let mut e = RealEmbeddings::new(n).unwrap();
        for _ in 0..12 {
            let (x, y, z) = (
                real_grid_element(n, &mut rng),
                real_grid_element(n, &mut rng),
                real_grid_element(n, &mut rng),
            );
            for k in e.classes().to_vec() {
                let k = i64::try_from(k).unwrap();
                let forward = e.compare(&x, &y, k).unwrap();
                assert_eq!(
                    e.compare(&y, &x, k).unwrap(),
                    forward.reverse(),
                    "antisymmetry"
                );
                assert_eq!(forward == Ordering::Equal, x == y, "equality is exact");
                let shifted = e
                    .compare(&x.add(&z).unwrap(), &y.add(&z).unwrap(), k)
                    .unwrap();
                assert_eq!(shifted, forward, "translation invariance");
                if forward == Ordering::Less && e.compare(&y, &z, k).unwrap() == Ordering::Less {
                    assert_eq!(
                        e.compare(&x, &z, k).unwrap(),
                        Ordering::Less,
                        "transitivity"
                    );
                }
            }
        }
    }


    #[test]
    fn enclosures_contain_the_exact_value_and_respect_the_tolerance() {
        let n = 5;
        let sqrt5 = sqrt_of_integer(n, &BigInt::from(5)).unwrap();
        let mut e = RealEmbeddings::new(n).unwrap();
        let enclosure = e.enclose(&sqrt5, 1, &tiny()).unwrap();
        assert!(enclosure.diam() <= tiny());
        assert!(enclosure.lo() * enclosure.lo() < ri(5), "lo^2 < 5");
        assert!(enclosure.hi() * enclosure.hi() > ri(5), "hi^2 > 5");
        assert!(enclosure.lo().is_positive());
        let other = e.enclose(&sqrt5, 2, &tiny()).unwrap();
        assert!(other.hi().is_negative());
        assert!(other.lo() * other.lo() > ri(5) && other.hi() * other.hi() < ri(5));
        assert!(matches!(
            e.enclose(&sqrt5, 1, &r_zero()),
            Err(EmbeddingError::NonPositiveTolerance(_))
        ));
    }

    #[test]
    fn refinement_is_remembered_between_queries() {
        let mut e = RealEmbeddings::new(24).unwrap();
        let before = e.root_location(1).unwrap();
        e.root_enclosure(1, &rq(1, 1_000_000_000_000_000)).unwrap();
        let after = e.root_location(1).unwrap();
        assert!(
            after.width() < before.width(),
            "the stored interval narrowed"
        );
        let t = t_of(24);
        assert_eq!(e.sign(&t).unwrap(), Ordering::Greater);
    }


    #[test]
    fn a_non_real_element_is_refused_not_given_a_sign() {
        let mut e = RealEmbeddings::new(8).unwrap();
        assert_eq!(e.sign(&zeta(8, 1)), Err(EmbeddingError::NotReal));
        assert_eq!(
            e.sign(&zeta(8, 2)),
            Err(EmbeddingError::NotReal),
            "i is not real"
        );
        assert!(e.signs(&zeta(8, 3)).is_err());
        assert!(e.is_positive_under_all_embeddings(&zeta(8, 1)).is_err());
        assert!(e.enclose(&zeta(8, 1), 1, &tiny()).is_err());
        assert_eq!(e.sign(&zeta(8, 1).real_part()).unwrap(), Ordering::Greater);
    }

    #[test]
    fn an_element_of_another_field_is_refused() {
        let mut e = RealEmbeddings::new(8).unwrap();
        assert_eq!(
            e.sign(&CyclotomicNumber::one(12).unwrap()),
            Err(EmbeddingError::ConductorMismatch {
                element: 12,
                embeddings: 8
            })
        );
        assert!(e
            .compare(
                &CyclotomicNumber::one(8).unwrap(),
                &CyclotomicNumber::one(5).unwrap(),
                1
            )
            .is_err());
    }


    #[test]
    fn conductor_120_decides_every_sign_of_a_generic_real_element() {
        let mut e = RealEmbeddings::new(120).unwrap();
        let t = t_of(120);
        let x = t
            .mul(&t)
            .unwrap()
            .sub(&t.scale(&ri(3)))
            .unwrap()
            .add(&CyclotomicNumber::one(120).unwrap())
            .unwrap();
        let signs = e.signs(&x).unwrap();
        assert_eq!(signs.len(), 16);
        for (k, sign) in &signs {
            let tk = 2.0 * (2.0 * std::f64::consts::PI * (*k as f64) / 120.0).cos();
            let value = tk * tk - 3.0 * tk + 1.0;
            if value.abs() > 1e-6 {
                assert_eq!(
                    *sign,
                    if value > 0.0 {
                        Ordering::Greater
                    } else {
                        Ordering::Less
                    },
                    "k = {k}"
                );
            }
        }
    }
}
