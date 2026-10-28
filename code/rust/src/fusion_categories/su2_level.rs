use crate::braided::{BraidedFusionCategory, RSymbols, RibbonFusionCategory};
use crate::error::FusionError;
use crate::fusion_category::{FSymbols, FusionCategory};
use crate::fusion_ring::FusionRing;
use crate::scalar::{root_of_unity, FusionScalar};
use linear_algebra::backend::basic_matrix::BasicMatrix;
use linear_algebra::exact_field::{involution, matrix};

pub const MAX_LEVEL: usize = 6;

fn checked_level(level: usize) -> Result<(), FusionError> {
    if level == 0 || level > MAX_LEVEL {
        return Err(FusionError::Budget {
            what: "SU(2) level (positive)",
            requested: level as u128,
            limit: MAX_LEVEL as u128,
        });
    }
    Ok(())
}

pub fn quantum_integer<K: FusionScalar>(level: usize, n: usize) -> Result<K, FusionError> {
    checked_level(level)?;
    if n > 2 * (level + 2) {
        return Err(FusionError::Budget {
            what: "q-integer index",
            requested: n as u128,
            limit: (2 * (level + 2)) as u128,
        });
    }
    let q = root_of_unity::<K>((2 * (level + 2)) as u32, 1)?;
    let q_inverse = tfqm_number_theory::scalar::inverse(&q).map_err(FusionError::from)?;
    let numerator = tfqm_number_theory::scalar::power_unsigned(&q, n as u64)
        .map_err(FusionError::from)?
        .sub(
            &tfqm_number_theory::scalar::power_unsigned(&q_inverse, n as u64)
                .map_err(FusionError::from)?,
        );
    tfqm_number_theory::scalar::divide(&numerator, &q.sub(&q_inverse)).map_err(FusionError::from)
}

fn triangle_squared<K: FusionScalar>(
    a: usize,
    b: usize,
    c: usize,
    factorials: &[K],
) -> Result<K, FusionError> {
    // Private admitted SU(2) triangle: even perimeter <= 2*level.
    let half = (a + b + c) / 2;
    let numerator = factorials[half - a]
        .mul(&factorials[half - b])
        .mul(&factorials[half - c]);
    tfqm_number_theory::scalar::divide(&numerator, &factorials[half + 1])
        .map_err(FusionError::from)
}

fn racah_term<K: FusionScalar>(
    z: usize,
    lower: &[usize; 4],
    upper: &[usize; 3],
    factorials: &[K],
) -> Result<K, FusionError> {
    let mut denominator = K::one();
    for &s in lower {
        denominator = denominator.mul(&factorials[z - s]);
    }
    for &s in upper {
        denominator = denominator.mul(&factorials[s - z]);
    }
    tfqm_number_theory::scalar::divide(&factorials[z + 1], &denominator).map_err(FusionError::from)
}

fn racah_sum<K: FusionScalar>(
    level: usize,
    lower: &[usize; 4],
    upper: &[usize; 3],
    factorials: &[K],
) -> Result<K, FusionError> {
    let start = lower.iter().copied().fold(0, usize::max);
    let end = upper.iter().copied().fold(level, usize::min);
    let mut sum = K::zero();
    for z in start..=end {
        let term = racah_term(z, lower, upper, factorials)?;
        sum = if z % 2 == 0 {
            sum.add(&term)
        } else {
            sum.sub(&term)
        };
    }
    Ok(sum)
}

fn associator<K: FusionScalar>(
    level: usize,
    [a, b, c, d]: [usize; 4],
    e: usize,
    f: usize,
    dimensions: &[K],
    factorials: &[K],
) -> Result<K, FusionError> {
    let lower = [
        (a + b + e) / 2,
        (e + c + d) / 2,
        (b + c + f) / 2,
        (a + f + d) / 2,
    ];
    let upper = [
        (a + b + c + d) / 2,
        (a + c + e + f) / 2,
        (b + d + e + f) / 2,
    ];
    let sum = racah_sum(level, &lower, &upper, factorials)?;
    let value = dimensions[e]
        .mul(&triangle_squared(a, b, e, factorials)?)
        .mul(&triangle_squared(e, c, d, factorials)?)
        .mul(&sum);
    Ok(if (a + b + c + d) / 2 % 2 == 0 {
        value
    } else {
        value.neg()
    })
}

fn quantum_dimensions<K: FusionScalar>(level: usize) -> Result<Vec<K>, FusionError> {
    // Caller admitted 1<=level<=6. One root/inverse and one denominator admission.
    let q = root_of_unity::<K>((2 * (level + 2)) as u32, 1)?;
    let inverse = tfqm_number_theory::scalar::inverse(&q).map_err(FusionError::from)?;
    let difference = q.sub(&inverse);
    let one =
        tfqm_number_theory::scalar::divide(&difference, &difference).map_err(FusionError::from)?;
    let step = q.add(&inverse);
    let mut dimensions = Vec::with_capacity(level + 1);
    dimensions.push(one);
    dimensions.push(step);
    for a in 2..=level {
        let next = dimensions[1]
            .mul(&dimensions[a - 1])
            .sub(&dimensions[a - 2]);
        dimensions.push(next);
    }
    Ok(dimensions)
}

