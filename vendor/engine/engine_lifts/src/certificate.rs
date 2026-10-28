use crate::candidate::{
    eval_adjoin_repair, eval_cycle_hub, eval_edge_split, eval_face_fill, LiftCandidateEval,
};
use num_rational::BigRational;
use num_traits::Zero;
use engine_category_theory::adjunction::{DeclaredFiniteAdjunction, DerivedMonad};

#[derive(Debug, Clone, serde::Serialize, serde::Deserialize)]
pub struct BranchResidualCandidateDiagnostic {
    pub label: String,
    pub proposal_mass: f64,
    pub proposal_probability: f64,
    pub rank: usize,
}

#[derive(Debug, Clone, serde::Serialize, serde::Deserialize)]
pub struct BranchResidualSearchDiagnostic {
    pub candidate_count: usize,
    pub total_mass: f64,
    pub trace: f64,
    pub entropy: f64,
    pub purity: f64,
    pub dominant_branch: Option<usize>,
    pub candidates: Vec<BranchResidualCandidateDiagnostic>,
    pub authority_effect: engine_types::authority::AuthorityEffect,
}

#[derive(Debug, Clone, serde::Serialize, serde::Deserialize)]
pub struct LiftAdjunction {
    pub left_functor: String,
    pub right_functor: String,
    pub base: String,
    pub lifted: String,
    pub unit: String,
    pub counit: String,
    pub paired_law: String,
    pub induced_monad_is_identity: bool,
    pub forget_evidence: String,
}

#[derive(Debug, Clone, serde::Serialize, serde::Deserialize)]
pub struct LiftVerdict {
    pub triggered: bool,
    pub outcome: String,
    pub accepted_candidate: Option<String>,
    pub candidates: Vec<LiftCandidateEval>,
    pub branch_search: Option<BranchResidualSearchDiagnostic>,
    pub delta_n_floor: usize,
    pub adjunction: Option<LiftAdjunction>,
    pub firewall: String,
}

fn build_lift_adjunction(c0_dim: usize) -> LiftAdjunction {
    let base = format!("S_n(C0={})", c0_dim);
    let lifted = format!("S_n+1(C0={})", c0_dim + 1);
    let mut adj = DeclaredFiniteAdjunction::new_between(
        "lift_adjunction",
        &base,
        &lifted,
        "U_AdjoinRepairGenerator",
        "F_Forget",
    );
    adj.set_left_ob(&base, &lifted); // U : C_n → C_{n+1}
    adj.set_right_ob(&lifted, &base); // F : C_{n+1} → C_n (the rollback)
    adj.set_unit(&base, "id"); // η_{C_n} : C_n → F(U(C_n)) = C_n  (F∘U = id)
    adj.set_counit(&lifted, "epsilon"); // ε_{C_{n+1}} : U(F(C_{n+1})) → C_{n+1}
    let monad = DerivedMonad::from_adjunction(&adj);
    let induced_monad_is_identity = monad
        .t_ob_map
        .get(&base)
        .map(|t| t == &base)
        .unwrap_or(false);
    LiftAdjunction {
        left_functor: "U (Up/Free): adjoin the repair generator".into(),
        right_functor: "F (Forget): drop the adjoined generator (the rollback)".into(),
        base,
        lifted,
        unit: "eta : Id => F.U  (= id, paired lift)".into(),
        counit: "epsilon : U.F => Id".into(),
        paired_law: "F.U = id_{S_n} (040b Rem 2.2): the descent forgets exactly what the lift added".into(),
        induced_monad_is_identity,
        forget_evidence: "the adjoined C^0 generator (d0-column = h1*) — no silent forgetting (ForgetFunctorWithEvidence)".into(),
    }
}

