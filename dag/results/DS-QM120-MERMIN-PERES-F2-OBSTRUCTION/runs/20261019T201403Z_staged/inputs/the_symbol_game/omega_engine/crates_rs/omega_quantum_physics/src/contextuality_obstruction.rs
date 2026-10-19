// AuthorityEffect: None. Citation: sealed-derivation-v1 (3100c4e)

//! Finite parity contextuality via an exact cochain complex
//! and Cech cohomology over Z_2.
//!
//! Reimplementation of:
//! - Measurement scenario schema (X, M, b) with parity targets over Z_2
//! - Nerve extraction and cochain complex C^0 -> C^1 -> C^2
//! - Exact differential d with d^2 = 0 verified by integer arithmetic
//! - Cohomology group H^1(M, S; Z_2) and exact obstruction class calculation
//! - Witness X1: Cabello 18-ray configuration in 9 contexts over Q (nonzero class)
//! - Negative control X2: product scenario with vanishing class and explicit global section
//! - Independent verification of global section restriction
//! - Zero floating-point arithmetic in all algebraic decision paths

use omega_homology::f2_cohomology::F2ChainComplex;
use omega_number_theory::gf2::{F2Matrix, F2Vector};
use serde::{Deserialize, Serialize};

pub const CARRIER: &str = "Q";
pub const CONDUCTOR: usize = 1;

use crate::kochen_specker::CABELLO_9_CONTEXTS;

#[derive(Debug, Clone, PartialEq, Eq, Serialize, Deserialize)]
pub struct MeasurementScenario {
    pub name: String,
    pub scenario_id: String,
    pub ray_count: usize,
    pub contexts: Vec<Vec<usize>>,
    pub b_targets: Vec<u8>,
    pub coefficient_group: String,
    pub carrier: String,
    pub conductor: usize,
    pub declared_global_section: Option<Vec<u8>>,
}

impl MeasurementScenario {
    pub fn validate(&self) -> Result<(), String> {
        if self.coefficient_group != "Z_2" {
            return Err("this obstruction kernel uses the declared coefficient group Z_2".into());
        }
        if self.ray_count > 512
            || self.contexts.len() > 64
            || self.contexts.iter().map(Vec::len).sum::<usize>() > 1024
        {
            return Err("finite scenario budget exceeded".into());
        }

        if self.ray_count == 0 {
            return Err(format!("{}: ray_count must be positive", self.scenario_id));
        }
        if self.contexts.is_empty() {
            return Err(format!("{}: contexts must be non-empty", self.scenario_id));
        }
        if self.contexts.len() != self.b_targets.len() {
            return Err(format!(
                "{}: contexts count ({}) != targets count ({})",
                self.scenario_id,
                self.contexts.len(),
                self.b_targets.len()
            ));
        }
        let mut covered = vec![false; self.ray_count];
        for (idx, ctx) in self.contexts.iter().enumerate() {
            if ctx.is_empty() {
                return Err(format!("{}: context {} is empty", self.scenario_id, idx));
            }
            let mut seen = std::collections::HashSet::new();
            for &r in ctx {
                if r >= self.ray_count {
                    return Err(format!(
                        "{}: ray {} out of bounds [0, {})",
                        self.scenario_id, r, self.ray_count
                    ));
                }
                if !seen.insert(r) {
                    return Err(format!(
                        "{}: duplicate ray {} in context {}",
                        self.scenario_id, r, idx
                    ));
                }
                covered[r] = true;
            }
        }
        if covered.iter().any(|&c| !c) {
            return Err(format!(
                "{}: cover does not cover all rays",
                self.scenario_id
            ));
        }
        for (idx, &b) in self.b_targets.iter().enumerate() {
            if b > 1 {
                return Err(format!(
                    "{}: target {} at {} not in Z_2",
                    self.scenario_id, b, idx
                ));
            }
        }
        Ok(())
    }
}

pub fn construct_cabello_scenario() -> MeasurementScenario {
    let contexts = CABELLO_9_CONTEXTS.iter().map(|ctx| ctx.to_vec()).collect();
    let scen = MeasurementScenario {
        name: "the Cabello 18-ray configuration".to_string(),
        scenario_id: "X1".to_string(),
        ray_count: 18,
        contexts,
        b_targets: vec![1; 9],
        coefficient_group: "Z_2".to_string(),
        carrier: CARRIER.to_string(),
        conductor: CONDUCTOR,
        declared_global_section: None,
    };
    scen.validate().expect("X1 validation failed");
    scen
}

