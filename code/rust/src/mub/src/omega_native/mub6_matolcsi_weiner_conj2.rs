
use crate::omega_native::exact::d6_exact_curvature_cochain::{
    inner, is_mutually_unbiased_triple_exact, ExactVec, COLUMN_COUNT,
};
use omega_number_theory::cyclotomic::Cyc24;
use serde::Serialize;

type GammaVec = [i64; 6];

pub fn gamma1_permutations() -> Vec<GammaVec> {
    let base = [1i64, 1, 1, -1, -1, -1];
    let mut perms = Vec::new();
    for_each_perm_of_multiset(&base, &mut perms);
    perms.sort();
    perms.dedup();
    perms
}

pub fn gamma2_permutations() -> Vec<GammaVec> {
    let base = [3i64, 3, 3, -3, -3, -3];
    let mut perms = Vec::new();
    for_each_perm_of_multiset(&base, &mut perms);
    perms.sort();
    perms.dedup();
    perms
}

fn for_each_perm_of_multiset(base: &[i64; 6], out: &mut Vec<GammaVec>) {
    let mut arr = *base;
    arr.sort();
    loop {
        out.push(arr);
        if !next_permutation(&mut arr) {
            break;
        }
    }
}

fn next_permutation(arr: &mut [i64; 6]) -> bool {
    let n = arr.len();
    if n <= 1 {
        return false;
    }
    let mut i = n - 1;
    while i > 0 && arr[i - 1] >= arr[i] {
        i -= 1;
    }
    if i == 0 {
        return false;
    }
    let mut j = n - 1;
    while arr[j] <= arr[i - 1] {
        j -= 1;
    }
    arr.swap(i - 1, j);
    arr[i..].reverse();
    true
}

pub fn evaluate_g_h(h: &[[Cyc24; 6]; 6], gamma: &GammaVec) -> Cyc24 {
    let mut sum = Cyc24::zero();
    for j in 0..6 {
        let mut prod = Cyc24::one();
        for k in 0..6 {
            let exp = gamma[k];
            let entry = &h[k][j];
            if exp >= 0 {
                for _ in 0..exp {
                    prod = prod.mul(entry);
                }
            } else {
                let conj = entry.conj();
                for _ in 0..(-exp) {
                    prod = prod.mul(&conj);
                }
            }
        }
        sum = sum.add(&prod);
    }
    sum.mul(&sum.conj())
}

#[derive(Debug, Clone, Serialize)]
pub struct Conj2SingleResult {
    pub matrix_id: String,
    pub gamma1_all_zero: bool,
    pub gamma1_failures: usize,
    pub gamma2_product_all_zero: bool,
    pub gamma2_failures: usize,
    pub conjecture_2_holds: bool,
}

#[derive(Debug, Clone, Serialize)]
pub struct Conj2TripleResult {
    pub triple_id: String,
    pub is_verified_mu_triple: bool,
    pub h12_result: Conj2SingleResult,
    pub h23_result: Conj2SingleResult,
    pub h31_result: Conj2SingleResult,
    pub conjecture_2_holds_on_triple: bool,
    pub firewall: String,
}

pub fn transition_matrix(basis1_cols: &[ExactVec], basis2_cols: &[ExactVec]) -> [[Cyc24; 6]; 6] {
    let sqrt_six = Cyc24::sqrt2().mul(&Cyc24::sqrt3());
    std::array::from_fn(|row| {
        std::array::from_fn(|col| {
            let ip = inner(&basis1_cols[row], &basis2_cols[col]);
            sqrt_six.mul(&ip)
        })
    })
}

pub fn extract_bases(all_cols: &[ExactVec]) -> (Vec<ExactVec>, Vec<ExactVec>, Vec<ExactVec>) {
    assert_eq!(all_cols.len(), COLUMN_COUNT, "expected 18 columns for triple");
    let b1: Vec<ExactVec> = all_cols[0..6].to_vec();
    let b2: Vec<ExactVec> = all_cols[6..12].to_vec();
    let b3: Vec<ExactVec> = all_cols[12..18].to_vec();
    (b1, b2, b3)
}

