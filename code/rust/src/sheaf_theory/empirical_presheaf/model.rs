
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

pub const KERNEL_SUPPORT_PRESHEAF: &str = "support presheaf over the maximal-context cover";

#[derive(Debug, Clone, PartialEq, Eq)]
pub struct Scenario {
    pub(super) arities: Vec<usize>,
    pub(super) contexts: Vec<Vec<usize>>,
}

pub type Cochain0 = Vec<Vec<Q>>;
pub type Cochain1 = BTreeMap<(usize, usize), Vec<Q>>;
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

    pub fn index_of(&self, positions: &[usize], assignment: &[usize]) -> usize {
        positions
            .iter()
            .zip(assignment)
            .fold(0, |acc, (&p, &a)| acc * self.arities[p] + a)
    }

    pub fn assignment_of(&self, positions: &[usize], index: usize) -> Vec<usize> {
        let mut rest = index;
        let mut out = vec![0; positions.len()];
        for (slot, &p) in positions.iter().enumerate().rev() {
            out[slot] = rest % self.arities[p];
            rest /= self.arities[p];
        }
        out
    }

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

    pub fn nerve_pairs(&self) -> Vec<(usize, usize)> {
        let n = self.contexts.len();
        (0..n)
            .flat_map(|i| (i + 1..n).map(move |j| (i, j)))
            .filter(|&(i, j)| self.context_mask(i) & self.context_mask(j) != 0)
            .collect()
    }

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

    fn zero_cochain0(&self) -> Result<Cochain0, EmpiricalError> {
        self.contexts
            .iter()
            .map(|c| Ok(vec![Q::zero(); self.section_count(c)?]))
            .collect()
    }

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

    pub fn flatten1(&self, cochain: &Cochain1) -> Result<Vec<Q>, EmpiricalError> {
        self.check1(cochain)?;
        let mut out = Vec::new();
        for pair in self.nerve_pairs() {
            let value = cochain.get(&pair).ok_or(EmpiricalError::Shape)?;
            out.extend(value.iter().cloned());
        }
        Ok(out)
    }

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

    pub fn delta0_matrix(&self) -> Result<Vec<Vec<Q>>, EmpiricalError> {
        let columns = self.delta0_generators()?;
        let height = columns.first().map_or(0, Vec::len);
        Ok((0..height)
            .map(|i| columns.iter().map(|c| c[i].clone()).collect())
            .collect())
    }

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

#[derive(Debug, Clone, PartialEq, Eq)]
pub struct SignallingWitness {
    pub left: usize,
    pub right: usize,
    pub overlap: Vec<usize>,
    pub left_marginal: Vec<Q>,
    pub right_marginal: Vec<Q>,
}

#[derive(Debug, Clone, PartialEq, Eq)]
pub struct EmpiricalModel {
    scenario: Scenario,
    distributions: Vec<Vec<Q>>,
}

#[derive(Debug, Clone, PartialEq, Eq)]
pub struct NoncontextualFractionReceipt {
    pub noncontextual_fraction: Q,
    pub contextual_fraction: Q,
    pub noncontextual_part: Vec<Q>,
    pub bell_functional: Vec<Q>,
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

    pub fn marginal(&self, context: usize, sub: &[usize]) -> Result<Vec<Q>, EmpiricalError> {
        let positions = self
            .scenario
            .contexts
            .get(context)
            .ok_or(EmpiricalError::Context { index: context })?;
        self.scenario
            .marginalize(positions, &self.distributions[context], sub)
    }

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

    pub fn cochain(&self) -> Cochain0 {
        self.distributions.clone()
    }

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

    fn global_limit(&self) -> Result<usize, EmpiricalError> {
        self.scenario.section_count(&self.scenario.all_positions())
    }

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

    pub fn is_strongly_contextual(&self) -> Result<bool, EmpiricalError> {
        Ok(self.global_support()?.is_empty())
    }

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

    pub fn l1_defect(&self, pivots: usize) -> Result<L1DefectReceipt, EmpiricalError> {
        let (rows, e) = self.incidence()?;
        l1_distance_to_convex_hull(&Self::columns(&rows), &e, pivots)
    }

    pub fn verify_l1_defect(&self, receipt: &L1DefectReceipt) -> bool {
        match self.incidence() {
            Ok((rows, e)) => verify_l1_defect_receipt(&Self::columns(&rows), &e, receipt),
            Err(_) => false,
        }
    }

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
