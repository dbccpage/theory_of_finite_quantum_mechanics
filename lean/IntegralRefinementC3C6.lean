import Std

/-!
# Integral refinement evidence for the three-cycle residual

This file studies one explicit refinement from an integral three-cycle to an
integral six-cycle.  It proves charge preservation for an integral block-last
cochain refinement and charge doubling for naive duplication.  These finite
statements do not identify a physical model, a quotient group, a character, or
a continuum limit.
-/

namespace PontryaginResidualDualProgramme.IntegralRefinementC3C6

/-- Integral zero- or one-cochains on the fixed three-cycle. -/
structure Z3 where
  c0 : Int
  c1 : Int
  c2 : Int
deriving DecidableEq, Repr

/-- Integral zero- or one-cochains on the factor-two six-cycle refinement. -/
structure Z6 where
  c0 : Int
  c1 : Int
  c2 : Int
  c3 : Int
  c4 : Int
  c5 : Int
deriving DecidableEq, Repr

/-- Oriented cyclic coboundary on three vertices. -/
def d0C3 (a : Z3) : Z3 :=
  { c0 := a.c1 - a.c0
    c1 := a.c2 - a.c1
    c2 := a.c0 - a.c2 }

/-- Oriented cyclic coboundary on six vertices. -/
def d0C6 (a : Z6) : Z6 :=
  { c0 := a.c1 - a.c0
    c1 := a.c2 - a.c1
    c2 := a.c3 - a.c2
    c3 := a.c4 - a.c3
    c4 := a.c5 - a.c4
    c5 := a.c0 - a.c5 }

def charge3 (v : Z3) : Int :=
  v.c0 + v.c1 + v.c2

def charge6 (v : Z6) : Int :=
  v.c0 + v.c1 + v.c2 + v.c3 + v.c4 + v.c5

def add3 (x y : Z3) : Z3 :=
  { c0 := x.c0 + y.c0
    c1 := x.c1 + y.c1
    c2 := x.c2 + y.c2 }

def sub3 (x y : Z3) : Z3 :=
  { c0 := x.c0 - y.c0
    c1 := x.c1 - y.c1
    c2 := x.c2 - y.c2 }

def add6 (x y : Z6) : Z6 :=
  { c0 := x.c0 + y.c0
    c1 := x.c1 + y.c1
    c2 := x.c2 + y.c2
    c3 := x.c3 + y.c3
    c4 := x.c4 + y.c4
    c5 := x.c5 + y.c5 }

def scale3 (n : Int) (v : Z3) : Z3 :=
  { c0 := n * v.c0
    c1 := n * v.c1
    c2 := n * v.c2 }

/-- Every integral three-cycle coboundary has zero total charge. -/
theorem d0C3_charge_zero (a : Z3) : charge3 (d0C3 a) = 0 := by
  grind [charge3, d0C3]

/-- Every integral six-cycle coboundary has zero total charge. -/
theorem d0C6_charge_zero (a : Z6) : charge6 (d0C6 a) = 0 := by
  grind [charge6, d0C6]

/-- Adding a local three-cycle repair cannot change total charge. -/
theorem charge3_invariant_under_repair (v a : Z3) :
    charge3 (add3 v (d0C3 a)) = charge3 v := by
  grind [charge3, add3, d0C3]

/-- Adding a local six-cycle repair cannot change total charge. -/
theorem charge6_invariant_under_repair (v a : Z6) :
    charge6 (add6 v (d0C6 a)) = charge6 v := by
  grind [charge6, add6, d0C6]

/-- The constant unit residual on the coarse cycle. -/
def beta3 : Z3 :=
  { c0 := 1, c1 := 1, c2 := 1 }

/-- A charge-one representative used only for the explicit reduction below. -/
def primitiveRepresentative : Z3 :=
  { c0 := 1, c1 := 0, c2 := 0 }

/-- An explicit local repair witnessing the representative reduction. -/
def reductionPotential : Z3 :=
  { c0 := 0, c1 := -2, c2 := -1 }

/-- A constructive normal-form potential for an arbitrary integral cochain. -/
def classReductionPotential (v : Z3) : Z3 :=
  { c0 := 0
    c1 := -v.c1 - v.c2
    c2 := -v.c2 }

/-- Membership in the displayed integral three-cycle coboundary image. -/
def InD0C3Image (v : Z3) : Prop :=
  ∃ a : Z3, d0C3 a = v

theorem primitive_representative_has_charge_one :
    charge3 primitiveRepresentative = 1 := by
  decide

/--
Modulo the displayed coboundary, beta3 is three times a charge-one
representative.  This equation does not identify the quotient as Z/3Z.
-/
theorem beta3_reduces_to_three_times_primitive :
    beta3 = add3 (d0C3 reductionPotential) (scale3 3 primitiveRepresentative) := by
  decide

theorem beta3_charge_is_three : charge3 beta3 = 3 := by
  decide

