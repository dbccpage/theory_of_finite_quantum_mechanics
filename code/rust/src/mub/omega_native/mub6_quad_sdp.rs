
use num_rational::BigRational;
use num_traits::{One, Zero};
use serde::{Deserialize, Serialize};

use crate::omega_native::exact::d6_exact_curvature_cochain::{canonical_triple_exact, inner};
use omega_number_theory::cyclotomic::Cyc24;
use omega_number_theory::rational::ri;

pub use crate::omega_native::exact::mub6_field::{inv_sqrt6, omega3_pow, sqrt6};
pub const DIM_HILBERT: usize = 6;
pub const NUM_BASES: usize = 4;
pub const GRAMIAN_DIM: usize = NUM_BASES * DIM_HILBERT;
pub const TAO_PHASES: [[i64; 6]; 6] = [
    [0, 0, 0, 0, 0, 0],
    [0, 0, 1, 1, 2, 2],
    [0, 1, 0, 2, 2, 1],
    [0, 1, 2, 0, 1, 2],
    [0, 2, 2, 1, 0, 1],
    [0, 2, 1, 2, 1, 0],
];
pub fn tao_s6_block() -> Vec<Vec<Cyc24>> {
    let s = inv_sqrt6();
    let mut mat = vec![vec![Cyc24::zero(); DIM_HILBERT]; DIM_HILBERT];
    for j in 0..DIM_HILBERT {
        for k in 0..DIM_HILBERT {
            mat[j][k] = omega3_pow(TAO_PHASES[j][k]).mul(&s);
        }
    }
    mat
}
pub fn canonical_quad_gramian() -> Vec<Vec<Cyc24>> {
    let cols = canonical_triple_exact();
    let s6 = tao_s6_block();
    let mut g = vec![vec![Cyc24::zero(); GRAMIAN_DIM]; GRAMIAN_DIM];

    for a in 0..3 {
        for b in 0..3 {
            for j in 0..DIM_HILBERT {
                for k in 0..DIM_HILBERT {
                    let u_col = &cols[a * DIM_HILBERT + j];
                    let v_col = &cols[b * DIM_HILBERT + k];
                    g[a * DIM_HILBERT + j][b * DIM_HILBERT + k] = inner(u_col, v_col);
                }
            }
        }
    }

    let one = Cyc24::rat(BigRational::one());
    for j in 0..DIM_HILBERT {
        g[3 * DIM_HILBERT + j][3 * DIM_HILBERT + j] = one.clone();
    }

    for a in 0..3 {
        for j in 0..DIM_HILBERT {
            for k in 0..DIM_HILBERT {
                let entry = s6[j][k].clone();
                g[a * DIM_HILBERT + j][3 * DIM_HILBERT + k] = entry.clone();
                g[3 * DIM_HILBERT + k][a * DIM_HILBERT + j] = entry.conj();
            }
        }
    }

    g
}
pub fn dual_witness_vector() -> Vec<Cyc24> {
    let mut v = vec![Cyc24::zero(); GRAMIAN_DIM];

    let v1_int = [-3i64, 1, -2, -2, 2, 1];
    for (i, &val) in v1_int.iter().enumerate() {
        v[DIM_HILBERT + i] = Cyc24::rat(ri(val));
    }

    let v2_int = [-3i64, 1, 1, -1, 3, 3];
    for (i, &val) in v2_int.iter().enumerate() {
        v[2 * DIM_HILBERT + i] = Cyc24::rat(ri(val));
    }

    let s6 = sqrt6();
    let v3_int = [-1i64, 1, 1, 1, 1, 1];
    for (i, &val) in v3_int.iter().enumerate() {
        v[3 * DIM_HILBERT + i] = s6.mul(&Cyc24::rat(ri(val)));
    }

    v
}
pub fn dual_certificate_matrix(strict: bool) -> Vec<Vec<Cyc24>> {
    let v = dual_witness_vector();
    let mut w = vec![vec![Cyc24::zero(); GRAMIAN_DIM]; GRAMIAN_DIM];

    for i in 0..GRAMIAN_DIM {
        for j in 0..GRAMIAN_DIM {
            w[i][j] = v[i].mul(&v[j].conj());
        }
    }

    if strict {
        let eps = Cyc24::rat(BigRational::new(1.into(), 24.into()));
        for i in 0..GRAMIAN_DIM {
            w[i][i] = w[i][i].add(&eps);
        }
    }

    w
}
pub fn trace_inner_product(w: &[Vec<Cyc24>], g: &[Vec<Cyc24>]) -> Cyc24 {
    let n = w.len();
    let mut acc = Cyc24::zero();
    for i in 0..n {
        for j in 0..n {
            acc = acc.add(&w[i][j].mul(&g[j][i]));
        }
    }
    acc
}

