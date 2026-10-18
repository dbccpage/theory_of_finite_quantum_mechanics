//! Measurement scenarios and the empirical models on their covers.

use std::collections::{BTreeMap, BTreeSet};

use num_traits::{One, Signed, Zero};
use omega_functional::phi1::VerifiedExactPhi1;
use omega_solvers::solver_cohomology_quotient_phi1::certified_phi1;
use omega_solvers::solver_lp_standard_form::{StandardLp, StandardLpError, StandardLpSolution};

use super::lp::{
    bound_dense, dot, l1_distance_to_convex_hull, too_large, verify_l1_defect_receipt,
    L1DefectReceipt,
};
use super::presheaf::AssignmentPresheaf;
use super::{mask, positions, EmpiricalError, MAX_GLOBAL_ASSIGNMENTS, Q};

/// Kernel label prefix of the support presheaf over the maximal-context
/// cover; [`Scenario::kernel_label`] completes it with the cover and the
/// arities of the scenario under evaluation.
pub const KERNEL_SUPPORT_PRESHEAF: &str = "support presheaf over the maximal-context cover";

/// A measurement scenario: outcome arities and a cover by maximal contexts.
#[derive(Debug, Clone, PartialEq, Eq)]
pub struct Scenario {
    pub(super) arities: Vec<usize>,
    pub(super) contexts: Vec<Vec<usize>>,
}

/// Čech 0-cochain: one vector over the joint outcomes of every maximal context.
pub type Cochain0 = Vec<Vec<Q>>;
/// Čech 1-cochain: one vector over the joint outcomes of every nonempty pairwise overlap.
pub type Cochain1 = BTreeMap<(usize, usize), Vec<Q>>;
/// Čech 2-cochain: one vector over the joint outcomes of every nonempty triple overlap.
pub type Cochain2 = BTreeMap<(usize, usize, usize), Vec<Q>>;

impl Scenario {
    pub fn new(arities: Vec<usize>, contexts: Vec<Vec<usize>>) -> Result<Self, EmpiricalError> {
        let n = arities.len();
        if n == 0 || n > 64 {
            return Err(EmpiricalError::CarrierSize);
        }
        if let Some(measurement) = (0..n).find(|&m| arities[m] < 2) {
            return Err(EmpiricalError::Arity { measurement });
        }
        for (index, context) in contexts.iter().enumerate() {
            let sorted = context.windows(2).all(|w| w[0] < w[1]);
            if context.is_empty() || !sorted || context.iter().any(|&m| m >= n) {
                return Err(EmpiricalError::Context { index });
            }
        }
        let masks: Vec<u64> = contexts
            .iter()
            .map(|c| mask(c))
            .collect::<Result<Vec<_>, _>>()?;
        for index in 0..masks.len() {
            for other in 0..masks.len() {
                if index != other && masks[index] & masks[other] == masks[index] {
                    return Err(EmpiricalError::NonMaximalContext { index, other });
                }
            }
        }
        if masks.iter().fold(0, |m, &c| m | c) != Self::full_of(n) {
            return Err(EmpiricalError::CarrierSize);
        }
        Ok(Self { arities, contexts })
    }

    /// Binary measurements only.
    pub fn binary(measurements: usize, contexts: Vec<Vec<usize>>) -> Result<Self, EmpiricalError> {
        Self::new(vec![2; measurements], contexts)
    }

    pub(super) fn full_of(n: usize) -> u64 {
        if n == 64 {
            u64::MAX
        } else {
            (1u64 << n) - 1
        }
    }

    pub fn measurement_count(&self) -> usize {
        self.arities.len()
    }

    pub fn arities(&self) -> &[usize] {
        &self.arities
    }

    pub fn contexts(&self) -> &[Vec<usize>] {
        &self.contexts
    }

    pub fn context_mask(&self, index: usize) -> u64 {
        mask(&self.contexts[index]).expect("scenario context positions fit in 64 bits")
    }

    pub fn full_mask(&self) -> u64 {
        Self::full_of(self.arities.len())
    }

    pub fn all_positions(&self) -> Vec<usize> {
        (0..self.arities.len()).collect()
    }

    /// Number of joint outcomes on a position list, folded with checked
    /// multiplication against [`MAX_GLOBAL_ASSIGNMENTS`]. The ceiling is
    /// enforced inside the fold, so the product can neither wrap nor be
    /// compared after the fact: an oversized carrier is refused here, before
    /// any caller allocates or enumerates it.
    pub fn section_count(&self, positions: &[usize]) -> Result<usize, EmpiricalError> {
        positions.iter().try_fold(1usize, |acc, &p| {
            let arity = *self.arities.get(p).ok_or(EmpiricalError::Shape)?;
            acc.checked_mul(arity)
                .filter(|&count| count <= MAX_GLOBAL_ASSIGNMENTS)
                .ok_or(EmpiricalError::EnumerationLimit {
                    limit: MAX_GLOBAL_ASSIGNMENTS,
                })
        })
    }

