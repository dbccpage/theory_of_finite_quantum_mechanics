
use serde::{Deserialize, Serialize};

#[derive(Debug, Clone, Serialize, Deserialize, PartialEq, Eq)]
pub struct ConductorCancellationClassification {
    pub conductor: usize,
    pub all_minimal_sums_pairable: bool,
    pub unpairable_minimal_length: Option<usize>,
    pub cancellation_family: String,
    pub mechanism: String,
}

pub fn classify_conductor_cancellations(
    conductor: usize,
) -> Result<
    ConductorCancellationClassification,
    engine_number_theory::vanishing_sums::VanishingLengthError,
> {
    let polygon = engine_number_theory::vanishing_sums::minimal_unpairable_polygon(
        conductor as u64,
        engine_number_theory::integer_factorization::FactorizationBudget::default(),
    )?;
    Ok(match polygon.map(|p| p as usize) {
        None => ConductorCancellationClassification {
            conductor,
            all_minimal_sums_pairable: true,
            unpairable_minimal_length: None,
            cancellation_family: "pairable".to_string(),
            mechanism: if conductor <= 1 {
                "identity".to_string()
            } else {
                "pairwise_reflection_involution".to_string()
            },
        },
        Some(p_odd) => ConductorCancellationClassification {
            conductor,
            all_minimal_sums_pairable: false,
            unpairable_minimal_length: Some(p_odd),
            cancellation_family: "prime".to_string(),
            mechanism: format!("irreducible_cyclic_vortex_order_{}", p_odd),
        },
    })
}

pub const TARGET_CONDUCTOR_MAP: [(usize, usize); 22] = [
    (1, 1),
    (2, 12),
    (3, 1),
    (4, 1),
    (5, 1),
    (6, 1),
    (7, 2),
    (8, 1),
    (9, 1),
    (10, 4),
    (11, 4),
    (12, 1),
    (13, 5),
    (14, 1),
    (15, 8),
    (16, 2),
    (17, 8),
    (18, 2),
    (19, 1),
    (20, 1),
    (21, 4),
    (22, 3),
];

#[derive(Debug, Clone, Serialize, Deserialize, PartialEq, Eq)]
pub struct CancellationCensusItem {
    pub target_id: usize,
    pub conductor: usize,
    pub is_unpairable: bool,
    pub unpairable_minimal_length: Option<usize>,
    pub cancellation_family: String,
}

#[derive(Debug, Clone, Serialize, Deserialize, PartialEq, Eq)]
pub struct CancellationCensusReport {
    pub targets_censused_count: usize,
    pub targets_with_unpairable_cancellation_count: usize,
    pub targets_with_unpairable_cancellation_ids: Vec<usize>,
    pub first_unpairable_length: usize,
    pub target_census: Vec<CancellationCensusItem>,
}

pub fn audit_target_cancellations() -> CancellationCensusReport {
    let mut census = Vec::with_capacity(22);
    let mut unpairable_ids = Vec::new();

    for &(tid, cond) in &TARGET_CONDUCTOR_MAP {
        let info = classify_conductor_cancellations(cond).expect("fixed positive conductor");
        let is_unpairable = !info.all_minimal_sums_pairable;
        if is_unpairable {
            unpairable_ids.push(tid);
        }
        census.push(CancellationCensusItem {
            target_id: tid,
            conductor: cond,
            is_unpairable,
            unpairable_minimal_length: info.unpairable_minimal_length,
            cancellation_family: info.cancellation_family,
        });
    }

    let unpairable_count = unpairable_ids.len();
    let first_unpairable_len = census
        .iter()
        .filter(|t| t.is_unpairable)
        .filter_map(|t| t.unpairable_minimal_length)
        .min()
        .unwrap_or(0);

    CancellationCensusReport {
        targets_censused_count: 22,
        targets_with_unpairable_cancellation_count: unpairable_count,
        targets_with_unpairable_cancellation_ids: unpairable_ids,
        first_unpairable_length: first_unpairable_len,
        target_census: census,
    }
}

#[derive(Debug, Clone, Serialize, Deserialize, PartialEq, Eq)]
pub struct SorkinI3CancellationReport {
    pub target_id: usize,
    pub interference_term: String,
    pub vanishing_identity: String,
    pub sum_length: usize,
    pub cancellation_type: String,
    pub is_pairable: Option<bool>,
    pub conductor: usize,
    pub parity_obstruction: String,
    pub i3_identically_zero: bool,
}

pub fn evaluate_sorkin_i3_cancellation() -> SorkinI3CancellationReport {
    let t3 = crate::qm::campaigns::foundational_targets::verify_target3_sorkin_interference();
    SorkinI3CancellationReport {
        target_id: 3,
        interference_term: "I_3".to_string(),
        vanishing_identity: "quadratic inclusion-exclusion for three amplitudes".to_string(),
        sum_length: 7,
        cancellation_type: "quadratic_inclusion_exclusion".to_string(),
        is_pairable: None,
        conductor: 1,
        parity_obstruction: "not applicable to intensity inclusion-exclusion".to_string(),
        i3_identically_zero: t3.sorkin_i3_identically_zero,
    }
}

#[derive(Debug, Clone, Serialize, Deserialize, PartialEq, Eq)]
pub struct EstateCertificateCorrespondence {
    pub estate_theorem: String,
    pub pairing_correspondence: String,
    pub prime_correspondence: String,
    pub estate_certificate_link_recorded: bool,
}

