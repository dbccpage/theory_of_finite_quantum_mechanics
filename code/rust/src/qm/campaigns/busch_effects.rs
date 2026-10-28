use engine_number_theory::cyclotomic_ordered::{
    CyclotomicRealRoot, FieldElementF, FieldElementFPlus,
};
use engine_number_theory::rational::{rq, Rational, Zero};
use engine_quantum_physics::busch_effects::*;
use serde::{Deserialize, Serialize};
pub fn construct_test_density_matrix(
    dim: usize,
    conductor: usize,
    state_kind: &str,
) -> Result<HermitianMatrix, String> {
    HermitianMatrix::zero(dim, conductor)?;
    Ok(match state_kind {
        "maximally_mixed" => {
            let inv_d = rq(1, dim as i64);
            let mut grid = vec![vec![FieldElementF::zero(conductor); dim]; dim];
            for i in 0..dim {
                grid[i][i] = FieldElementF::rational(inv_d.clone(), conductor);
            }
            HermitianMatrix::new(dim, conductor, grid).unwrap()
        }
        "pure_computational" => {
            let mut grid = vec![vec![FieldElementF::zero(conductor); dim]; dim];
            grid[0][0] = FieldElementF::one(conductor);
            HermitianMatrix::new(dim, conductor, grid).unwrap()
        }
        "mixed_cyclotomic" => {
            if dim == 2 {
                let c_factor = rq(1, 8);
                let theta_term = &FieldElementFPlus::theta(conductor) * &c_factor;
                let half = rq(1, 2);
                let grid = vec![
                    vec![
                        FieldElementF::rational(half.clone(), conductor),
                        FieldElementF::new(
                            conductor,
                            theta_term.clone(),
                            FieldElementFPlus::zero(conductor),
                        ),
                    ],
                    vec![
                        FieldElementF::new(
                            conductor,
                            theta_term,
                            FieldElementFPlus::zero(conductor),
                        ),
                        FieldElementF::rational(half, conductor),
                    ],
                ];
                HermitianMatrix::new(dim, conductor, grid).unwrap()
            } else if dim == 3 {
                let c_factor = rq(1, 16);
                let theta_term = &FieldElementFPlus::theta(conductor) * &c_factor;
                let third = rq(1, 3);
                let grid = vec![
                    vec![
                        FieldElementF::rational(third.clone(), conductor),
                        FieldElementF::new(
                            conductor,
                            theta_term.clone(),
                            FieldElementFPlus::zero(conductor),
                        ),
                        FieldElementF::zero(conductor),
                    ],
                    vec![
                        FieldElementF::new(
                            conductor,
                            theta_term,
                            FieldElementFPlus::zero(conductor),
                        ),
                        FieldElementF::rational(third.clone(), conductor),
                        FieldElementF::zero(conductor),
                    ],
                    vec![
                        FieldElementF::zero(conductor),
                        FieldElementF::zero(conductor),
                        FieldElementF::rational(third, conductor),
                    ],
                ];
                HermitianMatrix::new(dim, conductor, grid).unwrap()
            } else {
                return Err(format!("Unsupported dim {dim}"));
            }
        }
        _ => return Err(format!("Unknown state kind: {state_kind}")),
    })
}

#[derive(Clone, Debug, PartialEq, Eq, Serialize, Deserialize)]
pub struct RationalEntry {
    pub numer: String,
    pub denom: String,
}

#[derive(Clone, Debug, PartialEq, Eq, Serialize, Deserialize)]
pub struct CellEntryReport {
    pub real: Vec<RationalEntry>,
    pub imag: Vec<RationalEntry>,
}

#[derive(Clone, Debug, PartialEq, Eq, Serialize, Deserialize)]
pub struct StateRecoveryReport {
    pub dim: usize,
    pub conductor: usize,
    pub state_kind: String,
    pub exact_match: bool,
    pub recovered_trace: String,
    pub is_psd: bool,
    pub entries: Vec<Vec<CellEntryReport>>,
}

