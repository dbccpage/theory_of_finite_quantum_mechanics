//! Sovereign exact rational algebraic certifiers for the Fermion Sign Problem (FSP).
//!
//! AuthorityEffect: None.

#![forbid(unsafe_code)]

pub mod bqnf;
pub mod fock;
pub mod foliated_fracton_lineon;
pub mod gin;
pub mod hubbard;
pub mod normal_forms;
pub mod witness;

pub use bqnf::{route_packet, CochainComplex, SignPacketMetrics, TerminalRoute};
pub use foliated_fracton_lineon::{
    ComplexRat, HingeOrientation, LineonHingeConfig, Mat2x2, QuaternionRat,
};
pub use fock::{
    benchmark_fock_lattice_scaling, car_annihilate, car_create, car_hop,
    fock_scaling_from_canonical_json, fock_scaling_to_canonical_json, jordan_wigner_hop_sign,
    preceding_count, DiscreteFermionicHamiltonian, EulerPath, FermionicLattice,
    FockLatticeScalingRow, FockState, PartitionReceipt, Spin,
};
pub use gin::{
    audit_kitaev_chain_majorana, benchmark_gin_involution_scaling,
    benchmark_kitaev_chain_mzm_scaling, FermionConfiguration, GinIndex,
    InvolutionCancellationReceipt, MajoranaZeroModeReceipt,
};
pub use hubbard::{
    benchmark_hubbard_lattice_scaling, evaluate_hubbard_determinants, exact_determinant,
    exact_kinetic_matrix, exact_matrix_mul, hubbard_rectangular_bonds,
    hubbard_scaling_from_canonical_json, hubbard_scaling_to_canonical_json,
    HubbardDeterminantReceipt, HubbardEnsembleSummary, HubbardLatticeScalingRow,
};
pub use normal_forms::{
    benchmark_sign_switching_grid_scaling, normalize_cochain, normalize_sign_cochain,
    rref_with_witness, QuotientNormalForm, RrefResult, SignSwitchingGridRow,
    SignSwitchingNormalForm,
};
pub use witness::{refuse_foreign_fixture, refuse_removed_holonomy, witness, Witness, HOPS, MASKS};

/// Package level invariant self-test.
pub fn fsp_crate_invariants_hold() -> Result<(), &'static str> {
    let w = witness::witness();
    if w.hop_product != -1 {
        return Err("FSP carrier A hop product must equal -1");
    }
    if w.z_u != 0 || w.n_u != 2 {
        return Err("FSP carrier B orbit invariants must equal Z_u=0, N_u=2");
    }
    let m = bqnf::SignPacketMetrics::new(
        true,
        false,
        num_rational::BigRational::from(num_bigint::BigInt::from(0)),
        num_rational::BigRational::from(num_bigint::BigInt::from(0)),
        false,
    );
    if bqnf::route_packet(&m) != bqnf::TerminalRoute::ExactRepair {
        return Err("Exact metric packet must route to ExactRepair");
    }
    let mzm = gin::audit_kitaev_chain_majorana(4)?;
    if !mzm.is_boundary_isolated {
        return Err("MZM must be boundary isolated on Kitaev chain");
    }
    let lhc = foliated_fracton_lineon::LineonHingeConfig::new(
        foliated_fracton_lineon::HingeOrientation::XAxis,
        0,
        2,
    )?;
    if lhc.can_exchange_without_collision() {
        return Err("1D hinge lineon must forbid collision-free exchange");
    }
    if foliated_fracton_lineon::LineonHingeConfig::hinge_commutator_trace(true) != -2 {
        return Err("Non-abelian hinge commutator trace must be -2");
    }
    Ok(())
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_fsp_crate_invariants() {
        assert!(fsp_crate_invariants_hold().is_ok());
    }
}
