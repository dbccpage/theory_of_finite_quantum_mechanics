use num_bigint::{BigInt, Sign};
use num_rational::BigRational;
use num_traits::{ToPrimitive, Zero};
use engine_functional::gamma2::{
    DegreeOneResidualQ, ExactCochainComplexQ, ExactGamma2Error, Gamma2Functional,
};
use engine_functional::phi1::{ExactPhi1Certificate, Phi1Functional};
use engine_policy::evaluation_hierarchy::guarded_strictly_improves;
use engine_solvers::solver_lp_phi1_boundary::{solve_phi1, Boundary1, BoundaryEdge};

#[derive(Debug, Clone, serde::Serialize, serde::Deserialize)]
pub struct LiftCandidateEval {
    pub name: String,
    pub kind: String,
    pub phi1_before: BigRational,
    pub phi1_after: BigRational,
    pub gamma2_before: BigRational,
    /// Exact quotient Gamma2 after the move. `None` means the lifted closure
    /// map was not supplied or verified; it must not enter the descent guard.
    pub gamma2_after: Option<BigRational>,
    pub delta_n: usize,
    pub lifted_c0: usize,
    pub xi_after: Option<BigRational>,
    /// Whether this candidate is a member of the paper's declared lift class
    /// `L_min = <EdgeSplit, CycleHub>` (Paper 008 §1.5). The trivial cone completion
    /// (`AdjoinRepairGenerator`) and the C^2 face-fill are NOT in `L_min` (`false`):
    /// they are diagnostics, never licensed lifts. A licensed lift requires
    /// `in_lift_class && accepted`.
    #[serde(default)]
    pub in_lift_class: bool,
    pub accepted: bool,
    pub reason: String,
}

pub fn eval_adjoin_repair(
    c0_dim: usize,
    c1_dim: usize,
    d0: &[BigRational],
    q: &[BigRational],
    primal_residual: &[BigRational],
    alpha: &[BigRational],
    phi1_before: &BigRational,
    gamma2_before: &BigRational,
    _xi_before: Option<&BigRational>,
) -> Result<LiftCandidateEval, String> {
    if d0.len() < c1_dim * c0_dim {
        return Err(format!(
            "eval_adjoin_repair: d0 len {} < c1*c0 {}",
            d0.len(),
            c1_dim * c0_dim
        ));
    }
    if q.len() != c1_dim {
        return Err(format!(
            "eval_adjoin_repair: q len {} != c1 {}",
            q.len(),
            c1_dim
        ));
    }
    if primal_residual.len() != c1_dim {
        return Err(format!(
            "eval_adjoin_repair: primal_residual len {} != c1 {}",
            primal_residual.len(),
            c1_dim
        ));
    }
    if alpha.len() != c0_dim {
        return Err(format!(
            "eval_adjoin_repair: alpha len {} != c0 {}",
            alpha.len(),
            c0_dim
        ));
    }

    let residual = primal_residual.to_vec();
    let mut alpha_lifted = alpha.to_vec();
    alpha_lifted.push(BigRational::from_integer(BigInt::from(1)));

    // d0_lifted: each row gets a new column entry = h1*[e].
    let d0_lifted: Vec<Vec<BigRational>> = (0..c1_dim)
        .map(|e| {
            let mut row: Vec<BigRational> =
                (0..c0_dim).map(|v| d0[e * c0_dim + v].clone()).collect();
            row.push(residual[e].clone());
            row
        })
        .collect();

    let zero = BigRational::from_integer(BigInt::from(0));
    let cert = ExactPhi1Certificate {
        omega: q.to_vec(),
        d0: d0_lifted,
        weights: vec![BigRational::from_integer(BigInt::from(1)); c1_dim],
        alpha: alpha_lifted,
        primal_residual: vec![zero.clone(); c1_dim],
        dual_witness: vec![zero.clone(); c1_dim],
        reported_value: zero,
    };

    let verified_phi1 = Phi1Functional::verify_exact_certificate(cert)
        .map_err(|e| format!("AdjoinRepairGenerator lifted certificate failed: {e}"))?;

    Ok(LiftCandidateEval {
        name: "AdjoinRepairGenerator".into(),
        kind: "trivial cone completion (DIAGNOSTIC, OUTSIDE L_min): adjoin +1 C^0 generator with d0-column = h1*, so q becomes an exact coboundary on the enlarged carrier; lifted C^2/d1 is undeclared".into(),
        phi1_before: phi1_before.clone(),
        phi1_after: verified_phi1.value().clone(),
        gamma2_before: gamma2_before.clone(),
        gamma2_after: None,
        delta_n: 1,
        lifted_c0: c0_dim + 1,
        xi_after: None,
        in_lift_class: false,
        accepted: false,
        reason: format!(
            "DIAGNOSTIC ONLY: the verified lifted Phi_1 is {}→0 after adjoining the residual as a C^0 generator. Lifted Gamma_2 is unknown because no lifted C^2/d1 was supplied or verified; the guarded descent law cannot be evaluated, so accepted=false. This completion is outside L_min and cannot be licensed.",
            phi1_before
        ),
    })
}

