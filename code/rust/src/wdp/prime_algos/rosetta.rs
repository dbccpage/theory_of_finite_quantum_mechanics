
use crate::prime_algos::prime_algorithm_0::{
    run_prime_algorithm_0, DefectBranch, DomainAdapter, EvidenceProvenance, PrimeAlgorithm0Receipt,
    PrimeDomain, PrimeTerminal,
};
use crate::ddc::dda_alphabet::DdaOp;
use omega_types::authority::AuthorityEffect;
use serde::Serialize;
use std::collections::{BTreeMap, BTreeSet};

#[derive(Debug, Clone, PartialEq, Eq, Serialize)]
pub struct DomainTapeSummary {
    pub domain: String,
    pub residual_family_label: String,
    pub letter_tape: String,
    pub letter_histogram: BTreeMap<String, usize>,
    pub branch: String,
    pub terminal: String,
    pub phi1: Option<u64>,
    pub gamma2: Option<u64>,
    pub authority_effect: String,
    pub provenance: EvidenceProvenance,
}

impl DomainTapeSummary {
    pub fn from_receipt(r: &PrimeAlgorithm0Receipt) -> Self {
        let mut hist: BTreeMap<String, usize> = BTreeMap::new();
        for ch in r.letter_tape.chars() {
            *hist.entry(ch.to_string()).or_insert(0) += 1;
        }
        Self {
            domain: r.domain.as_str().to_string(),
            residual_family_label: r.residual_family_label.clone(),
            letter_tape: r.letter_tape.clone(),
            letter_histogram: hist,
            branch: r.branch.as_str().to_string(),
            terminal: r.terminal.as_str().to_string(),
            phi1: r.phi1,
            gamma2: r.gamma2,
            authority_effect: format!("{:?}", r.authority_effect),
            provenance: r.evidence_provenance,
        }
    }
}

#[derive(Debug, Clone, PartialEq, Eq, Serialize)]
pub enum RosterProvenance {
    AllFixtureDriven,
    Mixed { verifier_produced: Vec<String> },
    AllVerifierProduced,
}

#[derive(Debug, Clone, PartialEq, Eq, Serialize)]
pub struct RosettaReport {
    pub provenance: RosterProvenance,
    pub domains: Vec<DomainTapeSummary>,
    pub shared_required_letters: bool,
    pub alphabet_closed: bool,
    pub authority_all_none: bool,
    pub phi_gamma_separated: bool,
    pub literature_always_after_terminal: bool,
    pub branch_histogram: BTreeMap<String, usize>,
    pub terminal_histogram: BTreeMap<String, usize>,
    pub residual_family_count: usize,
    pub residual_families: Vec<String>,
    pub pairwise_letter_jaccard_x1000: BTreeMap<String, u64>,
    pub no_decidable_letter_law_violation: bool,
    pub letter_law_violations: BTreeMap<String, Vec<String>>,
    pub rosetta_smoke_pass: bool,
}

fn alphabet_letters() -> BTreeSet<char> {
    DdaOp::alphabet()
        .iter()
        .flat_map(|o| o.letter().chars())
        .collect()
}

