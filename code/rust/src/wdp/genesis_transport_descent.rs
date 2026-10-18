//! Source-25 carrier edits retain raw states alongside the exact gauge verdict.
//! This assesses fixed-writing gradient classes, not permission or all futures.
use crate::genesis_source_execution::{Source25Change, Source25State, SourceExecutionError};
use crate::types::AuthorityEffect;
use linear_algebra::backend::basic_matrix::BasicMatrix;
use linear_algebra::gauge_pair_transport::{GaugeDescent, GaugePairTransport, GaugeTransportError};
use num_rational::BigRational;

#[derive(Debug, thiserror::Error)]
pub enum CarrierDescentError {
    #[error("the selected event is outside the AddTerm/Identify carrier profile")]
    EventProfile,
    #[error("computed source edit does not match the declared pair transport")]
    TransportMismatch,
    #[error(transparent)]
    Source(#[from] SourceExecutionError),
    #[error(transparent)]
    Math(#[from] GaugeTransportError),
}

#[derive(Debug, Clone, PartialEq, Eq)]
pub struct DeclaredCarrierGaugeTransport {
    source: Source25State,
    change: Source25Change,
    target: Source25State,
    transport: GaugePairTransport,
    descent: GaugeDescent,
}
impl DeclaredCarrierGaugeTransport {
    pub fn new(source: Source25State, change: Source25Change) -> Result<Self, CarrierDescentError> {
        if !matches!(
            change,
            Source25Change::AddTerm | Source25Change::Identify { .. }
        ) {
            return Err(CarrierDescentError::EventProfile);
        }
        if !source.is_enabled(change) {
            return Err(SourceExecutionError::DisabledChange.into());
        }
        let n = source.packet().terms.len();
        let transport = match change {
            Source25Change::AddTerm => GaugePairTransport::new((0..n).collect(), n + 1)?,
            Source25Change::Identify { x, y } => GaugePairTransport::new(
                (0..n)
                    .map(|v| if v == y { x } else { v - usize::from(v > y) })
                    .collect(),
                n - 1,
            )?,
            _ => return Err(CarrierDescentError::EventProfile),
        };
        let target = source.perform_enabled(change)?;
        for (before, after) in [
            (&source.packet().r, &target.packet().r),
            (&source.packet().s, &target.packet().s),
        ] {
            let raw = BasicMatrix::from_row_major(
                n,
                n,
                before
                    .iter()
                    .cloned()
                    .map(BigRational::from_integer)
                    .collect(),
            )
            .map_err(GaugeTransportError::from)?;
            let actual = transport.apply(&raw)?;
            if !actual
                .as_slice()
                .iter()
                .zip(after)
                .all(|(a, b)| a == &BigRational::from_integer(b.clone()))
                || actual.as_slice().len() != after.len()
            {
                return Err(CarrierDescentError::TransportMismatch);
            }
        }
        let descent = transport.descent();
        Ok(Self {
            source,
            change,
            target,
            transport,
            descent,
        })
    }
    pub fn source(&self) -> &Source25State {
        &self.source
    }
    pub fn target(&self) -> &Source25State {
        &self.target
    }
    pub fn change(&self) -> Source25Change {
        self.change
    }
    pub fn transport(&self) -> &GaugePairTransport {
        &self.transport
    }
    pub fn descent(&self) -> &GaugeDescent {
        &self.descent
    }
    pub fn authority_effect(&self) -> AuthorityEffect {
        AuthorityEffect::None
    }
}
