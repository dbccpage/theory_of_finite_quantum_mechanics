import «qm_lift_classification_axioms»
import «qm_conditional_uniqueness»

/-!
# W5.6 / W5.8 — lift classification and conditional-uniqueness boundary

This module unifies the two previously self-contained registry surfaces behind
one generic classification record. The declared AX-LIFT-V0 registry is
inhabited and proved unique. Full Jordan reconstruction and absolute complex
selection remain typed external interfaces with no inhabitant constructed.

`LIB-014519` supports a Jordan-representation route from explicit operational
assumptions; it is not used as a proof that AX-LIFT-V0 selects complex Hilbert
among every mathematical lift.

AuthorityEffect: None.
-/

namespace QM
namespace LiftBoundary

/-! ## A generic, explicitly scoped classification theorem -/

/-- A classification boundary names its candidate type, satisfying predicate,
and distinguished representative. Completeness never extends beyond
`Candidate` without constructing a different boundary. -/
structure NamedClassification where
  Candidate : Type
  complex : Candidate
  Satisfies : Candidate → Prop
  axiomSetId : String
  axiomSetId_eq : axiomSetId = "AX-LIFT-V0"
  complex_satisfies : Satisfies complex
  conditional_unique : ∀ L, Satisfies L → L = complex

theorem satisfies_iff_complex (B : NamedClassification) (L : B.Candidate) :
    B.Satisfies L ↔ L = B.complex := by
  constructor
  · exact B.conditional_unique L
  · intro h
    simpa [h] using B.complex_satisfies

/-- Conditional uniqueness includes existence, not only exclusion. -/
theorem existsUnique_satisfier (B : NamedClassification) :
    ∃! L : B.Candidate, B.Satisfies L := by
  refine ⟨B.complex, B.complex_satisfies, ?_⟩
  intro L hL
  exact B.conditional_unique L hL

/-! ## The only inhabited classification boundary in this packet -/

open LiftClassification

def axLiftV0Registry : NamedClassification where
  Candidate := LiftClassification.NamedLift
  complex := .complexHilbert
  Satisfies := LiftClassification.satisfiesAxLiftV0
  axiomSetId := "AX-LIFT-V0"
  axiomSetId_eq := rfl
  complex_satisfies := LiftClassification.complex_satisfies_v0
  conditional_unique := by
    intro L h
    cases L with
    | complexHilbert => rfl
    | realHilbert => exact absurd h LiftClassification.real_fails_v0
    | quaternionicHilbert => exact absurd h LiftClassification.quat_fails_v0

theorem registry_satisfies_iff_complex
    (L : LiftClassification.NamedLift) :
    LiftClassification.satisfiesAxLiftV0 L ↔
      L = LiftClassification.NamedLift.complexHilbert :=
  satisfies_iff_complex axLiftV0Registry L

theorem registry_has_exactly_one_satisfier :
    ∃! L : LiftClassification.NamedLift,
      LiftClassification.satisfiesAxLiftV0 L :=
  existsUnique_satisfier axLiftV0Registry

/-- The historical W5.6 and W5.8 modules independently select their own
`complexHilbert` labels. This theorem binds both results without identifying
their separately declared carrier types by coercion. -/
theorem legacy_registry_surfaces_concordant :
    (∀ L : LiftClassification.NamedLift,
      LiftClassification.satisfiesAxLiftV0 L ↔
        L = LiftClassification.NamedLift.complexHilbert) ∧
    (∀ L : ConditionalUniqueness.NamedLift,
      ConditionalUniqueness.satisfiesAxLiftV0 L ↔
        L = ConditionalUniqueness.NamedLift.complexHilbert) :=
  ⟨registry_satisfies_iff_complex,
    ConditionalUniqueness.satisfies_v0_iff_complex⟩

/-! ## Typed external boundaries — deliberately uninhabited here -/

/-- Import shape supported by the operational Jordan route documented in
`LIB-014519`: finite dimensionality plus sharpness, a conjugate, and arbitrary
reversible filters yield a Jordan representation. This packet supplies no
value of this type. -/
structure WilceJordanImport where
  Model : Type
  FiniteDimensional : Model → Prop
  Sharp : Model → Prop
  HasConjugate : Model → Prop
  HasArbitraryReversibleFilters : Model → Prop
  HasEuclideanJordanRepresentation : Model → Prop
  jordanize : ∀ A,
    FiniteDimensional A → Sharp A → HasConjugate A →
    HasArbitraryReversibleFilters A → HasEuclideanJordanRepresentation A
  sourceId : String
  sourceId_eq : sourceId = "LIB-014519"

/-- Continuity is a distinct host import, never a property of the finite
`FinL1` registry by declaration. The interface records the exact connectedness
obligation without constructing a transformation group. -/
structure ContinuousReversibleDynamicsImport where
  State : Type
  Transform : Type
  identity : Transform
  act : Transform → State → State
  Reversible : Transform → Prop
  ConnectedToIdentity : Transform → Prop
  identity_reversible : Reversible identity
  every_reversible_connected : ∀ g, Reversible g → ConnectedToIdentity g
  hostId : String

/-- A stronger, separate import would be required to select complex Hilbert
from an all-lifts continuum candidate type. Neither Wilce's Jordan route nor
the finite registry theorem constructs this interface. -/
structure AbsoluteComplexSelectionImport where
  Candidate : Type
  complex : Candidate
  SatisfiesContinuumAxioms : Candidate → Prop
  complex_satisfies : SatisfiesContinuumAxioms complex
  selects_complex : ∀ L, SatisfiesContinuumAxioms L → L = complex
  namedAxiomSet : String

/-- Registry uniqueness is available without an absolute selection import. -/
theorem registry_result_does_not_require_absolute_import :
    ∃! L : LiftClassification.NamedLift,
      LiftClassification.satisfiesAxLiftV0 L :=
  registry_has_exactly_one_satisfier

def lift_boundary_authority_effect_none : True := True.intro

end LiftBoundary
end QM
