use linear_algebra::backend::basic_matrix::BasicMatrix;
use linear_algebra::exact_field::elimination::{image_basis, inverse, kernel_basis, rref};
use linear_algebra::exact_field::ExactFieldError;
use num_rational::BigRational;
use num_traits::{Signed, Zero};

pub type Vector = Vec<BigRational>;

pub const MAX_SHELF: usize = 16;

#[derive(Debug, Clone, PartialEq, Eq, thiserror::Error)]
pub enum DistinctImageError {
    #[error("ambient dimension must be positive")]
    EmptyAmbient,
    #[error("vector has {got} entries, ambient dimension is {expected}")]
    Shape { expected: usize, got: usize },
    #[error("exact elimination refused: {0}")]
    Elimination(#[from] ExactFieldError),
    #[error("{0}")]
    Rejected(&'static str),
}

type Result<T> = std::result::Result<T, DistinctImageError>;

#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub enum CompletionTarget {
    Raw,
    Quotient,
    Joint,
    RealizableQuotient,
}

#[derive(Debug, Clone, PartialEq, Eq)]
pub struct DistinctImageProblem {
    ambient: usize,
    source_columns: Vec<Vector>,
    repair_columns: Vec<Vector>,
    observer_rows: Vec<Vector>,
}

#[derive(Debug, Clone, PartialEq, Eq)]
pub struct DimensionFacts {
    pub dim_r: usize,
    pub dim_b: usize,
    pub dim_k: usize,
    pub dim_rk: usize,
    pub dim_kb: usize,
    pub dim_t: usize,
    pub raw_minimum: usize,
    pub quotient_minimum: usize,
    pub joint_minimum: usize,
    pub realizable_quotient_minimum: usize,
    pub separate_sum: usize,
}

#[derive(Debug, Clone, PartialEq, Eq)]
pub struct Completion {
    pub target: CompletionTarget,
    pub rows: Vec<Vector>,
    pub lower_columns: Vec<Vector>,
}

#[derive(Debug, Clone, PartialEq, Eq)]
pub struct RepairOperationWitness {
    pub admissible_columns: Vec<Vector>,
    pub preimage: Vector,
    pub repair: Vector,
    pub defect: Vector,
}

#[derive(Debug, Clone, PartialEq, Eq)]
pub enum AnnihilatorStatus {
    Feasible(Vec<Vector>),
    Impossible(Vector),
}

#[derive(Debug, Clone, PartialEq, Eq)]
pub struct ShelfSelection {
    pub indices: Option<Vec<usize>>,
    pub cost: Option<BigRational>,
}


fn columns_matrix(columns: &[Vector], n: usize) -> Result<BasicMatrix<BigRational>> {
    let k = columns.len();
    let mut data = Vec::with_capacity(n * k);
    for i in 0..n {
        for c in columns {
            data.push(c[i].clone());
        }
    }
    Ok(BasicMatrix::from_row_major(n, k, data).map_err(ExactFieldError::from)?)
}

fn rows_matrix(rows: &[Vector], n: usize) -> Result<BasicMatrix<BigRational>> {
    let data = rows.iter().flat_map(|r| r.iter().cloned()).collect();
    Ok(BasicMatrix::from_row_major(rows.len(), n, data).map_err(ExactFieldError::from)?)
}

fn unit(n: usize, i: usize) -> Vector {
    let mut v = vec![BigRational::zero(); n];
    v[i] = BigRational::from_integer(1.into());
    v
}

fn span(columns: &[Vector], n: usize) -> Result<Vec<Vector>> {
    if columns.is_empty() {
        return Ok(Vec::new());
    }
    Ok(image_basis(&columns_matrix(columns, n)?)?)
}

fn null_space(rows: &[Vector], n: usize) -> Result<Vec<Vector>> {
    if rows.is_empty() {
        return Ok((0..n).map(|i| unit(n, i)).collect());
    }
    Ok(kernel_basis(&rows_matrix(rows, n)?)?)
}

fn rank_of(columns: &[Vector], n: usize) -> Result<usize> {
    Ok(span(columns, n)?.len())
}

fn intersect(x: &[Vector], y: &[Vector], n: usize) -> Result<Vec<Vector>> {
    if x.is_empty() || y.is_empty() {
        return Ok(Vec::new());
    }
    let mut stacked: Vec<Vector> = x.to_vec();
    stacked.extend(y.iter().map(|v| v.iter().map(|e| -e).collect::<Vector>()));
    let kernel = kernel_basis(&columns_matrix(&stacked, n)?)?;
    let vectors: Vec<Vector> = kernel
        .iter()
        .map(|coeffs| {
            (0..n)
                .map(|i| {
                    x.iter()
                        .zip(coeffs)
                        .fold(BigRational::zero(), |acc, (col, c)| acc + &col[i] * c)
                })
                .collect()
        })
        .collect();
    span(&vectors, n)
}

fn contained(sub: &[Vector], sup: &[Vector], n: usize) -> Result<bool> {
    let mut joined = sup.to_vec();
    joined.extend_from_slice(sub);
    Ok(rank_of(&joined, n)? == rank_of(sup, n)?)
}

fn complement_in(sub: &[Vector], sup: &[Vector], n: usize) -> Result<Vec<Vector>> {
    let mut joined = sub.to_vec();
    joined.extend_from_slice(sup);
    if joined.is_empty() {
        return Ok(Vec::new());
    }
    let reduced = rref(&columns_matrix(&joined, n)?)?;
    Ok(reduced
        .pivot_columns()
        .iter()
        .filter(|&&p| p >= sub.len())
        .map(|&p| joined[p].clone())
        .collect())
}

fn dual_rows(prefix: &[Vector], block: std::ops::Range<usize>, n: usize) -> Result<Vec<Vector>> {
    if block.is_empty() {
        return Ok(Vec::new());
    }
    let standard: Vec<Vector> = (0..n).map(|i| unit(n, i)).collect();
    let mut basis = prefix.to_vec();
    basis.extend(complement_in(prefix, &standard, n)?);
    let inv = inverse(&columns_matrix(&basis, n)?)?;
    block
        .map(|r| {
            (0..n)
                .map(|c| {
                    inv.get(r, c)
                        .map_err(|e| DistinctImageError::Elimination(ExactFieldError::from(e)))
                })
                .collect()
        })
        .collect()
}

fn apply(rows: &[Vector], v: &Vector) -> Vector {
    rows.iter()
        .map(|r| r.iter().zip(v).fold(BigRational::zero(), |acc, (a, b)| acc + a * b))
        .collect()
}


struct Subspaces {
    r: Vec<Vector>,
    b: Vec<Vector>,
    k: Vec<Vector>,
    rk: Vec<Vector>,
    kb: Vec<Vector>,
    t: Vec<Vector>,
}

impl DistinctImageProblem {
    pub fn new(
        ambient: usize,
        source_columns: Vec<Vector>,
        repair_columns: Vec<Vector>,
        observer_rows: Vec<Vector>,
    ) -> Result<Self> {
        if ambient == 0 {
            return Err(DistinctImageError::EmptyAmbient);
        }
        for v in source_columns.iter().chain(&repair_columns).chain(&observer_rows) {
            if v.len() != ambient {
                return Err(DistinctImageError::Shape {
                    expected: ambient,
                    got: v.len(),
                });
            }
        }
        Ok(Self {
            ambient,
            source_columns,
            repair_columns,
            observer_rows,
        })
    }

