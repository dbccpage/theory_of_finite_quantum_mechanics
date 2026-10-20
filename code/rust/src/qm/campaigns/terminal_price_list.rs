
use serde::{Deserialize, Serialize};

#[derive(Debug, Clone, PartialEq, Eq, Serialize, Deserialize)]
pub struct Declaration {
    pub index: usize,
    pub name: String,
    pub label: String,
    pub description: String,
    pub is_primitive: bool,
    pub status: String,
}

#[derive(Debug, Clone, PartialEq, Eq, Serialize, Deserialize)]
pub struct FormalRefusal {
    pub index: usize,
    pub name: String,
    pub obstruction_type: String,
    pub description: String,
}

pub const BORN_STATUS: &str = "CONDITIONAL_EFFECT_MODELS_GENERAL_BRIDGE_OPEN";
pub const DYNAMICS_STATUS: &str = "FINITE_PERIODIC_AND_APERIODIC_MODELS_TOPOLOGY_DECLARED";
pub const CONTINUUM_STATUS: &str = "COMPLETION_AND_EMBEDDING_REQUIRE_ASSUMPTIONS";
pub const TERMINAL_CLAIM: &str = "Finite algebraic models and conditional obstructions are established in their stated scopes; effect-domain representation, dynamics, and continuum bridges require their recorded hypotheses. The six declarations form a chosen inventory; their independence and exhaustiveness are open.";

pub fn get_declarations() -> Vec<Declaration> {
    vec![
        Declaration {
            index: 1,
            name: "effect_domain".to_string(),
            label: "Effect Domain of Probability".to_string(),
            description: "Admission of the effect algebra domain (POVMs) supporting cyclic path transport and Bargmann 3-loop trace invariants tr(E_A E_B E_C).".to_string(),
            is_primitive: true,
            status: "DECLARED".to_string(),
        },
        Declaration {
            index: 2,
            name: "real_embedding".to_string(),
            label: "Single Real Embedding".to_string(),
            description: "Selection of one real embedding into R fixing positive branch orientations for algebraic roots and sign conventions.".to_string(),
            is_primitive: true,
            status: "DECLARED".to_string(),
        },
        Declaration {
            index: 3,
            name: "tensor_product_composition".to_string(),
            label: "Tensor Product Composition".to_string(),
            description: "Combining axioms and composition rule combining subsystems into composite tensor products while preserving local discrete holonomies.".to_string(),
            is_primitive: true,
            status: "DECLARED".to_string(),
        },
        Declaration {
            index: 4,
            name: "dynamics_generator_lift".to_string(),
            label: "Dynamics Generator Lift".to_string(),
            description: "Generator lift mapping discrete periodic unitary steps Q/Z to a continuous time flow parameter.".to_string(),
            is_primitive: true,
            status: "DECLARED".to_string(),
        },
        Declaration {
            index: 5,
            name: "branch_weighting_beyond_rational".to_string(),
            label: "Branch Weighting Beyond Rational Sector".to_string(),
            description: "Fine-graining or weighting of branches beyond the rational sector where integer branch counting admits no exact solution.".to_string(),
            is_primitive: true,
            status: "DECLARED".to_string(),
        },
        Declaration {
            index: 6,
            name: "conductor_escalation_purification".to_string(),
            label: "Conductor Escalation for Purification".to_string(),
            description: "Acceptance of unbounded conductor escalation for purification in the directed union tower Q^ab.".to_string(),
            is_primitive: true,
            status: "DECLARED".to_string(),
        },
    ]
}

pub fn get_declaration_count() -> usize {
    get_declarations().len()
}

fn accumulate_declaration_indices(decls: &[Declaration]) -> Result<usize, &'static str> {
    let n = decls.len();
    let mut seen = vec![false; n];
    let mut from_fields = 0usize;
    for decl in decls {
        if decl.name.is_empty() || decl.index == 0 || decl.index > n {
            return Err("declaration index is outside 1..=n");
        }
        if seen[decl.index - 1] {
            return Err("declaration index is duplicated");
        }
        seen[decl.index - 1] = true;
        from_fields = from_fields
            .checked_add(decl.index)
            .ok_or("index mass overflow")?;
    }
    Ok(from_fields)
}

fn verify_triangular_index_sum(n: usize, from_fields: usize) -> Result<(), &'static str> {
    let mut series = 0usize;
    for index in 1..=n {
        series = series.checked_add(index).ok_or("index mass overflow")?;
    }
    let closed = n.checked_mul(n.checked_add(1).ok_or("count")?).ok_or("count")? / 2;
    if from_fields != series || series != closed {
        return Err("declaration index mass disagrees with n(n+1)/2");
    }
    Ok(())
}

pub fn inventory_index_mass() -> Result<usize, &'static str> {
    let decls = get_declarations();
    let n = decls.len();
    if n == 0 {
        return Err("price list is empty");
    }
    let from_fields = accumulate_declaration_indices(&decls)?;
    verify_triangular_index_sum(n, from_fields)?;
    Ok(from_fields)
}

