use crate::genesis_carrier::{PassageAnswer, PassageCarrier, PassageQuestion};
use crate::genesis_joint_dynamics::{PassageJoint, PassageJointError, PassageJointRequest};
use tfqm_category_theory::finite_joint_dynamics::{JointDynamicsAnalysis, JointDynamicsError};
use engine_number_theory::rational::Rational;
use engine_quantum_physics::finite_bell_extension::BellLimits;
use engine_quantum_physics::finite_bell_preparation::{
    PreparationError, PreparedBellCertificate, PreparedBellProblem, ResponseFunctions,
};
use std::collections::BTreeSet;

#[derive(Debug, Clone, PartialEq, Eq)]
pub struct PassageMeasurement {
    pub word: Vec<usize>,
    pub question: PassageQuestion,
    pub outcomes: Vec<PassageAnswer>,
}
#[derive(Debug, Clone, PartialEq, Eq)]
pub enum PreparationLaw {
    Shared(Vec<Rational>),
    ByContext(Vec<Vec<Rational>>),
}
#[derive(Debug, Clone, PartialEq, Eq)]
pub struct PassageBellRequest {
    pub joint: PassageJointRequest,
    pub preparation_word: Vec<usize>,
    pub left_settings: Vec<PassageMeasurement>,
    pub right_settings: Vec<PassageMeasurement>,
    pub law: PreparationLaw,
    pub bell_limits: BellLimits,
    pub max_cells: usize,
}
#[derive(Debug, Clone, PartialEq, Eq)]
pub enum PassageBellError {
    Joint(PassageJointError),
    Analysis(JointDynamicsError),
    Probability(PreparationError),
    InvalidMeasurement,
    UnavailablePreparation {
        row: usize,
    },
    UnavailableMeasurement {
        row: usize,
        left: bool,
        setting: usize,
    },
    WorkLimit,
    CertificateMismatch,
}
#[derive(Debug, Clone, PartialEq, Eq)]
pub struct PassageBellCertificate {
    pub source: PassageBellRequest,
    pub joint_analysis: JointDynamicsAnalysis,
    pub prepared_rows: Vec<usize>,
    pub responses: Vec<ResponseFunctions>,
    pub experiment: PreparedBellCertificate,
}
#[derive(Debug, Clone, PartialEq, Eq)]
pub struct PassageBellExperiment {
    source: PassageBellRequest,
    joint: PassageJoint,
    prepared_rows: Vec<usize>,
    responses: Vec<ResponseFunctions>,
    probability: PreparedBellProblem,
}

