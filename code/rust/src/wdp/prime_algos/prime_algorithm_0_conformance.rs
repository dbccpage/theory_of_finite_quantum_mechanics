
use crate::prime_algos::prime_algorithm_0::PrimeAlgorithm0Receipt;
use crate::ddc::dda_alphabet::DdaOp;
use serde::Serialize;

pub const REQUIRED_LETTERS: [char; 3] = ['C', 'R', 'T'];

pub const AGENT_ACTIVE_LETTERS: [char; 5] = ['E', 'R', 'I', 'M', 'T'];

pub const UNDECIDABLE_WITHOUT_PER_STEP_STATE: [&str; 3] = [
    "E must land at Exact (needs the after-state cochain, not just its masses)",
    "I/M/T inert on the cochain (needs before/after cochain state)",
    "C/D/Lambda must actually change the carrier (needs per-step carrier identity)",
];

pub const NEWLY_DECIDABLE_WITH_PER_STEP_STATE: [&str; 2] = [
    "R must not move Phi1 (decided from PrimeStepRecord::phi1_after)",
    "D requires a loss ledger (decided from PrimeStepRecord::loss_ledger)",
];

#[derive(Debug, Clone, PartialEq, Eq, Serialize)]
pub enum ReceiptViolation {
    TerminalizedOpenResidual { gamma2: u64 },
    ForeignLetter { letter: char },
    MissingRequiredLetter { letter: char },
    AuthorityMinted { effect: String },
    TapeStepMismatch { tape: String, from_steps: String },
    ResidualProjectionMovedPhi1 {
        prime_step: u8,
        before: Option<u64>,
        after: Option<u64>,
    },
    DescentWithoutLossLedger { prime_step: u8 },
    StepMassesContradictReceipt {
        prime_step: u8,
        step_phi1: Option<u64>,
        receipt_phi1: Option<u64>,
    },
}

#[derive(Debug, Clone, PartialEq, Eq, Serialize)]
pub enum ConformanceVerdict {
    Conforms,
    Partial { unchecked_laws: Vec<String> },
    Violated {
        violations: Vec<ReceiptViolation>,
        unchecked_laws: Vec<String>,
    },
}

impl ConformanceVerdict {
    pub fn conforms(&self) -> bool {
        matches!(self, ConformanceVerdict::Conforms)
    }

    pub fn no_decidable_violation(&self) -> bool {
        !matches!(self, ConformanceVerdict::Violated { .. })
    }

    pub fn violations(&self) -> &[ReceiptViolation] {
        match self {
            ConformanceVerdict::Violated { violations, .. } => violations,
            _ => &[],
        }
    }

    pub fn unchecked_laws(&self) -> &[String] {
        match self {
            ConformanceVerdict::Conforms => &[],
            ConformanceVerdict::Partial { unchecked_laws }
            | ConformanceVerdict::Violated { unchecked_laws, .. } => unchecked_laws,
        }
    }
}

#[derive(Debug, Clone, PartialEq, Eq, Serialize)]
pub struct ReceiptConformance {
    pub domain: String,
    pub letter_tape: String,
    pub phi1: Option<u64>,
    pub gamma2: Option<u64>,
    pub terminal: String,
    pub verdict: ConformanceVerdict,
    pub letters_unrepresentable_at_agent_surface: Vec<char>,
}

impl ReceiptConformance {
    pub fn conforms(&self) -> bool {
        self.verdict.conforms()
    }

    pub fn no_decidable_violation(&self) -> bool {
        self.verdict.no_decidable_violation()
    }

    pub fn violations(&self) -> &[ReceiptViolation] {
        self.verdict.violations()
    }
}

fn alphabet_chars() -> Vec<char> {
    DdaOp::alphabet()
        .iter()
        .flat_map(|o| o.letter().chars())
        .collect()
}

fn unchecked() -> Vec<String> {
    UNDECIDABLE_WITHOUT_PER_STEP_STATE
        .iter()
        .map(|s| (*s).to_string())
        .collect()
}

