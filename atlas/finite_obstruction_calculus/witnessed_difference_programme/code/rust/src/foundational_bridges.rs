// Executable finite evidence; AuthorityEffect: None.
//! # Bounded Executable Witnesses for the 11 WDP Foundational Bridges
//!
//! Sovereign, hermetic Rust implementation mirroring `foundational_bridges.py`.
//! All operations operate with exact arithmetic, zero floating-point leakage, and AuthorityEffect: None.

use num_rational::BigRational;
use num_traits::Zero;
use serde::{Deserialize, Serialize};
use std::collections::{HashMap, HashSet};

use crate::error::WdpError;

// ---------------------------------------------------------------------------
// Bridge 1: Inscription <> -> Distinct Admitted Marks
// ---------------------------------------------------------------------------

#[derive(Debug, Clone, Copy, PartialEq, Eq, Hash, Serialize, Deserialize)]
pub struct Inscription {
    pub depth: usize,
}

impl Inscription {
    pub const fn new(depth: usize) -> Self {
        Self { depth }
    }

    pub const fn nest(&self) -> Self {
        Self {
            depth: self.depth + 1,
        }
    }
}

pub const fn empty_inscription() -> Inscription {
    Inscription::new(0)
}

pub fn admit_mark(inscription: Inscription) -> String {
    format!("mark_{}", inscription.depth)
}

pub fn apartness_witness(m1: Inscription, m2: Inscription) -> Result<bool, WdpError> {
    if m1.depth != m2.depth {
        Ok(true)
    } else {
        Err(WdpError::Refusal {
            reason: "inscriptions are identical; no distinction witnessed".to_string(),
        })
    }
}

// ---------------------------------------------------------------------------
// Bridge 2: Marks -> Algebra, Cochains, and Quotients
// ---------------------------------------------------------------------------

pub const fn bool_xor(x: bool, y: bool) -> bool {
    (x && !y) || (!x && y)
}

pub fn bool_d0<F>(f: F, u: &str, v: &str) -> bool
where
    F: Fn(&str) -> bool,
{
    bool_xor(f(u), f(v))
}

pub fn bool_d1<E>(e: E, a: &str, b: &str, c: &str) -> bool
where
    E: Fn(&str, &str) -> bool,
{
    bool_xor(bool_xor(e(a, b), e(b, c)), e(a, c))
}

pub fn verify_triangle_coboundary_zero<F>(f: F, a: &str, b: &str, c: &str) -> Result<bool, WdpError>
where
    F: Fn(&str) -> bool,
{
    let e = |u: &str, v: &str| bool_d0(&f, u, v);
    let coboundary = bool_d1(e, a, b, c);
    if !coboundary {
        Ok(true)
    } else {
        Err(WdpError::Refusal {
            reason: "binary triangle coboundary was non-zero".to_string(),
        })
    }
}

// ---------------------------------------------------------------------------
// Bridge 3: Genesis Histories -> Contextual Observers
// ---------------------------------------------------------------------------

#[derive(Debug, Clone, PartialEq, Eq, Serialize, Deserialize)]
pub struct FiniteTransducer {
    pub num_states: usize,
    pub num_inputs: usize,
    pub step_table: Vec<Vec<usize>>, // state x input -> next_state
}

impl FiniteTransducer {
    pub fn new(
        num_states: usize,
        num_inputs: usize,
        step_table: Vec<Vec<usize>>,
    ) -> Result<Self, WdpError> {
        if step_table.len() != num_states {
            return Err(WdpError::DimensionMismatch {
                expected: num_states,
                actual: step_table.len(),
            });
        }
        for (s, row) in step_table.iter().enumerate() {
            if row.len() != num_inputs {
                return Err(WdpError::DimensionMismatch {
                    expected: num_inputs,
                    actual: row.len(),
                });
            }
            for &ns in row {
                if ns >= num_states {
                    return Err(WdpError::InvalidInput {
                        detail: format!(
                            "target state {} out of range [0, {}) from state {}",
                            ns, num_states, s
                        ),
                    });
                }
            }
        }
        Ok(Self {
            num_states,
            num_inputs,
            step_table,
        })
    }

