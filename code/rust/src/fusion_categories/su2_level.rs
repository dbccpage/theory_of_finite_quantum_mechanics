//! Exact SU(2)_k associators and braidings in an algebraic Racah gauge.
//!
//! Simple labels `a=0..k` are twice the spins. Set `q=exp(pi i/(k+2))` and
//! `[n]=(q^n-q^-n)/(q-q^-1)`. The usual unitary q-6j expression is transformed
//! by the vertex gauge `u^{ab}_c=sqrt([c+1]) Delta(a,b,c)`. The resulting
//! F-symbols are `(-1)^((a+b+c+d)/2) [e+1] Delta(a,b,e)^2
//! Delta(e,c,d)^2` times the Racah sum. They need no square roots and lie in
//! `Q(zeta_(8(k+2)))`. This gauge is generally not orthonormal: its F-matrices
//! must not be advertised as unitary in the ordinary coordinate inner product.
//!
//! Every returned category has replayed the unit laws, pentagon, both hexagons,
//! quantum dimensions, twists and ribbon balance. Level and coefficient-field
//! refusals are explicit. AuthorityEffect: None.

use crate::braided::{BraidedFusionCategory, RSymbols, RibbonFusionCategory};
use crate::error::FusionError;
use crate::fusion_category::{FSymbols, FusionCategory};
use crate::fusion_ring::FusionRing;
use crate::scalar::{root_of_unity, FusionScalar};
use linear_algebra::backend::basic_matrix::BasicMatrix;
use linear_algebra::exact_field::{involution, matrix};

/// The general formula is evaluated only through this bounded level. The bound
/// controls the rank-dependent exhaustive pentagon replay, not the mathematics
/// of the SU(2) family.
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

/// The exact q-integer at level `k`. An index above `2(k+2)` is refused to
/// bound an independently requested coefficient evaluation.
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
    let numerator = omega_number_theory::scalar::power(&q, n as i64)
        .map_err(FusionError::from)?
        .sub(&omega_number_theory::scalar::power(&q, -(n as i64)).map_err(FusionError::from)?);
    omega_number_theory::scalar::divide(
        &numerator,
        &q.sub(&omega_number_theory::scalar::power(&q, -1).map_err(FusionError::from)?),
    )
    .map_err(FusionError::from)
}

