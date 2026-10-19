//! State-relative interchange in a declared finite partial machine.
//! Both orders must be enabled and their endpoints future-equivalent.
//! Raw endpoints may differ; no spacelike causal premise is inferred.
//! Certificates replay against the expected machine. Input/start errors are
//! typed; only a successful distinction search can report distinguished futures.
//! AuthorityEffect: None.
use crate::finite_continuation::{ContinuationError, DistinguishingWord, PartialDynamics};

#[derive(Debug, Clone, PartialEq, Eq)]
pub enum SwapOutcome {
    Independent {
        ab: usize,
        ba: usize,
    },
    Unavailable {
        a: Option<usize>,
        b: Option<usize>,
        ab: Option<usize>,
        ba: Option<usize>,
    },
    Distinguished {
        ab: usize,
        ba: usize,
        future: DistinguishingWord,
    },
}
#[derive(Debug, Clone, PartialEq, Eq)]
pub struct SwapCertificate {
    pub start: usize,
    pub a: usize,
    pub b: usize,
    pub outcome: SwapOutcome,
}

#[derive(Debug, PartialEq, Eq)]
struct SwapEndpoints {
    a: Option<usize>,
    b: Option<usize>,
    ab: Option<usize>,
    ba: Option<usize>,
}

impl SwapEndpoints {
    fn available(&self) -> Option<(usize, usize)> {
        match (self.a, self.b, self.ab, self.ba) {
            (Some(_), Some(_), Some(ab), Some(ba)) => Some((ab, ba)),
            _ => None,
        }
    }
}

fn swap_endpoints(
    machine: &PartialDynamics,
    start: usize,
    a: usize,
    b: usize,
) -> Result<SwapEndpoints, ContinuationError> {
    // Preserve start/alphabet refusal order, even across unavailable prefixes.
    Ok(SwapEndpoints {
        a: machine.run(start, &[a])?,
        b: machine.run(start, &[b])?,
        ab: machine.run(start, &[a, b])?,
        ba: machine.run(start, &[b, a])?,
    })
}

fn available_outcome(
    machine: &PartialDynamics,
    ab: usize,
    ba: usize,
    max_pairs: usize,
) -> Result<SwapOutcome, ContinuationError> {
    let q = machine.quotient();
    if q.state_to_block[ab] == q.state_to_block[ba] {
        Ok(SwapOutcome::Independent { ab, ba })
    } else {
        let future = machine
            .distinguish(ab, ba, max_pairs)?
            .ok_or(ContinuationError::CertificateMismatch)?;
        Ok(SwapOutcome::Distinguished { ab, ba, future })
    }
}

fn verify_independent(
    machine: &PartialDynamics,
    endpoints: &SwapEndpoints,
    ab: usize,
    ba: usize,
) -> bool {
    if endpoints.available() != Some((ab, ba)) {
        return false;
    }
    let q = machine.quotient();
    q.state_to_block[ab] == q.state_to_block[ba]
}

fn verify_distinguished(
    machine: &PartialDynamics,
    endpoints: &SwapEndpoints,
    ab: usize,
    ba: usize,
    future: &DistinguishingWord,
) -> bool {
    endpoints.available() == Some((ab, ba))
        && future.left == ab
        && future.right == ba
        && machine.verify_distinction(future).is_ok()
}

impl PartialDynamics {
    /// Unavailable orders (even both unavailable) never count as independence.
    /// Search exhaustion is a resource error, not a mathematical conclusion.
    pub fn certify_swap(
        &self,
        start: usize,
        a: usize,
        b: usize,
        max_pairs: usize,
    ) -> Result<SwapCertificate, ContinuationError> {
        let endpoints = swap_endpoints(self, start, a, b)?;
        let outcome = match endpoints.available() {
            Some((ab, ba)) => available_outcome(self, ab, ba, max_pairs)?,
            None => SwapOutcome::Unavailable {
                a: endpoints.a,
                b: endpoints.b,
                ab: endpoints.ab,
                ba: endpoints.ba,
            },
        };
        Ok(SwapCertificate {
            start,
            a,
            b,
            outcome,
        })
    }
    /// Replay against the expected machine. Candidate endpoints/availability
    /// are never trusted. A valid distinction need not be shortest.
    pub fn verify_swap(&self, c: &SwapCertificate) -> Result<(), ContinuationError> {
        let endpoints = swap_endpoints(self, c.start, c.a, c.b)?;
        let valid = match &c.outcome {
            SwapOutcome::Unavailable {
                a: ca,
                b: cb,
                ab: cab,
                ba: cba,
            } => {
                endpoints.available().is_none()
                    && endpoints
                        == SwapEndpoints {
                            a: *ca,
                            b: *cb,
                            ab: *cab,
                            ba: *cba,
                        }
            }
            SwapOutcome::Independent { ab: cab, ba: cba } => {
                verify_independent(self, &endpoints, *cab, *cba)
            }
            SwapOutcome::Distinguished {
                ab: cab,
                ba: cba,
                future,
            } => verify_distinguished(self, &endpoints, *cab, *cba, future),
        };
        if valid {
            Ok(())
        } else {
            Err(ContinuationError::CertificateMismatch)
        }
    }
}