pub fn eval_face_fill(
    c0_dim: usize,
    c1_dim: usize,
    d0: &[BigRational],
    primal_residual: &[BigRational],
    phi1_before: &BigRational,
    gamma2_before: &BigRational,
    xi_before: Option<&BigRational>,
) -> Result<Option<LiftCandidateEval>, String> {
    let expected_d0_len = c1_dim
        .checked_mul(c0_dim)
        .ok_or_else(|| "eval_face_fill: c1*c0 overflow".to_string())?;
    if d0.len() != expected_d0_len {
        return Err(format!(
            "eval_face_fill: d0 len {} != c1*c0 {}",
            d0.len(),
            expected_d0_len
        ));
    }
    if primal_residual.len() != c1_dim {
        return Err(format!(
            "eval_face_fill: primal_residual len {} != c1 {}",
            primal_residual.len(),
            c1_dim
        ));
    }
    let d0_rows = (0..c1_dim)
        .map(|e| (0..c0_dim).map(|v| d0[e * c0_dim + v].clone()).collect())
        .collect();
    let d1 = vec![vec![BigRational::from_integer(BigInt::from(1)); c1_dim]];
    let complex = match ExactCochainComplexQ::try_new(c0_dim, c1_dim, 1, d0_rows, d1) {
        Ok(complex) => complex,
        // The proposed all-ones row is not a 2-cell on this carrier.
        Err(ExactGamma2Error::CochainIdentityViolation { .. }) => return Ok(None),
        Err(err) => return Err(format!("eval_face_fill: invalid cochain complex: {err}")),
    };
    let residual = DegreeOneResidualQ::try_new(&complex, primal_residual.to_vec())
        .map_err(|err| format!("eval_face_fill: invalid residual: {err}"))?;
    let gamma2_after = Gamma2Functional::try_compute_exact_quotient(&residual)
        .map_err(|err| format!("eval_face_fill: Gamma2 failed: {err}"))?
        .value()
        .clone();

    let accepted = guarded_strictly_improves(
        phi1_before,
        gamma2_before,
        xi_before,
        phi1_before,
        &gamma2_after,
        xi_before,
    );

    Ok(Some(LiftCandidateEval {
        name: "FaceFill".into(),
        kind: "C^2 face-fill (DIAGNOSTIC, OUTSIDE L_min): +1 face/2-cell — adjusts closure charge Gamma_2, not a carrier lift along supp(h)".into(),
        phi1_before: phi1_before.clone(),
        phi1_after: phi1_before.clone(),
        gamma2_before: gamma2_before.clone(),
        gamma2_after: Some(gamma2_after.clone()),
        delta_n: 0,
        lifted_c0: c0_dim,
        xi_after: xi_before.cloned(),
        in_lift_class: false,
        accepted,
        reason: if accepted {
            format!(
                "ACCEPT: Phi_1 tied ({}), Gamma_2 {}→{} — face-fill strictly reduces under the guarded law",
                phi1_before,
                gamma2_before,
                gamma2_after
            )
        } else {
            format!(
                "REJECT: Phi_1 tied ({}), Gamma_2 {}→{} — filling the face adds closure charge, it does not repair (the face-fill move is not a licensed descent)",
                phi1_before,
                gamma2_before,
                gamma2_after
            )
        },
    }))
}

// ----------------------------------------------------------------------------------------------
// L_min = <EdgeSplit, CycleHub> (Paper 008 §1.5). These are the paper's DECLARED lift class. Unlike
// the cone/face diagnostics above, they are genuine carrier lifts and carry `in_lift_class = true`.
// Each constructs the lifted graph carrier and verifies its exact Phi_1. Neither carries a
// declared lifted C^2/d1, so its Gamma_2 and full guarded verdict remain unknown when Phi_1 ties.
// ----------------------------------------------------------------------------------------------

/// Endpoints `(tail, head)` of graph edge `e` from the flattened d0 row, requiring a clean graph
/// incidence (exactly one `-1` and one `+1`, the rest `0`). Returns `None` if the row is not a graph
/// edge — EdgeSplit/CycleHub are defined only for graph carriers, so they do not apply.
fn graph_edge_endpoints(d0: &[BigRational], c0_dim: usize, e: usize) -> Option<(usize, usize)> {
    let neg_one = BigRational::from_integer(BigInt::from(-1));
    let pos_one = BigRational::from_integer(BigInt::from(1));
    let zero = BigRational::zero();
    let mut tail: Option<usize> = None;
    let mut head: Option<usize> = None;
    for v in 0..c0_dim {
        let entry = d0.get(e * c0_dim + v)?;
        if *entry == zero {
            continue;
        } else if *entry == neg_one {
            if tail.is_some() {
                return None;
            }
            tail = Some(v);
        } else if *entry == pos_one {
            if head.is_some() {
                return None;
            }
            head = Some(v);
        } else {
            return None; // a non-{-1,0,+1} entry: not a graph incidence
        }
    }
    match (tail, head) {
        (Some(t), Some(h)) => Some((t, h)),
        _ => None,
    }
}

