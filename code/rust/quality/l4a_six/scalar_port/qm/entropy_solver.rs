use num_bigint::BigInt;
use num_rational::BigRational;
use num_traits::Zero;
use serde::{Deserialize, Serialize};
use std::collections::BTreeMap;

pub type Rational = BigRational;

pub fn r_int(n: i64) -> Rational {
    Rational::from_integer(BigInt::from(n))
}

pub fn r_frac(n: i64, d: i64) -> Rational {
    if d == 0 {
        panic!("Denominator cannot be zero in exact rational construction");
    }
    Rational::new(BigInt::from(n), BigInt::from(d))
}

pub fn parse_exact_rational(s: &str) -> Result<Rational, String> {
    let s = s.trim();
    if s.contains('.') || s.contains('e') || s.contains('E') {
        return Err(format!(
            "Floating-point representations forbidden in exact arithmetic: '{}'",
            s
        ));
    }
    if let Some((n_str, d_str)) = s.split_once('/') {
        let n = n_str
            .trim()
            .parse::<BigInt>()
            .map_err(|e| format!("Invalid numerator: {}", e))?;
        let d = d_str
            .trim()
            .parse::<BigInt>()
            .map_err(|e| format!("Invalid denominator: {}", e))?;
        if d.is_zero() {
            return Err("Denominator cannot be zero".to_string());
        }
        Ok(Rational::new(n, d))
    } else {
        let n = s
            .parse::<BigInt>()
            .map_err(|e| format!("Invalid integer: {}", e))?;
        Ok(Rational::from_integer(n))
    }
}

pub fn format_rational(r: &Rational) -> String {
    format!("{}/{}", r.numer(), r.denom())
}

fn canonical_evidence_json(
    eigenvalues: &[String],
    multiplicities: &[usize],
    prime_basis: &[u64],
    exponent_matrix: &[Vec<i64>],
    reduced_coefficients: &[String],
    verdict: &str,
    is_pure: bool,
) -> String {
    if is_pure {
        format!(
            "{{\"eigenvalues\": [{}], \"multiplicities\": [{}], \"prime_basis\": [], \"reduced_coefficients\": [], \"verdict\": \"{}\"}}",
            eigenvalues
                .iter()
                .map(|s| format!("\"{}\"", s))
                .collect::<Vec<_>>()
                .join(", "),
            multiplicities
                .iter()
                .map(|m| m.to_string())
                .collect::<Vec<_>>()
                .join(", "),
            verdict
        )
    } else {
        let exp_str = exponent_matrix
            .iter()
            .map(|row| {
                format!(
                    "[{}]",
                    row.iter()
                        .map(|x| x.to_string())
                        .collect::<Vec<_>>()
                        .join(", ")
                )
            })
            .collect::<Vec<_>>()
            .join(", ");
        format!(
            "{{\"eigenvalues\": [{}], \"exponent_matrix\": [{}], \"multiplicities\": [{}], \"prime_basis\": [{}], \"reduced_coefficients\": [{}], \"verdict\": \"{}\"}}",
            eigenvalues
                .iter()
                .map(|s| format!("\"{}\"", s))
                .collect::<Vec<_>>()
                .join(", "),
            exp_str,
            multiplicities
                .iter()
                .map(|m| m.to_string())
                .collect::<Vec<_>>()
                .join(", "),
            prime_basis
                .iter()
                .map(|p| p.to_string())
                .collect::<Vec<_>>()
                .join(", "),
            reduced_coefficients
                .iter()
                .map(|s| format!("\"{}\"", s))
                .collect::<Vec<_>>()
                .join(", "),
            verdict
        )
    }
}

