
use omega_category_theory::finite_report_descent::{CoverClassification, DescentOutcome};

#[derive(Debug, Clone, PartialEq, Eq, Default)]
pub struct DescentSummary {
    pub matching_families: usize,
    pub no_global_extension: usize,
    pub unique: usize,
    pub ambiguous: usize,
}

pub fn summarize_descent(classification: &CoverClassification) -> DescentSummary {
    let mut summary = DescentSummary {
        matching_families: classification.matching_fibers.len(),
        ..DescentSummary::default()
    };
    for fiber in &classification.matching_fibers {
        match fiber.outcome() {
            DescentOutcome::NoGlobalExtension => summary.no_global_extension += 1,
            DescentOutcome::Unique { .. } => summary.unique += 1,
            DescentOutcome::Ambiguous { .. } => summary.ambiguous += 1,
        }
    }
    summary
}
