
use std::collections::BTreeMap;
use num_bigint::BigInt;
use num_rational::BigRational;
use num_traits::{One, Zero};
use serde::{Deserialize, Serialize};

use linear_algebra::backend::basic_matrix::BasicMatrix;
use tfqm_number_theory::cyclotomic::Cyc8;
use crate::types::AuthorityEffect;


#[derive(Clone, Debug, PartialEq, Eq, Serialize, Deserialize)]
pub struct ExactMatrix {
    pub rows: usize,
    pub cols: usize,
    pub matrix: BasicMatrix<BigRational>,
}

impl ExactMatrix {
    pub fn zero(rows: usize, cols: usize) -> Self {
        let matrix = BasicMatrix::zero(rows, cols).expect("zero matrix allocation failed");
        Self { rows, cols, matrix }
    }

    pub fn eye(n: usize) -> Self {
        let matrix = BasicMatrix::try_from_fn(n, n, |r, c| {
            if r == c {
                BigRational::one()
            } else {
                BigRational::zero()
            }
        })
        .expect("identity matrix allocation failed");
        Self { rows: n, cols: n, matrix }
    }

    pub fn from_i64(slice: &[&[i64]]) -> Self {
        let rows = slice.len();
        let cols = if rows > 0 { slice[0].len() } else { 0 };
        let mut data = Vec::with_capacity(rows * cols);
        for row in slice {
            assert_eq!(row.len(), cols, "All rows must have identical column count");
            for &x in row.iter() {
                data.push(BigRational::from(BigInt::from(x)));
            }
        }
        let matrix = BasicMatrix::from_row_major(rows, cols, data)
            .expect("valid matrix from i64 slice");
        Self { rows, cols, matrix }
    }

    pub fn col_vector(slice: &[i64]) -> Self {
        let rows = slice.len();
        let data = slice.iter().map(|&x| BigRational::from(BigInt::from(x))).collect();
        let matrix = BasicMatrix::from_row_major(rows, 1, data)
            .expect("valid column vector from i64 slice");
        Self { rows, cols: 1, matrix }
    }

    pub fn from_basic_matrix(matrix: BasicMatrix<BigRational>) -> Self {
        Self {
            rows: matrix.rows(),
            cols: matrix.cols(),
            matrix,
        }
    }

    pub fn as_basic_matrix(&self) -> &BasicMatrix<BigRational> {
        &self.matrix
    }

    pub fn into_basic_matrix(self) -> BasicMatrix<BigRational> {
        self.matrix
    }

    pub fn add(&self, other: &Self) -> Self {
        Self::from_basic_matrix(
            self.matrix
                .add(&other.matrix)
                .expect("Dimension mismatch for matrix addition"),
        )
    }

    pub fn sub(&self, other: &Self) -> Self {
        Self::from_basic_matrix(
            self.matrix
                .sub(&other.matrix)
                .expect("Dimension mismatch for matrix subtraction"),
        )
    }

    pub fn mul(&self, other: &Self) -> Self {
        Self::from_basic_matrix(
            self.matrix
                .mul(&other.matrix)
                .expect("Inner dimension mismatch for matrix multiplication"),
        )
    }

    pub fn transpose(&self) -> Self {
        Self::from_basic_matrix(
            self.matrix
                .try_transpose()
                .expect("Transpose dimension overflow"),
        )
    }

    pub fn is_zero(&self) -> bool {
        self.matrix.as_slice().iter().all(|x| x.is_zero())
    }
}

impl std::ops::Deref for ExactMatrix {
    type Target = BasicMatrix<BigRational>;

    fn deref(&self) -> &Self::Target {
        &self.matrix
    }
}

impl From<BasicMatrix<BigRational>> for ExactMatrix {
    fn from(matrix: BasicMatrix<BigRational>) -> Self {
        Self::from_basic_matrix(matrix)
    }
}

impl From<ExactMatrix> for BasicMatrix<BigRational> {
    fn from(exact: ExactMatrix) -> Self {
        exact.matrix
    }
}