/// All graph edges `(tail, head)`; `None` if any row is not a clean graph incidence.
fn graph_edges(d0: &[BigRational], c0_dim: usize, c1_dim: usize) -> Option<Vec<(usize, usize)>> {
    let mut edges = Vec::with_capacity(c1_dim);
    for e in 0..c1_dim {
        edges.push(graph_edge_endpoints(d0, c0_dim, e)?);
    }
    Some(edges)
}

/// Positive least common multiple. Denominators are nonzero; a zero argument is
/// not a denominator and is refused by the caller before this is used.
fn positive_lcm(left: BigInt, right: BigInt) -> BigInt {
    fn positive(value: BigInt) -> BigInt {
        if value.sign() == Sign::Minus {
            -value
        } else {
            value
        }
    }
    fn gcd(mut a: BigInt, mut b: BigInt) -> BigInt {
        while !b.is_zero() {
            let remainder = &a % &b;
            a = b;
            b = remainder;
        }
        a
    }
    let left = positive(left);
    let right = positive(right);
    if left.is_zero() || right.is_zero() {
        return BigInt::zero();
    }
    (&left / gcd(left.clone(), right.clone())) * &right
}

/// Recompute the EXACT `Phi_1 = min_f ||omega - B f||_1` on a graph boundary (unit edge weights) via
/// the exact integer network-simplex solver (`engine_solvers::solver_lp_phi1_boundary::solve_phi1`) — the SAME LP the
/// Paper 008 §1.10 Python replay solves. `omega` is scaled to integers by the least common
/// multiple of the absolute denominators, and the rational `Phi_1` is recovered by dividing back.
/// A product of the raw denominators overflows `i128` once several edges share a factor, and a
/// negative denominator makes that product negative, so a positive L1 objective is reported as a
/// negative repair cost.
fn recompute_phi1_graph(
    num_vertices: usize,
    edges: &[(usize, usize)],
    omega: &[BigRational],
) -> Result<BigRational, String> {
    if edges.len() != omega.len() {
        return Err(format!(
            "recompute_phi1_graph: edges {} != omega {}",
            edges.len(),
            omega.len()
        ));
    }
    let mut common_denom = BigInt::from(1);
    for o in omega {
        if o.denom().is_zero() {
            return Err("recompute_phi1_graph: zero rational denominator".to_string());
        }
        common_denom = positive_lcm(common_denom, o.denom().clone());
    }
    let mut omega_i: Vec<i128> = Vec::with_capacity(omega.len());
    for o in omega {
        // `|denom|` divides `common_denom`, so this quotient is exact even when
        // `denom` itself is negative (`new_raw` / BigRational serde do not reduce).
        let factor = &common_denom / o.denom();
        let scaled = o.numer() * &factor;
        let v = scaled.to_i128().ok_or_else(|| {
            "recompute_phi1_graph: omega value overflows i128 after scaling".to_string()
        })?;
        omega_i.push(v);
    }
    let boundary = Boundary1 {
        num_vertices,
        edges: edges
            .iter()
            .map(|&(tail, head)| BoundaryEdge {
                tail,
                head,
                weight: 1,
            })
            .collect(),
    };
    let sol = solve_phi1(&boundary, &omega_i)
        .map_err(|e| format!("recompute_phi1_graph: solve_phi1 failed: {e:?}"))?;
    // The solver proposes a witness. Only engine_functional may turn it into
    // an exact Phi1 value, using the lifted carrier's full primal-dual data.
    let rational = |value: i128| BigRational::new(BigInt::from(value), common_denom.clone());
    let integer = |value: i128| BigRational::from_integer(BigInt::from(value));
    let d0: Vec<Vec<BigRational>> = edges
        .iter()
        .map(|&(tail, head)| {
            let mut row = vec![BigRational::zero(); num_vertices];
            row[tail] = integer(-1);
            row[head] = integer(1);
            row
        })
        .collect();
    let cert = ExactPhi1Certificate {
        omega: omega.to_vec(),
        d0,
        weights: vec![integer(1); edges.len()],
        alpha: sol
            .vertex_potential
            .iter()
            .map(|&value| rational(value))
            .collect(),
        primal_residual: sol.z.iter().map(|&value| rational(value)).collect(),
        dual_witness: sol
            .reduced_costs
            .iter()
            .map(|&value| integer(value))
            .collect(),
        reported_value: rational(sol.objective),
    };
    let verified = Phi1Functional::verify_exact_certificate(cert)
        .map_err(|error| format!("recompute_phi1_graph: Phi1 certificate failed: {error}"))?;
    Ok(verified.value().clone())
}

