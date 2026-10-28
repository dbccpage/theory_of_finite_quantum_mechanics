
use std::collections::BTreeSet;

use num_rational::BigRational;
use num_traits::{Signed, Zero};
use engine_functional::phi1::{ExactPhi1Certificate, Phi1Functional};
use serde::{Deserialize, Serialize};
use sha2::{Digest, Sha256};

use crate::legacy_observer_adapters::SourceCustody;

type Matrix = Vec<Vec<BigRational>>;

#[derive(Debug, Clone, PartialEq, Eq)]
pub enum PolicyAdapterError {
    InvalidSourceBinding,
    InvalidCarrier,
    InvalidComparisonDomain,
    InvalidRepairOperator,
    InvalidNormBridge,
    InvalidGaugeAction,
    GaugeNotAGroup,
    GaugeDoesNotPreserveProblem,
    InvalidTerminalRules,
    CertificateProblemMismatch,
    InvalidCertificate,
    Serialization,
}

#[derive(Debug, Clone, PartialEq, Eq, Serialize, Deserialize)]
pub struct PolicyCarrier {
    pub names: Vec<String>,
    pub coordinates: Vec<String>,
    pub values: Matrix,
}

#[derive(Debug, Clone, PartialEq, Eq, Serialize, Deserialize)]
pub struct PolicyComparisonDomain {
    pub names: Vec<String>,
    pub pairs: Vec<[usize; 2]>,
    pub restrictions: Vec<Matrix>,
}

#[derive(Debug, Clone, PartialEq, Eq, Serialize, Deserialize)]
pub struct SignedPermutation {
    pub image: Vec<usize>,
    pub signs: Vec<i8>,
}
impl SignedPermutation {
    pub fn identity(size: usize) -> Self {
        Self {
            image: (0..size).collect(),
            signs: vec![1; size],
        }
    }
    fn valid(&self, size: usize) -> bool {
        permutation(&self.image, size)
            && self.signs.len() == size
            && self.signs.iter().all(|&s| s == 1 || s == -1)
    }
    fn apply(&self, input: &[BigRational]) -> Vec<BigRational> {
        let mut output = vec![BigRational::zero(); input.len()];
        for (i, value) in input.iter().enumerate() {
            output[self.image[i]] = if self.signs[i] == 1 {
                value.clone()
            } else {
                -value
            };
        }
        output
    }
    fn then(&self, next: &Self) -> Self {
        Self {
            image: self.image.iter().map(|&i| next.image[i]).collect(),
            signs: self
                .image
                .iter()
                .enumerate()
                .map(|(i, &j)| self.signs[i] * next.signs[j])
                .collect(),
        }
    }
}

#[derive(Debug, Clone, PartialEq, Eq, Serialize, Deserialize)]
pub struct PolicyGaugeAction {
    pub states: Vec<usize>,
    pub comparisons: Vec<usize>,
    pub defects: SignedPermutation,
    pub repairs: SignedPermutation,
}
impl PolicyGaugeAction {
    pub fn identity(states: usize, comparisons: usize, defects: usize, repairs: usize) -> Self {
        Self {
            states: (0..states).collect(),
            comparisons: (0..comparisons).collect(),
            defects: SignedPermutation::identity(defects),
            repairs: SignedPermutation::identity(repairs),
        }
    }
    fn then(&self, next: &Self) -> Self {
        Self {
            states: self.states.iter().map(|&i| next.states[i]).collect(),
            comparisons: self
                .comparisons
                .iter()
                .map(|&i| next.comparisons[i])
                .collect(),
            defects: self.defects.then(&next.defects),
            repairs: self.repairs.then(&next.repairs),
        }
    }
}

#[derive(Debug, Clone, PartialEq, Eq, Serialize, Deserialize)]
pub struct PolicyRepairOperator {
    pub coordinates: Vec<String>,
    pub map: Matrix,
}

#[derive(Debug, Clone, PartialEq, Eq, Serialize, Deserialize)]
pub struct PolicyTerminalRules {
    pub permitted_statuses: BTreeSet<String>,
    pub tolerance: BigRational,
    pub within_tolerance: String,
    pub above_tolerance: String,
}

#[derive(Debug, Clone, PartialEq, Eq)]
pub struct PolicyObserverProblem {
    pub carrier: PolicyCarrier,
    pub comparison_domain: PolicyComparisonDomain,
    pub gauge_group: Vec<PolicyGaugeAction>,
    pub repair: PolicyRepairOperator,
    pub terminal_rules: PolicyTerminalRules,
    pub norm_weights: Vec<BigRational>,
    pub source: SourceCustody,
}