pub fn construct_product_scenario() -> MeasurementScenario {
    let contexts = vec![vec![0, 2], vec![0, 3], vec![1, 2], vec![1, 3]];
    let scen = MeasurementScenario {
        name: "a non-contextual product scenario".to_string(),
        scenario_id: "X2".to_string(),
        ray_count: 4,
        contexts,
        b_targets: vec![1, 1, 1, 1],
        coefficient_group: "Z_2".to_string(),
        carrier: CARRIER.to_string(),
        conductor: CONDUCTOR,
        declared_global_section: Some(vec![1, 1, 0, 0]),
    };
    scen.validate().expect("X2 validation failed");
    scen
}

// ==============================================================================
// INTEGER LINEAR ALGEBRA OVER Z_2
// ==============================================================================

// ==============================================================================
// COCHAIN COMPLEX AND COHOMOLOGY
// ==============================================================================

#[derive(Debug, Clone)]
pub struct CochainComplex {
    pub dim_c0: usize,
    pub dim_c1: usize,
    pub dim_c2: usize,
    pub cells_1: Vec<(usize, usize, Vec<usize>)>,
    pub cells_2: Vec<(usize, usize, usize, Vec<usize>)>,
    pub delta0_matrix: F2Matrix,
    pub d1_matrix: F2Matrix,
    pub diff_squares_to_zero: bool,
}

impl CochainComplex {
    pub fn checked_complex(&self) -> Result<F2ChainComplex, String> {
        if self.delta0_matrix.rows() != self.dim_c1
            || self.delta0_matrix.cols() != self.dim_c0
            || self.d1_matrix.rows() != self.dim_c2
            || self.d1_matrix.cols() != self.dim_c1
        {
            return Err("cochain row count differs from declared cells".into());
        }
        F2ChainComplex::new(
            vec![self.dim_c0, self.dim_c1, self.dim_c2],
            vec![self.delta0_matrix.transpose(), self.d1_matrix.transpose()],
        )
        .map_err(|e| e.to_string())
    }
}