pub fn check_receipt(r: &PrimeAlgorithm0Receipt) -> ReceiptConformance {
    let allowed = alphabet_chars();
    let mut violations = Vec::new();

    if r.letter_tape.contains('T') {
        if let Some(g) = r.gamma2 {
            if g != 0 {
                violations.push(ReceiptViolation::TerminalizedOpenResidual { gamma2: g });
            }
        }
    }

    let mut seen_foreign = Vec::new();
    for c in r.letter_tape.chars() {
        if !allowed.contains(&c) && !seen_foreign.contains(&c) {
            seen_foreign.push(c);
            violations.push(ReceiptViolation::ForeignLetter { letter: c });
        }
    }

    for req in REQUIRED_LETTERS {
        if !r.letter_tape.contains(req) {
            violations.push(ReceiptViolation::MissingRequiredLetter { letter: req });
        }
    }

    if !r.authority_is_none() {
        violations.push(ReceiptViolation::AuthorityMinted {
            effect: format!("{:?}", r.authority_effect),
        });
    }

    let from_steps: String = r.steps.iter().map(|s| s.op.as_str()).collect();
    if from_steps != r.letter_tape {
        violations.push(ReceiptViolation::TapeStepMismatch {
            tape: r.letter_tape.clone(),
            from_steps,
        });
    }

    let mut prev_phi1: Option<u64> = None;
    let mut seen_first = false;
    for step in &r.steps {
        if step.op == "R" && seen_first && step.phi1_after != prev_phi1 {
            violations.push(ReceiptViolation::ResidualProjectionMovedPhi1 {
                prime_step: step.prime_step,
                before: prev_phi1,
                after: step.phi1_after,
            });
        }
        prev_phi1 = step.phi1_after;
        seen_first = true;
    }

    for step in &r.steps {
        if step.op == "D"
            && step
                .loss_ledger
                .as_ref()
                .map(|l| l.is_empty())
                .unwrap_or(true)
        {
            violations.push(ReceiptViolation::DescentWithoutLossLedger {
                prime_step: step.prime_step,
            });
        }
    }

    for step in &r.steps {
        if step.prime_step >= 6 && step.phi1_after != r.phi1 {
            violations.push(ReceiptViolation::StepMassesContradictReceipt {
                prime_step: step.prime_step,
                step_phi1: step.phi1_after,
                receipt_phi1: r.phi1,
            });
            break;
        }
    }

    let mut unrepresentable: Vec<char> = Vec::new();
    for c in r.letter_tape.chars() {
        if allowed.contains(&c)
            && !AGENT_ACTIVE_LETTERS.contains(&c)
            && !unrepresentable.contains(&c)
        {
            unrepresentable.push(c);
        }
    }

    let verdict = if violations.is_empty() {
        ConformanceVerdict::Partial {
            unchecked_laws: unchecked(),
        }
    } else {
        ConformanceVerdict::Violated {
            violations,
            unchecked_laws: unchecked(),
        }
    };

    ReceiptConformance {
        domain: r.domain.as_str().to_string(),
        letter_tape: r.letter_tape.clone(),
        phi1: r.phi1,
        gamma2: r.gamma2,
        terminal: r.terminal.as_str().to_string(),
        verdict,
        letters_unrepresentable_at_agent_surface: unrepresentable,
    }
}

pub fn check_builtin_roster() -> Vec<ReceiptConformance> {
    crate::prime_algos::rosetta::builtin_receipts()
        .iter()
        .map(check_receipt)
        .collect()
}

#[cfg(test)]
mod tests {
    use super::*;
    use crate::prime_algos::prime_algorithm_0::{PrimeAlgorithm0Receipt, PrimeStepRecord};

    #[test]
    fn clean_receipt_is_partial_not_conformant() {
        let roster = check_builtin_roster();
        assert!(!roster.is_empty());
        for c in &roster {
            assert!(
                !c.conforms(),
                "{} reported full conformance while {} laws are unevaluated",
                c.domain,
                UNDECIDABLE_WITHOUT_PER_STEP_STATE.len()
            );
            assert_eq!(
                c.verdict.unchecked_laws().len(),
                UNDECIDABLE_WITHOUT_PER_STEP_STATE.len(),
                "{} dropped the unchecked-law list",
                c.domain
            );
        }
    }

    fn receipt_with(tape: &str, gamma2: Option<u64>) -> PrimeAlgorithm0Receipt {
        let mut r = crate::prime_algos::rosetta::builtin_receipts()
            .into_iter()
            .next()
            .expect("roster is non-empty");
        r.letter_tape = tape.to_string();
        r.gamma2 = gamma2;
        r.steps = tape
            .chars()
            .map(|c| PrimeStepRecord {
                prime_step: 1,
                op: c.to_string(),
                executed: c != 'M',
                message: String::new(),
                phi1_after: None,
                gamma2_after: None,
                loss_ledger: None,
            })
            .collect();
        r
    }

    #[test]
    fn terminalizing_an_open_residual_is_a_violation() {
        let c = check_receipt(&receipt_with("CRT", Some(1)));
        assert!(!c.no_decidable_violation());
        assert!(c
            .violations()
            .contains(&ReceiptViolation::TerminalizedOpenResidual { gamma2: 1 }));
    }

