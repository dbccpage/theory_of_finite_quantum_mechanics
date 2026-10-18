
pub const PILOT_USABLE_BUDGET: u64 = 3;

pub fn pilot_minimax_value(
    gate_cost: u64,
    issue_receipt_cost: u64,
    repair_cost: u64,
    manual_audit_cost: u64,
) -> u64 {
    let gated_branch = issue_receipt_cost;
    let rejected_branch = repair_cost + issue_receipt_cost;
    let g5_route = gate_cost + gated_branch.max(rejected_branch);
    g5_route.min(manual_audit_cost)
}

pub fn resolves_within_budget(budget: u64) -> &'static str {
    let opt = pilot_minimax_value(1, 1, 1, 5);
    if opt <= budget {
        "ResolvedWithinBudget"
    } else {
        "Exhausted"
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn pilot_arena_minimax_cost_resolves_within_usable_budget() {
        assert_eq!(pilot_minimax_value(1, 1, 1, 5), PILOT_USABLE_BUDGET);
        assert_eq!(resolves_within_budget(PILOT_USABLE_BUDGET), "ResolvedWithinBudget");
        assert_eq!(resolves_within_budget(2), "Exhausted");
    }
}
