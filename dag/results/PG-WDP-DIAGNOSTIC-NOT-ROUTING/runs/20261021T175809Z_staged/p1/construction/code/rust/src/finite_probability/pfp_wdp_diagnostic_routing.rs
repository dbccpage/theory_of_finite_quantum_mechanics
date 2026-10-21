//! Diagnostic class, routing terminal, residual class and authority tag: exhaustive tables of the real source maps.
//!
//! Exact replay of `code/python/src/qm/pfp_wdp_diagnostic_routing.py` for PFP batch 01, node
//! PG-WDP-DIAGNOSTIC-NOT-ROUTING. The enumerations and maps are transcribed from the_symbol_game
//! (`omega_types` routing.rs / terminal_status.rs, `omega_policy` trichotomy.rs, `omega_id_run` run.rs 626-633,
//! `omega_certifiers` checked_packet.rs 248, external WitnessedDifference/Routing.lean). Rust uses enums and `match`;
//! it recomputes every summary by enumeration (all 343 policies, all 640 fiber inputs, all 21 statuses) and never reads
//! the Python. The source defines no map from the diagnostic class to a routing terminal except the partial composite
//! run.rs + terminal_routing.json. AuthorityEffect: None.

use std::collections::{BTreeMap, BTreeSet};

#[derive(Clone, Copy, PartialEq, Eq, Debug)]
pub enum Ts {
    ExactRuleDerived, UniqueOutputDerived, NoRuleInSearchClass, NonUniqueOutput, EnumeratorFailure, Refused,
    LabelConflictsWithDerivation, BudgetUnknown, InvalidProposal, OperatorConflict, UnknownSector, NoDescentYet,
    LabelOnlyUncertified, LiftRequired, ParseRefused, ReplayMismatch, PolicyAmbiguous, NoPacket, VerifierDisabled,
    SearchIncomplete, PolicyUnderspecified,
}
use Ts::*;

pub const ALL_TS: [Ts; 21] = [
    ExactRuleDerived, UniqueOutputDerived, NoRuleInSearchClass, NonUniqueOutput, EnumeratorFailure, Refused,
    LabelConflictsWithDerivation, BudgetUnknown, InvalidProposal, OperatorConflict, UnknownSector, NoDescentYet,
    LabelOnlyUncertified, LiftRequired, ParseRefused, ReplayMismatch, PolicyAmbiguous, NoPacket, VerifierDisabled,
    SearchIncomplete, PolicyUnderspecified,
];

pub const ROUTES: [&str; 7] = ["CheckPassed", "RequiresLift", "Repair", "Refusal", "NoRule", "BudgetUnknown", "Refused"];

fn ts_name(s: Ts) -> String {
    format!("{:?}", s)
}

fn ts_route(s: Ts) -> &'static str {
    match s {
        ExactRuleDerived | UniqueOutputDerived => "CheckPassed",
        NoRuleInSearchClass => "NoRule",
        NonUniqueOutput | EnumeratorFailure | UnknownSector | NoDescentYet | LabelOnlyUncertified | ReplayMismatch
        | PolicyAmbiguous | VerifierDisabled | SearchIncomplete | PolicyUnderspecified => "Repair",
        Refused | LabelConflictsWithDerivation | InvalidProposal | OperatorConflict => "Refused",
        BudgetUnknown => "BudgetUnknown",
        LiftRequired => "RequiresLift",
        ParseRefused | NoPacket => "Refusal",
    }
}

fn ts_residual(s: Ts) -> &'static str {
    match s {
        ExactRuleDerived | UniqueOutputDerived => "Exact",
        NoRuleInSearchClass => "ClosedSurvivor",
        Refused | LabelConflictsWithDerivation | InvalidProposal | OperatorConflict | ParseRefused => "Refused",
        _ => "Open",
    }
}

fn ts_auth(s: Ts) -> &'static str {
    match s {
        ExactRuleDerived | UniqueOutputDerived => "Certifiable",
        Refused | LabelConflictsWithDerivation | InvalidProposal | OperatorConflict => "Refused",
        _ => "Uncertified",
    }
}

fn ts_authterm(s: Ts) -> bool {
    matches!(s, ExactRuleDerived | UniqueOutputDerived)
}

fn ts_from_name(name: &str) -> Option<Ts> {
    ALL_TS.iter().copied().find(|s| ts_name(*s) == name)
}

