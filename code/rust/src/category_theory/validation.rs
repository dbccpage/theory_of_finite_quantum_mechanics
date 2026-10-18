//! Validation — cross-cutting validation unit declarations.
//!
//! Maps directly to spec §4 and §10 validation unit lists.
//! Each validation unit is a single-property checker.

// ---------------------------------------------------------------------------
// Validation unit identifiers (spec §4)
// ---------------------------------------------------------------------------

/// Identifiers for all functor validation units.
///
/// These correspond 1:1 with the spec's declared validation obligations.
/// They are used as keys in validation reports and contract audit trails.
#[derive(Debug, Clone, Copy, PartialEq, Eq, Hash)]
pub enum FunctorValidation {
    Name,
    MappingDomain,
    // Covariant functor (spec §4)
    ObjectTotality,
    MorphismTotality,
    BoundaryPreservation,
    IdentityPreservation,
    CompositionPreservation,

    // Contravariant functor (spec §4)
    ContravariantIdentityPreservation,
    ContravariantCompositionReversal,
}

#[derive(Debug, Clone, Copy, PartialEq, Eq, Hash)]
pub enum NatTransValidation {
    Name,
    FunctorBinding,
    ComponentDomain,
    ComponentBoundary,
    NaturalitySquare,
}

#[derive(Debug, Clone, Copy, PartialEq, Eq, Hash)]
pub enum AdjunctionValidation {
    UnitNaturality,
    CounitNaturality,
    TriangleLeft,
    TriangleRight,
    HomSetMembership,
    HomBijectionTotality,
    HomBijectionRoundTrip,
}

#[derive(Debug, Clone, Copy, PartialEq, Eq, Hash)]
pub enum ProfunctorValidation {
    DimapIdentity,
    DimapComposition,
    StrongFirstSecond,
    ClosedInteraction,
}

#[derive(Debug, Clone, Copy, PartialEq, Eq, Hash)]
pub enum HigherFunctorValidation {
    TwoFunctorObjectMap,
    TwoFunctorOneMorphismMap,
    TwoFunctorTwoMorphismMap,
    TwoFunctorCompositionPreservation,
    TwoFunctorIdentityPreservation,
    PseudofunctorPentagonCoherence,
    PseudofunctorTriangleCoherence,
    InterchangeLaw,
}

#[derive(Debug, Clone, Copy, PartialEq, Eq, Hash)]
pub enum CoendValidation {
    /// Quotient respects all morphisms (spec §14).
    Dinaturality,
}

#[derive(Debug, Clone, Copy, PartialEq, Eq, Hash)]
pub enum KanExtensionValidation {
    /// Lan is universal (spec §16).
    UniversalProperty,
    /// Lan_id F ≅ F (Yoneda unit law, spec §16).
    YonedaUnitLaw,
}

#[derive(Debug, Clone, Copy, PartialEq, Eq, Hash)]
pub enum CauchyValidation {
    /// r ∘ s = id_R, s ∘ r = e (spec §17).
    IdempotentSplitting,
    /// All idempotents split (spec §17).
    CauchyCompleteness,
}

#[derive(Debug, Clone, Copy, PartialEq, Eq, Hash)]
pub enum MonadValidation {
    /// μ ∘ Tη = id_T (spec §22).
    UnitLeft,
    /// μ ∘ ηT = id_T (spec §22).
    UnitRight,
    /// μ ∘ Tμ = μ ∘ μT (spec §22).
    Associativity,
}

#[derive(Debug, Clone, Copy, PartialEq, Eq, Hash)]
pub enum CondensationValidation {
    /// Base splitting laws: r∘s = id, s∘r = e (spec §21).
    BaseSplitting,
    /// Homotopy coherence at each level (spec §21).
    CoherenceWitness,
    /// All condensations split (∞-Cauchy, spec §21).
    InfinityCauchyCompleteness,
}

#[derive(Debug, Clone, Copy, PartialEq, Eq, Hash)]
pub enum LawvereValidation {
    /// Theory respects finite products (spec §25).
    ProductPreservation,
    /// Composition = substitution (spec §25).
    SubstitutionAssociativity,
    /// All idempotent operations split (spec §25).
    CauchyCompleteness,
    /// Theory ↔ finitary monad correspondence (spec §25).
    MonadEquivalence,
}

#[derive(Debug, Clone, Copy, PartialEq, Eq, Hash)]
pub enum OperadValidation {
    /// Tree-substitution is associative (spec §26).
    Associativity,
    /// Identity operations act as units (spec §26).
    Unit,
    /// Symmetric group action is compatible (spec §26).
    Equivariance,
    /// Homotopy coherence at each level (spec §26).
    InfinityCoherence,
}

#[derive(Debug, Clone, Copy, PartialEq, Eq, Hash)]
pub enum FiniteCategoryValidation {
    ObjectReference,
    MorphismBoundary,
    IdentityTotality,
    IdentityLaw,
    CompositionTotality,
    CompositionClosure,
    CompositionBoundary,
    Associativity,
}