pub fn rosetta_from_receipts(receipts: &[PrimeAlgorithm0Receipt]) -> RosettaReport {
    let allowed = alphabet_letters();
    let domains: Vec<DomainTapeSummary> = receipts
        .iter()
        .map(DomainTapeSummary::from_receipt)
        .collect();

    let shared_required_letters = domains.iter().all(|d| {
        d.letter_tape.contains('C') && d.letter_tape.contains('R') && d.letter_tape.contains('T')
    });

    let alphabet_closed = domains.iter().all(|d| {
        d.letter_tape.chars().all(|c| {
            allowed.contains(&c) || "Λ".contains(c)
        })
    });

    let authority_all_none = receipts
        .iter()
        .all(|r| r.authority_effect == AuthorityEffect::None);

    let phi_gamma_separated = receipts.iter().any(|r| match (r.phi1, r.gamma2) {
        (Some(p), Some(g)) => p != g,
        (Some(_), None) | (None, Some(_)) => true,
        (None, None) => false,
    });

    let literature_always_after_terminal = receipts.iter().all(|r| {
        let first_t = r.steps.iter().position(|s| s.op == "T");
        match first_t {
            None => r.steps.iter().all(|s| s.prime_step != 12),
            Some(i) => r.steps[..i].iter().all(|s| s.prime_step != 12),
        }
    });

    let mut branch_histogram: BTreeMap<String, usize> = BTreeMap::new();
    let mut terminal_histogram: BTreeMap<String, usize> = BTreeMap::new();
    for d in &domains {
        *branch_histogram.entry(d.branch.clone()).or_insert(0) += 1;
        *terminal_histogram.entry(d.terminal.clone()).or_insert(0) += 1;
    }

    let mut families: BTreeSet<String> = BTreeSet::new();
    for d in &domains {
        families.insert(d.residual_family_label.clone());
    }
    let residual_families: Vec<String> = families.iter().cloned().collect();

    let mut pairwise: BTreeMap<String, u64> = BTreeMap::new();
    for i in 0..domains.len() {
        for j in (i + 1)..domains.len() {
            let a: BTreeSet<char> = domains[i].letter_tape.chars().collect();
            let b: BTreeSet<char> = domains[j].letter_tape.chars().collect();
            let inter = a.intersection(&b).count() as u64;
            let union = a.union(&b).count() as u64;
            let jacc = (inter * 1000).checked_div(union).unwrap_or(0);
            let key = format!("{}|{}", domains[i].domain, domains[j].domain);
            pairwise.insert(key, jacc);
        }
    }

    let letter_law_violations: BTreeMap<String, Vec<String>> = receipts
        .iter()
        .filter_map(|r| {
            let c = crate::prime_algos::prime_algorithm_0_conformance::check_receipt(r);
            let v = c.violations();
            if v.is_empty() {
                None
            } else {
                Some((
                    r.domain.as_str().to_string(),
                    v.iter().map(|x| format!("{x:?}")).collect(),
                ))
            }
        })
        .collect();
    let no_decidable_letter_law_violation = letter_law_violations.is_empty();

    let rosetta_smoke_pass = shared_required_letters
        && alphabet_closed
        && authority_all_none
        && phi_gamma_separated
        && literature_always_after_terminal
        && no_decidable_letter_law_violation
        && !domains.is_empty();

    let verifier_produced: Vec<String> = receipts
        .iter()
        .filter(|r| r.evidence_provenance == EvidenceProvenance::VerifierProduced)
        .map(|r| r.domain.as_str().to_string())
        .collect();
    let provenance = if verifier_produced.is_empty() {
        RosterProvenance::AllFixtureDriven
    } else if verifier_produced.len() == receipts.len() {
        RosterProvenance::AllVerifierProduced
    } else {
        RosterProvenance::Mixed { verifier_produced }
    };

    RosettaReport {
        provenance,
        domains,
        shared_required_letters,
        alphabet_closed,
        authority_all_none,
        phi_gamma_separated,
        literature_always_after_terminal,
        branch_histogram,
        terminal_histogram,
        residual_family_count: residual_families.len(),
        residual_families,
        pairwise_letter_jaccard_x1000: pairwise,
        no_decidable_letter_law_violation,
        letter_law_violations,
        rosetta_smoke_pass,
    }
}

pub fn rosetta_run(adapters: &[&dyn DomainAdapter]) -> RosettaReport {
    let receipts: Vec<PrimeAlgorithm0Receipt> =
        adapters.iter().map(|a| run_prime_algorithm_0(*a)).collect();
    rosetta_from_receipts(&receipts)
}

pub fn rosetta_builtin_roster() -> RosettaReport {
    rosetta_from_receipts(&builtin_receipts())
}

pub fn builtin_receipts() -> Vec<PrimeAlgorithm0Receipt> {
    use crate::prime_algos::domain_adapters::{
        CodaResidualAdapter, FspChannelAAdapter, GenericMss0Adapter,
        MubWallAdapter, SymbolGameExpressivityAdapter,
    };
    let g = GenericMss0Adapter;
    let m = MubWallAdapter;
    let f = FspChannelAAdapter;
    let c = CodaResidualAdapter;
    let s = SymbolGameExpressivityAdapter::default();
    let adapters: [&dyn DomainAdapter; 5] = [&g, &m, &f, &c, &s];
    adapters.iter().map(|a| run_prime_algorithm_0(*a)).collect()
}

