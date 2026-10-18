//! A bounded, task-bound encoding experiment. AuthorityEffect: None.
//!
//! Candidates are integer quadratics with each coefficient in [-2, 2].
//! The question is f' = b0 + b1*x and f(0) = v in Z[x]. Cochain closure
//! checks representation consistency; only the direct checker checks this
//! question. Gamma2 arithmetic is delegated to its canonical functional.

use std::collections::{BTreeMap, BTreeSet};

use omega_category_theory::finite_report_query::{ReportQueryDecision, ReportQueryProblem};
use omega_functional::gamma2::Gamma2Functional;
use serde::{Deserialize, Serialize};
use serde_json::{json, Value};
use sha2::{Digest, Sha256};

pub const DOMAIN: &str = "integer_quadratic_antiderivative_at_zero_v1";
pub const BOUND: i64 = 2;
pub const MAX_REPORT_BYTES: usize = 2048;

/// Detect a stale local build when replaying the pinned source snapshot.
/// This is build provenance under a trusted compiler/executable, not authentication.
pub fn compiled_source_sha256() -> BTreeMap<&'static str, String> {
    let inputs: &[(&str, &[u8])] = &[
        (
            "omega_engine/crates_rs/omega_wdp/src/question_preserving_encoding.rs",
            include_bytes!("question_preserving_encoding.rs"),
        ),
        (
            "omega_engine/crates_rs/omega_wdp/src/examples/question_preserving_encoding.rs",
            include_bytes!("examples/question_preserving_encoding.rs"),
        ),
        (
            "omega_engine/crates_rs/tests/omega_wdp/test_question_preserving_encoding.rs",
            include_bytes!(concat!(
                env!("CARGO_MANIFEST_DIR"),
                "/../tests/omega_wdp/test_question_preserving_encoding.rs"
            )),
        ),
        (
            "omega_engine/crates_rs/omega_category_theory/src/finite_report_query.rs",
            include_bytes!("../../omega_category_theory/src/finite_report_query.rs"),
        ),
        (
            "omega_engine/crates_rs/omega_functional/src/gamma2.rs",
            include_bytes!("../../omega_functional/src/gamma2.rs"),
        ),
        (
            "omega_engine/crates_rs/Cargo.lock",
            include_bytes!("../../Cargo.lock"),
        ),
    ];
    inputs
        .iter()
        .map(|(name, bytes)| (*name, hex::encode(Sha256::digest(bytes))))
        .collect()
}

#[derive(Clone, Copy, Debug, PartialEq, Eq, Serialize, Deserialize)]
#[serde(deny_unknown_fields)]
pub struct Task {
    pub derivative: [i64; 2],
    pub value_at_zero: i64,
}

#[derive(Clone, Copy, Debug, PartialEq, Eq, Serialize)]
#[serde(rename_all = "SCREAMING_SNAKE_CASE")]
pub enum Refusal {
    MalformedReport,
    SchemaMismatch,
    TaskOutOfDomain,
    TaskMismatch,
    CandidateOutOfDomain,
    EdgeOutOfDomain,
    NonClosedReport,
    FunctionalRefusal,
    ExperimentInvariant,
}

#[derive(Clone, Debug, PartialEq, Eq, Serialize, Deserialize)]
#[serde(deny_unknown_fields)]
pub struct DirectReport {
    pub schema_version: u8,
    pub domain: String,
    pub task: Task,
    pub coefficients: [i64; 3],
}

#[derive(Clone, Debug, PartialEq, Eq, Serialize, Deserialize)]
#[serde(deny_unknown_fields)]
pub struct CochainReport {
    pub schema_version: u8,
    pub domain: String,
    pub task: Task,
    pub anchor: i64,
    /// Fixed orientations 0->1, 1->2, 2->0 on the declared filled triangle.
    pub edges: [i64; 3],
}

fn in_range(value: i64, bound: i64) -> bool {
    (-bound..=bound).contains(&value)
}

pub fn validate_task(task: Task) -> Result<(), Refusal> {
    if !in_range(task.value_at_zero, BOUND)
        || !in_range(task.derivative[0], BOUND)
        || !in_range(task.derivative[1], 2 * BOUND)
    {
        return Err(Refusal::TaskOutOfDomain);
    }
    Ok(())
}

fn validate_candidate(candidate: [i64; 3]) -> Result<(), Refusal> {
    if candidate.iter().any(|&c| !in_range(c, BOUND)) {
        return Err(Refusal::CandidateOutOfDomain);
    }
    Ok(())
}

