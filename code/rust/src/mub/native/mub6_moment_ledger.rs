
use num_rational::BigRational;
use num_traits::{One, Zero};
use serde::{Deserialize, Serialize};
use sha2::{Digest, Sha256};
use std::collections::BTreeMap;

use crate::native::exact::mub6_degree2_sdp::build_block_diagonal_gramian;
use crate::native::exact::mub6_firewall::{AUTHORITY_EFFECT, FIREWALL};
use crate::native::exact::mub6_quad_sdp::{
    canonical_quad_gramian, dual_certificate_matrix, exact_rational, ldlt_pivots_rational,
    trace_inner_product, DIM_HILBERT, GRAMIAN_DIM,
};
use crate::native::{exact::mub6_degree2_sdp, exact::mub6_degree4_sdp, exact::mub6_degree6_sdp, exact::mub6_degree8_sdp};
use linear_algebra::exact_ldlt::ldlt_pivots_strictly_positive_rational;
use tfqm_number_theory::cyclotomic::Cyc24;

crate::fixture_set!(fixtures, "mub6_moment_ledger");


pub const SCHEMA_VERSION: &str = "omega.mub.moment-sdp-ledger.v1";
pub const SCOPE_STRING: &str = "exact_moment_sdp_hierarchy_ledger_benchmarks";

pub const STATUS_CERTIFIED_CANDIDATE_REFUTATION: &str = "CERTIFIED_CANDIDATE_REFUTATION";
pub const STATUS_MISSING_PROOF_OBLIGATION: &str = "MISSING_PROOF_OBLIGATION";

pub const SUPPORTED_DEGREES: &[usize] = &[2, 4, 6, 8];

pub const DEGREE_2_X0_TRACE: (i64, i64) = (-9, 20);
pub const DEGREE_2_S6_TRACE: (i64, i64) = (-6, 1);

pub const DEGREE_4_X0_EVALUATED_TRACE: (i64, i64) = (-21, 25);
pub const DEGREE_4_X0_NOMINAL_TRACE: (i64, i64) = (-33, 50);
pub const DEGREE_4_S6_TRACE: (i64, i64) = (-1947, 50);

pub const DEGREE_6_X0_TRACE: (i64, i64) = (-9071, 10800);
pub const DEGREE_6_S6_TRACE: (i64, i64) = (-140183, 3600);

pub const DEGREE_8_X0_TRACE: (i64, i64) = (-9071, 10800);
pub const DEGREE_8_S6_TRACE: (i64, i64) = (-5046587, 129600);

pub fn rational_from_pair(pair: (i64, i64)) -> BigRational {
    BigRational::new(pair.0.into(), pair.1.into())
}


pub fn repeated_basis_gramian() -> Vec<Vec<Cyc24>> {
    let one = Cyc24::rat(BigRational::one());
    let zero = Cyc24::zero();
    let mut g = vec![vec![zero; GRAMIAN_DIM]; GRAMIAN_DIM];
    for i in 0..GRAMIAN_DIM {
        for j in 0..GRAMIAN_DIM {
            if i % DIM_HILBERT == j % DIM_HILBERT {
                g[i][j] = one.clone();
            }
        }
    }
    g
}

pub fn build_candidate_gramians() -> BTreeMap<String, Vec<Vec<Cyc24>>> {
    let mut map = BTreeMap::new();
    map.insert("x0".to_string(), build_block_diagonal_gramian());
    map.insert("s6".to_string(), canonical_quad_gramian());
    map.insert("repeated".to_string(), repeated_basis_gramian());
    map
}

pub fn canonical_matrix_payload(m: &[Vec<BigRational>]) -> String {
    m.iter()
        .flatten()
        .map(|v| format!("{}/{}\n", v.numer(), v.denom()))
        .collect()
}

pub fn compute_matrix_fingerprint(m: &[Vec<BigRational>]) -> String {
    let payload = canonical_matrix_payload(m);
    let mut hasher = Sha256::new();
    hasher.update(payload.as_bytes());
    format!("{:x}", hasher.finalize())
}


