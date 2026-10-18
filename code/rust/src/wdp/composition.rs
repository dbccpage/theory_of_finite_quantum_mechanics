
use num_rational::BigRational;
use num_traits::{One, Signed, Zero};

use crate::empirical_adapter::{
    adapt_exact, chsh_cover, chsh_value, pr_box_run_table, signalling_defect, EmpiricalModel,
};
use crate::error::WdpError;
use crate::stochastic_package::{
    matrix_apply, matrix_shape, ClassicalInstrument, Matrix, MAX_MATRIX_ENTRIES,
};
use crate::types::AuthorityEffect;

pub const MAX_GRID_PAIRS: usize = 100_000;

pub const MAX_TARGET_STATES: usize = 1_000_000;

pub const MAX_TABLE_ENTRIES: usize = 1_000_000;

fn invalid(detail: String) -> WdpError {
    WdpError::InvalidInput { detail }
}

pub type Decoders = (Vec<usize>, Vec<usize>);

pub fn local_decoders(c: &[Vec<usize>]) -> Result<Option<Decoders>, WdpError> {
    let n_a = c.len();
    let n_b = c.first().map_or(0, Vec::len);
    if n_a == 0 || n_b == 0 {
        return Err(invalid(
            "a composition table needs at least one row and column".to_string(),
        ));
    }
    if let Some(row) = c.iter().position(|r| r.len() != n_b) {
        return Err(invalid(format!("composition table row {row} is ragged")));
    }
    let n_c = match c.iter().flatten().max() {
        None => 0,
        Some(&largest) => largest.checked_add(1).ok_or_else(|| {
            invalid(format!(
                "composition table value {largest} leaves no target count"
            ))
        })?,
    };
    if n_c > MAX_TARGET_STATES {
        return Err(invalid(format!(
            "composition table names {n_c} target states, more than {MAX_TARGET_STATES}"
        )));
    }
    let mut decoder_a = vec![0usize; n_c];
    let mut decoder_b = vec![0usize; n_c];
    let mut seen = vec![false; n_c];
    for (a, row) in c.iter().enumerate() {
        for (b, &value) in row.iter().enumerate() {
            if seen[value] {
                return Ok(None);
            }
            seen[value] = true;
            decoder_a[value] = a;
            decoder_b[value] = b;
        }
    }
    Ok(Some((decoder_a, decoder_b)))
}

pub fn decoders_are_left_inverse(c: &[Vec<usize>], decoders: &Decoders) -> bool {
    c.iter().enumerate().all(|(a, row)| {
        row.iter().enumerate().all(|(b, &value)| {
            decoders.0.get(value) == Some(&a) && decoders.1.get(value) == Some(&b)
        })
    })
}

fn check_table_size(n_a: usize, n_b: usize) -> Result<(), WdpError> {
    if n_a > MAX_TABLE_ENTRIES
        || n_b > MAX_TABLE_ENTRIES
        || n_a
            .checked_mul(n_b)
            .is_none_or(|entries| entries > MAX_TABLE_ENTRIES)
    {
        return Err(invalid(format!(
            "a {n_a} x {n_b} table exceeds {MAX_TABLE_ENTRIES} entries"
        )));
    }
    Ok(())
}

pub fn pairing_table(n_a: usize, n_b: usize) -> Result<Vec<Vec<usize>>, WdpError> {
    check_table_size(n_a, n_b)?;
    Ok((0..n_a)
        .map(|a| (0..n_b).map(|b| a * n_b + b).collect())
        .collect())
}

pub fn dump_right_table(n_a: usize, n_b: usize) -> Result<Vec<Vec<usize>>, WdpError> {
    check_table_size(n_a, n_b)?;
    Ok((0..n_a).map(|_| (0..n_b).collect()).collect())
}

