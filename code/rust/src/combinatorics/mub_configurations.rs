use crate::weyl_systems::{DiscreteWeylSystem, PhasePoint, WeylSystemError};
use std::collections::BTreeSet;
use thiserror::Error;

pub const PROVENANCE: &str = "Origin: code/rust/src/combinatorics/mub_configurations.rs\nClaim: urn:omega:fqm:combinatorics:prime-mub-operator-bundles:v1\nAuthorityEffect: None\nScope Fence: canonical bundles are the prime isotropic rays with the origin removed, not a completeness theorem for every dimension.\nMutation-Kills: 1 non-equivalent source mutant, executed by cargo test -p tfqm_combinatorics --lib.\n";

pub const AUTHORITY_EFFECT: &str = "AuthorityEffect: None";

#[derive(Debug, Clone, PartialEq, Eq, Error)]
pub enum MubConfigError {
    #[error("dimension {dim} is below the minimum {min}")]
    InvalidDimension { dim: usize, min: usize },
    #[error("bundle count {found} exceeds the maximum theoretical bound {bound} for dimension {dim}")]
    TooManyBundles { found: usize, bound: usize, dim: usize },
    #[error("bundle {index} contains {found} operators, expected {expected}")]
    InvalidBundleSize { index: usize, found: usize, expected: usize },
    #[error("bundle {index} contains non-commuting operators")]
    NonCommutingBundle { index: usize, q0: usize, p0: usize, q1: usize, p1: usize },
    #[error("bundles are not disjoint: phase point ({q}, {p}) appears in multiple bundles")]
    NonDisjointBundles { q: usize, p: usize },
    #[error("operator bundle contains the trivial identity phase point (0, 0)")]
    ContainsIdentity,
    #[error(transparent)]
    Weyl(#[from] WeylSystemError),
}

impl MubConfigError {
    pub fn violated_invariant(&self) -> &'static str {
        match self {
            Self::InvalidDimension { .. } => "dimension is at least 2",
            Self::TooManyBundles { .. } => "bundle count does not exceed dim+1",
            Self::InvalidBundleSize { .. } => "each bundle has dim-1 non-identity operators",
            Self::NonCommutingBundle { .. } => "operators inside a bundle commute",
            Self::NonDisjointBundles { .. } => "bundles are pairwise disjoint",
            Self::ContainsIdentity => "bundles exclude the identity phase point",
            Self::Weyl(err) => err.violated_invariant(),
        }
    }

    pub fn measured_parameters(&self) -> Vec<(&'static str, String)> {
        match self {
            Self::InvalidDimension { dim, min } => {
                vec![("dim", dim.to_string()), ("min", min.to_string())]
            }
            Self::TooManyBundles { found, bound, dim } => vec![
                ("found", found.to_string()),
                ("bound", bound.to_string()),
                ("dim", dim.to_string()),
            ],
            Self::InvalidBundleSize { index, found, expected } => vec![
                ("index", index.to_string()),
                ("found", found.to_string()),
                ("expected", expected.to_string()),
            ],
            Self::NonCommutingBundle { index, q0, p0, q1, p1 } => vec![
                ("index", index.to_string()),
                ("q0", q0.to_string()),
                ("p0", p0.to_string()),
                ("q1", q1.to_string()),
                ("p1", p1.to_string()),
            ],
            Self::NonDisjointBundles { q, p } => vec![("q", q.to_string()), ("p", p.to_string())],
            Self::ContainsIdentity => vec![("q", "0".to_owned()), ("p", "0".to_owned())],
            Self::Weyl(err) => err.measured_parameters(),
        }
    }
}

#[derive(Debug, Clone, PartialEq, Eq)]
pub struct MubOperatorConfiguration {
    dim: usize,
    bundles: Vec<Vec<PhasePoint>>,
}

impl MubOperatorConfiguration {
    pub fn new(dim: usize, bundles: Vec<Vec<PhasePoint>>) -> Result<Self, MubConfigError> {
        let weyl = admit_shape(dim, bundles.len())?;
        let mut seen = BTreeSet::new();
        for (index, bundle) in bundles.iter().enumerate() {
            admit_bundle(&weyl, dim, index, bundle, &mut seen)?;
        }
        Ok(Self { dim, bundles })
    }

    pub fn dim(&self) -> usize {
        self.dim
    }

    pub fn num_bases(&self) -> usize {
        self.bundles.len()
    }

    pub fn is_complete(&self) -> bool {
        self.bundles.len() == self.dim + 1
    }

    pub fn bundles(&self) -> &[Vec<PhasePoint>] {
        &self.bundles
    }

    pub fn canonical_prime(p: usize) -> Result<Self, MubConfigError> {
        let weyl = DiscreteWeylSystem::new(p)?;
        let rays = weyl.isotropic_rays()?;
        let origin = PhasePoint::new(0, 0);
        let bundles = rays
            .into_iter()
            .map(|ray| ray.into_iter().filter(|&pt| pt != origin).collect())
            .collect();
        Self::new(p, bundles)
    }
}

fn admit_shape(dim: usize, bundle_count: usize) -> Result<DiscreteWeylSystem, MubConfigError> {
    if dim < 2 {
        return Err(MubConfigError::InvalidDimension { dim, min: 2 });
    }
    let bound = dim + 1;
    if bundle_count > bound {
        return Err(MubConfigError::TooManyBundles {
            found: bundle_count,
            bound,
            dim,
        });
    }
    Ok(DiscreteWeylSystem::new(dim)?)
}

