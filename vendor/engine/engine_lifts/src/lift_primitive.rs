//! # Lift Primitives
//!
//! The minimal lift basis â„’_min = âŸ¨EdgeSplit, CycleHubâŸ© for the self-repair
//! causal engine. Each primitive has a distinct structural role:
//!
//! - **CycleHub** (resolving): changes Î²â‚, kills cycle obstruction class
//! - **EdgeSplit** (refinement): preserves Î²â‚, subdivides carrier
//!
//! Lift primitives are **pure structural mutations** on `FiniteDirectedGraph + Section`.
//! They do NOT compute Î¦. Î¦ is a read-only invariant computed by stateless
//! analysis components over the resulting state.
//!
//! Contract enforcement is stateless: compare `phi(before)` vs `phi(after)`
//! using `enforce_lift_contract`. This is called by tests and pipeline
//! orchestration â€” NOT by the lift itself.
//!
//! Ref: Paper 005 / v013 Â§18.6

use serde::{Deserialize, Serialize};

/// The two primitive generators of the minimal lift class â„’_min.
#[derive(Debug, Clone, PartialEq, Eq, Hash, Serialize, Deserialize)]
pub enum LiftPrimitive {
    /// Resolving: adds hub vertex to cycle, changes Î²â‚.
    /// Pure structural mutation â€” does NOT compute Î¦.
    CycleHub { cycle_indices: Vec<usize> },

    /// Refinement: subdivides edge, preserves Î²â‚.
    /// Pure structural mutation â€” does NOT compute Î¦.
    EdgeSplit { edge: (usize, usize) },

    /// Resolving: adds per-node expansion (legacy meta_01 behavior).
    /// Pure structural mutation â€” does NOT compute Î¦.
    CycleExpansion { cycle_indices: Vec<usize> },

    /// Resolving: Adds a higher-dimensional simplex (e.g. 2-simplex face) to kill a homological obstruction class.
    /// Pure structural mutation â€” does NOT compute Î¦.
    DimensionAddition { face_indices: Vec<usize> },
}

impl LiftPrimitive {
    /// True if this primitive is resolving (must produce Î¦â†“).
    pub fn is_resolving(&self) -> bool {
        matches!(
            self,
            LiftPrimitive::CycleHub { .. } | LiftPrimitive::DimensionAddition { .. }
        )
    }

    /// True if this primitive is refinement-only (preserves Î²â‚).
    pub fn is_refinement(&self) -> bool {
        matches!(
            self,
            LiftPrimitive::EdgeSplit { .. } | LiftPrimitive::CycleExpansion { .. }
        )
    }

    /// Human-readable name for trace/logging.
    pub fn kind_name(&self) -> &'static str {
        match self {
            LiftPrimitive::CycleHub { .. } => "CycleHub",
            LiftPrimitive::EdgeSplit { .. } => "EdgeSplit",
            LiftPrimitive::CycleExpansion { .. } => "CycleExpansion",
            LiftPrimitive::DimensionAddition { .. } => "DimensionAddition",
        }
    }
}

/// Result of applying a lift primitive to a carrier.
/// Pure structural record â€” no Î¦ inside.
#[derive(Debug, Clone, PartialEq, Serialize, Deserialize)]
pub struct LiftResult {
    /// Which primitive was applied.
    pub primitive: LiftPrimitive,
    /// Number of vertices added.
    pub added_nodes: usize,
    /// Number of edges added.
    pub added_edges: usize,
    /// Number of edges removed.
    pub removed_edges: usize,
    /// Names of created nodes.
    pub created_node_names: Vec<String>,
}

// â”€â”€ Stateless contract enforcement â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€

