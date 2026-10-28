
use crate::genesis_construction::{ConstructionError, ConstructionLimits, GenesisConstruction};
use crate::genesis_primitive_execution::{PrimitiveEvent, PrimitiveInstance};
use crate::genesis_questions::{
    Answer, History, Presentation, ProtectedQuestion, Question, QuestionLimits,
};
use tfqm_category_theory::finite_question_family::{factor_tables, FiniteQuestionFamily};
use tfqm_category_theory::finite_report_query::ReportQueryDecision;
use tfqm_category_theory::finite_report_repair::{
    repair_report, replay_repair_prefix, verify_repair, RepairLimits,
};
use omega_ooutwire_primitives::{
    event::Event,
    mark::{Mark, Pair},
    token::Token,
};
use omega_types::AuthorityEffect;
use serde::{Deserialize, Serialize};
use sha2::{Digest, Sha256};
use std::collections::BTreeSet;

pub const REQUEST_SCHEMA: &str = "omega.genesis.report-request.v1";
pub const RESULT_SCHEMA: &str = "omega.genesis.report-result.v1";
const SOURCE: &[u8] = include_bytes!(concat!(env!("CARGO_MANIFEST_DIR"),
    "/fixtures/model.py"));
const OBSERVATION_SOURCE: &[u8] = include_bytes!(concat!(env!("CARGO_MANIFEST_DIR"),
    "/fixtures/observe.py"));

pub fn source_sha256() -> String {
    let mut digest = Sha256::new();
    digest.update(b"omega.genesis.source-bundle.v1\0");
    for source in [SOURCE, OBSERVATION_SOURCE] {
        digest.update((source.len() as u64).to_be_bytes());
        digest.update(source);
    }
    format!("{:x}", digest.finalize())
}

#[derive(Clone, Debug, PartialEq, Eq, Serialize, Deserialize)]
#[serde(deny_unknown_fields)]
pub struct NamedHistory {
    pub id: String,
    pub events: Vec<PrimitiveEvent>,
}

#[derive(Clone, Debug, PartialEq, Eq, Serialize, Deserialize)]
#[serde(deny_unknown_fields)]
pub struct GlobalRequest {
    pub observed_columns: Vec<usize>,
    pub contexts: BTreeSet<u64>,
    pub cover: Vec<u64>,
    pub locals: Vec<usize>,
    pub fact_column: usize,
    pub work_limit: usize,
}

#[derive(Clone, Debug, PartialEq, Eq, Serialize, Deserialize)]
#[serde(deny_unknown_fields)]
pub struct RepairAllowance {
    pub max_steps: usize,
    pub max_pair_checks: usize,
}

#[derive(Clone, Debug, PartialEq, Eq, Serialize, Deserialize)]
#[serde(deny_unknown_fields)]
pub struct Request {
    pub schema_version: String,
    pub source_sha256: String,
    pub histories: Vec<NamedHistory>,
    pub questions: Vec<ProtectedQuestion>,
    pub continuations: Vec<NamedHistory>,
    pub report: Vec<String>,
    pub global: Option<GlobalRequest>,
    pub repair: Option<RepairAllowance>,
}

#[derive(Clone, Debug, PartialEq, Eq, Serialize, Deserialize)]
#[serde(deny_unknown_fields)]
pub struct State {
    pub data: Vec<String>,
    pub forms: Vec<usize>,
    pub instances: Vec<PrimitiveInstance>,
    pub rules: Vec<usize>,
    pub requirements: Vec<(usize, usize)>,
}

#[derive(Clone, Debug, PartialEq, Eq, Serialize, Deserialize)]
#[serde(tag = "kind", rename_all = "snake_case", deny_unknown_fields)]
pub enum Decision<R, A> {
    Decoder {
        entries: Vec<(R, A)>,
    },
    Collision {
        first: usize,
        second: usize,
        report: R,
        first_answer: A,
        second_answer: A,
    },
}

fn decision<R, A>(value: ReportQueryDecision<usize, R, A>) -> Decision<R, A> {
    match value {
        ReportQueryDecision::Factorable(c) => Decision::Decoder {
            entries: c.decoder.into_iter().collect(),
        },
        ReportQueryDecision::Collision(c) => Decision::Collision {
            first: c.first,
            second: c.second,
            report: c.report,
            first_answer: c.first_query,
            second_answer: c.second_query,
        },
    }
}

#[derive(Clone, Debug, PartialEq, Eq, Serialize, Deserialize)]
#[serde(deny_unknown_fields)]
pub struct Operation {
    pub continuation: String,
    pub decision: Decision<usize, Option<Vec<Answer>>>,
}

