
use std::collections::BTreeMap;

use num_traits::{One, Zero};
use tfqm_number_theory::rational::Rational;

#[derive(Debug, Clone, PartialEq, Eq, thiserror::Error)]
pub enum ClassicalInstrumentError {
    #[error("the input or output carrier is empty")]
    EmptyCarrier,
    #[error("the outcome family is empty")]
    EmptyOutcomeFamily,
    #[error("outcome {outcome}: expected a {rows}x{cols} matrix")]
    ShapeMismatch {
        outcome: usize,
        rows: usize,
        cols: usize,
    },
    #[error("outcome {outcome} has a negative entry at ({row}, {col})")]
    NegativeEntry {
        outcome: usize,
        row: usize,
        col: usize,
    },
    #[error("input column {col} carries total mass {total}, not one")]
    NormalizationDefect { col: usize, total: Rational },
    #[error("outcome {0} is not in the outcome family")]
    UnknownOutcome(usize),
    #[error("the second instrument reads {actual} inputs, the first writes {expected}")]
    CompositionMismatch { expected: usize, actual: usize },
    #[error("the coarse-graining map is not a function from the outcomes onto a declared range")]
    InvalidCoarseGraining,
    #[error("the state is not a probability vector of the declared length")]
    InvalidState,
    #[error("conditioning on an outcome of probability zero")]
    ZeroProbabilityConditioning,
    #[error("the conditional table is missing entries or ragged at input pair ({x}, {y})")]
    PartialTable { x: usize, y: usize },
    #[error("{actual} continuations supplied for {expected} outcomes")]
    ContinuationCount { expected: usize, actual: usize },
    #[error("the forgotten composite differs from the product of the forgotten maps")]
    ForgetLawDefect,
    #[error("the enumeration exceeds its declared budget")]
    ResourceLimit,
}

type Matrix = Vec<Vec<Rational>>;

fn mat_mul(left: &Matrix, right: &Matrix) -> Matrix {
    let rows = left.len();
    let inner = right.len();
    let cols = right.first().map_or(0, Vec::len);
    let mut out = vec![vec![Rational::zero(); cols]; rows];
    for (i, row) in left.iter().enumerate() {
        for k in 0..inner {
            if row[k].is_zero() {
                continue;
            }
            for j in 0..cols {
                out[i][j] += &row[k] * &right[k][j];
            }
        }
    }
    out
}

fn mat_add(left: &Matrix, right: &Matrix) -> Matrix {
    left.iter()
        .zip(right)
        .map(|(a, b)| a.iter().zip(b).map(|(x, y)| x + y).collect())
        .collect()
}

#[derive(Debug, Clone)]
pub struct ClassicalInstrument {
    inputs: usize,
    outputs: usize,
    maps: Vec<Matrix>,
}

impl PartialEq for ClassicalInstrument {
    fn eq(&self, other: &Self) -> bool {
        self.inputs == other.inputs && self.outputs == other.outputs && self.maps == other.maps
    }
}
impl Eq for ClassicalInstrument {}

impl ClassicalInstrument {
    pub fn try_new(
        inputs: usize,
        outputs: usize,
        maps: Vec<Matrix>,
    ) -> Result<Self, ClassicalInstrumentError> {
        if inputs == 0 || outputs == 0 {
            return Err(ClassicalInstrumentError::EmptyCarrier);
        }
        if maps.is_empty() {
            return Err(ClassicalInstrumentError::EmptyOutcomeFamily);
        }
        let mut totals = vec![Rational::zero(); inputs];
        for (outcome, k) in maps.iter().enumerate() {
            if k.len() != outputs || k.iter().any(|row| row.len() != inputs) {
                return Err(ClassicalInstrumentError::ShapeMismatch {
                    outcome,
                    rows: outputs,
                    cols: inputs,
                });
            }
            for (row, entries) in k.iter().enumerate() {
                for (col, value) in entries.iter().enumerate() {
                    if *value < Rational::zero() {
                        return Err(ClassicalInstrumentError::NegativeEntry { outcome, row, col });
                    }
                    totals[col] += value;
                }
            }
        }
        for (col, total) in totals.into_iter().enumerate() {
            if !total.is_one() {
                return Err(ClassicalInstrumentError::NormalizationDefect { col, total });
            }
        }
        Ok(Self {
            inputs,
            outputs,
            maps,
        })
    }

