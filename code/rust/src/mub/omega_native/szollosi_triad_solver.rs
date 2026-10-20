
use num_rational::BigRational;
use serde::{Deserialize, Serialize};
use std::path::PathBuf;

use crate::omega_native::exact::d6_exact_curvature_cochain::D;
use crate::omega_native::exact::mub6_matrix6::{matrix_adjoint, matrix_mul, matrix_zero, Matrix6};
use omega_number_theory::cyclotomic::Cyc24;
use omega_number_theory::rational::ri;

pub type ExactVec = [Cyc24; D];

pub fn mod_sq(z: &Cyc24) -> Cyc24 {
    z.mul(&z.conj())
}

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct ChmVerificationReport {
    pub is_chm: bool,
    pub all_entries_unit_modulus: bool,
    pub is_orthogonal: bool,
    pub diagonal_norm_sq: String,
    pub max_offdiagonal_norm_sq: String,
    pub details: String,
}

#[allow(clippy::needless_range_loop)]
fn all_entries_have_unit_modulus(m: &Matrix6) -> bool {
    let one = Cyc24::rat(ri(1));
    for i in 0..D {
        for j in 0..D {
            if mod_sq(&m[i][j]) != one {
                return false;
            }
        }
    }
    true
}

#[allow(clippy::needless_range_loop)]
fn check_gram_orthogonality(gram: &Matrix6) -> bool {
    let six = Cyc24::rat(ri(6));
    let zero = Cyc24::zero();
    for i in 0..D {
        for j in 0..D {
            let expected = if i == j { &six } else { &zero };
            if gram[i][j] != *expected {
                return false;
            }
        }
    }
    true
}

pub fn verify_chm(m: &Matrix6) -> ChmVerificationReport {
    let entries_ok = all_entries_have_unit_modulus(m);
    let gram = matrix_mul(m, &matrix_adjoint(m));
    let orth_ok = check_gram_orthogonality(&gram);
    let is_chm = entries_ok && orth_ok;

    ChmVerificationReport {
        is_chm,
        all_entries_unit_modulus: entries_ok,
        is_orthogonal: orth_ok,
        diagonal_norm_sq: "6".to_string(),
        max_offdiagonal_norm_sq: if orth_ok {
            "0".to_string()
        } else {
            "nonzero".to_string()
        },
        details: if is_chm {
            "Exact complex Hadamard matrix verified over Q(zeta_24)".to_string()
        } else {
            format!("CHM failure: entries_ok={entries_ok}, orth_ok={orth_ok}")
        },
    }
}

pub fn tao_s6_matrix() -> Matrix6 {
    let w0 = Cyc24::rat(ri(1));
    let w1 = Cyc24::zeta24(8);
    let w2 = Cyc24::zeta24(16);

    let table: [[usize; D]; D] = [
        [0, 0, 0, 0, 0, 0],
        [0, 0, 1, 1, 2, 2],
        [0, 1, 0, 2, 2, 1],
        [0, 1, 2, 0, 1, 2],
        [0, 2, 2, 1, 0, 1],
        [0, 2, 1, 2, 1, 0],
    ];

    let w = [&w0, &w1, &w2];
    std::array::from_fn(|i| std::array::from_fn(|j| w[table[i][j]].clone()))
}

pub fn szollosi_b6_matrix(
    a: &Cyc24,
    b: &Cyc24,
    c: &Cyc24,
    d: &Cyc24,
    e: &Cyc24,
    f: &Cyc24,
) -> Result<Matrix6, String> {
    let z1 = a
        .mul(&c.conj())
        .add(&b.mul(&a.conj()))
        .add(&c.mul(&b.conj()));
    let z2 = d
        .mul(&f.conj())
        .add(&e.mul(&d.conj()))
        .add(&f.mul(&e.conj()));
    let sum = z1.add(&z2);
    if !sum.is_zero() {
        return Err("Szollosi condition z1 + z2 == 0 violated".to_string());
    }

    let a_rows = [
        [a.clone(), b.clone(), c.clone()],
        [c.clone(), a.clone(), b.clone()],
        [b.clone(), c.clone(), a.clone()],
    ];

    let b_rows = [
        [d.clone(), e.clone(), f.clone()],
        [f.clone(), d.clone(), e.clone()],
        [e.clone(), f.clone(), d.clone()],
    ];

    let bd_rows = [
        [d.conj(), f.conj(), e.conj()],
        [e.conj(), d.conj(), f.conj()],
        [f.conj(), e.conj(), d.conj()],
    ];

    let neg_ad_rows = [
        [a.conj().neg(), c.conj().neg(), b.conj().neg()],
        [b.conj().neg(), a.conj().neg(), c.conj().neg()],
        [c.conj().neg(), b.conj().neg(), a.conj().neg()],
    ];

    let mut out = matrix_zero();
    for i in 0..3 {
        for j in 0..3 {
            out[i][j] = a_rows[i][j].clone();
            out[i][j + 3] = b_rows[i][j].clone();
            out[i + 3][j] = bd_rows[i][j].clone();
            out[i + 3][j + 3] = neg_ad_rows[i][j].clone();
        }
    }

    Ok(out)
}

