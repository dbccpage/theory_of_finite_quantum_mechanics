use engine_types::q_continuum::{AuthorityScope, DescentResult, QContinuumLedger, Residual};

#[derive(Clone, Debug, Default, PartialEq, Eq)]
pub struct QLedger {
    inner: QContinuumLedger,
}

impl QLedger {
    pub fn new() -> Self {
        Self::default()
    }

    pub fn inner(&self) -> &QContinuumLedger {
        &self.inner
    }

    pub fn inner_mut(&mut self) -> &mut QContinuumLedger {
        &mut self.inner
    }

    pub fn record_result(&mut self, about: impl Into<String>, result: DescentResult) {
        self.inner.record_descent_result(about, result);
    }

    pub fn record_residual(
        &mut self,
        about: impl Into<String>,
        obligation_id: impl Into<String>,
        scope: AuthorityScope,
        residual: Residual,
    ) {
        self.record_result(about, DescentResult::failed(obligation_id, scope, residual));
    }
}