#[derive(Clone, Debug, Serialize, Deserialize)]
pub struct CoveringEdgeDiagramCED {
    pub elements: Vec<String>,
    pub fiber_dimensions: BTreeMap<String, usize>,
    pub restrictions: BTreeMap<(String, String), ExactMatrix>,
}

impl CoveringEdgeDiagramCED {
    pub fn new(
        elements: Vec<String>,
        fiber_dimensions: BTreeMap<String, usize>,
        restrictions: BTreeMap<(String, String), ExactMatrix>,
    ) -> Result<Self, String> {
        for ((upper, lower), mat) in &restrictions {
            let dim_upper = *fiber_dimensions.get(upper).ok_or_else(|| format!("Unknown upper element {upper}"))?;
            let dim_lower = *fiber_dimensions.get(lower).ok_or_else(|| format!("Unknown lower element {lower}"))?;
            if mat.rows != dim_lower || mat.cols != dim_upper {
                return Err(format!(
                    "Shape mismatch for restriction {upper}->{lower}: got ({}, {}), expected ({dim_lower}, {dim_upper})",
                    mat.rows, mat.cols
                ));
            }
        }
        Ok(Self { elements, fiber_dimensions, restrictions })
    }

    pub fn get_restriction(&self, upper: &str, lower: &str) -> Option<&ExactMatrix> {
        self.restrictions.get(&(upper.to_string(), lower.to_string()))
    }

    pub fn check_diamond_path_independence(
        &self,
        a: &str,
        b1: &str,
        b2: &str,
        c: &str,
    ) -> Result<(bool, ExactMatrix), String> {
        let r_c_b1 = self.get_restriction(c, b1).ok_or("Missing restriction c->b1")?;
        let r_b1_a = self.get_restriction(b1, a).ok_or("Missing restriction b1->a")?;
        let r_c_b2 = self.get_restriction(c, b2).ok_or("Missing restriction c->b2")?;
        let r_b2_a = self.get_restriction(b2, a).ok_or("Missing restriction b2->a")?;

        let path1 = r_b1_a.mul(r_c_b1);
        let path2 = r_b2_a.mul(r_c_b2);
        let defect = path1.sub(&path2);
        let is_indep = defect.is_zero();
        Ok((is_indep, defect))
    }

    pub fn build_path_a_completion(
        elements: Vec<String>,
        fiber_dimensions: BTreeMap<String, usize>,
        covering_restrictions: BTreeMap<(String, String), ExactMatrix>,
        saturated_chains: BTreeMap<(String, String), Vec<String>>,
    ) -> Result<Self, String> {
        let mut full_restrictions = covering_restrictions.clone();

        for el in &elements {
            let dim = *fiber_dimensions.get(el).ok_or_else(|| format!("Unknown element {el}"))?;
            full_restrictions.insert((el.clone(), el.clone()), ExactMatrix::eye(dim));
        }

        for ((c, a), chain) in saturated_chains {
            if full_restrictions.contains_key(&(c.clone(), a.clone())) {
                continue;
            }
            if chain.len() < 2 || chain.first().unwrap() != &a || chain.last().unwrap() != &c {
                return Err(format!("Invalid chain from {a} to {c}"));
            }
            let mut comp = ExactMatrix::eye(*fiber_dimensions.get(&a).unwrap());
            for i in 0..(chain.len() - 1) {
                let low = &chain[i];
                let up = &chain[i + 1];
                let step = full_restrictions.get(&(up.clone(), low.clone())).ok_or_else(|| {
                    format!("Missing covering restriction {up}->{low}")
                })?;
                comp = step.mul(&comp);
            }
            full_restrictions.insert((c, a), comp);
        }

        Self::new(elements, fiber_dimensions, full_restrictions)
    }
}


#[derive(Clone, Debug, Serialize, Deserialize)]
pub struct CurvatureOperatorCED {
    pub diagram: CoveringEdgeDiagramCED,
}

impl CurvatureOperatorCED {
    pub fn new(diagram: CoveringEdgeDiagramCED) -> Self {
        Self { diagram }
    }