#[derive(Clone, Debug, PartialEq, Eq, Serialize, Deserialize)]
#[serde(tag = "kind", rename_all = "snake_case", deny_unknown_fields)]
pub enum Fact {
    NoGlobalExtension,
    Undetermined { first: usize, second: usize },
    Unavailable,
    Certified { answer: Answer },
}

#[derive(Clone, Debug, PartialEq, Eq, Serialize, Deserialize)]
#[serde(deny_unknown_fields)]
pub struct GlobalResult {
    pub profiles: Vec<(u64, Vec<Vec<Answer>>)>,
    pub histories: Vec<usize>,
    pub fact: Fact,
}

#[derive(Clone, Debug, PartialEq, Eq, Serialize, Deserialize)]
#[serde(deny_unknown_fields)]
pub struct RepairResult {
    pub steps: Vec<(usize, usize, usize)>,
    pub partitions: Vec<Vec<usize>>,
    pub ranks: Vec<usize>,
    pub global_rechecks: Vec<Option<GlobalResult>>,
}

#[derive(Clone, Debug, PartialEq, Eq, Serialize, Deserialize)]
#[serde(deny_unknown_fields)]
pub struct ResultPacket {
    pub schema_version: String,
    pub authority_effect: AuthorityEffect,
    pub source_sha256: String,
    pub request_sha256: String,
    pub states: Vec<State>,
    pub answers: Vec<Vec<Answer>>,
    pub profiles: Vec<Vec<Answer>>,
    pub class_of: Vec<usize>,
    pub report: Decision<String, Vec<Answer>>,
    pub operations: Vec<Operation>,
    pub global: Option<GlobalResult>,
    pub repair: Option<RepairResult>,
}

#[derive(Clone, Debug, PartialEq, Eq, Serialize, Deserialize, thiserror::Error)]
#[error("{code}: {detail}")]
#[serde(deny_unknown_fields)]
pub struct Refusal {
    pub code: String,
    pub detail: String,
}

fn refuse(code: &str, detail: impl std::fmt::Debug) -> Refusal {
    Refusal {
        code: code.into(),
        detail: format!("{detail:?}"),
    }
}

pub fn request_sha256(request: &Request) -> Result<String, Refusal> {
    let bytes = serde_json::to_vec(request).map_err(|e| refuse("WIRE", e))?;
    let mut digest = Sha256::new();
    digest.update(b"omega.genesis.report-request.v1\0");
    digest.update(bytes);
    Ok(format!("{:x}", digest.finalize()))
}

fn native(event: &PrimitiveEvent) -> Event {
    match event {
        PrimitiveEvent::Supply { token } => Event::Supply(Token::new(token)),
        PrimitiveEvent::AdmitDatum { token } => Event::AdmitDatum(Token::new(token)),
        PrimitiveEvent::AdmitForm { arity } => Event::AdmitForm(*arity),
        PrimitiveEvent::AdmitInst { form, args } => {
            Event::AdmitInst(*form, args.iter().copied().map(Mark).collect())
        }
        PrimitiveEvent::AdmitRuleAll { form } => Event::AdmitRuleAll(*form),
        PrimitiveEvent::Impose { i, j } => Event::Impose(Pair {
            i: Mark(*i),
            j: Mark(*j),
        }),
    }
}

fn validate(request: &Request) -> Result<(), Refusal> {
    if request.schema_version != REQUEST_SCHEMA {
        return Err(refuse("SCHEMA", "unsupported profile"));
    }
    if request.source_sha256 != source_sha256() {
        return Err(refuse(
            "SOURCE",
            "original source digest differs from compiled pin",
        ));
    }
    let width = request
        .continuations
        .len()
        .checked_mul(request.questions.len() + 1);
    if request.histories.len() > 64
        || request.questions.len() > 15
        || request.continuations.is_empty()
        || request.continuations.len() > 8
        || width.is_none_or(|n| n > 64)
        || request.report.len() != request.histories.len()
        || !request.continuations[0].events.is_empty()
    {
        return Err(refuse(
            "BOUNDS",
            "64 histories/columns, 15 questions, 1..8 words starting with empty",
        ));
    }
    let mut ids = BTreeSet::new();
    for word in &request.continuations {
        if word.id.trim().is_empty() || !ids.insert(&word.id) {
            return Err(refuse("IDENTITY", "duplicate or empty continuation id"));
        }
    }
    for word in request.histories.iter().chain(&request.continuations) {
        if word.id.len() > 128 || word.events.len() > 128 {
            return Err(refuse("BOUNDS", "history/word size"));
        }
        for event in &word.events {
            let valid = match event {
                PrimitiveEvent::Supply { token } | PrimitiveEvent::AdmitDatum { token } => {
                    token.len() <= 256
                }
                PrimitiveEvent::AdmitInst { args, .. } => args.len() <= 128,
                _ => true,
            };
            if !valid {
                return Err(refuse("BOUNDS", "event payload size"));
            }
        }
    }
    if request.report.iter().any(|x| x.len() > 128)
        || request.questions.iter().any(|q| q.id.len() > 128)
    {
        return Err(refuse("BOUNDS", "report/question identity size"));
    }
    for q in &request.questions {
        let bounded = match &q.question {
            Question::HasDatum(token) => token.len() <= 256,
            Question::Derivable(instance) => instance.args.len() <= 128,
            _ => true,
        };
        if !bounded {
            return Err(refuse("BOUNDS", "question payload size"));
        }
    }
    if let Some(r) = &request.repair {
        if r.max_steps > 64 || r.max_pair_checks > 1_000_000 {
            return Err(refuse("BOUNDS", "repair allowance"));
        }
    }
    Ok(())
}

