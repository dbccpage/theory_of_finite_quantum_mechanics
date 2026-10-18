use crate::types::AuthorityEffect;
use linear_algebra::backend::basic_matrix::BasicMatrix;
use num_rational::BigRational;
use num_traits::{One, Zero};
use omega_functional::projection_leakage::{
    evaluate_projection_leakage, ProjectionLeakage, ProjectionLeakageError,
};

pub const ORIGIN: &str = "Origin: code/rust/src/wdp/po000_projection_obstruction.rs @ 40de7d5cda1ff1f0db8305d0c1b2103646fab197";
pub const CLAIM: &str = "Claim: a declared rational projector pair with a zero generator has zero first-order leakage, and a negative elapsed time is refused";
pub const AUTHORITY_EFFECT_TEXT: &str = "AuthorityEffect: None";
pub const MUTATION_KILLS: u32 = 0;

#[derive(Debug, Clone, PartialEq, Eq)]
pub enum ProjectionTokenError {
    Leakage(ProjectionLeakageError),
    BinaryFloatRefused,
    BooleanAsNumber,
    InexactToken,
    Overflow,
}

impl From<ProjectionLeakageError> for ProjectionTokenError {
    fn from(error: ProjectionLeakageError) -> Self {
        Self::Leakage(error)
    }
}

#[derive(Debug, Clone, PartialEq, Eq)]
pub struct DeclaredProjectionProblem {
    pub first: BasicMatrix<BigRational>,
    pub second: BasicMatrix<BigRational>,
    pub generator: BasicMatrix<BigRational>,
    pub elapsed: BigRational,
    pub state: Vec<BigRational>,
}

#[derive(Debug, Clone, PartialEq, Eq)]
pub struct ProjectionObstructionReceipt {
    pub problem: DeclaredProjectionProblem,
    pub diagnostic: ProjectionLeakage,
    pub authority_effect: AuthorityEffect,
}

pub fn admit_exact_integer(token: &str) -> Result<i64, ProjectionTokenError> {
    if token == "true" || token == "false" {
        return Err(ProjectionTokenError::BooleanAsNumber);
    }
    if token.bytes().any(|byte| matches!(byte, b'.' | b'e' | b'E')) {
        return Err(ProjectionTokenError::BinaryFloatRefused);
    }
    parse_signed_digits(token)
}

fn parse_signed_digits(token: &str) -> Result<i64, ProjectionTokenError> {
    let (negative, digits) = match token.strip_prefix('-') {
        Some(rest) => (true, rest),
        None => (false, token),
    };
    if digits.is_empty() || !digits.bytes().all(|byte| byte.is_ascii_digit()) {
        return Err(ProjectionTokenError::InexactToken);
    }
    let mut value = 0i64;
    for byte in digits.bytes() {
        let digit = i64::from(byte - b'0');
        value = value
            .checked_mul(10)
            .and_then(|place| place.checked_add(digit))
            .ok_or(ProjectionTokenError::Overflow)?;
    }
    if negative {
        value = value.checked_neg().ok_or(ProjectionTokenError::Overflow)?;
    }
    Ok(value)
}

fn ratio(numer: i64, denom: i64) -> Result<BigRational, ProjectionTokenError> {
    if denom == 0 {
        return Err(ProjectionTokenError::InexactToken);
    }
    Ok(BigRational::new(numer.into(), denom.into()))
}

impl DeclaredProjectionProblem {
    pub fn evaluate(&self) -> Result<ProjectionObstructionReceipt, ProjectionLeakageError> {
        let diagnostic = evaluate_projection_leakage(
            &self.first,
            &self.second,
            &self.generator,
            &self.elapsed,
            &self.state,
        )?;
        Ok(ProjectionObstructionReceipt {
            problem: self.clone(),
            diagnostic,
            authority_effect: AuthorityEffect::None,
        })
    }

    pub fn verify(
        &self,
        candidate: &ProjectionObstructionReceipt,
    ) -> Result<bool, ProjectionLeakageError> {
        Ok(*candidate == self.evaluate()?)
    }

    pub fn evaluate_elapsed_token(
        &self,
        token: &str,
    ) -> Result<ProjectionObstructionReceipt, ProjectionTokenError> {
        let numer = admit_exact_integer(token)?;
        let mut problem = self.clone();
        problem.elapsed = ratio(numer, 1)?;
        Ok(problem.evaluate()?)
    }
}