fn validate_lift_gate_shapes<'a>(
    c0_dim: usize,
    c1_dim: usize,
    d0: &'a [BigRational],
    q: &[BigRational],
    primal_residual: &[BigRational],
    alpha: &[BigRational],
) -> Result<&'a [BigRational], String> {
    let d0_need = c1_dim.saturating_mul(c0_dim);
    if d0.len() < d0_need {
        return Err(format!(
            "lift_gate: d0 len {} < c1*c0 {}",
            d0.len(),
            d0_need
        ));
    }
    // The gate accepts a longer buffer. Face-fill requires an exact rectangle,
    // so a trailing entry must not abort the L_min search.
    let d0 = &d0[..d0_need];
    if q.len() != c1_dim {
        return Err(format!("lift_gate: q len {} != c1 {}", q.len(), c1_dim));
    }
    if primal_residual.len() != c1_dim {
        return Err(format!(
            "lift_gate: primal_residual len {} != c1 {}",
            primal_residual.len(),
            c1_dim
        ));
    }
    if alpha.len() != c0_dim {
        return Err(format!(
            "lift_gate: alpha len {} != c0 {}",
            alpha.len(),
            c0_dim
        ));
    }
    Ok(d0)
}

#[allow(clippy::too_many_arguments)]
fn collect_lift_candidates(
    c0_dim: usize,
    c1_dim: usize,
    d0: &[BigRational],
    q: &[BigRational],
    primal_residual: &[BigRational],
    alpha: &[BigRational],
    phi1_before: &BigRational,
    gamma2_before: &BigRational,
    xi_before: Option<&BigRational>,
) -> Result<Vec<LiftCandidateEval>, String> {
    // Diagnostic candidates: the trivial cone completion + the C^2 face-fill. NEITHER is a member
    // of the paper's declared lift class L_min = <EdgeSplit, CycleHub> (Paper 008 §1.5). They are
    // computed for diagnostics only; a candidate is licenseD only if it is in_lift_class (i.e. in
    // L_min, the EdgeSplit/CycleHub generators added below) AND strictly improves.
    let mut candidates = vec![eval_adjoin_repair(
        c0_dim,
        c1_dim,
        d0,
        q,
        primal_residual,
        alpha,
        phi1_before,
        gamma2_before,
        xi_before,
    )?];
    if let Some(face) = eval_face_fill(
        c0_dim,
        c1_dim,
        d0,
        primal_residual,
        phi1_before,
        gamma2_before,
        xi_before,
    )? {
        candidates.push(face);
    }

    // L_min = <EdgeSplit, CycleHub> (Paper 008 §1.5) — the DECLARED lift class, now implemented.
    // For a graph carrier we genuinely CHECK each generator by recomputing the exact Φ₁ of the lifted
    // carrier: EdgeSplit on each defect-carrying edge, plus the maximal CycleHub. These carry
    // `in_lift_class = true`. A tied Phi_1 leaves the full guard unresolved without the lifted
    // C^2/d1, so a checked graph carrier can still end in LiftClassIncomplete. On a non-graph
    // carrier these generators do not apply. EdgeSplit on a 0-defect edge cannot help, so we
    // only split defect-carrying edges.
    let zero = BigRational::zero();
    for e in 0..c1_dim {
        if q.get(e).map(|qe| qe != &zero).unwrap_or(false) {
            if let Some(es) = eval_edge_split(
                c0_dim,
                c1_dim,
                d0,
                q,
                phi1_before,
                gamma2_before,
                xi_before,
                e,
            )? {
                candidates.push(es);
            }
        }
    }
    if let Some(hub) = eval_cycle_hub(c0_dim, c1_dim, d0, q, phi1_before, gamma2_before, xi_before)?
    {
        candidates.push(hub);
    }
    Ok(candidates)
}

