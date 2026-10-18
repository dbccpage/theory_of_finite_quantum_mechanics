

use serde::{Deserialize, Serialize};

#[derive(Debug, Clone, PartialEq, Eq, Serialize, Deserialize)]
pub struct FieldExtension {
    pub id: String,
    pub name: String,
    pub degree: u32,
    pub conductor: u32,
    pub purchase_type: String,
    pub target_id: String,
}

pub fn build_field_extension_census() -> Vec<FieldExtension> {
    vec![
        FieldExtension {
            id: "EXT_Q".to_string(),
            name: "Base rational field Q".to_string(),
            degree: 1,
            conductor: 1,
            purchase_type: "FORCED".to_string(),
            target_id: "C1000-T802".to_string(),
        },
        FieldExtension {
            id: "EXT_Q_I".to_string(),
            name: "Gaussian rational field Q(i)".to_string(),
            degree: 2,
            conductor: 4,
            purchase_type: "FORCED".to_string(),
            target_id: "C1000-T827".to_string(),
        },
        FieldExtension {
            id: "EXT_Q_ZETA3".to_string(),
            name: "Eisenstein rational field Q(zeta_3)".to_string(),
            degree: 2,
            conductor: 3,
            purchase_type: "FORCED".to_string(),
            target_id: "C1000-T852".to_string(),
        },
        FieldExtension {
            id: "EXT_Q_SQRT5".to_string(),
            name: "Real quadratic field Q(sqrt(5))".to_string(),
            degree: 2,
            conductor: 5,
            purchase_type: "FORCED".to_string(),
            target_id: "C1000-T856".to_string(),
        },
        FieldExtension {
            id: "EXT_Q_ZETA5".to_string(),
            name: "Full cyclotomic field Q(zeta_5)".to_string(),
            degree: 4,
            conductor: 5,
            purchase_type: "CHOSEN".to_string(),
            target_id: "C1000-T852".to_string(),
        },
        FieldExtension {
            id: "EXT_Q_ZETA8".to_string(),
            name: "Cyclotomic field Q(zeta_8)".to_string(),
            degree: 4,
            conductor: 8,
            purchase_type: "FORCED".to_string(),
            target_id: "C1000-T928".to_string(),
        },
        FieldExtension {
            id: "EXT_Q_ZETA12".to_string(),
            name: "Cyclotomic field Q(zeta_12)".to_string(),
            degree: 4,
            conductor: 12,
            purchase_type: "CHOSEN".to_string(),
            target_id: "C1000-T852".to_string(),
        },
    ]
}

#[derive(Debug, Clone, PartialEq, Eq, Serialize, Deserialize)]
pub struct PriceListRow {
    pub item_id: String,
    pub item_kind: String,
    pub description: String,
    pub target_id: String,
    pub cost_metric: String,
    pub cost_value: String,
    pub purchase_type: String,
    pub carrier: String,
}

#[derive(Debug, Clone, PartialEq, Eq, Serialize, Deserialize)]
pub struct TotalityReport {
    pub total_rows: usize,
    pub forward_total: bool,
    pub reverse_total: bool,
    pub both_directions_total: bool,
    pub admissions_have_own_rows: bool,
    pub missing_extensions: Vec<String>,
    pub unbacked_rows: Vec<String>,
}

