
use crate::prime_algos::prime_algorithm_0::{
    CochainSlot, CochainWindow, DeclarationFill, DefectBranch, DomainAdapter, LiftSearch,
    PrimeAlgorithm0Receipt, PrimeStepRecord, PrimeTerminal,
};
use crate::ddc::dda_alphabet::{DdaOp, DdaStep, DdaTrace, TraceTerminal};
use omega_types::authority::AuthorityEffect;
use serde::Serialize;
use std::fmt;

#[derive(Debug, Clone, PartialEq, Eq, Serialize)]
pub struct AdmittedDeclaration {
    carrier: String,
    primitive_difference: String,
    zero_rel: String,
    cochain: CochainSlot,
    observer: String,
    witnesses: Vec<String>,
}

impl AdmittedDeclaration {
    pub fn carrier(&self) -> &str {
        &self.carrier
    }

    pub fn primitive_difference(&self) -> &str {
        &self.primitive_difference
    }

    pub fn zero_rel(&self) -> &str {
        &self.zero_rel
    }

    pub fn cochain(&self) -> &CochainSlot {
        &self.cochain
    }

    pub fn observer(&self) -> &str {
        &self.observer
    }

    pub fn witnesses(&self) -> &[String] {
        &self.witnesses
    }
}

#[derive(Debug, Clone, PartialEq, Eq, Serialize)]
pub struct AdmissionRefusal {
    pub prime_step: u8,
    pub reason: &'static str,
    pub detail: String,
}

impl fmt::Display for AdmissionRefusal {
    fn fmt(&self, f: &mut fmt::Formatter<'_>) -> fmt::Result {
        write!(
            f,
            "admission refused at step {}: {} ({})",
            self.prime_step, self.reason, self.detail
        )
    }
}

impl std::error::Error for AdmissionRefusal {}

impl AdmissionRefusal {
    pub fn to_receipt(&self, adapter: &dyn DomainAdapter) -> PrimeAlgorithm0Receipt {
        let decl = adapter.declaration();
        let family = adapter.residual_family_label();
        let mut trace = DdaTrace::new();
        let mut steps: Vec<PrimeStepRecord> = Vec::new();

        let mut emit = |prime_step: u8, op: DdaOp, executed: bool, message: String| {
            if executed {
                trace.emit(DdaStep::executed(op, message.clone()));
            } else {
                trace.emit(DdaStep::refused(op, message.clone()));
            }
            steps.push(PrimeStepRecord {
                prime_step,
                op: op.letter().to_string(),
                executed,
                message,
                phi1_after: None,
                gamma2_after: None,
                loss_ledger: None,
            });
        };

        if self.prime_step == 1 {
            emit(
                1,
                DdaOp::Refusal,
                false,
                format!("step1 refuse: {}", self.reason),
            );
        } else {
            emit(
                1,
                DdaOp::ContextExposure,
                true,
                format!("declare carrier={}", decl.carrier.as_deref().unwrap_or("")),
            );
            emit(1, DdaOp::Integration, true, "ledger open".into());
        }

        if self.prime_step > 1 {
            if self.prime_step == 2 {
                emit(
                    2,
                    DdaOp::Refusal,
                    false,
                    format!("step2 refuse: {}", self.reason),
                );
            } else {
                emit(
                    2,
                    DdaOp::Integration,
                    true,
                    format!(
                        "declare δ={}",
                        decl.primitive_difference.as_deref().unwrap_or("")
                    ),
                );
            }
        }

        if self.prime_step > 2 {
            if self.prime_step == 3 {
                emit(
                    3,
                    DdaOp::Refusal,
                    false,
                    format!("step3 refuse: {}", self.reason),
                );
            } else {
                emit(
                    3,
                    DdaOp::Integration,
                    true,
                    format!("declare ZeroRel={}", decl.zero_rel.as_deref().unwrap_or("")),
                );
            }
        }

        let cochain = if self.prime_step == 4 {
            emit(
                4,
                DdaOp::Refusal,
                false,
                format!("step4 refuse: {}", self.reason),
            );
            if self.reason == "COCHAIN_NOT_SQUARE_ZERO" {
                let mass = adapter
                    .cochain_window()
                    .map(|w| w.l1_defect_mass)
                    .unwrap_or(0);
                CochainSlot::RefusedNotSquareZero {
                    l1_defect_mass: mass,
                }
            } else {
                CochainSlot::MissingUnjustified
            }
        } else if self.prime_step > 4 {
            match adapter.cochain_window() {
                Some(w) => {
                    emit(
                        4,
                        DdaOp::ContextExposure,
                        true,
                        format!(
                            "construct C• dims=({},{},{}) d∘d=0 ok",
                            w.dim_c0, w.dim_c1, w.dim_c2
                        ),
                    );
                    CochainSlot::Constructed {
                        dim_c0: w.dim_c0,
                        dim_c1: w.dim_c1,
                        dim_c2: w.dim_c2,
                        square_zero: true,
                    }
                }
                None => CochainSlot::BlockedEarly,
            }
        } else {
            CochainSlot::BlockedEarly
        };

        let observer = if self.prime_step == 7 {
            emit(
                7,
                DdaOp::Refusal,
                false,
                "step7: observer undeclared — refuse view-from-nowhere".into(),
            );
            Some("MISSING_observer".into())
        } else {
            decl.observer.clone()
        };

        let witnesses = if self.prime_step == 8 {
            emit(
                8,
                DdaOp::Refusal,
                false,
                "step8: no witness supplied — a declared difference is not its own evidence".into(),
            );
            vec![]
        } else {
            decl.witnesses.clone()
        };

        emit(
            11,
            DdaOp::Terminalize,
            true,
            format!("terminalize Refusal reason={}", self.reason),
        );

        let letter_tape: String = steps.iter().map(|s| s.op.as_str()).collect();
        let letters_spaced = trace.letters();
        let trace_terminal = match trace.terminal() {
            TraceTerminal::Open => "Open".into(),
            TraceTerminal::Terminalized => "Terminalized".into(),
            TraceTerminal::Refused => "Refused".into(),
            TraceTerminal::OracleNeeded { import } => format!("OracleNeeded:{import}"),
            TraceTerminal::UnverifiedTerminal => "UnverifiedTerminal".into(),
        };

        PrimeAlgorithm0Receipt {
            domain: adapter.domain(),
            carrier: decl.carrier,
            primitive_difference: decl.primitive_difference,
            zero_rel: decl.zero_rel,
            cochain,
            q1: None,
            phi1: None,
            gamma2: None,
            observer,
            witnesses,
            structure_search: LiftSearch::SkippedClosed,
            licensed_lift: None,
            routing: "blocked_at_admission".into(),
            literature_compare: None,
            branch: DefectBranch::Unset,
            terminal: PrimeTerminal::Refusal,
            letter_tape,
            letters_spaced,
            trace_terminal,
            residual_family_label: family,
            authority_effect: AuthorityEffect::None,
            steps,
            evidence_provenance: adapter.evidence_provenance(),
        }
    }
}