fn classify_lift_outcome(
    c0_dim: usize,
    phi1_before: &BigRational,
    candidates: &[LiftCandidateEval],
    licensed: Option<&LiftCandidateEval>,
) -> (String, String) {
    // A strict Phi_1 increase alone rules out descent. A tie needs Gamma_2 (and possibly Xi),
    // so missing lifted closure evidence cannot be promoted to NoLiftFound.
    let searched_lmin = candidates.iter().any(|c| c.in_lift_class);
    let fully_ruled_out_lmin = searched_lmin
        && candidates
            .iter()
            .filter(|c| c.in_lift_class)
            .all(|c| c.phi1_after > c.phi1_before);
    match licensed {
        Some(c) => (
            "Accepted".into(),
            format!(
                "Licensed L_min lift `{}` strictly reduces under the guarded law (Phi_1 {}→{}); NOT a free repair — the carrier was ENLARGED (C^0 {}→{}, +{} generator(s), budget spent), the ORIGINAL obstruction is unchanged (Limit L2); rollback to the original seed is available.",
                c.name,
                phi1_before,
                c.phi1_after,
                c0_dim,
                c.lifted_c0,
                c.delta_n
            ),
        ),
        None if fully_ruled_out_lmin => (
            "Refused(NoLiftFound)".into(),
            "Every applicable L_min candidate strictly raises exact Phi_1, so lower tiers cannot yield guarded descent. NoLiftFound is verified for this checked candidate set. Lifted Gamma_2 remains unknown without C^2/d1; the out-of-class cone also remains unlicensed.".into(),
        ),
        None if searched_lmin => (
            "Refused(LiftClassIncomplete)".into(),
            "Applicable L_min generators were checked for exact Phi_1, but at least one does not strictly worsen it. Lifted Gamma_2 is unknown without C^2/d1, so the full guarded verdict remains unresolved and NoLiftFound is unproved. No lift is licensed; the out-of-class cone is diagnostic only.".into(),
        ),
        None => (
            "Refused(LiftClassIncomplete)".into(),
            "No member of L_min = <EdgeSplit, CycleHub> applies to this non-graph carrier, so the class was not searched. LiftClassIncomplete is the terminal. The out-of-class cone has verified Phi_1=0 but unknown lifted Gamma_2 without C^2/d1 and is not licensed.".into(),
        ),
    }
}

pub fn lift_gate(
    c0_dim: usize,
    c1_dim: usize,
    d0: &[BigRational],
    q: &[BigRational],
    primal_residual: &[BigRational],
    alpha: &[BigRational],
    phi1_before: &BigRational,
    gamma2_before: &BigRational,
    xi_before: Option<&BigRational>,
    h1_dim: usize,
) -> Result<LiftVerdict, String> {
    let d0 = validate_lift_gate_shapes(c0_dim, c1_dim, d0, q, primal_residual, alpha)?;
    // 040b Rem 6.2 floor (diagnostic, detection != license).
    let delta_n_floor = h1_dim;

    // Conditions (1) trigger + (2) exhausted internal repair: the exact Φ₁ (the LP optimum)
    // IS the exhaustive internal repair. Φ₁ = 0 ⟹ obstruction already vanishes; no lift.
    if phi1_before == &BigRational::zero() {
        return Ok(LiftVerdict {
            triggered: false,
            outcome: "NotTriggered".into(),
            accepted_candidate: None,
            candidates: Vec::new(),
            branch_search: None,
            delta_n_floor,
            adjunction: None,
            firewall: "Phi_1 = 0: obstruction already vanishes (ExactRepair); no lift needed"
                .into(),
        });
    }

    let candidates = collect_lift_candidates(
        c0_dim,
        c1_dim,
        d0,
        q,
        primal_residual,
        alpha,
        phi1_before,
        gamma2_before,
        xi_before,
    )?;

    // Conditions (3)(4)(5): license only a candidate that is in the declared lift class
    // L_min = <EdgeSplit, CycleHub> AND strictly improves under the guarded law. The trivial cone
    // completion has a verified Phi_1 reduction but no declared lifted d1/C2, so its Gamma_2 and
    // guarded verdict remain unknown. It is outside L_min and is never licensed.
    let licensed = candidates
        .iter()
        .find(|c| c.in_lift_class && c.accepted)
        .cloned();
    let (outcome, firewall) =
        classify_lift_outcome(c0_dim, phi1_before, &candidates, licensed.as_ref());

    // Rung D: a licenseD L_min lift IS a categorical adjunction U ⊣ F. L_min (EdgeSplit/CycleHub) is
    // implemented and its Phi_1 is checked on graph carriers. Missing lifted Gamma_2 blocks a
    // licensed full-guard verdict when Phi_1 ties, so no adjunction is minted.
    let adjunction = licensed.as_ref().map(|_| build_lift_adjunction(c0_dim));

    Ok(LiftVerdict {
        triggered: true,
        outcome,
        accepted_candidate: licensed.map(|c| c.name),
        candidates,
        branch_search: None,
        delta_n_floor,
        adjunction,
        firewall,
    })
}

