
use num_bigint::BigInt;
use num_rational::BigRational;
use num_traits::{Signed, Zero};
use serde::{Deserialize, Serialize};
use sha2::{Digest, Sha256};
use std::collections::BTreeSet;

#[derive(Debug, Clone, PartialEq, Eq, Serialize, Deserialize)]
pub struct ProblemEdge {
    pub u: String,
    pub v: String,
    pub weight: BigRational,
}

#[derive(Debug, Clone, PartialEq, Eq, Serialize, Deserialize)]
pub struct SymbolGameProblem {
    pub problem_id: String,
    pub vertices: Vec<String>,
    pub edges: Vec<ProblemEdge>,
    pub initial_claims: Vec<BigRational>,
    pub digest: String,
}

impl SymbolGameProblem {
    pub fn new(
        problem_id: String,
        vertices: Vec<String>,
        edges: Vec<ProblemEdge>,
        initial_claims: Vec<BigRational>,
    ) -> Result<Self, HostRefusalCode> {
        if edges.len() != initial_claims.len()
            || vertices.iter().collect::<BTreeSet<_>>().len() != vertices.len()
            || edges
                .iter()
                .map(|e| (&e.u, &e.v))
                .collect::<BTreeSet<_>>()
                .len()
                != edges.len()
        {
            return Err(HostRefusalCode::FormatViolation);
        }
        let zero = BigRational::zero();
        for edge in &edges {
            if edge.u == edge.v || edge.weight <= zero {
                return Err(HostRefusalCode::FormatViolation);
            }
            if !vertices.contains(&edge.u) || !vertices.contains(&edge.v) {
                return Err(HostRefusalCode::FormatViolation);
            }
        }

        let digest = Self::calculate_problem_digest(&problem_id, &vertices, &edges, &initial_claims);

        Ok(Self {
            problem_id,
            vertices,
            edges,
            initial_claims,
            digest,
        })
    }

    pub fn calculate_problem_digest(
        problem_id: &str,
        vertices: &[String],
        edges: &[ProblemEdge],
        initial_claims: &[BigRational],
    ) -> String {
        let payload = serde_json::to_vec(&(
            "SYMBOL_GAME_PROBLEM_V1",
            problem_id,
            vertices,
            edges,
            initial_claims,
        ))
        .expect("serializable exact problem");
        let mut hasher = Sha256::new();
        hasher.update(payload);
        format!("{:x}", hasher.finalize())
    }

    pub fn compute_digest(&self) -> String {
        Self::calculate_problem_digest(
            &self.problem_id,
            &self.vertices,
            &self.edges,
            &self.initial_claims,
        )
    }
}

#[derive(Debug, Clone, Copy, PartialEq, Eq, PartialOrd, Ord, Serialize, Deserialize)]
pub enum HostMoveOp {
    Assert,
    Cut,
    Verify,
    Retract,
}

#[derive(Debug, Clone, PartialEq, Eq, Serialize, Deserialize)]
pub struct UntrustedProposal {
    pub proposer_id: String,
    pub problem_digest: String,
    pub parent_state_digest: String,
    pub op: HostMoveOp,
    pub proposed_section: Option<Vec<BigRational>>,
    pub dual_witness: Option<Vec<BigRational>>,
    pub target_property: Option<String>,
    pub target_event_id: Option<String>,
    pub claimed_post_state_digest: String,
    pub claimed_defect: Option<BigRational>,
    pub rationale: String,
}

#[derive(Debug, Clone, PartialEq, Eq, PartialOrd, Ord, thiserror::Error, Serialize, Deserialize)]
pub enum HostRefusalCode {
    #[error("Problem digest mismatch: expected {expected}, got {found}")]
    ProblemDigestMismatch { expected: String, found: String },

    #[error("Parent state digest mismatch: expected {expected}, got {found}")]
    ParentStateMismatch { expected: String, found: String },