#[derive(Clone, Debug, PartialEq, Eq, Serialize, Deserialize)]
pub struct MultiplicativeReductionResult {
    pub authority_effect: String,
    pub eigenvalues: Vec<String>,
    pub multiplicities: Vec<usize>,
    pub prime_basis: Vec<u64>,
    pub exponent_matrix: Vec<Vec<i64>>,
    pub reduced_coefficients: Vec<String>,
    pub is_pure: bool,
    pub linear_form_nonvanishing: bool,
    pub entropy_value_exact: Option<String>,
    pub verdict: String,
    pub anchor_citation: String,
    pub evidence_sha256: String,
}

pub fn reduce_multiplicative_dependence(
    eigenvalues: &[Rational],
    multiplicities: Option<&[usize]>,
) -> Result<MultiplicativeReductionResult, String> {
    use omega_number_theory::integer_factorization::FactorizationBudget;
    use omega_quantum_physics::exact_entropy::RationalSpectrum;
    let mults = multiplicities
        .map(<[usize]>::to_vec)
        .unwrap_or_else(|| vec![1; eigenvalues.len()]);
    if mults.len() != eigenvalues.len() {
        return Err("SPECTRUM_MULTIPLICITY_LENGTH_MISMATCH".into());
    }
    let spectrum = RationalSpectrum::try_new(
        eigenvalues
            .iter()
            .cloned()
            .zip(mults.iter().copied())
            .collect(),
    )
    .map_err(|error| error.to_string())?;
    let reduction = spectrum
        .log_reduction(FactorizationBudget {
            max_operations: 1_000_000,
        })
        .map_err(|error| error.to_string())?;
    let evals_str = eigenvalues.iter().map(format_rational).collect::<Vec<_>>();
    let is_pure = spectrum.is_pure();
    let prime_basis = reduction.primes;
    let exponent_matrix = if is_pure {
        Vec::new()
    } else {
        reduction.exponents
    };
    let reduced_coeffs_str = reduction
        .gamma
        .iter()
        .map(format_rational)
        .collect::<Vec<_>>();
    let verdict = if is_pure {
        "ZERO_ENTROPY_PURE"
    } else {
        "TRANSCENDENTAL_BY_BAKER"
    };
    let payload = canonical_evidence_json(
        &evals_str,
        &mults,
        &prime_basis,
        &exponent_matrix,
        &reduced_coeffs_str,
        verdict,
        is_pure,
    );
    let evidence_sha =
        omega_kernel::digest::Digest::of_bytes(payload.as_bytes()).as_str()[7..].to_owned();
    let anchor = if is_pure {
        "Pure State Trivial (0 log 0 = 0, 1 log 1 = 0)"
    } else if prime_basis.len() == 1 {
        "Anchor A2 (Lindemann-Weierstrass)"
    } else {
        "Anchor A1 (Baker 1975), Ch. 1-3"
    };
    Ok(MultiplicativeReductionResult {
        authority_effect: "None".into(),
        eigenvalues: evals_str,
        multiplicities: mults,
        prime_basis,
        exponent_matrix,
        reduced_coefficients: reduced_coeffs_str,
        is_pure,
        linear_form_nonvanishing: !is_pure,
        entropy_value_exact: is_pure.then(|| "0/1".into()),
        verdict: verdict.into(),
        anchor_citation: anchor.into(),
        evidence_sha256: evidence_sha,
    })
}

pub fn exact_power_trace(
    eigenvalues: &[Rational],
    multiplicities: Option<&[usize]>,
    order: usize,
) -> Result<Rational, String> {
    let mults = multiplicities
        .map(<[usize]>::to_vec)
        .unwrap_or_else(|| vec![1; eigenvalues.len()]);
    if mults.len() != eigenvalues.len() {
        return Err("SPECTRUM_MULTIPLICITY_LENGTH_MISMATCH".into());
    }
    omega_quantum_physics::exact_entropy::RationalSpectrum::try_new(
        eigenvalues.iter().cloned().zip(mults).collect(),
    )
    .and_then(|spectrum| spectrum.power_trace(order, 4096))
    .map_err(|error| error.to_string())
}

