//! CPTP Channel Class, Choi's Theorem, Stinespring Dilation, and Conductor Escalation.
//!
//! Campaign C250 Block 06 (Global Steps 176-200).
//! AuthorityEffect: None. Citation: sealed-derivation-v1 (3100c4e).
//!
//! The dilation conductor of a census channel is computed, not declared. From
//! the channel's exact Choi matrix `J` over `Q(i)`, an exact `LDL*`
//! decomposition gives `J = sum_k d_k l_k l_k*` with rational `d_k >= 0` and
//! `l_k` over the field of `J`'s entries: a weighted Kraus family over that
//! field. Each weight `a/b` is `(ab)/b^2`, and `ab` is a sum of four squares
//! (Lagrange), so the family splits into unit-weight Kraus operators
//! `(s/b) K` over the same field, whose Stinespring isometry therefore has its
//! entries there too. The dilation conductor is the least `n` with those
//! entries in `Q(zeta_n)`: `1` for `Q`, `4` for `Q(i)`. So no dilation needs a
//! field beyond the Choi matrix's; in particular none needs `sqrt(3)` or
//! `sqrt(7)`, which the census used to report as conductors 12 and 28.
//! The canonical number-theory quadratic conductor records the conductor of
//! `Q(sqrt(d))`, which is what a unit-weight Kraus family with irrational
//! coefficients would need.

use crate::linear_algebra::basic_matrix::BasicMatrix;
use num_traits::Zero;
use serde::{Deserialize, Serialize};

use crate::linear_algebra::{elimination, matrix as mx, ExactFieldError};
use omega_number_theory::cyclotomic::GaussianRat;
use omega_number_theory::rational::{ri, rq, Rational};
use omega_quantum_physics::exact_channel::{ExactChannelError, ExactChoiMatrix, ExactKrausChannel};
use omega_quantum_physics::exact_hermitian::{self};

