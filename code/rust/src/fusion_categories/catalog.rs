use crate::braided::{BraidedFusionCategory, RSymbols, RibbonFusionCategory};
use crate::error::FusionError;
use crate::fusion_category::{FSymbols, FusionCategory};
use crate::fusion_ring::{AbelianGroup, FusionRing};
use crate::scalar::{golden_ratio, root_of_unity, sqrt_two, FusionScalar};

fn ribbon<K: FusionScalar>(
    ring: FusionRing,
    f: FSymbols<K>,
    r: RSymbols<K>,
    dimensions: Vec<K>,
) -> Result<RibbonFusionCategory<K>, FusionError> {
    let category = FusionCategory::new(ring, f)?;
    RibbonFusionCategory::try_new(BraidedFusionCategory::new(category, r)?, dimensions)
}

pub fn ising<K: FusionScalar>() -> Result<RibbonFusionCategory<K>, FusionError> {
    let ring = FusionRing::ising()?;
    let sqrt2 = sqrt_two::<K>()?;
    let f = ising_f(&ring, &sqrt2)?;
    let r = ising_r(&ring)?;
    ribbon(ring, f, r, vec![K::one(), sqrt2, K::one()])
}

fn ising_f<K: FusionScalar>(ring: &FusionRing, sqrt2: &K) -> Result<FSymbols<K>, FusionError> {
    let inverse = tfqm_number_theory::scalar::inverse(sqrt2).map_err(FusionError::from)?;
    let negative = inverse.neg();
    let minus_one = K::one().neg();
    FSymbols::from_fn(ring, |labels, e, f| match (labels, e, f) {
        ([1, 1, 1, 1], 2, 2) => negative.clone(),
        ([1, 1, 1, 1], _, _) => inverse.clone(),
        ([1, 2, 1, 2] | [2, 1, 2, 1], _, _) => minus_one.clone(),
        _ => K::one(),
    })
}

fn ising_r<K: FusionScalar>(ring: &FusionRing) -> Result<RSymbols<K>, FusionError> {
    let minus_1 = root_of_unity::<K>(16, -1)?;
    let three = root_of_unity::<K>(16, 3)?;
    let minus_i = root_of_unity::<K>(16, 4)?.neg();
    let minus_one = K::one().neg();
    RSymbols::from_fn(ring, |labels| match labels {
        [1, 1, 0] => minus_1.clone(),
        [1, 1, 2] => three.clone(),
        [1, 2, 1] | [2, 1, 1] => minus_i.clone(),
        [2, 2, 0] => minus_one.clone(),
        _ => K::one(),
    })
}

pub fn fibonacci<K: FusionScalar>() -> Result<RibbonFusionCategory<K>, FusionError> {
    let ring = FusionRing::fibonacci()?;
    let phi = golden_ratio::<K>()?;
    let f = fibonacci_f(&ring, &phi)?;
    let r = fibonacci_r(&ring)?;
    ribbon(ring, f, r, vec![K::one(), phi])
}

fn fibonacci_f<K: FusionScalar>(ring: &FusionRing, phi: &K) -> Result<FSymbols<K>, FusionError> {
    let inverse = phi.sub(&K::one());
    let negative = inverse.neg();
    FSymbols::from_fn(ring, |labels, e, f| match (labels, e, f) {
        ([1, 1, 1, 1], 0, 0) | ([1, 1, 1, 1], 1, 0) => inverse.clone(),
        ([1, 1, 1, 1], 1, 1) => negative.clone(),
        _ => K::one(),
    })
}

fn fibonacci_r<K: FusionScalar>(ring: &FusionRing) -> Result<RSymbols<K>, FusionError> {
    let minus_four = root_of_unity::<K>(10, -4)?;
    let three = root_of_unity::<K>(10, 3)?;
    RSymbols::from_fn(ring, |labels| match labels {
        [1, 1, 0] => minus_four.clone(),
        [1, 1, 1] => three.clone(),
        _ => K::one(),
    })
}

pub fn semion<K: FusionScalar>() -> Result<RibbonFusionCategory<K>, FusionError> {
    let ring = FusionRing::semion()?;
    let minus_one = K::one().neg();
    let f = FSymbols::from_fn(&ring, |labels, _, _| {
        if labels == [1, 1, 1, 1] {
            minus_one.clone()
        } else {
            K::one()
        }
    })?;
    let i = root_of_unity::<K>(4, 1)?;
    let r = RSymbols::from_fn(&ring, |labels| {
        if labels == [1, 1, 0] {
            i.clone()
        } else {
            K::one()
        }
    })?;
    ribbon(ring, f, r, vec![K::one(), K::one()])
}

