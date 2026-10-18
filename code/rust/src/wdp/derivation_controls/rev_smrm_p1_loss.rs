
#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub enum AbstentionLabel {
    Stalled,
    Exhausted,
    LosingInDeclaredArena,
    Impossible,
    RefusedCertificate,
}

pub fn verify_loss_trap_set(
    initial_belief: &str,
    trap_set: &[&str],
    trap_disjoint_from_goal: bool,
    trap_closed: bool,
    task_admits_impossibility: bool,
) -> AbstentionLabel {
    let contains_b0 = trap_set.contains(&initial_belief);
    if !contains_b0 || !trap_disjoint_from_goal || !trap_closed {
        return AbstentionLabel::RefusedCertificate;
    }
    if task_admits_impossibility {
        AbstentionLabel::Impossible
    } else {
        AbstentionLabel::LosingInDeclaredArena
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn loss_certificate_missing_initial_belief_is_refused() {
        assert_eq!(
            verify_loss_trap_set("b0", &["b1", "b2"], true, true, true),
            AbstentionLabel::RefusedCertificate
        );
        assert_eq!(
            verify_loss_trap_set("b0", &["b0", "b1"], true, true, true),
            AbstentionLabel::Impossible
        );
        assert_ne!(AbstentionLabel::Stalled, AbstentionLabel::Exhausted);
        assert_ne!(AbstentionLabel::Exhausted, AbstentionLabel::Impossible);
        assert_ne!(AbstentionLabel::Stalled, AbstentionLabel::Impossible);
    }
}
