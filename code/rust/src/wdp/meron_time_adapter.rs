
use crate::types::AuthorityEffect;
use tfqm_number_theory::rational::Rational;

pub const ORIGIN: &str =
    "Origin: code/rust/src/wdp/meron_time_adapter.rs @ 40de7d5cda1ff1f0db8305d0c1b2103646fab197";
pub const CLAIM: &str = "Claim: the intensive meron response is the staggered mean square divided by the positive site count";
pub const AUTHORITY_EFFECT_TEXT: &str = "AuthorityEffect: None";
pub const MUTATION_KILLS: u32 = 0;
use omega_quantum_physics::meron_source_field::{
    AnalyticResponseError, AnalyticResponsePlan, SourceFieldPlan,
};
use omega_quantum_physics::meron_time_refinement::{
    EulerTimePlan, FiniteMeronChain, MeronTimeError, StaggeredMoments,
};

#[derive(Debug, Clone, PartialEq, Eq)]
pub struct DeclaredMeronTime {
    plan: EulerTimePlan,
    unscaled_partition: Rational,
}

impl DeclaredMeronTime {
    pub fn new(plan: EulerTimePlan) -> Result<Self, MeronTimeError> {
        let chain = FiniteMeronChain::new(plan.sites())?;
        let unscaled_partition = chain.transfer_trace(plan.repetitions(), plan.q())?;
        Ok(Self {
            plan,
            unscaled_partition,
        })
    }

    pub fn plan(&self) -> &EulerTimePlan {
        &self.plan
    }
    pub fn unscaled_partition(&self) -> &Rational {
        &self.unscaled_partition
    }
    pub fn staggered_moments(&self) -> Result<StaggeredMoments, MeronTimeError> {
        let moments = FiniteMeronChain::new(self.plan.sites())?
            .staggered_moments(self.plan.repetitions(), self.plan.q())?;
        if moments.partition() != &self.unscaled_partition {
            return Err(MeronTimeError::Matrix(
                linear_algebra::exact_field::ExactFieldError::ReplayFailed {
                    operation: "Meron observable partition",
                },
            ));
        }
        Ok(moments)
    }
    pub fn authority_effect(&self) -> AuthorityEffect {
        AuthorityEffect::None
    }
}

#[derive(Debug, Clone, PartialEq, Eq)]
pub struct DeclaredMeronSource {
    plan: SourceFieldPlan,
    unscaled_partition: Rational,
}
impl DeclaredMeronSource {
    pub fn new(plan: SourceFieldPlan) -> Result<Self, MeronTimeError> {
        let time = plan.time();
        let unscaled_partition = FiniteMeronChain::new(time.sites())?.source_field_trace(
            time.repetitions(),
            time.q(),
            plan.v(),
        )?;
        Ok(Self {
            plan,
            unscaled_partition,
        })
    }
    pub fn plan(&self) -> &SourceFieldPlan {
        &self.plan
    }
    pub fn unscaled_partition(&self) -> &Rational {
        &self.unscaled_partition
    }
    pub fn authority_effect(&self) -> AuthorityEffect {
        AuthorityEffect::None
    }
}

#[derive(Debug, Clone, PartialEq, Eq)]
pub struct DeclaredMeronResponse {
    plan: AnalyticResponsePlan,
    moments: StaggeredMoments,
    intensive_response: Rational,
}
impl DeclaredMeronResponse {
    pub fn new(plan: AnalyticResponsePlan) -> Result<Self, AnalyticResponseError> {
        let time = plan.time();
        let moments = DeclaredMeronTime::new(time.clone())?.staggered_moments()?;
        let intensive_response = mean_square_per_site(moments.mean_square(), time.sites())?;
        Ok(Self {
            plan,
            moments,
            intensive_response,
        })
    }
    pub fn plan(&self) -> &AnalyticResponsePlan {
        &self.plan
    }
    pub fn moments(&self) -> &StaggeredMoments {
        &self.moments
    }
    pub fn intensive_response(&self) -> &Rational {
        &self.intensive_response
    }
    pub fn authority_effect(&self) -> AuthorityEffect {
        AuthorityEffect::None
    }
}

fn mean_square_per_site(mean_square: Rational, sites: usize) -> Result<Rational, MeronTimeError> {
    if sites == 0 {
        return Err(MeronTimeError::Sites);
    }
    Ok(mean_square / Rational::from_integer(sites.into()))
}

#[derive(Debug, Clone, PartialEq, Eq)]
pub enum MeronTokenError {
    BinaryFloatRefused,
    BooleanAsNumber,
    InexactToken,
    Overflow,
}