    pub fn compute_curvature(&self, a: &str, b: &str, c: &str) -> Result<ExactMatrix, String> {
        let r_cb = self.diagram.get_restriction(c, b).ok_or_else(|| format!("Missing restriction {c}->{b}"))?;
        let r_ba = self.diagram.get_restriction(b, a).ok_or_else(|| format!("Missing restriction {b}->{a}"))?;
        let r_ca = self.diagram.get_restriction(c, a).ok_or_else(|| format!("Missing restriction {c}->{a}"))?;

        let composite = r_ba.mul(r_cb);
        Ok(composite.sub(r_ca))
    }

    pub fn is_flat(&self, comparable_triples: &[(&str, &str, &str)]) -> Result<bool, String> {
        for &(a, b, c) in comparable_triples {
            let k = self.compute_curvature(a, b, c)?;
            if !k.is_zero() {
                return Ok(false);
            }
        }
        Ok(true)
    }
}


pub type SectionCED = BTreeMap<String, ExactMatrix>;

#[derive(Clone, Debug)]
pub struct CochainComplexCED {
    pub diagram: CoveringEdgeDiagramCED,
}

impl CochainComplexCED {
    pub fn new(diagram: CoveringEdgeDiagramCED) -> Self {
        Self { diagram }
    }

    pub fn d0(&self, s: &SectionCED, a: &str, b: &str) -> Result<ExactMatrix, String> {
        let s_b = s.get(b).ok_or_else(|| format!("Missing section value at {b}"))?;
        let s_a = s.get(a).ok_or_else(|| format!("Missing section value at {a}"))?;
        let r_ba = self.diagram.get_restriction(b, a).ok_or_else(|| format!("Missing restriction {b}->{a}"))?;
        Ok(r_ba.mul(s_b).sub(s_a))
    }

    pub fn d1(
        &self,
        omega: &BTreeMap<(String, String), ExactMatrix>,
        a: &str,
        b: &str,
        c: &str,
    ) -> Result<ExactMatrix, String> {
        let w_bc = omega.get(&(b.to_string(), c.to_string())).ok_or("Missing omega(b, c)")?;
        let w_ac = omega.get(&(a.to_string(), c.to_string())).ok_or("Missing omega(a, c)")?;
        let w_ab = omega.get(&(a.to_string(), b.to_string())).ok_or("Missing omega(a, b)")?;
        let r_ba = self.diagram.get_restriction(b, a).ok_or_else(|| format!("Missing restriction {b}->{a}"))?;

        let term1 = r_ba.mul(w_bc);
        let term2 = term1.sub(w_ac);
        Ok(term2.add(w_ab))
    }

    pub fn verify_theorem_3_2(
        &self,
        s: &SectionCED,
        a: &str,
        b: &str,
        c: &str,
    ) -> Result<(bool, ExactMatrix, ExactMatrix), String> {
        let d0_ab = self.d0(s, a, b)?;
        let d0_bc = self.d0(s, b, c)?;
        let d0_ac = self.d0(s, a, c)?;

        let mut omega = BTreeMap::new();
        omega.insert((a.to_string(), b.to_string()), d0_ab);
        omega.insert((b.to_string(), c.to_string()), d0_bc);
        omega.insert((a.to_string(), c.to_string()), d0_ac);

        let d1_d0 = self.d1(&omega, a, b, c)?;
        let curv_op = CurvatureOperatorCED::new(self.diagram.clone());
        let k = curv_op.compute_curvature(a, b, c)?;
        let s_c = s.get(c).ok_or_else(|| format!("Missing section value at {c}"))?;
        let k_sc = k.mul(s_c);

        let matches = d1_d0 == k_sc;
        Ok((matches, d1_d0, k_sc))
    }