    pub fn inputs(&self) -> usize {
        self.inputs
    }
    pub fn outputs(&self) -> usize {
        self.outputs
    }
    pub fn outcome_count(&self) -> usize {
        self.maps.len()
    }
    pub fn map(&self, outcome: usize) -> Result<&Matrix, ClassicalInstrumentError> {
        self.maps
            .get(outcome)
            .ok_or(ClassicalInstrumentError::UnknownOutcome(outcome))
    }

    pub fn forget(&self) -> Matrix {
        let mut out = vec![vec![Rational::zero(); self.inputs]; self.outputs];
        for k in &self.maps {
            out = mat_add(&out, k);
        }
        out
    }

    fn check_state(&self, p: &[Rational]) -> Result<(), ClassicalInstrumentError> {
        if p.len() != self.inputs
            || p.iter().any(|v| *v < Rational::zero())
            || !p.iter().sum::<Rational>().is_one()
        {
            return Err(ClassicalInstrumentError::InvalidState);
        }
        Ok(())
    }

    pub fn apply(
        &self,
        outcome: usize,
        p: &[Rational],
    ) -> Result<Vec<Rational>, ClassicalInstrumentError> {
        self.check_state(p)?;
        let k = self.map(outcome)?;
        Ok(k.iter()
            .map(|row| row.iter().zip(p).map(|(a, b)| a * b).sum())
            .collect())
    }

    pub fn outcome_masses(&self, p: &[Rational]) -> Result<Vec<Rational>, ClassicalInstrumentError> {
        (0..self.maps.len())
            .map(|a| Ok(self.apply(a, p)?.into_iter().sum()))
            .collect()
    }

    pub fn condition(
        &self,
        outcome: usize,
        p: &[Rational],
    ) -> Result<Vec<Rational>, ClassicalInstrumentError> {
        let v = self.apply(outcome, p)?;
        let mass: Rational = v.iter().sum();
        if mass.is_zero() {
            return Err(ClassicalInstrumentError::ZeroProbabilityConditioning);
        }
        Ok(v.into_iter().map(|x| x / &mass).collect())
    }

    pub fn compose(&self, next: &Self) -> Result<Self, ClassicalInstrumentError> {
        if next.inputs != self.outputs {
            return Err(ClassicalInstrumentError::CompositionMismatch {
                expected: self.outputs,
                actual: next.inputs,
            });
        }
        let mut maps = Vec::with_capacity(self.maps.len() * next.maps.len());
        for k in &self.maps {
            for l in &next.maps {
                maps.push(mat_mul(l, k));
            }
        }
        let composed = Self::try_new(self.inputs, next.outputs, maps)?;
        if composed.forget() != mat_mul(&next.forget(), &self.forget()) {
            return Err(ClassicalInstrumentError::ForgetLawDefect);
        }
        Ok(composed)
    }

    pub fn compose_adaptive(&self, continuations: &[Self]) -> Result<Self, ClassicalInstrumentError> {
        if continuations.len() != self.maps.len() {
            return Err(ClassicalInstrumentError::ContinuationCount {
                expected: self.maps.len(),
                actual: continuations.len(),
            });
        }
        let first = &continuations[0];
        let mut maps = Vec::new();
        for (k, l) in self.maps.iter().zip(continuations) {
            if l.inputs != self.outputs {
                return Err(ClassicalInstrumentError::CompositionMismatch {
                    expected: self.outputs,
                    actual: l.inputs,
                });
            }
            if l.outputs != first.outputs || l.maps.len() != first.maps.len() {
                return Err(ClassicalInstrumentError::CompositionMismatch {
                    expected: first.outputs,
                    actual: l.outputs,
                });
            }
            for lb in &l.maps {
                maps.push(mat_mul(lb, k));
            }
        }
        Self::try_new(self.inputs, first.outputs, maps)
    }