pub fn any_declaration_named_born_rule() -> bool {
    let decls = get_declarations();
    for d in &decls {
        let n = d.name.to_lowercase();
        let l = d.label.to_lowercase();
        if n == "born_rule"
            || n == "the_born_rule"
            || n == "born"
            || n == "born_postulate"
            || l.contains("born rule")
        {
            return true;
        }
    }
    false
}

pub fn get_formal_refusals() -> Vec<FormalRefusal> {
    vec![
        FormalRefusal {
            index: 1,
            name: "irrational_sector_branch_counting_refusal".to_string(),
            obstruction_type: "ALGEBRAIC_INTEGER_COUNTING_OBSTRUCTION".to_string(),
            description: "Equal-weight integer branch counting admits no finite representation for irrational Born weights without remainder.".to_string(),
        },
        FormalRefusal {
            index: 2,
            name: "unconditioned_d2_projective_frame_functions_refusal".to_string(),
            obstruction_type: "TOPOLOGICAL_DISCONNECTEDNESS_OBSTRUCTION".to_string(),
            description: "Dimension d=2 projective measurements admit non-Bornian frame assignments unless extended to the effect domain.".to_string(),
        },
        FormalRefusal {
            index: 3,
            name: "single_finite_conductor_carrier_refusal".to_string(),
            obstruction_type: "CYCLOTOMIC_FIELD_DEGREE_OBSTRUCTION".to_string(),
            description: "No single finite cyclotomic field Q(zeta_n) can host all prime-qudit MUB families, refusing bounded conductor escalation.".to_string(),
        },
    ]
}

pub fn get_refusal_count() -> usize {
    get_formal_refusals().len()
}

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct Block10VerificationReport {
    pub declaration_count: usize,
    pub any_declaration_named_born_rule: bool,
    pub born_status: String,
    pub dynamics_status: String,
    pub continuum_status: String,
    pub standing_bets_scored: bool,
    pub terminal_claim_verified: bool,
    pub declarations_independent: Option<bool>,
    pub refusal_count: usize,
    pub terminal_claim: String,
    pub declarations: Vec<Declaration>,
    pub refusals: Vec<FormalRefusal>,
}

pub fn run_block_10_verification() -> Block10VerificationReport {
    Block10VerificationReport {
        declaration_count: get_declaration_count(),
        any_declaration_named_born_rule: any_declaration_named_born_rule(),
        born_status: BORN_STATUS.to_string(),
        dynamics_status: DYNAMICS_STATUS.to_string(),
        continuum_status: CONTINUUM_STATUS.to_string(),
        standing_bets_scored: false,
        terminal_claim_verified: false,
        declarations_independent: None,
        refusal_count: get_refusal_count(),
        terminal_claim: TERMINAL_CLAIM.to_string(),
        declarations: get_declarations(),
        refusals: get_formal_refusals(),
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_declaration_count_in_bounds() {
        let count = get_declaration_count();
        assert!((5..=7).contains(&count));
        assert!((5..=8).contains(&count));
        assert_eq!(count, 6);
    }

    #[test]
    fn test_no_born_rule_primitive() {
        assert!(!any_declaration_named_born_rule());
    }

    #[test]
    fn test_statuses() {
        assert_eq!(BORN_STATUS, "CONDITIONAL_EFFECT_MODELS_GENERAL_BRIDGE_OPEN");
        assert_eq!(
            DYNAMICS_STATUS,
            "FINITE_PERIODIC_AND_APERIODIC_MODELS_TOPOLOGY_DECLARED"
        );
        assert_eq!(
            CONTINUUM_STATUS,
            "COMPLETION_AND_EMBEDDING_REQUIRE_ASSUMPTIONS"
        );
    }

    #[test]
    fn test_refusal_count_in_bounds() {
        let count = get_refusal_count();
        assert!((2..=5).contains(&count));
        assert_eq!(count, 3);
    }

    #[test]
    fn test_full_report() {
        let rep = run_block_10_verification();
        assert_eq!(rep.declaration_count, 6);
        assert!(!rep.any_declaration_named_born_rule);
        assert_eq!(
            rep.born_status,
            "CONDITIONAL_EFFECT_MODELS_GENERAL_BRIDGE_OPEN"
        );
        assert_eq!(
            rep.dynamics_status,
            "FINITE_PERIODIC_AND_APERIODIC_MODELS_TOPOLOGY_DECLARED"
        );
        assert_eq!(
            rep.continuum_status,
            "COMPLETION_AND_EMBEDDING_REQUIRE_ASSUMPTIONS"
        );
        assert!(!rep.standing_bets_scored);
        assert!(!rep.terminal_claim_verified);
        assert_eq!(rep.declarations_independent, None);
        assert_eq!(rep.refusal_count, 3);
        assert!(rep
            .terminal_claim
            .contains("independence and exhaustiveness are open"));
    }
}