    pub fn evaluate_d2_boundary(
        &self,
        a: &str,
        b: &str,
        c: &str,
        d: &str,
        s_d: &ExactMatrix,
        s_c: &ExactMatrix,
    ) -> Result<(ExactMatrix, ExactMatrix), String> {
        let r_dc = self.diagram.get_restriction(d, c).ok_or("Missing restriction d->c")?;
        let curv_op = CurvatureOperatorCED::new(self.diagram.clone());
        let k_cba = curv_op.compute_curvature(a, b, c)?;

        let r_dc_sd = r_dc.mul(s_d);
        let k_r_dc_sd = k_cba.mul(&r_dc_sd);
        let k_sc = k_cba.mul(s_c);
        let lower_diff = k_r_dc_sd.sub(&k_sc);

        let r_ba = self.diagram.get_restriction(b, a).ok_or("Missing restriction b->a")?;
        let k_dcb = curv_op.compute_curvature(b, c, d)?;
        let k_dca = curv_op.compute_curvature(a, c, d)?;
        let k_dba = curv_op.compute_curvature(a, b, d)?;

        let t1 = r_ba.mul(&k_dcb.mul(s_d));
        let t2 = k_dca.mul(s_d);
        let t3 = k_dba.mul(s_d);
        let t4 = k_cba.mul(s_c);

        let d2_val = t1.sub(&t2).add(&t3).sub(&t4);
        Ok((d2_val, lower_diff))
    }
}


#[derive(Clone, Debug)]
pub struct OperatorCochainCED {
    pub diagram: CoveringEdgeDiagramCED,
}

impl OperatorCochainCED {
    pub fn new(diagram: CoveringEdgeDiagramCED) -> Self {
        Self { diagram }
    }

    pub fn evaluate_operator_delta2_k(
        &self,
        a: &str,
        b: &str,
        c: &str,
        d: &str,
    ) -> Result<ExactMatrix, String> {
        let curv_op = CurvatureOperatorCED::new(self.diagram.clone());
        let k_dcb = curv_op.compute_curvature(b, c, d)?;
        let k_dca = curv_op.compute_curvature(a, c, d)?;
        let k_dba = curv_op.compute_curvature(a, b, d)?;
        let k_cba = curv_op.compute_curvature(a, b, c)?;

        let r_ba = self.diagram.get_restriction(b, a).ok_or("Missing restriction b->a")?;
        let r_dc = self.diagram.get_restriction(d, c).ok_or("Missing restriction d->c")?;

        let term1 = r_ba.mul(&k_dcb);
        let term2 = k_dca;
        let term3 = k_dba;
        let term4 = k_cba.mul(r_dc);

        let delta2_k = term1.sub(&term2).add(&term3).sub(&term4);
        Ok(delta2_k)
    }

    pub fn verify_four_term_comparison(
        &self,
        a: &str,
        b: &str,
        c: &str,
        d: &str,
    ) -> Result<(bool, ExactMatrix, ExactMatrix), String> {
        let curv_op = CurvatureOperatorCED::new(self.diagram.clone());
        let k_dcb = curv_op.compute_curvature(b, c, d)?;
        let k_dca = curv_op.compute_curvature(a, c, d)?;
        let k_dba = curv_op.compute_curvature(a, b, d)?;
        let k_cba = curv_op.compute_curvature(a, b, c)?;

        let r_ba = self.diagram.get_restriction(b, a).ok_or("Missing restriction b->a")?;
        let r_dc = self.diagram.get_restriction(d, c).ok_or("Missing restriction d->c")?;

        let lhs = r_ba.mul(&k_dcb).add(&k_dba);
        let rhs = k_dca.add(&k_cba.mul(r_dc));
        let matches = lhs == rhs;
        Ok((matches, lhs, rhs))
    }

    pub fn evaluate_curved_derivation(
        &self,
        t_dc: &ExactMatrix,
        t_ba: &ExactMatrix,
        a: &str,
        b: &str,
        c: &str,
        d: &str,
    ) -> Result<ExactMatrix, String> {
        let curv_op = CurvatureOperatorCED::new(self.diagram.clone());
        let k_cba = curv_op.compute_curvature(a, b, c)?;
        let k_dcb = curv_op.compute_curvature(b, c, d)?;

        let term1 = k_cba.mul(t_dc);
        let term2 = t_ba.mul(&k_dcb);
        Ok(term1.sub(&term2))
    }
}


#[derive(Clone, Debug, Serialize, Deserialize)]
pub struct AdditiveNormalFormCED {
    pub strict_hat: CoveringEdgeDiagramCED,
    pub perturbation_a: BTreeMap<(String, String), ExactMatrix>,
}