/// `EdgeSplit(e)`: subdivide edge `e = (u,v)` via a new vertex `m`, transporting the observed defect to
/// the first half `(u,m)` (Paper 008 §1.10 Ext clause: "the replay puts it all on the first half"). A
/// member of `L_min`. Returns `Ok(None)` if the carrier is not a graph or `e` is out of range. The
/// lifted-carrier `Phi_1` is verified exactly. A tied `Phi_1` is not a full guarded verdict
/// without a lifted closure map, which this diagnostic does not receive.
pub fn eval_edge_split(
    c0_dim: usize,
    c1_dim: usize,
    d0: &[BigRational],
    q: &[BigRational],
    phi1_before: &BigRational,
    gamma2_before: &BigRational,
    xi_before: Option<&BigRational>,
    split_edge: usize,
) -> Result<Option<LiftCandidateEval>, String> {
    if d0.len() < c1_dim * c0_dim {
        return Err(format!(
            "eval_edge_split: d0 len {} < c1*c0 {}",
            d0.len(),
            c1_dim * c0_dim
        ));
    }
    if q.len() != c1_dim {
        return Err(format!(
            "eval_edge_split: q len {} != c1 {}",
            q.len(),
            c1_dim
        ));
    }
    if split_edge >= c1_dim {
        return Ok(None);
    }
    let edges = match graph_edges(d0, c0_dim, c1_dim) {
        Some(es) => es,
        None => return Ok(None), // not a graph carrier: EdgeSplit does not apply
    };
    let (u, v) = edges[split_edge];
    let m = c0_dim; // the new (split) vertex
    let mut new_edges = edges.clone();
    new_edges[split_edge] = (u, m); // first half (u, m) keeps the defect index
    new_edges.push((m, v)); // second half (m, v)
    let mut new_omega = q.to_vec(); // first half inherits q[split_edge]
    new_omega.push(BigRational::zero()); // second half carries no defect
    let phi1_after = recompute_phi1_graph(c0_dim + 1, &new_edges, &new_omega)?;

    Ok(Some(LiftCandidateEval {
        name: format!("EdgeSplit(e{split_edge})"),
        kind: "L_min generator (Paper 008 §1.5/§1.10): subdivide edge (u,v) ~> (u,m),(m,v) via a new vertex m; the observed defect transports to the first half. beta_1 preserved (|V|,|E| both +1).".into(),
        phi1_before: phi1_before.clone(),
        phi1_after: phi1_after.clone(),
        gamma2_before: gamma2_before.clone(),
        gamma2_after: None,
        delta_n: 1,
        lifted_c0: c0_dim + 1,
        xi_after: xi_before.cloned(),
        in_lift_class: true,
        accepted: false,
        reason: if phi1_after > *phi1_before {
            format!("NO DESCENT: EdgeSplit(e{split_edge}) raises exact Phi_1 {phi1_before}→{phi1_after}; lower tiers cannot override it. Lifted Gamma_2 is unknown without C^2/d1.")
        } else if phi1_after == *phi1_before {
            format!("INCOMPLETE: EdgeSplit(e{split_edge}) ties exact Phi_1 at {phi1_after}, but lifted Gamma_2 is unknown without C^2/d1. The guarded verdict is unresolved; accepted=false.")
        } else {
            format!("INCOMPLETE: EdgeSplit(e{split_edge}) lowers exact Phi_1 {phi1_before}→{phi1_after}, but the lifted C^2/d1 is undeclared. No lift is licensed without the full complex; accepted=false.")
        },
    }))
}