pub fn build_full_price_list() -> Vec<PriceListRow> {
    let mut rows = Vec::new();

    rows.push(PriceListRow {
        item_id: "ADM_CAUSAL_ORDER".to_string(),
        item_kind: "DECLARED_ASSUMPTION".to_string(),
        description: "Causal order partial order relation on finite posets".to_string(),
        target_id: "C1000-T805".to_string(),
        cost_metric: "ASSUMPTION".to_string(),
        cost_value: "ADMITTED_NOT_SUPPLIED".to_string(),
        purchase_type: "FORCED".to_string(),
        carrier: "finite partial orders (posets)".to_string(),
    });
    rows.push(PriceListRow {
        item_id: "ADM_COMPOSITION_RULE".to_string(),
        item_kind: "DECLARED_ASSUMPTION".to_string(),
        description: "Tensor product bipartite state composition H_A (x) H_B".to_string(),
        target_id: "C1000-T830".to_string(),
        cost_metric: "ASSUMPTION".to_string(),
        cost_value: "DECLARED_ASSUMPTION".to_string(),
        purchase_type: "FORCED".to_string(),
        carrier: "Q(i) tensor products (Herm_4(Q(i)))".to_string(),
    });

    let imports = vec![
        (
            "IMP_B01_INCIDENCE_ALGEBRA",
            "Incidence algebra and Mobius inversion over Q",
            "C1000-T805",
            "CONDUCTOR",
            "1",
            "FORCED",
            "Q",
        ),
        (
            "IMP_B02_PARTIAL_TRACE",
            "Partial trace operator duality",
            "C1000-T830",
            "CONDUCTOR",
            "4",
            "FORCED",
            "Q(i)",
        ),
        (
            "IMP_B03_CYCLIC_ROT",
            "Cyclic rotation group family C_m in SO(3)",
            "C1000-T855",
            "CONDUCTOR",
            "lcm(m, 4)",
            "FORCED",
            "Q(zeta_lcm(m,4))",
        ),
        (
            "IMP_B03_DIHEDRAL_ROT",
            "Dihedral rotation group family D_2m in SO(3)",
            "C1000-T855",
            "CONDUCTOR",
            "lcm(m, 4)",
            "FORCED",
            "Q(zeta_lcm(m,4))",
        ),
        (
            "IMP_B03_TETRAHEDRAL_ROT",
            "Tetrahedral rotation group T =~ A_4",
            "C1000-T860",
            "CONDUCTOR",
            "1",
            "FORCED",
            "Q",
        ),
        (
            "IMP_B03_OCTAHEDRAL_ROT",
            "Octahedral rotation group O =~ S_4 (Member R2)",
            "C1000-T862",
            "CONDUCTOR",
            "1",
            "FORCED",
            "Q",
        ),
        (
            "IMP_B03_ICOSAHEDRAL_ROT",
            "Icosahedral rotation group I =~ A_5 (Member R3)",
            "C1000-T856",
            "CONDUCTOR",
            "5",
            "FORCED",
            "Q(sqrt(5))",
        ),
        (
            "IMP_B04_RATIONAL_BOOST",
            "Rational Lorentz boost matrix B1 with gamma=5/4",
            "C1000-T880",
            "CONDUCTOR",
            "1",
            "FORCED",
            "SO(2,1; Q)",
        ),
        (
            "IMP_B05_NONCOLLINEAR_BOOST",
            "Non-collinear boost pair composition B1(x) B1(y) (Member B2)",
            "C1000-T905",
            "CONDUCTOR",
            "1",
            "FORCED",
            "SO(2,1; Q)",
        ),
        (
            "IMP_B06_CHSH_BIPARTITE",
            "CHSH correlation setup and Bell states",
            "C1000-T930",
            "CONDUCTOR",
            "8",
            "FORCED",
            "Herm_4(Q(zeta_8))",
        ),
        (
            "IMP_B07_COHOMOLOGICAL_OBSTRUCTION",
            "Contextuality presheaf cohomology complex (Members X1, X2)",
            "C1000-T955",
            "CONDUCTOR",
            "1",
            "FORCED",
            "Z_2 presheaves",
        ),
        (
            "IMP_B08_MICROCAUSALITY_ALGEBRAS",
            "Commuting operator subalgebras for bipartite incomparability graphs",
            "C1000-T980",
            "CONDUCTOR",
            "4",
            "FORCED",
            "Herm_4(Q(i))",
        ),
        (
            "IMP_B09_ONE_PARAM_SUBGROUPS",
            "One-parameter subgroup parameter mappings and Lindemann-Weierstrass",
            "C1000-T1005",
            "TRANSCENDENTAL_REFUSAL",
            "REFUSED_TRANSCENDENTAL",
            "FORCED",
            "algebraic matrices",
        ),
    ];
    for (id, desc, target, metric, val, ptype, carr) in imports {
        rows.push(PriceListRow {
            item_id: id.to_string(),
            item_kind: "IMPORTED_STRUCTURE".to_string(),
            description: desc.to_string(),
            target_id: target.to_string(),
            cost_metric: metric.to_string(),
            cost_value: val.to_string(),
            purchase_type: ptype.to_string(),
            carrier: carr.to_string(),
        });
    }

    for ext in build_field_extension_census() {
        rows.push(PriceListRow {
            item_id: ext.id,
            item_kind: "FIELD_EXTENSION".to_string(),
            description: ext.name,
            target_id: ext.target_id,
            cost_metric: "DEGREE".to_string(),
            cost_value: format!("degree={}, conductor={}", ext.degree, ext.conductor),
            purchase_type: ext.purchase_type,
            carrier: "field extension".to_string(),
        });
    }

    let params = vec![
        (
            "PARAM_ROT_ID",
            "Rotation identity theta = 0",
            "C1000-T1006",
            "0 (CARRIED)",
            "FORCED",
            "Q",
        ),
        (
            "PARAM_ROT_C2",
            "Rotation C2 angle theta = pi",
            "C1000-T1006",
            "pi (REFUSED)",
            "FORCED",
            "R \\ Q_bar",
        ),
        (
            "PARAM_ROT_C3",
            "Rotation C3 angle theta = 2*pi/3",
            "C1000-T1006",
            "2*pi/3 (REFUSED)",
            "FORCED",
            "R \\ Q_bar",
        ),
        (
            "PARAM_ROT_C4",
            "Rotation C4 angle theta = pi/2",
            "C1000-T1006",
            "pi/2 (REFUSED)",
            "FORCED",
            "R \\ Q_bar",
        ),
        (
            "PARAM_ROT_C6",
            "Rotation C6 angle theta = pi/3",
            "C1000-T1006",
            "pi/3 (REFUSED)",
            "FORCED",
            "R \\ Q_bar",
        ),
        (
            "PARAM_ROT_I60_PLUS",
            "Icosahedral angle theta = 2*pi/5",
            "C1000-T1006",
            "2*pi/5 (REFUSED)",
            "FORCED",
            "R \\ Q_bar",
        ),
        (
            "PARAM_ROT_I60_MINUS",
            "Icosahedral angle theta = 4*pi/5",
            "C1000-T1006",
            "4*pi/5 (REFUSED)",
            "FORCED",
            "R \\ Q_bar",
        ),
        (
            "PARAM_ROT_PYTH_3_4_5",
            "Pythagorean angle theta = arccos(3/5)",
            "C1000-T1006",
            "arccos(3/5) (REFUSED)",
            "FORCED",
            "R \\ Q_bar",
        ),
        (
            "PARAM_ROT_POLAR_B05",
            "Polar angle theta = arccos(16/25)",
            "C1000-T1006",
            "arccos(16/25) (REFUSED)",
            "FORCED",
            "R \\ Q_bar",
        ),
        (
            "PARAM_BOOST_ID",
            "Boost identity rapidity eta = 0",
            "C1000-T1007",
            "0 (CARRIED)",
            "FORCED",
            "Q",
        ),
        (
            "PARAM_BOOST_B1",
            "Boost B1 rapidity eta = ln(2)",
            "C1000-T1007",
            "ln(2) (REFUSED)",
            "FORCED",
            "R \\ Q_bar",
        ),
        (
            "PARAM_BOOST_B1_SQ",
            "Boost B1^2 rapidity eta = ln(4)",
            "C1000-T1007",
            "ln(4) (REFUSED)",
            "FORCED",
            "R \\ Q_bar",
        ),
        (
            "PARAM_BOOST_PYTH_5_12_13",
            "Pythagorean boost rapidity eta = arcosh(13/5)",
            "C1000-T1007",
            "arcosh(13/5) (REFUSED)",
            "FORCED",
            "R \\ Q_bar",
        ),
        (
            "PARAM_BOOST_PYTH_7_24_25",
            "Pythagorean boost rapidity eta = arcosh(25/7)",
            "C1000-T1007",
            "arcosh(25/7) (REFUSED)",
            "FORCED",
            "R \\ Q_bar",
        ),
        (
            "PARAM_BOOST_POLAR_B05",
            "Polar boost factor rapidity eta = arcosh(41/32)",
            "C1000-T1007",
            "arcosh(41/32) (REFUSED)",
            "FORCED",
            "R \\ Q_bar",
        ),
        (
            "PARAM_TIME_ID",
            "Unitary time parameter t = 0",
            "C1000-T1008",
            "0 (CARRIED)",
            "FORCED",
            "Q",
        ),
        (
            "PARAM_TIME_PAULI_Z",
            "Pauli Z time parameter t = pi/2",
            "C1000-T1008",
            "pi/2 (REFUSED)",
            "FORCED",
            "R \\ Q_bar",
        ),
        (
            "PARAM_TIME_PAULI_X",
            "Pauli X time parameter t = pi/2",
            "C1000-T1008",
            "pi/2 (REFUSED)",
            "FORCED",
            "R \\ Q_bar",
        ),
    ];
    for (id, desc, target, val, ptype, carr) in params {
        rows.push(PriceListRow {
            item_id: id.to_string(),
            item_kind: "EXTERNAL_PARAMETER".to_string(),
            description: desc.to_string(),
            target_id: target.to_string(),
            cost_metric: "TRANSCENDENTAL_REFUSAL".to_string(),
            cost_value: val.to_string(),
            purchase_type: ptype.to_string(),
            carrier: carr.to_string(),
        });
    }

    let bounds = vec![
        (
            "BOUND_B01_POSET_CARDINALITY",
            "Max poset cardinality bound N=4",
            "C1000-T811",
            "N=4",
        ),
        (
            "BOUND_B04_CONDUCTOR_SEARCH",
            "Max conductor searched for boost closure m=60",
            "C1000-T886",
            "m=60",
        ),
        (
            "BOUND_B05_BOOST_PAIRS",
            "Two-boost composition pair enumeration bound",
            "C1000-T911",
            "1445 pairs",
        ),
        (
            "BOUND_B06_HEIGHT",
            "Height bound H=5 for CHSH correlation search",
            "C1000-T936",
            "H=5",
        ),
        (
            "BOUND_B07_SCENARIOS",
            "Contextuality scenario complexity bound",
            "C1000-T961",
            "2 scenarios",
        ),
        (
            "BOUND_B08_POSETS_SEARCHED",
            "Poset isomorphism search bound",
            "C1000-T986",
            "21 posets",
        ),
        (
            "BOUND_B09_INTERVAL_ERROR",
            "Rational interval approximation error bound",
            "C1000-T1013",
            "error <= 1e-5",
        ),
    ];
    for (id, desc, target, val) in bounds {
        rows.push(PriceListRow {
            item_id: id.to_string(),
            item_kind: "SEARCH_BOUND".to_string(),
            description: desc.to_string(),
            target_id: target.to_string(),
            cost_metric: "SEARCH_BOUND".to_string(),
            cost_value: val.to_string(),
            purchase_type: "CHOSEN".to_string(),
            carrier: "search bound".to_string(),
        });
    }

    rows
}