impl AdditiveNormalFormCED {
    pub fn decompose(
        full: &CoveringEdgeDiagramCED,
        strict_hat: &CoveringEdgeDiagramCED,
    ) -> Result<Self, String> {
        let mut perturbation_a = BTreeMap::new();
        for ((up, low), r_mat) in &full.restrictions {
            let hat_mat = strict_hat.get_restriction(up, low).ok_or_else(|| {
                format!("Missing strict restriction {up}->{low}")
            })?;
            let a_mat = r_mat.sub(hat_mat);
            perturbation_a.insert((up.clone(), low.clone()), a_mat);
        }
        Ok(Self { strict_hat: strict_hat.clone(), perturbation_a })
    }

    pub fn verify_covering_leg_curvature(
        &self,
        a: &str,
        _b: &str,
        c: &str,
        k_cba: &ExactMatrix,
    ) -> Result<bool, String> {
        let a_ca = self.perturbation_a.get(&(c.to_string(), a.to_string())).ok_or("Missing A(c, a)")?;
        let minus_a_ca = ExactMatrix::zero(a_ca.rows, a_ca.cols).sub(a_ca);
        Ok(k_cba == &minus_a_ca)
    }
}


pub fn evaluate_ddc_diamond_commutator(
    curv_op: &CurvatureOperatorCED,
    a: &str,
    b1: &str,
    b2: &str,
    c: &str,
) -> Result<ExactMatrix, String> {
    let k1 = curv_op.compute_curvature(a, b1, c)?;
    let k2 = curv_op.compute_curvature(a, b2, c)?;
    Ok(k1.sub(&k2))
}

#[derive(Clone, Debug, PartialEq, Eq, Serialize, Deserialize)]
pub struct DistinctionCollapseLedgerCED {
    pub collapsed_count: usize,
    pub declared_charge: usize,
    pub authority_effect: AuthorityEffect,
}

impl DistinctionCollapseLedgerCED {
    pub fn record_collapse(m: usize) -> Self {
        Self {
            collapsed_count: m,
            declared_charge: 2 * m,
            authority_effect: AuthorityEffect::None,
        }
    }
}


#[derive(Clone, Debug, PartialEq, Eq)]
pub struct Cyc8Matrix2x2 {
    pub data: [[Cyc8; 2]; 2],
}

impl Cyc8Matrix2x2 {
    pub fn eye() -> Self {
        Self {
            data: [
                [Cyc8::one(), Cyc8::zero()],
                [Cyc8::zero(), Cyc8::one()],
            ],
        }
    }

    pub fn mul(&self, other: &Self) -> Self {
        let mut out = [[Cyc8::zero(), Cyc8::zero()], [Cyc8::zero(), Cyc8::zero()]];
        for i in 0..2 {
            for j in 0..2 {
                let term0 = self.data[i][0].mul(&other.data[0][j]);
                let term1 = self.data[i][1].mul(&other.data[1][j]);
                out[i][j] = term0.add(&term1);
            }
        }
        Self { data: out }
    }

    pub fn dagger(&self) -> Self {
        Self {
            data: [
                [self.data[0][0].conj(), self.data[1][0].conj()],
                [self.data[0][1].conj(), self.data[1][1].conj()],
            ],
        }
    }

    pub fn is_identity(&self) -> bool {
        self == &Self::eye()
    }
}

pub fn compute_wilson_triangle_holonomy(
    u_ij: &Cyc8Matrix2x2,
    u_jk: &Cyc8Matrix2x2,
    u_ik: &Cyc8Matrix2x2,
) -> Cyc8Matrix2x2 {
    let u_ki = u_ik.dagger();
    u_ki.mul(&u_jk.mul(u_ij))
}

pub fn verify_tetrahedral_bianchi(
    w_012: &Cyc8Matrix2x2,
    w_023: &Cyc8Matrix2x2,
    w_013: &Cyc8Matrix2x2,
    w_123: &Cyc8Matrix2x2,
) -> Cyc8Matrix2x2 {
    w_012.mul(w_023).mul(&w_013.dagger()).mul(&w_123.dagger())
}
