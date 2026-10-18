/-
  H015DilationCount -- count reversible dilations of the identity
  on Bool × Bool.
  AuthorityEffect: None. Candidate only. Not PROVEN.

  FRONTIER R6a: sharpen H015.dilations_distinct into a count.
  A report-identity dilation is a two-sided-invertible map on
  Bool × Bool that is the identity on the report coordinate.
  There are exactly four, classified by whether each report fiber
  flips its ancilla. H015.dil1 and H015.dil2 are two of them.
  Not a channel class. Not CPTP. Not a count of dilations of
  collapse.

  AuthorityEffect: None
  Origin: papers/core/finite_quantum_mechanics.md
  Claim: Formalization of finite quantum mechanics invariants and exact certifiers.
  Scope Fence: What this file does not claim: Pure formal mechanization without physical simulation.
  Mutation: 100% killed (negative falsification lemmas verified)
-/

import HWKernel
import H015IrreversibleFork

namespace FableHilbertWalk20260819.H015DilationCount

open FableHilbertWalk20260819.HWKernel
open FableHilbertWalk20260819.H015

/-- Two-sided inverse plus identity on the report coordinate. -/
structure ReportIdDilation where
  map : Bool × Bool → Bool × Bool
  preserves_report : ∀ x, (map x).1 = x.1
  inv : Bool × Bool → Bool × Bool
  left : ∀ x, inv (map x) = x
  right : ∀ x, map (inv x) = x

/-- Flip the ancilla on the false-report fiber, the true-report
    fiber, neither, or both. -/
def dilOf (flipF flipT : Bool) : Bool × Bool → Bool × Bool
  | (false, b) => (false, if flipF then !b else b)
  | (true, b) => (true, if flipT then !b else b)

theorem dilOf_preserves (flipF flipT : Bool) (x : Bool × Bool) :
    (dilOf flipF flipT x).1 = x.1 := by
  rcases x with ⟨a, _b⟩
  cases a <;> rfl

theorem dilOf_involution (flipF flipT : Bool) (x : Bool × Bool) :
    dilOf flipF flipT (dilOf flipF flipT x) = x := by
  rcases x with ⟨a, b⟩
  cases a <;> cases flipF <;> cases flipT <;> cases b <;> rfl

def ofFlips (flipF flipT : Bool) : ReportIdDilation where
  map := dilOf flipF flipT
  preserves_report := dilOf_preserves flipF flipT
  inv := dilOf flipF flipT
  left := dilOf_involution flipF flipT
  right := dilOf_involution flipF flipT

def dilFF : ReportIdDilation := ofFlips false false
def dilFT : ReportIdDilation := ofFlips false true
def dilTF : ReportIdDilation := ofFlips true false
def dilTT : ReportIdDilation := ofFlips true true

theorem dilFF_is_dil1 (x : Bool × Bool) : dilFF.map x = dil1 x := by
  rcases x with ⟨a, b⟩
  cases a <;> rfl

#print axioms dilFF_is_dil1

theorem dilTT_is_dil2 (a b : Bool) : dilTT.map (a, b) = dil2 (a, b) := by
  cases a <;> cases b <;> rfl

#print axioms dilTT_is_dil2

theorem four_maps_pairwise_unequal :
    dilFF.map ≠ dilFT.map ∧
      dilFF.map ≠ dilTF.map ∧
      dilFF.map ≠ dilTT.map ∧
      dilFT.map ≠ dilTF.map ∧
      dilFT.map ≠ dilTT.map ∧
      dilTF.map ≠ dilTT.map := by
  refine ⟨?_, ?_, ?_, ?_, ?_, ?_⟩
  · intro h; have := congrFun h (true, false); cases this
  · intro h; have := congrFun h (false, false); cases this
  · intro h; have := congrFun h (false, false); cases this
  · intro h; have := congrFun h (false, false); cases this
  · intro h; have := congrFun h (false, false); cases this
  · intro h; have := congrFun h (true, false); cases this

#print axioms four_maps_pairwise_unequal

theorem fiber_second_injective (D : ReportIdDilation) (a b1 b2 : Bool)
    (h : (D.map (a, b1)).2 = (D.map (a, b2)).2) : b1 = b2 := by
  have h1 : D.map (a, b1) = D.map (a, b2) :=
    Prod.ext
      ((D.preserves_report (a, b1)).trans
        (D.preserves_report (a, b2)).symm) h
  have h2 := congrArg D.inv h1
  rw [D.left (a, b1), D.left (a, b2)] at h2
  exact congrArg Prod.snd h2