pub fn checked_trace_inner_product(w: &[Vec<Cyc24>], g: &[Vec<Cyc24>]) -> Result<Cyc24, String> {
    let n = w.len();
    if n == 0 || g.len() != n {
        return Err("mismatched or empty matrix dimensions".to_string());
    }
    for row in w {
        if row.len() != n {
            return Err("matrix w is not square".to_string());
        }
    }
    for row in g {
        if row.len() != n {
            return Err("matrix g is not square".to_string());
        }
    }
    Ok(trace_inner_product(w, g))
}
#[derive(Clone, Debug, PartialEq, Eq, Serialize, Deserialize)]
pub struct GramianStructureReport {
    pub diagonal_blocks_identity: bool,
    pub off_diagonal_blocks_modulus_sixth: bool,
    pub hermitian_exact: bool,
    pub verified_sound: bool,
}
pub fn verify_gramian_structure(g: &[Vec<Cyc24>]) -> GramianStructureReport {
    if g.len() != GRAMIAN_DIM || g.iter().any(|row| row.len() != GRAMIAN_DIM) {
        return GramianStructureReport {
            diagonal_blocks_identity: false,
            off_diagonal_blocks_modulus_sixth: false,
            hermitian_exact: false,
            verified_sound: false,
        };
    }
    let sixth = Cyc24::rat(BigRational::new(1.into(), 6.into()));
    let one = Cyc24::rat(BigRational::one());
    let zero = Cyc24::zero();

    let mut diag_ok = true;
    for a in 0..NUM_BASES {
        for i in 0..DIM_HILBERT {
            for j in 0..DIM_HILBERT {
                let idx_i = a * DIM_HILBERT + i;
                let idx_j = a * DIM_HILBERT + j;
                if i == j {
                    if g[idx_i][idx_j] != one {
                        diag_ok = false;
                    }
                } else if g[idx_i][idx_j] != zero {
                    diag_ok = false;
                }
            }
        }
    }

    let mut modulus_ok = true;
    for a in 0..NUM_BASES {
        for b in 0..NUM_BASES {
            if a == b {
                continue;
            }
            for i in 0..DIM_HILBERT {
                for j in 0..DIM_HILBERT {
                    let idx_i = a * DIM_HILBERT + i;
                    let idx_j = b * DIM_HILBERT + j;
                    let entry = &g[idx_i][idx_j];
                    let mod_sq = entry.mul(&entry.conj());
                    if mod_sq != sixth {
                        modulus_ok = false;
                    }
                }
            }
        }
    }

    let mut herm_ok = true;
    for i in 0..GRAMIAN_DIM {
        for j in 0..GRAMIAN_DIM {
            if g[j][i] != g[i][j].conj() {
                herm_ok = false;
            }
        }
    }

    let sound = diag_ok && modulus_ok && herm_ok;
    GramianStructureReport {
        diagonal_blocks_identity: diag_ok,
        off_diagonal_blocks_modulus_sixth: modulus_ok,
        hermitian_exact: herm_ok,
        verified_sound: sound,
    }
}
pub fn ldlt_pivots_rational(m: &[Vec<Cyc24>]) -> Result<Vec<BigRational>, String> {
    let n = m.len();
    if n == 0 || m.iter().any(|row| row.len() != n) {
        return Err("expected a nonempty square matrix".to_string());
    }
    for i in 0..n {
        for j in 0..n {
            if m[i][j] != m[j][i].conj() {
                return Err("matrix is not Hermitian".to_string());
            }
        }
    }
    let mut a: Vec<Vec<Cyc24>> = m.to_vec();
    let mut pivots = Vec::with_capacity(n);

    for k in 0..n {
        let piv_cyc = a[k][k].clone();
        let piv_rat = exact_rational(&piv_cyc)?;
        pivots.push(piv_rat.clone());

        if piv_rat < BigRational::zero() {
            return Err(format!("Negative pivot at step {}: {}", k, piv_rat));
        }

        if piv_rat.is_zero() {
            for i in (k + 1)..n {
                if !a[k][i].is_zero() || !a[i][k].is_zero() {
                    return Err(format!("Indefinite 2x2 minor at step {}", k));
                }
            }
            continue;
        }

        let piv_inv = piv_cyc.inv();
        for i in (k + 1)..n {
            if a[i][k].is_zero() {
                continue;
            }
            let factor = a[i][k].mul(&piv_inv);
            for j in k..n {
                let delta = factor.mul(&a[k][j]);
                a[i][j] = a[i][j].sub(&delta);
            }
        }
    }

    Ok(pivots)
}