    /// Subset walks on `positions` run only when the product of `(1 + arity_i)`
    /// fits in [`MAX_GLOBAL_ASSIGNMENTS`]. The product uses `checked_mul` and
    /// is not `1 << width`, so a wide binary window is refused before the
    /// power set is built.
    fn subset_window_fits(&self, positions: &[usize]) -> Result<(), EmpiricalError> {
        positions.iter().try_fold(
            1usize,
            |acc, &measurement| -> Result<usize, EmpiricalError> {
                let arity = *self.arities.get(measurement).ok_or(EmpiricalError::Shape)?;
                let factor = arity.checked_add(1).ok_or(EmpiricalError::EnumerationLimit {
                    limit: MAX_GLOBAL_ASSIGNMENTS,
                })?;
                acc.checked_mul(factor)
                    .filter(|&count| count <= MAX_GLOBAL_ASSIGNMENTS)
                    .ok_or(EmpiricalError::EnumerationLimit {
                        limit: MAX_GLOBAL_ASSIGNMENTS,
                    })
            },
        )?;
        Ok(())
    }

    /// The kernel label an observer declares to evaluate a model on this
    /// scenario: the support presheaf over this cover with these arities. A
    /// bare phrase names no carrier, so the label spells the cover out.
    pub fn kernel_label(&self) -> String {
        let cover = self
            .contexts
            .iter()
            .map(|c| {
                let inner = c.iter().map(usize::to_string).collect::<Vec<_>>().join(",");
                format!("{{{inner}}}")
            })
            .collect::<Vec<_>>()
            .join("|");
        let arities = self
            .arities
            .iter()
            .map(usize::to_string)
            .collect::<Vec<_>>()
            .join(",");
        format!("{KERNEL_SUPPORT_PRESHEAF} {cover} with arities {arities}")
    }

    /// Mixed-radix index of a joint outcome, first position most significant.
    pub fn index_of(&self, positions: &[usize], assignment: &[usize]) -> usize {
        positions
            .iter()
            .zip(assignment)
            .fold(0, |acc, (&p, &a)| acc * self.arities[p] + a)
    }

    /// Inverse of [`Scenario::index_of`].
    pub fn assignment_of(&self, positions: &[usize], index: usize) -> Vec<usize> {
        let mut rest = index;
        let mut out = vec![0; positions.len()];
        for (slot, &p) in positions.iter().enumerate().rev() {
            out[slot] = rest % self.arities[p];
            rest /= self.arities[p];
        }
        out
    }

    /// Restrict a joint outcome on `positions` to the sub-list `sub`; `None`
    /// when `sub` is not contained in `positions` or the outcome is short.
    pub fn restrict(
        positions: &[usize],
        assignment: &[usize],
        sub: &[usize],
    ) -> Option<Vec<usize>> {
        sub.iter()
            .map(|s| {
                positions
                    .iter()
                    .position(|p| p == s)
                    .and_then(|i| assignment.get(i).copied())
            })
            .collect()
    }

    fn restrict_checked(
        positions: &[usize],
        assignment: &[usize],
        sub: &[usize],
    ) -> Result<Vec<usize>, EmpiricalError> {
        Self::restrict(positions, assignment, sub).ok_or(EmpiricalError::Shape)
    }

    /// The restriction map of the distribution presheaf: marginalisation.
    pub fn marginalize(
        &self,
        positions: &[usize],
        dist: &[Q],
        sub: &[usize],
    ) -> Result<Vec<Q>, EmpiricalError> {
        if dist.len() != self.section_count(positions)? {
            return Err(EmpiricalError::Shape);
        }
        let mut out = vec![Q::zero(); self.section_count(sub)?];
        for (index, weight) in dist.iter().enumerate() {
            let assignment = self.assignment_of(positions, index);
            let target = self.index_of(sub, &Self::restrict_checked(positions, &assignment, sub)?);
            out[target] += weight;
        }
        Ok(out)
    }

    fn overlap(&self, i: usize, j: usize) -> Vec<usize> {
        positions(self.context_mask(i) & self.context_mask(j))
    }