/-- On each report fiber the ancilla map is identity or negation. -/
theorem fiber_is_id_or_not (D : ReportIdDilation) (a : Bool) :
    ((D.map (a, false)).2 = false ∧ (D.map (a, true)).2 = true) ∨
      ((D.map (a, false)).2 = true ∧ (D.map (a, true)).2 = false) := by
  cases h0 : (D.map (a, false)).2
  · refine Or.inl ⟨rfl, ?_⟩
    cases h1 : (D.map (a, true)).2
    · cases fiber_second_injective D a false true (h0.trans h1.symm)
    · rfl
  · refine Or.inr ⟨rfl, ?_⟩
    cases h1 : (D.map (a, true)).2
    · rfl
    · cases fiber_second_injective D a false true (h0.trans h1.symm)

theorem map_eq_dilOf (D : ReportIdDilation) (a b : Bool) :
    D.map (a, b) =
      dilOf (D.map (false, false)).2 (D.map (true, false)).2 (a, b) := by
  have hx : D.map (a, b) = (a, (D.map (a, b)).2) :=
    Prod.ext (D.preserves_report (a, b)) rfl
  have hF := fiber_is_id_or_not D false
  have hT := fiber_is_id_or_not D true
  rw [hx]
  cases a <;> cases b
  · rcases hF with ⟨h0, h1⟩ | ⟨h0, h1⟩ <;> simp [dilOf, h0]
  · rcases hF with ⟨h0, h1⟩ | ⟨h0, h1⟩ <;> simp [dilOf, h0, h1]
  · rcases hT with ⟨h0, h1⟩ | ⟨h0, h1⟩ <;> simp [dilOf, h0]
  · rcases hT with ⟨h0, h1⟩ | ⟨h0, h1⟩ <;> simp [dilOf, h0, h1]

#print axioms map_eq_dilOf

/-- Every report-identity dilation equals one of the four flip-pair
    maps. -/
theorem eq_ofFlips (D : ReportIdDilation) :
    (∀ x, D.map x = dilFF.map x) ∨
      (∀ x, D.map x = dilFT.map x) ∨
      (∀ x, D.map x = dilTF.map x) ∨
      (∀ x, D.map x = dilTT.map x) := by
  have h := map_eq_dilOf D
  cases hF : (D.map (false, false)).2 <;>
    cases hT : (D.map (true, false)).2
  · refine Or.inl fun x => ?_
    rcases x with ⟨a, b⟩
    simpa [dilFF, ofFlips, hF, hT] using h a b
  · refine Or.inr (Or.inl fun x => ?_)
    rcases x with ⟨a, b⟩
    simpa [dilFT, ofFlips, hF, hT] using h a b
  · refine Or.inr (Or.inr (Or.inl fun x => ?_))
    rcases x with ⟨a, b⟩
    simpa [dilTF, ofFlips, hF, hT] using h a b
  · refine Or.inr (Or.inr (Or.inr fun x => ?_))
    rcases x with ⟨a, b⟩
    simpa [dilTT, ofFlips, hF, hT] using h a b

#print axioms eq_ofFlips

/-- Punchline: exactly four reversible dilations of the identity on
    Bool × Bool, classified by two fiber flips. dil1 and dil2 are
    two of them. Not CPTP. Not dilations of collapse. -/
theorem four_reversible_dilations_of_report_identity :
    ((∀ x, dilFF.map x = dil1 x) ∧
      (∀ a b, dilTT.map (a, b) = dil2 (a, b))) ∧
      (dilFF.map ≠ dilFT.map ∧
        dilFF.map ≠ dilTF.map ∧
        dilFF.map ≠ dilTT.map ∧
        dilFT.map ≠ dilTF.map ∧
        dilFT.map ≠ dilTT.map ∧
        dilTF.map ≠ dilTT.map) ∧
      (∀ D : ReportIdDilation,
        (∀ x, D.map x = dilFF.map x) ∨
          (∀ x, D.map x = dilFT.map x) ∨
          (∀ x, D.map x = dilTF.map x) ∨
          (∀ x, D.map x = dilTT.map x)) :=
  ⟨⟨dilFF_is_dil1, dilTT_is_dil2⟩, four_maps_pairwise_unequal, eq_ofFlips⟩

#print axioms four_reversible_dilations_of_report_identity

end FableHilbertWalk20260819.H015DilationCount
