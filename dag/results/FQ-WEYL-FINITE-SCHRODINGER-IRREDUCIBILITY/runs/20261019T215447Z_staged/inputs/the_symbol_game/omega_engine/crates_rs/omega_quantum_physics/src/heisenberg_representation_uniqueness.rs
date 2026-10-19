//! Finite odd-prime Schrödinger representation certificate. AuthorityEffect: None.
//! Full Weyl operator reconstruction supplies the finite irreducibility witness;
//! this has no assertion about infinite dimensional Stone-von Neumann uniqueness.
use linear_algebra::exact_field::matrix as mx;
use omega_lie_theory::heisenberg::{HeisenbergError, WeylHeisenberg};
use omega_number_theory::cyclotomic_field::Cyclotomic;
#[derive(Debug, Clone, PartialEq, Eq)]
pub struct FiniteIrreducibilityCertificate {
    pub prime: usize,
    pub matrix_units_reconstructed: usize,
    pub center_characters: usize,
}
pub fn certify_schrodinger_irreducibility<const P: usize>(
) -> Result<FiniteIrreducibilityCertificate, HeisenbergError> {
    let census = omega_lie_theory::heisenberg::stone_von_neumann_census(P)?;
    let system = WeylHeisenberg::new(P, Cyclotomic::<P>::zeta(1))?;
    if P > 11 {
        return Err(HeisenbergError::Dimension(P));
    }
    for r in 0..P {
        for c in 0..P {
            let unit = mx::from_rows(
                (0..P)
                    .map(|i| {
                        (0..P)
                            .map(|j| {
                                if i == r && j == c {
                                    Cyclotomic::<P>::one()
                                } else {
                                    Cyclotomic::<P>::zero()
                                }
                            })
                            .collect()
                    })
                    .collect(),
            )?;
            if system.reconstruct_operator(&unit)? != unit {
                return Err(HeisenbergError::Shape { dimension: P });
            }
        }
    }
    let _ = census;
    Ok(FiniteIrreducibilityCertificate {
        prime: P,
        matrix_units_reconstructed: P * P,
        center_characters: P - 1,
    })
}
