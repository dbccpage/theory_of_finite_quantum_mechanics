use engine_types::q_continuum::{AuthorityScope, AuthorityTrace, DescentResult};

#[derive(Clone, Copy, Debug, Default, PartialEq, Eq)]
pub struct AuthorityPolicy;

impl AuthorityPolicy {
    pub fn new_trace(about: impl Into<String>, scope: AuthorityScope) -> AuthorityTrace {
        AuthorityTrace::new(about, scope)
    }

    pub fn record_result(trace: &mut AuthorityTrace, result: DescentResult) {
        trace.record_descent_result(result);
    }
}