pub fn rational_log_bounds(p: u64, precision_bits: usize) -> Result<(Rational, Rational), String> {
    if p <= 1 {
        return Err("LOG_ARGUMENT_MUST_BE_AT_LEAST_TWO".into());
    }
    let bits = u32::try_from(precision_bits).map_err(|_| "LOG_PRECISION_BUDGET")?;
    if bits == 0 {
        return Err("POSITIVE_LOG_PRECISION_REQUIRED".into());
    }
    let interval =
        omega_kernel::elementary::ln_enclosure(&Rational::from_integer(BigInt::from(p)), bits)
            .map_err(|error| error.to_string())?;
    Ok((interval.lo().clone(), interval.hi().clone()))
}

pub fn approximate_entropy_rational_bounds(
    reduction: &MultiplicativeReductionResult,
    precision_bits: usize,
) -> Result<(Rational, Rational), String> {
    let eigenvalues = reduction
        .eigenvalues
        .iter()
        .map(|q| parse_exact_rational(q))
        .collect::<Result<Vec<_>, _>>()?;
    let expected = reduce_multiplicative_dependence(&eigenvalues, Some(&reduction.multiplicities))?;
    if *reduction != expected {
        return Err("ENTROPY_REDUCTION_REPLAY_MISMATCH".into());
    }
    let bits = u32::try_from(precision_bits).map_err(|_| "ENTROPY_PRECISION_BUDGET")?;
    let spectrum = omega_quantum_physics::exact_entropy::RationalSpectrum::try_new(
        eigenvalues
            .into_iter()
            .zip(reduction.multiplicities.iter().copied())
            .collect(),
    )
    .map_err(|error| error.to_string())?;
    let interval = spectrum
        .log_reduction(
            omega_number_theory::integer_factorization::FactorizationBudget {
                max_operations: 1_000_000,
            },
        )
        .and_then(|form| form.enclosure(bits))
        .map_err(|error| error.to_string())?;
    Ok((interval.lo().clone(), interval.hi().clone()))
}

pub fn verify_negative_control_vanishing_linear_form() -> BTreeMap<String, serde_json::Value> {
    let args = vec![r_int(2), r_int(3), r_int(6)];
    let coeffs = vec![r_int(1), r_int(1), r_int(-1)];

    use omega_number_theory::integer_factorization::{
        factor_positive_rational, FactorizationBudget,
    };
    let factors = args
        .iter()
        .map(|q| {
            factor_positive_rational(
                q,
                FactorizationBudget {
                    max_operations: 1_000_000,
                },
            )
            .expect("fixed small rational factors")
        })
        .collect::<Vec<_>>();
    let gamma_2 = args
        .iter()
        .enumerate()
        .map(|(i, _)| &coeffs[i] * r_int(factors[i].get(&2u32.into()).copied().unwrap_or(0)))
        .sum::<Rational>();
    let gamma_3 = args
        .iter()
        .enumerate()
        .map(|(i, _)| &coeffs[i] * r_int(factors[i].get(&3u32.into()).copied().unwrap_or(0)))
        .sum::<Rational>();
    let is_vanishing = gamma_2.is_zero() && gamma_3.is_zero();

    let mut map = BTreeMap::new();
    map.insert("authority_effect".to_string(), serde_json::json!("None"));
    map.insert(
        "control_id".to_string(),
        serde_json::json!("T560_NEGATIVE_CONTROL_VANISHING_FORM"),
    );
    map.insert(
        "form_vanishes_identically".to_string(),
        serde_json::json!(is_vanishing),
    );
    map.insert(
        "reduced_coefficients".to_string(),
        serde_json::json!([format_rational(&gamma_2), format_rational(&gamma_3)]),
    );
    map.insert(
        "multiplicatively_dependent".to_string(),
        serde_json::json!(is_vanishing),
    );
    map
}

