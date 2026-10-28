
use engine_wire_primitives::{admission, event::Event, regime::Regime, token::Token};

use engine_homology::declared_incidence::{declared_chain_report, encode_declared};
use engine_homology::simplicial::SimplicialComplex;

use crate::genesis_geometry::{ChainReport, ComplexPacket};
use crate::genesis_primitive_execution::{
    PrimitiveEvent, PrimitiveInstance, PrimitiveReading, PrimitiveRegime,
};

pub const GENESIS_INSCRIPTION: &str = "<>";

#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub struct ConstructionLimits {
    pub max_events: usize,
    pub max_cells: usize,
    pub max_matrix_entries: usize,
}

impl Default for ConstructionLimits {
    fn default() -> Self {
        Self {
            max_events: 4096,
            max_cells: 512,
            max_matrix_entries: 262_144,
        }
    }
}

#[derive(Debug, Clone, PartialEq, Eq, thiserror::Error)]
pub enum ConstructionError {
    #[error("the first event must present the literal <> inscription")]
    MissingLiteralRoot,
    #[error("canonical admission at event {index} failed: {reason}")]
    Admission { index: usize, reason: String },
    #[error("WDP source correspondence at event {index} failed: {reason}")]
    Correspondence { index: usize, reason: String },
    #[error("the incidence interpretation requires at least one admitted form")]
    NoIncidenceForm,
    #[error("uniform rules and separation requirements need their own geometric interpretation")]
    UnsupportedIncidenceCommitments,
    #[error("admitted datum {0} has no explicit vertex instance")]
    MissingVertex(usize),
    #[error("invalid admitted incidence: {0}")]
    Incidence(String),
    #[error("the claimed chain report differs from the replayed history")]
    ReportMismatch,
    #[error("declared {resource} limit {limit} exceeded")]
    ResourceLimit {
        resource: &'static str,
        limit: usize,
    },
}

pub fn interpret_regime(regime: &Regime) -> Result<PrimitiveRegime, ConstructionError> {
    PrimitiveRegime::try_new(
        regime
            .data()
            .iter()
            .map(|token| token.text().to_owned())
            .collect(),
        regime.forms().to_vec(),
        regime
            .insts()
            .iter()
            .map(|instance| PrimitiveInstance {
                form: instance.form,
                args: instance.args.iter().map(|mark| mark.index()).collect(),
            })
            .collect(),
        regime.rules().clone(),
        regime
            .reqs()
            .iter()
            .map(|pair| (pair.i.index(), pair.j.index()))
            .collect(),
    )
    .map_err(|error| ConstructionError::Correspondence {
        index: 0,
        reason: error.to_string(),
    })
}

pub fn interpret_event(event: &Event) -> PrimitiveEvent {
    match event {
        Event::Supply(token) => PrimitiveEvent::Supply {
            token: token.text().to_owned(),
        },
        Event::AdmitDatum(token) => PrimitiveEvent::AdmitDatum {
            token: token.text().to_owned(),
        },
        Event::AdmitForm(arity) => PrimitiveEvent::AdmitForm { arity: *arity },
        Event::AdmitInst(form, args) => PrimitiveEvent::AdmitInst {
            form: *form,
            args: args.iter().map(|mark| mark.index()).collect(),
        },
        Event::AdmitRuleAll(form) => PrimitiveEvent::AdmitRuleAll { form: *form },
        Event::Impose(pair) => PrimitiveEvent::Impose {
            i: pair.i.index(),
            j: pair.j.index(),
        },
    }
}

#[derive(Debug, Clone, PartialEq, Eq)]
pub struct GenesisConstruction {
    limits: ConstructionLimits,
    history: Vec<Event>,
    regime: Regime,
    interpreted: PrimitiveRegime,
}

impl GenesisConstruction {
    pub fn pre_genesis() -> Self {
        Self::pre_genesis_with_limits(ConstructionLimits::default())
    }

    pub fn pre_genesis_with_limits(limits: ConstructionLimits) -> Self {
        Self {
            limits,
            history: Vec::new(),
            regime: Regime::genesis(),
            interpreted: PrimitiveRegime::empty(),
        }
    }

    pub fn from_literal_seed() -> Result<Self, ConstructionError> {
        Self::pre_genesis().advance(Event::Supply(Token::new(GENESIS_INSCRIPTION)))
    }

    pub fn replay(history: &[Event]) -> Result<Self, ConstructionError> {
        Self::replay_with_limits(history, ConstructionLimits::default())
    }

    pub fn replay_with_limits(
        history: &[Event],
        limits: ConstructionLimits,
    ) -> Result<Self, ConstructionError> {
        if history.is_empty() {
            return Err(ConstructionError::MissingLiteralRoot);
        }
        if history.len() > limits.max_events {
            return Err(ConstructionError::ResourceLimit {
                resource: "event count",
                limit: limits.max_events,
            });
        }
        Self::pre_genesis_with_limits(limits).extend(history)
    }