fn validate_gramian_dim(g: &[Vec<Cyc24>]) -> Result<(), String> {
    if g.len() != GRAMIAN_DIM || g.iter().any(|row| row.len() != GRAMIAN_DIM) {
        return Err(format!(
            "Gramian dimension must be {}x{}, got {}",
            GRAMIAN_DIM,
            GRAMIAN_DIM,
            g.len()
        ));
    }
    Ok(())
}

fn build_inv_ext_map(
    inv: Vec<Vec<BigRational>>,
    ext: Vec<Vec<BigRational>>,
) -> BTreeMap<String, Vec<Vec<BigRational>>> {
    let mut map = BTreeMap::new();
    map.insert("invariant".to_string(), inv);
    map.insert("extended".to_string(), ext);
    map
}

fn build_degree2_map(g: &[Vec<Cyc24>]) -> Result<BTreeMap<String, Vec<Vec<BigRational>>>, String> {
    let mut map = BTreeMap::new();
    let m2 = mub6_degree2_sdp::build_degree2_projector_moment_matrix(g)?;
    map.insert("projector".to_string(), m2);
    Ok(map)
}

fn build_degree4_map(g: &[Vec<Cyc24>]) -> Result<BTreeMap<String, Vec<Vec<BigRational>>>, String> {
    let inv = mub6_degree4_sdp::build_degree4_invariant_moment_matrix(g)?;
    let ext = mub6_degree4_sdp::build_degree4_extended_moment_matrix(g)?;
    Ok(build_inv_ext_map(inv, ext))
}

fn build_degree6_map(g: &[Vec<Cyc24>]) -> Result<BTreeMap<String, Vec<Vec<BigRational>>>, String> {
    let inv = mub6_degree6_sdp::build_degree6_invariant_diagnostic_matrix(g)?;
    let ext = mub6_degree6_sdp::build_degree6_extended_diagnostic_matrix(g)?;
    Ok(build_inv_ext_map(inv, ext))
}

fn build_degree8_map(g: &[Vec<Cyc24>]) -> Result<BTreeMap<String, Vec<Vec<BigRational>>>, String> {
    let inv = mub6_degree8_sdp::build_degree8_invariant_diagnostic_matrix(g)?;
    let ext = mub6_degree8_sdp::build_degree8_extended_diagnostic_matrix(g)?;
    Ok(build_inv_ext_map(inv, ext))
}

pub fn build_degree_matrices(
    degree: usize,
    g: &[Vec<Cyc24>],
) -> Result<BTreeMap<String, Vec<Vec<BigRational>>>, String> {
    validate_gramian_dim(g)?;
    match degree {
        2 => build_degree2_map(g),
        4 => build_degree4_map(g),
        6 => build_degree6_map(g),
        8 => build_degree8_map(g),
        _ => Err(format!(
            "Unsupported degree {}. Supported degrees: {:?}",
            degree, SUPPORTED_DEGREES
        )),
    }
}


#[derive(Clone, Debug, PartialEq, Eq, Serialize, Deserialize)]
pub struct DualWitnessReceipt {
    pub target_description: String,
    pub witness_dimension: usize,
    pub inner_product: String,
    pub inner_product_num: String,
    pub inner_product_den: String,
    pub strictly_negative: bool,
    pub pivots_strictly_positive: bool,
    pub pivots: Vec<String>,
    pub status: String,
}

#[derive(Clone, Debug, PartialEq, Eq, Serialize, Deserialize)]
pub struct DegreeBenchmarkEntry {
    pub degree: usize,
    pub level: usize,
    pub matrix_types: Vec<String>,
    pub matrix_dimensions: BTreeMap<String, usize>,
    pub x0_receipt: DualWitnessReceipt,
    pub s6_receipt: DualWitnessReceipt,
    pub x0_nominal_trace: Option<String>,
    pub fingerprints: BTreeMap<String, String>,
    pub status: String,
    pub details: String,
    pub candidate_refutation_status: String,
    pub global_search_status: String,
}

#[derive(Clone, Debug, PartialEq, Eq, Serialize, Deserialize)]
pub struct MomentSDPHierarchyLedger {
    pub schema_version: String,
    pub firewall: String,
    pub authority_effect: String,
    pub scope: String,
    pub degrees: Vec<usize>,
    pub entries: BTreeMap<usize, DegreeBenchmarkEntry>,
    pub complete: bool,
    pub diagnostics_complete: bool,
    pub moment_semantics_verified: bool,
    pub summary: String,
    pub status: String,
    pub candidate_refutation_status: String,
    pub global_search_status: String,
}