    pub fn ambient(&self) -> usize {
        self.ambient
    }

    fn check_vectors(&self, vectors: &[Vector]) -> Result<()> {
        match vectors.iter().find(|v| v.len() != self.ambient) {
            Some(v) => Err(DistinctImageError::Shape {
                expected: self.ambient,
                got: v.len(),
            }),
            None => Ok(()),
        }
    }

    fn subspaces(&self) -> Result<Subspaces> {
        let n = self.ambient;
        let r = span(&self.source_columns, n)?;
        let b = span(&self.repair_columns, n)?;
        let k = null_space(&self.observer_rows, n)?;
        let rk = intersect(&r, &k, n)?;
        let kb = intersect(&k, &b, n)?;
        let t = intersect(&rk, &b, n)?;
        Ok(Subspaces { r, b, k, rk, kb, t })
    }

    pub fn analyze(&self) -> Result<DimensionFacts> {
        let s = self.subspaces()?;
        let quotient = s.k.len() - s.kb.len();
        Ok(DimensionFacts {
            dim_r: s.r.len(),
            dim_b: s.b.len(),
            dim_k: s.k.len(),
            dim_rk: s.rk.len(),
            dim_kb: s.kb.len(),
            dim_t: s.t.len(),
            raw_minimum: s.rk.len(),
            quotient_minimum: quotient,
            joint_minimum: quotient + s.t.len(),
            realizable_quotient_minimum: s.rk.len() - s.t.len(),
            separate_sum: s.rk.len() + quotient,
        })
    }