    pub fn coarse_grain(
        &self,
        group: &[usize],
        target_count: usize,
    ) -> Result<Self, ClassicalInstrumentError> {
        if group.len() != self.maps.len()
            || target_count == 0
            || group.iter().any(|&c| c >= target_count)
        {
            return Err(ClassicalInstrumentError::InvalidCoarseGraining);
        }
        let zero = vec![vec![Rational::zero(); self.inputs]; self.outputs];
        let mut maps = vec![zero; target_count];
        for (a, &c) in group.iter().enumerate() {
            maps[c] = mat_add(&maps[c], &self.maps[a]);
        }
        Self::try_new(self.inputs, self.outputs, maps)
    }

    pub fn apply_local(&self, joint: &[Vec<Rational>]) -> Result<Vec<Matrix>, ClassicalInstrumentError> {
        let cols = joint.first().map_or(0, Vec::len);
        if joint.len() != self.inputs
            || cols == 0
            || joint.iter().any(|r| r.len() != cols || r.iter().any(|v| *v < Rational::zero()))
            || !joint.iter().flatten().sum::<Rational>().is_one()
        {
            return Err(ClassicalInstrumentError::InvalidState);
        }
        let joint: Matrix = joint.to_vec();
        Ok(self.maps.iter().map(|k| mat_mul(k, &joint)).collect())
    }
}

pub fn second_marginal(joint: &[Vec<Rational>]) -> Vec<Rational> {
    let cols = joint.first().map_or(0, Vec::len);
    (0..cols)
        .map(|z| joint.iter().map(|row| row[z].clone()).sum())
        .collect()
}

#[derive(Debug, Clone, Copy, PartialEq, Eq, PartialOrd, Ord, Hash)]
pub enum Party {
    Alice,
    Bob,
}

#[derive(Debug, Clone, PartialEq, Eq)]
pub struct SignallingWitness {
    pub party: Party,
    pub input: usize,
    pub outcome: usize,
    pub other_inputs: (usize, usize),
    pub sums: (Rational, Rational),
}

#[derive(Debug, Clone, PartialEq, Eq)]
pub struct LocalHiddenVariableTable {
    pub weights: BTreeMap<(Vec<usize>, Vec<usize>), Rational>,
}

#[derive(Debug, Clone, PartialEq, Eq)]
pub struct ConditionalBox {
    inputs: (usize, usize),
    outputs: (usize, usize),
    entries: Vec<Vec<Matrix>>,
}

impl ConditionalBox {
    pub fn try_new(
        inputs: (usize, usize),
        outputs: (usize, usize),
        entries: Vec<Vec<Matrix>>,
    ) -> Result<Self, ClassicalInstrumentError> {
        if inputs.0 == 0 || inputs.1 == 0 || outputs.0 == 0 || outputs.1 == 0 {
            return Err(ClassicalInstrumentError::EmptyCarrier);
        }
        for x in 0..inputs.0 {
            for y in 0..inputs.1 {
                let table = entries
                    .get(x)
                    .and_then(|r| r.get(y))
                    .ok_or(ClassicalInstrumentError::PartialTable { x, y })?;
                if table.len() != outputs.0 || table.iter().any(|r| r.len() != outputs.1) {
                    return Err(ClassicalInstrumentError::PartialTable { x, y });
                }
                if table.iter().flatten().any(|v| *v < Rational::zero()) {
                    return Err(ClassicalInstrumentError::NegativeEntry {
                        outcome: x * inputs.1 + y,
                        row: 0,
                        col: 0,
                    });
                }
                let total: Rational = table.iter().flatten().sum();
                if !total.is_one() {
                    return Err(ClassicalInstrumentError::NormalizationDefect {
                        col: x * inputs.1 + y,
                        total,
                    });
                }
            }
            if entries[x].len() != inputs.1 {
                return Err(ClassicalInstrumentError::PartialTable { x, y: inputs.1 });
            }
        }
        if entries.len() != inputs.0 {
            return Err(ClassicalInstrumentError::PartialTable { x: inputs.0, y: 0 });
        }
        Ok(Self {
            inputs,
            outputs,
            entries,
        })
    }