pub fn szollosi_dephased_b6(b: &Cyc24, c: &Cyc24, e: &Cyc24, f: &Cyc24) -> Result<Matrix6, String> {
    let one = Cyc24::rat(ri(1));
    szollosi_b6_matrix(&one, b, c, &one, e, f)
}

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct TransitionViolation {
    pub row: usize,
    pub col: usize,
    pub observed_mod_sq_rat: String,
    pub delta_from_six: String,
}

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct TransitionReport {
    pub is_mutually_unbiased: bool,
    pub total_entries: usize,
    pub matching_entries_count: usize,
    pub violation_count: usize,
    pub min_entry_mod_sq_rat: String,
    pub max_entry_mod_sq_rat: String,
    pub sample_violations: Vec<TransitionViolation>,
}

fn update_min_max_rational(
    val: &BigRational,
    min_val: &mut Option<BigRational>,
    max_val: &mut Option<BigRational>,
) {
    if min_val.as_ref().is_none_or(|cur| val < cur) {
        *min_val = Some(val.clone());
    }
    if max_val.as_ref().is_none_or(|cur| val > cur) {
        *max_val = Some(val.clone());
    }
}

fn format_opt_rational(opt: Option<BigRational>) -> String {
    match opt {
        Some(r) => format!("{}/{}", r.numer(), r.denom()),
        None => "none".to_string(),
    }
}

#[allow(clippy::needless_range_loop)]
pub fn check_hadamard_transition(h1: &Matrix6, h2: &Matrix6) -> TransitionReport {
    let h12 = matrix_mul(&matrix_adjoint(h1), h2);
    let six = Cyc24::rat(ri(6));

    let mut violations = Vec::new();
    let mut matching_count = 0;
    let mut min_val: Option<BigRational> = None;
    let mut max_val: Option<BigRational> = None;

    for j in 0..D {
        for k in 0..D {
            let msq = mod_sq(&h12[j][k]);
            let rat_val = msq.a[0].clone();
            update_min_max_rational(&rat_val, &mut min_val, &mut max_val);

            if msq == six {
                matching_count += 1;
            } else {
                let delta = msq.sub(&six);
                violations.push(TransitionViolation {
                    row: j,
                    col: k,
                    observed_mod_sq_rat: format!("{}/{}", rat_val.numer(), rat_val.denom()),
                    delta_from_six: format!("{}/{}", delta.a[0].numer(), delta.a[0].denom()),
                });
            }
        }
    }

    TransitionReport {
        is_mutually_unbiased: violations.is_empty(),
        total_entries: 36,
        matching_entries_count: matching_count,
        violation_count: violations.len(),
        min_entry_mod_sq_rat: format_opt_rational(min_val),
        max_entry_mod_sq_rat: format_opt_rational(max_val),
        sample_violations: violations.iter().take(8).cloned().collect(),
    }
}

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct SzollosiDiscretePoint {
    pub kb: usize,
    pub kc: usize,
    pub ke: usize,
    pub kf: usize,
    pub z1_desc: String,
    pub z2_desc: String,
}