#[derive(Clone, Debug, PartialEq, Eq)]
pub struct DualWitnessCyc {
    pub n: usize,
    pub m: usize,
    pub l: Vec<Vec<Cyc24>>,
    pub d_diag: Vec<BigRational>,
}

impl DualWitnessCyc {
    pub fn new(l: Vec<Vec<Cyc24>>, d_diag: Vec<BigRational>) -> Result<Self, String> {
        let n = l.len();
        if n == 0 {
            return Err("L matrix cannot be empty".to_string());
        }
        let m = d_diag.len();
        if l.iter().any(|row| row.len() != m) {
            return Err(format!("L matrix dimensions must be {} x {}", n, m));
        }
        Ok(Self { n, m, l, d_diag })
    }

    pub fn from_cols(cols: Vec<Vec<Cyc24>>, weights: Vec<BigRational>) -> Result<Self, String> {
        let m = cols.len();
        if m == 0 {
            return Err("column list cannot be empty".to_string());
        }
        if weights.len() != m {
            return Err("weights and cols count mismatch".to_string());
        }
        let n = cols[0].len();
        if n == 0 || cols.iter().any(|col| col.len() != n) {
            return Err("columns must have consistent non-zero dimension".to_string());
        }
        let mut l = vec![vec![Cyc24::zero(); m]; n];
        for i in 0..n {
            for k in 0..m {
                l[i][k] = cols[k][i].clone();
            }
        }
        Ok(Self {
            n,
            m,
            l,
            d_diag: weights,
        })
    }

    pub fn is_valid(&self) -> bool {
        self.d_diag.iter().all(|d| d >= &BigRational::zero())
    }

    pub fn validate_psd(&self) -> Result<(), String> {
        for (k, d) in self.d_diag.iter().enumerate() {
            if d < &BigRational::zero() {
                return Err(format!("Negative pivot at step {}: {}", k, d));
            }
        }
        Ok(())
    }

    pub fn to_full_matrix(&self) -> Vec<Vec<Cyc24>> {
        let mut w = vec![vec![Cyc24::zero(); self.n]; self.n];
        for i in 0..self.n {
            for j in 0..self.n {
                let mut s = Cyc24::zero();
                for k in 0..self.m {
                    let d_cyc = Cyc24::rat(self.d_diag[k].clone());
                    let term = self.l[i][k].mul(&d_cyc).mul(&self.l[j][k].conj());
                    s = s.add(&term);
                }
                w[i][j] = s;
            }
        }
        w
    }

    pub fn trace_inner(&self, g: &[Vec<Cyc24>]) -> Result<Cyc24, String> {
        if g.len() != self.n || g.iter().any(|row| row.len() != self.n) {
            return Err(format!(
                "matrix dimensions do not match witness dimension {}",
                self.n
            ));
        }
        let mut total = Cyc24::zero();
        for k in 0..self.m {
            let d_cyc = Cyc24::rat(self.d_diag[k].clone());
            let mut quad = Cyc24::zero();
            for i in 0..self.n {
                for j in 0..self.n {
                    let term = self.l[i][k].conj().mul(&g[i][j]).mul(&self.l[j][k]);
                    quad = quad.add(&term);
                }
            }
            total = total.add(&quad.mul(&d_cyc));
        }
        Ok(total)
    }

