use omega_wdp::question_preserving_encoding::{
    candidates, check, cochain_proposal, direct_proposal, encode_cochain, encode_direct,
    experiment, parse_cochain, parse_direct, verify_cochain, verify_direct, Refusal, Task,
    MAX_REPORT_BYTES,
};
use serde_json::{json, Value};

fn zero() -> Task {
    Task {
        derivative: [0, 0],
        value_at_zero: 0,
    }
}

fn encoded(candidate: [i64; 3]) -> Value {
    serde_json::to_value(encode_cochain(zero(), candidate).unwrap()).unwrap()
}

#[test]
fn closure_and_even_a_full_unanchored_report_do_not_decide_the_question() {
    let correct = encode_cochain(zero(), [0, 0, 0]).unwrap();
    let wrong = encode_cochain(zero(), [1, 1, 1]).unwrap();
    assert_eq!(correct.edges, wrong.edges);
    assert!(verify_cochain(zero(), &serde_json::to_string(&correct).unwrap()).unwrap());
    assert!(!verify_cochain(zero(), &serde_json::to_string(&wrong).unwrap()).unwrap());
}

#[test]
fn anchored_parser_round_trips_every_declared_candidate() {
    for c in candidates() {
        let cochain = serde_json::to_string(&encode_cochain(zero(), c).unwrap()).unwrap();
        let direct = serde_json::to_string(&encode_direct(zero(), c).unwrap()).unwrap();
        assert_eq!(parse_cochain(zero(), &cochain), Ok(c));
        assert_eq!(parse_direct(zero(), &direct), Ok(c));
        assert_eq!(verify_cochain(zero(), &cochain), check(zero(), c));
    }
}

#[test]
fn checker_uses_both_derivative_coefficients_and_the_initial_value() {
    let task = Task {
        derivative: [-1, 4],
        value_at_zero: 2,
    };
    assert_eq!(check(task, [2, -1, 2]), Ok(true));
    for wrong in [[1, -1, 2], [2, 1, 2], [2, -1, 1]] {
        assert_eq!(check(task, wrong), Ok(false));
    }
    let odd = Task {
        derivative: [0, 3],
        value_at_zero: 0,
    };
    assert_eq!(direct_proposal(odd), Ok(None));
    assert_eq!(cochain_proposal(odd), Ok(None));
    assert!(candidates().into_iter().all(|c| check(odd, c) == Ok(false)));
}

#[test]
fn task_identity_is_compared_with_an_independently_supplied_task() {
    let mut report = encoded([0, 0, 0]);
    report["task"]["value_at_zero"] = json!(1);
    assert_eq!(
        verify_cochain(zero(), &report.to_string()),
        Err(Refusal::TaskMismatch)
    );
    let direct = encode_direct(
        Task {
            derivative: [0, 0],
            value_at_zero: 1,
        },
        [1, 0, 0],
    )
    .unwrap();
    assert_eq!(
        verify_direct(zero(), &serde_json::to_string(&direct).unwrap()),
        Err(Refusal::TaskMismatch)
    );
}

#[test]
fn corrupt_wire_and_coherent_wrong_candidate_have_distinct_outcomes() {
    let mut report = encoded([0, 0, 0]);
    report["edges"][2] = json!(1);
    assert_eq!(
        verify_cochain(zero(), &report.to_string()),
        Err(Refusal::NonClosedReport)
    );
    let mut coherent = encoded([0, 0, 0]);
    coherent["anchor"] = json!(1);
    assert_eq!(parse_cochain(zero(), &coherent.to_string()), Ok([1, 1, 1]));
    assert_eq!(verify_cochain(zero(), &coherent.to_string()), Ok(false));
}

#[test]
fn parser_refuses_ambiguous_untyped_or_unbounded_reports() {
    let valid = encoded([0, 0, 0]);
    for replacement in [json!(true), json!(0.0), json!("0"), json!(null)] {
        let mut report = valid.clone();
        report["anchor"] = replacement;
        assert_eq!(
            parse_cochain(zero(), &report.to_string()),
            Err(Refusal::MalformedReport)
        );
    }
    let mut extra = valid.clone();
    extra["accepted"] = json!(true);
    assert_eq!(
        parse_cochain(zero(), &extra.to_string()),
        Err(Refusal::MalformedReport)
    );
    let mut missing = valid.clone();
    missing.as_object_mut().unwrap().remove("anchor");
    assert_eq!(
        parse_cochain(zero(), &missing.to_string()),
        Err(Refusal::MalformedReport)
    );
    let duplicate = valid.to_string().replacen("{", "{\"anchor\":0,", 1);
    assert_eq!(
        parse_cochain(zero(), &duplicate),
        Err(Refusal::MalformedReport)
    );
    assert_eq!(
        parse_cochain(zero(), &(valid.to_string() + " false")),
        Err(Refusal::MalformedReport)
    );
    assert_eq!(
        parse_cochain(zero(), &" ".repeat(MAX_REPORT_BYTES + 1)),
        Err(Refusal::MalformedReport)
    );
    let mut huge = valid;
    huge["edges"][0] = json!(i64::MAX);
    assert_eq!(
        parse_cochain(zero(), &huge.to_string()),
        Err(Refusal::EdgeOutOfDomain)
    );
}

#[test]
fn bounds_and_schema_are_checked_before_semantic_acceptance() {
    let mut report = encoded([0, 0, 0]);
    report["schema_version"] = json!(2);
    assert_eq!(
        parse_cochain(zero(), &report.to_string()),
        Err(Refusal::SchemaMismatch)
    );
    let mut report = encoded([0, 0, 0]);
    report["domain"] = json!("another_question");
    assert_eq!(
        parse_cochain(zero(), &report.to_string()),
        Err(Refusal::SchemaMismatch)
    );
    let mut report = encoded([0, 0, 0]);
    report["anchor"] = json!(2);
    report["edges"] = json!([1, 0, -1]);
    assert_eq!(
        parse_cochain(zero(), &report.to_string()),
        Err(Refusal::CandidateOutOfDomain)
    );
    assert_eq!(
        check(zero(), [i64::MAX, 0, 0]),
        Err(Refusal::CandidateOutOfDomain)
    );
    assert_eq!(
        check(
            Task {
                derivative: [0, i64::MAX],
                value_at_zero: 0
            },
            [0, 0, 0]
        ),
        Err(Refusal::TaskOutOfDomain)
    );
}

#[test]
fn exhaustive_comparison_retains_unsatisfiable_tasks_and_the_strong_baseline() {
    let result = experiment().unwrap();
    assert_eq!(result["candidate_count"], 125);
    assert_eq!(result["task_count"], 225);
    assert_eq!(result["audit_task_candidate_pairs"], 28125);
    assert_eq!(result["satisfiable_tasks"], 125);
    assert_eq!(result["unsatisfiable_tasks"], 100);
    assert_eq!(result["closed_wrong_task_candidate_pairs"], 28000);
    assert_eq!(result["unanchored_colliding_tasks"], 101);
    assert_eq!(result["closure_only_colliding_tasks"], 125);
    assert_eq!(result["strategies"][0]["checker_calls"], 20375);
    assert_eq!(result["strategies"][1]["checker_calls"], 125);
    assert_eq!(result["strategies"][2]["checker_calls"], 125);
    assert_eq!(result["strategies"][2]["gamma2_evaluations"], 125);
}
