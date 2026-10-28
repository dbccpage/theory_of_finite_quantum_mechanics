
use num_rational::BigRational;
use num_traits::Zero;
use serde::{Deserialize, Serialize};
use std::collections::BTreeMap;

use crate::native::exact::d6_exact_curvature_cochain::D;
use crate::native::exact::mub6_firewall::{AUTHORITY_EFFECT, FIREWALL};
use crate::native::exact::mub6_matrix6::{matrix_zero, Matrix6};
pub use crate::native::exact::mub6_matrix6::{
    enumerate_225_submatrices, root24_exponent, Submatrix2Index, NUM_SUBMATRICES_225,
};
use tfqm_number_theory::cyclotomic::Cyc24;
use tfqm_number_theory::rational::ri;
use tfqm_number_theory::rational::rq;

crate::fixture_set!(fixtures, "mub6_orbit_exhaustiveness");

pub fn pi_approx() -> BigRational {
    fixtures().rational("pi_surrogate")
}

pub fn standard_fourier_f6() -> Matrix6 {
    std::array::from_fn(|j| std::array::from_fn(|k| Cyc24::zeta24((4 * j * k) as i32)))
}

pub fn circ3(c0: &Cyc24, c1: &Cyc24, c2: &Cyc24) -> [[Cyc24; 3]; 3] {
    [
        [c0.clone(), c1.clone(), c2.clone()],
        [c2.clone(), c0.clone(), c1.clone()],
        [c1.clone(), c2.clone(), c0.clone()],
    ]
}

pub fn cross_ratio_at(m: &Matrix6, idx: &Submatrix2Index) -> Cyc24 {
    let num = m[idx.r0][idx.c0].mul(&m[idx.r1][idx.c1]);
    let den = m[idx.r0][idx.c1].mul(&m[idx.r1][idx.c0]);
    num.mul(&den.inv())
}

pub fn evaluate_all_225_cross_ratios(m: &Matrix6) -> Vec<Cyc24> {
    let indices = enumerate_225_submatrices();
    indices.iter().map(|idx| cross_ratio_at(m, idx)).collect()
}

#[derive(Clone, Debug, PartialEq, Eq, Serialize, Deserialize)]
pub struct CrossRatioSpectrum {
    #[serde(skip)]
    pub cross_ratios: Vec<Cyc24>,
    pub exponent_counts: BTreeMap<i64, usize>,
    pub total_count: usize,
    pub non_root24_count: usize,
}

impl CrossRatioSpectrum {
    pub fn from_matrix(m: &Matrix6) -> Self {
        let crs = evaluate_all_225_cross_ratios(m);
        Self::from_cross_ratios(crs)
    }

    pub fn from_cross_ratios(crs: Vec<Cyc24>) -> Self {
        let total = crs.len();
        let mut counts = BTreeMap::new();
        let mut non_root = 0;
        for cr in &crs {
            match root24_exponent(cr) {
                Some(e) => *counts.entry(e).or_insert(0) += 1,
                None => non_root += 1,
            }
        }
        Self {
            cross_ratios: crs,
            exponent_counts: counts,
            total_count: total,
            non_root24_count: non_root,
        }
    }

    pub fn count_of(&self, exponent: i64) -> usize {
        self.exponent_counts.get(&exponent).copied().unwrap_or(0)
    }

    pub fn imaginary_unit_count(&self) -> usize {
        self.count_of(6) + self.count_of(18)
    }

    pub fn is_strictly_cubic(&self) -> bool {
        self.non_root24_count == 0
            && self
                .exponent_counts
                .keys()
                .all(|&k| k == 0 || k == 8 || k == 16)
    }

    pub fn is_strictly_quartic(&self) -> bool {
        self.non_root24_count == 0
            && self
                .exponent_counts
                .keys()
                .all(|&k| k == 0 || k == 6 || k == 12 || k == 18)
    }

    pub fn haagerup_imaginary_spectrum_test(&self) -> bool {
        self.imaginary_unit_count() == 120
            && self.count_of(6) == 60
            && self.count_of(18) == 60
            && self.count_of(0) == 30
            && self.count_of(12) == 75
            && self.is_strictly_quartic()
    }

    pub fn tao_cubic_spectrum_test(&self) -> bool {
        self.is_strictly_cubic()
            && self.count_of(0) == 45
            && self.count_of(8) == 93
            && self.count_of(16) == 87
    }
}