    pub fn history(&self) -> &[Event] {
        &self.history
    }
    pub fn regime(&self) -> &Regime {
        &self.regime
    }
    pub fn interpreted(&self) -> &PrimitiveRegime {
        &self.interpreted
    }

    pub fn limits(&self) -> ConstructionLimits {
        self.limits
    }

    pub fn advance(&self, event: Event) -> Result<Self, ConstructionError> {
        let index = self.history.len();
        if index >= self.limits.max_events {
            return Err(ConstructionError::ResourceLimit {
                resource: "event count",
                limit: self.limits.max_events,
            });
        }
        if index == 0 && event != Event::Supply(Token::new(GENESIS_INSCRIPTION)) {
            return Err(ConstructionError::MissingLiteralRoot);
        }
        let regime = admission::step(&self.regime, &event).map_err(|error| {
            ConstructionError::Admission {
                index,
                reason: error.to_string(),
            }
        })?;
        let interpreted = self
            .interpreted
            .step(&interpret_event(&event), PrimitiveReading::Dedup)
            .map_err(|error| ConstructionError::Correspondence {
                index,
                reason: error.to_string(),
            })?;
        let restored =
            interpret_regime(&regime).map_err(|error| ConstructionError::Correspondence {
                index,
                reason: error.to_string(),
            })?;
        if restored != interpreted {
            return Err(ConstructionError::Correspondence {
                index,
                reason: "complete states differ".into(),
            });
        }
        let mut history = self.history.clone();
        history.push(event);
        Ok(Self {
            limits: self.limits,
            history,
            regime,
            interpreted,
        })
    }

    pub fn extend(&self, events: &[Event]) -> Result<Self, ConstructionError> {
        events
            .iter()
            .try_fold(self.clone(), |state, event| state.advance(event.clone()))
    }

    fn incidence_cells(&self) -> Result<Vec<Vec<usize>>, ConstructionError> {
        if self.regime.forms().is_empty() {
            return Err(ConstructionError::NoIncidenceForm);
        }
        if !self.regime.rules().is_empty() || !self.regime.reqs().is_empty() {
            return Err(ConstructionError::UnsupportedIncidenceCommitments);
        }
        let cell_count = self.regime.insts().len();
        if cell_count > self.limits.max_cells {
            return Err(ConstructionError::ResourceLimit {
                resource: "cell count",
                limit: self.limits.max_cells,
            });
        }
        if cell_count
            .checked_mul(cell_count)
            .is_none_or(|size| size > self.limits.max_matrix_entries)
        {
            return Err(ConstructionError::ResourceLimit {
                resource: "matrix entries",
                limit: self.limits.max_matrix_entries,
            });
        }
        let cells: Vec<Vec<usize>> = self
            .regime
            .insts()
            .iter()
            .map(|instance| instance.args.iter().map(|mark| mark.index()).collect())
            .collect();
        for vertex in 0..self.regime.n_data() {
            if !cells.contains(&vec![vertex]) {
                return Err(ConstructionError::MissingVertex(vertex));
            }
        }
        Ok(cells)
    }

    fn encoded_incidence(&self) -> Result<(ComplexPacket, SimplicialComplex), ConstructionError> {
        let cells = self.incidence_cells()?;
        let complex = encode_declared(&cells)
            .map_err(|error| ConstructionError::Incidence(format!("{error:?}")))?;
        Ok((ComplexPacket { cells }, complex))
    }

    pub fn simplicial_incidence(&self) -> Result<ComplexPacket, ConstructionError> {
        self.encoded_incidence().map(|(packet, _complex)| packet)
    }

    pub fn homology(&self) -> Result<ChainReport, ConstructionError> {
        let (_packet, complex) = self.encoded_incidence()?;
        declared_chain_report(&complex)
            .map(ChainReport::from)
            .map_err(|error| ConstructionError::Incidence(format!("{error:?}")))
    }
}

pub fn verify_history_report(
    history: &[Event],
    claimed: &ChainReport,
) -> Result<(), ConstructionError> {
    let actual = GenesisConstruction::replay(history)?.homology()?;
    if actual != *claimed {
        return Err(ConstructionError::ReportMismatch);
    }
    Ok(())
}

pub fn cycle_construction(labels: [&str; 3]) -> Result<GenesisConstruction, ConstructionError> {
    use engine_wire_primitives::mark::Mark;
    let mut walk = GenesisConstruction::from_literal_seed()?;
    for label in labels {
        walk = walk.advance(Event::Supply(Token::new(label)))?;
        walk = walk.advance(Event::AdmitDatum(Token::new(label)))?;
    }
    for arity in 1..=3 {
        walk = walk.advance(Event::AdmitForm(arity))?;
    }
    for vertex in 0..3 {
        walk = walk.advance(Event::AdmitInst(0, vec![Mark(vertex)]))?;
    }
    for [a, b] in [[0, 1], [1, 2], [0, 2]] {
        walk = walk.advance(Event::AdmitInst(1, vec![Mark(a), Mark(b)]))?;
    }
    Ok(walk)
}