    /// Pairs of the nerve: distinct contexts with nonempty overlap.
    pub fn nerve_pairs(&self) -> Vec<(usize, usize)> {
        let n = self.contexts.len();
        (0..n)
            .flat_map(|i| (i + 1..n).map(move |j| (i, j)))
            .filter(|&(i, j)| self.context_mask(i) & self.context_mask(j) != 0)
            .collect()
    }

    /// Triples of the nerve: distinct contexts with nonempty triple overlap.
    pub fn nerve_triples(&self) -> Vec<(usize, usize, usize)> {
        let n = self.contexts.len();
        let mut out = Vec::new();
        for i in 0..n {
            for j in i + 1..n {
                for k in j + 1..n {
                    if self.context_mask(i) & self.context_mask(j) & self.context_mask(k) != 0 {
                        out.push((i, j, k));
                    }
                }
            }
        }
        out
    }

    /// A 0-cochain declares one vector per context, each of that context's
    /// section count. The whole declaration is checked before any incidence
    /// is read, so a context that meets no other context is still checked.
    fn check0(&self, cochain: &Cochain0) -> Result<(), EmpiricalError> {
        if cochain.len() != self.contexts.len() {
            return Err(EmpiricalError::Shape);
        }
        for (context, value) in self.contexts.iter().zip(cochain) {
            if value.len() != self.section_count(context)? {
                return Err(EmpiricalError::Shape);
            }
        }
        Ok(())
    }

    /// A 1-cochain declares exactly the nerve pairs, each with the section
    /// count of its overlap: no pair missing and none extraneous, whether or
    /// not the pair lies in a triple.
    fn check1(&self, cochain: &Cochain1) -> Result<(), EmpiricalError> {
        let pairs = self.nerve_pairs();
        if cochain.len() != pairs.len() {
            return Err(EmpiricalError::Shape);
        }
        for (i, j) in pairs {
            let value = cochain.get(&(i, j)).ok_or(EmpiricalError::Shape)?;
            if value.len() != self.section_count(&self.overlap(i, j))? {
                return Err(EmpiricalError::Shape);
            }
        }
        Ok(())
    }

    /// The zero 0-cochain, one zero vector per context.
    fn zero_cochain0(&self) -> Result<Cochain0, EmpiricalError> {
        self.contexts
            .iter()
            .map(|c| Ok(vec![Q::zero(); self.section_count(c)?]))
            .collect()
    }

    /// `delta0(alpha)_{ij} = alpha_j|_{ij} - alpha_i|_{ij}` on the nerve pairs.
    pub fn delta0(&self, cochain: &Cochain0) -> Result<Cochain1, EmpiricalError> {
        self.check0(cochain)?;
        let mut out = Cochain1::new();
        for (i, j) in self.nerve_pairs() {
            let overlap = self.overlap(i, j);
            let left = self.marginalize(&self.contexts[i], &cochain[i], &overlap)?;
            let right = self.marginalize(&self.contexts[j], &cochain[j], &overlap)?;
            let diff = right.iter().zip(&left).map(|(r, l)| r - l).collect();
            out.insert((i, j), diff);
        }
        Ok(out)
    }

    /// `delta1(beta)_{ijk} = beta_{jk} - beta_{ik} + beta_{ij}` restricted to the triple overlap.
    pub fn delta1(&self, cochain: &Cochain1) -> Result<Cochain2, EmpiricalError> {
        self.check1(cochain)?;
        let mut out = Cochain2::new();
        for (i, j, k) in self.nerve_triples() {
            let triple =
                positions(self.context_mask(i) & self.context_mask(j) & self.context_mask(k));
            let term = |a: usize, b: usize| -> Result<Vec<Q>, EmpiricalError> {
                let value = cochain.get(&(a, b)).ok_or(EmpiricalError::Shape)?;
                self.marginalize(&self.overlap(a, b), value, &triple)
            };
            let (jk, ik, ij) = (term(j, k)?, term(i, k)?, term(i, j)?);
            let value = (0..jk.len()).map(|t| &jk[t] - &ik[t] + &ij[t]).collect();
            out.insert((i, j, k), value);
        }
        Ok(out)
    }

    /// Flatten a 1-cochain in nerve-pair order.
    pub fn flatten1(&self, cochain: &Cochain1) -> Result<Vec<Q>, EmpiricalError> {
        self.check1(cochain)?;
        let mut out = Vec::new();
        for pair in self.nerve_pairs() {
            let value = cochain.get(&pair).ok_or(EmpiricalError::Shape)?;
            out.extend(value.iter().cloned());
        }
        Ok(out)
    }

