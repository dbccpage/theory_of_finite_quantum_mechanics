use crate::integer_factorization::{factor_natural, FactorizationBudget, FactorizationError};
use num_bigint::{BigInt, BigUint};
use num_integer::Integer;
use num_traits::ToPrimitive;

#[derive(Debug, Clone, PartialEq, Eq, thiserror::Error)]
pub enum ResidueError {
    #[error("the modulus must be at least two")]
    Modulus,
    #[error("the CRT result is outside the u64 carrier")]
    Overflow,
    #[error(transparent)]
    Factorization(#[from] FactorizationError),
}

pub fn two_torsion(n: u64) -> Result<Vec<u64>, ResidueError> {
    if n < 2 {
        return Err(ResidueError::Modulus);
    }
    Ok(if n % 2 == 0 { vec![0, n / 2] } else { vec![0] })
}

fn local_square_roots_unity(prime: u64, e: u32, power: u64) -> Vec<u64> {
    if prime != 2 {
        return vec![1, power - 1];
    }
    match e {
        1 => vec![1],
        2 => vec![1, 3],
        _ => vec![1, power - 1, 1 + power / 2, power / 2 - 1],
    }
}

fn crt_join_roots(
    roots: &[u64],
    local: &[u64],
    modulus: u64,
    power: u64,
) -> Result<Vec<u64>, ResidueError> {
    let inverse = BigInt::from(modulus)
        .extended_gcd(&BigInt::from(power))
        .x
        .mod_floor(&BigInt::from(power))
        .to_u64()
        .ok_or(ResidueError::Overflow)?;
    let mut joined = Vec::with_capacity(roots.len() * local.len());
    for &a in roots {
        for &b in local {
            let difference =
                (u128::from(b) + u128::from(power) - u128::from(a % power)) % u128::from(power);
            let t = difference * u128::from(inverse) % u128::from(power);
            let x = u128::from(a) + u128::from(modulus) * t;
            joined.push(u64::try_from(x).map_err(|_| ResidueError::Overflow)?);
        }
    }
    Ok(joined)
}

pub fn square_roots_unity(n: u64, budget: FactorizationBudget) -> Result<Vec<u64>, ResidueError> {
    if n < 2 {
        return Err(ResidueError::Modulus);
    }
    let factors = factor_natural(&BigUint::from(n), budget)?;
    let (mut roots, mut modulus) = (vec![0u64], 1u64);
    for (p, e) in factors {
        let prime = p.to_u64().ok_or(ResidueError::Overflow)?;
        let power = prime.checked_pow(e).ok_or(ResidueError::Overflow)?;
        let local = local_square_roots_unity(prime, e, power);
        roots = crt_join_roots(&roots, &local, modulus, power)?;
        modulus = modulus.checked_mul(power).ok_or(ResidueError::Overflow)?;
    }
    roots.sort_unstable();
    roots.dedup();
    Ok(roots)
}