pub fn verify_state_recovery(
    dim: usize,
    conductor: usize,
    state_kind: &str,
) -> Result<StateRecoveryReport, String> {
    let rho_target = construct_test_density_matrix(dim, conductor, state_kind)?;
    let mut embedding = CyclotomicRealRoot::new(conductor);
    let frame_func = TraceFrameFunction::new(rho_target.clone());

    let rho_recovered = recover_density_matrix(
        &|e| frame_func.call(e).expect("checked fixed effect carrier"),
        dim,
        conductor,
        &mut embedding,
    )
    .unwrap();

    let diff = rho_recovered.sub(&rho_target).unwrap();
    let is_exact_match =
        diff == HermitianMatrix::zero(dim, conductor).expect("checked fixed effect carrier");
    let is_psd = rho_recovered.is_positive_semidefinite(&mut embedding);

    let mut entries_report = Vec::with_capacity(dim);
    for row in rho_recovered.entries.as_slice().chunks(dim) {
        let mut row_report = Vec::with_capacity(dim);
        for cell in row {
            let re_list: Vec<RationalEntry> = cell
                .real
                .coeffs
                .iter()
                .map(|c| RationalEntry {
                    numer: c.numer().to_string(),
                    denom: c.denom().to_string(),
                })
                .collect();
            let im_list: Vec<RationalEntry> = cell
                .imag
                .coeffs
                .iter()
                .map(|c| RationalEntry {
                    numer: c.numer().to_string(),
                    denom: c.denom().to_string(),
                })
                .collect();
            row_report.push(CellEntryReport {
                real: re_list,
                imag: im_list,
            });
        }
        entries_report.push(row_report);
    }

    Ok(StateRecoveryReport {
        dim,
        conductor,
        state_kind: state_kind.to_string(),
        exact_match: is_exact_match,
        recovered_trace: format!(
            "{:?}",
            rho_recovered
                .trace()
                .expect("checked fixed effect carrier")
                .coeffs
        ),
        is_psd,
        entries: entries_report,
    })
}

pub fn run_all_recovery_combinations() -> Vec<StateRecoveryReport> {
    let conductors = [4, 5, 8, 12, 24];
    let dimensions = [2, 3];
    let kinds = ["maximally_mixed", "pure_computational", "mixed_cyclotomic"];
    let mut results = Vec::with_capacity(30);

    for &cond in &conductors {
        for &dim in &dimensions {
            for &k in &kinds {
                let res = verify_state_recovery(dim, cond, k)
                    .expect("frozen valid state-recovery fixture");
                assert!(
                    res.exact_match,
                    "State recovery failed for exact match: cond={}, dim={}, kind={}",
                    cond, dim, k
                );
                assert!(
                    res.is_psd,
                    "State recovery failed for PSD: cond={}, dim={}, kind={}",
                    cond, dim, k
                );
                results.push(res);
            }
        }
    }
    results
}


#[derive(Clone, Debug, PartialEq, Eq, Serialize, Deserialize)]
pub struct D2CountermodelReport {
    pub conductor: usize,
    pub dim: usize,
    pub e1_in_effects: bool,
    pub e2_in_effects: bool,
    pub sum_in_effects: bool,
    pub w_e1: String,
    pub w_e2: String,
    pub sum_of_valuations: String,
    pub additivity_fails_on_effects: bool,
}

pub fn d2_projective_countermodel_evaluation(conductor: usize) -> D2CountermodelReport {
    let mut embedding = CyclotomicRealRoot::new(conductor);
    let p0 = HermitianMatrix::new(
        2,
        conductor,
        vec![
            vec![
                FieldElementF::one(conductor),
                FieldElementF::zero(conductor),
            ],
            vec![
                FieldElementF::zero(conductor),
                FieldElementF::zero(conductor),
            ],
        ],
    )
    .unwrap();

    let half = rq(1, 2);
    let p1 = HermitianMatrix::new(
        2,
        conductor,
        vec![
            vec![
                FieldElementF::rational(half.clone(), conductor),
                FieldElementF::rational(half.clone(), conductor),
            ],
            vec![
                FieldElementF::rational(half.clone(), conductor),
                FieldElementF::rational(half.clone(), conductor),
            ],
        ],
    )
    .unwrap();

    let e1 = p0
        .scalar_mul_rational(&half)
        .expect("checked fixed effect carrier");
    let e2 = p1
        .scalar_mul_rational(&half)
        .expect("checked fixed effect carrier");
    let e_sum = e1.add(&e2).unwrap();

    let e1_valid = e1.is_effect(&mut embedding);
    let e2_valid = e2.is_effect(&mut embedding);
    let sum_valid = e_sum.is_effect(&mut embedding);

    let cubic_extension = |e: &HermitianMatrix| {
        let t = e
            .trace()
            .expect("checked fixed effect carrier")
            .as_cyclotomic()
            .expect("fixed CM field")
            .as_rational()
            .expect("rational countermodel");
        if t.is_zero() {
            return Rational::zero();
        }
        let z = (&e.entries.get(0, 0).expect("fixed qubit carrier").real
            - &e.entries.get(1, 1).expect("fixed qubit carrier").real)
            .as_cyclotomic()
            .expect("fixed CM field")
            .as_rational()
            .expect("rational diagonal");
        &t / rq(2, 1) + &z * &z * &z / (rq(2, 1) * &t * &t)
    };
    let w_e1 = cubic_extension(&e1);
    let w_e2 = cubic_extension(&e2);
    let sum_of_valuations = &w_e1 + &w_e2;
    let at_sum = cubic_extension(&e_sum);

    D2CountermodelReport {
        conductor,
        dim: 2,
        e1_in_effects: e1_valid,
        e2_in_effects: e2_valid,
        sum_in_effects: sum_valid,
        w_e1: format!("{}", w_e1),
        w_e2: format!("{}", w_e2),
        sum_of_valuations: format!("{}", sum_of_valuations),
        additivity_fails_on_effects: e1_valid
            && e2_valid
            && sum_valid
            && at_sum != sum_of_valuations,
    }
}

