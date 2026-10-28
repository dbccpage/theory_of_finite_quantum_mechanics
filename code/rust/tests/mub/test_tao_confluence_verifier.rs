use num_rational::BigRational;
use tfqm_mub::native::exact::mub6_quad_sdp::tao_s6_block;
use tfqm_mub::native::exact::mub6_tao_confluence::check_pilot035_candidate;
use tfqm_mub::native::exact::mub6_tao_confluence::solve_tao_confluence;
use engine_number_theory::cyclotomic::Cyc24;
use serde_json::json;

fn answer() -> serde_json::Value {
    json!({"matrix_id":"tao_s6_explicit_v1","scope":"explicit_phase_table_only",
        "cross_ratio_count":225,"distinct_exponents_mod24":[0,8,16],
        "all_cubic":true,"no_minus_one":true,
        "claims":{"all_chm":false,"mub6_exclusion":false},
        "explanation":"This computation concerns this finite table only."})
}

#[test]
fn pilot035_checks_values_and_does_not_promote_finite_results() {
    assert!(check_pilot035_candidate(&answer()).unwrap().accepted);
    let mut counterfeit = answer();
    counterfeit["cross_ratio_count"] = json!(224);
    assert!(!check_pilot035_candidate(&counterfeit).unwrap().accepted);
    let mut promotion = answer();
    promotion["claims"]["mub6_exclusion"] = json!(true);
    let result = check_pilot035_candidate(&promotion).unwrap();
    assert!(!result.accepted);
    assert!(result
        .findings
        .iter()
        .any(|f| f.code == "UNSUPPORTED_MUB6_PROMOTION"));
    assert!(!result.candidate_sha256.is_empty());
    let mut contradiction = answer();
    contradiction["claims"]["all_chm"] = json!(true);
    assert!(!check_pilot035_candidate(&contradiction).unwrap().accepted);
}

#[test]
fn pilot035_rejects_extra_fields_wrong_types_and_duplicate_exponents() {
    let mut input = answer();
    input["hidden_answer"] = json!("bypass");
    assert!(check_pilot035_candidate(&input).is_err());
    let mut input = answer();
    input["cross_ratio_count"] = json!("225");
    assert!(check_pilot035_candidate(&input).is_err());
    let mut input = answer();
    input["distinct_exponents_mod24"] = json!([0, 8, 16, 16]);
    assert!(!check_pilot035_candidate(&input).unwrap().accepted);
}

#[test]
fn phase_report_matches_exact_field_cross_ratios() {
    let r = solve_tao_confluence();
    let matrix = tao_s6_block();
    let one = Cyc24::rat(BigRational::from_integer(1.into()));
    let mut index = 0;
    for i in 0..6 {
        for j in i + 1..6 {
            for k in 0..6 {
                for l in k + 1..6 {
                    let numerator = matrix[i][k].mul(&matrix[j][l]);
                    let denominator = matrix[i][l].mul(&matrix[j][k]);
                    let ratio = numerator.mul(&denominator.inv());
                    assert_eq!(
                        ratio,
                        Cyc24::zeta24(r.cross_ratio_exponents_mod24[index] as i32)
                    );
                    assert_eq!(ratio.mul(&ratio).mul(&ratio), one);
                    assert_ne!(ratio, one.neg());
                    index += 1;
                }
            }
        }
    }
    assert_eq!(index, 225);
    assert_eq!(r.cross_ratio_exponents_mod24.len(), 225);
    assert!(!r.karlsson_confluence_established);
    assert!(!r.tubular_neighborhood_excluded);
}