pub fn admit_exact_integer(token: &str) -> Result<i64, MeronTokenError> {
    if token == "true" || token == "false" {
        return Err(MeronTokenError::BooleanAsNumber);
    }
    if token.bytes().any(|byte| matches!(byte, b'.' | b'e' | b'E')) {
        return Err(MeronTokenError::BinaryFloatRefused);
    }
    parse_signed_digits(token)
}

fn parse_signed_digits(token: &str) -> Result<i64, MeronTokenError> {
    let (negative, digits) = match token.strip_prefix('-') {
        Some(rest) => (true, rest),
        None => (false, token),
    };
    if digits.is_empty() || !digits.bytes().all(|byte| byte.is_ascii_digit()) {
        return Err(MeronTokenError::InexactToken);
    }
    let mut value = 0i64;
    for byte in digits.bytes() {
        let digit = i64::from(byte - b'0');
        value = value
            .checked_mul(10)
            .and_then(|place| place.checked_add(digit))
            .ok_or(MeronTokenError::Overflow)?;
    }
    if negative {
        value = value.checked_neg().ok_or(MeronTokenError::Overflow)?;
    }
    Ok(value)
}

#[cfg(test)]
mod tests {
    use super::*;
    use super::StaggeredMoments;
    use tfqm_number_theory::rational::rq;
    use omega_quantum_physics::meron_source_field::AnalyticResponsePlan;

    fn need(cond: bool, message: &str) -> Result<(), String> {
        if cond {
            Ok(())
        } else {
            Err(message.to_string())
        }
    }

    fn response() -> Result<DeclaredMeronResponse, String> {
        let plan = AnalyticResponsePlan::new(4, 1, rq(1, 384), rq(1, 384), rq(1, 128))
            .map_err(|error| format!("{error}"))?;
        DeclaredMeronTime::new(plan.time().clone()).map_err(|error| format!("{error}"))?;
        DeclaredMeronResponse::new(plan).map_err(|error| format!("{error}"))
    }

    #[test]
    fn unit_intensive_response_times_sites_is_mean_square() -> Result<(), String> {
        let declared = response()?;
        let sites = Rational::from_integer(declared.plan().time().sites().into());
        let product = declared.intensive_response() * &sites;
        need(product == declared.moments().mean_square(), "intensive")?;
        Ok(())
    }

    #[test]
    fn integration_time_partition_matches_staggered_partition() -> Result<(), String> {
        integration_time().and_then(|(time, moments)| integration_partition(time, moments))
    }

    fn integration_time() -> Result<(DeclaredMeronTime, StaggeredMoments), String> {
        let plan = EulerTimePlan::new(4, 1, rq(1, 384), rq(1, 384)).map_err(|error| format!("{error}"))?;
        let time = DeclaredMeronTime::new(plan).map_err(|error| format!("{error}"))?;
        let moments = time.staggered_moments().map_err(|error| format!("{error}"))?;
        Ok((time, moments))
    }

    fn integration_partition(
        time: DeclaredMeronTime,
        moments: StaggeredMoments,
    ) -> Result<(), String> {
        need(moments.partition() == time.unscaled_partition(), "trace")?;
        need(time.authority_effect() == AuthorityEffect::None, "authority")
    }

    #[test]
    fn e2e_response_seals_authority_and_claim() -> Result<(), String> {
        response().and_then(e2e_seal).and_then(|_| e2e_claim())
    }

    fn e2e_seal(declared: DeclaredMeronResponse) -> Result<(), String> {
        need(declared.authority_effect() == AuthorityEffect::None, "authority")?;
        need(declared.authority_effect().to_string() == "None", "display")
    }

    fn e2e_claim() -> Result<(), String> {
        need(ORIGIN.contains("meron_time_adapter.rs"), "origin")?;
        need(CLAIM.contains("site count"), "claim")?;
        need(AUTHORITY_EFFECT_TEXT.ends_with("None"), "text")
    }

    #[test]
    fn negative_refuses_odd_sites_hot_temperature_and_float_token() -> Result<(), String> {
        negative_plans().and_then(|_| negative_tokens())
    }

    fn negative_plans() -> Result<(), String> {
        need(EulerTimePlan::new(3, 1, rq(1, 384), rq(1, 384)).is_err(), "sites")?;
        need(
            AnalyticResponsePlan::new(4, 1, rq(1, 10), rq(1, 384), rq(1, 128)).is_err(),
            "temperature",
        )
    }

    fn negative_tokens() -> Result<(), String> {
        need(
            admit_exact_integer("1.5") == Err(MeronTokenError::BinaryFloatRefused),
            "float",
        )?;
        need(
            admit_exact_integer("true") == Err(MeronTokenError::BooleanAsNumber),
            "bool",
        )
    }
}