/// The sole semantic checker in this profile: equality of derivative
/// coefficients and the value at zero. Bounds precede arithmetic.
pub fn check(task: Task, candidate: [i64; 3]) -> Result<bool, Refusal> {
    validate_task(task)?;
    validate_candidate(candidate)?;
    let tests = [
        candidate[0] == task.value_at_zero,
        candidate[1] == task.derivative[0],
        2 * candidate[2] == task.derivative[1],
    ];
    Ok(tests.into_iter().all(|equal| equal))
}

pub fn encode_direct(task: Task, candidate: [i64; 3]) -> Result<DirectReport, Refusal> {
    validate_task(task)?;
    validate_candidate(candidate)?;
    Ok(DirectReport {
        schema_version: 1,
        domain: DOMAIN.to_owned(),
        task,
        coefficients: candidate,
    })
}

/// Representation map, not a defect functional or a correctness decision.
pub fn encode_cochain(task: Task, candidate: [i64; 3]) -> Result<CochainReport, Refusal> {
    validate_task(task)?;
    validate_candidate(candidate)?;
    let [a, b, c] = candidate;
    Ok(CochainReport {
        schema_version: 1,
        domain: DOMAIN.to_owned(),
        task,
        anchor: a,
        edges: [b - a, c - b, a - c],
    })
}

fn header(schema: u8, domain: &str, declared: Task, expected: Task) -> Result<(), Refusal> {
    validate_task(expected)?;
    if schema != 1 || domain != DOMAIN {
        return Err(Refusal::SchemaMismatch);
    }
    if declared != expected {
        return Err(Refusal::TaskMismatch);
    }
    Ok(())
}

fn decode<T: serde::de::DeserializeOwned>(wire: &str) -> Result<T, Refusal> {
    if wire.len() > MAX_REPORT_BYTES {
        return Err(Refusal::MalformedReport);
    }
    serde_json::from_str(wire).map_err(|_| Refusal::MalformedReport)
}

pub fn parse_direct(expected: Task, wire: &str) -> Result<[i64; 3], Refusal> {
    let report: DirectReport = decode(wire)?;
    header(report.schema_version, &report.domain, report.task, expected)?;
    validate_candidate(report.coefficients)?;
    Ok(report.coefficients)
}

pub fn parse_cochain(expected: Task, wire: &str) -> Result<[i64; 3], Refusal> {
    let report: CochainReport = decode(wire)?;
    header(report.schema_version, &report.domain, report.task, expected)?;
    if !in_range(report.anchor, BOUND) {
        return Err(Refusal::CandidateOutOfDomain);
    }
    if report.edges.iter().any(|&e| !in_range(e, 2 * BOUND)) {
        return Err(Refusal::EdgeOutOfDomain);
    }
    let closure =
        Gamma2Functional::checked_face(report.edges).map_err(|_| Refusal::FunctionalRefusal)?;
    if closure != 0 {
        return Err(Refusal::NonClosedReport);
    }
    let c0 = report.anchor;
    let c1 = c0 + report.edges[0];
    let c2 = c1 + report.edges[1];
    let candidate = [c0, c1, c2];
    validate_candidate(candidate)?;
    Ok(candidate)
}

pub fn verify_direct(expected: Task, wire: &str) -> Result<bool, Refusal> {
    check(expected, parse_direct(expected, wire)?)
}

pub fn verify_cochain(expected: Task, wire: &str) -> Result<bool, Refusal> {
    check(expected, parse_cochain(expected, wire)?)
}

/// Algebraic proposal using the supplied derivative equations. This is not
/// acceptance; every returned proposal is passed to the independent checker.
pub fn direct_proposal(task: Task) -> Result<Option<[i64; 3]>, Refusal> {
    validate_task(task)?;
    if task.derivative[1] % 2 != 0 {
        return Ok(None);
    }
    Ok(Some([
        task.value_at_zero,
        task.derivative[0],
        task.derivative[1] / 2,
    ]))
}

/// The same equations solved in anchored edge coordinates. No invocation of
/// the direct proposal routine, checker, or search result constructs this.
pub fn cochain_proposal(task: Task) -> Result<Option<CochainReport>, Refusal> {
    validate_task(task)?;
    if task.derivative[1] % 2 != 0 {
        return Ok(None);
    }
    let anchor = task.value_at_zero;
    let e01 = task.derivative[0] - anchor;
    let e12 = task.derivative[1] / 2 - task.derivative[0];
    let e20 = anchor - task.derivative[1] / 2;
    Ok(Some(CochainReport {
        schema_version: 1,
        domain: DOMAIN.to_owned(),
        task,
        anchor,
        edges: [e01, e12, e20],
    }))
}