    pub fn pr_box() -> Self {
        let half = Rational::new(1.into(), 2.into());
        let entries = (0..2)
            .map(|x| {
                (0..2)
                    .map(|y| {
                        (0..2)
                            .map(|a| {
                                (0..2)
                                    .map(|b| {
                                        if (a ^ b) == (x & y) {
                                            half.clone()
                                        } else {
                                            Rational::zero()
                                        }
                                    })
                                    .collect()
                            })
                            .collect()
                    })
                    .collect()
            })
            .collect();
        Self {
            inputs: (2, 2),
            outputs: (2, 2),
            entries,
        }
    }

    pub fn entry(&self, a: usize, b: usize, x: usize, y: usize) -> Option<&Rational> {
        self.entries.get(x)?.get(y)?.get(a)?.get(b)
    }

    pub fn signalling_witness(&self) -> Option<SignallingWitness> {
        let (nx, ny) = self.inputs;
        let (na, nb) = self.outputs;
        for x in 0..nx {
            for a in 0..na {
                let s0: Rational = self.entries[x][0][a].iter().sum();
                for y in 1..ny {
                    let s1: Rational = self.entries[x][y][a].iter().sum();
                    if s1 != s0 {
                        return Some(SignallingWitness {
                            party: Party::Alice,
                            input: x,
                            outcome: a,
                            other_inputs: (0, y),
                            sums: (s0, s1),
                        });
                    }
                }
            }
        }
        for y in 0..ny {
            for b in 0..nb {
                let s0: Rational = (0..na).map(|a| self.entries[0][y][a][b].clone()).sum();
                for x in 1..nx {
                    let s1: Rational = (0..na).map(|a| self.entries[x][y][a][b].clone()).sum();
                    if s1 != s0 {
                        return Some(SignallingWitness {
                            party: Party::Bob,
                            input: y,
                            outcome: b,
                            other_inputs: (0, x),
                            sums: (s0, s1),
                        });
                    }
                }
            }
        }
        None
    }

    fn assignments(count: usize, values: usize, budget: usize) -> Result<Vec<Vec<usize>>, ClassicalInstrumentError> {
        let mut total = 1usize;
        for _ in 0..count {
            total = total
                .checked_mul(values)
                .filter(|t| *t <= budget)
                .ok_or(ClassicalInstrumentError::ResourceLimit)?;
        }
        Ok((0..total)
            .map(|mut code| {
                (0..count)
                    .map(|_| {
                        let v = code % values;
                        code /= values;
                        v
                    })
                    .collect()
            })
            .collect())
    }

    pub fn support_compatible_assignments(
        &self,
        budget: usize,
    ) -> Result<Vec<(Vec<usize>, Vec<usize>)>, ClassicalInstrumentError> {
        let fs = Self::assignments(self.inputs.0, self.outputs.0, budget)?;
        let gs = Self::assignments(self.inputs.1, self.outputs.1, budget)?;
        if fs.len().checked_mul(gs.len()).is_none_or(|n| n > budget) {
            return Err(ClassicalInstrumentError::ResourceLimit);
        }
        let mut out = Vec::new();
        for f in &fs {
            for g in &gs {
                let ok = (0..self.inputs.0).all(|x| {
                    (0..self.inputs.1).all(|y| !self.entries[x][y][f[x]][g[y]].is_zero())
                });
                if ok {
                    out.push((f.clone(), g.clone()));
                }
            }
        }
        Ok(out)
    }