#[derive(Clone, Debug, PartialEq, Eq, Serialize, Deserialize)]
pub struct GaloisTwistReport {
    pub conductor: usize,
    pub rho_is_valid_density_matrix: bool,
    pub pv_in_effects: bool,
    pub f_sigma_pv_is_negative: bool,
    pub f_sigma_ortho_exceeds_one: bool,
}

pub fn galois_twist_countermodel_evaluation() -> GaloisTwistReport {
    let conductor = 8;
    let mut embedding1 = CyclotomicRealRoot::new(conductor);
    let half = rq(1, 2);

    let off_diag = FieldElementFPlus::from_i64_slice(8, &[-1, 1]);
    let rho = HermitianMatrix::new(
        2,
        conductor,
        vec![
            vec![
                FieldElementF::rational(half.clone(), conductor),
                FieldElementF::new(
                    conductor,
                    off_diag.clone(),
                    FieldElementFPlus::zero(conductor),
                ),
            ],
            vec![
                FieldElementF::new(conductor, off_diag, FieldElementFPlus::zero(conductor)),
                FieldElementF::rational(half.clone(), conductor),
            ],
        ],
    )
    .unwrap();

    let is_valid_state = rho.is_positive_semidefinite(&mut embedding1)
        && (rho.trace().expect("checked fixed effect carrier")
            == FieldElementFPlus::one(conductor));

    let sigma_off_diag = FieldElementFPlus::from_i64_slice(8, &[-1, -1]);
    let sigma_rho = HermitianMatrix::new(
        2,
        conductor,
        vec![
            vec![
                FieldElementF::rational(half.clone(), conductor),
                FieldElementF::new(
                    conductor,
                    sigma_off_diag.clone(),
                    FieldElementFPlus::zero(conductor),
                ),
            ],
            vec![
                FieldElementF::new(
                    conductor,
                    sigma_off_diag,
                    FieldElementFPlus::zero(conductor),
                ),
                FieldElementF::rational(half.clone(), conductor),
            ],
        ],
    )
    .unwrap();

    let pv = HermitianMatrix::new(
        2,
        conductor,
        vec![
            vec![
                FieldElementF::rational(half.clone(), conductor),
                FieldElementF::rational(half.clone(), conductor),
            ],
            vec![
                FieldElementF::rational(half.clone(), conductor),
                FieldElementF::rational(half, conductor),
            ],
        ],
    )
    .unwrap();

    let pv_in_effects = pv.is_effect(&mut embedding1);

    let f_sigma_pv = sigma_rho
        .trace_prod(&pv)
        .expect("checked fixed effect carrier");
    let sign_pv = f_sigma_pv.sign(&mut embedding1);

    let ident = HermitianMatrix::identity(2, conductor).expect("checked fixed effect carrier");
    let pv_ortho = ident.sub(&pv).unwrap();
    let f_sigma_ortho = sigma_rho
        .trace_prod(&pv_ortho)
        .expect("checked fixed effect carrier");
    let one_fplus = FieldElementFPlus::one(conductor);
    let excess = &f_sigma_ortho - &one_fplus;
    let sign_excess = excess.sign(&mut embedding1);

    GaloisTwistReport {
        conductor,
        rho_is_valid_density_matrix: is_valid_state,
        pv_in_effects,
        f_sigma_pv_is_negative: sign_pv < 0,
        f_sigma_ortho_exceeds_one: sign_excess > 0,
    }
}