    fn observer_kernel(&self, rows: &[Vector]) -> Result<Vec<Vector>> {
        let mut all = self.observer_rows.clone();
        all.extend_from_slice(rows);
        null_space(&all, self.ambient)
    }

    pub fn raw_holds(&self, rows: &[Vector]) -> Result<bool> {
        self.check_vectors(rows)?;
        let n = self.ambient;
        Ok(intersect(&span(&self.source_columns, n)?, &self.observer_kernel(rows)?, n)?.is_empty())
    }

    pub fn quotient_holds(&self, rows: &[Vector]) -> Result<bool> {
        self.check_vectors(rows)?;
        contained(&self.observer_kernel(rows)?, &span(&self.repair_columns, self.ambient)?, self.ambient)
    }

    pub fn realizable_quotient_holds(&self, rows: &[Vector]) -> Result<bool> {
        self.check_vectors(rows)?;
        let n = self.ambient;
        let hidden = intersect(&span(&self.source_columns, n)?, &self.observer_kernel(rows)?, n)?;
        contained(&hidden, &span(&self.repair_columns, n)?, n)
    }

    pub fn suite_is_sufficient(&self, rows: &[Vector], target: CompletionTarget) -> Result<bool> {
        Ok(match target {
            CompletionTarget::Raw => self.raw_holds(rows)?,
            CompletionTarget::Quotient => self.quotient_holds(rows)?,
            CompletionTarget::Joint => self.raw_holds(rows)? && self.quotient_holds(rows)?,
            CompletionTarget::RealizableQuotient => self.realizable_quotient_holds(rows)?,
        })
    }