    pub fn verify_local_model(&self, model: &LocalHiddenVariableTable) -> bool {
        let total: Rational = model.weights.values().sum();
        if !total.is_one() || model.weights.values().any(|w| *w < Rational::zero()) {
            return false;
        }
        let (nx, ny) = self.inputs;
        let (na, nb) = self.outputs;
        for (f, g) in model.weights.keys() {
            if f.len() != nx || g.len() != ny || f.iter().any(|&a| a >= na) || g.iter().any(|&b| b >= nb) {
                return false;
            }
        }
        for x in 0..nx {
            for y in 0..ny {
                for a in 0..na {
                    for b in 0..nb {
                        let replay: Rational = model
                            .weights
                            .iter()
                            .filter(|((f, g), _)| f[x] == a && g[y] == b)
                            .map(|(_, w)| w.clone())
                            .sum();
                        if replay != self.entries[x][y][a][b] {
                            return false;
                        }
                    }
                }
            }
        }
        true
    }

    pub fn chsh(&self) -> Option<Rational> {
        if self.inputs != (2, 2) || self.outputs != (2, 2) {
            return None;
        }
        let mut s = Rational::zero();
        for x in 0..2 {
            for y in 0..2 {
                let mut e = Rational::zero();
                for a in 0..2 {
                    for b in 0..2 {
                        let v = &self.entries[x][y][a][b];
                        if (a + b) % 2 == 0 {
                            e += v;
                        } else {
                            e -= v;
                        }
                    }
                }
                if x * y == 1 {
                    s -= e;
                } else {
                    s += e;
                }
            }
        }
        Some(s)
    }
}

#[cfg(test)]
mod tests {
    use super::*;
    use tfqm_number_theory::rational::{ri, rq};

    fn m(rows: &[&[(i64, i64)]]) -> Matrix {
        rows.iter()
            .map(|r| r.iter().map(|&(n, d)| rq(n, d)).collect())
            .collect()
    }

    fn report_k() -> ClassicalInstrument {
        ClassicalInstrument::try_new(
            2,
            2,
            vec![
                m(&[&[(1, 2), (0, 1)], &[(0, 1), (1, 3)]]),
                m(&[&[(1, 2), (0, 1)], &[(0, 1), (2, 3)]]),
            ],
        )
        .expect("fixture is an instrument")
    }

    fn report_l() -> ClassicalInstrument {
        ClassicalInstrument::try_new(
            2,
            2,
            vec![
                m(&[&[(1, 3), (1, 2)], &[(0, 1), (0, 1)]]),
                m(&[&[(0, 1), (0, 1)], &[(2, 3), (1, 2)]]),
            ],
        )
        .expect("fixture is an instrument")
    }

    #[test]
    fn report_composition_masses_and_forgotten_state() {
        let lk = report_k().compose(&report_l()).expect("compatible");
        assert_eq!(lk.map(0).unwrap(), &m(&[&[(1, 6), (1, 6)], &[(0, 1), (0, 1)]]));
        assert_eq!(lk.map(1).unwrap(), &m(&[&[(0, 1), (0, 1)], &[(1, 3), (1, 6)]]));
        assert_eq!(lk.map(2).unwrap(), &m(&[&[(1, 6), (1, 3)], &[(0, 1), (0, 1)]]));
        assert_eq!(lk.map(3).unwrap(), &m(&[&[(0, 1), (0, 1)], &[(1, 3), (1, 3)]]));
        let p = vec![rq(2, 5), rq(3, 5)];
        assert_eq!(
            lk.outcome_masses(&p).unwrap(),
            vec![rq(1, 6), rq(7, 30), rq(4, 15), rq(1, 3)]
        );
        let forgotten: Vec<Rational> = lk
            .forget()
            .iter()
            .map(|row| row.iter().zip(&p).map(|(a, b)| a * b).sum())
            .collect();
        assert_eq!(forgotten, vec![rq(13, 30), rq(17, 30)]);
        assert_eq!(lk.forget(), mat_mul(&report_l().forget(), &report_k().forget()));
    }