fn names_valid(names: &[String], allow_empty: bool) -> bool {
    (allow_empty || !names.is_empty())
        && names.iter().all(|name| !name.is_empty())
        && names.iter().collect::<BTreeSet<_>>().len() == names.len()
}
fn permutation(values: &[usize], size: usize) -> bool {
    values.len() == size && values.iter().copied().collect::<BTreeSet<_>>() == (0..size).collect()
}
fn scalar_valid(value: &BigRational) -> bool {
    if value.denom() <= &0.into() {
        return false;
    }
    let normalized = BigRational::new(value.numer().clone(), value.denom().clone());
    normalized.numer() == value.numer() && normalized.denom() == value.denom()
}
fn matrix_valid(matrix: &Matrix, rows: usize, columns: usize) -> bool {
    matrix.len() == rows
        && matrix
            .iter()
            .all(|row| row.len() == columns && row.iter().all(scalar_valid))
}
fn apply_matrix(matrix: &Matrix, vector: &[BigRational]) -> Vec<BigRational> {
    matrix
        .iter()
        .map(|row| {
            row.iter()
                .zip(vector)
                .map(|(a, b)| a * b)
                .sum::<BigRational>()
        })
        .collect()
}
fn digest(value: &serde_json::Value) -> Result<String, PolicyAdapterError> {
    Ok(hex::encode(Sha256::digest(
        serde_json::to_vec(value).map_err(|_| PolicyAdapterError::Serialization)?,
    )))
}
fn problem_digest(problem: &PolicyObserverProblem) -> Result<String, PolicyAdapterError> {
    digest(&serde_json::json!({
        "kind": "wdp-policy-observer-problem-v1",
        "carrier": problem.carrier, "domain": problem.comparison_domain,
        "gauge_group": problem.gauge_group, "repair": problem.repair,
        "terminal_rules": problem.terminal_rules, "norm_weights": problem.norm_weights,
        "source": {"path": problem.source.path, "recorded_sha256": problem.source.recorded_sha256,
                   "receipts": problem.source.source_receipts, "authority_tags": problem.source.source_authority_tags}
    }))
}