    /// Columns spanning the image of `delta0`, in flattened 1-cochain coordinates.
    pub fn delta0_generators(&self) -> Result<Vec<Vec<Q>>, EmpiricalError> {
        let mut columns = Vec::new();
        for (i, context) in self.contexts.iter().enumerate() {
            for k in 0..self.section_count(context)? {
                let mut basis = self.zero_cochain0()?;
                basis[i][k] = Q::one();
                columns.push(self.flatten1(&self.delta0(&basis)?)?);
            }
        }
        Ok(columns)
    }

    /// Matrix of `delta0` in flattened coordinates: one row per 1-cochain
    /// coordinate, one column per 0-cochain coordinate.
    pub fn delta0_matrix(&self) -> Result<Vec<Vec<Q>>, EmpiricalError> {
        let columns = self.delta0_generators()?;
        let height = columns.first().map_or(0, Vec::len);
        Ok((0..height)
            .map(|i| columns.iter().map(|c| c[i].clone()).collect())
            .collect())
    }

    /// Graham–Yu–Özsoyoglu reduction. `Some(order)` lists `(context, parent)`
    /// in running-intersection order: each context meets the union of the
    /// earlier ones inside its parent. `None` means the cover is cyclic.
    pub fn join_tree(&self) -> Option<Vec<(usize, Option<usize>)>> {
        let n = self.contexts.len();
        let mut sets: Vec<u64> = (0..n).map(|i| self.context_mask(i)).collect();
        let mut alive = vec![true; n];
        let mut removed: Vec<(usize, Option<usize>)> = Vec::new();
        loop {
            let mut changed = false;
            for i in 0..n {
                if !alive[i] {
                    continue;
                }
                let others = (0..n)
                    .filter(|&j| alive[j] && j != i)
                    .fold(0, |m, j| m | sets[j]);
                let private = sets[i] & !others;
                if private != 0 {
                    sets[i] &= !private;
                    changed = true;
                }
            }
            let contained = (0..n).filter(|&i| alive[i]).find_map(|i| {
                (0..n)
                    .find(|&j| alive[j] && j != i && sets[i] & sets[j] == sets[i])
                    .map(|j| (i, j))
            });
            if let Some((i, j)) = contained {
                alive[i] = false;
                removed.push((i, Some(j)));
                changed = true;
            }
            if !changed {
                break;
            }
        }
        let survivors: Vec<usize> = (0..n).filter(|&i| alive[i]).collect();
        if survivors.len() != 1 {
            return None;
        }
        removed.push((survivors[0], None));
        removed.reverse();
        Some(removed)
    }

    pub fn is_gyo_acyclic(&self) -> bool {
        self.join_tree().is_some()
    }
}

/// First pair of contexts whose marginals disagree on their overlap.
#[derive(Debug, Clone, PartialEq, Eq)]
pub struct SignallingWitness {
    pub left: usize,
    pub right: usize,
    pub overlap: Vec<usize>,
    pub left_marginal: Vec<Q>,
    pub right_marginal: Vec<Q>,
}

/// An empirical model: one exact distribution per maximal context.
#[derive(Debug, Clone, PartialEq, Eq)]
pub struct EmpiricalModel {
    scenario: Scenario,
    distributions: Vec<Vec<Q>>,
}

/// The noncontextual-fraction LP receipt with its Bell-functional dual.
#[derive(Debug, Clone, PartialEq, Eq)]
pub struct NoncontextualFractionReceipt {
    pub noncontextual_fraction: Q,
    pub contextual_fraction: Q,
    /// Sub-probability weights over global assignments, in index order.
    pub noncontextual_part: Vec<Q>,
    /// Nonnegative functional over (context, local outcome) coordinates with
    /// `A^T beta >= 1` on every global assignment and `e . beta` the fraction.
    pub bell_functional: Vec<Q>,
    /// The standard-form solution. Replay rebuilds the LP, verifies
    /// `primal`, `dual` and `value` as its certificate and binds them to the
    /// part, the functional and the fraction. `lp.pivots` is the solver's
    /// pivot trace: it is carried for reproduction and is not bound by replay.
    pub lp: StandardLpSolution,
}

impl EmpiricalModel {
    pub fn new(scenario: Scenario, distributions: Vec<Vec<Q>>) -> Result<Self, EmpiricalError> {
        if distributions.len() != scenario.contexts.len() {
            return Err(EmpiricalError::Shape);
        }
        for (context, dist) in distributions.iter().enumerate() {
            if dist.len() != scenario.section_count(&scenario.contexts[context])? {
                return Err(EmpiricalError::Shape);
            }
            if dist.iter().any(|p| p.is_negative()) || dist.iter().sum::<Q>() != Q::one() {
                return Err(EmpiricalError::NotADistribution { context });
            }
        }
        Ok(Self {
            scenario,
            distributions,
        })
    }