    pub fn verify_dual_obstruction(&self, g: &[Vec<Cyc24>]) -> Result<bool, String> {
        self.validate_psd()?;
        let tr = self.trace_inner(g)?;
        let tr_rat = exact_rational(&tr)?;
        Ok(tr_rat < BigRational::zero())
    }
}

pub fn canonical_dual_witness_rank1() -> DualWitnessCyc {
    let v = dual_witness_vector();
    DualWitnessCyc::from_cols(vec![v], vec![BigRational::one()]).expect("valid rank1 witness")
}

pub fn canonical_dual_witness_strict() -> DualWitnessCyc {
    let v = dual_witness_vector();
    let mut cols = Vec::with_capacity(GRAMIAN_DIM + 1);
    let mut weights = Vec::with_capacity(GRAMIAN_DIM + 1);

    cols.push(v);
    weights.push(BigRational::one());

    let reg = BigRational::new(1.into(), 24.into());
    for i in 0..GRAMIAN_DIM {
        let mut e = vec![Cyc24::zero(); GRAMIAN_DIM];
        e[i] = Cyc24::rat(BigRational::one());
        cols.push(e);
        weights.push(reg.clone());
    }

    DualWitnessCyc::from_cols(cols, weights).expect("valid strict witness")
}

pub fn compute_gram_matrix_cyc(vectors: &[Vec<Cyc24>]) -> Result<Vec<Vec<Cyc24>>, String> {
    let n = vectors.len();
    if n == 0 {
        return Err("cannot compute Gram matrix for empty vector set".to_string());
    }
    let d = vectors[0].len();
    if vectors.iter().any(|v| v.len() != d) {
        return Err("all vectors must have consistent dimension".to_string());
    }
    let mut g = vec![vec![Cyc24::zero(); n]; n];
    for i in 0..n {
        for j in 0..n {
            let mut acc = Cyc24::zero();
            for k in 0..d {
                acc = acc.add(&vectors[i][k].conj().mul(&vectors[j][k]));
            }
            g[i][j] = acc;
        }
    }
    Ok(g)
}

pub fn is_psd_cyc(g: &[Vec<Cyc24>]) -> bool {
    match ldlt_pivots_rational(g) {
        Ok(pivots) => pivots.iter().all(|p| p >= &BigRational::zero()),
        Err(_) => false,
    }
}