pub fn verify_mub_triple_conjecture2(triple_id: &str, all_cols: &[ExactVec]) -> Conj2TripleResult {
    let is_mu = is_mutually_unbiased_triple_exact(all_cols);
    let (b1, b2, b3) = extract_bases(all_cols);

    let h12 = transition_matrix(&b1, &b2);
    let h23 = transition_matrix(&b2, &b3);
    let h31 = transition_matrix(&b3, &b1);

    let r12 = verify_conjecture2_single(&format!("{triple_id}_H12"), &h12);
    let r23 = verify_conjecture2_single(&format!("{triple_id}_H23"), &h23);
    let r31 = verify_conjecture2_single(&format!("{triple_id}_H31"), &h31);

    let all_hold = is_mu && r12.conjecture_2_holds && r23.conjecture_2_holds && r31.conjecture_2_holds;

    Conj2TripleResult {
        triple_id: triple_id.to_string(),
        is_verified_mu_triple: is_mu,
        h12_result: r12,
        h23_result: r23,
        h31_result: r31,
        conjecture_2_holds_on_triple: all_hold,
        firewall: "stated region only; mints no authority".to_string(),
    }
}

pub fn verify_gamma1(h: &[[Cyc24; 6]; 6]) -> usize {
    let perms = gamma1_permutations();
    let mut failures = 0;
    for gamma in &perms {
        let val = evaluate_g_h(h, gamma);
        if !val.is_zero() {
            failures += 1;
        }
    }
    failures
}

pub fn verify_gamma2_product(h: &[[Cyc24; 6]; 6]) -> usize {
    let perms = gamma2_permutations();
    let h_star = adjoint_matrix(h);
    let mut failures = 0;
    for gamma in &perms {
        let val_h = evaluate_g_h(h, gamma);
        let val_h_star = evaluate_g_h(&h_star, gamma);
        let product = val_h.mul(&val_h_star);
        if !product.is_zero() {
            failures += 1;
        }
    }
    failures
}

pub fn verify_conjecture2_single(matrix_id: &str, h: &[[Cyc24; 6]; 6]) -> Conj2SingleResult {
    let g1_failures = verify_gamma1(h);
    let g2_failures = verify_gamma2_product(h);

    Conj2SingleResult {
        matrix_id: matrix_id.to_string(),
        gamma1_all_zero: g1_failures == 0,
        gamma1_failures: g1_failures,
        gamma2_product_all_zero: g2_failures == 0,
        gamma2_failures: g2_failures,
        conjecture_2_holds: g1_failures == 0 && g2_failures == 0,
    }
}

pub fn adjoint_matrix(h: &[[Cyc24; 6]; 6]) -> [[Cyc24; 6]; 6] {
    std::array::from_fn(|i| std::array::from_fn(|j| h[j][i].conj()))
}

pub fn make_displayed_karlsson_ansatz(x: &Cyc24, y: &Cyc24) -> [[Cyc24; 6]; 6] {
    let one = Cyc24::one();
    let neg_one = one.neg();
    let omega = Cyc24::zeta24(8);
    let omega2 = Cyc24::zeta24(16);

    let ox = omega.mul(x);
    let o2x = omega2.mul(x);
    let oy = omega.mul(y);
    let o2y = omega2.mul(y);

    [
        [one.clone(), one.clone(), one.clone(), one.clone(), one.clone(), one.clone()],
        [one.clone(), neg_one.clone(), x.clone(), x.neg(), y.clone(), y.neg()],
        [one.clone(), one.clone(), omega.clone(), omega.clone(), omega2.clone(), omega2.clone()],
        [one.clone(), neg_one.clone(), ox.clone(), ox.neg(), o2y.clone(), o2y.neg()],
        [one.clone(), one.clone(), omega2.clone(), omega2.clone(), omega.clone(), omega],
        [one, neg_one, o2x.clone(), o2x.neg(), oy.clone(), oy.neg()],
    ]
}