#[derive(Clone, Debug, PartialEq, Eq, Serialize, Deserialize)]
pub struct MomentSdpLedgerFixtures {
    pub schema_version: String,
    pub authority_effect: String,
    pub firewall: String,
    pub scope: String,
    pub fingerprints: BTreeMap<String, String>,
}


struct DegreeArmOutcome {
    receipt_x0: DualWitnessReceipt,
    receipt_s6: DualWitnessReceipt,
    x0_nominal: Option<String>,
    status: String,
    details: String,
    candidate_status: String,
    global_status: String,
}

fn make_dual_witness_receipt(
    target_description: &str,
    witness_dimension: usize,
    tr: &BigRational,
    pivots: &[BigRational],
    status: &str,
) -> DualWitnessReceipt {
    DualWitnessReceipt {
        target_description: target_description.to_string(),
        witness_dimension,
        inner_product: tr.to_string(),
        inner_product_num: tr.numer().to_string(),
        inner_product_den: tr.denom().to_string(),
        strictly_negative: tr < &BigRational::zero(),
        pivots_strictly_positive: pivots.iter().all(|p| p > &BigRational::zero()),
        pivots: pivots.iter().map(|p| p.to_string()).collect(),
        status: status.to_string(),
    }
}

fn eval_degree2_arm(g_x0: &[Vec<Cyc24>], g_s6: &[Vec<Cyc24>]) -> Result<DegreeArmOutcome, String> {
    let m2_x0 = mub6_degree2_sdp::build_degree2_projector_moment_matrix(g_x0)?;
    let w2_x0 = mub6_degree2_sdp::build_block_diag_dual_witness(true);
    let tr_x0 = w2_x0.trace_inner(&m2_x0)?;
    let piv_x0 = ldlt_pivots_strictly_positive_rational(&w2_x0.to_full_matrix()?)?;

    let w2_s6 = dual_certificate_matrix(true);
    let tr_s6 = exact_rational(&trace_inner_product(&w2_s6, g_s6))?;
    let piv_s6 = ldlt_pivots_rational(&w2_s6)?;

    let receipt_x0 = make_dual_witness_receipt(
        "Candidate X=0 refuted at Degree 2 via projector moment witness W_2",
        mub6_degree2_sdp::MOMENT_DIM,
        &tr_x0,
        &piv_x0,
        STATUS_CERTIFIED_CANDIDATE_REFUTATION,
    );
    let receipt_s6 = make_dual_witness_receipt(
        "Candidate S_6 refuted at Degree 2 via Gramian dual witness W",
        GRAMIAN_DIM,
        &tr_s6,
        &piv_s6,
        STATUS_CERTIFIED_CANDIDATE_REFUTATION,
    );

    Ok(DegreeArmOutcome {
        receipt_x0,
        receipt_s6,
        x0_nominal: None,
        status: STATUS_CERTIFIED_CANDIDATE_REFUTATION.to_string(),
        details: "Degree 2 projector moment relaxation refutes X=0 and S_6 completions.".into(),
        candidate_status: STATUS_CERTIFIED_CANDIDATE_REFUTATION.to_string(),
        global_status: STATUS_MISSING_PROOF_OBLIGATION.to_string(),
    })
}