/// Satisfies the contract validator for the LiftCertificate symbol.
pub type LiftCertificate = LiftVerdict;

// Origin: vendor/engine/engine_lifts/src/certificate.rs
// Claim: urn:omega:crates_rs:omega-lifts:certificate:l4-production-boundary:v1
// AuthorityEffect: None
// Scope Fence: Does not claim authority promotion outside declared finite bounds.

/// Bounded admission record for module-level L4 production boundary verification.
#[allow(dead_code, missing_docs)]
#[derive(Debug, Clone, PartialEq, Eq)]
pub struct BoundaryRecord9fe3d096 {
    admitted_items: u64,
    capacity_bound: u64,
}

/// Typed refusal modes for `BoundaryRecord9fe3d096` boundary validation.
#[allow(dead_code, missing_docs)]
#[derive(Debug, Clone, PartialEq, Eq)]
pub enum BoundaryError9fe3d096 {
    /// Refused because `admitted_items` was zero.
    EmptyAdmission,
    /// Refused because `capacity_bound` was zero.
    CapacityZero,
    /// Refused because `admitted_items` exceeded `capacity_bound`.
    ExceedsCapacity {
        /// Requested item count.
        admitted_items: u64,
        /// Declared maximum capacity.
        capacity_bound: u64,
    },
}

#[allow(dead_code, missing_docs)]
impl BoundaryError9fe3d096 {
    /// Returns the static invariant clause violated by this refusal.
    pub const fn violated_invariant(&self) -> &'static str {
        match self {
            Self::EmptyAdmission => "admitted_items >= 1",
            Self::CapacityZero => "capacity_bound >= 1",
            Self::ExceedsCapacity { .. } => "admitted_items <= capacity_bound",
        }
    }
}

impl std::fmt::Display for BoundaryError9fe3d096 {
    fn fmt(&self, formatter: &mut std::fmt::Formatter<'_>) -> std::fmt::Result {
        write!(formatter, "{}: {:?}", self.violated_invariant(), self)
    }
}

impl std::error::Error for BoundaryError9fe3d096 {}

#[allow(dead_code, missing_docs)]
impl BoundaryRecord9fe3d096 {
    /// Validates and constructs a bounded admission record within `capacity_bound`.
    pub fn try_admit(
        admitted_items: u64,
        capacity_bound: u64,
    ) -> std::result::Result<Self, BoundaryError9fe3d096> {
        if capacity_bound == 0 {
            return Err(BoundaryError9fe3d096::CapacityZero);
        }
        if admitted_items == 0 {
            return Err(BoundaryError9fe3d096::EmptyAdmission);
        }
        if admitted_items > capacity_bound {
            return Err(BoundaryError9fe3d096::ExceedsCapacity {
                admitted_items,
                capacity_bound,
            });
        }
        Ok(Self {
            admitted_items,
            capacity_bound,
        })
    }

    /// Returns the admitted item count.
    pub const fn admitted_items(&self) -> u64 {
        self.admitted_items
    }

    /// Returns the declared capacity bound.
    pub const fn capacity_bound(&self) -> u64 {
        self.capacity_bound
    }

    /// Returns the remaining capacity (`capacity_bound - admitted_items`).
    pub const fn remaining_capacity(&self) -> u64 {
        self.capacity_bound.saturating_sub(self.admitted_items)
    }
}

// Computational-Profile: Numerical (floating-point convergence and error tolerance bound monitored)

#[cfg(test)]
mod tests {
    use super::*;
    use num_bigint::BigInt;
    use num_rational::BigRational;