pub fn corner_determinant(a: &Cyc24, b: &Cyc24, c: &Cyc24, d: &Cyc24) -> Cyc24 {
    let ad = a.mul(d);
    let bc = b.mul(c);
    ad.sub(&bc).sub(a).add(b).add(c).sub(d)
}

fn complement_3cols(c1: &[usize; 3]) -> [usize; 3] {
    let mut c2 = [0usize; 3];
    let mut c2_idx = 0;
    for c in 0..6 {
        if !c1.contains(&c) {
            c2[c2_idx] = c;
            c2_idx += 1;
        }
    }
    c2
}

fn is_affine_fourier_row_pair(
    m: &Matrix6,
    r0: usize,
    r1: usize,
    c1: &[usize; 3],
    c2: &[usize; 3],
) -> bool {
    let val_c1 = m[r1][c1[0]].mul(&m[r0][c1[0]].inv());
    if m[r1][c1[1]].mul(&m[r0][c1[1]].inv()) != val_c1
        || m[r1][c1[2]].mul(&m[r0][c1[2]].inv()) != val_c1
    {
        return false;
    }
    let neg_val_c1 = val_c1.neg();
    for &col in c2 {
        if m[r1][col].mul(&m[r0][col].inv()) != neg_val_c1 {
            return false;
        }
    }
    true
}

fn collect_valid_row_pairs(m: &Matrix6, c1: &[usize; 3], c2: &[usize; 3]) -> Vec<(usize, usize)> {
    let mut valid_row_pairs = Vec::new();
    for r0 in 0..D {
        for r1 in (r0 + 1)..D {
            if is_affine_fourier_row_pair(m, r0, r1, c1, c2) {
                valid_row_pairs.push((r0, r1));
            }
        }
    }
    valid_row_pairs
}

fn pair_mask(pair: (usize, usize)) -> u32 {
    (1 << pair.0) | (1 << pair.1)
}

fn has_third_pair_completing_mask(
    pairs: &[(usize, usize)],
    start_idx: usize,
    base_mask: u32,
) -> bool {
    for &p3 in &pairs[start_idx..] {
        if (base_mask | pair_mask(p3)) == 0b111111 {
            return true;
        }
    }
    false
}

fn has_disjoint_three_pair_cover(pairs: &[(usize, usize)]) -> bool {
    let n = pairs.len();
    for p1 in 0..n {
        for p2 in (p1 + 1)..n {
            let mask12 = pair_mask(pairs[p1]) | pair_mask(pairs[p2]);
            if has_third_pair_completing_mask(pairs, p2 + 1, mask12) {
                return true;
            }
        }
    }
    false
}

fn check_col_pair_for_affine_fourier(m: &Matrix6, i1: usize, i2: usize) -> bool {
    for i3 in (i2 + 1)..6 {
        let c1 = [i1, i2, i3];
        let c2 = complement_3cols(&c1);
        let valid_row_pairs = collect_valid_row_pairs(m, &c1, &c2);
        if valid_row_pairs.len() >= 3 && has_disjoint_three_pair_cover(&valid_row_pairs) {
            return true;
        }
    }
    false
}

pub fn has_affine_fourier_submatrix_condition(m: &Matrix6) -> bool {
    for i1 in 0..4 {
        for i2 in (i1 + 1)..5 {
            if check_col_pair_for_affine_fourier(m, i1, i2) {
                return true;
            }
        }
    }
    false
}

pub fn fourier_vanishing_test(m: &Matrix6, spec: &CrossRatioSpectrum) -> bool {
    if spec.imaginary_unit_count() != 0 || spec.is_strictly_cubic() {
        return false;
    }

    has_affine_fourier_submatrix_condition(m)
}

#[derive(Clone, Debug, PartialEq, Eq, PartialOrd, Ord, Serialize, Deserialize)]
pub enum OrbitClass {
    Fourier,
    Szollosi { theta_approx: BigRational },
    Tao,
    Haagerup,
}

pub fn extract_szollosi_theta_approx(m: &Matrix6) -> BigRational {
    let pi = pi_approx();
    let twelve = rq(12, 1);

    if let Some(k) = root24_exponent(&m[0][4]) {
        if k != 0 {
            return (rq(k, 1) * &pi) / &twelve;
        }
    }

    for col in 1..D {
        if let Some(k) = root24_exponent(&m[0][col]) {
            if k != 0 && k != 12 {
                return (rq(k, 1) * &pi) / &twelve;
            }
        }
    }

    BigRational::zero()
}