pub fn pushforward(
    dist: &[BigRational],
    map: &[usize],
    n_target: usize,
) -> Result<Vec<BigRational>, WdpError> {
    if map.len() != dist.len() {
        return Err(invalid(format!(
            "map has {} values for a vector of length {}",
            map.len(),
            dist.len()
        )));
    }
    if n_target > MAX_TARGET_STATES {
        return Err(invalid(format!(
            "target carrier {n_target} exceeds {MAX_TARGET_STATES} states"
        )));
    }
    let mut out = vec![BigRational::zero(); n_target];
    for (weight, &target) in dist.iter().zip(map) {
        let slot = out
            .get_mut(target)
            .ok_or_else(|| invalid(format!("map value {target} lies outside 0..{n_target}")))?;
        *slot += weight;
    }
    Ok(out)
}

pub fn lift_along_first(pres_a: &[usize], n_b: usize) -> Result<Vec<usize>, WdpError> {
    check_table_size(pres_a.len(), n_b)?;
    Ok(pres_a
        .iter()
        .flat_map(|&q| std::iter::repeat_n(q, n_b))
        .collect())
}

#[derive(Debug, Clone, PartialEq, Eq)]
pub struct JointState {
    p: Matrix,
    n_a: usize,
    n_b: usize,
}

impl JointState {
    pub fn new(p: Matrix) -> Result<Self, WdpError> {
        let (n_a, n_b) = matrix_shape(&p, "joint state")?;
        if let Some((a, b)) = (0..n_a)
            .flat_map(|a| (0..n_b).map(move |b| (a, b)))
            .find(|&(a, b)| p[a][b].is_negative())
        {
            return Err(invalid(format!("joint state entry ({a}, {b}) is negative")));
        }
        let total = p
            .iter()
            .flatten()
            .fold(BigRational::zero(), |acc, x| acc + x);
        if !total.is_one() {
            return Err(invalid(format!(
                "joint state has total mass {total}, not 1"
            )));
        }
        Ok(Self { p, n_a, n_b })
    }

    pub fn entries(&self) -> &[Vec<BigRational>] {
        &self.p
    }

    pub fn n_a(&self) -> usize {
        self.n_a
    }

    pub fn n_b(&self) -> usize {
        self.n_b
    }

    pub fn marginal_a(&self) -> Vec<BigRational> {
        self.p
            .iter()
            .map(|row| row.iter().fold(BigRational::zero(), |acc, x| acc + x))
            .collect()
    }

    pub fn marginal_b(&self) -> Vec<BigRational> {
        (0..self.n_b)
            .map(|b| {
                self.p
                    .iter()
                    .fold(BigRational::zero(), |acc, row| acc + &row[b])
            })
            .collect()
    }

    pub fn apply_instrument_on_b(
        &self,
        instrument: &ClassicalInstrument,
    ) -> Result<Vec<Matrix>, WdpError> {
        if instrument.n_in() != self.n_b {
            return Err(invalid(format!(
                "the instrument has {} inputs, B has {} states",
                instrument.n_in(),
                self.n_b
            )));
        }
        Ok(instrument
            .updates()
            .iter()
            .map(|k| self.p.iter().map(|row| matrix_apply(k, row)).collect())
            .collect())
    }

    pub fn apply_instrument_on_a(
        &self,
        instrument: &ClassicalInstrument,
    ) -> Result<Vec<Matrix>, WdpError> {
        if instrument.n_in() != self.n_a {
            return Err(invalid(format!(
                "the instrument has {} inputs, A has {} states",
                instrument.n_in(),
                self.n_a
            )));
        }
        let columns: Vec<Vec<BigRational>> = (0..self.n_b)
            .map(|b| self.p.iter().map(|row| row[b].clone()).collect())
            .collect();
        Ok(instrument
            .updates()
            .iter()
            .map(|k| {
                let images: Vec<Vec<BigRational>> =
                    columns.iter().map(|col| matrix_apply(k, col)).collect();
                (0..instrument.n_out())
                    .map(|a2| images.iter().map(|image| image[a2].clone()).collect())
                    .collect()
            })
            .collect())
    }

    pub fn pushforward_along_first(
        &self,
        pres_a: &[usize],
        n_q: usize,
    ) -> Result<Vec<BigRational>, WdpError> {
        if pres_a.len() != self.n_a {
            return Err(invalid(format!(
                "presentation has {} values for {} states of A",
                pres_a.len(),
                self.n_a
            )));
        }
        let flat: Vec<BigRational> = self.p.iter().flatten().cloned().collect();
        pushforward(&flat, &lift_along_first(pres_a, self.n_b)?, n_q)
    }