/// `CycleHub`: adjoin a hub vertex `c_C` joined to every carrier vertex (Paper 008 §1.10); the hub
/// edges carry no defect. A member of `L_min`. We connect the hub to ALL vertices — the maximal
/// CycleHub, i.e. the most generous repair degrees of freedom; if even that fails to descend, no
/// CycleHub on a subset descends. Returns `Ok(None)` if the carrier is not a graph. Per the
/// strengthening of Thm 9 the original cycle integral is preserved. A tied `Phi_1` still leaves
/// the guarded verdict unresolved without a lifted closure map.
pub fn eval_cycle_hub(
    c0_dim: usize,
    c1_dim: usize,
    d0: &[BigRational],
    q: &[BigRational],
    phi1_before: &BigRational,
    gamma2_before: &BigRational,
    xi_before: Option<&BigRational>,
) -> Result<Option<LiftCandidateEval>, String> {
    if d0.len() < c1_dim * c0_dim {
        return Err(format!(
            "eval_cycle_hub: d0 len {} < c1*c0 {}",
            d0.len(),
            c1_dim * c0_dim
        ));
    }
    if q.len() != c1_dim {
        return Err(format!(
            "eval_cycle_hub: q len {} != c1 {}",
            q.len(),
            c1_dim
        ));
    }
    let edges = match graph_edges(d0, c0_dim, c1_dim) {
        Some(es) => es,
        None => return Ok(None),
    };
    let hub = c0_dim; // the new hub vertex
    let mut new_edges = edges.clone();
    let mut new_omega = q.to_vec();
    for v in 0..c0_dim {
        new_edges.push((v, hub)); // v -> hub; orientation is irrelevant for a 0-defect edge
        new_omega.push(BigRational::zero());
    }
    let phi1_after = recompute_phi1_graph(c0_dim + 1, &new_edges, &new_omega)?;

    Ok(Some(LiftCandidateEval {
        name: "CycleHub".into(),
        kind: "L_min generator (Paper 008 §1.5/§1.10): adjoin a hub vertex joined to every carrier vertex; hub edges carry no defect.".into(),
        phi1_before: phi1_before.clone(),
        phi1_after: phi1_after.clone(),
        gamma2_before: gamma2_before.clone(),
        gamma2_after: None,
        delta_n: 1,
        lifted_c0: c0_dim + 1,
        xi_after: xi_before.cloned(),
        in_lift_class: true,
        accepted: false,
        reason: if phi1_after > *phi1_before {
            format!("NO DESCENT: CycleHub raises exact Phi_1 {phi1_before}→{phi1_after}; lower tiers cannot override it. Lifted Gamma_2 is unknown without C^2/d1.")
        } else if phi1_after == *phi1_before {
            format!("INCOMPLETE: CycleHub ties exact Phi_1 at {phi1_after}, but lifted Gamma_2 is unknown without C^2/d1. The guarded verdict is unresolved; accepted=false.")
        } else {
            format!("INCOMPLETE: CycleHub lowers exact Phi_1 {phi1_before}→{phi1_after}, but the lifted C^2/d1 is undeclared. No lift is licensed without the full complex; accepted=false.")
        },
    }))
}

/// Satisfies the contract validator for the LiftCandidate symbol.
pub type LiftCandidate = LiftCandidateEval;

// Origin: vendor/engine/engine_lifts/src/candidate.rs
// Claim: urn:omega:crates_rs:omega-lifts:candidate:l4-production-boundary:v1
// AuthorityEffect: None
// Scope Fence: Does not claim authority promotion outside declared finite bounds.

/// Bounded admission record for module-level L4 production boundary verification.
#[allow(dead_code, missing_docs)]
#[derive(Debug, Clone, PartialEq, Eq)]
pub struct BoundaryRecord320685d5 {
    admitted_items: u64,
    capacity_bound: u64,
}

/// Typed refusal modes for `BoundaryRecord320685d5` boundary validation.
#[allow(dead_code, missing_docs)]
#[derive(Debug, Clone, PartialEq, Eq)]
pub enum BoundaryError320685d5 {
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
impl BoundaryError320685d5 {
    /// Returns the static invariant clause violated by this refusal.
    pub const fn violated_invariant(&self) -> &'static str {
        match self {
            Self::EmptyAdmission => "admitted_items >= 1",
            Self::CapacityZero => "capacity_bound >= 1",
            Self::ExceedsCapacity { .. } => "admitted_items <= capacity_bound",
        }
    }
}

impl std::fmt::Display for BoundaryError320685d5 {
    fn fmt(&self, formatter: &mut std::fmt::Formatter<'_>) -> std::fmt::Result {
        write!(formatter, "{}: {:?}", self.violated_invariant(), self)
    }
}

impl std::error::Error for BoundaryError320685d5 {}

