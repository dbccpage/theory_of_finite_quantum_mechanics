
use crate::genesis_computation::{BridgeError, CheckedBooleanPacket, SourceBooleanPacket};
use crate::genesis_construction::{ConstructionError, ConstructionLimits, GenesisConstruction};
use crate::genesis_primitive_execution::{PrimitiveExecutionError, PrimitiveInstance};
use tfqm_category_theory::finite_question_family::{
    factor_tables, FiniteQuestionFamily, QuestionFamilyError, QuestionQuotient, QuestionReportSite,
};
use tfqm_category_theory::finite_report_descent::DescentFiber;
use tfqm_category_theory::finite_report_query::ReportQueryDecision;
use tfqm_finite_probability::error::ClassicalShadowError;
use tfqm_finite_probability::log_form::{shannon_entropy_form_with_bound, LogForm, LogFormError};
use tfqm_finite_probability::simplex::ProbabilitySimplex;
use tfqm_finite_probability::stochastic_map::StochasticMap;
use omega_ooutwire_primitives::event::Event;
use serde::{Deserialize, Serialize};
use std::collections::BTreeSet;

#[derive(Debug, Clone, PartialEq, Eq)]
pub enum QuestionError {
    InvalidIdentity,
    Budget,
    Source(ConstructionError),
    Primitive(PrimitiveExecutionError),
    Family(QuestionFamilyError),
    Probability(ClassicalShadowError),
    Entropy(LogFormError),
    CertificateMismatch,
    NotBooleanGraph,
    Computation(BridgeError),
}

#[derive(Debug, Clone, PartialEq, Eq)]
pub struct History {
    pub id: String,
    pub events: Vec<Event>,
}

#[derive(Debug, Clone, PartialEq, Eq, Serialize, Deserialize)]
#[serde(
    tag = "kind",
    content = "value",
    rename_all = "snake_case",
    deny_unknown_fields
)]
pub enum Question {
    DatumCount,
    FormCount,
    InstanceCount,
    RuleCount,
    RequirementCount,
    EventCount,
    HasDatum(String),
    Derivable(PrimitiveInstance),
}

#[derive(Debug, Clone, PartialEq, Eq, Serialize, Deserialize)]
#[serde(deny_unknown_fields)]
pub struct ProtectedQuestion {
    pub id: String,
    pub question: Question,
}

#[derive(Debug, Clone, PartialEq, Eq, PartialOrd, Ord, Serialize, Deserialize)]
#[serde(
    tag = "kind",
    content = "value",
    rename_all = "snake_case",
    deny_unknown_fields
)]
pub enum Answer {
    Boolean(bool),
    Count(usize),
    Unavailable,
}

#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub struct QuestionLimits {
    pub max_histories: usize,
    pub max_questions: usize,
    pub max_answer_cells: usize,
    pub construction: ConstructionLimits,
}

impl Default for QuestionLimits {
    fn default() -> Self {
        Self {
            max_histories: 256,
            max_questions: 64,
            max_answer_cells: 16_384,
            construction: ConstructionLimits::default(),
        }
    }
}

#[derive(Debug, Clone, PartialEq, Eq)]
pub struct Presentation {
    histories: Vec<History>,
    questions: Vec<ProtectedQuestion>,
    limits: QuestionLimits,
    constructions: Vec<GenesisConstruction>,
    family: FiniteQuestionFamily<Answer>,
}

#[derive(Debug, Clone, PartialEq, Eq)]
pub struct Report {
    pub values: Vec<String>,
}

#[derive(Debug, Clone, PartialEq, Eq)]
pub struct Certificate {
    pub presentation: Presentation,
    pub report: Report,
    pub decision: ReportQueryDecision<usize, String, Vec<Answer>>,
}

#[derive(Debug, Clone, PartialEq, Eq)]
pub struct ContinuationCertificate {
    pub presentation: Presentation,
    pub suffix: Vec<Event>,
    pub decision: ReportQueryDecision<usize, usize, Option<Vec<Answer>>>,
}

#[derive(Debug, Clone, PartialEq, Eq)]
pub struct GluingRequest {
    pub contexts: BTreeSet<u64>,
    pub work_limit: usize,
    pub target: u64,
    pub cover: Vec<u64>,
    pub locals: Vec<usize>,
}

#[derive(Debug, Clone, PartialEq, Eq)]
pub struct GluingCertificate {
    pub presentation: Presentation,
    pub request: GluingRequest,
    pub fiber: DescentFiber,
}

#[derive(Debug, Clone, PartialEq, Eq)]
pub struct InformationCertificate {
    pub presentation: Presentation,
    pub prior: ProbabilitySimplex,
    pub factor_bound: u32,
    pub quotient_law: ProbabilitySimplex,
    pub history_entropy_nats: LogForm,
    pub protected_entropy_nats: LogForm,
    pub discarded_entropy_nats: LogForm,
}

