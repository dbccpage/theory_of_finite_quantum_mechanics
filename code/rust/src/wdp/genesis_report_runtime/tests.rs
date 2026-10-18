use crate::genesis_primitive_execution::{PrimitiveEvent as E, PrimitiveInstance};
use crate::genesis_questions::{Answer, ProtectedQuestion, Question};
use crate::genesis_report_runtime::*;
use std::collections::BTreeSet;

fn history(id: &str, tokens: &[&str]) -> NamedHistory {
    NamedHistory {
        id: id.into(),
        events: std::iter::once(E::Supply { token: "<>".into() })
            .chain(tokens.iter().map(|s| E::AdmitDatum { token: (*s).into() }))
            .collect(),
    }
}
fn request(histories: Vec<NamedHistory>) -> Request {
    Request {
        schema_version: REQUEST_SCHEMA.into(),
        source_sha256: source_sha256(),
        report: vec!["forgotten".into(); histories.len()],
        histories,
        questions: [
            Question::HasDatum("a".into()),
            Question::HasDatum("b".into()),
            Question::DatumCount,
            Question::EventCount,
        ]
        .into_iter()
        .enumerate()
        .map(|(i, question)| ProtectedQuestion {
            id: format!("q{i}"),
            question,
        })
        .collect(),
        continuations: vec![NamedHistory {
            id: "now".into(),
            events: vec![],
        }],
        global: None,
        repair: Some(RepairAllowance {
            max_steps: 64,
            max_pair_checks: 1_000_000,
        }),
    }
}
fn global(fact_column: usize, locals: Vec<usize>) -> GlobalRequest {
    GlobalRequest {
        observed_columns: vec![1, 2],
        contexts: BTreeSet::from([0, 1, 2, 3]),
        cover: vec![1, 2],
        locals,
        fact_column,
        work_limit: 1_000_000,
    }
}

#[test]
fn keeps_all_five_fields_and_all_six_event_types() {
    let mut h = history("six", &["a", "b", "a"]);
    h.events.extend([
        E::AdmitForm { arity: 1 },
        E::AdmitForm { arity: 1 },
        E::AdmitInst {
            form: 0,
            args: vec![1],
        },
        E::AdmitRuleAll { form: 1 },
        E::Impose { i: 0, j: 1 },
    ]);
    let r = evaluate(&request(vec![h])).unwrap();
    assert_eq!(
        r.states[0],
        State {
            data: vec!["a".into(), "b".into()],
            forms: vec![1, 1],
            instances: vec![PrimitiveInstance {
                form: 0,
                args: vec![1]
            }],
            rules: vec![1],
            requirements: vec![(0, 1)]
        }
    );
    assert_eq!(r.answers[0][4], Answer::Count(9));
}

#[test]
fn empty_unique_ambiguous_and_definite_facts_remain_distinct() {
    let mut empty = request(vec![history("00", &[]), history("11", &["a", "b"])]);
    empty.global = Some(global(3, vec![0, 1]));
    let result = evaluate(&empty).unwrap();
    assert!(result.global.as_ref().unwrap().histories.is_empty());
    assert_eq!(
        result.global.as_ref().unwrap().fact,
        Fact::NoGlobalExtension
    );
    for check in &result.repair.unwrap().global_rechecks {
        assert_eq!(check, &result.global);
    }

    let mut unique = request(vec![history("10", &["a"]), history("01", &["b"])]);
    unique.global = Some(global(3, vec![1, 0]));
    assert_eq!(
        evaluate(&unique).unwrap().global.unwrap().histories,
        vec![0]
    );

    let mut duplicate = history("other occurrence", &["a"]);
    duplicate.events.push(E::Supply {
        token: "inert".into(),
    });
    let mut ambiguous = request(vec![history("10", &["a"]), duplicate]);
    ambiguous.global = Some(global(3, vec![0, 0]));
    let g = evaluate(&ambiguous).unwrap().global.unwrap();
    assert_eq!(g.histories, vec![0, 1]);
    assert_eq!(
        g.fact,
        Fact::Certified {
            answer: Answer::Count(1)
        }
    );
    ambiguous.global.as_mut().unwrap().fact_column = 4;
    assert_eq!(
        evaluate(&ambiguous).unwrap().global.unwrap().fact,
        Fact::Undetermined {
            first: 0,
            second: 1
        }
    );
}