pub fn candidates() -> Vec<[i64; 3]> {
    let mut rows = Vec::new();
    for a in -BOUND..=BOUND {
        for b in -BOUND..=BOUND {
            for c in -BOUND..=BOUND {
                rows.push([a, b, c]);
            }
        }
    }
    rows
}

fn factorable(reports: Vec<Vec<i64>>, answers: &[bool]) -> Result<bool, Refusal> {
    let source: Vec<usize> = (0..answers.len()).collect();
    let codomain: Vec<Vec<i64>> = reports
        .iter()
        .cloned()
        .collect::<BTreeSet<_>>()
        .into_iter()
        .collect();
    let report_rows: Vec<_> = source.iter().copied().zip(reports).collect();
    let query_rows: Vec<_> = source
        .iter()
        .copied()
        .zip(answers.iter().copied())
        .collect();
    let problem = ReportQueryProblem::new(
        &source,
        &codomain,
        &[false, true],
        &report_rows,
        &query_rows,
    )
    .map_err(|_| Refusal::ExperimentInvariant)?;
    let decision = problem.decide();
    problem
        .verify_decision(&decision)
        .map_err(|_| Refusal::ExperimentInvariant)?;
    Ok(matches!(decision, ReportQueryDecision::Factorable(_)))
}

fn wire<T: Serialize>(value: &T) -> Result<String, Refusal> {
    serde_json::to_string(value).map_err(|_| Refusal::ExperimentInvariant)
}

fn enumerate_then_check(
    task: Task,
    carrier: &[[i64; 3]],
) -> Result<(Option<[i64; 3]>, usize), Refusal> {
    let mut calls = 0;
    for &candidate in carrier {
        calls += 1;
        if check(task, candidate)? {
            return Ok((Some(candidate), calls));
        }
    }
    Ok((None, calls))
}