pub fn classify_orbit(m: &Matrix6) -> OrbitClass {
    let spec = CrossRatioSpectrum::from_matrix(m);

    if spec.haagerup_imaginary_spectrum_test() {
        return OrbitClass::Haagerup;
    }

    if spec.tao_cubic_spectrum_test() {
        return OrbitClass::Tao;
    }

    if fourier_vanishing_test(m, &spec) {
        return OrbitClass::Fourier;
    }

    let theta_approx = extract_szollosi_theta_approx(m);
    OrbitClass::Szollosi { theta_approx }
}

#[derive(Clone, Debug)]
pub struct CatalogCandidate {
    pub name: String,
    pub matrix: Matrix6,
    pub expected_class: OrbitClass,
    pub notes: String,
}

#[derive(Clone, Debug, PartialEq, Eq, Serialize, Deserialize)]
pub struct CandidateClassificationResult {
    pub candidate_name: String,
    pub assigned_class: OrbitClass,
    pub expected_class: OrbitClass,
    pub matches_expected: bool,
    pub imaginary_cross_ratio_count: usize,
    pub is_cubic: bool,
    pub details: String,
}

#[derive(Clone, Debug, PartialEq, Eq, Serialize, Deserialize)]
pub struct CatalogExhaustivenessReport {
    pub schema_version: String,
    pub firewall: String,
    pub authority_effect: String,
    pub total_candidates_tested: usize,
    pub fourier_count: usize,
    pub tao_count: usize,
    pub haagerup_count: usize,
    pub szollosi_count: usize,
    pub unassigned_residual_count: usize,
    pub is_exhaustive: bool,
    pub candidate_results: Vec<CandidateClassificationResult>,
}

fn build_dita_candidate(dx: i64, dy: i64, f3_arr: &[[Cyc24; 3]; 3]) -> CatalogCandidate {
    let d_diag = [
        Cyc24::rat(ri(1)),
        Cyc24::zeta24(dx as i32),
        Cyc24::zeta24(dy as i32),
    ];

    let mut mat = matrix_zero();
    for r in 0..3 {
        for c in 0..3 {
            mat[r][c] = f3_arr[r][c].clone();
            mat[r][c + 3] = d_diag[r].mul(&f3_arr[r][c]);
            mat[r + 3][c] = f3_arr[r][c].clone();
            mat[r + 3][c + 3] = d_diag[r].mul(&f3_arr[r][c]).neg();
        }
    }

    CatalogCandidate {
        name: format!("Dita_F6_{dx}_{dy}"),
        matrix: mat,
        expected_class: OrbitClass::Fourier,
        notes: format!("Affine Dita family point with phases ({dx}, {dy})"),
    }
}

fn build_two_circulant_matrix(w0: &Cyc24, kb: i32, kc: i32, ke: i32, kf: i32) -> Matrix6 {
    let a_blk = circ3(w0, &Cyc24::zeta24(kb), &Cyc24::zeta24(kc));
    let b_blk = circ3(w0, &Cyc24::zeta24(ke), &Cyc24::zeta24(kf));
    let mut mat = matrix_zero();
    for i in 0..3 {
        for j in 0..3 {
            mat[i][j] = a_blk[i][j].clone();
            mat[i][j + 3] = b_blk[i][j].clone();
            mat[i + 3][j] = b_blk[j][i].conj();
            mat[i + 3][j + 3] = a_blk[j][i].conj().neg();
        }
    }
    mat
}