#[derive(Debug, Clone, PartialEq, Eq, Serialize)]
pub struct ResidualFamilyStat {
    pub domain: PrimeDomain,
    pub family: String,
    pub branch: DefectBranch,
    pub terminal: PrimeTerminal,
    pub phi1: Option<u64>,
    pub gamma2: Option<u64>,
    pub letter_tape: String,
}

pub fn residual_family_table(receipts: &[PrimeAlgorithm0Receipt]) -> Vec<ResidualFamilyStat> {
    receipts
        .iter()
        .map(|r| ResidualFamilyStat {
            domain: r.domain,
            family: r.residual_family_label.clone(),
            branch: r.branch,
            terminal: r.terminal,
            phi1: r.phi1,
            gamma2: r.gamma2,
            letter_tape: r.letter_tape.clone(),
        })
        .collect()
}

#[cfg(test)]
mod tests {
    use super::*;
    use crate::prime_algos::domain_adapters::{
        CodaResidualAdapter, FspChannelAAdapter, GenericMss0Adapter, MubWallAdapter,
        SymbolGameExpressivityAdapter,
    };

    #[test]
    fn rosetta_builtin_roster_reports_measurable_structure() {
        let report = rosetta_builtin_roster();

        assert_eq!(report.domains.len(), 5);
        assert!(report.residual_family_count >= 4);
        assert!(report.authority_all_none);
        assert!(report.alphabet_closed);
        assert!(report.literature_always_after_terminal);

        assert!(
            !report.shared_required_letters,
            "a refusing domain cannot emit R; if this passes, refusals stopped              being terminal again"
        );
        let mub = report
            .domains
            .iter()
            .find(|d| d.domain == "mub")
            .expect("mub in roster");
        assert_eq!(mub.terminal, "Refusal");
        assert!(!mub.letter_tape.contains('R'));
    }

    #[test]
    fn smoke_verdict_sees_the_fsp_t_law_violation() {
        let report = rosetta_builtin_roster();

        assert!(
            !report.no_decidable_letter_law_violation,
            "expected FSP's T-law violation to be visible"
        );
        assert!(
            report.letter_law_violations.contains_key("fsp"),
            "violations recorded: {:?}",
            report.letter_law_violations
        );
        assert!(
            !report.rosetta_smoke_pass,
            "smoke must not pass while a domain terminalises an open residual"
        );
    }

    #[test]
    fn residual_family_table_has_distinct_labels() {
        let receipts = [
            run_prime_algorithm_0(&GenericMss0Adapter),
            run_prime_algorithm_0(&MubWallAdapter),
            run_prime_algorithm_0(&FspChannelAAdapter),
            run_prime_algorithm_0(&CodaResidualAdapter),
            run_prime_algorithm_0(&SymbolGameExpressivityAdapter::default()),
        ];
        let table = residual_family_table(&receipts);
        let labels: BTreeSet<_> = table.iter().map(|r| r.family.as_str()).collect();
        assert!(labels.len() >= 4);
        assert!(table.iter().any(|r| r.branch == DefectBranch::Open));
        assert!(table
            .iter()
            .any(|r| r.branch == DefectBranch::StabilizedSurvivor));
    }

    #[test]
    fn pairwise_jaccard_recorded() {
        let report = rosetta_run(&[&GenericMss0Adapter, &CodaResidualAdapter]);
        assert!(report
            .pairwise_letter_jaccard_x1000
            .contains_key("generic|coda"));
        let j = report.pairwise_letter_jaccard_x1000["generic|coda"];
        assert!(j > 0, "expected some shared letters");
    }

    #[test]
    fn roster_provenance_is_fixture_driven() {
        let report = rosetta_builtin_roster();
        match &report.provenance {
            RosterProvenance::AllFixtureDriven => {}
            other => panic!("expected AllFixtureDriven, got {other:?}"),
        }
        for d in &report.domains {
            assert_eq!(
                d.provenance,
                EvidenceProvenance::FixtureDrivenStructuralDemo,
                "{} claims verifier-produced masses it does not have",
                d.domain
            );
        }
    }
}