pub fn build_cochain_complex(scen: &MeasurementScenario) -> Result<CochainComplex, String> {
    scen.validate()?;
    let m = scen.contexts.len();

    // 1-cells
    let mut cells_1 = Vec::new();
    for i in 0..m {
        for j in (i + 1)..m {
            let mut inter: Vec<usize> = scen.contexts[i]
                .iter()
                .filter(|r| scen.contexts[j].contains(r))
                .copied()
                .collect();
            inter.sort_unstable();
            if !inter.is_empty() {
                cells_1.push((i, j, inter));
            }
        }
    }

    // 2-cells
    let mut cells_2 = Vec::new();
    for i in 0..m {
        for j in (i + 1)..m {
            for k in (j + 1)..m {
                let mut inter: Vec<usize> = scen.contexts[i]
                    .iter()
                    .filter(|r| scen.contexts[j].contains(r) && scen.contexts[k].contains(r))
                    .copied()
                    .collect();
                inter.sort_unstable();
                if !inter.is_empty() {
                    cells_2.push((i, j, k, inter));
                }
            }
        }
    }

    let mut context_offsets: Vec<usize> = vec![0];
    for ctx in &scen.contexts {
        context_offsets.push(context_offsets.last().copied().unwrap_or(0) + (ctx.len() - 1));
    }
    let dim_c0 = context_offsets.last().copied().unwrap_or(0);

    let mut pair_offsets: Vec<usize> = vec![0];
    for (_, _, inter) in &cells_1 {
        pair_offsets.push(pair_offsets.last().copied().unwrap_or(0) + inter.len());
    }
    let dim_c1 = pair_offsets.last().copied().unwrap_or(0);

    let mut triple_offsets: Vec<usize> = vec![0];
    for (_, _, _, inter) in &cells_2 {
        triple_offsets.push(triple_offsets.last().copied().unwrap_or(0) + inter.len());
    }
    let dim_c2 = triple_offsets.last().copied().unwrap_or(0);

    if dim_c1.checked_mul(dim_c0).is_none_or(|n| n > (1 << 24))
        || dim_c2.checked_mul(dim_c1).is_none_or(|n| n > (1 << 24))
    {
        return Err("cochain matrix budget exceeded".into());
    }
    // delta0 matrix: dim_c1 x dim_c0
    let mut delta0 = F2Matrix::zeros(dim_c1, dim_c0).map_err(|e| e.to_string())?;
    for (p_idx, (i, j, inter)) in cells_1.iter().enumerate() {
        let p_base = pair_offsets[p_idx];
        for (r_offset, &r) in inter.iter().enumerate() {
            let row = p_base + r_offset;

            // Context i contribution
            let pos_i = scen.contexts[*i].iter().position(|&x| x == r).unwrap();
            let base_i = context_offsets[*i];
            let k_i = scen.contexts[*i].len() - 1;
            if pos_i == 0 {
                for step in 0..k_i {
                    delta0
                        .set(
                            row,
                            base_i + step,
                            !delta0.get(row, base_i + step).map_err(|e| e.to_string())?,
                        )
                        .map_err(|e| e.to_string())?;
                }
            } else {
                delta0
                    .set(
                        row,
                        base_i + (pos_i - 1),
                        !delta0
                            .get(row, base_i + (pos_i - 1))
                            .map_err(|e| e.to_string())?,
                    )
                    .map_err(|e| e.to_string())?;
            }

            // Context j contribution
            let pos_j = scen.contexts[*j].iter().position(|&x| x == r).unwrap();
            let base_j = context_offsets[*j];
            let k_j = scen.contexts[*j].len() - 1;
            if pos_j == 0 {
                for step in 0..k_j {
                    delta0
                        .set(
                            row,
                            base_j + step,
                            !delta0.get(row, base_j + step).map_err(|e| e.to_string())?,
                        )
                        .map_err(|e| e.to_string())?;
                }
            } else {
                delta0
                    .set(
                        row,
                        base_j + (pos_j - 1),
                        !delta0
                            .get(row, base_j + (pos_j - 1))
                            .map_err(|e| e.to_string())?,
                    )
                    .map_err(|e| e.to_string())?;
            }
        }
    }

    // d1 matrix: dim_c2 x dim_c1
    let mut d1 = F2Matrix::zeros(dim_c2, dim_c1).map_err(|e| e.to_string())?;
    if dim_c2 > 0 && dim_c1 > 0 {
        for (t_idx, (i, j, k, inter)) in cells_2.iter().enumerate() {
            let t_base = triple_offsets[t_idx];
            let jk_p_idx = cells_1
                .iter()
                .position(|(a, b, _)| *a == *j && *b == *k)
                .unwrap();
            let ik_p_idx = cells_1
                .iter()
                .position(|(a, b, _)| *a == *i && *b == *k)
                .unwrap();
            let ij_p_idx = cells_1
                .iter()
                .position(|(a, b, _)| *a == *i && *b == *j)
                .unwrap();

            for (r_offset, &r) in inter.iter().enumerate() {
                let row = t_base + r_offset;
                let col_jk = pair_offsets[jk_p_idx]
                    + cells_1[jk_p_idx].2.iter().position(|&x| x == r).unwrap();
                let col_ik = pair_offsets[ik_p_idx]
                    + cells_1[ik_p_idx].2.iter().position(|&x| x == r).unwrap();
                let col_ij = pair_offsets[ij_p_idx]
                    + cells_1[ij_p_idx].2.iter().position(|&x| x == r).unwrap();

                d1.set(
                    row,
                    col_jk,
                    !d1.get(row, col_jk).map_err(|e| e.to_string())?,
                )
                .map_err(|e| e.to_string())?;
                d1.set(
                    row,
                    col_ik,
                    !d1.get(row, col_ik).map_err(|e| e.to_string())?,
                )
                .map_err(|e| e.to_string())?;
                d1.set(
                    row,
                    col_ij,
                    !d1.get(row, col_ij).map_err(|e| e.to_string())?,
                )
                .map_err(|e| e.to_string())?;
            }
        }
    }

    let checked = F2ChainComplex::new(
        vec![dim_c0, dim_c1, dim_c2],
        vec![delta0.transpose(), d1.transpose()],
    )
    .map_err(|e| e.to_string())?;
    let diff_squares_to_zero = checked.top_dimension() == 2;

    Ok(CochainComplex {
        dim_c0,
        dim_c1,
        dim_c2,
        cells_1,
        cells_2,
        delta0_matrix: delta0,
        d1_matrix: d1,
        diff_squares_to_zero,
    })
}

