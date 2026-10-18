
use crate::linear_algebra::basic_matrix::BasicMatrix;
use num_traits::Zero;
use serde::{Deserialize, Serialize};

use crate::linear_algebra::{elimination, matrix as mx, ExactFieldError};
use omega_number_theory::cyclotomic::GaussianRat;
use omega_number_theory::rational::{ri, rq, Rational};
use omega_quantum_physics::exact_channel::{ExactChannelError, ExactChoiMatrix, ExactKrausChannel};
use omega_quantum_physics::exact_hermitian::{self};

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

#[derive(Debug, Clone, Serialize, Deserialize, PartialEq, Eq)]
pub struct ChannelCensusItem {
    pub channel_id: String,
    pub name: String,
    pub targets: Vec<usize>,
    pub dimension: usize,
    pub kraus_rank: usize,
    pub declared_kraus_conductor: usize,
    pub choi_conductor: usize,
    pub dilation_conductor: usize,
    pub escalates_beyond_120: bool,
}

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

pub fn gaussian_conductor(entries: &[GaussianRat]) -> usize {
    if entries.iter().all(|z| z.im.is_zero()) {
        1
    } else {
        4
    }
}

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
        for m in [7u64, 182, 4550, 999_983] {
            let squares =
                omega_number_theory::four_squares::four_squares(&BigInt::from(m), 1_000_000)
                    .unwrap();
            assert_eq!(
                squares.iter().map(|x| x * x).sum::<BigInt>(),
                BigInt::from(m)
            );
        }
        let mut swap = mx::zeros(4, 4).unwrap();
        for (r, c) in [(0, 0), (1, 2), (2, 1), (3, 3)] {
            swap.set(r, c, GaussianRat::one()).unwrap();
        }
        assert!(ExactChoiMatrix::try_new(2, 2, swap).is_err());
    }
}

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
