
pub mod finite_routing;
pub mod descent_engine;
pub mod domain_adapters;
pub mod licensed_lift_gate;
pub mod prime_algorithm_0;
pub mod prime_algorithm_0_admission;
pub mod prime_algorithm_0_conformance;
pub mod prime_algorithm_1;
pub mod prime_algorithm_2;
pub mod prime_candidate;
pub mod prime_scope;
pub mod rosetta;

pub use prime_algorithm_0 as oeprmalg0;
pub use prime_algorithm_0_admission as oeprmalg0_admission;
pub use prime_algorithm_0_conformance as oeprmalg0_conformance;
pub use prime_algorithm_1 as oeprmalg1;
pub use prime_algorithm_2 as oeprmalg2;

pub use descent_engine::{DescentExecutionReceipt, DescentRefusal, PrimeDescentCoordinator};
pub use licensed_lift_gate::{LicensedLiftAdmission, NineUpLiftBits, PaperEr003LiftCertificate};
pub use prime_algorithm_0::{
    run_admitted, run_oeprmalg0, run_prime_algorithm_0, DomainAdapter, Oeprmalg0Receipt,
    PrimeAlgorithm0Receipt, PrimeDomain,
};
pub use prime_algorithm_1::{
    transport, LossLedger, TransportRefusal, TransportStatus, TransportedPacket,
};
pub use prime_algorithm_2::{
    can_continue_n, terminalize, write_step, AntiCheatLaw, Budget, ContinuationEvidence,
    ControlState, Gamma2Zero, LawRefusal, OpenControlState, StepClaim, StepOp, StepPermit,
    TerminalControlState, TerminalPermit, TerminalRefusal,
};
pub use prime_candidate::{
    compute_prime_stage_hash, CandidateProposalV1, PrimeStage, PrimeStageRecordV1, PrimeTraceLogger,
    EMPTY_STAGE_HASH,
};
pub use prime_scope::{BoundCarrierManifest, CallerAttested, ScopeBinding};

pub const ORIGIN: &str =
    "Origin: code/rust/src/wdp/prime_algos/mod.rs @ 40de7d5cda1ff1f0db8305d0c1b2103646fab197";
pub const CLAIM: &str = "Claim: prime stages are totally ordered and a later stage record links only by repeating the previous record hash";
pub const AUTHORITY_EFFECT: &str = "AuthorityEffect: None";
pub const MUTATION_KILLS: u32 = 0;

#[derive(Debug, Clone, PartialEq, Eq)]
pub enum FacadeLinkError {
    HashMismatch { seq: u64 },
    BrokenLink { seq: u64 },
    BinaryFloatRefused,
    BooleanAsNumber,
    InexactToken,
    Overflow,
}

pub fn stage_rank(stage: &PrimeStage) -> u8 {
    match stage {
        PrimeStage::PrimeMinus1 => 0,
        PrimeStage::Prime000 => 1,
        PrimeStage::Prime001 => 2,
        PrimeStage::Prime002 => 3,
    }
}

pub fn stage_precedes(left: &PrimeStage, right: &PrimeStage) -> bool {
    stage_rank(left) < stage_rank(right)
}

pub fn admit_exact_integer(token: &str) -> Result<i64, FacadeLinkError> {
    if token == "true" || token == "false" {
        return Err(FacadeLinkError::BooleanAsNumber);
    }
    if token.bytes().any(|byte| matches!(byte, b'.' | b'e' | b'E')) {
        return Err(FacadeLinkError::BinaryFloatRefused);
    }
    parse_signed_digits(token)
}

fn parse_signed_digits(token: &str) -> Result<i64, FacadeLinkError> {
    let (negative, digits) = match token.strip_prefix('-') {
        Some(rest) => (true, rest),
        None => (false, token),
    };
    if digits.is_empty() || !digits.bytes().all(|byte| byte.is_ascii_digit()) {
        return Err(FacadeLinkError::InexactToken);
    }
    let mut value = 0i64;
    for byte in digits.bytes() {
        let digit = i64::from(byte - b'0');
        value = value
            .checked_mul(10)
            .and_then(|place| place.checked_add(digit))
            .ok_or(FacadeLinkError::Overflow)?;
    }
    if negative {
        value = value.checked_neg().ok_or(FacadeLinkError::Overflow)?;
    }
    Ok(value)
}

