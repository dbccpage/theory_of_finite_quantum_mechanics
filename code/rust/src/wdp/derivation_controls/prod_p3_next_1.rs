//! Finite executable witness for `PROD-P3-NEXT-1`.
//!
//! Models the P3 `GuardTransferChecker` soundness check (source soundness +
//! target transfer safety under a representation adapter) and exact Appendix Q.4
//! rational break-even pricing, with fixed `authority_effect = "None"`.

#![forbid(unsafe_code)]

use std::collections::{BTreeMap, BTreeSet};

pub const AUTHORITY_EFFECT_NONE: &str = "None";

#[derive(Debug, Clone, PartialEq, Eq)]
pub struct GuardRule {
    pub rule_id: String,
    pub instance_id: String,
    pub rejects: BTreeSet<String>,
    pub authority_effect: &'static str,
}

#[derive(Debug, Clone, PartialEq, Eq)]
pub enum TransferRefusal {
    SourceUnsound(Vec<String>),
    TransferUnsafe(Vec<String>),
}

pub fn check_rule_transfer(
    rule: &GuardRule,
    source_valid: &BTreeSet<String>,
    target_id: &str,
    target_valid: &BTreeSet<String>,
    adapter: &BTreeMap<String, String>,
) -> Result<GuardRule, TransferRefusal> {
    let source_counterexamples: Vec<String> =
        rule.rejects.intersection(source_valid).cloned().collect();
    if !source_counterexamples.is_empty() {
        return Err(TransferRefusal::SourceUnsound(source_counterexamples));
    }

    let transferred_rejects: BTreeSet<String> = adapter
        .iter()
        .filter_map(|(y, x)| {
            if rule.rejects.contains(x) {
                Some(y.clone())
            } else {
                None
            }
        })
        .collect();

    let target_counterexamples: Vec<String> = transferred_rejects
        .intersection(target_valid)
        .cloned()
        .collect();
    if !target_counterexamples.is_empty() {
        return Err(TransferRefusal::TransferUnsafe(target_counterexamples));
    }

    Ok(GuardRule {
        rule_id: rule.rule_id.clone(),
        instance_id: target_id.to_string(),
        rejects: transferred_rejects,
        authority_effect: AUTHORITY_EFFECT_NONE,
    })
}

pub fn gcd(mut a: i128, mut b: i128) -> i128 {
    a = a.abs();
    b = b.abs();
    while b != 0 {
        let r = a % b;
        a = b;
        b = r;
    }
    if a == 0 { 1 } else { a }
}

/// Computes exact rational saving `h*v - N*g - C_0` as reduced `(num, den)`.
pub fn price_saving(
    candidates: i128,
    hits: i128,
    v_num: i128,
    v_den: i128,
    g_num: i128,
    g_den: i128,
    c0_num: i128,
    c0_den: i128,
) -> (i128, i128) {
    let den = v_den * g_den * c0_den;
    let num = hits * v_num * g_den * c0_den
        - candidates * g_num * v_den * c0_den
        - c0_num * v_den * g_den;
    let d = gcd(num, den);
    (num / d, den / d)
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn sound_transfer_admits_circulation_and_refuses_unsafe_or_unsound_rules() {
        let source_valid: BTreeSet<String> = ["zero".to_string()].into_iter().collect();
        let target_valid: BTreeSet<String> =
            ["zero".to_string(), "gradient".to_string()].into_iter().collect();
        let adapter: BTreeMap<String, String> = [
            ("zero".to_string(), "zero".to_string()),
            ("gradient".to_string(), "gradient".to_string()),
            ("curved".to_string(), "curved".to_string()),
        ]
        .into_iter()
        .collect();

        let circulation = GuardRule {
            rule_id: "circulation".to_string(),
            instance_id: "zero-repairs".to_string(),
            rejects: ["curved".to_string()].into_iter().collect(),
            authority_effect: AUTHORITY_EFFECT_NONE,
        };
        let transferred = check_rule_transfer(
            &circulation,
            &source_valid,
            "all-triangle-repairs",
            &target_valid,
            &adapter,
        )
        .expect("circulation transfers soundly");
        assert_eq!(transferred.instance_id, "all-triangle-repairs");
        assert_eq!(transferred.authority_effect, "None");

        let unsafe_rule = GuardRule {
            rule_id: "unsafe-point".to_string(),
            instance_id: "zero-repairs".to_string(),
            rejects: ["gradient".to_string()].into_iter().collect(),
            authority_effect: AUTHORITY_EFFECT_NONE,
        };
        assert_eq!(
            check_rule_transfer(
                &unsafe_rule,
                &source_valid,
                "all-triangle-repairs",
                &target_valid,
                &adapter
            ),
            Err(TransferRefusal::TransferUnsafe(vec!["gradient".to_string()]))
        );

        let unsound_rule = GuardRule {
            rule_id: "invalid-source-rule".to_string(),
            instance_id: "zero-repairs".to_string(),
            rejects: ["zero".to_string()].into_iter().collect(),
            authority_effect: AUTHORITY_EFFECT_NONE,
        };
        assert_eq!(
            check_rule_transfer(
                &unsound_rule,
                &source_valid,
                "all-triangle-repairs",
                &target_valid,
                &adapter
            ),
            Err(TransferRefusal::SourceUnsound(vec!["zero".to_string()]))
        );

        // Reference input.json saving: N=4, h=2, v=1, g=1/10, C_0=1 -> 3/5
        assert_eq!(price_saving(4, 2, 1, 1, 1, 10, 1, 1), (3, 5));
        // Q.4 worked example: N=10000, v=1, g=1/1000, C_0=2 -> h=12 gives 0, h=13 gives 1
        assert_eq!(price_saving(10000, 12, 1, 1, 1, 1000, 2, 1), (0, 1));
        assert_eq!(price_saving(10000, 13, 1, 1, 1, 1000, 2, 1), (1, 1));
    }
}