    pub fn scenario(&self) -> &Scenario {
        &self.scenario
    }

    pub fn distributions(&self) -> &[Vec<Q>] {
        &self.distributions
    }

    /// Marginal of context `context` on the sorted sub-list `sub`.
    pub fn marginal(&self, context: usize, sub: &[usize]) -> Result<Vec<Q>, EmpiricalError> {
        let positions = self
            .scenario
            .contexts
            .get(context)
            .ok_or(EmpiricalError::Context { index: context })?;
        self.scenario
            .marginalize(positions, &self.distributions[context], sub)
    }

    /// Identity and composition of marginalisation on every chain `E ⊆ D ⊆ C`.
    pub fn restriction_is_functorial(&self) -> Result<bool, EmpiricalError> {
        for (c, context) in self.scenario.contexts.iter().enumerate() {
            self.scenario.subset_window_fits(context)?;
            let dist = &self.distributions[c];
            if self.scenario.marginalize(context, dist, context)? != *dist {
                return Ok(false);
            }
            let width = context.len();
            for d_bits in 0..1u64 << width {
                let d: Vec<usize> = (0..width)
                    .filter(|&t| d_bits >> t & 1 == 1)
                    .map(|t| context[t])
                    .collect();
                let via_d = self.scenario.marginalize(context, dist, &d)?;
                for e_bits in (0..1u64 << width).filter(|&e_bits| e_bits & d_bits == e_bits) {
                    let e: Vec<usize> = (0..width)
                        .filter(|&t| e_bits >> t & 1 == 1)
                        .map(|t| context[t])
                        .collect();
                    if self.scenario.marginalize(&d, &via_d, &e)?
                        != self.scenario.marginalize(context, dist, &e)?
                    {
                        return Ok(false);
                    }
                }
            }
        }
        Ok(true)
    }

    /// `None` exactly when `delta0(e) = 0`: the model is a presheaf.
    pub fn signalling_witness(&self) -> Result<Option<SignallingWitness>, EmpiricalError> {
        for (left, right) in self.scenario.nerve_pairs() {
            let overlap = self.scenario.overlap(left, right);
            let left_marginal = self.marginal(left, &overlap)?;
            let right_marginal = self.marginal(right, &overlap)?;
            if left_marginal != right_marginal {
                return Ok(Some(SignallingWitness {
                    left,
                    right,
                    overlap,
                    left_marginal,
                    right_marginal,
                }));
            }
        }
        Ok(None)
    }

    pub fn is_no_signalling(&self) -> Result<bool, EmpiricalError> {
        Ok(self.signalling_witness()?.is_none())
    }

    /// The model as a Čech 0-cochain.
    pub fn cochain(&self) -> Cochain0 {
        self.distributions.clone()
    }

    /// Indices of the supported joint outcomes of a context.
    pub fn support(&self, context: usize) -> Result<Vec<usize>, EmpiricalError> {
        Ok(self
            .distributions
            .get(context)
            .ok_or(EmpiricalError::Context { index: context })?
            .iter()
            .enumerate()
            .filter(|(_, p)| p.is_positive())
            .map(|(k, _)| k)
            .collect())
    }

    /// The global assignment count under the declared ceiling; the checked
    /// fold of [`Scenario::section_count`] is the whole of the check.
    fn global_limit(&self) -> Result<usize, EmpiricalError> {
        self.scenario.section_count(&self.scenario.all_positions())
    }

    /// Global assignments whose restriction to every context is supported:
    /// the global sections of the support presheaf.
    pub fn global_support(&self) -> Result<Vec<usize>, EmpiricalError> {
        let total = self.global_limit()?;
        let all = self.scenario.all_positions();
        let mut globals = Vec::new();
        for g in 0..total {
            let assignment = self.scenario.assignment_of(&all, g);
            let mut supported = true;
            for (c, context) in self.scenario.contexts.iter().enumerate() {
                let local = Scenario::restrict_checked(&all, &assignment, context)?;
                if !self.distributions[c][self.scenario.index_of(context, &local)].is_positive() {
                    supported = false;
                    break;
                }
            }
            if supported {
                globals.push(g);
            }
        }
        Ok(globals)
    }

    /// Strong contextuality: no global section of the support presheaf.
    pub fn is_strongly_contextual(&self) -> Result<bool, EmpiricalError> {
        Ok(self.global_support()?.is_empty())
    }

