import Mathlib.Data.Fintype.BigOperators
import Mathlib.Data.Fintype.Sum
import Mathlib.Data.Fintype.Prod
import Mathlib.Logic.Equiv.Basic

/-!
# The root coproduct Real_0 = PrimitiveDifference + Structure: what the construction does and does not say

AuthorityEffect: None.  This node is an ADMITTED PRIMITIVE.  Nothing below derives the posit that the
two channels exist, or that either reduces to the other; the results show only that the typed coproduct
construction is a genuine categorical coproduct and is NEUTRAL about the two posits.

Scope: `Real0 PD S` has the same two-constructor shape as `FiniteCosmology.Ontology.Real0` in
`lean4/OntologyBasic.lean` (constructors `primitiveDifference` and `structure` taking the payload of each
channel); here the payload types `PD`, `S` are arbitrary types, because that file may not be imported.
Properties of the actual `OntologyBasic.Real0` (its universe-polymorphic record payloads) are not claimed.
The source bridge theorem `pg_root_coproduct_inert_diamond_and_six_operation_separation` is a conjunction
of integer identities (`0 != 1`, `d + 0 = d`, `0 + s = s`) and a `Fin 6` index coding; it says nothing
about a coproduct, which is why the general statements are proved here instead.
-/

namespace RootDiffStructure

variable {PD S C : Type}

/-- Same shape as `FiniteCosmology.Ontology.Real0`: a tagged union of the two channels' payloads. -/
inductive Real0 (PD S : Type) where
  | primitiveDifference : PD → Real0 PD S
  | structureChannel : S → Real0 PD S

namespace Real0

/-- Eliminator (the copairing of two maps). -/
def elim (f : PD → C) (g : S → C) : Real0 PD S → C
  | primitiveDifference d => f d
  | structureChannel s => g s

@[simp] theorem elim_pd (f : PD → C) (g : S → C) (d : PD) : elim f g (primitiveDifference d) = f d := rfl
@[simp] theorem elim_st (f : PD → C) (g : S → C) (s : S) : elim f g (structureChannel s) = g s := rfl

/-- Comparison with the Mathlib sum type. -/
def toSum : Real0 PD S → PD ⊕ S
  | primitiveDifference d => Sum.inl d
  | structureChannel s => Sum.inr s

def ofSum : PD ⊕ S → Real0 PD S
  | Sum.inl d => primitiveDifference d
  | Sum.inr s => structureChannel s

end Real0

/-- `Real0 PD S` is equivalent to `PD ⊕ S`. -/
def real0EquivSum : Real0 PD S ≃ PD ⊕ S where
  toFun := Real0.toSum
  invFun := Real0.ofSum
  left_inv := by intro x; cases x <;> rfl
  right_inv := by intro x; cases x <;> rfl

open Real0

/-- Both injections are injective. -/
theorem pd_injective : Function.Injective (primitiveDifference : PD → Real0 PD S) := by
  intro a b h; cases h; rfl

theorem st_injective : Function.Injective (structureChannel : S → Real0 PD S) := by
  intro a b h; cases h; rfl

/-- The two channels have disjoint ranges: no difference item equals a structure item. -/
theorem pd_ne_st (d : PD) (s : S) : (primitiveDifference d : Real0 PD S) ≠ structureChannel s := by
  intro h; cases h

/-- Every element lies in one of the two channels. -/
theorem exhaustive (x : Real0 PD S) : (∃ d, x = primitiveDifference d) ∨ (∃ s, x = structureChannel s) := by
  cases x with
  | primitiveDifference d => exact Or.inl ⟨d, rfl⟩
  | structureChannel s => exact Or.inr ⟨s, rfl⟩

/-- No map `g : S → PD` identifies a structure item with a difference item inside the coproduct. -/
theorem no_identification (g : S → PD) (s : S) : (structureChannel s : Real0 PD S) ≠ primitiveDifference (g s) :=
  fun h => pd_ne_st (g s) s h.symm