pub fn rank_one_zero_generator(elapsed: BigRational) -> Result<DeclaredProjectionProblem, String> {
    let one = BasicMatrix::from_row_major(1, 1, vec![BigRational::one()]).map_err(|error| error.to_string())?;
    let zero = BasicMatrix::from_row_major(1, 1, vec![BigRational::zero()]).map_err(|error| error.to_string())?;
    Ok(DeclaredProjectionProblem {
        first: one.clone(),
        second: one,
        generator: zero,
        elapsed,
        state: vec![BigRational::one()],
    })
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
    fn unit_zero_generator_has_zero_first_order_leakage() -> Result<(), String> {
        unit_receipt().and_then(|(problem, receipt)| unit_claims(problem, receipt))
    }

    fn unit_receipt() -> Result<(DeclaredProjectionProblem, ProjectionObstructionReceipt), String> {
        let elapsed = ratio(1, 10).map_err(show)?;
        let problem = rank_one_zero_generator(elapsed).map_err(|error| error)?;
        let receipt = problem.evaluate().map_err(show)?;
        Ok((problem, receipt))
    }

    fn unit_claims(
        problem: DeclaredProjectionProblem,
        receipt: ProjectionObstructionReceipt,
    ) -> Result<(), String> {
        need(receipt.diagnostic.first_order_state_leakage.is_zero(), "leakage")?;
        need(receipt.diagnostic.commutator_l1.is_zero(), "commutator")?;
        unit_verify(problem, receipt)
    }

    fn unit_verify(
        problem: DeclaredProjectionProblem,
        receipt: ProjectionObstructionReceipt,
    ) -> Result<(), String> {
        need(receipt.authority_effect == AuthorityEffect::None, "authority")?;
        need(problem.verify(&receipt).map_err(show)?, "verify")
    }

    #[test]
    fn integration_elapsed_token_preserves_zero_leakage() -> Result<(), String> {
        integration_receipt().and_then(integration_claims)
    }

    fn integration_receipt() -> Result<ProjectionObstructionReceipt, String> {
        let problem = rank_one_zero_generator(BigRational::zero()).map_err(|error| error)?;
        problem.evaluate_elapsed_token("0").map_err(show)
    }

    fn integration_claims(receipt: ProjectionObstructionReceipt) -> Result<(), String> {
        need(receipt.diagnostic.first_order_operator_bound.is_zero(), "bound")?;
        need(receipt.problem.elapsed.is_zero(), "elapsed")
    }

    #[test]
    fn e2e_receipt_rejects_a_different_problem() -> Result<(), String> {
        e2e_pair().and_then(|(same, different)| e2e_claims(same, different))
    }

    fn e2e_pair() -> Result<(bool, bool), String> {
        let first = elapsed_problem(1, 10)?;
        let second = elapsed_problem(1, 5)?;
        let receipt = second.evaluate().map_err(show)?;
        e2e_flags(first, receipt)
    }

    fn elapsed_problem(numer: i64, denom: i64) -> Result<DeclaredProjectionProblem, String> {
        let elapsed = ratio(numer, denom).map_err(show)?;
        rank_one_zero_generator(elapsed).map_err(|error| error)
    }

    fn e2e_flags(
        first: DeclaredProjectionProblem,
        receipt: ProjectionObstructionReceipt,
    ) -> Result<(bool, bool), String> {
        let own = first.evaluate().map_err(show)?;
        let same = first.verify(&own).map_err(show)?;
        let different = first.verify(&receipt).map_err(show)?;
        Ok((same, different))
    }

    fn e2e_claims(same: bool, different: bool) -> Result<(), String> {
        need(same, "same")?;
        need(!different, "different")?;
        e2e_text()
    }

    fn e2e_text() -> Result<(), String> {
        need(ORIGIN.contains("po000_projection_obstruction.rs"), "origin")?;
        need(CLAIM.contains("zero first-order leakage"), "claim")?;
        need(AUTHORITY_EFFECT_TEXT.contains("None"), "text")
    }

    #[test]
    fn negative_refuses_negative_time_non_idempotent_shape_and_float() -> Result<(), String> {
        negative_time().and_then(|_| negative_matrix()).and_then(|_| negative_tokens())
    }

    fn negative_time() -> Result<(), String> {
        let elapsed = ratio(-1, 1).map_err(show)?;
        let negative = rank_one_zero_generator(elapsed).map_err(|error| error)?;
        need(
            matches!(negative.evaluate(), Err(ProjectionLeakageError::NegativeTime)),
            "time",
        )
    }

    fn negative_matrix() -> Result<(), String> {
        let entry = ratio(2, 1).map_err(show)?;
        let broken = BasicMatrix::from_row_major(1, 1, vec![entry]).map_err(show)?;
        let mut problem = rank_one_zero_generator(BigRational::zero()).map_err(|error| error)?;
        problem.first = broken;
        negative_shape(problem)
    }

    fn negative_shape(mut problem: DeclaredProjectionProblem) -> Result<(), String> {
        need(
            matches!(
                problem.evaluate(),
                Err(ProjectionLeakageError::NotIdempotent { index: 0 })
            ),
            "idempotent",
        )?;
        problem.state.clear();
        need(
            matches!(problem.evaluate(), Err(ProjectionLeakageError::Shape)),
            "shape",
        )
    }

    fn negative_tokens() -> Result<(), String> {
        need(
            admit_exact_integer("1.5") == Err(ProjectionTokenError::BinaryFloatRefused),
            "float",
        )?;
        need(
            admit_exact_integer("false") == Err(ProjectionTokenError::BooleanAsNumber),
            "bool",
        )
    }
}