pub fn verify_negative_control_renyi_vs_von_neumann(
    eigenvalues: &[Rational],
    multiplicities: Option<&[usize]>,
) -> Result<BTreeMap<String, serde_json::Value>, String> {
    let p2 = exact_power_trace(eigenvalues, multiplicities, 2)?;
    let reduction = reduce_multiplicative_dependence(eigenvalues, multiplicities)?;

    let mut map = BTreeMap::new();
    map.insert("authority_effect".to_string(), serde_json::json!("None"));
    map.insert(
        "control_id".to_string(),
        serde_json::json!("T560_NEGATIVE_CONTROL_RENYI_VS_ENTROPY"),
    );
    map.insert(
        "renyi_2_power_trace".to_string(),
        serde_json::json!(format_rational(&p2)),
    );
    map.insert(
        "renyi_2_status".to_string(),
        serde_json::json!("EXACT_RATIONAL_CARRIER_INTERNAL"),
    );
    map.insert(
        "entropy_status".to_string(),
        serde_json::json!(reduction.verdict),
    );
    Ok(map)
}

#[derive(Clone, Debug, PartialEq, Eq, Serialize, Deserialize)]
pub struct SystemParityRecord {
    pub system_id: String,
    pub name: String,
    pub dimension: usize,
    pub conductor: u64,
    pub carrier: String,
    pub is_pure: bool,
    pub distinct_nonzero_eigenvalues: Vec<String>,
    pub purity_p2: String,
    pub prime_basis: Vec<u64>,
    pub reduced_coefficients: Vec<String>,
    pub entropy_value_exact: Option<String>,
    pub verdict: String,
    pub evidence_sha256: String,
    pub byte_parity_match: bool,
}

#[derive(Clone, Debug, PartialEq, Eq, Serialize, Deserialize)]
pub struct ParityReceipt {
    pub authority_effect: String,
    pub citation: String,
    pub campaign: String,
    pub block: u32,
    pub target: String,
    pub receipt_class: String,
    pub total_systems_verified: usize,
    pub all_byte_deterministic: bool,
    pub systems: BTreeMap<String, SystemParityRecord>,
    pub receipt_sha256: String,
}

pub fn get_fqmi1_system_spectrum(
    system_id: &str,
) -> Result<
    (
        Vec<Rational>,
        Option<Vec<usize>>,
        usize,
        u64,
        String,
        String,
    ),
    String,
> {
    match system_id {
        "S1" => Ok((
            vec![r_frac(3, 4), r_frac(1, 4)],
            None,
            2,
            4,
            "Q(i)".to_string(),
            "qubit at conductor 4".to_string(),
        )),
        "S2" => Ok((
            vec![r_frac(1, 3), r_frac(1, 3), r_frac(1, 3)],
            None,
            3,
            3,
            "Q(zeta_3)".to_string(),
            "qutrit at conductor 3".to_string(),
        )),
        "S3" => Ok((
            vec![r_frac(3, 4), r_frac(1, 4)],
            None,
            2,
            8,
            "Q(zeta_8)".to_string(),
            "qubit at conductor 8".to_string(),
        )),
        "S4" => Ok((
            vec![r_int(1), r_int(0), r_int(0), r_int(0)],
            None,
            4,
            8,
            "Q(zeta_8)".to_string(),
            "two qubits at conductor 8".to_string(),
        )),
        "S5" => Ok((
            vec![r_frac(1, 5); 5],
            None,
            5,
            5,
            "Q(zeta_5)".to_string(),
            "qudit at conductor 5".to_string(),
        )),
        "S6" => Ok((
            vec![r_frac(8, 15), r_frac(4, 15), r_frac(2, 15), r_frac(1, 15)],
            None,
            4,
            1,
            "Q".to_string(),
            "commensurable ladder at conductor 1".to_string(),
        )),
        "S7" => Ok((
            vec![r_frac(4, 7), r_frac(2, 7), r_frac(1, 7)],
            None,
            3,
            1,
            "Q".to_string(),
            "non-commensurable ladder at conductor 1".to_string(),
        )),
        "S8" => Ok((
            vec![r_frac(1, 2), r_frac(1, 2), r_int(0), r_int(0)],
            None,
            4,
            4,
            "Q(i)".to_string(),
            "[[4,2,2]] code space at conductor 4".to_string(),
        )),
        _ => Err(format!("Unknown system ID: {}", system_id)),
    }
}