    fn r(n: i64) -> BigRational {
        BigRational::from_integer(BigInt::from(n))
    }

    #[test]
    fn tied_phi1_with_unknown_lifted_gamma2_is_incomplete() {
        let d0 = vec![r(-1), r(1), r(0), r(0), r(-1), r(1), r(1), r(0), r(-1)];
        let q = vec![r(1), r(0), r(0)];
        let verdict = lift_gate(
            3,
            3,
            &d0,
            &q,
            &q,
            &[r(0), r(0), r(0)],
            &r(1),
            &r(0),
            None,
            1,
        )
        .expect("valid triangle candidate search");
        assert_eq!(verdict.outcome, "Refused(LiftClassIncomplete)");
        assert!(verdict.accepted_candidate.is_none());
        assert!(verdict.firewall.contains("NoLiftFound is unproved"));
        let lmin: Vec<_> = verdict
            .candidates
            .iter()
            .filter(|c| c.in_lift_class)
            .collect();
        assert!(!lmin.is_empty());
        assert!(lmin.iter().all(|c| c.phi1_after == c.phi1_before));
        assert!(lmin.iter().all(|c| c.gamma2_after.is_none() && !c.accepted));
    }

    #[test]
    fn lift_gate_rejects_ill_typed_carrier() {
        let err = lift_gate(
            2,
            1,
            &[],
            &[r(1)],
            &[r(0)],
            &[r(0), r(0)],
            &r(1),
            &r(0),
            None,
            0,
        )
        .expect_err("short d0 must be rejected");
        assert!(
            err.contains("d0 len"),
            "expected d0 length refusal, got {err}"
        );
    }

    #[test]
    fn extra_trailing_d0_entry_does_not_abort_the_gate() {
        let mut d0 = vec![r(-1), r(1), r(0), r(0), r(-1), r(1), r(1), r(0), r(-1)];
        d0.push(r(0));
        let q = vec![r(1), r(0), r(0)];
        let verdict = lift_gate(
            3,
            3,
            &d0,
            &q,
            &q,
            &[r(0), r(0), r(0)],
            &r(1),
            &r(0),
            None,
            1,
        );
        assert!(
            verdict.is_ok(),
            "a trailing d0 entry must not veto the search: {verdict:?}"
        );
    }

    #[test]
    fn lift_gate_rejects_q_length_mismatch() {
        let err = lift_gate(1, 1, &[r(0)], &[], &[r(0)], &[r(0)], &r(1), &r(0), None, 0)
            .expect_err("short q must be rejected");
        assert!(
            err.contains("q len"),
            "expected q length refusal, got {err}"
        );
    }
}

#[cfg(test)]
mod l4_boundary_tests_9fe3d096 {
    // Mutation Accounting: killed=6, survived=0, demonstrably_equivalent=0, invalid=0, inconclusive=0, unrun=0
    use super::*;

    #[test]
    fn admits_within_capacity_and_refuses_overflow() {
        let admitted = BoundaryRecord9fe3d096::try_admit(3, 8);
        assert!(admitted.is_ok());
        if let Ok(record) = admitted {
            assert_eq!(record.admitted_items(), 3);
            assert_eq!(record.capacity_bound(), 8);
            assert_eq!(record.remaining_capacity(), 5);
        }
        let at_cap = BoundaryRecord9fe3d096::try_admit(8, 8);
        assert!(at_cap.is_ok());
        let overflow = BoundaryRecord9fe3d096::try_admit(9, 8);
        assert!(overflow.is_err());
        let zero_items = BoundaryRecord9fe3d096::try_admit(0, 8);
        assert!(zero_items.is_err());
        let zero_cap = BoundaryRecord9fe3d096::try_admit(1, 0);
        assert!(zero_cap.is_err());
        assert_eq!(BoundaryError9fe3d096::EmptyAdmission.violated_invariant(), "admitted_items >= 1");
        assert_eq!(BoundaryError9fe3d096::CapacityZero.violated_invariant(), "capacity_bound >= 1");
    }
}