/-- Universal property: a pair of maps out of the channels has exactly one extension to `Real0`. -/
theorem universal (f : PD → C) (g : S → C) :
    ∃! h : Real0 PD S → C, (∀ d, h (primitiveDifference d) = f d) ∧ (∀ s, h (structureChannel s) = g s) := by
  refine ⟨Real0.elim f g, ⟨fun _ => rfl, fun _ => rfl⟩, ?_⟩
  rintro h ⟨h1, h2⟩
  funext x
  cases x with
  | primitiveDifference d => exact h1 d
  | structureChannel s => exact h2 s

/-- Maps out of the coproduct are pairs of maps out of the channels. -/
def mapsOutEquiv : (Real0 PD S → C) ≃ (PD → C) × (S → C) where
  toFun h := (fun d => h (primitiveDifference d), fun s => h (structureChannel s))
  invFun p := Real0.elim p.1 p.2
  left_inv := by
    intro h; funext x; cases x <;> rfl
  right_inv := by
    intro p; rfl

instance [Fintype PD] [Fintype S] : Fintype (Real0 PD S) := Fintype.ofEquiv (PD ⊕ S) real0EquivSum.symm

theorem card_real0 [Fintype PD] [Fintype S] : Fintype.card (Real0 PD S) = Fintype.card PD + Fintype.card S := by
  rw [Fintype.card_congr real0EquivSum, Fintype.card_sum]

/-- The number of maps out of the coproduct is the product of the numbers of maps out of the channels. -/
theorem card_maps_out [Fintype PD] [Fintype S] [Fintype C] [DecidableEq PD] [DecidableEq S] [DecidableEq (Real0 PD S)] :
    Fintype.card (Real0 PD S → C) = Fintype.card (PD → C) * Fintype.card (S → C) := by
  rw [Fintype.card_congr mapsOutEquiv, Fintype.card_prod]

/-- Same count in power form: `|C|^(|PD| + |S|)`. -/
theorem card_maps_out_pow [Fintype PD] [Fintype S] [Fintype C] [DecidableEq PD] [DecidableEq S] [DecidableEq (Real0 PD S)] :
    Fintype.card (Real0 PD S → C) = Fintype.card C ^ (Fintype.card PD + Fintype.card S) := by
  rw [Fintype.card_fun, card_real0]

/-! ## No reduction of either channel to the other in general -/

/-- A reduction of the structure channel to the difference channel, in the strongest sense: a map out of the
coproduct that is the identity on the difference channel. -/
def RetractsToPD (PD S : Type) : Prop := ∃ ρ : Real0 PD S → PD, ∀ d, ρ (primitiveDifference d) = d

def RetractsToS (PD S : Type) : Prop := ∃ ρ : Real0 PD S → S, ∀ s, ρ (structureChannel s) = s

/-- Such a retraction exists iff the difference channel is nonempty or the structure channel is empty.
In particular with an empty difference channel and a nonempty structure channel there is NO reduction. -/
theorem retracts_to_pd_iff : RetractsToPD PD S ↔ (Nonempty PD ∨ IsEmpty S) := by
  constructor
  · rintro ⟨ρ, _⟩
    by_cases hs : Nonempty S
    · exact Or.inl ⟨ρ (structureChannel hs.some)⟩
    · exact Or.inr (not_nonempty_iff.mp hs)
  · rintro (hd | hS)
    · exact ⟨Real0.elim id (fun _ => hd.some), fun _ => rfl⟩
    · exact ⟨Real0.elim id (fun s => (hS.false s).elim), fun _ => rfl⟩

theorem retracts_to_s_iff : RetractsToS PD S ↔ (Nonempty S ∨ IsEmpty PD) := by
  constructor
  · rintro ⟨ρ, _⟩
    by_cases hd : Nonempty PD
    · exact Or.inl ⟨ρ (primitiveDifference hd.some)⟩
    · exact Or.inr (not_nonempty_iff.mp hd)
  · rintro (hs | hP)
    · exact ⟨Real0.elim (fun _ => hs.some) id, fun _ => rfl⟩
    · exact ⟨Real0.elim (fun d => (hP.false d).elim) id, fun _ => rfl⟩