pub fn evaluate_fqmi1_system(system_id: &str) -> Result<SystemParityRecord, String> {
    let (evals, mults, dim, cond, carrier, name) = get_fqmi1_system_spectrum(system_id)?;
    let p2 = exact_power_trace(&evals, mults.as_deref(), 2)?;
    let reduction = reduce_multiplicative_dependence(&evals, mults.as_deref())?;

    let distinct_nonzero: std::collections::BTreeSet<Rational> =
        evals.iter().filter(|q| !q.is_zero()).cloned().collect();
    let distinct_nonzero_str: Vec<String> = distinct_nonzero
        .into_iter()
        .map(|r| format_rational(&r))
        .collect();

    let mut record = SystemParityRecord {
        system_id: system_id.to_string(),
        name,
        dimension: dim,
        conductor: cond,
        carrier,
        is_pure: reduction.is_pure,
        distinct_nonzero_eigenvalues: distinct_nonzero_str,
        purity_p2: format_rational(&p2),
        prime_basis: reduction.prime_basis,
        reduced_coefficients: reduction.reduced_coefficients,
        entropy_value_exact: reduction.entropy_value_exact,
        verdict: reduction.verdict,
        evidence_sha256: reduction.evidence_sha256,
        byte_parity_match: false,
    };
    let reference: ParityReceipt =
        serde_json::from_str(include_str!("data/c750_b01_parity_receipt.json"))
            .map_err(|error| format!("INVALID_PARITY_REFERENCE:{error}"))?;
    record.byte_parity_match = reference
        .systems
        .get(system_id)
        .is_some_and(|pinned| parity_against_reference(&record, pinned));
    Ok(record)
}

pub fn parity_against_reference(
    computed: &SystemParityRecord,
    reference: &SystemParityRecord,
) -> bool {
    let mut actual = computed.clone();
    let mut expected = reference.clone();
    actual.byte_parity_match = false;
    expected.byte_parity_match = false;
    actual == expected
}

pub fn generate_c750_b01_parity_receipt() -> Result<ParityReceipt, String> {
    let mut systems = BTreeMap::new();
    for id in &["S1", "S2", "S3", "S4", "S5", "S6", "S7", "S8"] {
        let record = evaluate_fqmi1_system(id)?;
        systems.insert(id.to_string(), record);
    }

    let systems_json =
        serde_json::to_string(&systems).map_err(|e| format!("Serialization error: {}", e))?;
    let receipt_sha =
        omega_kernel::digest::Digest::of_bytes(systems_json.as_bytes()).as_str()[7..].to_owned();
    let replay = (1..=8)
        .map(|index| {
            let id = format!("S{index}");
            evaluate_fqmi1_system(&id).map(|record| (id, record))
        })
        .collect::<Result<BTreeMap<_, _>, _>>()?;
    let replay_json = serde_json::to_string(&replay).map_err(|error| error.to_string())?;
    let byte_deterministic = systems_json.as_bytes() == replay_json.as_bytes();
    let verified_count = systems
        .values()
        .filter(|record| record.byte_parity_match)
        .count();

    Ok(ParityReceipt {
        authority_effect: "None".to_string(),
        citation: "sealed-derivation-v1 (3100c4e)".to_string(),
        campaign: "C750".to_string(),
        block: 1,
        target: "C750-T566".to_string(),
        receipt_class: "FQMI-1-CLASS-V1".to_string(),
        total_systems_verified: verified_count,
        all_byte_deterministic: byte_deterministic,
        systems,
        receipt_sha256: receipt_sha,
    })
}

#[cfg(test)]
mod tests {
    use super::*;
    use crate::linear_algebra::image_kernel::{solve_in_image, ExactRowReduction, ImageMembership};
    use crate::linear_algebra::matrix as mx;

