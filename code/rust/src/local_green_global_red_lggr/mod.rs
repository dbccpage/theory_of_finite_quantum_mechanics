
pub mod matrix_path_kernel;
pub mod lggr_engine;
pub use lggr_engine as epk_engine;

pub use crate::lggr_engine::{
    action_gluing_defect, analyze_composition, boundary_in_slice, calculate_metrics,
    compose_kernels, composed_kernel, evaluator_gluing_defect, evaluator_residual,
    exact_path_weight, fold_evaluator_events, g2_action_additive, g3_evaluator_factorizes,
    path_weight, residual_kernel_error, segment_kernel, validate_metric_identity, BoundarySlice,
    CompositionRecord, CompositionReport, EpkError, EpkMetrics, EvaluatorEvent, FormalExponent,
    FormalSeries, GluingDefect, Kernel, KernelKey, LggrError, LggrMetrics, ResidualKernelReport,
    TraceLedger, TraceRecord,
};

pub mod composition {
    pub use crate::lggr_engine::{
        analyze_composition, boundary_in_slice, evaluator_residual, g2_action_additive,
        g3_evaluator_factorizes, CompositionReport,
    };
}
pub mod core {
    pub use crate::lggr_engine::{
        fold_evaluator_events, BoundarySlice, CompositionRecord, EvaluatorEvent, TraceLedger,
        TraceRecord,
    };
}
pub mod defects {
    pub use crate::lggr_engine::{action_gluing_defect, evaluator_gluing_defect, GluingDefect};
}
pub mod error {
    pub use crate::lggr_engine::{EpkError, LggrError};
}
pub mod kernels {
    pub use crate::lggr_engine::{
        compose_kernels, composed_kernel, exact_path_weight, path_weight, segment_kernel,
        FormalExponent, FormalSeries, Kernel, KernelKey,
    };
}
pub mod metrics {
    pub use crate::lggr_engine::{
        calculate_metrics, validate_metric_identity, EpkMetrics, LggrMetrics,
    };
}
pub mod residuals {
    pub use crate::lggr_engine::{residual_kernel_error, ResidualKernelReport};
}

pub mod adequacy;
pub mod bound_measurement;
pub mod ledger;
pub mod lggr_overlay;
pub mod lggr_v;
pub mod prime_seam;
pub mod residual_families;
pub mod verified_continuation_context_v2;
pub mod verified_continuation_context_v2_refusal_store;
pub mod verdict;

pub use verified_continuation_context_v2 as v2;
pub use verified_continuation_context_v2_refusal_store as v2_refusal_store;

pub use crate::adequacy::{
    detector_observed_corpus_digest, evaluate_detector_adequacy, DetectorAdequacyVerdict,
    DetectorAdequacyVerdictKind, DetectorCarrierClosureDisclosure, DetectorCorpusCounts,
    DetectorLocalSide, DetectorNumericalUnresolvedReason, DetectorStructuralFailure,
    DetectorUndeclaredReason, DETECTOR_ADEQUACY_VERDICT_SCHEMA,
    DETECTOR_OBSERVED_CORPUS_DIGEST_SCOPE, DETECTOR_THREAT_8_DISCLOSURE,
};
pub use crate::ledger::{EpkResidualFamilyError, EpkResidualFamilyReceipt, EpkResidualLedger};
pub use crate::lggr_v::{
    check_soundness, verify_unsoundness_witness, LggrSoundnessError, LggrSoundnessReport,
    LGGR_SOUNDNESS_SCHEMA, MAX_LGGR_CELLS,
};

#[cfg(test)]
mod tests {
    use super::*;
    use num_rational::BigRational;

    #[test]
    fn host_reexports_engine_phone_test() {
        let comps: Vec<_> = [
            (true, true, true),
            (true, true, false),
            (true, true, false),
            (true, false, false),
            (false, true, false),
        ]
        .iter()
        .enumerate()
        .map(|(i, &(e1, e2, eg))| {
            CompositionRecord::new(format!("c{i}"), "l", "r", e1, e2, eg, None).unwrap()
        })
        .collect();
        let m = calculate_metrics(&comps, None, None, None, None).unwrap();
        assert_eq!(m.lpr, BigRational::new(3.into(), 5.into()));
        assert_eq!(m.ngd, BigRational::new(2.into(), 5.into()));
        assert_eq!(m.gpr, BigRational::new(1.into(), 5.into()));
        assert_eq!(m.avg_delta_eval, BigRational::new((-2).into(), 5.into()));
    }
}