fn coefficient_data<K: FusionScalar>(level: usize) -> Result<(Vec<K>, Vec<K>), FusionError> {
    let dimensions = quantum_dimensions::<K>(level)?;
    let mut factorials = Vec::with_capacity(level + 2);
    factorials.push(K::one());
    for (index, dimension) in dimensions.iter().enumerate() {
        factorials.push(factorials[index].mul(dimension));
    }
    Ok((dimensions, factorials))
}

fn tree_weight<K: FusionScalar>(
    channel: usize,
    total: usize,
    left: [usize; 3],
    right: [usize; 3],
    dimensions: &[K],
    factorials: &[K],
) -> Result<K, FusionError> {
    let squared = dimensions[channel]
        .mul(&dimensions[total])
        .mul(&triangle_squared(left[0], left[1], left[2], factorials)?)
        .mul(&triangle_squared(right[0], right[1], right[2], factorials)?);
    tfqm_number_theory::scalar::inverse(&squared).map_err(FusionError::from)
}

fn metric_diagonal<K: FusionScalar>(
    channels: &[usize],
    mut weight: impl FnMut(usize) -> Result<K, FusionError>,
) -> Result<BasicMatrix<K>, FusionError> {
    BasicMatrix::try_from_fn_result(channels.len(), channels.len(), |row, col| {
        if row == col {
            weight(channels[row])
        } else {
            Ok(K::zero())
        }
    })
}

fn tree_metrics_for_channels<K: FusionScalar>(
    [a, b, c, d]: [usize; 4],
    left: &[usize],
    right: &[usize],
    dimensions: &[K],
    factorials: &[K],
) -> Result<(BasicMatrix<K>, BasicMatrix<K>), FusionError> {
    Ok((
        metric_diagonal(left, |e| {
            tree_weight(e, d, [a, b, e], [e, c, d], dimensions, factorials)
        })?,
        metric_diagonal(right, |f| {
            tree_weight(f, d, [b, c, f], [a, f, d], dimensions, factorials)
        })?,
    ))
}

fn tree_metrics<K: FusionScalar>(
    ring: &FusionRing,
    [a, b, c, d]: [usize; 4],
    dimensions: &[K],
    factorials: &[K],
) -> Result<(BasicMatrix<K>, BasicMatrix<K>), FusionError> {
    let left = (0..ring.rank())
        .filter(|&e| ring.n(a, b, e) > 0 && ring.n(e, c, d) > 0)
        .collect::<Vec<_>>();
    let right = (0..ring.rank())
        .filter(|&f| ring.n(b, c, f) > 0 && ring.n(a, f, d) > 0)
        .collect::<Vec<_>>();
    tree_metrics_for_channels([a, b, c, d], &left, &right, dimensions, factorials)
}

pub fn associator_metrics<K: FusionScalar>(
    level: usize,
    labels: [usize; 4],
) -> Result<(BasicMatrix<K>, BasicMatrix<K>), FusionError> {
    checked_level(level)?;
    if let Some(&label) = labels.iter().find(|&&a| a > level) {
        return Err(FusionError::Label {
            label,
            rank: level + 1,
        });
    }
    let ring = FusionRing::su2_level(level)?;
    let (dimensions, factorials) = coefficient_data::<K>(level)?;
    tree_metrics(&ring, labels, &dimensions, &factorials)
}

fn require_weighted_unitarity<K: FusionScalar>(
    f: &BasicMatrix<K>,
    left: &BasicMatrix<K>,
    right: &BasicMatrix<K>,
) -> Result<(), FusionError> {
    let weighted = matrix::multiply(
        &involution::adjoint(f).map_err(FusionError::from)?,
        &matrix::multiply(left, f).map_err(FusionError::from)?,
    )
    .map_err(FusionError::from)?;
    if weighted != *right {
        return Err(FusionError::Inconsistent {
            context: "q-Racah weighted unitarity",
        });
    }
    Ok(())
}

fn check_associator_metrics<K: FusionScalar>(
    category: &FusionCategory<K>,
    dimensions: &[K],
    factorials: &[K],
) -> Result<(), FusionError> {
    for (labels, block) in category.f_symbols().blocks() {
        let (left, right) =
            tree_metrics_for_channels(*labels, block.rows(), block.cols(), dimensions, factorials)?;
        require_weighted_unitarity(block.matrix(), &left, &right)?;
    }
    Ok(())
}

fn phase_table<K: FusionScalar>(root: &K, order: usize) -> Vec<K> {
    // Private order=8*(level+2), hence 24..=64; root has this exact order.
    let mut phases = Vec::with_capacity(order);
    phases.push(K::one());
    for index in 1..order {
        let next = phases[index - 1].mul(root);
        phases.push(next);
    }
    phases
}