    #[error("Monotonic defect descent violated: before {before}, after {after}")]
    DefectIncrease { before: String, after: String },

    #[error("Unlicensed problem mutation: problem equations and edge claims are immutable")]
    UnlicensedProblemMutation,

    #[error("Dual witness violates divergence condition B^T z = 0 at vertex {vertex}: divergence {divergence}")]
    DualNotPerpendicular { vertex: String, divergence: String },

    #[error("Dual witness exceeds edge weight at index {edge_index}: |{value}| > {weight}")]
    DualExceedsWeight {
        edge_index: usize,
        value: String,
        weight: String,
    },

    #[error("Duality gap detected: inner product <z, r> = {pairing} != defect norm {defect}")]
    DualityGapDetected { pairing: String, defect: String },

    #[error("Non-zero obstruction: defect is {defect}")]
    NonzeroObstruction { defect: String },

    #[error("Post-state digest mismatch: host computed {host_digest}, proposer claimed {claimed_digest}")]
    PostStateDigestMismatch {
        host_digest: String,
        claimed_digest: String,
    },

    #[error("Target event '{event_id}' not found in event ledger")]
    EventNotFound { event_id: String },

    #[error("Carrier codepoint violation in rationale")]
    CarrierViolation,

    #[error("Format or dimension violation")]
    FormatViolation,
}

#[derive(Debug, Clone, PartialEq, Eq, Serialize, Deserialize)]
pub struct VerifiedEvent {
    pub event_id: String,
    #[serde(default)]
    pub event_digest: String,
    pub parent_event_id: Option<String>,
    pub problem_digest: String,
    pub parent_state_digest: String,
    pub post_state_digest: String,
    pub op: HostMoveOp,
    pub verified_defect: BigRational,
    pub details: String,
    pub section_snapshot: Vec<BigRational>,
}

impl VerifiedEvent {
    pub fn calculate_event_digest(
        event_id: &str,
        parent_event_id: Option<&str>,
        problem_digest: &str,
        parent_state_digest: &str,
        post_state_digest: &str,
        op: HostMoveOp,
        verified_defect: &BigRational,
    ) -> String {
        let mut hasher = Sha256::new();
        hasher.update(b"SG_EVENT_V1:");
        hasher.update(event_id.as_bytes());
        hasher.update(b":PARENT_EVENT:");
        if let Some(p) = parent_event_id {
            hasher.update(p.as_bytes());
        }
        hasher.update(b":PROBLEM:");
        hasher.update(problem_digest.as_bytes());
        hasher.update(b":PARENT_STATE:");
        hasher.update(parent_state_digest.as_bytes());
        hasher.update(b":POST_STATE:");
        hasher.update(post_state_digest.as_bytes());
        hasher.update(b":OP:");
        hasher.update(format!("{:?}", op).as_bytes());
        hasher.update(b":DEFECT:");
        hasher.update(verified_defect.to_string().as_bytes());
        format!("{:x}", hasher.finalize())
    }
}

#[derive(Debug, Clone, PartialEq, Eq, Serialize, Deserialize)]
pub struct HostVerdict {
    pub admitted: bool,
    pub refusal_code: Option<HostRefusalCode>,
    pub reason: Option<String>,
    pub post_state_digest: Option<String>,
    pub verified_defect: Option<BigRational>,
    pub event_id: Option<String>,
}

pub struct SymbolGameHost {
    pub problem: SymbolGameProblem,
    pub current_state_digest: String,
    pub section: Vec<BigRational>,
    pub history: Vec<VerifiedEvent>,
    pub refusals: Vec<HostRefusalCode>,
    pub step_counter: usize,
}