const PFP: [(&str, &str); 10] = [
    ("Exact", "CheckPassed"), ("Verified", "CheckPassed"), ("VerifiedWithResiduals", "CheckPassed"),
    ("StabilizedSurvivor", "RequiresLift"), ("NeedsExternalOracle", "RequiresLift"), ("OpenObstruction", "Refusal"),
    ("BlockedByEvidence", "Refusal"), ("InfrastructureFailure", "Refusal"), ("Refused", "Refused"),
    ("BudgetExhausted", "BudgetUnknown"),
];

const DIAG: [(&str, &str); 3] = [("ExactClass", "ExactRepair"), ("ClosedResidual", "StabilizedSurvivor"), ("ActiveClosureFailure", "OpenObstruction")];

fn pfp_route_of_tag(tag: &str) -> Option<&'static str> {
    PFP.iter().find(|(n, _)| *n == tag).map(|(_, r)| *r)
}

fn rel_status(in_profile: bool, contradicted: bool, supported: bool) -> &'static str {
    match (in_profile, contradicted, supported) {
        (false, _, _) => "outsideProfile",
        (true, true, _) => "refuted",
        (true, false, true) => "supported",
        (true, false, false) => "undetermined",
    }
}

/// `terminal_from_fiber`; `None` is an `Err`.
pub fn fiber_status(selected: bool, cand: i64, out: i64, exhaustive: bool, agr: &str, verifier: bool) -> Option<Ts> {
    if !selected {
        return if cand != 0 || out != 0 || exhaustive { None } else { Some(NoPacket) };
    }
    if !verifier {
        return Some(VerifierDisabled);
    }
    if cand > 0 && out == 0 {
        return None;
    }
    if out > cand {
        return None;
    }
    if cand == 0 {
        return Some(if exhaustive { NoRuleInSearchClass } else { SearchIncomplete });
    }
    if cand == 1 {
        return Some(ExactRuleDerived);
    }
    if out == 1 {
        let (coherent, replay) = match agr {
            "-" => (true, true),
            a => (a.as_bytes()[0] == b'1', a.as_bytes()[1] == b'1'),
        };
        if !coherent {
            return Some(PolicyAmbiguous);
        }
        if !replay {
            return Some(ReplayMismatch);
        }
        return Some(UniqueOutputDerived);
    }
    Some(NonUniqueOutput)
}

const AGREEMENTS: [&str; 5] = ["-", "00", "01", "10", "11"];

fn join_ints(xs: &[i64]) -> String {
    if xs.is_empty() { "-".to_string() } else { xs.iter().map(|x| x.to_string()).collect::<Vec<_>>().join(";") }
}

fn join_items(xs: &[String]) -> String {
    if xs.is_empty() { "-".to_string() } else { xs.join(";") }
}

fn all_fiber_inputs() -> Vec<(bool, i64, i64, bool, &'static str, bool)> {
    let mut v = Vec::new();
    for sel in [false, true] {
        for cand in 0..4 {
            for out in 0..4 {
                for exh in [false, true] {
                    for agr in AGREEMENTS {
                        for ver in [false, true] {
                            v.push((sel, cand, out, exh, agr, ver));
                        }
                    }
                }
            }
        }
    }
    v
}

fn determines(f: fn(Ts) -> &'static str, g: fn(Ts) -> &'static str) -> bool {
    let mut seen: BTreeMap<&str, &str> = BTreeMap::new();
    ALL_TS.iter().all(|s| *seen.entry(f(*s)).or_insert(g(*s)) == g(*s))
}