    /// A supported local outcome with no global extension in the support,
    /// as `(context, local index)`; logical contextuality is its existence.
    pub fn logical_contextuality_witness(&self) -> Result<Option<(usize, usize)>, EmpiricalError> {
        let globals = self.global_support()?;
        let all = self.scenario.all_positions();
        for (c, context) in self.scenario.contexts.iter().enumerate() {
            for k in self.support(c)? {
                let mut extends = false;
                for &g in &globals {
                    let assignment = self.scenario.assignment_of(&all, g);
                    let local = Scenario::restrict_checked(&all, &assignment, context)?;
                    if self.scenario.index_of(context, &local) == k {
                        extends = true;
                        break;
                    }
                }
                if !extends {
                    return Ok(Some((c, k)));
                }
            }
        }
        Ok(None)
    }

    /// Incidence matrix `A` (one row per (context, local outcome), one column
    /// per global assignment) and the flattened model vector `e`.
    pub fn incidence(&self) -> Result<(Vec<Vec<Q>>, Vec<Q>), EmpiricalError> {
        let total = self.global_limit()?;
        let mut height = 0usize;
        for context in &self.scenario.contexts {
            height = height
                .checked_add(self.scenario.section_count(context)?)
                .ok_or_else(too_large)?;
        }
        bound_dense(height, total)?;
        let all = self.scenario.all_positions();
        let mut rows = Vec::with_capacity(height);
        let mut e = Vec::with_capacity(height);
        for (c, context) in self.scenario.contexts.iter().enumerate() {
            for k in 0..self.scenario.section_count(context)? {
                let mut row = Vec::with_capacity(total);
                for g in 0..total {
                    let assignment = self.scenario.assignment_of(&all, g);
                    let local = Scenario::restrict_checked(&all, &assignment, context)?;
                    row.push(if self.scenario.index_of(context, &local) == k {
                        Q::one()
                    } else {
                        Q::zero()
                    });
                }
                rows.push(row);
                e.push(self.distributions[c][k].clone());
            }
        }
        Ok((rows, e))
    }

    fn columns(rows: &[Vec<Q>]) -> Vec<Vec<Q>> {
        let width = rows.first().map_or(0, Vec::len);
        (0..width)
            .map(|j| rows.iter().map(|r| r[j].clone()).collect())
            .collect()
    }

    /// Variables `(p, s)`, rows `A p + s = e`, cost `-sum p`: the
    /// noncontextual-fraction LP in standard form, built the same way by the
    /// solver and by the replay so a receipt's `lp` subrecord is verified
    /// against the LP it claims to solve.
    fn standard_form_ncf(rows: &[Vec<Q>], e: &[Q]) -> Result<StandardLp, EmpiricalError> {
        let (m, n) = (rows.len(), rows.first().map_or(0, Vec::len));
        let width = n.checked_add(m).ok_or_else(too_large)?;
        bound_dense(m, width)?;
        let matrix: Vec<Vec<Q>> = rows
            .iter()
            .enumerate()
            .map(|(i, row)| {
                let mut full = row.clone();
                full.extend((0..m).map(|j| if i == j { Q::one() } else { Q::zero() }));
                full
            })
            .collect();
        let costs = (0..width)
            .map(|j| if j < n { -Q::one() } else { Q::zero() })
            .collect();
        Ok(StandardLp::new(costs, matrix, e.to_vec())?)
    }

    /// Noncontextual fraction: `max sum(p)` with `A p <= e`, `p >= 0`, and its
    /// Bell-functional dual, certified by independent replay.
    pub fn noncontextual_fraction(
        &self,
        pivots: usize,
    ) -> Result<NoncontextualFractionReceipt, EmpiricalError> {
        let (rows, e) = self.incidence()?;
        let n = rows.first().map_or(0, Vec::len);
        let lp = Self::standard_form_ncf(&rows, &e)?;
        let solution = lp.solve(pivots)?;
        if !lp.verify(&solution) {
            return Err(EmpiricalError::Lp(StandardLpError::CertificateMismatch));
        }
        let receipt = NoncontextualFractionReceipt {
            noncontextual_fraction: -solution.value.clone(),
            contextual_fraction: Q::one() + &solution.value,
            noncontextual_part: solution.primal[..n].to_vec(),
            bell_functional: solution.dual.iter().map(|y| -y).collect(),
            lp: solution,
        };
        if self.verify_noncontextual_fraction(&receipt) {
            Ok(receipt)
        } else {
            Err(EmpiricalError::Lp(StandardLpError::CertificateMismatch))
        }
    }