fn braiding_value<K: FusionScalar>([a, b, c]: [usize; 3], phases: &[K]) -> K {
    // Only admitted SU(2) fusion channels reach this callback: a+b>=c, even sum.
    let exponent = (c * (c + 2)) as i64 - (a * (a + 2)) as i64 - (b * (b + 2)) as i64;
    let value = phases[exponent.rem_euclid(phases.len() as i64) as usize].clone();
    if (a + b - c) / 2 % 2 == 0 {
        value
    } else {
        value.neg()
    }
}

pub fn su2_level<K: FusionScalar>(level: usize) -> Result<RibbonFusionCategory<K>, FusionError> {
    checked_level(level)?;
    let root_order = 8 * (level + 2);
    let braiding_root = root_of_unity::<K>(root_order as u32, 1)?;
    let ring = FusionRing::su2_level(level)?;
    let (dimensions, factorials) = coefficient_data::<K>(level)?;
    let f = FSymbols::try_from_fn(&ring, |labels, e, f| {
        associator(level, labels, e, f, &dimensions, &factorials)
    })?;
    let category = FusionCategory::new(ring, f)?;
    check_associator_metrics(&category, &dimensions, &factorials)?;
    let phases = phase_table(&braiding_root, root_order);
    let r = RSymbols::from_fn(category.ring(), |labels| braiding_value(labels, &phases))?;
    RibbonFusionCategory::try_new(BraidedFusionCategory::new(category, r)?, dimensions)
}

#[cfg(test)]
mod tests {
    use super::*;
    use crate::braided::HexagonForm;
    use crate::modular::ModularData;
    use tfqm_number_theory::cyclotomic_field::Cyclotomic;

    fn replay<K: FusionScalar>(k: usize) {
        let model = su2_level::<K>(k).unwrap();
        assert!(model.category().first_pentagon_defect().is_none());
        assert!(model
            .braided()
            .first_hexagon_defect(HexagonForm::Direct)
            .is_none());
        assert!(model
            .braided()
            .first_hexagon_defect(HexagonForm::Mirror)
            .is_none());
        model
            .category()
            .verify_dimensions(model.dimensions())
            .unwrap();
        let modular = ModularData::verified(&model).unwrap();
        assert_eq!(
            modular.central_charge_mod_4().unwrap(),
            tfqm_number_theory::rational::rq((3 * k) as i64, (k + 2) as i64)
        );
        for a in 0..=k {
            assert_eq!(
                model.twists()[a],
                root_of_unity::<K>((4 * (k + 2)) as u32, (a * (a + 2)) as i64).unwrap()
            );
        }
    }
    #[test]
    fn racah_formula_replays_pentagon_hexagons_and_verlinde_through_maximum_level() {
        replay::<Cyclotomic<24>>(1);
        replay::<Cyclotomic<32>>(2);
        replay::<Cyclotomic<40>>(3);
        replay::<Cyclotomic<48>>(4);
        replay::<Cyclotomic<56>>(5);
        replay::<Cyclotomic<64>>(MAX_LEVEL);
    }
    #[test]
    fn level_three_has_actual_fibonacci_subcategory_and_nonorthonormal_gauge() {
        type K = Cyclotomic<40>;
        let model = su2_level::<K>(3).unwrap();
        assert_eq!(model.ring().fuse(2, 2).unwrap(), vec![0, 2]);
        let phi = model.dimensions()[2].clone();
        assert_eq!(phi.mul(&phi), phi.add(&K::one()));
        assert!(!model.category().is_unitary().unwrap());
        let (left, right) = associator_metrics::<K>(3, [2, 2, 2, 2]).unwrap();
        let f = model
            .category()
            .f_symbols()
            .block([2, 2, 2, 2])
            .unwrap()
            .matrix();
        assert_eq!(
            matrix::multiply(
                &involution::adjoint(f).map_err(FusionError::from).unwrap(),
                &matrix::multiply(&left, f)
                    .map_err(FusionError::from)
                    .unwrap()
            )
            .map_err(FusionError::from)
            .unwrap(),
            right
        );
        let bad = model
            .category()
            .f_symbols()
            .with_entry([2, 2, 2, 2], 0, 2, K::zero())
            .unwrap();
        let tampered = FusionCategory::new(model.ring().clone(), bad).unwrap();
        assert!(tampered.first_pentagon_defect().is_some());
    }
    #[test]
    fn unsupported_field_and_unbounded_level_are_typed_refusals() {
        assert!(matches!(
            su2_level::<Cyclotomic<8>>(3),
            Err(FusionError::FieldTooSmall { .. })
        ));
        assert!(matches!(
            su2_level::<Cyclotomic<40>>(usize::MAX),
            Err(FusionError::Budget { .. })
        ));
        assert!(matches!(
            su2_level::<Cyclotomic<64>>(MAX_LEVEL + 1),
            Err(FusionError::Budget { .. })
        ));
        assert!(matches!(
            su2_level::<Cyclotomic<40>>(0),
            Err(FusionError::Budget { .. })
        ));
    }
}