/--
Every integral three-cycle cochain has a constructive normal form: a displayed
local coboundary plus its total charge times the charge-one representative.
-/
theorem integral_class_reduction (v : Z3) :
    v = add3 (d0C3 (classReductionPotential v))
      (scale3 (charge3 v) primitiveRepresentative) := by
  rcases v with ⟨v0, v1, v2⟩
  simp [add3, d0C3, classReductionPotential, scale3, charge3,
    primitiveRepresentative]
  omega

/-- Two integral cochains have equal charge exactly when their difference is a coboundary. -/
theorem same_charge_iff_difference_in_d0_image (v w : Z3) :
    charge3 v = charge3 w ↔ InD0C3Image (sub3 v w) := by
  constructor
  · intro hCharge
    refine ⟨classReductionPotential (sub3 v w), ?_⟩
    grind [d0C3, classReductionPotential, sub3, charge3]
  · rintro ⟨a, ha⟩
    have hZero := d0C3_charge_zero a
    rw [ha] at hZero
    grind [charge3, sub3]

/-- Duplicate each coarse vertex potential over its two refined vertices. -/
def blockConstantPotential (a : Z3) : Z6 :=
  { c0 := a.c0, c1 := a.c0
    c2 := a.c1, c3 := a.c1
    c4 := a.c2, c5 := a.c2 }

/--
Put each coarse edge integral on the last fine edge of its block and put zero
on the first.  This is an integral refinement with no fractional coefficients.
-/
def blockLastRefine (v : Z3) : Z6 :=
  { c0 := 0, c1 := v.c0
    c2 := 0, c3 := v.c1
    c4 := 0, c5 := v.c2 }

/-- The block-constant potential map and block-last cochain map commute with d0. -/
theorem block_last_refinement_commutes_with_d0 (a : Z3) :
    d0C6 (blockConstantPotential a) = blockLastRefine (d0C3 a) := by
  grind [d0C6, blockConstantPotential, blockLastRefine, d0C3]

/-- Block-last integral refinement preserves the total charge. -/
theorem block_last_refinement_preserves_charge (v : Z3) :
    charge6 (blockLastRefine v) = charge3 v := by
  grind [charge6, blockLastRefine, charge3]

theorem refined_beta3_charge_is_three :
    charge6 (blockLastRefine beta3) = 3 := by
  rw [block_last_refinement_preserves_charge, beta3_charge_is_three]

/-- A contrasting map that repeats each coarse edge value twice. -/
def naiveDuplicate (v : Z3) : Z6 :=
  { c0 := v.c0, c1 := v.c0
    c2 := v.c1, c3 := v.c1
    c4 := v.c2, c5 := v.c2 }

/-- Naive duplication doubles total charge instead of preserving it. -/
theorem naive_duplication_doubles_charge (v : Z3) :
    charge6 (naiveDuplicate v) = 2 * charge3 v := by
  grind [charge6, naiveDuplicate, charge3]

theorem naively_duplicated_beta3_charge_is_six :
    charge6 (naiveDuplicate beta3) = 6 := by
  rw [naive_duplication_doubles_charge, beta3_charge_is_three]
  decide

/-- Stages tracked by this local evidence registry. -/
inductive EvidenceStage where
  | c3ChargeInvariant
  | c3PrimitiveReduction
  | c3IntegralClassReduction
  | c3ToC6IntegralRefinement
  | naiveDuplicationDiagnostic
  | orderThreeQuotient
  | pontryaginCharacter
  | freeZExtension
  | continuumPersistence
  | physicalIdentification
  | alphaHostRelation
deriving DecidableEq, Repr

/--
Constructor-indexed proof evidence.  Only the four finite stages have local
constructors; the registry below records no witness for any external stage.
-/
inductive StageEvidence : EvidenceStage -> Type where
  | c3Charge
      (zero : ∀ a : Z3, charge3 (d0C3 a) = 0)
      (invariant : ∀ v a : Z3, charge3 (add3 v (d0C3 a)) = charge3 v) :
      StageEvidence .c3ChargeInvariant
  | c3Reduction
      (primitive : charge3 primitiveRepresentative = 1)
      (reduction :
        beta3 = add3 (d0C3 reductionPotential) (scale3 3 primitiveRepresentative)) :
      StageEvidence .c3PrimitiveReduction
  | integralClassReduction
      (normalForm : ∀ v : Z3,
        v = add3 (d0C3 (classReductionPotential v))
          (scale3 (charge3 v) primitiveRepresentative))
      (classifies : ∀ v w : Z3,
        charge3 v = charge3 w ↔ InD0C3Image (sub3 v w)) :
      StageEvidence .c3IntegralClassReduction
  | integralRefinement
      (commutes : ∀ a : Z3,
        d0C6 (blockConstantPotential a) = blockLastRefine (d0C3 a))
      (preserves : ∀ v : Z3, charge6 (blockLastRefine v) = charge3 v) :
      StageEvidence .c3ToC6IntegralRefinement
  | duplicationDiagnostic
      (doubles : ∀ v : Z3, charge6 (naiveDuplicate v) = 2 * charge3 v) :
      StageEvidence .naiveDuplicationDiagnostic