#[derive(Debug, Clone, PartialEq, Eq)]
pub struct VerifiedPolicyObserver {
    problem: PolicyObserverProblem,
    defects: Matrix,
}
impl VerifiedPolicyObserver {
    pub fn try_new(problem: PolicyObserverProblem) -> Result<Self, PolicyAdapterError> {
        let c = &problem.carrier;
        let d = &problem.comparison_domain;
        let r = &problem.repair;
        let n = c.names.len();
        let m = c.coordinates.len();
        let queries = d.names.len();
        let repairs = r.coordinates.len();
        if problem.source.path.is_empty()
            || problem.source.recorded_sha256.len() != 64
            || !problem
                .source
                .recorded_sha256
                .bytes()
                .all(|b| b.is_ascii_hexdigit())
        {
            return Err(PolicyAdapterError::InvalidSourceBinding);
        }
        if !names_valid(&c.names, false)
            || !names_valid(&c.coordinates, false)
            || !matrix_valid(&c.values, n, m)
        {
            return Err(PolicyAdapterError::InvalidCarrier);
        }
        if !names_valid(&d.names, false)
            || d.pairs.len() != queries
            || d.restrictions.len() != queries
            || d.pairs.iter().flatten().any(|&i| i >= n)
            || d.restrictions.iter().any(|a| !matrix_valid(a, m, m))
        {
            return Err(PolicyAdapterError::InvalidComparisonDomain);
        }
        if !names_valid(&r.coordinates, true) || !matrix_valid(&r.map, m, repairs) {
            return Err(PolicyAdapterError::InvalidRepairOperator);
        }
        if problem.norm_weights.len() != m
            || problem
                .norm_weights
                .iter()
                .any(|w| !scalar_valid(w) || !w.is_positive())
        {
            return Err(PolicyAdapterError::InvalidNormBridge);
        }
        let t = &problem.terminal_rules;
        if t.permitted_statuses.is_empty()
            || t.permitted_statuses.iter().any(|s| s.is_empty())
            || !t.permitted_statuses.contains(&t.within_tolerance)
            || !t.permitted_statuses.contains(&t.above_tolerance)
            || !scalar_valid(&t.tolerance)
            || t.tolerance.is_negative()
        {
            return Err(PolicyAdapterError::InvalidTerminalRules);
        }
        let defects: Matrix = d
            .pairs
            .iter()
            .zip(&d.restrictions)
            .map(|(&[left, right], restriction)| {
                apply_matrix(restriction, &c.values[right])
                    .iter()
                    .zip(&c.values[left])
                    .map(|(a, b)| a - b)
                    .collect()
            })
            .collect();
        for g in &problem.gauge_group {
            if !permutation(&g.states, n)
                || !permutation(&g.comparisons, queries)
                || !g.defects.valid(m)
                || !g.repairs.valid(repairs)
            {
                return Err(PolicyAdapterError::InvalidGaugeAction);
            }
            for (i, &[left, right]) in d.pairs.iter().enumerate() {
                let j = g.comparisons[i];
                if d.pairs[j] != [g.states[left], g.states[right]]
                    || g.defects.apply(&defects[i]) != defects[j]
                {
                    return Err(PolicyAdapterError::GaugeDoesNotPreserveProblem);
                }
            }
            for i in 0..m {
                if problem.norm_weights[i] != problem.norm_weights[g.defects.image[i]] {
                    return Err(PolicyAdapterError::GaugeDoesNotPreserveProblem);
                }
                for j in 0..repairs {
                    let lhs = &r.map[i][j] * BigRational::from_integer(g.defects.signs[i].into());
                    let rhs = &r.map[g.defects.image[i]][g.repairs.image[j]]
                        * BigRational::from_integer(g.repairs.signs[j].into());
                    if lhs != rhs {
                        return Err(PolicyAdapterError::GaugeDoesNotPreserveProblem);
                    }
                }
            }
        }
        let identity = PolicyGaugeAction::identity(n, queries, m, repairs);
        if !problem.gauge_group.contains(&identity)
            || problem
                .gauge_group
                .iter()
                .enumerate()
                .any(|(i, g)| problem.gauge_group[..i].contains(g))
            || problem.gauge_group.iter().any(|g| {
                problem
                    .gauge_group
                    .iter()
                    .any(|h| !problem.gauge_group.contains(&g.then(h)))
            })
        {
            return Err(PolicyAdapterError::GaugeNotAGroup);
        }
        Ok(Self { problem, defects })
    }
    pub fn problem(&self) -> &PolicyObserverProblem {
        &self.problem
    }
    pub fn defects(&self) -> &[Vec<BigRational>] {
        &self.defects
    }
    pub fn evaluate(
        &self,
        comparison: usize,
        certificate: ExactPhi1Certificate,
    ) -> Result<PolicyEvaluationReceipt, PolicyAdapterError> {
        let actual = self
            .defects
            .get(comparison)
            .ok_or(PolicyAdapterError::InvalidComparisonDomain)?;
        let verified = Phi1Functional::verify_exact_certificate(certificate.clone())
            .map_err(|_| PolicyAdapterError::InvalidCertificate)?;
        if certificate.omega != *actual
            || certificate.d0 != self.problem.repair.map
            || certificate.weights != self.problem.norm_weights
            || certificate.alpha.len() != self.problem.repair.coordinates.len()
        {
            return Err(PolicyAdapterError::CertificateProblemMismatch);
        }
        let t = &self.problem.terminal_rules;
        let status = if verified.value() <= &t.tolerance {
            t.within_tolerance.clone()
        } else {
            t.above_tolerance.clone()
        };
        let mut receipt = PolicyEvaluationReceipt {
            problem_digest: problem_digest(&self.problem)?,
            comparison,
            comparison_name: self.problem.comparison_domain.names[comparison].clone(),
            defect: actual.clone(),
            value: verified.value().clone(),
            certificate,
            status,
            digest: String::new(),
        };
        receipt.refresh_digest()?;
        Ok(receipt)
    }
}

#[derive(Debug, Clone, PartialEq, Eq, Serialize, Deserialize)]
pub struct PolicyEvaluationReceipt {
    pub problem_digest: String,
    pub comparison: usize,
    pub comparison_name: String,
    pub defect: Vec<BigRational>,
    pub certificate: ExactPhi1Certificate,
    pub value: BigRational,
    pub status: String,
    pub digest: String,
}
impl PolicyEvaluationReceipt {
    pub fn refresh_digest(&mut self) -> Result<(), PolicyAdapterError> {
        let mut payload = self.clone();
        payload.digest.clear();
        self.digest = digest(&serde_json::json!({
            "kind": "wdp-policy-observer-evaluation-v1", "payload": payload
        }))?;
        Ok(())
    }
}

pub fn verify_policy_evaluation(
    actual: &PolicyObserverProblem,
    candidate: &PolicyEvaluationReceipt,
) -> Result<bool, PolicyAdapterError> {
    let observer = VerifiedPolicyObserver::try_new(actual.clone())?;
    if !scalar_valid(&candidate.value) || candidate.defect.iter().any(|q| !scalar_valid(q)) {
        return Ok(false);
    }
    Ok(observer.evaluate(candidate.comparison, candidate.certificate.clone())? == *candidate)
}