    pub fn step(&self, state: usize, input: usize) -> Result<usize, WdpError> {
        if state >= self.num_states {
            return Err(WdpError::InvalidInput {
                detail: format!("state {} out of range [0, {})", state, self.num_states),
            });
        }
        if input >= self.num_inputs {
            return Err(WdpError::InvalidInput {
                detail: format!("input {} out of range [0, {})", input, self.num_inputs),
            });
        }
        Ok(self.step_table[state][input])
    }
}

pub fn product_transducer(
    t1: &FiniteTransducer,
    t2: &FiniteTransducer,
) -> Result<FiniteTransducer, WdpError> {
    let prod_states = t1.num_states * t2.num_states;
    let prod_inputs = t1.num_inputs * t2.num_inputs;
    let mut table = Vec::with_capacity(prod_states);

    for s in 0..prod_states {
        let s1 = s / t2.num_states;
        let s2 = s % t2.num_states;
        let mut row = Vec::with_capacity(prod_inputs);
        for i in 0..prod_inputs {
            let i1 = i / t2.num_inputs;
            let i2 = i % t2.num_inputs;
            let ns1 = t1.step(s1, i1)?;
            let ns2 = t2.step(s2, i2)?;
            row.push(ns1 * t2.num_states + ns2);
        }
        table.push(row);
    }

    FiniteTransducer::new(prod_states, prod_inputs, table)
}

// ---------------------------------------------------------------------------
// Bridge 4: Observers -> Probability and Physical Adapters
// ---------------------------------------------------------------------------

#[derive(Debug, Clone, PartialEq, Eq, Serialize, Deserialize)]
pub struct MultiplicityDistribution {
    pub counts: HashMap<String, u64>,
    pub total: u64,
}

impl MultiplicityDistribution {
    pub fn from_counts(counts: HashMap<String, u64>) -> Result<Self, WdpError> {
        let total = counts.values().try_fold(0_u64, |total, count| total.checked_add(*count))
            .ok_or_else(|| WdpError::InvalidInput { detail: "event multiplicity total exceeds u64".into() })?;
        if total == 0 {
            return Err(WdpError::Refusal {
                reason: "total count must be positive".to_string(),
            });
        }
        Ok(Self { counts, total })
    }

    pub fn probability(&self, event: &str) -> BigRational {
        let count = self.counts.get(event).copied().unwrap_or(0);
        BigRational::new(count.into(), self.total.into())
    }

    pub fn disjoint_union_probability<S, I>(&self, events: I) -> Result<BigRational, WdpError>
    where
        S: AsRef<str>,
        I: IntoIterator<Item = S>,
    {
        let mut seen = HashSet::new();
        let mut sum = BigRational::zero();

        for e in events {
            let s = e.as_ref();
            if !seen.insert(s.to_string()) {
                return Err(WdpError::Refusal {
                    reason: format!("duplicate event in disjoint union: {}", s),
                });
            }
            sum += self.probability(s);
        }

        Ok(sum)
    }
}

// ---------------------------------------------------------------------------
// Bridge 5: Reports -> Evaluation
// ---------------------------------------------------------------------------

#[derive(Debug, Clone, Copy, PartialEq, Eq, Serialize, Deserialize)]
pub enum EvaluationStatus {
    Accept,
    Reject,
    Refuse,
    OutsideProfile,
}

pub const fn evaluate_report_claim(in_profile: bool, evidence_valid: bool) -> EvaluationStatus {
    if !in_profile {
        EvaluationStatus::OutsideProfile
    } else if evidence_valid {
        EvaluationStatus::Accept
    } else {
        EvaluationStatus::Reject
    }
}

// ---------------------------------------------------------------------------
// Bridge 6: Evaluation / Proposals -> Authorization
// ---------------------------------------------------------------------------

#[derive(Debug, Clone, Copy, PartialEq, Eq, Serialize, Deserialize)]
pub enum AuthorityEffect {
    None,
    MintsAuthority,
}

#[derive(Debug, Clone, PartialEq, Eq, Serialize, Deserialize)]
pub struct MathematicalReceipt {
    pub receipt_id: String,
    pub claim_id: String,
    pub verified: bool,
    pub authority_effect: AuthorityEffect,
}