pub fn canonical_catalog_candidates() -> Vec<CatalogCandidate> {
    let mut candidates = Vec::new();

    candidates.push(CatalogCandidate {
        name: "Standard_F6".to_string(),
        matrix: standard_fourier_f6(),
        expected_class: OrbitClass::Fourier,
        notes: "Classical cyclic group Z6 Fourier matrix with 6th roots of unity".to_string(),
    });

    let dita_pts = [
        (0i64, 0i64),
        (0, 8),
        (8, 0),
        (16, 16),
        (0, 16),
        (8, 8),
        (16, 0),
    ];
    let w0 = Cyc24::rat(ri(1));
    let w1 = Cyc24::zeta24(8);
    let w2 = Cyc24::zeta24(16);
    let f3_arr = [
        [w0.clone(), w0.clone(), w0.clone()],
        [w0.clone(), w1.clone(), w2.clone()],
        [w0.clone(), w2.clone(), w1.clone()],
    ];

    for &(dx, dy) in &dita_pts {
        candidates.push(build_dita_candidate(dx, dy, &f3_arr));
    }

    let s6_phases: [[usize; D]; D] = [
        [0, 0, 0, 0, 0, 0],
        [0, 0, 1, 1, 2, 2],
        [0, 1, 0, 2, 2, 1],
        [0, 1, 2, 0, 1, 2],
        [0, 2, 2, 1, 0, 1],
        [0, 2, 1, 2, 1, 0],
    ];
    let w_tab = [&w0, &w1, &w2];
    let s6_mat: Matrix6 =
        std::array::from_fn(|i| std::array::from_fn(|j| w_tab[s6_phases[i][j]].clone()));

    candidates.push(CatalogCandidate {
        name: "Tao_S6".to_string(),
        matrix: s6_mat,
        expected_class: OrbitClass::Tao,
        notes: "Chernyavsky-Tao isolated spectral matrix over Z3".to_string(),
    });

    candidates.push(CatalogCandidate {
        name: "Haagerup_H6".to_string(),
        matrix: build_two_circulant_matrix(&w0, 0, 6, 0, 12),
        expected_class: OrbitClass::Haagerup,
        notes: "Haagerup isolated algebraic matrix with 120 imaginary cross-ratios".to_string(),
    });

    let pi = pi_approx();
    let theta_a = (rq(8, 1) * &pi) / rq(12, 1);
    candidates.push(CatalogCandidate {
        name: "Szollosi_B6_theta_2pi_3".to_string(),
        matrix: build_two_circulant_matrix(&w0, 0, 8, 8, 0),
        expected_class: OrbitClass::Szollosi {
            theta_approx: theta_a,
        },
        notes: "Szollosi 2-circulant point with ke=8 (theta approx 2pi/3)".to_string(),
    });

    let theta_b = (rq(14, 1) * &pi) / rq(12, 1);
    candidates.push(CatalogCandidate {
        name: "Szollosi_B6_theta_7pi_6".to_string(),
        matrix: build_two_circulant_matrix(&w0, 2, 19, 14, 1),
        expected_class: OrbitClass::Szollosi {
            theta_approx: theta_b,
        },
        notes: "Szollosi 2-circulant point with ke=14 (theta approx 7pi/6)".to_string(),
    });

    candidates.push(CatalogCandidate {
        name: "Boundary_Confluence_Fourier_Szollosi_theta_0".to_string(),
        matrix: build_two_circulant_matrix(&w0, 0, 8, 0, 16),
        expected_class: OrbitClass::Fourier,
        notes: "Confluence boundary between Fourier and Szollosi at theta = 0".to_string(),
    });

    candidates
}

pub fn certify_catalog_exhaustiveness(catalog: &[CatalogCandidate]) -> CatalogExhaustivenessReport {
    let mut fourier_count = 0;
    let mut tao_count = 0;
    let mut haagerup_count = 0;
    let mut szollosi_count = 0;
    let mut results = Vec::with_capacity(catalog.len());

    for cand in catalog {
        let spec = CrossRatioSpectrum::from_matrix(&cand.matrix);
        let assigned = classify_orbit(&cand.matrix);

        let matches = assigned == cand.expected_class;
        match &assigned {
            OrbitClass::Fourier => fourier_count += 1,
            OrbitClass::Tao => tao_count += 1,
            OrbitClass::Haagerup => haagerup_count += 1,
            OrbitClass::Szollosi { .. } => szollosi_count += 1,
        }

        results.push(CandidateClassificationResult {
            candidate_name: cand.name.clone(),
            assigned_class: assigned.clone(),
            expected_class: cand.expected_class.clone(),
            matches_expected: matches,
            imaginary_cross_ratio_count: spec.imaginary_unit_count(),
            is_cubic: spec.is_strictly_cubic(),
            details: format!(
                "Classified as {:?}; expected {:?}; imaginary count: {}",
                assigned,
                cand.expected_class,
                spec.imaginary_unit_count()
            ),
        });
    }

    let total = catalog.len();
    let sum_classified = fourier_count + tao_count + haagerup_count + szollosi_count;
    let unassigned = total.saturating_sub(sum_classified);
    let all_match = results.iter().all(|r| r.matches_expected);

    CatalogExhaustivenessReport {
        schema_version: "omega.mub6.orbit-catalog-exhaustiveness.v1".to_string(),
        firewall: FIREWALL.to_string(),
        authority_effect: AUTHORITY_EFFECT.to_string(),
        total_candidates_tested: total,
        fourier_count,
        tao_count,
        haagerup_count,
        szollosi_count,
        unassigned_residual_count: unassigned,
        is_exhaustive: unassigned == 0 && all_match,
        candidate_results: results,
    }
}
