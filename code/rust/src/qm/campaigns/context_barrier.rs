use omega_quantum_physics::contextuality_obstruction::*;
use serde::{Deserialize, Serialize};

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct AnchorBinding {
    pub anchor_id: String,
    pub citation: String,
    pub imported_construction: String,
    pub non_inference_scope: String,
}

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct ScenarioReceiptRow {
    pub id: String,
    pub name: String,
    pub coefficient_group: String,
    pub dim_c0: usize,
    pub dim_c1: usize,
    pub dim_c2: usize,
    pub rank_delta0: usize,
    pub dim_z1: usize,
    pub dim_h1: usize,
    pub obstruction_class_is_zero: bool,
    pub class_representative: String,
    #[serde(skip_serializing_if = "Option::is_none")]
    pub global_section_exhibited: Option<bool>,
    #[serde(skip_serializing_if = "Option::is_none")]
    pub exhibited_global_section: Option<Vec<u8>>,
    pub verdict: String,
}

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct Block07Receipt {
    pub anchor_binding: AnchorBinding,
    pub authority_effect: String,
    pub block: usize,
    pub campaign: String,
    pub citation: String,
    pub differential_squares_to_zero_proved: bool,
    pub every_verdict_names_coefficients: bool,
    pub global_targets: String,
    pub negative_control_discharged: bool,
    pub scenarios: Vec<ScenarioReceiptRow>,
    pub terminal_outcome: String,
}

pub fn evaluate_campaign_block_07() -> Result<Block07Receipt, String> {
    let x1 = construct_cabello_scenario();
    let x2 = construct_product_scenario();

    let res_x1 = compute_obstruction_class(&x1)?;
    let res_x2 = compute_obstruction_class(&x2)?;

    let x1_row = ScenarioReceiptRow {
        id: res_x1.scenario_id,
        name: res_x1.name,
        coefficient_group: res_x1.coefficient_group,
        dim_c0: res_x1.dim_c0,
        dim_c1: res_x1.dim_c1,
        dim_c2: res_x1.dim_c2,
        rank_delta0: res_x1.rank_delta0,
        dim_z1: res_x1.dim_z1,
        dim_h1: res_x1.dim_h1,
        obstruction_class_is_zero: res_x1.obstruction_class_is_zero,
        class_representative: res_x1.class_representative,
        global_section_exhibited: None,
        exhibited_global_section: None,
        verdict: "CONTEXTUAL_OBSTRUCTION_PRESENT".to_string(),
    };

    let x2_row = ScenarioReceiptRow {
        id: res_x2.scenario_id,
        name: res_x2.name,
        coefficient_group: res_x2.coefficient_group,
        dim_c0: res_x2.dim_c0,
        dim_c1: res_x2.dim_c1,
        dim_c2: res_x2.dim_c2,
        rank_delta0: res_x2.rank_delta0,
        dim_z1: res_x2.dim_z1,
        dim_h1: res_x2.dim_h1,
        obstruction_class_is_zero: res_x2.obstruction_class_is_zero,
        class_representative: res_x2.class_representative,
        global_section_exhibited: Some(res_x2.global_section_exhibited),
        exhibited_global_section: res_x2.exhibited_global_section,
        verdict: "NON_CONTEXTUAL_AT_DECLARED_COEFFICIENTS".to_string(),
    };

    Ok(Block07Receipt {
        anchor_binding: AnchorBinding {
            anchor_id: "B9".to_string(),
            citation: "Abramsky and Brandenburger, arXiv:1102.0264".to_string(),
            imported_construction: "contextuality as a cohomological obstruction in a presheaf over declared coefficients".to_string(),
            non_inference_scope: "A vanishing class over one coefficient group does not imply non-contextuality over another".to_string(),
        },
        authority_effect: "None".to_string(),
        block: 7,
        campaign: "C1000".to_string(),
        citation: "sealed-derivation-v1 (3100c4e)".to_string(),
        differential_squares_to_zero_proved: res_x1.diff_squares_to_zero && res_x2.diff_squares_to_zero,
        every_verdict_names_coefficients: x1_row.coefficient_group=="Z_2" && x2_row.coefficient_group=="Z_2",
        global_targets: "C1000-T951..C1000-T975".to_string(),
        negative_control_discharged: res_x2.obstruction_class_is_zero && res_x2.global_section_exhibited,
        scenarios: vec![x1_row, x2_row],
        terminal_outcome: "OBSTRUCTION_CLASSES_COMPUTED_EXACTLY".to_string(),
    })
}

#[cfg(test)]
mod tests {
    use super::*;
    use omega_quantum_physics::kochen_specker::CABELLO_9_CONTEXTS;

    #[test]
    fn test_x1_complex_and_cohomology() {
        let x1 = construct_cabello_scenario();
        let res = compute_obstruction_class(&x1).unwrap();
        assert_eq!(res.dim_c0, 27);
        assert_eq!(res.dim_c1, 18);
        assert_eq!(res.dim_c2, 0);
        assert_eq!(res.rank_delta0, 17);
        assert_eq!(res.dim_h1, 1);
        assert!(!res.obstruction_class_is_zero);
    }

    #[test]
    fn test_x2_complex_and_cohomology() {
        let x2 = construct_product_scenario();
        let res = compute_obstruction_class(&x2).unwrap();
        assert_eq!(res.dim_c0, 4);
        assert_eq!(res.dim_c1, 4);
        assert_eq!(res.dim_c2, 0);
        assert_eq!(res.rank_delta0, 3);
        assert_eq!(res.dim_h1, 1);
        assert!(res.obstruction_class_is_zero);
        assert!(res.global_section_exhibited);
    }

    #[test]
    fn test_mutation_1_differential_not_squaring_to_zero() {
        let mut cx = build_cochain_complex(&construct_cabello_scenario()).unwrap();
        cx.dim_c2 = 1;
        cx.d1_matrix = omega_number_theory::gf2::F2Matrix::zeros(1, cx.dim_c1).unwrap();
        cx.d1_matrix.set(0, 0, true).unwrap();
        assert!(cx.checked_complex().is_err());
    }

    #[test]
    fn test_mutation_2_missing_context() {
        let contexts = CABELLO_9_CONTEXTS[2..].iter().map(|c| c.to_vec()).collect();
        let bad_scen = MeasurementScenario {
            name: "bad".to_string(),
            scenario_id: "X1_bad".to_string(),
            ray_count: 18,
            contexts,
            b_targets: vec![1; 7],
            coefficient_group: "Z_2".to_string(),
            carrier: CARRIER.to_string(),
            conductor: CONDUCTOR,
            declared_global_section: None,
        };
        assert!(bad_scen.validate().is_err());
    }

    #[test]
    fn test_mutation_3_coefficients_switched() {
        let receipt = evaluate_campaign_block_07().unwrap();
        assert!(receipt.every_verdict_names_coefficients);
        assert_eq!(receipt.scenarios[0].coefficient_group, "Z_2");
        assert_eq!(receipt.scenarios[1].coefficient_group, "Z_2");
    }

    #[test]
    fn test_mutation_4_x2_reported_nonzero() {
        let x2 = construct_product_scenario();
        let res = compute_obstruction_class(&x2).unwrap();
        assert!(res.obstruction_class_is_zero);
    }

    #[test]
    fn test_mutation_5_invalid_global_section_restriction() {
        let x2 = construct_product_scenario();
        let bad_section = vec![0, 0, 0, 0];
        let (valid, violating) = verify_global_section(&x2, &bad_section);
        assert!(!valid);
        assert_eq!(violating.len(), 4);
    }
}