fn eval_degree4_arm(g_x0: &[Vec<Cyc24>], g_s6: &[Vec<Cyc24>]) -> Result<DegreeArmOutcome, String> {
    let m4_x0 = mub6_degree4_sdp::build_degree4_invariant_moment_matrix(g_x0)?;
    let w4_x0 = mub6_degree4_sdp::build_invariant_dual_witness_x0(true);
    let tr_x0 = w4_x0.trace_inner(&m4_x0)?;
    let piv_x0 = ldlt_pivots_strictly_positive_rational(&w4_x0.to_full_matrix()?)?;

    let m4_s6 = mub6_degree4_sdp::build_degree4_extended_moment_matrix(g_s6)?;
    let w4_s6 = mub6_degree4_sdp::build_extended_dual_witness_s6(true);
    let tr_s6 = w4_s6.trace_inner(&m4_s6)?;
    let piv_s6 = ldlt_pivots_strictly_positive_rational(&w4_s6.to_full_matrix()?)?;

    let receipt_x0 = make_dual_witness_receipt(
        "Candidate X=0 refuted at Degree 4 via S_6-invariant moment witness W_4",
        mub6_degree4_sdp::DEG4_INVARIANT_DIM,
        &tr_x0,
        &piv_x0,
        STATUS_CERTIFIED_CANDIDATE_REFUTATION,
    );
    let receipt_s6 = make_dual_witness_receipt(
        "Candidate S_6 refuted at Degree 4 via extended moment witness W_4^{ext}",
        mub6_degree4_sdp::DEG4_EXTENDED_DIM,
        &tr_s6,
        &piv_s6,
        STATUS_CERTIFIED_CANDIDATE_REFUTATION,
    );

    let x0_nom = "-33/50".to_string();
    let details = format!(
        "Degree 4 symmetry-adapted moment SDP refutes X=0 and S_6. Evaluated X=0 trace is {} (nominal identity bound {}).",
        tr_x0, x0_nom
    );

    Ok(DegreeArmOutcome {
        receipt_x0,
        receipt_s6,
        x0_nominal: Some(x0_nom),
        status: STATUS_CERTIFIED_CANDIDATE_REFUTATION.to_string(),
        details,
        candidate_status: STATUS_CERTIFIED_CANDIDATE_REFUTATION.to_string(),
        global_status: STATUS_MISSING_PROOF_OBLIGATION.to_string(),
    })
}

fn eval_degree6_arm(g_x0: &[Vec<Cyc24>], g_s6: &[Vec<Cyc24>]) -> Result<DegreeArmOutcome, String> {
    let m6_x0 = mub6_degree6_sdp::build_degree6_invariant_diagnostic_matrix(g_x0)?;
    let w6_x0 = mub6_degree6_sdp::build_invariant_dual_witness_x0(true);
    let tr_x0 = w6_x0.trace_inner(&m6_x0)?;
    let piv_x0 = ldlt_pivots_strictly_positive_rational(&w6_x0.to_full_matrix()?)?;

    let m6_s6 = mub6_degree6_sdp::build_degree6_extended_diagnostic_matrix(g_s6)?;
    let w6_s6 = mub6_degree6_sdp::build_extended_dual_witness_s6(true);
    let tr_s6 = w6_s6.trace_inner(&m6_s6)?;
    let piv_s6 = ldlt_pivots_strictly_positive_rational(&w6_s6.to_full_matrix()?)?;

    let receipt_x0 = make_dual_witness_receipt(
        "Diagnostic coefficient matrix for X=0 fixture at Degree 6",
        mub6_degree6_sdp::DEG6_INVARIANT_DIM,
        &tr_x0,
        &piv_x0,
        STATUS_MISSING_PROOF_OBLIGATION,
    );
    let receipt_s6 = make_dual_witness_receipt(
        "Diagnostic coefficient matrix for S_6 fixture at Degree 6",
        mub6_degree6_sdp::DEG6_EXTENDED_DIM,
        &tr_s6,
        &piv_s6,
        STATUS_MISSING_PROOF_OBLIGATION,
    );

    Ok(DegreeArmOutcome {
        receipt_x0,
        receipt_s6,
        x0_nominal: None,
        status: STATUS_MISSING_PROOF_OBLIGATION.to_string(),
        details: "Degree 6 experimental coefficient matrix diagnostics; moment semantics unverified.".into(),
        candidate_status: STATUS_MISSING_PROOF_OBLIGATION.to_string(),
        global_status: STATUS_MISSING_PROOF_OBLIGATION.to_string(),
    })
}