/-- Empty difference channel, nonempty structure channel: no reduction of structure to difference. -/
theorem no_reduction_to_pd (hP : IsEmpty PD) (hS : Nonempty S) : ¬ RetractsToPD PD S := by
  rw [retracts_to_pd_iff]
  rintro (hd | h)
  · exact not_nonempty_iff.mpr hP hd
  · exact not_nonempty_iff.mpr h hS

theorem no_reduction_to_s (hS : IsEmpty S) (hP : Nonempty PD) : ¬ RetractsToS PD S := by
  rw [retracts_to_s_iff]
  rintro (hs | h)
  · exact not_nonempty_iff.mpr hS hs
  · exact not_nonempty_iff.mpr h hP

/-- Whenever both channels are inhabited (as the record types of the real `OntologyBasic.Real0` are), retractions onto
each channel exist, so bare existence of such a map is NOT a non-reduction statement there. -/
theorem retractions_both_ways_of_nonempty (hP : Nonempty PD) (hS : Nonempty S) : RetractsToPD PD S ∧ RetractsToS PD S :=
  ⟨retracts_to_pd_iff.mpr (Or.inl hP), retracts_to_s_iff.mpr (Or.inl hS)⟩

/-! ## The two posits are independent of the construction -/

/-- The coproduct is nonempty iff at least one channel is. -/
theorem nonempty_real0_iff : Nonempty (Real0 PD S) ↔ (Nonempty PD ∨ Nonempty S) := by
  constructor
  · rintro ⟨x⟩
    cases x with
    | primitiveDifference d => exact Or.inl ⟨d⟩
    | structureChannel s => exact Or.inr ⟨s⟩
  · rintro (hd | hs)
    · exact ⟨primitiveDifference hd.some⟩
    · exact ⟨structureChannel hs.some⟩

/-- The construction alone yields no element: with both channels empty, `Real0` is empty. -/
theorem real0_empty_of_both_empty : IsEmpty (Real0 Empty Empty) := ⟨fun x => by cases x with
  | primitiveDifference d => exact d.elim
  | structureChannel s => exact s.elim⟩

/-- Every combination of the two posits is realised by some pair of channels: neither posit follows from the
construction, nor from the other posit. -/
theorem posits_independent (a b : Bool) :
    ∃ PD S : Type, (Nonempty PD ↔ a = true) ∧ (Nonempty S ↔ b = true) :=
  ⟨PLift (a = true), PLift (b = true), ⟨fun ⟨x⟩ => x.down, fun h => ⟨⟨h⟩⟩⟩, ⟨fun ⟨x⟩ => x.down, fun h => ⟨⟨h⟩⟩⟩⟩

end RootDiffStructure

#print axioms RootDiffStructure.pd_injective
#print axioms RootDiffStructure.st_injective
#print axioms RootDiffStructure.pd_ne_st
#print axioms RootDiffStructure.exhaustive
#print axioms RootDiffStructure.no_identification
#print axioms RootDiffStructure.universal
#print axioms RootDiffStructure.card_real0
#print axioms RootDiffStructure.card_maps_out
#print axioms RootDiffStructure.card_maps_out_pow
#print axioms RootDiffStructure.retracts_to_pd_iff
#print axioms RootDiffStructure.retracts_to_s_iff
#print axioms RootDiffStructure.no_reduction_to_pd
#print axioms RootDiffStructure.no_reduction_to_s
#print axioms RootDiffStructure.retractions_both_ways_of_nonempty
#print axioms RootDiffStructure.nonempty_real0_iff
#print axioms RootDiffStructure.real0_empty_of_both_empty
#print axioms RootDiffStructure.posits_independent
