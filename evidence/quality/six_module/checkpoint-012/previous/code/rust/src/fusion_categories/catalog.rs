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
    let zeta = |k: i64| root_of_unity::<K>(16, k);
    let sqrt2 = sqrt_two::<K>()?;
    let inverse_sqrt2 = omega_number_theory::scalar::inverse(&sqrt2).map_err(FusionError::from)?;
    let negative_inverse_sqrt2 = inverse_sqrt2.neg();
    let minus_one = K::one().neg();
    let f = FSymbols::from_fn(&ring, |labels, e, f| match (labels, e, f) {
        ([1, 1, 1, 1], 2, 2) => negative_inverse_sqrt2.clone(),
        ([1, 1, 1, 1], _, _) => inverse_sqrt2.clone(),
        ([1, 2, 1, 2] | [2, 1, 2, 1], _, _) => minus_one.clone(),
        _ => K::one(),
    })?;
    let z_minus_1 = zeta(-1)?;
    let z_3 = zeta(3)?;
    let minus_i = zeta(4)?.neg();
    let r = RSymbols::from_fn(&ring, |labels| match labels {
        [1, 1, 0] => z_minus_1.clone(),
        [1, 1, 2] => z_3.clone(),
        [1, 2, 1] | [2, 1, 1] => minus_i.clone(),
        [2, 2, 0] => minus_one.clone(),
        _ => K::one(),
    })?;
    ribbon(ring, f, r, vec![K::one(), sqrt2, K::one()])
}

pub fn fibonacci<K: FusionScalar>() -> Result<RibbonFusionCategory<K>, FusionError> {
    let ring = FusionRing::fibonacci()?;
    let phi = golden_ratio::<K>()?;
    let phi_inverse = phi.sub(&K::one());
    let minus_phi_inverse = phi_inverse.neg();
    let f = FSymbols::from_fn(&ring, |labels, e, f| match (labels, e, f) {
        ([1, 1, 1, 1], 0, 0) | ([1, 1, 1, 1], 1, 0) => phi_inverse.clone(),
        ([1, 1, 1, 1], 1, 1) => minus_phi_inverse.clone(),
        _ => K::one(),
    })?;
    let z_minus_4 = root_of_unity::<K>(10, -4)?;
    let z_3 = root_of_unity::<K>(10, 3)?;
    let r = RSymbols::from_fn(&ring, |labels| match labels {
        [1, 1, 0] => z_minus_4.clone(),
        [1, 1, 1] => z_3.clone(),
        _ => K::one(),
    })?;
    ribbon(ring, f, r, vec![K::one(), phi])
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
    let r = moduli.len();
    if exponents.len() != r || exponents.iter().any(|row| row.len() != r) {
        return Err(FusionError::ListLength {
            what: "rows of bicharacter exponents",
            expected: r,
            got: exponents.len(),
        });
    }
    let gcd = |a: usize, b: usize| -> usize {
        let (mut a, mut b) = (a, b);
        while b != 0 {
            (a, b) = (b, a % b);
        }
        a
    };
    let denominators: Vec<Vec<usize>> = (0..r)
        .map(|i| {
            (0..r)
                .map(|j| {
                    gcd(
                        moduli.get(i).copied().unwrap_or(1),
                        moduli.get(j).copied().unwrap_or(1),
                    )
                })
                .collect()
        })
        .collect();
    let mut lcm: usize = 1;
    for (i, row) in exponents.iter().enumerate() {
        for (j, &b) in row.iter().enumerate() {
            if b != 0 {
                let g = denominators
                    .get(i)
                    .and_then(|row| row.get(j))
                    .copied()
                    .unwrap_or(1);
                lcm = lcm / gcd(lcm, g) * g;
            }
        }
    }
    let order = group.order();
    let ring = FusionRing::pointed(moduli, names)?;
    let f = FSymbols::trivial(&ring)?;
    let modulus = u32::try_from(lcm).map_err(|_| FusionError::Overflow {
        context: "the order of the bicharacter's roots of unity",
    })?;
    let mut failure: Option<FusionError> = None;
    let r_symbols = RSymbols::from_fn(&ring, |[x, y, _]| {
        let phase = (|| -> Result<K, FusionError> {
            let dx = group.digits(x)?;
            let dy = group.digits(y)?;
            let mut exponent: i128 = 0;
            for i in 0..r {
                for j in 0..r {
                    let b = exponents
                        .get(i)
                        .and_then(|row| row.get(j))
                        .copied()
                        .unwrap_or(0);
                    let g = denominators
                        .get(i)
                        .and_then(|row| row.get(j))
                        .copied()
                        .unwrap_or(1);
                    let xi = dx.get(i).copied().unwrap_or(0);
                    let yj = dy.get(j).copied().unwrap_or(0);
                    exponent += i128::from(b) * xi as i128 * yj as i128 * (lcm / g) as i128;
                }
            }
            let reduced = exponent.rem_euclid(i128::from(modulus));
            root_of_unity::<K>(
                modulus,
                i64::try_from(reduced).map_err(|_| FusionError::Overflow {
                    context: "the bicharacter exponent",
                })?,
            )
        })();
        match phase {
            Ok(value) => value,
            Err(error) => {
                failure.get_or_insert(error);
                K::one()
            }
        }
    })?;
    if let Some(error) = failure {
        return Err(error);
    }
    ribbon(ring, f, r_symbols, (0..order).map(|_| K::one()).collect())
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