pub fn pointed_braided<K: FusionScalar>(
    moduli: &[usize],
    exponents: &[Vec<i64>],
    names: Option<Vec<String>>,
) -> Result<RibbonFusionCategory<K>, FusionError> {
    let group = AbelianGroup::new(moduli)?;
    check_exponent_shape(exponents, moduli.len())?;
    let plan = PhasePlan::new(moduli, exponents);
    let order = group.order();
    let ring = FusionRing::pointed(moduli, names)?;
    // Admit the actual root subgroup before expensive symbol construction.
    let roots = phase_roots::<K>(plan.order)?;
    let digits = (0..order)
        .map(|x| group.digits(x))
        .collect::<Result<Vec<_>, _>>()?;
    let f = FSymbols::trivial(&ring)?;
    let r = RSymbols::from_fn(&ring, |[x, y, _]| {
        roots[plan.exponent(&digits[x], &digits[y])].clone()
    })?;
    ribbon(ring, f, r, (0..order).map(|_| K::one()).collect())
}

fn check_exponent_shape(exponents: &[Vec<i64>], factors: usize) -> Result<(), FusionError> {
    if exponents.len() != factors {
        return Err(FusionError::ListLength {
            what: "rows of bicharacter exponents",
            expected: factors,
            got: exponents.len(),
        });
    }
    if let Some(row) = exponents.iter().find(|row| row.len() != factors) {
        return Err(FusionError::ListLength {
            what: "columns of bicharacter exponents",
            expected: factors,
            got: row.len(),
        });
    }
    Ok(())
}

fn gcd(mut a: usize, mut b: usize) -> usize {
    while b != 0 {
        (a, b) = (b, a % b);
    }
    a
}

fn reduced_coefficient(coefficient: i64, left: usize, right: usize) -> (usize, usize) {
    // Private admitted moduli are 2..=32; the residue is at most 31.
    let denominator = gcd(left, right);
    let numerator = coefficient.rem_euclid(denominator as i64) as usize;
    let common = gcd(numerator, denominator);
    (numerator / common, denominator / common)
}

struct PhasePlan {
    order: usize,
    weights: Vec<Vec<usize>>,
}

impl PhasePlan {
    fn new(moduli: &[usize], exponents: &[Vec<i64>]) -> Self {
        // Caller established product(moduli)<=32 and the square exponent shape.
        let mut order = 1;
        for (i, row) in exponents.iter().enumerate() {
            for (j, &coefficient) in row.iter().enumerate() {
                let (_, denominator) = reduced_coefficient(coefficient, moduli[i], moduli[j]);
                order = order / gcd(order, denominator) * denominator;
            }
        }
        let weights = exponents
            .iter()
            .enumerate()
            .map(|(i, row)| {
                row.iter()
                    .enumerate()
                    .map(|(j, &coefficient)| {
                        let (numerator, denominator) =
                            reduced_coefficient(coefficient, moduli[i], moduli[j]);
                        numerator * (order / denominator)
                    })
                    .collect()
            })
            .collect();
        Self { order, weights }
    }

    fn exponent(&self, left: &[usize], right: &[usize]) -> usize {
        let mut total = 0;
        for (row, &x) in self.weights.iter().zip(left) {
            for (&weight, &y) in row.iter().zip(right) {
                total += weight * x * y;
            }
        }
        total % self.order
    }
}

fn phase_roots<K: FusionScalar>(order: usize) -> Result<Vec<K>, FusionError> {
    let generator = root_of_unity::<K>(order as u32, 1)?;
    let mut roots = Vec::with_capacity(order);
    roots.push(K::one());
    for i in 1..order {
        let next = roots[i - 1].mul(&generator);
        roots.push(next);
    }
    Ok(roots)
}

pub fn toric_code<K: FusionScalar>() -> Result<RibbonFusionCategory<K>, FusionError> {
    pointed_braided(
        &[2, 2],
        &[vec![0, 1], vec![0, 0]],
        Some(["1", "e", "m", "eps"].map(String::from).to_vec()),
    )
}

pub fn three_fermion<K: FusionScalar>() -> Result<RibbonFusionCategory<K>, FusionError> {
    pointed_braided(
        &[2, 2],
        &[vec![1, 1], vec![0, 1]],
        Some(["1", "f1", "f2", "f3"].map(String::from).to_vec()),
    )
}

pub fn quantum_double_cyclic<K: FusionScalar>(
    n: usize,
) -> Result<RibbonFusionCategory<K>, FusionError> {
    let i64_n = i64::try_from(n).map_err(|_| FusionError::Overflow {
        context: "the order of a quantum double",
    })?;
    if i64_n < 2 {
        return Err(FusionError::RankOutOfRange {
            rank: n,
            max: crate::fusion_ring::MAX_RANK,
        });
    }
    pointed_braided(&[n, n], &[vec![0, 1], vec![0, 0]], None)
}

pub fn cyclic_pointed<K: FusionScalar>(
    n: usize,
    k: i64,
) -> Result<RibbonFusionCategory<K>, FusionError> {
    pointed_braided(&[n], &[vec![k]], None)
}
