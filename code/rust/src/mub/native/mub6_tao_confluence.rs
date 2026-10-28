
use crate::native::exact::mub6_quad_sdp::TAO_PHASES;
use serde::{Deserialize, Serialize};
use serde_json::{json, Value};
use sha2::{Digest, Sha256};

#[derive(Deserialize)]
#[serde(deny_unknown_fields)]
struct Pilot035Answer {
    matrix_id: String,
    scope: String,
    cross_ratio_count: usize,
    distinct_exponents_mod24: Vec<i64>,
    all_cubic: bool,
    no_minus_one: bool,
    claims: Pilot035Claims,
    explanation: String,
}

#[derive(Deserialize)]
#[serde(deny_unknown_fields)]
struct Pilot035Claims {
    all_chm: bool,
    mub6_exclusion: bool,
}

#[derive(Debug, Serialize)]
pub struct Pilot035Finding {
    pub code: String,
    pub field: String,
}

#[derive(Debug, Serialize)]
pub struct Pilot035Check {
    pub schema_version: String,
    pub candidate_sha256: String,
    pub accepted: bool,
    pub findings: Vec<Pilot035Finding>,
    pub authority_effect: String,
    pub scope: String,
}

pub fn pilot035_public_input() -> Value {
    json!({
        "version":"pilot035.finite-tao.v1",
        "matrix_id":"tao_s6_explicit_v1",
        "phase_table":TAO_PHASES,
        "scope":"explicit_phase_table_only",
        "definition":"For every pair of rows i<j and columns k<l, calculate e=8*((phase[i][k]+phase[j][l]-phase[i][l]-phase[j][k]) mod 3). The cross-ratio is exp(2*pi*i*e/24). Report the number of pairs and the sorted distinct exponents. A cubic root satisfies 3*e mod 24=0; minus one has exponent 12."
    })
}

pub fn check_pilot035_candidate(value: &Value) -> Result<Pilot035Check, String> {
    let answer: Pilot035Answer =
        serde_json::from_value(value.clone()).map_err(|e| e.to_string())?;
    if answer.explanation.trim().is_empty() || answer.explanation.chars().count() > 2000 {
        return Err("explanation must contain 1..2000 characters".into());
    }
    let report = solve_tao_confluence();
    let mut expected = report.cross_ratio_exponents_mod24.clone();
    expected.sort_unstable();
    expected.dedup();
    let mut findings = Vec::new();
    for (ok, code, field) in [
        (
            answer.matrix_id == "tao_s6_explicit_v1",
            "MATRIX_MISMATCH",
            "matrix_id",
        ),
        (
            answer.scope == "explicit_phase_table_only",
            "SCOPE_MISMATCH",
            "scope",
        ),
        (
            answer.cross_ratio_count == report.cross_ratio_exponents_mod24.len(),
            "COUNT_MISMATCH",
            "cross_ratio_count",
        ),
        (
            answer.distinct_exponents_mod24 == expected,
            "EXPONENTS_MISMATCH",
            "distinct_exponents_mod24",
        ),
        (
            answer.all_cubic == report.cross_ratios_cubic,
            "CUBIC_MISMATCH",
            "all_cubic",
        ),
        (
            answer.no_minus_one == report.no_cross_ratio_minus_one,
            "MINUS_ONE_MISMATCH",
            "no_minus_one",
        ),
        (
            !answer.claims.all_chm,
            "UNSUPPORTED_ALL_CHM_PROMOTION",
            "claims.all_chm",
        ),
        (
            !answer.claims.mub6_exclusion,
            "UNSUPPORTED_MUB6_PROMOTION",
            "claims.mub6_exclusion",
        ),
    ] {
        if !ok {
            findings.push(Pilot035Finding {
                code: code.into(),
                field: field.into(),
            });
        }
    }
    let mut ordered = value.clone();
    ordered.sort_all_objects();
    let bytes = serde_json::to_vec(&ordered).map_err(|e| e.to_string())?;
    Ok(Pilot035Check {
        schema_version: "omega.mub.pilot035-check.v1".into(),
        candidate_sha256: format!("{:x}", Sha256::digest(bytes)),
        accepted: findings.is_empty(),
        findings,
        authority_effect: "None".into(),
        scope: "explicit_phase_table_only".into(),
    })
}

#[derive(Clone, Debug, PartialEq, Eq, Serialize, Deserialize)]
pub struct TaoConfluenceReport {
    pub schema_version: String,
    pub scope: String,
    pub authority_effect: String,
    pub firewall: String,
    pub phase_table: [[i64; 6]; 6],
    pub cross_ratio_exponents_mod24: Vec<i64>,
    pub cross_ratios_cubic: bool,
    pub no_cross_ratio_minus_one: bool,
    pub karlsson_confluence_established: bool,
    pub tubular_neighborhood_excluded: bool,
    pub missing_obligations: Vec<String>,
}

fn append_row_pair_exponents(i: usize, j: usize, exponents: &mut Vec<i64>) {
    for k in 0..6 {
        for l in k + 1..6 {
            let e = TAO_PHASES[i][k] + TAO_PHASES[j][l] - TAO_PHASES[i][l] - TAO_PHASES[j][k];
            exponents.push(8 * e.rem_euclid(3));
        }
    }
}

pub fn solve_tao_confluence() -> TaoConfluenceReport {
    let mut exponents = Vec::new();
    for i in 0..6 {
        for j in i + 1..6 {
            append_row_pair_exponents(i, j, &mut exponents);
        }
    }
    let cubic = exponents.iter().all(|e| (3 * e) % 24 == 0);
    let not_minus_one = exponents.iter().all(|e| *e != 12);
    TaoConfluenceReport {
        schema_version: "omega.mub.tao-phase-diagnostic.v2".into(),
        scope: "225_cross_ratios_of_the_explicit_tao_phase_table_only".into(),
        authority_effect: "None".into(),
        firewall: "stated region only; mints no authority".into(),
        phase_table: TAO_PHASES,
        cross_ratio_exponents_mod24: exponents,
        cross_ratios_cubic: cubic,
        no_cross_ratio_minus_one: not_minus_one,
        karlsson_confluence_established: false,
        tubular_neighborhood_excluded: false,
        missing_obligations: vec![
            "a concrete family chart and any claimed confluence identification".into(),
            "a checked candidate-space cover and curvature bound".into(),
        ],
    }
}
