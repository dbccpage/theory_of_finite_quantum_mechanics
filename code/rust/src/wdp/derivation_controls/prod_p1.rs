//! P1 Abstention and Impossibility Governor (PROD-P1) exact verifier.

#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub enum TerminationLabel {
    Terminated,
    OutOfFuel,
    Impossible,
    InvalidRequest,
}

pub fn decide_abstention(
    certificate_valid: bool,
    optimal_cost: Option<u64>,
    budget: u64,
) -> TerminationLabel {
    if !certificate_valid {
        return TerminationLabel::InvalidRequest;
    }
    match optimal_cost {
        None => TerminationLabel::Impossible,
        Some(cost) if budget < cost => TerminationLabel::OutOfFuel,
        Some(_) => TerminationLabel::Terminated,
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_p1_partition_labels() {
        assert_eq!(decide_abstention(true, Some(3), 2), TerminationLabel::OutOfFuel);
        assert_eq!(decide_abstention(true, Some(3), 3), TerminationLabel::Terminated);
        assert_eq!(decide_abstention(true, None, 100), TerminationLabel::Impossible);
        assert_eq!(decide_abstention(false, Some(3), 3), TerminationLabel::InvalidRequest);
    }
}