pub fn record_estate_certificate_correspondence() -> EstateCertificateCorrespondence {
    EstateCertificateCorrespondence {
        estate_theorem: "SignRepair.certificate_iff_dominated".to_string(),
        pairing_correspondence: "A pairing certificate corresponds to per-magnitude domination with magnitudes in {1}, where phase interference is resolved by pairwise involution.".to_string(),
        prime_correspondence: "Odd-prime vanishing sums (such as 1 + zeta_3 + zeta_3^2 = 0) are the finite-QM instances of certificate refusal at odd part counts (starting at part count 3), linking destructive interference directly to irreducible cyclic flux vortices.".to_string(),
        estate_certificate_link_recorded: true,
    }
}

#[derive(Debug, Clone, Serialize, Deserialize, PartialEq, Eq)]
pub struct Block08CancellationReport {
    pub authority_effect: String,
    pub citation: String,
    pub campaign: String,
    pub block_id: String,
    pub two_power_conductor_cancellations_all_pairable: bool,
    pub targets_with_unpairable_cancellation_count: usize,
    pub targets_with_unpairable_cancellation_ids: Vec<usize>,
    pub first_unpairable_length: usize,
    pub sorkin_i3_cancellation_type_target3: String,
    pub estate_certificate_link_recorded: bool,
    pub census_details: CancellationCensusReport,
    pub sorkin_evaluation: SorkinI3CancellationReport,
    pub estate_link: EstateCertificateCorrespondence,
}

pub fn run_block_08_execution() -> Block08CancellationReport {
    let census = audit_target_cancellations();
    let sorkin = evaluate_sorkin_i3_cancellation();
    let estate = record_estate_certificate_correspondence();

    let two_power_conductors = [2, 4, 8, 16, 32, 64, 128];
    let two_power_all_pairable = two_power_conductors.iter().all(|&c| {
        classify_conductor_cancellations(c)
            .expect("fixed positive conductor")
            .all_minimal_sums_pairable
    });

    Block08CancellationReport {
        authority_effect: "None".to_string(),
        citation: "sealed-derivation-v1 (3100c4e)".to_string(),
        campaign: "C250".to_string(),
        block_id: "block_08".to_string(),
        two_power_conductor_cancellations_all_pairable: two_power_all_pairable,
        targets_with_unpairable_cancellation_count: census
            .targets_with_unpairable_cancellation_count,
        targets_with_unpairable_cancellation_ids: census
            .targets_with_unpairable_cancellation_ids
            .clone(),
        first_unpairable_length: census.first_unpairable_length,
        sorkin_i3_cancellation_type_target3: sorkin.cancellation_type.clone(),
        estate_certificate_link_recorded: estate.estate_certificate_link_recorded,
        census_details: census,
        sorkin_evaluation: sorkin,
        estate_link: estate,
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_two_power_conductors_pairable() {
        for &cond in &[1, 2, 4, 8, 16, 32, 64, 128] {
            let res = classify_conductor_cancellations(cond).expect("fixed positive conductor");
            assert!(res.all_minimal_sums_pairable);
            assert_eq!(res.cancellation_family, "pairable");
            assert_eq!(res.unpairable_minimal_length, None);
        }
    }

    #[test]
    fn test_odd_prime_conductors() {
        let res3 = classify_conductor_cancellations(3).unwrap();
        assert!(!res3.all_minimal_sums_pairable);
        assert_eq!(res3.unpairable_minimal_length, Some(3));
        assert_eq!(res3.cancellation_family, "prime");

        let res5 = classify_conductor_cancellations(5).unwrap();
        assert!(!res5.all_minimal_sums_pairable);
        assert_eq!(res5.unpairable_minimal_length, Some(5));

        let res12 = classify_conductor_cancellations(12).unwrap();
        assert!(!res12.all_minimal_sums_pairable);
        assert_eq!(res12.unpairable_minimal_length, Some(3));
    }

    #[test]
    fn test_target_census_properties() {
        let census = audit_target_cancellations();
        assert_eq!(census.targets_censused_count, 22);
        assert_eq!(census.targets_with_unpairable_cancellation_count, 3);
        assert_eq!(
            census.targets_with_unpairable_cancellation_ids,
            vec![2, 13, 22]
        );
        assert_eq!(census.first_unpairable_length, 3);
    }

    #[test]
    fn test_sorkin_i3_report() {
        let rep = evaluate_sorkin_i3_cancellation();
        assert_eq!(rep.target_id, 3);
        assert_eq!(rep.cancellation_type, "quadratic_inclusion_exclusion");
        assert_eq!(rep.sum_length, 7);
        assert_eq!(rep.is_pairable, None);
        assert_eq!(rep.conductor, 1);
    }

    #[test]
    fn test_estate_link() {
        let link = record_estate_certificate_correspondence();
        assert!(link.estate_certificate_link_recorded);
    }

    #[test]
    fn test_run_block_08_execution() {
        let rep = run_block_08_execution();
        assert_eq!(rep.authority_effect, "None");
        assert_eq!(rep.block_id, "block_08");
        assert!(rep.two_power_conductor_cancellations_all_pairable);
        assert_eq!(rep.targets_with_unpairable_cancellation_count, 3);
        assert_eq!(
            rep.targets_with_unpairable_cancellation_ids,
            vec![2, 13, 22]
        );
        assert_eq!(rep.first_unpairable_length, 3);
        assert_eq!(
            rep.sorkin_i3_cancellation_type_target3,
            "quadratic_inclusion_exclusion"
        );
        assert!(rep.estate_certificate_link_recorded);
    }
}