pub fn count_rows_with_minus_one(h: &[[Cyc24; 6]; 6]) -> usize {
    let neg_one = Cyc24::one().neg();
    let mut count = 0;
    for row in h {
        if row.iter().any(|entry| entry == &neg_one) {
            count += 1;
        }
    }
    count
}

#[cfg(test)]
mod tests {
    use super::*;
    use crate::omega_native::campaign::mub6_dita_seed_cover::{
        all_genuine_dita_seeds, dita_seed_triple_columns_qa,
    };
    use crate::omega_native::exact::d6_exact_curvature_cochain::canonical_triple_exact;

    #[test]
    fn gamma1_has_20_permutations() {
        let perms = gamma1_permutations();
        assert_eq!(perms.len(), 20, "C(6,3) = 20");
    }

    #[test]
    fn gamma2_has_20_permutations() {
        let perms = gamma2_permutations();
        assert_eq!(perms.len(), 20, "C(6,3) = 20");
    }

    #[test]
    fn g_h_on_fourier_f6_gamma1_vanishes() {
        let mut f6: [[Cyc24; 6]; 6] =
            std::array::from_fn(|_| std::array::from_fn(|_| Cyc24::zero()));
        for j in 0..6 {
            for k in 0..6 {
                let pow = (j * k) as i32;
                f6[k][j] = Cyc24::zeta24(4 * pow);
            }
        }

        let g1_failures = verify_gamma1(&f6);
        assert_eq!(g1_failures, 0, "F6 must satisfy the gamma1 identity");
    }

    #[test]
    fn g_h_on_tao_s6_gamma1() {
        let w = Cyc24::zeta24(8);
        let w2 = w.mul(&w);
        let one = Cyc24::one();

        let s6 = [
            [
                one.clone(),
                one.clone(),
                one.clone(),
                one.clone(),
                one.clone(),
                one.clone(),
            ],
            [
                one.clone(),
                one.clone(),
                w.clone(),
                w.clone(),
                w2.clone(),
                w2.clone(),
            ],
            [
                one.clone(),
                w.clone(),
                one.clone(),
                w2.clone(),
                w2.clone(),
                w.clone(),
            ],
            [
                one.clone(),
                w.clone(),
                w2.clone(),
                one.clone(),
                w.clone(),
                w2.clone(),
            ],
            [
                one.clone(),
                w2.clone(),
                w2.clone(),
                w.clone(),
                one.clone(),
                w.clone(),
            ],
            [
                one.clone(),
                w2.clone(),
                w.clone(),
                w2.clone(),
                w.clone(),
                one.clone(),
            ],
        ];

        let g1_failures = verify_gamma1(&s6);
        assert_eq!(
            g1_failures, 20,
            "the isolated Tao S6 control must remain discriminating"
        );
    }

    #[test]
    fn adjoint_transposes_before_conjugating() {
        let h: [[Cyc24; 6]; 6] = std::array::from_fn(|row| {
            std::array::from_fn(|col| Cyc24::zeta24((row * 6 + col) as i32))
        });

        let h_star = adjoint_matrix(&h);

        assert_eq!(h_star[1][2], h[2][1].conj());
        assert_ne!(
            h_star[1][2],
            h[1][2].conj(),
            "H* must not collapse to entry-wise conjugation on a nonsymmetric matrix"
        );
    }

