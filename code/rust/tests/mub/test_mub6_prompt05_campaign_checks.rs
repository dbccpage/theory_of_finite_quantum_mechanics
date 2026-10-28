//! Prompt 05 campaign checks: the balanced table replay, its negative controls and the
//! exact checks of the campaign's local lemmas.
//!
//! The table is read from the 010_mub6 paper package and pinned by its SHA-256. Each
//! expected value below is what the campaign or the Lean definitions state; a mismatch
//! is a failure, not a revision.
//!
//! AuthorityEffect: None
//! Firewall Line: NOT MUB(6)=3, NOT MUB(6)<=3; stated region only; mints no authority

use std::{
    collections::{BTreeMap, BTreeSet},
    fs,
    path::PathBuf,
    process::Command,
};

use num_rational::BigRational;
use tfqm_mub::native::campaign::mub6_balanced_table_replay::{
    self as replay, BalancedReplayError, BalancedTable,
};
use tfqm_mub::native::campaign::mub6_prompt05_campaign_checks::{
    run_campaign_checks, CampaignCheckError, FIREWALL_LINE,
};

const TABLE: &str = "omega_engine_atlas/coda_atlas/F004_papers/010_mub6/artifacts/\
balanced_quadratic_coefficients_20261011.jsonl";
const RECEIPT: &str = "omega_engine_atlas/coda_atlas/F004_papers/010_mub6/artifacts/\
mub6_prompt05_campaign_receipt.json";

fn repo_root() -> PathBuf {
    PathBuf::from(env!("CARGO_MANIFEST_DIR")).join("../../..")
}

fn table_bytes() -> Vec<u8> {
    fs::read(repo_root().join(TABLE)).expect("balanced table is present")
}

fn set(values: &[&str]) -> BTreeSet<String> {
    values.iter().map(|s| s.to_string()).collect()
}

#[test]
fn table_is_the_regeneration_of_its_definitions() {
    let table = BalancedTable::from_bytes(&table_bytes()).expect("pinned table parses");
    let inventory = replay::inventory(&table);
    assert!(inventory.mismatched_rows.is_empty());
    assert_eq!((inventory.rows, inventory.variables), (648, 320));
    assert_eq!((inventory.total_terms, inventory.maximum_terms), (8313, 676));
    assert_eq!(inventory.empty_rows.len(), 42);
    assert_eq!(inventory.empty_gauge_modulus_rows + inventory.nonempty_modulus_rows, 108);
    assert_eq!(inventory.empty_gauge_modulus_rows, 23);
    assert_eq!(inventory.empty_gram_rows, 19);
    assert_eq!(inventory.empty_gauge_modulus_rows + inventory.empty_gram_rows, 42);
    // 216 Gram rows: 90 upper, 90 Hermitian duplicates, 18 zero imaginary diagonals,
    // 18 real diagonals equal to sums of modulus rows.
    assert_eq!(inventory.gram_upper_rows, 90);
    assert_eq!(inventory.gram_hermitian_duplicate_pairs * 2, 90);
    assert_eq!(inventory.gram_diagonal_real_equal_modulus_sum, 18);
    assert_eq!(90 + 90 + 18 + 18, replay::GRAPH_START - replay::GRAM_START);
    assert_eq!((inventory.graph_rows, inventory.transition_modulus_rows), (216, 108));
}

#[test]
fn a_changed_coefficient_is_named_by_row() {
    let mut table = BalancedTable::from_bytes(&table_bytes()).expect("pinned table parses");
    let row = 400;
    let (monomial, coefficient) = table.rows[row]
        .iter()
        .next()
        .map(|(m, c)| (m.clone(), c.clone()))
        .expect("row 400 has terms");
    table.rows[row].insert(monomial, coefficient + BigRational::from_integer(1.into()));
    assert_eq!(replay::inventory(&table).mismatched_rows, vec![row]);
}

#[test]
fn changed_or_truncated_bytes_are_refused() {
    let mut bytes = table_bytes();
    let last = bytes.len() - 2;
    bytes[last] ^= 1;
    assert!(matches!(
        BalancedTable::from_bytes(&bytes),
        Err(BalancedReplayError::InputHash(_))
    ));
    assert!(matches!(
        run_campaign_checks(&bytes[..bytes.len() / 2]),
        Err(CampaignCheckError::Table(BalancedReplayError::InputHash(_)))
    ));
}

#[test]
fn third_basis_equal_to_the_first_or_second_fails_only_its_transition_moduli() {
    let receipt = run_campaign_checks(&table_bytes()).expect("checks run");
    let controls = &receipt.negative_controls;
    assert_eq!(controls.len(), 2);
    let expected = [
        ("B3 := B1", 576..612, [220, 232, 244, 256, 268]),
        ("B3 := B2", 612..648, [270, 282, 294, 306, 318]),
    ];
    for (control, (name, rows, outside)) in controls.iter().zip(expected) {
        assert_eq!(control.name, name);
        assert_eq!(control.evaluation.nonzero_rows, rows.collect::<Vec<_>>());
        assert_eq!(
            control.nonzero_rows_by_block,
            BTreeMap::from([("transition_modulus", 36)])
        );
        assert_eq!(control.evaluation.nonzero_values, set(&["-6/1", "30/1"]));
        assert_eq!(control.evaluation.box_membership.outside, outside.to_vec());
        assert!(control.evaluation.box_membership.undecided.is_empty());
    }
}

