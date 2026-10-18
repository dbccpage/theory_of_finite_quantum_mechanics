//! Companion Rust witness for PROD-P1-NEXT-2 (P1 negative controls: Impossible policy gate & forged cert rejection).

#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub enum AbstentionLabel {
    SolvedOptimally,
    LosingInDeclaredArena,
    Impossible,
    RefusedCertificate,
}

#[derive(Debug, Clone, PartialEq, Eq)]
pub struct Certificate {
    pub task_id: &'static str,
    pub outcome: &'static str,
    pub trap_closed: bool,
    pub win_witness_valid: bool,
}

pub fn verify_and_classify(
    arena_task_id: &str,
    cert: &Certificate,
    task_admits_impossibility: bool,
) -> AbstentionLabel {
    if cert.task_id != arena_task_id {
        return AbstentionLabel::RefusedCertificate;
    }
    match cert.outcome {
        "WIN_OPTIMAL" => {
            if cert.win_witness_valid {
                AbstentionLabel::SolvedOptimally
            } else {
                AbstentionLabel::RefusedCertificate
            }
        }
        "LOSS" => {
            if !cert.trap_closed {
                AbstentionLabel::RefusedCertificate
            } else if task_admits_impossibility {
                AbstentionLabel::Impossible
            } else {
                AbstentionLabel::LosingInDeclaredArena
            }
        }
        _ => AbstentionLabel::RefusedCertificate,
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn negative_controls_impossible_without_policy_and_forged_certificates() {
        let valid_loss = Certificate {
            task_id: "arena-loss",
            outcome: "LOSS",
            trap_closed: true,
            win_witness_valid: false,
        };
        assert_eq!(
            verify_and_classify("arena-loss", &valid_loss, false),
            AbstentionLabel::LosingInDeclaredArena
        );
        assert_eq!(
            verify_and_classify("arena-loss", &valid_loss, true),
            AbstentionLabel::Impossible
        );

        let forged_task = Certificate {
            task_id: "forged-task-id",
            ..valid_loss
        };
        assert_eq!(
            verify_and_classify("arena-loss", &forged_task, true),
            AbstentionLabel::RefusedCertificate
        );

        let forged_win = Certificate {
            outcome: "WIN_OPTIMAL",
            ..valid_loss
        };
        assert_eq!(
            verify_and_classify("arena-loss", &forged_win, false),
            AbstentionLabel::RefusedCertificate
        );
    }
}