fn presentation(request: &Request) -> Result<Presentation, Refusal> {
    Presentation::new(
        request
            .histories
            .iter()
            .map(|h| History {
                id: h.id.clone(),
                events: h.events.iter().map(native).collect(),
            })
            .collect(),
        request.questions.clone(),
        QuestionLimits {
            max_histories: 64,
            max_questions: 15,
            max_answer_cells: 960,
            construction: ConstructionLimits {
                max_events: 384,
                ..Default::default()
            },
        },
    )
    .map_err(|e| refuse("ADMISSION", e))
}

fn extend(
    history: &GenesisConstruction,
    events: &[Event],
) -> Result<Option<GenesisConstruction>, Refusal> {
    match history.extend(events) {
        Ok(value) => Ok(Some(value)),
        Err(ConstructionError::Admission { .. } | ConstructionError::MissingLiteralRoot) => {
            Ok(None)
        }
        Err(error) => Err(refuse("REPLAY", error)),
    }
}

fn profile(
    history: &GenesisConstruction,
    words: &[Vec<Event>],
    questions: &[ProtectedQuestion],
) -> Result<Vec<Answer>, Refusal> {
    let mut row = Vec::new();
    for word in words {
        let next = extend(history, word)?;
        row.push(Answer::Boolean(next.is_some()));
        for q in questions {
            row.push(match &next {
                Some(h) => q.question.answer(h).map_err(|e| refuse("QUESTION", e))?,
                None => Answer::Unavailable,
            });
        }
    }
    Ok(row)
}

fn family(
    presentation: &Presentation,
    words: &[Vec<Event>],
) -> Result<FiniteQuestionFamily<Answer>, Refusal> {
    let rows = presentation
        .constructions()
        .iter()
        .map(|h| profile(h, words, presentation.questions()))
        .collect::<Result<_, _>>()?;
    FiniteQuestionFamily::new(words.len() * (presentation.questions().len() + 1), rows)
        .map_err(|e| refuse("FAMILY", e))
}

fn global(
    family: &FiniteQuestionFamily<Answer>,
    request: &GlobalRequest,
) -> Result<GlobalResult, Refusal> {
    let columns = &request.observed_columns;
    if columns.is_empty()
        || columns.len() > 63
        || request.fact_column >= family.question_count()
        || columns.iter().copied().collect::<BTreeSet<_>>().len() != columns.len()
        || columns.iter().any(|&c| c >= family.question_count())
        || request.contexts.len() > 32
        || request.cover.len() > 32
        || request.work_limit > 1_000_000
    {
        return Err(refuse("GLOBAL_INPUT", "invalid columns or work allowance"));
    }
    let observed = FiniteQuestionFamily::new(
        columns.len(),
        family
            .answers()
            .iter()
            .map(|row| columns.iter().map(|&c| row[c].clone()).collect())
            .collect(),
    )
    .map_err(|e| refuse("GLOBAL_INPUT", e))?;
    let site = observed
        .report_site(&request.contexts, request.work_limit)
        .map_err(|e| refuse("RESTRICTIONS", e))?;
    let full = (1u64 << columns.len()) - 1;
    let fiber = site
        .presheaf()
        .descent_fiber(full, &request.cover, &request.locals)
        .map_err(|e| refuse("LOCAL_REPORTS", e))?;
    let fact = match fiber.global_sections.first() {
        None => Fact::NoGlobalExtension,
        Some(&first) => {
            let answer = &family.answers()[first][request.fact_column];
            if let Some(&second) = fiber
                .global_sections
                .iter()
                .find(|&&i| family.answers()[i][request.fact_column] != *answer)
            {
                Fact::Undetermined { first, second }
            } else if *answer == Answer::Unavailable {
                Fact::Unavailable
            } else {
                Fact::Certified {
                    answer: answer.clone(),
                }
            }
        }
    };
    Ok(GlobalResult {
        profiles: site
            .profiles()
            .iter()
            .map(|(&k, v)| (k, v.clone()))
            .collect(),
        histories: fiber.global_sections,
        fact,
    })
}

