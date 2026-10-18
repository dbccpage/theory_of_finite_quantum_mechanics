//! Sovereign exact rational algebraic certifiers for the Fermion Sign Problem (FSP).
//!
//! AuthorityEffect: None.

#![forbid(unsafe_code)]

pub mod bqnf;
pub mod fock;
pub mod gin;
pub mod hubbard;
pub mod normal_forms;
pub mod witness;

pub use bqnf::{route_packet, CochainComplex, SignPacketMetrics, TerminalRoute};
pub use fock::{
    car_annihilate, car_create, car_hop, jordan_wigner_hop_sign, preceding_count,
    DiscreteFermionicHamiltonian, EulerPath, FermionicLattice, FockState, PartitionReceipt, Spin,
};
pub use gin::{
    audit_kitaev_chain_majorana, FermionConfiguration, GinIndex, InvolutionCancellationReceipt,
    MajoranaZeroModeReceipt,
};
pub use hubbard::{
    evaluate_hubbard_determinants, exact_determinant, exact_kinetic_matrix, exact_matrix_mul,
    HubbardDeterminantReceipt, HubbardEnsembleSummary,
};
pub use normal_forms::{
    normalize_cochain, normalize_sign_cochain, rref_with_witness, QuotientNormalForm, RrefResult,
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