#[derive(Debug, Clone, Copy, PartialEq, Eq, Hash)]
pub enum RewritingValidation {
    /// All critical pairs join (local confluence).
    LocalConfluence,
    /// No infinite rewrite chains (termination).
    Termination,
    /// 2-cells resolve all non-confluent pairs (homotopy resolution).
    HomotopyResolution,
    /// Higher cells are coherent at declared truncation level.
    TruncationCoherence,
}

#[derive(Debug, Clone, PartialEq, Eq, Hash)]
pub enum ValidationUnit {
    FiniteCategory(FiniteCategoryValidation),
    Functor(FunctorValidation),
    NatTrans(NatTransValidation),
    Adjunction(AdjunctionValidation),
    Profunctor(ProfunctorValidation),
    HigherFunctor(HigherFunctorValidation),
    Coend(CoendValidation),
    KanExtension(KanExtensionValidation),
    Cauchy(CauchyValidation),
    Monad(MonadValidation),
    Condensation(CondensationValidation),
    Lawvere(LawvereValidation),
    Operad(OperadValidation),
    Rewriting(RewritingValidation),
    Other(String),
}

#[derive(Debug, Clone, Copy, PartialEq, Eq, Hash)]
pub enum ValidationSeverity {
    Error,
    Warning,
    Info,
}

#[derive(Debug, Clone, PartialEq, Eq, Hash)]
pub enum ValidationLocation {
    Global,
    Object(String),
    Morphism(String),
    Named(String),
    Boundary {
        morphism: String,
        source: String,
        target: String,
    },
    Composition {
        first: String,
        second: String,
        composite: Option<String>,
    },
}

#[derive(Debug, Clone, PartialEq, Eq)]
pub struct ValidationViolation {
    pub unit: ValidationUnit,
    pub location: ValidationLocation,
    pub message: String,
    pub severity: ValidationSeverity,
}

impl ValidationViolation {
    pub fn new(
        unit: ValidationUnit,
        location: ValidationLocation,
        message: impl Into<String>,
        severity: ValidationSeverity,
    ) -> Self {
        Self {
            unit,
            location,
            message: message.into(),
            severity,
        }
    }
}

// ---------------------------------------------------------------------------
// Validation report
// ---------------------------------------------------------------------------

/// A single validation result.
#[derive(Debug, Clone)]
pub struct ValidationResult {
    pub unit: String,
    pub passed: bool,
    pub violations: Vec<String>,
}

impl ValidationResult {
    pub fn pass(unit: &str) -> Self {
        Self {
            unit: unit.into(),
            passed: true,
            violations: Vec::new(),
        }
    }

    pub fn fail(unit: &str, violations: Vec<String>) -> Self {
        Self {
            unit: unit.into(),
            passed: false,
            violations,
        }
    }
}

/// A collection of validation results for a functor or related structure.
#[derive(Debug, Clone)]
pub struct ValidationReport {
    pub target_name: String,
    pub results: Vec<ValidationResult>,
    pub typed_violations: Vec<ValidationViolation>,
}

impl ValidationReport {
    pub fn new(name: &str) -> Self {
        Self {
            target_name: name.into(),
            results: Vec::new(),
            typed_violations: Vec::new(),
        }
    }

    pub fn add(&mut self, result: ValidationResult) {
        self.results.push(result);
    }

    pub fn add_violation(&mut self, violation: ValidationViolation) {
        self.results.push(ValidationResult::fail(
            &format!("{:?}", violation.unit),
            vec![violation.message.clone()],
        ));
        self.typed_violations.push(violation);
    }

    pub fn add_typed(&mut self, unit: &str, violations: Vec<ValidationViolation>) {
        if violations.is_empty() {
            self.results.push(ValidationResult::pass(unit));
        } else {
            let messages = violations
                .iter()
                .map(|violation| violation.message.clone())
                .collect();
            self.results.push(ValidationResult::fail(unit, messages));
            self.typed_violations.extend(violations);
        }
    }

    pub fn all_passed(&self) -> bool {
        self.results.iter().all(|r| r.passed) && self.typed_violations.is_empty()
    }

    pub fn failure_count(&self) -> usize {
        self.results.iter().filter(|r| !r.passed).count()
    }

    pub fn violation_count(&self) -> usize {
        self.typed_violations.len()
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn validation_report_all_pass() {
        let mut report = ValidationReport::new("TestFunctor");
        report.add(ValidationResult::pass("identity"));
        report.add(ValidationResult::pass("composition"));
        assert!(report.all_passed());
        assert_eq!(report.failure_count(), 0);
    }

    #[test]
    fn validation_report_with_failure() {
        let mut report = ValidationReport::new("BadFunctor");
        report.add(ValidationResult::pass("identity"));
        report.add(ValidationResult::fail(
            "composition",
            vec!["F(gf) != F(g)∘F(f)".into()],
        ));
        assert!(!report.all_passed());
        assert_eq!(report.failure_count(), 1);
    }
}