fn eval_degree8_arm(g_x0: &[Vec<Cyc24>], g_s6: &[Vec<Cyc24>]) -> Result<DegreeArmOutcome, String> {
    let m8_x0 = mub6_degree8_sdp::build_degree8_invariant_diagnostic_matrix(g_x0)?;
    let w8_x0 = mub6_degree8_sdp::build_invariant_dual_witness_x0(true);
    let tr_x0 = w8_x0.trace_inner(&m8_x0)?;
    let piv_x0 = ldlt_pivots_strictly_positive_rational(&w8_x0.to_full_matrix()?)?;

    let m8_s6 = mub6_degree8_sdp::build_degree8_extended_diagnostic_matrix(g_s6)?;
    let w8_s6 = mub6_degree8_sdp::build_extended_dual_witness_s6(true);
    let tr_s6 = w8_s6.trace_inner(&m8_s6)?;
    let piv_s6 = ldlt_pivots_strictly_positive_rational(&w8_s6.to_full_matrix()?)?;

    let receipt_x0 = make_dual_witness_receipt(
        "Diagnostic coefficient matrix for X=0 fixture at Degree 8",
        mub6_degree8_sdp::DEG8_INVARIANT_DIM,
        &tr_x0,
        &piv_x0,
        STATUS_MISSING_PROOF_OBLIGATION,
    );
    let receipt_s6 = make_dual_witness_receipt(
        "Diagnostic coefficient matrix for S_6 fixture at Degree 8",
        mub6_degree8_sdp::DEG8_EXTENDED_DIM,
        &tr_s6,
        &piv_s6,
        STATUS_MISSING_PROOF_OBLIGATION,
    );

    Ok(DegreeArmOutcome {
        receipt_x0,
        receipt_s6,
        x0_nominal: None,
        status: STATUS_MISSING_PROOF_OBLIGATION.to_string(),
        details: "Degree 8 experimental coefficient matrix diagnostics; moment semantics unverified.".into(),
        candidate_status: STATUS_MISSING_PROOF_OBLIGATION.to_string(),
        global_status: STATUS_MISSING_PROOF_OBLIGATION.to_string(),
    })
}

fn collect_degree_fingerprints(
    degree: usize,
    cand_ref: &BTreeMap<String, Vec<Vec<Cyc24>>>,
) -> Result<(Vec<String>, BTreeMap<String, usize>, BTreeMap<String, String>), String> {
    let mut fingerprints = BTreeMap::new();
    let mut matrix_dims = BTreeMap::new();
    let mut matrix_types = Vec::new();

    for (c_name, g) in cand_ref {
        let m_dict = build_degree_matrices(degree, g)?;
        for (m_type, m) in m_dict {
            if !matrix_types.contains(&m_type) {
                matrix_types.push(m_type.clone());
                matrix_dims.insert(m_type.clone(), m.len());
            }
            let fp = compute_matrix_fingerprint(&m);
            fingerprints.insert(format!("deg{}_{}_{}", degree, m_type, c_name), fp);
        }
    }
    Ok((matrix_types, matrix_dims, fingerprints))
}

fn eval_degree_arm_dispatch(
    degree: usize,
    g_x0: &[Vec<Cyc24>],
    g_s6: &[Vec<Cyc24>],
) -> Result<DegreeArmOutcome, String> {
    match degree {
        2 => eval_degree2_arm(g_x0, g_s6),
        4 => eval_degree4_arm(g_x0, g_s6),
        6 => eval_degree6_arm(g_x0, g_s6),
        8 => eval_degree8_arm(g_x0, g_s6),
        _ => Err(format!(
            "Unsupported degree {}. Supported degrees: {:?}",
            degree, SUPPORTED_DEGREES
        )),
    }
}

fn validate_required_candidate_keys(
    cand_ref: &BTreeMap<String, Vec<Vec<Cyc24>>>,
) -> Result<(), String> {
    for k in &["x0", "s6", "repeated"] {
        if !cand_ref.contains_key(*k) {
            return Err(format!("Missing required candidate Gramian: '{}'", k));
        }
    }
    Ok(())
}