    #[test]
    fn coarse_graining_sums_classes_and_refuses_bad_maps() {
        let lk = report_k().compose(&report_l()).unwrap();
        let by_b = lk.coarse_grain(&[0, 1, 0, 1], 2).unwrap();
        assert_eq!(by_b.map(0).unwrap(), &m(&[&[(1, 3), (1, 2)], &[(0, 1), (0, 1)]]));
        assert_eq!(by_b.forget(), lk.forget());
        assert_eq!(lk.coarse_grain(&[0, 0, 0, 0], 1).unwrap().map(0).unwrap(), &lk.forget());
        assert_eq!(lk.coarse_grain(&[0, 1, 2], 3), Err(ClassicalInstrumentError::InvalidCoarseGraining));
        assert_eq!(lk.coarse_grain(&[0, 1, 2, 3], 3), Err(ClassicalInstrumentError::InvalidCoarseGraining));
        assert_eq!(lk.coarse_grain(&[], 0), Err(ClassicalInstrumentError::InvalidCoarseGraining));
    }

    #[test]
    fn adaptive_control_breaks_the_nonadaptive_forget_formula() {
        let k = ClassicalInstrument::try_new(2, 2, vec![m(&[&[(1, 1), (0, 1)], &[(0, 1), (0, 1)]]), m(&[&[(0, 1), (0, 1)], &[(0, 1), (1, 1)]])]).unwrap();
        let identity = ClassicalInstrument::try_new(2, 2, vec![m(&[&[(1, 1), (0, 1)], &[(0, 1), (1, 1)]])]).unwrap();
        let swap = ClassicalInstrument::try_new(2, 2, vec![m(&[&[(0, 1), (1, 1)], &[(1, 1), (0, 1)]])]).unwrap();
        let adaptive = k.compose_adaptive(&[identity, swap]).unwrap();
        assert_eq!(adaptive.forget(), m(&[&[(1, 1), (1, 1)], &[(0, 1), (0, 1)]]));
        let average = m(&[&[(1, 2), (1, 2)], &[(1, 2), (1, 2)]]);
        assert_eq!(mat_mul(&average, &k.forget()), average);
        assert_ne!(adaptive.forget(), mat_mul(&average, &k.forget()));
        assert_eq!(
            k.compose_adaptive(&[k.clone()]),
            Err(ClassicalInstrumentError::ContinuationCount { expected: 2, actual: 1 })
        );
    }

    #[test]
    fn admission_refusals() {
        assert_eq!(
            ClassicalInstrument::try_new(2, 2, vec![vec![vec![ri(2), ri(0)], vec![ri(-1), ri(1)]]]),
            Err(ClassicalInstrumentError::NegativeEntry { outcome: 0, row: 1, col: 0 })
        );
        assert_eq!(
            ClassicalInstrument::try_new(1, 1, vec![vec![vec![ri(2)]]]),
            Err(ClassicalInstrumentError::NormalizationDefect { col: 0, total: ri(2) })
        );
        assert_eq!(ClassicalInstrument::try_new(0, 1, vec![]), Err(ClassicalInstrumentError::EmptyCarrier));
        assert_eq!(ClassicalInstrument::try_new(1, 1, vec![]), Err(ClassicalInstrumentError::EmptyOutcomeFamily));
        assert!(matches!(
            ClassicalInstrument::try_new(2, 1, vec![vec![vec![ri(1)]]]),
            Err(ClassicalInstrumentError::ShapeMismatch { .. })
        ));
        let k = report_k();
        assert_eq!(k.map(2), Err(ClassicalInstrumentError::UnknownOutcome(2)));
        assert_eq!(k.apply(0, &[rq(1, 2), rq(1, 3)]), Err(ClassicalInstrumentError::InvalidState));
        let wide = ClassicalInstrument::try_new(3, 3, vec![vec![vec![ri(1), ri(0), ri(0)], vec![ri(0), ri(1), ri(0)], vec![ri(0), ri(0), ri(1)]]]).unwrap();
        assert_eq!(k.compose(&wide), Err(ClassicalInstrumentError::CompositionMismatch { expected: 2, actual: 3 }));
        let det = ClassicalInstrument::try_new(1, 1, vec![vec![vec![ri(1)]], vec![vec![ri(0)]]]).unwrap();
        assert_eq!(det.condition(1, &[ri(1)]), Err(ClassicalInstrumentError::ZeroProbabilityConditioning));
        assert_eq!(det.condition(0, &[ri(1)]), Ok(vec![ri(1)]));
    }