#[derive(Clone, Debug, PartialEq, Eq, Serialize, Deserialize)]
pub struct BoundedSearchReport {
    pub conductor: usize,
    pub height_bound: i64,
    pub total_candidate_vectors: usize,
    pub distinct_ray_projectors: usize,
    pub orthogonal_basis_pairs: usize,
    pub four_element_povms: usize,
    pub total_povm_resolutions: usize,
    pub termination: bool,
}

fn enumerate_single_elements(conductor: usize, h: i64) -> Vec<FieldElementF> {
    let mut elements = Vec::new();
    for c_re in -h..=h {
        for c_im in -h..=h {
            elements.push(FieldElementF::new(
                conductor,
                FieldElementFPlus::from_i64_slice(conductor, &[c_re]),
                FieldElementFPlus::from_i64_slice(conductor, &[c_im]),
            ));
        }
    }
    elements
}

fn enumerate_candidate_vectors(
    conductor: usize,
    height_bound: i64,
) -> Vec<(FieldElementF, FieldElementF)> {
    let elements = enumerate_single_elements(conductor, height_bound);
    let mut candidates = Vec::new();
    for v1 in &elements {
        for v2 in &elements {
            if !(v1.is_zero() && v2.is_zero()) {
                candidates.push((v1.clone(), v2.clone()));
            }
        }
    }
    candidates
}

fn candidate_to_projector(
    conductor: usize,
    v1: &FieldElementF,
    v2: &FieldElementF,
    embedding: &mut CyclotomicRealRoot,
) -> Option<HermitianMatrix> {
    let norm_sq = &v1.norm() + &v2.norm();
    if norm_sq.sign(embedding) <= 0 {
        return None;
    }
    let inv_norm = norm_sq.inverse();
    let p00 = &v1.norm() * &inv_norm;
    let p11 = &v2.norm() * &inv_norm;
    let p01 = &(v1 * &v2.conjugate()) * &inv_norm;
    let p10 = p01.conjugate();

    Some(
        HermitianMatrix::new(
            2,
            conductor,
            vec![
                vec![
                    FieldElementF::new(conductor, p00, FieldElementFPlus::zero(conductor)),
                    p01,
                ],
                vec![
                    p10,
                    FieldElementF::new(conductor, p11, FieldElementFPlus::zero(conductor)),
                ],
            ],
        )
        .unwrap(),
    )
}

fn build_distinct_ray_projectors(
    conductor: usize,
    candidates: &[(FieldElementF, FieldElementF)],
    embedding: &mut CyclotomicRealRoot,
) -> Vec<HermitianMatrix> {
    let mut projectors: Vec<HermitianMatrix> = Vec::new();
    for (v1, v2) in candidates {
        if let Some(p) = candidate_to_projector(conductor, v1, v2, embedding) {
            if !projectors.contains(&p) {
                projectors.push(p);
            }
        }
    }
    projectors
}

fn find_orthogonal_basis_pairs(
    conductor: usize,
    projectors: &[HermitianMatrix],
) -> Vec<(usize, usize)> {
    let mut orthogonal_pairs = Vec::new();
    let ident = HermitianMatrix::identity(2, conductor).expect("checked fixed effect carrier");
    for i in 0..projectors.len() {
        for j in (i + 1)..projectors.len() {
            if projectors[i].add(&projectors[j]).unwrap() == ident {
                orthogonal_pairs.push((i, j));
            }
        }
    }
    orthogonal_pairs
}

fn is_four_element_povm(
    conductor: usize,
    projectors: &[HermitianMatrix],
    indices: [usize; 4],
    ident: &HermitianMatrix,
    embedding: &mut CyclotomicRealRoot,
) -> bool {
    let half = rq(1, 2);
    let mut sum = HermitianMatrix::zero(2, conductor).expect("checked fixed effect carrier");
    for idx in indices {
        let eff = projectors[idx]
            .scalar_mul_rational(&half)
            .expect("checked fixed effect carrier");
        if !eff.is_effect(embedding) {
            return false;
        }
        sum = sum.add(&eff).expect("compatible fixed POVM effects");
    }
    &sum == ident
}