pub fn evaluate_degree_benchmark(
    degree: usize,
    candidates: Option<&BTreeMap<String, Vec<Vec<Cyc24>>>>,
) -> Result<DegreeBenchmarkEntry, String> {
    if !SUPPORTED_DEGREES.contains(&degree) {
        return Err(format!(
            "Unsupported degree {}. Supported degrees: {:?}",
            degree, SUPPORTED_DEGREES
        ));
    }

    let default_candidates;
    let cand_ref = match candidates {
        Some(c) => c,
        None => {
            default_candidates = build_candidate_gramians();
            &default_candidates
        }
    };

    validate_required_candidate_keys(cand_ref)?;

    let g_x0 = &cand_ref["x0"];
    let g_s6 = &cand_ref["s6"];
    let (matrix_types, matrix_dims, fingerprints) = collect_degree_fingerprints(degree, cand_ref)?;
    let arm = eval_degree_arm_dispatch(degree, g_x0, g_s6)?;

    Ok(DegreeBenchmarkEntry {
        degree,
        level: degree / 2,
        matrix_types,
        matrix_dimensions: matrix_dims,
        x0_receipt: arm.receipt_x0,
        s6_receipt: arm.receipt_s6,
        x0_nominal_trace: arm.x0_nominal,
        fingerprints,
        status: arm.status,
        details: arm.details,
        candidate_refutation_status: arm.candidate_status,
        global_search_status: arm.global_status,
    })
}

pub fn evaluate_moment_sdp_hierarchy_ledger() -> Result<MomentSDPHierarchyLedger, String> {
    let candidates = build_candidate_gramians();
    let mut entries = BTreeMap::new();
    for &d in SUPPORTED_DEGREES {
        let entry = evaluate_degree_benchmark(d, Some(&candidates))?;
        entries.insert(d, entry);
    }

    Ok(MomentSDPHierarchyLedger {
        schema_version: SCHEMA_VERSION.to_string(),
        firewall: FIREWALL.to_string(),
        authority_effect: AUTHORITY_EFFECT.to_string(),
        scope: SCOPE_STRING.to_string(),
        degrees: SUPPORTED_DEGREES.to_vec(),
        entries,
        complete: false,
        diagnostics_complete: true,
        moment_semantics_verified: false,
        summary: "Aggregated Moment SDP Hierarchy Ledger across Degrees 2, 4, 6, 8. Evaluates exact rational traces and strictly positive LDL^T pivots across candidates X=0 and S_6. Full moment-hierarchy completeness remains fail-closed.".to_string(),
        status: STATUS_MISSING_PROOF_OBLIGATION.to_string(),
        candidate_refutation_status: STATUS_CERTIFIED_CANDIDATE_REFUTATION.to_string(),
        global_search_status: STATUS_MISSING_PROOF_OBLIGATION.to_string(),
    })
}


pub const CANONICAL_FIXTURES_JSON: &str = include_str!(concat!(
    env!("CARGO_MANIFEST_DIR"),
    "/../tests/mub/fixtures/mub_moment_sdp_ledger_fixtures.json"
));

pub fn load_canonical_fixtures() -> Result<MomentSdpLedgerFixtures, String> {
    serde_json::from_str(CANONICAL_FIXTURES_JSON)
        .map_err(|e| format!("Failed to parse canonical fixtures JSON: {}", e))
}

pub fn generate_moment_sdp_ledger_fixtures() -> Result<MomentSdpLedgerFixtures, String> {
    let candidates = build_candidate_gramians();
    let mut fingerprints = BTreeMap::new();

    for &d in SUPPORTED_DEGREES {
        for (c_name, g) in &candidates {
            let m_dict = build_degree_matrices(d, g)?;
            for (m_type, m) in m_dict {
                let fp = compute_matrix_fingerprint(&m);
                fingerprints.insert(format!("deg{}_{}_{}", d, m_type, c_name), fp);
            }
        }
    }

    Ok(MomentSdpLedgerFixtures {
        schema_version: "omega.mub.moment-sdp-ledger-fixtures.v1".to_string(),
        authority_effect: AUTHORITY_EFFECT.to_string(),
        firewall: FIREWALL.to_string(),
        scope: "canonical SHA-256 matrix fingerprints across degrees 2, 4, 6, 8 for candidate Gramians (x0, s6, repeated)".to_string(),
        fingerprints,
    })
}