    #[test]
    fn terminalizing_a_closed_residual_is_lawful() {
        let c = check_receipt(&receipt_with("CRT", Some(0)));
        assert!(c.no_decidable_violation(), "{:?}", c.violations());
    }

    #[test]
    fn missing_required_letter_is_a_violation() {
        let c = check_receipt(&receipt_with("CR", Some(0)));
        assert!(c
            .violations()
            .contains(&ReceiptViolation::MissingRequiredLetter { letter: 'T' }));
    }

    #[test]
    fn foreign_letter_is_a_violation() {
        let c = check_receipt(&receipt_with("CRTZ", Some(0)));
        assert!(c
            .violations()
            .contains(&ReceiptViolation::ForeignLetter { letter: 'Z' }));
    }

    #[test]
    fn tape_disagreeing_with_steps_is_a_violation() {
        let mut r = receipt_with("CRT", Some(0));
        r.letter_tape = "CRTE".into();
        let c = check_receipt(&r);
        assert!(
            c.violations()
                .iter()
                .any(|v| matches!(v, ReceiptViolation::TapeStepMismatch { .. })),
            "expected a tape/step mismatch, got {:?}",
            c.violations()
        );
    }

    #[test]
    fn r_step_moving_phi1_is_a_violation() {
        let mut r = receipt_with("CRT", Some(0));
        r.steps[0].phi1_after = Some(1);
        r.steps[1].phi1_after = Some(4);
        let c = check_receipt(&r);
        assert!(
            c.violations().iter().any(|v| matches!(
                v,
                ReceiptViolation::ResidualProjectionMovedPhi1 {
                    before: Some(1),
                    after: Some(4),
                    ..
                }
            )),
            "expected an R-law violation, got {:?}",
            c.violations()
        );
    }

    #[test]
    fn r_step_preserving_phi1_is_lawful() {
        let mut r = receipt_with("CRT", Some(0));
        for step in r.steps.iter_mut() {
            step.phi1_after = Some(1);
        }
        let c = check_receipt(&r);
        assert!(
            !c.violations()
                .iter()
                .any(|v| matches!(v, ReceiptViolation::ResidualProjectionMovedPhi1 { .. })),
            "R law fired on an unchanged Φ₁: {:?}",
            c.violations()
        );
    }

    #[test]
    fn descent_without_loss_ledger_is_a_violation() {
        let r = receipt_with("CRDT", Some(0));
        let c = check_receipt(&r);
        assert!(
            c.violations()
                .iter()
                .any(|v| matches!(v, ReceiptViolation::DescentWithoutLossLedger { .. })),
            "expected a D-law violation, got {:?}",
            c.violations()
        );
    }

    #[test]
    fn descent_with_a_populated_loss_ledger_is_lawful() {
        let mut r = receipt_with("CRDT", Some(0));
        let d = r
            .steps
            .iter_mut()
            .find(|s| s.op == "D")
            .expect("D step present");
        let mut ledger = std::collections::BTreeMap::new();
        ledger.insert("gauge_potentials_removed".to_string(), 3u64);
        d.loss_ledger = Some(ledger);
        let c = check_receipt(&r);
        assert!(
            !c.violations()
                .iter()
                .any(|v| matches!(v, ReceiptViolation::DescentWithoutLossLedger { .. })),
            "D law fired despite a populated ledger: {:?}",
            c.violations()
        );
    }

    #[test]
    fn step_masses_contradicting_the_receipt_is_a_violation() {
        let mut r = receipt_with("CRT", Some(0));
        r.phi1 = Some(1);
        r.steps[0].prime_step = 6;
        r.steps[0].phi1_after = Some(99);
        let c = check_receipt(&r);
        assert!(
            c.violations()
                .iter()
                .any(|v| matches!(v, ReceiptViolation::StepMassesContradictReceipt { .. })),
            "expected a step/receipt mass contradiction, got {:?}",
            c.violations()
        );
    }

    #[test]
    fn undecidable_list_shrank_by_exactly_the_newly_decidable_laws() {
        assert_eq!(UNDECIDABLE_WITHOUT_PER_STEP_STATE.len(), 3);
        assert_eq!(NEWLY_DECIDABLE_WITH_PER_STEP_STATE.len(), 2);
        for law in UNDECIDABLE_WITHOUT_PER_STEP_STATE {
            assert!(
                !law.contains("loss ledger"),
                "the loss-ledger law is decided now; it must not be listed undecidable"
            );
            assert!(
                !law.starts_with("R must not move"),
                "the R law is decided now; it must not be listed undecidable"
            );
        }
    }
}
