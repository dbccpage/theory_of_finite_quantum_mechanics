// AuthorityEffect: None. Citation: sealed-derivation-v1 (3100c4e)

//! Discrete algebraic carrier definitions for finite quantum mechanics.
//!
//! Formalizes the carrier domains, coefficient boundaries, and exact zero relations
//! across exact rational, cyclotomic, and finite-field quantum representations.

use serde::{Deserialize, Serialize};

/// Target operational scope for finite quantum mechanical carriers.
#[derive(Debug, Clone, Copy, PartialEq, Eq, Serialize, Deserialize)]
pub enum DiscreteCarrierScope {
    /// Dimension 3 Maximal MUBs and Linear Inversion State Tomography (Target 22).
    Dimension3MubTomography,
    /// Dimension 5 Discrete Gross Phase Space and Wigner Negativity (Target 13).
    Dimension5WignerPhaseSpace,
    /// Finite Stone-von Neumann and Commutator Trace Obstruction (Target 19).
    FiniteCommutatorObstruction,
    /// Exact Rational Pythagorean and Bell Nonlocality (Loop 4).
    RationalBellChsh,
}

/// Status of the algebraic carrier specification.
#[derive(Debug, Clone, Copy, PartialEq, Eq, Serialize, Deserialize)]
pub enum DiscreteCarrierStatus {
    Declared,
    AlgebraicallyVerified,
}

/// Descriptive specification of an exact discrete carrier.
#[derive(Debug, Clone, PartialEq, Eq, Serialize, Deserialize)]
pub struct DiscreteQmCarrier {
    pub scope: DiscreteCarrierScope,
    pub dimension: usize,
    pub field_name: &'static str,
    pub ring_signature: &'static str,
    pub zero_relation: &'static str,
    pub status: DiscreteCarrierStatus,
    pub verified_properties: Vec<&'static str>,
}

/// Construct the carrier for Target 22: Dimension 3 Maximal MUB System and Tomography.
pub fn carrier_d3_mub_tomography() -> DiscreteQmCarrier {
    DiscreteQmCarrier {
        scope: DiscreteCarrierScope::Dimension3MubTomography,
        dimension: 3,
        field_name: "Q(zeta_3) (Eisenstein rationals) embedded in Q(zeta_24)",
        ring_signature: "Z[zeta_3] minimal polynomial x^2 + x + 1 = 0",
        zero_relation: "exact polynomial coefficient equality, zero float tolerance",
        status: DiscreteCarrierStatus::Declared,
        verified_properties: vec![
            "4 maximal MUB bases in d=3",
            "3 states per basis (12 states total)",
            "exact rank-one projector idempotence Pi^2 = Pi",
            "within-basis resolution sum_k Pi_{b,k} = I_3",
            "cross-basis trace overlap Tr(Pi_{b,k} Pi_{b',k'}) = 1/3 for b != b'",
            "exact linear inversion state reconstruction rho = sum p_{b,k} Pi_{b,k} - I_3",
        ],
    }
}

/// Construct the carrier for Target 13: Dimension 5 Discrete Wigner Phase Space.
pub fn carrier_d5_wigner_phase_space() -> DiscreteQmCarrier {
    DiscreteQmCarrier {
        scope: DiscreteCarrierScope::Dimension5WignerPhaseSpace,
        dimension: 5,
        field_name: "Q(zeta_5) (5th cyclotomic field)",
        ring_signature: "Z[zeta_5] minimal polynomial x^4 + x^3 + x^2 + x + 1 = 0",
        zero_relation: "exact cyclotomic polynomial equality",
        status: DiscreteCarrierStatus::Declared,
        verified_properties: vec![
            "25 phase point operators A(q, p) on F_5 x F_5",
            "exact trace Tr(A(u)) = 1",
            "phase point orthogonality Tr(A(u) A(v)) = 5 delta_{u,v}",
            "phase space resolution sum_u A(u) = 5 I_5",
            "Gross stabilizer covariance under displacements",
            "magic state negative Wigner value W(0, 0) = -1/5",
        ],
    }
}

/// Construct the carrier for Target 19: Finite Commutator Trace Obstruction.
pub fn carrier_finite_commutator_obstruction(n: usize) -> DiscreteQmCarrier {
    DiscreteQmCarrier {
        scope: DiscreteCarrierScope::FiniteCommutatorObstruction,
        dimension: n,
        field_name: "Q (exact rationals)",
        ring_signature: "Z/NZ discrete translation ring",
        zero_relation: "Tr([Q, P]) = 0 exact identity in any trace-cyclic algebra",
        status: DiscreteCarrierStatus::Declared,
        verified_properties: vec![
            "Tr(AB - BA) = 0 for any finite NxN operators",
            "obstruction Tr([Q, P]) = 0 != i N * I_N",
            "finite Stone-von Neumann uniqueness of Heisenberg-Weyl representation",
        ],
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn carrier_declarations_do_not_self_assign_verification() {
        let c3 = carrier_d3_mub_tomography();
        assert_eq!(c3.dimension, 3);
        assert_eq!(c3.status, DiscreteCarrierStatus::Declared);

        let c5 = carrier_d5_wigner_phase_space();
        assert_eq!(c5.dimension, 5);
        assert_eq!(c5.status, DiscreteCarrierStatus::Declared);

        let c_obs = carrier_finite_commutator_obstruction(3);
        assert_eq!(c_obs.dimension, 3);
        assert_eq!(c_obs.status, DiscreteCarrierStatus::Declared);
    }
}
