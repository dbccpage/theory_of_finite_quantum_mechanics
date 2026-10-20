extern crate self as omega_combinatorics;

pub const PROVENANCE: &str = "Origin: code/rust/src/combinatorics/lib.rs\nClaim: urn:omega:fqm:combinatorics:crate-surface:v1\nAuthorityEffect: None\nScope Fence: the crate root does not classify MUBs outside the certified prime-ray construction and does not inherit an authority grant.\nMutation-Kills: 1 non-equivalent source mutant, executed by cargo test -p tfqm_combinatorics --lib.\n";

pub mod cartesian_words;
pub mod enumeration;
pub mod finite_geometry;
pub mod mub_configurations;
pub mod weyl_systems;

pub mod color_constraints;

pub mod partitions;

#[path = "mod.rs"]
mod crate_certificate;

pub use crate_certificate::{surface_certificate, SurfaceCertificate, SurfaceError};

pub fn e2e_surface() -> Result<SurfaceCertificate, SurfaceError> {
    let cert = surface_certificate()?;
    if cert.partition_four != 5 {
        return Err(SurfaceError {
            invariant: "crate root repeats the partition witness p(4)=5",
            parameters: format!("partition_four={}", cert.partition_four),
        });
    }
    Ok(cert)
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn unit_surface_factorial_witness() {
        let cert = e2e_surface().unwrap();
        assert_eq!(cert.factorial_five, 120);
    }

    #[test]
    fn integration_surface_joins_partition_and_mub() {
        let cert = e2e_surface().unwrap();
        assert_eq!(cert.partition_four, 5);
        assert_eq!(cert.mub_bases, 6);
    }

    #[test]
    fn e2e_public_surface_certificate() {
        let cert = e2e_surface().unwrap();
        assert_eq!(cert.fano_lines, 7);
        assert_eq!(cert.affine_lines, 12);
        assert!(PROVENANCE.contains("Origin: code/rust/src/combinatorics/lib.rs"));
        assert!(PROVENANCE.contains("Claim: urn:omega:fqm:combinatorics:crate-surface:v1"));
        assert!(PROVENANCE.contains("AuthorityEffect: None"));
        assert!(PROVENANCE.contains("Mutation-Kills: 1 non-equivalent source mutant"));
    }

    #[test]
    fn negative_wrong_partition_witness_is_refused() {
        let err = crate_certificate::refuse_partition_witness(4).unwrap_err();
        assert_eq!(err.invariant, "p(4)=5");
        assert_eq!(err.parameters, "witness=4");
    }
}
