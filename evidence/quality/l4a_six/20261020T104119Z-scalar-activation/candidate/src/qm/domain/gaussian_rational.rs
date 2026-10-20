pub use crate::linear_algebra::scalars::GaussianRational;

use crate::linear_algebra::scalars::Semiring;

pub fn multiply(
    left: &GaussianRational,
    right: &GaussianRational,
) -> Result<GaussianRational, crate::linear_algebra::scalars::ScalarError> {
    Semiring::try_mul(left, right)
}

pub fn norm_is_multiplicative(
    left: &GaussianRational,
    right: &GaussianRational,
) -> Result<(), &'static str> {
    let by_product = multiply(left, right)
        .map_err(|_| "Gaussian multiplication refused")?
        .norm_sq();
    let by_factors = left.norm_sq() * right.norm_sq();
    if by_product == by_factors {
        Ok(())
    } else {
        Err("Gaussian norm is not multiplicative")
    }
}

pub fn sample_norm_identity() -> Result<(), &'static str> {
    let left = GaussianRational::from_integers(1, 1);
    let right = GaussianRational::from_integers(1, -1);
    let product = multiply(&left, &right).map_err(|_| "Gaussian multiplication refused")?;
    let two = GaussianRational::from_integers(2, 0);
    if product != two {
        return Err(" (1+i)(1-i) is not 2");
    }
    norm_is_multiplicative(&left, &right)?;
    let four = crate::linear_algebra::scalars::q(4);
    if product.norm_sq() != four || left.norm_sq() * right.norm_sq() != four {
        return Err("norm of (1+i)(1-i) is not 4");
    }
    Ok(())
}
