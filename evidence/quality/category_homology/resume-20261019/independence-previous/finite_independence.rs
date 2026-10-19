//! State-relative interchange in a declared finite partial machine.
//! Both orders must be enabled and their endpoints future-equivalent.
//! Raw endpoints may differ; no spacelike causal premise is inferred.
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
        let sa = self.run(start, &[a])?;
        let sb = self.run(start, &[b])?;
        let ab = self.run(start, &[a, b])?;
        let ba = self.run(start, &[b, a])?;
        let outcome = match (sa, sb, ab, ba) {
            (Some(_), Some(_), Some(ab), Some(ba)) => {
                let q = self.quotient();
                if q.state_to_block[ab] == q.state_to_block[ba] {
                    SwapOutcome::Independent { ab, ba }
                } else {
                    let future = self
                        .distinguish(ab, ba, max_pairs)?
                        .ok_or(ContinuationError::CertificateMismatch)?;
                    SwapOutcome::Distinguished { ab, ba, future }
                }
            }
            _ => SwapOutcome::Unavailable {
                a: sa,
                b: sb,
                ab,
                ba,
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
        let a = self.run(c.start, &[c.a])?;
        let b = self.run(c.start, &[c.b])?;
        let ab = self.run(c.start, &[c.a, c.b])?;
        let ba = self.run(c.start, &[c.b, c.a])?;
        let valid = match &c.outcome {
            SwapOutcome::Unavailable {
                a: ca,
                b: cb,
                ab: cab,
                ba: cba,
            } => {
                (a.is_none() || b.is_none() || ab.is_none() || ba.is_none())
                    && (a, b, ab, ba) == (*ca, *cb, *cab, *cba)
            }
            SwapOutcome::Independent { ab: cab, ba: cba } => {
                if a.is_none() || b.is_none() || ab != Some(*cab) || ba != Some(*cba) {
                    false
                } else {
                    let q = self.quotient();
                    q.state_to_block[*cab] == q.state_to_block[*cba]
                }
            }
            SwapOutcome::Distinguished {
                ab: cab,
                ba: cba,
                future,
            } => {
                a.is_some()
                    && b.is_some()
                    && ab == Some(*cab)
                    && ba == Some(*cba)
                    && future.left == *cab
                    && future.right == *cba
                    && self.verify_distinction(future).is_ok()
            }
        };
        if valid {
            Ok(())
        } else {
            Err(ContinuationError::CertificateMismatch)
        }
    }
}
