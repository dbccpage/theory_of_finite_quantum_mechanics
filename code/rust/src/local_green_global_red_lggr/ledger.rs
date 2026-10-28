
use tfqm_functional::gamma2::ExactGamma2Result;
use tfqm_functional::phi1::VerifiedExactPhi1;
use engine_policy::trichotomy::{CertifiedExactTrichotomy, ObstructionDiagnosticClass};
use crate::residual_families::{
    reconcile_verified, FamilyCollision, FamilyRegistry, RegistryWrite, ShapeSignature,
};
use engine_types::authority::{AuthorityEffect, Outcome, RefusalSource};
use engine_types::observer::Observer;
use serde::{Deserialize, Serialize};

use crate::epk_engine::EpkMetrics;
use num_traits::ToPrimitive;

#[derive(Debug, Clone, PartialEq, Eq, Serialize, Deserialize)]
pub struct EpkResidualFamilyReceipt {
    pub shape_signature: [u8; 32],
    pub q1_class_id: u64,
    pub gamma2_class_id: u64,
    pub lookup_hit: bool,
    pub inserted: bool,
}

#[derive(Debug, Clone, PartialEq, Eq, thiserror::Error)]
pub enum EpkResidualFamilyError {
    #[error("EPK residual-family binding requires a stabilized survivor, got {0:?}")]
    NotStabilized(ObstructionDiagnosticClass),
    #[error("the supplied trichotomy is not bound to the supplied Phi1/Gamma2 evidence")]
    EvidenceMismatch,
    #[error(transparent)]
    Family(#[from] FamilyCollision),
}

#[derive(Debug, Clone, PartialEq, Serialize, Deserialize)]
pub struct EpkResidualLedger {
    pub ngd: f64,
    pub nrke: Option<f64>,
    pub obstruction_status: Option<ObstructionDiagnosticClass>,
}

impl EpkResidualLedger {
    pub fn from_metrics(metrics: &EpkMetrics) -> Self {
        Self {
            ngd: metrics.ngd.to_f64().unwrap_or(0.0),
            nrke: metrics.nrke.as_ref().and_then(ToPrimitive::to_f64),
            obstruction_status: None,
        }
    }

    pub fn with_obstruction_status(mut self, status: ObstructionDiagnosticClass) -> Self {
        self.obstruction_status = Some(status);
        self
    }

    pub fn register_stabilized_family(
        &mut self,
        registry: &mut FamilyRegistry,
        signature: ShapeSignature,
        phi1: &VerifiedExactPhi1,
        gamma2: &ExactGamma2Result,
        trichotomy: &CertifiedExactTrichotomy,
        observer: &Observer,
    ) -> Result<EpkResidualFamilyReceipt, EpkResidualFamilyError> {
        if trichotomy.diagnostic_class() != ObstructionDiagnosticClass::ClosedResidual {
            return Err(EpkResidualFamilyError::NotStabilized(
                trichotomy.diagnostic_class(),
            ));
        }
        if trichotomy.phi1_value() != phi1.value()
            || trichotomy.gamma2_value() != gamma2.value()
            || phi1.primal_residual() != gamma2.residual()
            || phi1.d0() != gamma2.d0()
        {
            return Err(EpkResidualFamilyError::EvidenceMismatch);
        }

        let consultation = registry.consult(signature);
        let resolution = reconcile_verified(registry, consultation, phi1, gamma2, observer)?;
        self.obstruction_status = Some(trichotomy.diagnostic_class());

        Ok(EpkResidualFamilyReceipt {
            shape_signature: *resolution.signature().as_bytes(),
            q1_class_id: resolution.q1_class_id().as_u64(),
            gamma2_class_id: resolution.gamma2_class_id().as_u64(),
            lookup_hit: resolution.lookup_hit(),
            inserted: resolution.registry_write() == RegistryWrite::Inserted,
        })
    }