impl SymbolGameHost {
    pub fn try_new(problem: SymbolGameProblem) -> Result<Self, HostRefusalCode> {
        let expected_digest = problem.compute_digest();
        if problem.digest != expected_digest {
            return Err(HostRefusalCode::ProblemDigestMismatch {
                expected: expected_digest,
                found: problem.digest,
            });
        }
        let n_verts = problem.vertices.len();
        let section = vec![BigRational::zero(); n_verts];
        let initial_defect = Self::compute_defect(&problem, &section);

        let initial_digest = Self::calculate_state_digest(
            &problem.digest,
            "0000000000000000000000000000000000000000000000000000000000000000",
            0,
            &section,
            &initial_defect,
        );

        Ok(Self {
            problem,
            current_state_digest: initial_digest,
            section,
            history: Vec::new(),
            refusals: Vec::new(),
            step_counter: 0,
        })
    }

    pub fn new(problem: SymbolGameProblem) -> Self {
        Self::try_new(problem).expect("valid problem digest required at host bootstrap")
    }

    pub fn calculate_state_digest(
        problem_digest: &str,
        parent_digest: &str,
        step_idx: usize,
        sec: &[BigRational],
        defect: &BigRational,
    ) -> String {
        let mut hasher = Sha256::new();
        hasher.update(b"SG_STATE_V1:");
        hasher.update(problem_digest.as_bytes());
        hasher.update(b":PARENT:");
        hasher.update(parent_digest.as_bytes());
        hasher.update(b":STEP:");
        hasher.update(step_idx.to_string().as_bytes());
        hasher.update(b":SECTION:");
        for s in sec {
            hasher.update(s.to_string().as_bytes());
            hasher.update(b",");
        }
        hasher.update(b":DEFECT:");
        hasher.update(defect.to_string().as_bytes());
        format!("{:x}", hasher.finalize())
    }

    pub fn compute_defect(problem: &SymbolGameProblem, sec: &[BigRational]) -> BigRational {
        let mut total = BigRational::zero();
        for (i, edge) in problem.edges.iter().enumerate() {
            let u_idx = problem.vertices.iter().position(|v| v == &edge.u).unwrap();
            let v_idx = problem.vertices.iter().position(|v| v == &edge.v).unwrap();
            let diff = &sec[v_idx] - &sec[u_idx];
            let residual = &problem.initial_claims[i] - diff;
            let abs_res = if residual.is_negative() {
                -residual
            } else {
                residual
            };
            total += &edge.weight * abs_res;
        }
        total
    }

    pub fn section_defect(&self) -> BigRational {
        Self::compute_defect(&self.problem, &self.section)
    }

    pub fn compute_residuals(&self, sec: &[BigRational]) -> Vec<BigRational> {
        let mut residuals = Vec::with_capacity(self.problem.edges.len());
        for (i, edge) in self.problem.edges.iter().enumerate() {
            let u_idx = self
                .problem
                .vertices
                .iter()
                .position(|v| v == &edge.u)
                .unwrap();
            let v_idx = self
                .problem
                .vertices
                .iter()
                .position(|v| v == &edge.v)
                .unwrap();
            let diff = &sec[v_idx] - &sec[u_idx];
            residuals.push(&self.problem.initial_claims[i] - diff);
        }
        residuals
    }

    fn compute_dual_divergences(&self, dual: &[BigRational]) -> Vec<BigRational> {
        let mut divergences = vec![BigRational::zero(); self.problem.vertices.len()];
        for (e_idx, edge) in self.problem.edges.iter().enumerate() {
            let u_idx = self
                .problem
                .vertices
                .iter()
                .position(|v| v == &edge.u)
                .unwrap();
            let v_idx = self
                .problem
                .vertices
                .iter()
                .position(|v| v == &edge.v)
                .unwrap();
            divergences[v_idx] += &dual[e_idx];
            divergences[u_idx] -= &dual[e_idx];
        }
        divergences
    }

    fn check_dual_divergences(&self, divergences: &[BigRational]) -> Result<(), HostRefusalCode> {
        for (v_idx, div) in divergences.iter().enumerate() {
            if !div.is_zero() {
                return Err(HostRefusalCode::DualNotPerpendicular {
                    vertex: self.problem.vertices[v_idx].clone(),
                    divergence: div.to_string(),
                });
            }
        }
        Ok(())
    }

