
use engine_kernel::resource_limits::OperationLimits;
use serde::{Deserialize, Serialize};
use thiserror::Error;

#[derive(Debug, Clone, PartialEq, Eq, Error, Serialize, Deserialize)]
pub enum HigherCategoryError {
    #[error("Object (0-cell) not found: {id}")]
    ZeroCellNotFound { id: String },

    #[error("1-Morphism (1-cell) not found: {id}")]
    OneCellNotFound { id: String },

    #[error("2-Morphism (2-cell) not found: {id}")]
    TwoCellNotFound { id: String },

    #[error("Duplicate cell declared: {id}")]
    DuplicateCell { id: String },

    #[error("1-Cell boundary mismatch: morphism '{cell}' has source '{actual_src}', expected '{expected_src}'")]
    OneCellBoundaryMismatch {
        cell: String,
        expected_src: String,
        actual_src: String,
    },

    #[error("2-Cell 1-boundary mismatch: 2-cell '{cell}' source '{actual_1_src}' != expected '{expected_1_src}'")]
    TwoCellBoundaryMismatch {
        cell: String,
        expected_1_src: String,
        actual_1_src: String,
    },

    #[error("2-cell '{two_cell}' violates globular condition: src_1 boundaries {src_1_boundary:?} != tgt_1 boundaries {tgt_1_boundary:?}")]
    GlobularBoundaryViolation {
        two_cell: String,
        src_1_boundary: (String, String),
        tgt_1_boundary: (String, String),
    },

    #[error("1-cells are not parallel for 2-cell declaration: source={src_1}, target={tgt_1}")]
    NonParallel1Cells { src_1: String, tgt_1: String },

    #[error("1-Morphisms not horizontally composable: '{first}' (tgt={tgt}) then '{second}' (src={src})")]
    OneCellNotComposable {
        first: String,
        second: String,
        tgt: String,
        src: String,
    },

    #[error("2-Morphisms not vertically composable: '{alpha}' (tgt1={tgt1}) then '{beta}' (src1={src1})")]
    VerticalNotComposable {
        alpha: String,
        beta: String,
        tgt1: String,
        src1: String,
    },

    #[error("2-Morphisms not horizontally composable: '{alpha}' (tgt0={tgt0}) then '{beta}' (src0={src0})")]
    HorizontalNotComposable {
        alpha: String,
        beta: String,
        tgt0: String,
        src0: String,
    },

    #[error("Boundary mismatch: expected {expected}, found {found}")]
    BoundaryMismatch { expected: String, found: String },

    #[error("Exchange law violation: (beta . alpha) * (delta . gamma) != (beta * delta) . (alpha * gamma). Left='{left}', Right='{right}'. Details: {details}")]
    ExchangeLawViolation {
        left: String,
        right: String,
        details: String,
    },

    #[error("Associativity law violation: {details}")]
    AssociativityViolation { details: String },

    #[error("Unit law violation: {details}")]
    UnitLawViolation { details: String },