pub fn verify_price_list_totality(rows: &[PriceListRow]) -> TotalityReport {
    let census = build_field_extension_census();
    let row_ids: std::collections::HashSet<&str> =
        rows.iter().map(|r| r.item_id.as_str()).collect();

    let mut missing_extensions = Vec::new();
    for ext in &census {
        if !row_ids.contains(ext.id.as_str()) {
            missing_extensions.push(ext.id.clone());
        }
    }

    let full = build_full_price_list();
    let expected_ids: std::collections::HashSet<&str> =
        full.iter().map(|r| r.item_id.as_str()).collect();

    let mut unbacked_rows = Vec::new();
    for r in rows {
        if !expected_ids.contains(r.item_id.as_str()) {
            unbacked_rows.push(r.item_id.clone());
        }
    }

    let adm_causal = rows.iter().find(|r| r.item_id == "ADM_CAUSAL_ORDER");
    let adm_comp = rows.iter().find(|r| r.item_id == "ADM_COMPOSITION_RULE");
    let admissions_ok = match (adm_causal, adm_comp) {
        (Some(c), Some(p)) => {
            c.item_kind == "DECLARED_ASSUMPTION" && p.item_kind == "DECLARED_ASSUMPTION"
        }
        _ => false,
    };

    let fwd = missing_extensions.is_empty();
    let rev = unbacked_rows.is_empty();

    TotalityReport {
        total_rows: rows.len(),
        forward_total: fwd,
        reverse_total: rev,
        both_directions_total: fwd && rev && admissions_ok,
        admissions_have_own_rows: admissions_ok,
        missing_extensions,
        unbacked_rows,
    }
}