fn admit_bundle(
    weyl: &DiscreteWeylSystem,
    dim: usize,
    index: usize,
    bundle: &[PhasePoint],
    seen: &mut BTreeSet<PhasePoint>,
) -> Result<(), MubConfigError> {
    let expected = dim - 1;
    if bundle.len() != expected {
        return Err(MubConfigError::InvalidBundleSize {
            index,
            found: bundle.len(),
            expected,
        });
    }
    admit_members(bundle, seen)?;
    admit_commuting(weyl, index, bundle)
}

fn admit_members(bundle: &[PhasePoint], seen: &mut BTreeSet<PhasePoint>) -> Result<(), MubConfigError> {
    let identity = PhasePoint::new(0, 0);
    for &pt in bundle {
        if pt == identity {
            return Err(MubConfigError::ContainsIdentity);
        }
        if !seen.insert(pt) {
            return Err(MubConfigError::NonDisjointBundles { q: pt.q, p: pt.p });
        }
    }
    Ok(())
}

fn admit_commuting(
    weyl: &DiscreteWeylSystem,
    index: usize,
    bundle: &[PhasePoint],
) -> Result<(), MubConfigError> {
    for (j, u) in bundle.iter().enumerate() {
        admit_tail(weyl, index, bundle, j, *u)?;
    }
    Ok(())
}

fn admit_tail(
    weyl: &DiscreteWeylSystem,
    index: usize,
    bundle: &[PhasePoint],
    j: usize,
    u: PhasePoint,
) -> Result<(), MubConfigError> {
    let tail = bundle.get(j + 1..).unwrap_or(&[]);
    for v in tail {
        if !weyl.commutes(u, *v)? {
            return Err(MubConfigError::NonCommutingBundle {
                index,
                q0: u.q,
                p0: u.p,
                q1: v.q,
                p1: v.p,
            });
        }
    }
    Ok(())
}

pub fn mub_theoretical_upper_bound(dim: usize) -> usize {
    dim + 1
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn unit_upper_bound_is_dim_plus_one() {
        assert_eq!(mub_theoretical_upper_bound(6), 7);
    }

    #[test]
    fn test_canonical_mub_configurations_prime() {
        let config = MubOperatorConfiguration::canonical_prime(5).unwrap();
        assert_eq!(config.dim(), 5);
        assert_eq!(config.num_bases(), 6);
        assert!(config.is_complete());
        let total_ops: usize = config.bundles().iter().map(|bundle| bundle.len()).sum();
        assert_eq!(total_ops, 24);
    }

    #[test]
    fn integration_canonical_prime_uses_weyl_dimension() {
        let config = MubOperatorConfiguration::canonical_prime(3).unwrap();
        let weyl = DiscreteWeylSystem::new(config.dim()).unwrap();
        assert_eq!(weyl.dim(), 3);
        assert_eq!(config.num_bases(), 4);
    }

    #[test]
    fn e2e_complete_prime_bundle_contract() {
        let config = MubOperatorConfiguration::canonical_prime(2).unwrap();
        assert!(config.is_complete());
        assert!(PROVENANCE.contains("AuthorityEffect: None"));
        assert!(PROVENANCE.contains("Mutation-Kills: 1 non-equivalent source mutant"));
        assert_eq!(AUTHORITY_EFFECT, "AuthorityEffect: None");
    }

    #[test]
    fn test_non_disjoint_bundle_refusal() {
        let pt1 = PhasePoint::new(0, 1);
        let bundles = vec![vec![pt1], vec![pt1]];
        let err = MubOperatorConfiguration::new(2, bundles).unwrap_err();
        assert_eq!(err.violated_invariant(), "bundles are pairwise disjoint");
        assert_eq!(err.measured_parameters(), vec![("q", "0".to_owned()), ("p", "1".to_owned())]);
    }

    #[test]
    fn negative_dimension_size_and_identity() {
        let dim = MubOperatorConfiguration::new(1, vec![]).unwrap_err();
        assert_eq!(dim.measured_parameters()[0], ("dim", "1".to_owned()));
        let size = MubOperatorConfiguration::new(2, vec![vec![]]).unwrap_err();
        assert_eq!(size.violated_invariant(), "each bundle has dim-1 non-identity operators");
        let identity = MubOperatorConfiguration::new(2, vec![vec![PhasePoint::new(0, 0)]]).unwrap_err();
        assert_eq!(identity.violated_invariant(), "bundles exclude the identity phase point");
    }

    #[test]
    fn negative_too_many_and_noncommuting() {
        let pt = PhasePoint::new(0, 1);
        let bundles = vec![vec![pt], vec![pt], vec![pt], vec![pt]];
        let many = MubOperatorConfiguration::new(2, bundles).unwrap_err();
        assert_eq!(many.violated_invariant(), "bundle count does not exceed dim+1");
        let bundles = vec![vec![PhasePoint::new(0, 1), PhasePoint::new(1, 0)]];
        let commute = MubOperatorConfiguration::new(3, bundles).unwrap_err();
        assert_eq!(commute.violated_invariant(), "operators inside a bundle commute");
    }
}