/// Exhaustive reproducible experiment, including unsuccessful tasks. The
/// exhaustive audit is accounted separately from each strategy's workload.
pub fn experiment() -> Result<Value, Refusal> {
    let carrier = candidates();
    let mut rows = Vec::new();
    let mut total_enumeration_checks = 0_usize;
    let mut solved = 0_usize;
    let mut unanchored_collisions = 0_usize;
    let mut closure_only_collisions = 0_usize;
    let mut closed_wrong_pairs = 0_usize;
    for initial in -BOUND..=BOUND {
        for constant in -BOUND..=BOUND {
            for slope in -2 * BOUND..=2 * BOUND {
                let task = Task {
                    derivative: [constant, slope],
                    value_at_zero: initial,
                };
                let answers: Vec<bool> = carrier
                    .iter()
                    .map(|&c| check(task, c))
                    .collect::<Result<_, _>>()?;
                let solutions: Vec<_> = carrier
                    .iter()
                    .copied()
                    .zip(&answers)
                    .filter_map(|(c, &ok)| ok.then_some(c))
                    .collect();
                if solutions.len() > 1 {
                    return Err(Refusal::ExperimentInvariant);
                }
                let expected = solutions.first().copied();
                let (enumerated, enumeration_checks) = enumerate_then_check(task, &carrier)?;
                if enumerated != expected {
                    return Err(Refusal::ExperimentInvariant);
                }
                total_enumeration_checks += enumeration_checks;

                let mut unanchored = Vec::new();
                let mut anchored = Vec::new();
                let mut closure_reports = Vec::new();
                for (&candidate, &answer) in carrier.iter().zip(&answers) {
                    let encoded = encode_cochain(task, candidate)?;
                    if parse_cochain(task, &wire(&encoded)?)? != candidate
                        || verify_cochain(task, &wire(&encoded)?)? != answer
                    {
                        return Err(Refusal::ExperimentInvariant);
                    }
                    unanchored.push(encoded.edges.to_vec());
                    let closure = Gamma2Functional::checked_face(encoded.edges)
                        .map_err(|_| Refusal::FunctionalRefusal)?;
                    closure_reports.push(vec![
                        i64::try_from(closure).map_err(|_| Refusal::ExperimentInvariant)?
                    ]);
                    anchored.push(vec![
                        encoded.anchor,
                        encoded.edges[0],
                        encoded.edges[1],
                        encoded.edges[2],
                    ]);
                    if !answer {
                        closed_wrong_pairs += 1;
                    }
                }
                let unanchored_ok = factorable(unanchored, &answers)?;
                let closure_ok = factorable(closure_reports, &answers)?;
                if !factorable(anchored, &answers)? {
                    return Err(Refusal::ExperimentInvariant);
                }
                unanchored_collisions += usize::from(!unanchored_ok);
                closure_only_collisions += usize::from(!closure_ok);

                let direct = direct_proposal(task)?;
                if direct != expected {
                    return Err(Refusal::ExperimentInvariant);
                }
                if let Some(candidate) = direct {
                    if !verify_direct(task, &wire(&encode_direct(task, candidate)?)?)? {
                        return Err(Refusal::ExperimentInvariant);
                    }
                }
                let cochain = cochain_proposal(task)?;
                let decoded = cochain
                    .as_ref()
                    .map(|r| parse_cochain(task, &wire(r)?))
                    .transpose()?;
                if decoded != expected {
                    return Err(Refusal::ExperimentInvariant);
                }
                if let Some(report) = &cochain {
                    if !verify_cochain(task, &wire(report)?)? {
                        return Err(Refusal::ExperimentInvariant);
                    }
                }
                let checks = usize::from(expected.is_some());
                solved += checks;
                rows.push(json!({"task":task,"solution":expected,"enumeration_checker_calls":enumeration_checks,
                    "direct_reconstruction_checker_calls":checks,"cochain_reconstruction_checker_calls":checks,
                    "unanchored_factorable":unanchored_ok,"closure_only_factorable":closure_ok}));
            }
        }
    }
    let zero = Task {
        derivative: [0, 0],
        value_at_zero: 0,
    };
    let correct = encode_cochain(zero, [0, 0, 0])?;
    let wrong = encode_cochain(zero, [1, 1, 1])?;
    let mut corrupt = correct.clone();
    corrupt.edges[2] = 1;
    let mut wrong_task = correct.clone();
    wrong_task.task.value_at_zero = 1;
    let controls = json!({
        "same_unanchored_report":correct.edges == wrong.edges,
        "correct_accepted":verify_cochain(zero,&wire(&correct)?)?,
        "coherent_wrong_rejected":!verify_cochain(zero,&wire(&wrong)?)?,
        "corrupt_edge_refusal":parse_cochain(zero,&wire(&corrupt)?).err(),
        "changed_task_refusal":parse_cochain(zero,&wire(&wrong_task)?).err()
    });
    if correct.edges != wrong.edges
        || !check(zero, [0, 0, 0])?
        || check(zero, [1, 1, 1])?
        || parse_cochain(zero, &wire(&corrupt)?) != Err(Refusal::NonClosedReport)
        || parse_cochain(zero, &wire(&wrong_task)?) != Err(Refusal::TaskMismatch)
    {
        return Err(Refusal::ExperimentInvariant);
    }
    Ok(json!({
        "schema_version":1,"domain":DOMAIN,"authority_effect":"None",
        "compiled_source_sha256":compiled_source_sha256(),
        "coefficient_bound":BOUND,"candidate_count":carrier.len(),"task_count":rows.len(),
        "satisfiable_tasks":solved,"unsatisfiable_tasks":rows.len()-solved,
        "audit_task_candidate_pairs":rows.len()*carrier.len(),
        "audit_work_in_strategy_counts":false,
        "unanchored_colliding_tasks":unanchored_collisions,
        "closure_only_colliding_tasks":closure_only_collisions,
        "closed_wrong_task_candidate_pairs":closed_wrong_pairs,
        "strategies":[
            {"name":"enumerate_then_check","checker_calls":total_enumeration_checks,
                "checker_coefficient_comparisons":3*total_enumeration_checks,
                "report_parses":0,"candidate_integer_fields_sent":0,"gamma2_evaluations":0},
            {"name":"direct_reconstruct_then_check","checker_calls":solved,
                "checker_coefficient_comparisons":3*solved,
                "report_parses":solved,"candidate_integer_fields_sent":3*solved,"gamma2_evaluations":0},
            {"name":"cochain_reconstruct_then_check","checker_calls":solved,
                "checker_coefficient_comparisons":3*solved,
                "report_parses":solved,"candidate_integer_fields_sent":4*solved,"gamma2_evaluations":solved}
        ],
        "cost_scope":"Logical single-run strategy counts; exhaustive audit and duplicate diagnostic assertions are separate. Task headers, proposal arithmetic, JSON byte costs and wall time are not converted to a common cost.",
        "conclusion":"Both reconstruction routes reduce checker calls against enumeration; the cochain route has no checker-call advantage over direct reconstruction and adds parsing/closure data.",
        "controls":controls,"tasks":rows
    }))
}