fn count_four_element_povms(
    conductor: usize,
    projectors: &[HermitianMatrix],
    orthogonal_pairs: &[(usize, usize)],
    embedding: &mut CyclotomicRealRoot,
) -> usize {
    let ident = HermitianMatrix::identity(2, conductor).expect("checked fixed effect carrier");
    let mut four_element_povms = 0;
    for (i, &(a, b)) in orthogonal_pairs.iter().enumerate() {
        for &(c, d) in &orthogonal_pairs[i + 1..] {
            if is_four_element_povm(conductor, projectors, [a, b, c, d], &ident, embedding) {
                four_element_povms += 1;
            }
        }
    }
    four_element_povms
}

pub fn bounded_effect_algebraic_search(
    conductor: usize,
    height_bound: i64,
) -> Result<BoundedSearchReport, String> {
    if ![4, 5, 8].contains(&conductor) || !(1..=2).contains(&height_bound) {
        return Err("declared search budget/conductor refused".into());
    }
    let mut embedding = CyclotomicRealRoot::new(conductor);
    let candidates = enumerate_candidate_vectors(conductor, height_bound);
    let projectors = build_distinct_ray_projectors(conductor, &candidates, &mut embedding);
    let orthogonal_pairs = find_orthogonal_basis_pairs(conductor, &projectors);
    let four_element_povms =
        count_four_element_povms(conductor, &projectors, &orthogonal_pairs, &mut embedding);

    Ok(BoundedSearchReport {
        conductor,
        height_bound,
        total_candidate_vectors: candidates.len(),
        distinct_ray_projectors: projectors.len(),
        orthogonal_basis_pairs: orthogonal_pairs.len(),
        four_element_povms,
        total_povm_resolutions: orthogonal_pairs.len() + four_element_povms,
        termination: candidates.len() == ((2 * height_bound + 1) as usize).pow(4) - 1,
    })
}


#[cfg(test)]
mod tests {
    use super::*;
    use engine_number_theory::rational::{r_zero, ri};

    #[test]
    fn test_hermitian_matrix_algebra_and_minors() {
        for &cond in &[4, 8] {
            let mut emb = CyclotomicRealRoot::new(cond);
            let ident2 = HermitianMatrix::identity(2, cond).expect("checked fixed effect carrier");
            assert_eq!(
                ident2.trace().expect("checked fixed effect carrier"),
                FieldElementFPlus::rational(ri(2), cond)
            );
            assert!(ident2.is_positive_semidefinite(&mut emb));
            assert!(ident2.is_effect(&mut emb));

            let m_neg = HermitianMatrix::new(
                2,
                cond,
                vec![
                    vec![
                        FieldElementF::rational(ri(-1), cond),
                        FieldElementF::zero(cond),
                    ],
                    vec![FieldElementF::zero(cond), FieldElementF::one(cond)],
                ],
            )
            .unwrap();
            assert!(!m_neg.is_positive_semidefinite(&mut emb));
            assert!(!m_neg.is_effect(&mut emb));

            let two_ident = ident2
                .scalar_mul_rational(&ri(2))
                .expect("checked fixed effect carrier");
            assert!(two_ident.is_positive_semidefinite(&mut emb));
            assert!(!two_ident.is_effect(&mut emb));
        }
    }

    #[test]
    fn test_monotonicity_and_rational_homogeneity() {
        let cond = 8;
        let mut emb = CyclotomicRealRoot::new(cond);
        let ident = HermitianMatrix::identity(2, cond).expect("checked fixed effect carrier");
        let half = rq(1, 2);
        let quarter = rq(1, 4);

        let e1 = ident
            .scalar_mul_rational(&quarter)
            .expect("checked fixed effect carrier");
        let e2 = ident
            .scalar_mul_rational(&half)
            .expect("checked fixed effect carrier");

        let rho = HermitianMatrix::new(
            2,
            cond,
            vec![
                vec![FieldElementF::one(cond), FieldElementF::zero(cond)],
                vec![FieldElementF::zero(cond), FieldElementF::zero(cond)],
            ],
        )
        .unwrap();
        let f_struct = TraceFrameFunction::new(rho);
        let f = |e: &HermitianMatrix| f_struct.call(e).expect("checked fixed effect carrier");

        let (delta, is_ordered) = derive_monotonicity(&f, &e1, &e2, &mut emb).unwrap();
        assert!(is_ordered);
        assert!(delta.is_effect(&mut emb));

        for r in &[rq(1, 3), rq(2, 5), rq(1, 1)] {
            assert!(evaluate_rational_homogeneity(&f, &e2, r));
        }
    }

