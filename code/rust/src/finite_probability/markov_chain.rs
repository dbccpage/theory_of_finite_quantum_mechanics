
use linear_algebra::backend::basic_matrix::{BasicMatrix, MatrixError};
use linear_algebra::linear_algebra::image_kernel::{
    solve_in_image, ExactLinearAlgebraError, ExactRowReduction, ImageMembership,
};
use num_integer::Integer;
use num_traits::{One, Signed, Zero};
use omega_number_theory::rational::Rational;

use crate::error::ClassicalShadowError;
use crate::simplex::ProbabilitySimplex;
use crate::stochastic_map::StochasticMap;

pub const MAX_EXACT_STEPS: u32 = 1024;

#[derive(Debug, Clone, PartialEq, Eq, thiserror::Error)]
pub enum MarkovChainError {
    #[error("a chain needs a square kernel, found {source_n} x {target_n}")]
    NotSquare { source_n: usize, target_n: usize },
    #[error("state {index} is outside 0..{bound}")]
    StateOutOfRange { index: usize, bound: usize },
    #[error("the chain has {closed_classes} closed communicating classes, so its stationary distribution is not unique")]
    NotUnique { closed_classes: usize },
    #[error("state {from} cannot reach state {target}, so its hitting time is infinite")]
    TargetUnreachable { from: usize, target: usize },
    #[error("the system for {what} has no solution")]
    NoSolution { what: &'static str },
    #[error("the system for {what} has more than one solution")]
    SolutionNotUnique { what: &'static str },
    #[error("the solution for {what} failed its exact replay")]
    ReplayFailed { what: &'static str },
    #[error("the distance to stationarity is still above epsilon after {max_steps} steps")]
    NotMixedWithin { max_steps: u32 },
    #[error("{what} {requested} exceeds the limit {limit}")]
    LimitExceeded {
        what: &'static str,
        requested: usize,
        limit: usize,
    },
    #[error("probability refusal: {0}")]
    Probability(#[from] ClassicalShadowError),
    #[error("matrix storage refusal: {0}")]
    Matrix(#[from] MatrixError),
    #[error("linear algebra refusal: {0}")]
    LinearAlgebra(#[from] ExactLinearAlgebraError),
}

#[derive(Debug, Clone, PartialEq, Eq)]
pub struct CommunicatingClass {
    states: Vec<usize>,
    closed: bool,
    period: Option<usize>,
}

impl CommunicatingClass {
    pub fn states(&self) -> &[usize] {
        &self.states
    }

    pub fn is_closed(&self) -> bool {
        self.closed
    }

    pub fn period(&self) -> Option<usize> {
        self.period
    }
}

#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub enum StateKind {
    Recurrent,
    Transient,
}

#[derive(Debug, Clone, PartialEq, Eq)]
pub struct ClassStationary {
    pub class: Vec<usize>,
    pub distribution: ProbabilitySimplex,
}

#[derive(Debug, Clone, PartialEq, Eq)]
pub struct AbsorptionAnalysis {
    pub transient: Vec<usize>,
    pub closed_classes: Vec<Vec<usize>>,
    pub probabilities: Vec<Vec<Rational>>,
    pub expected_steps: Vec<Rational>,
}

#[derive(Debug, Clone, PartialEq, Eq)]
pub struct MarkovChain {
    kernel: StochasticMap,
}

fn support_graph(kernel: &StochasticMap) -> Vec<Vec<usize>> {
    kernel
        .rows()
        .iter()
        .map(|row| {
            row.iter()
                .enumerate()
                .filter(|(_, p)| p.is_positive())
                .map(|(j, _)| j)
                .collect()
        })
        .collect()
}

fn advance_dfs_step(
    v: usize,
    edge_idx: usize,
    adjacency: &[Vec<usize>],
    unvisited: usize,
    next_index: &mut usize,
    index: &mut [usize],
    lowlink: &mut [usize],
    stack: &mut Vec<usize>,
    on_stack: &mut [bool],
    frames: &mut Vec<(usize, usize)>,
) {
    let w = adjacency[v][edge_idx];
    if index[w] == unvisited {
        index[w] = *next_index;
        lowlink[w] = *next_index;
        *next_index += 1;
        stack.push(w);
        on_stack[w] = true;
        frames.push((w, 0));
    } else if on_stack[w] {
        lowlink[v] = lowlink[v].min(index[w]);
    }
}

fn pop_scc_component(
    v: usize,
    stack: &mut Vec<usize>,
    on_stack: &mut [bool],
    components: &mut Vec<Vec<usize>>,
) {
    let mut component = Vec::new();
    while let Some(member) = stack.pop() {
        on_stack[member] = false;
        component.push(member);
        if member == v {
            break;
        }
    }
    component.sort_unstable();
    components.push(component);
}

fn strongly_connected_components(adjacency: &[Vec<usize>]) -> Vec<Vec<usize>> {
    let n = adjacency.len();
    let unvisited = usize::MAX;
    let mut index = vec![unvisited; n];
    let mut lowlink = vec![0usize; n];
    let mut on_stack = vec![false; n];
    let mut stack: Vec<usize> = Vec::new();
    let mut components: Vec<Vec<usize>> = Vec::new();
    let mut next_index = 0usize;

    for root in 0..n {
        if index[root] != unvisited {
            continue;
        }
        index[root] = next_index;
        lowlink[root] = next_index;
        next_index += 1;
        stack.push(root);
        on_stack[root] = true;
        let mut frames: Vec<(usize, usize)> = vec![(root, 0)];
        while let Some(frame) = frames.last_mut() {
            let v = frame.0;
            if frame.1 < adjacency[v].len() {
                let edge_idx = frame.1;
                frame.1 += 1;
                advance_dfs_step(
                    v,
                    edge_idx,
                    adjacency,
                    unvisited,
                    &mut next_index,
                    &mut index,
                    &mut lowlink,
                    &mut stack,
                    &mut on_stack,
                    &mut frames,
                );
            } else {
                frames.pop();
                if lowlink[v] == index[v] {
                    pop_scc_component(v, &mut stack, &mut on_stack, &mut components);
                }
                if let Some(parent) = frames.last() {
                    lowlink[parent.0] = lowlink[parent.0].min(lowlink[v]);
                }
            }
        }
    }
    components.sort_by_key(|component| component[0]);
    components
}

fn class_period(adjacency: &[Vec<usize>], class: &[usize]) -> Option<usize> {
    let mut level = vec![usize::MAX; adjacency.len()];
    let mut in_class = vec![false; adjacency.len()];
    for &s in class {
        in_class[s] = true;
    }
    let root = class[0];
    level[root] = 0;
    let mut queue = std::collections::VecDeque::from([root]);
    while let Some(u) = queue.pop_front() {
        for &v in &adjacency[u] {
            if in_class[v] && level[v] == usize::MAX {
                level[v] = level[u] + 1;
                queue.push_back(v);
            }
        }
    }
    let mut g = 0usize;
    for &u in class {
        for &v in &adjacency[u] {
            if in_class[v] {
                g = g.gcd(&(level[u] + 1).abs_diff(level[v]));
            }
        }
    }
    (g > 0).then_some(g)
}

fn solve_unique(
    system: &BasicMatrix<Rational>,
    target: &[Rational],
    what: &'static str,
) -> Result<Vec<Rational>, MarkovChainError> {
    if system.rank()? != system.cols() {
        return Err(MarkovChainError::SolutionNotUnique { what });
    }
    match solve_in_image(system, target)? {
        ImageMembership::InImage(witness) => Ok(witness.potential),
        ImageMembership::NotInImage { .. } => Err(MarkovChainError::NoSolution { what }),
    }
}

impl MarkovChain {
    pub fn try_new(kernel: StochasticMap) -> Result<Self, MarkovChainError> {
        if !kernel.is_endomorphism() {
            return Err(MarkovChainError::NotSquare {
                source_n: kernel.source_n(),
                target_n: kernel.target_n(),
            });
        }
        Ok(Self { kernel })
    }

    pub fn from_rows(
        rows: Vec<Vec<Rational>>,
        label: impl Into<String>,
    ) -> Result<Self, MarkovChainError> {
        let n = rows.len();
        let kernel = StochasticMap::try_from_rows(n, n, rows, label)?;
        Self::try_new(kernel)
    }

    pub fn kernel(&self) -> &StochasticMap {
        &self.kernel
    }

    pub fn n(&self) -> usize {
        self.kernel.source_n()
    }

    pub fn step(&self, p: &ProbabilitySimplex) -> Result<ProbabilitySimplex, MarkovChainError> {
        Ok(self.kernel.apply(p)?)
    }

    pub fn distribution_after(
        &self,
        initial: &ProbabilitySimplex,
        steps: u32,
    ) -> Result<ProbabilitySimplex, MarkovChainError> {
        if steps > MAX_EXACT_STEPS {
            return Err(MarkovChainError::LimitExceeded {
                what: "step count",
                requested: steps as usize,
                limit: MAX_EXACT_STEPS as usize,
            });
        }
        let mut current = initial.clone();
        for _ in 0..steps {
            current = self.step(&current)?;
        }
        Ok(current)
    }


    pub fn classes(&self) -> Vec<CommunicatingClass> {
        let adjacency = support_graph(&self.kernel);
        let components = strongly_connected_components(&adjacency);
        let mut class_of = vec![0usize; self.n()];
        for (k, component) in components.iter().enumerate() {
            for &s in component {
                class_of[s] = k;
            }
        }
        components
            .into_iter()
            .enumerate()
            .map(|(k, states)| {
                let closed = states
                    .iter()
                    .all(|&s| adjacency[s].iter().all(|&t| class_of[t] == k));
                let period = class_period(&adjacency, &states);
                CommunicatingClass {
                    states,
                    closed,
                    period,
                }
            })
            .collect()
    }

    pub fn closed_classes(&self) -> Vec<Vec<usize>> {
        self.classes()
            .into_iter()
            .filter(|c| c.closed)
            .map(|c| c.states)
            .collect()
    }

    pub fn state_kinds(&self) -> Vec<StateKind> {
        let mut kinds = vec![StateKind::Transient; self.n()];
        for class in self.classes().iter().filter(|c| c.closed) {
            for &s in &class.states {
                kinds[s] = StateKind::Recurrent;
            }
        }
        kinds
    }

    pub fn transient_states(&self) -> Vec<usize> {
        self.state_kinds()
            .iter()
            .enumerate()
            .filter(|(_, kind)| **kind == StateKind::Transient)
            .map(|(s, _)| s)
            .collect()
    }

    pub fn absorbing_states(&self) -> Vec<usize> {
        self.kernel
            .rows()
            .iter()
            .enumerate()
            .filter(|(i, row)| row[*i].is_one())
            .map(|(i, _)| i)
            .collect()
    }

    pub fn is_irreducible(&self) -> bool {
        self.classes().len() == 1
    }

    pub fn period(&self) -> Option<usize> {
        let mut classes = self.classes();
        if classes.len() == 1 {
            classes.pop().and_then(|c| c.period)
        } else {
            None
        }
    }

    pub fn is_aperiodic(&self) -> bool {
        self.period() == Some(1)
    }

    pub fn is_primitive(&self) -> bool {
        self.is_aperiodic()
    }
}

fn boolean_matrix_multiply(a: &[Vec<bool>], b: &[Vec<bool>], n: usize) -> Vec<Vec<bool>> {
    let mut next = vec![vec![false; n]; n];
    for i in 0..n {
        for (m, &reaches) in a[i].iter().enumerate() {
            if !reaches {
                continue;
            }
            for j in 0..n {
                next[i][j] |= b[m][j];
            }
        }
    }
    next
}

impl MarkovChain {
    pub fn first_positive_power(&self, max_power: u32) -> Option<u32> {
        let adjacency = support_graph(&self.kernel);
        let n = self.n();
        let mut step = vec![vec![false; n]; n];
        for (i, successors) in adjacency.iter().enumerate() {
            for &j in successors {
                step[i][j] = true;
            }
        }
        let mut power = step.clone();
        for k in 1..=max_power {
            if power.iter().all(|row| row.iter().all(|&b| b)) {
                return Some(k);
            }
            power = boolean_matrix_multiply(&power, &step, n);
        }
        None
    }


    pub fn is_stationary(&self, p: &ProbabilitySimplex) -> Result<bool, MarkovChainError> {
        Ok(self.kernel.apply(p)? == *p)
    }

    pub fn is_reversible_with(&self, pi: &ProbabilitySimplex) -> Result<bool, MarkovChainError> {
        if pi.n() != self.n() {
            return Err(ClassicalShadowError::ShapeMismatch {
                left: pi.n(),
                right: self.n(),
            }
            .into());
        }
        let rows = self.kernel.rows();
        let p = pi.probs();
        Ok((0..self.n())
            .all(|i| (i + 1..self.n()).all(|j| &p[i] * &rows[i][j] == &p[j] * &rows[j][i])))
    }

    fn class_stationary(&self, class: &[usize]) -> Result<ProbabilitySimplex, MarkovChainError> {
        const WHAT: &str = "the stationary law of a closed class";
        let k = class.len();
        let rows = self.kernel.rows();
        let mut data = Vec::with_capacity((k + 1) * k);
        for r in 0..k {
            for c in 0..k {
                let mut entry = rows[class[c]][class[r]].clone();
                if r == c {
                    entry -= Rational::one();
                }
                data.push(entry);
            }
        }
        data.extend(std::iter::repeat_with(Rational::one).take(k));
        let system = BasicMatrix::from_row_major(k + 1, k, data)?;
        let mut target = vec![Rational::zero(); k + 1];
        target[k] = Rational::one();
        let on_class = solve_unique(&system, &target, WHAT)?;

        let mut full = vec![Rational::zero(); self.n()];
        for (c, value) in on_class.into_iter().enumerate() {
            full[class[c]] = value;
        }
        let distribution = ProbabilitySimplex::try_new(full)?;
        if !self.is_stationary(&distribution)? {
            return Err(MarkovChainError::ReplayFailed { what: WHAT });
        }
        Ok(distribution)
    }

    pub fn closed_class_stationary_distributions(
        &self,
    ) -> Result<Vec<ClassStationary>, MarkovChainError> {
        self.closed_classes()
            .into_iter()
            .map(|class| {
                let distribution = self.class_stationary(&class)?;
                Ok(ClassStationary {
                    class,
                    distribution,
                })
            })
            .collect()
    }

    pub fn stationary_distribution(&self) -> Result<ProbabilitySimplex, MarkovChainError> {
        let mut closed = self.closed_classes();
        if closed.len() != 1 {
            return Err(MarkovChainError::NotUnique {
                closed_classes: closed.len(),
            });
        }
        let class = closed.remove(0);
        self.class_stationary(&class)
    }

    pub fn stationarity_matrix(&self) -> Result<BasicMatrix<Rational>, MarkovChainError> {
        let n = self.n();
        let rows = self.kernel.rows();
        let mut data = Vec::with_capacity(n * n);
        for r in 0..n {
            for c in 0..n {
                let mut entry = rows[c][r].clone();
                if r == c {
                    entry -= Rational::one();
                }
                data.push(entry);
            }
        }
        Ok(BasicMatrix::from_row_major(n, n, data)?)
    }

    pub fn time_reversal(&self, pi: &ProbabilitySimplex) -> Result<MarkovChain, MarkovChainError> {
        if pi.n() != self.n() {
            return Err(ClassicalShadowError::ShapeMismatch {
                left: pi.n(),
                right: self.n(),
            }
            .into());
        }
        if let Some(index) = pi.probs().iter().position(Zero::is_zero) {
            return Err(ClassicalShadowError::ZeroMass { index }.into());
        }
        let rows = self.kernel.rows();
        let p = pi.probs();
        let reversed: Vec<Vec<Rational>> = (0..self.n())
            .map(|i| (0..self.n()).map(|j| &p[j] * &rows[j][i] / &p[i]).collect())
            .collect();
        Self::from_rows(reversed, format!("reverse({})", self.kernel.label()))
    }
}

fn build_identity_minus_submatrix(
    states: &[usize],
    rows: &[Vec<Rational>],
) -> Result<BasicMatrix<Rational>, MarkovChainError> {
    let m = states.len();
    let mut data = Vec::with_capacity(m * m);
    for (r, &i) in states.iter().enumerate() {
        for (c, &j) in states.iter().enumerate() {
            let mut entry = -rows[i][j].clone();
            if r == c {
                entry += Rational::one();
            }
            data.push(entry);
        }
    }
    BasicMatrix::from_row_major(m, m, data).map_err(Into::into)
}

fn validate_absorption_probabilities(
    probabilities: &[Vec<Rational>],
) -> Result<(), MarkovChainError> {
    for row in probabilities {
        let sum: Rational = row.iter().sum();
        if !sum.is_one() || row.iter().any(Signed::is_negative) {
            return Err(MarkovChainError::ReplayFailed {
                what: "absorption probabilities",
            });
        }
    }
    Ok(())
}

fn verify_target_reachable(
    target: usize,
    n: usize,
    adjacency: &[Vec<usize>],
) -> Result<(), MarkovChainError> {
    let mut predecessors = vec![Vec::new(); n];
    for (i, successors) in adjacency.iter().enumerate() {
        for &j in successors {
            predecessors[j].push(i);
        }
    }
    let mut reaches = vec![false; n];
    reaches[target] = true;
    let mut queue = std::collections::VecDeque::from([target]);
    while let Some(v) = queue.pop_front() {
        for &u in &predecessors[v] {
            if !reaches[u] {
                reaches[u] = true;
                queue.push_back(u);
            }
        }
    }
    if let Some(from) = reaches.iter().position(|&r| !r) {
        return Err(MarkovChainError::TargetUnreachable { from, target });
    }
    Ok(())
}

impl MarkovChain {
    pub fn absorption_analysis(&self) -> Result<AbsorptionAnalysis, MarkovChainError> {
        let closed_classes = self.closed_classes();
        let transient = self.transient_states();
        if transient.is_empty() {
            return Ok(AbsorptionAnalysis {
                transient,
                closed_classes,
                probabilities: Vec::new(),
                expected_steps: Vec::new(),
            });
        }
        let rows = self.kernel.rows();
        let t = transient.len();
        let system = build_identity_minus_submatrix(&transient, rows)?;

        let mut probabilities = vec![vec![Rational::zero(); closed_classes.len()]; t];
        for (k, class) in closed_classes.iter().enumerate() {
            let target: Vec<Rational> = transient
                .iter()
                .map(|&i| class.iter().map(|&j| &rows[i][j]).sum::<Rational>())
                .collect();
            let column = solve_unique(&system, &target, "absorption probabilities")?;
            for (row, value) in probabilities.iter_mut().zip(column) {
                row[k] = value;
            }
        }
        validate_absorption_probabilities(&probabilities)?;
        let expected_steps = solve_unique(
            &system,
            &vec![Rational::one(); t],
            "expected absorption steps",
        )?;
        if expected_steps.iter().any(|s| *s < Rational::one()) {
            return Err(MarkovChainError::ReplayFailed {
                what: "expected absorption steps",
            });
        }
        Ok(AbsorptionAnalysis {
            transient,
            closed_classes,
            probabilities,
            expected_steps,
        })
    }

    pub fn expected_hitting_times(&self, target: usize) -> Result<Vec<Rational>, MarkovChainError> {
        let n = self.n();
        if target >= n {
            return Err(MarkovChainError::StateOutOfRange {
                index: target,
                bound: n,
            });
        }
        let adjacency = support_graph(&self.kernel);
        verify_target_reachable(target, n, &adjacency)?;

        let others: Vec<usize> = (0..n).filter(|&i| i != target).collect();
        let mut times = vec![Rational::zero(); n];
        if others.is_empty() {
            return Ok(times);
        }
        let rows = self.kernel.rows();
        let m = others.len();
        let system = build_identity_minus_submatrix(&others, rows)?;
        let solution = solve_unique(&system, &vec![Rational::one(); m], "expected hitting times")?;
        for (&i, value) in others.iter().zip(solution) {
            times[i] = value;
        }
        Ok(times)
    }

    pub fn expected_return_time(&self, state: usize) -> Result<Rational, MarkovChainError> {
        let times = self.expected_hitting_times(state)?;
        let rows = self.kernel.rows();
        Ok(Rational::one()
            + rows[state]
                .iter()
                .zip(&times)
                .map(|(p, h)| p * h)
                .sum::<Rational>())
    }


    pub fn distance_profile(&self, max_steps: u32) -> Result<Vec<Rational>, MarkovChainError> {
        if max_steps > MAX_EXACT_STEPS {
            return Err(MarkovChainError::LimitExceeded {
                what: "mixing steps",
                requested: max_steps as usize,
                limit: MAX_EXACT_STEPS as usize,
            });
        }
        let pi = self.stationary_distribution()?;
        let mut profile = Vec::with_capacity(max_steps as usize);
        let mut power = self.kernel.clone();
        for k in 1..=max_steps {
            if k > 1 {
                power = power.compose(&self.kernel)?;
            }
            profile.push(self.worst_distance(&power, &pi)?);
        }
        Ok(profile)
    }

    fn worst_distance(
        &self,
        power: &StochasticMap,
        pi: &ProbabilitySimplex,
    ) -> Result<Rational, MarkovChainError> {
        let mut worst = Rational::zero();
        for i in 0..power.source_n() {
            let d = power.conditional(i)?.total_variation(pi)?;
            if d > worst {
                worst = d;
            }
        }
        Ok(worst)
    }

    pub fn mixing_time(&self, epsilon: &Rational, max_steps: u32) -> Result<u32, MarkovChainError> {
        let profile = self.distance_profile(max_steps)?;
        let index = profile
            .iter()
            .position(|d| d <= epsilon)
            .ok_or(MarkovChainError::NotMixedWithin { max_steps })?;
        u32::try_from(index + 1).map_err(|_| MarkovChainError::LimitExceeded {
            what: "mixing steps",
            requested: index + 1,
            limit: MAX_EXACT_STEPS as usize,
        })
    }
}

#[cfg(test)]
mod tests {
    use super::*;
    use crate::test_support::stochastic;
    use omega_number_theory::rational::{ri, rq};

    fn chain(rows: &[&[(i64, i64)]]) -> MarkovChain {
        MarkovChain::try_new(stochastic(rows)).unwrap()
    }

    fn mixed_chain() -> MarkovChain {
        let z = (0, 1);
        chain(&[
            &[z, (1, 2), (1, 4), z, z, z, z, (1, 4)],
            &[(1, 4), z, z, (1, 2), (1, 4), z, z, z],
            &[z, z, z, (1, 1), z, z, z, z],
            &[z, z, (1, 1), z, z, z, z, z],
            &[z, z, z, z, (1, 2), (1, 2), z, z],
            &[z, z, z, z, z, z, (1, 1), z],
            &[z, z, z, z, (1, 1), z, z, z],
            &[z, z, z, z, z, z, z, (1, 1)],
        ])
    }

    #[test]
    fn a_non_square_kernel_is_not_a_chain() {
        let rectangular = stochastic(&[&[(1, 2), (1, 2), (0, 1)], &[(0, 1), (1, 2), (1, 2)]]);
        assert_eq!(
            MarkovChain::try_new(rectangular),
            Err(MarkovChainError::NotSquare {
                source_n: 2,
                target_n: 3
            })
        );
        assert_eq!(
            MarkovChain::from_rows(vec![vec![rq(1, 2), rq(1, 3)]], "bad"),
            Err(MarkovChainError::Probability(
                ClassicalShadowError::DimensionMismatch {
                    expected: 1,
                    actual: 2
                }
            ))
        );
    }

    #[test]
    fn classes_closedness_periods_and_state_kinds_have_their_hand_values() {
        let c = mixed_chain();
        let classes = c.classes();
        let summary: Vec<(Vec<usize>, bool, Option<usize>)> = classes
            .iter()
            .map(|k| (k.states().to_vec(), k.is_closed(), k.period()))
            .collect();
        assert_eq!(
            summary,
            vec![
                (vec![0, 1], false, Some(2)),
                (vec![2, 3], true, Some(2)),
                (vec![4, 5, 6], true, Some(1)),
                (vec![7], true, Some(1)),
            ]
        );
        assert_eq!(c.closed_classes(), vec![vec![2, 3], vec![4, 5, 6], vec![7]]);
        assert_eq!(c.transient_states(), vec![0, 1]);
        assert_eq!(c.absorbing_states(), vec![7]);
        assert_eq!(
            c.state_kinds(),
            vec![
                StateKind::Transient,
                StateKind::Transient,
                StateKind::Recurrent,
                StateKind::Recurrent,
                StateKind::Recurrent,
                StateKind::Recurrent,
                StateKind::Recurrent,
                StateKind::Recurrent,
            ]
        );
        assert!(!c.is_irreducible());
        assert_eq!(c.period(), None);
        assert!(!c.is_primitive());
    }

    #[test]
    fn a_single_state_without_a_self_loop_has_no_period_and_is_not_a_chain_class_with_a_cycle() {
        let c = chain(&[&[(0, 1), (1, 1)], &[(0, 1), (1, 1)]]);
        let classes = c.classes();
        assert_eq!(classes[0].states(), &[0]);
        assert_eq!(classes[0].period(), None);
        assert!(!classes[0].is_closed());
        assert_eq!(classes[1].period(), Some(1));
        assert!(classes[1].is_closed());
    }

    #[test]
    fn a_long_path_does_not_overflow_the_stack_of_the_component_search() {
        let n = 20_000usize;
        let mut adjacency = vec![Vec::new(); n];
        for (i, successors) in adjacency.iter_mut().enumerate() {
            successors.push(if i + 1 < n { i + 1 } else { i });
        }
        let components = strongly_connected_components(&adjacency);
        assert_eq!(components.len(), n);
        assert!(components.iter().enumerate().all(|(k, c)| c == &vec![k]));
    }

    #[test]
    fn the_stationary_laws_of_the_closed_classes_are_exact_and_the_chain_has_none_unique() {
        let c = mixed_chain();
        let laws = c.closed_class_stationary_distributions().unwrap();
        assert_eq!(laws.len(), 3);
        let mass = |l: &ClassStationary| l.distribution.probs().to_vec();
        let z = ri(0);
        assert_eq!(
            mass(&laws[0]),
            vec![
                z.clone(),
                z.clone(),
                rq(1, 2),
                rq(1, 2),
                z.clone(),
                z.clone(),
                z.clone(),
                z.clone()
            ]
        );
        assert_eq!(
            mass(&laws[1]),
            vec![
                z.clone(),
                z.clone(),
                z.clone(),
                z.clone(),
                rq(1, 2),
                rq(1, 4),
                rq(1, 4),
                z.clone()
            ]
        );
        assert_eq!(
            mass(&laws[2]),
            vec![
                z.clone(),
                z.clone(),
                z.clone(),
                z.clone(),
                z.clone(),
                z.clone(),
                z,
                ri(1)
            ]
        );
        for law in &laws {
            assert!(c.is_stationary(&law.distribution).unwrap());
        }
        assert_eq!(
            c.stationary_distribution(),
            Err(MarkovChainError::NotUnique { closed_classes: 3 })
        );
        let kernel_dimension = c
            .stationarity_matrix()
            .unwrap()
            .kernel_basis()
            .unwrap()
            .len();
        assert_eq!(kernel_dimension, 3);
    }

    #[test]
    fn absorption_probabilities_and_times_have_their_hand_values() {
        let analysis = mixed_chain().absorption_analysis().unwrap();
        assert_eq!(analysis.transient, vec![0, 1]);
        assert_eq!(
            analysis.closed_classes,
            vec![vec![2, 3], vec![4, 5, 6], vec![7]]
        );
        assert_eq!(
            analysis.probabilities,
            vec![
                vec![rq(4, 7), rq(1, 7), rq(2, 7)],
                vec![rq(9, 14), rq(2, 7), rq(1, 14)],
            ]
        );
        assert_eq!(analysis.expected_steps, vec![rq(12, 7), rq(10, 7)]);
    }

    #[test]
    fn a_chain_with_no_transient_state_has_an_empty_absorption_analysis() {
        let c = chain(&[&[(1, 2), (1, 2)], &[(1, 3), (2, 3)]]);
        let analysis = c.absorption_analysis().unwrap();
        assert!(analysis.transient.is_empty() && analysis.probabilities.is_empty());
        assert_eq!(analysis.closed_classes, vec![vec![0, 1]]);
    }

    #[test]
    fn hitting_times_are_refused_when_a_state_cannot_reach_the_target() {
        let c = mixed_chain();
        assert_eq!(
            c.expected_hitting_times(2),
            Err(MarkovChainError::TargetUnreachable { from: 4, target: 2 })
        );
        assert_eq!(
            c.expected_hitting_times(8),
            Err(MarkovChainError::StateOutOfRange { index: 8, bound: 8 })
        );
        let one = chain(&[&[(1, 1)]]);
        assert_eq!(one.expected_hitting_times(0).unwrap(), vec![ri(0)]);
        assert_eq!(one.expected_return_time(0).unwrap(), ri(1));
    }

    #[test]
    fn the_time_reversal_needs_a_positive_stationary_law() {
        let c = chain(&[&[(1, 2), (1, 2)], &[(1, 3), (2, 3)]]);
        let pi = c.stationary_distribution().unwrap();
        assert_eq!(pi.probs(), &[rq(2, 5), rq(3, 5)]);
        let not_stationary = ProbabilitySimplex::try_new(vec![rq(1, 2), rq(1, 2)]).unwrap();
        assert!(matches!(
            c.time_reversal(&not_stationary),
            Err(MarkovChainError::Probability(
                ClassicalShadowError::RowNotNormalized { .. }
            ))
        ));
        let dirac = ProbabilitySimplex::try_new(vec![ri(1), ri(0)]).unwrap();
        assert_eq!(
            c.time_reversal(&dirac),
            Err(MarkovChainError::Probability(
                ClassicalShadowError::ZeroMass { index: 1 }
            ))
        );
        let wrong_size = ProbabilitySimplex::try_new(vec![rq(1, 3); 3]).unwrap();
        assert!(c.time_reversal(&wrong_size).is_err());
        assert!(c.is_reversible_with(&wrong_size).is_err());
    }

    #[test]
    fn step_counts_above_the_exact_limit_are_refused() {
        let c = chain(&[&[(1, 2), (1, 2)], &[(1, 3), (2, 3)]]);
        assert_eq!(
            c.distance_profile(MAX_EXACT_STEPS + 1),
            Err(MarkovChainError::LimitExceeded {
                what: "mixing steps",
                requested: (MAX_EXACT_STEPS + 1) as usize,
                limit: MAX_EXACT_STEPS as usize
            })
        );
        let start = ProbabilitySimplex::try_new(vec![ri(1), ri(0)]).unwrap();
        assert!(matches!(
            c.distribution_after(&start, MAX_EXACT_STEPS + 1),
            Err(MarkovChainError::LimitExceeded { .. })
        ));
        assert_eq!(c.distribution_after(&start, 0).unwrap(), start);
        assert_eq!(
            c.distribution_after(&start, 1).unwrap().probs(),
            &[rq(1, 2), rq(1, 2)]
        );
    }
}