#[test]
fn jacobian_at_the_centre_is_nonzero_and_rank_deficient() {
    let receipt = run_campaign_checks(&table_bytes()).expect("checks run");
    let j = &receipt.jacobian_at_centre;
    assert_eq!((j.rows, j.columns), (648, 320));
    assert_eq!(j.linear_terms, 1045);
    assert_eq!(
        j.linear_terms_by_block,
        BTreeMap::from([("gram", 100), ("graph", 720), ("transition_modulus", 225)])
    );
    assert_eq!(j.rows_with_linear_part, 269);
    assert_eq!(j.rank, 184);
    assert!(!j.jacobian_is_zero);
    assert!(!j.full_column_rank);
}

#[test]
fn local_lemmas_match_their_stated_values() {
    let r = run_campaign_checks(&table_bytes()).expect("checks run");
    assert_eq!(r.authority_effect, "None");
    assert_eq!(r.firewall_line, FIREWALL_LINE);

    let d1 = &r.d1_product_triple;
    assert!(d1.entries_unimodular && d1.entries_in_q_zeta12);
    assert!(d1.gram_equals_six_identity && d1.gauge_first_rows_and_column_one);
    assert_eq!(d1.normalized_cross_overlaps, set(&["1/6"]));
    assert_eq!(d1.normalized_identity_overlaps, set(&["1/6"]));

    let d2 = &r.d2_decoys;
    assert_eq!(d2.qubit_sigma_z, set(&["0/1", "1/1"]));
    assert_eq!(d2.qutrit_diag_one_w_w2, set(&["0/1", "1/1"]));
    assert_eq!(d2.six_dim_sigma_z_seed, set(&["0/1", "1/3"]));

    let d3 = &r.d3_gram_spectrum;
    assert_eq!(
        (d3.multiplicity_four, d3.multiplicity_one, d3.multiplicity_zero),
        (1, 20, 3)
    );

    let d9 = &r.d9_fixed_triple_counts;
    assert_eq!((d9.equations, d9.coordinates), (180, 72));
    assert_eq!((d9.overlap_rows, d9.column_unitarity_rows), (108, 72));
    assert!(d9.coefficients_real);
    assert_eq!(
        (
            d9.hermitian_duplicate_rows,
            d9.zero_diagonal_imaginary_rows,
            d9.diagonal_real_equal_identity_overlap_sums
        ),
        (30, 6, 6)
    );
    assert_eq!(d9.rows_not_implied_by_these_identities, 138);
    assert_eq!(d9.row_unitarity_components_listed, 0);

    let e1 = &r.e1_affine_multipliers;
    assert_eq!((e1.equations, e1.multipliers), (252, 73));
    assert_eq!(e1.nonzero_expectations, 0);
    assert_eq!(e1.second_moment_of_a_coordinate, "1/12");
    assert!(e1.degree_two_example_nonzero);

    let f2 = &r.f2_commutative_model;
    assert!(f2.idempotent_and_orthogonal && f2.complete);
    assert_eq!(f2.single_traces, set(&["1/6"]));
    assert_eq!(f2.pair_traces_across_bases, set(&["1/36"]));
    assert_eq!(f2.sandwich_violations, f2.sandwich_cases);
    assert_eq!(f2.sandwich_cases, 432);

    let g = &r.g_gauge_counts;
    assert_eq!(
        g.slot_coordinates + g.d_block_coordinates + g.core_coordinates,
        g.coordinates
    );
    assert_eq!((g.slot_coordinates, g.d_block_coordinates, g.core_coordinates), (152, 18, 150));
    assert!(g.product_triple_balance);
}

#[test]
fn committed_receipt_matches_a_fresh_run() {
    let fresh = run_campaign_checks(&table_bytes()).expect("checks run");
    let mut bytes = serde_json::to_vec_pretty(&fresh).expect("receipt serializes");
    bytes.push(b'\n');
    let committed = fs::read(repo_root().join(RECEIPT)).expect("receipt is committed");
    let parsed: serde_json::Value = serde_json::from_slice(&committed).expect("receipt is JSON");
    let expected: serde_json::Value = serde_json::from_slice(&bytes).expect("fresh is JSON");
    assert_eq!(parsed, expected);
}

#[test]
fn bin_refuses_an_existing_output() {
    let dir = std::env::temp_dir().join(format!("mub6_prompt05_{}", std::process::id()));
    fs::create_dir_all(&dir).expect("temp dir");
    let output = dir.join("receipt.json");
    fs::write(&output, b"{}").expect("placeholder");
    let status = Command::new(env!("CARGO_BIN_EXE_mub6_prompt05_campaign_checks"))
        .arg(repo_root().join(TABLE))
        .arg(&output)
        .output()
        .expect("bin launches");
    assert_eq!(status.status.code(), Some(1));
    assert_eq!(fs::read(&output).expect("placeholder kept"), b"{}");
    fs::remove_dir_all(&dir).expect("cleanup");
}
