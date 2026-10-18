//! Continuum Lift and Boundary Classification for Finite Quantum Mechanics (Band E).
//!
//! AuthorityEffect: None.
//! Citation: sealed-derivation-v1 (3100c4e).

use crate::linear_algebra::matrix as mx;
use omega_number_theory::cyclotomic::GaussianRat;
use omega_number_theory::rational::Rational;
use omega_quantum_physics::continuum::canonical_commutator_obstruction;

/// Wintner-Wielandt trace evaluation on finite-dimensional matrices.
#[derive(Debug, Clone, PartialEq, Eq)]
pub struct WintnerWielandtWitness {
    pub dimension: usize,
    pub trace_commutator: Rational,
    pub trace_identity_coefficient: usize,
    pub is_obstructed: bool,
}

impl WintnerWielandtWitness {
    /// In any finite dimension d >= 1, tr(AB - BA) = 0 in any commutative ring,
    /// whereas tr(c * I_d) = d * c. If c != 0, tr(AB - BA) = tr(c * I_d) is algebraically obstructed.
    pub fn new(dimension: usize) -> Self {
        assert!(dimension >= 1, "Dimension must be >= 1");
        assert!(dimension <= 128, "finite dimension budget is 128");
        let a = mx::from_fn(dimension, dimension, |r, c| {
            if r == c {
                GaussianRat::from_rational(Rational::from_integer(r.into()))
            } else {
                GaussianRat::zero()
            }
        })
        .expect("admitted matrix");
        let b = mx::from_fn(dimension, dimension, |r, c| {
            if c == (r + 1) % dimension {
                GaussianRat::one()
            } else {
                GaussianRat::zero()
            }
        })
        .expect("admitted matrix");
        let certificate = canonical_commutator_obstruction(&a, &b, &GaussianRat::one())
            .expect("declared equal square operators");
        let tr_comm = certificate.trace_commutator.re;
        Self {
            dimension,
            trace_commutator: tr_comm,
            trace_identity_coefficient: dimension,
            is_obstructed: certificate.equality_obstructed,
        }
    }
}

/// Weyl-Heisenberg clock and shift operator invariants in dimension d.
#[derive(Debug, Clone, PartialEq, Eq)]
pub struct WeylHeisenbergInvariants {
    pub dimension: usize,
    pub clock_period: usize,
    pub shift_period: usize,
    pub root_of_unity_order: usize,
    pub weyl_commutation_holds: bool,
}

impl WeylHeisenbergInvariants {
    pub fn new(dimension: usize) -> Self {
        assert!(dimension >= 2, "Dimension must be >= 2");
        let holds = match dimension {
            2 => weyl_fixture::<2, 4>(),
            3 => weyl_fixture::<3, 6>(),
            4 => weyl_fixture::<4, 8>(),
            5 => weyl_fixture::<5, 10>(),
            6 => weyl_fixture::<6, 12>(),
            7 => weyl_fixture::<7, 14>(),
            8 => weyl_fixture::<8, 16>(),
            _ => panic!("declared campaign Weyl fixtures have dimension 2..=8"),
        };
        Self {
            dimension,
            clock_period: dimension,
            shift_period: dimension,
            root_of_unity_order: dimension,
            weyl_commutation_holds: holds,
        }
    }
}

fn weyl_fixture<const D: usize, const C: usize>() -> bool {
    use omega_number_theory::cyclotomic_field::Cyclotomic;
    let omega = Cyclotomic::<C>::zeta(2);
    let system = if D % 2 == 0 {
        omega_lie_theory::heisenberg::WeylHeisenberg::with_phase_root(
            D,
            omega,
            Cyclotomic::<C>::zeta(1),
        )
    } else {
        omega_lie_theory::heisenberg::WeylHeisenberg::new(D, omega)
    }
    .expect("fixed primitive phase");
    system.verify_relations() == Ok(true)
}

/// Structural inventory of gains and losses under the continuum completion functor Q^ab -> C.
#[derive(Debug, Clone, PartialEq, Eq)]
pub struct ContinuumBoundaryReport {
    pub authority_effect: &'static str,
    pub citation: &'static str,
    pub band: &'static str,
    pub bet_id: &'static str,
    pub gap_id: &'static str,
    pub gap_status: &'static str,
    pub structural_gains_count: usize,
    pub structural_losses_count: usize,
    pub finite_internal_targets_count: usize,
    pub continuum_interface_targets_count: usize,
}

impl Default for ContinuumBoundaryReport {
    fn default() -> Self {
        Self {
            authority_effect: "None",
            citation: "sealed-derivation-v1 (3100c4e)",
            band: "Band E (Steps 39-46)",
            bet_id: "BET-E",
            gap_id: "GAP-F001-S000-002",
            gap_status: "PRICED_CONTINUUM_INTERFACE",
            structural_gains_count: 5,
            structural_losses_count: 5,
            finite_internal_targets_count: 19,
            continuum_interface_targets_count: 3,
        }
    }
}

#[cfg(test)]
mod tests {
    use super::*;
    use omega_number_theory::rational::r_zero;

    #[test]
    fn test_wintner_wielandt_trace_obstruction() {
        for d in 1..=16 {
            let witness = WintnerWielandtWitness::new(d);
            assert_eq!(witness.trace_commutator, r_zero());
            assert_eq!(witness.trace_identity_coefficient, d);
            assert!(witness.is_obstructed);
        }
    }

    #[test]
    fn test_weyl_heisenberg_invariants() {
        for d in 2..=8 {
            let wh = WeylHeisenbergInvariants::new(d);
            assert_eq!(wh.dimension, d);
            assert_eq!(wh.clock_period, d);
            assert_eq!(wh.shift_period, d);
            assert!(wh.weyl_commutation_holds);
        }
    }

    #[test]
    fn test_continuum_boundary_report() {
        let r = ContinuumBoundaryReport::default();
        assert_eq!(r.authority_effect, "None");
        assert_eq!(r.gap_id, "GAP-F001-S000-002");
        assert_eq!(r.gap_status, "PRICED_CONTINUUM_INTERFACE");
        assert_eq!(r.structural_gains_count, 5);
        assert_eq!(r.structural_losses_count, 5);
        assert_eq!(r.finite_internal_targets_count, 19);
        assert_eq!(r.continuum_interface_targets_count, 3);
    }
}