    #[test]
    fn conj2_catalog_discriminant_survey() {
        use crate::omega_native::exact::mub6_orbit_exhaustiveness::canonical_catalog_candidates;

        let candidates = canonical_catalog_candidates();
        eprintln!(
            "\n=== Conjecture 2 Discriminant Survey: {} catalog candidates ===",
            candidates.len()
        );
        eprintln!(
            "{:<45} {:>5} {:>5} {:>6}",
            "Candidate", "g1_f", "g2_f", "holds?"
        );
        eprintln!("{}", "-".repeat(65));

        let mut fourier_pass = 0usize;
        let mut fourier_total = 0usize;
        let mut non_fourier_pass = 0usize;
        let mut non_fourier_total = 0usize;

        for c in &candidates {
            let g1 = verify_gamma1(&c.matrix);
            let g2 = verify_gamma2_product(&c.matrix);
            let holds = g1 == 0 && g2 == 0;
            let class_name = format!("{:?}", c.expected_class);
            let is_fourier = class_name.contains("Fourier");

            eprintln!(
                "{:<45} {:>5} {:>5} {:>6}",
                c.name,
                g1,
                g2,
                if holds { "YES" } else { "NO" }
            );

            if is_fourier {
                fourier_total += 1;
                if holds {
                    fourier_pass += 1;
                }
            } else {
                non_fourier_total += 1;
                if holds {
                    non_fourier_pass += 1;
                }
            }
        }

        eprintln!("\nSummary:");
        eprintln!("  Fourier-class:     {fourier_pass}/{fourier_total} pass Conj2 individually");
        eprintln!(
            "  Non-Fourier-class: {non_fourier_pass}/{non_fourier_total} pass Conj2 individually"
        );
        eprintln!("  NOTE: Conj2 is about TRANSITION MATRICES in triples,");
        eprintln!("  not individual CHMs. Failures on individual CHMs are expected.");

        assert_eq!(fourier_pass, fourier_total);
        assert_eq!(non_fourier_pass + 1, non_fourier_total);
    }

    #[test]
    fn two_circulant_family_parity_cancellation_survey() {
        use crate::omega_native::exact::mub6_orbit_exhaustiveness::circ3;

        let make_2circulant = |b: &Cyc24, c: &Cyc24, e: &Cyc24, f: &Cyc24| -> [[Cyc24; 6]; 6] {
            let one = Cyc24::one();
            let a = circ3(&one, b, c);
            let b_mat = circ3(&one, e, f);
            let mut h = std::array::from_fn(|_| std::array::from_fn(|_| Cyc24::zero()));
            for i in 0..3 {
                for j in 0..3 {
                    h[i][j] = a[i][j].clone();
                    h[i][j + 3] = b_mat[i][j].clone();
                    h[i + 3][j] = b_mat[j][i].conj();
                    h[i + 3][j + 3] = a[j][i].conj().neg();
                }
            }
            h
        };

        let test_exponents = [
            (2, 5, 7, 11),
            (1, 4, 10, 19),
            (3, 9, 15, 21),
            (0, 8, 16, 4),
            (6, 12, 18, 0),
        ];

        let perms2 = gamma2_permutations();

        for (kb, kc, ke, kf) in test_exponents {
            let b = Cyc24::zeta24(kb);
            let c = Cyc24::zeta24(kc);
            let e = Cyc24::zeta24(ke);
            let f = Cyc24::zeta24(kf);

            let h = make_2circulant(&b, &c, &e, &f);
            let h_star = adjoint_matrix(&h);

            let g1_fail_h = verify_gamma1(&h);
            assert_eq!(
                g1_fail_h, 0,
                "Clause (a) G_H(gamma1) must vanish for 2-circulant ({kb},{kc},{ke},{kf})"
            );

            let g1_fail_h_star = verify_gamma1(&h_star);
            assert_eq!(
                g1_fail_h_star, 0,
                "Clause (a) G_H*(gamma1) must vanish for 2-circulant ({kb},{kc},{ke},{kf})"
            );

            let g2_fail_prod = verify_gamma2_product(&h);
            assert_eq!(
                g2_fail_prod, 0,
                "Clause (b) G_H(gamma2) * G_H*(gamma2) must vanish for 2-circulant ({kb},{kc},{ke},{kf})"
            );

            for gamma in &perms2 {
                let v_h = evaluate_g_h(&h, gamma);
                let v_h_star = evaluate_g_h(&h_star, gamma);
                assert!(
                    v_h.is_zero(),
                    "G_H(gamma2) factor must vanish individually for ({kb},{kc},{ke},{kf})"
                );
                assert!(
                    v_h_star.is_zero(),
                    "G_H*(gamma2) factor must vanish individually for ({kb},{kc},{ke},{kf})"
                );
            }
        }
    }