    pub fn pushforward_presentation_a(
        &self,
        pres_a: &[usize],
        n_q: usize,
    ) -> Result<Matrix, WdpError> {
        if pres_a.len() != self.n_a {
            return Err(invalid(format!(
                "presentation has {} values for {} states of A",
                pres_a.len(),
                self.n_a
            )));
        }
        if n_q
            .checked_mul(self.n_b)
            .is_none_or(|n| n > MAX_MATRIX_ENTRIES)
        {
            return Err(invalid(format!(
                "a {n_q} x {} table exceeds {MAX_MATRIX_ENTRIES} entries",
                self.n_b
            )));
        }
        let mut out = vec![vec![BigRational::zero(); self.n_b]; n_q];
        for (a, row) in self.p.iter().enumerate() {
            let target = out.get_mut(pres_a[a]).ok_or_else(|| {
                invalid(format!("presentation value {} outside 0..{n_q}", pres_a[a]))
            })?;
            for (slot, x) in target.iter_mut().zip(row) {
                *slot += x;
            }
        }
        Ok(out)
    }
}

pub fn outcome_marginal_a(q: &[Matrix]) -> Result<Vec<BigRational>, WdpError> {
    let first = q
        .first()
        .ok_or_else(|| invalid("no outcomes to marginalize".to_string()))?;
    let mut out = vec![BigRational::zero(); first.len()];
    for outcome in q {
        if outcome.len() != out.len() {
            return Err(invalid(
                "outcome tables have different numbers of rows".to_string(),
            ));
        }
        for (slot, row) in out.iter_mut().zip(outcome) {
            *slot += row.iter().fold(BigRational::zero(), |acc, x| acc + x);
        }
    }
    Ok(out)
}

pub fn outcome_marginal_b(q: &[Matrix]) -> Result<Vec<BigRational>, WdpError> {
    let width = q
        .first()
        .and_then(|m| m.first())
        .map(Vec::len)
        .ok_or_else(|| invalid("no outcomes to marginalize".to_string()))?;
    let mut out = vec![BigRational::zero(); width];
    for outcome in q {
        for row in outcome {
            if row.len() != width {
                return Err(invalid("outcome tables have ragged rows".to_string()));
            }
            for (slot, x) in out.iter_mut().zip(row) {
                *slot += x;
            }
        }
    }
    Ok(out)
}

#[derive(Debug, Clone, PartialEq, Eq)]
pub struct BilinearForm {
    w: Matrix,
    n_a: usize,
    n_b: usize,
}

impl BilinearForm {
    pub fn new(w: Matrix) -> Result<Self, WdpError> {
        let (n_a, n_b) = matrix_shape(&w, "bilinear form")?;
        Ok(Self { w, n_a, n_b })
    }

    pub fn evaluate(&self, e: &[BigRational], f: &[BigRational]) -> Result<BigRational, WdpError> {
        if e.len() != self.n_a || f.len() != self.n_b {
            return Err(invalid(format!(
                "effects have lengths ({}, {}), the form is {} x {}",
                e.len(),
                f.len(),
                self.n_a,
                self.n_b
            )));
        }
        Ok(self
            .w
            .iter()
            .zip(e)
            .fold(BigRational::zero(), |acc, (row, ea)| {
                acc + ea
                    * row
                        .iter()
                        .zip(f)
                        .fold(BigRational::zero(), |s, (x, fb)| s + x * fb)
            }))
    }
}

pub fn composite_state_from_bilinear(w: &[Vec<BigRational>]) -> Result<JointState, WdpError> {
    let form = BilinearForm::new(w.to_vec())?;
    for (a, row) in form.w.iter().enumerate() {
        for (b, value) in row.iter().enumerate() {
            if value.is_negative() {
                return Err(invalid(format!(
                    "the form is {value} on the indicator product effect (1_{a}, 1_{b})"
                )));
            }
        }
    }
    let top_a = vec![BigRational::one(); form.n_a];
    let top_b = vec![BigRational::one(); form.n_b];
    let total = form.evaluate(&top_a, &top_b)?;
    if !total.is_one() {
        return Err(invalid(format!("omega(1, 1) = {total}, not 1")));
    }
    JointState::new(w.to_vec())
}