#[derive(Debug, Clone, PartialEq, Eq, Serialize, Deserialize)]
pub struct CohomologyResult {
    pub scenario_id: String,
    pub name: String,
    pub coefficient_group: String,
    pub dim_c0: usize,
    pub dim_c1: usize,
    pub dim_c2: usize,
    pub rank_delta0: usize,
    pub dim_z1: usize,
    pub dim_h1: usize,
    pub diff_squares_to_zero: bool,
    pub obstruction_class_is_zero: bool,
    pub class_representative: String,
    pub global_section_exhibited: bool,
    pub exhibited_global_section: Option<Vec<u8>>,
}

pub fn compute_obstruction_class(scen: &MeasurementScenario) -> Result<CohomologyResult, String> {
    let cx = build_cochain_complex(scen)?;
    if !cx.diff_squares_to_zero {
        return Err(format!(
            "{}: differential does not square to zero",
            scen.scenario_id
        ));
    }

    // Base section s0
    let mut base_sections = Vec::new();
    for (ctx, &target) in scen.contexts.iter().zip(scen.b_targets.iter()) {
        let mut sec = std::collections::HashMap::new();
        for (idx, &r) in ctx.iter().enumerate() {
            sec.insert(r, if idx == 0 { target } else { 0 });
        }
        base_sections.push(sec);
    }

    // Discrepancy c0
    let mut c0_vector = Vec::new();
    for (i, j, inter) in &cx.cells_1 {
        for &r in inter {
            let val_i = base_sections[*i][&r];
            let val_j = base_sections[*j][&r];
            c0_vector.push((val_j + val_i) % 2);
        }
    }

    let checked = cx.checked_complex()?;
    let delta0 = &cx.delta0_matrix;
    let discrepancy = F2Vector::from_bits(&c0_vector).map_err(|e| e.to_string())?;
    let repair = delta0.solve(&discrepancy).map_err(|e| e.to_string())?;
    let obstruction_vanishes = repair.is_some();
    let rank_delta0 = delta0.rank();
    let dim_h1 = checked.cohomology_dimension(1).map_err(|e| e.to_string())?;
    let dim_z1 = dim_h1 + rank_delta0;
    // The named class must actually be closed, independently of image membership.
    checked
        .cohomology_coordinates(1, &discrepancy)
        .map_err(|e| e.to_string())?;

    let class_rep = if obstruction_vanishes {
        format!(
            "c_{} = 0 in H^1(U, F; {})",
            scen.scenario_id, scen.coefficient_group
        )
    } else {
        let items: Vec<String> = c0_vector.iter().map(|x| x.to_string()).collect();
        format!(
            "c_{} = [{}] in H^1(U, F; {}) != 0",
            scen.scenario_id,
            items.join(", "),
            scen.coefficient_group
        )
    };

    let mut exhibited_sec = None;
    if let Some(repair) = repair {
        if let Some(sec) = &scen.declared_global_section {
            if verify_global_section(scen, sec).0 {
                exhibited_sec = Some(sec.clone());
            }
        }
        if exhibited_sec.is_none() {
            let bits = repair.particular().to_bits();
            let mut offset = 0;
            let mut global = vec![0; scen.ray_count];
            for (c, &target) in scen.contexts.iter().zip(&scen.b_targets) {
                let mut first = target;
                for (j, &r) in c.iter().enumerate().skip(1) {
                    let value = bits[offset + j - 1];
                    global[r] = value;
                    first ^= value;
                }
                global[c[0]] = first;
                offset += c.len() - 1;
            }
            if !verify_global_section(scen, &global).0 {
                return Err("cochain repair did not replay a global section".into());
            }
            exhibited_sec = Some(global);
        }
    }
    let exhibited = exhibited_sec.is_some();

    Ok(CohomologyResult {
        scenario_id: scen.scenario_id.clone(),
        name: scen.name.clone(),
        coefficient_group: scen.coefficient_group.clone(),
        dim_c0: cx.dim_c0,
        dim_c1: cx.dim_c1,
        dim_c2: cx.dim_c2,
        rank_delta0,
        dim_z1,
        dim_h1,
        diff_squares_to_zero: cx.diff_squares_to_zero,
        obstruction_class_is_zero: obstruction_vanishes,
        class_representative: class_rep,
        global_section_exhibited: exhibited,
        exhibited_global_section: exhibited_sec,
    })
}

