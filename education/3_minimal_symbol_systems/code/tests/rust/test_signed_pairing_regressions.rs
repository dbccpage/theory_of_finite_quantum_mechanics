use mssn_stage_024::finite_algebra::{verify_bqnf_involution_pairing, SignedPathConfiguration};
use num_rational::Rational64;
use std::collections::BTreeMap;

fn pair(sign: i8) -> Vec<SignedPathConfiguration> {
    vec![
        SignedPathConfiguration { config_id: 1, action: Rational64::new(1, 1), fermion_sign: sign, mode_postings: vec![] },
        SignedPathConfiguration { config_id: 2, action: Rational64::new(1, 1), fermion_sign: -sign, mode_postings: vec![] },
    ]
}

#[test]
fn cancelling_pair_has_zero_average_sign() {
    let receipt = verify_bqnf_involution_pairing(&pair(1), &BTreeMap::from([(1,2),(2,1)])).unwrap();
    assert_eq!(receipt.average_sign, Rational64::new(0,1));
}

#[test]
fn non_sign_values_are_refused() {
    assert!(verify_bqnf_involution_pairing(&pair(0), &BTreeMap::from([(1,2),(2,1)])).is_err());
}

#[test]
fn duplicate_configuration_ids_are_refused() {
    let mut configurations = pair(1);
    configurations.extend(pair(1));
    assert!(verify_bqnf_involution_pairing(&configurations, &BTreeMap::from([(1,2),(2,1)])).is_err());
}

#[test]
fn empty_ensemble_has_no_average_sign_certificate() {
    assert!(verify_bqnf_involution_pairing(&[], &BTreeMap::new()).is_err());
}