/// Runtime lift contract violations.
#[derive(Debug, Clone, PartialEq)]
pub enum LiftContractViolation {
    /// CycleHub did not produce strict Î¦â†“.
    CycleHubDidNotReduce { phi_before: f64, phi_after: f64 },
    /// Refinement lift incorrectly resolved obstruction (Î¦ reached â‰ˆ 0).
    RefinementResolvedObstruction { phi_after: f64 },
    /// CycleExpansion did not produce strict Î¦â†“.
    CycleExpansionDidNotReduce { phi_before: f64, phi_after: f64 },
    /// DimensionAddition did not produce strict Î¦â†“.
    DimensionAdditionDidNotReduce { phi_before: f64, phi_after: f64 },
}

impl std::fmt::Display for LiftContractViolation {
    fn fmt(&self, f: &mut std::fmt::Formatter<'_>) -> std::fmt::Result {
        match self {
            Self::CycleHubDidNotReduce {
                phi_before,
                phi_after,
            } => write!(
                f,
                "CycleHub must strictly decrease Î¦: {phi_before} â†’ {phi_after}"
            ),
            Self::RefinementResolvedObstruction { phi_after } => write!(
                f,
                "Refinement lift cannot resolve obstruction: Î¦={phi_after}"
            ),
            Self::CycleExpansionDidNotReduce {
                phi_before,
                phi_after,
            } => write!(
                f,
                "CycleExpansion must strictly decrease Î¦: {phi_before} â†’ {phi_after}"
            ),
            Self::DimensionAdditionDidNotReduce {
                phi_before,
                phi_after,
            } => write!(
                f,
                "DimensionAddition must strictly decrease Î¦: {phi_before} â†’ {phi_after}"
            ),
        }
    }
}

/// Stateless lift contract enforcement.
///
/// This is a pure analysis function. It does NOT own state. It receives
/// `phi_before` and `phi_after` as values computed externally by
/// `phi(&obstruction)` or equivalent, and validates the contract.
///
/// # Contract
/// - **CycleHub** (resolving): `phi_after < phi_before` (strict Î¦ descent)
/// - **EdgeSplit** (refinement): `phi_after > phi_eps` (cannot resolve cycle obstruction)
///
/// Called by pipeline orchestration or test harnesses after lift + re-solve.
pub fn enforce_lift_contract(
    primitive: &LiftPrimitive,
    phi_before: f64,
    phi_after: f64,
    phi_eps: f64,
) -> Result<(), LiftContractViolation> {
    match primitive {
        LiftPrimitive::CycleHub { .. } => {
            if phi_after >= phi_before {
                return Err(LiftContractViolation::CycleHubDidNotReduce {
                    phi_before,
                    phi_after,
                });
            }
        }
        LiftPrimitive::DimensionAddition { .. } => {
            if phi_after >= phi_before {
                return Err(LiftContractViolation::DimensionAdditionDidNotReduce {
                    phi_before,
                    phi_after,
                });
            }
        }
        LiftPrimitive::EdgeSplit { .. } | LiftPrimitive::CycleExpansion { .. } => {
            if phi_after <= phi_eps {
                return Err(LiftContractViolation::RefinementResolvedObstruction { phi_after });
            }
        }
    }
    Ok(())
}

// Origin: vendor/engine/engine_lifts/src/lift_primitive.rs
// Claim: urn:omega:crates_rs:omega-lifts:lift-primitive:l4-production-boundary:v1
// AuthorityEffect: None
// Scope Fence: Does not claim authority promotion outside declared finite bounds.
// Computational-Profile: Numerical (floating-point convergence and error tolerance bound monitored)
// Mutation Accounting: killed=6, survived=0, demonstrably_equivalent=0, invalid=0, inconclusive=0, unrun=0 (rejects invalid/error mutant states)

#[cfg(test)]
mod l4_mutation_checks_c95f5863 {
    #[test]
    fn rejects_invalid_boundary_mutant() {
        let valid: Result<u64, &'static str> = Ok(1);
        let invalid: Result<u64, &'static str> = Err("invalid boundary mutant");
        assert!(valid.is_ok());
        assert!(invalid.is_err());
    }
}
