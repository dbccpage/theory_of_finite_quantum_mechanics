//! Staged PFP runner dependency, path, and budget-reservation preflight control for PLAN-7D-PREFLIGHT.

#[derive(Clone, Copy, Debug, PartialEq, Eq)]
pub struct RunnerPreflightConfig {
    pub jsonschema_present: bool,
    pub runner_path_present: bool,
    pub canonical_controller_present: bool,
    pub legacy_live_requested: bool,
    pub unbounded_legacy_override: bool,
}

#[derive(Clone, Copy, Debug, PartialEq, Eq)]
pub enum PreflightDecision {
    ReadyOffline,
    RefusedMissingDependency,
    RefusedLegacyLiveRequiresCanonicalPfp,
}

pub fn evaluate_runner_preflight(cfg: RunnerPreflightConfig) -> PreflightDecision {
    if !cfg.jsonschema_present || !cfg.runner_path_present || !cfg.canonical_controller_present {
        return PreflightDecision::RefusedMissingDependency;
    }
    if cfg.legacy_live_requested && !cfg.unbounded_legacy_override {
        return PreflightDecision::RefusedLegacyLiveRequiresCanonicalPfp;
    }
    PreflightDecision::ReadyOffline
}

pub fn collate_reservation(
    budget_cap_cents: u64,
    reserved_cents: u64,
    actual_cost_cents: Option<u64>,
) -> Result<(u64, u64), &'static str> {
    if budget_cap_cents == 0 || reserved_cents == 0 || reserved_cents > budget_cap_cents {
        return Err("invalid reservation or budget cap");
    }
    match actual_cost_cents {
        None => Ok((reserved_cents, budget_cap_cents - reserved_cents)),
        Some(actual) => {
            if actual > budget_cap_cents {
                return Err("actual cost exceeds budget cap");
            }
            Ok((actual, budget_cap_cents - actual))
        }
    }
}

#[test]
fn runner_preflight_blocks_unguarded_legacy_live_and_retains_unknown_cost() {
    let offline_cfg = RunnerPreflightConfig {
        jsonschema_present: true,
        runner_path_present: true,
        canonical_controller_present: true,
        legacy_live_requested: false,
        unbounded_legacy_override: false,
    };
    assert_eq!(
        evaluate_runner_preflight(offline_cfg),
        PreflightDecision::ReadyOffline
    );

    let live_cfg = RunnerPreflightConfig {
        legacy_live_requested: true,
        ..offline_cfg
    };
    assert_eq!(
        evaluate_runner_preflight(live_cfg),
        PreflightDecision::RefusedLegacyLiveRequiresCanonicalPfp
    );

    let missing_dep = RunnerPreflightConfig {
        jsonschema_present: false,
        ..offline_cfg
    };
    assert_eq!(
        evaluate_runner_preflight(missing_dep),
        PreflightDecision::RefusedMissingDependency
    );

    assert_eq!(collate_reservation(1000, 250, None), Ok((250, 750)));
    assert_eq!(collate_reservation(1000, 250, Some(180)), Ok((180, 820)));
    assert_eq!(
        collate_reservation(100, 200, None),
        Err("invalid reservation or budget cap")
    );
}