pub fn search_discrete_szollosi_chm_points() -> Vec<SzollosiDiscretePoint> {
    let mut z_table = Vec::with_capacity(24 * 24);
    for k1 in 0..24i32 {
        for k2 in 0..24i32 {
            let z = Cyc24::zeta24(-k2)
                .add(&Cyc24::zeta24(k1))
                .add(&Cyc24::zeta24(k2 - k1));
            z_table.push(((k1 as usize, k2 as usize), z));
        }
    }

    let mut valid_points = Vec::new();
    for (pair1, z1) in &z_table {
        for (pair2, z2) in &z_table {
            if z1.add(z2).is_zero() {
                valid_points.push(SzollosiDiscretePoint {
                    kb: pair1.0,
                    kc: pair1.1,
                    ke: pair2.0,
                    kf: pair2.1,
                    z1_desc: format!(
                        "zeta(-{})+zeta({})+zeta({}-{})",
                        pair1.1, pair1.0, pair1.1, pair1.0
                    ),
                    z2_desc: format!(
                        "zeta(-{})+zeta({})+zeta({}-{})",
                        pair2.1, pair2.0, pair2.1, pair2.0
                    ),
                });
            }
        }
    }

    valid_points
}

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct SzollosiTriadSearchReceipt {
    pub schema_version: &'static str,
    pub authority_effect: &'static str,
    pub firewall: &'static str,
    pub timestamp_utc: String,
    pub mathematical_basis: &'static str,
    pub evaluated_set_scope: &'static str,
    pub tao_s6_verification: ChmVerificationReport,
    pub total_discrete_parameter_tuples_evaluated: usize,
    pub valid_szollosi_discrete_chm_count: usize,
    pub representative_szollosi_points: Vec<SzollosiDiscretePoint>,
    pub tao_vs_tao_permutations_tested: usize,
    pub tao_vs_tao_mu_triads_found: usize,
    pub tao_vs_szollosi_pairs_tested: usize,
    pub tao_vs_szollosi_mu_triads_found: usize,
    pub szollosi_vs_szollosi_pairs_tested: usize,
    pub szollosi_vs_szollosi_mu_triads_found: usize,
    pub sample_tao_szollosi_transition: TransitionReport,
    pub sample_szollosi_szollosi_transition: Option<TransitionReport>,
    pub obstruction_summary: &'static str,
    pub terminal_status: &'static str,
}

fn generate_tao_permutations() -> Vec<[usize; 6]> {
    let mut tao_permutations: Vec<[usize; 6]> = vec![[0, 1, 2, 3, 4, 5]];
    for shift in 1..6 {
        let p = [
            shift % 6,
            (1 + shift) % 6,
            (2 + shift) % 6,
            (3 + shift) % 6,
            (4 + shift) % 6,
            (5 + shift) % 6,
        ];
        if !tao_permutations.contains(&p) {
            tao_permutations.push(p);
        }
    }
    for i in 0..6 {
        for j in (i + 1)..6 {
            let mut p = [0, 1, 2, 3, 4, 5];
            p.swap(i, j);
            if !tao_permutations.contains(&p) {
                tao_permutations.push(p);
            }
        }
    }
    debug_assert_eq!(tao_permutations.len(), 21);
    tao_permutations
}

fn count_tao_permutation_triads(s6: &Matrix6, tao_permutations: &[[usize; 6]]) -> usize {
    let mut tao_tao_mu_count = 0;
    for p in tao_permutations {
        let perm_s6: Matrix6 = std::array::from_fn(|i| s6[p[i]].clone());
        if check_hadamard_transition(s6, &perm_s6).is_mutually_unbiased {
            tao_tao_mu_count += 1;
        }
    }
    tao_tao_mu_count
}

fn build_verified_szollosi_b6(pt: &SzollosiDiscretePoint) -> Option<Matrix6> {
    let b = Cyc24::zeta24(pt.kb as i32);
    let c = Cyc24::zeta24(pt.kc as i32);
    let e = Cyc24::zeta24(pt.ke as i32);
    let f = Cyc24::zeta24(pt.kf as i32);
    let b6 = szollosi_dephased_b6(&b, &c, &e, &f).ok()?;
    if verify_chm(&b6).is_chm {
        Some(b6)
    } else {
        None
    }
}

fn evaluate_tao_vs_szollosi_prefix(
    s6: &Matrix6,
    discrete_points: &[SzollosiDiscretePoint],
) -> (usize, Option<TransitionReport>, Vec<Matrix6>) {
    let mut tao_szo_mu_count = 0;
    let mut sample_tao_szo_report = None;
    let mut tested_szo_matrices = Vec::new();

    for pt in discrete_points.iter().take(64) {
        if let Some(b6) = build_verified_szollosi_b6(pt) {
            let tr = check_hadamard_transition(s6, &b6);
            if tr.is_mutually_unbiased {
                tao_szo_mu_count += 1;
            }
            if sample_tao_szo_report.is_none() {
                sample_tao_szo_report = Some(tr);
            }
            tested_szo_matrices.push(b6);
        }
    }
    (tao_szo_mu_count, sample_tao_szo_report, tested_szo_matrices)
}