    fn check_dual_weights(&self, dual: &[BigRational]) -> Result<(), HostRefusalCode> {
        for (e_idx, edge) in self.problem.edges.iter().enumerate() {
            let z_val = &dual[e_idx];
            let abs_z = if z_val.is_negative() {
                -z_val.clone()
            } else {
                z_val.clone()
            };
            if abs_z > edge.weight {
                return Err(HostRefusalCode::DualExceedsWeight {
                    edge_index: e_idx,
                    value: z_val.to_string(),
                    weight: edge.weight.to_string(),
                });
            }
        }
        Ok(())
    }

    pub fn verify_dual_witness(
        &self,
        dual: &[BigRational],
        sec: &[BigRational],
    ) -> Result<(), HostRefusalCode> {
        if dual.len() != self.problem.edges.len() || sec.len() != self.problem.vertices.len() {
            return Err(HostRefusalCode::FormatViolation);
        }

        let divergences = self.compute_dual_divergences(dual);
        self.check_dual_divergences(&divergences)?;
        self.check_dual_weights(dual)?;

        let residuals = self.compute_residuals(sec);
        let defect = Self::compute_defect(&self.problem, sec);

        let mut pairing = BigRational::zero();
        for (e_idx, res) in residuals.iter().enumerate() {
            pairing += &dual[e_idx] * res;
        }

        if pairing != defect {
            return Err(HostRefusalCode::DualityGapDetected {
                pairing: pairing.to_string(),
                defect: defect.to_string(),
            });
        }

        Ok(())
    }

    fn is_valid_rationale(rationale: &str) -> bool {
        for c in rationale.chars() {
            if !matches!(
                c as u32,
                32..=126 | 0x0391..=0x03A9 | 0x03B1..=0x03C9 | 0x2192 | 0x22A2 | 0x22A5 | 0x2261
            ) {
                return false;
            }
        }
        true
    }

    fn validate_proposal_header(&self, proposal: &UntrustedProposal) -> Result<(), HostRefusalCode> {
        if proposal.problem_digest != self.problem.digest {
            return Err(HostRefusalCode::ProblemDigestMismatch {
                expected: self.problem.digest.clone(),
                found: proposal.problem_digest.clone(),
            });
        }
        if proposal.parent_state_digest != self.current_state_digest {
            return Err(HostRefusalCode::ParentStateMismatch {
                expected: self.current_state_digest.clone(),
                found: proposal.parent_state_digest.clone(),
            });
        }
        if !Self::is_valid_rationale(&proposal.rationale) {
            return Err(HostRefusalCode::CarrierViolation);
        }
        Ok(())
    }

    #[allow(clippy::too_many_arguments)]
    fn commit_verified_move(
        &mut self,
        next_step: usize,
        event_id: String,
        parent_state_digest: String,
        post_state_digest: String,
        op: HostMoveOp,
        defect: BigRational,
        details: String,
        section: Vec<BigRational>,
    ) -> HostVerdict {
        let parent_event_id = self.history.last().map(|e| e.event_id.clone());
        let ev_digest = VerifiedEvent::calculate_event_digest(
            &event_id,
            parent_event_id.as_deref(),
            &self.problem.digest,
            &parent_state_digest,
            &post_state_digest,
            op,
            &defect,
        );
        self.history.push(VerifiedEvent {
            event_id: event_id.clone(),
            event_digest: ev_digest,
            parent_event_id,
            problem_digest: self.problem.digest.clone(),
            parent_state_digest,
            post_state_digest: post_state_digest.clone(),
            op,
            verified_defect: defect.clone(),
            details,
            section_snapshot: section.clone(),
        });
        self.section = section;
        self.step_counter = next_step;
        self.current_state_digest = post_state_digest.clone();

        HostVerdict {
            admitted: true,
            refusal_code: None,
            reason: None,
            post_state_digest: Some(post_state_digest),
            verified_defect: Some(defect),
            event_id: Some(event_id),
        }
    }