fn distinct_ids<'a>(ids: impl Iterator<Item = &'a str>) -> bool {
    let mut seen = BTreeSet::new();
    ids.into_iter()
        .all(|id| !id.trim().is_empty() && seen.insert(id))
}

impl Question {
    pub(crate) fn answer(&self, history: &GenesisConstruction) -> Result<Answer, QuestionError> {
        let state = history.interpreted();
        Ok(match self {
            Self::DatumCount => Answer::Count(state.data().len()),
            Self::FormCount => Answer::Count(state.forms().len()),
            Self::InstanceCount => Answer::Count(state.instances().len()),
            Self::RuleCount => Answer::Count(state.rules().len()),
            Self::RequirementCount => Answer::Count(state.requirements().len()),
            Self::EventCount => Answer::Count(history.history().len()),
            Self::HasDatum(token) => Answer::Boolean(state.data().contains(token)),
            Self::Derivable(instance) => match state.derivable(instance) {
                Ok(value) => Answer::Boolean(value),
                Err(PrimitiveExecutionError::InvalidArgument) => Answer::Unavailable,
                Err(error) => return Err(QuestionError::Primitive(error)),
            },
        })
    }
}

impl Presentation {
    pub fn new(
        histories: Vec<History>,
        questions: Vec<ProtectedQuestion>,
        limits: QuestionLimits,
    ) -> Result<Self, QuestionError> {
        if histories.len() > limits.max_histories
            || questions.len() > limits.max_questions
            || histories
                .len()
                .checked_mul(questions.len())
                .is_none_or(|n| n > limits.max_answer_cells)
        {
            return Err(QuestionError::Budget);
        }
        if !distinct_ids(histories.iter().map(|h| h.id.as_str()))
            || !distinct_ids(questions.iter().map(|q| q.id.as_str()))
        {
            return Err(QuestionError::InvalidIdentity);
        }
        let constructions = histories
            .iter()
            .map(|h| {
                GenesisConstruction::pre_genesis_with_limits(limits.construction)
                    .extend(&h.events)
                    .map_err(QuestionError::Source)
            })
            .collect::<Result<Vec<_>, _>>()?;
        let answers = constructions
            .iter()
            .map(|h| questions.iter().map(|q| q.question.answer(h)).collect())
            .collect::<Result<Vec<Vec<_>>, _>>()?;
        let family =
            FiniteQuestionFamily::new(questions.len(), answers).map_err(QuestionError::Family)?;
        Ok(Self {
            histories,
            questions,
            limits,
            constructions,
            family,
        })
    }

    pub fn histories(&self) -> &[History] {
        &self.histories
    }
    pub(crate) fn constructions(&self) -> &[GenesisConstruction] {
        &self.constructions
    }
    pub fn questions(&self) -> &[ProtectedQuestion] {
        &self.questions
    }
    pub fn family(&self) -> &FiniteQuestionFamily<Answer> {
        &self.family
    }
    pub fn quotient(&self) -> QuestionQuotient<Answer> {
        self.family.quotient()
    }

    pub fn boolean_graph(
        &self,
        inputs: &[usize],
        output: usize,
        labels: [String; 2],
    ) -> Result<CheckedBooleanPacket, QuestionError> {
        if inputs.is_empty()
            || inputs.iter().copied().collect::<BTreeSet<_>>().len() != inputs.len()
            || inputs
                .iter()
                .chain(std::iter::once(&output))
                .any(|&q| q >= self.questions.len())
        {
            return Err(QuestionError::NotBooleanGraph);
        }
        let instances = self
            .family
            .answers()
            .iter()
            .map(|row| {
                inputs
                    .iter()
                    .chain(std::iter::once(&output))
                    .map(|&q| match row[q] {
                        Answer::Boolean(value) => Ok(usize::from(value)),
                        _ => Err(QuestionError::NotBooleanGraph),
                    })
                    .collect()
            })
            .collect::<Result<_, _>>()?;
        SourceBooleanPacket {
            datum_labels: labels.to_vec(),
            arity: inputs.len(),
            instances,
        }
        .admit()
        .map_err(QuestionError::Computation)
    }

    pub fn certify_report(&self, report: &Report) -> Result<Certificate, QuestionError> {
        let problem = self
            .family
            .factor_report(&report.values)
            .map_err(QuestionError::Family)?;
        Ok(Certificate {
            presentation: self.clone(),
            report: report.clone(),
            decision: problem.decide(),
        })
    }