fn summary(name: &str) -> Option<(Vec<i64>, Vec<String>)> {
    match name {
        "residual_routing" => {
            let pairs: BTreeSet<String> = ALL_TS.iter().map(|s| format!("{}:{}", ts_residual(*s), ts_route(*s))).collect();
            Some((vec![28, pairs.len() as i64], pairs.into_iter().collect()))
        }
        "determination" => {
            let items = vec![
                format!("residual->route:{}", determines(ts_residual, ts_route) as i32),
                format!("route->residual:{}", determines(ts_route, ts_residual) as i32),
                format!("residual->auth:{}", determines(ts_residual, ts_auth) as i32),
                format!("auth->residual:{}", determines(ts_auth, ts_residual) as i32),
                format!("route->auth:{}", determines(ts_route, ts_auth) as i32),
                format!("auth->route:{}", determines(ts_auth, ts_route) as i32),
            ];
            Some((vec![], items))
        }
        "policies" => {
            let (mut total, mut injective, mut surjective) = (0i64, 0i64, 0i64);
            let mut pair01: BTreeSet<(usize, usize)> = BTreeSet::new();
            for a in 0..7usize {
                for b in 0..7usize {
                    for c in 0..7usize {
                        total += 1;
                        let distinct: BTreeSet<usize> = [a, b, c].into_iter().collect();
                        if distinct.len() == 3 {
                            injective += 1;
                        }
                        if distinct.len() == 7 {
                            surjective += 1;
                        }
                        pair01.insert((a, b));
                    }
                }
            }
            Some((vec![3, 7, total, injective, surjective, pair01.len() as i64, 3 * 7], vec![]))
        }
        "diag_cells" => {
            let routed: BTreeSet<String> =
                DIAG.iter().filter_map(|(d, t)| pfp_route_of_tag(t).map(|r| format!("{}:{}", d, r))).collect();
            let n = routed.len() as i64;
            Some((vec![21, n, 3 - n, 21 - n], routed.into_iter().collect()))
        }
        "fiber_routes" | "fiber_statuses" | "image_sizes" => {
            let mut errs = 0i64;
            let mut counts: BTreeMap<String, i64> = BTreeMap::new();
            let mut routes: BTreeSet<&str> = BTreeSet::new();
            let inputs = all_fiber_inputs();
            for (sel, cand, out, exh, agr, ver) in &inputs {
                match fiber_status(*sel, *cand, *out, *exh, agr, *ver) {
                    None => errs += 1,
                    Some(s) => {
                        *counts.entry(ts_name(s)).or_insert(0) += 1;
                        routes.insert(ts_route(s));
                    }
                }
            }
            if name == "fiber_routes" {
                Some((vec![inputs.len() as i64, errs, inputs.len() as i64 - errs, routes.len() as i64], routes.iter().map(|r| r.to_string()).collect()))
            } else if name == "fiber_statuses" {
                Some((vec![counts.len() as i64], counts.iter().map(|(k, v)| format!("{}:{}", k, v)).collect()))
            } else {
                let pfp_image: BTreeSet<&str> = PFP.iter().map(|(_, r)| *r).collect();
                let status_image: BTreeSet<&str> = ALL_TS.iter().map(|s| ts_route(*s)).collect();
                let mut rel_image: BTreeSet<&str> = BTreeSet::new();
                for i in [false, true] {
                    for c in [false, true] {
                        for s in [false, true] {
                            rel_image.insert(rel_status(i, c, s));
                        }
                    }
                }
                let mut missing: Vec<String> = Vec::new();
                for r in ROUTES {
                    if !pfp_image.contains(r) {
                        missing.push(format!("pfp-missing:{}", r));
                    }
                    if !routes.contains(r) {
                        missing.push(format!("fiber-missing:{}", r));
                    }
                }
                missing.sort();
                Some((vec![status_image.len() as i64, pfp_image.len() as i64, routes.len() as i64, rel_image.len() as i64], missing))
            }
        }
        "authority" => {
            let n = |t: &str| ALL_TS.iter().filter(|s| ts_auth(**s) == t).count() as i64;
            let terms = ALL_TS.iter().filter(|s| ts_authterm(**s)).count() as i64;
            // certified = witness && authority terminal; without a witness nothing is certified.
            let certified = |s: Ts, witness: bool| witness && ts_authterm(s);
            let without = ALL_TS.iter().filter(|s| certified(**s, false)).count() as i64;
            let with = ALL_TS.iter().filter(|s| certified(**s, true)).count() as i64;
            Some((vec![21, n("Certifiable"), n("Refused"), n("Uncertified"), terms, without, with], vec![]))
        }
        _ => None,
    }
}

fn bit(s: &str) -> Option<bool> {
    match s {
        "0" => Some(false),
        "1" => Some(true),
        _ => None,
    }
}

