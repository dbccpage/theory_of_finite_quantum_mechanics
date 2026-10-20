use std::collections::BTreeSet;
use thiserror::Error;

pub const PROVENANCE: &str = "Origin: code/rust/src/combinatorics/weyl_systems.rs\nClaim: urn:omega:fqm:combinatorics:discrete-weyl-symplectic-form:v1\nAuthorityEffect: None\nScope Fence: the symplectic form is the exact mod-p alternating form, not a continuum Heisenberg representation.\nMutation-Kills: 2 non-equivalent source mutants, executed by cargo test -p tfqm_combinatorics --lib.\n";

pub const AUTHORITY_EFFECT: &str = "AuthorityEffect: None";

#[derive(Debug, Clone, PartialEq, Eq, Error)]
pub enum WeylSystemError {
    #[error("dimension {dim} lies outside [{min}, {max}]")]
    InvalidDimension { dim: usize, min: usize, max: usize },
    #[error("dimension {0} must be prime for isotropic ray decomposition")]
    NotPrime(usize),
    #[error("coordinate ({0}, {1}) is out of bounds for dimension {2}")]
    CoordinateOutOfBounds(usize, usize, usize),
    #[error("isotropic rays fail the partition invariant for prime {prime}: rays {rays}, nonzero {nonzero}")]
    PartitionFailed {
        prime: usize,
        rays: usize,
        nonzero: usize,
    },
}

impl WeylSystemError {
    pub fn violated_invariant(&self) -> &'static str {
        match self {
            Self::InvalidDimension { .. } => "dimension lies in 2..=256",
            Self::NotPrime(_) => "isotropic rays are admitted only for prime dimension",
            Self::CoordinateOutOfBounds(_, _, _) => "phase coordinates lie in the dimension",
            Self::PartitionFailed { .. } => "nonzero phase points partition into isotropic rays",
        }
    }

    pub fn measured_parameters(&self) -> Vec<(&'static str, String)> {
        match self {
            Self::InvalidDimension { dim, min, max } => vec![
                ("dim", dim.to_string()),
                ("min", min.to_string()),
                ("max", max.to_string()),
            ],
            Self::NotPrime(dim) => vec![("dim", dim.to_string())],
            Self::CoordinateOutOfBounds(q, p, dim) => vec![
                ("q", q.to_string()),
                ("p", p.to_string()),
                ("dim", dim.to_string()),
            ],
            Self::PartitionFailed {
                prime,
                rays,
                nonzero,
            } => vec![
                ("prime", prime.to_string()),
                ("rays", rays.to_string()),
                ("nonzero", nonzero.to_string()),
            ],
        }
    }
}

#[derive(Debug, Clone, Copy, PartialEq, Eq, Hash, PartialOrd, Ord)]
pub struct PhasePoint {
    pub q: usize,
    pub p: usize,
}

impl PhasePoint {
    pub fn new(q: usize, p: usize) -> Self {
        Self { q, p }
    }
}

#[derive(Debug, Clone, PartialEq, Eq)]
pub struct DiscreteWeylSystem {
    dim: usize,
}

impl DiscreteWeylSystem {
    pub fn new(dim: usize) -> Result<Self, WeylSystemError> {
        if dim < 2 || dim > 256 {
            return Err(WeylSystemError::InvalidDimension {
                dim,
                min: 2,
                max: 256,
            });
        }
        Ok(Self { dim })
    }

    pub fn dim(&self) -> usize {
        self.dim
    }

    /// PhasePoint is a raw coordinate record; admission is relative to this modulus.
    pub fn validate_point(&self, point: PhasePoint) -> Result<(), WeylSystemError> {
        if point.q >= self.dim || point.p >= self.dim {
            return Err(WeylSystemError::CoordinateOutOfBounds(
                point.q, point.p, self.dim,
            ));
        }
        Ok(())
    }

    pub fn symplectic_form(&self, u: PhasePoint, v: PhasePoint) -> Result<usize, WeylSystemError> {
        self.validate_point(u)?;
        self.validate_point(v)?;
        let term1 = (u.q * v.p) % self.dim;
        let term2 = (u.p * v.q) % self.dim;
        let res = (self.dim + term1 - term2) % self.dim;
        Ok(res)
    }

    pub fn commutes(&self, u: PhasePoint, v: PhasePoint) -> Result<bool, WeylSystemError> {
        Ok(self.symplectic_form(u, v)? == 0)
    }

    pub fn add(&self, u: PhasePoint, v: PhasePoint) -> Result<PhasePoint, WeylSystemError> {
        self.validate_point(u)?;
        self.validate_point(v)?;
        Ok(PhasePoint {
            q: (u.q + v.q) % self.dim,
            p: (u.p + v.p) % self.dim,
        })
    }