#[derive(Clone, Debug, PartialEq, Eq, Serialize, Deserialize)]
pub struct MubQuadSdpCertificate {
    pub schema_version: &'static str,
    pub dimension: usize,
    pub bases_count: usize,
    pub gramian_dim: usize,
    pub gramian_structure: GramianStructureReport,
    pub rank1_inner_product: String,
    pub rank1_inner_product_num: String,
    pub rank1_inner_product_den: String,
    pub rank1_strictly_negative: bool,
    pub strict_inner_product: String,
    pub strict_inner_product_num: String,
    pub strict_inner_product_den: String,
    pub strict_strictly_negative: bool,
    pub strict_regularizer: String,
    pub rank1_pivots: Vec<String>,
    pub rank1_pivots_nonnegative: bool,
    pub strict_pivots: Vec<String>,
    pub strict_pivots_strictly_positive: bool,
    pub dual_certificate_psd_certified: bool,
    pub fixed_matrix_witness_checked: bool,
    pub constructed_matrix_not_psd: bool,
    pub complete: bool,
    pub scope: &'static str,
    pub mub_nonexistence_established: bool,
    pub firewall: &'static str,
    pub authority_effect: &'static str,
    pub sha256_digest: Option<String>,
}
pub fn solve_quad_sdp_certificate() -> MubQuadSdpCertificate {
    let g = canonical_quad_gramian();
    let struct_report = verify_gramian_structure(&g);

    let w_rank1 = dual_certificate_matrix(false);
    let w_strict = dual_certificate_matrix(true);

    let inner_rank1 = trace_inner_product(&w_rank1, &g);
    let inner_strict = trace_inner_product(&w_strict, &g);

    let rat_rank1 = exact_rational(&inner_rank1).expect("fixed witness trace must be rational");
    let rat_strict = exact_rational(&inner_strict).expect("fixed witness trace must be rational");

    let rank1_neg = rat_rank1 < BigRational::zero();
    let strict_neg = rat_strict < BigRational::zero();

    let rank1_pivots =
        ldlt_pivots_rational(&w_rank1).expect("LDL^T decomposition failed for W_rank1");
    let rank1_all_nonneg = rank1_pivots.iter().all(|p| p >= &BigRational::zero());

    let strict_pivots =
        ldlt_pivots_rational(&w_strict).expect("LDL^T decomposition failed for W_strict");
    let strict_all_pos = strict_pivots.iter().all(|p| p > &BigRational::zero());

    let psd_ok = rank1_all_nonneg && strict_all_pos;
    let contradiction = psd_ok && rank1_neg && strict_neg && struct_report.verified_sound;

    MubQuadSdpCertificate {
        schema_version: "omega.mub.quad-sdp.v2",
        dimension: DIM_HILBERT,
        bases_count: NUM_BASES,
        gramian_dim: GRAMIAN_DIM,
        gramian_structure: struct_report,
        rank1_inner_product: rat_rank1.to_string(),
        rank1_inner_product_num: rat_rank1.numer().to_string(),
        rank1_inner_product_den: rat_rank1.denom().to_string(),
        rank1_strictly_negative: rank1_neg,
        strict_inner_product: rat_strict.to_string(),
        strict_inner_product_num: rat_strict.numer().to_string(),
        strict_inner_product_den: rat_strict.denom().to_string(),
        strict_strictly_negative: strict_neg,
        strict_regularizer: "1/24".to_string(),
        rank1_pivots: rank1_pivots.iter().map(|p| p.to_string()).collect(),
        rank1_pivots_nonnegative: rank1_all_nonneg,
        strict_pivots: strict_pivots.iter().map(|p| p.to_string()).collect(),
        strict_pivots_strictly_positive: strict_all_pos,
        dual_certificate_psd_certified: psd_ok,
        fixed_matrix_witness_checked: contradiction,
        constructed_matrix_not_psd: contradiction,
        complete: contradiction,
        scope: "single_synthetic_block_matrix",
        mub_nonexistence_established: false,
        firewall: "stated region only; mints no authority",
        authority_effect: "None",
        sha256_digest: None,
    }
}

pub fn get_basis_pairs() -> Vec<(usize, usize)> {
    let mut pairs = Vec::with_capacity(6);
    for a in 0..NUM_BASES {
        for b in (a + 1)..NUM_BASES {
            pairs.push((a, b));
        }
    }
    pairs
}

pub fn get_basis_triples() -> Vec<(usize, usize, usize)> {
    let mut triples = Vec::with_capacity(4);
    for a in 0..NUM_BASES {
        for b in (a + 1)..NUM_BASES {
            for c in (b + 1)..NUM_BASES {
                triples.push((a, b, c));
            }
        }
    }
    triples
}

pub fn get_basis_quadruples() -> Vec<(usize, usize, usize, usize)> {
    let mut quadruples = Vec::with_capacity(1);
    for a in 0..NUM_BASES {
        for b in (a + 1)..NUM_BASES {
            for c in (b + 1)..NUM_BASES {
                for d in (c + 1)..NUM_BASES {
                    quadruples.push((a, b, c, d));
                }
            }
        }
    }
    quadruples
}

pub fn cyc_real_rational(z: &Cyc24) -> Result<BigRational, String> {
    exact_rational(
        &z.add(&z.conj())
            .mul(&Cyc24::rat(BigRational::new(1.into(), 2.into()))),
    )
}

pub fn cyc_real_constant_coefficient(z: &Cyc24) -> BigRational {
    let re = z
        .add(&z.conj())
        .mul(&Cyc24::rat(BigRational::new(1.into(), 2.into())));
    re.a[0].clone()
}

pub fn exact_rational(value: &Cyc24) -> Result<BigRational, String> {
    if value.a[1..]
        .iter()
        .any(|coefficient| !coefficient.is_zero())
    {
        return Err("cyclotomic value is not rational".to_string());
    }
    Ok(value.a[0].clone())
}