    #[test]
    fn karlsson_two_phase_affine_ansatz_parity_cancellation_survey() {
        let test_exponents = [
            (1, 5),
            (2, 7),
            (3, 11),
            (4, 13),
            (6, 18),
            (0, 8),
            (9, 15),
            (10, 22),
        ];

        let perms2 = gamma2_permutations();

        for (kx, ky) in test_exponents {
            let x = Cyc24::zeta24(kx);
            let y = Cyc24::zeta24(ky);
            let k_mat = make_displayed_karlsson_ansatz(&x, &y);
            let k_star = adjoint_matrix(&k_mat);

            let g1_fail = verify_gamma1(&k_mat);
            assert_eq!(
                g1_fail, 0,
                "Clause (a) G_H(gamma1) must vanish for Karlsson ({kx}, {ky})"
            );

            let g1_fail_star = verify_gamma1(&k_star);
            assert_eq!(
                g1_fail_star, 0,
                "Clause (a) G_H*(gamma1) must vanish for Karlsson* ({kx}, {ky})"
            );

            let g2_fail_prod = verify_gamma2_product(&k_mat);
            assert_eq!(
                g2_fail_prod, 0,
                "Clause (b) G_H(gamma2) * G_H*(gamma2) must vanish for Karlsson ({kx}, {ky})"
            );

            for gamma in &perms2 {
                let v_h = evaluate_g_h(&k_mat, gamma);
                let v_h_star = evaluate_g_h(&k_star, gamma);
                assert!(
                    v_h.is_zero(),
                    "G_H(gamma2) factor vanishes by column pair cancellation for Karlsson ({kx}, {ky})"
                );
                assert!(
                    v_h.mul(&v_h_star).is_zero(),
                    "Conjecture 2(b) product G_H(gamma2) * G_H*(gamma2) must vanish for Karlsson ({kx}, {ky})"
                );
            }
        }
    }

    #[test]
    fn karlsson_broken_pair_discriminant_negative_control() {
        let x = Cyc24::zeta24(2);
        let y = Cyc24::zeta24(5);
        let mut broken = make_displayed_karlsson_ansatz(&x, &y);
        broken[1][1] = Cyc24::one();

        let g1_failures = verify_gamma1(&broken);
        assert!(
            g1_failures > 0,
            "Broken pairwise column sign symmetry must fail gamma1 verification"
        );
    }

    #[test]
    fn odd_parity_sign_vector_invariants_exact() {
        let perms1 = gamma1_permutations();
        assert_eq!(perms1.len(), 20);
        for p in &perms1 {
            let alpha1: i64 = p[0] + p[1] + p[2];
            let beta1: i64 = p[3] + p[4] + p[5];
            assert_eq!(alpha1 + beta1, 0);
            assert!(
                alpha1 % 2 != 0,
                "alpha1 must be strictly odd: {alpha1}"
            );
            assert!(
                alpha1 == -3 || alpha1 == -1 || alpha1 == 1 || alpha1 == 3,
                "alpha1 must be in {{-3, -1, 1, 3}}: {alpha1}"
            );
        }

        let perms2 = gamma2_permutations();
        assert_eq!(perms2.len(), 20);
        for p in &perms2 {
            let alpha2: i64 = p[0] + p[1] + p[2];
            let beta2: i64 = p[3] + p[4] + p[5];
            assert_eq!(alpha2 + beta2, 0);
            assert!(
                alpha2 % 2 != 0,
                "alpha2 must be strictly odd: {alpha2}"
            );
            assert!(
                alpha2 == -9 || alpha2 == -3 || alpha2 == 3 || alpha2 == 9,
                "alpha2 must be in {{-9, -3, 3, 9}}: {alpha2}"
            );
        }
    }

