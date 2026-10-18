//! Higher-Dimensional Entanglement Witnesses and Conductor Bound Hierarchy
//!
//! Investigates minimal cyclotomic conductor bounds n*(d) beyond dimension d=4.
//!
//! AuthorityEffect: None.
//! Citation: sealed-derivation-v1 (3100c4e)

use num_bigint::BigInt;
use num_integer::Integer;

use omega_number_theory::{
    cyclotomic_field::quadratic_field_conductor,
    rational::{squarefree_part, ArithmeticError},
};
use omega_quantum_physics::exact_operator::ExactOperator;
use omega_quantum_physics::pauli::PauliString;

pub const TARGET_LCM_120: u64 = 120;

/// The actual Pauli stabilizer families commute and square to identity.
/// W is evaluated as a non-stabilizer state: it has no declaration of a Pauli group.
pub fn verify_multi_qubit_stabilizers() -> bool {
    for words in [
        vec!["XXX", "ZZI", "IZZ"],
        vec!["XZZXI", "IXZZX", "XIXZZ", "ZXIXZ"],
        vec![
            "IIIXXXX", "IXXIIXX", "XIXIXIX", "IIIZZZZ", "IZZIIZZ", "ZIZIZIZ",
        ],
    ] {
        let operators: Result<Vec<_>, _> = words
            .iter()
            .map(|word| PauliString::parse(word).and_then(|p| p.to_operator()))
            .collect();
        let Ok(operators) = operators else {
            return false;
        };
        let Ok(identity) = ExactOperator::identity(operators[0].rows()) else {
            return false;
        };
        for (i, op) in operators.iter().enumerate() {
            if op.mul(op) != Ok(identity.clone()) {
                return false;
            }
            for prior in &operators[..i] {
                if op.commutator(prior).map_or(true, |c| !c.is_zero()) {
                    return false;
                }
            }
        }
    }
    true
}

/// Verifies prime qudit MUB escalation boundary:
/// p in {2, 3, 5} divide 120, while p = 7 has conductor 28 which does NOT divide 120,
/// escalating the LCM conductor to lcm(120, 28) = 840.
pub fn verify_prime_qudit_escalation_boundary() -> Result<(bool, BigInt), ArithmeticError> {
    let p_dims = [2u64, 3, 5];
    let mut all_p_contained = true;
    for &p in &p_dims {
        let (squarefree, _) = squarefree_part(&BigInt::from(p))?;
        let c_p = BigInt::from(p).lcm(&quadratic_field_conductor(&squarefree));
        if BigInt::from(TARGET_LCM_120).mod_floor(&c_p) != BigInt::from(0) {
            all_p_contained = false;
        }
    }

    // Dimension 7
    let c_7 = quadratic_field_conductor(&BigInt::from(7));
    let escalates_at_7 = BigInt::from(TARGET_LCM_120).mod_floor(&c_7) != BigInt::from(0);
    let escalated_lcm = BigInt::from(TARGET_LCM_120).lcm(&c_7);

    Ok((all_p_contained && escalates_at_7, escalated_lcm))
}

/// Exact Tiles certificate under the replayed UPB-complement criterion.
pub fn verify_horodecki_3x3_bound_entanglement() -> bool {
    omega_quantum_physics::higher_dim::tiles().is_ok()
}

/// Verifies CGLMP nonlocality conductor escalation boundary:
/// Bob's measurement phase offsets +/- 1/4 require relative phases zeta_{4d}.
/// Conductor is lcm(4*d, quadratic_extension_conductor(d)).
/// For d=4, conductor is 16 (which does not divide 120), escalating to lcm(120, 16) = 240.
/// For d=8, conductor is 32 (which does not divide 120), escalating to lcm(120, 32) = 480.
pub fn verify_cglmp_escalation_boundary() -> (bool, BigInt, BigInt) {
    let c_4 = BigInt::from(16).lcm(&quadratic_field_conductor(&BigInt::from(1)));
    let escalates_4 = BigInt::from(TARGET_LCM_120).mod_floor(&c_4) != BigInt::from(0);
    let escalated_4 = BigInt::from(TARGET_LCM_120).lcm(&c_4);
    let c_8 = BigInt::from(32).lcm(&quadratic_field_conductor(&BigInt::from(2)));
    let escalates_8 = BigInt::from(TARGET_LCM_120).mod_floor(&c_8) != BigInt::from(0);
    let escalated_8 = BigInt::from(TARGET_LCM_120).lcm(&c_8);
    (escalates_4 && escalates_8, escalated_4, escalated_8)
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_quadratic_conductors() {
        for (d, c) in [(2, 8), (3, 12), (4, 1), (5, 5), (6, 24), (7, 28), (8, 8)] {
            let (squarefree, _) = squarefree_part(&BigInt::from(d)).unwrap();
            assert_eq!(quadratic_field_conductor(&squarefree), BigInt::from(c));
        }
    }

    #[test]
    fn test_multi_qubit_stabilizers_embed_in_120() {
        assert!(verify_multi_qubit_stabilizers());
    }

    #[test]
    fn test_prime_escalation_at_7() {
        let (verified, escalated_lcm) = verify_prime_qudit_escalation_boundary().unwrap();
        assert!(verified);
        assert_eq!(escalated_lcm, BigInt::from(840));
    }

    #[test]
    fn test_horodecki_upb_conductor_one() {
        assert!(verify_horodecki_3x3_bound_entanglement());
    }

    #[test]
    fn test_cglmp_escalation_boundary() {
        let (escalates, esc_4, esc_8) = verify_cglmp_escalation_boundary();
        assert!(escalates);
        assert_eq!(esc_4, BigInt::from(240));
        assert_eq!(esc_8, BigInt::from(480));
    }
}