#[test]
fn repairs_preserve_old_reports_have_strict_rank_and_replay_original_task() {
    let mut r = request(vec![
        history("0", &[]),
        history("a", &["a"]),
        history("b", &["b"]),
        history("ab", &["a", "b"]),
    ]);
    r.global = Some(global(3, vec![1, 0]));
    let result = evaluate(&r).unwrap();
    assert!(matches!(result.report, Decision::Collision { .. }));
    let repair = result.repair.as_ref().unwrap();
    assert_eq!(repair.ranks.last(), Some(&0));
    assert!(repair.ranks.windows(2).all(|pair| pair[1] < pair[0]));
    assert_eq!(repair.partitions.len(), repair.steps.len() + 1);
    assert!(repair.global_rechecks.iter().all(|g| g == &result.global));
    verify(&r, &result).unwrap();
    let mut forged = result.clone();
    forged
        .repair
        .as_mut()
        .unwrap()
        .partitions
        .last_mut()
        .unwrap()[0] = 88;
    assert_eq!(verify(&r, &forged).unwrap_err().code, "CANDIDATE");
    r.repair.as_mut().unwrap().max_steps = 0;
    assert_eq!(evaluate(&r).unwrap_err().code, "REPAIR");
}

#[test]
fn declared_language_does_not_silently_claim_compositional_closure() {
    let mut r = request(vec![
        history("with datum", &["a"]),
        history("without datum", &[]),
    ]);
    r.questions = vec![ProtectedQuestion {
        id: "form1".into(),
        question: Question::Derivable(PrimitiveInstance {
            form: 1,
            args: vec![0],
        }),
    }];
    r.continuations.push(NamedHistory {
        id: "one form".into(),
        events: vec![E::AdmitForm { arity: 1 }],
    });
    let result = evaluate(&r).unwrap();
    assert_eq!(result.class_of, vec![0, 0]);
    assert!(matches!(
        result.operations[1].decision,
        Decision::Collision {
            first: 0,
            second: 1,
            ..
        }
    ));
    r.continuations.push(NamedHistory {
        id: "two forms".into(),
        events: vec![E::AdmitForm { arity: 1 }, E::AdmitForm { arity: 1 }],
    });
    assert_ne!(
        evaluate(&r).unwrap().class_of[0],
        evaluate(&r).unwrap().class_of[1]
    );
}

#[test]
fn availability_is_protected_even_with_no_questions() {
    let mut r = request(vec![
        NamedHistory {
            id: "pre".into(),
            events: vec![],
        },
        history("root", &[]),
    ]);
    r.questions.clear();
    r.continuations.push(NamedHistory {
        id: "admit".into(),
        events: vec![E::AdmitDatum { token: "a".into() }],
    });
    let result = evaluate(&r).unwrap();
    assert_eq!(
        result.answers,
        vec![
            vec![Answer::Boolean(true), Answer::Boolean(false)],
            vec![Answer::Boolean(true), Answer::Boolean(true)]
        ]
    );
}

#[test]
fn admission_errors_source_changes_and_resource_failures_refuse() {
    let mut r = request(vec![history("a", &["a", "b"])]);
    r.histories[0].events.push(E::Impose { i: 1, j: 0 });
    assert_eq!(evaluate(&r).unwrap_err().code, "ADMISSION");
    r.histories[0].events.pop();
    let result = evaluate(&r).unwrap();
    r.histories[0].events.push(E::Supply {
        token: "changed occurrence".into(),
    });
    assert_eq!(verify(&r, &result).unwrap_err().code, "CANDIDATE");
    r.source_sha256 = "0".repeat(64);
    assert_eq!(evaluate(&r).unwrap_err().code, "SOURCE");
    r.source_sha256 = source_sha256();
    r.global = Some(global(3, vec![0, 0]));
    r.global.as_mut().unwrap().work_limit = 0;
    assert_eq!(evaluate(&r).unwrap_err().code, "RESTRICTIONS");
    r.global.as_mut().unwrap().work_limit = 1_000_000;
    r.global.as_mut().unwrap().contexts.remove(&0);
    assert_eq!(evaluate(&r).unwrap_err().code, "RESTRICTIONS");
}

#[test]
fn no_histories_never_certifies_a_vacuous_fact_or_creates_a_repair() {
    let mut r = request(vec![]);
    r.global = Some(global(3, vec![0, 0]));
    assert_eq!(evaluate(&r).unwrap_err().code, "LOCAL_REPORTS");
    r.global = None;
    let result = evaluate(&r).unwrap();
    assert!(result.profiles.is_empty());
    assert_eq!(result.repair.unwrap().partitions, vec![Vec::<usize>::new()]);
}

#[test]
fn uniform_unavailability_is_not_a_certified_answer() {
    let mut r = request(vec![history("a", &["a"]), history("b", &["b"])]);
    r.questions.push(ProtectedQuestion {
        id: "invalid form".into(),
        question: Question::Derivable(PrimitiveInstance {
            form: 1,
            args: vec![0],
        }),
    });
    r.global = Some(global(5, vec![1, 0]));
    assert_eq!(
        evaluate(&r).unwrap().global.unwrap().fact,
        Fact::Unavailable
    );
    r.questions[0].question = Question::HasDatum("a".repeat(257));
    assert_eq!(evaluate(&r).unwrap_err().code, "BOUNDS");
}
