/-
Provenance (recovery, 2026-10-21)
  source    : C:\.ana\coda_university\coda_research\authorization_an_incompleteness_theory\formal\primitive_difference_authorization_models.lean
  recovered : 2026-10-21
  status    : ported to Lean 4.35.0; statements unchanged
  module    : AuthIncompleteness.PDModels
-/
/-!
# Primitive Difference to authorization: finite extension models

Paper key: `authorization_an_incompleteness_theory`

This is the first finite countermodel for AIT-PD0. It uses a deliberately
small Primitive Difference analogue on Bool and exhibits two authorization
extensions indexed by exactly the same primitive object. The extensions
disagree about validity and terminal policy.

This proves non-uniqueness for this finite model. It does not yet bind to
the full J011 PrimitiveDifference interface, derive a report, or prove a
general naturality theorem about all Primitive Differences.

AuthorityEffect: None.
-/

namespace AuthorizationIncompleteness.PrimitiveDifferenceModels

/-- A minimal raw difference interface. The later J011 binding must use
    its complete laws; this file deliberately does not claim to do so. -/
structure RawPrimitiveDifference where
  Carrier : Type
  mark : Carrier -> Carrier -> Bool
  zero : Bool -> Bool

/-- A concrete carrier with two unequal marks and a Boolean difference
    mark. -/
def boolPrimitive : RawPrimitiveDifference where
  Carrier := Bool
  mark := fun left right =>
    match left with
    | false => right
    | true => !right
  zero := fun mark => !mark

theorem boolPrimitive_has_two_marks :
    (true : boolPrimitive.Carrier) != false := by
  decide

theorem boolPrimitive_marks_the_pair :
    boolPrimitive.mark true false = true := by
  rfl

/-- Validity and terminal policy are additional structure over the same
    raw primitive. `terminal` maps an evaluation bit to a policy bit. -/
structure AuthorizationExtension (primitive : RawPrimitiveDifference) where
  valid : primitive.Carrier -> Bool
  terminal : Bool -> Bool

/-- One admissible extension: retain the Boolean value and approve a
    positive evaluation. -/
def identityExtension : AuthorizationExtension boolPrimitive where
  valid := id
  terminal := id

/-- A distinct extension over the same primitive: reverse the validity
    reading and reject every evaluation. -/
def rejectingExtension : AuthorizationExtension boolPrimitive where
  valid := fun value => !value
  terminal := fun _ => false

/-- The two extensions have the same primitive index but disagree about
    the validity of the same marked carrier point. -/
theorem same_primitive_extensions_split_validity :
    identityExtension.valid true = true /\
      rejectingExtension.valid true = false := by
  exact ⟨rfl, rfl⟩

/-- The same primitive index also permits distinct terminal policies. -/
theorem same_primitive_extensions_split_policy :
    identityExtension.terminal true = true /\
      rejectingExtension.terminal true = false := by
  exact ⟨rfl, rfl⟩

/-- The finite non-uniqueness package for AIT-PD0. -/
theorem primitive_interface_has_distinct_authorization_extensions :
    (true : boolPrimitive.Carrier) != false /\
      boolPrimitive.mark true false = true /\
      identityExtension.valid true = true /\
      rejectingExtension.valid true = false /\
      identityExtension.terminal true = true /\
      rejectingExtension.terminal true = false := by
  exact ⟨boolPrimitive_has_two_marks, boolPrimitive_marks_the_pair,
    same_primitive_extensions_split_validity.1,
    same_primitive_extensions_split_validity.2,
    same_primitive_extensions_split_policy.1,
    same_primitive_extensions_split_policy.2⟩

end AuthorizationIncompleteness.PrimitiveDifferenceModels

#print axioms AuthorizationIncompleteness.PrimitiveDifferenceModels.boolPrimitive_has_two_marks
#print axioms AuthorizationIncompleteness.PrimitiveDifferenceModels.same_primitive_extensions_split_validity
#print axioms AuthorizationIncompleteness.PrimitiveDifferenceModels.same_primitive_extensions_split_policy
#print axioms AuthorizationIncompleteness.PrimitiveDifferenceModels.primitive_interface_has_distinct_authorization_extensions