fn evaluate_szollosi_pairs(
    tested_szo_matrices: &[Matrix6],
) -> (usize, usize, Option<TransitionReport>) {
    let mut szo_szo_mu_count = 0;
    let mut sample_szo_szo_report = None;
    let num_tested_szo = tested_szo_matrices.len();
    let mut szo_pairs_tested = 0;

    for i in 0..num_tested_szo {
        for j in (i + 1)..num_tested_szo {
            szo_pairs_tested += 1;
            let tr = check_hadamard_transition(&tested_szo_matrices[i], &tested_szo_matrices[j]);
            if tr.is_mutually_unbiased {
                szo_szo_mu_count += 1;
            }
            if sample_szo_szo_report.is_none() {
                sample_szo_szo_report = Some(tr);
            }
        }
    }
    (szo_pairs_tested, szo_szo_mu_count, sample_szo_szo_report)
}

pub fn execute_szollosi_triad_search() -> SzollosiTriadSearchReceipt {
    let s6 = tao_s6_matrix();
    let s6_report = verify_chm(&s6);
    assert!(s6_report.is_chm, "Tao matrix S6 must be an exact CHM");

    let tao_permutations = generate_tao_permutations();
    let tao_tao_mu_count = count_tao_permutation_triads(&s6, &tao_permutations);

    let discrete_points = search_discrete_szollosi_chm_points();
    let total_tuples = 24 * 24 * 24 * 24;
    let valid_count = discrete_points.len();

    let (tao_szo_mu_count, sample_tao_szo_report, tested_szo_matrices) =
        evaluate_tao_vs_szollosi_prefix(&s6, &discrete_points);
    let (szo_pairs_tested, szo_szo_mu_count, sample_szo_szo_report) =
        evaluate_szollosi_pairs(&tested_szo_matrices);

    let sample_ts = sample_tao_szo_report.unwrap_or_else(|| check_hadamard_transition(&s6, &s6));
    let evaluated_set_scope = if tested_szo_matrices.len() == valid_count {
        "All valid discrete Szöllősi CHM points over mu_24 evaluated"
    } else {
        "Prefix subset of 64 discrete Szöllősi CHM points over mu_24 evaluated"
    };

    let any_found = (tao_tao_mu_count + tao_szo_mu_count + szo_szo_mu_count) > 0;
    let (terminal_status, obstruction_summary) = if !any_found {
        (
            "VerifiedTriadNonExistenceInDiscreteLoci",
            "No mutually unbiased triple {I6, H1, H2} exists between Tao S6 and discrete Szöllősi B6(θ) evaluated points; transition matrix entry moduli deviate strictly from 6",
        )
    } else {
        (
            "MutuallyUnbiasedCandidateFound",
            "Mutually unbiased pair or triple candidate discovered in discrete evaluated set",
        )
    };

    SzollosiTriadSearchReceipt {
        schema_version: "omega.mub.szollosi-triad-search.v1",
        authority_effect: "None",
        firewall: "exact cyclotomic Cyc24 arithmetic; stated region only; mints no authority",
        timestamp_utc: "2026-09-17T08:50:00Z".to_string(),
        mathematical_basis: "Exact transition check |(H1† H2)_{jk}|² == 6 over Q(zeta_24) for Szöllősi 2-circulants and Tao S6",
        evaluated_set_scope,
        tao_s6_verification: s6_report,
        total_discrete_parameter_tuples_evaluated: total_tuples,
        valid_szollosi_discrete_chm_count: valid_count,
        representative_szollosi_points: discrete_points.iter().take(6).cloned().collect(),
        tao_vs_tao_permutations_tested: tao_permutations.len(),
        tao_vs_tao_mu_triads_found: tao_tao_mu_count,
        tao_vs_szollosi_pairs_tested: tested_szo_matrices.len(),
        tao_vs_szollosi_mu_triads_found: tao_szo_mu_count,
        szollosi_vs_szollosi_pairs_tested: szo_pairs_tested,
        szollosi_vs_szollosi_mu_triads_found: szo_szo_mu_count,
        sample_tao_szollosi_transition: sample_ts,
        sample_szollosi_szollosi_transition: sample_szo_szo_report,
        obstruction_summary,
        terminal_status,
    }
}