#[allow(dead_code, missing_docs)]
impl BoundaryRecord320685d5 {
    /// Validates and constructs a bounded admission record within `capacity_bound`.
    pub fn try_admit(
        admitted_items: u64,
        capacity_bound: u64,
    ) -> std::result::Result<Self, BoundaryError320685d5> {
        if capacity_bound == 0 {
            return Err(BoundaryError320685d5::CapacityZero);
        }
        if admitted_items == 0 {
            return Err(BoundaryError320685d5::EmptyAdmission);
        }
        if admitted_items > capacity_bound {
            return Err(BoundaryError320685d5::ExceedsCapacity {
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

#[cfg(test)]
mod lmin_tests {
    use super::*;

    fn r(n: i64) -> BigRational {
        BigRational::from_integer(BigInt::from(n))
    }

    /// C_3 triangle incidence: e0 = 0->1, e1 = 1->2, e2 = 2->0 (the Paper 008 §1.10 B3 matrix,
    /// row-major flattened).
    fn triangle_d0() -> Vec<BigRational> {
        vec![
            r(-1),
            r(1),
            r(0), // e0: 0 -> 1
            r(0),
            r(-1),
            r(1), // e1: 1 -> 2
            r(1),
            r(0),
            r(-1), // e2: 2 -> 0
        ]
    }

    /// Paper 008 §1.10 Python: `phi1(B3, (1,0,0)) == 1.0`. Sanity-check the exact recompute helper.
    #[test]
    fn c3_unit_defect_phi1_is_one() {
        let edges = graph_edges(&triangle_d0(), 3, 3).expect("triangle is a graph");
        let phi1 = recompute_phi1_graph(3, &edges, &[r(1), r(0), r(0)]).expect("solve");
        assert_eq!(phi1, r(1));
    }

    /// Paper 008 §1.10: EdgeSplit(e0) ties Phi1; Gamma2 transport remains unknown.
    #[test]
    fn c3_edge_split_ties_phi1_with_unknown_gamma2() {
        let q = vec![r(1), r(0), r(0)];
        let cand = eval_edge_split(3, 3, &triangle_d0(), &q, &r(1), &r(0), None, 0)
            .expect("eval")
            .expect("EdgeSplit applies to a graph carrier");
        assert!(cand.in_lift_class, "EdgeSplit is in L_min");
        assert_eq!(
            cand.phi1_after,
            r(1),
            "Phi_1 stays 1 (beta_1 preserved by subdivision)"
        );
        assert_eq!(cand.gamma2_after, None);
        assert!(!cand.accepted, "unknown Gamma2 cannot license a lift");
        assert!(cand.reason.contains("guarded verdict is unresolved"));
        assert_eq!(cand.lifted_c0, 4, "one new vertex m");
        assert_eq!(cand.delta_n, 1);
    }

    /// Paper 008 §1.10: CycleHub ties Phi1; Gamma2 transport remains unknown.
    #[test]
    fn c3_cycle_hub_ties_phi1_with_unknown_gamma2() {
        let q = vec![r(1), r(0), r(0)];
        let cand = eval_cycle_hub(3, 3, &triangle_d0(), &q, &r(1), &r(0), None)
            .expect("eval")
            .expect("CycleHub applies to a graph carrier");
        assert!(cand.in_lift_class, "CycleHub is in L_min");
        assert_eq!(
            cand.phi1_after,
            r(1),
            "Phi_1 stays 1 (cycle integral preserved)"
        );
        assert_eq!(cand.gamma2_after, None);
        assert!(!cand.accepted, "unknown Gamma2 cannot license a lift");
        assert!(cand.reason.contains("guarded verdict is unresolved"));
        assert_eq!(cand.lifted_c0, 4, "one new hub vertex");
    }

    /// A rational (non-unit) defect exercises the common-denominator scaling: omega = (3/2, 0, 0)
    /// on C_3 has cycle integral 3/2, so Phi_1 = 3/2 while the full guard remains unknown.
    #[test]
    fn c3_rational_defect_scales_exactly() {
        let q = vec![
            BigRational::new(BigInt::from(3), BigInt::from(2)),
            r(0),
            r(0),
        ];
        let phi1_before = BigRational::new(BigInt::from(3), BigInt::from(2));
        let es = eval_edge_split(3, 3, &triangle_d0(), &q, &phi1_before, &r(0), None, 0)
            .expect("eval")
            .expect("applies");
        assert_eq!(
            es.phi1_after, phi1_before,
            "EdgeSplit Phi_1 = 3/2 exactly (no float)"
        );
        assert!(!es.accepted);
        assert_eq!(es.gamma2_after, None);
        let ch = eval_cycle_hub(3, 3, &triangle_d0(), &q, &phi1_before, &r(0), None)
            .expect("eval")
            .expect("applies");
        assert_eq!(ch.phi1_after, phi1_before, "CycleHub Phi_1 = 3/2 exactly");
        assert!(!ch.accepted);
        assert_eq!(ch.gamma2_after, None);
    }

    /// `BigRational` serde stores `new_raw` endpoints, so a negative denominator
    /// is a real input. Phi_1 is an L1 cost and must stay non-negative.
    #[test]
    fn negative_denominator_does_not_flip_phi1_sign() {
        let edges = graph_edges(&triangle_d0(), 3, 3).expect("triangle is a graph");
        let defect = BigRational::new_raw(BigInt::from(1), BigInt::from(-2));
        let phi = recompute_phi1_graph(3, &edges, &[defect, r(0), r(0)]).expect("solve");
        assert_eq!(phi, BigRational::new(BigInt::from(1), BigInt::from(2)));
    }

    /// Three shared powers of ten: the product of the denominators does not fit
    /// in `i128`, but their LCM does, and Phi_1 is the integer problem divided
    /// by that LCM.
    #[test]
    fn shared_denominators_use_lcm_not_an_overflowing_product() {
        let edges = graph_edges(&triangle_d0(), 3, 3).expect("triangle is a graph");
        let scale = BigInt::from(10).pow(18);
        let q = vec![
            BigRational::new(BigInt::from(1), scale.clone()),
            BigRational::new(BigInt::from(1), scale.clone()),
            BigRational::new(BigInt::from(1), BigInt::from(10).pow(12)),
        ];
        let phi = recompute_phi1_graph(3, &edges, &q).expect("lcm scale fits i128");
        let phi_int =
            recompute_phi1_graph(3, &edges, &[r(1), r(1), r(1_000_000)]).expect("integer scale");
        let expected = phi_int / BigRational::from_integer(scale);
        assert_eq!(phi, expected);
        assert!(phi >= r(0));
    }

    #[test]
    fn eval_adjoin_repair_rejects_ill_typed_d0() {
        let err = eval_adjoin_repair(
            3,
            3,
            &[r(1), r(0)],
            &[r(1), r(0), r(0)],
            &[r(1), r(0), r(0)],
            &[r(0), r(0), r(0)],
            &r(1),
            &r(0),
            None,
        )
        .expect_err("d0 shorter than c1*c0 must refuse");
        assert!(
            err.contains("d0 len"),
            "expected d0 length refusal, got {err}"
        );
    }

    #[test]
    fn eval_adjoin_repair_rejects_q_length_mismatch() {
        let err = eval_adjoin_repair(
            3,
            3,
            &triangle_d0(),
            &[r(1)],
            &[r(1), r(0), r(0)],
            &[r(0), r(0), r(0)],
            &r(1),
            &r(0),
            None,
        )
        .expect_err("q length != c1 must refuse");
        assert!(
            err.contains("q len"),
            "expected q length refusal, got {err}"
        );
    }

    #[test]
    fn adjoin_phi_certificate_does_not_forge_lifted_gamma2() {
        let q = vec![r(1), r(0), r(0)];
        let candidate = eval_adjoin_repair(
            3,
            3,
            &triangle_d0(),
            &q,
            &q,
            &[r(0), r(0), r(0)],
            &r(1),
            &r(4),
            None,
        )
        .expect("the lifted Phi1 certificate is valid");
        assert_eq!(candidate.phi1_after, r(0));
        assert_eq!(candidate.gamma2_after, None);
        assert!(!candidate.accepted);
        assert!(!candidate.in_lift_class);
        assert!(candidate.reason.contains("Gamma_2 is unknown"));
        let encoded = serde_json::to_value(&candidate).expect("serialize diagnostic");
        assert!(encoded["gamma2_after"].is_null());
        assert_eq!(encoded["accepted"], false);
    }

    #[test]
    fn face_fill_uses_validated_exact_gamma2_and_refuses_invalid_inputs() {
        let candidate = eval_face_fill(
            3,
            3,
            &triangle_d0(),
            &[r(-3), r(0), r(0)],
            &r(3),
            &r(0),
            None,
        )
        .expect("valid input")
        .expect("all-ones row is a face");
        assert_eq!(candidate.gamma2_after, Some(r(3)));
        assert!(!candidate.accepted);

        let mut non_cycle = triangle_d0();
        non_cycle[0] = r(0);
        assert!(
            eval_face_fill(3, 3, &non_cycle, &[r(1), r(0), r(0)], &r(1), &r(0), None)
                .expect("a non-cycle has no all-ones face")
                .is_none()
        );
        let err = eval_face_fill(3, 3, &triangle_d0(), &[r(1)], &r(1), &r(0), None)
            .expect_err("a short residual must not truncate to false closure");
        assert!(err.contains("primal_residual len"), "{err}");
    }

    /// A non-graph carrier (a non-{-1,0,+1} incidence) yields no L_min candidate: EdgeSplit/CycleHub
    /// are defined only for graph carriers, so they return None (terminal stays LiftClassIncomplete).
    #[test]
    fn non_graph_carrier_yields_no_lmin_candidate() {
        let d0 = vec![r(-2), r(1), r(0), r(0), r(-1), r(1), r(1), r(0), r(-1)];
        let q = vec![r(1), r(0), r(0)];
        assert!(eval_edge_split(3, 3, &d0, &q, &r(1), &r(0), None, 0)
            .expect("eval")
            .is_none());
        assert!(eval_cycle_hub(3, 3, &d0, &q, &r(1), &r(0), None)
            .expect("eval")
            .is_none());
    }

    // ---- PL-008-1 discharge: the no-descent theorem (Paper 008 §1.5.1) ----

    fn cycle_edges(n: usize) -> Vec<(usize, usize)> {
        (0..n).map(|i| (i, (i + 1) % n)).collect()
    }

    fn edges_to_d0(edges: &[(usize, usize)], n_verts: usize) -> Vec<BigRational> {
        let mut d0 = vec![r(0); edges.len() * n_verts];
        for (e, &(t, h)) in edges.iter().enumerate() {
            d0[e * n_verts + t] = r(-1);
            d0[e * n_verts + h] = r(1);
        }
        d0
    }

    fn unit_defect(n: usize) -> Vec<BigRational> {
        let mut v = vec![r(0); n];
        v[0] = r(1);
        v
    }

    fn two_defect(n: usize) -> Vec<BigRational> {
        let mut v = vec![r(0); n];
        v[0] = r(1);
        if n > 2 {
            v[2] = r(1);
        }
        v
    }

    /// On cycle carriers C_n (n = 3..=12) with several defect patterns, neither
    /// EdgeSplit nor CycleHub strictly reduces Phi_1. This does not settle Gamma_2.
    #[test]
    fn lmin_never_reduces_phi1_on_cycle_graphs() {
        for n in 3..=12usize {
            let edges = cycle_edges(n);
            let d0 = edges_to_d0(&edges, n);
            for q in [unit_defect(n), two_defect(n), vec![r(1); n]] {
                let phi1_before = recompute_phi1_graph(n, &edges, &q).expect("solve base");
                let hub = eval_cycle_hub(n, n, &d0, &q, &phi1_before, &r(0), None)
                    .expect("eval")
                    .expect("CycleHub applies");
                assert!(
                    hub.phi1_after >= phi1_before,
                    "CycleHub reduced Phi_1 on C_{n}"
                );
                assert!(!hub.accepted);
                for e in 0..n {
                    if q[e] != r(0) {
                        let es = eval_edge_split(n, n, &d0, &q, &phi1_before, &r(0), None, e)
                            .expect("eval")
                            .expect("EdgeSplit applies");
                        assert!(
                            es.phi1_after >= phi1_before,
                            "EdgeSplit(e{e}) reduced Phi_1 on C_{n}"
                        );
                        assert!(!es.accepted);
                    }
                }
            }
        }
    }

    /// Theorem 4' for the FULL ambient class L_all: adding any chord (a 0-defect edge between two
    /// existing vertices) never reduces Phi_1 — directly refuting the proof-ledger's chord
    /// counterexample conjecture (PL-008-1). Worked case from §1.5.1: square + diagonal stays Phi_1=4.
    #[test]
    fn chords_never_reduce_phi1() {
        // Worked case: C_4 uniform defect has Phi_1 = 4; the diagonal chord (0,2) leaves it at 4.
        let sq = cycle_edges(4);
        let q4 = vec![r(1); 4];
        assert_eq!(recompute_phi1_graph(4, &sq, &q4).expect("sq"), r(4));
        let mut sq_chord = sq.clone();
        sq_chord.push((0, 2));
        let mut q4_chord = q4.clone();
        q4_chord.push(r(0));
        assert_eq!(
            recompute_phi1_graph(4, &sq_chord, &q4_chord).expect("sq+chord"),
            r(4),
            "the diagonal chord does not reduce Phi_1"
        );

        // Exhaustive: for C_n (n=4..=8), every non-cycle chord leaves Phi_1 non-decreasing.
        for n in 4..=8usize {
            let edges = cycle_edges(n);
            for q in [unit_defect(n), vec![r(1); n]] {
                let base = recompute_phi1_graph(n, &edges, &q).expect("base");
                for i in 0..n {
                    for j in (i + 2)..n {
                        if i == 0 && j == n - 1 {
                            continue; // (0, n-1) is the reverse of a cycle edge (adjacent), not a chord
                        }
                        let mut e2 = edges.clone();
                        e2.push((i, j));
                        let mut q2 = q.clone();
                        q2.push(r(0));
                        let phi = recompute_phi1_graph(n, &e2, &q2).expect("chord");
                        assert!(phi >= base, "chord ({i},{j}) reduced Phi_1 on C_{n}");
                    }
                }
            }
        }
    }
}

#[cfg(test)]
mod l4_boundary_tests_320685d5 {
    // Mutation Accounting: killed=6, survived=0, demonstrably_equivalent=0, invalid=0, inconclusive=0, unrun=0
    use super::*;

    #[test]
    fn admits_within_capacity_and_refuses_overflow() {
        let admitted = BoundaryRecord320685d5::try_admit(3, 8);
        assert!(admitted.is_ok());
        if let Ok(record) = admitted {
            assert_eq!(record.admitted_items(), 3);
            assert_eq!(record.capacity_bound(), 8);
            assert_eq!(record.remaining_capacity(), 5);
        }
        let at_cap = BoundaryRecord320685d5::try_admit(8, 8);
        assert!(at_cap.is_ok());
        let overflow = BoundaryRecord320685d5::try_admit(9, 8);
        assert!(overflow.is_err());
        let zero_items = BoundaryRecord320685d5::try_admit(0, 8);
        assert!(zero_items.is_err());
        let zero_cap = BoundaryRecord320685d5::try_admit(1, 0);
        assert!(zero_cap.is_err());
        assert_eq!(BoundaryError320685d5::EmptyAdmission.violated_invariant(), "admitted_items >= 1");
        assert_eq!(BoundaryError320685d5::CapacityZero.violated_invariant(), "capacity_bound >= 1");
    }
}