    /// Replay of a noncontextual-fraction receipt against this model. The LP
    /// is rebuilt from the model and the embedded `lp` subrecord is verified
    /// as its certificate and bound to the part, the functional and the
    /// fraction, so a corrupted subrecord is refused, not carried along.
    pub fn verify_noncontextual_fraction(&self, receipt: &NoncontextualFractionReceipt) -> bool {
        let Ok((rows, e)) = self.incidence() else {
            return false;
        };
        let (m, n) = (rows.len(), rows.first().map_or(0, Vec::len));
        if receipt.noncontextual_part.len() != n || receipt.bell_functional.len() != m {
            return false;
        }
        let Ok(lp) = Self::standard_form_ncf(&rows, &e) else {
            return false;
        };
        if !lp.verify(&receipt.lp) {
            return false;
        }
        let lp_bound = receipt.lp.primal.len() == n + m
            && receipt.lp.dual.len() == m
            && receipt.lp.primal[..n] == receipt.noncontextual_part[..]
            && receipt
                .lp
                .dual
                .iter()
                .zip(&receipt.bell_functional)
                .all(|(y, b)| -y == *b);
        if !lp_bound {
            return false;
        }
        let part_ok = receipt.noncontextual_part.iter().all(|p| !p.is_negative())
            && receipt.noncontextual_part.iter().sum::<Q>() == receipt.noncontextual_fraction
            && rows
                .iter()
                .zip(&e)
                .all(|(row, bound)| dot(row, &receipt.noncontextual_part) <= *bound);
        let beta = &receipt.bell_functional;
        let functional_ok = beta.iter().all(|b| !b.is_negative())
            && Self::columns(&rows)
                .iter()
                .all(|column| dot(column, beta) >= Q::one())
            && dot(&e, beta) == receipt.noncontextual_fraction;
        let fraction_ok = &receipt.noncontextual_fraction + &receipt.contextual_fraction
            == Q::one()
            && receipt.lp.value == -receipt.noncontextual_fraction.clone();
        part_ok && functional_ok && fraction_ok
    }

    /// `min_{p in simplex} ||A p - e||_1`: the L1 distance of the model from
    /// the noncontextual polytope, with its dual witness.
    pub fn l1_defect(&self, pivots: usize) -> Result<L1DefectReceipt, EmpiricalError> {
        let (rows, e) = self.incidence()?;
        l1_distance_to_convex_hull(&Self::columns(&rows), &e, pivots)
    }

    /// Replay of an L1-defect receipt against this model.
    pub fn verify_l1_defect(&self, receipt: &L1DefectReceipt) -> bool {
        match self.incidence() {
            Ok((rows, e)) => verify_l1_defect_receipt(&Self::columns(&rows), &e, receipt),
            Err(_) => false,
        }
    }

    /// A signed measure on global assignments with the model's marginals, or
    /// `None` when the linear system is infeasible. Abramsky–Brandenburger
    /// (2011) show one exists for every no-signalling model, which is why the
    /// linear Čech obstruction does not detect probabilistic contextuality.
    pub fn signed_global_section(&self, pivots: usize) -> Result<Option<Vec<Q>>, EmpiricalError> {
        let (rows, e) = self.incidence()?;
        let n = rows.first().map_or(0, Vec::len);
        bound_dense(rows.len(), n.checked_mul(2).ok_or_else(too_large)?)?;
        let matrix: Vec<Vec<Q>> = rows
            .iter()
            .map(|row| {
                let mut full = row.clone();
                full.extend(row.iter().map(|x| -x));
                full
            })
            .collect();
        let width = n.checked_mul(2).ok_or_else(too_large)?;
        let lp = StandardLp::new(vec![Q::zero(); width], matrix, e)?;
        match lp.solve(pivots) {
            Ok(solution) if lp.verify(&solution) => Ok(Some(
                (0..n)
                    .map(|j| &solution.primal[j] - &solution.primal[n + j])
                    .collect(),
            )),
            Ok(_) => Err(EmpiricalError::Lp(StandardLpError::CertificateMismatch)),
            Err(StandardLpError::Infeasible) => Ok(None),
            Err(error) => Err(EmpiricalError::Lp(error)),
        }
    }

