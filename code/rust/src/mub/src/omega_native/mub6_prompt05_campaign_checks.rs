
use crate::omega_native::campaign::mub6_balanced_table_replay::{
    self as table_replay, exact_conj_transpose_mul, imag_part, real_part, BalancedReplayError,
    BalancedTable, ExactMatrix, Monomial, PointEvaluation, TableInventory,
};
use linear_algebra::backend::basic_matrix::BasicMatrix;
use linear_algebra::exact_field::elimination;
use linear_algebra::linear_algebra::rank::compute_exact_rank;
use num_rational::{BigRational, Rational64};
use num_traits::{One, Zero};
use omega_number_theory::cyclotomic::Cyc24;
use serde::Serialize;
use std::collections::btree_map::Entry;
use std::collections::{BTreeMap, BTreeSet};
use thiserror::Error;

pub const RECEIPT_SCHEMA: &str = "omega.mub6.prompt05_campaign_checks.v1";
pub const FIREWALL_LINE: &str =
    "NOT MUB(6)=3, NOT MUB(6)<=3; stated region only; mints no authority";

#[derive(Debug, Error)]
pub enum CampaignCheckError {
    #[error(transparent)]
    Table(#[from] BalancedReplayError),
    #[error("exact rank: {0}")]
    Rank(String),
}

fn q(n: i64, d: i64) -> BigRational {
    BigRational::new(n.into(), d.into())
}

fn canonical(value: &Cyc24) -> String {
    match value.as_rational() {
        Some(r) => format!("{}/{}", r.numer(), r.denom()),
        None => "irrational".to_string(),
    }
}

fn modulus_squared(z: &Cyc24) -> Cyc24 {
    z.mul(&z.conj())
}

fn identity(n: usize) -> ExactMatrix {
    (0..n)
        .map(|i| {
            (0..n)
                .map(|j| if i == j { Cyc24::one() } else { Cyc24::zero() })
                .collect()
        })
        .collect()
}

pub fn fourier2() -> ExactMatrix {
    vec![
        vec![Cyc24::one(), Cyc24::one()],
        vec![Cyc24::one(), Cyc24::from_int(-1)],
    ]
}

pub fn fourier3() -> ExactMatrix {
    (0..3)
        .map(|j| (0..3).map(|k| Cyc24::zeta3_pow(j * k)).collect())
        .collect()
}

pub fn diagonal_times(d: &[Cyc24], m: &ExactMatrix) -> ExactMatrix {
    m.iter()
        .zip(d)
        .map(|(row, s)| row.iter().map(|x| s.mul(x)).collect())
        .collect()
}

pub fn kronecker(x: &ExactMatrix, y: &ExactMatrix) -> ExactMatrix {
    let (n, m) = (x.len(), y.len());
    let mut out = vec![vec![Cyc24::zero(); n * m]; n * m];
    for a in 0..n {
        for b in 0..m {
            for c in 0..n {
                for d in 0..m {
                    out[m * a + b][m * c + d] = x[a][c].mul(&y[b][d]);
                }
            }
        }
    }
    out
}

pub fn product_triple() -> (ExactMatrix, ExactMatrix) {
    let w = Cyc24::zeta3();
    let d2 = [Cyc24::one(), Cyc24::i()];
    let d3 = [Cyc24::one(), w.clone(), w];
    let h = kronecker(&fourier2(), &fourier3());
    let u = kronecker(
        &diagonal_times(&d2, &fourier2()),
        &diagonal_times(&d3, &fourier3()),
    );
    (h, u)
}

fn overlap_values(x: &ExactMatrix, y: &ExactMatrix, scale: BigRational) -> BTreeSet<String> {
    exact_conj_transpose_mul(x, y)
        .iter()
        .flatten()
        .map(|z| canonical(&modulus_squared(z).scale_rat(&scale)))
        .collect()
}

#[derive(Debug, Clone, PartialEq, Eq, Serialize)]
pub struct ProductTripleCheck {
    pub entries_unimodular: bool,
    pub entries_in_q_zeta12: bool,
    pub gram_equals_six_identity: bool,
    pub gauge_first_rows_and_column_one: bool,
    pub normalized_cross_overlaps: BTreeSet<String>,
    pub normalized_identity_overlaps: BTreeSet<String>,
}

pub fn check_product_triple() -> ProductTripleCheck {
    let (h, u) = product_triple();
    let all = |m: &ExactMatrix, f: &dyn Fn(&Cyc24) -> bool| m.iter().flatten().all(f);
    let unimodular = |z: &Cyc24| modulus_squared(z) == Cyc24::one();
    let in_q_zeta12 = |z: &Cyc24| z.a.iter().skip(1).step_by(2).all(|c| c.is_zero());
    let six_identity = identity(6)
        .into_iter()
        .map(|row| row.into_iter().map(|z| z.scale_rat(&q(6, 1))).collect())
        .collect::<ExactMatrix>();
    let gauge = (0..6).all(|j| h[0][j] == Cyc24::one() && u[0][j] == Cyc24::one())
        && (0..6).all(|i| h[i][0] == Cyc24::one());
    let mut identity_overlaps = overlap_values(&identity(6), &h, q(1, 6));
    identity_overlaps.extend(overlap_values(&identity(6), &u, q(1, 6)));
    ProductTripleCheck {
        entries_unimodular: all(&h, &unimodular) && all(&u, &unimodular),
        entries_in_q_zeta12: all(&h, &in_q_zeta12) && all(&u, &in_q_zeta12),
        gram_equals_six_identity: exact_conj_transpose_mul(&h, &h) == six_identity
            && exact_conj_transpose_mul(&u, &u) == six_identity,
        gauge_first_rows_and_column_one: gauge,
        normalized_cross_overlaps: overlap_values(&h, &u, q(1, 36)),
        normalized_identity_overlaps: identity_overlaps,
    }
}

#[derive(Debug, Clone, PartialEq, Eq, Serialize)]
pub struct DecoyCheck {
    pub qubit_sigma_z: BTreeSet<String>,
    pub qutrit_diag_one_w_w2: BTreeSet<String>,
    pub six_dim_sigma_z_seed: BTreeSet<String>,
}

pub fn check_decoys() -> DecoyCheck {
    let w = Cyc24::zeta3();
    let sigma_z = [Cyc24::one(), Cyc24::from_int(-1)];
    let d3 = [Cyc24::one(), w.clone(), w.clone()];
    let d3_squared = [Cyc24::one(), w.clone(), w.mul(&w)];
    let seed = kronecker(
        &diagonal_times(&sigma_z, &fourier2()),
        &diagonal_times(&d3, &fourier3()),
    );
    DecoyCheck {
        qubit_sigma_z: overlap_values(&fourier2(), &diagonal_times(&sigma_z, &fourier2()), q(1, 4)),
        qutrit_diag_one_w_w2: overlap_values(
            &fourier3(),
            &diagonal_times(&d3_squared, &fourier3()),
            q(1, 9),
        ),
        six_dim_sigma_z_seed: overlap_values(&kronecker(&fourier2(), &fourier3()), &seed, q(1, 36)),
    }
}

#[derive(Debug, Clone, PartialEq, Eq, Serialize)]
pub struct GramSpectrumCheck {
    pub size: usize,
    pub rank_g: usize,
    pub rank_g_minus_identity: usize,
    pub rank_g_minus_four_identity: usize,
    pub multiplicity_zero: usize,
    pub multiplicity_one: usize,
    pub multiplicity_four: usize,
}

pub fn check_gram_spectrum() -> Result<GramSpectrumCheck, CampaignCheckError> {
    let n = 24;
    let entry = |r: usize, c: usize, shift: i64| -> Rational64 {
        let (a, i, b, j) = (r / 6, r % 6, c / 6, c % 6);
        let mut value = if a == b {
            Rational64::from_integer(i64::from(i == j))
        } else {
            Rational64::new(1, 6)
        };
        if r == c {
            value -= Rational64::from_integer(shift);
        }
        value
    };
    let rank_of = |shift: i64| -> Result<usize, CampaignCheckError> {
        let data: Vec<Rational64> = (0..n * n).map(|k| entry(k / n, k % n, shift)).collect();
        let matrix = BasicMatrix::from_row_major(n, n, data)
            .map_err(|e| CampaignCheckError::Rank(format!("{e:?}")))?;
        compute_exact_rank(&matrix).map_err(|e| CampaignCheckError::Rank(format!("{e:?}")))
    };
    let (r0, r1, r4) = (rank_of(0)?, rank_of(1)?, rank_of(4)?);
    Ok(GramSpectrumCheck {
        size: n,
        rank_g: r0,
        rank_g_minus_identity: r1,
        rank_g_minus_four_identity: r4,
        multiplicity_zero: n - r0,
        multiplicity_one: n - r1,
        multiplicity_four: n - r4,
    })
}

type CycPoly = BTreeMap<Monomial, Cyc24>;

fn cyc_accumulate(acc: &mut CycPoly, monomial: Monomial, coefficient: Cyc24) {
    if coefficient.is_zero() {
        return;
    }
    match acc.entry(monomial) {
        Entry::Vacant(slot) => {
            slot.insert(coefficient);
        }
        Entry::Occupied(mut slot) => {
            let sum = slot.get().add(&coefficient);
            if sum.is_zero() {
                slot.remove();
            } else {
                *slot.get_mut() = sum;
            }
        }
    }
}

fn cyc_add(p: &CycPoly, r: &CycPoly, sign: i64) -> CycPoly {
    let mut out = p.clone();
    for (m, c) in r {
        cyc_accumulate(&mut out, m.clone(), c.scale_rat(&q(sign, 1)));
    }
    out
}

fn cyc_mul(p: &CycPoly, r: &CycPoly) -> CycPoly {
    let mut out = CycPoly::new();
    for (m1, c1) in p {
        for (m2, c2) in r {
            let mut m = m1.clone();
            m.extend_from_slice(m2);
            m.sort_unstable();
            cyc_accumulate(&mut out, m, c1.mul(c2));
        }
    }
    out
}

fn cyc_term(monomial: Monomial, coefficient: Cyc24) -> CycPoly {
    let mut out = CycPoly::new();
    cyc_accumulate(&mut out, monomial, coefficient);
    out
}

pub fn fixed_triple_coordinate(k: usize, j: usize, b: usize) -> usize {
    12 * k + 2 * j + b
}

pub fn fixed_triple_system() -> Vec<CycPoly> {
    let (h, u) = product_triple();
    let inv_sqrt6 = Cyc24::sqrt2().mul(&Cyc24::sqrt3()).scale_rat(&q(1, 6));
    let scale = |m: &ExactMatrix| -> ExactMatrix {
        m.iter()
            .map(|row| row.iter().map(|z| z.mul(&inv_sqrt6)).collect())
            .collect()
    };
    let triple = [identity(6), scale(&h), scale(&u)];
    let x = |k, j, b| cyc_term(vec![fixed_triple_coordinate(k, j, b)], Cyc24::one());
    let mut system = Vec::with_capacity(180);
    for t in &triple {
        for i in 0..6 {
            for j in 0..6 {
                let mut re = CycPoly::new();
                let mut im = CycPoly::new();
                for (k, row) in t.iter().enumerate() {
                    let (tr, ti) = (real_part(&row[i]), imag_part(&row[i]));
                    re = cyc_add(&re, &cyc_mul(&cyc_term(vec![], tr.clone()), &x(k, j, 0)), 1);
                    re = cyc_add(&re, &cyc_mul(&cyc_term(vec![], ti.clone()), &x(k, j, 1)), 1);
                    im = cyc_add(&im, &cyc_mul(&cyc_term(vec![], tr), &x(k, j, 1)), 1);
                    im = cyc_add(&im, &cyc_mul(&cyc_term(vec![], ti), &x(k, j, 0)), -1);
                }
                let squared = cyc_add(&cyc_mul(&re, &re), &cyc_mul(&im, &im), 1);
                system.push(cyc_add(&squared, &cyc_term(vec![], Cyc24::rat(q(1, 6))), -1));
            }
        }
    }
    for i in 0..6 {
        for j in 0..6 {
            let mut re = cyc_term(vec![], Cyc24::from_int(-i64::from(i == j)));
            let mut im = CycPoly::new();
            for k in 0..6 {
                re = cyc_add(&re, &cyc_mul(&x(k, i, 0), &x(k, j, 0)), 1);
                re = cyc_add(&re, &cyc_mul(&x(k, i, 1), &x(k, j, 1)), 1);
                im = cyc_add(&im, &cyc_mul(&x(k, i, 0), &x(k, j, 1)), 1);
                im = cyc_add(&im, &cyc_mul(&x(k, i, 1), &x(k, j, 0)), -1);
            }
            system.push(re);
            system.push(im);
        }
    }
    system
}

pub fn row_unitarity_components() -> Vec<CycPoly> {
    let x = |k, j, b| cyc_term(vec![fixed_triple_coordinate(k, j, b)], Cyc24::one());
    let mut out = Vec::with_capacity(72);
    for i in 0..6 {
        for j in 0..6 {
            let mut re = cyc_term(vec![], Cyc24::from_int(-i64::from(i == j)));
            let mut im = CycPoly::new();
            for k in 0..6 {
                re = cyc_add(&re, &cyc_mul(&x(i, k, 0), &x(j, k, 0)), 1);
                re = cyc_add(&re, &cyc_mul(&x(i, k, 1), &x(j, k, 1)), 1);
                im = cyc_add(&im, &cyc_mul(&x(i, k, 1), &x(j, k, 0)), 1);
                im = cyc_add(&im, &cyc_mul(&x(i, k, 0), &x(j, k, 1)), -1);
            }
            out.push(re);
            out.push(im);
        }
    }
    out
}

#[derive(Debug, Clone, PartialEq, Eq, Serialize)]
pub struct FixedTripleCountCheck {
    pub equations: usize,
    pub coordinates: usize,
    pub overlap_rows: usize,
    pub column_unitarity_rows: usize,
    pub coefficients_real: bool,
    pub hermitian_duplicate_rows: usize,
    pub zero_diagonal_imaginary_rows: usize,
    pub diagonal_real_equal_identity_overlap_sums: usize,
    pub implied_rows: usize,
    pub rows_not_implied_by_these_identities: usize,
    pub row_unitarity_components_listed: usize,
}

pub fn check_fixed_triple_counts() -> FixedTripleCountCheck {
    let system = fixed_triple_system();
    let unitary = |i: usize, j: usize, b: usize| &system[108 + 2 * (6 * i + j) + b];
    let coefficients_real = system.iter().flat_map(|p| p.values()).all(|c| c.conj() == *c);
    let mut hermitian = 0;
    let mut zero_imag = 0;
    let mut diagonal_sums = 0;
    for i in 0..6 {
        for j in 0..6 {
            if i > j {
                if unitary(i, j, 0) == unitary(j, i, 0) {
                    hermitian += 1;
                }
                if *unitary(i, j, 1) == cyc_add(&CycPoly::new(), unitary(j, i, 1), -1) {
                    hermitian += 1;
                }
            }
        }
        if unitary(i, i, 1).is_empty() {
            zero_imag += 1;
        }
        let identity_overlap_sum = (0..6).fold(CycPoly::new(), |acc, k| {
            cyc_add(&acc, &system[6 * k + i], 1)
        });
        if *unitary(i, i, 0) == identity_overlap_sum {
            diagonal_sums += 1;
        }
    }
    let listed = row_unitarity_components()
        .iter()
        .filter(|p| !p.is_empty() && system.contains(p))
        .count();
    let implied = hermitian + zero_imag + diagonal_sums;
    FixedTripleCountCheck {
        equations: system.len(),
        coordinates: 72,
        overlap_rows: 108,
        column_unitarity_rows: system.len() - 108,
        coefficients_real,
        hermitian_duplicate_rows: hermitian,
        zero_diagonal_imaginary_rows: zero_imag,
        diagonal_real_equal_identity_overlap_sums: diagonal_sums,
        implied_rows: implied,
        rows_not_implied_by_these_identities: system.len() - implied,
        row_unitarity_components_listed: listed,
    }
}

pub fn design_moment(monomial: &[usize]) -> BigRational {
    let mut counts: BTreeMap<usize, (u32, u32)> = BTreeMap::new();
    for &v in monomial {
        let slot = counts.entry(v / 2).or_insert((0, 0));
        if v % 2 == 0 {
            slot.0 += 1;
        } else {
            slot.1 += 1;
        }
    }
    let mut moment = BigRational::one();
    for (x, y) in counts.into_values() {
        let e = x + y;
        if (x > 0 && y > 0) || e % 2 == 1 {
            return BigRational::zero();
        }
        let mut factor = q(1, 2);
        for _ in 0..e / 2 {
            factor *= q(1, 6);
        }
        moment *= factor;
    }
    moment
}

fn design_expectation(p: &CycPoly, extra: Option<usize>) -> Cyc24 {
    p.iter().fold(Cyc24::zero(), |acc, (m, c)| {
        let mut monomial = m.clone();
        monomial.extend(extra);
        acc.add(&c.scale_rat(&design_moment(&monomial)))
    })
}

#[derive(Debug, Clone, PartialEq, Eq, Serialize)]
pub struct AffineMultiplierCheck {
    pub equations: usize,
    pub multipliers: usize,
    pub expectations_checked: usize,
    pub nonzero_expectations: usize,
    pub second_moment_of_a_coordinate: String,
    pub support_modulus_squared: String,
    pub degree_two_example_nonzero: bool,
}

pub fn check_affine_multipliers() -> AffineMultiplierCheck {
    let mut equations = fixed_triple_system();
    equations.extend(row_unitarity_components());
    let multipliers: Vec<Option<usize>> =
        std::iter::once(None).chain((0..72).map(Some)).collect();
    let mut nonzero = 0;
    for f in &equations {
        for &m in &multipliers {
            if !design_expectation(f, m).is_zero() {
                nonzero += 1;
            }
        }
    }
    let example = &equations[36];
    let square = cyc_mul(example, example);
    AffineMultiplierCheck {
        equations: equations.len(),
        multipliers: multipliers.len(),
        expectations_checked: equations.len() * multipliers.len(),
        nonzero_expectations: nonzero,
        second_moment_of_a_coordinate: {
            let m = design_moment(&[0, 0]);
            format!("{}/{}", m.numer(), m.denom())
        },
        support_modulus_squared: "1/6".to_string(),
        degree_two_example_nonzero: !design_expectation(&square, None).is_zero(),
    }
}

#[derive(Debug, Clone, PartialEq, Eq, Serialize)]
pub struct CommutativeModelCheck {
    pub outcomes: usize,
    pub projectors: usize,
    pub idempotent_and_orthogonal: bool,
    pub complete: bool,
    pub single_traces: BTreeSet<String>,
    pub pair_traces_across_bases: BTreeSet<String>,
    pub sandwich_violations: usize,
    pub sandwich_cases: usize,
}

pub fn check_commutative_model() -> CommutativeModelCheck {
    let outcomes = 6usize.pow(4);
    let value = |o: usize, a: u32| (o / 6usize.pow(a)) % 6;
    let p = |a: u32, i: usize, o: usize| -> i64 { i64::from(value(o, a) == i) };
    let trace = |f: &dyn Fn(usize) -> i64| -> String {
        let total: i64 = (0..outcomes).map(f).sum();
        let r = q(total, outcomes as i64);
        format!("{}/{}", r.numer(), r.denom())
    };
    let mut idempotent_and_orthogonal = true;
    let mut complete = true;
    let mut single = BTreeSet::new();
    let mut pairs = BTreeSet::new();
    let mut violations = 0;
    let mut cases = 0;
    for a in 0..4u32 {
        for o in 0..outcomes {
            complete &= (0..6).map(|i| p(a, i, o)).sum::<i64>() == 1;
        }
        for i in 0..6 {
            single.insert(trace(&|o| p(a, i, o)));
            for j in 0..6 {
                idempotent_and_orthogonal &= (0..outcomes)
                    .all(|o| p(a, i, o) * p(a, j, o) == if i == j { p(a, i, o) } else { 0 });
            }
            for b in (0..4u32).filter(|&b| b != a) {
                for j in 0..6 {
                    pairs.insert(trace(&|o| p(a, i, o) * p(b, j, o)));
                    cases += 1;
                    let differs = (0..outcomes).any(|o| {
                        q(p(a, i, o) * p(b, j, o) * p(a, i, o), 1) != q(p(a, i, o), 6)
                    });
                    if differs {
                        violations += 1;
                    }
                }
            }
        }
    }
    CommutativeModelCheck {
        outcomes,
        projectors: 24,
        idempotent_and_orthogonal,
        complete,
        single_traces: single,
        pair_traces_across_bases: pairs,
        sandwich_violations: violations,
        sandwich_cases: cases,
    }
}

#[derive(Debug, Clone, PartialEq, Eq, Serialize)]
pub struct GaugeCountCheck {
    pub coordinates: usize,
    pub slot_coordinates: usize,
    pub d_block_coordinates: usize,
    pub core_coordinates: usize,
    pub product_triple_balance: bool,
}

pub fn check_gauge_counts() -> GaugeCountCheck {
    let (h, u) = product_triple();
    let t = exact_conj_transpose_mul(&h, &u);
    let six = Cyc24::from_int(6);
    let rows = (0..6).all(|i| t[i].iter().fold(Cyc24::zero(), |s, z| s.add(z)) == six);
    let columns = (0..6).all(|j| (0..6).fold(Cyc24::zero(), |s, i| s.add(&t[i][j])) == six);
    let core_sum = (0..5)
        .flat_map(|i| (0..5).map(move |j| (i, j)))
        .fold(Cyc24::zero(), |s, (i, j)| s.add(&t[i][j]));
    let corner = core_sum.sub(&Cyc24::from_int(24)) == t[5][5];
    GaugeCountCheck {
        coordinates: table_replay::VARIABLES,
        slot_coordinates: table_replay::D_START,
        d_block_coordinates: table_replay::CORE_START - table_replay::D_START,
        core_coordinates: table_replay::VARIABLES - table_replay::CORE_START,
        product_triple_balance: rows && columns && corner,
    }
}

#[derive(Debug, Clone, PartialEq, Eq, Serialize)]
pub struct NegativeControl {
    pub name: String,
    pub third_basis: String,
    pub evaluation: PointEvaluation,
    pub nonzero_rows_by_block: BTreeMap<&'static str, usize>,
}

pub fn negative_controls(table: &BalancedTable) -> Result<Vec<NegativeControl>, CampaignCheckError> {
    let (h, u) = product_triple();
    let mut out = Vec::new();
    for (name, third, v) in [
        ("B3 := B1", "H", &h),
        ("B3 := B2", "U", &u),
    ] {
        let point = table_replay::encode_triple(&h, &u, v)?;
        let evaluation = table_replay::evaluate_point(table, &point);
        out.push(NegativeControl {
            name: name.to_string(),
            third_basis: third.to_string(),
            nonzero_rows_by_block: table_replay::rows_per_block(&evaluation.nonzero_rows),
            evaluation,
        });
    }
    Ok(out)
}

#[derive(Debug, Clone, PartialEq, Eq, Serialize)]
pub struct CentreJacobianCheck {
    pub rows: usize,
    pub columns: usize,
    pub linear_terms: usize,
    pub linear_terms_by_block: BTreeMap<&'static str, usize>,
    pub rows_with_linear_part: usize,
    pub rank: usize,
    pub jacobian_is_zero: bool,
    pub full_column_rank: bool,
}

pub fn centre_jacobian(table: &BalancedTable) -> Result<CentreJacobianCheck, CampaignCheckError> {
    let columns = table_replay::VARIABLES;
    let mut linear_terms = 0;
    let mut by_block: BTreeMap<&'static str, usize> = BTreeMap::new();
    let mut dense: Vec<BigRational> = Vec::new();
    let mut kept = 0;
    for (code, row) in table.rows.iter().enumerate() {
        let mut line = vec![BigRational::zero(); columns];
        let mut any = false;
        for (monomial, coefficient) in row {
            if monomial.len() != 1 || coefficient.is_zero() {
                continue;
            }
            let column = monomial[0];
            if column >= columns {
                return Err(CampaignCheckError::Rank(format!(
                    "row {code} names coordinate {column} outside {columns}"
                )));
            }
            line[column] += coefficient;
            linear_terms += 1;
            *by_block.entry(table_replay::block_of(code)).or_insert(0) += 1;
            any = true;
        }
        if any {
            dense.extend(line);
            kept += 1;
        }
    }
    let rank = if kept == 0 {
        0
    } else {
        let matrix = BasicMatrix::from_row_major(kept, columns, dense)
            .map_err(|e| CampaignCheckError::Rank(format!("{e:?}")))?;
        elimination::rank(&matrix).map_err(|e| CampaignCheckError::Rank(format!("{e:?}")))?
    };
    Ok(CentreJacobianCheck {
        rows: table.rows.len(),
        columns,
        linear_terms,
        linear_terms_by_block: by_block,
        rows_with_linear_part: kept,
        rank,
        jacobian_is_zero: rank == 0,
        full_column_rank: rank == columns,
    })
}

#[derive(Debug, Clone, PartialEq, Eq, Serialize)]
pub struct CampaignReceipt {
    pub schema: String,
    pub authority_effect: String,
    pub firewall_line: String,
    pub balanced_table: TableInventory,
    pub negative_controls: Vec<NegativeControl>,
    pub jacobian_at_centre: CentreJacobianCheck,
    pub d1_product_triple: ProductTripleCheck,
    pub d2_decoys: DecoyCheck,
    pub d3_gram_spectrum: GramSpectrumCheck,
    pub d9_fixed_triple_counts: FixedTripleCountCheck,
    pub e1_affine_multipliers: AffineMultiplierCheck,
    pub f2_commutative_model: CommutativeModelCheck,
    pub g_gauge_counts: GaugeCountCheck,
}

pub fn run_campaign_checks(table_bytes: &[u8]) -> Result<CampaignReceipt, CampaignCheckError> {
    let table = BalancedTable::from_bytes(table_bytes)?;
    Ok(CampaignReceipt {
        schema: RECEIPT_SCHEMA.to_string(),
        authority_effect: "None".to_string(),
        firewall_line: FIREWALL_LINE.to_string(),
        balanced_table: table_replay::inventory(&table),
        negative_controls: negative_controls(&table)?,
        jacobian_at_centre: centre_jacobian(&table)?,
        d1_product_triple: check_product_triple(),
        d2_decoys: check_decoys(),
        d3_gram_spectrum: check_gram_spectrum()?,
        d9_fixed_triple_counts: check_fixed_triple_counts(),
        e1_affine_multipliers: check_affine_multipliers(),
        f2_commutative_model: check_commutative_model(),
        g_gauge_counts: check_gauge_counts(),
    })
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn design_moments_match_the_circle_up_to_degree_three() {
        assert_eq!(design_moment(&[]), q(1, 1));
        assert_eq!(design_moment(&[0, 0]), q(1, 12));
        assert_eq!(design_moment(&[1, 1]), q(1, 12));
        assert!(design_moment(&[0, 1]).is_zero());
        assert!(design_moment(&[0]).is_zero());
        assert!(design_moment(&[0, 0, 2]).is_zero());
        assert_eq!(design_moment(&[0, 0, 2, 2]), q(1, 144));
    }

    #[test]
    fn a_shifted_residual_has_nonzero_expectation() {
        let mut system = fixed_triple_system();
        let shifted = cyc_add(&system.swap_remove(40), &cyc_term(vec![], Cyc24::one()), 1);
        assert!(!design_expectation(&shifted, None).is_zero());
    }
}