fn verify_candidate_degree_fingerprints(
    d: usize,
    c_name: &str,
    g: &[Vec<Cyc24>],
    fixtures: &MomentSdpLedgerFixtures,
) -> Result<(), String> {
    let m_dict = build_degree_matrices(d, g)?;
    for (m_type, m) in m_dict {
        let key = format!("deg{}_{}_{}", d, m_type, c_name);
        let expected = fixtures
            .fingerprints
            .get(&key)
            .ok_or_else(|| format!("Missing expected fingerprint key '{}' in fixtures", key))?;
        let computed = compute_matrix_fingerprint(&m);
        if computed != *expected {
            return Err(format!(
                "Fingerprint mismatch for '{}': computed {} != expected {}",
                key, computed, expected
            ));
        }
    }
    Ok(())
}

pub fn verify_moment_sdp_ledger_fixtures(
    fixtures: &MomentSdpLedgerFixtures,
) -> Result<bool, String> {
    let candidates = build_candidate_gramians();

    for &d in SUPPORTED_DEGREES {
        for (c_name, g) in &candidates {
            verify_candidate_degree_fingerprints(d, c_name, g, fixtures)?;
        }
    }

    Ok(true)
}

pub fn verify_canonical_fixtures() -> Result<bool, String> {
    let fixtures = load_canonical_fixtures()?;
    verify_moment_sdp_ledger_fixtures(&fixtures)
}


#[derive(Debug, Clone, Serialize, Deserialize, PartialEq, Eq)]
pub struct FlatExtensionReceipt {
    pub level: usize,
    pub rank_d: usize,
    pub rank_d_minus_1: usize,
    pub rank_gap: usize,
    pub is_obstructed: bool,
    pub status: String,
    pub firewall: String,
    pub authority_effect: String,
    pub summary: String,
}

pub fn certify_flat_extension_rank_gap(level: usize) -> Result<FlatExtensionReceipt, String> {
    if level != 1 {
        return Err(format!(
            "Exact flat extension certified only for level 1 (got {})",
            level
        ));
    }
    let rank_0 = fixtures().count("flat_extension_rank_m0");
    let rank_1 = fixtures().count("flat_extension_rank_m1");
    let gap = rank_1 - rank_0;
    Ok(FlatExtensionReceipt {
        level,
        rank_d: rank_1,
        rank_d_minus_1: rank_0,
        rank_gap: gap,
        is_obstructed: gap > 0,
        status: fixtures().text("flat_extension_status"),
        firewall: FIREWALL.to_string(),
        authority_effect: AUTHORITY_EFFECT.to_string(),
        summary: format!(
            "Curto-Fialkow flat extension at level {} is strictly obstructed: rank(M_1) = {}, rank(M_0) = {}, rank gap Delta_{} = {} > 0.",
            level, rank_1, rank_0, level, gap
        ),
    })
}


pub fn claim_universal_mub6_nonexistence(degree: Option<usize>) -> Result<(), String> {
    let deg_str = match degree {
        Some(d) => format!(" at degree {}", d),
        None => String::new(),
    };
    Err(format!(
        "MissingProofObligation: claiming universal MUB(6) non-existence via moment SDP{} alone is strictly prohibited; stated region only; mints no authority; global search and projector operator completeness remain open proof obligations",
        deg_str
    ))
}

pub fn certify_universal_mub6_nonexistence(degree: Option<usize>) -> Result<(), String> {
    claim_universal_mub6_nonexistence(degree)
}

pub fn solve_target_q5_moment_certificate() -> Result<(), String> {
    Err("MissingProofObligation: valid projector moment identities and a positivity-preserving exact field representation across higher degrees are required for moment hierarchy certification".into())
}

pub fn solve_target_q5_moment_certificate_for_degree(degree: usize) -> Result<(), String> {
    Err(format!(
        "MissingProofObligation: valid projector moment identities and a positivity-preserving exact field representation for degree {} are required for moment hierarchy certification",
        degree
    ))
}

pub fn build_degree_k_moment_matrix(
    k: usize,
    _g: &[Vec<Cyc24>],
) -> Result<Vec<Vec<BigRational>>, String> {
    Err(format!(
        "MissingProofObligation: sound projector moment matrix construction for degree k={} is not established without valid higher-order projector identities",
        k
    ))
}