/-- The current registry; none means unrecorded here, not mathematically impossible. -/
def registeredEvidence : (stage : EvidenceStage) -> Option (StageEvidence stage)
  | .c3ChargeInvariant =>
      some (.c3Charge d0C3_charge_zero charge3_invariant_under_repair)
  | .c3PrimitiveReduction =>
      some (.c3Reduction primitive_representative_has_charge_one
        beta3_reduces_to_three_times_primitive)
  | .c3IntegralClassReduction =>
      some (.integralClassReduction integral_class_reduction
        same_charge_iff_difference_in_d0_image)
  | .c3ToC6IntegralRefinement =>
      some (.integralRefinement block_last_refinement_commutes_with_d0
        block_last_refinement_preserves_charge)
  | .naiveDuplicationDiagnostic =>
      some (.duplicationDiagnostic naive_duplication_doubles_charge)
  | .orderThreeQuotient => none
  | .pontryaginCharacter => none
  | .freeZExtension => none
  | .continuumPersistence => none
  | .physicalIdentification => none
  | .alphaHostRelation => none

/-- A Boolean presentation of registry occupancy, not a non-derivability test. -/
def evidenceRecorded (stage : EvidenceStage) : Bool :=
  (registeredEvidence stage).isSome

/-- Model outputs from this module carry no authority effect. -/
inductive AuthorityEffect where
  | none
  | proposed
  | promoted
deriving DecidableEq, Repr

/--
The boundary fields summarize the constructor-indexed registry.  The scalar
carrier is integral here.  Merely choosing Lean real arithmetic in a successor
module would not itself be an authority violation or an authority promotion;
such a model-produced result would still have AuthorityEffect.none.
-/
structure ScopeBoundary where
  c3ChargeInvariantRecorded : Bool
  c3PrimitiveReductionRecorded : Bool
  c3IntegralClassReductionRecorded : Bool
  c3ToC6IntegralRefinementRecorded : Bool
  naiveDuplicationDiagnosticRecorded : Bool
  orderThreeQuotientRecorded : Bool
  pontryaginCharacterRecorded : Bool
  freeZExtensionRecorded : Bool
  continuumPersistenceRecorded : Bool
  physicalIdentificationRecorded : Bool
  alphaHostRelationRecorded : Bool
  leanRealArithmeticWouldViolateAuthority : Bool
  authorityEffect : AuthorityEffect
deriving DecidableEq, Repr

def scopeBoundary : ScopeBoundary :=
  { c3ChargeInvariantRecorded := evidenceRecorded .c3ChargeInvariant
    c3PrimitiveReductionRecorded := evidenceRecorded .c3PrimitiveReduction
    c3IntegralClassReductionRecorded := evidenceRecorded .c3IntegralClassReduction
    c3ToC6IntegralRefinementRecorded := evidenceRecorded .c3ToC6IntegralRefinement
    naiveDuplicationDiagnosticRecorded := evidenceRecorded .naiveDuplicationDiagnostic
    orderThreeQuotientRecorded := evidenceRecorded .orderThreeQuotient
    pontryaginCharacterRecorded := evidenceRecorded .pontryaginCharacter
    freeZExtensionRecorded := evidenceRecorded .freeZExtension
    continuumPersistenceRecorded := evidenceRecorded .continuumPersistence
    physicalIdentificationRecorded := evidenceRecorded .physicalIdentification
    alphaHostRelationRecorded := evidenceRecorded .alphaHostRelation
    leanRealArithmeticWouldViolateAuthority := false
    authorityEffect := .none }

theorem scope_boundary_summarizes_registry :
    scopeBoundary.c3ChargeInvariantRecorded = true ∧
      scopeBoundary.c3PrimitiveReductionRecorded = true ∧
      scopeBoundary.c3IntegralClassReductionRecorded = true ∧
      scopeBoundary.c3ToC6IntegralRefinementRecorded = true ∧
      scopeBoundary.naiveDuplicationDiagnosticRecorded = true ∧
      scopeBoundary.orderThreeQuotientRecorded = false ∧
      scopeBoundary.pontryaginCharacterRecorded = false ∧
      scopeBoundary.freeZExtensionRecorded = false ∧
      scopeBoundary.continuumPersistenceRecorded = false ∧
      scopeBoundary.physicalIdentificationRecorded = false ∧
      scopeBoundary.alphaHostRelationRecorded = false ∧
      scopeBoundary.leanRealArithmeticWouldViolateAuthority = false ∧
      scopeBoundary.authorityEffect = .none := by
  decide

#print axioms d0C3_charge_zero
#print axioms d0C6_charge_zero
#print axioms charge3_invariant_under_repair
#print axioms charge6_invariant_under_repair
#print axioms primitive_representative_has_charge_one
#print axioms beta3_reduces_to_three_times_primitive
#print axioms beta3_charge_is_three
#print axioms integral_class_reduction
#print axioms same_charge_iff_difference_in_d0_image
#print axioms block_last_refinement_commutes_with_d0
#print axioms block_last_refinement_preserves_charge
#print axioms refined_beta3_charge_is_three
#print axioms naive_duplication_doubles_charge
#print axioms naively_duplicated_beta3_charge_is_six
#print axioms scope_boundary_summarizes_registry

end PontryaginResidualDualProgramme.IntegralRefinementC3C6