#[derive(Debug, Clone, PartialEq, Eq, Serialize, Deserialize)]
pub struct FQMR1Clause {
    pub clause_index: usize,
    pub clause_key: String,
    pub witness_member: String,
    pub discharged: bool,
    pub verdict: String,
    pub target_id: String,
}

pub fn adjudicate_fqmr1_clauses() -> Vec<FQMR1Clause> {
    vec![
        FQMR1Clause {
            clause_index: 1,
            clause_key: "1_causal_order_status".to_string(),
            witness_member: "C1".to_string(),
            discharged: true,
            verdict: "CAUSAL_ORDER_ADMITTED_NOT_SUPPLIED".to_string(),
            target_id: "C1000-T805".to_string(),
        },
        FQMR1Clause {
            clause_index: 2,
            clause_key: "2_composition_and_marginal".to_string(),
            witness_member: "Q1".to_string(),
            discharged: true,
            verdict: "COMPOSITION_RULE_DECLARED_MARGINAL_UNIQUE".to_string(),
            target_id: "C1000-T830".to_string(),
        },
        FQMR1Clause {
            clause_index: 3,
            clause_key: "3_no_signalling_verdict".to_string(),
            witness_member: "Q1".to_string(),
            discharged: true,
            verdict: "NO_SIGNALLING_DERIVED_FROM_ADMITTED_COMPOSITION".to_string(),
            target_id: "C1000-T835".to_string(),
        },
        FQMR1Clause {
            clause_index: 4,
            clause_key: "4_element_inventory_with_price".to_string(),
            witness_member: "R3".to_string(),
            discharged: true,
            verdict: "ROTATION_GROUPS_CLOSE_AT_COMPUTED_PRICE".to_string(),
            target_id: "C1000-T856".to_string(),
        },
        FQMR1Clause {
            clause_index: 5,
            clause_key: "5_group_closure_verdict".to_string(),
            witness_member: "B1".to_string(),
            discharged: true,
            verdict: "BOOSTS_EXACT_BUT_NEVER_FINITE".to_string(),
            target_id: "C1000-T880".to_string(),
        },
        FQMR1Clause {
            clause_index: 6,
            clause_key: "6_parameter_verdict".to_string(),
            witness_member: "B1".to_string(),
            discharged: true,
            verdict: "PARAMETERS_REFUSED_ELEMENTS_CARRIED".to_string(),
            target_id: "C1000-T1007".to_string(),
        },
        FQMR1Clause {
            clause_index: 7,
            clause_key: "7_terminating_algorithms".to_string(),
            witness_member: "R2".to_string(),
            discharged: true,
            verdict: "OCTAHEDRAL_ENUMERATION_TERMINATING".to_string(),
            target_id: "C1000-T862".to_string(),
        },
        FQMR1Clause {
            clause_index: 8,
            clause_key: "8_structural_verdicts".to_string(),
            witness_member: "C2".to_string(),
            discharged: true,
            verdict: "MICROCAUSALITY_COMMUTING_CRITERION_DISCHARGED".to_string(),
            target_id: "C1000-T985".to_string(),
        },
        FQMR1Clause {
            clause_index: 9,
            clause_key: "9_correlation_bound_attainment".to_string(),
            witness_member: "Q2".to_string(),
            discharged: true,
            verdict: "TSIRELSON_ATTAINED_IFF_EIGHT_DIVIDES_CONDUCTOR".to_string(),
            target_id: "C1000-T930".to_string(),
        },
        FQMR1Clause {
            clause_index: 10,
            clause_key: "10_price_ledger".to_string(),
            witness_member: "R3".to_string(),
            discharged: true,
            verdict: "PRICE_LIST_TOTAL_BOTH_DIRECTIONS".to_string(),
            target_id: "C1000-T1033".to_string(),
        },
    ]
}

pub fn check_structural_sentence(stmt1: bool, stmt2: bool, stmt3: bool) -> (String, bool) {
    let sentence = "The carrier holds group elements and never group parameters; \
                    rotation groups close at a computed conductor price; \
                    the boost group closes at no price."
        .to_string();
    let supported = stmt1 && stmt2 && stmt3;
    (sentence, supported)
}