fn triangle_squared<K: FusionScalar>(
    a: usize,
    b: usize,
    c: usize,
    factorials: &[K],
) -> Result<K, FusionError> {
    let half = (a + b + c) / 2;
    let numerator = factorials[half - a]
        .mul(&factorials[half - b])
        .mul(&factorials[half - c]);
    omega_number_theory::scalar::divide(&numerator, &factorials[half + 1])
        .map_err(FusionError::from)
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
    let start = *lower.iter().max().ok_or(FusionError::Inconsistent {
        context: "Racah lower limit",
    })?;
    // Terms z>k have [z+1]!=0. All denominator factorials of admissible
    // labels have indices <=k, so omitting those zero terms is exact.
    let end = level.min(*upper.iter().min().ok_or(FusionError::Inconsistent {
        context: "Racah upper limit",
    })?);
    let mut sum = K::zero();
    for z in start..=end {
        let mut denominator = K::one();
        for &s in &lower {
            denominator = denominator.mul(&factorials[z - s]);
        }
        for &s in &upper {
            denominator = denominator.mul(&factorials[s - z]);
        }
        let term = omega_number_theory::scalar::divide(&factorials[z + 1], &denominator)
            .map_err(FusionError::from)?;
        sum = if z % 2 == 0 {
            sum.add(&term)
        } else {
            sum.sub(&term)
        };
    }
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

fn coefficient_data<K: FusionScalar>(level: usize) -> Result<(Vec<K>, Vec<K>), FusionError> {
    let dimensions = (0..=level)
        .map(|a| quantum_integer::<K>(level, a + 1))
        .collect::<Result<Vec<_>, _>>()?;
    let mut factorials = vec![K::one()];
    for n in 1..=level + 1 {
        factorials.push(factorials[n - 1].mul(&quantum_integer::<K>(level, n)?));
    }
    Ok((dimensions, factorials))
}
fn tree_metrics<K: FusionScalar>(
    ring: &FusionRing,
    [a, b, c, d]: [usize; 4],
    dimensions: &[K],
    factorials: &[K],
) -> Result<(BasicMatrix<K>, BasicMatrix<K>), FusionError> {
    let left = (0..ring.rank())
        .filter(|&e| ring.n(a, b, e) > 0 && ring.n(e, c, d) > 0)
        .map(|e| {
            let squared = dimensions[e]
                .mul(&dimensions[d])
                .mul(&triangle_squared(a, b, e, factorials)?)
                .mul(&triangle_squared(e, c, d, factorials)?);
            omega_number_theory::scalar::inverse(&squared).map_err(FusionError::from)
        })
        .collect::<Result<Vec<_>, _>>()?;
    let right = (0..ring.rank())
        .filter(|&f| ring.n(b, c, f) > 0 && ring.n(a, f, d) > 0)
        .map(|f| {
            let squared = dimensions[f]
                .mul(&dimensions[d])
                .mul(&triangle_squared(b, c, f, factorials)?)
                .mul(&triangle_squared(a, f, d, factorials)?);
            omega_number_theory::scalar::inverse(&squared).map_err(FusionError::from)
        })
        .collect::<Result<Vec<_>, _>>()?;
    Ok((
        matrix::diagonal(&left).map_err(FusionError::from)?,
        matrix::diagonal(&right).map_err(FusionError::from)?,
    ))
}

/// Exact positive diagonal metrics on the two association-tree coordinate
/// bases, in the same channel order as FSymbols. They make the Racah F-block
/// an isometry: `F^dag G_left F = G_right`, without adjoining square roots.
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

/// Construct the actual F/R data for SU(2)_k, for `1 <= k <= MAX_LEVEL`.
/// `K` must contain the primitive `8(k+2)`-th roots of unity. Its F-symbols
/// use the algebraic gauge above; a physical orthonormal basis requires a
/// compatible metric or a further square-root field extension.
pub fn su2_level<K: FusionScalar>(level: usize) -> Result<RibbonFusionCategory<K>, FusionError> {
    checked_level(level)?;
    let root_order = (8 * (level + 2)) as u32;
    // A field refusal precedes any table allocation or partial symbol carrier.
    let braiding_root = root_of_unity::<K>(root_order, 1)?;
    let ring = FusionRing::su2_level(level)?;
    let (dimensions, factorials) = coefficient_data::<K>(level)?;
    let f = FSymbols::try_from_fn(&ring, |labels, e, f| {
        associator(level, labels, e, f, &dimensions, &factorials)
    })?;
    let category = FusionCategory::new(ring.clone(), f)?;
    for (labels, block) in category.f_symbols().blocks() {
        let (left, right) = tree_metrics(&ring, *labels, &dimensions, &factorials)?;
        let f = block.matrix();
        let weighted = matrix::multiply(
            &involution::adjoint(f).map_err(FusionError::from)?,
            &matrix::multiply(&left, f).map_err(FusionError::from)?,
        )
        .map_err(FusionError::from)?;
        if weighted != right {
            return Err(FusionError::Inconsistent {
                context: "q-Racah weighted unitarity",
            });
        }
    }
    let mut coefficient_error = None;
    let r = RSymbols::from_fn(&ring, |[a, b, c]| {
        let exponent = (c * (c + 2)) as i64 - (a * (a + 2)) as i64 - (b * (b + 2)) as i64;
        match omega_number_theory::scalar::power(&braiding_root, exponent)
            .map_err(FusionError::from)
        {
            Ok(value) => {
                if (a + b - c) / 2 % 2 == 0 {
                    value
                } else {
                    value.neg()
                }
            }
            Err(error) => {
                coefficient_error = Some(error);
                K::zero()
            }
        }
    })?;
    if let Some(error) = coefficient_error {
        return Err(error);
    }
    RibbonFusionCategory::try_new(BraidedFusionCategory::new(category, r)?, dimensions)
}

#[cfg(test)]
mod tests {
    use super::*;
    use crate::braided::HexagonForm;
    use crate::modular::ModularData;
    use omega_number_theory::cyclotomic_field::Cyclotomic;

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
        // This includes an independently computed Verlinde replay, S^2 and
        // (ST)^3, rather than relying on a family-name assertion.
        let modular = ModularData::verified(&model).unwrap();
        assert_eq!(
            modular.central_charge_mod_4().unwrap(),
            omega_number_theory::rational::rq((3 * k) as i64, (k + 2) as i64)
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