    pub fn authority_effect(&self) -> AuthorityEffect {
        AuthorityEffect::None
    }

    pub fn as_outcome(&self) -> Outcome {
        Outcome::Refused(RefusalSource::Residual)
    }
}

#[cfg(test)]
mod tests {
    use super::*;
    use crate::epk_engine::{calculate_metrics, CompositionRecord};
    use engine_types::authority::{
        authority_from_outcome_f13, AuthorityTerminal, DescentWitness, IsAuth,
    };

    fn valid_witness() -> DescentWitness {
        DescentWitness::from_verified_replay(
            AuthorityTerminal::ExactRuleDerived,
            "descent:epk-residual",
            "blake3:deadbeef",
        )
        .expect("nonempty refs produce a witness")
    }

    fn valid_is_auth() -> IsAuth {
        let evidence =
            engine_types::GuardEvidence::new_valid(["cand_01"], "K_carrier_01", "blake3:deadbeef");
        IsAuth::decide(AuthorityTerminal::ExactRuleDerived, evidence)
            .expect("all seven guards produce an IsAuth token")
    }

    fn ledgers_across_states() -> Vec<EpkResidualLedger> {
        vec![
            EpkResidualLedger {
                ngd: 0.0,
                nrke: Some(0.0),
                obstruction_status: Some(ObstructionDiagnosticClass::ExactRepair),
            },
            EpkResidualLedger {
                ngd: 0.4,
                nrke: Some(0.75),
                obstruction_status: Some(ObstructionDiagnosticClass::ClosedResidual),
            },
            EpkResidualLedger {
                ngd: 1.0,
                nrke: None,
                obstruction_status: Some(ObstructionDiagnosticClass::ActiveClosureFailure),
            },
            EpkResidualLedger {
                ngd: 0.0,
                nrke: None,
                obstruction_status: None,
            },
        ]
    }

    #[test]
    fn outcome_is_refused_residual_for_every_state() {
        for ledger in ledgers_across_states() {
            assert_eq!(
                ledger.as_outcome(),
                Outcome::Refused(RefusalSource::Residual),
                "state {ledger:?} must map to Refused(Residual)"
            );
            assert!(
                ledger.as_outcome().authority_terminal().is_none(),
                "state {ledger:?} must yield no authority terminal"
            );
        }
    }

    #[test]
    fn authority_effect_is_none_for_every_state() {
        for ledger in ledgers_across_states() {
            assert!(
                ledger.authority_effect().is_none(),
                "state {ledger:?} must carry no authority effect"
            );
        }
    }

    #[test]
    fn firewall_no_authority_even_with_valid_witness() {
        for ledger in ledgers_across_states() {
            let got = authority_from_outcome_f13(
                ledger.as_outcome(),
                Some(valid_witness()),
                Some(valid_is_auth()),
            );
            assert!(
                got.is_none(),
                "EPK residual must never authorize, even with a witness and IsAuth token; state {ledger:?}"
            );
        }
    }

    use num_rational::BigRational;

    #[test]
    fn from_metrics_carries_residual_signals_but_still_refuses() {
        let comps =
            vec![CompositionRecord::new("c0", "l0", "r0", true, true, false, None).unwrap()];
        let metrics = calculate_metrics(
            &comps,
            None,
            Some(BigRational::new(1.into(), 2.into())),
            Some(BigRational::new(1.into(), 4.into())),
            None,
        )
        .unwrap();

        let ledger = EpkResidualLedger::from_metrics(&metrics);
        assert_eq!(ledger.nrke, Some(0.25));
        assert!((ledger.ngd - 1.0).abs() < 1e-12);

        assert_eq!(
            ledger.as_outcome(),
            Outcome::Refused(RefusalSource::Residual)
        );
        assert!(ledger.authority_effect().is_none());
        assert!(authority_from_outcome_f13(
            ledger.as_outcome(),
            Some(valid_witness()),
            Some(valid_is_auth())
        )
        .is_none());
    }
}