/// Replay one tab-separated public-input line; the wire line is byte-identical to the Python producer.
pub fn replay(input: &str) -> Option<String> {
    let f: Vec<&str> = input.split('\t').collect();
    match f[0] {
        "stat" if f.len() == 2 => {
            let i: usize = f[1].parse().ok()?;
            let s = *ALL_TS.get(i)?;
            Some(format!("stat\t{}\t{}\t{}\t{}\t{}\t{}", i, ts_name(s), ts_route(s), ts_residual(s), ts_auth(s), ts_authterm(s) as i32))
        }
        "pfp" if f.len() == 2 => {
            let i: usize = f[1].parse().ok()?;
            let (n, r) = PFP.get(i)?;
            Some(format!("pfp\t{}\t{}\t{}", i, n, r))
        }
        "diag" if f.len() == 2 => {
            let i: usize = f[1].parse().ok()?;
            let (n, tag) = DIAG.get(i)?;
            Some(format!("diag\t{}\t{}\t{}\t{}\t{}", i, n, tag, pfp_route_of_tag(tag).unwrap_or("-"), (i == 0) as i32))
        }
        "rel" if f.len() == 4 => {
            let (i, c, s) = (bit(f[1])?, bit(f[2])?, bit(f[3])?);
            Some(format!("rel\t{}\t{}\t{}\t{}", i as i32, c as i32, s as i32, rel_status(i, c, s)))
        }
        "fib" if f.len() == 7 => {
            let (sel, exh, ver) = (bit(f[1])?, bit(f[4])?, bit(f[6])?);
            let (cand, out): (i64, i64) = (f[2].parse().ok()?, f[3].parse().ok()?);
            let agr = *AGREEMENTS.iter().find(|a| **a == f[5])?;
            let (status, route) = match fiber_status(sel, cand, out, exh, agr, ver) {
                None => ("ERR".to_string(), "-"),
                Some(s) => (ts_name(s), ts_route(s)),
            };
            Some(format!("fib\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}", sel as i32, cand, out, exh as i32, agr, ver as i32, status, route))
        }
        "sum" if f.len() == 2 => {
            let (ints, items) = summary(f[1])?;
            Some(format!("sum\t{}\t{}\t{}", f[1], join_ints(&ints), join_items(&items)))
        }
        _ => None,
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn pfp_wdp_diagnostic_routing_all_seven_routes_reachable_from_statuses_only() {
        let routes: BTreeSet<&str> = ALL_TS.iter().map(|s| ts_route(*s)).collect();
        assert_eq!(routes.len(), 7);
        let pfp: BTreeSet<&str> = PFP.iter().map(|(_, r)| *r).collect();
        assert_eq!(pfp.len(), 5);
        assert!(!pfp.contains("Repair") && !pfp.contains("NoRule"));
    }

    #[test]
    fn pfp_wdp_diagnostic_routing_policies_none_forced_injective_exist_no_surjective() {
        let (ints, _) = summary("policies").unwrap();
        assert_eq!(ints, vec![3, 7, 343, 210, 0, 49, 21]);
    }

    #[test]
    fn pfp_wdp_diagnostic_routing_exact_class_has_no_declared_route() {
        assert_eq!(replay("diag\t0").unwrap(), "diag\t0\tExactClass\tExactRepair\t-\t1");
        assert_eq!(replay("diag\t1").unwrap(), "diag\t1\tClosedResidual\tStabilizedSurvivor\tRequiresLift\t0");
        assert_eq!(replay("diag\t2").unwrap(), "diag\t2\tActiveClosureFailure\tOpenObstruction\tRefusal\t0");
        assert_eq!(summary("diag_cells").unwrap().0, vec![21, 2, 1, 19]);
    }

    #[test]
    fn pfp_wdp_diagnostic_routing_residual_and_route_do_not_determine_each_other() {
        let (_, items) = summary("determination").unwrap();
        assert_eq!(items, vec!["residual->route:0", "route->residual:0", "residual->auth:0", "auth->residual:0", "route->auth:1", "auth->route:0"]);
        assert_eq!(summary("residual_routing").unwrap().0, vec![28, 8]);
    }

    #[test]
    fn pfp_wdp_diagnostic_routing_fiber_reaches_four_routes() {
        let (ints, items) = summary("fiber_routes").unwrap();
        assert_eq!(ints, vec![640, 400, 240, 4]);
        assert_eq!(items, vec!["CheckPassed", "NoRule", "Refusal", "Repair"]);
    }

    #[test]
    fn pfp_wdp_diagnostic_routing_authority_never_certified_without_witness() {
        assert_eq!(summary("authority").unwrap().0, vec![21, 2, 4, 15, 2, 0, 2]);
        assert_eq!(replay("rel\t1\t1\t0").unwrap(), "rel\t1\t1\t0\trefuted");
        assert_eq!(replay("rel\t0\t1\t1").unwrap(), "rel\t0\t1\t1\toutsideProfile");
    }

    #[test]
    fn pfp_wdp_diagnostic_routing_replay_rejects_malformed_lines() {
        assert!(replay("stat\t21").is_none());
        assert!(replay("stat").is_none());
        assert!(replay("fib\t1\t1\t1\t1\t22\t1").is_none());
        assert!(replay("fib\t2\t1\t1\t1\t-\t1").is_none());
        assert!(replay("sum\tnothing").is_none());
        assert!(replay("diag\t3").is_none());
        assert_eq!(replay("fib\t1\t2\t1\t0\t01\t1").unwrap(), "fib\t1\t2\t1\t0\t01\t1\tPolicyAmbiguous\tRepair");
        assert_eq!(replay("fib\t1\t0\t1\t0\t-\t1").unwrap(), "fib\t1\t0\t1\t0\t-\t1\tERR\t-");
    }
}
