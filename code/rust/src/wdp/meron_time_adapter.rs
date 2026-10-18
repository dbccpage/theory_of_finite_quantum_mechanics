//! Retains the declared finite time plan and the mathematical owner's trace.
//! Source correspondence and the written common-target theorem have separate scopes.

use crate::types::AuthorityEffect;
use omega_number_theory::rational::Rational;
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

/// Retains the actual model owner's nonzero-source trace and declared plan.
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

/// Retains the actual intensive time-averaged SQL/Kubo query and AR-9 radius.
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
        let intensive_response =
            moments.mean_square() / Rational::from_integer(time.sites().into());
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