fn requested_global(
    family: &FiniteQuestionFamily<Answer>,
    request: &Request,
) -> Result<Option<GlobalResult>, Refusal> {
    request
        .global
        .as_ref()
        .map(|g| global(family, g))
        .transpose()
}

pub fn evaluate(request: &Request) -> Result<ResultPacket, Refusal> {
    validate(request)?;
    let presentation = presentation(request)?;
    let words: Vec<Vec<Event>> = request
        .continuations
        .iter()
        .map(|w| w.events.iter().map(native).collect())
        .collect();
    let family = family(&presentation, &words)?;
    let quotient = family.quotient();
    let report = decision(
        family
            .factor_report(&request.report)
            .map_err(|e| refuse("REPORT", e))?
            .decide(),
    );
    let mut operations = Vec::new();
    for (index, word) in words.iter().enumerate() {
        let targets = presentation
            .constructions()
            .iter()
            .map(|h| {
                extend(h, word)?
                    .map(|next| profile(&next, &words, presentation.questions()))
                    .transpose()
            })
            .collect::<Result<Vec<_>, Refusal>>()?;
        operations.push(Operation {
            continuation: request.continuations[index].id.clone(),
            decision: decision(
                factor_tables(&quotient.class_of, &targets)
                    .map_err(|e| refuse("OPERATION", e))?
                    .decide(),
            ),
        });
    }
    let global_result = requested_global(&family, request)?;
    let repair = request
        .repair
        .as_ref()
        .map(|allowance| {
            let limits = RepairLimits {
                max_rows: 64,
                max_questions: 64,
                max_steps: allowance.max_steps,
                max_pair_checks: allowance.max_pair_checks,
            };
            let cert =
                repair_report(&family, &request.report, limits).map_err(|e| refuse("REPAIR", e))?;
            verify_repair(&family, &request.report, &cert, limits)
                .map_err(|e| refuse("REPAIR_REPLAY", e))?;
            let partitions = replay_repair_prefix(&family, &request.report, &cert.steps, limits)
                .map_err(|e| refuse("REPAIR_REPLAY", e))?;
            let final_count = cert.class_of.iter().collect::<BTreeSet<_>>().len();
            let ranks = partitions
                .iter()
                .map(|p| final_count - p.iter().collect::<BTreeSet<_>>().len())
                .collect();
            let global_rechecks = partitions
                .iter()
                .map(|_| {
                    let original = self::presentation(request)?;
                    requested_global(&self::family(&original, &words)?, request)
                })
                .collect::<Result<Vec<_>, Refusal>>()?;
            Ok::<_, Refusal>(RepairResult {
                steps: cert
                    .steps
                    .iter()
                    .map(|s| (s.first, s.second, s.question))
                    .collect(),
                partitions,
                ranks,
                global_rechecks,
            })
        })
        .transpose()?;
    let states = presentation
        .constructions()
        .iter()
        .map(|h| {
            let s = h.interpreted();
            State {
                data: s.data().to_vec(),
                forms: s.forms().to_vec(),
                instances: s.instances().iter().cloned().collect(),
                rules: s.rules().iter().copied().collect(),
                requirements: s.requirements().iter().copied().collect(),
            }
        })
        .collect();
    Ok(ResultPacket {
        schema_version: RESULT_SCHEMA.into(),
        authority_effect: AuthorityEffect::None,
        source_sha256: source_sha256(),
        request_sha256: request_sha256(request)?,
        states,
        answers: family.answers().to_vec(),
        profiles: quotient.profiles,
        class_of: quotient.class_of,
        report,
        operations,
        global: global_result,
        repair,
    })
}

pub fn verify(expected: &Request, candidate: &ResultPacket) -> Result<(), Refusal> {
    if evaluate(expected)? != *candidate {
        return Err(refuse("CANDIDATE", "source-bound replay differs"));
    }
    Ok(())
}

#[cfg(test)]
mod tests;
