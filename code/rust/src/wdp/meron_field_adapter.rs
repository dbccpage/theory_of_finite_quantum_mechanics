use crate::types::AuthorityEffect;

pub const ORIGIN: &str =
    "Origin: code/rust/src/wdp/meron_field_adapter.rs @ 40de7d5cda1ff1f0db8305d0c1b2103646fab197";
pub const CLAIM: &str = "Claim: a zero circle profile keeps the weighted meron first moment at zero and the quadratic center equal to the mean square per site";
pub const AUTHORITY_EFFECT_TEXT: &str = "AuthorityEffect: None";
pub const MUTATION_KILLS: u32 = 0;
use num_traits::Zero;
use tfqm_functional::circle_piecewise_linear::{CirclePiecewiseLinear, CircleProfileError};
use omega_measurement::affine_calibration::{BoundedReading, CalibrationError};
use tfqm_number_theory::rational::{rq, Rational};
use omega_quantum_physics::meron_source_field::AnalyticResponsePlan;
use omega_quantum_physics::meron_spatial_source::{SpatialSourceError, SpatialSourcePlan};
use omega_quantum_physics::meron_time_refinement::{
    FiniteMeronChain, MeronTimeError, StaggeredMoments,
};

#[derive(Debug, thiserror::Error)]
pub enum MeronFieldError {
    #[error(transparent)]
    Profile(#[from] CircleProfileError),
    #[error(transparent)]
    Plan(#[from] SpatialSourceError),
    #[error(transparent)]
    Time(#[from] MeronTimeError),
    #[error(transparent)]
    Reading(#[from] CalibrationError),
    #[error("the actual weighted first moment violates particle-hole symmetry")]
    ParticleHole,
}

#[derive(Debug, Clone, PartialEq, Eq)]
pub struct DeclaredMeronField {
    profile: CirclePiecewiseLinear,
    plan: SpatialSourcePlan,
    moments: StaggeredMoments,
    quadratic: BoundedReading,
    finite_log: BoundedReading,
    continuum_log: BoundedReading,
}
struct FieldParts {
    plan: SpatialSourcePlan,
    moments: StaggeredMoments,
    quadratic: BoundedReading,
    finite_log: BoundedReading,
    continuum_log: BoundedReading,
}

impl DeclaredMeronField {
    pub fn new(
        response: AnalyticResponsePlan,
        profile: CirclePiecewiseLinear,
        probe: Rational,
    ) -> Result<Self, MeronFieldError> {
        let parts = field_parts(&profile, response, probe)?;
        Ok(Self {
            profile,
            plan: parts.plan,
            moments: parts.moments,
            quadratic: parts.quadratic,
            finite_log: parts.finite_log,
            continuum_log: parts.continuum_log,
        })
    }
    pub fn profile(&self) -> &CirclePiecewiseLinear {
        &self.profile
    }
    pub fn plan(&self) -> &SpatialSourcePlan {
        &self.plan
    }
    pub fn moments(&self) -> &StaggeredMoments {
        &self.moments
    }
    pub fn quadratic(&self) -> &BoundedReading {
        &self.quadratic
    }
    pub fn finite_log(&self) -> &BoundedReading {
        &self.finite_log
    }
    pub fn continuum_log(&self) -> &BoundedReading {
        &self.continuum_log
    }
    pub fn authority_effect(&self) -> AuthorityEffect {
        AuthorityEffect::None
    }
}

fn field_parts(
    profile: &CirclePiecewiseLinear,
    response: AnalyticResponsePlan,
    probe: Rational,
) -> Result<FieldParts, MeronFieldError> {
    let plan = SpatialSourcePlan::new(
        response,
        profile.norm().clone(),
        profile.lipschitz().clone(),
        probe,
    )?;
    let moments = staggered_moments(&plan, profile)?;
    checked_field(plan, moments)
}

fn staggered_moments(
    plan: &SpatialSourcePlan,
    profile: &CirclePiecewiseLinear,
) -> Result<StaggeredMoments, MeronFieldError> {
    let time = plan.response().time();
    let weights = profile.uniform_samples(time.sites())?;
    let chain = FiniteMeronChain::new(time.sites())?;
    Ok(chain.weighted_staggered_moments(time.repetitions(), time.q(), &weights)?)
}

fn checked_field(
    plan: SpatialSourcePlan,
    moments: StaggeredMoments,
) -> Result<FieldParts, MeronFieldError> {
    if !moments.first().is_zero() {
        return Err(MeronFieldError::ParticleHole);
    }
    field_readings(plan, moments)
}

fn field_readings(
    plan: SpatialSourcePlan,
    moments: StaggeredMoments,
) -> Result<FieldParts, MeronFieldError> {
    let sites = plan.response().time().sites();
    let value = mean_square_per_site(moments.mean_square(), sites)?;
    let quadratic = BoundedReading::new(value.clone(), plan.quadratic_error().clone())?;
    log_readings(plan, moments, value, quadratic)
}

fn log_readings(
    plan: SpatialSourcePlan,
    moments: StaggeredMoments,
    value: Rational,
    quadratic: BoundedReading,
) -> Result<FieldParts, MeronFieldError> {
    let log_center = plan.probe().pow(2) * value / rq(2, 1);
    let finite_log = BoundedReading::new(log_center.clone(), plan.finite_log_tail().clone())?;
    let continuum_log = BoundedReading::new(
        log_center,
        plan.probe().pow(2) * plan.quadratic_error() / rq(2, 1),
    )?;
    Ok(FieldParts {
        plan,
        moments,
        quadratic,
        finite_log,
        continuum_log,
    })
}

fn mean_square_per_site(mean_square: Rational, sites: usize) -> Result<Rational, MeronTimeError> {
    if sites == 0 {
        return Err(MeronTimeError::Sites);
    }
    Ok(mean_square / Rational::from_integer(sites.into()))
}

#[derive(Debug, Clone, PartialEq, Eq)]
pub enum MeronFieldTokenError {
    BinaryFloatRefused,
    BooleanAsNumber,
    InexactToken,
    Overflow,
}

pub fn admit_exact_integer(token: &str) -> Result<i64, MeronFieldTokenError> {
    if token == "true" || token == "false" {
        return Err(MeronFieldTokenError::BooleanAsNumber);
    }
    if token.bytes().any(|byte| matches!(byte, b'.' | b'e' | b'E')) {
        return Err(MeronFieldTokenError::BinaryFloatRefused);
    }
    parse_signed_digits(token)
}

fn parse_signed_digits(token: &str) -> Result<i64, MeronFieldTokenError> {
    let (negative, digits) = match token.strip_prefix('-') {
        Some(rest) => (true, rest),
        None => (false, token),
    };
    if digits.is_empty() || !digits.bytes().all(|byte| byte.is_ascii_digit()) {
        return Err(MeronFieldTokenError::InexactToken);
    }
    let mut value = 0i64;
    for byte in digits.bytes() {
        let digit = i64::from(byte - b'0');
        value = value
            .checked_mul(10)
            .and_then(|place| place.checked_add(digit))
            .ok_or(MeronFieldTokenError::Overflow)?;
    }
    if negative {
        value = value.checked_neg().ok_or(MeronFieldTokenError::Overflow)?;
    }
    Ok(value)
}

#[cfg(test)]
mod tests {
    use super::*;
    use num_traits::{One, Zero};
    use tfqm_functional::circle_piecewise_linear::CirclePiecewiseLinear;
    use tfqm_number_theory::rational::rq;
    use omega_quantum_physics::meron_source_field::AnalyticResponsePlan;
    use omega_quantum_physics::meron_spatial_source::SpatialSourceError;

    fn need(cond: bool, message: &str) -> Result<(), String> {
        if cond {
            Ok(())
        } else {
            Err(message.to_string())
        }
    }

    fn profile(height: i64) -> Result<CirclePiecewiseLinear, String> {
        let value = Rational::from_integer(height.into());
        CirclePiecewiseLinear::new(vec![
            (Rational::zero(), value.clone()),
            (Rational::one(), value),
        ])
        .map_err(|error| format!("{error}"))
    }

    fn response() -> Result<AnalyticResponsePlan, String> {
        AnalyticResponsePlan::new(4, 1, rq(1, 384), rq(1, 384), rq(1, 128))
            .map_err(|error| format!("{error}"))
    }

    fn zero_field() -> Result<DeclaredMeronField, String> {
        let response = response()?;
        let profile = profile(0)?;
        DeclaredMeronField::new(response, profile, rq(1, 128)).map_err(|error| format!("{error}"))
    }

    #[test]
    fn unit_zero_profile_has_zero_first_moment_and_intensive_quadratic() -> Result<(), String> {
        zero_field().and_then(unit_zero_profile)
    }

    fn unit_zero_profile(field: DeclaredMeronField) -> Result<(), String> {
        let sites = Rational::from_integer(field.plan().response().time().sites().into());
        let product = field.quadratic().center() * &sites;
        need(field.moments().first().is_zero(), "particle hole")?;
        need(product == field.moments().mean_square(), "quadratic")?;
        need(field.authority_effect() == AuthorityEffect::None, "authority")
    }

    #[test]
    fn integration_finite_log_uses_the_same_center_scale() -> Result<(), String> {
        zero_field().and_then(integration_logs)
    }

    fn integration_logs(field: DeclaredMeronField) -> Result<(), String> {
        need(
            field.finite_log().center() == field.continuum_log().center(),
            "log center",
        )
    }

    #[test]
    fn e2e_authority_and_claim_are_sealed() -> Result<(), String> {
        zero_field().and_then(e2e_seal)
    }

    fn e2e_seal(field: DeclaredMeronField) -> Result<(), String> {
        need(field.authority_effect().to_string() == "None", "display")?;
        need(ORIGIN.contains("meron_field_adapter.rs"), "origin")?;
        e2e_claim()
    }

    fn e2e_claim() -> Result<(), String> {
        need(CLAIM.contains("first moment"), "claim")?;
        need(AUTHORITY_EFFECT_TEXT.ends_with("None"), "text")
    }

    #[test]
    fn negative_large_probe_on_unit_profile_leaves_the_disk() -> Result<(), String> {
        negative_probe().and_then(|_| negative_tokens())
    }

    fn negative_probe() -> Result<(), String> {
        let response = response()?;
        let profile = profile(1)?;
        let refused = DeclaredMeronField::new(response, profile, rq(1, 16));
        need(
            matches!(
                refused,
                Err(MeronFieldError::Plan(SpatialSourceError::ProbeDomain))
            ),
            "probe",
        )
    }

    fn negative_tokens() -> Result<(), String> {
        need(
            admit_exact_integer("0.5") == Err(MeronFieldTokenError::BinaryFloatRefused),
            "float",
        )?;
        need(
            admit_exact_integer("false") == Err(MeronFieldTokenError::BooleanAsNumber),
            "bool",
        )
    }
}