pub fn record_links(
    previous: &PrimeStageRecordV1,
    next: &PrimeStageRecordV1,
) -> Result<(), FacadeLinkError> {
    let expected = compute_prime_stage_hash(
        next.seq,
        next.stage.as_str(),
        &next.packet_id,
        &next.actor,
        &next.status,
        &next.witness_or_refusal,
        next.prev_record_hash.as_deref(),
    );
    if next.record_hash != expected {
        return Err(FacadeLinkError::HashMismatch { seq: next.seq });
    }
    match next.prev_record_hash.as_deref() {
        Some(link) if link == previous.record_hash => Ok(()),
        _ => Err(FacadeLinkError::BrokenLink { seq: next.seq }),
    }
}

#[cfg(test)]
mod facade_tests {
    use super::*;

    fn need(cond: bool, message: &str) -> Result<(), String> {
        if cond {
            Ok(())
        } else {
            Err(message.to_string())
        }
    }

    fn pair() -> (PrimeStageRecordV1, PrimeStageRecordV1) {
        let previous = PrimeStageRecordV1::new(
            0,
            PrimeStage::PrimeMinus1,
            "PKT_0",
            "actor_0",
            "UNTRUSTED",
            "none",
            None,
        );
        let next = PrimeStageRecordV1::new(
            1,
            PrimeStage::Prime000,
            "PKT_1",
            "actor_1",
            "ADMITTED",
            "valid_cochain",
            Some(previous.record_hash.clone()),
        );
        (previous, next)
    }

    #[test]
    fn unit_stage_order_is_total_on_the_four_names() -> Result<(), String> {
        unit_order().and_then(|_| unit_rank())
    }

    fn unit_order() -> Result<(), String> {
        need(stage_precedes(&PrimeStage::PrimeMinus1, &PrimeStage::Prime000), "m1")?;
        need(stage_precedes(&PrimeStage::Prime000, &PrimeStage::Prime001), "000")?;
        need(stage_precedes(&PrimeStage::Prime001, &PrimeStage::Prime002), "001")
    }

    fn unit_rank() -> Result<(), String> {
        need(!stage_precedes(&PrimeStage::Prime002, &PrimeStage::PrimeMinus1), "not cyclic")?;
        need(stage_rank(&PrimeStage::Prime002) == 3, "rank")
    }

    #[test]
    fn integration_facade_links_a_real_hash_chain() -> Result<(), String> {
        let (previous, next) = pair();
        record_links(&previous, &next).map_err(|error| format!("{error:?}"))?;
        need(previous.record_hash == EMPTY_STAGE_HASH, "vector")?;
        need(AUTHORITY_EFFECT.ends_with("None"), "authority")?;
        Ok(())
    }

    #[test]
    fn e2e_claim_names_the_link_law() -> Result<(), String> {
        let (previous, next) = pair();
        record_links(&previous, &next).map_err(|error| format!("{error:?}"))?;
        need(ORIGIN.contains("prime_algos/mod.rs"), "origin")?;
        need(CLAIM.contains("totally ordered"), "claim")?;
        Ok(())
    }

    #[test]
    fn negative_broken_link_float_and_boolean_are_refused() -> Result<(), String> {
        let (previous, mut next) = pair();
        next.prev_record_hash = Some("00".to_string());
        next.record_hash = compute_prime_stage_hash(
            next.seq,
            next.stage.as_str(),
            &next.packet_id,
            &next.actor,
            &next.status,
            &next.witness_or_refusal,
            next.prev_record_hash.as_deref(),
        );
        need(
            matches!(record_links(&previous, &next), Err(FacadeLinkError::BrokenLink { seq: 1 })),
            "link",
        )?;
        need(admit_exact_integer("1.5") == Err(FacadeLinkError::BinaryFloatRefused), "float")?;
        need(admit_exact_integer("false") == Err(FacadeLinkError::BooleanAsNumber), "bool")?;
        Ok(())
    }
}
