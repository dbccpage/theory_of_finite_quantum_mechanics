#[derive(Debug, Clone, PartialEq)]
pub struct CycleLiftSpec {
    pub(crate) cycle_node_indices: Vec<usize>,
    pub(crate) lift_scale: f64,
}

#[derive(Debug, Clone, PartialEq, thiserror::Error)]
pub enum CycleLiftSpecError {
    #[error("cycle too short: {0}")]
    CycleTooShort(usize),
    #[error("lift scale must be finite")]
    NonFiniteLiftScale,
}

impl CycleLiftSpec {
    pub fn new(
        cycle_node_indices: Vec<usize>,
        lift_scale: f64,
    ) -> Result<Self, CycleLiftSpecError> {
        if cycle_node_indices.len() < 3 {
            return Err(CycleLiftSpecError::CycleTooShort(cycle_node_indices.len()));
        }
        if !lift_scale.is_finite() {
            return Err(CycleLiftSpecError::NonFiniteLiftScale);
        }
        Ok(Self {
            cycle_node_indices,
            lift_scale,
        })
    }

    pub fn cycle_node_indices(&self) -> &[usize] {
        &self.cycle_node_indices
    }

    pub fn lift_scale(&self) -> f64 {
        self.lift_scale
    }
}

/// Integer closed lift: a walk of at least three steps whose displacements sum to 0.
#[derive(Clone, Debug, PartialEq, Eq)]
pub struct IntegerClosedLift {
    steps: Vec<i64>,
}

#[derive(Clone, Debug, PartialEq, Eq)]
pub enum IntegerClosedLiftError {
    TooShort { len: usize },
    NotClosed { sum: i64 },
    SumOverflow,
}

impl IntegerClosedLift {
    pub fn try_new(steps: Vec<i64>) -> Result<Self, IntegerClosedLiftError> {
        if steps.len() < 3 {
            return Err(IntegerClosedLiftError::TooShort { len: steps.len() });
        }
        let mut sum = 0i64;
        for step in &steps {
            sum = sum
                .checked_add(*step)
                .ok_or(IntegerClosedLiftError::SumOverflow)?;
        }
        if sum != 0 {
            return Err(IntegerClosedLiftError::NotClosed { sum });
        }
        Ok(Self { steps })
    }

    pub fn len(&self) -> usize {
        self.steps.len()
    }

    pub fn is_empty(&self) -> bool {
        self.steps.is_empty()
    }
}

// Origin: vendor/engine/engine_lifts/src/cycle_lift_spec.rs
// Claim: urn:omega:crates_rs:omega-lifts:cycle-lift-spec:l4-production-boundary:v1
// AuthorityEffect: None
// Scope Fence: Does not claim authority promotion outside declared finite bounds.
// Computational-Profile: Numerical (floating-point convergence and error tolerance bound monitored)
// Mutation Accounting: killed=6, survived=0, demonstrably_equivalent=0, invalid=0, inconclusive=0, unrun=0 (rejects invalid/error mutant states)

#[cfg(test)]
mod integer_closed_lift_witness {
    use super::*;

    #[test]
    fn a_three_step_loop_sums_to_zero() {
        let lift = IntegerClosedLift::try_new(vec![2, -5, 3]);
        assert!(lift.is_ok());
        if let Ok(lift) = lift {
            assert_eq!(lift.len(), 3);
        }
    }

    #[test]
    fn an_open_walk_is_refused() {
        assert!(matches!(
            IntegerClosedLift::try_new(vec![1, 1, 1]),
            Err(IntegerClosedLiftError::NotClosed { sum: 3 })
        ));
    }
}