    /// Quotient evaluator on the Čech side: `Phi_1([omega]) = min_alpha
    /// ||omega - delta0 alpha||_1`, with `phi*` in `ker(delta0^T)` and
    /// `||phi*||_inf <= 1` at zero duality gap. The LP is proposed by
    /// `omega_solvers` and the certificate replayed by `omega_functional`.
    pub fn cech_quotient_defect(
        &self,
        omega: &Cochain1,
        pivots: usize,
    ) -> Result<VerifiedExactPhi1, EmpiricalError> {
        let d0 = self.scenario.delta0_matrix()?;
        let c0 = d0.first().map_or(0, Vec::len);
        let x = self.scenario.flatten1(omega)?;
        let weights = vec![Q::one(); x.len()];
        certified_phi1(c0, &d0, &x, &weights, pivots)
            .map_err(|error| EmpiricalError::CertifiedPhi1(error.to_string()))
    }

    /// Vorob'ev gluing on a GYO-acyclic cover: the product formula along the
    /// join tree yields a global distribution with the model's marginals.
    pub fn acyclic_global_section(&self) -> Result<Vec<Q>, EmpiricalError> {
        if !self.is_no_signalling()? {
            return Err(EmpiricalError::Signalling);
        }
        let order = self
            .scenario
            .join_tree()
            .ok_or(EmpiricalError::NotAcyclic)?;
        let total = self.global_limit()?;
        let all = self.scenario.all_positions();
        let mut seen: u64 = 0;
        let mut factors: Vec<(usize, Vec<usize>, Option<(usize, Vec<Q>)>)> = Vec::new();
        for (context, parent) in order {
            let separator = positions(self.scenario.context_mask(context) & seen);
            let denominator = match parent {
                Some(p) => Some((p, self.marginal(p, &separator)?)),
                None => None,
            };
            factors.push((context, separator, denominator));
            seen |= self.scenario.context_mask(context);
        }
        let mut global = vec![Q::zero(); total];
        for (g, slot) in global.iter_mut().enumerate() {
            let assignment = self.scenario.assignment_of(&all, g);
            let mut weight = Q::one();
            for (context, separator, denominator) in &factors {
                let positions_c = &self.scenario.contexts[*context];
                let local = Scenario::restrict_checked(&all, &assignment, positions_c)?;
                let numerator =
                    &self.distributions[*context][self.scenario.index_of(positions_c, &local)];
                weight *= numerator;
                if let Some((_, marginal)) = denominator {
                    let sep_value = Scenario::restrict_checked(&all, &assignment, separator)?;
                    let d = &marginal[self.scenario.index_of(separator, &sep_value)];
                    if d.is_zero() {
                        weight = Q::zero();
                    } else {
                        weight /= d;
                    }
                }
                if weight.is_zero() {
                    break;
                }
            }
            *slot = weight;
        }
        for (context, positions_c) in self.scenario.contexts.iter().enumerate() {
            if self.scenario.marginalize(&all, &global, positions_c)? != self.distributions[context]
            {
                return Err(EmpiricalError::ProductFormulaMismatch { context });
            }
        }
        Ok(global)
    }

    /// The locally admissible assignment presheaf: on a set `W` of
    /// measurements, the assignments whose restriction to every maximal
    /// context inside `W` is supported. Keys are the down-closure of the
    /// cover, `extra`, the carrier, the empty set, and all intersections.
    pub fn admissible_presheaf(&self, extra: &[u64]) -> Result<AssignmentPresheaf, EmpiricalError> {
        let mut keys: BTreeSet<u64> = extra.iter().copied().collect();
        for (i, context) in self.scenario.contexts.iter().enumerate() {
            self.scenario.subset_window_fits(context)?;
            let m = self.scenario.context_mask(i);
            let width = context.len();
            for bits in 0..1u64 << width {
                keys.insert(
                    (0..width)
                        .filter(|&t| bits >> t & 1 == 1)
                        .fold(0, |acc, t| acc | 1 << context[t]),
                );
            }
            keys.insert(m);
        }
        keys.insert(self.scenario.full_mask());
        let mut supports: Vec<BTreeSet<usize>> = Vec::new();
        for c in 0..self.scenario.contexts.len() {
            supports.push(self.support(c)?.into_iter().collect());
        }
        let scenario = self.scenario.clone();
        AssignmentPresheaf::from_rule(
            self.scenario.arities.clone(),
            &keys,
            move |window, assignment| {
                scenario.contexts.iter().enumerate().all(|(c, context)| {
                    let inside = match (mask(context), mask(window)) {
                        (Ok(context_bits), Ok(window_bits)) => {
                            context_bits & window_bits == context_bits
                        }
                        _ => false,
                    };
                    !inside
                        || Scenario::restrict(window, assignment, context).is_some_and(|local| {
                            supports[c].contains(&scenario.index_of(context, &local))
                        })
                })
            },
        )
    }
}
