use num_rational::BigRational;
use num_traits::{One, Zero};
use omega_epk::matrix_path_kernel::{EvaluatedPathKernelGraph, MatrixPathError, RationalMatrix2x2};

pub const ORIGIN: &str =
    "Origin: code/rust/src/wdp/wdp_kernel_check.rs @ 40de7d5cda1ff1f0db8305d0c1b2103646fab197";
pub const CLAIM: &str = "Claim: the path-kernel product of exact 2x2 rational factors is the ordered matrix product, and the empty path is the identity";
pub const AUTHORITY_EFFECT: &str = "AuthorityEffect: None";
pub const MUTATION_KILLS: u32 = 0;

#[derive(Debug, Clone, PartialEq, Eq)]
pub enum KernelBoundError {
    PathTooLong { length: usize, bound: usize },
    Matrix(MatrixPathError),
    BinaryFloatRefused,
    BooleanAsNumber,
    InexactToken,
    Overflow,
}

impl From<MatrixPathError> for KernelBoundError {
    fn from(error: MatrixPathError) -> Self {
        Self::Matrix(error)
    }
}

pub fn admit_exact_integer(token: &str) -> Result<i64, KernelBoundError> {
    if token == "true" || token == "false" {
        return Err(KernelBoundError::BooleanAsNumber);
    }
    if token.bytes().any(|byte| matches!(byte, b'.' | b'e' | b'E')) {
        return Err(KernelBoundError::BinaryFloatRefused);
    }
    parse_signed_digits(token)
}

fn parse_signed_digits(token: &str) -> Result<i64, KernelBoundError> {
    let (negative, digits) = match token.strip_prefix('-') {
        Some(rest) => (true, rest),
        None => (false, token),
    };
    if digits.is_empty() || !digits.bytes().all(|byte| byte.is_ascii_digit()) {
        return Err(KernelBoundError::InexactToken);
    }
    let mut value = 0i64;
    for byte in digits.bytes() {
        let digit = i64::from(byte - b'0');
        value = value
            .checked_mul(10)
            .and_then(|place| place.checked_add(digit))
            .ok_or(KernelBoundError::Overflow)?;
    }
    if negative {
        value = value.checked_neg().ok_or(KernelBoundError::Overflow)?;
    }
    Ok(value)
}

pub fn wdp_kernel_check(
    factors: &[RationalMatrix2x2],
) -> Result<RationalMatrix2x2, MatrixPathError> {
    if factors.is_empty() {
        return Ok(RationalMatrix2x2::identity());
    }
    let vertices: Vec<String> = (0..=factors.len())
        .map(|index| format!("v{index}"))
        .collect();
    let edges: Vec<(String, String)> = (0..factors.len())
        .map(|index| (format!("v{index}"), format!("v{}", index + 1)))
        .collect();
    let graph = EvaluatedPathKernelGraph::new(vertices, edges, factors.to_vec())?;
    let edge_indices: Vec<usize> = (0..factors.len()).collect();
    graph.evaluate_path(&edge_indices)
}

pub fn wdp_kernel_check_bounded(
    factors: &[RationalMatrix2x2],
    max_edges: usize,
) -> Result<RationalMatrix2x2, KernelBoundError> {
    if factors.len() > max_edges {
        return Err(KernelBoundError::PathTooLong {
            length: factors.len(),
            bound: max_edges,
        });
    }
    Ok(wdp_kernel_check(factors)?)
}

pub fn swap_matrix() -> RationalMatrix2x2 {
    RationalMatrix2x2::new(
        BigRational::zero(),
        BigRational::one(),
        BigRational::one(),
        BigRational::zero(),
    )
}

pub fn authority_effect() -> &'static str {
    AUTHORITY_EFFECT
}

#[cfg(test)]
mod tests {
    use super::*;

    fn need(cond: bool, message: &str) -> Result<(), String> {
        if cond {
            Ok(())
        } else {
            Err(message.to_string())
        }
    }

    fn show(error: impl std::fmt::Debug) -> String {
        format!("{error:?}")
    }

    #[test]
    fn unit_identity_path_and_empty_path_are_identity() -> Result<(), String> {
        unit_products().and_then(|(identity, product, empty)| unit_claims(identity, product, empty))
    }

    fn unit_products() -> Result<(RationalMatrix2x2, RationalMatrix2x2, RationalMatrix2x2), String> {
        let identity = RationalMatrix2x2::identity();
        let product = wdp_kernel_check(&[identity.clone(), identity.clone()]).map_err(show)?;
        let empty = wdp_kernel_check(&[]).map_err(show)?;
        Ok((identity, product, empty))
    }

    fn unit_claims(
        identity: RationalMatrix2x2,
        product: RationalMatrix2x2,
        empty: RationalMatrix2x2,
    ) -> Result<(), String> {
        need(product == identity, "product")?;
        need(empty == identity, "empty")?;
        need(authority_effect() == AUTHORITY_EFFECT, "authority")
    }

    #[test]
    fn integration_swap_square_matches_direct_multiply() -> Result<(), String> {
        integration_products().and_then(|(swap, once, twice, direct)| {
            integration_claims(swap, once, twice, direct)
        })
    }

    fn integration_products()
    -> Result<(RationalMatrix2x2, RationalMatrix2x2, RationalMatrix2x2, RationalMatrix2x2), String>
    {
        let swap = swap_matrix();
        let once = wdp_kernel_check(&[swap.clone()]).map_err(show)?;
        let twice = wdp_kernel_check(&[swap.clone(), swap.clone()]).map_err(show)?;
        let direct = swap.multiply(&swap).map_err(show)?;
        Ok((swap, once, twice, direct))
    }

    fn integration_claims(
        swap: RationalMatrix2x2,
        once: RationalMatrix2x2,
        twice: RationalMatrix2x2,
        direct: RationalMatrix2x2,
    ) -> Result<(), String> {
        need(once == swap, "order two generator")?;
        need(twice == direct, "path agrees with multiply")?;
        need(twice == RationalMatrix2x2::identity(), "order two")
    }

    #[test]
    fn e2e_bounded_identity_path_keeps_the_claim() -> Result<(), String> {
        e2e_product().and_then(e2e_claims)
    }

    fn e2e_product() -> Result<RationalMatrix2x2, String> {
        let identity = RationalMatrix2x2::identity();
        let product = wdp_kernel_check_bounded(&[identity.clone()], 1).map_err(show)?;
        need(product == identity, "bounded")?;
        Ok(product)
    }

    fn e2e_claims(_product: RationalMatrix2x2) -> Result<(), String> {
        need(ORIGIN.contains("wdp_kernel_check.rs"), "origin")?;
        need(CLAIM.contains("empty path"), "claim")?;
        need(admit_exact_integer("2") == Ok(2), "bound token")
    }

    #[test]
    fn negative_refuses_overlong_path_float_and_boolean() -> Result<(), String> {
        let identity = RationalMatrix2x2::identity();
        need(
            matches!(
                wdp_kernel_check_bounded(&[identity.clone(), identity], 1),
                Err(KernelBoundError::PathTooLong { length: 2, bound: 1 })
            ),
            "bound",
        )?;
        need(
            admit_exact_integer("1.0") == Err(KernelBoundError::BinaryFloatRefused),
            "float",
        )?;
        need(
            admit_exact_integer("true") == Err(KernelBoundError::BooleanAsNumber),
            "bool",
        )?;
        Ok(())
    }
}