    #[error(
        "Pentagon coherence axiom failed: step '{step}', path A '{path_a}' != path B '{path_b}'"
    )]
    PentagonCoherenceViolation {
        step: String,
        path_a: String,
        path_b: String,
    },

    #[error("Triangle coherence axiom failed: (1_g * l_f) . a_{{g, id, f}} != r_g * 1_f. Left='{left}', Right='{right}'. Details: {details}")]
    TriangleCoherenceViolation {
        left: String,
        right: String,
        details: String,
    },

    #[error("2-cell '{two_cell}' is not an isomorphism: {reason}")]
    NonInvertible2Cell { two_cell: String, reason: String },

    #[error("Invertibility violation for cell '{cell}': {details}")]
    InvertibilityViolation { cell: String, details: String },

    #[error("Soviet Builder allocation failure: unable to reserve {requested} elements")]
    AllocationFailed { requested: usize },

    #[error("Soviet Builder allocation limit exceeded: requested {requested}, limit is {limit}")]
    AllocationLimitExceeded { requested: usize, limit: usize },

    #[error("Operation count limit exceeded: requested {requested}, budget is {limit}")]
    OperationLimitExceeded { requested: usize, limit: usize },

    #[error("Differential not nilpotent at degree {degree}: {details}")]
    DifferentialNotNilpotent { degree: i32, details: String },

    #[error("Graded Leibniz rule violated: {details}")]
    LeibnizRuleViolation { details: String },

    #[error("Rotation axiom TR2 violated: {details}")]
    RotationAxiomViolation { details: String },

    #[error("Octahedral axiom TR4 violated: {details}")]
    OctahedralAxiomViolation { details: String },

    #[error("Square boundary mismatch for square '{square_id}': expected {expected}, actual {actual}")]
    SquareBoundaryMismatch {
        square_id: String,
        expected: String,
        actual: String,
    },

    #[error("Squares not composable ({direction}): '{first}' and '{second}': {details}")]
    SquareNotComposable {
        first: String,
        second: String,
        direction: String,
        details: String,
    },

    #[error("Square interchange law violated: Left='{left}', Right='{right}'. Details: {details}")]
    SquareInterchangeViolation {
        left: String,
        right: String,
        details: String,
    },

    #[error("Enriched unit morphism mismatch for object '{object_id}': {details}")]
    EnrichedUnitMismatch {
        object_id: String,
        details: String,
    },

    #[error("Enriched associativity diagram violation: {details}")]
    EnrichedAssociativityViolation { details: String },

    #[error("Model category two-out-of-three axiom violated for f='{f}', g='{g}': {details}")]
    TwoOutOfThreeViolation {
        f: String,
        g: String,
        details: String,
    },

    #[error("Lifting property violated for cofibration='{cofibration}', fibration='{fibration}': {details}")]
    LiftingPropertyViolation {
        cofibration: String,
        fibration: String,
        details: String,
    },

    #[error("Functorial factorization violated for morphism '{morphism}': {details}")]
    FactorizationViolation {
        morphism: String,
        details: String,
    },

    #[error("Simplicial identity violated at dimension {dimension}: {details}")]
    SimplicialIdentityViolation {
        dimension: usize,
        details: String,
    },

    #[error("Inner horn filling violated for horn Lambda^{k}_{dimension}: {details}")]
    InnerHornFillingViolation {
        dimension: usize,
        k: usize,
        details: String,
    },

    #[error("Zero object violation in pointed category: {details}")]
    ZeroObjectViolation {
        object: String,
        details: String,
    },

    #[error("Suspension-loop invertibility violation for object '{object}': {details}")]
    SuspensionLoopInvertibilityViolation {
        object: String,
        details: String,
    },

    #[error("Spectrum structure map equivalence violation at level {level}: {details}")]
    SpectrumEquivalenceViolation {
        level: usize,
        details: String,
    },

    #[error("Compactness filtered colimit factorization violation for object '{object}': {details}")]
    CompactnessViolation {
        object: String,
        details: String,
    },

    #[error("Compact generator coverage violation for object '{object}': {details}")]
    CompactGeneratorCoverageViolation {
        object: String,
        details: String,
    },

    #[error("Operadic nerve horn boundary mismatch: {details}")]
    OperadicNerveBoundaryMismatch { details: String },

    #[error("Operadic nerve missing face d1 mismatch: expected '{expected}', found '{actual}'")]
    OperadicNerveMissingFaceMismatch { expected: String, actual: String },

    #[error("Dendroidal horn boundary mismatch: expected '{expected}', found '{found}'")]
    DendroidalBoundaryMismatch { expected: String, found: String },

    #[error("Dendroidal missing inner face mismatch: expected '{expected}', found '{found}'")]
    DendroidalMissingFaceMismatch { expected: String, found: String },

    #[error("Tree cycle violation: {details}")]
    TreeCycleViolation { details: String },
}

pub fn reserve_exact<T>(
    vec: &mut Vec<T>,
    additional: usize,
    limits: &OperationLimits,
) -> Result<(), HigherCategoryError> {
    let target_len = vec.len().saturating_add(additional);
    if target_len > limits.max_cells {
        return Err(HigherCategoryError::AllocationLimitExceeded {
            requested: target_len,
            limit: limits.max_cells,
        });
    }
    vec.try_reserve_exact(additional)
        .map_err(|_| HigherCategoryError::AllocationFailed {
            requested: additional,
        })
}
