use crate::genesis_source_execution::{Source25Change, Source25State, SourceRelation};
use num_bigint::BigInt;
use num_traits::ToPrimitive;
use tfqm_category_theory::bounded_counter::{
    CounterBoundary, CounterEvent, CounterReport, CounterReportError,
};

#[derive(Debug, Clone, PartialEq, Eq)]
pub enum CellGuardError {
    OutsideCarrier,
    UnsupportedContextEvent,
    InvalidCount,
    Report(CounterReportError),
    Boundary(CounterBoundary),
}

#[derive(Debug, Clone, PartialEq, Eq)]
pub struct Source25CellGuard {
    relation: SourceRelation,
    x: usize,
    y: usize,
    report: CounterReport,
}

impl Source25CellGuard {
    pub fn from_state(
        state: &Source25State,
        relation: SourceRelation,
        x: usize,
        y: usize,
        remaining: usize,
    ) -> Result<Self, CellGuardError> {
        if !state.is_enabled(Source25Change::AddAssertion { relation, x, y }) {
            return Err(CellGuardError::OutsideCarrier);
        }
        let packet = state.packet();
        let counts = match relation {
            SourceRelation::R => &packet.r,
            SourceRelation::S => &packet.s,
        };
        let count = &counts[x * packet.terms.len() + y];
        let clipped = if count >= &BigInt::from(remaining) {
            remaining
        } else {
            count.to_usize().ok_or(CellGuardError::InvalidCount)?
        };
        Ok(Self {
            relation,
            x,
            y,
            report: CounterReport::try_from_clip(remaining, clipped)
                .map_err(CellGuardError::Report)?,
        })
    }

    pub fn report(&self) -> CounterReport {
        self.report
    }

    pub fn advance(&self, change: Source25Change) -> Result<Self, CellGuardError> {
        let event = match change {
            Source25Change::AddAssertion { relation, x, y }
                if relation == self.relation && x == self.x && y == self.y =>
            {
                CounterEvent::Increment
            }
            Source25Change::Remove { relation, x, y }
                if relation == self.relation && x == self.x && y == self.y =>
            {
                CounterEvent::Decrement
            }
            _ => return Err(CellGuardError::UnsupportedContextEvent),
        };
        let report = self
            .report
            .advance(event)
            .map_err(CellGuardError::Boundary)?;
        Ok(Self {
            report,
            ..self.clone()
        })
    }

    pub fn observe(&self, changes: &[Source25Change]) -> Result<Self, CellGuardError> {
        changes
            .iter()
            .try_fold(self.clone(), |state, &change| state.advance(change))
    }
}