/// Refusals of the channel census.
#[derive(Debug, Clone, PartialEq, Eq, thiserror::Error)]
pub enum CensusError {
    #[error("channel: {0}")]
    Channel(#[from] ExactChannelError),
    #[error("algebra: {0}")]
    Algebra(#[from] ExactFieldError),
    #[error("invalid probability or multiplicity overflow")]
    Probability,
    #[error("the Choi matrix is not positive semidefinite at pivot {pivot}")]
    NotPositiveSemidefinite { pivot: usize },
    #[error("the weight {0} is too large to split into squares")]
    WeightTooLarge(Rational),
    #[error("the unit-weight family does not reproduce the channel")]
    SplitChangedTheChannel,
}

/// Record for a censused open-system channel in the 22 foundational targets.
#[derive(Debug, Clone, Serialize, Deserialize, PartialEq, Eq)]
pub struct ChannelCensusItem {
    pub channel_id: String,
    pub name: String,
    pub targets: Vec<usize>,
    pub dimension: usize,
    /// The rank of the Choi matrix, computed exactly.
    pub kraus_rank: usize,
    /// The least conductor carrying the entries of the declared Kraus family.
    pub declared_kraus_conductor: usize,
    /// The least conductor carrying the entries of the Choi matrix.
    pub choi_conductor: usize,
    /// The least conductor carrying the entries of the computed Stinespring isometry.
    pub dilation_conductor: usize,
    pub escalates_beyond_120: bool,
}

/// Verification report for Block 06 execution.
#[derive(Debug, Clone, Serialize, Deserialize, PartialEq, Eq)]
pub struct Block06Report {
    pub authority_effect: String,
    pub citation: String,
    pub block_id: String,
    pub choi_theorem_ported_lean: bool,
    pub stinespring_requires_extension: Option<bool>,
    pub depolarizing_p_1_3_dilation_conductor: usize,
    pub depolarizing_p_1_7_dilation_conductor: usize,
    pub kraus_rank_bound_d2: usize,
    pub channels_censused: usize,
    pub channels_escalating_beyond_120: usize,
    pub channel_census: Vec<ChannelCensusItem>,
}

/// The least conductor `n` with every entry in `Q(zeta_n)`, for entries in `Q(i)`:
/// `1` when all are rational, `4` otherwise.
pub fn gaussian_conductor(entries: &[GaussianRat]) -> usize {
    if entries.iter().all(|z| z.im.is_zero()) {
        1
    } else {
        4
    }
}

/// `J = sum_k d_k l_k l_k*` for a Hermitian PSD `J` over `Q(i)`: an exact
/// `LDL*` with zero pivots skipped (their columns must vanish), returned as
/// the weighted Kraus family `(d_k, K_k)` with `K_k[r][i] = l_k[i d_out + r]`.
pub fn kraus_from_choi(
    choi: &ExactChoiMatrix,
) -> Result<Vec<(Rational, BasicMatrix<GaussianRat>)>, CensusError> {
    let channel = choi.weighted_kraus()?;
    Ok(channel
        .weights()
        .iter()
        .cloned()
        .zip(channel.operators().iter().cloned())
        .collect())
}

/// The unit-weight Kraus family of a weighted one: `(a/b) K rho K*` becomes the
/// terms `(s/b) K` for the four squares `s^2` summing to `ab`.
pub fn unit_weight_family(
    terms: &[(Rational, BasicMatrix<GaussianRat>)],
) -> Result<Vec<BasicMatrix<GaussianRat>>, CensusError> {
    let mut out = Vec::new();
    for (weight, op) in terms {
        let split = omega_number_theory::four_squares::rational_square_split(weight, 1_000_000)
            .map_err(|_| CensusError::WeightTooLarge(weight.clone()))?;
        for q in split {
            out.push(mx::scale(op, &GaussianRat::from_rational(q))?);
        }
    }
    Ok(out)
}

/// One census channel: its declared weighted Kraus family and what is computed from it.
fn census_item(
    channel_id: &str,
    name: &str,
    targets: Vec<usize>,
    channel: ExactKrausChannel,
) -> Result<ChannelCensusItem, CensusError> {
    let choi = channel.choi()?;
    let family = unit_weight_family(&kraus_from_choi(&choi)?)?;
    let unit = ExactKrausChannel::try_new(channel.dim_in(), channel.dim_out(), family, "unit")?;
    if unit.choi()?.matrix() != choi.matrix() {
        return Err(CensusError::SplitChangedTheChannel);
    }
    let isometry = unit.stinespring_isometry()?;
    let declared: Vec<GaussianRat> = channel
        .operators()
        .iter()
        .flat_map(|k| k.as_slice().iter().cloned())
        .collect();
    let dilation_conductor = gaussian_conductor(isometry.as_slice());
    Ok(ChannelCensusItem {
        channel_id: channel_id.to_string(),
        name: name.to_string(),
        targets,
        dimension: channel.dim_in(),
        kraus_rank: elimination::rank(choi.matrix())?,
        declared_kraus_conductor: gaussian_conductor(&declared),
        choi_conductor: gaussian_conductor(choi.matrix().as_slice()),
        dilation_conductor,
        escalates_beyond_120: 120 % dilation_conductor != 0,
    })
}

fn qubit(entries: [(i64, i64); 4]) -> BasicMatrix<GaussianRat> {
    BasicMatrix::<GaussianRat>::from_row_major(
        2,
        2,
        entries
            .iter()
            .map(|&(re, im)| GaussianRat::from_ints(re, im))
            .collect(),
    )
    .expect("fixed four-entry Pauli fixture")
}

/// Operational census of open-system quantum channels across the 22 corpus
/// targets, each declared by its weighted Kraus family; ranks and conductors
/// are computed.
pub fn evaluate_channel_census() -> Result<Vec<ChannelCensusItem>, CensusError> {
    let identity = mx::identity(2)?;
    let x = qubit([(0, 0), (1, 0), (1, 0), (0, 0)]);
    let y = qubit([(0, 0), (0, -1), (0, 1), (0, 0)]);
    let z = qubit([(1, 0), (0, 0), (0, 0), (-1, 0)]);
    let flip = |p: Rational, pauli: &BasicMatrix<GaussianRat>, name: &str| {
        ExactKrausChannel::try_weighted(
            2,
            2,
            vec![(ri(1) - &p, identity.clone()), (p, pauli.clone())],
            name,
        )
    };
    let projector = |q: usize| {
        let mut m = mx::zeros(2, 2).expect("fixed qubit fixture");
        m.set(q, q, GaussianRat::one()).expect("qubit basis index");
        m
    };
    let zz = mx::kronecker_with_limits(&z, &z, exact_hermitian::exact_limits())?;
    let half = rq(1, 2);
    let syndrome = [
        mx::scale(
            &mx::add(&mx::identity(4)?, &zz)?,
            &GaussianRat::from_rational(half.clone()),
        )?,
        mx::scale(
            &mx::sub(&mx::identity(4)?, &zz)?,
            &GaussianRat::from_rational(half),
        )?,
    ];
    Ok(vec![
        census_item(
            "CH-01",
            "Identity / Ideal Coherent Channel",
            vec![1, 2, 3, 4, 5, 6, 7, 8],
            ExactKrausChannel::identity(2, "identity")?,
        )?,
        census_item(
            "CH-02",
            "Bit-Flip Channel (p = 1/3)",
            vec![9],
            flip(rq(1, 3), &x, "bit flip")?,
        )?,
        census_item(
            "CH-03",
            "Phase-Flip Channel (p = 1/4)",
            vec![12],
            flip(rq(1, 4), &z, "phase flip")?,
        )?,
        census_item(
            "CH-04",
            "Bit-Phase Flip Channel (p = 1/3)",
            vec![14],
            flip(rq(1, 3), &y, "bit-phase flip")?,
        )?,
        census_item(
            "CH-05",
            "Single-Qubit Depolarizing Channel (p = 1/3)",
            vec![20],
            ExactKrausChannel::depolarizing_qubit(rq(1, 3), "depolarizing")?,
        )?,
        census_item(
            "CH-06",
            "Single-Qubit Depolarizing Channel (p = 1/7)",
            vec![20],
            ExactKrausChannel::depolarizing_qubit(rq(1, 7), "depolarizing")?,
        )?,
        census_item(
            "CH-07",
            "Single-Qubit Projective Measurement Channel",
            vec![10, 11],
            ExactKrausChannel::try_new(2, 2, vec![projector(0), projector(1)], "measurement")?,
        )?,
        census_item(
            "CH-08",
            "Two-Qubit CSS Plaquette Syndrome Extraction Channel",
            vec![12, 16],
            ExactKrausChannel::try_new(4, 4, syndrome.to_vec(), "syndrome")?,
        )?,
    ])
}

/// Run full Block 06 execution battery.
///
/// `stinespring_requires_extension` is computed: whether any census channel's
/// dilation conductor exceeds its Choi matrix's.
pub fn run_block_06_execution() -> Result<Block06Report, CensusError> {
    let census = evaluate_channel_census()?;
    let conductor_of = |id: &str| {
        census
            .iter()
            .find(|c| c.channel_id == id)
            .map_or(0, |c| c.dilation_conductor)
    };
    let escalating_count = census.iter().filter(|c| c.escalates_beyond_120).count();
    let requires_extension = census
        .iter()
        .any(|c| c.dilation_conductor > c.choi_conductor);
    Ok(Block06Report {
        authority_effect: "None".to_string(),
        citation: "sealed-derivation-v1 (3100c4e)".to_string(),
        block_id: "block_06".to_string(),
        choi_theorem_ported_lean: false,
        stinespring_requires_extension: Some(requires_extension),
        depolarizing_p_1_3_dilation_conductor: conductor_of("CH-05"),
        depolarizing_p_1_7_dilation_conductor: conductor_of("CH-06"),
        kraus_rank_bound_d2: 2 * 2,
        channels_censused: census.len(),
        channels_escalating_beyond_120: escalating_count,
        channel_census: census,
    })
}

#[cfg(test)]
mod tests {
    use super::*;
    use num_bigint::BigInt;
    use omega_number_theory::cyclotomic_field::quadratic_field_conductor;
    use omega_number_theory::rational::squarefree_part;

    #[test]
    fn test_minimal_cyclotomic_conductor_for_sqrt() {
        for (d, expected) in [(1, 1), (4, 1), (2, 8), (3, 12), (5, 5), (6, 24), (7, 28)] {
            let (squarefree, _) = squarefree_part(&BigInt::from(d)).unwrap();
            assert_eq!(
                quadratic_field_conductor(&squarefree),
                BigInt::from(expected)
            );
        }
    }

    /// The census used to report conductors 12 (bit flip, depolarizing at
    /// p = 1/3) and 28 (depolarizing at p = 1/7), the conductors of sqrt(3) and
    /// sqrt(7). Computed from the Choi matrices, every dilation lives over the
    /// Choi matrix's own field, here `Q`, even where the declared Kraus family
    /// uses `Y` and so `Q(i)`.
    #[test]
    fn test_channel_census() {
        let census = evaluate_channel_census().unwrap();
        assert_eq!(census.len(), 8);
        for c in &census {
            assert_eq!(c.dilation_conductor, c.choi_conductor, "{}", c.channel_id);
            assert_eq!(c.dilation_conductor, 1, "{}", c.channel_id);
            assert!(!c.escalates_beyond_120);
        }
        let ranks: Vec<usize> = census.iter().map(|c| c.kraus_rank).collect();
        assert_eq!(ranks, vec![1, 2, 2, 2, 4, 4, 2, 2]);
        let declared: Vec<usize> = census.iter().map(|c| c.declared_kraus_conductor).collect();
        assert_eq!(declared, vec![1, 1, 1, 4, 4, 4, 1, 1]);
    }

    #[test]
    fn test_block_06_full_report() {
        let rep = run_block_06_execution().unwrap();
        assert_eq!(rep.authority_effect, "None");
        assert_eq!(rep.block_id, "block_06");
        assert!(!rep.choi_theorem_ported_lean);
        assert_eq!(rep.stinespring_requires_extension, Some(false));
        assert_eq!(rep.depolarizing_p_1_3_dilation_conductor, 1);
        assert_eq!(rep.depolarizing_p_1_7_dilation_conductor, 1);
        assert_eq!(rep.kraus_rank_bound_d2, 4);
        assert_eq!(rep.channels_censused, 8);
        assert_eq!(rep.channels_escalating_beyond_120, 0);
    }

    /// A channel whose Choi matrix has non-real entries dilates over `Q(i)`,
    /// conductor 4, and no further; the split family reproduces the channel.
    #[test]
    fn a_gaussian_choi_matrix_dilates_over_q_i() {
        let s = qubit([(1, 0), (0, 0), (0, 0), (0, 1)]);
        let item = census_item(
            "S",
            "phase gate",
            vec![],
            ExactKrausChannel::try_new(2, 2, vec![s], "S").unwrap(),
        )
        .unwrap();
        assert_eq!(
            (
                item.choi_conductor,
                item.dilation_conductor,
                item.kraus_rank
            ),
            (4, 4, 1)
        );
        // Four squares for the pivots of depolarizing at p = 1/7.
        for m in [7u64, 182, 4550, 999_983] {
            let squares =
                omega_number_theory::four_squares::four_squares(&BigInt::from(m), 1_000_000)
                    .unwrap();
            assert_eq!(
                squares.iter().map(|x| x * x).sum::<BigInt>(),
                BigInt::from(m)
            );
        }
        // A non-PSD "Choi" matrix is refused by the decomposition.
        let mut swap = mx::zeros(4, 4).unwrap();
        for (r, c) in [(0, 0), (1, 2), (2, 1), (3, 3)] {
            swap.set(r, c, GaussianRat::one()).unwrap();
        }
        assert!(ExactChoiMatrix::try_new(2, 2, swap).is_err());
    }
}

/// A rational Pauli weight a/b can use a*b repeated coefficients 1/b.
/// This construction trades extra Kraus terms for avoiding square roots.
pub fn rational_kraus_weight(
    a: usize,
    b: usize,
) -> Result<(usize, num_rational::BigRational), CensusError> {
    if b == 0 || a > b {
        return Err(CensusError::Probability);
    }
    Ok((
        a.checked_mul(b).ok_or(CensusError::Probability)?,
        num_rational::BigRational::new(1.into(), b.into()),
    ))
}

#[cfg(test)]
mod review_counterexamples {
    use super::*;
    use num_bigint::BigInt;
    use num_rational::BigRational;

    #[test]
    fn redundant_kraus_weights_avoid_square_roots() {
        for (a, b) in [(3, 4), (1, 12), (25, 28), (1, 28)] {
            let (count, c) = rational_kraus_weight(a, b).unwrap();
            assert_eq!(
                BigRational::from_integer(count.into()) * &c * &c,
                BigRational::new(a.into(), b.into())
            );
        }
    }

    #[test]
    fn zero_carriers_are_refused_and_zero_radicands_are_exact() {
        assert!(
            omega_number_theory::cyclotomic_field::sqrt_of_integer(0, &BigInt::from(1)).is_err()
        );
        assert!(
            omega_number_theory::vanishing_sums::minimal_unpairable_polygon(
                0,
                omega_number_theory::integer_factorization::FactorizationBudget::default()
            )
            .is_err()
        );
        assert!(omega_quantum_physics::growth_refinement::growth_witness(0).is_err());
        assert_eq!(
            omega_number_theory::rational::squarefree_part(&BigInt::from(0)).unwrap(),
            (BigInt::from(0), BigInt::from(1))
        );
    }
}
