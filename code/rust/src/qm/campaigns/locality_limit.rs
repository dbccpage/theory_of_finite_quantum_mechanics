use omega_number_theory::rational::{ri, rq};
use omega_quantum_physics::continuous_time_locality_limit::*;
use serde_json::json;
pub fn audit_c250_dense_orbit() -> (&'static str, bool) {
    ("NARROWED", false)
}

pub fn generate_canonical_block06_rust_receipt() -> serde_json::Value {
    let (status, dense_implies) = audit_c250_dense_orbit();
    let b1 = trotter_first_order_error_bound(&rq(1, 2), &10.into(), &ri(2))
        .expect("fixed nonnegative bound");
    let b2 = trotter_second_order_error_bound(&rq(1, 2), &10.into(), &ri(4), &ri(4))
        .expect("fixed nonnegative bounds");
    let outside_cone = DeclaredInteractionGraph::new(5, &[(0, 1), (1, 2), (2, 3), (3, 4)])
        .expect("fixed path")
        .outside_cone(0, 4, &ri(1), &ri(2))
        .expect("declared cone");

    json!({
        "campaign": "C500",
        "block": "block_06",
        "authority_effect": "None",
        "terminal_outcome": "CONDITIONAL_PRODUCT_FORMULA_BOUNDS_LOCALITY_OPEN",
        "predecessor_binding_status": "NOT_VERIFIED_BY_KERNEL",
        "trotter_first_order_bound": format!("{}/{}", b1.numer(), b1.denom()),
        "trotter_second_order_bound": format!("{}/{}", b2.numer(), b2.denom()),
        "outside_declared_cone": outside_cone,
        "locality_bound_status": "OPEN_MISSING_INTERACTION_AND_BOUND_CONSTANTS",
        "dense_orbit_audit_status": status,
        "dense_orbit_alone_implies_continuous_action": dense_implies,
        "status": "SCOPED_FORMULA_EVALUATION",
        "fixture": {"A": [[0, 1], [1, 0]], "B": [[1, 0], [0, -1]]},
        "bound_source": "https://arxiv.org/abs/1912.08854 (section 5.1)"
    })
}

#[cfg(test)]
mod tests {
    use super::*;
    #[test]
    fn test_dense_orbit_audit() {
        let (status, implies_continuous) = audit_c250_dense_orbit();
        assert_eq!(status, "NARROWED");
        assert!(!implies_continuous);
    }
}