    fn process_cut_move(
        &mut self,
        proposal: &UntrustedProposal,
        next_step: usize,
        event_id: String,
    ) -> HostVerdict {
        let candidate_section = match &proposal.proposed_section {
            Some(sec) if sec.len() == self.problem.vertices.len() => sec.clone(),
            _ => return self.refuse(HostRefusalCode::FormatViolation),
        };

        let defect_before = self.section_defect();
        let defect_after = Self::compute_defect(&self.problem, &candidate_section);

        if defect_after > defect_before {
            return self.refuse(HostRefusalCode::DefectIncrease {
                before: defect_before.to_string(),
                after: defect_after.to_string(),
            });
        }

        let host_post_digest = Self::calculate_state_digest(
            &self.problem.digest,
            &self.current_state_digest,
            next_step,
            &candidate_section,
            &defect_after,
        );

        if host_post_digest != proposal.claimed_post_state_digest {
            return self.refuse(HostRefusalCode::PostStateDigestMismatch {
                host_digest: host_post_digest,
                claimed_digest: proposal.claimed_post_state_digest.clone(),
            });
        }

        let details = format!(
            "CUT accepted: defect reduced from {} to {}",
            defect_before, defect_after
        );
        self.commit_verified_move(
            next_step,
            event_id,
            proposal.parent_state_digest.clone(),
            host_post_digest,
            HostMoveOp::Cut,
            defect_after,
            details,
            candidate_section,
        )
    }

    fn verify_target_property(
        &self,
        proposal: &UntrustedProposal,
        cur_defect: &BigRational,
    ) -> Result<String, HostRefusalCode> {
        let target_prop = proposal.target_property.as_deref().unwrap_or("");
        if target_prop == "ZERO_OBSTRUCTION" {
            if !cur_defect.is_zero() {
                return Err(HostRefusalCode::NonzeroObstruction {
                    defect: cur_defect.to_string(),
                });
            }
            return Ok(target_prop.to_string());
        }
        if target_prop == "DUAL_WITNESS" {
            let dual = match &proposal.dual_witness {
                Some(d) if d.len() == self.problem.edges.len() => d,
                _ => return Err(HostRefusalCode::FormatViolation),
            };
            self.verify_dual_witness(dual, &self.section)?;
            return Ok(target_prop.to_string());
        }
        Err(HostRefusalCode::FormatViolation)
    }

    fn process_verify_move(
        &mut self,
        proposal: &UntrustedProposal,
        next_step: usize,
        event_id: String,
    ) -> HostVerdict {
        let cur_defect = self.section_defect();
        let target_prop = match self.verify_target_property(proposal, &cur_defect) {
            Ok(tp) => tp,
            Err(code) => return self.refuse(code),
        };

        let host_post_digest = Self::calculate_state_digest(
            &self.problem.digest,
            &self.current_state_digest,
            next_step,
            &self.section,
            &cur_defect,
        );

        if host_post_digest != proposal.claimed_post_state_digest {
            return self.refuse(HostRefusalCode::PostStateDigestMismatch {
                host_digest: host_post_digest,
                claimed_digest: proposal.claimed_post_state_digest.clone(),
            });
        }

        let details = format!("VERIFY '{}' accepted with defect {}", target_prop, cur_defect);
        let section_clone = self.section.clone();
        self.commit_verified_move(
            next_step,
            event_id,
            proposal.parent_state_digest.clone(),
            host_post_digest,
            HostMoveOp::Verify,
            cur_defect,
            details,
            section_clone,
        )
    }