    fn sharp_count(&self, facts: &DimensionFacts, target: CompletionTarget) -> usize {
        match target {
            CompletionTarget::Raw => facts.raw_minimum,
            CompletionTarget::Quotient => facts.quotient_minimum,
            CompletionTarget::Joint => facts.joint_minimum,
            CompletionTarget::RealizableQuotient => facts.realizable_quotient_minimum,
        }
    }
}

pub fn produce_completion(
    problem: &DistinctImageProblem,
    target: CompletionTarget,
) -> Result<Completion> {
    let n = problem.ambient;
    let s = problem.subspaces()?;
    let (prefix, block, lower) = match target {
        CompletionTarget::Raw => {
            let m = s.rk.len();
            (s.rk.clone(), 0..m, s.rk.clone())
        }
        CompletionTarget::Quotient => {
            let c = complement_in(&s.kb, &s.k, n)?;
            let mut prefix = s.kb.clone();
            prefix.extend(c.iter().cloned());
            (prefix, s.kb.len()..s.kb.len() + c.len(), c)
        }
        CompletionTarget::Joint => {
            let s0 = complement_in(&s.t, &s.kb, n)?;
            let c = complement_in(&s.kb, &s.k, n)?;
            let mut w = s.t.clone();
            w.extend(c);
            let mut prefix = s0.clone();
            prefix.extend(w.iter().cloned());
            (prefix, s0.len()..s0.len() + w.len(), w)
        }
        CompletionTarget::RealizableQuotient => {
            let comp = complement_in(&s.t, &s.rk, n)?;
            let mut prefix = s.t.clone();
            prefix.extend(comp.iter().cloned());
            (prefix, s.t.len()..s.t.len() + comp.len(), comp)
        }
    };
    Ok(Completion {
        target,
        rows: dual_rows(&prefix, block, n)?,
        lower_columns: lower,
    })
}

pub fn check_completion(
    problem: &DistinctImageProblem,
    completion: &Completion,
) -> Result<DimensionFacts> {
    let n = problem.ambient;
    problem.check_vectors(&completion.rows)?;
    problem.check_vectors(&completion.lower_columns)?;
    let facts = problem.analyze()?;
    let s = problem.subspaces()?;
    let sharp = problem.sharp_count(&facts, completion.target);
    if completion.rows.len() != sharp {
        return Err(DistinctImageError::Rejected("row count is not the sharp count"));
    }
    if !problem.suite_is_sufficient(&completion.rows, completion.target)? {
        return Err(DistinctImageError::Rejected("completion rows are insufficient"));
    }
    let lower = &completion.lower_columns;
    if lower.len() != sharp || rank_of(lower, n)? != sharp {
        return Err(DistinctImageError::Rejected("lower certificate"));
    }
    let ok = match completion.target {
        CompletionTarget::Raw => contained(lower, &s.rk, n)?,
        CompletionTarget::Quotient => {
            contained(lower, &s.k, n)? && intersect(&span(lower, n)?, &s.b, n)?.is_empty()
        }
        CompletionTarget::Joint => {
            contained(lower, &s.k, n)? && contained(&intersect(&span(lower, n)?, &s.kb, n)?, &s.t, n)?
        }
        CompletionTarget::RealizableQuotient => {
            contained(lower, &s.rk, n)? && intersect(&span(lower, n)?, &s.t, n)?.is_empty()
        }
    };
    if !ok {
        return Err(DistinctImageError::Rejected("lower certificate"));
    }
    Ok(facts)
}

pub fn check_repair_operation(
    problem: &DistinctImageProblem,
    witness: &RepairOperationWitness,
) -> Result<()> {
    let n = problem.ambient;
    problem.check_vectors(&witness.admissible_columns)?;
    problem.check_vectors(&[witness.repair.clone(), witness.defect.clone()])?;
    if witness.preimage.len() != witness.admissible_columns.len() {
        return Err(DistinctImageError::Rejected("observation_completion_does_not_certify_repairs"));
    }
    let image: Vector = (0..n)
        .map(|i| {
            witness
                .admissible_columns
                .iter()
                .zip(&witness.preimage)
                .fold(BigRational::zero(), |acc, (col, u)| acc + &col[i] * u)
        })
        .collect();
    let in_b = contained(&[witness.repair.clone()], &span(&problem.repair_columns, n)?, n)?;
    if image != witness.repair || !in_b || witness.repair != witness.defect {
        return Err(DistinctImageError::Rejected("observation_completion_does_not_certify_repairs"));
    }
    Ok(())
}

pub fn annihilator_status(
    problem: &DistinctImageProblem,
    target: CompletionTarget,
) -> Result<AnnihilatorStatus> {
    let n = problem.ambient;
    let s = problem.subspaces()?;
    let needs_raw = matches!(target, CompletionTarget::Raw | CompletionTarget::Joint);
    if needs_raw {
        if let Some(witness) = s.t.first() {
            return Ok(AnnihilatorStatus::Impossible(witness.clone()));
        }
    }
    match target {
        CompletionTarget::Quotient | CompletionTarget::Joint => {
            let c = complement_in(&s.kb, &s.k, n)?;
            let mut prefix = s.b.clone();
            prefix.extend(c.iter().cloned());
            let rows = dual_rows(&prefix, s.b.len()..s.b.len() + c.len(), n)?;
            Ok(AnnihilatorStatus::Feasible(rows))
        }
        CompletionTarget::Raw => {
            let mut prefix = s.b.clone();
            prefix.extend(s.rk.iter().cloned());
            let rows = dual_rows(&prefix, s.b.len()..s.b.len() + s.rk.len(), n)?;
            Ok(AnnihilatorStatus::Feasible(rows))
        }
        CompletionTarget::RealizableQuotient => {
            let comp = complement_in(&s.t, &s.rk, n)?;
            let mut prefix = s.b.clone();
            prefix.extend(comp.iter().cloned());
            let rows = dual_rows(&prefix, s.b.len()..s.b.len() + comp.len(), n)?;
            Ok(AnnihilatorStatus::Feasible(rows))
        }
    }
}

fn validate_shelf(problem: &DistinctImageProblem, shelf: &[Vector], costs: &[BigRational]) -> Result<()> {
    if shelf.len() > MAX_SHELF || shelf.len() != costs.len() {
        return Err(DistinctImageError::Rejected("shelf shape"));
    }
    if costs.iter().any(|c| !c.is_positive()) {
        return Err(DistinctImageError::Rejected("positive costs"));
    }
    problem.check_vectors(shelf)
}

fn subset_rows(shelf: &[Vector], mask: u32) -> Vec<Vector> {
    shelf
        .iter()
        .enumerate()
        .filter(|(i, _)| mask & (1 << i) != 0)
        .map(|(_, r)| r.clone())
        .collect()
}

fn subset_cost(costs: &[BigRational], mask: u32) -> BigRational {
    costs
        .iter()
        .enumerate()
        .filter(|(i, _)| mask & (1 << i) != 0)
        .fold(BigRational::zero(), |acc, (_, c)| acc + c)
}

pub fn produce_shelf(
    problem: &DistinctImageProblem,
    shelf: &[Vector],
    costs: &[BigRational],
    target: CompletionTarget,
) -> Result<ShelfSelection> {
    validate_shelf(problem, shelf, costs)?;
    let mut best: Option<(BigRational, u32)> = None;
    for mask in 0..(1u32 << shelf.len()) {
        let cost = subset_cost(costs, mask);
        if best.as_ref().is_some_and(|(b, _)| &cost >= b) {
            continue;
        }
        if problem.suite_is_sufficient(&subset_rows(shelf, mask), target)? {
            best = Some((cost, mask));
        }
    }
    Ok(match best {
        Some((cost, mask)) => ShelfSelection {
            indices: Some((0..shelf.len()).filter(|i| mask & (1 << i) != 0).collect()),
            cost: Some(cost),
        },
        None => ShelfSelection {
            indices: None,
            cost: None,
        },
    })
}

pub fn check_shelf(
    problem: &DistinctImageProblem,
    shelf: &[Vector],
    costs: &[BigRational],
    target: CompletionTarget,
    selection: &ShelfSelection,
) -> Result<()> {
    validate_shelf(problem, shelf, costs)?;
    match (&selection.indices, &selection.cost) {
        (None, None) => {
            if problem.suite_is_sufficient(shelf, target)? {
                return Err(DistinctImageError::Rejected("impossibility claimed for a sufficient shelf"));
            }
            Ok(())
        }
        (Some(indices), Some(cost)) => {
            let mut mask = 0u32;
            for &i in indices {
                if i >= shelf.len() || mask & (1 << i) != 0 {
                    return Err(DistinctImageError::Rejected("invalid shelf indices"));
                }
                mask |= 1 << i;
            }
            if &subset_cost(costs, mask) != cost {
                return Err(DistinctImageError::Rejected("cost does not match indices"));
            }
            if !problem.suite_is_sufficient(&subset_rows(shelf, mask), target)? {
                return Err(DistinctImageError::Rejected("selected suite is insufficient"));
            }
            for other in 0..(1u32 << shelf.len()) {
                if &subset_cost(costs, other) < cost
                    && problem.suite_is_sufficient(&subset_rows(shelf, other), target)?
                {
                    return Err(DistinctImageError::Rejected("selected suite is not minimum"));
                }
            }
            Ok(())
        }
        _ => Err(DistinctImageError::Rejected("feasible flag")),
    }
}

pub fn report(rows: &[Vector], v: &Vector) -> Vector {
    apply(rows, v)
}