pub fn admit(
    decl: &DeclarationFill,
    justify_cochain: bool,
    window: Option<&CochainWindow>,
) -> Result<AdmittedDeclaration, AdmissionRefusal> {
    let carrier = match &decl.carrier {
        Some(c) if !c.trim().is_empty() => c.clone(),
        _ => {
            return Err(AdmissionRefusal {
                prime_step: 1,
                reason: "MISSING_carrier",
                detail: "carrier undeclared or empty".into(),
            });
        }
    };

    let primitive_difference = match &decl.primitive_difference {
        Some(d) if !d.trim().is_empty() => d.clone(),
        _ => {
            return Err(AdmissionRefusal {
                prime_step: 2,
                reason: "MISSING_primitive_difference",
                detail: "primitive difference undeclared or empty".into(),
            });
        }
    };

    let zero_rel = match &decl.zero_rel {
        Some(z) if !z.trim().is_empty() => z.clone(),
        _ => {
            return Err(AdmissionRefusal {
                prime_step: 3,
                reason: "MISSING_zero_rel",
                detail: "zero_rel undeclared or empty".into(),
            });
        }
    };

    if !justify_cochain {
        return Err(AdmissionRefusal {
            prime_step: 4,
            reason: "COCHAIN_UNJUSTIFIED",
            detail: "cochain not justified by δ/ZeroRel".into(),
        });
    }
    let cochain = match window {
        None => {
            return Err(AdmissionRefusal {
                prime_step: 4,
                reason: "COCHAIN_WINDOW_MISSING",
                detail: "cochain justified but window missing".into(),
            });
        }
        Some(w) if !w.square_zero => {
            return Err(AdmissionRefusal {
                prime_step: 4,
                reason: "COCHAIN_NOT_SQUARE_ZERO",
                detail: format!("d1∘d0 ≠ 0, mass={}", w.l1_defect_mass),
            });
        }
        Some(w) => CochainSlot::Constructed {
            dim_c0: w.dim_c0,
            dim_c1: w.dim_c1,
            dim_c2: w.dim_c2,
            square_zero: true,
        },
    };

    let observer = match &decl.observer {
        Some(o) if !o.trim().is_empty() && o != "MISSING_observer" => o.clone(),
        _ => {
            return Err(AdmissionRefusal {
                prime_step: 7,
                reason: "MISSING_observer",
                detail: "observer undeclared — refuse view-from-nowhere".into(),
            });
        }
    };

    if decl.witnesses.is_empty() {
        return Err(AdmissionRefusal {
            prime_step: 8,
            reason: "MISSING_witness",
            detail: "no witness supplied — a declared difference is not its own evidence".into(),
        });
    }
    let witnesses = decl.witnesses.clone();

    Ok(AdmittedDeclaration {
        carrier,
        primitive_difference,
        zero_rel,
        cochain,
        observer,
        witnesses,
    })
}