    pub fn verify_report(
        &self,
        report: &Report,
        candidate: &Certificate,
    ) -> Result<(), QuestionError> {
        if candidate.presentation != *self || candidate.report != *report {
            return Err(QuestionError::CertificateMismatch);
        }
        self.family
            .factor_report(&report.values)
            .map_err(QuestionError::Family)?
            .verify_decision(&candidate.decision)
            .map_err(|_| QuestionError::CertificateMismatch)
    }

    pub fn continuation(&self, suffix: &[Event]) -> Result<ContinuationCertificate, QuestionError> {
        if suffix.len() > self.limits.construction.max_events {
            return Err(QuestionError::Budget);
        }
        let outcomes = self
            .constructions
            .iter()
            .map(|h| match h.extend(suffix) {
                Ok(after) => self
                    .questions
                    .iter()
                    .map(|q| q.question.answer(&after))
                    .collect::<Result<Vec<_>, _>>()
                    .map(Some),
                Err(
                    ConstructionError::Admission { .. } | ConstructionError::MissingLiteralRoot,
                ) => Ok(None),
                Err(error) => Err(QuestionError::Source(error)),
            })
            .collect::<Result<Vec<_>, _>>()?;
        let decision = factor_tables(&self.quotient().class_of, &outcomes)
            .map_err(QuestionError::Family)?
            .decide();
        Ok(ContinuationCertificate {
            presentation: self.clone(),
            suffix: suffix.to_vec(),
            decision,
        })
    }

    pub fn verify_continuation(
        &self,
        suffix: &[Event],
        candidate: &ContinuationCertificate,
    ) -> Result<(), QuestionError> {
        if *candidate != self.continuation(suffix)? {
            return Err(QuestionError::CertificateMismatch);
        }
        Ok(())
    }

    pub fn report_site(
        &self,
        contexts: &BTreeSet<u64>,
        work_limit: usize,
    ) -> Result<QuestionReportSite<Answer>, QuestionError> {
        self.family
            .report_site(contexts, work_limit)
            .map_err(QuestionError::Family)
    }

    pub fn certify_gluing(
        &self,
        request: &GluingRequest,
    ) -> Result<GluingCertificate, QuestionError> {
        let cover_count = request.cover.len();
        let fiber_work = cover_count.checked_mul(cover_count).and_then(|overlaps| {
            cover_count
                .checked_mul(self.histories.len())
                .and_then(|extensions| overlaps.checked_add(extensions))
        });
        if fiber_work.is_none_or(|n| n > request.work_limit) {
            return Err(QuestionError::Budget);
        }
        let site = self.report_site(&request.contexts, request.work_limit)?;
        let fiber = site
            .presheaf()
            .descent_fiber(request.target, &request.cover, &request.locals)
            .map_err(|e| QuestionError::Family(QuestionFamilyError::Descent(e)))?;
        Ok(GluingCertificate {
            presentation: self.clone(),
            request: request.clone(),
            fiber,
        })
    }

    pub fn verify_gluing(
        &self,
        request: &GluingRequest,
        candidate: &GluingCertificate,
    ) -> Result<(), QuestionError> {
        if *candidate != self.certify_gluing(request)? {
            return Err(QuestionError::CertificateMismatch);
        }
        Ok(())
    }

    pub fn information(
        &self,
        prior: &ProbabilitySimplex,
        factor_bound: u32,
    ) -> Result<InformationCertificate, QuestionError> {
        if prior.n() != self.histories.len() {
            return Err(QuestionError::CertificateMismatch);
        }
        let quotient = self.quotient();
        let channel = StochasticMap::from_function(
            quotient.profiles.len(),
            &quotient.class_of,
            "protected questions",
        )
        .map_err(QuestionError::Probability)?;
        let law = channel.apply(prior).map_err(QuestionError::Probability)?;
        let history_entropy_nats =
            shannon_entropy_form_with_bound(prior, factor_bound).map_err(QuestionError::Entropy)?;
        let protected_entropy_nats =
            shannon_entropy_form_with_bound(&law, factor_bound).map_err(QuestionError::Entropy)?;
        let discarded_entropy_nats = history_entropy_nats.sub(&protected_entropy_nats);
        Ok(InformationCertificate {
            presentation: self.clone(),
            prior: prior.clone(),
            factor_bound,
            quotient_law: law,
            history_entropy_nats,
            protected_entropy_nats,
            discarded_entropy_nats,
        })
    }

    pub fn verify_information(
        &self,
        prior: &ProbabilitySimplex,
        factor_bound: u32,
        candidate: &InformationCertificate,
    ) -> Result<(), QuestionError> {
        if *candidate != self.information(prior, factor_bound)? {
            return Err(QuestionError::CertificateMismatch);
        }
        Ok(())
    }
}