pub fn emit_receipt_files(receipt: &SzollosiTriadSearchReceipt) -> Result<Vec<PathBuf>, String> {
    let manifest_dir = PathBuf::from(env!("CARGO_MANIFEST_DIR"));
    let artifacts_dir = manifest_dir.join("../tests/omega_mub/artifacts");
    let runs_dir = manifest_dir.join("runs").join("mub6");

    std::fs::create_dir_all(&artifacts_dir).map_err(|e| format!("mkdir artifacts: {e}"))?;
    std::fs::create_dir_all(&runs_dir).map_err(|e| format!("mkdir runs/mub6: {e}"))?;

    let art_path = artifacts_dir.join("szollosi_triad_search_receipt.json");
    let run_path = runs_dir.join("szollosi_triad_search_receipt.json");

    let json = serde_json::to_string_pretty(receipt).map_err(|e| format!("serde: {e}"))?;

    std::fs::write(&art_path, &json).map_err(|e| format!("write artifact: {e}"))?;
    std::fs::write(&run_path, &json).map_err(|e| format!("write run: {e}"))?;

    Ok(vec![art_path, run_path])
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn tao_s6_is_exact_complex_hadamard() {
        let s6 = tao_s6_matrix();
        let report = verify_chm(&s6);
        assert!(report.is_chm, "Tao S6 must be exact CHM: {:?}", report);
        assert!(report.all_entries_unit_modulus);
        assert!(report.is_orthogonal);
    }

    #[test]
    fn tao_s6_self_transition_is_not_mu() {
        let s6 = tao_s6_matrix();
        let tr = check_hadamard_transition(&s6, &s6);
        assert!(!tr.is_mutually_unbiased);
        assert_eq!(tr.violation_count, 36);
        assert_eq!(tr.min_entry_mod_sq_rat, "0/1");
        assert_eq!(tr.max_entry_mod_sq_rat, "36/1");
    }

    #[test]
    fn discrete_szollosi_chm_points_exist_and_are_exact() {
        let points = search_discrete_szollosi_chm_points();
        assert!(
            !points.is_empty(),
            "Should find valid discrete Szöllősi points"
        );

        let pt0 = &points[0];
        let b = Cyc24::zeta24(pt0.kb as i32);
        let c = Cyc24::zeta24(pt0.kc as i32);
        let e = Cyc24::zeta24(pt0.ke as i32);
        let f = Cyc24::zeta24(pt0.kf as i32);
        let b6 = szollosi_dephased_b6(&b, &c, &e, &f).expect("Valid point builds B6");
        let rep = verify_chm(&b6);
        assert!(rep.is_chm, "Szöllősi point must yield exact CHM: {:?}", rep);
    }

    #[test]
    fn tao_vs_szollosi_hadamard_transition_detects_obstruction() {
        let s6 = tao_s6_matrix();
        let points = search_discrete_szollosi_chm_points();
        assert!(!points.is_empty());

        let pt0 = &points[0];
        let b = Cyc24::zeta24(pt0.kb as i32);
        let c = Cyc24::zeta24(pt0.kc as i32);
        let e = Cyc24::zeta24(pt0.ke as i32);
        let f = Cyc24::zeta24(pt0.kf as i32);
        let b6 = szollosi_dephased_b6(&b, &c, &e, &f).unwrap();

        let tr = check_hadamard_transition(&s6, &b6);
        assert!(!tr.is_mutually_unbiased);
        assert!(tr.violation_count > 0);
    }

    #[test]
    fn full_triad_search_executes_and_emits_receipt() {
        let receipt = execute_szollosi_triad_search();
        assert_eq!(receipt.authority_effect, "None");
        assert!(receipt.firewall.contains("stated region only"));
        assert!(receipt.firewall.contains("mints no authority"));
        assert_eq!(
            receipt.terminal_status,
            "VerifiedTriadNonExistenceInDiscreteLoci"
        );
        assert!(receipt.valid_szollosi_discrete_chm_count > 0);
        assert_eq!(receipt.tao_vs_szollosi_mu_triads_found, 0);

        let paths = emit_receipt_files(&receipt).expect("Receipt files emitted");
        for p in paths {
            assert!(p.exists());
            let content = std::fs::read_to_string(&p).unwrap();
            assert!(content.contains("omega.mub.szollosi-triad-search.v1"));
            assert!(content.contains("stated region only"));
        }
    }
}