    #[test]
    fn conjecture2_forces_three_minus_one_rows_algebraic_test() {
        use crate::omega_native::exact::mub6_orbit_exhaustiveness::canonical_catalog_candidates;

        let mut f6: [[Cyc24; 6]; 6] =
            std::array::from_fn(|_| std::array::from_fn(|_| Cyc24::zero()));
        for j in 0..6 {
            for k in 0..6 {
                let pow = (j * k) as i32;
                f6[k][j] = Cyc24::zeta24(4 * pow);
            }
        }
        let f6_count = count_rows_with_minus_one(&f6);
        assert!(f6_count >= 3, "F6 must contain >= 3 rows with -1, got {f6_count}");

        let x = Cyc24::zeta24(1);
        let y = Cyc24::zeta24(5);
        let k_mat = make_displayed_karlsson_ansatz(&x, &y);
        let k_count = count_rows_with_minus_one(&k_mat);
        assert!(k_count >= 3, "Karlsson ansatz must contain >= 3 rows with -1, got {k_count}");

        let candidates = canonical_catalog_candidates();
        for c in &candidates {
            let g1 = verify_gamma1(&c.matrix);
            let g2 = verify_gamma2_product(&c.matrix);
            let conj2_holds = g1 == 0 && g2 == 0;
            let minus_one_rows = count_rows_with_minus_one(&c.matrix);

            if conj2_holds {
                assert!(
                    minus_one_rows >= 3,
                    "Candidate {} satisfies Conj2 but has fewer than 3 rows of -1 ({minus_one_rows})",
                    c.name
                );
            }
        }
    }

    #[test]
    fn actual_mu_triples_satisfy_conjecture2_laurent_conditions() {
        let t0_cols = canonical_triple_exact();
        assert_eq!(t0_cols.len(), 18);
        assert!(
            is_mutually_unbiased_triple_exact(&t0_cols),
            "T0 must be certified as an actual MU triple"
        );
        let res_t0 = verify_mub_triple_conjecture2("T0_canonical", &t0_cols);
        assert!(
            res_t0.is_verified_mu_triple,
            "T0 must be certified as an actual MU triple"
        );
        assert!(
            res_t0.conjecture_2_holds_on_triple,
            "Conjecture 2 must hold on all transition matrices of T0"
        );
        assert!(res_t0.h12_result.conjecture_2_holds);
        assert!(res_t0.h23_result.conjecture_2_holds);
        assert!(res_t0.h31_result.conjecture_2_holds);

        let seeds = all_genuine_dita_seeds();
        assert_eq!(seeds.len(), 6, "must test all 6 genuine Dita seeds");
        for &(dx, dy, qa) in &seeds {
            let cols = dita_seed_triple_columns_qa(dx, dy, qa);
            assert_eq!(cols.len(), 18);
            assert!(
                is_mutually_unbiased_triple_exact(&cols),
                "seed F6({dx},{dy})+Y2Q{qa} must be certified as an actual MU triple"
            );
            let res = verify_mub_triple_conjecture2(&format!("Dita_F6_{dx}_{dy}_Y2Q{qa}"), &cols);
            assert!(
                res.is_verified_mu_triple,
                "seed F6({dx},{dy})+Y2Q{qa} must be verified as an actual MU triple"
            );
            assert!(
                res.conjecture_2_holds_on_triple,
                "Conjecture 2 must hold on seed F6({dx},{dy})+Y2Q{qa}"
            );
            assert!(res.h12_result.conjecture_2_holds);
            assert!(res.h23_result.conjecture_2_holds);
            assert!(res.h31_result.conjecture_2_holds);
        }
    }
}