#[cfg(test)]
mod tests {
    use super::*;

    fn valid_fill() -> DeclarationFill {
        DeclarationFill {
            carrier: Some("torus".into()),
            primitive_difference: Some("d0".into()),
            zero_rel: Some("z0".into()),
            observer: Some("observer_alpha".into()),
            witnesses: vec!["w1".into()],
        }
    }

    fn valid_window() -> CochainWindow {
        CochainWindow {
            dim_c0: 2,
            dim_c1: 3,
            dim_c2: 1,
            square_zero: true,
            l1_defect_mass: 0,
        }
    }

    #[test]
    fn valid_declaration_admits() {
        let decl = valid_fill();
        let win = valid_window();
        let admitted = admit(&decl, true, Some(&win)).expect("should admit valid declaration");
        assert_eq!(admitted.carrier(), "torus");
        assert_eq!(admitted.observer(), "observer_alpha");
        assert_eq!(admitted.witnesses(), &["w1"]);
    }

    #[test]
    fn missing_carrier_refuses_at_step_1() {
        let mut decl = valid_fill();
        decl.carrier = None;
        let win = valid_window();
        let err = admit(&decl, true, Some(&win)).expect_err("missing carrier must refuse");
        assert_eq!(err.prime_step, 1);
        assert_eq!(err.reason, "MISSING_carrier");
    }

    #[test]
    fn missing_primitive_difference_refuses_at_step_2() {
        let mut decl = valid_fill();
        decl.primitive_difference = Some("".into());
        let win = valid_window();
        let err = admit(&decl, true, Some(&win)).expect_err("empty delta must refuse");
        assert_eq!(err.prime_step, 2);
        assert_eq!(err.reason, "MISSING_primitive_difference");
    }

    #[test]
    fn missing_zero_rel_refuses_at_step_3() {
        let mut decl = valid_fill();
        decl.zero_rel = None;
        let win = valid_window();
        let err = admit(&decl, true, Some(&win)).expect_err("missing zero_rel must refuse");
        assert_eq!(err.prime_step, 3);
        assert_eq!(err.reason, "MISSING_zero_rel");
    }

    #[test]
    fn unjustified_cochain_refuses_at_step_4() {
        let decl = valid_fill();
        let win = valid_window();
        let err = admit(&decl, false, Some(&win)).expect_err("unjustified cochain must refuse");
        assert_eq!(err.prime_step, 4);
        assert_eq!(err.reason, "COCHAIN_UNJUSTIFIED");
    }

    #[test]
    fn non_square_zero_cochain_refuses_at_step_4() {
        let decl = valid_fill();
        let mut win = valid_window();
        win.square_zero = false;
        win.l1_defect_mass = 5;
        let err = admit(&decl, true, Some(&win)).expect_err("non square-zero cochain must refuse");
        assert_eq!(err.prime_step, 4);
        assert_eq!(err.reason, "COCHAIN_NOT_SQUARE_ZERO");
    }

    #[test]
    fn missing_observer_refuses_at_step_7() {
        let mut decl = valid_fill();
        decl.observer = None;
        let win = valid_window();
        let err = admit(&decl, true, Some(&win)).expect_err("missing observer must refuse");
        assert_eq!(err.prime_step, 7);
        assert_eq!(err.reason, "MISSING_observer");
    }

    #[test]
    fn empty_witnesses_refuses_at_step_8() {
        let mut decl = valid_fill();
        decl.witnesses = vec![];
        let win = valid_window();
        let err = admit(&decl, true, Some(&win)).expect_err("empty witnesses must refuse");
        assert_eq!(err.prime_step, 8);
        assert_eq!(err.reason, "MISSING_witness");
    }
}