    pub fn isotropic_rays(&self) -> Result<Vec<Vec<PhasePoint>>, WeylSystemError> {
        let p = self.dim;
        for d in 2..p {
            if p % d == 0 {
                return Err(WeylSystemError::NotPrime(p));
            }
        }

        let mut rays = Vec::with_capacity(p + 1);

        let mut ray_inf = Vec::with_capacity(p);
        for y in 0..p {
            ray_inf.push(PhasePoint::new(0, y));
        }
        rays.push(ray_inf);

        for m in 0..p {
            let mut ray_m = Vec::with_capacity(p);
            for x in 0..p {
                ray_m.push(PhasePoint::new(x, (m * x) % p));
            }
            rays.push(ray_m);
        }

        Ok(rays)
    }
}

pub fn certify_ray_partition(prime: usize) -> Result<(usize, usize), WeylSystemError> {
    let system = DiscreteWeylSystem::new(prime)?;
    let rays = system.isotropic_rays()?;
    let nonzero = count_nonzero(&rays);
    let expected = prime
        .checked_mul(prime)
        .and_then(|square| square.checked_sub(1))
        .ok_or(WeylSystemError::InvalidDimension {
            dim: prime,
            min: 2,
            max: 256,
        })?;
    if rays.len() != prime + 1 || nonzero != expected {
        return Err(WeylSystemError::PartitionFailed {
            prime,
            rays: rays.len(),
            nonzero,
        });
    }
    Ok((rays.len(), nonzero))
}

fn count_nonzero(rays: &[Vec<PhasePoint>]) -> usize {
    let mut seen = BTreeSet::new();
    for ray in rays {
        collect_nonzero(&mut seen, ray);
    }
    seen.len()
}

fn collect_nonzero(seen: &mut BTreeSet<PhasePoint>, ray: &[PhasePoint]) {
    for pt in ray {
        if *pt != PhasePoint::new(0, 0) {
            seen.insert(*pt);
        }
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn unit_symplectic_antisymmetry() {
        let weyl = DiscreteWeylSystem::new(5).unwrap();
        let u = PhasePoint::new(2, 3);
        let v = PhasePoint::new(1, 4);
        let omega_uv = weyl.symplectic_form(u, v).unwrap();
        let omega_vu = weyl.symplectic_form(v, u).unwrap();
        assert_eq!((omega_uv + omega_vu) % 5, 0);
        assert_eq!(weyl.symplectic_form(u, u).unwrap(), 0);
    }

    #[test]
    fn integration_ray_partition_certificate() {
        let (rays, nonzero) = certify_ray_partition(5).unwrap();
        assert_eq!(rays, 6);
        assert_eq!(nonzero, 24);
    }

    #[test]
    fn e2e_addition_and_commutation() {
        let weyl = DiscreteWeylSystem::new(5).unwrap();
        let sum = weyl
            .add(PhasePoint::new(4, 4), PhasePoint::new(2, 3))
            .unwrap();
        assert_eq!(sum, PhasePoint::new(1, 2));
        assert!(weyl
            .commutes(PhasePoint::new(1, 2), PhasePoint::new(2, 4))
            .unwrap());
        assert!(PROVENANCE.contains("AuthorityEffect: None"));
        assert!(PROVENANCE.contains("Mutation-Kills: 2 non-equivalent source mutants"));
        assert_eq!(AUTHORITY_EFFECT, "AuthorityEffect: None");
    }

    fn assert_ray_commutes(weyl: &DiscreteWeylSystem, ray: &[PhasePoint]) {
        for u in ray {
            assert_pairs_commute(weyl, ray, *u);
        }
    }

    fn assert_pairs_commute(weyl: &DiscreteWeylSystem, ray: &[PhasePoint], u: PhasePoint) {
        for v in ray {
            assert!(weyl.commutes(u, *v).unwrap());
        }
    }

    #[test]
    fn test_prime_five_rays_commute() {
        let weyl = DiscreteWeylSystem::new(5).unwrap();
        let rays = weyl.isotropic_rays().unwrap();
        for ray in &rays {
            assert_ray_commutes(&weyl, ray);
        }
        assert_eq!(rays.len(), 6);
    }

    #[test]
    fn negative_dimension_prime_and_coordinate() {
        let dim = DiscreteWeylSystem::new(1).unwrap_err();
        assert_eq!(dim.violated_invariant(), "dimension lies in 2..=256");
        assert_eq!(dim.measured_parameters()[0], ("dim", "1".to_owned()));
        let composite = DiscreteWeylSystem::new(4)
            .unwrap()
            .isotropic_rays()
            .unwrap_err();
        assert_eq!(
            composite.violated_invariant(),
            "isotropic rays are admitted only for prime dimension"
        );
        let weyl = DiscreteWeylSystem::new(5).unwrap();
        let coord = weyl
            .symplectic_form(PhasePoint::new(5, 0), PhasePoint::new(0, 0))
            .unwrap_err();
        assert_eq!(coord.measured_parameters()[0], ("q", "5".to_owned()));
    }
}