fn show(v: &[BigRational]) -> String {
    let items: Vec<String> = v.iter().map(ToString::to_string).collect();
    format!("[{}]", items.join(", "))
}

fn indicator(n: usize, i: usize) -> Vec<BigRational> {
    (0..n)
        .map(|k| {
            if k == i {
                BigRational::one()
            } else {
                BigRational::zero()
            }
        })
        .collect()
}

fn effect_grid(n: usize) -> Vec<Vec<BigRational>> {
    let levels = [
        BigRational::zero(),
        BigRational::new(1.into(), 2.into()),
        BigRational::one(),
    ];
    let mut grid = vec![Vec::new()];
    for _ in 0..n {
        grid = grid
            .into_iter()
            .flat_map(|prefix| {
                levels.iter().map(move |level| {
                    let mut next = prefix.clone();
                    next.push(level.clone());
                    next
                })
            })
            .collect();
    }
    grid
}

#[derive(Debug, Clone, PartialEq, Eq)]
pub struct FormReceipt {
    pub state: JointState,
    pub grid_pairs_checked: usize,
    pub authority_effect: AuthorityEffect,
}

pub fn composite_state_from_form(
    n_a: usize,
    n_b: usize,
    omega: &dyn Fn(&[BigRational], &[BigRational]) -> BigRational,
) -> Result<FormReceipt, WdpError> {
    if n_a == 0 || n_b == 0 {
        return Err(invalid("a form needs positive dimensions".to_string()));
    }
    n_a.checked_add(n_b)
        .and_then(|dimension| u32::try_from(dimension).ok())
        .and_then(|dimension| 3usize.checked_pow(dimension))
        .filter(|&g| g <= MAX_GRID_PAIRS)
        .ok_or_else(|| invalid(format!("effect grid exceeds {MAX_GRID_PAIRS} pairs")))?;
    let w: Matrix = (0..n_a)
        .map(|a| {
            (0..n_b)
                .map(|b| omega(&indicator(n_a, a), &indicator(n_b, b)))
                .collect()
        })
        .collect();
    let state = composite_state_from_bilinear(&w)?;
    let form = BilinearForm::new(state.p.clone())?;
    let mut grid_pairs_checked = 0usize;
    let grid_b = effect_grid(n_b);
    for e in effect_grid(n_a) {
        for f in &grid_b {
            if omega(&e, f) != form.evaluate(&e, f)? {
                return Err(invalid(format!(
                    "the form differs from its extracted bilinear form on the {{0, 1/2, 1}} grid at effects {}, {}",
                    show(&e),
                    show(f)
                )));
            }
            grid_pairs_checked += 1;
        }
    }
    Ok(FormReceipt {
        state,
        grid_pairs_checked,
        authority_effect: AuthorityEffect::None,
    })
}

#[derive(Debug, Clone, PartialEq, Eq)]
pub struct PrBoxFixture {
    pub model: EmpiricalModel,
    pub max_signalling_defect: BigRational,
    pub chsh_value: BigRational,
    pub positive_global_assignments: usize,
    pub strongly_contextual: bool,
    pub authority_effect: AuthorityEffect,
}

pub fn pr_box_fixture() -> Result<PrBoxFixture, WdpError> {
    let cover = chsh_cover()?;
    let table = pr_box_run_table()?;
    let model = adapt_exact(&cover, &table)?;
    let max_signalling_defect =
        signalling_defect(&cover, &table)?
            .into_iter()
            .fold(
                BigRational::zero(),
                |acc, (_, d)| if d > acc { d } else { acc },
            );
    let value = chsh_value(&model)?;
    let positive = model.positive_global_assignments()?.len();
    Ok(PrBoxFixture {
        model,
        max_signalling_defect,
        chsh_value: value,
        positive_global_assignments: positive,
        strongly_contextual: positive == 0,
        authority_effect: AuthorityEffect::None,
    })
}