    #[test]
    fn test_density_squeeze() {
        let cond = 5;
        let mut emb = CyclotomicRealRoot::new(cond);
        let ident = HermitianMatrix::identity(2, cond).expect("checked fixed effect carrier");
        let theta = FieldElementFPlus::theta(cond);
        let half = rq(1, 2);
        let lam = &theta * &half;
        assert!(lam.sign(&mut emb) > 0);

        let rho = ident
            .scalar_mul_rational(&half)
            .expect("checked fixed effect carrier");
        let f_struct = TraceFrameFunction::new(rho);
        let f = |e: &HermitianMatrix| f_struct.call(e).expect("checked fixed effect carrier");

        let epsilon = rq(1, 100);
        let (r, s) = density_squeeze(&f, &ident, &lam, &mut emb, &epsilon).unwrap();
        assert!((&s - &r) <= epsilon);
        assert!(r >= r_zero());
        assert!(s <= ri(1));
    }

    #[test]
    fn test_linear_extension_and_density_recovery() {
        let cond = 12;
        let mut emb = CyclotomicRealRoot::new(cond);
        let rho_target = HermitianMatrix::new(
            2,
            cond,
            vec![
                vec![
                    FieldElementF::rational(rq(2, 3), cond),
                    FieldElementF::zero(cond),
                ],
                vec![
                    FieldElementF::zero(cond),
                    FieldElementF::rational(rq(1, 3), cond),
                ],
            ],
        )
        .unwrap();
        let f_struct = TraceFrameFunction::new(rho_target.clone());
        let f = |e: &HermitianMatrix| f_struct.call(e).expect("checked fixed effect carrier");

        let test_a = HermitianMatrix::new(
            2,
            cond,
            vec![
                vec![
                    FieldElementF::rational(ri(3), cond),
                    FieldElementF::rational(ri(1), cond),
                ],
                vec![
                    FieldElementF::rational(ri(1), cond),
                    FieldElementF::rational(ri(2), cond),
                ],
            ],
        )
        .unwrap();
        let ext_val =
            linear_extension(&f, &test_a, &mut emb).expect("checked fixed effect carrier");
        let expected_val = rho_target
            .trace_prod(&test_a)
            .expect("checked fixed effect carrier");
        assert_eq!(ext_val, expected_val);

        let recovered_rho = recover_density_matrix(&f, 2, cond, &mut emb).unwrap();
        assert_eq!(recovered_rho, rho_target);
        assert_eq!(
            recovered_rho.trace().expect("checked fixed effect carrier"),
            FieldElementFPlus::one(cond)
        );
        assert!(recovered_rho.is_positive_semidefinite(&mut emb));
    }

    #[test]
    fn test_state_recovery_all_10_combinations() {
        let results = run_all_recovery_combinations();
        assert_eq!(results.len(), 30);
        for res in results {
            assert!(res.exact_match);
            assert!(res.is_psd);
        }
    }

    #[test]
    fn test_d2_projective_countermodel() {
        let res = d2_projective_countermodel_evaluation(4);
        assert_eq!(res.dim, 2);
        assert!(res.e1_in_effects);
        assert!(res.e2_in_effects);
        assert!(res.sum_in_effects);
        assert!(res.additivity_fails_on_effects);
    }

    #[test]
    fn test_galois_twist_countermodel() {
        let res = galois_twist_countermodel_evaluation();
        assert_eq!(res.conductor, 8);
        assert!(res.rho_is_valid_density_matrix);
        assert!(res.pv_in_effects);
        assert!(res.f_sigma_pv_is_negative);
        assert!(res.f_sigma_ortho_exceeds_one);
    }

    #[test]
    fn test_bounded_algebraic_search() {
        for &cond in &[4, 5, 8] {
            let res = bounded_effect_algebraic_search(cond, 1).unwrap();
            assert!(res.termination);
            assert!(res.total_candidate_vectors > 0);
            assert!(res.distinct_ray_projectors > 0);
            assert!(res.orthogonal_basis_pairs > 0);
            assert!(res.total_povm_resolutions > 0);
        }
    }
}