    #[test]
    fn test_exact_rref_and_solve() {
        let mat = mx::from_rows(vec![
            vec![r_int(1), r_int(2), r_int(3)],
            vec![r_int(4), r_int(5), r_int(6)],
            vec![r_int(7), r_int(8), r_int(9)],
        ])
        .unwrap();
        let reduction = mat.rank_and_rref().unwrap();
        assert_eq!(reduction.pivot_columns(), &[0, 1]);
        assert_eq!(reduction.rank(), 2);

        let nulls = mat.kernel_basis().unwrap();
        assert_eq!(nulls.vectors().len(), 1);
        let prod = mx::multiply_vector(&mat, &nulls.vectors()[0]).unwrap();
        assert!(prod.iter().all(|x| x.is_zero()));

        let rhs = vec![r_int(3), r_int(9), r_int(15)];
        let ImageMembership::InImage(solution) = solve_in_image(&mat, &rhs).unwrap() else {
            panic!("System is consistent");
        };
        let check = mx::multiply_vector(&mat, &solution.potential).unwrap();
        assert_eq!(check, rhs);
    }

    #[test]
    fn test_pure_state_reduction_with_zero_eigenvalues() {
        let evals = vec![r_int(1), r_int(0), r_int(0)];
        let res = reduce_multiplicative_dependence(&evals, None).unwrap();
        assert!(res.is_pure);
        assert_eq!(res.verdict, "ZERO_ENTROPY_PURE");
        assert_eq!(res.entropy_value_exact, Some("0/1".to_string()));
        assert!(res.prime_basis.is_empty());
        assert!(res.reduced_coefficients.is_empty());
    }

    #[test]
    fn test_s6_ladder_reduction_parity() {
        let evals = vec![r_frac(8, 15), r_frac(4, 15), r_frac(2, 15), r_frac(1, 15)];
        let res = reduce_multiplicative_dependence(&evals, None).unwrap();
        assert!(!res.is_pure);
        assert_eq!(res.verdict, "TRANSCENDENTAL_BY_BAKER");
        assert_eq!(res.prime_basis, vec![2, 3, 5]);
        assert_eq!(res.reduced_coefficients, vec!["-34/15", "1/1", "1/1"]);
        assert_eq!(
            res.evidence_sha256,
            "11e1159c05e8ea711deab83652d7dd42be98fa00806122218da87013926a11b5"
        );
    }

    #[test]
    fn test_all_eight_systems_evidence_sha256_parity() {
        let expected_hashes = [
            (
                "S1",
                "1fd92aca24fa9a3398f396c401d428c78c30e1b437fd4a766987281441eb1cf4",
            ),
            (
                "S2",
                "a670504f9047db3ef5530cadb3a1aa443f34a430c056d6a45513a3985d95af41",
            ),
            (
                "S3",
                "1fd92aca24fa9a3398f396c401d428c78c30e1b437fd4a766987281441eb1cf4",
            ),
            (
                "S4",
                "414ef45d8ce3923fdefc1dc8966864ec4dd631037f481e7a46e9701ba65ccb96",
            ),
            (
                "S5",
                "7641443bda07d1a327968ed25d174b38ef41c211b1e936192f8f32ecb4f62c58",
            ),
            (
                "S6",
                "11e1159c05e8ea711deab83652d7dd42be98fa00806122218da87013926a11b5",
            ),
            (
                "S7",
                "c6773ecec368f818045c9b599c815e591e6e9c4bee0a0ee0e1be031cb8112d5c",
            ),
            (
                "S8",
                "6824aa3db6ac9350012fe4f03ca958f17f7eb1919b4076010b9215d3ee31d7fd",
            ),
        ];

        for (id, expected_sha) in expected_hashes {
            let rec = evaluate_fqmi1_system(id).unwrap();
            assert_eq!(rec.evidence_sha256, expected_sha, "Mismatch on {}", id);
        }
    }
}