    fn resolve_retract_section(
        &self,
        proposal: &UntrustedProposal,
    ) -> Result<(String, Vec<BigRational>), HostRefusalCode> {
        let target_ev = proposal
            .target_event_id
            .as_ref()
            .ok_or(HostRefusalCode::FormatViolation)?;
        let idx = self
            .history
            .iter()
            .position(|e| &e.event_id == target_ev)
            .ok_or_else(|| HostRefusalCode::EventNotFound {
                event_id: target_ev.clone(),
            })?;
        let restored = if idx == 0 {
            vec![BigRational::zero(); self.problem.vertices.len()]
        } else {
            self.history[idx - 1].section_snapshot.clone()
        };
        Ok((target_ev.clone(), restored))
    }

    fn process_retract_move(
        &mut self,
        proposal: &UntrustedProposal,
        next_step: usize,
        event_id: String,
    ) -> HostVerdict {
        let (target_ev, restored) = match self.resolve_retract_section(proposal) {
            Ok(pair) => pair,
            Err(code) => return self.refuse(code),
        };
        let defect = Self::compute_defect(&self.problem, &restored);
        let post_digest = Self::calculate_state_digest(
            &self.problem.digest,
            &self.current_state_digest,
            next_step,
            &restored,
            &defect,
        );
        if post_digest != proposal.claimed_post_state_digest {
            return self.refuse(HostRefusalCode::PostStateDigestMismatch {
                host_digest: post_digest,
                claimed_digest: proposal.claimed_post_state_digest.clone(),
            });
        }
        let parent_state_digest = self.current_state_digest.clone();
        let details = format!("Restored state before {}; prior events retained", target_ev);
        self.commit_verified_move(
            next_step,
            event_id,
            parent_state_digest,
            post_digest,
            HostMoveOp::Retract,
            defect,
            details,
            restored,
        )
    }

    pub fn process_proposal(&mut self, proposal: &UntrustedProposal) -> HostVerdict {
        if let Err(code) = self.validate_proposal_header(proposal) {
            return self.refuse(code);
        }
        let next_step = self.step_counter + 1;
        let event_id = format!("ev_{:04}_{:?}", next_step, proposal.op);

        match proposal.op {
            HostMoveOp::Cut => self.process_cut_move(proposal, next_step, event_id),
            HostMoveOp::Verify => self.process_verify_move(proposal, next_step, event_id),
            HostMoveOp::Assert => self.refuse(HostRefusalCode::UnlicensedProblemMutation),
            HostMoveOp::Retract => self.process_retract_move(proposal, next_step, event_id),
        }
    }

    fn refuse(&mut self, code: HostRefusalCode) -> HostVerdict {
        let reason = code.to_string();
        self.refusals.push(code.clone());
        HostVerdict {
            admitted: false,
            refusal_code: Some(code),
            reason: Some(reason),
            post_state_digest: None,
            verified_defect: None,
            event_id: None,
        }
    }
}

pub fn build_mub6_det_cycle(
    a: BigRational,
    b: BigRational,
    c: BigRational,
    d: BigRational,
) -> SymbolGameProblem {
    let prod_diff = &a * &d - &b * &c;
    let lin_corr = (&a - &b) + (&d - &c);
    let _det = &prod_diff - &lin_corr;

    let vertices = vec!["origin".to_string(), "mid".to_string(), "end".to_string()];
    let edges = vec![
        ProblemEdge {
            u: "origin".to_string(),
            v: "mid".to_string(),
            weight: BigRational::from_integer(BigInt::from(1)),
        },
        ProblemEdge {
            u: "mid".to_string(),
            v: "end".to_string(),
            weight: BigRational::from_integer(BigInt::from(1)),
        },
        ProblemEdge {
            u: "end".to_string(),
            v: "origin".to_string(),
            weight: BigRational::from_integer(BigInt::from(1)),
        },
    ];
    let initial_claims = vec![prod_diff, -lin_corr, BigRational::zero()];

    SymbolGameProblem::new(
        format!("MUB6_DET_CYCLE_a{}_b{}_c{}_d{}", a, b, c, d),
        vertices,
        edges,
        initial_claims,
    )
    .expect("Valid 3-cycle problem")
}