    #[test]
    fn local_instrument_keeps_the_other_marginal_and_postselection_does_not() {
        let joint = m(&[&[(1, 3), (1, 6)], &[(1, 6), (1, 3)]]);
        let read = ClassicalInstrument::try_new(
            2,
            2,
            vec![m(&[&[(1, 1), (0, 1)], &[(0, 1), (0, 1)]]), m(&[&[(0, 1), (0, 1)], &[(0, 1), (1, 1)]])],
        )
        .unwrap();
        let parts = read.apply_local(&joint).unwrap();
        let summed = mat_add(&parts[0], &parts[1]);
        assert_eq!(second_marginal(&summed), second_marginal(&joint));
        assert_eq!(second_marginal(&joint), vec![rq(1, 2), rq(1, 2)]);
        let mass: Rational = parts[0].iter().flatten().sum();
        let post: Matrix = parts[0].iter().map(|r| r.iter().map(|v| v / &mass).collect()).collect();
        assert_eq!(second_marginal(&post), vec![rq(2, 3), rq(1, 3)]);
    }

    #[test]
    fn pr_box_is_no_signalling_has_chsh_four_and_no_local_table() {
        let pr = ConditionalBox::pr_box();
        assert_eq!(pr.signalling_witness(), None);
        assert_eq!(pr.chsh(), Some(ri(4)));
        assert!(pr.support_compatible_assignments(64).unwrap().is_empty());
        let mut weights = BTreeMap::new();
        weights.insert((vec![0, 0], vec![0, 0]), ri(1));
        assert!(!pr.verify_local_model(&LocalHiddenVariableTable { weights }));
    }

    #[test]
    fn local_box_has_a_verified_hidden_variable_table() {
        let point = m(&[&[(1, 1), (0, 1)], &[(0, 1), (0, 1)]]);
        let local = ConditionalBox::try_new((2, 2), (2, 2), vec![vec![point.clone(), point.clone()], vec![point.clone(), point]]).unwrap();
        assert_eq!(local.signalling_witness(), None);
        assert_eq!(local.chsh(), Some(ri(2)));
        assert_eq!(local.support_compatible_assignments(64).unwrap(), vec![(vec![0, 0], vec![0, 0])]);
        let mut weights = BTreeMap::new();
        weights.insert((vec![0, 0], vec![0, 0]), ri(1));
        let table = LocalHiddenVariableTable { weights };
        assert!(local.verify_local_model(&table));
        let mut bad = table.clone();
        bad.weights.insert((vec![1, 0], vec![0, 0]), rq(0, 1));
        assert!(local.verify_local_model(&bad));
        bad.weights.insert((vec![0, 0], vec![0, 0]), rq(1, 2));
        bad.weights.insert((vec![1, 0], vec![0, 0]), rq(1, 2));
        assert!(!local.verify_local_model(&bad));
    }

    #[test]
    fn signalling_box_returns_an_exact_witness_and_partial_tables_are_refused() {
        let b0 = m(&[&[(1, 2), (0, 1)], &[(1, 2), (0, 1)]]);
        let b1 = m(&[&[(0, 1), (1, 2)], &[(0, 1), (1, 2)]]);
        let signalling = ConditionalBox::try_new((2, 2), (2, 2), vec![vec![b0.clone(), b0], vec![b1.clone(), b1]]).unwrap();
        assert_eq!(
            signalling.signalling_witness(),
            Some(SignallingWitness {
                party: Party::Bob,
                input: 0,
                outcome: 0,
                other_inputs: (0, 1),
                sums: (ri(1), ri(0)),
            })
        );
        let point = m(&[&[(1, 1), (0, 1)], &[(0, 1), (0, 1)]]);
        assert_eq!(
            ConditionalBox::try_new((2, 2), (2, 2), vec![vec![point.clone(), point.clone()], vec![point.clone()]]),
            Err(ClassicalInstrumentError::PartialTable { x: 1, y: 1 })
        );
        assert_eq!(
            ConditionalBox::pr_box().support_compatible_assignments(3),
            Err(ClassicalInstrumentError::ResourceLimit)
        );
    }
}