pub fn verify_global_section(scen: &MeasurementScenario, section: &[u8]) -> (bool, Vec<usize>) {
    if scen.validate().is_err() || section.len() != scen.ray_count || section.iter().any(|&x| x > 1)
    {
        return (false, (0..scen.contexts.len()).collect());
    }
    let mut violating = Vec::new();
    for (idx, (ctx, &target)) in scen.contexts.iter().zip(scen.b_targets.iter()).enumerate() {
        let sum = ctx.iter().fold(0u8, |s, &r| s ^ section[r]);
        if sum % 2 != target % 2 {
            violating.push(idx);
        }
    }
    let valid = violating.is_empty();
    (valid, violating)
}

/// A declared binary empirical model. Each row is a normalized distribution on
/// the listed context's bit patterns, with its first variable the low-order bit.
/// Nondisturbance is checked on every overlap before any contextuality verdict.
#[derive(Debug, Clone, PartialEq, Eq)]
pub struct BinaryEmpiricalModel {
    pub variables: usize,
    pub contexts: Vec<Vec<usize>>,
    pub probabilities: Vec<Vec<omega_number_theory::rational::Rational>>,
}

#[derive(Debug, Clone, PartialEq, Eq, thiserror::Error)]
pub enum EmpiricalModelError {
    #[error("a context table has the wrong shape, negative entries or nonunit mass")]
    InvalidDistribution,
    #[error("context distributions disagree on an overlap")]
    DisturbingModel,
    #[error(transparent)]
    Carrier(#[from] omega_finite_probability::local_deterministic::LocalVertexError),
    #[error(transparent)]
    Geometry(#[from] omega_solvers::solver_convex_vertex_enum::ConvexGeometryError),
    #[error(transparent)]
    Matrix(#[from] linear_algebra::exact_field::ExactFieldError),
}

#[derive(Debug, Clone, PartialEq, Eq)]
pub struct ContextualFractionCertificate {
    pub noncontextual_fraction: omega_number_theory::rational::Rational,
    pub contextual_fraction: omega_number_theory::rational::Rational,
    pub packing: omega_solvers::solver_convex_vertex_enum::PackingWitness,
}

impl BinaryEmpiricalModel {
    fn checked_vertices(
        &self,
        limits: omega_finite_probability::local_deterministic::LocalVertexLimits,
    ) -> Result<Vec<Vec<omega_number_theory::rational::Rational>>, EmpiricalModelError> {
        use num_traits::{One, Signed};
        use omega_number_theory::rational::Rational;
        let vertices = omega_finite_probability::local_deterministic::binary_local_vertices(
            self.variables,
            &self.contexts,
            limits,
        )?;
        if self.probabilities.len() != self.contexts.len()
            || self.probabilities.iter().zip(&self.contexts).any(|(p, c)| {
                p.len() != (1usize << c.len())
                    || p.iter().any(Signed::is_negative)
                    || p.iter().sum::<Rational>() != Rational::one()
            })
        {
            return Err(EmpiricalModelError::InvalidDistribution);
        }
        for i in 0..self.contexts.len() {
            for j in i + 1..self.contexts.len() {
                let overlap: Vec<usize> = self.contexts[i]
                    .iter()
                    .copied()
                    .filter(|v| self.contexts[j].contains(v))
                    .collect();
                for pattern in 0..1usize << overlap.len() {
                    let marginal = |context: usize| -> Rational {
                        self.probabilities[context]
                            .iter()
                            .enumerate()
                            .filter(|(local, _)| {
                                overlap.iter().enumerate().all(|(k, v)| {
                                    ((local
                                        >> self.contexts[context]
                                            .iter()
                                            .position(|x| x == v)
                                            .expect("overlap membership"))
                                        & 1)
                                        == ((pattern >> k) & 1)
                                })
                            })
                            .map(|(_, p)| p)
                            .sum()
                    };
                    if marginal(i) != marginal(j) {
                        return Err(EmpiricalModelError::DisturbingModel);
                    }
                }
            }
        }
        // Keep the allocation independent of a zero-mass support decision.
        Ok(vertices)
    }
    /// Global assignments whose restriction belongs to every contextual support.
    /// Empty means strongly contextual on exactly this declared binary carrier.
    pub fn supported_global_assignments(
        &self,
        limits: omega_finite_probability::local_deterministic::LocalVertexLimits,
    ) -> Result<Vec<usize>, EmpiricalModelError> {
        use num_traits::Zero;
        let vertices = self.checked_vertices(limits)?;
        let probabilities: Vec<_> = self.probabilities.iter().flatten().collect();
        Ok(vertices
            .iter()
            .enumerate()
            .filter(|(_, v)| {
                v.iter()
                    .zip(&probabilities)
                    .all(|(indicator, p)| indicator.is_zero() || !p.is_zero())
            })
            .map(|(i, _)| i)
            .collect())
    }
    /// A supported contextual outcome has no supported global extension.
    pub fn is_logically_contextual(
        &self,
        limits: omega_finite_probability::local_deterministic::LocalVertexLimits,
    ) -> Result<bool, EmpiricalModelError> {
        use num_traits::Zero;
        let vertices = self.checked_vertices(limits)?;
        let p: Vec<_> = self.probabilities.iter().flatten().collect();
        let support: Vec<_> = vertices
            .iter()
            .filter(|v| {
                v.iter()
                    .zip(&p)
                    .all(|(indicator, p)| indicator.is_zero() || !p.is_zero())
            })
            .collect();
        Ok(p.iter()
            .enumerate()
            .any(|(i, q)| !q.is_zero() && !support.iter().any(|v| !v[i].is_zero())))
    }
    fn incidence(
        &self,
        vertices: &[Vec<omega_number_theory::rational::Rational>],
    ) -> Result<
        linear_algebra::backend::basic_matrix::BasicMatrix<omega_number_theory::rational::Rational>,
        EmpiricalModelError,
    > {
        let coordinates = self.probabilities.iter().map(Vec::len).sum();
        Ok(linear_algebra::exact_field::matrix::from_fn(
            coordinates,
            vertices.len(),
            |i, j| vertices[j][i].clone(),
        )?)
    }
    /// The maximal subnormalized noncontextual part A x<=e; its mass is sum x.
    /// A replayed dual certificate bounds every possible deterministic mixture.
    pub fn contextual_fraction(
        &self,
        limits: omega_finite_probability::local_deterministic::LocalVertexLimits,
        candidate_budget: usize,
    ) -> Result<ContextualFractionCertificate, EmpiricalModelError> {
        use num_traits::One;
        use omega_number_theory::rational::Rational;
        let vertices = self.checked_vertices(limits)?;
        let probabilities = self
            .probabilities
            .iter()
            .flatten()
            .cloned()
            .collect::<Vec<_>>();
        let packing = omega_solvers::solver_convex_vertex_enum::packing_optimum(
            &self.incidence(&vertices)?,
            &probabilities,
            candidate_budget,
        )?;
        let result = ContextualFractionCertificate {
            noncontextual_fraction: packing.value.clone(),
            contextual_fraction: Rational::one() - &packing.value,
            packing,
        };
        self.verify_contextual_fraction(limits, &result)?;
        Ok(result)
    }
    pub fn verify_contextual_fraction(
        &self,
        limits: omega_finite_probability::local_deterministic::LocalVertexLimits,
        certificate: &ContextualFractionCertificate,
    ) -> Result<(), EmpiricalModelError> {
        use num_traits::{One, Zero};
        use omega_number_theory::rational::Rational;
        let vertices = self.checked_vertices(limits)?;
        let probabilities = self
            .probabilities
            .iter()
            .flatten()
            .cloned()
            .collect::<Vec<_>>();
        omega_solvers::solver_convex_vertex_enum::verify_packing_witness(
            &self.incidence(&vertices)?,
            &probabilities,
            &certificate.packing,
        )?;
        if certificate.noncontextual_fraction != certificate.packing.value
            || certificate.contextual_fraction
                != Rational::one() - &certificate.noncontextual_fraction
            || certificate.noncontextual_fraction < Rational::zero()
            || certificate.noncontextual_fraction > Rational::one()
        {
            return Err(omega_solvers::solver_convex_vertex_enum::ConvexGeometryError::InvalidWitness.into());
        }
        Ok(())
    }
}
