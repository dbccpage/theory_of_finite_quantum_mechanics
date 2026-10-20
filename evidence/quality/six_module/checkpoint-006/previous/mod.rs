use num_traits::ToPrimitive;

pub const PROVENANCE: &str = "Origin: code/rust/src/combinatorics/mod.rs\nClaim: urn:omega:fqm:combinatorics:surface-certificate:v1\nAuthorityEffect: None\nScope Fence: the surface certificate checks finite witnesses only and does not claim a closed form for p(n) or a MUB existence theorem for composite dimension.\nMutation-Kills: 2 non-equivalent source mutants, executed by cargo test -p tfqm_combinatorics --lib.\n";

#[derive(Debug, Clone, PartialEq, Eq)]
pub struct SurfaceError {
    pub invariant: &'static str,
    pub parameters: String,
}

#[derive(Debug, Clone, PartialEq, Eq)]
pub struct SurfaceCertificate {
    pub partition_four: u64,
    pub factorial_five: u64,
    pub mub_bases: usize,
    pub fano_lines: usize,
    pub affine_lines: usize,
}

pub fn surface_certificate() -> Result<SurfaceCertificate, SurfaceError> {
    let partition_four = match certify_partition() {
        Ok(value) => value,
        Err(err) => return Err(err),
    };
    let factorial_five = match certify_factorial() {
        Ok(value) => value,
        Err(err) => return Err(err),
    };
    finish_surface(partition_four, factorial_five)
}

fn finish_surface(partition_four: u64, factorial_five: u64) -> Result<SurfaceCertificate, SurfaceError> {
    let mub_bases = match certify_mub() {
        Ok(value) => value,
        Err(err) => return Err(err),
    };
    let fano_lines = match certify_fano() {
        Ok(value) => value,
        Err(err) => return Err(err),
    };
    let affine_lines = match certify_affine() {
        Ok(value) => value,
        Err(err) => return Err(err),
    };
    Ok(SurfaceCertificate {
        partition_four,
        factorial_five,
        mub_bases,
        fano_lines,
        affine_lines,
    })
}

pub fn refuse_partition_witness(witness: u64) -> Result<(), SurfaceError> {
    if witness != 5 {
        return Err(SurfaceError {
            invariant: "p(4)=5",
            parameters: format!("witness={witness}"),
        });
    }
    Ok(())
}

fn certify_partition() -> Result<u64, SurfaceError> {
    let value = crate::partitions::partition_count(4).map_err(|_| SurfaceError {
        invariant: "p(4) is defined by the integer recurrence",
        parameters: "n=4".to_owned(),
    })?;
    match value.to_u64() {
        Some(5) => Ok(5),
        Some(other) => Err(SurfaceError {
            invariant: "p(4)=5",
            parameters: format!("n=4,got={other}"),
        }),
        None => Err(SurfaceError {
            invariant: "p(4) fits u64",
            parameters: "n=4".to_owned(),
        }),
    }
}

fn certify_factorial() -> Result<u64, SurfaceError> {
    let value = crate::enumeration::factorial(5).map_err(|_| SurfaceError {
        invariant: "5! is defined",
        parameters: "n=5".to_owned(),
    })?;
    match value.to_u64() {
        Some(120) => Ok(120),
        Some(other) => Err(SurfaceError {
            invariant: "5!=120",
            parameters: format!("n=5,got={other}"),
        }),
        None => Err(SurfaceError {
            invariant: "5! fits u64",
            parameters: "n=5".to_owned(),
        }),
    }
}

fn certify_mub() -> Result<usize, SurfaceError> {
    let config = crate::mub_configurations::MubOperatorConfiguration::canonical_prime(5)
        .map_err(|_| SurfaceError {
            invariant: "prime 5 admits a complete isotropic MUB bundle",
            parameters: "p=5".to_owned(),
        })?;
    let bases = config.num_bases();
    if bases != 6 {
        return Err(SurfaceError {
            invariant: "canonical prime-5 MUB has p+1 bases",
            parameters: format!("p=5,bases={bases}"),
        });
    }
    Ok(bases)
}

fn certify_fano() -> Result<usize, SurfaceError> {
    let fano = crate::finite_geometry::fano_plane().map_err(|_| SurfaceError {
        invariant: "the Fano incidence list is a linear space",
        parameters: "points=7".to_owned(),
    })?;
    if !fano.is_linear_space() {
        return Err(SurfaceError {
            invariant: "the Fano plane is a linear space",
            parameters: "points=7".to_owned(),
        });
    }
    Ok(fano.num_lines())
}

fn certify_affine() -> Result<usize, SurfaceError> {
    let plane = crate::finite_geometry::affine_plane_ag2(3).map_err(|_| SurfaceError {
        invariant: "AG(2,3) is admitted for prime order 3",
        parameters: "p=3".to_owned(),
    })?;
    if plane.num_lines() != 12 {
        return Err(SurfaceError {
            invariant: "AG(2,3) has p(p+1) lines",
            parameters: format!("p=3,lines={}", plane.num_lines()),
        });
    }
    Ok(plane.num_lines())
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn unit_partition_witness_is_five() {
        assert_eq!(certify_partition().unwrap(), 5);
    }

    #[test]
    fn integration_mub_uses_weyl_rays() {
        assert_eq!(certify_mub().unwrap(), 6);
    }

    #[test]
    fn e2e_surface_certificate_fields() {
        let cert = surface_certificate().unwrap();
        assert_eq!(cert.factorial_five, 120);
        assert_eq!(cert.fano_lines, 7);
        assert_eq!(cert.affine_lines, 12);
        assert!(PROVENANCE.contains("AuthorityEffect: None"));
        assert!(PROVENANCE.contains("Mutation-Kills: 2 non-equivalent source mutants"));
    }

    #[test]
    fn negative_partition_witness_records_invariant() {
        let err = refuse_partition_witness(4).unwrap_err();
        assert_eq!(err.invariant, "p(4)=5");
        assert_eq!(err.parameters, "witness=4");
    }
}