pub fn check_no_authority_effect(receipt: &MathematicalReceipt) -> Result<bool, WdpError> {
    if matches!(receipt.authority_effect, AuthorityEffect::None) {
        Ok(true)
    } else {
        Err(WdpError::Refusal {
            reason: "receipt attempted authority leakage".to_string(),
        })
    }
}

// ---------------------------------------------------------------------------
// Bridge 7: Binary Carrier vs. General Triangle Parity Law
// ---------------------------------------------------------------------------

pub fn compute_triangle_mark_differences(marks: (&str, &str, &str)) -> (bool, bool, bool, bool) {
    let (a, b, c) = marks;
    let d_ab = a != b;
    let d_bc = b != c;
    let d_ac = a != c;
    let parity = bool_xor(bool_xor(d_ab, d_bc), d_ac);
    (d_ab, d_bc, d_ac, parity)
}

// ---------------------------------------------------------------------------
// Bridge 8: Arbitrary-Norm Rational Attainment
// ---------------------------------------------------------------------------

pub fn rational_l1_norm(point: &[BigRational]) -> BigRational {
    omega_functional::Phi1Functional::unweighted_l1_rational(point)
        .expect("exact rational coordinates")
}

pub fn find_rational_l1_minimizer(
    points: &[Vec<BigRational>],
) -> Result<(Vec<BigRational>, BigRational), WdpError> {
    if points.is_empty() {
        return Err(WdpError::Refusal {
            reason: "points set cannot be empty".to_string(),
        });
    }

    let mut min_pt = points[0].clone();
    let mut min_val = rational_l1_norm(&min_pt);

    for pt in &points[1..] {
        let val = rational_l1_norm(pt);
        if val < min_val {
            min_val = val;
            min_pt = pt.clone();
        }
    }

    Ok((min_pt, min_val))
}

// ---------------------------------------------------------------------------
// Bridge 9: Flat Locus Invariance under Graded Perturbations
// ---------------------------------------------------------------------------

pub fn verify_flat_locus_curvature(d_op: &[Vec<BigRational>]) -> Result<bool, WdpError> {
    let dim = d_op.len();
    for row in d_op {
        if row.len() != dim {
            return Err(WdpError::DimensionMismatch {
                expected: dim,
                actual: row.len(),
            });
        }
    }

    // Compute d^2 = d * d
    for i in 0..dim {
        for j in 0..dim {
            let mut sum = BigRational::zero();
            for k in 0..dim {
                sum += &d_op[i][k] * &d_op[k][j];
            }
            if !sum.is_zero() {
                return Err(WdpError::Refusal {
                    reason: format!("d^2 is not zero at ({}, {}); non-flat curvature", i, j),
                });
            }
        }
    }

    Ok(true)
}

// ---------------------------------------------------------------------------
// Bridge 10: Cover Marginals vs. Global Hidden Variables
// ---------------------------------------------------------------------------

pub fn solve_frustrated_spin_cycle(num_nodes: usize) -> Result<HashMap<String, bool>, WdpError> {
    if num_nodes % 2 != 0 {
        return Err(WdpError::Refusal {
            reason: format!(
                "odd cycle of length {} is frustrated; no global binary assignment exists",
                num_nodes
            ),
        });
    }

    let mut assignment = HashMap::with_capacity(num_nodes);
    for i in 0..num_nodes {
        assignment.insert(format!("s_{}", i), i % 2 == 1);
    }

    Ok(assignment)
}

// ---------------------------------------------------------------------------
// Bridge 11: Deterministic Retention vs. Branching Observer Packets
// ---------------------------------------------------------------------------

pub fn verify_deterministic_retention(
    transitions: &[(&str, &str, &str)],
) -> Result<bool, WdpError> {
    let mut table: HashMap<(&str, &str), &str> = HashMap::new();

    for &(src, inp, dst) in transitions {
        let key = (src, inp);
        if let Some(&existing_dst) = table.get(&key) {
            if existing_dst != dst {
                return Err(WdpError::Refusal {
                    reason: format!(
                        "branching detected: input {:?} from state {:?} has multiple destinations: {:?} and {:?}",
                        inp, src, existing_dst, dst
                    ),
                });
            }
        } else {
            table.insert(key, dst);
        }
    }

    Ok(true)
}