fn response(
    carrier: &PassageCarrier,
    state: usize,
    settings: &[PassageMeasurement],
    row: usize,
    left: bool,
) -> Result<Vec<usize>, PassageBellError> {
    settings
        .iter()
        .enumerate()
        .map(|(setting, m)| {
            let end = carrier
                .dynamics()
                .run(state, &m.word)
                .map_err(|_| PassageBellError::InvalidMeasurement)?
                .ok_or(PassageBellError::UnavailableMeasurement { row, left, setting })?;
            let answer = m.question.answer(&carrier.certificate().states[end]);
            m.outcomes
                .iter()
                .position(|a| *a == answer)
                .ok_or(PassageBellError::InvalidMeasurement)
        })
        .collect()
}
impl PassageBellExperiment {
    pub fn build(request: &PassageBellRequest) -> Result<Self, PassageBellError> {
        if request.left_settings.is_empty()
            || request.right_settings.is_empty()
            || request
                .left_settings
                .len()
                .checked_add(request.right_settings.len())
                .is_none_or(|n| n > 20)
        {
            return Err(PassageBellError::InvalidMeasurement);
        }
        let mut cells = request
            .preparation_word
            .len()
            .checked_add(1)
            .ok_or(PassageBellError::WorkLimit)?;
        for (m, carrier) in request
            .left_settings
            .iter()
            .map(|m| (m, &request.joint.left))
            .chain(
                request
                    .right_settings
                    .iter()
                    .map(|m| (m, &request.joint.right)),
            )
        {
            cells = cells
                .checked_add(m.word.len())
                .and_then(|n| n.checked_add(m.outcomes.len()))
                .and_then(|n| n.checked_add(1))
                .ok_or(PassageBellError::WorkLimit)?;
            if cells > request.max_cells {
                return Err(PassageBellError::WorkLimit);
            }
            if !carrier.questions.contains(&m.question)
                || m.outcomes.is_empty()
                || m.outcomes.iter().collect::<BTreeSet<_>>().len() != m.outcomes.len()
            {
                return Err(PassageBellError::InvalidMeasurement);
            }
        }
        if cells
            .checked_mul(request.joint.pairs.len())
            .is_none_or(|n| n > request.max_cells)
        {
            return Err(PassageBellError::WorkLimit);
        }
        let joint = PassageJoint::build(&request.joint).map_err(PassageBellError::Joint)?;
        let mut prepared_rows = Vec::new();
        let mut responses = Vec::new();
        for row in 0..joint.joint().pairs().len() {
            let prepared = joint
                .joint()
                .dynamics()
                .run(row, &request.preparation_word)
                .map_err(|_| PassageBellError::InvalidMeasurement)?
                .ok_or(PassageBellError::UnavailablePreparation { row })?;
            let (l, r) = joint.joint().pairs()[prepared];
            responses.push(ResponseFunctions {
                left: response(joint.left(), l, &request.left_settings, row, true)?,
                right: response(joint.right(), r, &request.right_settings, row, false)?,
            });
            prepared_rows.push(prepared);
        }
        let contexts = request.left_settings.len() * request.right_settings.len();
        if contexts
            .checked_mul(request.joint.pairs.len())
            .is_none_or(|n| n > request.max_cells)
        {
            return Err(PassageBellError::WorkLimit);
        }
        let priors = match &request.law {
            PreparationLaw::Shared(p) => {
                if p.len() != request.joint.pairs.len() {
                    return Err(PassageBellError::Probability(
                        PreparationError::InvalidPriors,
                    ));
                }
                vec![p.clone(); contexts]
            }
            PreparationLaw::ByContext(p) => {
                if p.len() != contexts || p.iter().any(|row| row.len() != request.joint.pairs.len())
                {
                    return Err(PassageBellError::Probability(
                        PreparationError::InvalidPriors,
                    ));
                }
                p.clone()
            }
        };
        let probability = PreparedBellProblem::new(
            request
                .left_settings
                .iter()
                .map(|m| m.outcomes.len())
                .collect(),
            request
                .right_settings
                .iter()
                .map(|m| m.outcomes.len())
                .collect(),
            &responses,
            &priors,
            request.bell_limits,
            request.max_cells,
        )
        .map_err(PassageBellError::Probability)?;
        Ok(Self {
            source: request.clone(),
            joint,
            prepared_rows,
            responses,
            probability,
        })
    }
    pub fn joint(&self) -> &PassageJoint {
        &self.joint
    }
    pub fn probability(&self) -> &PreparedBellProblem {
        &self.probability
    }
    pub fn certify(&self, pivots: usize) -> Result<PassageBellCertificate, PassageBellError> {
        Ok(PassageBellCertificate {
            source: self.source.clone(),
            joint_analysis: self
                .joint
                .joint()
                .analyze()
                .map_err(PassageBellError::Analysis)?,
            prepared_rows: self.prepared_rows.clone(),
            responses: self.responses.clone(),
            experiment: self
                .probability
                .decide(pivots)
                .map_err(PassageBellError::Probability)?,
        })
    }
    pub fn verify(
        request: &PassageBellRequest,
        c: &PassageBellCertificate,
    ) -> Result<(), PassageBellError> {
        if c.source != *request {
            return Err(PassageBellError::CertificateMismatch);
        }
        let expected = Self::build(request)?;
        if c.prepared_rows != expected.prepared_rows || c.responses != expected.responses {
            return Err(PassageBellError::CertificateMismatch);
        }
        expected
            .joint
            .joint()
            .verify(&c.joint_analysis)
            .map_err(PassageBellError::Analysis)?;
        expected
            .probability
            .verify(&c.experiment)
            .map_err(PassageBellError::Probability)
    }
}
